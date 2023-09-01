当用户向 eKuiper 中注册规则并运行以后，eKuiper 便会开始持续订阅该规则所属的流。当上游的流向 eKuiper 发送数据时，eKuiper 便会将数据包进行解析，并按照规则所定义的运算规则进行运算，并将结果汇入到指定的下游阶段。而在这一过程中，数据包的解析对于 CPU 的运算则是不容忽视的一部分开销。在本篇文章中，我们将介绍如何通过预定义上游流的 schema，使 eKuiper 在上述过程中在不降低吞吐的前提下，降低整体的 CPU 运算开销。

## 通过 Schema 预检验数据

原来的 eKuiper 的 Stream schema 主要作用在于验证流每一列的属性是否正确。在这里我们看一个例子:

```
my_stream (id bigint, name string, score float)WITH ( datasource = "topic/temperature", FORMAT = "json", KEY = "id");
```

在这个例子中，我们定义 my_stream 这个流有 id、name 和 score 三个列，每一个列则各自定义了该列的属性。然后我们向 eKuiper 中注册以下 SQL 作为运行规则:

```
select id, name from my_stream where score > 60
```

当上述规则注册进 eKuiper 后，eKuiper 就会根据该 SQL 进行算子的解析与运行，并向 my_stream 流持续订阅消息。  

假如我们在 SQL 规则中出现了 schema 中不存在的列，那么 eKuiper 则会在 SQL 解析阶段发现该问题并返回验证错误的信息，如以下例子:

```
select id, name from my_stream where email = 'mock'
```

则 eKuiper 在验证规则时会报如下错误:

```
unknown field email
```

同样的，eKuiper 在解析数据时也会检查对应的 column 与所注册的 column schema 信息是否一致。对于上述例子，对于下列数据时，eKuiper 则会发现 name 列所携带的信息列属性与其注册的属性并不一致，而 eKuiper 此时则会进行将该列强转为注册属性。

```
{
    "id": 1,
    "name": 12,
    "score": 75
}
```

## 解析 Schemaless 数据

当 stream 没有注册对应的 schema 时，即 schemaLess stream，eKuiper 则会使用 golang 的标准 std json 进行解析，如下:

```
func (c *Converter) Decode(b []byte) (interface{}, error) {
    var r0 interface{}
    err := json.Unmarshal(b, &r0)
    if err != nil {
       return nil, err
    }
    return r0, nil
}
```

这么做则会将对应数据包中的所有数据都解析并合并进一个 `map[string]interface{}` 的结构下。如果该数据包中大部分列并不参与计算，那么这部分解析计算的开销便被浪费了，并且消耗也不容忽视。  

我们在 eKuiper 中注册以下规则, 并且向对应的流发送 7000 qps 消息数据，每一条消息都包含了 100 个 column，从 a1 一直到 a100，每个 column 都携带了 10 - 20 长度的字符串数据。

```
select a1,a2,a3,a4,a5 from my_stream;
```

当规则开启运行后，通过 grafana 监控面板我们可以看到，在 sink 端保持 7000 qps 的同时，eKuiper 整体的 CPU 消耗在 200% 左右，当我们进行 CPU 火焰图抓取的时候，我们可以看到绝大部分 CPU 开销都被花费在了 `json.unmarshal` 上。

![图片.png](https://assets.emqx.com/images/c90f6457d741ab2355089146524fdaaf.png)
![图片.png](https://assets.emqx.com/images/2f971e3bb33190637d21a250d650f702.png)

### 优化思路

通过该 SQL 规则我们可以发现，虽然该 stream 每次消息包内都会携带 100 个 column，但实际上我们仅仅需要 SQL 中被声明的 5 个 column，其余 95 个 column 的信息则不需要参与到计算中。如果我们能在解析数据时，识别出哪些 column 是需要参与计算的，哪些 column 是不需要参与计算的，而对于不需要参与计算的 column 而言，我们则在解析数据时直接跳过，那么就不会再浪费这上面浪费 CPU 开销。那么，我们该如何得到必须要进行解析的 column 呢？

### 预定义 Schema

通过 schema ，我们可以很容易的将需要参与解析的 column 范围缩小。当消息包中的 column 并没有在被 schema 中所定义时，那么我们则可以直接跳过该 column 的解析, 如以下这个例子:

```
create stream my_stream '(a1 string, a2 string, a3 string) WITH (FORMAT="JSON", DATASOURCE="test")'
```

```
{
    "a1": "sdafasdf",
    "a2": "zxczxczx",
    "a3": "weqeqwee",
    "a4": "sdfsdfsf",
    "a5": "dsafsadf"
}
```

对于上述例子，由于只有 a1,a2,a3 3个 column 在 schema 中被定义了，所以对于 a4,a5 这两个 column 则不需要被参与到数据包的解析中。

### 列裁剪

虽然 schema 可以帮助我们跳过解析没有被定义的列，然而对于同一个 stream 来说，在不同的 SQL 规则下，所需要用到的列也会是不同的，我们通过以下 2 条 SQL 的例子来详细说明:

```
select a1,a2 from my_stream
```

```
select a2,a3 from my_stream
```

还是以上述的 stream schema 和数据包为例，虽然按照 schema 定义我们只需要解析 a1,a2,a3 并且跳过了多余的解析 column 步骤，但是对于第一条 SQL 规则而言，它只用到了 a1,a2 两个 column，对于第二条 SQL 而言，它只用到了 a2,a3 两个 column。对于这两条 SQL 而言，解析 a1,a2,a3 这三条 column 都分别解析了其他不被用到的、多余的 column。所以我们需要通过列裁剪这个优化，进一步从 schema 信息内解析出该规则中哪些 column 被使用到了，哪些 column 没有被使用到，对于没有被使用到的 column，我们则需要将其从待解析 column 中裁剪掉，从而保证解析消息包时只解析必要的列。

### fastjson

当我们得到必要的解析列信息时，下一步则是如何从消息包中解析必要的数据。好在 golang 的社区中已经有人提供了相关的库，即 https://github.com/valyala/fastjson%E3%80%82

 通过 golang fastjson，我们可以在解析消息包时，将必要的 column 和其事先定义好的 schema 信息进行解析，这里我们以 fastjson 的 example 为例，来了解它是如何工作的:

```
        var p fastjson.Parserv, err := p.Parse(`{                
             "str": "bar",                
             "int": 123,                
             "float": 1.23,                
              "bool": true,                
              "arr": [1, "foo", {}]        
        }`)
        if err != nil {
                log.Fatal(err)
        }
        fmt.Printf("foo=%s\n", v.GetStringBytes("str"))
        fmt.Printf("int=%d\n", v.GetInt("int"))
        fmt.Printf("float=%f\n", v.GetFloat64("float"))
        fmt.Printf("bool=%v\n", v.GetBool("bool"))
        fmt.Printf("arr.1=%s\n", v.GetStringBytes("arr", "1"))
```

而在 eKuiper 中，我们也使用了 fastjson 来作为我们的 json 解析器，我们会传入所需要的 column 与其对应的 schema 信息，并通过 fastjson 帮助我们解析必要的数据。如果你想要了解 eKuiper 是如何使用 fastjson 的，可以通过搜索 `FastJsonConverter` 来了解源码。

### 优化结果

最后，当我们通过将 schema 信息，列裁剪，fastjson 这些方案和工具都集成优化进 eKuiper 的数据解析流程中后，我们对于之前的 benchmark 重新进行部署与测试，得到了新的结果。  

首先，我们需要定义 stream 的 schema 信息:

```
create stream my_stream '(a1 string, a2 string,a3 string,a4 string, a5 string) WITH (FORMAT="JSON", DATASOURCE="test")'
```

然后我们向 eKuiper 中再次注册之前的 SQL 规则:

```
select a1,a2,a3,a4,a5 from my_stream;
```

接着我们再次以 7000 qps 的速率让上游向 eKuiper 发送消息，最后我们得到了如下的结果:

当规则开启运行后，通过 grafana 监控面板我们可以看到，在 sink 端保持 7000 qps 不变的同时, CPU 开销从 200% 降低到了 150%。通过抓取 CPU 火焰图，我们发现解析数据所占据的 CPU 开销比重和之前相比有了明显的降低。

![图片.png](https://assets.emqx.com/images/0602749d38551d6800957f42843942a4.png)
![图片.png](https://assets.emqx.com/images/60e57ef2d938b8973a7f1234ae8fb9f6.png)

## 总结与使用建议

通过上述例子，我们可以发现定义 stream schema 可以有效帮助我们减少在数据解析时的冗余开销，从而降低 CPU 压力。如果你的场景中，消息包所携带数据和 SQL 中所使用的数据差距较大，那么你可以通过给该 stream 定义 schema 的方式，从而降低这部分的 CPU 开销压力。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
