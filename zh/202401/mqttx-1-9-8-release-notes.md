MQTTX 1.9.8 现已发布，新版本中 MQTTX CLI 新增了调试模式，这一功能增强了开发者的故障排查和分析能力。此外，更新也改进了 MQTTX AI Copilot 功能，为用户提供了更先进的基于 AI 驱动的 MQTT 交互支持。

> 点击此处下载最新版本：[https://mqttx.app/zh/downloads](https://mqttx.app/zh/downloads)

## MQTTX CLI - 调试模式

MQTTX 1.9.8 的调试模式由 MQTT.js 提供支持，让 MQTT 的调试流程更加简单。通过使用 `--debug` 开关来激活该模式，在连接、发布和订阅期间，提供实时日志，详细记录客户端的配置以及数据包处理情况。对于开发者来说，这个功能在理解和排查 MQTT 协议使用方面变得极其便利。

以 `mqttx conn -h broker.emqx.io -p 1883 --debug` 命令为例，来展示新调试模式的功能。该命令启动了一个详细的 MQTT 连接过程，其中显示的日志内容包括：

- 向 MQTT 代理发起连接的过程。
- 客户端设置，包括协议版本、保持连接时间和客户端 ID。
- 为 MQTT 通信设置和处理数据流。
- 发送诸如连接（connect）和心跳请求（pingreq）等数据包的过程。
- 包括数据包处理和响应检查在内的 MQTT 交互的实时监控。

这些细节有助于理解从建立连接到维护连接的整个 MQTT 通信生命周期，对于故障排查和高级 MQTT 使用至关重要。

![MQTT communication lifecycle](https://assets.emqx.com/images/c810a2e4e6a7442e6b51b5d72b14dbae.png)

## MQTTX Copilot 功能增强

MQTTX 1.9.8 版本中对 MQTTX Copilot 功能进行了优化改进：

- **流响应支持**：提高回答内容的响应速度和用户体验，使用户与 Copilot 的互动更加流畅和即时。

- **一键功能增强**：

  - **EMQX 日志分析**：用户现在可以一键分析 EMQX 日志，简化了日志审查过程。

    ![EMQX Log Analysis](https://assets.emqx.com/images/2543f9d9b788f131140b3e9d124276ac.png)

  - **复制 MQTT 客户端代码**：提高生成和使用 MQTT 客户端代码的效率。

    ![Copy MQTT Client Code](https://assets.emqx.com/images/caca6089bb96693d411612b8972c1113.png)

  - **插入 MQTT 测试数据**：现可轻松地将生成的 MQTT 测试数据插入到 Payload 编辑器中。

    ![Insert MQTT Test Data](https://assets.emqx.com/images/6ec2e4ff7f9974a3ef681d987e8707b9.png)

    ![Insert MQTT Test Data](https://assets.emqx.com/images/5457c7f755b79cdf0a6c0605fe21542b.png)

  - **多样化的 MQTT 测试数据生成**：自动创建和模拟多种真实场景下的 MQTT 测试数据。

    ![Diverse MQTT Test Data Generation](https://assets.emqx.com/images/e5b22a0a184443231010126f6e605adf.png)

  - **测试文档生成**：为当前 MQTT 连接自动生成测试文档。

    ![Test Documentation Generation](https://assets.emqx.com/images/8e95de89f6fbe59cd38ea9f22a7bd748.png)

  - **Copilot 用户设置**：为了实现对用户定制化和隐私的承诺，我们在 Copilot 中引入了一个新的设置。用户可以根据自己的喜好打开或关闭 Copilot 功能，提供对工具的更大控制，并确保本地测试数据的隐私保护。

    ![User Settings for Copilot](https://assets.emqx.com/images/32bb968de9b1c92712d8904cd9458bd0.png)

  - **消息发送优化**：优化 Copilot 内容输入框，实现通过 Enter 键实现更快的消息发送、Shift + Enter 实现换行。

  - **通过连接信息进行有效故障排除**：利用连接数据实现更高效的问题解决方案回答，简化当前测试环境中的故障排除过程。

  - **增强的 MQTT FAQ 提示**：包括额外的预设 MQTT FAQ 提示，为用户提供更好的指导和对 MQTTX 功能的理解。

## 其他

- **连接管理优化**：
  - 使用 echart 替换 chart.js，以增强流量统计的显示，提供改进的可视化效果。
  - 解决发送空认证信息的问题，提供了临时解决方案。
    - 已知问题：在 MQTT-v5 协议中，即使只设置了密码，MQTT-packet 库也错误地强制要求用户名，这与 MQTT-v5 支持的仅密码认证相矛盾。感谢 [JimMoen](https://github.com/JimMoen) 对 [mqtt-packet PR #148](https://github.com/mqttjs/mqtt-packet/pull/148) 中此问题修复的贡献。
- **OpenAI API**：调整 OpenAI API 中的温度值，以获得更准确的 Copilot 响应。

## 未来规划

在 MQTTX 1.9.8 之后的下一阶段开发中，我们将专注于提升可视化能力，并引入其他关键功能和改进。

- **Payload 图表可视化增强 - MQTTX Viewer**：
  - **主题树视图**：增强主题的组织和可视化。
  - **差异视图**：轻松比较不同的消息或负载。
  - **仪表板视图**：提供 MQTT 活动的可定制概览，以获取个性化洞见。
  - **JSON 视图**：改进 JSON 格式数据的处理和显示。
  - **系统主题视图**：专门针对系统相关 MQTT 主题的视图。
- **物联网场景数据模拟**：将此功能带到桌面客户端，以简化物联网场景测试。
- **Sparkplug B 支持**：扩展 MQTTX 功能，包括对 Sparkplug B 的特殊支持。
- **QoS 0 消息存储优化**：可配置选项以减少存储空间使用。
- **MQTT GUI 调试功能**：帮助调试 MQTT 通信的新功能。
- **插件功能**：引入支持协议扩展（如 CoAP 和 MQTT-SN）的插件系统。
- **Avro 消息格式支持**：对 Avro 消息格式的编码和解码能力。
- **脚本测试自动化（流程）**：简化自动化测试工作流的创建和管理。



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
