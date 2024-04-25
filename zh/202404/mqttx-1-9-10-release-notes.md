MQTTX 1.9.10 版本现已发布。本次更新带来了重要的 Faker.js 升级、对连接断开和订阅问题的深度诊断，并增强了 CLI 与 UI 的多项功能。此次更新旨在简化用户操作流程，并提升问题排查效率。

> *点击此处下载最新版本：*[https://mqttx.app/zh/downloads](https://mqttx.app/zh/downloads)

## CLI 中的 Faker.js 升级

MQTTX 1.9.10 引入了一项关键更新：将 Faker.js 升级到 v8，带来重大变更。此次升级将影响那些使用自定义模拟脚本的用户，需要对脚本进行修改以保持与新版本的兼容。

本次更新简化了地区设置管理，但取消了在现有实例上更改地区设置的能力。详细的调整指南，请参阅 [Faker.js 升级指南](https://fakerjs.dev/guide/upgrading.html)。这一更新旨在提高 MQTTX 中模拟功能的精确性和效率。

关于脚本升级的指导，可参考此 PR 示例：[适配 Faker.js v8](https://github.com/emqx/MQTTX/pull/1585)。该示例详细展示了为了匹配新版本 Faker.js 所做的调整，为您的脚本修改提供了实用的参考。

## 模拟命令支持消息限制

现在，`simulate` 命令新增了 `--limit` 参数，这一功能与 `bench` 命令中的功能相似。此增强功能允许用户设置要发布的消息的确切数量，从而对模拟操作进行了更精确的控制。

**使用示例：**

通过 10 个连接共发布 100 条消息的模拟命令：

```shell
mqttx simulate -sc tesla -c 10 -h broker.emqx.io -t 'testtopic/simulate' -u 'admin' -P 'public' --limit 100
[4/10/2024] [11:13:42 AM] › ℹ  Start simulation publishing, scenario: tesla, connections: 10, req interval: 10ms, message interval: 1000ms
✔  success   [10/10] - Connected
[4/10/2024] [11:13:44 AM] › ℹ  Created 10 connections in 2.111s
[4/10/2024] [11:13:55 AM] › ℹ  Published total: 100, message rate: 0/s
```

**参数：**

- `-L, --limit <NUMBER>`：设置要发布的消息总数。将此设置为 0 可以发布无限消息（默认值：0）。

## 连接与订阅的诊断增强

MQTTX 1.9.10 版本通过引入 MQTT 5.0 的原因码，使得对连接断开或订阅失败的原因有了更清晰的反馈。这一改进使得用户能够更精确地识别问题，尤其是在处理诸如订阅 ACL 拒绝或服务器主动断开连接等情况时。

- **订阅失败**：现在系统会提示“Not authorized”原因，指出是由于访问控制限制导致的失败。

  ![订阅失败](https://assets.emqx.com/images/7244f8b00645662414381809445f4e72.png)

- **断开连接**：系统会标明是由“Administrative action”引起的，帮助用户明确是由服务器端的操作导致了连接中断。

  ![断开连接](https://assets.emqx.com/images/63ae6c575fa14d4ebf208627633af9b4.png)

这些直接且实用的信息特别适用于使用 MQTT 5.0 的用户，可简化问题排查过程，同时增加操作过程的透明度。如需进一步了解 MQTT 5.0 的原因码，请查阅 [MQTT 原因码介绍及快速指南](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack)。

## 新增保存功能优化连接管理

MQTTX 1.9.10 响应了社区用户的强烈需求，在新建和编辑连接界面新增了保存按钮。这一改进让用户在配置连接过程中能够临时保存信息，而无需立即完成所有设置，提高了使用的灵活性和便利性。现在，即使用户没有填写完所有字段，也可以先保存当前的进度，以便后续补充，提升了用户体验并加强了应用的实用性。

### 使用步骤：

在编辑或新建连接界面，用户可以在右上角连接按钮旁的下拉菜单中选择“仅保存”选项。这样，连接信息将被保存而不是立刻尝试连接，允许用户在任何时候返回继续编辑，从而确保了更加灵活和精确的连接管理。

![仅保存](https://assets.emqx.com/images/8c3fdcff0a81c1aa7a4dd1eb7515e8eb.png)

## 其他

在本次更新中，我们还包括了几项改进以提升用户体验：

- **多主题订阅验证**：修复了同时订阅多个主题时的验证问题，确保订阅的准确性。
- **记录编码/解码类型**：MQTTX 现在能够记住用户选择的编码/解码类型，避免在重启或切换时重置，这有助于防止消息出现乱码。
- **改善** `sub` **命令展示**：优化了 CLI 中 `sub` 命令的输出，使得主题和服务质量（QoS）的展示更为直观明了。

这些调整旨在进一步简化操作流程，增强应用的易用性，并提高稳定性。

## 未来规划

在 MQTTX 1.9.10 之后的下一阶段开发中，我们将专注于提升产品的可视化能力，并引入其他关键功能和改进：

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
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient">免费下载 →</a>
</section>
