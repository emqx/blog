**HStreamDB 是一款专为流式数据设计的云原生分布式数据库，可针对大规模实时数据流的接入、存储、处理、分发等环节进行全生命周期管理。** 它使用标准 SQL (及其流式拓展）作为主要接口语言，以实时性作为主要特征，旨在简化数据流的运维管理以及实时应用的开发，不仅支持高效存储和管理大规模数据流，还能够在动态变化的数据流上进行复杂的实时分析。

在[《当数据库遇上流计算：流数据库的诞生》](https://www.emqx.com/zh/blog/birth-of-streaming-database)一文中，我们介绍了流数据库的概念。以此为产品设计理念基础，我们所开发的[流数据库 - HStreamDB](https://hstream.io/zh) 于今年初正式开源。

今天，EMQ HStreamDB 团队非常高兴地向大家宣布：**HStreamDB v0.5 正式发布！**

下载地址：[https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream)



## 版本更新

在此次发布的 0.5 版本中，我们除了对原有的功能（如：对数据流的管理、数据的写入与消费）进行了升级，还新增加了很多对使用 HStreamDB  进行开发具有重大意义的功能特性，例如 Java SDK、MySQL 和 Clickhouse Connector，以及对物化视图的支持等。

### 增加对物化视图的支持

提供物化视图功能，支持在持续更新的数据流上进行复杂的查询和分析操作。同时，HStreamDB 内部的增量计算引擎会根据数据流的变化实时更新物化视图，用户可通过 SQL 语句查询物化视图获得实时的数据洞察。

### 增加 Java SDK，方便基于 HStreamDB 的开发

这是我们主要推荐的使用 HStreamDB 的方式，用户可以查阅 [HStreamDB 文档](https://docs.hstream.io/develop/java-sdk/installation/)了解如何安装以及使用 Java 进行开发。

### 提供 Sink Connector

我们提供了两种 Sink Connector，包括 MySQL 和 Clickhouse。用户可以通过 SQL 语句轻松指定哪些数据需要导入到特定的数据库中。

### 新增 Dashboard

用户可以通过 Dashboard 来完成对 HStreamDB 内部资源的管理。

### 重构 Server，基于 gRPC 设计实现了 Server 的接口

基于 gRPC 的重新设计了 HStream Server，使 Server 的实现清晰，增强了 Server 的可扩展能力。

### 改进了基于 SQL 的流数据处理

新增了大量 SQL 函数，完善和优化了聚合函数。增强了对流处理任务的管理功能。

### 优化了低层存储逻辑



## 发展规划

在之后的版本中，我们将朝着以下目标继续努力。

### 提升 HStream Server 的扩展能力

- 实现 HStream Server 集群支持
- 支持多个 consumer 进行[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)和并行消费
- 优化控制平面元数据存储

### 增强运维和监控能力

- 支持使用 k8s 进行部署
- 实现统计监控框架
- 丰富 Dashboard 功能

### 增强流处理能力

- 优化流引擎的实现，提升处理效率
- 增加 SQL 优化器，优化执行计划生成
- 实现流任务调度框架，支持并行处理

### 提升易用性

- 改进 Java SDK
- 完善用户文档，提供更多教程和示例
- 提供更多应用案例

### 丰富 HStreamDB 生态，提升集成能力

- 重构 Connector 框架，方便开发者自行实现所需的 Connector
- 实现分级存存储
- 实现更多常用系统的 Connector 支持

我们也计划在下个阶段完成与[云原生分布式物联网接入平台 - EMQX](https://www.emqx.com/zh/products/emqx) 的集成，这将不仅能验证 HStreamDB 功能完善程度，更意味着一个为物联网应用开发量身打造的产品组合的诞生。



## 未来展望

HStreamDB 作为流数据库这一基础软件品类的开创者，正向着能够被投入生产环境使用这一阶段性目标稳步前进。我们将继续推进 HStreamDB  的开发，完善功能，稳定性能，保证可靠。相信在不远的将来，用户便能使用 HStreamDB  更加快速地开发实时应用，更加简单地获取即时数据洞察。同时，我们也在此感谢广大社区成员的每一次使用和每一次贡献。敬请期待一个更加完善成熟的  HStreamDB。

有关 HStreamDB v0.5 版本的更多细节，可观看 [HStreamDB v0.5 功能演示视频](https://www.emqx.com/zh/resources/hstreamdb-v-0-5-features-demo)回放。
