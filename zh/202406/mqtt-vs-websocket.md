## 引言

在现代实时通信中，MQTT 和 WebSocket 均占据着举足轻重的地位。尽管它们在功能和应用场景上存在差别，但本文的比较并不是将两者对立起来，而是揭示每种协议所扮演的独特角色，帮助您理解它们之间的关系，并了解何时单独或结合使用它们以发挥各自的优势，从而为您的应用构建一个更加优化的通信架构。

## MQTT 与 WebSocket 概览

### MQTT 简介

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（Message Queuing Telemetry Transport）是一种为资源受限设备设计的轻量级消息传输协议，适合在低带宽、高延迟或不稳定网络环境下使用。它在物联网（IoT）领域得到了广泛应用，为传感器、执行器和其他设备提供高效的通信。

要想有效使用 MQTT，需要一个中心 Broker，例如 [EMQX](https://www.emqx.com/zh/products/emqx)，它不仅能确保消息传递的可靠性，还能帮助您高效地扩展系统规模。

![image.png](https://assets.emqx.com/images/2a584a13dba6db647f402774f97adaf9.png)

### WebSocket 简介

WebSocket 是一种网络协议，它通过单一、持久的 TCP 连接实现了双向通信通道。与 HTTP 的短暂交互不同，WebSocket 在初始握手之后维持一个开放的连接，这使得它能够支持实时和交互式的数据交换。这一特性对于需要快速响应的应用程序，如在线游戏、聊天系统和实时股票交易平台等，尤为重要。

WebSocket 协议包括建立连接的握手阶段和交换信息的数据传输阶段。

![WebSocket handshake](https://assets.emqx.com/images/269d797a452ad5d491c78f2f4dd573b7.png)

## 深入了解 MQTT 和 WebSocket：应用场景

下面，我们将详细探讨 MQTT 和 WebSocket 的特定特性及其应用场景，以便您更深入地理解它们在各种环境中的有效运作。

### MQTT：为物联网高效通信量身定制

MQTT 是一种专为资源受限的环境设计的轻量级发布-订阅消息传输协议，非常适合功率低、带宽有限或网络不稳定的场合。它的数据包尺寸小、基于主题的消息路由和多种服务质量（QoS）级别，使其在需要高效率和可靠性的物联网应用中表现出色。

#### MQTT 的关键特性

- **轻量化**：降低资源消耗，适合功能有限的设备。
- **高可靠性**：提供多级服务质量（QoS），确保在不稳定的网络环境中也能传递消息。
- **安全通讯**：支持 TLS/SSL 加密和客户端认证，保障数据安全。
- **双向通信**：通过发布-订阅模式实现双向交流。
- **有状态会话**：管理连接状态，提升通信可靠性。
- **高扩展性**：在带宽消耗最小的情况下处理大规模部署。
- **多语言支持**：支持多种编程语言，易于集成。

#### 实际应用场景

MQTT 的以上特性使其成为满足物联网生态系统复杂多样需求的理想选择。以下是一些特别能够体现 MQTT 能力的具体应用场景。

- **物联网设备**：在智能家居中，为传感器和温控器等设备提供高效的通信能力，提升自动化水平和能源管理效率。
- [**车联网**](https://www.emqx.com/zh/solutions/internet-of-vehicles)：支持车载信息通信系统的数据交换，包括**软件定义汽车**，增强车队管理、维护和实时车辆监控能力。
- [**工业物联网**](https://www.emqx.com/zh/solutions/industrial-iot)：将工业环境中的传感器和机械设备连接到中央服务器，促进实时操作控制和预测性维护。
- [**智能制造**](https://www.emqx.com/zh/solutions/smart-manufacturing)：通过实时数据通信，自动化和优化制造流程，提高安全性和生产效率。
- **可穿戴设备**：将健身追踪器和智能手表与智能手机或云服务器连接，为用户提供实时健康监测和数据分析。

#### MQTT 应用示例：智能家居

假设您拥有一套智能家居系统，并希望通过 MQTT 技术来控制灯光开关。以下是一个由 JavaScript 实现的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)代码示例。我们将连接至由 EMQ 提供的[公共 MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)——`broker.emqx.io`，它允许您在无需部署个人 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 的情况下测试和体验 MQTT 协议：

```javascript
// 引入 MQTT 库，本例采用 Node.js 环境；如果您在浏览器或其他环境操作，
// 可以选择使用 CDN 或 ES 模块导入方式。
// 更多信息和选择，请访问：https://github.com/mqttjs/MQTT.js
const mqtt = require('mqtt');

// 连接至 EMQ X 公共 MQTT Broker
const client = mqtt.connect('mqtt://broker.emqx.io');

// 成功连接后，发布消息以开启灯光
client.on('connect', () => {
  console.log('Connected to EMQ X broker');
  // 指定主题和消息内容
  client.publish('home/livingroom/light', 'ON');
  console.log('Light turned ON');

  // 如有需要，可在发布消息后断开连接
  client.end();
});

// 处理连接过程中的错误
client.on('error', (error) => {
  console.error('Connection error:', error);
});
```

此示例清晰展示了如何利用 MQTT 轻松实施物联网功能，并通过公共基础设施实现家居自动化的实时操作。

### WebSocket：实现高级实时通信

WebSocket 协议通过单个 TCP 连接实现全双工通信。它始于一个 HTTP 握手，该握手将连接从 HTTP 升级到 WebSocket，从而允许不间断的双向数据流，避免了重复建立连接的开销。

**WebSocket 的工作原理**

WebSocket 从一个握手动作开始。客户端请求从 HTTP 升级到 WebSocket，一旦得到服务器的批准，就会建立一个持久的 TCP 通道。这样就消除了 HTTP 连接周期的延迟，使数据交换能够即时进行。

#### WebSocket 的关键特性

- **双向通信**：促进实时的双向交互。
- **低延迟**：通过保持连接开放，减少通信延迟。
- **高效率**：有效处理频繁的小型消息和大量数据。
- **广泛兼容**：在现代浏览器和服务器技术中得到广泛支持。

#### 实际应用场景

- **互动游戏**：在多人游戏中提供流畅的玩家互动体验。
- **实时通知**：为金融交易和社交媒体即时发送提醒。
- **实时内容更新**：动态更新新闻动态和体育比分。
- **协作工具**：支持文档和项目的实时共同编辑。

实施 WebSocket 时，需要注意安全风险，如跨站 WebSocket 劫持，并且需要处理代理和防火墙。利用带 TLS 加密的 WebSocket Secure (WSS) 以及强化的服务器配置，可以缓解这些问题。

总的来说，WebSocket 通过支持高效的实时交互，增强了 Web 应用的功能。尽管面临挑战，但它的功能对于当今交互式应用中的动态用户体验至关重要。

#### WebSocket 应用示例：实时聊天应用

以下展示了如何在 JavaScript 中使用 WebSocket 实现一个基础的实时聊天功能，它能够实现用户之间快速而高效的消息交换：

```javascript
// 与聊天服务器建立 WebSocket 连接
const chatSocket = new WebSocket('wss://yourserver.com/chat');

// 向服务器发送消息
function sendMessage(message) {
  chatSocket.send(JSON.stringify({ message }));
  console.log('Message sent:', message);
}

// 接收来自服务器的消息
chatSocket.onmessage = function(event) {
  const message = JSON.parse(event.data).message;
  console.log('Message received:', message);
};

// 发送消息的示例用法
sendMessage('Hello, world!');
```

这个简明的示例建立了一个 WebSocket 连接，包含发送和接收消息的功能，这对于聊天应用程序来说是必不可少的。它展示了双向通信所必需的主要功能。

## 对比分析

MQTT 和 WebSocket 在现代应用中解决了不同的通信需求，每种技术在不同场景下都有其优势。尽管它们有一些相似之处，但各自的独特属性提供了不同的优势。以下是一个详细的对比，突出了这些差异和相似点，帮助您明确何时使用每种协议。

| 特性                     | MQTT                                      | WebSocket                        |
| :----------------------- | :---------------------------------------- | :------------------------------- |
| **架构**                 | 发布/订阅模式，可选请求/响应机制          | 双向通信，类 Socket API          |
| **通信类型**             | 异步通信，支持广播（一对多）              | 异步通信，点对点（一对一）       |
| **连接类型**             | 通过 Broker 实现长期连接                  | 持久化直接连接                   |
| **安全连接**             | TLS over TCP                              | TLS over TCP                     |
| **消息格式**             | 二进制数据                                | 二进制数据（基于帧的结构）       |
| **消息大小**             | 最大 256 MB                               | 每帧最大 2^63 字节               |
| **消息开销**             | 最小，起始于 2 字节                       | 最小 2 字节，掩码帧 6 字节       |
| **消息分发**             | Broker 可为离线订阅者缓存消息             | 不支持原生消息队列；依赖额外软件 |
| **消息 QoS**             | 0（最多一次），1（至少一次），2（仅一次） | 无内置 QoS；依赖 TCP             |
| **消息排队**             | 由 Broker 支持                            | 原生不支持                       |
| **标准和协议合规**       | 遵循 OASIS 标准，具备全面安全特性         | 符合 RFC 6455，遵守网络标准      |
| **数据效率**             | 由于头部开销极小，效率高                  | 由于帧结构开销较大，效率略低     |
| **可扩展性**             | 通过 Broker，具有广泛的扩展性             | 受限于直接连接，需要额外层       |
| **集成复杂度**           | 中等，取决于 Broker 配置                  | 一般较低，易于与 HTTP/S 环境集成 |
| **维护和运营成本**       | 需要 Broker 管理                          | 较低，除非进行水平扩展           |
| **实时能力**             | 高，但 Broker 可能引入延迟                | 极高，支持即时数据传输           |
| **受限网络条件下的表现** | 适应性强，适合各种网络条件                | 在稳定网络条件下表现最佳         |
| **协议成熟度**           | 成熟，物联网领域广泛使用                  | Web 开发中流行                   |
| **适用场景**             | 物联网、车联网、网络受限环境              | 实时网络应用、游戏、互动平台     |

## MQTT over WebSocket

MQTT 和 WebSocket 各自承担着不同的功能，但它们的结合却开辟了强大的应用前景。通过将 MQTT 嵌入到 WebSocket 协议中，开发者得以在 Web 环境下发挥 MQTT 出色的消息传递能力，实现物联网数据与 Web 应用的无缝对接。这种方式让我们能够通过 Web 浏览器直接与物联网设备进行实时互动，从而提升用户体验，并将物联网的潜力延伸至更广阔的 Web 领域。

![MQTT over WebSocket](https://assets.emqx.com/images/82e6d52ea88d452032eddc8a2c381751.png)

### 为何选择 MQTT over WebSocket

MQTT 与 WebSocket 的结合汇聚了两种技术的优势，通过 Web 浏览器提升了物联网的交互体验，并使物联网的应用变得更加普及。以下是其优点所在：

- **交互简化**：实现了浏览器与物联网设备的直接交互。
- **普及性**：使得任何 Web 用户都能够连接并操控物联网设备。
- **实时更新**：能够即时将设备的最新数据传送至浏览器。
- **高效与广泛支持**：将 MQTT 的高效性与 WebSocket 的普及性相结合。
- **数据可视化增强**：在 Web 页面上更加直观地展示实时数据。

想了解更多关于 MQTT over WebSocket 的优势，请参阅 [MQTT over WebSocket 快速入门指南](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket#why-use-mqtt-over-websocket)。

### 快速入门：MQTT over WebSocket

EMQX MQTT Broker 默认支持 WebSocket，使得在 WebSocket 上实现 MQTT 变得简单直接。以下是快速入门的步骤：

**1. 使用 Docker 安装 EMQX：**使用 Docker 部署 EMQX，无缝处理 MQTT 和 WebSocket 通信：

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.6.1
```

此命令将安装 EMQX 并启用 WebSocket，并可立即使用。有关在 EMQX 中配置 WebSocket 监听器的详细说明，请访问 [EMQX 文档：配置 WebSocket 监听器](https://docs.emqx.com/en/emqx/latest/configuration/listener.html#configure-websocket-listener)。

**2. 安装 MQTT.js：**安装 MQTT.js 库以通过 WebSocket 与 MQTT Broker 进行交互：

```
npm install mqtt
```

**3. 连接、订阅和发布：**使用 [MQTT.js](https://www.emqx.com/zh/blog/mqtt-js-tutorial) 建立连接，订阅主题，并高效发布消息：

```
const mqtt = require("mqtt");

// 连接到 EMQX WebSocket 端口
const client = mqtt.connect("ws://localhost:8083/mqtt");

client.on("connect", () => {
    console.log("Connection established");
    // 订阅一个主题
    client.subscribe("topic/test", (err) => {
        if (!err) {
            // 发布一条消息
            client.publish("topic/test", "Hello MQTT over WebSocket");
        }
    });
});

// 记录接收到的消息
client.on("message", (topic, message) => {
    console.log(`Received message: ${message.toString()}`);
    // 收到消息后断开连接
    client.end();
});
```

这种简化的设置能够迅速将 MQTT 通信能力整合到任何 Web 应用中，利用 WebSocket 实现有效的实时数据交换。

## Q&A

### 如何在 MQTT 与 WebSocket 之间做出选择？

- **MQTT** 最适合采用一对多通信模型的不稳定网络上的低功耗设备。为了确保与基于 Web 的客户端兼容，MQTT 可以运行在 WebSocket 之上。
- **WebSocket** 在一对一的实时交互场景中表现优异，尤其是在 Web 浏览器或其他需要直接连接的环境中。

MQTT over WebSocket 在物联网应用与 Web 技术之间架起了一座桥梁，使得通过浏览器进行实时交互成为可能。

### 是否有 MQTT over WebSokcet SDK？

对于 MQTT over WebSocket，**MQTT.js** 是一个出色的选择。它是一个为 MQTT 协议设计的客户端库，使用 JavaScript 编写，适用于 Node.js 和浏览器环境。

### 是否有适用于 MQTT over WebSocket 的测试工具？

推荐使用 [**MQTTX**](https://mqttx.app/zh) 来测试 MQTT over WebSocket。它是一个全能的、跨平台的 MQTT 客户端，提供桌面应用、CLI 工具和 Web 应用。

### MQTT over TCP 与 MQTT over WebSocket 性能对比？

**MQTT over TCP** 由于直接使用 TCP 层，提供了更低的延迟和更少的开销，非常适合不稳定的网络和需要高效实时通信的应用。**MQTT over WebSocket** 虽然由于额外的帧处理引入了轻微的开销，但更适合 Web 应用。它通过标准 Web 端口提供了更容易的集成，并增强了与 HTTP 协议和防火墙穿透的兼容性。请根据您的应用对效率或 Web 集成的需求进行选择。

## 结语

在本文的探索中，我们深入了解了 MQTT 和 WebSocket 的独特特性和使用场景，突出了每种协议在物联网和 Web 应用中对特定需求的服务方式。

MQTT 在需要跨设备进行稳健、高效通信的环境中表现出色，而 WebSocket 则在实时、交互式网络环境中大放异彩。通过将 MQTT 与 WebSocket 结合，开发者可以利用两种协议的优势，确保在多样化的环境中无缝且安全的通信。这种结合增强了 Web 应用中的物联网功能，并扩大了可访问性，使得跨多平台的实时数据互动成为可能。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
