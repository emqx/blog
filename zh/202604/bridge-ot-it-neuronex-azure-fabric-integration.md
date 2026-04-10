在工业 4.0 的浪潮中，最大的挑战往往不在于数据太少，而在于数据**「听不懂」**。PLC 协议碎片化、格式不统一，使得车间数据难以进入云端进行分析。

本文将教你如何利用 **NeuronEX** 工业边缘网关软件与 **Microsoft Fabric** 下一代统一数据分析平台，在 **15 分钟**内搭建一套从设备采集、边缘处理到云端存储的完整数据管道。

## 为什么选择 NeuronEX + Microsoft Fabric？

### 什么是 Microsoft Fabric？

**Microsoft Fabric** 是微软推出的统一 SaaS 级大数据分析平台，通过 **OneLake**（统一数据湖）将数据集成、数据工程、实时分析和可视化无缝结合。

对于工业场景，其核心组件 **Eventstream** 提供了：

- **原生 Kafka 兼容性**：支持标准 Kafka 协议接入，无需复杂 SDK 开发。
- **毫秒级流式摄入**：实时处理工业设备采样数据。
- **无服务器弹性伸缩**：自动应对上万个点位的突发流量。
- **实时数据转换引擎**：在数据「落地」前进行过滤、聚合和映射。

### NeuronEX：工业协议的「翻译官」

**NeuronEX** 是一款面向工业领域的边缘数据采集与处理软件，核心优势包括：

- **100+ 工业协议支持**：Modbus、OPC UA、西门子 S7、三菱、欧姆龙等。
- **轻量化部署**：支持 X86/ARM 架构，Docker/Kubernetes 容器化部署。
- **边缘流式计算**：内置 SQL 引擎，可在边缘侧进行数据过滤、聚合、转换。
- **高性能低延迟**：轻松处理 10,000+ 数据点，毫秒级采集响应。

### 为什么这个组合是工业数字化的理想方案?

NeuronEX 与 Microsoft Fabric 的联动，本质上是**将工业数据的「最后一公里」采集能力与云端「无限算力」完美结合**。

**在边缘侧**，NeuronEX 将 100+ 碎片化的工业协议统一转换为标准 Kafka 格式，其内置的 **SQL 流计算引擎**可以在数据离开工厂之前完成清洗、过滤和聚合——这意味着仅将高价值数据上云，而非一股脑传输原始数据。

**在云端**，Fabric 提供的不仅仅是一个「存储桶」，而是一个**从数据湖到 AI 模型的全栈分析平台**。工业数据进入 Fabric 的 Eventhouse 后，企业可以利用 Synapse Data Warehouse 进行跨系统的历史数据关联分析（如将设备运行日志与 ERP 订单数据结合）。使用 Synapse Data Science 训练预测性维护模型，最后通过 Power BI Direct Lake 构建实时监控大屏——所有这些能力都基于统一的 OneLake 数据湖，无需数据搬运。

通过 NeuronEX 与 Microsoft Fabric 的组合，数据可以驱动 AI 预测、优化生产排程、支持跨工厂的供应链决策，让数据真正流动起来，为业务创造持续价值。

## 15 分钟实战：搭建从边到云的数据管道

### 数据流架构概述

![image.png](https://assets.emqx.com/images/b40c95cf0183d6bb157c2a5f534636f3.png)

### 步骤 1：在 NeuronEX 中配置南向数据采集

本示例使用 **OPC UA Server Simulator** 作为数据源，通过创建 OPC UA 南向驱动连接模拟器，获取实时数据。

![image.png](https://assets.emqx.com/images/32dc5436892e3e23e6e605e558f5a244.png)

![image.png](https://assets.emqx.com/images/3559c0ea03a9f072ea4693a0abb03ccd.png)

**快速入门指南：**

- **使用内置 Modbus 模拟器**。NeuronEX 提供内置 Modbus TCP Server 模拟器，无需外部设备即可快速测试。参考：[Modbus 模拟器配置指南](https://docs.emqx.com/zh/neuronex/latest/configuration/modbus-simulator.html)
- **连接真实 PLC 设备**。支持西门子、三菱、欧姆龙等主流 PLC。参考：[PLC 设备采集最佳实践](https://docs.emqx.com/zh/neuronex/latest/best-practise/plc-to-mqtt.html)

### 步骤 2：通过数据处理模块推送数据到 Fabric

#### 1. 将采集数据订阅到数据处理节点

![image.png](https://assets.emqx.com/images/afac15fe2dbbe085afbdffe9d64cdd7e.png)

#### 2. 创建数据处理规则

**默认 SQL 示例**：

```
SELECT * FROM neuronStream
```

> 此 SQL 会将采集到的 JSON 数据全部转发到 Fabric。在生产环境中，建议使用 `WHERE` 条件过滤高价值数据。

#### 3. 配置 Kafka Sink（连接到 Fabric）

| **配置项**                          | **说明**                                | **示例值**                                       |
| :---------------------------------- | :-------------------------------------- | :----------------------------------------------- |
| **Broker**                          | Fabric Eventstream 的 Bootstrap server  | `neuron-eventstream.servicebus.windows.net:9093` |
| **Topic**                           | Fabric 中的 Topic name                  | `neuron-topic`                                   |
| **SASL Username**                   | 固定字符串                              | `$ConnectionString`                              |
| **SASL Password**                   | Fabric 的 Connection string-primary key | `Endpoint=sb://...`                              |
| **SASL Auth Type**                  | 认证方式                                | `plain`                                          |
| **Skip Certification Verification** | 跳过 TLS 证书验证（开发环境）           | `True`                                           |

> 如何获取以上Fabric信息，请参考后续章节。

点击「**测试连接**」按钮，显示「连接成功」即表示 NeuronEX 与 Fabric Eventstream 通讯正常。

![image.png](https://assets.emqx.com/images/6dcbb5d80afa8fd38e3c03d69abd2a58.png)

保存规则，NeuronEX 端配置完成。

![image.png](https://assets.emqx.com/images/e0a0c9484f7b6e4c0759f782fbdf02a1.png)

### 步骤 3：在 Fabric 配置 Eventstream 数据流

#### 为什么在工业场景首选 Eventstream？

Microsoft Fabric 提供了多种数据接入路径：**Data Factory** 擅长离线批处理，**Warehouse** 适合结构化分析。但在工业物联网场景下，我们面对的是秒级的设备采样，**Eventstream** 才是真正的「实时数据枢纽」。

**Eventstream 的四大优势**：

- **原生 Kafka 兼容性**：NeuronEX 无需 SDK 开发即可无缝连接。
- **超低延迟**：在几秒钟内实现从设备到云端真正的流式传输。
- **无服务器弹性**：无需管理 Kafka 集群即可自动扩展到数千个点。
- **实时转换**：在数据流入湖之前对其进行过滤和聚合。

#### 创建 Eventstream

1. 在 Fabric 工作区中新建 Eventstream：

   ![image.png](https://assets.emqx.com/images/e7c85c42318f3e2e0e4b05969b0acbf6.png)

   ![image.png](https://assets.emqx.com/images/3682289a6f60be1304659a5daaaff181.png)

1. **选择数据源接入方式**：`Use custom endpoint`（自定义终端节点）

   ![image.png](https://assets.emqx.com/images/b2a96a3397abc316031918534f5ac54d.png)

1. **配置数据目标**：选择 `Eventhouse`（数据库）

   ![image.png](https://assets.emqx.com/images/7b3040fd8da64cb44c81ddb1df497365.png)

1. **配置 Eventhouse 存储**：

   ![image.png](https://assets.emqx.com/images/2e9b60510d06bd7fcab9f28ba69d4fe6.png)

1. **发布 Eventstream**：

   ![image.png](https://assets.emqx.com/images/1268b455748cc6f38cc8a30c9269cc62.png)

### 步骤 4：获取 Eventstream 连接信息

从 Fabric Eventstream 页面中检索 Bootstrap server、Topic name、Connection string-primary key，并将内容填入到 NeuronEX 对应配置页面中。

![image.png](https://assets.emqx.com/images/8283936b31b454cc2c74e397c997156a.png)

### 步骤 5：数据验证与入库

#### Eventstream 数据预览

点击 Eventstream 画布中的节点 `eventstream-neuron`，切换到「**数据预览**」，实时查看 JSON 消息的更新，即可确认数据已成功上传至云端。

![image.png](https://assets.emqx.com/images/e8ca5fae48322fc252c484728d4baea6.png)

#### Eventhouse 数据查询

数据流入 Eventhouse 后，可在 `eventhouse-neuron` 页面查看 `table-neuron` 中的详细数据：

![image.png](https://assets.emqx.com/images/4f195a22064b530adc767cca164cedbe.png)

**至此，从 PLC 到云端的数据管道已完全打通！**

## 超越数据传输：Eventstream 与 Fabric 的强大数据能力

Eventstream 不仅是数据传输工具，更是一款发挥关键作用的「智能过滤器」。工业现场往往会产生大量冗余数据（例如：恒定不变的温度读数）若不经过滤全量上云，将显著增加存储成本。

### Eventstream 的实时数据处理能力

在 Eventstream 中，您可以通过内置的**数据转换操作（Operations）** 完成以下任务：

| **能力**                      | **应用场景**                                                |
| :---------------------------- | :---------------------------------------------------------- |
| **数据过滤（Filter）**        | 仅上传温度 > 80°C 的数据，过滤掉稳态运行的冗余记录          |
| **字段映射（Manage fields）** | 将 PLC 的 `tag001` 重命名为 `temperature_celsius`，增强语义 |
| **聚合运算（Aggregate）**     | 每 1 分钟聚合一次平均值、最大值、最小值                     |
| **路由分发（Route）**         | 根据设备 ID 将数据路由到不同的 Eventhouse 表中              |

### Fabric 平台的全栈数据分析能力

数据进入 Fabric 后，您可以利用其全栈能力构建从数据到洞察的完整闭环：

#### **Data Factory**：企业级 ETL/ELT

- 将 Eventhouse 的实时数据与 ERP/MES 系统的历史数据进行关联
- 支持 100+ 数据源连接器（SQL Server、SAP、Snowflake 等）
- 低代码 Dataflow Gen2 或代码优先的 Pipeline

#### **Synapse Data Warehouse**：湖仓一体分析

- 直接在 OneLake 的 Delta Parquet 文件上运行 T-SQL 查询
- 无服务器架构，按查询付费
- 支持 PB 级数据的交互式分析

#### **Synapse Data Science**：AI/ML 模型训练

- 利用工业历史数据训练预测性维护模型
- 内置 MLflow 进行实验管理
- 模型推理结果直接写回 OneLake，供 Power BI 调用

#### **Power BI Direct Lake**：实时可视化

- 对海量工业数据进行亚秒级交互式分析
- 无需数据导入，直接查询 OneLake
- 构建生产监控大屏、OEE 分析仪表盘

![image.png](https://assets.emqx.com/images/acccd28a88b5a3fb32a4315842e909af.png)

通过 Fabric 可快速搭建 IIoT 分析仪表盘

完整了解 Fabric 的功能，请阅读 Fabric 官方文档：[Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)

## NeuronEX 能力扩展：工业智能数据平台

基础的 PLC 数据采集只是第一步。在实际的工业场景中，企业往往需要整合多种数据源、在边缘侧进行智能过滤，并结合云端 AI 实现预测性分析。以下是三种进阶应用场景。

### 多源数据集成：打破信息孤岛

传统工业生产数据通常分散在 PLC、MES、ERP 和视频系统中。NeuronEX 的多源数据集成能力可以在单一平台完成异构数据的统一采集，结合其数据处理引擎，支持在边缘侧将 PLC 数据与 MES 工单信息关联，从而为 Fabric 提供具有完整业务上下文的的数据流。

这种能力彻底打破了 IT 与 OT 的数据孤岛，为跨系统的根因分析奠定了基础。

**推荐阅读**：[NeuronEX 最佳实践：集成 MySQL 数据到 IIoT 平台](https://docs.emqx.com/zh/neuronex/latest/best-practise/sql-data.html)

### 边缘数据预处理：仅上传「高价值」数据

工业设备的采样频率很高，上传原始高频数据会消耗大量的带宽和存储成本。利用 NeuronEX 的 SQL 引擎，企业可以实现阈值过滤、变化率检测、时间窗口聚合以及异常检测。这些策略可以将云端数据量减少 90% 以上，从而显著降低存储成本并提高分析效率。

这种能力确保了进入 Fabric 的每一条数据都是经过筛选的高价值信息。

**推荐阅读**：超越连接：如何在边缘侧构建高效的工业数据处理与清洗引擎（待发布）

### 边缘 AI + 云端分析：预测性维护闭环

通过 Neuron + Fabric 的组合，构建「边缘 AI 实时告警 + 云端 ML 长期预测」的智能运维体系，实现从「被动式」维护到「预测性」维护的转变。

NeuronEX 可在边缘加载 Python 或 ONNX AI 模型，实现毫秒级异常检测（例如，通过 REST Sink 向 MES 发送振动警报）。同时，Fabric 中的历史数据用于训练长期模型（例如 LSTM），以预测未来 7 天的故障概率，并在 Power BI 上显示。此循环可将计划外停机时间减少 30-50%，同时降低 20-30% 的维护成本。

**推荐阅读**：[NeuronEX 算法集成指南](https://docs.emqx.com/zh/neuronex/latest/streaming-processing/extension.html)

## 总结

NeuronEX 与 Microsoft Fabric 的集成，实现了工业数据从「采集」到「洞察」的无缝衔接。通过在边缘侧完成协议转换和智能过滤，企业可以大幅降低云端成本。同时，借助 Fabric 提供的全栈数据分析能力（ Eventstream 实时处理、Synapse 深度分析、Power BI 可视化），让工业数据的价值得以充分释放。

无论您是希望快速验证工业数据上云方案，还是构建企业级智能运维平台，这套组合都能为您提供从边缘到云端的完整解决方案。

**立即行动，让您的工业数据发挥真正的价值**

------

**立即体验：**[**下载 NeuronEX**](https://emqx.atlassian.net/wiki/spaces/EMQXBC/pages/2428043344/OT+IT+15+NeuronEX+Azure+Fabric#)

**深入了解：**[**产品概述 | NeuronEX 文档**](https://docs.emqx.com/zh/neuronex/latest/)
