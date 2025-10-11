**EMQX 6.0 是继 5.x 系列之后，首个具有里程碑意义的重大更新。**该版本首次将 MQTT 消息通信与消息队列能力结合，重新定义了物联网数据流处理。这一里程碑版本引入了多项变革性功能，例如：支持持久化、异步消息传输的消息队列功能、支持多租户安全隔离的命名空间角色管理，以及与 AWS AlloyDB 和 BigQuery 等数据库的无缝集成。

EMQX 6.0 专为动态环境构建，为智慧城市、工业物联网和车联网提供强大支撑，将复杂挑战转化为可扩展、高可用的解决方案。让我们一起探索塑造未来万物互联系统的创新技术。

## **消息队列：**实现更可靠的 MQTT 消息传输

**EMQX 6.0 通过原生的消息队列功能，重新定义了 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)通信方式，将实时发布/订阅模式与持久化、异步的消息传递机制无缝融合，为物联网场景提供更强大的可靠性与灵活性。**

该功能在服务端引入缓冲区，用于捕获符合指定主题过滤器的消息，即使在订阅客户端离线时也能持续保存。客户端可以通过订阅特殊的 `$q/{TopicFilter}` 主题格式来消费这些离线期间积累的消息，从而在动态多变的物联网环境中确保数据可靠送达。

### 为什么这很重要？

传统 MQTT 通信依赖订阅者在线接收消息，而消息队列机制则实现了发布者与订阅者的解耦，同时支持实时与异步消息传输。该功能还支持消息持久化存储、可配置的保留周期（如 TTL）以及 QoS 1 等级的传输保障。通过在 EMQX 平台中集成 MQTT 与异步消息队列能力，用户无需额外部署外部消息队列系统，从而简化了物联网架构的设计与运维。

### **核心优势：**

- **统一 MQTT 与消息队列**：将 MQTT 轻量级发布/订阅架构与企业级消息队列功能结合，无需额外部署 RabbitMQ 或 Kafka 等外部系统。
- **可选的最后值语义（last-value semantics）**：可按队列键属性（如：设备 ID）保留每个主题的最新消息，特别适用于传感器读数、设备配置等快速变化状态的追踪场景。
- **灵活的消息分发机制**：提供可配置的消息分发策略（如：随机、轮询、最少未确认优先），在多客户端场景下实现消息分发优化。
- **投递保障**：确保订阅者断开连接或网络中断时数据零丢失，完美适配物联网部署中不稳定的网络环境。

### **典型应用场景：**

在智能农业系统中，发布到 `farm/+/sensors` 的土壤传感器数据被存储在消息队列中。监控应用程序订阅 `$q/farm/+/sensors` 以检索所有读数，包括离线期间的数据。启用「最后值语义」后，每个设备仅保留最新的传感器数据，从而简化灌溉决策的数据处理。

了解更多信息，请参阅[**消息队列**](https://docs.emqx.com/zh/emqx/latest/message-queue/message-queue-concept.html)**。**

## **命名空间角色：**多租户管理的新突破

**EMQX 6.0 通过在 Dashboard 中引入命名空间角色功能，将多租户管理提升到了一个新的水平。**

该功能增强了基于角色的访问控制（RBAC），可将用户权限限定在特定命名空间内，使用户仅能访问与其职责相关的资源，从而更高效地管理大规模物联网场景下的多租户部署。

命名空间角色使管理员能够高效地管理多个租户，每个租户都在一个独立的资源空间中运行。用户登录后会直接进入已过滤的 Dashboard 概览页面，仅能看到自己命名空间下的规则、连接器等资源，实现真正的租户隔离。

### **核心优势：**

- **安全隔离**：命名空间角色将用户限制在其分配的命名空间内（例如`ns:team_a::administrator`），确保跨团队、业务部门或客户等租户的数据和资源隔离。
- **精细化权限控制**：管理员可对特定命名空间下的资源（如连接器、规则）拥有完整管理权限；而对于集群级配置，命名空间用户则仅具备只读权限，仅全局管理员可修改，保障系统核心配置的安全性。
- **高效运维**：通过 Dashboard、API 或 CLI 添加用户时，可以快速创建并分配命名空间角色（管理员或查看者），显著降低运维复杂度。
- **企业级服务**：适用于需要为多个客户、团队或部门提供隔离服务的服务提供商或企业用户，提供安全、云原生、可扩展的物联网解决方案。

### **典型应用场景：**

某一车联网平台提供 MQTT 即服务，其内部车队运营与设备维护团队作为独立租户运行。

- 车队运营人员拥有 `ns:fleet_ops::administrator` 角色，可在命名空间 `ns:fleet_ops` 中管理以 `sensors/data` 为主题的 MQTT 消息，用于公交实时追踪。
- 维护人员则在 `ns:maintenance` 命名空间内，使用结构相同的 MQTT 主题 `sensors/data` 接收传感器数据，用于设备诊断，二者互不干扰。

管理员还可为不同租户设置资源配额（如消息吞吐量），确保资源公平分配，防止单一团队过度占用系统资源。

具体命名空间角色创建方法，请参阅 [*创建命名空间角色*](https://docs.emqx.com/zh/emqx/latest/dashboard/system.html#命名空间角色)。

## **优化持久化存储，全面提升性能**

**EMQX 6.0 通过将会话数据与 broker 的其他元数据解耦，显著优化了持久化存储机制。**

这一改进大幅降低了内存占用，并有效提升了存储效率，对大规模物联网部署至关重要。

以智能电网为例：当数以百万计的电表读数需要持久化存储时，优化后的存储机制能够有效降低内存消耗，使得集群无需扩展硬件即可接入并处理更多设备数据。

### **关键改进：**

- **内存占用降低**：通过新的配置参数优化了 RocksDB 内存使用。
  - `durable_storage.messages.rocksdb.write_buffer_size`：控制每个分片的 memtable 大小。
  - `durable_storage.messages.rocksdb.cache_size`：设置每个分片的块缓存大小。
  - `durable_storage.messages.rocksdb.max_open_files`：限制每个分片的文件描述符数量。
  - `durable_storage.messages.layout.wildcard_thresholds`：为 `wildcard_optimized_v2` 布局调整通配符优化。
- **全新序列化方案**：默认序列化格式升级为 asn1，实现更高效的消息存储。
- **性能显著提升**：存储效率的改进确保了更快的消息检索速度和更低的资源消耗。

## **全新增强的数据集成能力**

EMQX 6.0 进一步扩展了数据集成能力，新增支持 [AWS AlloyDB](https://docs.emqx.com/zh/emqx/latest/data-integration/alloydb.html)、[CockroachDB](https://docs.emqx.com/zh/emqx/latest/data-integration/cockroachdb.html)、[AWS Redshift](https://docs.emqx.com/zh/emqx/latest/data-integration/redshift.html) 以及 [BigQuery](https://docs.emqx.com/zh/emqx/latest/data-integration/bigquery.html) 四大数据平台，并对 Snowflake、RocketMQ、S3 Tables 和 RabbitMQ 等现有集成进行了全面增强。

### **新增集成支持**

- **AWS AlloyDB、CockroachDB 与 Redshift**：将 MQTT 实时数据流传输到这些高性能数据库，既满足实时分析需求，又提供可扩展的存储方案，特别适合企业级物联网分析场景。
- **Google BigQuery**：将 MQTT 数据与 BigQuery 的无缝集成，实现大规模数据仓库和高级查询能力，从海量的物联网数据集中挖掘深层价值。

### 集成功能增强

- **Snowflake Snowpipe 流式接入**：新增对 Snowpipe 流式接入功能（preview 功能，限 AWS 托管的 Snowflake 账户）的支持，可低延迟的将数据传输到 Snowflake tables。
- **RocketMQ 动作配置**：新增 Key 和 Tag 模板字段，结合用于生产策略的 `key_dispatch` 选项，提供更灵活的消息元数据自定义能力。
- **S3 Tables 连接器**：现在可以自由选择 `access_key_id` 与 `secret_access_key` 配置，允许通过 EC2 Instance Metadata Service v2 APIs 自动获取凭证，实现与 AWS 环境的无缝集成。
- **RabbitMQ 数据输出**：支持自定义消息头与属性模板，有效增强 RabbitMQ 内部的消息路由能力与系统兼容性。

## **基于 LLM 的高级 MQTT 数据处理**

继 5.10.0 版本引入 AI 能力后，EMQX 6.0 进一步增强了基于 LLM 的数据处理功能，新增支持 Google Gemini 模型，并持续兼容 OpenAI 与 Anthropic Claude。全新打造的 API 和配置选项使 AI 集成更稳健且可定制。

### **关键改进**

- **Google Gemini 支持**：借助 Gemini 的高级推理能力构建智能数据流，分析结构化的 MQTT 负载、检测多字段复杂状态，并生成精准、上下文感知的告警。
- **新增 API 端点**：通过专用 API 获取 AI 服务商所有可用模型，简化了集成与模型选择。
- **传输配置优化**：支持配置 AI Completion Providers 的连接超时与最大连接数参数，有效提升系统性能与可靠性。

在 Flow 设计器中通过[全新的 Gemini 节点](https://docs.emqx.com/zh/emqx/latest/flow-designer/gemini-node-quick-start.html)，探索基于大语言模型的数据处理实践。

## **其他重要升级**

**EMQX 6.0 还包括许多其他改进和错误修复，以增强性能、安全性和可用性。**

**许可证 TPS 限制**：新增对企业版许可证的每秒事务处理量（TPS）限制，可设定集群处理 MQTT 消息处理总量的上限。超出限制时将触发可观测性告警，但不会阻断消息流。该告警将持续存在，直至应用更高 TPS 规格的许可证或通过 Dashboard 或 CLI 手动清除。

**安全能力增强**：引入客户端重连频率限制机制，防止因频繁重连导致系统不稳定；支持通过认证结果动态覆盖客户端 ID，实现灵活管控；在 LDAP 认证中集成 ACL 规则，有效减少服务端查询次数；默认授权流操作由 `allow` 更改为 `deny`，进一步增强安全性。

**部署运维优化**：新增 EMQX Operator 与 Helm Charts 部署文档；支持 Debian 13 系统包（停止支持 Debian 10）；引入跟踪日志自动轮换机制；新增「强制解除告警」API，增强运维管控能力。

**性能显著提升**：针对一对多消息推送/分发场景进行专项优化，实现更快速的消息处理；降低授权流程中的内存占用，为大规模部署提供更高效率。

**完整的更新日志将详细介绍增强的可观测性、集群改进和重要的错误修复。**

欢迎查看 [EMQX 6.0 Release Notes](https://www.emqx.com/zh/changelogs/enterprise/6.0.0) 获取完整列表。

## **欢迎体验全新 EMQX 6.0**

从官方网站下载 EMQX Enterprise 6.0，解锁持久化消息传输、AI 驱动的洞察和多租户 IoT 解决方案的强大能力，构建更智能、更可扩展、更安全的数据管道。

需要帮助或想探索 EMQX 6.0 如何适用于您的 IoT 用例？请联系我们的团队进行个性化咨询。



<section class="promotion">
    <div>
        免费试用 EMQX Enterprise
    </div>
    <a href="https://www.emqx.com/zh/try?tab=self-managed" class="button is-gradient">开始试用 →</a>
</section>
