## 引言：MQTTX 与 MCP 的融合

作为最受欢迎的 MQTT 客户端工具，MQTTX 在 1.12.0 beta 版本中集成了模型上下文协议（MCP）到 Copilot AI 功能中，显著提升了服务能力。这一融合让 MQTTX 转变为 MCP Host（也就是发起请求的 LLM 应用程序），支持 MQTTX Copilot 直接与 MQTT 服务（如 EMQX）和本地资源进行交互。这种将大语言模型（LLM）与 MQTT 操作相结合的方式，为物联网自动化、监控和开发带来了全新可能。

> *下载最新版本：*[Release v1.12.0-beta.2 · emqx/MQTTX](https://github.com/emqx/MQTTX/releases/tag/v1.12.0-beta.2) 
>
> *由于目前处于测试版本，应用不会自动更新。请从 Assets 部分手动下载并安装。*

## MCP 简介

[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)提供了 AI 模型与外部数据源或工具间的标准化接口，可以理解为「AI 应用的 USB-C 接口」。通过这一协议，MQTTX Copilot 可以实现以下功能：

- 访问训练数据之外的上下文信息。
- 与本地和远程系统进行安全交互。
- 在各种 AI 提供商间维持统一接口。
- 通过标准化工具调用实现特定功能。

MCP 基于客户端-服务器架构设计，Host 应用（比如 Cursor、MQTTX 等）内置 MCP 客户端，通过客户端连接到 MCP 服务器以提供特定功能。这种架构不仅确保了数据在用户自有基础设施中的安全存储，同时还支持强大的 AI 驱动工作流。

## MQTTX Host 功能实现概览

通过集成 MCP 客户端，MQTTX 成为 MCP Host，可以与各种 MCP 服务器连接，这一实现支持：

- SSE（服务器推送事件）和 Stdio（标准输入输出）两种 MCP 服务器类型。
- 通过 MQTTX 设置界面进行简单配置。
- 集成多种 AI 模型，包括 OpenAI GPT-4o、Claude 3.5/3.7、Grok 2 和 DeepSeek 等。
- 对特定模型提供「思维链」支持，实现高级推理能力。

配置过程非常简单，用户只需通过 MQTTX 设置面板，将 MCP 服务器设置为命令行进程或 HTTP 端点即可。

## 应用场景：MQTTX 中的 MCP 实践

让我们通过实例来探索如何在 MQTTX 中设置和使用 MCP：

### 在 MQTTX 中设置 MCP

1. 打开 MQTTX 并导航至左侧边栏的「设置」。
2. 启用 Copilot 功能并使用 API 密钥配置您偏好的 AI 模型。
3. 向下滚动至 MCP 部分并启用它。
4. 在提供的输入框中以 JSON 格式添加 MCP 服务器配置。
5. 添加配置后，可用服务器将显示在下方列表中。
6. 点击右上角的「连接」按钮，测试服务器连接。
7. 对于成功连接的服务器，您将看到可用工具列表。
8. 使用「禁用/启用」开关切换服务器状态。

![image.png](https://assets.emqx.com/images/7cdfb84d743eef8f23a070c3a7eae9a7.png)

### 本地文件系统集成

通过文件系统 MCP 服务器，Copilot 可以与您的本地文件交互，直接生成并保存代码到指定目录：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

具体工作流程示例如下：

1. 按照上述方式配置文件系统 MCP 服务器。
2. 在 Copilot 聊天框中，使用 `@connection` 关键词提取当前连接详情。
3. 要求 Copilot "为这个 MQTT @connection 生成 JavaScript 代码并将其保存到 /Users/username/Downloads 路径下，命名为 mqtt-test.js"。
4. AI 将使用 MCP 创建文件并保存到您指定的位置。

![image.png](https://assets.emqx.com/images/2d461afff3fad8c19b29fc2f37fd8f2c.png)

![image.png](https://assets.emqx.com/images/b136fdc8cc41247187e5750125e3781d.png)

在终端中使用 `cat mqtt-test.js` 命令可以验证代码已成功创建，并包含了正确的连接参数。

![image.png](https://assets.emqx.com/images/76da82c36c1951436483289b519b59f7.png)

这种方法通过消除「复制粘贴」的工作流程，极大地简化了开发过程：代码会直接生成并保存到您需要的位置，随时可以执行。

### 通过 MCP SSE 服务器进行 MQTT 操作

要通过 AI 直接执行 MQTT 操作，您可以部署自定义的 MQTTX MCP SSE 服务器（https://github.com/ysfscream/mqttx-mcp-sse-server）。 

```json
{
  "mcpServers": {
    "mqttx-server": {
      "url": "http://localhost:4000/mqttx/sse"
    }
  }
}
```

具体工作流程示例如下：

1. 在本地或云端部署 MQTTX MCP SSE 服务器。
2. 按照上述方式在 MQTTX 中配置服务器。
3. 在 Copilot 聊天框中，输入请求："连接到 mqtt://broker.emqx.io:1883 并向 testtopic/mcp 主题发布消息"。
4. 在另一个 MQTTX 连接中，订阅相同的主题。
5. AI 将通过 MCP 调用发布的消息，并实时显示在您的订阅窗口中。

![image.png](https://assets.emqx.com/images/0873eba7349d71f8db64c4d87a842c5b.png)

这一功能彻底改变了用户与 MQTT 服务的交互方式：用户无需再手动配置连接或发布消息，只需通过自然语言指令，即可让 MQTTX Copilot 自动执行操作。这一特性在快速 MQTT 交互测试、调试以及教学场景中展现出重要价值，极大提升了效率和易用性。

## 结论

将 MCP 整合到 MQTTX 是 EMQ 连接物联网与 AI 技术融合愿景中的关键一步。目前的 beta 版本已经实现让 AI 助手通过自然语言与 MQTT 服务交互，但我们的目标远不止于此。

EMQ 正在积极开发「MCP over MQTT」实现方案，旨在利用 MQTT 的服务发现和发布-订阅机制来突破现有 MCP 架构的限制。这些探索将为智能物联网通信奠定坚实基础，结合 MQTTX Copilot 的 AI 服务能力，未来将支持模式生成、连接诊断及测试数据创建等更多功能。

欢迎社区成员体验这些新功能并提供反馈，助力开发更友好、更强大的 MQTT 操作解决方案。

「构建物联网应用或集成 AI 到 MQTT 工作流程」欢迎与我们联系。

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
