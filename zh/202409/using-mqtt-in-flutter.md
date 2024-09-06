## 引言

[Flutter](https://flutter.dev/) 是 Google 推出并开源的移动应用开发框架，主打跨平台、高保真、高性能。开发者可以通过 Dart 语言开发 App，一套代码同时运行在 iOS 和 Android 平台。 Flutter 提供了丰富的组件、接口，开发者可以快速地为 Flutter 添加 native 扩展。同时 Flutter 还使用 Native 引擎渲染视图，这无疑能为用户提供良好的体验。

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可在严重受限的硬件设备和低带宽、高延迟的网络上实现稳定传输。它凭借简单易实现、支持 QoS、报文小等特点，占据了物联网协议的半壁江山。

本文主要介绍如何在 Flutter 项目中使用 MQTT，实现客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

## 项目初始化

### 新建项目

新建一个项目，可以参考以下链接：

- [Set up an editor](https://docs.flutter.dev/get-started/editor?tab=androidstudio)
- [Android Studio and IntelliJ](https://docs.flutter.dev/development/tools/android-studio)

### 安装依赖

我们将使用 [mqtt_client](https://pub.dev/packages/mqtt_client) 作为依赖项。

运行以下命令:

```shell
 $ flutter pub add mqtt_client
```

这将在软件包的 `pubspec.yaml` 中添加如下一行

```
dependencies:
  mqtt_client: ^9.6.8
```

### 导入

在代码中如下导入便可以使用

```dart
import 'package:mqtt_client/mqtt_client.dart';
```

## MQTT 的使用

### 连接 MQTT 服务器

首先，请确保您有一个 [MQTT broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 可以与之通信和测试。

本文中我们将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**
- WebSocket Port: 8083
- SSL/TLS Port: 8883
- Secure WebSocket Port: 8084

详细信息请查看: [Free Public MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker).

#### TCP 连接

要建立 MQTT 连接，需要设置连接地址、端口和客户端 ID。此外，我们还可以设置用户名、密码、keep alive 等参数。

```dart
MqttServerClient client = MqttServerClient.withPort('broker.emqx.io', 'flutter_client', 1883);
client.keepAlivePeriod = 60;
final connMessage = MqttConnectMessage()
    .authenticateAs('username', 'password')
    .withWillTopic('willtopic')
    .withWillMessage('Will message')
    .startClean()
    .withWillQos(MqttQos.atLeastOnce);
client.connectionMessage = connMessage;
```

#### WebSocket

```dart
MqttServerClient client = MqttServerClient.withPort('ws://broker.emqx.io', 'flutter_client', 8083);
client.useWebSocket = true;
client.keepAlivePeriod = 60;
final connMessage = MqttConnectMessage()
    .authenticateAs('username', 'password')
    .withWillTopic('willtopic')
    .withWillMessage('Will message')
    .startClean()
    .withWillQos(MqttQos.atLeastOnce);
client.connectionMessage = connMessage;
```

接下来，我们连接到 MQTT broker。

```dart
try {
  print('Connecting');
  await client.connect();
} catch (e) {
  print('Exception: $e');
  client.disconnect();
}
print("connected");
```

#### TLS/SSL

```dart
/// Security context
SecurityContext context = new SecurityContext()
  ..useCertificateChain('path/to/my_cert.pem')
  ..usePrivateKey('path/to/my_key.pem', password: 'key_password')
  ..setClientAuthorities('path/to/client.crt', password: 'password');
client.secure = true
client.securityContext = context;
```

### 其他 MQTT 操作

#### 主题订阅

```dart
client.subscribe("topic/test", MqttQos.atLeastOnce)
```

#### 消息发布

```dart
const pubTopic = 'topic/test';
final builder = MqttClientPayloadBuilder();
builder.addString('Hello MQTT');
client.publishMessage(pubTopic, MqttQos.atLeastOnce, builder.payload);
```

#### 取消订阅

```dart
client.unsubscribe('topic/test');
```

#### 断开连接

```dart
client.disconnect();
```

### 回调

我们可以按照以下方法设置回调：

```dart
client.onConnected = onConnected;
client.onDisconnected = onDisconnected;
client.onUnsubscribed = onUnsubscribed;
client.onSubscribed = onSubscribed;
client.onSubscribeFail = onSubscribeFail;
client.pongCallback = pong;

// Connected callback
void onConnected() {
  print('Connected');
}

// Disconnected callback
void onDisconnected() {
  print('Disconnected');
}

// Subscribed callback
void onSubscribed(String topic) {
  print('Subscribed topic: $topic');
}

// Subscribed failed callback
void onSubscribeFail(String topic) {
  print('Failed to subscribe $topic');
}

// Unsubscribed callback
void onUnsubscribed(String? topic) {
  print('Unsubscribed topic: $topic');
}

// Ping callback
void pong() {
  print('Ping response client callback invoked');
}
```

- `onConnected`: 客户端连接回调，在连接成功时调用
- `onDisconnected:`客户端断连回调，在断开连接时调用
- `onUnsubscribed`: 取消订阅回调
- `onSubscribed:`订阅回调
- `onSubscribeFail:` 订阅失败回调
- `pongCallback:` Ping 响应回调

我们还可以添加以下监听器来接受消息更新：

```dart
client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
  final recMessage = c![0].payload as MqttPublishMessage;
  final payload = MqttPublishPayload.bytesToStringAsString(recMessage.payload.message);
  print('Received message:$payload from topic: ${c[0].topic}');
});
```

### 完整代码

```dart
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

Future<MqttClient> connect() async {
  MqttServerClient client = MqttServerClient.withPort('broker.emqx.io', 'flutter_client', 1883);
  client.logging(on: true);
  client.keepAlivePeriod = 60;
  client.onConnected = onConnected;
  client.onDisconnected = onDisconnected;
  client.onUnsubscribed = onUnsubscribed;
  client.onSubscribed = onSubscribed;
  client.onSubscribeFail = onSubscribeFail;
  client.pongCallback = pong;

  // Security context
//  SecurityContext context = new SecurityContext()
//    ..useCertificateChain('path/to/my_cert.pem')
//    ..usePrivateKey('path/to/my_key.pem', password: 'my_key_password')
//    ..setClientAuthorities('path/to/client.crt', password: 'password');
//  client.secure = true;
//  client.securityContext = context;

  final connMess = MqttConnectMessage()
      .authenticateAs("username", "password")
      .withWillTopic('willtopic')
      .withWillMessage('My Will message')
      .startClean() // Non persistent session for testing
      .withWillQos(MqttQos.atLeastOnce);
  client.connectionMessage = connMess;
  try {
    print('Connecting');
    await client.connect();
  } catch (e) {
    print('Exception: $e');
    client.disconnect();
  }
  print("connected");

  client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
    final recMessage = c![0].payload as MqttPublishMessage;
    final payload = MqttPublishPayload.bytesToStringAsString(recMessage.payload.message);

    print('Received message:$payload from topic: ${c[0].topic}');
  });

  return client;
}

// Connected callback
void onConnected() {
  print('Connected');
}

// Disconnected callback
void onDisconnected() {
  print('Disconnected');
}

// Subscribed callback
void onSubscribed(String topic) {
  print('Subscribed topic: $topic');
}

// Subscribed failed callback
void onSubscribeFail(String topic) {
  print('Failed to subscribe $topic');
}

// Unsubscribed callback
void onUnsubscribed(String? topic) {
  print('Unsubscribed topic: $topic');
}

// Ping callback
void pong() {
  print('Ping response client callback invoked');
}
```

## 测试

我们为该项目编写了一个简单的 UI 界面，并配合 [MQTT 5.0 客户端工具 - MQTTX](https://mqttx.app/zh) 进行以下测试：

- 连接
- 订阅
- 发布
- 取消订阅
- 断开连接

界面如下：

![应用界面](https://assets.emqx.com/images/a450f294fee8b678abbaee592be403c7.png)

使用 MQTTX 作为另一个客户端来发送和接收消息：

![MQTTX](https://assets.emqx.com/images/8ecc0746d065af953aef92fcc3ecf07a.png)

<center>MQTTX</center>

我们可以看到整个过程的日志

![Log](https://assets.emqx.com/images/4cd5f281fb9f629fcd9351c633009a1a.png)

<center>Log</center>

## Q&A

### 当一条消息发布成功时，我如何收到通知?

您可以在发布消息时设置一个订阅。

```dart
client.published!.listen((MqttPublishMessage message) {
  final payload = MqttPublishPayload.bytesToStringAsString(message.payload.message);
  print('Published message: payload $payload is published to ${message.variableHeader!.topicName} with Qos ${message.header!.qos}');
});
```

### 如何设置自动重连？

您可以设置自动重连并且设置自动重连的回调。

```dart
client.autoReconnect = true;
client.onAutoReconnect = onAutoReconnect;
client.onAutoReconnected = onAutoReconnected;

/// The pre auto re connect callback
void onAutoReconnect() {
  print('Client auto reconnection sequence will start');
}

/// The post auto re connect callback
void onAutoReconnected() {
  print('Client auto reconnection sequence has completed');
}
```

- `onAutoReconnect`: 自动重新连接回调，该回调将在调用自动重新连接处理之前被调用，以便用户执行任何预自动重新连接操作。
- `onAutoReconnected`: 自动重新连接成功回调，自动重新连接处理完成后将调用此回调，以便用户执行任何自动重新连接后的操作。

## 结语

至此，我们完成了在 Android 平台上利用 Flutter 构建 MQTT 应用，实现了客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

Flutter 通过统一的开发语言和跨平台特性让开发强大的移动应用变得十分容易，它将来可能会是开发移动应用的最佳解决方案。结合 Flutter、MQTT 协议及 [MQTT 云服务](https://www.emqx.com/zh/cloud)，我们可以开发更多有趣的应用。

您也可以查看 EMQ 提供的《[MQTT 协议入门指南](https://www.emqx.com/zh/mqtt-guide)》系列文章，了解 MQTT 协议特性，探索 MQTT 的更多高级应用，开启 MQTT 应用和服务开发之旅。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
