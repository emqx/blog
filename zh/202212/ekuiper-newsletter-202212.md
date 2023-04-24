本月 eKuiper 团队继续专注于 1.8.0 版本新功能的开发。我们重构了外部连接（source/sink) 的格式机制，更加清晰地分离了连接、格式和 Schema，同时支持了格式的自定义；受益于新的格式机制，我们大幅完善了文件源（file source）的能力，支持定时监控文件系统及各种格式的文件，并且采用流的方式消费文件系统数据；最后，我们增加了完整数据包括规则和配置的导入导出功能，支持节点的迁移。另外，我们也修复了一些问题，并发布到 1.7.x 版本中。

本月的版本发布包括：

- [v1.8.0-alpha.3](https://github.com/lf-edge/ekuiper/releases/tag/1.8.0-alpha.2)：包含 1.8.0 已开发完成的新功能
- [v1.7.4](https://github.com/lf-edge/ekuiper/releases/tag/1.7.4)：包含 bug fixes
- [v1.7.5](https://github.com/lf-edge/ekuiper/releases/tag/1.7.5)：包含 bug fixes


## 连接格式优化和自定义：序列化和 Schema

eKuiper 通过 source/sink 与外部系统进行连接、读入或写出数据。以 source 为例，每种类型的 source 读取数据时都需要经过连接（connect）和序列化（serialization）两个步骤。例如，MQTT source，连接意味着遵循 MQTT 协议连接 broker，而序列化则是将读取到的数据 payload 解析成 eKuiper 内部的 map 格式。

### 连接和序列化

此前，连接和序列化通常在 source 内部实现，因此当用户需要解析自定义格式时，即使连接协议是 MQTT 等已支持协议，仍然需要编写完整的 source 插件。新的版本中，格式和 source 类型进一步分离，用户可以自定义格式，而各种格式可以与不同的连接类型结合使用。自定义格式的编写方法请参考[格式扩展](https://ekuiper.org/docs/zh/latest/guide/serialization/serialization.html#格式扩展)。

例如，创建 MQTT 类型的数据流时可定义各种不同的 payload 格式。默认的 JSON 格式：

```
CREATE STREAM demo1() WITH (FORMAT="json", TYPE="mqtt", DATASOURCE="demo")
```

MQTT 类型的数据流使用自定义格式，此时 MQTT 的 payload 中的数据应当使用自定义的格式：

```
CREATE STREAM demo1() WITH (FORMAT="custom", SCHEMAID="myFormat.myMessage", TYPE="mqtt", DATASOURCE="demo")
```

### Schema

此前 eKuiper 支持在 Create Stream 的时候指定数据结构类型等。然而该方式有几个问题：

- 额外性能消耗。当前的 Schema 没有与数据原本的格式 Schema 关联，因此在数据解码之后，需要再额外进行一次 validation/转换；而且该过程基于反射动态完成，性能较差。例如，使用 Protobuf 等强Schema 时，经 Protobuf 解码之后的数据应当已经符合格式，不应再进行转换。
- Schema 定义繁琐。同样无法利用数据本身格式的 Schema，而是需要额外配置。

新的版本中，Stream 定义时支持逻辑 Schema 和格式中的物理 Schema 定义。SQL 解析时，会自动合并物理 Schema 和逻辑 Schema，用于指导 SQL 的验证和优化。同时，我们也提供了 API，用于外部系统获取数据流的实际推断 Schema。

```
GET /streams/{streamName}/schema
```

### 格式列表

新版本中，支持的格式扩展到如下几种。部分格式包含内置的序列化；部分格式，例如 Protobuf 既可以使用内置的动态序列化方式也可以由用户提供静态序列化插件以获得更好的性能。在 Schema 支持方面，部分格式带有 Schema，其中自定义格式也可以提供 Schema 实现。

| 格式      | 序列化                          | 自定义序列化 | Schema     |
| :-------- | :------------------------------ | :----------- | :--------- |
| json      | 内置                            | 不支持       | 不支持     |
| binary    | 内置                            | 不支持       | 不支持     |
| delimiter | 内置，必须配置 `delimiter` 属性 | 不支持       | 不支持     |
| protobuf  | 内置                            | 支持         | 支持且必需 |
| custom    | 无内置                          | 支持且必需   | 支持且可选 |


## 文件源

之前版本的文件源主要用于创建 Table，对流式处理的支持不够完善。新的版本中，文件源也支持作为用作流，此时通常需要设置 `interval` 参数以定时拉取更新。同时增加了文件夹的支持，多种文件格式的支持和更多的配置项。

新版本中支持的文件类型有：

- json：标准的 JSON 数组格式文件。如果文件格式是行分隔的 JSON 字符串，需要用 lines 格式定义。
- csv：支持逗号分隔的 csv 文件，以及自定义分隔符。
- lines：以行分隔的文件。每行的解码方法可以通过流定义中的格式参数来定义。例如，对于一个行分开的 JSON 字符串，文件类型应设置为 lines，格式应设置为 JSON。

创建读取 csv 文件的数据流，语法如下：

```
CREATE STREAM cscFileDemo () WITH (FORMAT="DELIMITED", DATASOURCE="abc.csv", TYPE="file", DELIMITER=",", CONF_KEY="csv"
```


## 数据导入导出

新版本中提供了 REST API 和 CLI 接口，用于导入导出当前 eKuiper 实例中的所有配置（流、表、规则、插件、源配置、动作配置、模式）。这样可以快速地备份配置或者移植配置到新的 eKuiper 实例中。导入导出的规则集为文本的 JSON 格式，可读性较强，也可以手工编辑。

导出配置的 rest 接口如下，通过此 API 可导出当前节点的所有配置

```
GET /data/export
```

导出配置的 rest 接口如下，通过此 API 可导入已有配置至目标 eKuiper 实例中

```
POST /data/import
```

如果导入的配置中包含插件 (native)、静态模式(static schema)的更新，则需要调用以下接口

```
POST /data/import?stop=1
```

导入配置的状态统计可用以下接口查看

```
GET /data/import/status
```


## 即将到来

下个月我们将继续进行 1.8.0 版本其他功能的开发，并重构文档，同时推进 Flow Editor 整合到 eKuiper manager 中。敬请期待。
