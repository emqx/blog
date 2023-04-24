>eKuiper (原名 EMQ X Kuiper，现已捐献给 LF Edge 基金会，成为其旗下独立项目) 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。eKuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架 (如 Apache Spark、Apache Storm、Apache Flink) 迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于源 (Source)、SQL (业务逻辑处理)、目标 (Sink) 的规则引擎来实现边缘端的流式数据处理。
>
>社区站网址：[https://ekuiper.org/zh](https://ekuiper.org/zh) 
>
>GitHub 仓库：[https://github.com/lf-edge/ekuiper](https://github.com/lf-edge/ekuiper) 

本月初，eKuiper 团队发布了 v1.4.4 版本，完成 1.4.x 版本周期的最后一个 fixpack 。而在月底，我们正式发布了 [v1.5.0 版本](https://github.com/lf-edge/ekuiper/releases/tag/1.5.0)，包含一波功能上新。同时，[eKuiper 中英文社区网站](https://ekuiper.org/zh)也已正式上线，搭载了 eKuiper 开源项目的最新信息以及重新设计的中英文文档，欢迎大家访问。

## v1.5.0 新功能速览

本月新增加的功能包括：

### Neuron 整合

Neuron ([https://github.com/emqx/neuron](https://github.com/emqx/neuron)) 是一个EMQ 发起并开源的工业物联网（IIoT）边缘工业协议网关软件，用于现代大数据技术，以发挥工业 4.0 的力量。它支持对多种工业协议的一站式访问，并将其转换为标准 MQTT 协议以访问工业物联网平台。Neuron 和 eKuiper 整合使用，可以方便地进行 IIoT 边缘数据采集和计算。

Neruon 2.0 版本与 eKuiper 1.5.0 版本将无缝整合，用户无需配置即可在 eKuiper 中接入 Neruon 中采集到的数据，进行计算；也可以方便地从 eKuiper 中反控 Neuron 。两个产品的整合，可以显著降低边缘计算解决方案的部署成本，简化使用门槛。使用 NNG 协议进行通信，也可显著降低网络通信消耗，提高性能。

### 通用的 SQL source 和 sink 插件

在旧的系统升级改造过程中，我们往往还需要考虑对原有的系统的兼容。大量的老旧系统采用传统关系数据库存储采集的数据。在新的系统中，可能也有保存在数据库中，不方便提供流式接入的数据却需要进行实时计算的数据。还有更多的场景需要接入形形色色数量庞大的支持SQL的数据库或其他外部系统。

eKuiper 提供了统一的，多数据库通用的 SQL 拉取 source，可定时拉取支持 SQL 的数据源的数据，并提供基础的去重能力，形成流式数据进行统一的流式计算处理。该插件的预编译版本支持 MySQL、PostgresSQL 等常见数据库的接入；同时插件中搭载了几乎所有常见数据库的连接能力，用户只需要在编译时提供所需支持的数据库的参数，即可自行编译支持自定义数据库类型的插件。

除了数据拉取，我们也提供了数据写入的通用 SQL 插件。值得注意的是，eKuiper 本身已经提供了针对 InfluxDB、TDengine 等时序数据库的专用插件。通用 SQL 插件同样可以支持连接这些数据库，但提供的是 insert 功能，不支持特定数据库的非标准概念，例如 TDengine 的超级表只能使用 TDengine 插件进行写入。

更多信息以及支持的数据库列表，请参见 [SQL source 插件](https://ekuiper.org/docs/zh/latest/guide/sources/plugin/sql.html)和 [SQL sink 插件](https://ekuiper.org/docs/zh/latest/guide/sinks/plugin/sql.html)文档。

### 其余新功能回顾

前两个月开发版本中的新功能也在 1.5.0 版本中发布，主要包括：

- 按需编译：用户可自行选择需要编译的功能，以适应部署环境的资源限制
- 变化监测：提供一系列变化检测相关函数，方便灵活地实现去重，变化触发等常见需求
- 规则隔离：运行时规则软隔离规则错误和负载，提高整体服务稳定性
- 选择分组：提供对select 结果进行分组的函数，方便后续应用按组进行动态处理

## eKuiper 社区站上线

eKuiper 官方网站于本月正式上线。网站提供了产品的相关介绍，下载信息和文档博客的链接。同时，我们对文档进行了重构，增加了概念介绍、教程等模块，调整了导航树，希望能帮助用户更方便地找到有用的信息。扫描下方二维码即可快速访问：

![eKuiper 社区站](https://assets.emqx.com/images/030f3218bb39e7150e7cb5d9d27024da.png)
