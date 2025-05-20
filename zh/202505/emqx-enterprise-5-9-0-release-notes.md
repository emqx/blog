我们高兴地宣布 EMQX Enterprise 5.9.0 正式发布，这是我们致力于提供全球最可扩展和可靠的 MQTT 消息平台的重要里程碑。本次更新变更了许可证模式，旨在持续驱动创新并为用户提供更优质的支持。

> 有关新许可证的详细信息，请参阅[此博客](https://www.emqx.com/zh/blog/adopting-business-source-license-to-accelerate-mqtt-and-ai-innovation)。

与此同时，命名空间和智能数据中心等开创性功能也同步推出，助力企业构建高效、智能和安全的物联网生态系统。让我们一起来探索新功能！

### 命名空间：多租户部署更简单、更高效

全新[命名空间](https://docs.emqx.com/zh/emqx/latest/multi-tenancy/namespace.html)功能极大简化了多租户管理，允许在单个 EMQX 集群内为不同租户创建隔离的配置环境。每个命名空间可灵活设置租户专属的速率限制等参数，确保资源高效利用、数据隐私保护，同时免去部署多集群的复杂性。

**主要优势：**

- **无缝支持多租户**：在同一集群内轻松管理多个租户（如部门、客户或应用），大幅降低基础设施成本。
- **简单配置**：通过 EMQX HTTP API 或 Dashboard 创建和管理命名空间。
- **精细化控制**：支持在命名空间级别设置速率限制等策略。
- **增强可扩展性**：高效支持数千租户，完美适配智慧城市或联网车联网等场景。

例如，在一个联网车辆平台中，管理员可通过 HTTP API 为某租户（如 `tenant-a`）创建命名空间，并设置每秒 10 次连接的速率限制，确保该租户在限定资源范围内运行，同时与其他租户保持性能隔离。

### 数据智能中心：一站式智能数据处理解决方案

5.9.0 版本中的[数据智能中心](https://docs.emqx.com/zh/emqx/latest/data-integration/smart-data-hub.html)将 Schema Registry、Schema 验证和消息转换等核心数据处理功能整合为一套高效解决方案。本次更新的亮点之一是 Schema Registry 新增对外部 HTTP Schema 的支持，显著提升了 Schema 管理的灵活性。

**主要功能与升级：**

- **Schema Registry**：集中管理 Avro、Protobuf 和 JSON Schema。新推出的外部 HTTP Schema Registry 功能允许 EMQX 从外部 HTTP 服务动态获取 schema，简化与第三方系统的集成，并支持实时 schema 更新，无需改动 EMQX 集群。
- **Schema 验证**：通过对传入消息进行预定义 schema 验证，确保数据完整性，减少下游处理中的错误。
- **消息转换**：实时转换消息 payload（例如过滤、丰富或重新格式化），实现与数据库、AI/ML 平台或分析工具的无缝数据集成。

例如，在一个联网车辆平台中，数据智能中心可以根据从外部 HTTP 服务获取的 Protobuf schema 验证传感器数据，将其转换为与云分析平台兼容的格式，并提供实时洞察以优化车辆性能。这种集成使数据智能中心成为制造、物流和智能能源等行业的核心支柱。

### 备选动作：保障数据集成稳定可靠

新增的[备选动作](https://docs.emqx.com/zh/emqx/latest/data-integration/data-bridges.html#备选动作)功能确保数据集成在遇到故障时依然可靠。当消息无法传递至外部系统（例如因网络问题或服务不可用）时，备选动作支持定义备用策略，如将消息暂存至缓冲区、转发至其他 Sink 或重发布到监控主题以供后续分析，确保关键物联网数据零丢失。

以智能能源电网为例，若主数据集成至云分析平台失败，备选动作可将电表数据重定向至本地缓冲区，确保在网络恢复前数据完整保存。

### 安全性全面升级：为数据基础设施保驾护航

安全性在物联网中至关重要，EMQX Enterprise 5.9.0 推出了一系列高级安全功能，为部署提供多层次保护，兼顾精细化控制与管理便捷性。

#### 认证器调用条件

[认证器调用条件](https://docs.emqx.com/zh/emqx/latest/access-control/authn/authn.html#认证器调用条件)功能通过在认证链中引入条件逻辑，优化认证流程并减轻后端压力。EMQX 可根据客户端连接的监听器或属性动态应用不同认证器，仅在必要时调用，避免对外部系统的不必要请求。

#### 多因素认证

EMQX Enterprise 5.9.0 为 EMQX Dashboard 引入了[多因素认证（MFA）](https://docs.emqx.com/zh/emqx/latest/multi-factor-authn/multi-factor-authentication.html)。管理员和用户必须使用主凭证（密码）和次要因素（例如通过认证器应用生成的时间同步一次性密码，TOTP）进行认证。MFA 可通过 Dashboard 启用，确保对关键管理功能的安全访问。

#### 账户锁定与解锁

[账户锁定与解锁](https://docs.emqx.com/zh/emqx/latest/dashboard/introduction.html#账户锁定与解锁)功能有效防御暴力破解攻击，通过在多次登录失败后临时锁定账户实现保护。管理员可通过 Dashboard 手动解锁，或设置自动解锁时间，在安全与用户体验之间取得平衡。

#### 密码过期管理

[密码过期](https://docs.emqx.com/zh/emqx/latest/dashboard/introduction.html#密码过期)功能允许管理员强制 Dashboard 用户定期更新密码，降低长期凭证暴露的风险。系统会在密码到期前提醒用户更新，确保访问不中断。

这些安全升级使 EMQX Enterprise 5.9.0 成为业内最安全的 MQTT 平台之一，充分满足受监管行业和关键任务场景的物联网部署需求。

### 其他优化与关键修复

EMQX Enterprise 5.9.0 还包括多项性能优化、可观测性改进和关键问题修复，进一步提升平台的可靠性与易用性。

#### 节点级缓存优化外部认证与授权

通过在节点级别本地缓存[认证](https://docs.emqx.com/zh/emqx/latest/access-control/authn/authn.html#外部资源缓存)和[授权](https://docs.emqx.com/zh/emqx/latest/access-control/authz/authz.html#外部资源缓存)结果，该功能显著提升吞吐量，缩短响应时间并降低后端负载。

#### 磁盘日志 (Disk Log) 数据集成

[Disk Log 数据集成](https://docs.emqx.com/zh/emqx/latest/data-integration/disk-log.html#将-mqtt-数据写入-disk-log)功能使 EMQX 能够将事件数据持久化至磁盘，便于故障排查或历史数据分析。

#### 规则引擎的 OpenTelemetry 端到端追踪

规则引擎的 OpenTelemetry 端到端跟踪支持实现了对规则和动作的数据流的全面监控，提升了可观测性，便于调试和优化复杂的数据管道。

#### 增强 MQTT 速率限制，支持突发容量

升级后的 MQTT 速率限制功能新增突发流量支持，允许连接或消息速率的短暂激增。可通过 Dashboard 或配置文件灵活调整，确保智能计量等场景在高峰负载下稳定运行。

#### 其他重要优化与修复

- **持久会话性能提升 (**[**#14498**](https://github.com/emqx/emqx/pull/14498)**)**：优化会话管理，空闲持久会话不再占用 CPU 资源。同时修复 QoS 升级问题，确保订阅者仅接收符合其订阅 QoS 级别的消息，提升效率与交付精准性。
- **集群连接路由复制修复 (**[**#15067**](https://github.com/emqx/emqx/pull/15067)**)**：解决路由复制中的多项问题，包括配置错误导致的重连循环、关闭不存在 MQTT 客户端连接时的崩溃，以及共享订阅复制启动失败。

这些优化与修复让 EMQX Enterprise 5.9.0 更加高效、可靠且易于监控，为企业物联网部署提供了坚实的基础。更多信息，请参阅[版本发布历史](https://docs.emqx.com/zh/emqx/latest/changes/changes-ee-v5.html#_5-9-0)。

### 立即体验 EMQX Enterprise 5.9.0

EMQX Enterprise 5.9.0 现已上线[官网](https://www.emqx.com/zh/downloads-and-install/enterprise)！无论您是扩展多租户平台、实现实时数据处理，还是保障关键任务部署的安全性，这一版本都能为您提供强大支持。

立即下载 EMQX Enterprise 5.9.0，体验全新功能，探索 EMQX 如何助力您的物联网战略升级。如有疑问或需讨论具体应用场景，请随时联系我们的[销售团队](https://www.emqx.com/zh/contact)。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
