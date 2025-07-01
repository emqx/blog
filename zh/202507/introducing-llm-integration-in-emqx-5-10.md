物联网（IoT）的核心在于数据。然而，随着联网设备产生的数据量激增，行业面临的挑战也从单纯的数据收集，转变为如何实时理解和处理数据。不妨想象这样一个场景：您只需像日常对话一样，使用自然语言就能实时查询数据流；而原本晦涩难懂的传感器数据，转眼间就能变成清晰明了的预警提示，直接指导您的下一步行动。

这一愿景正在成为现实。随着 EMQX 5.10.0 的发布，实时数据流与人工智能的融合已进入全新阶段，我们创新性地在可视化流处理引擎中集成大语言模型（LLM）。这将为您的 MQTT 数据流注入 OpenAI GPT、Anthropic Claude 以及任何兼容 OpenAI 的大模型的强大功能。

![image.png](https://assets.emqx.com/images/74b33dc1243c013e4f5bdfb4e9f8192e.png)

<center>EMQX - 连接物理世界和人工智能</center>

## 为什么要将物联网数据流与人工智能相结合？

传统上，将人工智能应用于物联网数据需要复杂且昂贵的工程设计。您必须将数据从 [MQTT broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 迁移到单独的平台进行处理，这会给时效性要求高的应用程序带来不可接受的延迟。

EMQX 创新性地解决了这一痛点。通过将 AI 处理能力直接嵌入数据流，您可以构建智能工作流，实时分析、增强和转换 MQTT 消息。这为开发具备实时感知、推理和响应能力的新型应用奠定了基础。在首个版本中，我们已实现与 OpenAI 和 Anthropic 模型的深度集成。

![image.png](https://assets.emqx.com/images/2ec7a9bf1682dc77098fb4335b6ced5d.png)

<center>将 AI 处理嵌入到 MQTT 数据流中</center>

## 解锁全新可能：关键应用场景

将大模型融入数据流，可轻松实现过去难以构建的创新应用场景。

- **智能异常检测：**

  **大模型能够综合分析多字段关联关系，识别复杂异常状态，突破传统阈值告警的局限。**

  例如，对 `{'振动值': 9.5, '温度': 85, '压力': 1.2}` 这样的数据进行整体分析，大模型可以智能推断：同一读数中，当振动与温度同时升高时，其风险程度远高于单一指标异常，进而生成精准告警：「紧急告警：设备 XYZ 同时出现高振动与高温，可能存在轴承过载风险」。

- **实时数据汇总：**

  **将传感器原始、复杂的 JSON 数据自动转换为简洁直观的业务语言，用于仪表板或移动通知。**

  例如，将原始数据 `{"device_id": "device123", "temperature": 38.2, "humidity": 75}` 自动转换为「设备 device123 高温告警：温度 38.2°C，湿度 75%」，以此显著提升监控效率。

- **自然语言数据处理：**

  **通过简单指令完成复杂数据转换。**

  例如，您可以指示大模型处理包含多个功率读数的 JSON 数据并仅返回总和，从而简化下游分析的数据准备工作。

- **语义数据分类：**

  **根据消息内容自动对其进行分类和路由。**

  例如：大模型可以读取设备日志，确定其事件是「INFO」、「WARNING」还是「CRITICAL_ERROR」，并标记消息以便将其路由到不同的系统。

## 5 分钟快速入门：创建您的首个 AI 驱动流程

无需编写代码，通过可视化 Flow 设计器即可快速构建一个读取传感器数据，并使用 OpenAI 生成易读摘要的数据流。

**准备工作：**您需要一个有效的 OpenAI API 密钥。

**步骤 1：设置数据源**

在 EMQX Flow 设计器中，将「消息节点」拖到画布上。配置它以订阅您设备发布数据的 MQTT 主题，例如`sensors/temp_humid`。

![image.png](https://assets.emqx.com/images/2ab172c30aa252392e603022092bd410.png)

**步骤 2：添加 AI 处理**

从处理面板拖拽「OpenAI 节点」到数据源节点。在配置面板中：

- **输入：**选择 `payload` 将整个 MQTT 消息传递给模型。
- **系统消息：**输入自然语言指令。例如：将设备传感器读数转换为易读的简短摘要。
- **模型：**选择一个 OpenAI 模型，例如 `gpt-4o`。
- **API 密钥：**安全输入您的 OpenAI API 密钥。
- **输出别名：**为 AI 的输出命名，例如 `summary`。

![image.png](https://assets.emqx.com/images/52fdacbeb490c779938f842144b9d7a5.png)

**步骤 3：重新发布洞察**

从输出面板拖出一个**「重新发布」**节点并将其连接到 OpenAI 节点。配置它并将结果发布到一个新主题中，如 `ai/summary`，在 `payload` 字段中使用刚才创建的别名： `${summary}`。

![image.png](https://assets.emqx.com/images/5451e1e49d3eebddfaf9d202ec51fdb8.png)

**步骤 4：部署和测试**

连接所有节点并保存流程。

![image.png](https://assets.emqx.com/images/2cae54cca2e4e192f5612922b404efd8.png)

现在，当您向主题发布 JSON 消息时，您将看到该主题上实时 `sensors/temp_humid` 出现自然语言摘要`ai/summary`。

发布一条测试消息，例如：

```json
{
  "device_id": "device123",
  "temperature": 38.2,
  "humidity": 75,
  "timestamp": 1717568000000
}
```

并收到智能摘要：

> 2024 年 6 月 5 日，ID 为「device123」的设备记录的温度为 38.2°C，湿度为 75%。

![image.png](https://assets.emqx.com/images/a5c545fad2e17ff7fed1d99b815c66fe.png)

如需完整演示，请观看此视频：

<video src="https://assets.emqx.com/data/video/EMQX_LLM_DEMO.mp4" controls style="max-width: 100%;">
  Your browser does not support the video tag.
</video>

## 突破数据处理边界：高级 AI 功能

EMQX 5.10.0 中的大模型集成超越了简单的数据汇总，您可以实现以下高级功能：

- 对传入数据流**进行分类。**
- 基于复杂模式识别**生成告警。**
- 从非结构化传感器日志中**提取结构化信息。**
- 根据历史数据模式**提供上下文建议。**
- **将技术数据转化**为业务友好的分析见解。

## 性能优化建议

调用大模型处理数据需要一定时间，整个过程大概有几秒到十几秒，具体取决于模型的响应速度。因此，大模型处理节点并不适用于高消息吞吐量（TPS）的场景。

为了获得最佳性能：

- 选择性地将大模型处理应用于高价值数据。
- 使用数据过滤仅处理相关消息。
- 考虑在边缘端聚合多个数据点或消息，然后将它们作为单个 MQTT 消息发送到 broker。
- 持续监控处理时间并进行相应调整

## 拓展能力边界

EMQX 5.10.0 中的大模型集成仅仅是我们 AI 征程的起点。我们正在开发更多 AI 功能，包括：

- 支持更多大模型供应商。
- 用于语义搜索的向量嵌入生成。
- 与主流 AI 框架集成。
- 增强提示词模板和优化工具。

## 实时智能：EMQX 的未来

EMQX 与大模型的深度融合，正在重新定义物联网开发的边界。这不仅是一次简单的功能升级，而是一场从底层改变物联网应用开发方式的革命性突破。

我们为开发者打造了直观易用的低代码交互界面，让生成式 AI 的能力可以无缝融入数据流转的每个环节。打造具备真正智能、即时响应和自主决策能力的物联网系统变得前所未有的简单。

准备好利用人工智能激活您的物联网数据了吗？

- 即刻[下载 EMQX 5.10.0 ](https://www.emqx.com/zh/downloads-and-install/enterprise)开启智能数据处理之旅。
- 深度解析「[基于 LLM 的数据处理](https://docs.emqx.com/zh/emqx/latest/flow-designer/llm-based-data-processing.html)」技术文档。
- 根据 [OpenAI](https://docs.emqx.com/zh/emqx/latest/flow-designer/openai-node-quick-start.html) 与 [Anthropic](https://docs.emqx.com/zh/emqx/latest/flow-designer/anthropic-node-quick-start.html) 实战指南，轻松上手。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
