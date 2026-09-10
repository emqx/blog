Microduck 是一台面向 Physical AI、强化学习和机器人开发的小型双足机器人，它可以通过强化学习策略行走、转向并完成多种动作，实现一些非常有趣的功能。**本系列文章将介绍如何利用 Device Agent 来扩展 Microduck，通过 MQTT 为其接入云端运行的 LLM，Web 或者手机端应用等，实现更加复杂、有趣的边云协作场景。**

首先我们将介绍 Microduck 的硬件与软件架构，并在 MuJoCo 仿真环境中，完成基于基础的 MQTT 协议控制机器人实验「通过在第三方发送控制命令，让机器人在模拟环境中行动」。其次，我们将讨论如何通过一个设备端适配服务 `mqttd`，将同样的设计扩展到真实机器人。

**本文作为系列文章的上篇，将完成：**

- 初始化 Microduck 仿真环境
- 连接 EMQX 公共 Broker，使用 Python 脚本发布速度命令
- 理解从仿真控制走向真机控制所需的架构与安全机制

## 认识 Microduck

在正式开始之前，我们先了解 Microduck 的组成，以及一条运动命令最终如何变成机器人的动作。

### 产品与规格

![](https://assets.emqx.com/images/dc99f28edc03896ee37b6b04cccff265.png)

Microduck 是 Pollen Robotics 推出的小型双足机器人，高约 25 cm，重量低于 800 g。它使用 Rockchip RK3566 及 AI 加速器作为计算平台，运行 Linux 系统。

| **组件**   | **公开规格**                          | **作用**                                                 |
| :--------- | :------------------------------------ | :------------------------------------------------------- |
| 计算平台   | Rockchip RK3566、1 GB RAM、32 GB 存储 | 运行策略推理、机器人服务和网络程序                       |
| 关节执行器 | 15 个电机                             | 驱动双腿、头颈和嘴部机构，其中运动策略输出 14 个关节动作 |
| 姿态传感器 | 2 个 IMU，分别位于身体和头部          | 提供机器人姿态与头部运动状态                             |
| 视觉       | 前置摄像头                            | 提供视觉输入和远程视频能力                               |
| 距离感知   | 8×8 ToF LiDAR                         | 提供多区域距离数据                                       |
| 音频       | 麦克风与扬声器                        | 支持声音输入和音效播放                                   |
| 近场交互   | 2 个 NFC 天线，分别位于头部和嘴部     | 支持标签与物体交互                                       |
| 电源       | 可拆卸 NP-F550 电池                   | 根据负载提供约一小时续航                                 |

根据 Pollen Robotics 当前的公开说明，摄像头分辨率与视场角、LiDAR 测距范围、无线版本等规格仍在最终确认中。因此，本文采用官方已确认的能力口径，不绑定开发样机上的具体传感器型号。

Microduck 的舵机与机身 IMU 通过同一条硬件总线通信，因此实时控制程序必须独占总线。其他程序通过本地控制接口发送意图，不能直接操作串口。

### 能力与玩法

Microduck 的运动接口可以表达前后、横向和转向速度。在不同策略的支持下，它还可以完成坐下与起立、跌倒后起身、低头取物、踢球、前滚翻以及轮滑等动作。不过，接口能够表达某个方向，并不代表每一份策略都能稳定完成对应动作；实际能力取决于所加载的模型。

对于本次实验，最适合作为起点的是连续速度控制：控制端（云端管理控制台、手机应用等）通过 MQTT 持续发送前进速度和转向角速度，运动策略根据这些意图实时生成关节动作。一次性技能也可以通过 MQTT 触发，但应在完成基础速度控制、权限控制和安全机制后再逐步开放。

### 软件架构

Microduck 的软件可以理解为三个层次：

```
训练与策略：microduck_rl【MuJoCo / PPO / ONNX】
                         ↓
机器人运行时：robotd【观测 / 策略推理 / 安全 / 50Hz 控制】
                         ↓
硬件：电机 【IMU / 摄像头 / 音频 / ToF】
```

**在训练与策略层**，[microduck_rl](https://github.com/pollen-robotics/microduck_rl) 使用 [MuJoCo](https://github.com/google-deepmind/mujoco) 建立 Microduck 的数字模型。MuJoCo 是开源物理仿真器，可以模拟关节、执行器、重力及接触等动力学过程，使策略能够在虚拟环境中反复训练和验证。

Microduck 的步态通过强化学习获得。**策略（Policy）** 可以理解为一个从“观测”到“动作”的函数：

- 输入：机器人姿态、关节状态和目标速度等信息。
- 输出：下一控制周期的关节动作。

MuJoCo 执行动作并产生新的状态，奖励函数则根据机器人是否保持稳定、跟随目标速度等条件对结果进行评分。PPO（Proximal Policy Optimization）是训练该策略的强化学习算法。它根据策略与仿真环境交互产生的轨迹和奖励更新神经网络参数，并限制单次更新幅度以提高训练稳定性。经过反复优化，策略逐步学会将速度目标转换为协调的关节动作。

训练完成后，策略被导出为 ONNX 模型。ONNX 是一种开放的机器学习模型表示格式，用于保存神经网络的计算图和参数，使模型可以脱离训练框架独立部署。运行时只执行模型推理，不再进行 PPO 训练。

**在机器人运行时层**，robotd 以 50 Hz 读取 IMU 和关节状态、构造模型输入并执行 ONNX 推理，再将输出转换为经过滤波和安全限制的关节目标。

**在硬件层**，电机执行关节目标，传感器将新状态反馈给下一轮控制。在仿真中，MuJoCo 代替真实的执行器、传感器和物理环境，但仍采用相同的“观测—策略推理—动作”闭环。

本文引入的 MQTT 位于实时控制循环之外，只传递目标速度等运动意图，不直接操作关节或电机。运动策略负责将这些意图转化为步态。下面将首先在 MuJoCo 环境中接入 MQTT，以可视化方式验证完整的控制链路。

## 通过 MQTT 控制仿真机器人

下面使用开源工程 [hjianbo/microduck_demo_part1](https://github.com/hjianbo/microduck_demo_part1) 启动 Microduck 的 MuJoCo 仿真，并通过 Paho MQTT 发布速度命令。

### 架构及介绍

在本文的仿真实验中，MQTT 负责把第三方控制端产生的运动意图传递给 Microduck 策略。我们先了解这条控制链路和示例采用的消息格式，再动手启动仿真。

仿真控制链路由 Python 控制脚本、EMQX Broker 和 MQTT 仿真适配器组成：

1. Python 控制脚本，通过 MQTT 发布速度意图
2. EMQX Broker 转发消息
3. MQTT 仿真适配器，更新最新速度意图
4. Microduck ONNX 策略，生成关节动作
5. MuJoCo 仿真器执行

控制端不需要了解 MuJoCo 的步进逻辑，也不需要直接调用策略。只要使用同一会话生成的 Topic 和 Payload，就可以从另一台计算机或其他应用发送控制命令。

演示工程默认使用以下配置：

```
Broker: broker.emqx.io
Port: 1883
Topic: microduck/demo/{sessionId}/cmd/velocity
QoS: 0
Retain: false
```

> 初始化时，工程会生成随机 `sessionId` 并保存到本地 `.demo/session.env`。它用于避免不同读者在公共的 MQTT 服务器时产生冲突。

速度消息包含三个字段：

| **字段** | **含义**   | **单位** | **正方向** | **允许范围**                    |
| :------- | :--------- | :------- | :--------- | :------------------------------ |
| `vx`     | 前进速度   | m/s      | 向前       | 0 ～ 0.25                       |
| `vy`     | 横向速度   | m/s      | 向左       | 当前策略固定为 0                |
| `yaw`    | 转向角速度 | rad/s    | 逆时针     | -0.8 ～ 0.8，需与正向 `vx` 组合 |

例如，下面的消息表示以 0.25 m/s 的目标速度向前运动：

```json
{
  "vx": 0.25,
  "vy": 0.0,
  "yaw": 0.0
}
```

这些值表示运动意图，而不是对实际速度的绝对保证。本文固定的 `BEST_alpha_walking.onnx` 已验证能够前进和在前进中转弯，但不能可靠后退或原地转向；官方 Simulator 也明确禁用了横移输入。因此，演示工程只开放经过实际验证的动作组合。

> `broker.emqx.io:1883` 是公开、未加密的演示服务，所有消息都可能被其他用户看到，仅适合原型验证。生产环境应使用私有 Broker、TLS、独立设备凭证、Client ID 身份绑定和严格的 Topic 权限。

### 准备与启动

开始前，请准备 Git、Python 3.12、[uv](https://docs.astral.sh/uv/) 以及能够打开 MuJoCo 窗口的桌面环境。

克隆演示工程：

```shell
git clone --recurse-submodules \
  https://github.com/hjianbo/microduck_demo_part1.git
cd microduck_demo_part1
```

然后通过一个命令完成初始化：

```shell
./scripts/bootstrap.sh
```

初始化脚本会下载固定版本的 `microduck_rl` 和 Microduck Simulator，同步官方锁定的 Python 依赖，下载并校验 ONNX 行走策略，安装 Paho MQTT，并生成随机会话配置。重复执行该命令会保留已有的 `sessionId`。

在第一个终端启动仿真：

```shell
./scripts/run_simulator.sh
```

启动成功后，终端会显示 61 维策略输入、14 维动作输出、Broker 地址和当前会话 Topic，MuJoCo 窗口中则会显示 Microduck。

### 发送控制命令

在第二个终端发送一条持续三秒的前进命令：

```shell
./scripts/send.sh forward --duration 3
```

发送脚本基于 MQTT 协议，默认以 10 Hz 发布速度意图。除直行外，还可以在前进中向左或向右转弯：

```shell
./scripts/send.sh forward-left --duration 3
./scripts/send.sh forward-right --duration 5
./scripts/send.sh stop
```

例如，使用 `forward-right` 预设持续发送 5 秒速度指令：

![](https://assets.emqx.com/images/b74211ae073d8d44e4526b3c1f07ee23.gif)

需要调整速度和转向幅度时，可以覆盖 `vx` 与 `yaw`：

```shell
./scripts/send.sh forward \
  --duration 3 \
  --vx 0.2 \
  --yaw 0.5
```

发送端和仿真接收端都会检查参数。负向 `vx`、非零 `vy` 以及没有正向 `vx` 的纯转向命令会被明确拒绝，避免把当前策略无法可靠完成的动作呈现为受支持能力。

### 实现原理

示例工程没有改写 Microduck 的运动策略，而是在官方仿真程序外增加了一层 MQTT 适配。理解它可以从工程中的四个部分入手：

| **组成**       | **主要文件**                                     | **职责**                                                     |
| :------------- | :----------------------------------------------- | :----------------------------------------------------------- |
| 环境初始化     | `scripts/bootstrap.sh`                           | 拉取固定版本的子依赖、安装 Python 包、准备 ONNX 模型并生成会话配置 |
| MQTT 发送端    | `scripts/send.sh`、`send_velocity.py`            | 解析动作参数，使用 Paho MQTT 发布速度消息                    |
| MQTT 接收端    | `mqtt_control.py`                                | 订阅会话 Topic，解析 JSON，并保存最新速度意图                |
| 仿真适配运行器 | `build_runner.py`、生成的 `mqtt_infer_policy.py` | 将 MQTT 接收端接入官方 MuJoCo 推理循环                       |

执行 `bootstrap.sh` 时，脚本完成以下工作：

- 首先初始化 `microduck_rl` 和 Microduck Simulator 两个固定版本的子模块；
- 然后使用 `microduck_rl` 自带的锁文件安装依赖。由于仿真模型存储在 Git LFS 中，脚本还会下载指定版本的真实 ONNX 文件并校验 SHA-256，避免误把 LFS 指针文件当成模型加载；
- 最后，脚本在 `.demo/session.env` 中生成随机 `sessionId`，发送端和接收端都会读取这份配置，因此它们会自动使用相同的 Broker 和 Topic。

`send.sh` 是一个便于使用的脚本入口。它加载会话配置后：

1. 调用 `microduck-send` 命令；该命令实际对应 `send_velocity.py` 中的 Python `main()` 函数；
2. 程序连接 Broker，将 `forward`、`forward-left` 等预设动作转换为 `vx`、`vy` 和 `yaw`，编码为 JSON 后发布到当前会话的速度主题。发送端不导入 MuJoCo，也不会直接调用运动策略
3. 仿真端的 `mqtt_control.py` 连接成功后，它订阅同一个MQTT 主题；
4. 在 MQTT 网络线程中接收消息，完成 JSON 解析、字段检查和速度限幅，该线程只负责接收数据，不直接推进 MuJoCo，也不在网络线程中执行策略；
5. 把最新命令写入线程安全的 Mailbox。

MuJoCo 仿真和 MQTT 网络循环分别在不同的线程中运行。仿真控制循环每次迭代都会检查 Mailbox；发现新命令后，才把速度意图交给官方策略接口，以下为流程说明：


![](https://assets.emqx.com/images/aac2228c544c6598b315794c2252a2e3.jpg)


mailbox 只保存最新的速度意图，仿真循环不需要处理 MQTT 连接、JSON 或消息队列细节。这个边界也解释了为什么示例是真正的 MQTT 控制：发送脚本与 MuJoCo 之间没有直接函数调用，二者只通过 Broker 上的 Topic 交换消息。

为了保持示例可复现，工程不会直接修改上游子模块，而是由 `build_runner.py` 基于固定版本的官方 `infer_policy.py` 生成 MQTT 适配运行器。生成过程会检查预期的代码标记；如果未来上游脚本结构发生变化，初始化会明确失败并提示重新适配，避免在不兼容的代码上继续运行。

## 从边缘到边云协同：MQTTD + Device Agent

仿真实验验证了通过 MQTT 协议控制机器人的运动和方向。要把这套方式用于更正式的 Microduck 运行环境，还需要一个遵循现有运行时边界的设备端适配服务。本文将这个尚待实现的方案称为 `mqttd`。

目前在 Microduck 的官方规范中，是通过 `WebRTC` 建立统一的远程会话：

- 音视频通过 Media Track 传输；
- 远程控制请求通过可靠、有序的 DataChannel 发送；
- 高频遥测则通过低延迟、非可靠的 DataChannel 传输。

而且，官方的 [Remote Access Design](https://github.com/pollen-robotics/microduck/blob/main/docs/design/remote-access-design.md) 进一步规划了机器人账号、远程发现和 rendezvous 服务，使用户能够从局域网之外访问 Microduck。该方案目前仍处于持续演进阶段。

本文提出的 mqttd 并不是要取代 WebRTC，而是在现有本地控制接口之外增加一条 MQTT 接入路径，用于设备能力建模、状态上报、云端应用以及 Device Agent 集成。

### WebRTC vs. Device Agent

Device Agent 是由 EMQX 提供的产品，用于快速实现基于 MQTT + LLM 的自然语言设备控制、上报设备数据采集，以及通过语音等方式来实现设备的控制。与目前 Microduck 内置的基于 WebRTC 方案相比，Device Agent 具有以下优势，

1. MQTT 协议作为事实物联网标准协议，在数据上报，设备安全控制，低时延控制，以及设备管理和控制方面先天比 WebRTC 更具有优势；
2. Device Agent 实现了对机器人控制和数据上报的建模，让 LLM 对 Microduck 建立了清晰的上下文，通过自然语言可以准确地控制 Microduck；
3. Device Agent 通过更加轻量级的 WebSocket 协议实现了音、视频对接的能力，可以使用语音等方式直接跟 Microduck 进行聊天；
4. Device Agent 提供的 A2A 能力，可以让 Microduck 跟其他设备进行直接沟通，实现机器人对设备的聊天和控制，实现一些更有意思的场景。

本系列的下一篇文章将介绍如何使用 Device Agent + MQTTD 扩展来做一个更加丰富的场景。

## 总结

本文从 Microduck 的产品能力和软件架构出发，定义了一套简单的 MQTT 速度协议，并完成了环境初始化、Broker 连接和运动控制。本系列文章的下篇将介绍按照 Microduck 的标准扩展方式来实现扩展控制界面的适配服务 `mqttd`, 以及如何使用 EMQX Device Agent 快速地实现基于 LLM 的控制和语音等交互能力，甚至通过 A2A 协议实现设备之间的协作功能。

## **参考资料**

- 本文演示工程：[GitHub - hjianbo/microduck_demo_part1: Reproducible MQTT control demo for the official Microduck MuJoCo walking policy](https://github.com/hjianbo/microduck_demo_part1)
