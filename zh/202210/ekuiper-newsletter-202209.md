本月，eKuiper 处于 v1.7.0 的开发周期中，开发团队和社区的伙伴共同完成了一系列的新功能。我们初步实现了 Lookup Table（查询表）的支持，从而完善了流批结合的运算能力，例如实时数据补全的能力。另外，我们扩展和优化了数据集成，添加了 HTTP 推送源、Influx V2 sink；扩展了 EdgeX 源的数据格式支持。同时，本月底我们也发布了 1.6.2 版本，主要是 Bug 修复和管理控制台的增强。

## 流批结合计算

并非所有的数据都会经常变化，即使在实时计算中也是如此。在某些情况下，你可能需要用外部存储的静态数据来补全流数据。例如，用户元数据可能存储在一个关系数据库中，流数据中只有实时变化的数据，需要连接流数据与数据库中的批量数据才能补全出完整的数据。新的版本中，eKuiper 添加了新的 Lookup Table 概念，用于绑定外部静态数据，可以在规则中与流数据进行连接，实现流批结合的运算。

使用查询表时，通常有三个步骤。

1. 创建数据流。该步骤与之前创建普通数据流的过程无异。

   `CREATE STREAM demoStream() WITH (DATASOURCE="demo", FORMAT="json", TYPE="mqtt")`

2. 创建查询表。创建表时，增加了新的属性 KIND，用于指定是否为查询表。此处表的源类型为 SQL，需要在 etc/sources.sql.yaml 中配置数据库连接的相关信息。DATASOURCE 属性指定了要连接的物理表名。

   `CREATE TABLE myTable() WITH (DATASOURCE=\"myTable\", TYPE=\"sql\", KIND=\"lookup\")`

3. 创建规则，连接流和表，并进行计算。

   `SELECT * FROM demoStream INNER JOIN myTable on demoStream.id = myTable.id`

与之前版本支持的动态表不同，查询表不需要在内存中存储表数据的快照，而是在连接时直接查询外部数据，从而可支持更大量的静态数据的查询。查询表提供了可配置的数据内存缓存的支持，提高查询效率。

查询表本身需要有存储能力，因此并非所有数据源都可作为查询表类型。目前，我们适配或添加了以下几种查询源（source)：

- SQL
- Redis
- Memory ：配合规则流水线，可将别的规则的历史结果作为查询源使用

此外，原生插件中增加了 LookupSource 接口，供用户自定义查询源扩展。

## 使用 HTTP 推送数据流

新增了 httppush source ，它作为一个 HTTP 服务器，可以接收来自 HTTP 客户端的消息。所有的 HTTP 推送源共用单一的全局 HTTP 数据服务器。每个源可以有自己的 URL，这样就可以支持多个端点。HTTP 推送源的配置分成两个部分：全局服务器配置和源配置。全局服务器配置位于 `etc/kuiper.yaml` 中，可配置服务器的监听地址和端口，以及 HTTPS 的相关证书配置。源配置位于 `etc/sources/httppush.yaml` 中，用于配置推送的 HTTP 方法。创建数据流时，可通过 DataSource 属性，配置数据流监听的 URL 端点，从而区分各个数据流的推送 URL。

```
CREATE STREAM httpDemo() WITH (DATASOURCE="/api/data", FORMAT="json", TYPE="httppush")
```

在此例中，DataSource 配置为 `/api/data`。假设用户使用默认服务器配置，则推送到 `http://localhost:10081/api/data` 中的数据将形成数据流 httpDemo。后续可创建规则对该数据流进行处理。

## InfluxDB 2.x Sink

之前的版本中，eKuiper 提供了 InfluxDB sink，支持写入数据到 1.x 版本的 InfluxDB 中。然而，由于 InfluxDB 2.x 的 API 不兼容 v1，原有的 sink 不支持写入到 v2 中。新的版本中，感谢社区用户 @elpsyr 提供了 InfluxDB 2.x sink 插件，我们实现了写入 InfluxDB 2.x 的支持。

## 处理 EdgeX Foundry 图像数据

EdgeX Foundry 中使用 `application/cbor` 格式传输二进制数据，例如图像数据。新的版本中，我们提供了对该格式的支持，使得用户使用 eKuiper 处理 EdgeX 中的图像数据成为可能。Edge X Camera 服务采集到图像数据，可通过 eKuiper 进行预处理、AI 推理、后处理等，从而实现使用 SQL 规则完成 AI 图像处理流水线的功能。

## 即将到来

下个月我们将继续进行 v1.7.0 的开发，计划的新功能包括连接资源管理、分流计算等。预计将在 10 月底完成发布。
