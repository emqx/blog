## Introduction

[MQTT (Message Queue Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), originally designed as a lightweight publish/subscribe messaging transport, is now the de facto standard messaging protocol for the Internet of Things (IoT). An [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) is critical in connecting clients, such as IoT devices, and moving MQTT messages between them.

![publish/subscribe](https://assets.emqx.com/images/b5d67261f50a597d5d37b97eebc1cdf5.png)

As [a16z](https://a16z.com/) said over a decade ago, ["Software is eating the world."](https://a16z.com/2011/08/20/why-software-is-eating-the-world/) Open source is eating up software. More than 20 open-source MQTT broker implementations are available today, making the selection process challenging for software architects and developers.

In this post series, we’ll explore the top open-source MQTT brokers in 2023 and compare them in-depth to help you choose the best one for your needs.

## Evaluation Criteria:  Community and Popularity

To thoroughly compare open-source MQTT brokers in 2023, it is essential to consider the following evaluation criteria:

- **Community**: evaluated by the number of GitHub stars, contributors, and issues.
- **Popularity**: evaluated by examining the user base, downloads, and docker pulls.
- **Project Activity**: evaluated the frequency of GitHub commits, PRs, and releases, especially those made within the last 12 months.

Based on the criteria, we choose to focus on four popular open-source MQTT brokers that have the most influence in the open-source community:

- **EMQX**: This is the most starred MQTT broker on GitHub, with 11.4k stars.
- **Mosquitto**: This is the second-most-starred but the most prevalent among MQTT brokers.
- **NanoMQ**: This is the latest and one of the most active MQTT brokers available.
- **VerneMQ**: Although not actively developing on Github, this MQTT broker has the third-highest number of stars.

Here is a summary of the four projects hosted on GitHub:

|                                     | **EMQX**                                    | **Mosquitto**                                            | **NanoMQ**                                      | **VerneMQ**                                          |
| :---------------------------------- | :------------------------------------------ | :------------------------------------------------------- | :---------------------------------------------- | :--------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) | [NanoMQ GitHub](https://github.com/emqx/nanomq) | [VerneMQ GitHub](https://github.com/vernemq/vernemq) |
| **Project Created**                 | 2012                                        | 2009                                                     | 2020                                            | 2014                                                 |
| **License**                         | Apache Version 2.0                          | EPL/EDL License                                          | MIT License                                     | Apache Version 2.0                                   |
| **Programming Language**            | Erlang                                      | C/C++                                                    | C                                               | Erlang                                               |
| **Latest Release**                  | v5.0.23 (April 2023)                        | 2.0.15 (Aug 2022)                                        | v0.17.0 (March 2023)                            | v1.12.6.2 (Nov. 2022)                                |
| **GitHub Stars**                    | **11.5k**                                   | **7.2k**                                                 | **800+**                                        | **3k**                                               |
| **GitHub Commits**                  | 14k+                                        | 2800+                                                    | 2000+                                           | 2400+                                                |
| **GitHub Commits (Last 12 Months)** | **3000+**                                   | **500+**                                                 | **1200+**                                       | **50+**                                              |
| **GitHub Issues**                   | 3500+                                       | 2200+                                                    | 120+                                            | 1300+                                                |
| **GitHub Releases**                 | 260+                                        | 60+                                                      | 75+                                             | 40                                                   |
| **GitHub PRs**                      | 6000+                                       | 600                                                      | 780+                                            | 600                                                  |
| **GitHub Contributors**             | 100+                                        | 110+                                                     | 20+                                             | 50                                                   |

## Overview of Top Open Source MQTT Brokers

### EMQX

[EMQX](https://www.emqx.io/) is one of the most popular MQTT brokers and has 11.5k stars on GitHub. The EMQX project was launched in 2012 and is licensed under Apache version 2.0. EMQX is written in Erlang/OTP, a programming language for building massively scalable soft real-time systems.

EMQX is the world's most scalable MQTT broker that supports advanced features such as MQTT 5.0, MQTT-SN, and MQTT over QUIC. It supports masterless clustering for high availability and horizontal scalability. EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

See: [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

![MQTT Cluster](https://assets.emqx.com/images/9abfe5ee5df4f1c544915f5e4605b253.png)

EMQX offers rich enterprise features, data integration, cloud hosting services, and commercial support from [EMQ Technologies Inc.](https://www.emqx.com/en) Over the years, EMQX has gained popularity among enterprises, startups, and individuals due to its performance, reliability, and scalability. EMQX is widely used for business-critical applications in various industries, such as IoT, [industrial IoT](https://www.emqx.com/en/use-cases/industrial-iot), [connected cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know), [manufacturing](https://www.emqx.io/use-cases#manufacturing), and telecommunications.

Official Website: [https://www.emqx.io/](https://www.emqx.io/)

GitHub: [https://github.com/emqx/emqx](https://github.com/emqx/emqx)

**Pros:**

- Supports large-scale deployments
- High availability
- Horizontal scalability
- High-performance and low-latency
- Rich enterprise features
- Pioneering [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)

**Cons:**

- Complex to set up and configure
- Difficult to manage effectively
- Logs may be confusing

<section class="promotion">
    <div>
        Download EMQX
      <div class="is-size-14 is-text-normal has-text-weight-normal">The most scalable open-source MQTT broker for IoT, IIoT, and connected vehicles.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=broker" class="button is-gradient px-5">Download →</a>
</section>

### Mosquitto 

The Mosquitto project was initially developed by Roger Light in 2009 and later donated to the Eclipse Foundation, licensed under the Eclipse Public License (EPL/EDL license). As of March 2023, it is the most widely deployed open-source MQTT broker with a large community and over 7k GitHub stars.

Mosquitto is written in C/C++ and uses a single-threaded architecture. Mosquitto implements MQTT protocol versions 5.0, 3.1.1, and 3.1, and supports SSL/TLS and WebSocket. Its lightweight design makes Mosquitto suitable for deployment on embedded devices or servers with limited resources.

Mosquitto is known for its small booting footprint of about 200k. However, it does not provide native support for multi-threading or clustering. Mosquitto is available for various platforms, including Linux, Windows, and macOS.

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

Official website: [https://mosquitto.org/](https://mosquitto.org/)

GitHub: [https://github.com/eclipse/mosquitto](https://github.com/eclipse/mosquitto)

**Pros:**

- Easy to setup and use
- MQTT 5.0 protocol support
- Lightweight and small footprint
- Active community support

**Cons:**

- Single-threaded architecture
- Limited scalability in production ( <100k )
- No clustering support
- Lacking enterprise features
- Limited cloud-native support

### NanoMQ

[NanoMQ](https://nanomq.io/), an open-source project released in 2020, is a lightweight and fast MQTT messaging broker designed for edge computing scenarios in the Internet of Things (IoT). 

NanoMQ is implemented in purely C, based on NNG's asynchronous I/O with a multi-threading [Actor Model](https://en.wikipedia.org/wiki/Actor_model). It fully supports MQTT 3.1.1 and MQTT 5.0 protocol versions and pioneers MQTT over QUIC.

NanoMQ is lightweight and high-performance, making it suitable for various edge computing platforms. It is highly compatible and portable, relying solely on the native POSIX API. This makes it easy to deploy on any POSIX-compatible platform and runs smoothly on various CPU architectures, including x86_64, ARM, MIPS, and RISC-V.

![NanoMQ](https://assets.emqx.com/images/44a45e8732eef0076a95f095f6551d2e.png)

Official website: [https://nanomq.io/](https://nanomq.io/)

GitHub: [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq)

**Pros**

- Lightweight design
- Multi-threading and Async IO
- Highly portable
- Small booting footprint
- Easy to deploy
- Bridging with brokerless protocols

**Cons**

- No clustering support
- Small community and user base
- Lack of documentation and tutorials
- Lack of enterprise features (data Integrations)

<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>

### VerneMQ

The VerneMQ project was launched in [2014](https://github.com/vernemq/vernemq/tree/3c7703f0d62e758ba22a34ceb756f2ac2a4da44a) and initially developed by [Erlio GmbH](https://vernemq.com/company.html). The project is licensed under Apache Version 2.0. It supports MQTT versions 3.1, 3.1.1, and 5.0. As the second broker wrote in Erlang/OTP, it borrowed [some code](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl) from the EMQX project.

Regarding architectural design, VerneMQ is designed to handle millions of concurrent connections and messages with low latency and high throughput. It supports MQTT message persistence in LevelDB and uses a clustering architecture based on the [Plumtree](https://github.com/lasp-lang/plumtree) library, which implements [the Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf) algorithm.

Unfortunately, this Plumtree cluster architecture has not proven to work, even though it seems perfect in theory. The VerneMQ team and community have spent many years trying to make it work, fixing problems such as network split, data inconsistency, and crash recovery. 

Finally, the project has stopped being actively developed and maintained, with only about 50 commits in the last 12 months.

Official website: [https://www.vernemq.com/](https://www.vernemq.com/)

GitHub: [https://github.com/vernemq/vernemq](https://github.com/vernemq/vernemq)

**Pros:**

- High availability
- Horizontal scalability
- Message persistence

**Cons:**

- Not proofed clustering
- Limited documentation
- Limited enterprise features
- Not actively developing

## Scalability, Performance, and Reliability

Before we dive into the comparison of features and capabilities of these MQTT brokers, let's review their scalability, availability, performance, latency, and reliability first.

- Scalability: Can the broker scale horizontally to handle millions of concurrent MQTT connections?
- Availability: Does the broker support highly available clustering for mission-critical applications?
- Performance: How many [QoS/0/1/2](https://www.emqx.com/en/blog/introduction-to-mqtt-qos) MQTT messages per second can the broker route and deliver?
- Latency:  How fast can the broker dispatch and deliver an MQTT message from one [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) to another?
- Reliability:  Does the broker support MQTT message persistence and delivery without data loss?

Below is a brief analysis of the four MQTT brokers: 

|                                          | **EMQX**                                  | **Mosquitto**                           | **NanoMQ**                                  | **VerneMQ**                             |
| :--------------------------------------- | :---------------------------------------- | :-------------------------------------- | :------------------------------------------ | :-------------------------------------- |
| **Scalability**                          |                                           |                                         |                                             |                                         |
| Multi-threading                          | Yes                                       | No                                      | Yes                                         | Yes                                     |
| Asynchronous I/O                         | Yes                                       | Yes                                     | Yes                                         | Yes                                     |
| Clustering                               | Yes (over 20 nodes cluster)               | No                                      | No                                          | Yes                                     |
| MQTT connections per node                | 4M                                        | 100k                                    | 100k                                        | 1M                                      |
| MQTT connections per cluster             | 100M                                      | N/A                                     | N/A                                         | **?**                                   |
| **Availability**                         |                                           |                                         |                                             |                                         |
| Masterless Clustering Architecture       | Yes                                       | No                                      | No                                          | Yes                                     |
| Elastic and Resilient scaling at runtime | Yes                                       | No                                      | No                                          | Yes                                     |
| Auto Clustering                          | Yes                                       | No                                      | No                                          | No                                      |
| Overload Protection                      | Yes                                       | No                                      | No                                          | Yes                                     |
| Fault tolerance                          | Yes                                       | No                                      | No                                          | **?**                                   |
| **Performance (per node)**               |                                           |                                         |                                             |                                         |
| QoS0 msgs/sec                            | 2 million                                 | 120k                                    | 500k                                        | **?**                                   |
| QoS1 msgs/sec                            | 800k                                      | 80k                                     | 400k                                        | **?**                                   |
| QoS2 msgs/sec                            | 200k                                      | 40k                                     | 200k                                        | **?**                                   |
| **Latency**                              |                                           |                                         |                                             |                                         |
| Latency (varies on different scenarios)  | Single-digit millisecond latency at scale | Up to seconds latency in some scenarios | Less than 10 milliseconds in most scenarios | Up to seconds latency in some scenarios |
| **Reliability**                          |                                           |                                         |                                             |                                         |
| Message Persistence                      | In RocksDB and External Databases         | In Files                                | In SQLite                                   | In LevelDB                              |
| Zero Downtime/Hot  Upgrade               | Yes                                       | No                                      | No                                          | No                                      |
| Hot Patch                                | Yes                                       | No                                      | No                                          | No                                      |

> **?** *here means that we were unable to find any publicly available documentation or files that could serve as evidence regarding the item under discussion.*

## MQTT Protocol and Connectivity

All the presented brokers fully implement MQTT versions 3.1.1 and 5.0 and support [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) and SSL/TLS encryption. Additionally, EMQX supports MQTT-SN, CoAP, and LwM2M protocol gateways. NanoMQ supports brokerless mode and can work with DDS, ZeroMQ, and Nanomsg.

EMQX and NanoMQ have committed to advancing the MQTT standard. They are pioneers in implementing MQTT over QUIC, the next generation of MQTT protocol that aims to optimize further IoT communication.

|                        | **EMQX** | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :--------------------- | :------- | :------------ | :--------- | :---------- |
| MQTT 3.1/3.1.1         | Yes      | Yes           | Yes        | Yes         |
| MQTT 5.0               | Yes      | Yes           | Yes        | Yes         |
| MQTT-SN 1.2            | Yes      | No            | No         | No          |
| MQTT over TCP          | Yes      | Yes           | Yes        | Yes         |
| MQTT over SSL/TLS      | Yes      | Yes           | Yes        | Yes         |
| MQTT over WebSocket    | Yes      | Yes           | Yes        | Yes         |
| **MQTT over QUIC**     | Yes      | No            | Yes        | No          |
| MQTT Bridging          | Yes      | Yes           | Yes        | Yes         |
| Shared Subscription    | Yes      | Yes           | Yes        | Yes         |
| Retained Message       | Yes      | Yes           | Yes        | Yes         |
| Will Message           | Yes      | Yes           | Yes        | Yes         |
| MQTT Request/Response  | Yes      | Yes           | Yes        | Yes         |
| LB (Proxy Protocol)    | Yes      | No            | No         | Yes         |
| Multi-protocol Gateway | Yes      | No            | No         | No          |
| CoAP                   | Yes      | No            | No         | No          |
| LwM2M                  | Yes      | No            | No         | No          |
| DDS Gateway            | No       | No            | Yes        | No          |
| ZeroMQ Gateway         | No       | No            | Yes        | No          |
| Nanomsg/NNG            | No       | No            | Yes        | No          |

## Security, Authentication & Authorization

Security is crucial for connecting IoT devices and data exchanged between connected devices using MQTT brokers. All the compared brokers support secure connections based on TLS/SSL and authentication and authorization mechanisms such as [username/password](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication), JWT, X.509 certificates, and [access control lists](https://www.emqx.com/en/blog/authorization-in-mqtt-using-acls-to-control-access-to-mqtt-messaging). 

Additionally, EMQX offers advanced security features like integration with external databases, OCSP Stapling, fine-grained access control policies, flapping detection, and support for OAuth 2.0 authorization.

|                                   | **EMQX**       | **Mosquitto**          | **NanoMQ** | **VerneMQ**            |
| --------------------------------- | -------------- | ---------------------- | ---------- | ---------------------- |
| TLS/SSL                           | Yes            | Yes                    | Yes        | Yes                    |
| OCSP Stapling                     | Yes            | Yes                    | No         | No                     |
| Username/Password Authentication  | Yes            | Yes                    | Yes        | Yes                    |
| X.509 Certificates Authentication | Yes            | Yes                    | Yes        | Yes                    |
| JWT Authentication                | Yes            | Yes (via auth plugin)  | No         | **?**                  |
| LDAP Authentication               | Yes            | Yes (via auth plugin)  | No         | Yes (via plugin)       |
| Fine-grained Access Control       | Yes            | Yes                    | Yes        | Yes                    |
| Authorization using Databases     | Yes (built-in) | Yes (via auth plugins) | No         | Yes (via auth plugins) |
| Flapping Detection                | Yes            | No                     | No         | No                     |
| Audit Logs                        | Yes            | No                     | No         | No                     |

## Data Integrations (Out-of-the-Box)

All the brokers support integration with external services using REST APIs and WebHook. As lightweight brokers, Mosquitto and NanoMQ do not support data integration. Users can write code to consume MQTT messages from Mosquitto and ingest them into external databases or cloud services.

EMQX implements a built-in SQL-based rule engine to help extract, filter, enrich, and transform MQTT messages in real time within the broker. And the Enterprise Edition of EMQX can seamlessly integrate with Kafka, databases, and cloud services using out-of-the-box data bridges.

|                 | **EMQX**                 | **Mosquitto** | **NanoMQ**    | **VerneMQ** |
| --------------- | ------------------------ | ------------- | ------------- | ----------- |
| WebHook         | Yes                      | Yes           | Yes           | Yes         |
| Rule Engine     | Yes                      | No            | Yes (limited) | No          |
| Message Codec   | Yes                      | No            | No            | No          |
| Schema Registry | Yes                      | No            | No            | No          |
| Data Bridge     | Yes                      | No            | No            | No          |
| Confluent/Kafka | Yes (Enterprise Edition) | No            | No            | No          |
| SAP Event Mesh  | Yes (Enterprise Edition) | No            | No            | No          |
| Apache Pulsar   | Yes (Enterprise Edition) | No            | No            | No          |
| RabbitMQ        | Yes (Enterprise Edition) | No            | No            | No          |
| MySQL           | Yes (Enterprise Edition) | No            | No            | No          |
| PostgreSQL      | Yes (Enterprise Edition) | No            | No            | No          |
| SQL Server      | Yes (Enterprise Edition) | No            | No            | No          |
| MongoDB         | Yes (Enterprise Edition) | No            | No            | No          |
| AWS DynamoDB    | Yes (Enterprise Edition) | No            | No            | No          |
| ClickHouse      | Yes (Enterprise Edition) | No            | No            | No          |
| InfluxDB        | Yes (Enterprise Edition) | No            | No            | No          |
| TimeScaleDB     | Yes (Enterprise Edition) | No            | No            | No          |
| Oracle          | Yes (Enterprise Edition) | No            | No            | No          |
| Redis           | Yes (Enterprise Edition) | No            | No            | No          |
| Cassandra       | Yes (Enterprise Edition) | No            | No            | No          |

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

## Operability, Observability, and Compatibility

Each broker is user-friendly and equipped with essential logging and debugging features to monitor their status and troubleshoot issues effectively. They can run on various operating systems and public cloud platforms. Besides, EMQX has excellent support for Kubernetes Operator and Terraform.

Additionally, EMQX provides rich visual monitoring capabilities through HTTP API and Dashboard, making it easier to monitor and manage. In addition, EMQX supports integration with **Prometheus** and **Grafana**, enabling O&M teams to use third-party monitoring platforms easily.

See: [Monitoring MQTT broker with Prometheus and Grafana](https://www.emqx.com/en/blog/emqx-prometheus-grafana)

|                     | **EMQX**                                                     | **Mosquitto**    | **NanoMQ**    | **VerneMQ**      |
| ------------------- | ------------------------------------------------------------ | ---------------- | ------------- | ---------------- |
| Dashboard           | Yes                                                          | No               | No            | No               |
| Configuration       | HOCON Format                                                 | Key-value Format | HOCON Format  | Key-value Format |
| Config Hot update   | Yes                                                          | No               | Yes (Limited) | No               |
| REST API            | Yes                                                          | Yes              | Yes           | Yes              |
| CLI                 | Yes                                                          | Yes              | Yes           | Yes              |
| Remote Console      | Yes                                                          | No               | No            | Yes              |
| Metrics             | Yes                                                          | Yes              | Yes           | Yes              |
| Grafana Integration | Yes                                                          | Yes              | Yes           | Yes              |
| Prometheus          | Yes                                                          | Yes              | Yes           | Yes              |
| Docker              | Yes                                                          | Yes              | Yes           | Yes              |
| Kubernetes Operator | Yes ([EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator)) | No               | No            | No               |
| Terraform           | Yes ([EMQX Terraform](https://www.emqx.com/en/emqx-terraform)) | No               | No            | No               |

## Head-to-Head Comparison Chart

Finally, we summarize an overall evaluation of the top open-source MQTT brokers in the following chart.

|                               | **EMQX**  | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :---------------------------- | :-------- | :------------ | :--------- | :---------- |
| Scalability                   | Excellent | Moderate      | Good       | Good        |
| Availability                  | Excellent | Moderate      | Moderate   | Good        |
| Performance                   | Excellent | Excellent     | Excellent  | Good        |
| Latency                       | Excellent | Good          | Excellent  | Good        |
| Reliability                   | Good      | Good          | Good       | Moderate    |
| Security                      | Excellent | Excellent     | Good       | Good        |
| Authenticaton & Authorization | Excellent | Good          | Moderate   | Good        |
| Connectivity                  | Excellent | Good          | Good       | Good        |
| Integration                   | Excellent | Moderate      | Moderate   | Moderate    |
| Operability                   | Good      | Excellent     | Good       | Moderate    |
| Observability                 | Excellent | Moderate      | Moderate   | Good        |
| Compatibility                 | Good      | Excellent     | Excellent  | Good        |
| Ease of Use                   | Good      | Excellent     | Good       | Good        |
| Community Support             | Excellent | Excellent     | Good       | Moderate    |

## Final Thoughts on the Comparison

Over the past decade, open-source MQTT brokers have led the way in innovating MQTT technology.  These brokers have played a significant role in advancing the functionality, scalability, and interoperability of the MQTT messaging protocol. Without these contributions, MQTT may not have become as widely adopted and versatile as it is today.

Choosing an MQTT broker depends on various factors, such as the number of connected devices, message throughput, and integration requirements. From the comparison, we can conclude that [EMQX](https://www.emqx.io/) is a highly scalable and enterprise-grade broker for large-scale, mission-critical deployments in the cloud. While Mosquitto and [NanoMQ](https://nanomq.io/) are fast and lightweight, making them suitable for deployment on resource-constrained embedded hardware, industrial gateways, and IoT edge servers.

## Future Developments

With the rapid expansion of IoT, the number of connected devices is predicted to exceed 100 billion by 2030. As a result, MQTT is poised to become even more indispensable and could potentially serve as the nervous system of the IoT.

Several exciting technological advancements are in the pipeline, including MQTT over QUIC, [MQTT Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), MQTT Unified Namespace, and more. To learn more about these developments, feel free to check out our blog posts at:

- [Shaping the Future of IoT: 7 MQTT Technology Trends in 2023](https://www.emqx.com/en/blog/7-mqtt-trends-in-2023) 
- [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) 

## References

[1] [125 billion IoT devices by 2030 says IHS Markit](https://www.tvbeurope.com/tvbeverywhere/125-billion-iot-devices-2030-ihs-markit) 

[2] [Comparison of MQTT implementations](https://en.wikipedia.org/wiki/Comparison_of_MQTT_implementations) 

[3] [A Comparison of MQTT Brokers for Distributed IoT Edge Computing](https://link.springer.com/chapter/10.1007/978-3-030-58923-3_23)

[4] [Open MQTT benchmark suite blog series](https://www.emqx.com/en/blog/tag/mqtt-benchmark)

[5] [2023 MQTT broker comparison blog series](https://www.emqx.com/en/blog/tag/2023-mqtt-broker-comparison)



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
