[MQTT 5.0 客户端工具](https://mqttx.app/zh) MQTTX 近期推出了 1.9.7 版本更新。此次更新的一大亮点是引入了 **MQTTX Copilot**，全新的 MQTT AI 助手，为用户提供更方便、快捷的使用体验。AI 助手能增强用户互动，帮助用户更深入理解并使用 MQTT 和 EMQX。更新还包括多项错误修复，显著提升整体用户体验。

> 点击此处下载最新版本：[https://mqttx.app/zh/downloads](https://mqttx.app/zh/downloads)

## MQTTX Copilot

MQTTX Copilot 是专为解决 MQTT 相关问题而设计的 AI 助手。它为用户提供了常见问题的解决方案和最佳实践见解，帮助用户更好地使用 MQTTX 和 [EMQX](https://www.emqx.com/zh/products/emqx)。通过 Copilot，用户可以测试 MQTT 连接、发布和订阅主题、进行调试，以及开发 MQTT 应用与服务。不仅简化了操作流程，还丰富了用户的 MQTT 使用体验。

![MQTTX Copilot](https://assets.emqx.com/images/bdeccbc17b7f10b7cab98b9b811d0be9.png)

### 开始使用前的准备

MQTTX Copilot 功能由 OpenAI 的 GPT 模型驱动，因此在使用前，您需要在 MQTTX 的设置界面底部配置 OpenAI API 密钥才能启用此功能。如需获取 OpenAI 的 API 密钥，请参考 [OpenAI API Key](https://platform.openai.com/api-keys) 页面。

根据您的具体使用需求，您还可以选择合适的 GPT 模型版本，如 GPT-3.5 或 GPT-4。请确保所选模型与您的 OpenAI API 密钥相匹配。

![配置 OpenAI API 密钥](https://assets.emqx.com/images/eba0654f14045c75ee542575b1a42c90.png)

### 一键错误分析

在连接或订阅过程中遇到错误时，您可以快速点击错误提示框中的「Ask Copilot」按钮。激活后，MQTTX Copilot 将协助您分析问题的可能原因，并帮助您逐一检查和排查，以便准确地识别并解决错误。

![Ask Copilot](https://assets.emqx.com/images/66f4028a0d08d97a4fa39e96206395b2.png)

![MQTTX Copilot 问题解答](https://assets.emqx.com/images/d7360e7dd3245c4e217109558bbbdcdb.png)

### AI 驱动的代码生成器

MQTTX Copilot 现提供一键生成 MQTT 客户端代码，并适配和使用您当前的测试连接。此功能极大地简化了在各种编程语言中设置 MQTT 客户端的过程。目前，MQTTX Copilot 支持为多种语言生成代码，包括JavaScript、Python、Java、Golang 等等。这一功能确保了更加流畅、高效的开发过程，使用户更容易将 MQTT 集成到他们的项目中。

![一键生成 MQTT 客户端代码](https://assets.emqx.com/images/09f21a76879996112997e81f08c5a96f.png)

### MQTT 常见问题解答与 EMQX 教程

MQTTX Copilot 为用户提供了关于 MQTT 常见问题的提示和指导，以及关于安装和使用 EMQX 的全面教程，增强了用户在 MQTT 和 EMQX 方面的知识和熟练度，提供了一体化的学习体验。

![MQTT 常见问题解答与 EMQX 教程](https://assets.emqx.com/images/a90de902860234152328289e1de82714.png)

### 自动化测试数据生成

MQTTX Copilot 简化了测试载荷的生成过程，使用户能够快速分析和优化 MQTT 数据实现。

![自动化测试数据生成](https://assets.emqx.com/images/fe025f077a83c9969161e43973f4e635.png)

### 当前连接配置分析

只需一键，MQTTX Copilot 就能分析并解读您的连接配置，提供对 MQTT 连接配置的深入见解。这一功能帮助用户理解他们的连接细节，使得 MQTT 连接的使用和管理更加高效。

![连接配置分析](https://assets.emqx.com/images/9920b4bedd1dec4da1be745cef5c7c86.png)

除了上述功能之外，MQTTX Copilot 还允许用户自定义编辑提示信息，并通过使用 `@connection` 关键字快速访问连接的相关信息。这使得用户能够进行定制化设置，并且为即将推出的其他功能提供支持，如主题管理、Payload 自动填充以及 EMQX 日志分析等，增强 MQTTX Copilot 的使用体验。

## 修复和改进

此外，MQTTX 1.9.7 版本还包含了多种优化和修复：

### JSON 数据精度丢失问题（Desktop、CLI、Web）

我们提高了 JSON 消息中的数据精度。修复并解决了 JSON 消息中数据精度丢失的问题，确保了长数字型数据的准确表示。（支持 BigInt）

![JSON 数据精度丢失问题](https://assets.emqx.com/images/eb23a741042e945896f35874fa1f7a6f.png)

### 优化 SSL 证书选项的名称 (Desktop)

优化了 SSL 证书选项，明确区分了 CA 签名的服务器证书和 CA 或自签名证书，使选项名称更加清晰，便于用户理解和选择。

![优化 SSL 证书选项的名称](https://assets.emqx.com/images/76a82dcf2823d146184dbef445cb1f7c.png)

### Topic-Alias 问题修复（Web、CLI）

解决了 Web 和 CLI 连接中 topic-alias 的最大值错误。此修复确保了 MQTTX CLI 能够正确接收带有主题别名的消息，并且解决了设置最大主题别名不生效的问题。

### 其他修复和改进

- **重连问题修复（桌面版）：** 解决了断开连接后无限重连的问题。
- **移除未使用的占位符（桌面版）：** 清理了代码和页面中无效的占位符。
- **翻译更新（桌面版、Web）：** 改善了特定语言的翻译。
- **错别字修正（桌面版）：** 更正了文档和代码中的错别字。
- **Web README 文档更新：** 改善了 MQTTX Web 的 README 文档。

## 特别感谢

感谢 [@ni00](https://github.com/ni00) 解决了 JSON 精度和主题别名等关键问题，以及 [@Rotzbua](https://github.com/Rotzbua) 在 MQTTX 中对文档和工程化问题的修复。

## 未来规划

- **MQTTX Copilot 功能增强：** 升级以包含流输出、Payload 自动填充、Payload 的数据分析，以及根据提示信息自动创建连接和订阅主题等。
- **IoT 场景数据模拟：** 将此功能同步到桌面客户端，简化 IoT 场景的测试。
- **Sparkplug B 支持：** 扩展 MQTTX 的功能，以包括对 Sparkplug B 的支持。
- **QoS 0 消息存储优化：** 通过可配置选项减少存储空间的使用。
- **MQTT 调试功能：** 引入协助用户调试 MQTT 通信的功能。
- **自动图表绘制：** 将接收到的消息自动转换为图表，便于更直观的分析。
- **插件功能：** 推出支持诸如 CoAP 和 MQTT-SN 等协议扩展的插件系统。
- **Avro 消息格式支持：** 引入 Avro 消息格式的编码和解码功能。
- **脚本测试自动化（流程）：** 简化自动化测试工作流的创建和管理。



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
