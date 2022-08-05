HStreamDB 最新版本 v0.9 现已正式发布！

v0.9 主要有以下亮点更新：

- stream 分区模型扩展，支持用户直接访问分区上指定位置的数据；
- 新增 HStreamDB 的内部数据集成框架 HStream IO；
- 集群转用基于 SWIM 的成员发现和故障检测机制；
- 全新的流处理引擎；
- 升级了 Java 和 Go 客户端，并新增了 Python 客户端。

## Stream 分区模型扩展

v0.9 对之前的分区模型进行了扩展，允许用户直接操作和访问 stream 内部的分区，从而可以对 stream 中的数据分布和分区伸缩进行精细化控制。HStreamDB 采用的是 key-range-based 分区机制，stream 下的所有分区共同划分整个 key space，每个分区归属一段连续的子空间(key range)。若 record 所带 partitionKey 的哈希值落在某个子空间内，那么这条 record 将会被存储在对应的分区中。

具体地，v0.9 的分区模型新增了以下能力:

- 在创建 stream 的时候配置初始分区数
- 通过  `partitionKey` 将写入的 record 分发到相应的 stream 的分区
- 直接从任意位置读取指定分区的数据
- 查看 stream 包含的分区和各个分区对应的 key range

在之后的版本中，我们将支持通过分区分裂和合并对 stream 进行动态伸缩。

## HStream IO 发布

HStream IO 是 v0.9 包含的一个内部数据集成框架，包含 source connectors、sink connectors、IO runtime 等组件，它能够实现 HStreamDB 和多种外部系统的互联互通，促进数据在整个企业数据栈内的高效流转以及实时价值释放。

v0.9 提供了以下的 connectors，可支持多种数据库之间的增量同步。

Source connectors: 

- [source-mysql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_mysql_spec.md) 
- [source-postgresql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/source_postgresql_spec.md) 
- [source-sqlserver](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/source_sqlserver_spec.md) 

Sink connectors:

- [sink-mysql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_mysql_spec.md)
- [sink-postgresql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_postgresql_spec.md)

用户可以通过对应的 SQL commands 创建和管理 IO task，具体可参考[文档](https://hstream.io/docs/en/latest/io/overview.html)了解 HStream IO 的功能和使用。

## 新的流处理引擎

v0.9 基于迭代和差分计算原理重新实现了流处理引擎，显著提升了吞吐量，并降低了延迟。此外，新的引擎还支持多路 Join 语句、子查询(sub-queries)和更普适的物化视图(materialized view)。

该特性仍然处于开发阶段，属于实验性的功能，用户可以参考[ SQL 指南](https://hstream.io/docs/en/latest/guides/sql.html) 进行试用。

## 基于 Gossip 的 HServer 集群

v0.9 对 HServer 的集群实现进行了重构，新的实现主要采用了 gossip style 的集群机制和基于 SWIM 的故障检测机制，取代了上一版本中基于 ZooKeeper 的实现。新的实现将提高集群的可扩展性，并减少对外部系统的依赖。

## Advertised Listeners

生产中的部署和使用可能涉及复杂的网络设置。例如，如果服务器集群是内部托管的，它需要一个外部可见的 IP 地址让客户连接到集群，尤其是当遇到使用 docker 或者云托管等情况，会使环境更加复杂。

为了确保来自不同网络环境的客户端能够与集群进行交互，HStreamDB 0.9 支持配置 advertised listerners。在配置了 advertised listerners 后，服务器可以根据客户端发送请求的端口，为不同的客户端返回相应的地址。

## 统一的 HStream CLI

为了使 CLI 更加统一和简易，我们已经将旧的 HStream SQL Shell 和其他一些节点管理功能迁移到新的 HStream CLI。HStream CLI 目前支持启动交互式 SQL Shell、发送集群 bootstrap 请求和检查服务器节点状态等功能。用户可以通过参考 [CLI 文档](https://hstream.io/docs/en/latest/cli/cli.html)了解具体的使用方法。

## 基于 Grafana 的监控

v0.9 新增了通过 Prometheus 和 Grafana 对 HStreamDB 集群进行监控的支持，HStreamDB 内部的 Metrics 将通过 exporter 存储到 Prometheus 并最终展示在 Grafana 面板上。具体的部署和使用流程可以参考[文档](https://hstream.io/docs/en/latest/monitoring/grafana.html#installations-and-set-up)。

## 支持用 Helm 在 K8s 上进行部署

v0.9 提供了 HStreamDB 的 Helm Chart，现在可通过 Helm 在 K8s上快速部署 HStreamDB 集群，更加详细的使用步骤可以参考[文档](https://hstream.io/docs/zh/latest/deployment/deploy-helm.html)。

## 客户端版本升级和改进

Java 客户端 v0.9.0、Go 客户端 v0.2.0、Python 客户端 v0.2.0 均已发布，提供对 HStreamDB 0.9 的支持。详情请见：

- Java 客户端 v0.9.0：[https://github.com/hstreamdb/hstreamdb-java/releases/tag/v0.9.0](https://github.com/hstreamdb/hstreamdb-java/releases/tag/v0.9.0) 
- Go 客户端 v0.2.0：[https://github.com/hstreamdb/hstreamdb-go/releases/tag/v0.2.0](https://github.com/hstreamdb/hstreamdb-go/releases/tag/v0.2.0) 
- Python 客户端 v0.2.0：[https://github.com/hstreamdb/hstreamdb-py/releases/tag/v0.2.0](https://github.com/hstreamdb/hstreamdb-py/releases/tag/v0.2.0)
