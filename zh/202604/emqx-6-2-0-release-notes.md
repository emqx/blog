EMQX 6.2 现已正式发布！

新版本在 MQTT 之上原生支持 A2A 协议，让 AI 智能体无需任何额外基础设施，即可直接通过 Broker 完成注册、发现和协作。

与此同时，EMQX 6.2 在 MQTT 5.0 发布/订阅模型的基础上，增加了订阅层面的消息过滤能力；新增动态 Keep Alive 管理能力，专为大规模设备集群设计；新增与 Azure Event Grid 和 QuasarDB 的数据集成；通过工作负载身份联合（Workload Identity Federation）进一步强化了 GCP 连接器的安全性。

无论您是在构建分布式 AI 系统、运营大规模物联网设备集群，还是在工业数据管道中推行数据质量标准化，EMQX 6.2 都能提供企业级规模运行所需的协调、治理与运维管控能力。

## 基于 MQTT 的 A2A 协议：实时智能体发现与协作

本次版本的核心特性是 A2A 注册表（Registry），这是一套直接内置于 MQTT Broker 的标准化智能体发现系统。

标准的 A2A 协议以 HTTP 作为传输层，在云端环境中运行良好，却难以适配资源受限的边缘设备，而这恰恰是 MQTT 的强项。EMQX 6.2 引入了 **A2A over MQTT**，一种 Broker 中立的传输扩展方案，无需额外基础设施，即可将符合 A2A 规范的智能体发现与协作能力延伸至边缘场景。

智能体将结构化 Agent Card 作为保留消息发布到标准发现主题`$a2a/v1/discovery/{org_id}/{unit_id}/{agent_id}` 来完成注册。订阅者连接后立刻获取全量已注册节点信息，并在智能体上下线时实时收到更新。无需轮询，也无需独立的注册服务。

### **核心功能**

- **事件驱动的发现机制**：智能体发布一次 Agent Card 就立即可被发现，上下线变化实时推送。
- **内置在线状态感知**：EMQX 在发现消息中附加 `a2a-status` 用户属性（`online`、`offline`、`lwt`），将发现与存活检测整合到单一的订阅流中。
- **灵活的交互模式**：智能体通过 MQTT v5 的响应主题（Response Topic）和关联数据（Correlation Data）属性进行通信，支持请求/响应、流式响应、多轮对话、负载均衡池调度以及智能体实例间的任务移交。
- **Schema 校验**：Agent Card 在注册时可依据 A2A 规范进行校验，不合规的 Agent Card 在进入注册表前即被拒绝。
- **Dashboard 界面与 CLI**：运维人员可通过 EMQX Dashboard 或 `emqx ctl a2a-registry` 命令管理 Agent Card。
- **机器可读的 API 规范**：新增 `/api-spec.md` 和 `/api-spec.html` 端点，对外暴露 EMQX HTTP API 的精简视图，Claude Code、Codex 等工具可直接调用这些端点与 EMQX 交互。

A2A Registry 遵循不断演进中的 A2A 协议规范，并将作为即将推出的各类基于 Agent 的产品的底层基础——其中就包括 EMQ 的 Device Agent，目前该产品已开放早期体验。

### **典型场景**

在某工厂自动化系统中，边缘网关上的监控智能体检测到 7 号电机生产线出现异常振动。

监控智能体通过订阅 `$a2a/v1/discovery/com.example/factory-a/+` 发现了一个维修智能体，收到 Broker 推送的 Agent Card 后发起任务请求。维修智能体流式推送状态更新——「正在分析振动特征」、「检测到轴承磨损」；监控智能体据此触发维修工单。整个协作过程中，两个智能体互不知晓对方的网络地址，EMQX 的认证与授权对所有智能体通信统一生效。

了解更多关于 [A2A over MQTT](https://docs.emqx.com/zh/emqx/latest/emqx-ai/a2a-over-mqtt/overview.html) 的内容。

## 订阅层面的消息过滤

当 EMQX 启用 `mqtt.subscription_message_filter` 后，客户端可在订阅时附加 `?` 查询后缀，让 Broker 在消息投递前完成过滤。例如：

```
sensor/+/temperature?location=roomA&value>25
```

EMQX 会根据每条入站消息的 MQTT 5.0 用户属性对表达式进行求值，仅投递匹配的消息。被过滤器丢弃的消息将记录在新的 `delivery.dropped.filter` 指标下。

**核心优势：**

- **节省带宽**：过滤在 Broker 侧执行，只有匹配的消息才会下发，受限网络路径上的带宽消耗显著降低。
- **降低客户端负载**：消费端应用只需处理其需要的数据，无需自行编写过滤逻辑。
- **高吞吐场景增益明显**：当单个通配符订阅覆盖了高消息量的 Topic 空间，而消费端只需其中一小部分消息时，效果尤为突出。

了解更多关于[消息过滤](https://docs.emqx.com/zh/emqx/latest/subscription-filter/subscription-filter-concept.html)的内容。

## 无中断动态设备管理

EMQX 6.2 新增了在运行时动态调整客户端 Keep Alive 间隔，无需断开重连。

客户端可通过向 `$SETOPTS/mqtt/keepalive` 发布消息来更新自身的 Keep Alive 设置；后端系统则可通过 `$SETOPTS/mqtt/keepalive-bulk` 批量更新设备集群，多个会话应用可以同步变更。

**典型场景：**

某电动汽车制造商管理着逾 10 万辆联网车辆。

车辆进入低功耗停车状态时，通过 `$SETOPTS/mqtt/keepalive-bulk` 延长 Keep Alive 间隔，降低空闲网络流量和电池消耗；车辆重新点火后，原始间隔自动恢复——全程无需重连，会话不中断，在途消息不受影响。

了解更多关于[动态 Keep Alive 调整](https://docs.emqx.com/zh/emqx/latest/configuration/mqtt.html#动态-keep-alive-调整)的内容。

## 新增与增强的数据集成

EMQX 6.2 新增两个集成目标，并增强了现有 GCP 连接器的安全性。

### 新增集成

[**Azure Event Grid**](https://docs.emqx.com/zh/emqx/latest/data-integration/azure-event-grid.html)：实现 EMQX 与 Azure 全托管事件路由服务之间的双向 MQTT 桥接。EMQX 以 MQTT 客户端身份接入，通过 TLS 和客户端证书认证建立连接，支持 Sink 与 Source 双向数据流。数据进入 Azure Event Grid 后，可自然流转至 Azure Functions、Event Hubs、Storage 等 Azure 服务。

[**QuasarDB**](https://docs.emqx.com/zh/emqx/latest/data-integration/quasardb.html)：将 MQTT 数据直接写入 QuasarDB——一款高性能列式时序数据库。消息经由规则引擎通过 ODBC 批量写入 QuasarDB，非常适合需要在大时间窗口上进行快速范围查询的高频工业遥测场景。

### 集成增强

[**GCP 工作负载身份联合（Workload Identity Federation）**](https://docs.emqx.com/zh/emqx/latest/data-integration/data-bridge-gcp-pubsub.html#配置工作负载身份联合)：GCP 连接器（Pub/Sub 生产者、Pub/Sub 消费者、BigQuery）现已支持通过服务账户模拟（Service Account Impersonation）进行 WIF 认证。

EMQX 从外部身份提供商（如 Azure Entra ID）获取短效 OIDC 令牌，换取临时 GCP 凭证，彻底消除了长期服务账户密钥文件的存储与轮换负担。

## NATS 网关：补齐完整认证能力

EMQX 的 NATS 网关允许 NATS 客户端连接到 EMQX，并与 MQTT 双向互通消息。在 6.2 版本中，该网关新增了 Token、NKey 和 JWT 三种内部认证方式，填补了与原生 NATS Server 之间的主要能力差距。

**新增认证方式：**

- **Token 认证**：基于共享密钥的轻量认证，适用于开发环境或简单部署场景。
- **NKey 认证**：基于 Ed25519 密钥对的加密身份认证，是 NATS 生产环境的标准机制。
- **JWT 认证**：完整的 NATS JWT 凭证链校验，支持运营商/账户/用户的层级体系。

将 NATS 工作负载迁移至 EMQX 的团队无需修改任何客户端侧认证配置，NATS 客户端对 EMQX 的认证体验与面对原生 NATS Server 完全一致。

了解更多关于配置 [NATS 网关内部认证](https://docs.emqx.com/zh/emqx/latest/gateway/nats.html#配置网关内部认证-internal-authn)的内容。

## 统一命名空间治理：在 ACL 检查阶段强制规范主题结构

EMQX 6.2 引入了 UNS 治理插件 `emqx_unsgov`，在 ACL 检查阶段强制执行统一命名空间（UNS）主题结构，并可在发布处理环节进行可选的 Payload Schema 校验。

在大规模物联网部署中，随着团队扩张和固件迭代，Topic 结构往往会发生漂移。缺乏 Broker 级别的强制管控，格式有误的数据就会静默地流入管道，直到被下游系统发现才能察觉。UNS 治理采用快速失败（fail-fast）策略：不合规的发布在源头即被拦截，确保下游系统的数据清洁。

插件以模型为核心：每个模型是一份 JSON 文档，定义主题树结构、可变段的约束条件以及各端点节点的可选 Payload Schema。

主题与激活的模型在 ACL 检查阶段进行匹配；若匹配失败，对 QoS 1/2 消息返回 `Not Authorized`，对 QoS 0 消息静默丢弃。

Payload 校验在发布处理环节单独执行，不合规的 Payload 直接丢弃，不触发认证拒绝。如果没有任何模型处于启用状态，所有未豁免的主题默认拒绝（fail-closed）。

### **典型场景**

某制造业运营商定义了一个模型，要求有效主题遵循 `default/{site_id}/Lines/{line_id}/LineControl` 格式，`site_id` 和 `line_id` 须匹配正则约束，`LineControl` 端点要求 Payload 包含 `Status` 和 `Mode` 字段。

某设备向格式错误主题发布消息，在 ACL 检查时将直接收到 `Not Authorized`；向合法主题发布消息但 Payload 不合规，消息在发布处理环节将被丢弃。无论哪种情况，违规信息都会立即出现在 `recent_drops` 中，在不合规数据到达任何下游系统之前就将其拦截。

了解更多关于 [UNS 治理](https://docs.emqx.com/zh/emqx/latest/extensions/plugin-catalog/emqx-unsgov.html#uns-governance)的内容。

## 其他增强与修复

### 性能优化

- 认证/授权的节点级缓存现已默认开启，大幅减少回访客户端的重复后端查询，提升典型部署场景下的认证性能。
- Kafka Source 轮询现在会短暂等待新数据后再返回，提高消费者响应速度，同时减少不必要的轮询开销。

### 数据集成

- 规则引擎中的 jq 库升级至 1.8.1，带来更好的标准兼容性。此次升级引入了若干细微的行为变更，如果您的规则中使用了 jq 表达式，请在升级前仔细阅读不兼容变更说明。
- GreptimeDB 和 EMQX Tables 现在会自动将裸整数值转换为 float64，避免目标列类型为浮点数时写入失败。
- MQTT 入站桥接现已支持使用 `$queue/{name}/{bind-filter}` 格式从远端消息队列消费数据。

### 访问控制与管理

- **认证/授权指标重置 API**：新增 `POST /authentication/:id/metrics/reset` 和 `POST /authorization/sources/:type/metrics/reset` 端点，支持按需清除统计计数。
- **SSO OIDC 支持 jq 表达式**：OIDC SSO 后端现支持通过 jq 表达式提取角色和命名空间值，用于自动创建 Dashboard 用户。
- **API Key 命令行管理**：`emqx ctl api_keys` 现已支持从命令行执行 `list`、`show`、`add`、`delete`、`enable` 和 `disable` 操作。

完整变更内容请参阅 [Release Notes](https://docs.emqx.com/zh/emqx/latest/changes/changes-ee-v6.html#_6-2-0)。

## 开始体验 EMQX 6.2

立即下载 [EMQX 6.2](https://www.emqx.com/zh/downloads-and-install/enterprise)，探索全新特性。

升级前，请务必查阅 [6.2.0 不兼容变更说明](https://docs.emqx.com/zh/emqx/latest/changes/breaking-changes-6.2.html#emqx-6-2-中的不兼容变更)。

> 如果您的规则中使用了 jq 表达式，jq 1.8.1 的行为变更需要特别关注。

如有任何问题，或希望进一步了解适合您的使用方案，欢迎联系我们的[销售团队](https://www.emqx.com/zh/contact)。
