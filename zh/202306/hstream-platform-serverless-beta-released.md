我们非常高兴地向大家宣布，HStream Platform Serverless Beta 现已正式发布！

HStream Platform Serverless 是基于公有云的 Serverless 流数据平台服务，向开发者提供免部署、零运维、高可用、一站式的流数据摄取、存储、实时处理和分发服务。用户完全无需关心任何服务器基础设施和软件集群部署等内容，只要完成注册，无需任何等待即可获得一个全功能的流数据平台，立即开始业务开发。

目前，HStream Platform Serverless Beta 版本的免费公测已经全面开启，您可以访问 HStream 官方网站（[https://hstream.io/zh/platform](https://hstream.io/zh/platform)）进行免费试用。

## 面向实时流数据的 Serverless 服务：可靠、易用、经济

Serverless 是近年来随着云计算蓬勃发展提出的一种新的计算和架构范式，它旨在将开发者从繁琐的基础设施管理任务中进一步解放：开发者只需专注自己的代码，基础设施的分配和管理都由服务提供商来负责，而且能够做到**随应用需求或负载情况按需分配和伸缩**。

HStream Platform Serverless 正是将 Serverless 的这种**以开发者为中心、充分发挥云弹性**的理念带到了实时流数据领域，旨在为用户带来最易用、最可靠、最经济的一站式流数据平台产品。

它采用多租户架构，将底层的物理集群按租户进行隔离，每个租户的数据位于自己的 Namespace 下，只能通过自己的证书进行访问，从而确保多租户之间数据的安全隔离。同时得益于 HStream 集群的存算分离架构设计，我们可以根据负载情况灵活地分别对计算和存储层进行弹性地独立伸缩。

## 统一的流数据平台：一站式解决流数据摄取、存储、处理、分发

随着如今越来越多的数据正以流数据的形式从多种数据源持续不断地生成，在企业愈发认识到实时数据处理的必要性和巨大价值的同时，也发现搭建、运维一套可用的实时数据平台以及在其之上进行实际的应用开发，都是非常复杂且成本昂贵的。这往往需要整合多个分布式系统，进行繁琐的二次开发，而且整个平台在实际运行过程中经常由于其中某个系统或组件的影响变得非常脆弱和不稳定的。这不但给运维带来巨大的压力，开发人员往往也被迫需要学习这些不同系统的多种编程接口以及各个系统的实现细节才能完成基本的应用开发。

为了解决以上问题，并给开发者运行和管理各种 streaming data workloads 提供真正友好的、统一的、现代化的产品体验，我们围绕实时流数据的摄取、存储、处理、分发等环节的核心需求，推出了一站式的流数据平台 HStream Platform。它主要提供了以下核心功能：

### 事件、消息和数据流的统一存储与实时订阅消费

HStream Platform 以 stream 为单位组织和管理数据。stream 提供 append-only 的逻辑存储模型，能够承载极高吞吐的流数据写入。基于底层的分布式架构和可靠的复制协议，每条写入的数据都被复制到多个存储节点上，保证容错和高可用。

数据写入后会立刻通过订阅交付给消费客户端，整个过程提供 ms 级的端到端消费时延。支持多种订阅模式，比如可以按照流或者队列的模式由多个消费客户端并行消费。另外，由于数据都被持久化存储，客户端可以从任何位置按照需要进行数据重放。

### 基于 SQL 的实时流处理

平台提供内置的实时流处理能力，用户可通过熟悉的 SQL 语句来表达流处理任务。这些 SQL 语句最终会被编译成 Dataflow Pipeline 交给底层的引擎去执行。从基本的实时数据过滤、转换，到多流 join、复杂的基于时间窗口的实时分析等都能通过 SQL 方便地实现。另外，后续还将提供自定义函数等扩展能力，结合平台的存储、订阅以及上下游系统连接等功能，可以轻松实现一站式的实时异常监控、实时 ETL、实时风控等复杂的实时应用开发。

### 与多种上下游系统无缝集成

尽管平台本身不需要任何依赖任何上下游系统就能完成大规模流数据的存储和实时处理，但考虑到如今企业内部应用和数据系统的复杂多样性，通过流平台来实现企业数据在多个系统之间的按需实时流转或同步是非常有价值的。为此，平台提供了与多种上下游系统集成的连接器组件，典型的比如数据库 CDC 连接器。用户通过填写必要的连接参数后即可启动对应的连接器的运行，同时由平台本身来负责这些连接器的运行时调度、进度监控、错误恢复等各方面的管理。

另外值得一提的是，当外部系统的数据通过 source 连接器摄入平台的同时，即可通过上述的流处理功能进行按需处理和转换，再将结果通过对应的 sink 连接器分发给下游系统。这种功能的组合具备强大的灵活性和可扩展性，能够轻松实现多种复杂的业务需求。

![与多种上下游系统无缝集成](https://assets.emqx.com/images/045fbacbe859711581b22d0c57584def.png)

### 可观测性和管理能力

平台内置丰富的业务 Metrics 指标，用户可通过图形管理界面直接查看对应的 Metrics 图表来直观地了解和掌握业务运行的当前和历史状态。具体任务的运行日志也能通过管理界面直接查看，这给开发和排错提供了很大的便利。此外，通过平台的控制台界面可以对多种 streaming data workloads 和资源进行统一的管理。

![HStream Platform 控制台](https://assets.emqx.com/images/1e2ee38473704a10b5ed6150afcd4b26.png)

## 快速开始

HStream Platform Serverless 提供完全的开箱即用的产品体验，用户只需要访问产品页面 （[https://hstream.io/zh/platform](https://hstream.io/zh/platform)），完成注册后即可立即开始使用，没有等待部署和配置完成的延迟。

目前，HStream Platform Serverless Beta 版本的**免费公测**已经全面开启，欢迎大家使用并提出宝贵意见。更多使用教程可参考文档 [开始使用 HStream Platform | HStream 文档](https://docs.hstream.io/zh/start/try-out-hstream-platform.html)。

## 结语

HStream Platform Serverless 的推出将让更多企业和个人开发者以最低的成本、最便捷的方式享受到真正友好、统一、现代化的一站式流数据平台服务。我们将持续专注和深耕实时流数据领域，不断创新并改进产品和服务，让用户只需关心数据，而无需关心背后的数据平台。
