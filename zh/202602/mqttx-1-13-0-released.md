MQTTX 1.13.0 现已正式发布。

该版本带来了全新的消息体查看器功能，包含差异视图和 JSON 树视图，让消息调试更加直观高效。同时新增快速复制功能，支持一键复制 Topic、Payload 和连接地址。此外，新增 Protobuf Editions 2023 支持、Windows 便携版、主题空格检测等实用功能，Desktop 和 Web 版本的 UI 也进行了优化，并通过 Electron 39 升级解决了 macOS 26 Tahoe 上的性能问题。

> ***点击下载最新版本：***[***https://mqttx.app/zh/downloads***](https://mqttx.app/zh/downloads)

## 消息体查看器

> 特别感谢 [@muzaffarmhd](https://github.com/muzaffarmhd) 对此功能的贡献

MQTTX 1.13.0 引入了全新的消息体查看器。在 MQTT 开发测试中，经常需要分析设备上报数据的变化、对比不同时刻的消息内容、或在复杂 JSON 中快速定位字段。为此，我们提供了差异视图和 JSON 树视图两种可视化方式，显著提升消息分析效率。

### 差异视图

差异视图允许用户直观比较两条消息的 Payload 差异，变更内容以高亮方式清晰展示。

**典型应用场景：**

- **设备状态追踪**：对比设备前后两次上报的状态数据，快速发现哪些字段发生了变化
- **数据传输验证**：验证发送的消息与接收的消息是否一致
- **问题排查**：当设备行为异常时，对比正常和异常时的消息内容

**使用方法：**

1. 进入视图器页面，切换到**消息体查看器**标签页并开启**差异视图**模式
2. 从工具栏选择连接和主题以加载消息列表，可按消息类型筛选（全部/收到/发布）
3. 使用箭头按钮或键盘快捷键（`←` 旧消息，`→` 新消息）浏览，到达最早消息时自动加载更多历史记录
4. 每条消息显示时间戳、QoS、Retain 标志和 Payload 大小等元数据

![image.png](https://assets.emqx.com/images/bae3ed03ef93897928c96a8fa1772cca.png)

### JSON 树视图

对于 JSON 格式的 Payload，JSON 树视图提供了结构化的展示和导航能力。

**典型应用场景：**

- **复杂数据分析**：浏览深层嵌套的 JSON 结构，如传感器数据包或设备配置信息
- **字段查找**：在大型 JSON 数据中快速搜索和定位特定字段
- **数据可视化**：以全屏可视化方式查看 JSON 结构层级

**使用方法：**

1. 在消息体查看器切换到 **JSON 树**视图模式，选择连接和主题
2. 使用箭头按钮（`←`/`→`）浏览消息，使用搜索框查找并高亮 JSON 内容
3. 点击复制图标复制 Payload，或点击饼图图标打开全屏 JSON 结构可视化

![image.png](https://assets.emqx.com/images/edde702969e0f30e0d80145886d8b01a.png)

## 可配置的最大 Payload 显示大小

新增最大 Payload 显示大小设置，用于自动折叠消息列表中的大型 Payload。

**设置方法：**

1. 进入 **设置 > 通用**
2. 找到 **最大 Payload 显示大小** 选项
3. 通过滑块调整阈值（最小 16KB，默认 512KB，最大 2MB）

当消息 Payload 达到或超过设定阈值时，消息列表中该条消息会自动折叠显示，避免大 Payload 占据过多屏幕空间。完整数据仍会保存，可随时展开查看。

![image.png](https://assets.emqx.com/images/9a36570117486c993f7034b3aacfb204.png)

## 快速复制功能

之前右键消息只能复制 Payload，本版本新增了独立的 Copy Topic 和 Copy Host/Broker 选项（[#1962](https://github.com/emqx/MQTTX/issues/1962)）。这对于使用动态主题的场景特别有用，方便快速复制主题用于订阅配置或集成到 Home Assistant、Node-RED 等自动化工具。

**连接信息复制：**

在左侧连接列表中右键点击连接，可以快速复制：

- **Copy Host**：复制主机地址，如 `broker.emqx.io`
- **Copy Broker**：复制完整连接地址，如 `mqtt://broker.emqx.io:1883`

![image.png](https://assets.emqx.com/images/5449e3085a9698352d416ff4889f55fe.png)

**Topic / Payload 复制：**

在消息列表中右键点击目标消息，可以快速复制：

- **Copy Topic**：复制该消息的 Topic
- **Copy Payload**：复制该消息的完整 Payload

![image.png](https://assets.emqx.com/images/ac87818baef461a529e0db6378c41b5f.png)

## Protobuf Editions 2023 支持

MQTTX 1.13.0 升级了 protobufjs 依赖，现已支持 Protobuf Editions 2023 格式。此功能在 Desktop、CLI 和 Web 三个版本中均可使用。

**什么是 Protobuf Editions？**

Protobuf Editions 是 Google 在 2023 年推出的新一代 Protocol Buffers 语法，取代了之前的 proto2 和 proto3。它引入了更灵活的特性系统，允许开发者精细控制字段行为。

**Editions 语法示例：**

```protobuf
edition = "2023";

message SensorData {
  int32 device_id = 1;
  float temperature = 2;
  float humidity = 3;
  int64 timestamp = 4;
}

```

**使用方法：**

1. 进入 **设置 > Schema**
2. 点击 **新建 Schema**
3. 选择 **Protobuf** 类型
4. 粘贴或上传您的 `.proto` 文件（支持 edition = "2023" 语法）
5. 在连接中选择该 Schema 进行编解码

如果您的项目已升级到 Protobuf Editions 2023，MQTTX 现在可以正确解析和编码这些消息。

## 主题空格检测

新增主题空格检测功能，帮助识别主题中可能导致发布与订阅不匹配的空格字符。

MQTT 主题中的空格是合法的，但通常是用户输入错误。例如 `sensor/temperature `和 `sensor/temperature` 是两个不同的主题，这种差异很难用肉眼发现，却会导致消息无法正确路由。

开启此功能后，当主题中包含空格字符时，MQTTX 会在订阅对话框中显示提示，并使用 `␣` 符号标记空格位置，帮助您快速定位问题。

![image.png](https://assets.emqx.com/images/3d361d3f62569dfb8ebadf2d2d614c3e.png)

进入 **设置 > 高级**，找到 **主题空格检测** 开关即可开启。

## UI 优化

- **Desktop**：优化配色和动画过渡效果，简化连接列表选中状态样式，重新设计帮助页面和关于页面布局
- **Web**：新增 JSON Payload 语法高亮，同步 Desktop UI 优化

![image.png](https://assets.emqx.com/images/2b101a3d82649cf5f422f6504af3a981.png)

## 性能与兼容性改进

- **Electron 39 升级**：解决 macOS 26 Tahoe 上的界面卡顿和响应延迟问题，带来更好的渲染性能和内存管理
- **Windows 便携版**：新增 Portable 版本，下载解压即可使用，无需安装
- **跨平台兼容性**：使用 cross-env 修复 Windows 构建脚本兼容性问题

## Bug 修复

- 修复编辑禁用主题后状态被意外启用的问题 ([#2007](https://github.com/emqx/MQTTX/issues/2007))
- 修复 Topic 输入框按 Enter 键插入换行符的问题 ([#2001](https://github.com/emqx/MQTTX/issues/2001))
- 修复 Meta 按钮红点位置错乱的问题
- 修复 Web 版 Topic 输入框强制换行的问题

## 未来规划

- **MQTTX 2.0 重构**：正在进行中
- **MCP over MQTT 支持**：支持 Model Context Protocol，实现 AI Agent 与 MQTT 设备的交互
- **AI Agent 模式**：Desktop 和 CLI 支持 AI Agent 模式
- **Protobuf 消息与订阅路由映射**：为不同订阅主题配置不同的 Protobuf 解码 Schema
- **MQTTX Viewer 增强**：Dashboard 视图、System Topic 视图等可视化功能
- **可配置断开连接属性**：支持 MQTT 5.0 断开连接属性配置
- **IoT 场景数据模拟**：集成更多 IoT 场景的数据模拟能力
- **Sparkplug B 支持**：扩展 MQTTX 支持 Sparkplug B 协议
- **插件系统**：支持 CoAP、MQTT-SN、Kafka、MessageQueue 等协议扩展
- **脚本测试自动化（Flow）**：简化自动化测试工作流的创建和管理





<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://mqttx.app/zh/downloads" class="button is-gradient">Get Started →</a>
</section>
