MQTTX 1.12.1 带来了重要的安全更新，包括全平台支持的 SCRAM 增强认证、修复了消息显示中的 XSS 漏洞、更新了 2025 年最新的 AI 模型，以及关键的稳定性改进——全面提升生产和测试环境的安全防护能力。

> 点击下载最新版本：[https://mqttx.app/downloads](https://mqttx.app/downloads)

## SCRAM 增强认证

MQTTX 1.12.1 在桌面端、命令行和 Web 端全面支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 的 **SCRAM（安全认证机制）** 增强认证。

SCRAM 采用加密验证方式保护密码安全，凭证不会以明文传输，每次会话都使用唯一的随机数和盐值，有效防止重放攻击。

### 在 EMQX 中启用 SCRAM

在 MQTTX 中使用 SCRAM 之前，需要先在 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)上启用它。以 EMQX 为例：

1. 进入**认证**设置页面

2. 创建新的认证器，选择 **SCRAM** 作为认证机制

   ![image.png](https://assets.emqx.com/images/8be81d67f6974ad1d15f92a6f416cbeb.png)

1. 配置用户数据库（内置数据库或 HTTP 服务器）

   ![image.png](https://assets.emqx.com/images/0a0dd5e9f9565af606379ab59d1b2593.png)

4. 选择哈希算法（sha256 或 sha512）

5. 添加用户和密码

### 配置方式：桌面端和 Web 端

具体步骤如下：

1. 打开连接设置
2. 选择 **MQTT 5.0** 协议（默认）
3. 在**认证**区域，选择 **SCRAM** 作为认证方式
4. 选择哈希算法：
   - **SCRAM-SHA-1**：兼容较旧版本的服务器
   - **SCRAM-SHA-256**：安全性和性能兼顾（推荐）
   - **SCRAM-SHA-512**：高安全性环境的最佳选择
5. 输入用户名和密码
6. 点击连接——MQTTX 会自动完成认证流程

![image.png](https://assets.emqx.com/images/6caabd18b78605800f082e5b6bb8712c.png)

### 配置方式：命令行

使用新增的 `-am` 或 `--authentication-method` 参数进行连接：

```shell
# 使用 SCRAM-SHA-256 连接（推荐）
mqttx conn -h broker.emqx.io -p 1883 -am SCRAM-SHA-256 -u username -P password

# 高安全环境使用 SCRAM-SHA-512
mqttx sub -t 'sensor/#' -h broker.emqx.io -am SCRAM-SHA-512 -u admin -P secure_pass

# 兼容旧版服务器使用 SCRAM-SHA-1
mqttx pub -t 'device/data' -m 'hello' -am SCRAM-SHA-1 -u device01 -P device_password
```

SCRAM 特别适用于需要关注密码存储和网络安全的生产环境，能够与 EMQX 及其他支持增强认证的 MQTT 5.0 服务器无缝集成。

## 安全：修复 XSS 漏洞

本版本修复了消息显示中潜在的 **XSS（跨站脚本攻击）漏洞**。旧版本可能会执行 MQTT 消息中嵌入的恶意 HTML 或 JavaScript 代码，导致用户面临代码注入攻击的风险。

**修复内容** – 现在所有接收到的消息内容在显示前都会进行转义处理。包含 HTML 标签、`<script>` 代码块或事件处理器的消息将以纯文本形式显示，不会被应用解析执行。

**影响范围** – 如果您在不受信任的环境或多租户场景中使用 MQTT 服务器，消息内容无法完全可控，**强烈建议**尽快升级到 1.12.1 版本。

## AI 模型更新

Copilot 现已支持 2025 年最新的 AI 模型：

- **OpenAI**：GPT-5、GPT-5-mini、GPT-5-nano
- **Anthropic**：Claude Opus 4.1、Claude Sonnet 4.5
- **xAI**：Grok 4 系列（稳定版）
- **Google**：最新 Gemini 模型

可以根据不同任务切换模型——快速编写脚本时使用轻量级模型，进行复杂的协议问题分析时使用更强大的模型。

## 桌面端改进

### 流式导出

大量消息历史记录导出时现在采用流式写入方式，不再将所有内容一次性加载到内存中，避免了导出成千上万条消息时出现的卡顿和崩溃问题。

### 用户体验优化

**长主机名显示** – 当连接名称包含较长的服务器地址时，会自动使用省略号显示，鼠标悬停时可以查看完整内容。

**消息导航优化** – 重新设计了历史消息前进/后退按钮的布局，浏览之前的消息更加直观便捷。

![image.png](https://assets.emqx.com/images/6efb51b2454db55eb4c5544abd212bbd.png)

**搜索高亮修复** – 修复了搜索关键词高亮显示的逻辑问题，现在即使搜索参数为空或包含特殊字符也能正常工作。

![image.png](https://assets.emqx.com/images/a9975a292a2d60c0c8d308a81e648d8e.png)

### 显示问题修复

**窗口恢复** – 修复了在外接显示器断开后（拔掉显示器或合上笔记本）重新打开 MQTTX 时出现的崩溃问题。

**Windows 路径处理** – 统一了应用数据路径的处理逻辑，修复了某些 Windows 系统上因 `%APPDATA%` 重定向导致的设置丢失问题。

**用户属性显示** – 修复了主题树中 MQTT 5.0 自定义用户属性无法正确显示的问题。

**Linux 图标** – 应用图标升级到 512×512 分辨率，在现代桌面环境中显示更加清晰。

## 未来规划

**MQTTX 2.0 重构**正在进行中。

- **[MCP over MQTT](https://www.emqx.com/en/blog/mcp-over-mqtt) 支持**
- **桌面端和命令行的 AI 代理模式**
- **消息可视化增强 - MQTTX Viewer**：
  - 差异对比视图：轻松比较不同的消息内容
  - 仪表盘视图：提供可自定义的 MQTT 活动总览
  - JSON 视图：优化 JSON 格式数据的处理和展示
  - 系统主题视图：专门用于查看系统相关的 MQTT 主题
- **支持可配置的断开连接属性（MQTT 5.0）**：通过自定义断开连接设置增强连接管理
- **IoT 场景数据模拟**：将该功能集成到桌面客户端，简化 IoT 场景测试
- **Sparkplug B 支持**：扩展对 Sparkplug B 工业物联网协议的支持
- **MQTT GUI 调试功能**：新增用于调试 MQTT 通信的功能
- **插件系统**：引入插件机制，支持 CoAP 和 MQTT-SN 等协议扩展
- **JSON Schema 支持**：提供 JSON Schema 的编解码能力
- **脚本测试自动化（Flow）**：简化自动化测试工作流的创建和管理



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://mqttx.app/zh/downloads" class="button is-gradient">Get Started →</a>
</section>
