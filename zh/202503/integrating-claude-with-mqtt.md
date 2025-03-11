在飞速发展的物联网和消息传输领域，一个可靠、低延迟、可扩展的消息服务至关重要。作为 MQTT 解决方案的领导者，EMQ 提供了 [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)，帮助用户仅用几秒钟即可部署强大的 MQTT 服务。

近期，EMQ 推出了与大模型紧密通讯的 EMQX MCP Server，它是 [Model Context Protocol (MCP 协议)](https://www.anthropic.com/news/model-context-protocol) 的服务器实现。它将 Anthropic 的 Claude 等大型语言模型与 EMQX 连接，使 Claude 能够与 MQTT 消息服务交互。本文将为您介绍这一创新解决方案，并提供详细的使用教程。

![Send an MQTT Message From Cloud Desktop](https://assets.emqx.com/images/e6df4c662cf19fc4fc8b27fcc12fb3ab.png)

<center>Send an MQTT Message From Cloud Desktop</center>

## EMQX MCP Server 简介

![EMQX MCP Server Tools](https://assets.emqx.com/images/1ffdac5f3181b7752ad2272799f50197.png)

<center>EMQX MCP Server Tools</center>

<br>

EMQX MCP Server 是 Anthropic [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) 的实现，允许 Claude 与 EMQX MQTT 平台交互。它在 Claude Desktop（MCP 客户端）或其他 MCP 客户端（如 Cursor、Cline）与 EMQX MQTT 平台之间充当桥梁，使 Claude 能够实现以下能力：

- 列出和管理 MQTT 客户端
- 获取详细的客户端信息
- 在需要时断开客户端连接
- 向任何 MQTT 主题发布消息

这一集成利用 Claude 的自然语言处理能力，将其功能扩展到物联网和消息传递领域，为 AI 辅助的设备管理和监控开辟了全新可能。

EMQX MCP Server 可与任何支持 MCP 协议的 Agent 配合使用。例如，您可将其添加到 Cursor 中，通过聊天与开发环境中的 MQTT 服务器通信，从而在编码时实时测试和交互，提升开发效率和直观性。

将 AI Assistant 与 EMQX MQTT 平台集成具有以下重要意义：

- **自然语言物联网控制**：通过对话提示管理物联网设备和消息传递。
- **简化监控**：可要求 Claude 检查客户端连接并以易懂语言报告状态。
- **智能消息发布**：借助 Claude 编写消息并无缝发布。
- **降低使用门槛**：让非技术用户也能操作复杂的 MQTT 系统。
- **自定义 AI Agents**：EMQX MCP Server 可与其他 MCP 服务器结合，创建针对特定工作流程的个性化 AI Agents，用户可混合搭配功能（如数据库访问、MQTT 控制、API 集成等），无需编码即可构建满足独特需求的 AI Assistant。

## 使用教程

以下是如何使用 EMQX Serverless 设置 EMQX MCP Server 的步骤：

### **步骤 1：创建 EMQX Serverless 部署**

EMQX Serverless 提供免费试用，无需复杂设置，用户即可获取所有必需的 MQTT 消息服务功能。

1. 访问 [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)
2. 注册免费账户
3. 创建新的 Serverless 部署：
   - 点击“+ 新建部署”
   - 选择“Serverless”版本
   - 选择您想要部署的地区
   - 点击“创建”
4. 部署激活后，前往“概览”记录连接信息
5. 在“访问控制”→“客户端认证”下为 MQTT 客户端（如 MQTTX、设备或应用）配置认证
6. 创建 API 密钥（供 EMQX MCP Server 连接 EMQX）：
   - 前往“概览”，点击“+ 新建应用程序”
   - 点击“创建”生成 API 密钥和秘密
   - 安全保存这些凭据，后续需要使用

详情请参阅[官方文档](https://docs.emqx.com/en/cloud/latest/create/serverless.html)。

### **步骤 2：安装 Claude Desktop 应用**

EMQX MCP Server 支持任何兼容 MCP 的客户端，本教程以 Claude Desktop 应用为例：

1. 下载并安装 [Claude Desktop 应用](https://claude.ai/download)
2. 启动应用并使用 Anthropic 账户登录

### **步骤 3：设置 EMQX MCP Server**

有两种方法可以设置 EMQX MCP Server，本文我们选择更简单的 Docker：

1. 确保电脑已安装 Docker

2. 拉取 EMQX MCP Server Docker 镜像：

   ```shell
   docker pull benniuji/emqx-mcp-server
   ```

1. 找到 Claude Desktop 配置文件：

   - MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. 编辑配置文件添加 EMQX MCP Server:

   ```json
   {
     "mcpServers": {
       "EMQX_MCP_Server": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "-e", "EMQX_API_URL=https://your-emqx-cloud-instance.com:8443/api/v5",
           "-e", "EMQX_API_KEY=<YOUR-API-KEY>",
           "-e", "EMQX_API_SECRET=<YOUR-API-SECRET>",
           "benniuji/emqx-mcp-server"
         ]
       }
     }
   }
   ```

3. 用 EMQX Serverless 的实际信息替换环境变量：

   - `EMQX_API_URL`：部署的 API URL（在云控制台查看）
   - `EMQX_API_KEY`：创建的 API 密钥
   - `EMQX_API_SECRET`：对应的密钥

4. 保存配置文件并重启 Claude Desktop 应用

### **步骤 4：连接测试客户端到 MQTT Broker**

连接一个 MQTT 客户端以测试集成：

1. 安装 [MQTTX](https://mqttx.app/)
2. 使用云控制台的连接信息连接 EMQX Serverless 部署
3. 输入部署中配置的客户端 ID、用户名和密码
4. 连接并订阅主题 `test/topic`
5. 保持客户端运行

### **步骤 5：通过 Claude 与 MQTT 交互**

现在您可通过 Claude 与 EMQX MQTT 平台交互，以下是一些示例提示词：

1. 列出连接的客户端：

   ```
   Please list all clients currently connected to my MQTT broker.
   ```

1. 获取特定客户端详情：

   ```
   Can you show me detailed information about the client [CLIENT_ID]?
   ```

1. 发布消息到主题：

   ```
   Please publish a "Hello World" message to the topic "test/topic" with QoS 1.
   ```

1. 断开客户端连接：

   ```
   Please disconnect the client [CLIENT_ID] from the broker.
   ```

   

## 交互示例

**用户**：请列出连接到 EMQX MQTT 平台的客户端。

**Claude**：以下是当前连接的客户端：

- 客户端 ID：mqttx_2232bdb1
- 用户名：test
- 协议：MQTT v5
- …

当前有 1 个客户端连接。您想了解更多详情还是执行其他操作？

**用户**：是的，请提供此客户端详情。

**Claude**：以下是客户端 "mqttx_2232bdb1" 的详细信息：

- 基本信息：
  - 客户端 ID：mqttx_2232bdb1
  - 用户名：test
- 连接详情：
  - 已连接：是
  - 创建时间：2025-03-02T05:29:51.103+00:00

您想对此客户端执行什么操作？例如发送一条消息到主题或者断开客户端连接？

**用户**：请写一首诗并以 QoS 1 发送到主题 '/poem'。

**Claude**：我已将以下诗歌以 QoS 1 发布到主题 '/poem'，消息 ID 为：00062F55A1EFB1156ABC481240B30000：

> *Signals in the ether,*
>
> *Invisible threads that bind,*
>
> *Devices speak in whispers,*
>
> *Across the digital divide.*
>
> *Messages like leaves falling,*
>
> *From cloud to waiting ground,*
>
> *Connected yet untethered,*
>
> *Where silence makes no sound.*
>
> *Brokers of the modern age,*
>
> *Routing dreams from here to there,*
>
> *In this web of connections,*
>
> *We find ourselves everywhere.*
>
> *Like stars in constellation,*
>
> *Each point of light has worth,*
>
> *The language of machines,*
>
> *Redefining our Earth.*

您还想执行其他操作吗？

## **更多可能**

EMQX MCP Server 还可实现更多高级应用：

- **物联网设备管理**：让 Claude 检查设备状态、断开问题设备或发送配置更新。
- **监控仪表板**：定期检查客户端连接并以自然语言报告。
- **系统集成**：将 Claude 作为消息基础设施的对话接口，便于非技术用户使用。
- **测试与调试**：发布特定负载的测试消息以排查问题。
- **智能家居控制**：通过对话提示控制家庭自动化设备。
- **数据管道编排**：结合多个 MCP 服务器实现复杂工作流程，例如：

```
用户：“请分析昨天 PostgreSQL 数据库中的温度数据，并将摘要发布到 'reports/temperature' 主题。”

Claude：“我已分析数据，平均温度 22.3°C，峰值 27.8°C（下午 2:15），凌晨 3-4 点发现异常波动 ±3°C。我已将分析和 JSON 数据以 QoS 2 发布到主题，启用保留功能，仪表板可显示此信息。”
```

这一工作流程展示了 Claude 的以下能力：

- 从数据库中查询复杂数据
- 应用分析推理来识别模式和异常
- 将结果以适当的格式呈现给不同受众（人类可读的摘要和机器可读的 JSON）
- 通过 MQTT 将这些洞察分发给下游应用
- 所有这些都由一个自然语言请求触发

## EMQX Serverless：MQTT 与大语言模型集成首选

EMQX Serverless 的以下优势使其成为此集成的理想平台：

- **零基础设施管理**：无需维护服务器或担心扩展问题。
- **免费额度**：无需前期成本即可开始。
- **即时部署**：几分钟内运行 MQTT 服务。
- **可扩展性**：随需求增长无缝扩展。
- **企业级功能**：提供认证、访问控制和监控等强大功能。

## 结语

EMQX MCP Server 将对话 AI 与物联网消息传递相结合，通过结合 Claude 的自然语言能力和强大的 EMQX MQTT 平台，为与设备和系统的交互带来新可能。无论您是希望简化设备管理的开发者、寻求直观监控工具的管理员，还是探索 AI 与物联网前沿的爱好者，EMQX MCP Server 都为您提供了与 MQTT 生态系统交互的新方式。

立即体验 EMQX Serverless，开启对话式物联网控制的未来！



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
