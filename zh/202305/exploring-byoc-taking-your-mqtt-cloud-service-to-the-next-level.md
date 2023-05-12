## 引言

您是否希望将物联网基础设施提升到更高的水平？为了应对业务的不断扩展，您需要一个强大且安全的消息平台来支持它。

MQTT 协议凭借其轻量级、[发布/订阅模型](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)和可靠性，已经成为构建物联网平台的首选方案。但是，随着业务的增长，物联网解决方案提供商可能面临基础设施维护费用上升和数据隐私要求提高的挑战。

开源 MQTT 消息平台的领导者 EMQ 近日推出了 [EMQX Cloud BYOC](https://www.emqx.com/zh/cloud/byoc)，允许用户在自选的云环境中部署 MQTT 集群，从而完全掌控数据隐私和安全。

本文将对 BYOC 模式和 EMQX Cloud BYOC 的架构进行详细介绍，帮助您全面了解它如何助力您的业务。

## 什么是 BYOC

BYOC（Bring Your Own Cloud）是一种让您可以在自选的公有云环境（如阿里云、华为云、亚马逊云等）部署 MQTT 集群并交由专业团队托管的服务模式。它让您可以完全掌控云基础设施，并能够满足严格的数据合规要求。

## 服务模式：只需为您使用的服务付费

EMQX Cloud BYOC 采用云原生架构，注重扩展性、可用性和安全性，提供 99.99% 服务等级协议（SLA）的高可用 MQTT 服务。

基于订阅的许可证模式使您能够根据需要灵活扩展 MQTT 基础设施。得益于对云平台上资源管理的便利性和 BYOC 托管服务，您无需提前投入人力和物力，只需为使用的服务付费。

订阅的服务中还涵盖基于 Prometheus、Grafana、Open Telemetry 等云原生工具的 7x24 小时技术支持和维护服务，让您的 MQTT 基础设施始终保持稳定，获得及时更新。

## 架构：保证高级别的数据隐私

EMQX Cloud BYOC 架构由 EMQX Cloud 云环境和客户的云环境两部分组成，它们的构建方式如下图所示。

![EMQX Cloud BYOC](https://assets.emqx.com/images/67ec52b7f37ffc06b5ebe356cbccd64e.png)

在客户自己的云环境中，有一个 EMQX 集群和一个 BYOC Agent 节点，它们位于一个独立的 VPC 内。您可以使用云平台提供的负载均衡服务（例如阿里云 SLB）来控制 MQTT 设备的流量，同时通过 VPC 对等连接与其他物联网应用或消息持久化组件进行通信。BYOC Agent 节点负责管理 EMQX 集群、获取监控日志、执行数据备份。

在 EMQX Cloud 端，有一个 BYOC 管理控制台。这个控制台可以让您通过图形界面轻松地管理和控制 EMQX 集群，包括查看集群日志、监控数据。

在数据控制方面，该架构可以分为两层：控制层和数据层。

- 控制层位于 EMQX Cloud 端，负责收集监控数据并向您的集群发送控制指令。它不处理任何业务数据的流入或流出。
- 数据层包括您自己云环境中的 EMQX 集群和 BYOC Agent 节点。它们主要处理客户业务数据的流入或流出。

这种 BYOC 架构可以将您的业务数据完全隔离在自己的云环境中，以满足公司的数据隐私安全和合规要求。

## 优势：灵活、可靠、易用的 MQTT 云服务

选择 EMQX Cloud BYOC，可以享受以下好处：

- 完全掌控您的系统和数据
- 几乎无需运维
- 低网络延迟
- 灵活的部署方案
- 有 SLA 保证的稳定服务
- 专业的技术支持
- 按照需求定制自己的云环境
- 将数据保留在自己的云中，确保数据安全

## 应用场景：保障各类业务的数据安全

EMQX Cloud BYOC 已被包括车联网、医疗保健和智慧城市在内的多个行业广泛采用。

以车联网场景为例，需要将车辆位置和驾驶行为等敏感数据通过公网或私网从车辆端传送到 [MQTT Broker](https://www.emqx.io/zh)，然后存储到公司的统一数据平台。

EMQX Cloud BYOC 可以保证整个数据链都在客户自己的云账户内，避免未授权的访问和数据泄漏。这从源头上解决了数据泄露的风险，减少了中间方的干预，简化了数据管理的难度。

## 结语

总的来说，EMQX Cloud BYOC 为需要严格数据控制和高级安全措施的企业提供了一个强大的解决方案。采用 BYOC 架构，企业不但可以充分利用 EMQX 成熟的 MQTT 技术，同时还可以实现在自己的云环境中完全掌控自己的数据，从而既提高了安全和合规性，也增加了灵活性和扩展性。

如果您想获得更高级的 MQTT 消息云服务，欢迎[访问我们的网站](https://www.emqx.com/zh/cloud/byoc)或[联系我们](https://www.emqx.com/zh/contact?product=cloud)预约演示。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
