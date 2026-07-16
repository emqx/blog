[Device Agent](https://www.emqx.com/zh/device-agent) 0.3.0 于 2026 年 7 月 1 日发布，主要新增了以下功能：

- 通过自然语言为 Device Agent 构建工作流：设备上报状态、事件、命令响应或校验错误后，可以自动记录事件、下发命令、发布 MQTT 消息，或交给 Agent 继续处理，并在控制台查看每次执行结果；
- 设备智能体个性设置，增加设备智能体返回文本的个性化、趣味性和多样性；
- 模拟器事件上报，用于快速测试工作流和智能体行为；
- 新增了基于 VSS 的智能座舱示例，以及其他多项功能改进。

## 功能更新

### 自然语言构建工作流，以及工作流可视化

0.3.0 新增工作流能力，用于关联设备事件和后续处理。比如在设备低电量、传感器告警、命令失败、设备离线恢复等情况发生时，可以记录事件、下发命令、发布 MQTT 消息，或交给 Agent 下一步处理。

工作流页面提供图形视图、启停控制和全屏查看。触发条件、节点关系和后续动作可以在图上直接查看，更容易理解一条自动化任务实际会怎样运行。

![image.png](https://assets.emqx.com/images/b701d3294e63f53bd7a7eea1fe9f9aca.png)

以上图的车机低电量场景为例：设备上报 `battery_low_warning` 事件后，工作流先记录告警，再根据电量和剩余续航判断处理方式。普通告警可以发布 MQTT 消息通知外部系统；严重低电量时，可以同时下发节能模式命令，并让 Agent 给出后续建议。

![image.png](https://assets.emqx.com/images/6ad4997c12f3484430c0f53e397c28ff.png)

通过自然语言创建工作流，输入以下内容：

```
创建名为 battery-low-range-guard 的工作流：
当当前设备上报 battery_low_warning 事件时，先记录一条 device_event，detail 包含 soc、estimated_range_km 和 deviceId。
如果 payload.soc 小于 20，向当前设备下发 set_drive_mode 命令，将 mode 设置为 eco，并让 Agent 生成一条简短处理建议。
如果 payload.soc 不低于 20，但 payload.estimated_range_km 小于 80，向 device-agent/alerts/range 发布一条 MQTT 提醒。
```

工作流也支持分支节点，可以按电量区间、错误码、设备状态或命令结果拆成不同处理路径，让同一类事件不必只走固定动作。

每次触发后，Device Agent 都会保存运行记录，包括时间、状态、耗时、触发事件、设备 ID 和步骤结果。排查事件没有触发、命令没有下发、分支没有命中时，可以直接从记录里看到实际执行路径。

![image.png](https://assets.emqx.com/images/77b6f9e54391305ec6cd04dfb24c73c3.png)

### 设备智能体个性化设置

该功能主要用于设备智能体在组织回复文本时，按照用户的设置给用户组织更具有个性化的语言，比如儿童玩具、医疗健康等需要特定语义回复的场景。在创建设备智能体后的预览面板中，点击 **个性 → 设置**，可以设置回复风格，例如“先给结论，语气简洁”。设置后，设备相关回复会按同一风格输出，比如先说明结果、减少无关寒暄、优先给出下一步操作。

个性设置只影响表达方式，不会改变 DeviceSpec、设备命令或权限边界。

![image.png](https://assets.emqx.com/images/95bfa9c1e89823d562903ccb95844644.png)

### 模拟器事件上报

浏览器模拟设备现在可以主动上报事件，并编辑 Payload。处理设备事件时，可以直接在控制台构造上报内容，观察设备状态、最近事件和工作流触发结果。

这减少了手动准备 MQTT 消息的步骤，也方便复现某一次设备上报。

![image.png](https://assets.emqx.com/images/5a34049e3068195d03ad27265ee39f3c.png)

### VSS 车载示例

0.3.0 新增基于 VSS 的车载示例，覆盖座舱续航、空调和场景模式等方向。上面的截图使用的是 `Smart Cockpit Range` 示例。

## 改进

- 优化日志页布局，并记住左右分栏宽度，调试 MQTT、设备事件和工作流时更容易定位问题。
- 更新智能体模型选择：
  - Qwen 新增 `qwen3.7-plus`、`qwen3.7-max`；
  - Kimi / Kimi Coding 新增 `kimi-k2.7-code`、`kimi-k2.7-code-highspeed`、`kimi-k2.6`、`kimi-k2.5`、`kimi-k2-thinking`；
  - Anthropic 新增 `claude-opus-4-8`。
- 更新视觉模型选择：
  - DashScope 新增 `qwen3-vl-plus`、`qwen3-vl-flash`。
- 改进远程连接信息展示，语音和 MQTT 连接状态更容易确认。
- 改进未选择设备类型时的命令目标选择，降低手动下发命令时选错对象的概率。

![image.png](https://assets.emqx.com/images/73233d93b69c7d89a7dec1dab85dd0ec.png)

## 修复

- 修复浏览器模拟器 MQTT 注册时机问题，模拟设备接入更稳定。
- 修复 SDK 包生成后无法正常下载的问题。

## 升级方式

macOS 和 Linux：

```
curl -fsSL https://emqx.sh/device-agent | sh device-agent --version
```

Windows PowerShell：

```
irm https://emqx.sh/device-agent.ps1 | iex device-agent --version
```

已安装的用户也可以直接更新：

```
device-agent update
```

升级后启动 Device Agent，打开控制台即可使用 0.3.0。
