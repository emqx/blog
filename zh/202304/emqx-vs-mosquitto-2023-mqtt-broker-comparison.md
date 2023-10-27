## 引言

物联网开发者需要为自己的物联网项目选择合适的 MQTT 消息产品或服务，从而构建可靠高效的基础数据层，保障上层物联网业务。目前市面上有很多开源的 MQTT 产品，在性能功能等方面各有优点。本文将选取目前最为流行的两个开源 MQTT Broker：[EMQX](https://www.emqx.io/zh) 和 [Mosquitto](https://mosquitto.org/)，从技术架构、性能、功能、社区情况等多维度进行 1v1 对比，帮助读者更加深入了解这两个产品。 

## Mosquitto 简介

[Mosquitto](https://github.com/eclipse/mosquitto) 项目最初由 Roger Light 于 2009 年开发，后来捐赠给了 Eclipse 基金会。Eclipse Mosquitto 基于 Eclipse 公共许可证(EPL/EDL license)发布，用户可以免费使用。作为全球使用最广的 MQTT 协议实现之一 ，截至 2023 年 3 月，Mosquitto 的 GitHub Star 数超过了 7.1 K。

Mosquitto 用 C/C++ 编写，采用单线程架构。Mosquitto 支持 MQTT 协议的 5.0、3.1.1 和 3.1 版本，同时支持 SSL/TLS 和 WebSockets。轻量级设计使其适合部署在嵌入式设备或资源有限的服务器上。

优点：

- 易于安装使用
- 支持 MQTT 5.0 协议
- 轻量高效
- 积极的社区支持

缺点：

- 可扩展性有限（<100k）
- 没有集群支持
- 缺少企业功能
- 有限的云原生支持

## EMQX 简介

[EMQX](https://github.com/emqx/emqx) 项目于 2012 年底在 Github 发布，许可证为 Apache2，如今已成为世界上最具扩展性的 MQTT 消息服务器，被广泛应用于物联网、车联网、[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)等各类关键业务场景。

EMQX 采用 Erlang/OTP 编写，这是一种用于构建大规模可扩展软实时系统的编程语言。与 Mosquitto 不同，EMQX 在设计之初即采用了分布式集群架构，可以轻松实现弹性水平扩展，从而稳定承载大规模的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)接入。最新版本 EMQX 5.0 可在 23 个节点的单集群中建立 1 亿个并发的 MQTT 连接。

优点：

- 支持大规模部署
- 高可用性
- 横向可扩展性
- 高性能和高可靠
- 丰富的企业功能 
- 率先采用 MQTT over QUIC 

缺点：

- 上手相对复杂
- 难以有效管理

## 社区情况

EMQX 是 GitHub 上最活跃、Star 数最高的 MQTT Broker 项目，在过去 12 个月里有 11.4K 个 Star 和超过 3000 个 Commit。

Mosquitto 以其轻量级的单线程架构在部署上比 EMQX 更普遍，特别是在资源有限的嵌入式设备上。

|                                     | **EMQX**                                    | **Mosquitto**                                                |
| :---------------------------------- | :------------------------------------------ | :----------------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto)     |
| **Project Created**                 | 2013                                        | 2009                                                         |
| **License**                  | Apache License 2.0                        | EPL/EDL License                                            |
| **GitHub Stars**                    | 11.4k                                       | 7.2 k                                                        |
| **GitHub Forks**                    | 2k                                          | 2.1k                                                         |
| **GitHub Commits**                  | 14k+                                        | 2.8k+                                                        |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 500+ ([Eclipse Mosquitto™](https://projects.eclipse.org/projects/iot.mosquitto) ) |
| **GitHub Issues**                   | 3500+                                       | 2200+                                                        |
| **GitHub Releases**                 | 260+                                        | 60+                                                          |
| **GitHub PRs**                      | 6000+                                       | 600                                                          |
| **GitHub Contributors**             | 100+                                        | 110+                                                         |

<center>以上数据截至 2023-03-24</center>


## 性能与可扩展性

Mosquitto 作为一个轻量级 MQTT 消息中间件有着比较优秀的单节点性能，单机可以支撑 10w 级别的设备并发连接。但不支持集群架构。

EMQX 作为可集群部署的大规模消息服务器，单节点可以支持百万级并发连接，单集群支持亿级并发连接。但 CPU 和内存使用率更高。

|                                              | **EMQX**                                                     | **Mosquitto**                                                | **Notes & Links**                                            |
| :------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Scalability**                              | - 4M MQTT connections per node<br>- 100M MQTT connections per cluster | <100K MQTT connections per node                              | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | - 2 million QoS0 MQTT msgs/sec per node<br>- 800k QoS1 msgs/sec<br>- 200k QoS2 msgs/sec | - Up to 120k QoS0 MQTT msgs/sec per node<br>- 80k QoS1 msgs/sec<br> - 60k QoS2 msgs/sec |                                                              |
| **Latency**                                  | Single-digit millisecond latency at scale                                              | Up to seconds latency in some scenarios                                          |                                                              |
| **Clustering**                               | 20+ nodes of cluster                                         | ❌                                                            | [Cluster Scalability](https://www.emqx.io/docs/en/v5.0/deploy/cluster/db.html#node-roles) |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | ❌                                                            |                                                              |
| **Auto Clustering**                          | ✅                                                            | ❌                                                            | [EMQX Node Discovery and Autocluster](https://www.emqx.io/docs/en/v5.0/deploy/cluster/intro.html#emqx-node-discovery-and-autocluster) |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            | ❌                                                            | [Release Upgrade](https://docs.emqx.com/en/enterprise/v4.4/advanced/relup.html#release-upgrade) |

<section class="promotion">
    <div>
        EMQX 是如何支持单集群亿级 MQTT 并发连接的？
    </div>
    <a href="https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0" class="button is-gradient px-5">点击查看详细测试过程 →</a>
</section>

## 协议支持

Mosiquitto 作为 MQTT Broker 提供了完整的 MQTT 3.1/3.1.1/5.0 协议支持，支持协议规范中的遗嘱消息、保留消息、共享订阅等能力，同时也支持 [MQTT over WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)，可以满足大多数 MQTT 设备接入需求。

EMQX 同样完整支持 MQTT 3.1/3.1.1/5.0 以及 MQTT over Websocket 协议。同时 EMQX 5.0 开创性地引入了下一代互联网协议 HTTP/3 的底层传输协议 QUIC 的支持，以解决复杂网络环境下的通信问题，提升整体吞吐量和移动连接的稳定性。此外，EMQX 也扩展支持 MQTT-SN、CoAP、LwM2M、STOMP 以及其他协议扩展。

|                              | **EMQX**                                                     | **Mosquitto** | **Notes and Links**                                          |
| :--------------------------- | :----------------------------------------------------------- | :------------ | :----------------------------------------------------------- |
| **MQTT 3.1/3.1.1**           | ✅                                                            | ✅             | [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) |
| **MQTT 5.0**                 | ✅                                                            | ✅             | [MQTT 5 Explore](https://www.emqx.com/en/blog/introduction-to-mqtt-5)         |
| **MQTT Shared Subscription** | ✅                                                            | ✅             |                                                              |
| **MQTT Add-ons**             | - [Exclusive subscription](https://www.emqx.io/docs/en/v5.0/mqtt/mqtt-exclusive-subscription.html#exclusive-subscription)<br>- [Delayed Publish](https://www.emqx.io/docs/en/v5.0/advanced/delayed-publish.html)<br>- [Auto-subscription](https://www.emqx.io/docs/en/v5.0/advanced/auto-subscriptions.html)<br>- [Topic rewrite](https://www.emqx.io/docs/en/v5.0/advanced/topic-rewrite.html) | ❌             |                                                              |
| **MQTT over TCP**            | ✅                                                            | ✅             | [EMQX Getting Started](https://www.emqx.io/docs/en/v5.0/getting-started/getting-started.html#quick-verification-using-an-mqtt-client) |
| **MQTT over TLS**            | ✅                                                            | ✅             | [Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) |
| **MQTT over WebSocket**      | ✅                                                            | ✅             | [Connect to MQTT broker with Websocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) |
| **MQTT over QUIC**           | ✅                                                            | ❌             | EMQX is now the only MQTT broker in the world that supports QUIC transport. ([MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)) |
| **LB (Proxy Protocol)**      | ✅                                                            | ✅             | Proxy Protocol v1, v2 ([Cluster load balancing](https://www.emqx.io/docs/en/v5.0/deploy/cluster/lb.html)) |
| **IPv6 Support**             | ✅                                                            | ✅             |                                                              |
| **Multi-protocol Gateway**   | ✅                                                            | ❌             | [Extended protocol gateway](https://www.emqx.io/docs/en/v5.0/gateway/gateway.html#design) |
| **MQTT-SN**                  | ✅                                                            | ❌             | [MQTT-SN Gateway](https://www.emqx.io/docs/en/v5.0/gateway/mqttsn.html) |
| **CoAP**                     | ✅                                                            | ❌             | [CoAP Protocol Gateway](https://www.emqx.io/docs/en/v5.0/configuration/configuration-manual.html#coap) |
| **LwM2M**                    | ✅                                                            | ❌             | [LwM2M Protocol Gateway](https://www.emqx.io/docs/en/v5.0/configuration/configuration-manual.html#lwm2m) |
| **STOMP**                    | ✅                                                            | ❌             | [Stomp Gateway](https://www.emqx.io/docs/en/v5.0/gateway/stomp.html) |

## 安全性

安全性对于物联网设备连接以及设备之间、设备与云服务之间的数据交换至关重要。Mosquitto 和 EMQX 都支持基于 TLS/SSL 的安全连接。此外，EMQX 还支持 QUIC 传输、OCSP Stapling、Audit Logs 和 Black Duck 源代码扫描。

|                         | **EMQX** | **Mosquitto** | **Notes and Links**                                          |
| :---------------------- | :------- | :------------ | :----------------------------------------------------------- |
| **TLS/SSL**             | ✅        | ✅             | EMQX: TLS 1.1, 1.2, 1.3 ([Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)) |
| **QUIC**                | ✅        | ❌             | [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) |
| **OCSP Stapling**       | ✅        | ✅             | [EMQX Supports OCSP stapling](https://www.youtube.com/watch?v=e9SiF7ptvpU) |
| **Audit Logs**          | ✅        | ❌             |                                                              |

## 认证与鉴权

在客户端认证权限与访问控制方面，Mosiquitto 提供了动态安全插件，通过灵活的方式处理用户名/密码身份验证和访问控制。Mosiquitto 支持匿名与用户名密码方式认证，并可以通过动态安全插件提供的自定义组群和角色的方式控制消息主题的访问权限。

EMQX 支持多种认证机制，如用户名密码认证、JWT 认证以及基于 MQTT 5.0 协议的增强认证。EMQX 支持与多种数据存储方式集成，包括内置数据库、文件、MySQL、PostgreSQL、MongoDB 和 Redis。

此外，EMQX 为用户提供了黑名单功能，用户可以通过 Dashboard 和 HTTP API 将指定客户端加入黑名单以拒绝该客户端访问，除了客户端标识符以外，还支持直接封禁用户名甚至 IP 地址，方便用户灵活管理客户端的连接与访问。

|                                      | **EMQX** | **Mosquitto** | **Notes & Links**                                            |
| :----------------------------------- | :------- | :------------ | :----------------------------------------------------------- |
| **Username/Password**                | ✅        | ✅             | [EMQX: AuthN Introduction](https://www.emqx.io/docs/en/v5.0/security/authn/authn.html)<br>[Mosquitto: Authentication methods](https://mosquitto.org/documentation/authentication-methods/#:~:text=In%20Mosquitto%202.0%20and%20up%2C%20you%20must%20choose,authentication%3A%20password%20files%2C%20authentication%20plugins%2C%20and%20unauthorised%2Fanonymous%20access.) |
| **JWT**                              | ✅        | ✅             | EMQX：[JWT Authenticaton](https://www.emqx.io/docs/en/v5.0/security/authn/jwt.html)<br>Mosquitto: [Auth plugin for mosquitto](https://github.com/iegomez/mosquitto-go-auth) |
| **MQTT 5.0 Enhanced Authentication** | ✅        | ❌             | [SCRAM Authentication](https://www.emqx.io/docs/en/v5.0/security/authn/scram.html) |
| **PSK**                              | ✅        | ✅             | [SSL/TLS](https://www.emqx.io/docs/en/v5.0/security/ssl.html#psk-authentication) |
| **X.509 Certificates**               | ✅        | ✅             |                                                              |
| **LDAP**                             | ✅        | ✅             | [LDAP Authentication/ACL](https://docs.emqx.com/en/enterprise/v4.4/modules/ldap_authentication.html) |
| **Fine-grained Access Control**      | ✅        | ✅             | [EMQX Authorization](https://www.emqx.io/docs/en/v5.0/security/authz/authz.html) |
| **Authentication  Backends**         | ✅        | ✅             | [Authentication Introduction](https://www.emqx.io/docs/en/v5.0/security/authn/authn.html) |
| **ACL Database Backends**            | ✅        | ✅             | EMQX：Files, MySQL, PostgreSQL, MongoDB, Built-in Database, HTTP<br>[EMQX Authorization Introduction](https://www.emqx.io/docs/en/v5.0/security/authz/authz.html) |
| **Flapping Detect**                  | ✅        | ❌             |                                                              |
| **Block List**                       | ✅        | ❌             |                                                              |

## 数据集成

Mosquitto 默认通过 MQTT 客户端消息订阅方式实现外部系统对数据的消费。此外，Mosquitto 提供了多个 Mosquitto 之间的数据桥接能力，可以用于多个 broker 之间的分布式部署与数据打通。

EMQX 在数据集成方面提供了 WebHook 方式将客户端消息和事件推送到外部系统中。EMQX 也同样提供了类似于 Mosquitto 的 MQTT 数据桥接功能，可以连接多个 EMQX 集群或其他标准 MQTT 服务。EMQX 在企业版中重点增强了数据集成能力。EMQX 企业版可以通过规则引擎对接各类主流型数据库、消息队列以及云服务，在数据可靠性与架构设计灵活性上大大增强。

|                     | **EMQX**               | **Mosquitto** | **Notes and Links**                                          |
| :------------------ | :--------------------- | :------------ | :----------------------------------------------------------- |
| **Webhook**         | ✅                      | ✅             | [Webhook](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridge-webhook.html#example-setup-webhook-using-config-files) |
| **Rule Engine**     | ✅                      | ❌             | [Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) |
| **Message Codec**     | ✅                    | ❌             |  |
| **Data Bridge**     | ✅                      | ❌             | [Data bridges](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridges.html) |
| **Confluent/Kafka** | ✅ (Enterprise Edition) | ❌             | [Stream Data into Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html) |
| **SAP Event Mesh**  | ✅(Enterprise Edition)  | ❌             | [Ingest Data into SAP Event Mesh](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_sap_event_mesh.html#bridge-data-to-sap-event-mesh) |
| **Apache Pulsar**   | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Pulsar](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_pulsar.html) |
| **RabbitMQ**        | ✅(Enterprise Edition)  | ❌             | [Ingest Data into RabbitMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rabbitmq.html) |
| **MySQL**           | ✅(Enterprise Edition)  | ❌             | [Ingest Data into MySQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mysql.html) |
| **PostgreSQL**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into PostgreSQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_pgsql.html) |
| **SQL Server**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into SQL Server](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_sqlserver.html) |
| **MongoDB**         | ✅(Enterprise Edition)  | ❌             | [Ingest Data into MongoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mongodb.html) |
| **Redis**           | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Redis](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_redis.html) |
| **Cassandra**       | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Cassandra](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_cassandra.html) |
| **AWS DynamoDB**    | ✅(Enterprise Edition)  | ❌             | [Ingest Data into DynamoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_dynamodb.html) |
| **ClickHouse**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into ClickHouse](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_clickhouse.html) |
| **InfluxDB**        | ✅(Enterprise Edition)  | ❌             | [Ingest Data into InfluxDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_influxdb.html) |
| **TimeScaleDB**     | ✅(Enterprise Edition)  | ❌             | [Ingest Data into TimescaleDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_timescaledb.html) |
| **Oracle**          | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Oracle](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_oracle.html) |

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

## 规则引擎

为了用户更加方便地实现高性能数据预处理与基于业务需求的数据路由，EMQX 内置了基于 SQL 的规则引擎组件，搭配数据桥接使用，无需编写代码即可实现一站式的 IoT 数据提取、过滤、转换、存储与处理，以加速应用集成和业务创新。

|                        | **EMQX**               | **Mosquitto** | **Notes and Links**                                          |
| :--------------------- | :--------------------- | :------------ | :----------------------------------------------------------- |
| **Rule Engine**        | ✅                      | ❌             | [Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) |
| **Built-in Functions** | ✅                      | ❌             | [Built-in SQL Functions](https://www.emqx.io/docs/en/v5.0/data-integration/rule-sql-builtin-functions.html#built-in-sql-functions) |
| **JQ Functions**       | ✅                      | ❌             | [JQ functions](https://www.emqx.io/docs/en/v5.0/data-integration/rule-sql-jq.html#jq-functions) |
| **Event Trigger**      | ✅                      | ❌             | [Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html#rule-engine) |
| **JSON Codec**         | ✅                      | ❌             |                                                              |
| **Avro Codec**         | ✅(Enterprise Edition)  | ❌             | [Custom codec example - Avro](https://docs.emqx.com/en/enterprise/v4.4/rule/schema-registry-examp-avro.html) |
| **ProtoBuf Codec**     | ✅(Enterprise Edition)  | ❌             | [Custom codec example - Protobuf](https://docs.emqx.com/en/enterprise/v4.4/rule/schema-registry-examp-protobuf.html) |
| **Schema Registry**    | ✅ (Enterprise Edition) | ❌             | [Introduction to Schema Registry](https://docs.emqx.com/en/enterprise/v4.4/rule/schema-registry.html) |

## 可操作性与可观测性

Mosquitto 提供了基本的日志和调试功能，用于监控代理状态和故障排除。然而，它缺乏先进的管理和监控功能，使用户难以从其运行状态获得更多洞察进行性能优化。

EMQX 通过 HTTP API 和 Dashboard 提供丰富和可视化的监控功能，使其更容易监控和管理。此外，EMQX 支持与 Prometheus 和 Datadog 的集成，使运维团队能够轻松使用第三方监控平台。

|                                  | **EMQX**     | **Mosquitto**   | **Notes and Links**                                          |
| :------------------------------- | :----------- | :-------------- | :----------------------------------------------------------- |
| **Dashboard**                    | ✅            | ❌               | [EMQX Dashboard](https://www.emqx.io/docs/en/v5.0/getting-started/dashboard.html) |
| **Configuration**                | HOCON Format | Key-Value Fomat |                                                              |
| **HTTP API**                     | ✅            | ❌               | [EMQX REST API](https://www.emqx.io/docs/en/v5.0/admin/api.html) |
| **CLI**                          | ✅            | ✅               | [Command Line Interface](https://www.emqx.io/docs/en/v5.0/admin/cli.html) |
| **Config Hot update**            | ✅            | ❌               | [Configuration Files](https://www.emqx.io/docs/en/v5.0/admin/cfg.html) |
| **Metrics**                      | ✅            | ✅               | Node metrics:<br> [Metrics](https://www.emqx.io/docs/en/v5.0/observability/metrics-and-stats.html) <br> Mosquitto - $SYS topic |
| **Grafana**                      | ✅            | ✅               | [Integrate with Prometheus](https://www.emqx.io/docs/en/v5.0/observability/prometheus.html) |
| **Cluster Metrics**              | ✅            | ❌               | [Metrics](https://www.emqx.io/docs/en/v5.0/observability/metrics-and-stats.html) |
| **Alarm Alerts**                 | ✅            | ❌               | [System Topic](https://www.emqx.io/docs/en/v5.0/advanced/system-topic.html#alarms-system-alarms) |
| **Slow Subscription Monitoring** | ✅            | ❌               | [Slow subscribers statistics](https://www.emqx.io/docs/en/v5.0/observability/slow_subscribers_statistics.html) |
| **Prometheus**                   | ✅            | ✅               | [Integrate with Prometheus](https://www.emqx.io/docs/en/v5.0/observability/prometheus.html#dashboard-update) |

## 云原生部署与 K8s 支持

Mosquitto 支持基于 docker 的容器化部署。EMQX 在此基础上提供了基于 Kubernetes Operator 和 Terraform 云原生自动部署能力，更加方便在容器环境下的部署与运维。

|                         | **EMQX**                                      | **Mosquitto** | **Notes and Links**                                          |
| :---------------------- | :-------------------------------------------- | :------------ | :----------------------------------------------------------- |
| **Docker**              | ✅                                             | ✅             | [EMQX Docker](https://hub.docker.com/r/emqx/emqx)            |
| **Kubernetes Operator** | ✅                                             | ❌             | [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) |
| **Terraform**           | ✅                                             | ❌             | [EMQX Terraform](https://www.emqx.com/en/emqx-terraform)     |
| **Cloud Service**       | - Serverless<br>- Hosting/Dedicated<br>- BYOC | Hosting       |                                                              |

EMQX Kubernetes Operator: [https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator)

![EMQX Kubernetes Operator](https://assets.emqx.com/images/f8483728a4241191e4f49ac3f8fa5740.png?imageMogr2/thumbnail/1520x)

## 桥接 Mosquitto 到 EMQX

虽然 EMQX 和 Mosquitto 作为 MQTT Broker 有着很多不同之处，但它们可以通过 MQTT 桥接的方式实现完美结合。

我们可以在物联网边缘的嵌入式硬件或网关上部署 Mosquitto，实现小规模边缘数据接入，然后通过桥接方式与云端的 EMQX 集成，实现大规模的云端数据汇聚接入。

> [桥接 Mosquitto MQTT 消息至 EMQX](https://www.emqx.com/zh/blog/bridging-mosquitto-to-emqx-cluster)

![Bridging Mosquitto to EMQX](https://assets.emqx.com/images/35635ecd1ac7c7453bce2d7c46ee1511.png?imageMogr2/thumbnail/1520x)

## 结语

通过以上对比，我们可以看出：Mosquitto 作为单节点的轻量级 MQTT 消息中间件，更加适合部署在工业网关、工控机、小型服务器中，实现中小规模的 MQTT 设备连接场景下快速高效的数据接入与消息路由。而 EMQX 作为支持高可用集群的大规模 MQTT 消息服务器，更适合部署在数据中心、公有云或私有云环境，为较大规模数据接入以及对高可用有需求的用户提供服务。

**您可以选择 Mosquitto 用于嵌入式硬件和 IoT 边缘部署，并使用 EMQX 作为云中高度可扩展、高可用的 MQTT 消息服务。**

此外，对于有更大规模设备连接与大吞吐数据接入需求，且对数据完整性、数据持久化以及数据集成灵活性有较高要求的用户，我们建议您使用 [EMQX 企业版本](https://www.emqx.com/zh/products/emqx)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
