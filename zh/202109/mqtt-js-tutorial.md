## 简介

[MQTT.js](https://github.com/mqttjs/MQTT.js) 是一个开源的 [MQTT 协议](https://www.emqx.com/zh/mqtt)的客户端库，使用 JavaScript 编写，主要用于 Node.js 和 浏览器环境中。是目前 JavaScript 生态中使用最为广泛的 [MQTT 客户端库](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)。

> MQTT 是一种基于发布/订阅模式的轻量级物联网消息传输协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。

由于 JavaScript 单线程特性，MQTT.js 是全异步 MQTT 客户端，MQTT.js 支持 MQTT/TCP、MQTT/TLS、MQTT/WebSocket，在不同运行环境支持的度如下：

- 浏览器环境：MQTT over WebSocket（包括微信小程序、支付宝小程序等定制浏览器环境）
- Node.js 环境：MQTT、MQTT over WebSocket

不同环境里除了少部分连接参数不同，其他 API 均是相同的。且在 MQTT.js v3.0.0 及以上版本后，已经完整支持到 MQTT 5.0。

## 安装

### 使用 npm 或 yarn 安装

```shell
npm install mqtt --save

# 或使用 yarn

yarn add mqtt
```

**注意**：如果您的 Node 环境是 v12 或 v14 及以上版本，请使用 MQTT.js 4.0.0 及以上版本

### 使用 CDN 安装

在浏览器环境中，我们还可以使用 CDN 的方式引入 MQTT.js。MQTT.js 的 bundle 包通过 [http://unpkg.com](http://unpkg.com/) 管理，我们可以直接添加 [unpkg.com/mqtt/dist/mqtt.min.js](https://unpkg.com/mqtt/dist/mqtt.min.js) 来进行使用。

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

本文将使用 EMQ X Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQ X Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQ X Cloud 文档](https://docs.emqx.cn/cloud/latest/)。

### 简单例子

我们简单编写一段代码实现连接到 EMQ X Cloud 的并完成订阅主题、收发消息的例子：

```javascript
const mqtt = require('mqtt')
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Auth
  clientId: 'emqx_test',
  username: 'emqx_test',
  password: 'emqx_test',
}
const client  = mqtt.connect('mqtt://broker.emqx.io:1883')
client.on('connect', function () {
  console.log('Connected')
  client.subscribe('test', function (err) {
    if (!err) {
      client.publish('test', 'Hello mqtt')
    }
  })
})

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

### API 介绍

#### mqtt.connect([url], options)

连接到指定的 MQTT Broker 的函数，并始终返回一个 Client 对象。第一个参数传入一个 URL 值，URL 可以是以下协议：`mqtt`, `mqtts`, `tcp`, `tls`, `ws`, `wss`。URL 也可以是一个由 URL.parse() 返回的对象。然后再传入一个 Options 对象，用于配置 MQTT 连接时的选项。下面列举一些常用的 Options 对象中的属性值：

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
  - `properties`: [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 新增，可配置的对象的属性值，详情请参考：[https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options)

- 如果需要配置 SSL/TLS 连接，Option 对象会被传递给 [`tls.connect()`](http://nodejs.org/api/tls.html#tls_tls_connect_options_callback) ，因此可以在 option 中配置以下属性
  - `rejectUnauthorized`: 是否验证服务端证书链和地址名称，设置为 false 时将跳过验证，会暴露在中间人的攻击之下，所以不建议在生产环境中使用这种配置，当设置为 true 时，将开启强认证模式，且如果是自签名证书，请在证书配置时设置 Alt name。
  - `ca`:  只有在服务器使用自签名证书时才有必要，自签名证书中生成的 CA 文件
  - cert: 只有当服务器需要客户证书认证时才有必要（双向认证），客户端证书
  - key: 只有当服务器需要客户证书认证时才有必要（双向认证），客户端密钥

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

  当客户端收到一个发布过来的 Payload 时触发，其中包含三个参数，topic、payload 和 packet，其中 topic 为接收到的消息的 topic，payload 为接收到的消息内容，packet 为 MQTT 报文信息，其中包含 QoS、retain 等信息

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

## 总结

至此就简单的介绍了 MQTT.js 一些常用的 API 的使用方法等，具体在实际项目中的使用请参考以下链接：

- [如何在 Vue 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-vue)
- [如何在 React 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-react)
- [如何在 Electron 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-electron)
- [如何在 Node.js 项目中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-nodejs)
- [使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)
