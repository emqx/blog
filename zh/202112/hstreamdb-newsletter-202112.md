目前 [HStreamDB](https://hstream.io/zh) 团队正专注于 v0.7 的研发工作。正如我们之前所提到的，v0.7 主要致力于改进 HServer 集群的稳定性与可用性以及引入新的透明分区功能。

本月我们主要完成了透明分区的原型开发，引入了新的基于一致性哈希的 HServer 集群负载均衡策略，改进了 Java Client 的集群支持，新增了集群部署脚本，并通过继续引入更多测试手段和用例发现并修复了当前存在的一些问题。

## 透明分区

透明分区旨在解决单个 stream 在高读写流量下的扩展性问题，其主要挑战在于如何在不给用户引入额外复杂度的情况下实现 stream 的内部分区，同时维护数据的顺序性。

在我们的设计方案里，每条 record 会包含一个分区键，每个分区键对应一个逻辑分区。HServer 会根据 record 携带的分区键将它路由到 stream 内对应的物理分区，同时保证同一个逻辑分区内的数据始终按照顺序交付给消费者。

需要注意的是，物理分区对于用户是完全透明的，用户只需要面向逻辑分区进行开发，也不用考虑逻辑分区和物理分区的映射关系。这不仅带来了良好的扩展性，也极大减轻了用户的心智负担。

目前我们已经完成了透明分区的原型开发，将在下个月开始着手于该功能在主项目上的引入。

## 负载均衡

为了让集群内各节点的资源得到合理的利用，需要将客户端的读写流量尽可能均衡地分配到各节点上。目前，写请求是以 stream 为单位进行分配的；读请求是以 subscription 为单位进行分配的，一个 stream 上可能存在多个不同的 subscription。

我们之前的负载均衡策略是基于节点的硬件资源负载情况来实现的。存在的主要问题是需要节点间相互通信交换多种硬件资源信息，包括 CPU、内存、网络等，同时这种方式存在一定的滞后性，总体来看实现相对复杂，效率较低。

为此我们选择基于一致性哈希算法重新实现新的负载均衡模块。一致性哈希是一个优雅而强大的算法，被多种分布式系统所采用，比如 DynamoDB。基于它的分配策略不仅使得负载均衡模块不用再实时维护硬件资源信息，而且核心算法更加简洁，也能很好应对集群成员变更的时候的重分配问题。同时它也很灵活，容易被扩展和优化，比如通过配置不同权重的方式应对异质节点。还有一些最新的研究优化，比如 Google 的 [Consistent Hashing with Bounded Loads](https://ai.googleblog.com/2017/04/consistent-hashing-with-bounded-loads.html)。

## Java Client

本月 Java Client 主要完善了请求出错时在多个 HServer 节点之间重试的能力，改进了对 HStream 集群的支持。

Java Client 向 HServer 发送网络请求基于 gRPC-java，由于 gRPC-java 提供的接口主要都是基于回调风格的，要实现多节点的请求重试很容易陷入回调地狱。同时，由于客户端和服务端的交互逻辑，很多时候重试需要涉及多个 RPC 的调用，比如需要首先刷新集群节点信息，再重新查询对应请求的节点，然后才是向对应节点发送请求。基于 gRPC-java 的回调 API 让这些逻辑实现起来很困难，更棘手的是对于双向流的 RPC 的处理。

我们通过 Kotlin Coroutine 提供的能力完美解决了回调地狱的问题，更使得实现代码得到了简化。值得注意的是，Kotlin 的引入只是重构了 Client 的内部实现，Client 的外部接口没有任何变化，因此不会影响到用户对 Java Client 的使用。

另外，对于本月 log4j2 的一系列安全问题，Java Client 也进行了相关修复和更新。

## 测试和问题修复

本月我们继续对集成测试和 Jepsen 测试进行完善，主要通过测试发现并修复的较为严重的问题如下：

- HServer 在创建资源时候的存在竞态条件，会出现并发错误
- 在向 subscription 交付数据的时候，某些情况下可能触发丢数据
- Client 端的 channel 资源泄漏

## 部署与使用

**集群部署和启动脚本**

为了方便用户在多台机器上快速部署和使用 HStreamDB 集群，我们开发了专门的集群部署脚本，可通过以下链接下载 [https://github.com/hstreamdb/hstream/blob/main/script/dev-deploy](https://github.com/hstreamdb/hstream/blob/main/script/dev-deploy)。

**HServer 配置文件**

随着 HStreamDB 配置项的不断增加，原有的通过命令行选项传递配置的方式不太足够，因此我们又引入了通过配置文件的方式来统一管理配置项，请参考 [https://github.com/hstreamdb/hstream/blob/main/conf/hstream.yaml](https://github.com/hstreamdb/hstream/blob/main/conf/hstream.yaml)。

## 文档资源更新

- 新增部分中文文档 [https://hstream.io/docs/zh/latest/](https://hstream.io/docs/zh/latest/) 
- 新增在多节点上部署 HStreamDB 集群的文档 [https://hstream.io/docs/en/latest/deployment/deploy-docker.html](https://hstream.io/docs/en/latest/deployment/deploy-docker.html) 
- HStreamDB 与 EMQX 快速集成的教程 [https://www.emqx.com/zh/blog/integration-practice-of-emqx-and-hstreamdb](https://www.emqx.com/zh/blog/integration-practice-of-emqx-and-hstreamdb)
