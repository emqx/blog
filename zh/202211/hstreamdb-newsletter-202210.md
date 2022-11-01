十月底，我们正式发布了 HStreamDB 0.10 。除[之前 Newsletter 中](https://hstream.io/zh/blog/hstreamdb-newsletter-202209)提到的内容之外，这一版本还完成了 HStore 对新 MetaStore 的支持，同时改进了 HServer 的资源分配机制以及 Grafana 监控栈的部署和使用，并带来了流引擎、多语言客户端以及 HStream IO 的多项更新。

## HStore 支持基于 Rqlite 的 MetaStore

HStore 是 HStreamDB 的存储子系统，它为 HStreamDB 提供高性能、可扩展、高可靠的大规模流数据底层存储服务。此前 HStore 主要依赖 Zookeeper 作为 MetaStore 实现两方面的功能：一是节点注册和服务发现，二是用作 EpochStore，存储关联于每个 StreamShard 的 Epoch 信息。

[如之前提到的](https://hstream.io/zh/blog/hstreamdb-newsletter-202209)，我们正在采用新的 MetaStore 架构统一 HServer 和 HStore 的集群元信息存储。此前我们已经完成了 HServer 对新 MetaStore 的适配，十月我们进一步完成了 HStore 对基于 Rqlite 的 MetaStore 的实验性支持。由于新的 MetaStore 还需要更多的测试，v0.10 将继续使用 Zookeeper 作为默认的 MetaStore，但同时也支持试用 Rqlite 的版本。

## HServer 资源分配改进

HServer 的资源分配是指 HServer 集群内部如何将对给类资源的请求负载，比如 stream、subscription 的读写负载，以及 Streaming Query、IO Task 的计算负载等在各个节点间分配的过程，这一过程的主要目标是让各类负载能够比较均衡地在集群各节点间进行分配，以充分发挥集群的水平扩展能力，同时需要处理好集群成员变更，比如节点新增或退出过程中资源的迁移以及一致性等问题。

此前 HStreamDB 的资源分配机制主要基于一致性哈希算法，能够将不同类的负载以资源为单位比较均匀到分配到集群的各个节点上。这套机制相对轻量高效，主要问题是在面临节点变更的情况下可能发生资源迁移和重分配的不一致。为此我们对原来的资源分配机制进行了扩展，主要是在原来的基础上引入了全局的资源分配表作为 Single source of truth 来解决一致性问题，目前这张表存储在 MetaStore 里。

## SQL 和流引擎更新

本月我们对 HStreamDB 的 SQL 前端和流处理引擎进行了扩展和改进，旨在支持更多标准 SQL 语法所提供的功能，支撑复杂的流处理任务场景。主要更新包括：

- 对子查询的全面支持。新版本中大部分表达式出现的位置都允许使用子查询。
- 数据类型的细化。支持大部分数据库系统内建的日期、时间、数组及 JSON 等类型，同时新增显式类型转换和 JSON 相关的运算符。
- 时间窗口的调整。与上个版本只允许至多一个时间窗口不同，现在可以为每个 source stream 单独配置时间窗口。
- 更泛化的 materialized view 查询语句。对于 materialized view 的查询不再局限于特定格式的 SQL 语句，现在任何用于 stream 操作的语句都同样适用于 materialized view，包括嵌套子查询和时间窗口。
- JOIN 语句的优化。新版本支持标准 SQL 语法所规定的多种 JOIN（CROSS、INNER、OUTER、NATURAL 等），同时允许 stream 和 materialized view 互相 JOIN 产生新的 stream。

## 监控改进

我们对 HStreamDB Prometheus exporter 进行了问题修复和更新，并提供了默认的 Grafana 监控面板，面板上包含多项 HStreamDB 的监控指标，方便用户更好的观察和掌握 HStreamDB 的运行状态。此外，HStreamDB 的集群部署工具 hdt [https://github.com/hstreamdb/deployment-tool](https://github.com/hstreamdb/deployment-tool)  也新增了对上述监控栈的一键部署支持。

![Grafana](https://assets.emqx.com/images/20ceea8d2c4a11e7e77efeae4a9f7607.png)

![Grafana](https://assets.emqx.com/images/5c07811720dbafe23dae15ad5990ebd6.png)

## Clients 及 CLI 更新

### Java Client

- 新增 StreamBuilder
- 修复 BufferedProducer 内存释放不及时的问题
- 使用 directExecutor 作为 grpcChannel 的默认 executor
- 修复 Reader的读取结果中缺少 RecordId 的问题
- 修复通过 maven 使用 hstreamdb-java 时的依赖冲突问题

### Go Client

- 新增 TLS 支持
- 新增对端到端压缩的支持，包括：gzip 和 zstd
- 新增集成测试和单元测试

### Python Client

- 新增对端到端压缩的支持，目前仅支持 gzip

### Rust Client

- 新增 TLS 支持
- 新增 shard reader 实现
- 优化了 client 用户 API
- 优化了 buffer producer 实现，修复了已知 bug

### CLI

- 新增 stream subcommands

## HStream IO 新增对 MongoDB 的支持

HStream IO 增加了 MongoDB 的 source 和 sink connectors，支持从 MongoDB 实时摄取增量的数据到 HStreamDB 以及将 HStreamDB 的数据实时导出到 MongoDB，相关使用和配置可参考文档：[source-mongodb configuration](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/source_mongodb_spec.md)，[sink-mongodb configuration](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_mongodb_spec.md)。

## 即刻体验

有关 HStreamDB 0.10 的更新详情请查看 [https://hstream.io/docs/en/latest/release_notes/HStreamDB.html#v0-10-0-2022-10-28](https://hstream.io/docs/en/latest/release_notes/HStreamDB.html#v0-10-0-2022-10-28) ，欢迎大家下载使用，向我们提供您的宝贵意见。
