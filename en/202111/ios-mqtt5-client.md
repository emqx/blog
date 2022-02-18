In August 2017, the draft of MQTT 5.0 was officially released by the OASIS MQTT Technical Committee for Public Review. In 2018, the official version of MQTT 5.0 was released. However, there is still no client SDK that fully supports [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) in the Apple ecosystem.

[CocoaMQTT](https://github.com/emqx/CocoaMQTT) is an MQTT client SDK provided by the EMQ for iOS developers, which is widely used by them at present. To make up for the gap in support of MQTT 5.0 in the Apple ecosystem, the **EMQ team officially released the new CocoaMQTT v2.0 recently.** CocoaMQTT v2.0 supports MQTT 5.0, is compatible with version 3.1.1, and supports iOS, tvOS, and OSX operating systems. Users can now connect iOS system devices to the MQTT 5.0 cloud services through CocoaMQTT and enjoy the powerful features provided by MQTT5.0.

CocoaMQTT is developed in Swift language instead of Objective-C. This is because Swift is a type-safe language with richer support for protocols. Protocol-oriented programming can be realized in combination with extension, generics, and association types, which greatly improves the flexibility of the code.

In addition, at the WWDC 2021 conference, Apple announced a major update of the concurrency model in Swift language: the Actor concurrency model implemented by the compiler and the new actor reference type can help developers avoid data competition issues. Therefore, we also believe that in MQTT-related I/O-intensive concurrent applications, Swift's performance will be more expected than that of Objective-C.

## MQTT 5.0 vs MQTT 3.1.1

There are still many imperfections in MQTT 3.1.1. For example, when the connection is abnormally disconnected, the opposite end cannot notify the reason. For MQTT 5.0, it has made many changes based on MQTT 3.1.1, but it is not backward compatible. MQTT 5.0 adds new functions such as session/message delay, reason codes, topic alias, in-flight stream control, [user properties](https://www.emqx.com/en/blog/mqtt5-user-properties), [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), as well as AUTH packet to enhance authentication security. The fields of reason code and the user properties enable MQTT 5.0 to carry more contextual information to solve the problem that is difficult to deal with in version 3.1.1 due to incomplete protocol.

The main functional advantages of MQTT 5.0 are:

- Further support for larger-scale Extensible systems
- More detailed error reporting and handling mechanism
- Standardized operation of general modes such as capacity exploration and request-response
- Extensible User Property
- Improve performance and support small clients
- Session retention and message timeout settings
- New support for Req/Rsp message mode

## How to use MQTT in iOS client - CocoaMQTT

This article will use the [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ to introduce the CocoaMQTT function. This service is created based on the [MQTT Cloud service - EMQX Cloud](https://www.emqx.com/en/cloud).

The broker access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**
- TCP/TLS Port: **8883**
- Websocket/TLS Port:**8084**

### Connect to MQTT service

We see that many properties have been added in MQTT 5.0, among which the `Property` field allows users to fulfill their requirements in a more detailed way according to their own situation.

```swift
///MQTT 5.0
let clientID = "CocoaMQTT-" + String(ProcessInfo().processIdentifier)
let mqtt5 = CocoaMQTT5(clientID: clientID, host: "broker.emqx.io", port: 1883)

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
let mqtt = CocoaMQTT(clientID: clientID, host: "broker.emqx.io", port: 1883)
mqtt.username = "test"
mqtt.password = "public"
mqtt.willMessage = CocoaMQTTWill(topic: "/will", message: "dieout")
mqtt.keepAlive = 60
mqtt.delegate = self
mqtt.connect()

```

### Subscribe

MQTT 5.0 has more operations such as [subscription options](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options) than of MQTT 3.1.1.

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

### Publish

```swift
///MQTT 5.0
mqtt5!.publish("chat/room/animals/client/" + animal!, withString: message!, qos: .qos1, DUP: false, retained: false, properties: publishProperties)

///MQTT 3.1.1
mqtt!.publish("chat/room/animals/client/" + animal!, withString: message!, qos: .qos1)

```

### Reconnect automatically

MQTT is a protocol based on TCP long connections. In actual scenarios, connection interruption due to network failures or signal problems is a common problem. Many developers hope that the SDK can provide a convenient way to reconnect automatically.

```swift
///MQTT 5.0
mqtt5!.autoReconnect = true

///MQTT 3.1.1
mqtt!.autoReconnect = true

```

### Single-way and two-way SSL

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

If you need a `.p12` file, you can generate it at the terminal using the following statement.

```bash
openssl pkcs12 -export -clcerts -in client-cert.pem -inkey client-key.pem -out client.p12
```

### Set retained message and will message

Compared with MQTT 3.1.1, MQTT 5.0 has more property settings for users to use.

```swift
///MQTT 5.0
let lastWillMessage = CocoaMQTTMessage(topic: "/chat/room/animals/client/Sheep", string: "dieout")
lastWillMessage.retained = true
lastWillMessage.qos = .qos1
mqtt5!.willMessage = lastWillMessage

///MQTT 3.1.1
mqtt!.willMessage = CocoaMQTTMessage(topic: "/will", string: "dieout")

```

### AUTH packet

MQTT may not provide enough information for the server to perform authentication through `CONNECT` alone, so this feature is added in MQTT 5.0, which is used to strengthen authentication between the client and the server.

```swift
let authProperties = MqttAuthProperties()
        mqtt5!.auth(reasonCode: CocoaMQTTAUTHReasonCode.continueAuthentication, authProperties: authProperties)
 
```

### iOS application running in the background

It is recommended to use the 「Background fetch」 mode or the newly added 「Background processing」 mode in IOS 13.

![iOS application running in the background](https://static.emqx.net/images/7d487fe5022b5c2785c4df43adf9f983.png) 

If you use the APIs related to `beginBackgroundTaskWithName` and `endBackgroundTask`, you can keep the APP running in the background for 30 seconds.

 

## Summary

So far, we have connected the CocoaMQTT client to the public MQTT Broker and realized the connection, message publishing, and subscription between the client and the [MQTT Broker](https://www.emqx.io).

> Get the code from [https://github.com/emqx/CocoaMQTT/tree/master/Example](https://github.com/emqx/CocoaMQTT/tree/master/Example). 

EMQ is committed to helping users easily and conveniently use MQTT to carry out IoT business. A series of our client SDKs are under continuous development, please stay tuned.
