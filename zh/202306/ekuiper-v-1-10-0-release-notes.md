经过为期两个月的开发，我们很高兴地宣布 eKuiper 1.10.0 现已正式发布！

作为一个里程碑版本，eKuiper 1.10.0 升级了基础依赖的版本，如 Go 语言版本升级到 1.20、EdgeX 支持最新的大版本 Minnesota（v3）等。我们也一如既往地完善提升产品的表达能力、连接能力和易用性，同时注意保持轻量小巧以适应边缘部署。

最新版本的新特性与改进优化主要有以下几个方面：

- 规则管理：规则可计划执行时间，一定程度上实现了规则边缘自治。
- 连接生态：添加/完善了更多的数据源和目标，包括 EdgeX v3、Kafka Sink、文件 Sink 等。Sink/Source 支持了更高效的数据变换，如数据抽取、批量和压缩等。以帮助用户更好地连接各种数据源和目标，适应更复杂的数据结构。
- 表达能力：添加了更多的函数和语法，如数组和对象处理、外部状态支持、数组动态下标语法等，助力用户实现更复杂的数据处理。

详细更新内容请查看[更新日志](https://github.com/lf-edge/ekuiper/releases/tag/1.10.0)。

## 规则定时执行

某些场景下，用户数据可能是周期性的，为了节省运行资源，用户希望在没有数据的情况下停止规则，而只在指定的时间段启用规则。用户需要规则自动周期性执行，如每天凌晨执行一次、每周执行一次等。用户可以采用 eKuiper 的 API 进行规则的手工启停，但是在边缘大规模部署的情况下，手工启停是不可行的，边缘规则自治迫在眉睫。因此，我们在新版本的规则中添加了定时执行的功能，用户可以指定规则的定时执行时间，规则会自动在指定的时间段启动和停止，无需人工干预。

规则的 option 添加了两个参数，分别是 `cron` 和 `duration`。

- `cron` 参数指定了规则的定时执行时间，格式遵循 cron 表达式的格式，如 `0 0 0 * * *` 表示每天凌晨 0 点执行一次。
- `duration` 参数指定了规则的执行时间，采用 duration string 格式，包含数字和时间单位，如 `1m` 表示执行 1 分钟。

例如，以下的规则通过 options 里的参数定义了每两分钟执行一次，每次执行 1 分钟。

```
{
  "id": "ruleSchedule",
  "sql": "SELECT * FROM demo;",
  "options": {
    "cron": "*/2 * * * *",
    "duration": "1m"
  },
  "actions": [{
    "mqtt":  {
      "server": "tcp://broker.emqx.io:1883",
      "topic": "result/rule"
    }
  }]
}
```

> *注意*，duration 不应该超过两次 cron 周期之间的时间间隔，否则会引起非预期的行为。

计划任务规则的增删改查和状态查询与普通的规则一致，可以通过 API 或者 CLI 进行操作。计划任务执行时，规则为 `Running` 状态。若计划任务执行时间到期，规则会自动停止等待下次调度，状态变为 `Stopped: waiting for next schedule.`。通过 Stop 命令停止计划任务，规则将立即停止而且从调度器中移除。

## 灵活适配数据源和目标

eKuiper 是 EdgeX Foundry 默认的规则引擎实现。即将发布的 EdgeX Minnesota (v3) 是一个重要版本，eKuiper 也同步进行了支持和更新 。同时，我们也添加了更多的数据源和目标，如 Kafka Sink、文件 Sink 等。这些数据源和目标的支持，使得 eKuiper 可以更好地连接各种数据源和目标，更方便地接入各种数据基础设施。

### EdgeX v3 支持

EdgeX v3 是 EdgeX Foundry 的下一个重要版本，eKuiper 1.10.0 版本已经支持了 EdgeX v3。eKuiper 的 EdgeX Source 和 Sink 已更新适配，用户已有的规则可以无缝迁移到 EdgeX v3。

同时，在我们的测试中，1.10 版本的 eKuiper 仍然可以兼容 EdgeX v2，用户可以根据自己的需要选择 EdgeX v2 或者 EdgeX v3。

需要注意的是，由于 EdgeX 中已移除 ZeroMQ 总线的支持，我们也移除了 eKuiper 中的 EdgeX Source/Sink 的 zmq 协议支持。采用默认 Redis 总线或 MQTT 总线的用户不受影响。

### 更强大的文件 Sink

文件系统属于操作系统的内核，无需任何的外部系统依赖，因此具有很高的适用性，几乎可以应用于任何的部署环境，特别是资源受限的系统中。采用文件 Sink，我们可以在安全性要求较高或没有网络的环境中，作为数据批量的持久化的方式，然后再通过其他手段将数据传输到其他的系统中，实现网闸穿透。另外，我们也可以在带宽较低的环境中，将数据先批量写入到文件后再压缩传输，从而实现更大的压缩率，减少带宽消耗。

延续上个版本对文件连接器的优化，新的版本中，文件 Sink 支持了更多的文件类型，如 csv、json 和 lines 等。同时，文件 Sink 支持了更多的数据变换，如数据抽取、批量和压缩等，有利于更多应用的适配。另外，文件写入支持自定义切分策略，支持更大的数据量和更方便的管理。

新版本 File Sink 的主要亮点有：

- 支持多种文件格式，且写入的文件可由 File source 读取，实现数据的循环传输。
- 支持多种切分策略：
  - 按时间切分，支持设置文件切分的间隔时间
  - 按消息数目切分
  - 切分文件名自动添加时间戳，避免文件名重复，并可设置时间戳的添加位置
- 支持写入多文件，即动态文件名。根据消息内容，可以将消息写入到不同的文件中，实现数据的分流。
- 写入性能优化，支持批量写入，提升写入效率。多文件写入时，支持并发写入，共用定时器，提升写入效率。
- 支持压缩，支持 gzip 和 ztsd 两种压缩方式。

所有这些能力都可通过属性进行配置。下面是一个使用文件 Sink 的规则的示例。其中，path 采用了动态文件名，即根据消息内容，将消息写入到不同的文件中。以下的示例中，文件类型设置为 `csv`，而 `rolling` 开头的属性则配置了文件切分的策略。compression 配置了压缩方式，采用 gzip 压缩。详细配置说明请查看产品文档。

```
{
  "id": "fileSinkRule",
  "sql": "SELECT * from demo ",
  "actions": [
     {
      "file": {
        "path": "{{.device}}_{{.ts}}.csv.gzip",
        "format": "delimited",
        "delimiter": ",",
        "hasHeader": true,
        "fileType": "csv",
        "rollingCount": 10,
        "rollingInterval": 0,
        "rollingNamePattern": "none",
        "compression":"gzip"
      }
    }
  ]
}
```

### Kafka Sink

Kafka 是一个分布式的消息系统，具有高吞吐量、高可用性、可伸缩性和持久性等特点。新版本中添加了 Kafka Sink 可以将 eKuiper 的数据写入到 Kafka 中，实现 eKuiper 与 Kafka 的无缝对接。使用示例如下所示：

```
{
  "id": "kafka",
  "sql": "SELECT * from demo",
  "actions": [
    {
      "kafka":{
        "brokers": "127.0.0.1:9091",
        "topic": "sample_topic",
        "saslAuthType": "none"
      }
    }
  ]
}
```

### 数据库支持优化

新版本中对 SQL source/sink 插件进行了一些优化。主要包括：

1. 更新 ClickHouse 驱动，测试 ClickHouse 的支持。
2. 支持达梦数据库。
3. 支持连接池配置，提升数据库连接的效率。

用户可在配置文件 etc/kuiper.yaml 中或通过环境变量，配置 sql/maxConnections 属性，指定数据库连接池的最大连接数，避免连接数过多导致的性能问题。示例如下所示：

```
  sql:
    # maxConnections indicates the max connections for the certain database instance group by driver and dsn sharing between the sources/sinks
    # 0 indicates unlimited
    maxConnections: 0
```

## Sink 数据变换

用户的数据可能会有嵌套结构，例如 Neuron 接入的数据中通常包含一些元数据，payload 里的 values 字段才是用户需要的数据。另外，使用复杂 SQL 语句进行数据处理时，可能 SELECT 子句中会定义一些计算的中间结果，并不需要全部输出到 Sink 端。在这种情况下，Sink 端需要对数据再进行变换或者格式化。数据模板是一种常用的方式，它功能强大，支持各种格式化。然而它需要用户有一定的编写模板能力，同时运行性能较差。

新版本中，Sink 端支持了更多的常用的数据变换，包括数据抽取，批量发送的相关属性，并扩展到大部分的 Sink 类型中。在一些常用的简单数据变换中，用户配置参数即可，减少了用户的编写模板的工作量，同时提升了运行效率。

### 批量发送

默认情况下，Sink 为每个事件产生一条数据。但是如果数据吞吐量很大，这样会有一些问题，例如 IO 开销大；若压缩的话，压缩比低；发送到云端的网络开销大等。同时，发送速率快可能增加了云端处理压力。为了解决这些问题，新版本中支持了 MQTT Sink 中的批量发送功能。

批量发送的原理是，Sink 会采用一定的策略对数据进行缓存，然后一次性发送到云端。用户可通过配置参数 `batchSize` 和 `lingerInterval` 来控制批量发送的数据量和时间间隔。示例如下所示：

```
{
    "id": "batch",
    "sql": "select a,b from demo",
    "actions": [
       {
        "log": {
        },
        "mqtt": {
          "server": "tcp://broker.emqx.io:1883",
          "topic": "devices/messages",
          "lingerInterval": 10000,
          "batchSize": 3
        }
      }
    ]
}
```

该示例中，当数据量达到 3 条或者累积 10 秒后，Sink 才会发送一次数据。用户可根据自己的需求，调整这两个参数。

### 数据抽取

在使用中间数据或者计算数据与写入数据格式不一致时，我们需要在 Sink 端抽取出需要的数据。新版本中，所有 Sink 添加了两个通用参数 `fields` 和 `dataField`。 这两个参数在之前的数据存储相关 Sink，包括 SQL、Redis、InfluxDB 等中已经支持。因为在数据写入中，目标数据库通常有严格的列定义，而 SQL SELECT 语句不一定能匹配列，往往有冗余选择的字段。在其他的 Sink 中，也会有这样的数据抽取的需求。新版本中，这两个属性扩展到了 MQTT、Kafka、File 等 Sink 中。其中，`dataField` 参数用于指定表示数据的字段以区分于表示元数据等其他数据的字段，例如 `dataField: values`。`fields` 参数用于指定需要输出的字段，从而可以完全匹配目标系统需求，例如 `fields: ["a","b"]`。

示例1：提取 Neuron 数据的 values 部分输出。如下所示，通过配置 dataField 属性来提取嵌套的数据：

```
{
  "id": "extract",
  "sql": "SELECT * FROM neuronStream",
  "actions": [
    {
      "mqtt": {
        "server": "tcp://broker.emqx.io:1883",
        "topic": "devices/messages",
        "dataField": "values"
      }
    }
  ]
}
```

示例2：提取需要的字段，忽略中间计算结果的部分字段输出。如下所示，通过配置 fields 属性来提取指定的字段：

```
{
  "id": "extract",
  "sql": "SELECT temperature, lag(temperature) as lt, humidity FROM demo WHERE lt > 10",
  "actions": [
    {
      "mqtt": {
        "server": "tcp://broker.emqx.io:1883",
        "topic": "devices/messages",
        "fields": ["temperature","humidity"]
      }
    }
  ]
}
```

在这个示例中，SQL 语句中的 `lag(temperature) as lt` 会产生一个中间计算结果，方便在 WHERE 字段中进行过滤，简化 SQL 编写。但是在 Sink 端，我们只需要 `temperature` 和 `humidity` 两个字段，因此通过配置 `fields` 属性来指定需要输出的字段。

这两个属性可以同时使用，也可以配合 DataTemplate 使用，完成更复杂的数据变换。当 3 个属性都配置之后，会先执行 DataTemplate，然后再执行 dataField，最后执行 dataField 的数据抽取。

## 数组和对象处理

SQL 语法最初是针对关系数据库设计的，而数据库中的复合数据类型较少，因此对于数组和对象的处理能力有限。在 IoT 场景中，接入的数据格式多为 JSON，嵌套的复合数据类型是一等公民。eKuiper SQL 在最初就加入了对嵌套数据的访问能力。然而，对于其中的更深入的数据变换仍然有很多需求尚未得到满足。新版本中，我们对数组和对象的处理能力进行了增强，包括数组数据转为多行、数组和对象处理函数等。

### 支持数据源的数组 payload

当数据源使用 JSON 格式时，之前的版本只支持 JSON 对象的 payload，新版本中支持了 JSON 数组的 payload。而且，用户无需配置，系统会自动识别 payload 类型。

例如，使用 MQTT Source 新版中可以接入数组类型数据：

```
[
    {"temperature":23},
    {"temperature":24},
    {"temperature":25}
]
```

当接收到数组数据时，数据会拆分成多条数据进行处理，每条数据包含一个数组元素。例如，上述数据会被拆分成三条数据。此后，处理过程与普通的 JSON 对象数据一致。

### 数组数据转为多行

有些数据源中传入的是批量的数据，但又有一些公共的元数据，因而整体格式仍然是一个 JSON 对象，例如下面的数据。这种数据格式在 HTTP 服务的返回值里尤其常见。

```
{
    "device_id": "device1",
    "data": [
        {"temperature":23},
        {"temperature":24},
        {"temperature":25}
    ]
}
```

这样一条数据在 eKuiper 中是作为**单行**的数据来处理的。而逻辑上，用户需要的是多行的数据。在新版本中，我们增加了一种新的函数类型：多行函数，用于将单行数据转为多行处理。同时，我们增加了唯一的多行函数：`unnest`。用于展开数组列为多行。

unnest | unnest(array) | 参数列必须是一个 array 对象。该函数将参数 array 展开成多行作为结果返回。如果 array 对象中每一个子项为 map[string]interface{} 对象，则该子项会作为列在返回的行中。

嵌套数据可以作为多行处理，得到多个输出结果。例如上述数据可以得到三条输出结果。

**用法示例**

创建流 demo，并给与如下输入。

```
{"a": [1,2], "b": 3} 
```

获取 unnest 结果的规则:

```
SQL: SELECT unnest(a) FROM demo
___________________________________________________
{"unnest":1}
{"unnest":2}
```

获取 unnest 结果与其他列的规则:

```
SQL: SELECT unnest(a), b FROM demo
___________________________________________________
{"unnest":1, "b":3}
{"unnest":2, "b":3}
```

创建流 demo，并给与如下输入。

```
{"x": [{"a": 1,"b": 2}, {"a": 3,"b": 4}], "c": 5} 
```

获取 unnest 结果与其他列的规则:

```
SQL: SELECT unnest(x), b FROM demo
___________________________________________________
{"a":1, "b":2, "c": 5}
{"a":3, "b":4, "c": 5}
```

### 数组和对象处理函数

新版中通过函数的形式，我们完善了对数组和对象的处理能力。例如，获取列表中最大值的函数 `array_max`，获取列表中最小值的函数 `array_min`，获取列表中元素个数的函数 `array_length`，获取列表中元素的函数 `array_element`，获取对象中元素的函数 `object_element`。目前已支持的函数请查看 [函数文档](https://ekuiper.org/docs/zh/latest/sqls/functions/array_functions.html)。

接下来的版本中，我们仍将持续增强对数组和对象的处理能力。

### 嵌套结构访问语法糖

初次接触 eKuiper 的用户最常询问的问题可能就是如何访问嵌套结构的数据。在标准的 SQL 中并没有定义这种语法。在编程语言中，我们通常使用点号（.）访问嵌套数据。然而，在 SQL 中，点号表示的是表名。因此，我们扩展了 SQL 语法，使用箭头符号（->）访问内嵌结构。但是这个语法并不直观，对于新手有学习成本。

在新版中，我们增加了嵌套结构访问语法糖，用于简化嵌套结构的访问。在没有歧义的情况下，用户可以使用点号访问嵌套结构。例如，对于下面的数据：

```
{
    "a": {
        "b": {
            "c": 1
        }
    }
}
```

可以在语句中可以直接使用 `a.b.c` 访问嵌套结构。原来的箭头符号也仍然兼容支持，例如 `a->b->c`。

## 外部状态支持

eKuiper 是有状态的流式处理引擎，状态主要是内部使用，包括窗口状态、分析函数状态等。之前的版本中，我们通过 Table 支持较粗粒度（基于行）的外部状态访问。在新版本中，我们增加了基于 Key（列）的外部状态存储和访问能力。通过外部状态访问，可以实现更多的功能，例如动态阈值和动态开关状态。用户可以轻松实现与第三方应用的状态共享，从而实现协同工作。

外部状态存储可与系统内部状态存储共存，也可以单独使用。外部状态存储同样支持 SQLite 或者 Redis。基于 KV 的 Redis 更加适合存储外部状态。在配置文件 etc/kuiper.yaml 中，我们可以配置外部状态存储的类型。

```
store:
  #Type of store that will be used for keeping state of the application
  extStateType: redis
```

- 状态访问：假设第三方应用已经写入一个缓存数据 `$device1$temperatureL`: "20"。在 SQL 中，我们可以通过 `get_keyed_state` 函数访问外部状态。例如，`get_keyed_state(\"$device1$temperatureL\", \"bigint\", 0) as temperatureL` 从而让外部状态参与计算。
- 状态写入：假设我们需要将计算结果写入 Redis 外部状态，我们可以使用 Redis Sink。新版本中，Redis Sink 支持一次写入多个 key-value 对。在以下示例中，通过配置 `keyType` 为 `multiple`，我们可以一次写入多个 key-value 对。也可以通过 `field` 配置项指定写入的字段名。

```
{
  "id": "ruleUpdateState",
  "sql":"SELECT status as `$device1$status`,temperatureH as `$device1$temperatureH`,temperatureL as `$device1$temperatureL` FROM stateStream",
  "actions":[
    {
      "redis": {
        "addr": "{{localhost}}:6379",
        "dataType": "string",
        "keyType": "multiple",
        "sendSingle": true
      }
    }
  ]
}
```

## SQL 语法更新

除了前文提到的一些 SQL 语法更新外，新版本还包括以下 SQL 语法更新：

### 获取当前规则

添加了 `rule_id()` 函数，可以在获取当前规则的 ID，方便用户回溯数据产生的规则。

### 数组动态下标

新版本中数组下标可用表达式，实现动态索引。例如，`SELECT a[start] FROM stream`，其中 `start` 可以是一个 field，值为变量；下标可使用任意表达式。

动态化可实现之前版本中难以完成的非常灵活的数组操作。例如，流水线上有多个传感器，其数据采集为数组。物件进入流水线后，根据流水线和速度，可以计算出物件在流水线上的位置，从而确定物件的传感器数据。这个计算过程可以通过数组下标动态计算实现。

### 延迟执行函数

新版本中，我们增加了延迟执行函数。这些函数在执行时，会延迟一段时间。例如，`delay` 函数会延迟一段时间后，返回输入的值。

若数据目的有流量限制，使用该函数可以实现消峰填谷的作用。

## Graph API 增强

新版本中，我们增加了 Graph API 访问已定义的流和查询表的支持。同时，在 JoinOp 支持流和查询表。我们也改进了 Graph API 验证信息，使得用户更容易定位错误。Graph API 乃至基于其上的可视化编辑器可实现更多的数据处理能力。

用户需通过 `Create Stream` 和 `Create Table` 定义流和查询表。在 Graph API 规则中，可通过 `sourceName` 属性指向已定义的流和查询表。例如，以下规则中，`demo` 和 `alertTable` 分别指向已定义的流和查询表。

```
{
  "id": "ruleAlert",
  "graph": {
    "nodes": {
      "demo": {
        "type": "source",
        "nodeType": "mqtt",
        "props": {
          "sourceType": "stream",
          "sourceName": "demo"
        }
      },
      "alertTable": {
        "type": "source",
        "nodeType": "memory",
        "props": {
          "sourceType": "table",
          "sourceName": "alertTable"
        }
      },
      "joinop": {
        "type": "operator",
        "nodeType": "join",
        "props": {
          "from": "demo",
          "joins": [
            {
              "name": "alertTable",
              "type": "inner",
              "on": "demo.deviceKind = alertTable.id"
            }
          ]
        }
      },
      "log": {
        "type": "sink",
        "nodeType": "log",
        "props": {}
      }
    },
    "topo": {
      "sources": ["demo", "alertTable"],
      "edges": {
        "demo": ["joinop"],
        "alertTable": ["joinop"],
        "joinop": ["log"]
      }
    }
  }
}
```

## 依赖更新

除了 EdgeX 相关依赖之外，eKuiper 还进行了如下的依赖更新：

- Go 语言版本更新到 1.20
- SQLite 依赖切换到纯 Go 实现的版本
- Redis 依赖 GitHub - redis/go-redis: Redis Go client 更新到 v9
- 移除默认的 zeroMQ 依赖
- 更新其他依赖库

## 特别鸣谢

eKuiper 1.10 版本的开发得到了社区的大力支持。

在此特别感谢以下贡献者：

- @carlclone：贡献了 Kafka sink 的实现以及多种压缩/解压算法的实现。
- @wangxye: 贡献了多个数组/对象函数。

感谢开发团队和所有贡献者的努力和付出！Have fun with eKuiper！



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
