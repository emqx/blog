## AI 的碎片化问题：跨运行时 Agent 协同

AI Agent 目前已具备调用工具的能力。无论是借助 MCP 服务器，还是依靠 Skills（Agent 原生能力，以附带工具访问权限的提示词形式定义，当下很多从业者更青睐这种简便的方案），Agent 都可以读取数据库、调用 API、操控设备。这一层技术正在快速发展。

在同一体系内组建多个 Agent 的方案也已经成熟。CrewAI、LangGraph、AutoGen 这类框架可以设定不同职责的 Agent，并把它们接入任务链路。如果所有 Agent 共用一套代码库和运行环境，这些工具就能稳定运转。

试想一下，在具备 AI Agent 的智能家居场景：灯光智能体、温控智能体、安防智能体与能耗优化智能体，分别由不同厂商开发。各方代码库、编程语言、部署环境、版本迭代周期均不统一。用户需要一套串联四大模块的工作流程：「离家时锁门、关灯、调低暖气温度」。这类跨智能体的协同，能让智能家居系统实现整体效能大于各模块简单相加的效果。

现有框架无法整合分属不同运行环境的智能体；Skill 与 MCP 服务端也无法实现 Agent 之间的通信。目前缺失的关键要素是一套标准协议，让独立部署的智能体互相发现彼此的能力，并跨企业主体协同完成任务。

Google 推出的 A2A 协议正是为解决这一痛点而生。

## A2A 协议：智能体互操作的标准化时代

A2A 定义了四大核心概念：

- Agent Cards—— 结构化元数据，用于描述 AI Agent 的能力、接口与安全要求
- Messages——AI Agent 间单次通信内容，包含请求、回复、问询澄清三类
- Tasks—— 带状态的工作单元，由一条或多条消息组成，拥有完整生命周期：已提交、处理中、已完成
- Artifacts—— 任务推进过程中逐步产出的结果

该协议统一规范了智能体的互相发现与任务分配流程，不受开发者和部署运行环境的限制。

**引入 A2A 之后，行业方案可划分为三类：**

| **对比项**   | **个人智能体**         | **多智能体框架**         | **A2A**                       |
| :----------- | :--------------------- | :----------------------- | :---------------------------- |
| **模型形态** | 单个 Agent，挂载多工具 | 多个 Agent，共用单一进程 | 多个 Agent，遵循一套协议      |
| **通信方式** | 人与 Agent 交互        | 进程内函数调用           | Agent 互传（发布 / 订阅模式） |
| **能力发现** | 无（仅单个 Agent）     | 编排器内硬编码配置       | 依靠 Agent Cards 动态识别     |
| **耦合程度** | 无耦合关系             | 共用运行时、同一代码仓库 | 独立进程、支持任意编程语言    |
| **互操作性** | 私有封闭体系           | 框架专属兼容             | 开放通用协议                  |

A2A 采用传输层无关的架构设计，其参考实现基于 HTTP 和服务器推送事件搭建。但多 Agent 系统所需的各类协同能力，包括 Agent 发现、在线状态监测、消息广播分发与负载均衡调度，均无法适配点对点的请求响应通信模式。本文将深入阐释：如何基于 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 在协议层实现 Agent 自动发现、该方案可支撑的各类智能体协同模型，以及 EMQX 6.2 如何让整套架构方案达到企业级落地与生产可用标准。

## MQTT Broker 的原生能力

在拆解协议运行逻辑前，先做一个简要的铺垫。

MQTT 原生支持多 Agent 系统必备的协同基础能力，不用额外搭建独立的配套系统：

- 保留消息可以为新的订阅者持久推送状态信息，实现 Agent 发现；
- 遗嘱消息无需轮询式健康检测，在异常停机时主动推送告警，实现在线状态跟踪；
- 共享订阅可以把任务分配给多个消费者，实现负载均衡；
- 主题级 ACL 能够限制每个客户端仅可访问与 {org_id}/{unit_id}/{Agent_id} 身份匹配的主题路径，实现权限管控。

同一套协议既能在 ESP32 硬件端运行，也可部署于云端，无需网关做协议转换。整套架构只需要一个操作界面。

## A2A over MQTT 如何完成 Agent 发现

A2A over MQTT 明确了依托 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 完成 Agent 发现、消息互通与任务协同的整套规则。该规范为开源标准，托管在 GitHub 平台，兼容所有 MQTT 5.0 版本。

### 主题命名空间

所有 A2A 通信报文统一以 $a2a/v1 / 作为前缀，划分为四个独立的命名空间。

![image.png](https://assets.emqx.com/images/d944056d6cf7a8dc092f530425229dd1.png)

该层级结构采用多租户设计，层级顺序为组织、业务单元、Agent。

借助通配符即可快速批量检索节点：

- $a2a/v1/discovery/{org_id}/+/+：查询单个组织下全部 Agent
- $a2a/v1/discovery/+/+/+：查询当前 Broker 接入的所有 Agent

其中， {reply_suffix} 片段由请求方生成，是冲突概率极低的标识令牌，保障多请求并行处理时，各路应答的数据流不会相互串扰。

### Agent Cards

Agent Cards 是一段 JSON 文档，用于描述 Agent 具备的能力以及对接通信方式。它以保留消息的形式发布至发现主题，相当于 Agent 在网络中的身份名片。

```json
{
  "name": "energy-optimizer",
  "description": "Optimizes energy usage across connected devices",
  "version": "1.0",
  "defaultInputModes": ["application/json"],
  "defaultOutputModes": ["application/json"],
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "optimize-schedule",
      "name": "Optimize Energy Schedule",
      "description": "Generates an optimal schedule based on tariffs and occupancy",
      "tags": ["energy", "optimization"]
    }
  ],
  "supportedInterfaces": [
    {
      "url": "mqtt://broker.emqx.io:8883",
      "protocolBinding": "a2a-over-mqtt/0.1",
      "protocolVersion": "0.1"
    }
  ],
  "securitySchemes": {
    "oauth2": {
      "oauth2SecurityScheme": {
        "flows": {
          "clientCredentials": {
            "tokenUrl": "https://auth.example.com/token",
            "scopes": { "energy:read": "Read data", "energy:control": "Control devices" }
          }
        }
      }
    }
  }
}
```

示例为精简内容省略了可选字段；完整的 Agent Card 结构由 A2A JSON Schema 定义。

由于 Agent Card 以保留消息形式发布，新订阅者无需等待各个 Agent 重新上报自身信息。只需订阅发现类通配主题，Broker 会立刻推送所有已存在的 Agent Card。当 Agent 更新自身能力时，会发布新版 Agent Card，订阅端将以普通消息形式收到更新内容。

为兼容标准 A2A 客户端，也可通过 HTTP 地址 /.well-known/Agent-card.json 检索 Agent 信息。若部署同时支持两种传输通道，客户端会依据 supportedInterfaces 配置选择 MQTT 通道。

### **请求/响应流程**

一次完整的交互流程如下：

**发现 Agent。**请求方订阅 `$a2a/v1/discovery/{org_id}/+/+`，获取所有可用 Agent 的保留 Agent Card。

**订阅回复。**请求方订阅自己的回复主题：`$a2a/v1/reply/{org_id}/{unit_id}/{Agent_id}/{reply_suffix}`。

**发布请求。**请求方向目标 Agent 的请求主题发布消息，包含：

- MQTT v5 响应主题，指向请求方的回复主题
- MQTT v5 关联数据，本次请求的唯一标识
- 负载，内含 A2A JSON-RPC 请求及 Task.id

**消息路由。**Broker 将消息投递给订阅该请求主题的 Agent。

**Agent 回复。**Agent 处理任务，将结果发布到响应主题，回传关联数据，负载中包含任务状态。

**Broker 推送。**请求方在应答订阅中收到消息，通过关联数据进行匹配。

整个流程均使用标准 MQTT v5 特性。响应主题和关联数据正是为请求-响应模式而引入协议的。推荐使用 QoS 1（至少一次送达）。无需自定义消息头，也无需在协议上调整。

![image.png](https://assets.emqx.com/images/a9ad3ff2a8cea4f75643e3f385147981.png)

## Agent 发现带来的价值

Agent 发现并非最终目的，而是实现高效协同的基础。如果 Agent 之间能够互相检索、建立通信通道，依托 MQTT 基础能力便可衍生多种高效实用的协同模式。

### 任务状态流式推送

并非所有任务都能一次性返回完整结果。比如撰写报告的调研型 Agent、处理海量数据集的分析型 Agent、比对方案的规划型 Agent，这类任务都需要较长执行时间。

A2A over MQTT 可原生适配该场景：Agent 向请求方的响应主题分批推送多个回复报文，全部携带同一组关联数据。每条回复附带任务阶段状态：`submitted`→ `working`（包含部分 Artifacts）→ `completed`。请求者会一直保持订阅状态，直到收到终止状态：`completed`、 `failed`、 `canceled` 或者 `rejected`。Agent 每产出一部分 Artifacts，就即时推送至请求端。

该模式属于离散事件流式传输，并非持久的长连接。每一次状态更新都是独立的 MQTT 发布请求。即便请求方短暂断连后重连，QoS 1 等级也能保证未接收的更新消息完整送达。

### Agent 集群与负载均衡

当需要部署多套相同 Agent 实例（例如十个翻译 Agent 并行承接请求），借助集群主题与共享订阅即可完成负载均衡，无需额外部署第三方中间件。

各个 Agent 通过 MQTT 共享订阅绑定集群主题，Broker 收到消息后，仅将请求分发至组内其中一个订阅实例。

被选中处理任务的 Agent，会在回复报文的 MQTT 5.0 用户属性 a2a-responder-Agent-id 中填入自身唯一标识。请求方可精准获知处理任务的 Agent，后续跟进消息直接发送至该 Agent 独立请求主题，保持会话关联性。

增加订阅者的操作也及其简单：新建 Agent 实例、加入共享订阅组即可接收任务，无需调整负载均衡配置或更新路由表。

### 在线状态与存活检测

前文提到遗嘱消息（LWT）可免费实现异常宕机检测，A2A over MQTT 在此之上搭建了更完善的在线状态模型。智能体发布 Agent Card 时，会在 MQTT 5.0 用户属性中标注 a2a-status=online；对应的遗嘱消息携带同一份 Agent Card，但状态字段为 a2a-status=offline。额外设置 a2a-status-source 字段区分三种状态来源：

- Agent：正常主动下线，状态由 Agent 自身上报
- lwt：意外断连，由 Broker 触发遗嘱消息推送
- broker：状态由 Broker 统一托管（EMQX A2A 注册表采用该模式）

这种区分具备实际运维价值：监控服务识别到 lwt 类型状态，会自动重启 Agent；可视化面板识别到 Agent 主动下线，则不会触发告警通知。

### 任务转交

部分场景下，启动任务的 Agent 并非最适合收尾执行的角色。通用接待 Agent 接收需求后，评估判定交由专业 Agent 处理更合适，便在应答的 a2a-responder-Agent-id 中填写专业 Agent 标识。请求方后续消息直接转发至专业 Agent 的请求主题。

转交过程中 Task ID 保持不变，对请求方而言任务流程无缝衔接；接待 Agent 无需转发流量、持续占用数据链路。该模式非常适配分层架构：分诊类 Agent 将业务分流至各领域专业 Agent。

### 多轮交互会话

为了满足更多应用场景，A2A 定义了两种多轮交互形式，均可稳定运行在 MQTT 之上。

**中断式任务：共用同一个 Task ID**

预订型 Agent 经常需要补充信息：“出行日期？经济舱还是商务舱？” 此时应答状态标记为 input-required 而非 completed，任务暂停等待补充输入。请求方在原请求主题回填信息，沿用原有 Task ID，Agent 从上一进度继续执行。每次收发报文会生成全新关联数据（单次交互独立），但 Task ID 在任务全生命周期内固定不变。

**多步骤会话：独立 Task ID，共用同一 Context ID**

一套串联任务流程（例如先订机票、再订酒店）可依靠 Context ID 归为同一会话。每一项子任务拥有独立 UUIDv4 格式 Task ID，全部绑定同一个 UUIDv4 格式 Context ID，方便 Agent 全程留存会话状态（对话记录、大模型上下文等）。

Context ID 为可选配置，在简单的一问一答场景中无需启用；在中断续跑任务、多步骤连贯会话等场景启用它维持会话上下文。

## 从规范到生产：EMQX 6.2 内置 A2A 注册表

以上所有内容均兼容任何 MQTT v5 Broker，该规范刻意保持了对 Broker 的中立性。但在大规模运行发现机制时，会遇到两个规范未覆盖的实际问题。EMQX 6.2 的 A2A 注册表（Registry）正是为解决这两个问题而设计的，它提供了模式校验、Agent 状态跟踪、仪表盘和 CLI 管理等功能：

### **多条注册通道，统一命名空间**

Agent 可通过 MQTT 保留消息自注册，操作员可通过控制面板注册，自动化脚本可通过 REST API 注册。三种方式最终都会生成一条 `$a2a/v1/discovery/` 下的保留消息。订阅者感知不到任何差异，因此你可以在开发环境手动引导，到生产环境切换为自注册，无需修改发现逻辑。

### 注册速率与大小限制

当 Agent 重启或网络分区恢复后，数百个 Agent 同时重连，命名空间可能被大量注册消息淹没。可配置的速率限制与 Agent Card 大小上限能吸收这类突发流量，避免影响 Broker 性能。

## 未来方向

AI Agent 协同技术栈的架构形态正在逐步成型。

Skills 和 MCP 赋予 Agent 执行能力——使用工具和访问数据。A2A 赋予 Agent 身份和交互能力——在网络上可以被发现、基于一套标准方式来进行分工和协作。MQTT Broker 则是连接这一切的统一平台，整合了 Agent 发现、在线状态监测、负载均衡和权限控制等能力，节省了单独搭建、运维多套独立配套系统的成本。

如果你想继续深入了解：

- [A2A over MQTT](https://github.com/emqx/mqtt-for-ai/tree/main/a2a-over-mqtt) 的规范是开源的。[Skitter](https://github.com/id/skitter) 是可参考的案例，可以立即克隆并运行。
- [EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt) 提供永久免费套餐，几秒内即可提供生产级 MQTT Broker，足以支撑多 Agent 系统运行，无需管理基础设施。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
