我们正处于一场由云计算、大数据和人工智能驱动的全新工业革命浪潮中。

AI 智能体（Agent）的快速演进催生了全新的经济增长模式，推动着工业企业加速融入云生态体系。

公有云平台不仅提供了最先进的大模型、丰富的开发工具和低成本的算力，更构建了一个能让 AI 智能体快速开发、高效交付、敏捷迭代并触达海量客户的产业生态。

对工业企业而言，拥抱云和云上的 AI 能力已不再是「选择题」，而是通往智能制造的「必答题」。

今天的工厂管理者们，追求的早已不只是在 HMI 屏幕上看到一个转速读数。他们渴望的是：

- **预测性维护**：在设备发生故障前，通过 AI 模型预测其健康状况，避免非计划停机。
- **供应链优化**：将实时生产数据与 ERP 的订单数据结合，动态调整生产节拍。
- **能耗管理**：结合电价和生产负荷，智能调度高耗能设备的启停。
- **质量溯源**：利用机器视觉和传感器数据，自动检测微小瑕疵，并将数据与产品批次绑定。

这一切都指向一个核心：**数据不再是孤立的监控指标，而是驱动智能决策、业务优化的血液和燃料。**

这正是传统数采网关（如：Kepware ）逐渐成为「数据瓶颈」的原因所在。Kepware 在工业数据采集与连接方面表现出色，但其核心功能仍停留在「数据传输」层面，缺乏对数据的「理解」和「增值」。在这个云 + AI 的新时代，工业领域迫切需要一款全新的边缘数据基础设施——兼具云原生架构、智能分析能力和开放生态三大特征。

**这就是我们打造 NeuronEX 的初衷：它不仅是 Kepware 的替代品，更是面向未来的、超越性的新一代工业边缘智能网关。**

## NeuronEX：为云 + AI 时代而生的工业边缘大脑

[NeuronEX](https://www.emqx.com/zh/products/neuronex) 是一款面向工业领域的设备数据采集和边缘智能分析软件。它不仅仅是一个协议转换器，更是一个集**多源数据融合、边缘流式计算、AI 算法集成与云边协同**于一体的智能数据中枢。

![image.png](https://assets.emqx.com/images/3752b0c5055d15a0186faff8a3f7ec60.png)

相较于以 Kepware 为代表的传统数采网关，NeuronEX 在设计理念和核心能力上实现了代际超越。

## 五大革新：NeuronEX 重新定义工业边缘

### 架构革新：从重量级 Windows 应用到云原生轻量化部署

| **传统方式（Kepware）**                                      | **NeuronEX 的变革：**                                        |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 典型的 Windows 桌面应用，安装包庞大，依赖特定的操作系统环境，通常需要人工进行安装、配置和维护。在规模化部署和自动化运维场景下，显得笨重且低效。 | **极致轻量**：基于 C 语言和 Actor 模型开发，启动内存占用不足 100MB，资源消耗极低，可以轻松部署在资源受限的边缘硬件（如小型工控机、边缘网关）上。<br>**云原生部署**：全面拥抱容器化技术，提供官方 **Docker** 镜像，支持在 **Kubernetes、K3s** 等容器编排平台中进行声明式部署和自动化管理。这意味着您可以像管理互联网应用一样，快速、可靠、可重复地部署和扩展数以千计的边缘节点，运维效率实现数量级的提升。 |

**核心价值：**NeuronEX 云原生架构带来的敏捷性、可扩展性和易管理性，是传统架构无法比拟的，它彻底解决了大规模工业物联网项目部署和维护的难题。

### 数据流向：从封闭的 OPC 孤岛到开放的数据高速公路

| **传统方式（Kepware）**                                      | **NeuronEX 的变革：**                                        |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 主要通过 OPC-UA/DA 向上提供数据。OPC 是工业自动化领域的优秀标准，但对于云端大数据和 AI 平台而言，它并非原生协议。数据往往需要经过多层中间件转换，才能被大数据系统消费，链路复杂，延迟增加。 | **原生云端协议支持**：NeuronEX 内置丰富的北向应用，支持通过标准的 MQTT 协议，无缝对接到 **Azure IoT Hub、AWS IoT Core** 等主流公有云物联网平台，或 EMQX 等各类 MQTT Broker。<br>**直连大数据生态**：NeuronEX 内置 Kafka、REST API 等多种北向应用，能够将边缘数据直接推送到企业的数据湖、消息队列或任何云端/本地应用，彻底打通了 OT 与 IT 之间的数据壁垒。<br>**支持 SparkplugB 规范**：NeuronEX 深度支持专为工业场景优化的 SparkplugB 规范，能实现设备上线/离线状态的自动感知、设备元数据的自动上报和复杂的拓扑结构定义，这远非一个简单的 MQTT Client 插件所能及。 |

**核心价值**：NeuronEX 采用现代 IT 和互联网领域通用的数据协议，让工业数据从工厂的「局域网」真正融入企业的「数据高速公路」，实现从边缘到云端的高效、无缝流动。

### 数据源：从单一设备采集到多源数据融合

| **传统方式（Kepware）**                                      | **NeuronEX 的变革：**                                        |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 专注于从 PLC、CNC 等工业设备中采集时序数据，这是一个「单向」的数据采集过程。 | NeuronEX 是一个真正的**边缘数据融合平台**。除了支持 100+ 种工业协议外，它还能主动连接和集成来自**数据库（如 MES/WMS/ERP）、企业服务总线(ESB)、RESTful API** 等多种 IT 系统的数据。 |

**核心价值**：这意味着数据处理的变革。您可以在边缘端，将来自 PLC 的实时温度数据，与来自 MES 数据库的当前工单信息进行关联和丰富，形成带有完整业务上下文的「富数据」，再发送到云端。这种边缘侧的数据融合能力，极大地提升了后续数据分析和 AI 应用的价值。

### 核心能力：从「数据管道」到「边缘智能」

| **传统方式（Kepware）**                                      | **NeuronEX 的变革：**                                        |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 本质上是一个「数据管道」（Data Pipe），负责将原始数据从一端原封不动地搬到另一端。所有的计算和分析都发生在 SCADA 或更上层的系统中。 | **强大的边缘流式计算（Stream Processing）**：内置强大的 SQL-based 规则引擎，提供 160+ 内置函数，可在数据上报前进行实时的过滤、清洗、标准化、窗口计算和智能告警。例如，您可以轻松实现「只上报变化超过 5% 的数据」、「将不同设备的温度单位统一为摄氏度」、「计算过去 1 分钟的平均压力值」等。这不仅能大幅减少无效数据传输，还能为云端应用提供高质量的规整数据。<br>**原生 AI/ML 算法集成**：这是 NeuronEX 的「杀手锏」。它允许用户直接在边缘端集成并运行 Python、Go 等语言开发的 AI/ML 模型。无论是基于工业机理的专家模型，还是基于深度学习的预测模型，都能在 NeuronEX 中实现低延迟的推理。<br>更重要的是，它完美支持「**云端训练、模型下发、边端推理」**的主流 AI 模式，通过与云端强大的 AI 能力协同，为边缘赋予更强大的智能。 |

**核心价值**：NeuronEX 将计算和智能推向了离数据源最近的地方。它不再是一个被动的管道，而是一个主动的、具备思考和分析能力的「边缘大脑」，能够实现更快的本地决策和更高效的数据预处理。

### 生态协同：从单点软件到无缝的云边协同

| **传统方式（Kepware）**                                      | **NeuronEX 的变革：**                                        |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 作为一个独立的本地软件，与云平台的集成通常需要二次开发，在身份认证、统一管理、大规模部署等方面存在天然的短板。 | **深度云平台集成**：NeuronEX 从设计之初就考虑了与主流云厂商的协同。它可以作为 **Azure IoT Edge** 或 **AWS IoT Greengrass** 的一个模块运行，接受来自云端的统一部署和管理。<br>**企业级安全集成**：支持与 **Azure Active Directory、AWS Single Sign-On (SSO)** 等服务集成，实现企业级的统一身份认证和单点登录，完美融入企业现有的 IT 安全体系。 |

**核心价值**：NeuronEX 不是一个孤立的边缘产品，而是云战略在边缘的自然延伸。它能够帮助企业构建一个管理统一、安全可靠、高效协同的云边一体化架构。

## 对比总结：Kepware vs. NeuronEX

| **特性维度** | **Kepware（传统数采网关）**    | **NeuronEX（新一代工业边缘智能网关）**       |
| ------------ | ------------------------------ | -------------------------------------------- |
| **核心架构** | Windows 重量级应用，手动部署   | 轻量化、跨平台，**云原生（Docker/K8s）**     |
| **部署运维** | 规模化部署困难，运维成本高     | 敏捷、可扩展，支持自动化运维                 |
| **数据接口** | 主要为 OPC-UA/DA，面向工控领域 | **MQTT/Kafka/API**，原生面向云和大数据       |
| **数据能力** | 单一设备数据采集               | **多源数据融合** (设备 + IT 系统)            |
| **智能处理** | 原始数据转发（数据管道）       | **边缘流式计算 + AI/ML模型集成**（边缘大脑） |
| **生态集成** | 孤立的本地软件                 | **无缝云边协同** (Azure/AWS)，企业级SSO      |

## 结语

NeuronEX 通过云原生的架构、开放的数据生态、强大的边缘智能以及无缝的云边协同能力，为工业数字化转型构筑了坚实的数据底座。选择 NeuronEX，就是选择更敏捷的响应速度、更智能的决策能力、更弹性的扩展空间，让工业数据真正成为驱动业务增长的核心引擎。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
