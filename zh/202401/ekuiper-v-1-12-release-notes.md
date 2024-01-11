轻量级物联网数据分析和流处理引擎 eKuiper 1.12 版本现已正式发布！

本次升级聚焦于提升外部系统的接入和服务管理能力，为您带来更好的使用体验。主要新功能亮点有：

- **全新的 source/sink 支持：** 引入了 WebSocket、RedisPubSub、Simulator 等新的 source/sink，进一步扩展了数据接入方式。
- **现有 source/sink 加强：** 对 Kafka 和 InfluxDB v1 和 v2 等现有 source/sink 进行优化和加强。
- **HTTP table & service：**支持使用 HTTP Pull 作为 lookup table；使用 HTTP 微服务作为外部服务时，无需再提前定义 schema。两个功能使得数据流和 HTTP 服务结合的计算更加快捷和灵活。
- **配置增强：**支持更丰富的 Log 配置，包括 syslog 和按文件大小的 rotation 等能力的配置。支持配置写入数据库，方便多节点配置共享和管理。
- **规则管理相关 API：** 增加了丰富的规则管理相关 API，例如规则的试运行、规则 SQL 验证和 Explain 等，助力您更高效地管理系统。
- **更多预编译打包版本：**二进制包添加 full 版本，预装了大部分 source/sink 插件。提供了预编译的 apk 文件，可直接安装到手机或车机上的安卓系统。

eKuiper 1.12 的发布离不开海内外社区贡献者的辛勤付出，在此我们表示衷心的感谢。

## 灵活适配数据源和目标

在边缘计算领域，涉及到各种多样化的场景和设备，而这些设备和场景可能会产生各式各样格式的数据，并将其存储在不同类型的数据库或消息队列中。为了应对这种异构性，eKuiper 必须具备灵活适配异构系统的能力，以确保流畅地集成和处理各种数据。

在最新版本中，eKuiper 进一步加强了对不同数据源和目标的适配。新版本引入了更多的 source/sink，同时对现有的 sink 进行了改进，特别是在处理大规模数据时，提升了现有 sink 的批量发送能力。在高吞吐量的数据处理过程中，传统的串行 IO 操作可能无法有效消耗产生的数据，因此批量发送的优化显得尤为重要，能够更有效地处理和传输数据。这一改进将为用户提供更出色的性能和更高效的数据处理能力。

单靠一个团队或组织难以维护如此大量的异构接入协议和格式。在开源社区的支持下，我们可以更容易地吸纳和整合来自不同背景的贡献者，使适配器更加灵活和具有广泛适用性。欢迎更多的用户加入社区，共同维护更广泛的数据源和目标。

### WebSocket 支持

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议，它允许在客户端和服务器之间进行实时、双向的数据传输，适合进行数据的传输。新版本中，新增的 **WebSocket source 和 sink** 允许您与 WebSocket 连接进行交互，从而实现实时数据的接收和发送。

eKuiper 支持 server/client 两种模式来建立 websocket 连接。您可以通过 websocket 连接来让 eKuiper 发送或者接收数据。在创建规则时，您可以通过是否指定远端 host 地址来让 eKuiper 推断以何种模式创建 websocket 连接。当远端 host 地址被提供时，eKuiper 将会向远端 websocket server 发起连接请求来建立 websocket 连接。当远端 host 地址没有被提供时，eKuiper 将会自己建立一个 websocket 端点，等待远端 client 向 eKuiper 发起 websocket 连接请求。

同时 websocket 也支持 shared connection 模式。您可以通过在 connection.yaml 声明 websocket 连接后，在多条规则中声明使用同一个 websocket connection。当多个 Websocket source 使用一个 websocket shared connection 时，websocket 连接收到的消息将被广播到所有使用这个 shared connection 的规则。当多个 Websocket sink 使用一个 websocket shared connection 时，所有使用这个 shared connection 的规则的数据输出都会发送到这一个 websocket connection 内。

### Kafka 支持

Apache Kafka 是一个分布式的消息系统，具有高吞吐量、高可用性、可伸缩性和持久性等特点。新的版本中，我们对 Kafka sink 进行了增强，主要包括：

1. 支持批量发送，可配置 batchSize 和 lingerInterval 来定义批量的大小和时间；
2. 支持配置 Key 和 headers，并支持模板；
3. 支持 TLS 连接。

新版本添加了 Kafka source，支持从 Kafka 中消费事件。基于 Kafka 的持久化能力，使用 Kafka source 配合规则 QoS 配置可实现自动回拨消费，保证意外故障后不丢失数据。

### HTTP Scheme-less External Service

随着微服务架构的兴起，用户往往有大量的存量服务，每个服务都专注于执行一组特定的业务功能。这些服务可以独立部署、独立扩展，它们之间通过 API 进行通信。微服务架构旨在简化复杂的应用程序，提高灵活性、可维护性和可扩展性。其中，HTTP 是最常见的微服务通信方式之一。

eKuiper 提供了[外部函数](https://ekuiper.org/docs/en/latest/extension/external/external_func.html)的方式，可以通过配置将微服务包装为规则 SQL 可使用的函数。之前版本的外部函数要求用户定义函数的基于 protobuf 的模式(schema)，但是大部分的 HTTP 服务没有现成的 schema，额外编写异常繁琐。新版本提供了 schema-less 的方式使用 HTTP 服务，只需要声明一个 endpoint，即可以用一个函数动态地调用该 endpoint 下的所有服务。详情请查看 [Schema-less 服务定义](https://ekuiper.org/docs/en/latest/extension/external/external_func.html#schemaless-external-function)和[Schema-less 外部函数的使用](https://ekuiper.org/docs/en/latest/extension/external/external_func.html#schemaless-external-function-1)。

### HTTP Lookup Table

Lookup table 查询表功能，使得用户可以进行流批结合的运算，将实时的数据流与外部持久化的数据，例如数据库表格中的数据结合运算，实现诸如数据补全等功能。新的版本在 SQL 和 Redis 的基础上，新增了 HTTP 查询表功能。基于 HTTP 查询表，用户可将流式实时数据与通过 HTTP 服务暴露的数据结合进行运算。

### Redis Pub/Sub 支持

Redis Pub/Sub（发布/订阅）是 Redis 提供的一种消息传递模式，用于实现消息的发布和订阅。在这种模式中，消息的发送者称为发布者（Publisher），而接收消息的实体称为订阅者（Subscriber）。发布者不直接发送消息给特定的订阅者，而是将消息发布到一个特定的频道（Channel），所有订阅该频道的订阅者都会接收到消息。

新版本在普通 Redis source/sink 的基础上，我们添加了 RedisSub source 和 RedisPub sink，更适合基于 Redis 做大吞吐量的消息传递和处理。用户可以订阅和发布到 Redis 的 Channel 中。

### InfluxDB v1/v2 Sink 增强

InfluxDB 是一个开源的时序数据库，在物联网场景中得到了广泛的应用。得益于社区的支持，eKuiper 在之前的版本中提供了 Influx1 和 Influx2 sink，支持将处理后的数据写入 InfluxDB v1 和 v2 版本中。新版本中，eKuiper 增加了大量的属性和批量写入功能，使得这两个 sink 可以应用于更高数据吞吐量的场景中。

- 支持批量写入设置；
- 支持多个 tag，支持基于数据模板的动态 tag；
- 支持配置动态时间戳以及时间精度；
- 支持行模式（v2），支持行模式下使用数据模板格式化数据。

### Simulator Source

模拟器源提供了一种用于测试和演示目的的数据生成方式，它可以用来模拟来自设备或传感器的数据流。使用这种数据源，用户可以快速进行规则场景的验证而无需连接真实的数据源。使用如下语句创建 simulator 数据源，接下来就可以在规则中使用并测试。

```
CREATE STREAM mock_stream () WITH (TYPE="simulator")
```

## 配置和管理

边缘计算通常涉及到分布在不同地理位置的设备和系统。这使得监控、管理和升级变得更加复杂。因此，eKuiper 在提升功能的同时，也一直致力于提升可维护性。eKuiper 1.12 提供了更多的配置和管理的能力。

NeuronEX 是一款工业边缘网关软件，专注于工业数据的实时接入和智能分析。目前 NeuronEX 中已经集成了 eKuiper 1.12 中的流处理功能和管理功能，并在用户体验方面进行了较大优化，欢迎试用：[https://www.emqx.com/zh/try?product=neuronex](https://www.emqx.com/zh/try?product=neuronex)。

### 日志配置增强

新的版本支持更多的日志配置，主要包括：

- Log level 的配置，可配置日志级别；
- Syslog 的配置，例如 syslog 的远程地址、tag 等；
- Rotate 配置，在基于时间的 rotation 的基础上，增加了基于文件大小的 rotation。

完整配置文档，请参阅 [基本配置 | eKuiper 文档](https://ekuiper.org/docs/zh/latest/configuration/global_configurations.html#基本配置)。

### 新的管理 API

新的版本添加了一些管理 API

- 规则试运行相关 API，用户可以基于这些 API 创建试运行规则，进行规则调试。
- 规则 SQL explain API
- 关闭 eKuiper API

## 结语

欢迎您升级到 eKuiper 1.12.0，体验全新功能和改进。我们将一如既往地倾听社区的声音，不断优化 eKuiper，为用户提供更强大、稳定的边缘计算体验。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
