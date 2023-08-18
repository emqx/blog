MQTT Sparkplug 是广泛应用于[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)领域的通信协议。Sparkplug 3.0 是其最新版本，进行了诸多重大改进和规范化。该版本由 Eclipse Sparkplug Working Group 制定，旨在澄清之前 2.2 版本规范中存在的不明确之处，并与 2.2 版本保持兼容。

## **Sparkplug 3.0 的主要改进**

### 更清晰的规范结构

新规范将 v2.2 中的“背景”章节替换为“原则”章节，详细阐述了 Sparkplug 遵循的基本原则。此外，“操作行为”章节更加全面地涵盖了 Sparkplug 环境中与操作相关的内容。

### 更明确严谨的规范目标

Sparkplug 3.0 的主要目标是提供清晰严谨的规范，消除先前版本中的歧义。它为协议制定了明确规范的声明，以确保一致性并便于实施。

### 支持 MQTT 5.0

Sparkplug 3.0 包含了一些与 MQTT 5.0 相关的特定配置，主要针对会话设置的差异，例如，在 MQTT 3.1.1 中是“[Clean Session](https://www.emqx.com/zh/blog/mqtt-session)”，而在 MQTT 5.0 中是“Clean Start”。这些新增内容使 Sparkplug 能够支持 MQTT 5.0 引入的一些新功能。

### 对 MQTT 服务器的特定要求

Sparkplug 基础设施对 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)有一定的特定要求。任何遵守完整规范的 MQTT 3.1.1 服务器或 Broker 都能够满足这些要求。

在 Sparkplug 规范中对 MQTT 服务器有两个不同的要求等级。第一级（*Sparkplug Compliant MQTT Server*）是只要 MQTT 服务器遵循 MQTT 3.1.1 标准，就可以满足基本的要求。第二级（*Sparkplug Aware MQTT Server*）则需要 MQTT 服务器具备一些额外的功能。

**第一级：Sparkplug Compliant MQTT Server**

Sparkplug Compliant MQTT 服务器必须支持以下功能：

- QoS 0（最多一次）用于传输数据
- QoS 1（至少一次）用于管理状态
- 支持保留消息
- 遗嘱消息（LWT）用于管理状态
- 支持通配符

**第二级：Sparkplug Aware MQTT Server**

除了满足 Sparkplug Compliant MQTT 服务器的要求外，Sparkplug Aware MQTT 服务器必须还具有以下附加功能：

- 在 NBIRTH 和 DBIRTH 消息经过 MQTT 服务器时，把它们保存下来。
- 为以下格式的主题提供 NBIRTH 消息：`$sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id}`。例如，如果 `group_id=GROUP1`，`edge_node_id=EON1`，则必须为下面的主题提供 NBIRTH 消息：`$sparkplug/certificates/spBv1.0/GROUP1/NBIRTH/EON1`
- 为以下主题提供 NBIRTH 消息：`$sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id}`，并将 MQTT 保留标志设置为 true。
- 为以下格式的主题提供 DBIRTH 消息：`$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}`。例如，如果 `group_id=GROUP1`，`edge_node_id=EON1`，`device_id=DEVICE1`，则必须为下面的主题提供 DBIRTH 消息：`$sparkplug/certificates/spBv1.0/GROUP1/DBIRTH/EON1/DEVICE1`
- 为以下主题提供 DBIRTH 消息：`$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}`，并将 MQTT 保留标志设置为 true。
- 修改 NDEATH 消息的时间戳。在 MQTT 服务器修改时间戳时，时间戳必须设置为向订阅客户端发送 NDEATH 消息的时间（使用 UTC 时间）。

Sparkplug Aware MQTT 服务器扩展了 Sparkplug 的状态管理方式。本质上，birth 和 death 证书现在作为保留消息存储，并且可以使用新引入的主题结构 `$sparkplug/certificates/#` 来访问。

更新 NDEATH 消息的时间戳的能力是这个版本的一个显著特点。由于使用了遗嘱消息功能，所以这些时间戳被存储在 Broker 中。遗嘱消息包含在 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)尝试中，因为客户端断开连接的实际时间是未知的，所以连接中包含了一个无效的时间戳，通过发布 LWT 消息来更新这个时间戳解决了这个问题。

## **Sparkplug 3.0 给工业物联网应用带来的优势**

### 增强互操作性

Sparkplug 3.0 通过建立更标准更明确的规范，提高了工业物联网设备、系统和平台的互操作能力。这为工业环境中的无缝集成和通信提供了条件。

### 高效数据同步

MQTT Sparkplug 3.0 通过强化状态管理功能，实现了设备之间高效且同步的数据更新。这一功能对于应对大规模的工业物联网部署非常有用。

### 简化部署

Sparkplug 规范要求兼容现有的 MQTT v3.1.1 服务器，以减少在采用 Sparkplug 3.0 过程中对基础设施的变更需求。

## **Sparkplug 兼容性计划**

Sparkplug 兼容性计划使软件和硬件厂商可以验证它们的产品是否与 Eclipse Sparkplug 和基于 MQTT 的物联网基础设施相兼容。该计划推动了工业物联网中各种设备和网络的无缝集成，保障了解决方案的质量和易用性。

经过认证的厂商能够保证其产品符合 Sparkplug 规范，从而实现平稳的互操作和高效的部署。厂商需要通过开源测试来验证其产品是否符合 Sparkplug 技术兼容工具包（TCK）的标准。通过了测试的产品将被列入官方的兼容产品名单，您可以在 [Sparkplug Working Group 网站](https://www.eclipse.org/org/workinggroups/eclipse_sparkplug_charter.php)上查看该名单。

Sparkplug Compatible logo 为厂商产品的兼容性提供了背书。经过认证的产品通过了严格的测试，达到了必要的标准，值得客户信任。

该计划给厂商和客户都带来了益处：

- 实现无缝集成

  该项目提高了互操作性，为系统集成商和终端用户简化了集成过程。经过认证的组件能够协同工作，让组织可以放心地打造强大的物联网解决方案。

- 激发创新和合作

  认证促进了创新和合作。厂商让其产品符合 Sparkplug 标准，实现了功能强大、互通的解决方案。供应商之间的知识交流和协作，构建了一个活跃的生态系统。

## **结语**

Sparkplug 3.0 为 MQTT Sparkplug 协议带来了重大改进和规范化，使其更加清晰、明确，并增加了对 MQTT 5.0 的支持。Sparkplug 3.0 提供了更强的互操作性、更高效的数据同步和更便捷的工业环境部署。随着工业物联网生态系统的不断发展，Sparkplug 3.0 为在工业物联网网络中实现可靠和可扩展的通信提供了一个强大且标准化的解决方案。

作为全球领先的[开源 MQTT Broker，EMQX](https://www.emqx.io/zh) 是处理 Sparkplug 3.0 消息流的基础设施的核心部分。[工业物联网连接服务器 Neuron](https://neugates.io/zh) 则可以作为边缘节点，让 OT 设备更加智能，并以异步方式发送 Sparkplug 3.0 消息。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
