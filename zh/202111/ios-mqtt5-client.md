2017 年 8 月，OASIS MQTT Technical Committee 正式发布了用于 Public Review 的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 的草案。2018 年，MQTT 5.0 正式发布，然而直到目前苹果生态里仍没有完整支持 MQTT 5.0 的客户端 SDK 。

[CocoaMQTT](https://github.com/emqx/CocoaMQTT) 是 EMQ 团队为 iOS 开发者提供的 MQTT 客户端 SDK，目前在 iOS 开发者中有着较为广泛的使用。

为弥补苹果生态中对 MQTT 5.0 支持方面的空白，**EMQ 团队于近日正式发布了 CocoaMQTT 全新版本 v2.0**。CocoaMQTT v2.0 支持 MQTT 5.0，同时兼容 3.1.1 版本，支持 iOS、tvOS 与 OSX 操作系统。用户现已可通过 CocoaMQTT 实现 iOS 系统设备连接 MQTT 5.0 云服务，享受 MQTT 5.0 带来的强大功能加成。

CocoaMQTT 使用 Swift 语言开发，而非 Objective-C。这是因为 Swift 是一门类型安全的语言，对协议的支持更加丰富，配合扩展（extension）、泛型、关联类型等可以实现面向协议编程，从而大大提高代码的灵活性。

此外，在 WWDC 2021 大会上，苹果宣布了 Swift 语言中并发模型的重大更新：通过编译器实现的 Actor 并发模型，新增 Actor 引用类型帮助开发者避免数据竞争问题。

因此，我们相信在 [MQTT](https://www.emqx.com/zh/mqtt) 相关的 I/O 密集型并发应用中，相较于 Objective-C，Swift 的表现将更值得期待。

## MQTT 5.0 vs MQTT 3.1.1

MQTT 3.1.1 仍然有很多不完善的地方，例如连接异常断开时无法通知原因到对端。MQTT 5.0 在 MQTT 3.1.1 的基础上做了很多改变，但并不是向下兼容的。

MQTT 协议 5.0 版本新增了会话/消息延时功能、原因码、主题别名、in-flight 流控、用户属性、共享订阅等功能，以及用于增强认证安全的 AUTH 报文。其中，原因码和用户属性 `Property`字段使得 MQTT 5.0 能够携带更多上下文信息，从而解决在 3.1.1 版本因协议不完整而较难处理的问题。

MQTT 5.0 的主要功能优势有：

- 进一步支持更大规模的可扩展系统
- 更加详细的错误报告和处理机制
- 容量探索和请求响应等通用模式的规范化操作
- 可扩展的用户属性 （User Property）
- 改进性能并支持小型客户端
- 会话保持和消息超时设置
- 新增支持 Req/Rsp 消息模式

## CocoaMQTT 客户端的使用

本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 进行 CocoaMQTT 功能使用介绍，该服务基于 [MQTT 云服务](https://www.emqx.com/zh/cloud) EMQ X Cloud 创建。

服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**
- TCP/TLS 端口: **8883**
- Websocket/TLS 端口:**8084**

### 连接 MQTT 服务

我们看到 MQTT 5.0 增加了许多属性，其中 `Property` 字段可以让使用者根据自己的情况，更加细致化去完成需求。

```swift
///MQTT 5.0
let clientID = "CocoaMQTT-" + String(ProcessInfo().processIdentifier)
let mqtt5 = CocoaMQTT5(clientID: clientID, host: "broker-cn.emqx.io", port: 1883)

let connectProperties = MqttConnectProperties()
connectProperties.topicAliasMaximum = 0
connectProperties.sessionExpiryInterval = 0
connectProperties.receiveMaximum = 100
connectProperties.maximumPacketSize = 500
mqtt5.connectProperties = connectProperties

mqtt5.username = "test"
mqtt5.password = "public"
mqtt5.willMessage = CocoaMQTTWill(topic: "/will", message: "dieout")
mqtt5.keepAlive = 60
mqtt5.delegate = self
mqtt5.connect()

///MQTT 3.1.1
let clientID = "CocoaMQTT-" + String(ProcessInfo().processIdentifier)
let mqtt = CocoaMQTT(clientID: clientID, host: "broker-cn.emqx.io", port: 1883)
mqtt.username = "test"
mqtt.password = "public"
mqtt.willMessage = CocoaMQTTWill(topic: "/will", message: "dieout")
mqtt.keepAlive = 60
mqtt.delegate = self
mqtt.connect()

```

### 订阅主题

MQTT 5.0 在 MQTT 3.1.1 上面多了订阅选项等操作。

```swift
///MQTT 5.0
mqtt5.subscribe("chat/room/animals/client/+", qos: CocoaMQTTQoS.qos1)
//or
//let subscriptions : [MqttSubscription] = [MqttSubscription(topic: "chat/room/animals/client/+"),MqttSubscription(topic: "chat/room/foods/client/+"),MqttSubscription(topic: "chat/room/trees/client/+")]
//mqtt.subscribe(subscriptions)

///MQTT 3.1.1
mqtt.subscribe("chat/room/animals/client/+", qos: CocoaMQTTQoS.qos1)
//or
//let subscriptions : [(String, CocoaMQTTQoS)] = [("chat/room/animals/client/+", qos: CocoaMQTTQoS.qos1),("chat/room/foods/client/+", qos: CocoaMQTTQoS.qos1),("chat/room/trees/client/+", qos: CocoaMQTTQoS.qos1)]
//mqtt.subscribe(subscriptions)

```

###  发布消息

```swift
///MQTT 5.0
mqtt5!.publish("chat/room/animals/client/" + animal!, withString: message!, qos: .qos1, DUP: false, retained: false, properties: publishProperties)

///MQTT 3.1.1
mqtt!.publish("chat/room/animals/client/" + animal!, withString: message!, qos: .qos1)

```

### 自动重连

MQTT 是基于 TCP 长连接的协议，在实际使用的场景中，由于网络故障或信号问题导致连接中断是经常出现的问题。许多开发者会希望 SDK 能够提供方便的自动重连方式。

```swift
///MQTT 5.0
mqtt5!.autoReconnect = true

///MQTT 3.1.1
mqtt!.autoReconnect = true
```

### 单双向 SSL 连接

```swift
///MQTT 5.0
mqtt5!.enableSSL = true

///MQTT 3.1.1
mqtt!.enableSSL = true

let clientCertArray = getClientCertFromP12File(certName: "client-keycert", certPassword: "MySecretPassword")
var sslSettings: [String: NSObject] = [:]
sslSettings[kCFStreamSSLCertificates as String] = clientCertArray

///MQTT 5.0
mqtt5!.sslSettings = sslSettings

///MQTT 3.1.1
mqtt!.sslSettings = sslSettings

```

如果需要.p12文件可以在终端使用以下语句生成

```bash
1openssl pkcs12 -export -clcerts -in client-cert.pem -inkey client-key.pem -out client.p12
```

### 设置保留消息和遗嘱消息

MQTT 5.0 与 MQTT 3.1.1 比，多了更多的属性设置可供用户使用。

```swift
///MQTT 5.0
let lastWillMessage = CocoaMQTTMessage(topic: "/chat/room/animals/client/Sheep", string: "dieout")
lastWillMessage.retained = true
lastWillMessage.qos = .qos1
mqtt5!.willMessage = lastWillMessage

///MQTT 3.1.1
mqtt!.willMessage = CocoaMQTTMessage(topic: "/will", string: "dieout")

```

### AUTH 报文

MQTT 单纯通过 `CONNECT` 可能无法提供足够的信息给 Server 进行身份认证，所以 MQTT 5.0 新增此功能。用于客户端和服务器之间的加强认证。

```swift
  let authProperties = MqttAuthProperties()
        mqtt5!.auth(reasonCode: CocoaMQTTAUTHReasonCode.continueAuthentication, authProperties: authProperties)
```

## iOS 应用后台运行

推荐使用 「Background fetch」模式或 IOS 13 新增的「Background processing」模式。

![iOS 应用后台运行](https://static.emqx.net/images/7d487fe5022b5c2785c4df43adf9f983.png)

如果使用 `beginBackgroundTaskWithName` 和 `endBackgroundTask` 相关的 API，可以保持 APP 在后台运行 30 秒。

 

## 总结

至此，我们完成了使用 CocoaMQTT 客户端连接到公共 MQTT 服务器，并实现了客户端与 MQTT 服务器的连接、消息发布和订阅。

项目完整代码请见 [https://github.com/emqx/CocoaMQTT/tree/master/Example](https://github.com/emqx/CocoaMQTT/tree/master/Example)。

EMQ 致力于帮助用户轻松便捷地使用 MQTT 开展物联网业务，我们的一系列客户端 SDK 均在持续开发中，敬请关注。
