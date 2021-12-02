[云原生分布式流数据库 HStreamDB](https://hstream.io/zh) 本月正式发布了 v0.6。之后，HStreamDB 团队又继续投入到了 v0.7 的开发工作中。v0.7 将引入透明分区等重要功能，提高 HStreamDB 集群的稳定性，并对核心的数据存储和消费能力进行完善和扩展。

## v0.6 正式发布

HStreamDB v0.6 新增了很多实用的新特性和功能，包括 HServer 集群模式、共享订阅、HStream Metrics 以及 REST API 等，详情请查看[《HStreamDB v0.6 正式发布：水平扩展性、数据分发实时性提升，新功能带来新可能》](https://www.emqx.com/zh/blog/hstreamdb-v-0-6-release-notes)。

## v0.7 稳步推进

在 v0.7 我们将着眼于提高 HStreamDB 集群的稳定性，并对核心的数据存储和消费能力进行完善和扩展。以下是当前的主要进展：

### 透明分区功能设计与原型开发

HStreamDB 目前已经支持存储和管理大规模的数据流(stream)，为了进一步提升单个 stream 的扩展能力和读写性能，v0.7 即将引入透明分区的功能：一个 stream 内部将包含多个分区，读写流量将通过分区在集群中实现负载均衡，可以支持单个 stream 的更高吞吐。同时分区对于用户来说是完全透明的，用户无需提前指定分区数量和分区逻辑，也不用担心分区的增加和减少带来的数据重分配以及数据顺序等一系列困扰。我们相信 stream 本身是足够简洁和有力的抽象，分区只是实现的细节，不应该暴露给用户。

目前透明分区已经完成基本的功能设计，由于该功能对内部的实现影响较大，我们将首先通过一个原型系统进行功能验证和实现探索，目前正处在原型开发阶段。

### 支持 docker-compose

HStreamDB 本身是一个包含多组件的分布式系统，部署和使用相对比较复杂。为了方便用户在本地环境快速上手和体验，我们对之前基于 docker 的启动方式进行了改善，现在支持通过 docker compose 一键启动，也支持本地启动一个多节点的 HStreamDB 集群，具体介绍可参考[HStreamDB 文档](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html#start-hstreamdb-server-and-store)。

### Jepsen 测试

我们正在尝试使用 Jepsen 框架测试 HStreamDB 集群的功能和稳定性。Jepsen 是由 Kyle Kingsbury 用 Clojure 编写的验证分布式系统一致性的测试框架，许多知名的数据库产品都通过该框架发现过问题，包括：Elasticsearch，Cassandra 等，目前也有越来越多的分布式系统通过它来测试和验证自身的功能和容错能力。

当前我们已经成功将该框架应用于 HStreamDB，进行了一些基本的测试，并发现了几个小问题。后续将结合 HStreamDB 的数据一致性模型，在 Jepsen 中实现专门的 checker 来测试相关功能，并基于 Jepsen 提供的错误注入能力，进行更丰富的测试。

### 基于 grpc-gateway 的 REST API

HStreamDB Server 与客户端的通信协议和接口是基于 gRPC 的，虽然 gRPC 在开发和性能上都有很大优势，但在比如浏览器以及三方生态集成等场景下还是需要通过 REST API 来支持。为此 v0.6 我们基于 Haskell 的 servant 框架实现了部分 REST API，这带来的主要问题是我们需要同时维护这两套接口，代价较高，而且不能总是保证这两套接口的行为是一致的。为了解决这些问题，我们通过调研决定采用 gRPC-Gateway 来替换当前独立的 REST API 实现。

gRPC-Gateway 能够基于底层的 grpc 实现自动生成一层 REST 的代理服务，这样我们就只需维护一套 grpc 的实现，并且始终能够保证行为的一致性，代价是会损失一部分性能，不过这对于 REST API 应用的大部分场景来说都不是问题。当前我们已经基本完成了 servant 到  gRPC-Gateway 的迁移工作。
