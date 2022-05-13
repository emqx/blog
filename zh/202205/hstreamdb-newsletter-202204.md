HStreamDB 是业界首个专为流数据设计的开源云原生流数据库，致力于推动和实现数据基础设施的现代化和实时化，提供统一的大规模数据流的存储和处理能力，支持在动态变化的数据流上进行复杂的实时分析，能够高效助力企业精简复杂的实时数据栈，并快速从实时数据流中获取业务价值。

Github 仓库：[https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream)。

本月，HStreamDB 团队针对 HStream Server 进行了多项功能优化和问题修复，新增了多个监控指标，并提供了新的 Admin Server 以及 Erlang 客户端。

## HStream Server 

### 核心功能优化和问题修复

#### Subscription

- 新增配置项 `maxUnackedRecords`：该配置项用于控制每个订阅上已派发但尚未 acked 的最大的 record 的数量，当某个订阅上的未 acked 的数据达到这个配置的最大值后，便会停止该订阅上的数据交付，防止极端情况下造成大量 unacked records 堆积，影响 HServer 和对应 consumers 的性能表现。建议用户根据自身实际应用场景下的数据消费能力对这一参数进行合理配置。
- 优化了数据消费超时后的重传的实现，提升了数据重传的效率。
- 优化了读数据的性能。
- 优化了订阅删除的实现。
- 改进了对重复的 ack 消息的处理。
- 修复了订阅数据派发过程中因为 workload 排序错误引起数据分发的问题。
- 修复了订阅数据重传过程中由于原 consumer 不可用造成的重传数据丢失的问题。

#### Stream

- 新增配置项 `maxRecordSize`：在创建 stream 时，用户可以通过该配置来控制当前 stream 支持的最大的数据大小，超过这一阈值的数据会返回写入失败。
- 优化了 stream 删除的实现。
- 修复了数据写入过程中的内存分配问题。

### 新增多项监控指标

本月我们对 HStreamDB 的监控指标进行了细化和丰富，整体分为实时指标（e.g.，秒级的写入速率）和
历史指标（e.g.，分钟级的请求数）两大类，并增加了 records、bytes、requests 等多个维度的统计指标，以及 success_requests、failed_requests 之类的细化指标，还有核心链路的百分位时延指标等。

![HStreamDB 监控指标](https://assets.emqx.com/images/4cd2453b1b80aa76142bf9c781ba9148.png)

## HStream Admin Server

在之前的 0.7 版本中，我们提供了一个基于 gRPC-Gateway 自动生成的 HTTP Server，它可以向外提供 REST API 并将接收到的 HTTP 请求转发成到 HStream Server 的 gRPC 请求。虽然这种基于自动生成的方式具有开发简单、维护成本低的优点，但也存在着一些功能上的限制。

同时，考虑到我们将原来 HTTP Server 的定位升级为统一的 Admin Server，后续它将负责服务多种 CLI Tools、Dashboard 以及提供开放的 REST API 供开发者使用。为此我们重新实现了一个 Admin Server，仓库地址见 [https://github.com/hstreamdb/http-services](https://github.com/hstreamdb/http-services) 。

![HStream Admin Server](https://assets.emqx.com/images/a6e204882da4ab01da354065428c151a.png)

## HStreamDB 客户端

### HStreamDB Java Client

- 新增 Subscription 的 `maxUnackedRecords` 配置支持。
- 新增 Consumer 的 `ackAgeLimit` 配置，用于控制 batched ack 的发送时延。
- 新增 Subscription 的强制删除支持。
- 新增 Stream 的强制删除支持。
- 优化了 Consumer 关闭时的行为。
- 调整 `BatchSetting` 和 `FlowControlSetting` 暴露的公共接口。
- 修复了 `BufferedProducer` 对累积的 record size 的计算问题。
- 丰富了 Javadoc 中相关接口的介绍和说明。

### HStreamDB Erlang Client

本月我们为 HStreamDB 新增了 Erlang 客户端库 hstreamdb-erlang，仓库地址：[https://github.com/hstreamdb/hstreamdb-erlang](https://github.com/hstreamdb/hstreamdb-erlang) 。它将主要用于支持和高性能 IoT 消息服务器 [EMQX](https://www.emqx.com/zh/products/emqx) 的高效集成，实现将 EMQX 接收到的海量物联网数据快速持久化存储到 HStreamDB 中，为用户提供端到端的物联网数据解决方案。 目前 Erlang 客户端已经具备基本的 stream 创建和数据写入能力，但整体尚处在早期开发阶段，新功能和性能优化工作在持续进行中。
