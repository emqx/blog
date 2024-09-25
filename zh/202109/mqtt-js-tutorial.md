## 简介

在物联网（IoT）和实时通信领域快速发展中，MQTT 协议已成为一个至关重要的组成部分。对于那些希望在应用程序中充分利用 MQTT 功能的 JavaScript 开发者来说，[**MQTT.js**](https://github.com/mqttjs/MQTT.js) 无疑是一个不可或缺的利器。

**MQTT.js** 是一个为 [**MQTT 协议**](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 精心打造的 JavaScript 客户端库，同时适用于 Node.js 和浏览器环境。凭借其强大的功能和高效性，MQTT.js 已成为 JavaScript 生态系统中最受欢迎的 [**MQTT 客户端库**](https://www.emqx.com/zh/mqtt-client-sdk)之一，让开发者能够轻松构建复杂的物联网和消息应用。

MQTT.js 的主要特点如下：

- 异步操作：充分利用 JavaScript 的单线程特性，MQTT.js 作为一个完全异步的 MQTT 客户端，能够在应用程序中实现最佳性能和响应速度。

- 全面的协议支持：该库无缝支持 MQTT/TCP、MQTT/TLS 和 MQTT/WebSocket，为各种网络配置和安全需求提供了灵活的解决方案。

- 跨平台兼容：MQTT.js 为不同的运行环境提供了专门的支持：

  - 浏览器：支持 [**MQTT over WebSocket**](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)，实现 Web 应用程序中的实时通信。

  - Node.js：支持 MQTT 和 MQTT over WebSocket，适用于服务器端应用和物联网设备。

本指南将带您深入了解 MQTT.js 的世界，探讨其配置、基本用法和实际应用。我们将涵盖以下内容：

- MQTT.js 的项目配置
- 连接 MQTT 服务器
- 主题的发布与订阅
- 消息和事件处理
- 错误处理和安全最佳实践

> 注意：MQTT.js v5.0.0（2023年7月发布）引入了重大变更，包括使用 TypeScript 重写和支持 Node.js v18/v20，而 v4.0.0（2020年4月发布）支持 Node.js v12/v14。

## 安装

### 使用 npm 或 yarn 安装

```shell
npm install mqtt --save

# 或使用 yarn

yarn add mqtt
```

**注意**：如果您的 Node 环境是 v12 或 v14 及以上版本，请使用 MQTT.js 4.0.0 及以上版本

### 使用 CDN 安装

在**浏览器环境**中，我们还可以使用 CDN 的方式引入 MQTT.js。MQTT.js 的 bundle 包通过 [http://unpkg.com](http://unpkg.com/) 管理，我们可以直接添加 [unpkg.com/mqtt/dist/mqtt.min.js](https://unpkg.com/mqtt/dist/mqtt.min.js) 来进行使用。

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<script>
  // 将在全局初始化一个 mqtt 变量
  console.log(mqtt)
</script>
```

### 全局安装

除了上述的安装方式外，MQTT.js 还提供了全局安装的方式，使用命令行工具来完成 MQTT 的连接、发布和订阅等。

```shell
npm install mqtt -g
```

我们会在下文中的一些使用教程中详细描述如何使用 MQTT.js 的命令行工具。

## 使用

本文将使用 EMQX Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQX Cloud 文档](https://docs.emqx.com/zh/cloud/latest/)。

### 简单例子

我们简单编写一段代码实现连接到 EMQX Cloud 并完成订阅主题、收发消息的简单例子。因为在浏览器环境中仅支持使用 WebSocket 连接，所以我们将使用在**浏览器环境**和 **Node.js 环境**两种不同的连接参数来完成连接。不过除连接地址外，其它参数均是相同的，因此读者可根据自己的实际情况选择使用。

```javascript
const mqtt = require('mqtt')

/***
 * 浏览器环境
 * 使用协议为 ws 和 wss 的 MQTT over WebSocket 连接
 * EMQX 的 ws 连接默认端口为 8083，wss 为 8084
 * 注意需要在连接地址后加上一个 path, 例如 /mqtt
 */
const url = 'ws://broker.emqx.io:8083/mqtt'
/***
 * Node.js 环境
 * 使用协议为 mqtt 和 mqtts 的 MQTT over TCP 连接
 * EMQX 的 mqtt 连接默认端口为 1883，mqtts 为 8084
 */
// const url = 'mqtt://broker.emqx.io:1883'

// 创建客户端实例
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // 认证信息
  clientId: 'emqx_test',
  username: 'emqx_test',
  password: 'emqx_test',
}
const client = mqtt.connect(url, options)
client.on('connect', function () {
  console.log('Connected')
  // 订阅主题
  client.subscribe('test', function (err) {
    if (!err) {
      // 发布消息
      client.publish('test', 'Hello mqtt')
    }
  })
})

// 接收消息
client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})
```

### 命令行

在全局安装完 MQTT.js 后，我们同样可以使用命令行工具来完成主题订阅消息发布接收的动作。

示例连接到 `broker.emqx.io` 并订阅 `testtopic/#` 主题：

```shell
mqtt sub -t 'testtopic/#' -h 'broker.emqx.io' -v
```

示例连接到 `broker.emqx.io` 并向 `testtopic/hello` 主题发送消息

```shell
mqtt pub -t 'testtopic/hello' -h 'broker.emqx.io' -m 'from MQTT.js'
```

如需使用功能更加全面的 MQTT 命令行工具，可参考使用 [MQTTX CLI](https://mqttx.app/zh/cli)。

### API 介绍

#### mqtt.connect([url], options)

连接到指定的 MQTT Broker 的函数，并始终返回一个 Client 对象。第一个参数传入一个 URL 值，URL 可以是以下协议：`mqtt`, `mqtts`, `tcp`, `tls`, `ws`, `wss`。URL 也可以是一个由 URL.parse() 返回的对象。然后再传入一个 Options 对象，用于配置 MQTT 连接时的选项。当使用 WebSocket 连接时需要注意地址后是否需要加上一个 path，例如 `/mqtt`。

下面列举一些常用的 Options 对象中的属性值：

- Options
  - `keepalive`: 单位为`秒`，数值类型，默认为 60 秒，设置为 0 时禁止
  - `clientId`: 默认为 `'mqttjs_' + Math.random().toString(16).substr(2, 8)`，可以支持自定义修改的字符串
  - `protocolVersion`: MQTT 协议版本号，默认为 4（v3.1.1）可以修改为 3（v3.1）和 5（v5.0）
  - `clean`: 默认为 `true`，是否清除会话。当设置为 `true` 时，断开连接后将清除会话，订阅过的 Topics 也将失效。当设置为 `false` 时，离线状态下也能收到 QoS 为 1 和 2 的消息
  - `reconnectPeriod`: 重连间隔时间，单位为毫秒，默认为 1000 毫秒，**注意：**当设置为 0 以后将取消自动重连
  - `connectTimeout`: 连接超时时长，收到 CONNACK 前的等待时间，单位为毫秒，默认 30000 毫秒
  - `username`: 认证用户名，如果 Broker 要求用户名认证的话，请设置该值
  - `password`: 认证密码，如果 Broker 要求密码认证的话，请设置该值
  - `will`: 遗嘱消息，一个可配置的对象值，当客户端非正常断开连接时，Broker 就会向遗嘱 Topic 里面发布一条消息，格式为：
    - `topic`: 遗嘱发送的 Topic
    - `payload`: 遗嘱发布的消息
    - `QoS`: 遗嘱发送的 QoS 值
    - `retain`: 遗嘱发布的消息的 retain 标志
  - `properties`: [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 新增，可配置的对象的属性值，详情请参考：[https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options)

- 如果需要配置 SSL/TLS 连接，Option 对象会被传递给 [`tls.connect()`](http://nodejs.org/api/tls.html#tls_tls_connect_options_callback) ，因此可以在 option 中配置以下属性
  - `rejectUnauthorized`: 是否验证服务端证书链和地址名称，设置为 false 时将跳过验证，会暴露在中间人的攻击之下，所以不建议在生产环境中使用这种配置，当设置为 true 时，将开启强认证模式，且如果是自签名证书，请在证书配置时设置 Alt name。
  - `ca`:  只有在服务器使用自签名证书时才有必要，自签名证书中生成的 CA 文件
  - `cert`: 只有当服务器需要客户证书认证时才有必要（双向认证），客户端证书
  - `key`: 只有当服务器需要客户证书认证时才有必要（双向认证），客户端密钥

#### Client 事件

当连接成功后，返回的 Client 对象可通过 on 方法监听多个事件，业务逻辑可在监听的回调函数中完成。以下列举一些常用的事件：

- `connect`

  当连接成功时触发，参数为 connack

  ```javascript
  client.on('connect', function (connack) {
    console.log('Connected')
  })
  ```

- `reconnect`

  当断开连接后，经过重连间隔时间重新自动连接到 Broker 时触发

  ```javascript
  client.on('reconnect', function () {
    console.log('Reconnecting...')
  })
  ```

- `close`

  在断开连接以后触发

  ```javascript
  client.on('close', function () {
    console.log('Disconnected')
  })
  ```

- `disconnect`

  在收到 Broker 发送过来的断开连接的报文时触发，参数 packet 即为断开连接时接收到的报文，MQTT 5.0 中的功能

  ```javascript
  client.on('disconnect', function (packet) {
    console.log(packet)
  })
  ```

- `offline`

  当客户端下线时触发

  ```javascript
  client.on('offline', function () {
    console.log('offline')
  })
  ```

- `error`

  当客户端无法成功连接时或发生解析错误时触发，参数 error 为错误信息

  ```javascript
  client.on('error', function (error) {
    console.log(error)
  })
  ```

- `message`

  当客户端收到一个发布过来的 Payload 时触发，其中包含三个参数，topic、payload 和 packet，其中 topic 为接收到的消息的 topic，payload 为接收到的消息内容，packet 为 [MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)信息，其中包含 QoS、retain 等信息

  ```javascript
  client.on('message', function (topic, payload, packet) {
    // Payload is Buffer
    console.log(`Topic: ${topic}, Message: ${payload.toString()}, QoS: ${packet.qos}`)
  })
  ```

#### Client 方法

Client 除监听事件外，也内置一些方法，用来进行发布订阅的操作等，以下列举一些常用的方法。

- `Client.publish(topic, message, [options], [callback])`

  向某一 topic 发布消息的函数方法，其中包含四个参数：

  - topic: 要发送的主题，为字符串
  - message: 要发送的主题的下的消息，可以是字符串或者是 Buffer
  - options: 可选值，发布消息时的配置信息，主要是设置发布消息时的 QoS、Retain 值等。
  - callback: 发布消息后的回调函数，参数为 error，当发布失败时，该参数才存在

  ```javascript
  // 向 testtopic 主题发送一条 QoS 为 0 的测试消息
  client.publish('testtopic', 'Hello, MQTT!', { qos: 0, retain: false }, function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Published')
    }
  })
  ```

- `Client.subscribe(topic/topic array/topic object, [options], [callback])`

  订阅一个或者多个 topic 的方法，当连接成功需要订阅主题来获取消息，该方法包含三个参数：

  - topic: 可传入一个字符串，或者一个字符串数组，也可以是一个 topic 对象，`{'test1': {qos: 0}, 'test2': {qos: 1}}`
  - options: 可选值，订阅 Topic 时的配置信息，主要是填写订阅的 Topic 的 QoS 等级的
  - callback: 订阅 Topic 后的回调函数，参数为 error 和 granted，当订阅失败时 error 参数才存在, granted 是一个 {topic, qos} 的数组，其中 topic 是一个被订阅的主题，qos 是 Topic 是被授予的 QoS 等级

  ```javascript
  // 订阅一个名为 testtopic QoS 为 0 的 Topic
  client.subscribe('testtopic', { qos: 0 }, function (error, granted) {
    if (error) {
      console.log(error)
    } else {
      console.log(`${granted[0].topic} was subscribed`)
    }
  })
  ```

- `Client.unsubscribe(topic/topic array, [options], [callback])`

  取消订阅单个主题或多个主题，该方法包含三个参数：

  - topic: 可传入一个字符串或一个字符串数组
  - options: 可选值，取消订阅时的配置信息
  - callback: 取消订阅时的回调函数，参数为 error，当取消订阅失败时 error 参数才存在

  ```javascript
  // 取消订阅名为 testtopic 的 Topic
  client.unsubscribe('testtopic', function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Unsubscribed')
    }
  })
  ```

- `Client.end([force], [options], [callback])`

  关闭客户端，该方法包含三个参数:

  - force: 设置为 true 时将立即关闭客户端，而无需等待断开连接的消息被接受。这个参数是可选的，默认为 false。**注意**：使用该值为 true 时，Broker 无法接收到 disconnect 的报文
  - options: 可选值，关闭客户端时的配置信息，主要是可以配置 reasonCode，断开连接时的 Reason Code
  - callback: 当客户端关闭时的回调函数

  ```javascript
  client.end()
  ```

#### MQTT 5.0

MQTT.js 全面支持 MQTT 5.0 协议，提供了多项新功能和改进。本节将介绍如何在 MQTT.js 中使用 MQTT 5.0 的主要特性。

- 会话过期间隔：允许客户端指定会话的保持时间。

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      protocolVersion: 5,
      clean: true,
      properties: {
        sessionExpiryInterval: 300 // 300秒
      }
    })
    ```

- 主题别名：使用简短的整数别名替代长主题字符串，减少网络流量。

    ```javascript
    client.publish('long/topic/name', 'message', {
      properties: {
        topicAlias: 1
      }
    })

    // 后续发布可直接使用别名
    client.publish('', 'another message', {
      properties: {
        topicAlias: 1
      }
    })
    ```

- 用户属性：允许在消息中添加自定义键值对。

    ```javascript
    client.publish('topic', 'message', {
      properties: {
        userProperties: {
          'custom-key': 'custom-value'
        }
      }
    })
    ```

- 订阅标识符：用于识别特定的订阅。

    ```javascript
    client.subscribe('topic', {
      properties: {
        subscriptionIdentifier: 123
      }
    })

    client.on('message', (topic, message, packet) => {
      if (packet.properties.subscriptionIdentifier === 123) {
        console.log('收到来自订阅 123 的消息')
      }
    })
    ```

- 请求响应：实现请求-响应模式。

    ```javascript
    client.publish('request/topic', 'request', {
      properties: {
        responseTopic: 'response/topic',
        correlationData: Buffer.from('request-1')
      }
    })

    client.subscribe('response/topic')
    client.on('message', (topic, message, packet) => {
      if (packet.properties.correlationData) {
        console.log('收到响应，对应请求：', packet.properties.correlationData.toString())
      }
    })
    ```

- 消息过期间隔：为消息设置有效期。

    ```javascript
    client.publish('topic', 'message', {
      properties: {
        messageExpiryInterval: 60 // 60秒
      }
    })
    ```

- 遗嘱延迟间隔：延迟发送遗嘱消息。

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      will: {
        topic: 'will/topic',
        payload: 'client gone offline',
        properties: {
          willDelayInterval: 30 // 30秒
        }
      }
    })
    ```

- 接收最大值：控制未确认的 PUBLISH 报文的最大数量。

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      properties: {
        receiveMaximum: 100
      }
    })
    ```

- 最大报文大小：指定客户端能接受的最大报文大小。

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      properties: {
        maximumPacketSize: 100 * 1024 // 100 KB
      }
    })
    ```

这些示例展示了 MQTT.js 中一些重要的 MQTT 5.0 特性。使用这些特性可以提高应用程序的灵活性和效率。在使用这些特性时，请确保您的 MQTT 服务器支持 MQTT 5.0 协议。

如需了解 MQTT.js 的完整 API 文档，包括所有 MQTT 5.0 属性，请参阅 [MQTT.js GitHub 仓库](https://github.com/mqttjs/MQTT.js)。

## MQTT.js 常见问题

### 浏览器中能实现双向认证连接吗？

不可以，在浏览器环境中无法通过 JavaScript 代码指定客户端证书来建立连接，即使您的操作系统证书存储或智能卡中已设置了客户端证书。这意味着 MQTT.js 在浏览器中也无法实现双向认证。此外，您也不能指定证书颁发机构(CA)，因为这些都是由浏览器控制的。

参考: [https://github.com/mqttjs/MQTT.js/issues/1515](https://github.com/mqttjs/MQTT.js/issues/1515)

### MQTT.js 可以与 TypeScript 一起使用吗？

可以。MQTT.js 库中已包含 TypeScript 的类型定义文件，可以直接在 TypeScript 项目中使用。

类型定义文件位置: [https://github.com/mqttjs/MQTT.js/tree/main/types](https://github.com/mqttjs/MQTT.js/tree/main/types)

以下是使用 TypeScript 的示例代码:

```typescript
import * as mqtt from "mqtt"
const client: mqtt.MqttClient = mqtt.connect('mqtt://broker.emqx.io:1883')
```

### 一个 MQTT.js 客户端可以同时连接多个 Broker 吗？

不可以，每个 MQTT.js 客户端实例只能同时连接到一个 Broker。如果您需要连接多个 Broker，就需要创建多个 MQTT.js 客户端实例。

### MQTT.js 可以在 Vue、React 或 Angular 应用中使用吗？

完全可以。MQTT.js 是一个通用的 JavaScript 库，可以集成到任何基于 JavaScript 的应用中，包括使用 Vue、React 或 Angular 框架的项目。

### WebSocket 连接无法建立怎么办？

使用 WebSocket 连接时，如果协议、端口和主机都正确，但仍然无法连接，请确保添加了正确的路径。WebSocket 连接通常需要指定一个特定的路径，例如 `/mqtt` 或 `/ws`。检查您的 Broker 配置，确保使用了正确的 WebSocket 路径。

## MQTT.js 高级用法

### 如何调试 MQTT.js 应用程序

调试 MQTT.js 应用程序是开发过程中的一个重要部分。本指南解释了如何在 Node.js 和浏览器环境中启用 MQTT.js 调试日志，以及何时使用网络协议分析器（如 Wireshark）进行更深入的故障排除。

**在 Node.js 中调试 MQTT.js**

在 Node.js 环境中，您可以通过使用 `DEBUG` 环境变量来启用 MQTT.js 调试日志：

```bash
DEBUG=mqttjs* node your-app.js
```

您将看到调试信息打印出来，您可以将其与每个步骤进行比较，以查看 MQTT 消息在传输过程中发生了什么。

```bash
DEBUG=mqttjs* node index.js
mqttjs connecting to an MQTT broker... +0ms
mqttjs:client MqttClient :: options.protocol mqtt +0ms
mqttjs:client MqttClient :: options.protocolVersion 4 +0ms
mqttjs:client MqttClient :: options.username emqx_test +1ms
mqttjs:client MqttClient :: options.keepalive 60 +0ms
mqttjs:client MqttClient :: options.reconnectPeriod 1000 +0ms
mqttjs:client MqttClient :: options.rejectUnauthorized undefined +0ms
mqttjs:client MqttClient :: options.topicAliasMaximum undefined +0ms
mqttjs:client MqttClient :: clientId emqx_nodejs_986165 +0ms
mqttjs:client MqttClient :: setting up stream +0ms
mqttjs:client _setupStream :: calling method to clear reconnect +1ms
mqttjs:client _clearReconnect : clearing reconnect timer +0ms
mqttjs:client _setupStream :: using streamBuilder provided to client to create stream +0ms
mqttjs calling streambuilder for mqtt +3ms
mqttjs:tcp port 1883 and host broker.emqx.io +0ms
mqttjs:client _setupStream :: pipe stream to writable stream +3ms
mqttjs:client _setupStream: sending packet `connect` +2ms
mqttjs:client sendPacket :: packet: { cmd: 'connect' } +0ms
mqttjs:client sendPacket :: emitting `packetsend` +1ms
mqttjs:client sendPacket :: writing to stream +0ms
mqttjs:client sendPacket :: writeToStream result true +11ms
...
```

执行此命令将在控制台中生成调试日志，提供有关您的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools) 操作的详细信息，如连接、消息发布和订阅，以及潜在的错误。

**在浏览器中调试 MQTT.js**

在浏览器环境中调试时，需要在 JavaScript 代码中设置 localStorage 对象的特定值：

```bash
localStorage.debug = 'mqttjs*'
```

刷新浏览器后，MQTT.js 将开始将详细的调试信息记录到 **浏览器的 Console** 中，这对于调试 MQTT 通过 WebSocket 连接特别有用。

如果您无法使用 MQTT.js 调试日志修复问题，请尝试使用网络协议分析器（如 Wireshark）。它可以捕获和解释您的 MQTT.js 应用程序和 MQTT Broker 之间的网络流量，显示 MQTT 通信的具体信息，IP 地址，端口号和 TCP 握手。通过从 MQTT.js 调试日志开始，并在需要时切换到 Wireshark，您可以全面排查您的 MQTT.js 应用程序。

### 使用 RxJS 优化 MQTT.js 的消息处理

> RxJS 是一个用于 JavaScript 的响应式编程库，它遵循观察者模式和函数式编程原则。它为开发者简化了异步数据流和事件流的处理，并提供了各种操作符，包括 map、filter 和 reduce，用于转换和组合这些流。

在实际开发中，MQTT 服务器会向客户端发送各种类型的消息，这些消息需要被处理。例如，我们可能需要将消息保存到数据库或在处理后在 UI 上渲染它们。然而，使用 MQTT.js 时，我们必须依赖回调来处理这些消息，每收到一条消息就会触发回调函数。这可能会导致性能问题，特别是在处理高频消息时，频繁的回调调用可能会成为瓶颈。

通过利用 RxJS 的强大功能，我们可以更方便、高效地处理 MQTT.js 的消息。RxJS 可以将 MQTT.js 的消息订阅转换为可观察对象，这使我们更容易处理异步数据流和事件流。此外，RxJS 提供了一系列操作符，允许我们转换和过滤消息，使我们能够更高效地处理它们。RxJS 还可以帮助我们实现高级功能，如合并或分割多个流。另外，RxJS 可以提供消息缓存和处理延迟功能，使复杂数据流的处理更加方便和灵活。

下面，我们将通过一个简单的例子来演示如何使用 RxJS 优化 MQTT.js 的消息处理。

```javascript
import { fromEvent } from 'rxjs'
import { bufferTime, map, takeUntil } from 'rxjs/operators'

// 将连接关闭事件转换为 Observable
const unsubscribe$ = fromEvent(client, 'close')

// 将消息订阅转换为 Observable，继续接收和处理消息，直到连接关闭
const message$ = fromEvent(client, 'message').pipe(takeUntil(unsubscribe$)).pipe(
  map(([topic, payload, packet]: [string, Buffer, IPublishPacket]) => {
    return processMessage(topic, payload, packet)
  }),
)

// 使用 filter 过滤系统消息
const nonSYSMessage$ = message$.pipe(filter((message: MessageModel) => !message.topic.includes('$SYS')))

// 使用 bufferTime 缓存消息，并按每秒一次的频率将它们保存到数据库中
nonSYSMessage$.pipe(bufferTime(1000)).subscribe((messages: MessageModel[]) => {
  messages.length && saveMessage(id, messages)
})

// 使用 bufferTime 缓存消息，并按每秒两次的频率在 UI 上渲染它们
nonSYSMessage$.pipe(bufferTime(500)).subscribe((messages: MessageModel[]) => {
  messages.length && renderMessage(messages)
})
```

## 总结

至此就简单的介绍了 MQTT.js 一些常用的 API 的使用方法等，具体在实际项目中的使用请参考以下链接：

- [如何在 Vue 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-vue)

- [如何在 React 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-react)
- [如何在 Electron 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-electron)
- [如何在 Node.js 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-nodejs)
- [使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
