**目录**

- [MQTT over QUIC](#mqtt-over-quic)

- [MQTT Serverless](#mqtt-serverless)

- [MQTT 多租户架构](#mqtt-多租户架构)

- [MQTT Sparkplug 3.0](#mqtt-sparkplug-3-0)

- [MQTT 统一命名空间](#mqtt-统一命名空间)

- [MQTT 跨域集群](#mqtt-跨域集群)

- [MQTT Streams](#mqtt-streams)

- [结语](#结语)

  
MQTT 是物联网消息传输标准协议，其采用极其轻量级的发布订阅消息模型，以可扩展、可靠且高效的方式连接物联网设备。

自 1999 年 IBM 发布 MQTT 以来已经过去了二十多年，而自 2012 年 EMQ 在 GitHub 上发布[开源 MQTT 消息服务器 EMQX](https://github.com/emqx/emqx)，也已经过去了十年。如今，我们来到了各类新兴技术飞速进步的 2023 年，随着 MQTT 在物联网中的使用规模不断增长，场景更加多样化，我们可以预见在 MQTT 技术领域中将会出现以下 7 个发展趋势。

## MQTT over QUIC

QUIC（Quick UDP Internet Connections）是由 Google 开发的一种新的传输协议，运行于 UDP 之上，旨在减少建立新连接所带来的延迟，提高数据传输速率，并解决 TCP 的一些限制。

下一代互联网协议 HTTP/3 使用了 QUIC 作为底层传输协议，为网络应用带来了比 HTTP/2 更低的时延和更好的加载体验。

[MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 是自 2017 年 MQTT 5.0 规范发布以来 MQTT 协议中最具创新性的进展。凭借多路复用、更快的连接建立和迁移等优势特性，其具有成为下一代 MQTT 协议标准的潜力。

MQTT 5.0 定义了三种传输类型：TCP、TLS 和 WebSocket。在物联网安全最佳实践中，MQTT over TLS/SSL 广泛用于生产环境以保护客户端和 Broker 之间的通信。然而它速度慢、延迟高，需要 7 个 RTT，即 TCP 3 次握手以及 TLS 4 次握手才能建立新的 MQTT 连接。

与 MQTT over TLS/SSL 相比，MQTT over QUIC 更快且延迟更低，在初次建立连接时仅需 1 RTT，并可以利用 0 RTT 连接恢复的特性来加速重连。QUIC 协议栈可以针对各种用例进行定制，例如在不稳定网络环境下，或是客户端到服务器更低延迟通信的场景。它能够在诸如移动网络下的车联网（IoV）以及要求极低时延的工业物联网（IIoT）场景下发挥重要作用，并有效提升其使用体验。

开源 MQTT 消息服务器 EMQX 在其最新的 [5.0 版本](https://www.emqx.com/zh/blog/tag/emqx-5.0-%E4%BA%A7%E5%93%81%E8%A7%A3%E8%AF%BB)中引入了 [MQTT over QUIC 支持](https://www.emqx.com/zh/blog/mqtt-over-quic)，是全球首个支持 MQTT over QUIC 的 MQTT 消息服务器。目前 EMQ 正以 OASIS MQTT 技术委员会成员身份积极推进 MQTT over QUIC 的标准化落地，可以预见在不久的将来，MQTT 也将和 HTTP/3 一样使用 QUIC 作为其主要传输层。

![MQTT over QUIC](https://assets.emqx.com/images/a172e1693e8b7c86ec51e5d69936a802.png)

## MQTT Serverless

云计算中 Serverless 模式的兴起标志着应用的设计、开发、部署和运行方式发生了突破性的范式转变。这种模式下开发者将能够专注于应用的业务逻辑，无需管理基础设施，从而提高敏捷性、可扩展性和成本效益。

Serverless 模式的 MQTT 消息服务器将是 2023 年的一种前沿架构创新。传统的物联网应用需要数分钟甚至数小时才能在云上或在企业私有环境中部署 MQTT 消息服务，相比之下，Serverless MQTT 只需点击几下就能快速完成 MQTT 服务的部署。

除了极快的部署速度，Serverless MQTT 更大的价值在于其无可比拟的灵活性：根据用户需求对资源进行无缝扩展，以及与这种弹性架构相匹配的按量计费定价模式。Serverless MQTT 有望推动 MQTT 更广泛的应用，降低运营成本，激发不同行业的创新协作。我们甚至可能看到每个物联网和工业物联网开发者都能拥有一个免费的 Serverless MQTT 消息服务器。

2023 年 3 月，EMQX Cloud 推出了全球首个 [Serverless MQTT 服务](https://www.emqx.com/zh/blog/emqx-cloud-serverless-launched)，为用户提供了 5 秒极速部署和更灵活的计费方式，帮助用户以更低的成本高效开发物联网应用。

<section class="promotion">
    <div>
        试用 EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">每月 100 万免费的连接分钟数，无需绑定信用卡。</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

## MQTT 多租户架构

多租户架构是实现 Serverless MQTT 服务的一个重要基础。来自不同用户或租户的物联网设备可以连接到同一个大规模的 MQTT 集群，同时保持其数据和业务逻辑与其他租户隔离。

在 SaaS 应用中多租户架构很常见，即一个应用为多个客户或租户服务。其通常有两种以下不同的实现方式：

- 租户隔离： 向每个租户提供一个单独的应用实例，在服务器或虚拟机上运行。
- 数据库隔离： 多个租户共享一个应用实例，但每个租户有自己的数据库模式，以确保数据隔离。

在 MQTT Broker 的多租户架构中，每个设备和租户都有一个单独的、隔离的命名空间，包括一个独特的主题前缀和访问控制列表（ACL），用来定义用户可以发布或订阅哪些主题。

多租户 MQTT 消息服务器能够减少管理开销，并灵活支持复杂场景或大规模物联网应用场景。例如，一个大型组织中的部门和应用可以作为不同的租户使用同一个 MQTT 集群。

## MQTT Sparkplug 3.0

MQTT Sparkplug 是由 Eclipse 基金会设计的开放标准规范，其最新版本为 MQTT Sparkplug 3.0，它定义了工业设备的统一数据接入规范，能够通过 MQTT 协议连接各类工业传感器、动作执行器、可编程逻辑控制器（PLC）和网关。

MQTT Sparkplug 3.0 于 2022 年 11 月发布，具有以下关键的新功能和改进：

- MQTT 5.0 支持： 增加了对 MQTT 5.0 的支持，包括共享订阅、消息过期和流量控制等新功能。
- 优化的数据传输：对数据传输进行了优化，使用更紧凑的数据编码和压缩算法。
- 扩展的数据模型： 引入了一个扩展的数据模型，它允许更详细的设备信息通信，还支持配置数据和设备元数据等其他信息的传输。
- 更高的安全性： 包括对安全性的若干改进，如支持双向 TLS 认证、优化的访问控制机制等。
- 简化的设备管理： 包括自动设备注册和发现，简化设备配置，以及改进诊断等。

MQTT Sparkplug 旨在简化不同工业设备间的连接和通信，实现高效的工业数据采集、处理和分析。随着新版本的发布，MQTT Sparkplug 3.0 将会在工业物联网领域得到更广泛的应用。

## MQTT 统一命名空间

统一命名空间（Unified Namespace）是一个建立在面向工业物联网和工业 4.0 的 [MQTT Broker](https://www.emqx.io/zh) 上的解决方案架构。它为 MQTT 主题提供了一个统一的命名空间，并为消息和结构化数据提供了一个集中的存储库。

统一命名空间使用中央 MQTT Broker ，以星形拓扑结构连接工业设备、传感器和应用程序，如 SCADA、MES 和 ERP。统一命名空间以事件驱动的架构极大简化了工业物联网应用的开发。

在传统的工业物联网系统中，OT 和 IT 系统通常是分开的，其数据、协议和工具均独立运行。通过采用统一命名空间，可以让 OT 和 IT 系统更有效地交换数据，最终实现物联网时代 OT 和 IT 的统一。

![MQTT 统一命名空间](https://assets.emqx.com/images/4bd773c5f0197e690c0c819f75940d95.png)

如今，通过 EMQ 提供的[开源 MQTT 消息服务器 EMQX](https://www.emqx.io/zh) 或 [NanoMQ](https://nanomq.io/zh)，结合[工业协议网关软件 Neuron](https://neugates.io/zh)，用户将可以构建一个由 IT 界最先进技术支持的统一命名空间架构。

## MQTT 跨域集群

MQTT 跨域集群（MQTT Geo-Distribution）是一个创新架构，允许部署在不同地区或云上的 MQTT Broker 作为一个单集群一起工作。通过跨域集群，MQTT 消息可以在不同地区的 MQTT Broker 之间自动同步和传输。

有两种方法可以实现 MQTT 跨域集群：

- 单集群，多地区： 单个 MQTT 集群，每个节点在不同地区运行。
- 多集群，多云： 分布在不同云中的多个 MQTT 集群连接在一起。

我们可以将这两种方法结合，在跨区域部署的 MQTT Broker 之间创建一个可靠的物联网数据基础设施。通过 MQTT 跨域集群，企业可以建立一个跨多云的全球 MQTT 接入网络。不管所处的物理位置在哪里，设备和应用都能从最近的节点接入实现相互通信。

![MQTT 跨域集群](https://assets.emqx.com/images/8d37c93155161dc872b657673d028372.png)

## MQTT Streams

MQTT Streams 是 MQTT 协议备受期待的一项扩展能力，能够在 MQTT Broker 内实时处理海量、高频的数据流。这在发布订阅模式消息传输的基础上进一步增强了传统 MQTT Broker 的能力。通过 MQTT Streams，客户端可以像 Apache Kafka 一样将 MQTT 消息以流的形式进行生产和消费，从而实现历史消息回放。这对事件驱动的处理尤为重要，可以确保最终的数据一致性、可审计和合规性。

流处理对于从物联网设备产生的大量数据中实时挖掘商业价值至关重要。以前，这一过程通过一个过时且复杂的大数据堆栈实现，需要 MQTT Broker 与 Kafka、Hadoop、Flink 或 Spark 进行集成。

而通过内置的流处理，MQTT Streams 简化了物联网数据处理架构，提高了数据处理效率和响应时间，并为物联网提供了一个统一的消息传递和流处理平台。通过消息去重、消息重放和消息过期等功能，MQTT Streams 实现了高吞吐量、低时延和容错，使其成为基于 MQTT 的物联网应用中实时数据流处理的强大工具。

## 结语

总的来说，MQTT 的这 7 个技术趋势反映了新兴技术的进步以及它们在推动物联网发展进程中的重要作用。作为一个发展了二十多年的标准消息传输协议，MQTT 的重要性正在持续增长。随着物联网在各行业被越来越广泛地应用，MQTT 协议也在不断发展以应对新的挑战，满足更低延迟的连接、更便捷的 MQTT 服务部署、复杂场景或大规模物联网应用下灵活管理以及工业设备接入的需求。作为庞大物联网的神经系统，在 2023 年及更远的未来，MQTT 必将在工业物联网和车联网等关键领域中发挥重要作用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
