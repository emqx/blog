近日，企业级 MQTT 物联网接入平台 [EMQX Enterprise 5.1](https://www.emqx.com/zh/products/emqx) 正式发布。该版本为用户提供了更强大、更灵活的物联网解决方案，通过简化功能操作与管理流程，帮助用户快速构建所需的业务。

新版本提供了更大规模且更具伸缩性的全新集群架构，单集群可达 1 亿客户端连接；创新性地引入 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 协议；同时提供了 MQTT 大文件传输能力以及可视化数据集成能力。企业用户将可以利用 EMQX Enterprise 5.1 构建更加安全可靠的、可随业务需求动态伸缩的大规模物联网应用。

<section class="promotion">
    <div>
        现在试用 Enterprise 5.1
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

## 全新架构，集群规模、扩展性和可靠性大幅提升

基于开创性的自研 Mria 集群架构，EMQX 5.0 进入了亿级物联网连接的时代。最新的 EMQX Enterprise 5.1 版本则对集群的稳定性与可靠性进行了进一步的巩固。单个 EMQX Enterprise 5.1 集群支持至多 23 个节点并能够承载超过 1 亿 MQTT 连接——相比当前版本实现了 10 倍的接入能力提升。

除此之外，新架构还为 EMQX 带来了更强的水平扩展能力和更高的可靠性。得益于新架构的核心-复制（Core-Replicant）节点模式，企业用户可以在不中断业务的情况下灵活伸缩增减节点数量，以支撑不断增长的业务规模或降低运行成本。与此同时，大规模部署下节点脑裂风险以及脑裂后对业务产生的影响也被显著降低，这能够为企业用户提供更加稳定可靠的物联网数据接入服务。

![Mira 集群架构图](https://assets.emqx.com/images/206cf3dca10ecb1e8690612f13ec052c.png)

<center>Mira 集群架构图</center>

<br>

[EMQX Cloud](https://www.emqx.com/zh/cloud) 在今年全新推出的 Severless 版本中已经率先使用了该集群架构为客户提供服务，稳定支撑全球 3000+ 用户使用。为了在 EMQX Enterprise 5.1 版本中更好地实现 EMQX 集群的自动化部署与弹性伸缩能力，自动化管理工具 [EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 也针对新架构进行了适配，企业用户可以充分体验 EMQX Enterprise 5.1 在性能、扩展能力、可靠性上的巨大提升带来的收益。

关于全新架构的更多内容可查看：

- [EMQX 企业版文档 - 部署架构与集群要求](https://docs.emqx.com/zh/enterprise/v5.0/deploy/cluster/mria-introduction.html)

- [Mria + RLOG 新架构下的 EMQX 5.1 如何实现 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)

- [EMQX+阿里云飞天洛神云网络 NLB：MQTT 消息亿级并发、千万级吞吐性能达成](https://www.emqx.com/zh/blog/achieve-mqtt-message-concurrent-performance-of-100-million-and-throughput-of-millions)

## MQTT over QUIC，下一代物联网标准协议优化消息传输场景

随着物联网设备在移动网络与不稳定网络中进行数据传输的场景不断丰富，如何提高设备连接稳定性、降低设备重连开销、降低延迟并提高吞吐量是物联网设备接入技术亟待解决的问题之一。

[QUIC](https://www.emqx.com/zh/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) 是下一代互联网协议 HTTP/3 的底层传输协议，与 TCP/TLS 协议相比，它在减少连接开销与消息延迟的同时，为现代移动互联网提供了有效灵活的传输层。

EMQX Enterprise 是首个将 QUIC 与 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)结合的开创性产品。在长期的客户服务和技术探索中，我们注意到 QUIC 的特性能够完美解决弱网与不固定的网络通路这类特定物联网环境中的挑战性问题，于是尝试将 QUIC 融入 MQTT 的传输层并设计了独特的消息传输机制和管理方式，由此诞生了 MQTT over QUIC。

![MQTT over QUIC Protocol Layers](https://assets.emqx.com/images/60fc64f70bd64b983ca438a33beede2d.png)

在多项与 TCP/TLS 的[测试对比](https://www.emqx.com/zh/blog/mqtt-over-quic#:~:text=的流量控制。-,QUIC vs TCP/TLS 测试对比,-我们在实验)中，基于 EMQX Enterprise 5.1 版本提供的 MQTT over QUIC 都展现出更出色的性能表现。对于时刻处于移动中的物联网场景，如车联网或是需要频繁断连不适合做长连接的场景（如设备需要定期休眠）来说，QUIC 都能够满足其高质量、稳定的消息通信需求，弥补了现有 TCP/TLS 传输层的不足。

目前 MQTT over QUIC 已经具备投入生产能力，在 EMQX Enterprise 用户中进行了深度测试集成并获得了良好反馈。EMQ 也正在以 OASIS 成员身份推动 MQTT over QUIC 的标准化落地，车联网、移动数据采集等场景的 EMQX 客户将从中受益。

有关 MQTT over QUIC 的入门使用请查看：[从零开始上手 MQTT over QUIC：快速体验下一代物联网标准协议](https://www.emqx.com/zh/blog/getting-started-with-mqtt-over-quic-from-scratch)。

## 基于 MQTT 的文件传输，统一数据通道简化系统架构

在物联网应用中，除了一些实时的物联网数据（如结构化的传感器数据与控制指令）传输外，还存在离线类型的大批量数据（如音视频、图片）传输需求。

一个基于现有 MQTT 连接的统一物联网数据传输通道可以避免使用不同的协议和技术来处理文件类型业务数据传输。因此 EMQX Enterprise 5.1 基于标准的 MQTT 协议实现了一个专用于文件传输的扩展功能。该功能无需改造现有的客户端与应用即可进行集成。相比于 HTTP/FTP 协议，MQTT 具有低带宽消耗和资源占用少的特点，能够快速且高效的进行文件传输。统一的物联网数据通道也简化了系统架构，减少应用的复杂性和维护成本。

**关键特性：**

- 支持与其他业务使用同一个 MQTT 连接，充分复用现有的客户端管理体系；
- 支持分块传输，这意味着轻量级的客户端也能够处理大型文件，同时超过 MQTT 协议限制大小（256MB）的文件也能够被传输；
- 支持断点续传，客户端设备可以随时暂停文件传输以进行更高优先级的数据传输，或从网络中断中恢复传输；
- 可靠性保障，通过 QoS 与精心设计的校验、重传机制确保文件传输完整性；
- 灵活的存储层配置，上传的文件能够保存到本地指定目录或与 S3 兼容的对象存储中，方便后续使用。

**应用场景：**

- 车联网：批量打包车内信号数据文件上传

  将车辆产生的大量信号数据，包括车速、位置、油耗、驾驶行为监控数据等在本地缓存后批量上传至云平台或数据中心。

- 工业互联网：非结构化生产数据统一上报

  将工业互联网环境中生产设备和传感器产生的多样化非结构化数据（如文本、图像、视频等）可靠地上传至服务器或云平台，以便进行数据分析、监控和工业生产过程的优化。

- 智慧城市：视频监控图片等文件传输

  在智慧城市中，利用 MQTT 文件传输功能可将监控摄像头和人脸识别设备产生的大量图片数据传输到指定的 MQTT 主题，以便于存储、分析和处理，并与上层服务进行无缝对接。

## 可视化双向数据集成能力加速业务创新

EMQX 通过规则引擎与数据桥接功能，以灵活、低代码的配置方式，为用户提供数据集成能力，进行物联网数据的实时处理和与第三方数据系统的集成，包括 Kafka、AWS RDS、MongoDB、Oracle 以及 TimescaleDB、InfluxDB 等各类时序数据库。

在 EMQX Enterprise 5.1 中，我们进一步完善了数据集成能力，以帮助企业用户更加轻松灵活地实现各类应用集成与业务创新。

### 可视化编排规则处理数据流

在之前的版本中，EMQX 的数据集成是通过配置 SQL + 规则动作的方式实现的，用户需要熟悉 SQL 语法才能编写规则，规则较多的情况下很难维护和管理无数据处理与集成流程，这在一定程度上提高了用户开发与配置的门槛。

EMQX Enterprise 5.1 通过可视化查看 Flows 页面改善了以上问题，用户可以清晰看到每个主题的数据处理规则与对接的第三方数据系统，并实时监控这一链路中每个步骤的状态。

![Data Flow View](https://assets.emqx.com/images/62ec79a60cbb850b41e2d8c1aa4a12fd.png)

### 更灵活的双向数据集成

EMQX Enterprise 5.1 提供了双向数据桥接能力——除了将设备数据桥接至外部系统外，还能从外部数据系统如另一个 MQTT 服务、Kafka 中桥接数据至 EMQX，并经过规则处理后发送到指定设备。

双向数据集成适用于云端下发场景，在支撑持续大规模消息下发的同时，能够使用统一的语言实现物联网数据实时处理，为物联网业务开发提供了更多的可能性。

![Data Bridge and Rule Engine](https://assets.emqx.com/images/e410f207f9765a9323bc02ba0f6a70c4.png)

此外，我们还为 EMQX Enterprise 5.1 数据集成增加了缓冲功能，以实现海量消息集成时的削峰与过载保护，有效提升数据集成的可靠性并保障业务的可用性。

## 安全至上，全面的安全保障

近年来，全球关键信息基础设施网络安全事件层出不穷。物联网涉及出行、电力、石油、工业制造等关键行业，对数据安全有更高的要求，需要底层的基础设施服务具有极高的稳定性与可靠性。

EMQX 针对物联网安全拥有完整的解决方案。

在传输层上，除了使用 SSL/TLS 实现通信安全与 X.509 设备认证外，EMQX Enterprise 5.1 还包含了 CRL 与 OCSP Stapling 认证机制，进一步增强认证的安全性和灵活性。

在应用层认证上，EMQX Enterprise 5.1 内置实现了客户端认证授权、黑名单以及连接抖动防护功能，确保系统只与合法的客户端进行通信，并有效防范潜在的安全风险和异常连接行为。

以上安全选项都可以通过 Dashboard 一键配置开启，无需编写代码即可实现各个层级的防护，以更高的开发效率获得更安全的保障。

除此之外，EMQX Enterprise 5.1 不停机热更新以及补丁能力则可以做到平滑、不暂停业务的实时故障修复，这一机制允许企业用户在保证业务可用性的同时不断加固安全防护能力，为用户打造可靠、可信、安全且健壮的物联网系统奠定了良好的基础。

## 全新 Dashboard，轻松管理和监控你的 Broker

自早期版本开始，EMQX Dashboard 就一直是管理和监控 EMQX 的关键组件。EMQX Enterprise 5.1 中，我们对 Dashboard 进行了全新的 UI/UX 设计，针对不同用户角色重新优化了菜单结构，并为每个功能设计了最佳的操作路径，以提供更出色的使用体验。

在提升视觉体验的同时，全新 Dashboard 将集群状态的实时可观测性、功能配置与使用和问题分析诊断有机地结合在一起，为用户使用 EMQX 进行物联网开发提供了便利，帮助其快速构建所需的物联网解决方案。

![Real-Time MQTT Cluster Overview](https://assets.emqx.com/images/cc6419f3a395a5910529b729d87a6234.png)

## 结语

随着物联网亿级连接时代的到来，具有极强可扩展性的 EMQX Enterprise 5.1 无疑将为企业业务规模的扩张提供有力支撑。而在数据集成能力、产品易用性与安全性等方面的进一步提升，则使得 EMQX Enterprise 5.1 成为企业构建数字化底座、开展物联网业务必备的可靠基础设施。我们希望在未来，EMQX 将连接更多的物联网关键设备，见证更多企业的业务发展与创新。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
