MQTTX 1.10.1 版本现已发布！

本次更新带来了一系列提升用户体验的重要功能，主要包括：

- 通过桌面应用一键安装 MQTTX 命令行工具；
- 增加对自定义 AI Copilot API 的支持，为中国区域内的用户提供内置的 Moonshot LLM API；
- 迁移新的 Web 客户端地址。

> 下载最新版本：[https://mqttx.app/zh/downloads](https://mqttx.app/zh/downloads)

## 一键安装 MQTTX CLI

从 1.10.1 版本开始，MQTTX 桌面客户端支持一键安装 MQTTX 命令行工具。用户可以通过一个友好的图形界面轻松自动完成下载和安装过程，避免了手动下载和配置的麻烦。这一功能确保用户能够轻松获取最新版本的 MQTTX CLI。

**安装步骤：**

1. 进入设置页面，找到 MQTTX CLI 部分并点击安装按钮。
2. 或者，可以从顶部菜单选择“安装 MQTTX CLI”选项。
3. 点击后，客户端将自动下载并安装所需的系统软件包。您可能需要输入管理员密码以授予安装权限。
4. 安装完成后，您可以在任意命令行窗口中使用 `mqttx` 命令。

> **注意：** 对于 Windows 用户，点击安装后，您需要手动下载 MQTTX CLI 可执行文件并在相应目录中使用。

![一键安装 MQTTX CLI](https://assets.emqx.com/images/71a4c60eda5073fc7416994e04608eaa.png)

![一键安装 MQTTX CLI 2](https://assets.emqx.com/images/6dbe3b020f60b8beef42cceb7d7855d1.png)

![连接到服务器](https://assets.emqx.com/images/aac57a3cc3b33f5977e10168527d305a.png)

## 支持自定义 AI Copilot API

在之前的版本中，MQTTX Copilot 仅限于使用内置的 OpenAI API。

从 v1.10.1 开始，我们更新了这一策略，允许用户自定义 AI 服务的 API endpoint 和模型。只要 API 符合 OpenAI 格式，MQTTX Copilot 就能支持各种生成式 AI LLM。这一灵活性使用户能够输入他们的 API 密钥、主机 API 和支持的模型，集成各种 AI 服务，并在 MQTTX 中提供增强和个性化的 AI 功能。用户可以轻松切换不同的 AI 提供商和模型，根据他们的需求和偏好定制 Copilot。

![自定义 AI Copilot API](https://assets.emqx.com/images/db636c0504b80edededf73cefca9a772.png)

该功能来自社区用户 [@ni00](https://github.com/ni00) 的贡献。

### 提供内置的 Moonshot（月之暗面）API

MQTTX Copilot 现在支持内置的 Moonshot API，为中国区域内的用户提供增强的 AI 功能。用户只需获取 Moonshot API 密钥并在设置页面中输入，即可选择兼容的 Moonshot 模型并开始使用。目前支持的模型版本包括 moonshot-v1-8k、moonshot-v1-32k 和 moonshot-v1-128k。配置完成后，用户可以利用这些强大的模型来提升他们的 MQTTX Copilot 体验，包括一键生成测试客户端代码、测试数据等。

### 其它支持的模型

MQTTX Copilot 还支持其他推荐的模型，用户可以根据需求选择：

- **Zhipu**：通过 API 文档 https://open.bigmodel.cn/  获取相关信息并配置支持的模型，如 glm-4-0520、glm-4、glm-4-air、glm-4-airx 和 glm-4-flash。
- **DeepSeek**：通过 API 文档 https://www.deepseek.com/zh  获取相关信息并配置支持的模型，如 deepseek-chat 和 deepseek-coder。

![支持的模型](https://assets.emqx.com/images/d21e4492939d72901cdab916c6081ec8.png)

## 迁移 MQTTX Web 地址

我们再次迁移了 MQTTX Web 在线地址至 [https://mqttx.app/web-client](https://mqttx.app/web-client) ，以提高安全性和合规性。

**影响：**

- WebSocket 连接现在必须使用安全 WebSocket (wss://) 代替 ws://。
- 用户需要更新他们的 WebSocket 连接配置。

**解决方案：**

- 下载 MQTTX 桌面版或 CLI 版本。
- 考虑私有化部署 Web 客户端。

详细信息请参阅我们的[迁移公告](https://www.emqx.com/zh/blog/mqttx-web-migration-announcement#why-migrate)。

同时，我们增加了数据收集政策。如果您对数据收集有任何疑问，可以在关于页面中查看详细信息。

![数据收集声明](https://assets.emqx.com/images/53bbea720a85c28eb1218ab691a76810.png)

## 配置文件中指定默认协议

MQTTX 现在允许用户在配置文件中设置默认协议。用户可以选择 WebSocket (ws, wss) 或 MQTT over SSL (mqtts) 等协议作为默认选项，从而避免每次连接时都需手动指定协议的麻烦。

要进行配置，请使用 `mqttx init` 命令并选择您首选的默认协议。

该功来自社区用户 [@rpendleton](https://github.com/rpendleton) 的贡献。

![配置文件中指定默认协议 1](https://assets.emqx.com/images/a478bace38457ffa64d42678c75a3bf2.png)

![配置文件中指定默认协议 2](https://assets.emqx.com/images/8d17eb132a2365d7684668b962b6ecc9.png)

## 其他更新

**新功能和改进**

- **改进桌面端备份导入进度**：支持导入大备份文件并显示进度条。
- **在桌面端显示加载数据错误**：桌面应用现在清晰显示加载数据时遇到的错误，帮助用户快速识别和解决问题。
- **支持在加载连接错误时重建数据库**：提供在发生加载连接错误时重建数据库的选项。
- **在 CLI 订阅输出中突出显示订阅信息**：CLI 已增强以在输出中突出显示订阅信息，使管理和跟踪订阅更容易。

**错误修复**

- **修复桌面端重新订阅问题**：解决了导致重新订阅问题的错误，提高了桌面应用的可靠性。
- **修正 CLI 发布消息格式的数据转换问题**：修复了 CLI 在发布特定格式消息时导致数据转换错误的问题。

这些更新着重于改善用户体验，增强功能，并修复关键错误，以确保 MQTTX 更顺畅和可靠的操作。

## 未来规划

- **Payload 图表可视化增强 - MQTTX Viewer**：
  - **主题树视图**：增强主题的组织和可视化。
  - **差异视图**：轻松比较不同的消息或负载。
  - **仪表板视图**：提供可定制的 MQTT 活动概览，以获取个性化洞见。
  - **JSON 视图**：改进 JSON 格式数据的处理和显示。
  - **系统主题视图**：专门针对系统相关 MQTT 主题的视图。
- **支持可配置的断开连接属性（MQTT 5.0）**：通过自定义断开连接设置来增强连接管理。
- **物联网场景数据模拟**：将此功能带到桌面客户端，以简化物联网场景测试。
- **Sparkplug B 支持**：扩展 MQTTX 功能，包括对 Sparkplug B 的特殊支持。
- **QoS 0 消息存储优化**：提供可配置选项，减少存储空间使用。
- **MQTT GUI 调试功能**：帮助调试 MQTT 通信的新功能。
- **插件功能**：引入支持协议扩展（如 CoAP 和 MQTT-SN）的插件系统。
- **Avro 消息格式支持**：增加对 Avro 消息格式的编码和解码能力。
- **脚本测试自动化（流程）**：简化自动化测试工作流的创建和管理。

 

<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://mqttx.app/zh/downloads" class="button is-gradient">免费下载 →</a>
</section>
