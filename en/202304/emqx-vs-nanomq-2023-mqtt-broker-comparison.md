## Introduction

[EMQX](https://www.emqx.io/) and [NanoMQ](https://nanomq.io/) are both open-source MQTT Brokers, initially developed by [EMQ Technologies Inc](https://www.emqx.com/en/about), a leading open-source IoT data infrastructure software provider. 

EMQX is a highly scalable, distributed MQTT Broker for connecting millions of IoT devices to the cloud, while NanoMQ is a fast and lightweight broker designed for IoT edge.

We'll compare these two brokers in the second post of the "[2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)" blog series.

## EMQX Overview

EMQX is the world's most scalable MQTT messaging server and is widely used in mission-critical business scenarios such as the IoT, Industrial IoT ([IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)), and Internet of Vehicles (IoV).

EMQX is written in Erlang/OTP and adopts a masterless distributed architecture to achieve high availability and horizontal scalability.

EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

See: [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) 

![EMQX Cluster](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png?imageMogr2/thumbnail/1520x)

**Pros**

- Supports large-scale deployments
- Clustering & horizontal scalability
- High-performance and reliable
- Rich enterprise features 
- Out-of-box data integration

**Cons**

- Complicated to set up and configure
- Difficult to manage effectively

## NanoMQ Overview

NanoMQ is a lightweight and fast MQTT broker designed for the IoT edge. NanoMQ is implemented in purely C, based on NNG's asynchronous I/O with a multi-threading [Actor Model](https://en.wikipedia.org/wiki/Actor_model), and fully supports MQTT 3.1.1 and MQTT 5.0 protocol versions. 

NanoMQ is high-performance in the context of a stand-alone broker. The fascinating advantage is its portability. It can be deployed on any POSIX-compatible platform and runs on different CPU architectures such as x86_64, ARM, MIPS, and RISC-V.

![NanoMQ MQTT Broker](https://assets.emqx.com/images/892a0de52bd6288686aec1f0bbc330d9.png)

**Pros**

- Lightweight design
- Highly portable
- Small booting footprint
- Easy to deploy
- Bridging with brokerless protocols

**Cons**

- No horizontal scalability
- Small community and user base
- Lack of documentation and tutorials
- No clustering support
- Lacking enterprise features (data Integrations)


<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>


## Community and Popularity

EMQX and NanoMQ open-source projects are hosted on GitHub. Launched in 2012, EMQX is one of the most popular MQTT brokers and has 11.4k stars. NanoMQ, as a project launched in 2020, is in the early stage and currently has over 800 stars. Both projects are actively developing, with thousands of commits in the last 12 months.

|                                     | **EMQX**                                    | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------ | :---------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [NanoMQ GitHub](https://github.com/nanomq/nanomq) |
| **Project Created**                 | 2012                                        | 2020                                            |
| **License**                         | Apache License 2.0                          | The MIT License                                 |
| **Latest Release**                  | v5.0.21 (March 2023)                        | v0.17.0 (March 2023)                            |
| **GitHub Stars**                    | 11.4k                                       | 800+                                            |
| **GitHub Forks**                    | 2k                                          | 100+                                            |
| **GitHub Commits**                  | 14k+                                        | 2k+                                             |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 1200+                                           |
| **GitHub Releases**                 | 260+                                        | 75+                                             |
| **GitHub PRs**                      | 6000+                                       | 780+                                            |
| **GitHub Contributors**             | 100+                                        | 20+                                             |

## Features and Capabilities

EMQX and NanoMQ fully implement the MQTT 3.1.1 and 5.0 specifications, support [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) and SSL/TLS encryption, and pioneer [MQTT Over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), the next generation of the MQTT standard.

EMQX is a highly scalable MQTT Broker with multiple protocol gateways, including LwM2M/CoAP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), and Stomp. In contrast, NanoMQ is a lightweight broker which supports brokerless mode and can work with DDS, ZeroMQ, and Nanomsg.

Both brokers offer various authentication mechanisms, including username-password, JWT, OAuth 2.0 authentication, and IP white-/blacklisting.

Regarding enterprise features, [EMQX's Enterprise Edition](https://www.emqx.com/en/products/emqx) can integrate with Kafka, SQL, NoSQL databases, and cloud services via a rule engine and out-of-box data bridges.

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

## Scalability and Performance

EMQX is known for its high scalability and performance, making it the best choice for large-scale, mission-critical IoT projects. It also offers high availability through its masterless clustering architecture. 

NanoMQ has an excellent lightweight design based on NNG’s async-io and multi-threading model. It scales well with multiple cores in modern SMP systems, and has a small booting footprint of less than 200k, efficiently using CPU/memory resources.

In short, both brokers have performance, scalability, and reliability strengths compared to other MQTT brokers.

See: [EMQX vs NanoMQ Performance Benchmark Report](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-nanomq).

|                                              | **EMQX**                                                     | **NanoMQ**                                                   | **Notes and Links**                                          |
| :------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Clustering**                               | ✅ 20+ nodes of cluster                                       | ❌                                                            | [EMQX Cluster](https://www.emqx.io/docs/en/v5.0/deploy/cluster/introduction.html) |
| **Scalability**                              | - 4M MQTT connections per node<br>- 100M MQTT connections per cluster | 200k MQTT connections per node                               | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | - 2 million QoS0 MQTT msgs/sec per node<br>- 800k QoS1 msgs/sec<br>- 200k QoS2 msgs/sec | - Up to 1 million+ QoS0 MQTT msgs/sec per node<br>- 500k QoS1 msgs/sec<br>- 180k QoS2 msgs/sec |                                                              |
| **Latency**                                  | Single-digit millisecond latency in most scenarios                                              | Less than 10 milliseconds in most scenarios                                             |                                                              |
| **Booting footprint**                        | 30Mb+                                                        | 200Kb+                                                       |                                                              |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | ❌                                                            |                                                              |
| **Auto Clustering**                          | ✅                                                            | ❌                                                            |                                                              |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            | ❌                                                            |                                                              |

## Operability and Observability

EMQX offers a user-friendly dashboard and extensive HTTP APIs. It supports monitoring with StatsD, Prometheus, and Grafana. NanoMQ is simple to deploy and easy to configure and manage. But it lacks advanced management and monitoring features.

Both brokers are relatively easy to use, but NanoMQ's minimalist design makes it easier for beginners to learn and use MQTT. 

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
| **Docker**              | ✅            | ✅            | - [EMQX Docker](https://hub.docker.com/r/emqx/emqx)<br>- [NanoMQ Docker](https://hub.docker.com/r/emqx/nanomq) |
| **Kubernetes Operator** | ✅            | ❌            | [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) |
| **Terraform**           | ✅            | ❌            |                                                              |

## Data Integration

As a lightweight broker, NanoMQ does not support data integration. EMQX, especially the Enterprise Edition running in the cloud, can seamlessly integrate with Kafka, databases, and cloud services via out-of-the-box data bridges.

|                     | **EMQX**               | **NanoMQ** | **Notes and Links**                                          |
| :------------------ | :--------------------- | :--------- | :----------------------------------------------------------- |
| **Rule Engine**     | ✅                      | ✅Limited   | [EMQX Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) |
| **Message Codec**   | ✅                      | ❌          |  |
| **Data Bridge**     | ✅                      | ❌          | [Data bridges](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridges.html) |
| **Confluent/Kafka** | ✅ (Enterprise Edition) | ❌          | [Stream Data into Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html) |
| **SAP Event Mesh**  | ✅(Enterprise Edition)  | ❌          | [Ingest Data into SAP Event Mesh](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_sap_event_mesh.html#bridge-data-to-sap-event-mesh) |
| **Apache Pulsar**   | ✅(Enterprise Edition)  | ❌          | [Bridge data to Pulsar](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_pulsar.html) |
| **RabbitMQ**        | ✅(Enterprise Edition)  | ❌          | [Bridge data to RabbitMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rabbitmq.html) |
| **MySQL**           | ✅(Enterprise Edition)  | ❌          | [EMQX MySQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mysql.html) |
| **PostgreSQL**      | ✅(Enterprise Edition)  | ❌          | [Ingest data into PostgreSQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_pgsql.html) |
| **SQL Server**      | ✅(Enterprise Edition)  | ❌          | [Ingest data into SQLServer](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_sqlserver.html) |
| **MongoDB**         | ✅(Enterprise Edition)  | ❌          | [Ingest data into MongoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mongodb.html) |
| **Redis**           | ✅(Enterprise Edition)  | ❌          | [Ingest data into Redis](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_redis.html) |
| **Cassandra**       | ✅(Enterprise Edition)  | ❌          | [Ingest data into Cassandra](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_cassandra.html) |
| **AWS DynamoDB**    | ✅(Enterprise Edition)  | ❌          | [Ingest data into DynamoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_dynamodb.html) |
| **ClickHouse**      | ✅(Enterprise Edition)  | ❌          | [Ingest data into ClickHouse](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_clickhouse.html) |
| **InfluxDB**        | ✅(Enterprise Edition)  | ❌          | [Ingest data into InfluxDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_influxdb.html) |
| **TimeScaleDB**     | ✅(Enterprise Edition)  | ❌          | [Ingest data into TimescaleDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_timescaledb.html) |
| **Oracle**          | ✅(Enterprise Edition)  | ❌          | [Ingest data into Oracle](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_oracle.html) |
| **HStreamDB**       | ✅(Enterprise Edition)  | ❌          | [Stream Data into HStreamDB ](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_hstreamdb.html) |

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>


## Bridging NanoMQ to EMQX

We can deploy NanoMQ on small devices or gateways at the IoT edge and then aggregate and ingest data to a large-scale EMQX cluster in the cloud via an MQTT bridge.

![Bridging NanoMQ to EMQX](https://assets.emqx.com/images/a2fc8b04a0059369d61507f4cb7dbf63.png)

## Conclusion

EMQX and NanoMQ are now the most actively developing MQTT brokers with a fantastic open-source community and commercial support. 

EMQX is scalable, reliable, and feature-rich, making it the best choice in the cloud as an MQTT messaging service in mission-critical IoT projects. NanoMQ is lightweight, efficient, and affordable, making it suitable for industrial IoT and IoT applications at the edge.

In short, you can choose to use one or both, catering to different needs and use cases. We expect the two brokers to drive MQTT technology innovation in 2023 and beyond.

## References

1. [EMQX: The World's #1 Open Source Distributed MQTT Broker](https://www.emqx.io/)
2. [NanoMQ: An Ultra-lightweight MQTT Broker for IoT Edge](https://nanomq.io/)
3. [EMQX 5.0 Documentation](https://www.emqx.io/docs/en/v5.0/)
4. [NanoMQ Documentation](https://nanomq.io/docs/en/latest/) 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
