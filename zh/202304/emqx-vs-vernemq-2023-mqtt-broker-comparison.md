## 引言

[EMQX](https://www.emqx.io/zh) 和 [VerneMQ](https://vernemq.com/) 都是用 Erlang/OTP 开发的高性能、分布式开源 MQTT Broker，以其稳定性、容错性和扩展性著称。

EMQX 是目前全球最受欢迎的 MQTT Broker 之一，而 VerneMQ 项目近年来却没有积极地开发和维护。

本文是《2023 年 MQTT Broker 对比》系列博客的第四篇，我们将对这两个 Broker 进行简要的对比分析。

## EMQX 简介

EMQX 于 2012 年在 GitHub 发布，遵循 Apache 2.0 许可证。它旨在以百万级的并发连接为需要高可扩展性 MQTT Broker 的应用场景提供解决方案。

EMQX 是目前全球最具扩展性的 MQTT Broker。通过采用基于 [Mria+RLOG](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections) 的分布式架构，最新版本 EMQX 5.0 单个集群可支持至多 23 个节点，能够承载高达 1 亿的 MQTT 并发连接。

详情请浏览：[高度可扩展，EMQX 5.0 达成 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0) 

![MQTT Cluster](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png)

EMQX 提供了丰富的企业功能、数据集成、云托管服务以及来自 EMQ 公司的商业支持。多年来，EMQX 凭借其卓越的性能、可靠性和扩展性，在大型企业、创业公司和个人用户中赢得了广泛的认可，被广泛应用于物联网、[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)、智能汽车和电信等各个领域。

**优点：**

- 支持大规模部署
- 高可用
- 水平可扩展性
- 高性能和高可靠
- 提供丰富的企业功能
- 率先引入 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic)

**Cons:** **缺点：**

- 难以有效管理
- 配置较为复杂
- 日志不易理解

## VerneMQ 简介

VerneMQ 项目于 [2014](https://github.com/vernemq/vernemq/tree/3c7703f0d62e758ba22a34ceb756f2ac2a4da44a) 年启动，最初由 [Erlio GmbH](https://vernemq.com/company.html) 开发。它是第二个用 Erlang/OTP 编写的 MQTT Broker，遵循 Apache 2.0 许可证，[部分代码](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl)参考了 EMQX 项目。

在架构设计上，VerneMQ 支持使用 LevelDB 进行 MQTT 消息持久化，并采用基于 [Plumtree](https://github.com/lasp-lang/plumtree) 库的集群架构，该库实现了[Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf) 算法。

然而，尽管 Plumtree 集群架构从理论上看很完美，但其可行性尚未得到证明。VerneMQ 团队和社区花费了多年时间尝试解决系统存在的问题，如网络分裂、数据不一致和崩溃恢复等，但是取得的成果有限。

目前，该项目已不再积极地开发和维护，在过去的一年中只有大约 50 次提交。

**优点：**

- 高可用
- 水平可扩展性
- 支持消息持久化

**Cons:** **缺点：**

- 未经验证的集群架构
- 文档不足
- 企业功能有限
- 缺少开发维护

## 社区情况

EMQX 和 VerneMQ 项目都托管在 GitHub 上。EMQX 始于 2012 年，是最早且目前 Star 数最多的 MQTT Broker 之一，拥有 11.4k Stars。VerneMQ 项目创建于 2014 年，目前有 3k Stars。

| **Community & Users**               | **EMQX**                                    | **VerneMQ**                                          | **Notes and Links**                                          |
| :---------------------------------- | :------------------------------------------ | :--------------------------------------------------- | :----------------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [VerneMQ GitHub](https://github.com/vernemq/vernemq) |                                                              |
| **Product Created**                 | 2012                                        | 2014                                                 |                                                              |
| **License Mode**                    | Apache License 2.0                          | Apache License 2.0                                   |                                                              |
| **Latest Release**                  | v5.0.21 (March 2023)                        | v1.12.6.2 (Nov. 2022)                                |                                                              |
| **GitHub Stars**                    | 11.4k+                                      | 3k                                                   |                                                              |
| **GitHub Forks**                    | 2k                                          | 300+                                                 | [EMQX GitHub Forks](https://github.com/emqx/emqx/network/members)<br>[VerneMQ GitHub Forks](https://github.com/vernemq/vernemq/forks) |
| **GitHub Commits**                  | 14k+                                        | 2400+                                                | [EMQX GitHub Commits](https://github.com/emqx/emqx/commits)<br>[VerneMQ GitHub Commits](https://github.com/vernemq/vernemq/commits) |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 50+                                                  |                                                              |
| **GitHub Issues**                   | 3500+                                       | 1300+                                                | [EMQX GitHub Issues](https://github.com/emqx/emqx/issues?q=is%3Aissue+is%3Aall+) <br>[VerneMQ GitHub Issues](https://github.com/vernemq/vernemq/issues) |
| **GitHub PRs**                      | 6000+                                       | 600                                                  | [EMQX GitHub PRs](https://github.com/emqx/emqx/pulls) <br>[VerneMQ GitHub PRs](https://github.com/vernemq/vernemq/pulls) |
| **GitHub Releases**                 | 260+                                        | 40                                                   | [EMQX GitHub Releases](https://github.com/emqx/emqx/releases) <br>[VerneMQ GitHub Releases](https://github.com/vernemq/vernemq/releases) |
| **GitHub Contributors**             | 110+                                        | 50                                                   | [EMQX GitHub Contributors](https://github.com/emqx/emqx/graphs/contributors) <br>[VerneMQ GitHub Contributors](https://github.com/vernemq/vernemq/graphs/contributors) |
| **Docker Pulls**                    | 24M+                                        | 5M+                                                  | [EMQX Docker Pulls](https://hub.docker.com/r/emqx/emqx) <br>[VerneMQ Docker Pulls](https://hub.docker.com/r/vernemq/vernemq/) |

## 功能特性

EMQX 和 VerneMQ 都完整支持 MQTT 3.1.1 和 MQTT 5.0，支持 [MQTT over WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket) 和 SSL/TLS 加密。同时它们都支持多种身份认证方式，包括用户名密码、JWT、LDAP 和 OAuth 2.0。

EMQX 支持多个协议网关，包括 LwM2M/CoAP、MQTT-SN 和 Stomp。EMQX 5.0 引领了 MQTT over QUIC 技术，MQTT over QUIC 通过多路复用、更快的连接建立和迁移等特性，有望成为下一代 MQTT 标准。

此外，EMQX 还提供了一系列管理和集成功能，如 HTTP API、WebHook 和规则引擎。通过这些内置的数据桥接功能可以轻松地与 Kafka、SQL、NoSQL 数据库以及云服务进行集成。

|                          | **EMQX**                                                     | **VerneMQ**  |
| :----------------------- | :----------------------------------------------------------- | :----------- |
| **MQTT 3.1.1**           | ✅                                                            | ✅            |
| **MQTT 5.0**             | ✅                                                            | ✅            |
| **MQTT over TLS**        | ✅                                                            | ✅            |
| **MQTT over WebSocket**  | ✅                                                            | ✅            |
| **MQTT over QUIC**       | ✅                                                            | ❌            |
| **LwM2M/CoAP**           | ✅                                                            | ❌            |
| **MQTT-SN**              | ✅                                                            | ❌            |
| **Stomp**                | ✅                                                            | ❌            |
| **MQTT Bridging**        | ✅                                                            | ✅            |
| **Authentication & ACL** | ✅                                                            | ✅            |
| **Message Persistence**  | ✅ In RocksDB and external databases                          | ✅ In LevelDB |
| **WebHook**              | ✅                                                            | ✅            |
| **Rule Engine**          | ✅                                                            | ❌            |
| **Data Integration**     | ✅                                                            | ❌            |
| **Cloud Service**        | [Cloud Hosting](https://www.emqx.com/zh/cloud)<br>[Serverless MQTT](https://www.emqx.com/zh/cloud/serverless-mqtt)<br>[BYOC](https://www.emqx.com/zh/cloud/byoc) | ❌            |

## 扩展性和性能

EMQX 和 VerneMQ 都基于分布式架构，具有高性能、低延迟和可扩展的特点，都能够实现单集群百万级并发连接支持。

EMQX 已有超过 30000 个集群在生产环境中部署，具有经过验证的扩展性和可靠性。最新的 EMQX 5.0 在一个 23 个节点集群的基准测试中成功实现了 1 亿 MQTT 连接。

虽然 VerneMQ 在理论和设计上应该能够很好地工作，但关于其扩展性和性能的基准测试报告很少。您可以使用 MQTT 负载测试工具（例如 [emqtt-bench](https://github.com/emqx/emqtt-bench)、[emqttb](https://github.com/emqx/emqttb) 或 [XMeter 云服务](https://www.emqx.com/zh/products/xmeter)）对其进行基准测试。

|                                              | **EMQX**                                                     | **VerneMQ**                   | **Notes & Links**                                            |
| :------------------------------------------- | :----------------------------------------------------------- | :---------------------------- | :----------------------------------------------------------- |
| **Scalability**                              | 4M MQTT connections per node<br>100M MQTT connections per cluster | **?**                         | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | 4 million QoS0 MQTT msgs/sec per node<br>800k QoS1 msgs/sec<br>200k QoS2 msgs/sec | **?**                         |                                                              |
| **Latency**                                  | Single-digit millisecond latency in most scenarios                                              | Up to seconds latency in some scenarios                         |                                                              |
| **Reliability**                              | Message Persistence in RocksDB and external Database         | Message Persistence in LevelDB | [Highly Reliable MQTT Data Persistence Based on RocksDB](https://www.emqx.com/zh/blog/mqtt-persistence-based-on-rocksdb)<br>[VerneMQ Storage](https://docs.vernemq.com/configuring-vernemq/storage) |
| **Clustering**                               | 20+ nodes of cluster                                         | **?**                         | [EMQX Cluster Scalability](https://docs.emqx.com/en/emqx/v5.0/deploy/cluster/db.html#node-roles)<br>[Vernemq - Cluster](https://docs.vernemq.com/vernemq-clustering/introduction) |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | **?**                         |                                                              |
| **Auto Clustering**                          | ✅                                                            | **?**                         | [EMQX Node Discovery and Autocluster](https://docs.emqx.com/en/emqx/v5.0/deploy/cluster/intro.html#emqx-node-discovery-and-autocluster) |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            |                               | [EMQX Release Upgrade](https://docs.emqx.com/en/enterprise/v4.4/advanced/relup.html#release-upgrade) |

> **?** 代表对于表中对比的相关条目，我们未能找到任何公开的文档或资料。

## 数据集成（开箱即用）

VerneMQ 对 MQTT 数据集成的支持有限。用户可以通过编写插件，将数据导入外部数据库或云服务。

EMQX 内置了基于 SQL 的规则引擎，可以轻松实现在 Broker 内实时提取、过滤、处理和转换 MQTT 消息。

EMQX 企业版可以利用规则引擎和内置的数据桥接功能与 Kafka、数据库以及云服务实现无缝的数据集成。

| **Data Integrations** | **EMQX** | **VerneMQ** | **Notes and Links**                                          |
| :-------------------- | :------- | :---------- | :----------------------------------------------------------- |
| **Rule Engine**       | ✅        | ❌           | [Introduction to Data Integration](https://docs.emqx.com/en/emqx/v5.0/data-integration/introduction.html) |
| **Message Codec**     | ✅        | ❌           | [Introduction to Schema Registry](https://docs.emqx.com/en/enterprise/v4.4/rule/schema-registry.html) |
| **Data Bridge**       | ✅        | ❌           | [Data Bridges](https://docs.emqx.com/en/emqx/v5.0/data-integration/data-bridges.html) |
| **MQTT Bridging**       | ✅        | ✅           | [Bridge Data into MQTT Broker](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-mqtt.html)<br>[MQTT Bridge](https://docs.vernemq.com/configuring-vernemq/bridge) |
| **Webhook**           | ✅        | ✅           | [Ingest Data into Webhook](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-webhook.html)<br>[Webhooks](https://docs.vernemq.com/plugin-development/webhookplugins) |
| **Kafka/Confluent**   | ✅        | **?**       | [Bridge data to Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html)<br>[GitHub - crisrise/vmq_kafka: A VerneMQ plugin that sends all published messages to Apache Kafka](https://github.com/crisrise/vmq_kafka) |
| **Azure Event Hubs**  | ✅        | ❌           | [Stream Data into Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html) |
| **Apache Pulsar**     | ✅        | ❌           | [Ingest Data into Pulsar](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_pulsar.html) |
| **Apache RocketMQ**   | ✅        | ❌           | [Ingest Data into RocketMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rocketmq.html) |
| **RabbitMQ**          | ✅        | ❌           | [Ingest Data into RabbitMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rabbitmq.html) |
| **MySQL**             | ✅        | ❌           | [Ingest Data into MySQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mysql.html) |
| **PostgreSQL**        | ✅        | ❌           | [Ingest Data into PostgreSQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_pgsql.html) |
| **SQL Server**        | ✅        | ❌           | [Ingest Data into SQL Server](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_sqlserver.html) |
| **MongoDB**           | ✅        | ❌           | [Ingest Data into MongoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mongodb.html) |
| **Redis**             | ✅        | ❌           | [Ingest Data into Redis](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_redis.html) |
| **Cassandra**         | ✅        | ❌           | [Ingest Data into Cassandra](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_cassandra.html) |
| **AWS DynamoDB**      | ✅        | ❌           | [Ingest Data into DynamoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_dynamodb.html) |
| **ClickHouse**        | ✅        | ❌           | [Ingest Data into ClickHouse](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_clickhouse.html) |
| **OpenTSDB**          | ✅        | ❌           | [Ingest Data into OpenTSDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_opentsdb.html) |
| **InfluxDB**          | ✅        | ❌           | [Ingest Data into InfluxDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_influxdb.html) |
| **TimeScaleDB**       | ✅        | ❌           | [Ingest Data into TimescaleDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_timescaledb.html) |
| **Oracle DB**         | ✅        | ❌           | [Ingest Data into Oracle](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_oracle.html) |
| **HStreamDB**         | ✅        | ❌           | [Stream Data into HStreamDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_hstreamdb.html) |

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## 扩展开发

EMQX 和 VerneMQ 都支持使用钩子和插件实现灵活的扩展。此外，EMQX 还提供了多协议网关扩展，使用户能够开发新的连接协议。

| **Extensibility**      | **EMQX** | **VerneMQ** | **Notes and Links**                                          |
| :--------------------- | :------- | :---------- | :----------------------------------------------------------- |
| **Hooks**              | ✅        | ✅           | [Hooks](https://docs.emqx.com/en/enterprise/v4.4/advanced/hooks.html#definition) |
| **Plugins**            | ✅        | ✅           | [Plugins](https://docs.emqx.com/en/enterprise/v4.4/advanced/plugins.html#list-of-plugins)<br>[Plugin Development](https://docs.vernemq.com/plugin-development/introduction) |
| **Plugin Hot-loading** | ✅        | ✅           |                                                              |
| **Gateways**           | ✅        | ❌           | [Gateway Introduction](https://docs.emqx.com/en/emqx/v5.0/gateway/gateway.html) |
| **ExHooks/gRPC**       | ✅        | ❌           | [gRPC Hook Extension](https://docs.emqx.com/en/emqx/v5.0/advanced/lang-exhook.html) |

## 可操作性和可观测性

EMQX 拥有易用的 Dashboard 和丰富的 HTTP API，支持通过 Prometheus 和 Grafana 进行监控。而 VerneMQ 部署简单、配置方便，但它在管理和监控方面还不够完善。

|                                  | **EMQX**     | **VerneMQ**     | **Notes and Links**                                          |
| :------------------------------- | :----------- | :-------------- | :----------------------------------------------------------- |
| **Dashboard**                    | ✅            | ❌               | [Dashboard](https://docs.emqx.com/en/emqx/v5.0/getting-started/dashboard.html) |
| **Configuration**                | HOCON Format | Key-Value Fomat |                                                              |
| **HTTP API**                     | ✅            | ✅               | [REST API](https://docs.emqx.com/en/emqx/v5.0/admin/api.html)  |
| **CLI**                          | ✅            | ✅               | [Command Line Interface](https://docs.emqx.com/en/emqx/v5.0/admin/cli.html) |
| **Config Hot update**            | ✅            | ❌               | [Configuration Files](https://docs.emqx.com/en/emqx/v5.0/admin/cfg.html) |
| **Metrics**                      | ✅            | ✅               | Node metrics:<br>[Metrics](https://docs.emqx.com/en/emqx/v5.0/observability/metrics-and-stats.html)<br>[$SYSTree](https://docs.vernemq.com/monitoring/systree)<br>[Monitor - Metrics CLI](https://docs.vernemq.com/monitoring/introduction) |
| **Grafana**                      | ✅            | ✅               | [EMQX \| Grafana Labs](https://grafana.com/grafana/dashboards/17446-emqx/)<br>[VerneMQ Node Metrics \| Grafana Labs](https://grafana.com/grafana/dashboards/16479-vernemq-node-metrics/) |
| **Cluster Metrics**              | ✅            | ✅               | [Metrics](https://docs.emqx.com/en/emqx/v5.0/observability/metrics-and-stats.html)<br>[Monitor - Metrics CLI](https://docs.vernemq.com/monitoring/introduction) |
| **Alarm Alerts**                 | ✅            | ❌               | [System Topic](https://docs.emqx.com/en/emqx/v5.0/advanced/system-topic.html#alarms-system-alarms) |
| **Slow Subscription Monitoring** | ✅            | ❌               | [Slow subscribers statistics](https://docs.emqx.com/en/emqx/v5.0/observability/slow_subscribers_statistics.html) |
| **Prometheus**                   | ✅            | ✅               | [Integrate with Prometheus](https://docs.emqx.com/en/emqx/v5.0/observability/prometheus.html#dashboard-update)<br>[Prometheus](https://docs.vernemq.com/monitoring/prometheus) |

## 结语

简而言之，EMQX 是 2023 年在生产环境中部署 MQTT Broker 的最佳选择之一。如果想要深入了解分布式 MQTT Broker 的设计原理和实现难点，可以参考 [EMQX](https://github.com/emqx/emqx) 和 [VerneMQ](https://github.com/vernemq/vernemq) 在 GitHub 上的源代码。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
