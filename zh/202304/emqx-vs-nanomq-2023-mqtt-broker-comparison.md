**目录**

- [引言](#引言)
- [EMQX 简介](#emqx-简介)
- [NanoMQ 简介](#nanomq-简介)
- [社区情况](#社区情况)
- [功能特性](#功能特性)
- [扩展性和性能](#扩展性和性能)
- [可操作性和可观测性](#可操作性和可观测性)
- [数据集成](#数据集成)
- [桥接 NanoMQ 到 EMQX](#桥接-nanomq-到-emqx)
- [结语](#结语)

## 引言

[EMQX](https://www.emqx.io/zh) 和 [NanoMQ](https://nanomq.io/zh) 都是由全球领先的开源物联网数据基础设施软件供应商 EMQ 开发的开源 MQTT Broker。

EMQX 是一个高度可扩展的大规模分布式 MQTT Broker，能够将百万级的物联网设备连接到云端。NanoMQ 则是专为物联网边缘场景设计的轻量级 Broker。

本文中我们将对 EMQX 和 NanoMQ 这两个 Broker 进行详细的对比分析。

## EMQX 简介

EMQX 是目前全球最具扩展性的 MQTT 消息服务器，广泛用于物联网、工业物联网（IIoT）和车联网（IoV）等各类关键业务场景。其使用 Erlang/OTP 开发，采用了去中心化的分布式架构，具有高可用性并且支持横向扩展。

最新版本 EMQX 5.0 能够通过一个由 23 个节点组成的集群，支持高达 1 亿的 MQTT 并发连接。

了解详情请浏览：[高度可扩展，EMQX 5.0 达成 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0) 

![MQTT 集群](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png)

**优点**

- 支持大规模部署
- 支持集群，高度可扩展
- 高性能和高可靠
- 提供丰富的企业级功能
- 开箱即用的数据集成功能

缺点：

- 上手复杂
- 难以有效管理

## NanoMQ 简介

NanoMQ 是一个轻量级的 MQTT Broker，专为 IoT 边缘场景设计。它采用纯 C 语言编写，基于 NNG 的异步 I/O 多线程 Actor 模型，完全支持 MQTT 3.1.1 和 MQTT 5.0。

在单节点的场景下，NanoMQ 表现出很高的性能。其最为吸引人的优点是其轻便小巧，具备高度的可移植性和兼容性。它可以部署在任何支持 POSIX 标准的平台上，并且可以在多种 CPU 架构上运行，包括 x86_64、ARM、MIPS 和 RISC-V 等等。

![NanoMQ MQTT Broker 架构图](https://assets.emqx.com/images/892a0de52bd6288686aec1f0bbc330d9.png)

**优点**

- 设计轻巧
- 具有高度的轻便性
- 占用启动空间小
- 部署方便
- 能够与无代理协议桥接

**缺点**

- 不支持水平扩展
- 社区和用户群规模较小
- 文档和教程不多
- 不支持集群
- 缺少企业级功能（如数据集成）

<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>


## 社区情况

EMQX 和 NanoMQ 两个开源项目都托管在 GitHub 上。EMQX 自 2012 年推出以来，已经成为最受欢迎的 MQTT Broker 之一，目前 Star 数为 11.4k 。NanoMQ 是一个于 2020 年发起的新项目，处于初期阶段，目前有 800+ Star。这两个项目都在持续开发中，在过去的 12 个月里有数千次  Commit 提交。

|                                     | **EMQX**                                    | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------ | :---------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [NanoMQ GitHub](https://github.com/emqx/nanomq) |
| **Project Created**                 | 2012                                        | 2020                                            |
| **License**                         | Apache Version 2.0                          | The MIT License                                 |
| **Latest Release**                  | v5.0.21 (March 2023)                        | v0.17.0 (March 2023)                            |
| **GitHub Stars**                    | 11.4k                                       | 800+                                            |
| **GitHub Forks**                    | 2k                                          | 100+                                            |
| **GitHub Commits**                  | 14k+                                        | 2k+                                             |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 1200+                                           |
| **GitHub Releases**                 | 260+                                        | 75+                                             |
| **GitHub PRs**                      | 6000+                                       | 780+                                            |
| **GitHub Contributors**             | 100+                                        | 20+                                             |

## 功能特性

EMQX 和 NanoMQ 都完全遵循 MQTT 3.1.1 和 MQTT 5.0 规范，支持 [MQTT over WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket) 和 SSL/TLS 加密，并且是率先支持 MQTT 新一代协议 [MQTT Over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 的 Broker。

EMQX 提供多个协议网关支持，包括 LwM2M/CoAP、MQTT-SN 和 Stomp。而 NanoMQ 则支持将边缘场景中去中心化的协议如 DDS、ZeroMQ 和 Nanomsg/NNG 等转换成 MQTT 消息并与云端桥接。

两者都支持多种身份认证方式，包括用户名密码、JWT。EMQX 还额外支持 OAuth 2.0 身份验证和 IP 白名单/黑名单。

在企业级功能方面，[EMQX 企业版](https://www.emqx.com/zh/products/emqx)提供了强大的规则引擎和数据桥接功能，可以轻松地与 Kafka、SQL、NoSQL 数据库和云服务进行集成。

|                          | **EMQX**                            | **NanoMQ**  |
| :----------------------- | :---------------------------------- | :---------- |
| **MQTT 3.1.1**           | ✅                                   | ✅           |
| **MQTT 5.0**             | ✅                                   | ✅           |
| **MQTT over TLS**        | ✅                                   | ✅           |
| **MQTT over WebSocket**  | ✅                                   | ✅           |
| **MQTT over QUIC**       | ✅                                   | ✅           |
| **LwM2M/CoAP**           | ✅                                   | ❌           |
| **MQTT-SN**              | ✅                                   | ❌           |
| **Stomp**                | ✅                                   | ❌           |
| **MQTT Bridging**        | ✅                                   | ✅           |
| **DDS Gateway**          | ❌                                   | ✅           |
| **ZeroMQ Gateway**       | ❌                                   | ✅           |
| **Nanomsg/NNG**          | ❌                                   | ✅           |
| **Authentication & ACL** | ✅                                   | ✅           |
| **Message Persistence**  | ✅ In RocksDB and external databases | ✅ In SQLite |
| **WebHook**              | ✅                                   | ✅           |
| **Rule Engine**          | ✅                                   | ✅           |
| **Data Integration**     | ✅                                   | ❌           |

## 扩展性和性能

EMQX 因其极高的可扩展性和优异性能成为大规模物联网关键业务项目的首选。此外，其分布式的集群架构还保证了高可用性。

NanoMQ 基于 NNG 的异步 I/O 和多线程模型，具有优秀的轻量级设计。它能够有效地利用 CPU 和内存资源，在现代 SMP 系统上可以良好的支持多内核，并且其启动占用空间不到 200k，具有小巧高效的特点。

简而言之，两者在性能、扩展性和可靠性方面与其他 MQTT Broker 相比都有很大的优势。

|                                              | **EMQX**                                                     | **NanoMQ**                                                   | **Notes and Links**                                          |
| :------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Clustering**                               | ✅ 20+ nodes of cluster                                       | ❌                                                            | [EMQX Cluster](https://www.emqx.io/docs/en/v5.0/deploy/cluster/introduction.html) |
| **Scalability**                              | 4M MQTT connections per node<br>100M MQTT connections per cluster | 200k MQTT connections per node                               | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | 2 million QoS0 MQTT msgs/sec per node<br>800k QoS1 msgs/sec<br>200k QoS2 msgs/sec | Up to 1 million+ QoS0 MQTT msgs/sec per node<br>500k QoS1 msgs/sec<br>180k QoS2 msgs/sec |                                                              |
| **Latency**                                  | 1~5 millisecond                                              | 1～5 millisecond                                             |                                                              |
| **Booting footprint**                        | 30Mb+                                                        | 200Kb+                                                       |                                                              |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | ❌                                                            |                                                              |
| **Auto Clustering**                          | ✅                                                            | ❌                                                            |                                                              |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            | ❌                                                            |                                                              |

## 可操作性和可观测性

EMQX 拥有用户友好的 Dashboard 和丰富的 HTTP API，支持通过 StatsD、Prometheus 和 Grafana 进行监控。NanoMQ 部署简单、配置方便、管理便捷，但它在管理和监控方面还不够完善。

这两个 Broker 都相对容易使用，但是 NanoMQ 的极简设计更利于初学者学习和掌握 MQTT。

|                         | **EMQX**     | **NanoMQ**   | **Notes and Links**                                          |
| :---------------------- | :----------- | :----------- | :----------------------------------------------------------- |
| **Configuration**       | HOCON Format | HOCON Format |                                                              |
| **HTTP API**            | ✅            | ✅            | [REST API](https://www.emqx.io/docs/en/v5.0/admin/api.html)  |
| **CLI**                 | ✅            | ✅            | [Command Line Interface](https://www.emqx.io/docs/en/v5.0/admin/cli.html) |
| **Dashboard**           | ✅            | ❌            | [EMQX Dashboard](https://www.emqx.io/docs/en/v5.0/getting-started/dashboard.html) |
| **Grafana**             | ✅            | ❌            | [Integrate with Prometheus](https://www.emqx.io/docs/en/v5.0/observability/prometheus.html) |
| **Prometheus**          | ✅            | ❌            | [Integrate with Prometheus](https://www.emqx.io/docs/en/v5.0/observability/prometheus.html) |
| **StatsD**              | ✅            | ❌            | [Integrate with StatsD](https://www.emqx.io/docs/en/v5.0/observability/statsd.html#statsd) |
| **Cross Platform**      | ✅            | ✅            |                                                              |
| **Docker**              | ✅            | ✅            | [EMQX Docker](https://hub.docker.com/r/emqx/emqx) - [NanoMQ Docker](https://hub.docker.com/r/emqx/nanomq) |
| **Kubernetes Operator** | ✅            | ❌            | [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) |
| **Terraform**           | ✅            | ❌            |                                                              |

## 数据集成

NanoMQ 作为一个轻量级 Broker，没有提供数据集成功能。而 EMQX 提供了丰富的数据集成，特别是运行在云端的企业版，可以通过内置的数据桥接功能与 Kafka、数据库和云服务实现无缝集成。

|                     | **EMQX**               | **NanoMQ** | **Notes and Links**                                          |
| :------------------ | :--------------------- | :--------- | :----------------------------------------------------------- |
| **Rule Engine**     | ✅                      | ✅Limited   | [EMQX Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) |
| **Data Bridge**     | ✅                      | ❌          | [Data bridges](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridges.html) |
| **Confluent/Kafka** | ✅ (Enterprise Edition) | ❌          | [Bridge data to Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html) |
| **SAP Event Mesh**  | ✅(Enterprise Edition)  | ❌          | [Ingest Data into SAP Event Mesh](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_sap_event_mesh.html#bridge-data-to-sap-event-mesh) |
| **Apache Pulsar**   | ✅(Enterprise Edition)  | ❌          | [Bridge data to Pulsar](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_pulsar.html) |
| **RabbitMQ**        | ✅(Enterprise Edition)  | ❌          | [Bridge data to RabbitMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rabbitmq.html) |
| **MySQL**           | ✅(Enterprise Edition)  | ❌          | [EMQX MySQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mysql.html) |
| **PostgreSQL**      | ✅(Enterprise Edition)  | ❌          | [Ingest Data to PostgreSQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_pgsql.html) |
| **SQL Server**      | ✅(Enterprise Edition)  | ❌          | [Ingest Data to SQLServer](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_sqlserver.html) |
| **MongoDB**         | ✅(Enterprise Edition)  | ❌          | [Ingest Data to MongoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mongodb.html) |
| **Redis**           | ✅(Enterprise Edition)  | ❌          | [Ingest Data to Redis](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_redis.html) |
| **Cassandra**       | ✅(Enterprise Edition)  | ❌          | [Ingest Data to Cassandra](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_cassandra.html) |
| **AWS DynamoDB**    | ✅(Enterprise Edition)  | ❌          | [Ingest Data to DynamoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_dynamodb.html) |
| **ClickHouse**      | ✅(Enterprise Edition)  | ❌          | [Ingest Data to ClickHouse](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_clickhouse.html) |
| **InfluxDB**        | ✅(Enterprise Edition)  | ❌          | [Ingest Data to InfluxDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_influxdb.html) |
| **TimeScaleDB**     | ✅(Enterprise Edition)  | ❌          | [Ingest Data to TimescaleDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_timescaledb.html) |
| **Oracle**          | ✅(Enterprise Edition)  | ❌          | [Ingest Data to Oracle](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_oracle.html) |

 

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## 桥接 NanoMQ 到 EMQX

我们可以将 NanoMQ 部署在物联网边缘端的小型设备或网关上，然后通过桥接功能把数据汇总和传输到云端的大型 EMQX 集群。

![将 NanoMQ 桥接到 EMQX](https://assets.emqx.com/images/a2fc8b04a0059369d61507f4cb7dbf63.png)

## 结语

EMQX 和 NanoMQ 是当前最活跃的 MQTT Broker 项目，拥有优秀的开源社区和商业支持。 

EMQX 凭借其扩展性、可靠性和丰富的功能，成为物联网关键业务云端 MQTT 消息服务的首选。而轻量、高效、低成本的 NanoMQ 则更适用于工业物联网和边缘物联网应用。

您可以根据自己的需求和场景选择使用其中一个或两个配合使用。我们相信这两个 MQTT Broker 将在未来引领 MQTT 技术创新。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
