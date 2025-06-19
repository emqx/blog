如果您一直在期待构建更智能、更灵活的 MQTT 数据管道，EMQX 5.10.0 将满足您的需求。

本次更新引入了基于大模型的消息处理功能、自然语言 SQL 规则生成功能以及全新 NATS 协议网关。同时，新增对 Apache Doris 和 Amazon S3 Tables 的数据集成支持。

无论您需要整合 AI 能力、实现跨协议连接或构建实时分析数据流，本次更新都通过切实改进帮助您显著提升工作效率。

## **Flow 设计器支持基于大模型的 MQTT 数据处理**

Flow 设计器现已支持 LLM 集成，让您可以使用 OpenAI 和 Anthropic Claude 等 AI 模型处理 MQTT 消息。通过此更新，您可以创建智能化的低代码工作流，使用自然语言指令来响应传入的 MQTT 数据。

### **核心优势：**

- **实时 AI 增强：**实时动态处理 MQTT 消息，例如：通过上下文感知自动分类传感器数据。
- **无代码 AI 管道：**在 Flow 设计器的可视化 UI 中轻松配置大模型节点。这些节点使用 EMQX 的 `ai_completion` 功能调用外部大模型 API。
- **灵活的提供商支持：**灵活接入不同的 AI 服务商，自定义提示词与 API 密钥和设置。
- **智能物联网场景优化：**与第三方引擎或逻辑相结合，实现预测性维护、异常检测或便于理解的摘要等应用场景，无需编写代码或 SQL。

### **应用示例：**

在智慧城市部署中，传感器数据通过大模型节点可生成可读的告警信息，例如：“市中心空气质量中等，PM2.5 浓度升高。”，这将助力决策者实现快速响应。

**更多信息：**

- [基于 LLM 的数据处理概述](https://docs.emqx.com/zh/emqx/latest/flow-designer/llm-based-data-processing.html)
- [使用 OpenAI 节点创建 Flow](https://docs.emqx.com/zh/emqx/latest/flow-designer/openai-node-quick-start.html)
- [使用 Anthropic 节点创建 Flow](https://docs.emqx.com/zh/emqx/latest/flow-designer/anthropic-node-quick-start.html)

## **规则引擎支持自然语言编写**

EMQX Dashboard 中新增 AI SQL 生成器，允许用户以通俗易懂的语言描述业务逻辑，EMQX 会将其转换为规则引擎可立即使用的 SQL 语句，让用户编写 SQL 规则变得更容易。

### **核心优势：**

- **自然语言到 SQL**
  输入：“温度 > 80 时发出警报”
  输出：有效的 SQL 规则语法。
- **更快的规则创建**
  加快规则配置并降低新用户的技术门槛。

### **应用示例：**

1. **任务描述：**
   技术人员输入：「如果主题 `factory/+/status` 下任何设备发出的消息包含温度超过 90 度且振动级别超过 5 度的内容，则触发警报」。

2. **相关主题：**指定主题示例，例如 `factory/machine-42/status`

3. **输入示例（MQTT Payload）：**提供示例 MQTT 消息 Payload，以帮助 AI 理解您的数据结构。

   ```sql
   {   
     "device_id": "machine-42",   
     "temperature": 95.6,   
     "vibration": 6.2,   
     "status": "running",   
     "timestamp": "2025-06-12T08:15:30Z" 
   }
   ```

1. **输出示例（可选）：**指定预期结果格式。例如：

   ```
   {  
     "device_id": "machine-42",  
     "alert": "Temperature and vibration thresholds exceeded",  
     "temperature": 95.6,  
     "vibration": 6.2,  
     "timestamp": "2025-06-12T08:15:30Z"  
   }
   ```

   **注意：**此输出是 EMQX 使用规则动作中的模板生成的告警消息示例。它不是 SQL 查询的原始结果，而是满足规则条件时发送的通知或警报的预期格式。

1. **AI SQL 生成器返回以下 SQL 规则：**

   ```
   SELECT *, payload.temperature, payload.vibration FROM "factory/+/status" WHERE payload.temperature > 90 AND payload.vibration > 5
   ```

    参阅 [AI SQL 生成器](https://docs.emqx.com/zh/emqx/latest/data-integration/rule-get-started.html#sql-生成器)了解更多信息。

## **全新数据集成：Apache Doris 与 Amazon S3 Tables**

5.10.0 版本引入了两个新的数据集成，用于高性能分析和经济高效的 MQTT 数据长期存储。

### **将 MQTT 数据传输到 Apache Doris 进行实时分析**

EMQX 现已原生集成高速分析型数据库 Apache Doris。通过规则引擎，MQTT 消息按主题匹配、处理并映射到结构化 SQL 模板后，将通过 HTTP 或 JDBC 写入 Doris。

您可以使用标准 SQL 实时查询您的 IoT 数据，并使用 Grafana 等 BI 工具构建实时仪表看板。

[Apache Doris 集成指南](https://docs.emqx.com/zh/emqx/latest/data-integration/apache-doris.html)

### **使用 Iceberg 格式将 MQTT 数据存储在 Amazon S3 Tables 中**

新版本 EMQX 还支持 Amazon S3 Tables，使用 Apache Iceberg 格式进行大规模数据存储和分析。

此集成将 MQTT 数据转换为 Iceberg 格式的表格，并将其直接传输到 S3。它消除了对传统数据库的需求，同时保留了类似 SQL 的查询功能。

将 MQTT 数据转换为 Apache Iceberg 格式的表格，并流式传输到 S3，在保留类似 SQL 查询能力的同时，消除了对传统数据库的需求。

存储后，用户可通过 Amazon Athena、EMR、Redshift Spectrum 或 Trino、Presto 和 Snowflake 等第三方工具查询数据。

[Amazon S3 表集成指南](https://docs.emqx.com/zh/emqx/latest/data-integration/s3-tables.html)

## **全新协议网关桥接 MQTT 和 NATS**

EMQX 现原生支持轻量级高性能消息协议 NATS，实现微服务与云原生场景的跨协议通信。

### **核心优势：**

- **MQTT - NATS 桥接**
  通过 topic - subject 映射进行双向数据交换。
- **跨协议通信**
  NATS 客户端发布的消息被转换为 MQTT 发布，反之亦然，包括对通配符、队列组和请求/回复模式的支持。
- **简单配置**
  支持通过 Dashboard、REST API 或配置文件进行配置。

[NATS 协议网关文档](https://docs.emqx.com/zh/emqx/latest/gateway/nats.html)

## **使用命名空间事件主题简化规则创建**

EMQX 5.10.0 为客户端事件（例如：客户端连接、断开连接）引入了命名空间事件主题，从而可以通过通配符支持更轻松地创建规则。

以前，用户必须明确列出每个事件主题：

```sql
SELECT * FROM "$events/client_connected", "$events/client_disconnected" WHERE clientid = 'c123'
```

现在，事件遵循如下结构化格式 `$events/client/connected`，从而允许简化查询：

```sql
SELECT * FROM "$events/client/+" WHERE clientid = 'c123' 
```

这使得使用单个通配符模式匹配多个相关事件（例如，所有客户端事件）变得更加容易。

请参阅[事件主题列表](https://docs.emqx.com/zh/emqx/latest/data-integration/rule-sql-events-and-fields.html#客户端事件)以了解支持的客户端事件主题以及旧事件主题与新（命名空间）事件主题之间的映射。

## **MQTT 会话持久化的可观测性改进**

引入了 API 级别的指标接口，增强了以下方面的可观测性与监控能力：

- **Raft 复制与快照状态**：监控持久化存储中 Raft 协议的日志复制进度、快照生成情况等核心状态信息。
- **分片分布与性能指标**：支持查看会话数据在集群节点间的分布情况及各分片的处理性能。
- **故障诊断**：例如，可通过监测复制延迟或不稳定行为，识别潜在故障节点或性能瓶颈。

## **安全性、性能和用户体验方面的其他改进**

### **使用基于 LDAP 的规则简化访问控制**

LDAP 认证器现在支持在客户端认证期间动态检索 ACL 规则。MQTT 主题级权限可以定义为 LDAP 架构中的属性，并按会话进行缓存。这项更新统一了认证和授权流程。

参阅[从 LDAP 获取 ACL 规则](https://docs.emqx.com/zh/emqx/latest/access-control/authn/ldap.html#从-ldap-获取-acl-规则)了解更多信息。

### 命名空间列表中的「Created At」选项

Dashboard 现在可显示每个命名空间的创建时间戳，从而可以在多租户环境中更轻松地进行管理和操作跟踪。

### Kafka 连接器：AWS IAM 身份验证支持

使用 IAM 角色实现对 Amazon MSK 的安全访问，简化凭证管理。

### 通过静态发现改进集群（[#15304](https://github.com/emqx/emqx/pull/15304)

EMQX 5.10.0 修复了使用 `static` 发现策略的集群中，影响副本节点发现的问题。之前，副本节点可能会忽略 `static_seeds` 列表中未明确列出的核心节点，这可能导致集群视图不一致和负载不均衡。

通过此修复，复制器现在可以正确识别所有核心节点，确保在静态模式部署中实现更一致的集群和更均衡的资源使用。

此版本还包含多项性能改进和错误修复。完整变更列表，请参阅 [EMQX 企业版发布历史](https://docs.emqx.com/zh/emqx/latest/changes/changes-ee-v5.html#_5-10-0)。

## **开启 EMQX 5.10.0 探索之旅**

[立即下载 EMQX 5.10.0](https://www.emqx.com/zh/try?tab=self-managed) 并开始构建智能、可扩展且安全的物联网解决方案。无论您是扩展多租户平台、实现实时数据处理，还是保障关键任务部署的安全性，这一版本都能为您提供强大支持。

需要帮助或想了解 EMQX 如何适合您的 IoT 用例？请联系[我们的团队](https://www.emqx.com/zh/contact)进行个性化咨询。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
