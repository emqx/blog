MQTTX 1.9.9 现已正式发布。新版本带来了多项关键更新：包括优化连接事件的处理、新增 CBOR 数据格式支持、提供可定制的调试日志级别以及增强用户界面灵活性。此外，新版本在连接管理、数据处理和用户体验方面也进行了全面优化。

> 点击此处下载最新版本：[https://mqttx.app/zh/downloads](https://mqttx.app/zh/downloads)

## 日志级别

新版的 MQTTX 桌面客户端新增了日志级别自定义功能，包括调试日志，以便用户对连接状态有更清晰的了解。现在，用户可以从设置界面或日志页的右上角选择不同的日志级别：DEBUG（调试）、INFO（信息）、WARN（警告）以及 ERROR（错误）。这一功能可帮助用户更有效地进行问题排查，例如，选择 DEBUG 会显示所有日志信息，而选择 ERROR 则只会展示错误信息，以此类推。

![日志级别1](https://assets.emqx.com/images/b9a21bd73a2780fb4d040c327e6ce79c.png)

![日志级别2](https://assets.emqx.com/images/c9ef203405a6a406716700e553e5df2c.png)

此更新增强了 MQTTX 的诊断能力，使得追踪和解决问题变得更加容易。

## 连接列表显示控制

MQTTX 桌面版新功能允许用户一键隐藏连接列表，这样用户就能更专注于查看当前连接的详细信息，从而使得调试体验更加清晰和有针对性。这项改进让界面变得更加简洁，还能适应不同屏幕大小，进而提升用户体验。

![连接列表](https://assets.emqx.com/images/78517f790ed1c13a725a00e21fbb00bc.png)

![连接列表隐藏](https://assets.emqx.com/images/03025b7b764a071e632f6d4ac2639e7e.png)

该特性旨在简化工作流程，帮助用户减少视觉上的干扰，更有效利用屏幕空间。

## CBOR 格式支持

MQTTX 新增了对 CBOR（Concise Binary Object Representation）格式的支持，它在数据压缩上优于 JSON，从而能让设备运行更高效，减少网络带宽消耗，并延长电池使用寿命。想要深入了解 CBOR，可以访问 [cbor.io](http://cbor.io/)。

> CBOR 旨在实现极小的代码体积和消息尺寸，同时支持无需版本协商的扩展性。

### 桌面端：

在 MQTTX 桌面版本中，用户现在可以选择使用 CBOR 格式进行数据传输：

- 发送消息时，选择 CBOR 格式并输入对应的 JSON 数据。
- 接收消息时，选择 CBOR 格式，MQTTX 会自动把数据解码成 JSON。

![CBOR 格式](https://assets.emqx.com/images/08f06a8c0b1012383cd89db996bd60a0.png)

**命令行界面（CLI）**：

MQTTX CLI 通过 `--format cbor` 选项支持 CBOR，使用方法如下：

- 订阅消息：

  ```
  mqttx sub -h broker.emqx.io -t 'cbor' --format cbor
  ```

- 发布消息：

  ```
  mqttx pub -h broker.emqx.io -t 'cbor' -m '{"msg": "hello"}' --format cbor
  ```

![支持 CBOR](https://assets.emqx.com/images/0f904f1bb33c584ddd48d5867a511099.png)

感谢开源用户 [@Danfx](https://github.com/Danfx) 对这一更新所作出的重要贡献，他的支持对 MQTTX 的持续发展至关重要。

## Bench Pub 消息限制

`bench pub` 命令现在支持 `--limit` 选项，允许指定要发布的消息数量。使用 `-L` 或 `--limit <NUMBER>` 来设置此选项，其中 `0` 表示无限制（默认值为 `0`）。

例如，要发布 100 条消息，您可以使用以下命令：

```
mqttx bench pub -h broker.emqx.io -t 'testtopic' -m 'hello' -c 10 --limit 100
```

![MQTT Bench Pub](https://assets.emqx.com/images/f14c5959d7754f90aab479376f2f6f63.png)

此功能允许进行受控消息发布，使用户能够为测试或资源管理目的限制数据量。

## MQTTX Copilot 功能扩展

MQTTX Copilot 现支持更多客户端代码生成选项，涵盖软件和硬件项目，包括 Vue.js 和 React 等 UI 框架，以及 ESP32、ESP8266、Arduino、Raspberry Pi 等硬件平台。此外，它还支持 Android、iOS、React Native 和 Flutter 等移动应用程序。MQTTX Copilot 的适用范围得到了更大的拓展，能够满足更多类型的开发项目需求。

![MQTTX Copilot 功能扩展](https://assets.emqx.com/images/67e88a270200025e73bb8a6e7a5e3264.png)

## 其他

在此次发布中，我们还进行了若干其他增强和更新，以改善您的使用体验：

- **连接事件**：我们增强了桌面端、Web 和 CLI 平台对断开连接和离线事件的支持。这些改进确保了更好的连接管理处理和鲁棒性，包括当从代理接收到断开连接包或客户端离线时的特定行为。
- **连接问题修复**：在桌面版本中，我们修复了重连功能的一个问题，现在确保重连仅在当前连接的页面内有效。
- **UI/UX 增强**：桌面端与 Web 端 UI 进行了更新，提供了更加协调和用户友好的体验。这包括更清晰的日志消息和所有的图标更新。
- **文档和 README 更新**：我们简化并更新了 CLI 的 README 文件，使新用户更容易上手，同时让现有用户更清楚地理解工具的功能。

## 未来规划

在 MQTTX 1.9.8 之后的下一阶段开发中，我们将专注于提升可视化能力，并引入其他关键功能和改进：

- **Payload 图表可视化增强 - MQTTX Viewer**：
  - **主题树视图**：增强主题的组织和可视化。
  - **差异视图**：轻松比较不同的消息或负载。
  - **仪表板视图**：提供 MQTT 活动的可定制概览，以获取个性化洞见。
  - **JSON 视图**：改进 JSON 格式数据的处理和显示。
  - **系统主题视图**：专门针对系统相关 MQTT 主题的视图。
- **支持可配置的断开连接属性（MQTT 5.0）**：通过自定义断开连接设置来增强连接管理。
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
