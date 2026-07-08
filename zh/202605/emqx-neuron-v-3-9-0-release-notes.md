我们很高兴地宣布，NeuronEX 3.9.0 版本正式发布！

该版本核心亮点包括：推出在线驱动配置迁移工具，支持将 KEPServerEX 和 Litmus Edge 的采集配置批量转换为 NeuronEX 可导入格式；新增 Kafka 北向驱动，可与 Microsoft Fabric 原生对接，打通从工业现场到云端数据湖的完整链路；[OPC UA](https://www.emqx.com/zh/blog/opc-ua-protocol) 插件新增 Part 9 条件与报警能力，支持实时订阅报警事件并通过方法调用完成确认操作。

此外，3.9.0 版本还在点位配置、Kafka 连接器、Azure IoT Hub 离线缓存、标准产品包内容等多个方面进行了功能增强，进一步提升了平台的易用性、完整性与稳定性。

## 迁移工具：从 Kepware 和 Litmus Edge 平滑切换至 NeuronEX

从 KEPServerEX 或 Litmus Edge 迁移至 NeuronEX 时，最耗时的环节往往不是软件部署，而是将现有的驱动连接、设备参数与大规模点位（Tag）配置在新平台上重新录入——手工操作不仅拉长实施周期，还会带来抄写差错、寻址不一致和联调返工的风险。

为此，3.9.0 版本配套推出**在线驱动配置迁移工具**（网站托管，无需安装），将第三方平台的导出文件批量映射为 NeuronEX 南向可用的标准 JSON，并与 Dashboard 南向模块的导入流程直接对齐。迁移流程分为四步：**盘点现有协议 → 在源平台导出配置 → 上传至迁移工具完成转换 → 导入 NeuronEX 并联调验证**。

**来源支持：**

- **KEPServerEX**：通过「另存为」导出 JSON，覆盖 Modbus、OPC UA Client、西门子、三菱、欧姆龙、Allen-Bradley 等十余类常用驱动。
- **Litmus Edge**：从 Device Management 导出 Plain Text 模板，支持 Modbus 系列、OPC UA、DF1、欧姆龙 FINS、西门子 S7、BACnet/IP 等常见协议。

转换完成后，工具会展示**设备数量与标签成功/失败汇总**，失败项附带原因说明，便于在 NeuronEX 侧补配或回到源侧调整后重新转换，输出结果与 Dashboard 导入流程完全对齐。

**典型应用场景：**

- **平台替换**：以 NeuronEX 承接原 Kepware 或 Litmus Edge 的采集职能，通过批量迁移压缩割接窗口。
- **试点验证（POC）**：快速复现现有点位与寻址配置，减少因配置偏差引发的验收分歧。
- **灾备与双栈**：在保留原系统的同时，于 NeuronEX 侧快速复现等价南向配置，用于比对或渐进切换。

详细操作步骤请参考：[Kepware 到 EMQX Neuron 迁移指南](https://docs.emqx.com/zh/neuronex/latest/configuration/driver-migration-tool/kepware-to-neuron.html)、[Litmus Edge 到 EMQX Neuron 迁移指南](https://docs.emqx.com/zh/neuronex/latest/configuration/driver-migration-tool/litmus-edge-to-neuron.html)。

![image.png](https://assets.emqx.com/images/66f0d071ea480d7dab093c61ceb5eac3.png)

## 直连 Microsoft Fabric：工业现场数据进入云端数据湖

在工业 4.0 的背景下，最大的挑战往往不是数据太少，而是数据「进不了云」——PLC 协议碎片化、格式不统一，使车间数据难以接入云端分析平台。3.9.0 版本新增**北向 Kafka 插件**，将 NeuronEX 作为标准 Kafka 生产者，而 Microsoft Fabric 的 **Eventstream** 原生兼容 Kafka 协议——两者无需 SDK 开发即可直接打通，形成从设备采集到云端数据湖的完整链路。

**为什么是 Fabric + NeuronEX？**

在边缘侧，NeuronEX 对接 Modbus、OPC UA、各类 PLC 等 100+ 工业协议，将现场时序数据整理为结构化 JSON，由**北向 Kafka 插件**作为生产者直接发布到 Fabric Eventstream Topic，无需经过额外的中间件或采集适配器。

在云端，数据进入 Eventhouse 后，企业可使用 Synapse Data Warehouse 与 ERP/MES 历史数据做关联分析、训练预测性维护模型，并通过 Power BI Direct Lake 构建实时监控大屏——所有能力基于统一的 OneLake，无需数据搬运。

**典型数据流：**

- **实时监控**：NeuronEX 北向 Kafka → Fabric Eventstream → Eventhouse → Power BI 大屏
- **预测性维护**：Eventhouse 历史数据 → Synapse Data Science → 故障预测模型 → 计划外停机预警
- **跨系统分析**：Fabric 将工业时序数据与 ERP 订单、MES 工单在 OneLake 层关联，支撑 OEE 等综合指标计算

详细连接配置及集成步骤请参考：[NeuronEX 与 Microsoft Fabric 集成指南](https://docs.emqx.com/zh/neuronex/latest/configuration/north-apps/kafka/overview.html#对接-microsoft-fabric)

![image.png](https://assets.emqx.com/images/4fe0ebd34a744f4cecbd9afae3242f5e.png)

## OPC UA 条件与报警（Part 9）：订阅报警事件并远程确认

3.8.0 版本已支持 OPC DA AE（基于 COM/DCOM 的传统报警协议），3.9.0 版本则在 OPC UA 插件中新增了完全独立的 **OPC UA Part 9 条件与报警**（Conditions & Alarms）能力。

两者属于不同的协议体系：OPC UA Part 9 是现代 OPC UA 协议栈的原生报警模型，基于订阅机制接收服务器推送的结构化 JSON 事件，并支持通过方法调用（Method）直接对报警执行确认等操作。

**工作方式：**

- 在设备配置中将更新模式设置为 **Subscribe** 或 **Read&Subscribe**，并配置**事件根节点**（默认 `0!2253`，即 Server 节点）。
- 通过点位浏览功能（地址空间扫描）找到报警节点，地址格式为 `alarm:<NS>!<NodeID>`，数据类型为 **JSON**。
- 每条报警事件包含完整的结构化字段：`active`（是否激活）、`confirmed`（是否已确认）、`severity`（严重等级 0-1000）、`message`（报警文本）、`source_name`（报警源）、`time`（Unix 毫秒时间戳）等。
- 方法节点地址格式为 `method:<NS>!<ObjectNodeID>(<MethodNS>!<MethodNodeID>)?<参数名>=<类型>`，数据类型为 JSON，属性为**只写**，可直接调用 OPC UA Server 上的 Confirm 等方法完成报警确认闭环。

**应用场景：**

- **集中报警管理**：将多台 OPC UA 设备的报警事件统一汇聚，通过 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 上送至云端告警平台，实现跨站点的报警集中监控。
- **报警确认自动化**：结合数据处理规则，对特定类别报警自动调用 Confirm 方法，减少人工干预。
- **合规与审计**：完整记录报警的 `event_id`、触发时间与确认状态，满足 GMP、ISO 55000 等合规要求。

详细连接配置步骤请参考：[OPC UA 条件和报警](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/opc-ua/conditions.html)

## 更多增强功能

除了上述亮点，3.9.0 版本还包含以下重要更新：

### 点位配置增强

本版本对点位（Tag）配置能力进行了多项实用增强：

- **单位支持**：点位现在可以配置物理单位（如 `°C`、`bar`、`rpm`），并在点位配置界面和数据监控页面同步展示，提升数据可读性。
- **名称可修改**：支持在创建后修改点位名称，无需删除重建。
- **描述长度提升**：点位描述字段的最大长度由原有限制提升至 **256 个字符**，支持更完整的运维备注。

![image.png](https://assets.emqx.com/images/4d4006aef13e87b9a1b2ff0490b4b429.png)

### Kafka Connector：多节点共享连接

新增 **Kafka Connector** 功能，允许数据处理模块中的多个 Kafka Sink 共享同一个 Kafka 连接配置。在此之前，每个 Kafka Sink 节点都需要独立维护一套连接参数（Broker 地址、认证信息、SSL 证书等），当多个规则（Rule）需要将数据发布到同一 Kafka 集群时，重复配置不仅繁琐，还会建立多条独立的物理连接，消耗额外的系统资源。

通过 Kafka Connector，用户只需在 Connector 层统一维护连接参数，多个 Kafka Sink 节点均可引用同一 Connector，从而复用底层 Broker 连接。

![image.png](https://assets.emqx.com/images/d1ce3244286c929082adfd0ccfe5a20c.png)

### Azure IoT Hub 离线缓存

北向 Azure IoT Hub 插件新增**离线缓存**能力。网络短时中断期间，采集数据自动写入本地缓存队列；网络恢复后按时序自动续传，确保数据完整性，适用于工厂无线网络、4G/5G 蜂窝网络及矿山、风电场等远程站点场景。

### 标准产品包扩充 CNC 驱动

标准产品包现已内置**全部 CNC 驱动插件**，用户无需单独申请授权即可使用完整的 CNC 设备接入能力，降低了数控机床接入场景的使用门槛。

## 结语

NeuronEX 3.9.0 的发布，进一步降低了从 Kepware、Litmus Edge 迁移的门槛，通过 Kafka 北向驱动打通了与 Microsoft Fabric 等现代数据平台的直连通路，并以 OPC UA Part 9 条件与报警能力补全了工业报警管理的关键拼图。

欢迎您下载并试用新版本，体验更完整、更可靠的工业数据连接：[下载 EMQX Neuron](https://www.emqx.com/zh/downloads-and-install/neuronex)

**NeuronEX 3.9.0 完整功能，请查阅文档：** [产品概览 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/)
