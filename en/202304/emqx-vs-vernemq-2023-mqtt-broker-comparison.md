## Introduction

[EMQX](https://www.emqx.io/) and [VerneMQ](https://vernemq.com/) are open-source, highly scalable distributed MQTT brokers written in Erlang/OTP, known for their robustness, fault tolerance, and scalability.

EMQX is now one of the most popular MQTT brokers in the world. While VerneMQ has not been actively developing and maintaining these years.

In the fourth blog of the “[2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)“ series, we will briefly compare these two brokers as a memo in the history of MQTT.

## EMQX Overview

The EMQX project was launched on GitHub in 2012 and is licensed under Apache version 2.0. The idea for EMQX originated from the need for a massively scalable MQTT broker that could handle millions of concurrent connections.

EMQX is now the world's most scalable MQTT messaging server with a distributed architecture based on [Mria + RLOG](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connections). EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

See: [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

![MQTT Cluster](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png)

EMQX offers rich enterprise features, data integration, cloud hosting services, and commercial support from [EMQ Technologies Inc.](https://www.emqx.com/en/about) Over the years, EMQX has gained popularity among enterprises, startups, and individuals due to its performance, reliability, and scalability. EMQX is widely used in various industries, such as IoT, [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges), connected cars, and telecommunications.

**Pros:**

- Supports large-scale deployments
- High availability
- Horizontal scalability
- High-performance and reliable
- Rich enterprise features 
- Pioneering MQTT over QUIC 

**Cons:**

- Complex to set up and configure
- Difficult to manage effectively
- Logs may be confusing

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

## VerneMQ Overview

The VerneMQ project was launched in [2014](https://github.com/vernemq/vernemq/tree/3c7703f0d62e758ba22a34ceb756f2ac2a4da44a) and initially developed by [Erlio GmbH](https://vernemq.com/company.html). As the second broker wrote in Erlang/OTP, the project is licensed under Apache Version 2.0 and borrowed [some code](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl) from the EMQX project.

Regarding architectural design, VerneMQ supports MQTT message persistence in LevelDB and uses a clustering architecture based on the [Plumtree](https://github.com/lasp-lang/plumtree) library, which implements [the Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf) algorithm.

Unfortunately, this Plumtree cluster architecture has not proven to work, even though it seems perfect in theory. The VerneMQ team and community have spent many years trying to make it work, fixing problems such as network split, data inconsistency, and crash recovery. 

Finally, the project has stopped being actively developed and maintained, with about 50 commits in the last 12 months.

**Pros:**

- High availability
- Horizontal scalability
- Message persistence

**Cons:**

- Not proofed clustering architecture
- Limited documentation
- Limited enterprise features
- Not actively developing

## Community and Popularity

Both the EMQX and VerneMQ projects are hosted on GitHub. EMQX was launched in 2012 and is one of the earliest and now the highest-starred MQTT brokers with 11.4k stars. The VerneMQ project was created in 2014 and has 3k GitHub stars now.

| **Community & Users**               | **EMQX**                                    | **VerneMQ**                                          | **Notes and Links**                                          |
| :---------------------------------- | :------------------------------------------ | :--------------------------------------------------- | :----------------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [VerneMQ GitHub](https://github.com/vernemq/vernemq) |                                                              |
| **Product Created**                 | 2012                                        | 2014                                                 |                                                              |
| **License Mode**                    | Apache License 2.0                          | Apache License 2.0                                   |                                                              |
| **Latest Release**                  | v5.0.21 (March 2023)                        | v1.12.6.2 (Nov. 2022)                                |                                                              |
| **GitHub Stars**                    | 11.4k+                                      | 3k                                                   |                                                              |
| **GitHub Forks**                    | 2k                                          | 300+                                                 | [EMQX GitHub Forks](https://github.com/emqx/emqx/network/members)<br>[VerneMQ GitHub Forks](https://github.com/vernemq/vernemq/forks) |
| **GitHub Commits**                  | 14k+                                        | 2400+                                                | [EMQX GitHub Commits](https://github.com/emqx/emqx/commits)<br>[VerneMQ GitHub Commits ](https://github.com/vernemq/vernemq/commits) |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 50+                                                  |                                                              |
| **GitHub Issues**                   | 3500+                                       | 1300+                                                | [EMQX GitHub Issues](https://github.com/emqx/emqx/issues?q=is%3Aissue+is%3Aall+)<br>[VerneMQ GitHub Issues](https://github.com/vernemq/vernemq/issues) |
| **GitHub PRs**                      | 6000+                                       | 600                                                  | [EMQX GitHub PRs](https://github.com/emqx/emqx/pulls)<br>[VerneMQ GitHub PRs](https://github.com/vernemq/vernemq/pulls) |
| **GitHub Releases**                 | 260+                                        | 40                                                   | [EMQX GitHub Releases](https://github.com/emqx/emqx/releases)<br>[VerneMQ GitHub Releases](https://github.com/vernemq/vernemq/releases) |
| **GitHub Contributors**             | 110+                                        | 50                                                   | [EMQX GitHub Contributors](https://github.com/emqx/emqx/graphs/contributors)<br>[VerneMQ GitHub Contributors](https://github.com/vernemq/vernemq/graphs/contributors) |
| **Docker Pulls**                    | 24M+                                        | 5M+                                                  | [EMQX Docker Pulls](https://hub.docker.com/r/emqx/emqx)<br>[VerneMQ Docker Pulls](https://hub.docker.com/r/vernemq/vernemq/) |

## Features and Capabilities

EMQX and VerneMQ fully implement the MQTT 3.1.1 and 5.0 specifications and support [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) and SSL/TLS encryption. Both brokers offer various authentication mechanisms, including username-password, JWT, LDAP, and OAuth 2.0 authentication.

EMQX has multiple protocol gateways, including LwM2M/CoAP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), and Stomp. EMQX 5.0 pioneers MQTT over QUIC, which has the potential to be the next-generation MQTT standard, with multiplexing and faster connection establishment and migration support.

In addition, EMQX provides rich enterprise features for management and integration, such as HTTP API, WebHook, and Rule Engine, which can integrate with Kafka, SQL, NoSQL databases, and cloud services via out-of-box data bridges.

|                          | **EMQX**                            | **VerneMQ**  |
| :----------------------- | :---------------------------------- | :----------- |
| **MQTT 3.1.1**           | ✅                                   | ✅            |
| **MQTT 5.0**             | ✅                                   | ✅            |
| **MQTT over TLS**        | ✅                                   | ✅            |
| **MQTT over WebSocket**  | ✅                                   | ✅            |
| **MQTT over QUIC**       | ✅                                   | ❌            |
| **LwM2M/CoAP**           | ✅                                   | ❌            |
| **MQTT-SN**              | ✅                                   | ❌            |
| **Stomp**                | ✅                                   | ❌            |
| **MQTT Bridging**        | ✅                                   | ✅            |
| **Authentication & ACL** | ✅                                   | ✅            |
| **Message Persistence**  | ✅ In RocksDB and external databases | ✅ In LevelDB |
| **WebHook**              | ✅                                   | ✅            |
| **Rule Engine**          | ✅                                   | ❌            |
| **Data Integration**     | ✅                                   | ❌            |
| **Cloud Service**        | [Cloud Hosting](https://www.emqx.com/en/cloud)<br>[Serverless MQTT](https://www.emqx.com/en/cloud/serverless-mqtt)<br>[BYOC](https://www.emqx.com/en/cloud/byoc)    | ❌            |

## Scalability and Performance

EMQX and VerneMQ are designed for high performance, low latency, and scalability with a distributed architecture. Both can scale to handle millions of concurrent MQTT connections using a single cluster.

EMQX has over 30,000 clusters deployed in production with proven scalability and reliability. The latest EMQX 5.0 hits 100 million MQTT connections in the benchmark with a 23 nodes cluster.

For VerneMQ, few benchmark reports are available on the scalability and performance though it should work well in theory and design. You can benchmark it with the MQTT load testing tools like [emqtt-bench](https://github.com/emqx/emqtt-bench), [emqttb](https://github.com/emqx/emqttb), or [XMeter cloud service](https://www.emqx.com/en/products/xmeter).

|                                              | **EMQX**                                                     | **VerneMQ**                   | **Notes & Links**                                            |
| :------------------------------------------- | :----------------------------------------------------------- | :---------------------------- | :----------------------------------------------------------- |
| **Scalability**                              | 4M MQTT connections per node<br>100M MQTT connections per cluster | **?**                         | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | 4 million QoS0 MQTT msgs/sec per node<br>800k QoS1 msgs/sec<br>200k QoS2 msgs/sec | **?**                         |                                                              |
| **Latency**                                  | Single-digit millisecond latency in most scenarios                                             | Up to seconds latency in some scenarios                         |                                                              |
| **Reliability**                              | Message Persistence in RocksDB and external Database         | Message Persistence in LevelDB | [Highly Reliable MQTT Data Persistence Based on RocksDB](https://www.emqx.com/en/blog/mqtt-persistence-based-on-rocksdb) <br>[VerneMQ Storage](https://docs.vernemq.com/configuring-vernemq/storage) |
| **Clustering**                               | 20+ nodes of cluster                                         | **?**                         | [EMQX Cluster Scalability](https://www.emqx.io/docs/en/v5.0/deploy/cluster/db.html#node-roles)<br>[Vernemq - Cluster](https://docs.vernemq.com/vernemq-clustering/introduction) |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | **?**                         |                                                              |
| **Auto Clustering**                          | ✅                                                            | **?**                         | [EMQX Node Discovery and Autocluster](https://www.emqx.io/docs/en/v5.0/deploy/cluster/intro.html#emqx-node-discovery-and-autocluster) |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            |                               | [EMQX Release Upgrade](https://docs.emqx.com/en/enterprise/v4.4/advanced/relup.html#release-upgrade) |

> **?** here means that we were unable to find any publicly available documentation or files that could serve as evidence regarding the item under discussion.

## Data Integrations (Out of the box)

VerneMQ has limited support for MQTT data integration. It allows users to write plugins to ingest data into external databases or cloud services.

EMQX has a built-in SQL-based rule engine to help extract, filter, enrich, and transform MQTT messages in real-time within the broker.

The Enterprise Edition of EMQX can seamlessly integrate with Kafka, databases, and cloud services using the rule engine and out-of-the-box data bridges.

| **Data Integrations** | **EMQX** | **VerneMQ** | **Notes and Links**                                          |
| :-------------------- | :------- | :---------- | :----------------------------------------------------------- |
| **Rule Engine**       | ✅        | ❌           | [Introduction to Data Integration](https://www.emqx.io/docs/en/v5.0/data-integration/introduction.html) |
| **Message Codec**     | ✅        | ❌           | [Introduction to Schema Registry](https://docs.emqx.com/en/enterprise/v4.4/rule/schema-registry.html) |
| **Data Bridge**       | ✅        | ❌           | [Data Bridges](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridges.html) |
| **MQTT Bridge**       | ✅        | ✅           | [Bridge Data into MQTT Broker](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-mqtt.html)<br>[MQTT Bridge](https://docs.vernemq.com/configuring-vernemq/bridge) |
| **Webhook**           | ✅        | ✅           | [Ingest Data into Webhook](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-webhook.html)<br>[Webhooks](https://docs.vernemq.com/plugin-development/webhookplugins) |
| **Kafka/Confluent**   | ✅        | **?**       | [Stream Data into Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html)<br>[GitHub - crisrise/vmq_kafka: A VerneMQ plugin that sends all published messages to Apache Kafka](https://github.com/crisrise/vmq_kafka) |
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

## Extensibility

Both EMQX and VerneMQ can be easily extended with Hooks and Plugins. In addition, EMQX supports multiple protocol gateways, allowing users to develop new connection protocols.

| **Extensibility**      | **EMQX** | **VerneMQ** | **Notes and Links**                                          |
| :--------------------- | :------- | :---------- | :----------------------------------------------------------- |
| **Hooks**              | ✅        | ✅           | [Hooks](https://docs.emqx.com/en/enterprise/v4.4/advanced/hooks.html#definition) |
| **Plugins**            | ✅        | ✅           | [Plugins](https://docs.emqx.com/en/enterprise/v4.4/advanced/plugins.html#list-of-plugins)  [Plugin Development](https://docs.vernemq.com/plugin-development/introduction) |
| **Plugin Hot-loading** | ✅        | ✅           |                                                              |
| **Gateways**           | ✅        | ❌           | [Gateway Introduction](https://www.emqx.io/docs/en/v5.0/gateway/gateway.html) |
| **ExHooks/gRPC**       | ✅        | ❌           | [gRPC Hook Extension](https://www.emqx.io/docs/en/v5.0/advanced/lang-exhook.html) |

## Operability and Observability

EMQX offers a user-friendly dashboard and extensive HTTP APIs. It supports monitoring with Prometheus, and Grafana. VerneMQ is easy to deploy and configure but lacks advanced management and monitoring features.

|                                  | **EMQX**     | **VerneMQ**     | **Notes and Links**                                          |
| :------------------------------- | :----------- | :-------------- | :----------------------------------------------------------- |
| **Dashboard**                    | ✅            | ❌               | [Dashboard](https://www.emqx.io/docs/en/v5.0/getting-started/dashboard.html) |
| **Configuration**                | HOCON Format | Key-Value Fomat |                                                              |
| **HTTP API**                     | ✅            | ✅               | [REST API](https://www.emqx.io/docs/en/v5.0/admin/api.html)  |
| **CLI**                          | ✅            | ✅               | [Command Line Interface](https://www.emqx.io/docs/en/v5.0/admin/cli.html) |
| **Config Hot update**            | ✅            | ❌               | [Configuration Files](https://www.emqx.io/docs/en/v5.0/admin/cfg.html) |
| **Metrics**                      | ✅            | ✅               | Node metrics:<br>[Metrics](https://www.emqx.io/docs/en/v5.0/observability/metrics-and-stats.html)<br>[$SYSTree](https://docs.vernemq.com/monitoring/systree)<br>[Monitor - Metrics CLI](https://docs.vernemq.com/monitoring/introduction) |
| **Grafana**                      | ✅            | ✅               | [EMQX \| Grafana Labs](https://grafana.com/grafana/dashboards/17446-emqx/)<br>[VerneMQ Node Metrics \| Grafana Labs](https://grafana.com/grafana/dashboards/16479-vernemq-node-metrics/) |
| **Cluster Metrics**              | ✅            | ✅               | [Metrics](https://www.emqx.io/docs/en/v5.0/observability/metrics-and-stats.html)<br>[Monitor - Metrics CLI](https://docs.vernemq.com/monitoring/introduction) |
| **Alarm Alerts**                 | ✅            | ❌               | [System Topic](https://www.emqx.io/docs/en/v5.0/advanced/system-topic.html#alarms-system-alarms) |
| **Slow Subscription Monitoring** | ✅            | ❌               | [Slow subscribers statistics](https://www.emqx.io/docs/en/v5.0/observability/slow_subscribers_statistics.html) |
| **Prometheus**                   | ✅            | ✅               | [Integrate with Prometheus](https://www.emqx.io/docs/en/v5.0/observability/prometheus.html#dashboard-update)<br>[Prometheus](https://docs.vernemq.com/monitoring/prometheus) |


## Conclusion

In short, EMQX is one of the best choices for deploying MQTT brokers in production in 2023. If you want to dive into how to design a distributed MQTT broker and understand the challenges involved, you can read the source code of [EMQX](https://github.com/emqx/emqx) and [VerneMQ](https://github.com/vernemq/vernemq) on GitHub.

## References

- [VerneMQ - A MQTT broker that is scalable, enterprise ready, and open source](https://vernemq.com/) 
- [VerneMQ Documentation](https://docs.vernemq.com/) 
- [EMQX: The World's #1 Open Source Distributed MQTT Broker](https://www.emqx.io/) 
- [EMQX 5.0 Documentation](https://www.emqx.io/docs/en/v5.0/) 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
