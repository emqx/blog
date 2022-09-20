[Node.js](https://nodejs.org/zh-cn/) 是一个基于 [Chrome V8 引擎](https://v8.dev/) 的 JavaScript 运行时环境。在 Node.js 出现之前，JavaScript 通常作为客户端程序设计语言使用，以 JavaScript 写出的程序常在用户的浏览器上运行。Node.js 的出现使 JavaScript 也能用于服务端编程。

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的轻量级物联网消息传输协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

本文主要介绍如何在 Node.js 项目中使用 MQTT 实现客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

## MQTT 客户端库选择

[MQTT.js](https://github.com/mqttjs/MQTT.js) 是一个 MQTT 协议的客户端库，使用 JavaScript 编写，用于 Node.js 和 浏览器环境中。是 JavaScript 生态中目前使用最为广泛的 [MQTT 客户端库](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)。

## 项目初始化

### 确认 Node.js 版本

本项目使用 Node.js v14.14.0 进行开发和测试，读者可用如下命令确认 Node.js 的版本

```shell
node --version

v14.14.0
```

### 使用 npm 安装 MQTT.js 客户端库

```shell
# 新建项目
npm init -y

# 安装依赖
npm install mqtt --save
```

完成后我们在当前目录下新建一个 index.js 文件作为项目的入口文件，在该文件中来实现 MQTT 连接测试的完整逻辑。

## Node.js MQTT 使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**（国内可以使用 broker-cn.emqx.io）
- TCP Port: **1883**
- SSL/TLS Port: **8883**

引入 MQTT.js 客户端库

> 注意：在 Node.js 环境中，导入依赖模块请使用 commonjs 规范

```javascript
const mqtt = require('mqtt')
```

### 设置 MQTT Broker 的连接参数

设置 MQTT Broker 连接地址，端口以及 topic，这里我们使用 JavaScript 中的生成随机数的函数来生成客户端 ID。

```javascript
const host = 'broker.emqx.io'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`
```

### 编写 MQTT 连接函数

我们使用刚才设置的连接参数来进行连接，连接的 URL 通过上面定义的 host、port 端口来进行拼接。然后调用 mqtt 模块内置的 connect 函数，连接成功后返回一个 Client 实例。

```javascript
const connectUrl = `mqtt://${host}:${port}`

const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
})
```

### 订阅主题

使用返回的 Client 实例的 on 方法来监听连接成功状态，并在连接成功后的回调函数中订阅 topic。此时我们连接成功后调用 Client 实例的 subscribe 方法订阅 `/nodejs/mqtt` 主题。

```javascript
const topic = '/nodejs/mqtt'
client.on('connect', () => {
  console.log('Connected')
  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
})
```

订阅主题成功后，我们再使用 on 方法来监听接收消息的方法，当接受到消息时，我们可以在该方法的回调函数中获取到 topic 和 message 消息。

> 注意：回调函数中的 message 是 Buffer 类型，需要使用 toString 方法将其转化为字符串

```javascript
client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})
```

### 消息发布

完成上述的订阅主题和消息监听后，我们再来编写一个发布消息的方法。

> 注意：消息发布需要在 MQTT 连接成功以后，因此这里我们写到 Connect 成功的回调函数里

```java
client.on('connect', () => {
  client.publish(topic, 'nodejs mqtt test', { qos: 0, retain: false }, (error) => {
    if (error) {
      console.error(error)
    }
  })
})
```

## 完整代码

服务器连接、主题订阅、消息发布与接收的代码。

```javascript
const mqtt = require('mqtt')

const host = 'broker.emqx.io'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `mqtt://${host}:${port}`
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
})

const topic = '/nodejs/mqtt'
client.on('connect', () => {
  console.log('Connected')
  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
  client.publish(topic, 'nodejs mqtt test', { qos: 0, retain: false }, (error) => {
    if (error) {
      console.error(error)
    }
  })
})
client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})
```

项目完整代码请见：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Node.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Node.js)

## 测试

我们在 package.json 文件中的脚本字段中添加一行启动脚本。

```json
"scripts": {
  "start": "node index.js"
}
```

然后就可以简单使用 `npm start` 来运行项目。

```shell
npm start
```

运行后我们可以看到控制的输出信息如下：

![NodeJS MQTT 启动](https://assets.emqx.com/images/9897e6cd56163dfe7139cf6d84361e63.png)

我们看到了客户端已经成功连接到 [MQTT 服务器](https://www.emqx.io/zh)并且订阅主题、接收和发布消息成功。此时我们再使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 作为另一个客户端进行消息收发测试。

![MQTT 5.0 客户端工具 - MQTT X](https://assets.emqx.com/images/5c841598f78eed0b186572165832f861.png)

可以看到控制台内打印出了 MQTT X 发送过来的消息。

![控制台接收到 MQTT X 发送的消息](https://assets.emqx.com/images/02d8a35312ca1309f18a628dacca8910.png)

至此，我们完成了使用 Node.js 来作为 MQTT 客户端连接到[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
