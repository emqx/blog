在上一篇文章中，我们从 Microduck 的硬件与软件架构出发，在 MuJoCo 仿真环境中为它接入了 MQTT 控制。本文将探讨如何将 Microduck 和 Device Agent 集成，通过 Device Agent 中集成的 LLM，ASR 和 TTS 等 AI 服务，进一步为其提供面向用户的智能交互与自动化能力：用户可以用文字或语音让它行走、转向和踢球，也可以用自然语言描述需求，大模型根据设备事件编排连续动作，或用定时任务让它在指定时间执行指令等有趣的内容。

**本文将完成：**

- 构造设备规格描述将 Microduck 接入 Device  Agent；
- 使用自然语言控制 Microduck 行走、转向和踢球；
- 利用 Device Agent 的工作流和定时任务实现自动动作编排和控制；

## Device Agent 如何接入 Microduck



上一篇文章已经让 Microduck 能够通过 MQTT 接收速度指令，但调用者仍然需要知道 MQTT 协议的详细信息，比如主题、字段名称和取值范围。

Device Agent 在 MQTT 协议上增加了一层设备语义：通过这层语义，AI 可以先理解用户的自然语言意图，然后再依据设备规格选择合法命令、补全参数，并通过 MQTT 将结构化指令发送给设备。

在官方推荐的 Remote Access Design 方案中，Microduck 基于 WebRTC 搭建了一条完整的实时远程会话通道：音视频通过 Media Track 传输，控制请求与高频遥测则通过不同类型的 Data Channel 传递。它解决的核心问题是——如何让远端用户实时接入并操控机器人。

如果说 Remote Access 负责「连得上、控得住」，那么 Device Agent 解决的就是「看得懂、会决策」。它让运行在云端的 LLM 能够理解设备能力，并根据用户意图完成数据查询、机器人控制与自动化任务；同时提供机器人数据上报、动作控制等基础能力，并集成语音识别与合成、工作流、定时任务等功能，最终为机器人构建一套端到端的「云端大脑」。

### 设备规格



[设备规格（DeviceSpec）](https://docs.emqx.com/en/device-agent/latest/usage/create-agent.html#devicespec-schema)是设备与 Device Agent 之间的能力契约，主要由四部分组成：

- **Name+Description：**名称和描述，用于记录设备的基础信息；
- **Commands：**设备能够执行的操作，以及每个操作所需的参数，例如移动方向、持续时间或踢球脚；
- **Properties：**设备持续上报的状态，例如是否正在移动、当前动作和最近一次执行结果；
- **Events：**设备主动报告的离散事件，例如动作完成、动作失败或通信超时。

DeviceSpec 同时也是大模型与设备安全边界之间的第一道约束。模型不能凭空创造设备没有声明的命令，设备端也不应因为指令来自 Agent 就跳过自身的参数校验和安全控制。

### 设计 Microduck 的设备规格



示例工程 [microduck_demo_part1](https://github.com/hjianbo/microduck_demo_part1) 在 `src/device_agent_integration_demo/device-spec.json` 中提供了可导入的 Microduck DeviceSpec。它把底层速度控制和强化学习策略封装为更适合用户理解的高层能力。

**设备命令**

| **命令**     | **参数**                         | **功能**                                     |
| :----------- | :------------------------------- | :------------------------------------------- |
| `move`       | `direction``duration_s` （可选） | 向前移动，或以向前曲线方式左转、右转         |
| `stop`       | 无                               | 停止当前行走动作                             |
| `kick`       | `foot`                           | 使用左脚或右脚执行踢球策略                   |
| `place_ball` | 可选 `position`                  | 在仿真环境中重新放置小球，用于调试和演示维护 |

`move` 对外使用 `forward`、`left`、`right` 和 `backward` 等高层方向。适配器再把这些方向映射为当前策略已经验证过的速度组合。其中，左转和右转是向前运动中的曲线转弯，不是横移或原地旋转；固定版本的行走策略不能可靠后退，因此 `backward` 会返回明确的「不支持」响应。

**设备属性**

- `motion_state`、`vx`、`vy`、`yaw`：当前运动状态与运动意图；
- `active_action`、`kick_side`：当前高层动作与最近请求的踢球脚；
- `ball_state`、`last_action_result`：小球状态与最近一次动作结果；
- `command_timeout_s`：MQTT 断线后触发运动停止的超时时间。

这些属性会通过 MQTT 协议上报到云端并存入数据库中，Device Agent 通过这些上报属性信息，用户可以直接询问“Microduck 现在还在走吗”，或者“上次踢球成功了吗”，Device Agent 理解用户的语义后读取设备上报的状态回答，而不是根据对话历史猜测。

**设备事件**

- `action_completed`：移动、放球或踢球完成；
- `action_failed`：动作失败，或当前策略不支持该动作；
- `command_timeout`：MQTT 连接中断超过安全阈值，正在进行的移动被停止。

这些事件既可以在 Device Agent 中展示执行结果，也可以成为工作流的触发条件。经过这层建模，Microduck 不再只是一个被动接收 MQTT 消息的客户端，而成为一个有能力、有状态、也会主动报告结果的设备智能体。

## 通过 Device Agent 控制仿真机器人



### 安装与配置 Device Agent



开始前，请准备能够打开 MuJoCo 窗口的桌面环境、Python 3.12、Git 和 [uv](https://docs.astral.sh/uv/)。

打开 [Device Agent 产品官网](https://www.emqx.com/zh/device-agent)找到对应系统的安装方式进行安装；在 macOS 或 Linux 上执行以下命令安装并启动 Device Agent：

```
curl -fsSL https://emqx.sh/device-agent | sh
device-agent
```

启动后打开 `http://127.0.0.1:3000`。首次使用需要完成三项基础配置：

**配置 MQTT Broker**

在「设置」→「MQTT」处可配置 Device Agent 要链接的 MQTT Broker。快速体验可以使用 Device Agent 提供的 Zero MQTT Broker。点击创建后会自动将得到 MQTT 的全部配置，直接保存配置即可；长期运行时可切换到自建 EMQX，或者 EMQX Cloud 等 MQTT 服务器。

![image.png](https://assets.emqx.com/images/31b426562fcfec2a3c5b8149a1880a75.png)

**配置大模型**

在「设置」→「模型」中选择支持工具调用的模型服务，并填写模型名称与访问凭证。Device Agent 依靠它理解用户意图、选择工具和组织执行步骤。下图所示配置了 DeepSeek v4 Flash 模型。

![image.png](https://assets.emqx.com/images/1f0233435dc04c99409d18d97b9012bb.png) 

**配置语音模型**

进入「设置」→「语音」，启用语音能力并选择服务商，配置语音识别和语音合成所需的模型与凭证。完成后，Device Agent 才能把语音输入转换为文字，并将回复合成为语音。

![image.png](https://assets.emqx.com/images/60152761826cdcf2e771a9def60a6a23.png)

### 接入仿真机器人



克隆示例工程并完成初始化：

```
git clone --recurse-submodules https://github.com/hjianbo/microduck_demo_part1.git
cd microduck_demo_part1
./scripts/bootstrap.sh
```

`bootstrap.sh` 会拉取固定版本的 Microduck 强化学习工程和 Simulator，安装 Python 依赖，下载并校验 ONNX 策略，同时生成本地测试所需的 `.demo/device-agent.env`。该目录已被 Git 忽略，用于保存实际的 Broker 和设备凭证。

接下来，在 Device Agent 的网页控制台的「创建设备智能体」页面，点击「导入设备描述」并上传刚刚所克隆仓库的设备规格描述文件：

```
src/device_agent_integration_demo/device-spec.json
```

确认 Device Agent 识别出的命令、属性和事件与前文一致后，点击创建设备智能体。

![image.png](https://assets.emqx.com/images/5bd9a9549555024021fa34a8a40d575e.png)

在「接入设备」指引中复制 Broker、Product ID、Device ID 和认证信息，将它们写入 `.demo/device-agent.env`，例如：

```
DEVICE_AGENT_BROKER=mqtts://zero.emqx.io:8883
DEVICE_AGENT_PRODUCT_ID=<product-id>
DEVICE_AGENT_DEVICE_ID=<device-id>
DEVICE_AGENT_USERNAME=<username>
DEVICE_AGENT_PASSWORD=<password>
DEVICE_AGENT_MQTT_QOS=1
DEVICE_AGENT_MQTT_KEEPALIVE=30
DEVICE_AGENT_COMMAND_TIMEOUT=1.0
```

配置完成后，执行以下命令即可启动 Microduck 仿真机器人：

```
./scripts/run_device_agent_integration_demo.sh
```

观察日志可以看看到以下类似日志：

```
Loading walking policy from: .. BEST_alpha_walking.onnx
Loading kick_left policy from: .. ball_kick_left.onnx
Loading kick_right policy from: .. ball_kick_right.onnx
...
Device Agent MQTT: connecting to zero.emqx.io:8883; commands=device-agent/.../device/../commands
Device Agent MQTT: connected and subscribed to device-agent/../device/../commands
```

表明该机器人：

- 加载了 `BEST_alpha_walking.onnx`, `ball_kick_left.onnx`, `ball_kick_right.onnx` 这三个已训练好的模型，包括：行走、左脚踢球和右脚踢球；
- 成功连接到配置的 MQTT 服务器，并成功订阅了相关的主题。

同时也会弹出 Mircoduck 的仿真界面：

![image.png](https://assets.emqx.com/images/f0d02ea4e42b66eae6f309ec5d349123.png)

同样，进入 Device Agent 控制台对于的「MicroduckSimulator」智能体，也可以看到这个刚上线的设备，和它当前的状态：

![image.png](https://assets.emqx.com/images/2d1db6eb420ce018b8225934e01a0abd.png)

至此，Microduck 已成功接入到 Device Agent 之中。

### 控制演示示例



#### 语音控制行走、踢球



进入 Microduck 工作区，打开语音入口，并允许浏览器使用麦克风。可以依次尝试：

- 向前走两秒
- 向左转三秒
- 停下来
- 用右脚踢球
- Microduck 现在是什么状态

「向前移动 10 秒」表现如下：

<video controls width="760px">
    <source src="https://assets.emqx.com/videos/microduck-device-agent/move-forward-10-seconds.mp4" type="video/mp4">
</video>

这条语音指令会在 Device Agent 根据设备规格描述将其自动转换成以下格式控制指令，并通过 MQTT 协议发送给机器人：

```
{
  "cmd": "move",
  "params": {
    "direction": "forward",
    "duration_s": 10
  },
  "requestId": "...",
  "ts": 1710000000000,
  "metadata": {
    "productId": "..."
  }
}
```

**放球和踢球：**

<video controls width="760px">
    <source src="https://assets.emqx.com/videos/microduck-device-agent/ball-release-and-kicking.mp4" type="video/mp4">
</video>

也可以回到和设备的对话框，能清晰看到在这个示例下  Device  Agent 发送了2条指令来完成我们的期望：

![image.png](https://assets.emqx.com/images/5bc6ab323c6b28ac4eee10f8ac768039.png)

#### 工作流和定时任务实现自动控制



语音交互解决了「人如何自然地控制设备」，工作流和定时任务则让设备能够在没有连续人工指令的情况下，AI 自主规划和行动。

**使用 Workflow 串联连续动作**

例如，打开和该设备的对话框，输入

> 创建一个工作流，让机器人顺时针循环移动

可以看到机器人在一直做向右前方移动来完成顺时针的循环，左侧 Device Agent 窗口也监控到了当前机器人的移动状态：

<video controls width="760px">
    <source src="https://assets.emqx.com/videos/microduck-device-agent/workflow-serial-actions.mp4" type="video/mp4">
</video>

也可打开工作流页面，查看 Device Agent 所创建的工作流详情和触发逻辑：

![image.png](https://assets.emqx.com/images/ed184f9fa3c5f12a259db1b2dc488923.png)

**使用定时任务安排设备行动**

工作流由设备事件或状态变化触发，定时任务则由时间触发，适合未来执行、固定间隔或按日运行的设备操作。例如：

> 每分钟前进5s，然后踢右脚

Device Agent 会保存任务并返回下一次运行时间。到期后，Device Agent 启动一次独立执行，并调用当前设备的 `move` 命令，移动完成后还会继续触发踢球，从而组成一条「到点出发，走到球前，自动踢球」的完整链路。

在「定时任务」页面可以查看任务状态、下一次运行时间和执行历史，也可以暂停、恢复或取消任务。

![image.png](https://assets.emqx.com/images/1bd64fc6f1db3b88823b97f3bd945951.png)

也可以创建查询类的周期任务，例如：

> 每天下午四点，查询当前 Microduck 是否在线，并汇总最近一次动作结果。

### 实现原理



从用户说出一句话，到 MuJoCo 中的机器人开始行动，完整链路如下：

![image.png](https://assets.emqx.com/images/9af8b39c0120fa3b4307f2e21a4b6225.png)

语音通道负责语音识别和语音合成，设备上线、命令执行和状态上报仍然通过 MQTT 完成。Device Agent 与仿真器之间使用四类 Topic：

| **方向**            | **Topic**                                              | **用途**                          |
| :------------------ | :----------------------------------------------------- | :-------------------------------- |
| Device Agent → 设备 | `device-agent/{productId}/device/{deviceId}/commands`  | 下发结构化设备命令                |
| 设备 → Device Agent | `device-agent/{productId}/device/{deviceId}/responses` | 返回与 `requestId` 对应的命令响应 |
| 设备 → Device Agent | `v1/{productId}/{deviceId}/telemetry`                  | 上报在线状态和设备属性            |
| 设备 → Device Agent | `v1/{productId}/{deviceId}/event`                      | 上报动作完成、失败和超时事件      |

MQTT 网络线程只负责解析消息、校验基础信封并把命令放入线程安全的 Mailbox。MuJoCo 控制循环在主线程中取出命令，再调用动作控制器，避免网络回调直接修改仿真状态。

动作控制器采用确定性的单动作状态机：移动命令设置速度和截止时间，到期后自动停止；`stop` 可以优先终止行走；踢球期间拒绝新的移动或踢球命令，避免策略被中途切换；命令被接受时立即返回响应，最终结果则通过属性和事件继续上报。

无论命令来自文字、语音、Workflow 还是定时任务，都会经过同一套设备侧保护：

- **参数白名单：**只接受 DeviceSpec 定义的命令与字段，并检查参数类型和范围；
- **有界运动：**移动命令必须带有有限持续时间，截止后自动归零速度；
- **断线停止：**MQTT 中断超过默认 1 秒时，正在进行的行走会在仿真主线程中停止；
- **幂等处理：**命令携带非空 `requestId`，最近 128 个已完成请求会被缓存，QoS 重投不会让机器人重复踢球；
- **生命周期状态：**连接后上报在线状态，异常断开由 MQTT Last Will 上报离线；

这种分层让设备接入与交互体验保持解耦。将来从 MuJoCo 迁移到真实 Microduck 时，DeviceSpec、Device Agent、工作流、定时任务和 MQTT 协议都可以继续复用，主要替换的是设备侧执行层：由真机上的控制服务接收运动意图，继续负责策略推理、关节控制和实时安全。

## 下一步：使用真实机器人



上一篇文章中，我们把面向真实 Microduck 的 MQTT 设备端适配服务称为 mqttd。它需要运行在真实的物理设备上，将来自 MQTT 的设备命令转换为机器人现有控制接口能够执行的运动意图，并负责状态和事件上报。由于作者写本文的时候只有模拟仿真环境，但文中所述的架构方向保持和真机环境是一致的，后续可实现平滑迁移。 

## 总结



在本文中，我们把 Microduck 变成了 Device Agent 能够理解人类语言，进行对话和自动编排的智能设备。

DeviceSpec 将机器人的命令、属性和事件转化为结构化能力，因此 Device Agent 能够把“向前走五秒”“用左脚踢球”这样的自然语言可靠地映射为设备命令。语音让控制更加直接，工作流将设备事件连接成连续动作，定时任务则为设备增加了时间维度上的自动执行能力。无论入口如何变化，命令最终都经过同一套设备侧校验、状态机和安全边界。

Microduck 是一个直观而有趣的起点，但这套模式并不局限于机器人。只要设备能够通过 MQTT 或 SDK 接收命令、上报属性和事件，就可以使用 Device Agent 将设备能力开放给自然语言、语音和自动化流程。

现在，你可以从这个开源 Demo 开始，为自己的机器人或 IoT 设备接入 Device Agent，让设备从「能够联网」进一步走向「能够被理解、被对话、被编排」。最后，读者可以参考 Device Agent 提供的 A2A 能力，可以实现更有趣的小鸭子和其他设备进行协作的场景。

## 参考资料



- 本文演示工程：[GitHub - hjianbo/microduck_demo_part1: Reproducible MQTT control demo for the official Microduck MuJoCo walking policy](https://github.com/hjianbo/microduck_demo_part1)
- Device Agent 安装：[下载安装 | Device Agent 文档](https://docs.emqx.com/zh/device-agent/latest/installation.html)
- 定义设备智能体：[定义设备智能体 | Device Agent 文档](https://docs.emqx.com/zh/device-agent/latest/usage/create-agent.html)
- 语音交互：[语音交互 | Device Agent 文档](https://docs.emqx.com/zh/device-agent/latest/usage/voice.html)
- 工作流：[工作流 | Device Agent 文档](https://docs.emqx.com/zh/device-agent/latest/usage/workflows.html)
- 定时任务：[定时任务 | Device Agent 文档](https://docs.emqx.com/zh/device-agent/latest/usage/scheduled-tasks.html)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
