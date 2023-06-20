## 什么是 MQTT Broker？

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种适用于物联网的轻量级协议，MQTT Broker 是其核心组件。本文介绍了 MQTT Broker 的作用，对比分析了它的不同实现方式，并概述了它的应用场景、特点和最佳实践。

MQTT Broker 是个中介实体，它负责 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)之间的通信。具体来说，MQTT Broker 接收客户端发布的消息，并根据主题对消息进行筛选，然后将其分发给订阅者。

通过使用 MQTT Broker 实现发布/订阅通信模型，可以显著提高 MQTT 协议的效率和可扩展性。

## MQTT Broker 的重要性

MQTT Broker 是 MQTT 架构的核心，因为它负责协调 MQTT 客户端（发布者和订阅者）之间的通信。

以下是 MQTT Broker 的一些重要作用：

- **消息路由：**MQTT Broker 接收发布者发送的消息，并根据主题将其转发给相应的订阅者。这保证了消息能够有效和准确地传送，而无需客户端之间建立直接连接。
- **扩展性：**MQTT Broker 能够处理大量并发连接，这对于物联网和 M2M 通信场景非常重要，在这些场景中，可能有成千上万甚至数百万个设备连接。Broker 处理这些连接和消息的能力使 MQTT 协议能够高效地扩展。
- **安全性：**MQTT Broker 可以提供身份验证和加密等安全机制，以保证物联网设备和应用之间数据传输的安全性。要了解更多信息请阅读：[MQTT 安全指南：2023 年你需要了解的 7 个要点](https://www.emqx.com/zh/blog/essential-things-to-know-about-mqtt-security)。
- **集成性：**MQTT Broker 可以与其他通信协议和云平台集成，以构建完整的物联网解决方案。例如，MQTT Broker 可以与 AWS IoT、Google Cloud IoT 或 Microsoft Azure IoT Hub 集成，以实现一个无缝的物联网生态系统。
- **会话管理：**MQTT Broker 负责管理客户端会话，包括维护客户端订阅信息，以及处理保留消息以便在客户端上线时发送给客户端。会话管理功能可以确保在客户端断开连接并在稍后重新连接到 Broker 时不会丢失消息。要了解更多信息请阅读：[MQTT Persistent Session 与 Clean Session 详解](https://www.emqx.com/zh/blog/mqtt-session)。

## MQTT Broker 架构

MQTT Broker 架构基于[发布-订阅消息传输模式](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)，将消息生产者（发布者）与消息消费者（订阅者）解耦。该架构包括三个主要组件：客户端、主题和 Broker 。

- **MQTT Broker 服务器**

  MQTT Broker 是个服务器，它接收发布者发送的消息，并根据订阅者订阅的主题将消息转发给订阅者。它管理客户端连接、处理订阅和退订，并保证按照指定的[服务质量（QoS）级别](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)发送消息。

- **MQTT 客户端**

  MQTT 客户端可以是发布者，也可以是订阅者，或者两者都是。发布者向 MQTT Broker 发送消息，而订阅者从 Broker 接收消息。客户端可以是任何能够使用 MQTT 协议与 MQTT Broker 建立连接的设备或应用，如物联网设备、移动应用或其他服务器。

- **主题**

  主题是具有层次结构的字符串，描述了消息的类别。当发布者向 Broker 发送消息时，会指定一个主题。订阅者通过订阅一个或多个 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)来表明他们想要接收消息的类别。Broker 根据用户订阅的主题，将消息转发给相应的用户。

MQTT Broker 架构可以是集中式的，也可以是分布式的。在集中式架构中，单个 Broker 负责客户端之间的所有通信。在分布式架构中，多个 Broker 协同工作，以构建一个可扩展和容错的消息传输基础设施。分布式架构中的每个 Broker 都可以与其他 Broker 通信，管理消息转发，保证消息送达预期的接收者。

总之，MQTT Broker 架构提供了一个灵活高效的消息传输基础架构，使设备和应用能够安全、高效和大规模地进行通信。

## 热门开源 MQTT Broker

### EMQX

[EMQX](https://www.emqx.io/zh) 是目前物联网应用中最具扩展性的 MQTT Broker。它能够以亚毫秒级的延迟在一秒钟内处理百万级的 MQTT 消息，并支持在一个集群内连接高达 1 亿个客户端进行消息传输。EMQX 兼容 MQTT 5.0 和 3.x 版本。它是分布式物联网网络的理想选择，可以在 Microsoft Azure、Amazon Web Services 和 Google Cloud 等云上运行。EMQX 支持 MQTT over TLS/SSL，并支持多种认证机制，如 PSK、JWT 和 X.5093。与 Mosquitto 不同，EMQX 支持通过 CLI、HTTP API 和 Dashboard 进行集群管理。

### Mosquitto

[Eclipse Mosquitto](https://github.com/eclipse/mosquitto) 也是一款开源的 MQTT Broker，兼容 MQTT 协议的 5.0、3.1.1 和 3.1 版本。Mosquitto 体积小巧，既可以运行在低功耗的单板计算机上，也可以部署在企业级服务器上。它采用 C 语言编写，可以用 C 库实现 MQTT 客户端。它支持 Windows、Mac、Linux 和 Raspberry Pi 等多种平台，为每个平台提供了方便安装的二进制文件。最新版本还增加了一个认证和授权插件 “mosquitto-go-auth”，以及一个用于管理 Mosquitto 实例的 Web 用户界面。此外，它还提供了一个 PHP 包装器 “Mosquitto-PHP”，可以方便地在 PHP 中开发 MQTT 客户端。

### NanoMQ

[NanoMQ](https://nanomq.io/zh) 是一款为物联网边缘设计的轻量级 MQTT Broker。NanoMQ 以纯 C 语言实现，基于 NNG 的异步 I/O 和多线程 [Aactor 模型](https://en.wikipedia.org/wiki/Actor_model)，支持 MQTT 3.1.1 和 MQTT 5.0。NanoMQ 在独立 Broker 的环境中具有较高的性能。它的优势在于它的可移植性，它可以部署在任何 POSIX 兼容的平台上，并可在 x86_64、ARM、MIPS 和 RISC-V 等多种 CPU 架构上运行。

### VerneMQ

[VerneMQ](https://github.com/vernemq/vernemq) 项目于 [2014](https://github.com/vernemq/vernemq/tree/3c7703f0d62e758ba22a34ceb756f2ac2a4da44a) 启动，最初由 [Erlio GmbH](https://vernemq.com/company.html) 开发。它是第二个用 Erlang/OTP 开发的 MQTT Broker，该项目遵循 Apache 2.0 开源协议，并借鉴了 EMQX 项目的[部分代码](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl)。在架构设计方面，VerneMQ 支持将 MQTT 消息持久化到 LevelDB 中，并使用基于 [Plumtree](https://github.com/lasp-lang/plumtree) 库的集群架构，该库实现了 [Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf) 算法。

## MQTT Broker 选择指南以及一些有用的评估资源

接下来，本文将指导您如何根据需求，评估和选择最合适的 MQTT Broker。

### 评估标准

- [**2023 年选择 MQTT Broker 时要考虑的 7 个因素**](https://www.emqx.com/zh/blog/7-factors-to-consider-when-choosing-mqtt-broker-2023)

  正在寻找 2023 年最适合您的 MQTT Broker？在做出决策之前，请考虑这七个基本要素。请阅读我们的指南以获取更多信息。

### MQTT Broker 对比

- [**2023 年开源 MQTT Broker 综合比较**](https://www.emqx.com/zh/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)

  这篇文章对 2023 年最受欢迎的开源 MQTT Broker 进行了详细比较，以便您根据自己的需求做出明智的选择。

- [**2023 年最适用于工业物联网领域的三款开源 MQTT Broker**](https://www.emqx.com/zh/blog/top-3-open-source-mqtt-brokers-for-industrial-iot-in-2023)

  这篇文章对 2023 年工业物联网领域最优秀的 3 款 MQTT Broker 进行了对比分析，介绍了它们各自的优缺点和适用场景。

- [**EMQX vs Mosquitto | 2023 年 MQTT Broker 对比**](https://www.emqx.com/zh/blog/emqx-vs-mosquitto-2023-mqtt-broker-comparison)

  要了解 EMQX 和 Mosquitto 这两款 2023 年备受关注的开源 MQTT Broker 的异同，请阅读我们的详细对比。

- [**EMQX vs NanoMQ | 2023 年 MQTT Broker 对比**](https://www.emqx.com/zh/blog/emqx-vs-nanomq-2023-mqtt-broker-comparison)

  根据您的物联网项目需求，从 EMQX 和 NanoMQ 这两款 MQTT Broker 中选择最合适的一款。请阅读我们的指南，了解它们在扩展性、安全性和可靠性方面的差异。

- [**EMQX vs VerneMQ | 2023 年 MQTT Broker 对比**](https://www.emqx.com/zh/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison)

  请阅读我们对 EMQX 和 VerneMQ 这两款 MQTT Broker 的详细分析，以便您根据自己的物联网项目需求做出正确的选择。

- [**Mosquitto vs NanoMQ | 2023 年 MQTT Broker 对比**](https://www.emqx.com/zh/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison)

  这篇文章对 Mosquitto 和 NanoMQ 这两款 MQTT Broker 进行了对比分析，并为读者提供了 2023 年它们各自适用的应用场景。

- [**热门在线公共 MQTT Broker 评估**](https://www.emqx.com/zh/blog/popular-online-public-mqtt-brokers)

  这篇文章为您整理了一些免费的在线 MQTT Broker，并对它们的特点和优劣进行了分析，希望能帮助您做出正确的选择。

### MQTT Broker 基准测试

- [**MQTT 开放基准测试规范：全面评估你的 MQTT Broker 性能**](https://www.emqx.com/zh/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing)

  这篇文章介绍了 Open MQTT Benchmark Suite 的原理和功能，以及如何利用它对 MQTT Broker 的扩展性和性能进行客观公正的评估。

- [**MQTT 开放基准测试对比: 2023 年的 MQTT Broker**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mqtt-brokers-in-2023)

  这篇文章为您提供了 2023 年物联网领域最流行的 MQTT Broker 的对比分析，帮助您找到最适合您的 MQTT Broker。立即获取详尽的基准报告，了解各个 MQTT Broker 的优势和劣势。

- [**MQTT 开放基准测试对比: Mosquitto vs NanoMQ**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mosquitto-vs-nanomq)

  这篇文章利用 MQTT 开放基准测试工具，对 Mosquitto 和 NanoMQ 这两款 MQTT Broker 的性能进行了全方位的分析和对比。通过这篇文章，您可以了解两款 MQTT Broker 的特点和差异，从而选择最符合您需求的 Broker。

- [**MQTT 开放基准测试对比: EMQX vs NanoMQ**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-nanomq)

  这篇文章使用 Open MQTT Benchmark Suite 工具，对 EMQX 和 NanoMQ 这两款 MQTT Broker 的性能进行了全面的基准测试和评估，为您选择合适的 MQTT Broker 提供参考和指导。

- [**MQTT 开放基准测试对比: EMQX vs Mosquitto**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-mosquitto)

  这篇文章采用 MQTT 开放基准测试工具，对 EMQX 和 Mosquitto 这两款 MQTT Broker 的性能进行了综合分析和比较，从而帮助您选择最适合您需求的 MQTT Broker。

- [**MQTT 开放基准测试对比: EMQX vs VerneMQ**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-vernemq)

  这篇文章采用 MQTT 开放基准测试工具，对 EMQX 和 VerneMQ 这两款 MQTT Broker 的性能进行了综合分析和比较，从而帮助您选择最适合您需求的 MQTT Broker。

- [**高度可扩展，EMQX 5.0 达成 1 亿 MQTT 连接**](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

  为了评估 EMQX 的扩展性，我们在一个由 23 个 EMQX 节点组成的集群上，建立了 1 亿个 MQTT 连接，并观察了 EMQX 的性能表现。

## 帮助您入门 MQTT Broker 的有用资源

### 快速上手

- [**EMQX Cloud 入门：启动 MQTT 服务的最简单方法**](https://docs.emqx.com/zh/cloud/latest/quick_start/introduction.html)

  该页面为您提供了使用完全托管的 MQTT 服务 - EMQX Cloud 的指南，并提供了创建账户和体验其功能和特点的步骤说明。

- [**如何在 Ubuntu 上安装 MQTT Broker**](https://www.emqx.com/zh/blog/how-to-install-emqx-mqtt-broker-on-ubuntu)

  这篇文章以 EMQX 为例，教您如何在 Ubuntu 系统上搭建一个单节点 MQTT Broker。

- [**为 EMQX MQTT Broker 启用 SSL/TLS**](https://www.emqx.com/zh/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)

  EMQX 提供了多种安全认证方式，这篇文章将教您如何在 EMQX 中为 MQTT 配置 SSL/TLS。

### MQTT Broker 集成

- [**EMQX+Prometheus+Grafana：MQTT 数据可视化监控实践**](https://www.emqx.com/zh/blog/emqx-prometheus-grafana)

  这篇文章教您如何将 EMQX 5.0 的监控数据集成到 Prometheus 平台，并使用 Grafana 工具来展示 EMQX 的监控数据，从而搭建一个简单而实用的 MQTT Broker 监控系统。

- [**EMQX + ClickHouse 实现物联网数据接入与分析**](https://www.emqx.com/zh/blog/emqx-and-clickhouse-for-iot-data-access-and-analysis)

  物联网数据采集涉及大量的设备和数据，需要高效的访问、存储、分析和处理能力。EMQX + ClickHouse 的组合完美地满足了这一需求。

- [**如何使用 ThingsBoard 接入 MQTT 数据**](https://www.emqx.com/zh/blog/how-to-use-thingsboard-to-access-mqtt-data)

  这篇文章以 ThingsBoard Cloud 和 EMQX Cloud 为例，介绍如何将第三方 MQTT Broker 集成到 ThingsBoard 平台，从而实现对 MQTT 数据的访问和管理。

- [**使用 Node-RED 处理 MQTT 数据**](https://www.emqx.com/zh/blog/using-node-red-to-process-mqtt-data)

  这篇文章教您如何使用 Node-RED 工具访问 MQTT Broker，并对 MQTT 数据进行预处理后再发送到 Broker。

## EMQX：全球最具扩展性的 MQTT Broker

[EMQX](https://www.emqx.io/zh) 是全球最受欢迎的 MQTT Broker 之一，在 [GitHub](https://github.com/emqx/emqx) 上拥有 11.5k Stars。EMQX 项目于 2012 年启动，采用 Apache 2.0 协议开源。EMQX 是用 Erlang/OTP 编写的，这是一种专为构建大规模可扩展软实时系统而设计的编程语言。

EMQX 是全球最具扩展性的 MQTT Broker，支持 MQTT 5.0、MQTT-SN 和 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 等先进的功能。它支持无主集群架构，保证了高可用性和水平扩展性。EMQX 5.0 是最新的版本，能够在由 23 个节点组成的单一集群上，支持高达 1 亿的 MQTT 并发连接。

EMQX 不仅提供了丰富的企业功能、数据集成、云主机服务，还有来自 [EMQ](https://www.emqx.com/en) 的商业支持。EMQX 以其卓越的性能、可靠性和可扩展性，赢得了企业、初创公司和个人开发者的广泛认可。EMQX 被应用于各个行业的关键业务场景，如物联网、[工业物联网](https://www.emqx.com/zh/use-cases/industrial-iot)、[网联汽车](https://www.emqx.com/zh/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know)、[制造业](https://www.emqx.com/zh/solutions/industries/manufacturing)和电信。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
