随着 AI Agent 从独立执行任务走向多 Agent 协同，如何让不同 Agent 发现彼此的能力、高效交接任务，并持续跟踪执行进度，成为构建复杂 AI 应用的重要问题。

在 10 月 30 日的线上直播中，EMQ 资深研发工程师刘新宇围绕 **Google A2A 协议、A2A over MQTT 传输层设计及 EMQX A2A Registry** 展开介绍，并通过冷库异常处置 Demo，展示了多个 Agent 如何基于 MQTT 完成任务协同。

以下是本次分享的主要内容（更多详情请观看文末的直播回放视频）：

## A2A：建立 Agent 之间的协作机制



随着 Agent 应用不断复杂化，单个 Agent 往往难以独立完成涉及多个专业领域的任务。例如，在一项设备运维任务中，负责接收告警的 Agent 可能需要委派诊断 Agent 分析故障原因，再由设备控制 Agent 执行相应操作。

这些 Agent 可能由不同团队开发，采用不同的技术框架，但要实现有效协作，就需要一套统一的交互约定，明确如何发现能力、交接任务、反馈进度和交付结果。

Google 提出的 A2A（Agent-to-Agent）协议正是为此而设计。它规范了 Agent 之间的协作方式，主要围绕三个核心对象展开：

1. **Agent Card：描述与发现 Agent 能力**

   Agent Card 可以理解为 Agent 的数字名片，以 JSON 格式描述 Agent 的身份、技能和交互能力，主要包含：

   - **Name / Description**：Agent 的名称与基本介绍。
   - **Skills**：Agent 能够完成的业务任务，例如资料检索、故障诊断等。
   - **Supported Interfaces**：Agent 提供的调用接口及协议版本。
   - **Capabilities**：Agent 支持的交互能力，例如是否支持流式响应。

   请求方可以通过读取 Agent Card，了解其他 Agent 的能力，并选择合适的执行方。

2. **Message：交接任务与上下文**

   找到合适的 Agent 后，请求方通过 Message 发送任务目标和相关信息。

   Message 支持文本及结构化数据，并通过不同字段标识消息来源和关联关系。其中，`messageId` 用于唯一标识一条消息，`role` 用于区分请求方和执行方，`taskId` 与 `contextId` 则分别用于关联已有任务和同一上下文中的交互。

   这种设计不仅支持简单的任务委派，也为后续多轮沟通和信息补充提供了基础。

3. **Task 与 Artifact：跟踪任务并交付结果**

   对于需要较长时间完成的任务，仅有请求和回复还不够。A2A 通过 Task 跟踪任务的执行状态，通过 Artifact 承载任务产生的结果。

   Task 的状态会随着执行过程发生变化，例如：

   - `SUBMITTED`：任务已提交。
   - `WORKING`：任务正在处理。
   - `INPUT_REQUIRED`：任务需要补充信息。
   - `COMPLETED`：任务已完成。

   如果执行过程中发现信息不足，执行方可以将任务置为 `INPUT_REQUIRED`，请求方补充信息后，继续原有任务，而不必重新发起一项工作。

   对于需要持续反馈的任务，A2A 还支持流式响应。执行方可以通过状态更新和结果更新事件，分阶段返回任务进度及 Artifact，让请求方持续了解执行情况。

需要注意的是，**A2A 与 MCP 并不是相互替代的关系**：A2A 负责 Agent 之间的任务协作，MCP 则用于 Agent 内部接入工具和数据，两者分别解决不同层面的问题。

## A2A over MQTT：让 Agent 协作融入物联网消息系统



A2A 定义了 Agent 之间如何协作，但在物联网环境中，还需要解决一个实际问题：分布在设备、边缘和云端的 Agent，如何建立连接并可靠地交换消息？

例如，部署在工厂内网或网关之后的边缘 Agent，通常可以主动连接外部服务，但如果需要从外部直接访问它，就可能涉及网络地址、访问配置和网络穿透等问题。

与此同时，随着 Agent 数量增加，能力发现、在线状态感知和异步任务交互也会带来更多管理需求。

针对这些问题，EMQ 提出了 **A2A over MQTT**，在 Google A2A 协议的基础上，定义了如何使用 MQTT 5 承载 Agent 发现、任务请求和结果返回。

其核心思路是：让不同位置的 Agent 都作为 MQTT 客户端主动连接 Broker，通过发布订阅机制完成协作，无需为每个 Agent 单独建立直接连接。

### 基于 MQTT 保留消息实现 Agent 发现



在 A2A over MQTT 中，执行方 Agent 将自己的 Agent Card 发布到约定的 Discovery Topic，并设置为保留消息（Retained Message）。

请求方只需要订阅相应的发现主题，就可以获取指定组织和单元下的 Agent 信息。

例如，执行方使用以下主题发布自己的 Agent Card：

```
$a2a/v1/discovery/{org_id}/{unit_id}/{agent_id}
```

请求方则可以通过通配符订阅：

```
$a2a/v1/discovery/{org_id}/{unit_id}/+
```

订阅后，请求方可以获得两类信息：

- **Payload**：Agent Card JSON，包含 Agent 的名称、技能、接口和交互能力等信息。
- **MQTT 5 User Properties**：包含 `a2a-status` 等属性，用于提示 Agent 当前的在线或离线状态。

这里，MQTT 保留消息发挥了重要作用：新加入的订阅者无需等待 Agent 再次发布，就能立即获取最新的 Agent Card；后续 Agent 信息发生更新时，也可以持续接收更新。

此外，还可以结合 MQTT 遗嘱消息（Last Will and Testament，LWT），在 Agent 异常断开时发布离线状态，帮助其他 Agent 感知其连接状态变化。

### 基于 MQTT 5 实现请求与回复关联



完成能力发现后，请求方需要将任务发送给目标 Agent，并准确接收对应的执行结果。

A2A over MQTT 利用 MQTT 5 的两个关键属性实现这一机制：

- **Response Topic**：请求方在发送任务时指定回复地址，执行方完成处理后，将响应发布到指定主题。
- **Correlation Data**：请求方在请求中携带关联数据，执行方回复时原样返回。请求方据此将响应与对应的调用进行匹配。

其中，Response Topic 负责确定回复消息的路由地址，Correlation Data 则负责关联一轮具体的请求与回复。二者配合，可以支持同一任务中的多轮交互。

这里还有一个**与核心 A2A 协议不同的设计**：在标准 A2A 交互中，Task ID 通常由执行方生成；而在 A2A over MQTT 中，要求请求方预先生成 Task ID，以便在发起请求时建立任务关联。

### 完整协作流程：从能力发现到结果交付



通过上述机制，A2A over MQTT 将 Agent 协作完整地融入 MQTT 消息系统：

1. **能力发现**：执行方发布 Agent Card 保留消息，请求方订阅发现主题，获取 Agent 能力及在线状态。
2. **准备交互**：请求方选择目标 Agent，并提前订阅自己的回复主题。
3. **任务委派**：请求方发送任务请求，同时携带 Response Topic 和 Correlation Data。
4. **任务执行与反馈**：Broker 根据 Topic 将请求路由给目标 Agent，执行方处理任务，并通过 Broker 持续返回任务状态和结果。
5. **结果交付**：请求方根据 Correlation Data 关联响应，并通过 Task ID 跟踪任务；如果需要补充信息，还可以继续原有任务。

通过这种方式，A2A over MQTT 复用了物联网系统中成熟的 MQTT 连接与消息路由机制，使分布在不同网络环境中的 Agent 能够进行异步协作。

![image.png](https://assets.emqx.com/images/87e3305fe7ae4d4a34a34162342e193f.png)

## EMQX A2A Registry：集中注册与管理 Agent 能力



当 Agent 数量逐渐增加，仅依靠各个 Agent 自行发布和订阅 Agent Card，可能难以满足集中管理和能力维护的需求。

为此，EMQX 提供了 **A2A Registry**，用于集中注册、校验和管理 Agent Card，为 Agent 能力发现与管理提供统一入口。

A2A Registry 主要支持以下功能：

- **注册**：收录 Agent 发布的 Agent Card，建立 Agent 能力目录。
- **校验**：支持通过 JSON Schema 校验 Agent Card，确保注册信息符合预期格式。
- **查看**：在 EMQX Dashboard 中查看已注册 Agent 的名称、技能及完整 Card JSON。
- **管理**：支持对 Agent 信息进行更新、注销及在线状态管理。

## 实战演示：多 Agent 协作处理冷库温度异常



为了展示 A2A over MQTT 在物联网场景中的实际应用，直播中搭建了一个冷库异常处置 Demo。模拟冷库的正常温度范围为 2–8°C，当系统监测到温度升至 9.2°C 时，多个 Agent 开始协同处理这一异常。

整个流程由三个 Agent 共同完成：

- **协调 Agent**：接收异常信息，制定处理流程，并协调其他 Agent 完成任务。
- **诊断 Agent**：分析冷库运行数据，判断温度异常的原因。
- **设备控制 Agent**：根据诊断结果执行设备调节，并反馈执行状态。

首先，协调 Agent 将异常诊断任务交给诊断 Agent。诊断 Agent 分析设备数据后，发现制冷功率过低是导致温度升高的原因，并将诊断结果返回给协调 Agent。

随后，协调 Agent 将设备调节任务交给设备控制 Agent。考虑到设备操作需要人工确认，设备控制 Agent 在获得确认后，将模拟制冷设备的功率从 25% 提高至 80%，并通过 Artifact 返回执行结果。最后，协调 Agent 汇总诊断与执行信息，生成完整的异常处置报告。

在这一过程中，三个 Agent 无需彼此了解内部实现，只需通过 A2A 协议交接任务；MQTT 则负责在不同 Agent 之间传递请求、响应和状态信息。EMQX A2A Registry 为 Agent 提供统一的注册与发现机制，使协调 Agent 能够找到具备相应能力的 Agent，并发起协作。

这个 Demo 展示了从异常发现、原因诊断到设备控制的完整协作链路，也说明了 A2A over MQTT 如何将多 Agent 协作引入真实的物联网设备管理场景。

![image.png](https://assets.emqx.com/images/43453a2ba0c6e8bf4ac8b64b8e141153.png)

## 总结



A2A 定义了 Agent 之间的协作方式，MQTT 提供可靠的连接与消息路由，EMQX A2A Registry 则让 Agent 能力的注册与发现更加便捷。

三者结合，为设备、边缘与云端的 Agent 建立协作基础，也让 EMQX 的 MQTT 消息基础设施进一步延伸至物联网多 Agent 协作场景，**让设备、数据与智能应用能够更高效地连接和协同。**



**探索更多相关内容：**

- A2A over MQTT 详细介绍：[A2A over MQTT 工作原理 | EMQX 企业版 文档](https://docs.emqx.com/zh/emqx/latest/develop/emqx-ai/a2a-over-mqtt/architecture.html) 
- 基于 A2A 协议的机械臂与机器狗协作演示：[视频号](https://weixin.qq.com/sph/AaV3HeFL4l) 


<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
