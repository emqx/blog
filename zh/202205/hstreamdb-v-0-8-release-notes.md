HStreamDB v0.8 现已正式发布！

在 0.8 版本中，我们优化了读写性能，提升了长时间运行的稳定性，新增了基于 mTLS 的安全性支持、多项监控指标、Admin Server、Benchmark Tools 和 Terraform 部署支持，并包含 stream 和 subscription 上的多项配置新增和功能改进，同时带来了多种语言（Java、Go、Erlang）的客户端更新。

>Github 仓库：[https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream) 
>
>Docker 镜像：[https://hub.docker.com/r/hstreamdb/hstream](https://hub.docker.com/r/hstreamdb/hstream) 


## HStream Server 新功能

### 新增 mTLS 支持

考虑到用户在生产环境（比如公有云，私有云等）部署时的安全性需求，比如：连接加密，身份认证等，v0.8 新增了 mTLS 的支持，用户可通过在 server 和 client（当前仅 Java client 支持）上开启相关的配置来使用，具体可参考文档 https://hstream.io/docs/en/latest/security/overview.html

### 新增 Stream 和 Subscription 的多项配置

#### Stream

新增配置项 `maxRecordSize`：在创建 stream 时，用户可以通过该配置来控制当前 stream 支持的最大的数据大小，超过这一阈值的数据会返回写入失败

新增配置项 `backlogRetention` : 这个属性决定了当前 stream 的数据可以在 HStreamDB 中驻留多久，超过这个期限的数据将被清理。 

#### Subscription

新增配置项 `maxUnackedRecords`：该配置项用于控制每个订阅上已派发但尚未 acked 的最大的 record 的数量，当某个订阅上的未 acked 的数据达到这个配置的最大值后，便会停止该订阅上的数据交付，防止极端情况下造成大量 unacked records 堆积，影响 HServer 和对应 consumers 的性能表现。建议用户根据自身实际应用场景下的数据消费能力对这一参数进行合理配置。

### 新增多项监控指标

为了使用户更加方便地监控 HStream 集群，我们对 stream 的监控指标进行了细化和丰富，整体分为实时指标（e.g. 秒级到分钟级的写入速率）和历史指标（e.g. 所有的 append_request 总数）两大类，并增加了 records、bytes、requests 等多个维度的统计指标，以及 success / failed 等细化指标，还有核心链路的百分位时延指标等。当前可以使用 hadmin 来查看这些指标，具体可参考文档 [https://hstream.io/docs/en/latest/admin/admin.html#hsteam-stats](https://hstream.io/docs/en/latest/admin/admin.html#hsteam-stats) 

### 新增 Admin Server

在之前的 0.7 版本中，我们提供了一个基于 gRPC-Gateway 自动生成的 HTTP Server，它可以向外提供 REST API 并将接收到的 HTTP 请求转发成到 HStream Server 的 gRPC 请求。虽然这种基于自动生成的方式具有开发简单、维护成本低的优点，但也存在着一些功能上的限制。

同时，考虑到我们将原来 HTTP Server 的定位升级为统一的 Admin Server，后续它将负责服务多种 CLI Tools、Dashboard 以及提供开放的 REST API 供开发者使用。

为此我们重新实现了一个 Admin Server，仓库地址: 

[https://github.com/hstreamdb/http-services](https://github.com/hstreamdb/http-services) 

### 新增基于 Terraform 的快速部署

Terraform 是一款由 HashiCorp 主导开发的开源「基础设施即代码」工具，可以帮助开发及运维人员以自动化和可重现的方式来管理基础架构和资源，高效管理云服务。通过 Terraform 可以快速在多种公有云和私有云环境下部署，体验和测试 HStreamDB，具体可参考文档 [https://hstream.io/docs/en/latest/deployment/deploy-terraform.html](https://hstream.io/docs/en/latest/deployment/deploy-terraform.html) 

## HStream Server 优化改进

### 数据消费优化

在 v0.7 的实现里，一个 subscription 的相关状态可能分布在集群内的多个 HServer 的节点上，虽然这种设计带来了很大的灵活性和细粒度的扩展性，但也造成了实现的复杂性，包括需要多轮 RPC 通信，跨节点的状态维护等。在新的实现中，我们限制让一个 subscription 的状态不跨节点，这带来了协议的简化，而且在新的实现中我们大量使用 STM 进行并发状态的处理，得益于 STM 提供的易用性和可组合性，在保证正确性的同时改进了高并发情况下的性能。

此外，我们对整体的数据消费流程还做出了以下改进：

- 优化了数据消费超时后的重传的实现，提升了数据重传的效率。
- 优化了读数据的性能。
- 改进了对重复的 ack 消息的处理。

### 资源删除优化

改进了对 stream 和 subscription 的删除操作，新增了强制删除的选项。关于如何创建和管理 HStreamDB 中的相关资源，请参考文档 [https://hstream.io/docs/en/latest/guides/stream.html#create-and-manage-streams](https://hstream.io/docs/en/latest/guides/stream.html#create-and-manage-streams)   和 [https://hstream.io/docs/en/latest/guides/subscription.html](https://hstream.io/docs/en/latest/guides/subscription.html)   

## HStreamDB Java 客户端 v0.8

### hstreamdb-java v0.8 新功能

- 新增对 hstreamdb v0.8 多项新功能的支持：包括 TLS、stream 和 subscription 的新增配置项以及强制删除的支持。
-  `BufferedProducer` 采用新的配置项，主要分为 `BatchSetting` 和 `FlowControlSetting` ：其中 `BatchSetting` 主要控制 `BufferedProducer` 如何做 batch、batch 的大小和发送时机等，可以通过 `recordCountLimit` 、`bytesLimit` 、`ageLimit` 三个选项来共同控制，可以灵活配置实现根据不同场景满足不同的吞吐和时延需求。而 `FlowControlSetting` 主要控制整个 `BufferedProducer` 占用的内存空间大小，以及达到限制之后的行为。

### hstreamdb-java v0.8 性能优化

- BufferedProducer 对多个不同 orderingKey 的数据改用并行发送的策略，大幅提高了多 key 场景下的写入性能。
- 为 `Consumer` 的 acknowledgement 发送启用了 batch 机制，提升了 Consumer 的性能，新增 `Consumer` 的 `ackAgeLimit` 配置，用于控制 batched ack 的发送时延。

## 新增多语言客户端和性能测试工具

### hstreamdb-go v0.1.0 发布

hstreamdb-go 是 HStreamDB 的 Golang 客户端，已发布 v0.1.0，目前支持和 HStreamDB 的基本交互能力，仓库请见 [https://github.com/hstreamdb/hstreamdb-go](https://github.com/hstreamdb/hstreamdb-go) 。

### 新增 hstreamdb-erlang 

hstreamdb-erlang 是 HStreamDB 的 Erlang 客户端库，仓库地址见 [https://github.com/hstreamdb/hstreamdb-erlang](https://github.com/hstreamdb/hstreamdb-erlang) ，它将主要用于支持和高性能 IoT 消息服务器 EMQX 的高效集成，实现将 EMQX 接收到的海量物联网数据快速持久化存储到 HStreamDB 中，为用户提供端到端的物联网数据解决方案。 目前 Erlang 客户端已经具备基本的 stream 创建和数据写入能力，但整体尚处在早期开发阶段，新功能和性能优化工作还在持续进行中。

其它更多语言的支持也在陆续规划中，欢迎大家进行建议和反馈。由于 HStreamDB 采用 gRPC 和客户端进行通信，得益于 gRPC 广泛的语言支持和工程便利性，开发新语言客户端的成本大大降低，欢迎社区的伙伴们尝试开发新客户端。

### 新增 benchmark tools

为了方便用户快速评测 HStreamDB 的性能，我们开源了一组 benchmark tools，具体请参考 [https://github.com/hstreamdb/bench](https://github.com/hstreamdb/bench) 

## 问题修复

v0.8 还包含大量问题修复，改进了长期运行的稳定性，详见 release notes [https://hstream.io/docs/zh/latest/release_notes/HStreamDB.html#v0-8-0-2022-04-29](https://hstream.io/docs/zh/latest/release_notes/HStreamDB.html#v0-8-0-2022-04-29)
