[HStreamDB](https://hstream.io/zh) 是首个专为流数据设计的「流原生数据库」，支持高效存储和管理大规模流数据，以及在动态变化的数据流上进行复杂的实时分析，旨在对大规模数据流的接入、存储、处理、分发等环节进行全生命周期管理，非常适合应用于 IoT、互联网、金融等领域的数据管理和实时分析场景。

继七月末 v0.5 发布后，HStreamDB 团队一直在专注于下一版本的研发工作。本月里，我们针对易用性和 HStream Server 扩展能力的提升方面为 v0.6 版本规划了诸多新特性。该版本预计将于下周发布。

## 新增 HServer 集群支持

作为一款[云原生分布式流数据库](https://hstream.io/zh)，HStreamDB 从设计之初就采用了计算和存储分离的架构，目标是支持计算层和存储层的独立水平扩展。在 HStreamDB 之前的版本中，存储层 HStore 已经具备了水平扩展的能力。在即将发布的 v0.6 版本中，计算层 HServer 也将支持集群模式，从而可以实现随客户端请求和计算任务的规模对计算层的 HServer 节点进行扩展。

HStreamDB 的计算节点 HServer 整体上被设计成无状态的，因此非常适合进行快速的水平扩展。v0.6 的 HServer 集群模式主要包含以下特性：

- 自动节点健康检测和失败恢复
- 按照节点负载情况对客户端请求或者计算任务进行调度和均衡
- 支持节点的动态加入和退出

## 新增共享订阅功能

在之前的版本中，一个 Subscription 同时只允许一个客户端进行消费，这在较大数据量的场景下限制了客户端的消费能力。因此，为了支持扩展客户端的消费能力，v0.6 版本新增了共享订阅功能，它允许多个客户端在一个订阅上并行消费。

同一个订阅里包含的所有的消费者组成一个消费者组(Consumer Group)，HServer 会通过 round-robin 的方式向消费者组中的多个消费者派发数据。消费者组中的成员支持随时动态变更，客户端可以在任何时候加入或退出当前的消费者组。

HStreamDB 目前支持 at least once 的消费语义，每条数据在客户端消费完之后需要回复 Ack，如果超时未接收到某条数据的 Ack，HServer 会自动重新向可用的消费者投递该条数据。

同一个消费者组中的成员共享消费进度，HStream 会根据客户端 Ack 的情况维护消费进度，客户端任何时候都可以从上一次的位置恢复消费。

需要注意的是，v0.6 的共享订阅模式下不保持数据的顺序，后续共享订阅将支持按 key 派发的模式，可以支持相同 key 的数据有序交付。

## 新增统计功能

v0.6 还增加了基本的数据统计功能，支持对诸如 stream 的写入速率，消费速率等关键指标进行统计。用户可以通过 HStream CLI 来查看相应的统计指标，如下图所示。

![HStream CLI 统计功能](https://static.emqx.net/images/d4dd69dd47f47163f028154245833913.png)

## 新增数据写入 Rest API 

v0.6 版本增加了向 HStreamDB 写入数据的 Rest API，通过此 API 并结合 EMQX 开源版的 web hook 功能，可以实现 EMQX 和 HStreamDB 的快速集成。

## HStreamDB Java SDK 更新

HStreamDB-Java 是目前主要支持的 HStreamDB 客户端（后续将会有更多语言的客户端支持），用户主要通过该客户端来使用 HStreamDB 的大多数功能。

即将发布的 HStreamDB Java SDK v0.6 主要包含以下特性：

- 新增对 HStreamDB 集群的支持
- 新增对[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)的支持
- 重构部分 API
- 修复了一些已知的问题
