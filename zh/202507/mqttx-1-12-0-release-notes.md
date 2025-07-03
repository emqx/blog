MQTTX 1.12.0 版本正式发布，带来了 **Copilot 2.0 功能**（集成 Gemini 2.5 Pro、Claude-4、GPT-4.1、o3/o4-mini、Azure OpenAI 等模型）。新版本通过**原生 MCP 集成**，可即时创建 AI 工作流；桌面端升级至 **Electron 33 和 Node 18**，响应更迅速；同时，命令行工具（CLI）现已支持发送精确大小的负载以进行压力测试。这一切为您的 MQTT 工具套件带来了一次重大的智能化升级。

> 点击下载最新版本：[https://mqttx.app/downloads](https://mqttx.app/zh/downloads)

## Copilot 2.0：多模型支持

Copilot 2.0 已在 MQTTX 内置多款主流 LLM：**Gemini 2.5（Pro）、Claude-4、GPT-4.1、o3/o4-mini** 与 **Azure OpenA**I 等。你可按工作流需要即时选用，并在同一会话中随时切换。

![image.png](https://assets.emqx.com/images/3a24f89b65e79f9224ec4aea9ce994bd.png)

### 快速脚本生成功能

需要为新的设备类型编写 Protobuf 或 Avro Schema，或想要一个用于随机生成遥测数据的 JavaScript 脚本？只需用自然语言描述需求，Copilot 即可返回可直接投入生产的代码块：包含校验、错误处理、行内注释与示例数据，在脚本页面即可使用。

### 智能数据模拟

Copilot 还了解常见 IoT 数据模式——传感器漂移、工作周期、异常峰值等，可生成逼真、可参数化的数据流，让后端像在真实场景中一样接受压力测试。通过自然语言调整数值范围、频率或离群比例，Copilot 会立即重新生成对应的模拟器。

### 实现 5 分钟工作流

1. **选择模型**（例如需要长链推理时可选 Claude-4）。
2. **提问**：「创建一个 JS 函数，模拟工业泵的压力、温度和随机故障码。」
3. **复制** 并将生成的函数粘贴到脚本面板。
4. **再提问**：「现在给我一个与该数据匹配的 Avro Schema。」
5. **发布** 到 MQTT Broker，实时查看包含真实异常的数据流。

Copilot 把原本数小时的手动脚本编写缩短为几分钟的对话操作，让你专注于验证业务逻辑，而非忙于构造测试数据。

![image.png](https://assets.emqx.com/images/2f1d5fdeef281a212ae7777aa967c6e4.png)

## MCP 集成

MQTTX 1.12.0 首次全面支持 Model Context Protocol（MCP），让 Copilot 通过统一、厂商无关的接口调用外部工具和数据源。

### MCP 的优势

- **为 AI 提供标准“USB-C”接口** —— Copilot 能在不暴露原始凭据的情况下访问本地或远程资源。
- **两种服务器模式** —— 可通过 stdio （本地进程）或 SSE （HTTP 端点）连接 MCP 服务器。
- **模型无关** —— 兼容 Copilot 2.0 支持的全部 LLM。

### 快速配置

1. 打开 **设置 → Copilot → MCP**。

2. 粘贴包含一个或多个服务器定义的 JSON，例如：

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/Users/you/Desktop",
           "/Users/you/Downloads"
         ]
       },
       "mqttx-sse": {
         "url": "http://localhost:4000/mqttx/sse"
       }
     }
   }
   ```

1. 保存。可用服务器将出现在列表中；使用开关即可启用或禁用各服务器。

### 工作流示例

| **场景**                                                     | **提示词**                                                   | **结果**                                                     |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **将代码写到磁盘**（filesystem 服务）                        | 写一个 JS 脚本，连接到 @connection，每秒发送一个随机温度，并保存为 /Users/you/Downloads/mqtt-demo.js | Copilot 会调用 filesystem 服务，并把包含正确连接字符串代码的文件写入磁盘 |
| **通过 AI 发布消息** ([MQTTX HTTP SSE server](https://github.com/ysfscream/mqttx-mcp-sse-server)) | 连接到 mqtt://broker.emqx.io:1883，然后将 “hello MCP” 发布到 testtopic/mcp | 订阅 testtopic/mcp 的所有客户端都会立即收到这条消息          |

### 状态与反馈

MCP 支持目前处于 Beta 阶段。我们正在尝试 “MCP-over-MQTT”，让原生发现和发布/订阅式工具调用更顺畅。欢迎体验，并告诉我们下一步想要哪些 AI 工作流！

![image.png](https://assets.emqx.com/images/9a7c6993f148e79d08abf784f91122d4.png)

## 桌面端增强

**升级运行时：**MQTTX 1.12.0 现采用 **Electron 33 + Node 18**，启动更快、内存占用更低，并带来最新安全补丁。

**工作区自动还原：**退出时会记录窗口大小和位置，重新打开即可回到上次的布局。

**更清晰的搜索：**输入关键字时，匹配词会在主题名和消息载荷中实时高亮，结果即刻显现。特别感谢社区贡献者 [**@muzaffarmhd**](https://github.com/muzaffarmhd)。

![image.png](https://assets.emqx.com/images/9c556027e163c3aca1825596205e643d.png)

在生产版里也能随时调出开发者工具，方便现场排查，使用**快捷键**

- Windows / Linux：按 **Ctrl + Shift + I**
- macOS：按 **Cmd + Opt + I**
- 或菜单 **View → Toggle Developer Tools**

面板打开后，切到 **Console** 标签页，重现问题，再把红色的错误或警告信息完整复制出来。

这个临时控制台能帮你快速定位白屏、渲染异常等 UI 奇怪现象，还能直接在接近生产的环境里查看网络请求和性能数据。

![image.png](https://assets.emqx.com/images/fa22bbf1da4d300bfe70878cbe23a63f.png)

## CLI 精确消息生成

在 1.12.0 版 CLI 中，你可以按**指定大小**发送消息：

- 订阅时会显示每条收到的 **消息大小**。
- 发布时可生成精确尺寸的随机消息，非常适合可重复的压测、带宽规划或 MQTT Broker 调优。

**参数**

-S, `--payload-size` <SIZE> — 生成指定大小的随机消息。

- 支持单位：B | KB | MB | GB（上限为 MQTT 规定的 256 MB）。
- 若同时使用 -m, -s, -M 或 --file-read，此参数将被忽略，以免覆盖手写消息内容。

**示例**

```shell
# 订阅主题并显示消息大小
mqttx sub -t demo
> topic: demo | qos: 0 | size: 12 B
> Hello World!

# 发布一条 1 KB 的随机消息
mqttx pub -t demo --payload-size 1KB

# 生成 512 B 和 2.5 MB 的消息
mqttx pub -t demo --payload-size 512B
mqttx pub -t demo --payload-size 2.5MB

# 压力测试：100 个发布者，各发送 1 KB 消息
mqttx bench pub -c 100 -t demo --payload-size 1KB
```

## 修复与优化

- **Copilot 预设指令快捷键 “/”**

  在任何 Copilot 对话框中按 /，即可调出内置命令菜单。最亮眼的是 **Generate Client Code**：一键生成 JavaScript、Python、Java、Go 等语言的 MQTT 客户端脚手架；需要其他语言也能随叫随到。

- **Monaco 编辑器恢复粘贴**

  现在脚本和消息内容都可以像往常一样复制 / 粘贴。

- **原生滚动条样式优化（Windows）**

  滚动条外观将自动匹配系统主题，更加一致。

- **搜索过滤器持久化并实时生效**

  设置一次过滤条件即可长期保留，并随新流量即时更新结果。

- **Copilot UI 小问题修复**

  解决了焦点跳转、闪烁和预设指令卡顿等现象，并清理了无用代码。

## Windows arm64 桌面用户注意

1.12.0 版本暂未提供专用的 arm64 安装包。请在下载页面选择 **Universal** 通用安装包，它可同时运行在 x64 与 arm64 系统上。

## 未来规划

- **MQTTX 2.0 重构** 正在进行
- **MCP over MQTT** 支持
- 桌面端与 CLI 的 **AI Agent 模式**
- **Payload 图表可视化增强 — MQTTX Viewer：**
  - **Diff 视图**：轻松比较不同消息或消息大小
  - **Dashboard 视图**：提供可自定义的 MQTT 活动概览，便于个性化洞察
  - **JSON 视图**：改进 JSON 格式数据的处理与展示
  - **系统主题视图**：专用于系统相关 MQTT 主题的视图
- **可配置断开属性（MQTT 5.0）支持**：通过可自定义的断开设置提升连接管理
- **IoT 场景数据模拟**：将该功能带到桌面端以简化 IoT 场景测试
- **Sparkplug B 支持**：扩展 MQTTX 功能以支持 Sparkplug B
- **MQTT GUI 调试功能**：新增特性来辅助调试 MQTT 通信
- **插件功能**：引入插件系统，支持 CoAP、MQTT-SN 等协议扩展
- **JSON Schema**：提供 JSON Schema 的编码与解码能力
- **脚本测试自动化（Flow）**：简化自动化测试流程的创建与管理



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://mqttx.app/zh/downloads" class="button is-gradient">免费下载 →</a>
</section>
