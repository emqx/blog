## 引言

[Mosquitto](https://mosquitto.org/) 和 [NanoMQ](https://nanomq.io/zh) 都是用 C/C++ 开发的快速轻量的开源 MQTT Broker，完全支持 MQTT 3.1.1 和 5.0。

虽然 Mosquitto 和 NanoMQ 都具有轻量级和低资源消耗的特点，但它们的架构设计却截然不同。Mosquitto 采用单线程模式，而 NanoMQ 则基于 NNG 的异步 I/O 实现了多线程并行。

两者都很适用于[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)和嵌入式设备等资源受限的场景。本文将从功能、性能、技术细节和应用场景等方面对这两款 Broker 进行详细的对比分析。

## Mosquitto 简介

Mosquitto 是由 Roger Light 在 2009 年开发的开源 MQTT 消息 Broker（EPL/EDL 许可证），后来捐赠给了 Eclipse 基金会。

Mosquitto 设计简洁高效，以单线程守护进程的形式运行，并支持 epoll。它能够接收某个套接字传入的数据，然后将其转发给其他套接字。

Mosquitto 虽然易于实现，但也存在一些局限性。由于它采用了单线程的架构，无法利用多核 CPU 来处理更多的 MQTT 并发连接。而且，随着消息吞吐量的增长，它的延迟也会随之增加。

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

**优点：**

- 上手简单
- 支持 MQTT 5.0 协议
- 资源占用少，运行速度快
- 拥有活跃的开源社区

**缺点：**

- 扩展性有限（<10万）
- 不支持集群
- 缺少企业级功能
- 有限的云原生支持

## NanoMQ 简介

[NanoMQ](https://github.com/nanomq/nanomq) 是 EMQ 于 2020 年发布的一个开源项目（MIT 许可证），旨在为物联网边缘场景提供轻量级、快速、支持多线程的 MQTT Broker。该项目计划在 2023 年 Q3 之前捐赠给 LF Edge 基金会。

与 Mosquitto 的单线程设计不同，NanoMQ 基于 NNG 的异步 I/O 构建，内置 Actor 多线程模型。这使得 NanoMQ 能够充分发挥现代 SMP 系统的多核优势。

NanoMQ 还可以用作边缘消息总线，可以将 DDS、NNG、ZeroMQ 等协议转换为 MQTT，然后通过 MQTT 或者 QUIC 在 Broker 之间或从边缘到云之间桥接 MQTT 消息。

它具备高度的可移植性，可以部署在任何支持 POSIX 标准的平台上，并且可以在多种 CPU 架构上运行，包括 x86_64、ARM、MIPS 和 RISC-V 等等。

![NanoMQ](https://assets.emqx.com/images/892a0de52bd6288686aec1f0bbc330d9.png)

<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>

## 社区情况

[Mosquitto](https://github.com/eclipse/mosquitto) 是目前最流行的 MQTT Broker 之一，以其轻量级的设计而闻名，适合在嵌入式硬件上部署。

NanoMQ 作为一个 2020 年才启动的项目，虽然还处于早期阶段，但发展势头强劲。在过去的一年里，该项目已经完成了 1000 多次代码提交。

这两个开源项目都托管在 GitHub 上，其社区相关指标如下：

|                                     | **Mosquitto**                                            | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------------------- | :---------------------------------------------- |
| **GitHub Project**                  | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) | [NanoMQ GitHub](https://github.com/nanomq/nanomq) |
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

## 功能特性

Mosquitto 和 NanoMQ 均完整支持 MQTT 3.1/3.1.1/5.0 协议，包括遗嘱消息、保留消息、共享订阅等功能。

在传输方面，两者都支持 MQTT over TCP、TLS/SSL 和 WebSocket。NanoMQ 作为一个 2020 年设计的 Broker，还引入了 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic)，使其桥接功能具有多路复用以及快速建立和连接地址迁移的优势。

此外，NanoMQ 还提供了一系列管理和集成功能，如 HTTP API、WebHook、上线/下线事件钩子和规则引擎等。边缘计算领域用户可以基于 NanoMQ 产品组合获取很多实用功能，从而为边缘应用的开发节省更多时间。

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

## 扩展性和性能

NanoMQ 是一款专为边缘计算打造的现代 MQTT Broker，可以满足不断增长的性能、扩展性、空间参数、并发和延迟等方面需求。NanoMQ 内置先进的 Actor 线程模型，可以有效利用多核 CPU 的算力资源，在保证高吞吐量的同时能够实现低延时。这给了用户自由选择的空间：无论是性能、CPU 核心还是功能集，都可以随着需求变化而轻松调整和迁移。无论是用它来构建智能家居网关、工业机器人、无人机，还是复杂的智能车辆，NanoMQ 都能够胜任。

Mosquitto 针对的是传统嵌入式场景，这意味着它更加节省资源，消耗更少的内存和 CPU。因此，Mosquitto 更适用于物联网传感器和低处理能力设备，而 NanoMQ 则更适合高性能网关和服务器。此外，Mosquitto 的悠久的开源历史，保证其具有很高的稳定性，当用户对性能和功能的要求不高，并且项目有紧迫的时间表，需要快速完成时，它依然是最佳选择。

|                 | **Mosquitto**                                                | **NanoMQ**                                                   |
| :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Scalability** | 160k                                                         | 160k MQTT connections per node                               |
| **Performance** | Up to 120k QoS0 MQTT msgs/sec per node<br>80k QoS1 msgs/sec<br>40k QoS2 msgs/sec | Up to 1 million+ QoS0 MQTT msgs/sec per node<br>800k QoS1 msgs/sec<br>400k QoS2 msgs/sec |
| **Latency**     | Up to seconds latency in some scenarios                                           | Less than 10 milliseconds in most scenarios                                            |



## 易用性

Mosquitto 和 NanoMQ 的安装包都很小巧，安装起来很方便。但它们都缺少一些高级的管理和监控功能，比如 Dashboard。

Mosquitto 的配置文件采用键值格式，使得配置过程很直观。它还拥有完善的文档和活跃的用户社区。

相比之下，NanoMQ 对配置的要求更高，可能会让初学者花费一些时间。但对于有经验的用户来说，它提供了更多的控制和定制选项。

|                    | **Mosquitto**    | **NanoMQ**   | **Notes and Links**                                          |
| :----------------- | :--------------- | :----------- | :----------------------------------------------------------- |
| **Configuration**  | Key-Value Format | HOCON Format |                                                              |
| **HTTP API**       | ❌                | ✅            | [REST API](https://nanomq.io/docs/en/latest/http-api/v4.html) |
| **CLI**            | ✅                | ✅            | [Command Line Interface](https://nanomq.io/docs/en/latest/toolkit.html#client) |
| **Dashboard**      | ❌                | ❌            |                                                              |
| **Grafana**        | ❌                | ❌            |                                                              |
| **Prometheus**     | ❌                | ❌            |                                                              |
| **Docker**         | ✅                | ✅            | [NanoMQ Docker](https://hub.docker.com/r/emqx/nanomq)        |
| **Cross Platform** | ✅                | ✅            |                                                              |

## 桥接到 EMQX Cloud

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是基于开源分布式 MQTT Broker [EMQX ](https://www.emqx.io/zh)构建的高度可扩展的 MQTT 消息服务。我们可以轻松地将物联网边缘的 Mosquitto 或 NanoMQ 桥接至 EMQX Cloud 服务。

![将 Mosquitto 和 NanoMQ 桥接到 EMQX Cloud](https://assets.emqx.com/images/05b6602329f65d45aa2c87d115e2f51e.png)

## 未来展望

Mosquitto 2.0 版本新增了 epoll 支持，旨在解决 c10k 连接扩展问题。

NanoMQ 正在引领 [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) 技术，这是自 2017 年发布 MQTT 5.0 规范以来 MQTT 协议最具创新性的进展。MQTT over QUIC 通过多路复用、更快的连接建立和迁移等特性，有望成为下一代 MQTT 标准。通过实现基于 QUIC 的 QoS 优先级和流-主题配对等创新功能，NanoMQ 正在不断加速 QUIC 的普及。

## 结语

总的来说，Mosquitto 和 NanoMQ 都是优秀的轻量级 MQTT Broker，适用于物联网边缘的消息传递。用户可以根据自身需求，将它们部署在低功耗传感器、嵌入式硬件和工业物联网等多种场景中。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
