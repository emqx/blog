## Introduction

[Mosquitto](https://mosquitto.org/) and [NanoMQ](https://nanomq.io/) are fast, lightweight open-source message brokers written in C/C++, fully implementing MQTT version 3.1.1 and 5.0.

Although Mosquitto and NanoMQ are both lightweight and have a low CPU/memory footprint, they adopt very different architectural designs. Mosquitto is single-threaded, and NanoMQ is built on NNG's asynchronous I/O with a multi-threading model.

Both are suitable for industrial IoT and embedded devices with constrained resources. This blog post will compare the features, performance, tech details, and use cases of two brokers in 2023.

## Mosquitto Overview

The Mosquitto project was initially developed by Roger Light in 2009 and later donated to the Eclipse Foundation, licensed under the Eclipse Public License (EPL/EDL license).

Mosquitto’s design is straightforward and clean. It runs as a single-threaded daemon process with epoll support. It receives incoming data from one socket and dispatches it to other sockets.

Although simple, this architectural design restricts Mosquitto from using multi-core CPUs to connect more concurrent MQTT clients. At the same time, latency will increase as throughput increases.

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

**Pros:**

- Easy to setup and use
- MQTT 5.0 protocol support
- Lightweight and fast
- Active community support

**Cons:**

- Limited scalability ( <100k )
- No clustering support
- Lacking enterprise features
- Limited cloud-native support

## NanoMQ Overview

The [NanoMQ](https://github.com/emqx/nanomq) project was initially developed by [EMQ Technologies Inc.](https://www.emqx.com/en/about) in 2020 to provide a lightweight and fast MQTT broker with multi-threading support for the IoT edge. The project is under the MIT license and will be donated to the LF Edge Foundation before Q3 in 2023.

Unlike Mosquitto's single-threaded design, NanoMQ built on NNG's asynchronous I/O with a built-in Actor multi-threading model. Thanks to the excellent NNG library, NanoMQ takes full advantage of multiple cores in modern SMP systems. 

NanoMQ is also an edge messaging bus that converts protocols such as DDS, NNG, and ZeroMQ to MQTT, then bridges the MQTT messages between brokers or from the edge to multiple clouds via MQTT and QUIC.

In addition, NanoMQ is highly portable and can be deployed on any POSIX-compatible platform, and runs on different CPU architectures such as x86_64, ARM, MIPS, and RISC-V.

![NanoMQ MQTT Broker](https://assets.emqx.com/images/892a0de52bd6288686aec1f0bbc330d9.png)

<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>

## Community and Popularity

[Mosquitto](https://github.com/eclipse/mosquitto) is one of the most popular MQTT brokers and is prevalent in deployment on embedded hardware with its lightweight design. 

As a project launched in 2020, NanoMQ is in its early stages but is actively developing and evolving, with over 1000 commits in the last 12 months.

Both open-source projects are hosted on GitHub. The following community metrics are available:

|                                     | **Mosquitto**                                            | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------------------- | :---------------------------------------------- |
| **GitHub Project**                  | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) | [NanoMQ GitHub](https://github.com/emqx/nanomq) |
| **Project Created**                 | 2009                                                     | 2020                                            |
| **License**                         | EPL/EDL License                                          | MIT License                                     |
| **Programming Language**            | C/C++                                                    | C                                               |
| **Latest Release**                  | 2.0.15 (Aug 2022)                                        | v0.17.0 (March 2023)                            |
| **GitHub Stars**                    | 7.1 k                                                    | 800+                                            |
| **GitHub Commits**                  | 2.8k+                                                    | 1.9k+                                           |
| **GitHub Commits (Last 12 Months)** | 500+                                                     | 1200+                                           |
| **GitHub Releases**                 | 60+                                                      | 75+                                             |
| **GitHub PRs**                      | 600                                                      | 780+                                            |
| **GitHub Contributors**             | 100+                                                     | 20+                                             |

## Features and Capabilities

Mosquitto and NanoMQ fully implement MQTT 3.1/3.1.1/5.0 protocol versions, supporting the protocol specification for will messages, retained messages, shared subscriptions, and other capabilities.

Regarding the transports, both support MQTT over TCP, TLS/SSL, and WebSocket. NanoMQ as the broker designed in 2020, introduces [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) with multiplexing and faster connection establishment and migration support.

In addition, NanoMQ provides some features for management and integration, such as HTTP API, WebHook, On/Off-line Event Hook, and Rule Engine. NanoMQ’s portfolio is one of the broadest in edge computing. So you can get the exact features you need from a single broker and get more done with less time for your newly developed edge application. 

|                            | **Mosquitto**    | **NanoMQ**   |
| :------------------------- | :--------------- | :----------- |
| **MQTT 3.1.1**             | ✅                | ✅            |
| **MQTT 5.0**               | ✅                | ✅            |
| **MQTT over TLS/SSL**      | ✅                | ✅            |
| **MQTT over WebSocket**    | ✅                | ✅            |
| **MQTT over QUIC**         | ❌                | ✅            |
| **MQTT Bridging**          | ✅                | ✅            |
| **AWS Bridging**           | ❌                | ✅            |
| **DDS Proxy**              | ❌                | ✅            |
| **HTTP API**               | ❌                | ✅            |
| **WebHook**                | ❌                | ✅            |
| **Rule Engine**            | ❌                | ✅            |
| **On/Off-line Event Hook** | ❌                | ✅            |
| **Message Persistence**    | ✅ In Files       | ✅ In SQLite  |
| **Authentication & ACL**   | ✅                | ✅            |
| **Configuration**          | Key-value Format | HOCON Format |
| **CLI**                    | ✅                | ✅            |
| **Clustering**             | ❌                | ❌            |
| **Docker**                 | ✅                | ✅            |
| **Cross Platform**         | ✅                | ✅            |
| **SMP Support**            | ❌                | ✅            |

## Scalability and Performance 

NanoMQ, a modern designed MQTT broker for edge computing, continuously evolves to meet new performance and scalability requirements, space constraints, concurrency, and latency. With an advanced built-in Actor threading model, NanoMQ is highly versatile, can scale from single to dozens of cores, and supports superior throughput with low latency. Therefore, Users are granted maximum choices: any performance, any CPU cores, and any feature set, easy to scale and migrate when your requirements grow or change. Whether you are designing a smart home gateway or industrial robotics or drones, or even sophisticated intelligence vehicles, NanoMQ can always fit in.

Mosquitto, on the other hand, targets traditional embedded scenarios, which means it is more resource-friendly and consumes less memory and CPU. Therefore, Mosquitto is ideal for IoT sensors and devices with low processing power, while NanoMQ is suitable for high-performance gateways and servers. Additionally, Mosquitto, as an open-source project with a long legacy, assures stability; it is the best fit when users only have limited performance and feature requests and a swift project development cycle. 

See: [Mosquitto vs NanoMQ Performance Benchmark Report](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mosquitto-vs-nanomq).

|                 | **Mosquitto**                                                | **NanoMQ**                                                   |
| :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Scalability** | 160k                                                         | 160k MQTT connections per node                               |
| **Performance** | Up to 120k QoS0 MQTT msgs/sec per node<br>80k QoS1 msgs/sec<br>40k QoS2 msgs/sec | Up to 1 million+ QoS0 MQTT msgs/sec per node<br>800k QoS1 msgs/sec<br>400k QoS2 msgs/sec |
| **Latency**     | Up to seconds latency in some scenarios                                            | Less than 10 milliseconds in most scenarios                                            |

## Ease of Use

Mosquitto and NanoMQ have small install packages and are easy to set up. But both lack advanced management and monitoring features such as Dashboard.

Mosquitto uses a configuration file in a key-value format, making it configure intuitively. It also comes with comprehensive documentation and an active user community.

In contrast, NanoMQ may pose a challenge for beginners due to its more advanced configuration requirements. But for experienced users, it offers more control and customization options.

|                    | **Mosquitto**    | **NanoMQ**   | **Notes and Links**                                          |
| :----------------- | :--------------- | :----------- | :----------------------------------------------------------- |
| **Configuration**  | Key-Value Format | HOCON Format |                                                              |
| **HTTP API**       | ❌                | ✅            | [REST API](https://nanomq.io/docs/en/latest/http-api/v4.html) |
| **CLI**            | ✅                | ✅            | [Command Line Interface](https://nanomq.io/docs/en/latest/toolkit.html#client) |
| **Dashboard**      | ❌                | ❌            |                                                              |
| **Grafana**        | ❌                | ❌            |                                                              |
| **Prometheus**     | ❌                | ❌            |                                                              |
| **Docker**         | ✅                | ✅            | [NanoMQ Docker](https://hub.docker.com/r/emqx/nanomq)        |
| **Cross Platform** | ✅                | ✅            |  


## Bridging to EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is a highly scalable MQTT messaging service built on the open-source distributed [EMQX broker](https://www.emqx.io/). We can easily bridge Mosquitto or NanoMQ at the IoT edge to the EMQX Cloud service.

![Bridge Mosquitto to EMQX Cloud](https://assets.emqx.com/images/05b6602329f65d45aa2c87d115e2f51e.png)

## Future Outlook

Mosquitto version 2.0 introduced epoll support to address the c10k connection scalability issue.

NanoMQ is pioneering [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), the most innovative advancement in the MQTT protocol since the first release of the MQTT 5.0 specification in 2017. With multiplexing and faster connection establishment and migration, MQTT over QUIC has the potential to become the next generation of the MQTT standard. NanoMQ commits minor innovations like QoS prioritization and stream-topic pairing based on QUIC to fasten the pace of QUIC adoption.

## Conclusion

In conclusion, Mosquitto and NanoMQ are excellent lightweight [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for messaging at the IoT edge. You can choose any for your deployments on low-power sensors, embedded hardware, and industrial IoT in 2023.

## References

1. [Eclipse Mosquitto](https://mosquitto.org/) 
2. [Mosquitto Documentation](https://mosquitto.org/documentation/) 
3. [NanoMQ: An Ultra-lightweight MQTT Broker for IoT Edge](https://nanomq.io/) 
4. [NanoMQ Documentation](https://nanomq.io/docs/en/latest/) 
5. [NanoMQ GitHub](https://github.com/emqx/nanomq) 
6. [Mosquitto GitHub](https://github.com/eclipse/mosquitto)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
