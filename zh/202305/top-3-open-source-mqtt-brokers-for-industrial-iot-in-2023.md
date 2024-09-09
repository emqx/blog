[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 最初作为一种轻量级的[发布/订阅消息传递协议](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)而设计，如今已经成为工业物联网（IIoT）和工业 4.0 发展的重要基础。它的意义在于实现了各类工业设备与云端的无缝连接，促进了运营技术（OT）和信息技术（IT）的融合。

本文对比分析了 2023 年[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)领域最优秀的三款 MQTT Broker，介绍了它们的优点、缺点和应用场景。同时，还展示了如何利用这三款 MQTT Broker，为您的工业物联网解决方案打造统一命名空间（UNS）架构。

## 项目概览

本文选取的开源 MQTT Broker 主要基于以下两个标准：

- 开源项目的社区规模、受欢迎程度和项目活跃度。
- 与资源受限的工业设备和网关的兼容性。

基于此，我们选出了三款最热门的开源 MQTT Broker：

- **EMQX：**GitHub 上 Star 数最多的 MQTT Broker，拥有 11.6k Stars。EMQX 在启动时的内存占用约为 50M，支持集群功能。
- **Mosquitto：**Star 数位居第二但是使用最为广泛的 MQTT Broker。它采用单线程架构，在启动时的内存占用不到 1M。
- **NanoMQ：**目前最新且最活跃的 MQTT Broker 之一。它支持多线程和异步 IO，在启动时的内存占用约为2M。

以下是这三个项目在 GitHub 上的相关概况：

|                                     | **EMQX**                                    | **Mosquitto**                                            | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------ | :------------------------------------------------------- | :---------------------------------------------- |
| **Official Website**                | [EMQX](https://www.emqx.com/zh)                | [Eclipse Mosquitto](https://mosquitto.org/)              | [NanoMQ](https://nanomq.io/)                    |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) | [NanoMQ GitHub](https://github.com/nanomq/nanomq) |
| **Project Created**                 | 2012                                        | 2009                                                     | 2020                                            |
| **License**                         | Apache License 2.0                          | EPL/EDL License                                          | MIT License                                     |
| **Programming Language**            | Erlang                                      | C/C++                                                    | C                                               |
| **Latest Release**                  | v5.0.23 (April 2023)                        | 2.0.15 (Aug 2022)                                        | v0.17.0 (March 2023)                            |
| **GitHub Stars**                    | **11.5k**                                   | **7.2k**                                                 | **800+**                                        |
| **GitHub Releases**                 | 260+                                        | 60+                                                      | 75+                                             |
| **GitHub Commits**                  | 14k+                                        | 2800+                                                    | 2000+                                           |
| **GitHub Commits (Last 12 Months)** | **3000+**                                   | **500+**                                                 | **1200+**                                       |
| **GitHub PRs**                      | 6000+                                       | 600                                                      | 780+                                            |
| **GitHub Contributors**             | 100+                                        | 110+                                                     | 20+                                             |

## 1. EMQX

[EMQX](https://github.com/emqx/emqx) 是一款高度可扩展的分布式 MQTT Broker，适用于企业级的工业物联网部署。它支持 MQTT 5.0、MQTT-SN、SSL/TLS、[MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 等多种协议。它通过 masterless 集群方式实现了高可用性和水平扩展性。

凭借在 GitHub 上的 11.5k 个 Star，EMQX 已经成为市场上[最受欢迎的 MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) 之一。EMQX 项目于 2012 年启动，采用 Apache 2.0 许可证进行开源。EMQX 由 Erlang/OTP 编写，这是一种能够构建高度可扩展的软实时系统的编程语言。

EMQX 既可以在云端部署，也可以在边缘部署。在边缘，它可以与各种工业网关集成，例如 [N3uron](https://n3uron.com/)、[Neuron](https://github.com/emqx/neuron)、[Kepware](https://www.ptc.com/en/products/kepware)。在云环境中，EMQX 能够在 AWS、GCP、Azure 等主流的公共云平台上与包括 Kafka、数据库和云服务在内的多种技术无缝集成。

借助全面的企业级功能、数据集成能力、云托管服务和 EMQ 团队提供的商业支持，EMQX 广泛应用于工业物联网领域的多种重要场景。

![EMQX MQTT Cluster](https://assets.emqx.com/images/5063b00be9fc0e46ee1431793dc33d24.png)

### 优点

- Masterless 集群和高可用性
- 具有高性能和低延迟
- 提供丰富的认证机制
- 即可以在边缘部署也可以在云端部署
- 首个支持 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 的 MQTT Broker

### 缺点

- 安装和配置相对复杂
- CPU 和内存使用率较高

### 应用场景

- 汽车制造
- 钢铁制造
- 石油和天然气
- 半导体制造
- 供水

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## 2. Mosquitto

[Mosquitto](https://mosquitto.org/) 是一个广泛使用的开源 MQTT Broker，隶属于 Eclipse 基金会，遵循 Eclipse 公共许可证（EPL/EDL 许可证）。截至 2023 年 3 月，它在 GitHub 上拥有超过 7k 个 Star。Mosquitto 支持 MQTT 5.0、3.1.1、3.1，并且提供了对 SSL/TLS 和 WebSocket 的支持。

Mosquitto 由 C/C++ 编写，采用单线程架构。其轻量级设计使得它非常适合在资源受限的嵌入式设备或工业网关上部署。Mosquitto 是跨平台的，可以在包括 Linux、Windows、macOS 在内的多种平台上运行。

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

### 优点

- 轻量级、占用资源少
- 简单易用

### 缺点

- 不支持多线程和集群
- 不支持在云端部署

### 应用场景

- 工厂自动化
- 智能制造
- 智能硬件

## 3. NanoMQ

[NanoMQ](https://nanomq.io/zh) 是一个最新的开源 MQTT Broker 项目，于 2020 年发布。它采用纯 C 语言编写，基于 NNG 的异步 I/O 多线程 [Actor 模型](https://en.wikipedia.org/wiki/Actor_model)，支持 MQTT 3.1.1、MQTT 5.0、SSL/TLS、MQTT over QUIC。

NanoMQ 的突出亮点是轻量级、快速、极低的内存占用，这使它成为一款在工业物联网中表现非常优秀的 MQTT Broker，因为在工业物联网中效率和资源优化非常重要。此外，NanoMQ 还可以用作消息总线，将 DDS、NNG、ZeroMQ 等协议转换为 MQTT，然后再将 MQTT 消息桥接到云端。

NanoMQ 具有高度的兼容性和可移植性，只依赖于原生的 POSIX API。这使得它可以轻松地部署在任何支持 POSIX 标准的平台上，并且能够在 x86_64、ARM、MIPS、RISC-V 等各种 CPU 架构上顺畅运行。

![NanoMQ](https://assets.emqx.com/images/44a45e8732eef0076a95f095f6551d2e.png)

### 优点

- 支持多线程和异步 IO
- 启动占用资源少
- 可以与无代理协议桥接

### 缺点

- 项目还处于早期阶段
- 不支持集群

### 应用场景

- 汽车制造
- 机器人：边缘服务融合
- 工业物联网边缘网关

<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>


## 横向对比

|                       | **EMQX**                      | **Mosquitto**  | **NanoMQ**                                     |
| :-------------------- | :---------------------------- | :------------- | :--------------------------------------------- |
| **Protocols**         | MQTT 5.0/3.1.1<br>MQTT over QUIC | MQTT 5.0/3.1.1 | MQTT 5.0/3.1.1<br>MQTT over QUIC<br>ZeroMQ & NanoMSG |
| **Scalability**       | Excellent                     | Moderate       | Good                                           |
| **Availability**      | Excellent                     | Moderate       | Moderate                                       |
| **Performance**       | Excellent                     | Good           | Excellent                                      |
| **Latency**           | Excellent                     | Good           | Excellent                                      |
| **Reliability**       | High                          | High           | High                                           |
| **Security**          | Excellent                     | Excellent      | Good                                           |
| **Integrations**      | Excellent                     | Moderate       | Moderate                                       |
| **Compatibility**     | Good                          | Excellent      | Excellent                                      |
| **Ease of Use**       | Good                          | Excellent      | Good                                           |
| **Community Support** | Excellent                     | Excellent      | Excellent                                      |

## UNS：优化工业物联网项目的 Broker 部署

统一命名空间（UNS）是一种针对工业物联网和工业 4.0 的解决方案架构，它基于 MQTT Broker，为 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)提供统一的命名空间，为消息和结构化数据提供集中的存储库。

本文提到的这三款 MQTT Broker 可以搭建 UNS 架构，形成一个协同的系统。其中，Mosquitto 和 NanoMQ 部署在工业网关上，EMQX 部署在云端作为集中式枢纽。这种配置使得工业物联网数据可以通过 MQTT 桥接器从边缘无缝地传输到云端，然后进行聚合和采集。

![MQTT Unified Namespace](https://assets.emqx.com/images/f7031dc2592e6a32a061b78378821086.png)

## 结语

通过前文的介绍和对比，我们可以看到，每个 MQTT Broker 都有其独特的优点，适合不同的部署场景。[EMQX](https://github.com/emqx/emqx) 具有高扩展性和企业级功能，适合在云端部署。[Mosquitto](https://mosquitto.org/) 和 [NanoMQ](https://nanomq.io/zh) 快速、轻便，适合在工业网关上部署。

这三款 MQTT Broker 在工业物联网应用中都扮演着非常重要的角色，它们推动了 UNS 架构的实施，促进了 IT 和 OT 的融合。在具体的工业物联网项目中，您可以根据自己的需求对这些 Broker 进行自由搭配。您可以建立一个高度协同的系统，让这些 MQTT Broker 共同合作，充分发挥它们各自的优势。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
