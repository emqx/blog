[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.4.0 版本现已正式发布！

新版本提供 OpenTelemetry 分布式追踪与日志集成功能，新增了开放充电协议 OCPP 协议接入能力，并为数据集成添加了 Confluent 支持。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## OpenTelemetry 分布式追踪与日志集成

在 EMQX v5.2.0 中，EMQX 提供了 [OpenTelemetry](https://opentelemetry.io/) 指标（Metrics）的集成，本次发布中，EMQX 进一步提供了分布式追踪（Traces）与日志（Logs）的集成，完全实现了 OpenTelemetry 可观测性框架所需的功能。

![OpenTelemetry 分布式追踪与日志集成](https://assets.emqx.com/images/299ed61d334cdeae406f70958114ede8.png)

 

### 分布式追踪（Traces）

OpenTelemetry 分布式追踪是一个用于追踪请求在分布式系统中的流动的规范，用于追踪请求在分布式系统中的流动情况，并提供可视化分析请求的性能和行为的能力。在 MQTT 场景下，这一概念可以实现跨越 MQTT 消息传输中的不同参与者（发布者-MQTT 服务器-订阅者）的请求追踪。

EMQX 遵循 [W3C 的 Trace Context MQTT](https://w3c.github.io/trace-context-mqtt/) 规范实现了端到端的分布式追踪功能：客户端在发布时为消息添加 `traceparent` 用户属性，Traces 将记录消息在 EMQX 集群节点以及订阅者之间的流转情况。对于不支持设置用户属性的 MQTT v3.1/3.1.1 客户端，也可以配置 EMQX 在内部自动为消息添加追踪 ID 实现分布式追踪。

借助 OpenTelemetry 分布式追踪，EMQX 系统管理员或开发者可以实时监测和分析物联网应用的性能和行为，并在出现故障时快速定位并排除故障。

### 日志（Logs）

与基于文件的日志一样，OpenTelemetry 日志同样用于记录关键事件、状态信息和错误消息，帮助开发人员和运维团队理解应用程序的行为和故障排查。

不同的是，OpenTelemetry 日志使用了规范化的日志记录格式，使得日志更易于解析、分析和处理。初次之外 OpenTelemetry 日志还支持在记录中添加丰富的上下文信息，如 Trace ID、标签、属性等。

EMQX 支持同时开启 OpenTelemetry 指标、追踪与日志功能。指标用于实时状态监测，追踪数据显示请求的流程和途径，而日志数据可以提供每个流程上更多的细节和上下文信息，三者相互集成可以建立一个统一的视图和分析平台，形成一个完整的观测解决方案。通过统一的平台，用户可以更高效地管理和利用数据以获得全面的应用程序观测能力，从而准确地定位和解决问题，大大提升开发人员和运维团队的工作效率。

## 开放充电协议 OCPP 协议网关

[OCPP](https://www.openchargealliance.org/) (Open Charge Point Protocol) 是一个连接充电桩与中央管理系统的开放通信协议，旨在为电动汽车充电基础设施提供统一的通信规范。

本次发布新增了 OCPP 1.6-J 版本的协议网关，能够为符合 OCPP 规范的各品牌充电桩设备提供开箱即用的海量接入与上下行消息传输能力，并提供了一系列安全、管理与集成的支持，包括：

1. 提供 TLS/SSL 加密连接，保障传输层安全
2. 提供用户名/密码、JWT 接入认证
3. 提供上下行消息权限控制能力
4. 提供基于 Dashboard 与 REST API 的客户端管理能力
5. 支持与 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)异构结合，满足更加灵活和多样化的应用场景需求
6. 支持通过规则引擎、数据集成以及 REST API 等方式与第三方管理系统（Central System）集成

借助以上特性，用户可以快速构建安全可靠的电动汽车充电基础设施，快速交付并实现有效充电业务管理和运营。

## JT/T 808 与 GB/T 32960 协议网关

本次发布新增了 JT/808 与 GB/T 32960 两种车联网协议网关，能够提供符合标准的车辆数据接入，并通过 EMQX 的集成能力与车辆管理平台侧集成，实现互联互通。

JT/T 808 是交通部颁布的车载终端通信协议，广泛用于车辆远程监控和调度管理。该标准规定了车辆与监控中心之间的通信协议格式和数据传输方式。协议包括车辆定位、报警信息、语音通信、数据传输等功能，可以实现车辆位置追踪、实时监控、报警处理等功能。

GB/T 32960 电动汽车远程服务与管理系统技术规范的国家标准。该标准规定了电动汽车的远程服务与管理系统的技术要求、数据格式和交互方式。协议包括了电动汽车的基本信息、驱动电池信息、车辆位置信息、行驶数据、故障诊断等内容，通过这些信息可以实现电动汽车的远程监控、能源管理和安全管理等功能。

借助两种车联网专属协议以及标准 MQTT 协议支持，EMQX 能够提供多类数据一体的接入和集成能力，帮助车企与车辆平台快速构建车联网应用，提供更高效、智能化的车辆管理和运营服务。

## Confluent 集成支持

Confluent 是一个全面的数据流平台，提供全托管的 Confluent Cloud 与自托管的 Confluent Platform 产品，用于处理和管理连续、实时的数据流。

Confluent 包含多项服务，例如 Kafka 服务，Schema Registry 与事件流处理工具，以及跨区域的数据复制能力和其他丰富的扩展功能。EMQX 与 Confluent 生态集成，能够为企业提供灵活的物联网实时数据采集、传输、处理和分析全套解决方案，为企业提供更多的洞察和决策支持。

## 安全增强

1. 通过 Prometheus Pull 模式集成时，支持为用于获取指标的 REST API `GET /api/v5/prometheus/stats` 启用身份验证功能。
2. 配置文件现在支持将敏感配置存储为文件，并通过在配置文件中使用特殊前缀 `file://` 来指定文件路径进行加载。
3. REST API 现在添加了 RBAC 功能，实现更精细安全管理。通过 Dashboard 或密钥初始化文件创建 API 密钥时，可以指定 API 密钥的角色，现有以下角色可供选择：
   - 管理员：可以访问系统中的所有资源。
   - 查看者：只能查看资源和数据，对应 REST API 中的所有 GET 请求。
   - 发布者：专门用于 MQTT 消息发布，只能访问与发布相关的 API。

## 性能增强的新路由存储架构

本次发布设计了新的路由存储架构，在内存使用量略有增加的情况下提高订阅和路由性能，尤其是对于共享订阅下使用通配符的场景。在内部基准测试对比中，EMQX 5.4.0 版本相较于 5.3.0 版本，平均订阅速度提升了 30%。

同时由于新存储架构取消了建立单独索引操作，也因此彻底避免了极端情况下集群路由状态不一致的情况出现。

新存储架构默认启用，旧版本集群将在滚动升级后也将自动切换到新架构。如果你不想使用新架构，可以通过配置 `broker.routing.storage_schema` 指定使用旧架构。

## 其他新增与变更功能

1. REST API 与 Dashboard 添加了备份与恢复功能，用户可以为集群创建多个数据备份，并在需要的时候恢复。
2. Dashboard 中添加了审计日志管理页面，用户可以使用该页面查看对 EMQX 设备和数据进行的所有更改操作，例如踢出设备、创建/删除规则等。
3. Dashboard 单点登录中的 SAML 协议支持与 Azure Entra ID 进行集成。
4. 客户端认证使用 LDAP  作为数据源时支持通过 bind 操作进行验证，适用于已经在 LDAP 服务器上拥有账户数据或缺乏添加或修改数据权限的情况。
5. 调整数据桥接设计，将其拆分为连接器与动作（Sink）。连接用于管理数据集成与外部系统的连接，可以在多个动作之间重复使用，动作仅用于配置数据操作方式。这个设计能够提供更大的灵活性和更好的可扩展性，实现更清晰的数据集成配置与管理。
6. 节点重平衡操作状态 API `GET /api/v5/load_rebalance/availability_check` 取消身份验证，简化了负载均衡器配置。
7. 新增重置  License 功能，允许将现有的 License 设置为默认试用 License。
8. 调整默认试用 License 规格，由 100 连接调整为 25 连接。

## BUG 修复

以下是主要 BUG 修复列表：

- [#10976](https://github.com/emqx/emqx/pull/10976) 修复共享订阅中的主题过滤器重复处理问题。 在之前的实现中，订阅选项的存储方法没有充分适配共享订阅，这导致在特定的主题和流程下，”订阅-取消订阅” 期间消息路由失败并且节点之间的路由表出现泄漏问题。
- [#12048](https://github.com/emqx/emqx/pull/12048) 修复 COAP 网关忽略订阅选项的错误。
- [#12158](https://github.com/emqx/emqx/pull/12158) 修复规则引擎无法连接到 [Upstash](https://upstash.com/) Redis 的问题。修复前，在与 Redis 服务建立 TCP 连接之后，EMQX 的 Redis 驱动程序使用 [inline commands](https://redis.io/docs/reference/protocol-spec/#inline-commands) 来发送 AUTH 和 SELECT 命令。但 Upstash Redis 服务不支持 inline commands，导致 EMQX 无法连接到 Upstash Redis 服务。 修复后，EMQX 的 Redis 驱动使用 RESP (Redis Serialization Protocol) 来发送 AUTH 和 SELECT 命令。

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.4.0 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.4.0)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
