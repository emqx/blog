MQTT v5 带来了很多新的特性，我们会尽量以通俗易懂的方式展示这些特性，并探讨这些特性对开发者的影响。到目前为止，我们已经探讨过这些 [MQTT v5 新特性](https://www.emqx.com/zh/blog/introduction-to-mqtt-5)，今天我们将继续讨论： **用户属性**。

## 什么是用户属性

用户属性（User Properties）其实是一种自定义属性，允许用户向 MQTT 消息添加自己的元数据，传输额外的自定义信息以扩充更多应用场景。

它由一个用户自定义的 UTF-8 的键/值对数组组成，并在消息属性字段中配置，只要不超过最大的消息大小，可以使用无限数量的用户属性来向 MQTT 消息添加元数据，并在发布者、[MQTT 服务器](https://www.emqx.io/zh)和订阅者之间传递信息。

如果你熟悉 HTTP 协议的话，该功能与 HTTP 的 Header 的概念非常类似。用户属性有效地允许用户扩展 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)，并且可以出现在所有消息和响应中。因为用户属性是由用户定义的，它们只对该用户的实现有意义。

## 为什么需要使用用户属性

MQTT 3 的协议扩展性能力较差，用户属性其实就是为了解决这个问题，它支持在消息中传递任何信息，确保了用户可扩展标准协议的功能。

对于选择和配置不同的消息类型，用户属性可以在客户端与 MQTT 服务器之间，或者客户端和客户端之间发送。在连接客户端中配置用户属性时，只能在 MQTT 服务器上接收，无法在客户端中接收。如果在发送消息的时候配置用户属性，则可以在其它客户端中接收。常用的有以下两种用户属性配置。

### 连接客户端的用户属性

当客户端与 MQTT 服务器发起连接时，服务器可以预先定义好一些需要并且可以使用到的元数据信息，即用户属性，当连接成功后，MQTT 服务可以拿到连接发送过来的相关信息进行使用，因此连接客户端的用户属性依赖于 MQTT 服务器。

### 消息发布的用户属性

消息发布时的用户属性可能是较为常用的，因为它们可以在客户端与客户端之间进行元数据信息传递。比如可以在发布时添加一些常见的信息：消息编号，时间戳，文件，客户端信息和路由信息等属性。

除上述较为常用的用户属性设置外，还可以在订阅 Topic 时，取消订阅时，断开连接时配置用户属性。

## 用户属性的使用

### 文件传输

MQTT 5 的用户属性，可扩展为使用其进行文件传输，而不是像之前的 MQTT 3 中将数据放到消息体的 Payload 中，用户属性使用键值对的方式。这也意味着文件可以保持为二进制，因为文件的元数据在用户属性中。例如：

```json
{
  "filename": "test.txt",
  "content": "xxxx"
}
```

### 资源解析

当客户端连接到 MQTT 服务器后，不同的客户端、供应商平台或系统存在着不同的方式传递消息数据，消息数据的格式可能都存在着一些结构差异。还有一些客户端是分布在不同的地域下。比如：地域 A 的设备发送的消息格式是 JSON 的，地域 B 的设备发送的是 XML 的，此时服务器接收到消息后可能需要一一进行判断和对比，找到合适的解析器来进行数据解析。

此时为了提高效率和减少计算负载，我们可以利用用户属性功能来添加数据格式信息和地域信息，当服务器接收到消息后，可以使用用户属性中提供的元数据来进行数据解析操作。并且当区域 A 的客户端订阅接收到来自区域 B 的客户端消息时，也能快速的清楚特定的消息的来自于哪个区域等，从而使的消息具有了可追溯性。

```json
{
  "region": "A",
  "type": "JSON"
}
```

![MQTT 资源解析](https://assets.emqx.com/images/c2f4e34d2ff553f12a81826382846366.png)

### 消息路由

我们还可以使用用户属性来做应用层级别的路由。如上所述，存在着不同的系统和平台，每个区域存在着不同的设备，多个系统可能收到同一个设备的消息，有些系统需要将数据进行实时的展示，另一个系统可能将这些数据进行时序存储。因此 MQTT 服务器可以通过上报消息中配置的用户属性来确定将消息分发到存储消息的系统还是展示数据的系统。

```json
{
  "type": "real-time",
  "timestamp": 1636620444
}
```

![MQTT 消息路由](https://assets.emqx.com/images/39dfdc8de0b0251bab3697d72169dfef.png)

## 在客户端中配置用户属性

我们以 JavaScript 环境为例，使用 [MQTT.js](https://github.com/mqttjs/MQTT.js) 客户端来进行编程。

> 注意：在连接客户端时需指定 MQTT 的版本 `protocolVersion `  为 5。

### 连接

我们在连接时的 options 中设置 properties 的 User Properties 属性，添加 type 和 region 属性。连接成功后，MQTT 服务器将收到这个用户自定义的信息。

```javascript
// connect options
const OPTIONS = {
  clientId: 'mqtt_test',
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
  protocolVersion: 5,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}
const client = mqtt.connect('mqtt://broker.emqx.io', OPTIONS)
```

### 发布消息

连接成功后发布消息，发布消息的配置中设置用户属性，并且监听消息接收。在 publish 函数中，我们配置 user properties 属性，并在接收消息的函数中打印 packet。

```
client.publish(topic, 'nodejs mqtt test', {
  qos: 0,
  retain: false,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}, (error) => {
  if (error) {
    console.error(error)
  }
})
client.on('message', (topic, payload, packet) => {
  console.log('packet:', packet)
  console.log('Received Message:', topic, payload.toString())
})
```

此时我们看到控制台中已经打印并输出了刚才发送时所配置的用户属性。

![MQTT 消息接收](https://assets.emqx.com/images/d4b8692b38ebe33f1ab126845461e667.png)

对于其它客户端，我们将在[跨平台 MQTT 5.0 桌面客户端工具 - MQTTX](https://mqttx.app/zh) 的后续版本中支持用户属性的自定义配置，方便用户快速测试 MQTT 5.0 的一些新特性，敬请期待！


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
