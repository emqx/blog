这个五月，eKuiper 处在 1.6.0 版本新功能开发早期阶段，产品功能开发主要包括 protobuf 编解码支持。针对用户多次提出的用拖拽方式编写数据处理规则需求，我们也在进行原型验证。v1.5.1 的 bug 修复也在进行中，预计于 6 月初发布。 

此外，作为边缘流式数据处理软件，eKuiper 还参与了中国信通院发起的《边缘流式数据处理技术能力要求》标准评估，通过后 eKuiper 将成为首个通过此标准认定的产品。 

## protobuf 编解码支持

目前 source 和 sink 关于编解码的配置属性 format 默认值为 JSON，用户可以通过新增的 protobuf 的选项选用 protobuf 的编解码能力。相比于 JSON，protobuf 编码的数据量更小，有利于节省云边之间传输的带宽。该功能目前已经开发完成但尚未发布，用户可以通过边缘源码的 v1.6.0 分支进行试用。

相比于无模式（schema）的 JSON 格式，protobuf 需要定义 proto 文件作为编解码的 schema。在使用 protobuf 格式之前，用户需要先注册 schema，并通过新增的 schemaId 属性，指定编解码选用的 schema。

#### Schema 管理

使用 REST API 注册，schema 内容可通过文件路径或者文本提供。

```
// POST /schemas
{
  "id":"fileName",
  "file":"http://myhost/files/abc.proto"
}
```

或者通过文本内容配置：

```
// POST /schemas
{
  "id":"schemaName",
  "content":"message Person {
    required string name = 1;
    required int32 id = 2;
    optional string email = 3;
  }"
}
```

无论何种方式，内容会被存储于 etc/schemas/protobuf。

#### Sink 中使用 protobuf

- format，用于指定使用的编码
- schemaId， 用于指定使用的 schema

```
{
  "mqtt":{
    "server":"tcp://127.0.0.1:1883",
    "topic": "result",
    "format":"protobuf",
    "schemaId":"schemaName.Person"    // protobuf的 ID分为两部分，前面为文件名，后面为message名
  }
}
```

#### Source 中使用 protobuf

FORMAT，支持 protobuf

SCHEMA_ID ，用于指定使用的 schema

```
CREATE STREAM demo() WITH (TYPE="NEURON", FORMAT="protobuf", SCHEMA_ID="schemaName.Person")
```

## 可视化拖拽编辑能力

之前 eKuiper 针对流式数据仅支持 SQL 形式编写数据处理规则，有一定门槛，不方便业务人员直接参与规则编写。为了进一步降低使用门槛，eKuiper 准备支持以可视化方式拖拽数据处理单元并进行简单编辑配置，最终将多个数据处理单元连接起来自动形成数据处理规则，方便更多人直接使用 eKuiper 进行业务处理。目前这个方案正在原型设计阶段。

![eKuiper 可视化拖拽编辑能力](https://assets.emqx.com/images/0b82c091c8cfb7d90f82f6436cf11293.png)

## 即将到来

下个月我们将完善可视化拖拽编辑，并合并到主分支中。另外，eKuiper 将优化 sink 出错之后的缓存机制，实现内存 + 磁盘的离线存储，并在错误恢复后顺序重发，以支持网络断开情况下更强的恢复能力，缓存更长时间的数据。
