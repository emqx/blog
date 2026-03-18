## 事件背景

**2026 年 3 月初，一场外部因素引发的基础设施事故重创了 AWS 中东区域（ME-CENTRAL-1，UAE）。** 

事故造成数据中心物理损坏、电力中断及网络连接异常，导致多个可用区（Availability Zone）出现中断或性能下降，影响了 EC2、S3、DynamoDB 等多项核心服务。随着 AWS 故障持续扩散，ME-CENTRAL-1 区域内的多个可用区（AZ）相继停摆，引发了区域可用性的整体瘫痪。

作为 IoT 消息基础设施平台，EMQX Cloud 在该区域部署的部分实例也受到影响。但凭借多 AZ 集群架构、快速故障转移以及跨 Region 灾备方案，EMQX Cloud 有效保障了客户设备连接和关键业务的持续运行。

**本文将复盘 EMQX Cloud 在本次事件中的应急响应过程，并深度拆解 EMQX 在云原生 IoT 消息服务中的高可用设计。**

------

## 事件响应时间线

### AZ2 触发故障转移

**2026 年 3 月 1 日 14:00 (UTC)，**EMQX Cloud 监控系统检测到 UAE Region **AZ2 出现基础设施故障**，部分部署触发告警。

EMQX Cloud 立即执行以下措施：

- 将 AZ2 上的节点进行**故障转移（Failover）**
- 节点迁移至 **AZ1 和 AZ3。**
- 维持集群多 AZ 高可用状态。

在多 AZ 架构下，MQTT 客户端可以自动连接到其他可用节点，因此：

- 设备连接**未出现大规模中断。**
- MQTT 消息服务持续提供。

### AZ3 性能下降

**2026 年 3 月 2 日 06:00 (UTC)**，EMQX Cloud 监控发现：

- AZ3 出现**性能下降。**
- 部分连接请求失败。

此时 AWS 区域内仅剩 AZ1 仍保持相对稳定。EMQX Cloud 团队采取以下措施：

- 通过多渠道联系受影响客户。
- 建议客户评估**跨 Region 迁移方案。**
- 将 UAE Region 的实例**集中迁移至 AZ1。**

同时，EMQX Cloud 为可能发生的 Region 迁移做准备：

- 将 EMQX 配置数据**备份频率调整为每 60 分钟一次。**
- 确保集群配置可以快速恢复。

此阶段 UAE Region 的部署进入**临时单 AZ 运行模式**。

### 启动跨 Region 灾备迁移

**2026 年 3 月 3 日 04:00 (UTC)**，监控系统检测到 **AZ1 实例性能开始下降**。

考虑到区域稳定性风险持续上升，EMQX Cloud 团队与客户沟通并决定执行**跨 Region 迁移**。具体迁移流程如下：

- 从 **S3 恢复 EMQX 配置备份**
- 在新的 AWS Region 创建集群
- 协助客户修改外部资源地址
- 验证设备连接
- 执行 DNS 切换

迁移工作从 07:00 (UTC) 开始，至 19:00 (UTC) 完成。在迁移过程中：

- 设备连接逐步切换至新 Region
- EMQX Cloud 团队持续监控 UAE Region 状态
- 持续联系客户进行验证

------

## 客户协作与迁移策略

EMQX Cloud 的跨 Region 迁移策略**不会自动触发**。主要原因包括：

- 客户业务系统可能依赖外部资源地址。
- 需要验证设备连接与应用兼容性。
- 需要确保业务迁移不会影响客户系统。

因此，迁移流程采用**「客户确认 + 平台协助迁移」模式，**在整个事件过程中，EMQX Cloud 团队主动通知受影响客户，提供相应的灾备建议，并协助客户完成 DNS 切换和验证设备重新连接。

------

## EMQX Cloud 的高可用设计：从架构理念到实战验证

本次突发的基础设施事故，再次验证了 EMQX Cloud 在 IoT 消息基础设施方面的高可用设计。

通过以下三个维度，EMQX Cloud 确保了 IoT 消息基础设施在危机下的稳健运行：

### 多可用区架构

EMQX Cloud 集群通常部署在多个可用区中，集群中的每个节点独立运行，当单个可用区遭遇物理损毁或断电时，集群会自动在存活节点间平滑切换，结合 MQTT 客户端支持的自动重连特性，保障设备端连接零中断。

### 快速故障转移

在此次事件中，当 AZ2 故障发生时，EMQX Cloud 触发了故障转移机制。系统根据集群容量，将失效节点及其承载的业务负载自动重新分配到健康的 AZ1 与 AZ3。

这种动态治理能力，保证了消息分发性能不因局部硬件瘫痪而折损，维护了消息服务的持续运行。

### 配置与状态备份

EMQX Cloud 会对 集群配置和关键元数据进行定期备份，并同步至高可靠性的对象存储，以支持在新 Region 中快速恢复集群环境。

需要说明的是，EMQX Cloud 的备份机制 仅包含平台配置与运行所需的元数据，例如：

- 认证与权限配置
- 规则引擎配置
- 资源连接配置
- 其他集群级运行配置

客户的 MQTT 消息数据（message payload）不会被备份或持久化存储。

在本次事件的预警阶段，EMQX Cloud 将配置备份频率从常规策略提升至 **60 分钟一次**，以便在需要执行跨 Region 恢复时，能够快速恢复集群配置并完成部署。

**多次实战验证了 EMQX 的高可用设计：**

[硬件故障，服务不停：EMQX 创造 1770 天不间断运行纪录](https://www.emqx.com/zh/blog/emqx-1770-days-uninterrupted-operation) 

[How EMQX Cloud Weathered the AWS us-east-1 Storm: Lessons in Building Resilient IoT Infrastructure](https://www.emqx.com/en/blog/how-emqx-cloud-weathered-the-aws-us-east-1-storm)   

------

## 未来的灾备架构规划

基于此次故障事件的实战经验，EMQX Cloud 计划进一步增强跨 Region 容灾能力。

**在原本 Core + Replica 架构的基础上，EMQX Cloud 将针对高风险区域提供新的部署模式：**

- **Core 节点：**部署在高度稳定的 Region，负责核心数据与集群状态。
- **Replica 节点：**部署于客户就近 Region，提供高性能的设备接入与消息吞吐。

该部署模式下，当特定区域遭遇灾难性停摆时，系统无需复杂的数据迁移，仅通过简单的 DNS 切换，即可在异地实现业务的满血复活，大幅减少传统灾备中繁琐的恢复周期。

同时，EMQX Cloud 也将进一步 **增强集群配置与数据迁移能力**，为跨 Region 灾备提供更加高效和标准化的工具与流程。

通过完善的配置备份、数据恢复以及集群迁移机制，客户可以在新的 Region 快速恢复 EMQX 集群环境，并完成业务接管。

在这一模式下：

- **AZ 级故障转移** 由 EMQX Cloud 平台自动完成
- **Region 级故障转移** 可由客户根据业务需求主动执行

当区域级故障发生时，客户可以基于已有的备份和迁移能力，在新的 Region 快速恢复集群并完成 DNS 切换，从而实现区域级灾备恢复。

------

## **结语**

本次 AWS 中东区域的意外停摆再次向行业敲响警示：即使是顶级的云服务商，也无法完全规避物理世界的极端扰动。数据底座的脆弱性，往往在风暴来临时才显现。

**故障不可完全避免，但中断可以提前防御。**EMQX Cloud 在本次事件中的稳健表现，源于我们对高可用设计的坚持：

- 多 AZ 高可用架构。
- 快速故障转移能力。
- 跨 Region 灾备迁移。
- 持续的客户协作与支持。

AI 与全球化快速发展，IoT 消息基础设施已成为企业出海的生命线。未来，EMQX Cloud 将强化跨 Region 容灾架构，为全球 IoT 应用提供更可靠的消息基础设施，确保每一台设备、每一个智能体的数据都能自由流动，永不停歇。

**消息来源：**

- [AWS Power Outage in Middle East Triggers Major Disruption to EC2 and Networking Services](https://cybersecuritynews.com/aws-power-outage/?utm_source=chatgpt.com) 

- [Middle East AWS Outage Sends Shockwaves Through Cloud Infrastructure Service](https://gbhackers.com/middle-east-aws-outage/?utm_source=chatgpt.com) 



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/new" class="button is-gradient">开始试用 →</a>
</section>
