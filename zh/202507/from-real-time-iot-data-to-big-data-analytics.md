物联网技术的核心价值在于利用设备数据实现智能运营、预测性维护和突破性的 AI 应用。长期以来，运营技术（OT）的实时数据流与大数据和 IT 的分析之间存在难以逾越的鸿沟。

OT 领域依赖实时流数据运转，而 IT 领域的分析与 AI 则需要结构化、可查询的数据集。传统方式需要通过复杂、脆弱且昂贵的 ETL（提取、转换、加载）管道来实现数据互通。

随着EMQX 5.10.0 的发布，我们推出了一项突破性功能——与 Amazon S3 Tables 的原生数据集成，彻底打破这一壁垒。

![image.png](https://assets.emqx.com/images/6ffc62b8f4ae2a73c3a63c56b24fcd48.png)

<center>EMQX 数据集成 - S3 Tables</center>

## 挑战：从数据流到数据湖

将原始 MQTT 数据流式传输至标准 Amazon S3 存储桶是数据采集的常见步骤。但这些原始数据无法直接用于分析，必须经过结构化处理、模式管理，并针对 Amazon Athena、Spark、Presto 等查询引擎进行优化。传统批量处理作业不仅带来延迟和成本，更增加了系统复杂性，严重阻碍关键洞察的获取。

## 解决方案：与可分析的 S3 Tables 直接集成

基于开源引擎 Apache Iceberg 构建的 Amazon S3 Tables 通过高性能开放表格式完美解决了这一难题。

现在，EMQX 可无缝地将数据流注入 S3 Tables 中，构建起连接 MQTT 实时数据流与分析生态的强大桥梁。EMQX 不只是简单地转储原始文件，而是持续地将物联网数据流式写入结构化、高性能且立即可分析的表格中。

## EMQX 与 S3 Tables 集成的核心优势

- **OT 与 IT 无缝融合：**

  建立从联网设备到数据湖的最直接路径，实现信息流统一，让数据分析师能即时处理 OT 数据。

- **消除复杂的 ETL 管道：**

  数据从源头就以可供分析的格式写入，减少甚至彻底消除中间数据处理和转换的环节。数据架构化繁为简，运维成本显著降低，实现降本增效。

- **加速大数据和 AI 计划：**

  借助 S3 Lakehouse 中即时可用且可查询的数据，您的团队可以加速工作流程。无论是构建仪表板、运行临时分析查询，还是基于最新数据训练机器学习模型，洞察时间都将显著缩短。

- **开放架构、面向未来、极致性能：**

  S3 Tables 基于Apache Iceberg 构建，采用开放标准，彻底摆脱供应商锁定。该格式专为海量数据集的高速查询而设计，支持事务一致性和架构演化等功能，确保您的数据湖能够随业务需求灵活调整，始终保持稳定可控。

## 工作原理：简化的工作流程

![image.png](https://assets.emqx.com/images/3c5e8f1464df3c2d4c198c424e2484fa.png)

**S3 Tables Sink 作为 EMQX 数据集成引擎的核心部分，配置流程非常简单：**

1. **设备连接到 EMQX：**物联网设备通过 MQTT 连接到 EMQX 并开始发布遥测数据。
2. **选择您的数据源：**在 EMQX 仪表板中，选择您想要捕获的 MQTT 主题，例如 `telemetry/+/data`。
3. **数据转换：**EMQX 规则引擎可以对消息 payloads 进行过滤、转换或增强，使其完美适配目标 Iceberg 表的结构。
4. **创建 S3 Tables Sink：**向您的数据规则添加一个新的接收器并选择「Amazon S3 Tables」。
5. **配置和连接：**提供您的 AWS 凭证，指定 S3 Tables ARN、命名空间和表名。EMQX 通过 Iceberg REST 端点管理元数据，高效缓冲消息并以 Iceberg 格式写入 S3 Tables。

提交后，您的数据可立即供任何兼容 Iceberg 的服务进行查询和分析。

## 未来基础

EMQX 与 Amazon S3 Tables 的深度集成是构建现代实时数据策略的基础。它通过统一实时数据和分析数据，帮助企业最终释放其物联网数据的全部潜力。

**准备好构建从 OT 到 AI 的桥梁了吗？**

- 立即下载 [**EMQX Enterprise 5.10.0**](https://www.emqx.com/zh/downloads-and-install/enterprise)**。**
- **查看**[ **S3 Tables 集成文档**](https://docs.emqx.com/zh/emqx/latest/data-integration/s3-tables.html)中的分步教程。
- [**联系我们的团队**](https://www.emqx.com/zh/contact?product=emqx)进行个性化演示。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
