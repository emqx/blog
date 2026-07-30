Device Agent 0.4.0 现已发布。

新增基于 A2A 的多智能体编排，提供场景和任务两种用法：场景保存并重复运行一套协作流程，任务直接处理一次性协作需求。同时新增独立的定时任务管理页面、可复用的出站 Webhook，以及 HTTPS 直连访问。

## 功能更新

### A2A 多智能体编排

设备智能体在创建时启用 A2A 协作并发布卡片后，设备规格中的命令会成为可调用技能。打开 **A2A** 工作区，可以查看在线智能体及其技能，并基于这些智能体创建 **场景** 或执行 **A2A 任务**。

#### 场景：保存一套可重复执行的协作流程

以 A2A 列表中的 Humidifier、Smart Fan 和 Smart Lock 为例，在 **A2A → 场景** 中点击 **+**，填写：

- 场景名称：`离家模式`
- 目标：`出门前锁好门，并关闭风扇和加湿器`
- A2A 智能体：三个全选

![image.png](https://assets.emqx.com/images/48854f5fa58c298c407c7aaed51857dc.png)

创建后，Device Agent 会按三个智能体的技能拆分操作，并生成协作流程。目标里缺少必须确定的信息时，会先让你补充，再继续生成。

场景就绪后，在 **A2A → 场景** 的对话框里直接说：

```
我出门了
```

Device Agent 会匹配离家模式；如果多个场景都符合，会先问用哪一个。选好本次运行使用的设备后即可执行，并逐步查看每一步的状态。

![image.png](https://assets.emqx.com/images/3f9e6b4659cc1a8f94db66523caab8e4.png)

#### A2A 任务：直接执行一次临时协作

不需要保存成固定场景、但要多个智能体当场配合时，切换到 **A2A → 任务**，只描述想要的结果：

```
准备休息了，把家里安排妥当，安全、安静，湿度也舒服一点。
```

不用点名具体设备，也不用把目标拆成命令。拆解目标由 A2A 的 **Task Agent** 负责：它结合在线智能体公开的技能和当前状态，选参与者、拆步骤、定参数和执行顺序，生成本次的协作流程。

某一步有多台设备可用时，计划生成后页面会让你选本次使用的设备，也可以用输入框旁的设备按钮提前选。执行轨迹会显示 Task Agent 安排的步骤、每步状态和最终结果。任务不会保存成场景，下次执行会按当时的在线能力和设备状态重新安排。

![image.png](https://assets.emqx.com/images/c126be6e018d3b93a8fca867a59a0252.png)

### 定时任务管理页面

通过对话创建一次性、固定间隔或 `cron` 定时任务的能力此前已经提供。本版本新增独立的 **定时任务** 页面，已创建的任务不再只能回到原对话里找。

创建方式不变。在设备智能体工作区选中温控器后输入：

```
每天早上 9 点检查当前温度；如果高于 30°C，把目标温度设为 24°C。
```

任务会保存完整指令、调度规则、时区、设备智能体和设备范围。到期后 Device Agent 在独立会话中执行，不需要创建时的对话仍然开着。任务定义、执行上下文和运行记录都会持久化。网关重启后会恢复已启用任务的调度，已暂停的仍然暂停。

定时任务页面上可以：查看下次和上次执行时间；暂停或恢复任务；修改后续执行使用的指令；回到来源对话；取消不再需要的任务。**执行历史** 保存每次运行的状态、耗时、结果摘要或错误，可以继续打开详情和相关日志。

![image.png](https://assets.emqx.com/images/732f4b727254741649dec15df4dad979.png)

![image.png](https://assets.emqx.com/images/a8efef02017bfb9e502accd0382e3256.png)

### 可复用的出站 Webhook

以前要把目标 URL、Headers 和签名信息写进每条指令。现在在 **设置 → Webhook** 里配置一次并命名，之后由设备智能体和工作流按名称重复使用。下面的例子把它命名为 `operations-alerts`。

内置预设支持飞书、钉钉、Slack 和 Discord，其中飞书和钉钉可以使用对应的 HMAC 签名。其他 HTTPS 服务用自定义 Webhook，可以配置 JSON Body 模板、Headers 和可选的成功条件。保存时可以直接发一条测试消息，确认 HTTP 响应和目标平台是否收到内容。

![image.png](https://assets.emqx.com/images/3b884de733fdd3aa6659d136f8ad8bcd.png)

配置完成后，在对话中这样用：

```
通过 operations-alerts Webhook 发送“温控器 01 已离线，请检查电源和网络”。
```

也可以把同一个 Webhook 加进工作流，在设备上报告警后发送通知。工作流消息支持引用 `deviceId`、事件名称和 Payload 字段，适合把低电量、离线或异常事件推到已有的协作频道。

![image.png](https://assets.emqx.com/images/fd329f41b430528cb1115b5bb90878d0.png)

### HTTPS 直连控制台和 API

配置 TLS 证书和私钥后，Device Agent 控制台和 HTTP API 可以直接通过 HTTPS 访问。HTTPS 只提供传输加密，外网部署仍需配合身份认证和访问控制。

## 改进

- 改进聊天输入框的多行布局。输入变长时，操作按钮和输入区域会同步调整，切换到多行后高度不再滞后，减少遮挡和跳动。
- 清理设备 SDK 工具包中的冗余生成内容，下载包结构更简洁。

## 修复

- 修复网关重启后定时任务可能丢失设备智能体或设备执行范围的问题。
- 修复工作流切换或重新加载时可能短暂显示旧运行记录的问题。

## 升级前注意

- 多个 Gateway 共用同一数据库时，请先停止全部 0.3.x Gateway，再启动 0.4.0。不要让两个版本滚动混跑，否则同一个定时任务可能重复执行。
- 原 Marketplace 工作区已由 **A2A** 替代。把书签和集成地址从 `/workspace/marketplace` 改为 `/workspace/a2a`，旧路由不会自动跳转。
- 删除已废弃的 `VITE_FF_A2A_MARKETPLACE_ENABLE` 配置。

## 升级方式

macOS 和 Linux：

```
curl -fsSL https://emqx.sh/device-agent | sh
device-agent --version
```

Windows PowerShell：

```
irm https://emqx.sh/device-agent.ps1 | iex
device-agent --version
```

已安装的用户也可以直接更新：

```
device-agent update
```

升级后确认 `device-agent --version` 显示 `0.4.0`，再启动 Device Agent。


<section class="promotion">
    <div>
        立即体验 Device Agent
    </div>
    <a href="https://docs.emqx.com/zh/device-agent/latest/installation.html">Get Started →</a>
</section>
