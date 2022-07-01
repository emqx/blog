本月，HStreamDB 团队专注于 v0.9 的开发工作，目前已经完成了 HServer 去中心化集群的切换、HStream IO Embedded Runtime 和 CDC Source Connector 的开发， 并带来了新的 Grafana 监控集成以及正式发布了首个可用的 Python 客户端。另外，还与 EMQX 团队协作完成了 HStreamDB 与 EMQX 的集成。

## HServer 采用新的集群机制

目前我们已经初步完成将 HServer 集群机制从基于 ZooKeeper 的中心化方案切换到基于 SWIM[1] 的去中心化方案，其主要目的是为了支持更大的集群和更好的扩展性，同时减少对外部系统的依赖。后续我们将继续对新集群机制进行更多测试和完善，这一特性将在 v0.9 中正式发布。

## HStream IO 支持 CDC Source

HStream IO 是 HStreamDB v0.9 即将发布一个内部数据集成框架，包含 source connectors、sink connectors、IO Runtime 等组件，它能够实现 HStreamDB 和多种外部系统的互联互通，从而助力促进数据在整个企业数据栈内的高效流转以及实时价值释放。

本月我们完成了 Embedded IO Runtime 以及多种数据库的 CDC Source Connector 的开发，包括：MySQL、PostgreSQL、SQL Server 等，能够高效实现将这些数据库的数据增量、实时地同步到 HStreamDB。

## 新增 Grafana 监控集成

为了方便用户运维和管理 HStreamDB 集群，我们新增了基于 Prometheus 和 Grafana 的监控支持，这也是目前业界主流的监控方案。HStreamDB 内部的监控数据会通过 Exporter 存储到 Prometheus，然后通过 Grafana 的面板进行可视化展示，当前效果如下图所示。

关于监控相关的更多内容请参考文档 [https://hstream.io/docs/en/latest/monitoring/grafana.html](https://hstream.io/docs/en/latest/monitoring/grafana.html) 

![HStream Grafana](https://assets.emqx.com/images/2f4672f1e6f7d9bb280d195cb61779f8.png)

## Python 客户端正式发布

本月我们正式发布了 HStreamDB 的 Python 客户端 hstreamdb-py [https://github.com/hstreamdb/hstreamdb-pyy](https://github.com/hstreamdb/hstreamdb-py)  v0.1.0，支持 HStreamDB v0.8，目前已经具备数据批量写入、订阅消费以及资源管理等核心功能，欢迎大家使用并反馈建议。

相关安装指令可参考 [https://pypi.org/project/hstreamdb/](https://pypi.org/project/hstreamdb/) ，更多使用文档参见 [https://hstreamdb.github.io/hstreamdb-py/](https://hstreamdb.github.io/hstreamdb-py/)

## 支持与 EMQX 集成

EMQX 是由 EMQ 开发的全球领先的开源 MQTT 消息服务器，在物联网领域有着广泛应用。本月通过与 EMQX 研发团队合作，我们完成了 EMQX 与 HStreamDB 的高效集成，这将助力用户实现一站式的物联网设备连接、数据接入、持久化存储和实时分析。具体可参考 [https://www.emqx.com/zh/blog/integration-practice-of-emqx-and-hstreamdb](https://www.emqx.com/zh/blog/integration-practice-of-emqx-and-hstreamdb)

 

[1]：Das, A., Gupta, I. and Motivala, A., 2002, June. Swim: Scalable weakly-consistent infection-style process group membership protocol. In *Proceedings International Conference on Dependable Systems and Networks* (pp. 303-312). IEEE.
