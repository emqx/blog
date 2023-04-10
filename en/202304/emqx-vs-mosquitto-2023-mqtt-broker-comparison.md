**Table of Contents**

- [Introduction](#introduction)
- [Mosquitto Overview](#mosquitto-overview)
- [EMQX Overview](#emqx-overview)
- [Community and Popularity](#community-and-popularity)
- [Scalability and Performance](#scalability-and-performance)
- [MQTT and Connectivity](#mqtt-and-connectivity)
- [Security](#security)
- [Authentication and Authorization](#authentication-and-authorization)
- [Rule Engine](#rule-engine)
- [Data Integration](#data-integration)
- [Operability and Observability](#operability-and-observability)
- [Cloud-Native and Kubernetes](#cloud-native-and-kubernetes)
- [Bridging Mosquitto to EMQX](#bridging-mosquitto-to-emqx)
- [Conclusion](#conclusion)
- [References](#references)


## Introduction

MQTT (Message Queuing Telemetry Transport) is a de facto standard messaging protocol for the Internet of Things (IoT). 

With the growth of the Internet of Things (IoT), MQTT brokers are becoming vital in connecting IoT devices and moving data between connected devices and cloud services.

[EMQX](https://www.emqx.io/) and [Mosquitto](https://mosquitto.org/) are two of the most popular open-source MQTT brokers. This blog post will provide an in-depth comparison of EMQX and Mosquitto as MQTT brokers in 2023.

## Mosquitto Overview

The Mosquitto project was initially developed by IBM and Eurotech in 2013 and later donated to the Eclipse Foundation in 2016, licensed under the Eclipse Public License (EPL/EDL license). As one of the world's most widely used MQTT brokers, Mosquitto has over 7k GitHub Stars as of March 2023.

Mosquitto is written in C/C++ and uses a single-threaded architecture. Mosquitto implements MQTT protocol versions 5.0, 3.1.1, and 3.1 and supports SSL/TLS and WebSockets. Its lightweight design makes Mosquitto suitable for deployment on embedded devices or servers with limited resources.

![Mosquitto MQTT Broker](https://assets.emqx.com/images/60243f02373956439d68b2008a8d0959.png)

**Pros:**

- Easy to setup and use
- MQTT 5.0 protocol support
- Lightweight and efficient
- Active community support

**Cons:**

- Limited scalability ( <100k )
- No clustering support
- Lacking enterprise features
- Limited Cloud-Native support

## EMQX Overview

The EMQX project was launched on GitHub in 2012 and is licensed under Apache version 2.0. EMQX is now the world's most scalable MQTT messaging server and is widely used in mission-critical business scenarios such as the IoT, Industrial IoT (IIoT), and Internet of Vehicles (IoV).

EMQX is written in Erlang/OTP, a programming language for building massively scalable soft real-time systems. Unlike Mosquitto, EMQX has adopted a masterless distributed architecture from its inception to achieve high availability and horizontal scalability. EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

See: [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) 

![100M MQTT connections with EMQX 5.0](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png)

**Pros:**

- Supports large-scale deployments
- High availability
- Horizontal scalability
- High-performance and reliable
- Rich enterprise features 
- Pioneering MQTT over QUIC 

**Cons:**

- Complex to set up
- Difficult to manage effectively

## Community and Popularity

[EMQX](https://github.com/emqx/emqx) is the highest-rated and most active MQTT Broker project on GitHub, with 11.4 stars and over 3,000 commits in the last 12 months.

[Mosquitto](https://github.com/eclipse/mosquitto) is more prevalent in deployment than EMQX with its lightweight single-thread architecture, especially on embedded devices with limited resources.

|                                     | **EMQX**                                    | **Mosquitto**                                            |
| :---------------------------------- | :------------------------------------------ | :------------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) |
| **Project Created**                 | 2012                                        | 2013                                                     |
| **Latest Release**                  | v5.0.21 (March 2023)                        | 2.0.15 (Aug 2022)                                        |
| **GitHub Stars**                    | 11.4k                                       | 7.2 k                                                    |
| **GitHub Forks**                    | 2k                                          | 2.1k                                                     |
| **GitHub Commits**                  | 14k+                                        | 2.8k+                                                    |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 500+                                                     |
| **GitHub Issues**                   | 3500+                                       | 2200+                                                    |
| **GitHub Releases**                 | 260+                                        | 60+                                                      |
| **GitHub PRs**                      | 6000+                                       | 600                                                      |
| **GitHub Contributors**             | 100+                                        | 110+                                                     |

<center>Community and Popularity (Mar 24, 2023)</center>

<br>

> **Note:** The Mosquitto project was created by Roger Light in 2008 and later acquired by Eclipse Foundation in 2013.

## Scalability and Performance

Mosquitto, as a lightweight MQTT broker, does not support clustering architecture but has excellent single-node performance. A server with a small resource footprint can support 10k concurrent MQTT connections.

EMQX, as a highly scalable distributed MQTT messaging broker, can support millions of concurrent connections on a single node and 100 million connections on a single cluster, but with much higher CPU and memory usage.

|                                              | **EMQX**                                                     | **Mosquitto**                                                | **Notes & Links**                                            |
| :------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Scalability**                              | - 4M MQTT connections per node<br>- 100M MQTT connections per cluster | <100K MQTT connections per node                              | [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **Performance**                              | - 2 million QoS0 MQTT msgs/sec per node<br>- 800k QoS1 msgs/sec<br>- 200k QoS2 msgs/sec | - Up to 120k QoS0 MQTT msgs/sec per node<br>- 80k QoS1 msgs/sec<br> - 60k QoS2 msgs/sec |                                                              |
| **Latency**                                  | 1-5 millisecond                                              | 1-1000 millisecond                                           |                                                              |
| **Clustering**                               | 20+ nodes of cluster                                         | ❌                                                            | [Cluster Scalability](https://www.emqx.io/docs/en/v5.0/deploy/cluster/db.html#node-roles) |
| **Elastic and Resilient scaling at runtime** | ✅                                                            | ❌                                                            |                                                              |
| **Auto Clustering**                          | ✅                                                            | ❌                                                            | [EMQX Node Discovery and Autocluster](https://www.emqx.io/docs/en/v5.0/deploy/cluster/intro.html#emqx-node-discovery-and-autocluster) |
| **Zero Downtime/Hot Upgrade**                | ✅                                                            | ❌                                                            | [Release Upgrade](https://docs.emqx.com/en/enterprise/v4.4/advanced/relup.html#release-upgrade) |

## MQTT and Connectivity

Mosiquitto implements the MQTT protocol versions 3.1/3.1.1/5.0, supporting the protocol specification for will messages, retained messages, shared subscriptions, and other capabilities and supporting MQTT over WebSocket.

EMQX fully supports MQTT 3.1/3.1.1/5.0 and [MQTT over Websocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) protocols. EMQX 5.0 also introduces groundbreaking support for [MQTT Over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic). With multiplexing and faster connection establishment and migration, it has the potential to become the next generation of the MQTT standard.

In addition, EMQX can be extended to support multiple protocol gateways, such as MQTT-SN, CoAP, LwM2M, and STOMP.

|                              | **EMQX**                                                     | **Mosquitto** | **Notes and Links**                                          |
| :--------------------------- | :----------------------------------------------------------- | :------------ | :----------------------------------------------------------- |
| **MQTT 3.1/3.1.1**           | ✅                                                            | ✅             | [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt) |
| **MQTT 5.0**                 | ✅                                                            | ✅             | [MQTT 5 Explore](https://www.emqx.com/en/mqtt/mqtt5)         |
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

## Security

Security is crucial for connecting IoT devices and data exchanged between connected devices and cloud services. Both Mosquitto and EMQX support secure connections based on TLS/SSL. In addition, EMQX supports QUIC transport, OCSP Stapling, Audit Logs, and source code scanning with Black Duck.

|                         | **EMQX** | **Mosquitto** | **Notes and Links**                                          |
| :---------------------- | :------- | :------------ | :----------------------------------------------------------- |
| **TLS/SSL**             | ✅        | ✅             | EMQX: TLS 1.1, 1.2, 1.3 ([Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)) |
| **QUIC**                | ✅        | ❌             | [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) |
| **OCSP Stapling**       | ✅        | ✅             | [EMQX Supports OCSP stapling](https://www.youtube.com/watch?v=e9SiF7ptvpU) |
| **Audit Logs**          | ✅        | ❌             |                                                              |
| **Black Duck Analysis** | ✅        | ❌             | Partner with Synopsis                                        |

## Authentication and Authorization

Regarding MQTT client authentication and access control, Mosiquitto provides a dynamic security plug-in that flexibly handles username/password authentication and access control.

EMQX has built-in support for multiple authentication mechanisms, such as [username-password authentication](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication), JWT authentication, and enhanced authentication based on the MQTT 5.0 protocol. Authentication in EMQX integrates with various data backends, including files, Redis, MySQL, PostgreSQL, MongoDB, etc.

In addition, EMQX provides flapping detect and blocklist features, enabling users to block specific clients by adding their IP address, clientId, or username to a blocklist via Dashboard and HTTP API. 

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

## Rule Engine

EMQX has a built-in SQL-based rule engine to help extract, filter, enrich, and transform MQTT messages in real-time within the broker.

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

## Data Integration

As a lightweight broker, Mosquitto does not support data integration. Users can write code to consume MQTT messages from Mosquitto and ingest them into external databases or cloud services.

EMQX, especially the Enterprise Edition, can seamlessly integrate with Kafka, databases, and cloud services using the built-in rule engine and out-of-the-box data bridge.

|                     | **EMQX**               | **Mosquitto** | **Notes and Links**                                          |
| :------------------ | :--------------------- | :------------ | :----------------------------------------------------------- |
| **Webhook**         | ✅                      | ✅             | [Webhook](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridge-webhook.html#example-setup-webhook-using-config-files) |
| **Rule Engine**     | ✅                      | ❌             | [Rule Engine](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) |
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

## Operability and Observability

Mosquitto offers fundamental logging and debugging capabilities for monitoring broker status and troubleshooting issues. However, it lacks advanced management and monitoring features, making it difficult to gain insight into the running status and optimize the performance.

EMQX provides rich and visual monitoring capabilities through HTTP API and Dashboard, making it easier to monitor and manage. In addition, EMQX supports integration with **Prometheus**, **StatsD**, and **Datadog**, enabling O&M teams to use third-party monitoring platforms easily.

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
| **StatsD**                       | ✅            | ❌               | [Integrate with StatsD](https://www.emqx.io/docs/en/v5.0/observability/statsd.html#statsd) |

## Cloud-Native and Kubernetes

EMQX and Mosquitto both support docker-based containerized deployments. EMQX has excellent Kubernetes Operator and Terraform support, making it easier to deploy and operate on public cloud platforms.

In addition, EMQX offers [serverless](https://www.emqx.com/en/cloud/serverless-mqtt), [dedicated](https://www.emqx.com/en/cloud/dedicated), and [BYOC](https://www.emqx.com/en/cloud/byoc) MQTT messaging services on over 17 Regions from AWS, Google Cloud, and Microsoft Azure worldwide.

|                         | **EMQX**                                      | **Mosquitto** | **Notes and Links**                                          |
| :---------------------- | :-------------------------------------------- | :------------ | :----------------------------------------------------------- |
| **Docker**              | ✅                                             | ✅             | [EMQX Docker](https://hub.docker.com/r/emqx/emqx)            |
| **Kubernetes Operator** | ✅                                             | ❌             | [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) |
| **Terraform**           | ✅                                             | ❌             | [EMQX Terraform](https://www.emqx.com/en/emqx-terraform)     |
| **Cloud Service**       | - Serverless<br>- Hosting/Dedicated<br>- BYOC | Hosting       |                                                              |

EMQX Kubernetes Operator: [https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator) 

![EMQX Kubernetes Operator](https://assets.emqx.com/images/f8483728a4241191e4f49ac3f8fa5740.png)

## Bridging Mosquitto to EMQX

Although EMQX and Mosquitto are two very different MQTT brokers, they can work perfectly with the MQTT bridge approach.

We can deploy Mosquitto on embedded hardware or gateways at the IoT edge, and then aggregate and ingest IoT data into a large-scale EMQX cluster in the cloud via an MQTT bridge.

See [Bridging Mosquitto MQTT Messages to EMQX](https://www.emqx.com/en/blog/bridging-mosquitto-to-emqx-cluster)

![Bridging Mosquitto to EMQX](https://assets.emqx.com/images/35635ecd1ac7c7453bce2d7c46ee1511.png)


## Conclusion

The comparison above shows that EMQX and Mosquitto are popular MQTT brokers catering to different needs and use cases.

Mosquitto, as a single-threaded lightweight MQTT Broker, is more suitable for deployment in embedded hardware, industrial gateways, and small servers for IoT edge.

EMQX is a highly scalable, distributed MQTT server with clustering architecture supporting high availability and horizontal scalability. It is more suitable for deployment in the cloud, providing mission-critical services for large-scale applications in IoT, IIoT, and connected cars.

In short, you can choose Mosquitto for embedded hardware and IoT edge deployments and use EMQX as a massively scalable, highly available MQTT messaging service in the cloud.

## References

- [Eclipse Mosquitto](https://mosquitto.org/) 
- [Eclipse Mosquitto Documentation](https://mosquitto.org/documentation/) 
- [EMQX: The World's #1 Open Source Distributed MQTT Broker](https://www.emqx.io/) 
- [EMQX 5.0 Documentation](https://www.emqx.io/docs/en/v5.0/) 
- [EMQX Enterprise Documentation](https://docs.emqx.com/en/enterprise/v5.0/) 
- [EMQX Operator Documentation](https://docs.emqx.com/en/emqx-operator/latest/) 
- [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
