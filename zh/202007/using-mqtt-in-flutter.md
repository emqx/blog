
[Flutter](https://flutter.dev/) 是 Google 推出并开源的移动应用开发框架，主打跨平台、高保真、高性能。开发者可以通过 Dart 语言开发 App，一套代码同时运行在 iOS 和 Android 平台。 Flutter 提供了丰富的组件、接口，开发者可以快速地为 Flutter 添加 native 扩展。同时 Flutter 还使用  Native 引擎渲染视图，这无疑能为用户提供良好的体验。

[MQTT](https://www.emqx.cn/mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可在严重受限的硬件设备和低带宽、高延迟的网络上实现稳定传输。它凭借简单易实现、支持 QoS、报文小等特点，占据了物联网协议的半壁江山。

本文主要介绍如何在 Flutter 项目中使用 MQTT，实现客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

## 项目初始化

### 新建项目

新建一个项目，可以参考以下链接：

- [Set up an editor](https://flutter.dev/docs/get-started/editor?tab=androidstudio)
- [Android Studio and IntelliJ](https://flutter.dev/docs/development/tools/android-studio)

### 安装依赖

添加依赖到 `pubspec.yaml` 文件中

```yaml
dependencies: 
  mqtt_client: ^7.2.1
```

安装依赖：

```bash
flutter pub get
```

导入

```dart
import 'package:mqtt_client/mqtt_client.dart';
```



## MQTT 的使用

### 连接 MQTT 服务器

本文将使用 EMQ X 提供的 [免费公共 MQTT 服务器](https://www.emqx.cn/mqtt/public-mqtt5-broker)，该服务基于 EMQ X 的 [MQTT 物联网云平台](https://cloud.emqx.io) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

#### 连接示例代码

```dart
Future<MqttServerClient> connect() async {
  MqttServerClient client =
      MqttServerClient.withPort('broker.emqx.io', 'flutter_client', 1883);
  client.logging(on: true);
  client.onConnected = onConnected;
  client.onDisconnected = onDisconnected;
  client.onUnsubscribed = onUnsubscribed;
  client.onSubscribed = onSubscribed;
  client.onSubscribeFail = onSubscribeFail;
  client.pongCallback = pong;

  final connMessage = MqttConnectMessage()
      .authenticateAs('username', 'password')
      .keepAliveFor(60)
      .withWillTopic('willtopic')
      .withWillMessage('Will message')
      .startClean()
      .withWillQos(MqttQos.atLeastOnce);
  client.connectionMessage = connMessage;
  try {
    await client.connect();
  } catch (e) {
    print('Exception: $e');
    client.disconnect();
  }

  client.updates.listen((List<MqttReceivedMessage<MqttMessage>> c) {
    final MqttPublishMessage message = c[0].payload;
    final payload =
    MqttPublishPayload.bytesToStringAsString(message.payload.message);

    print('Received message:$payload from topic: ${c[0].topic}>');
  });

  return client;
}
```

#### 回调方法说明

```dart
// 连接成功
void onConnected() {
  print('Connected');
}

// 连接断开
void onDisconnected() {
  print('Disconnected');
}

// 订阅主题成功
void onSubscribed(String topic) {
  print('Subscribed topic: $topic');
}

// 订阅主题失败
void onSubscribeFail(String topic) {
  print('Failed to subscribe $topic');
}

// 成功取消订阅
void onUnsubscribed(String topic) {
  print('Unsubscribed topic: $topic');
}

// 收到 PING 响应
void pong() {
  print('Ping response client callback invoked');
}
```

`MqttConnectMessage`：设置连接选项，包含超时设置，认证以及遗愿消息等。

`client.updates.listen`：用于监听已订阅主题的消息到达。

#### 证书连接示例

```dart
/// Security context
SecurityContext context = new SecurityContext()
  ..useCertificateChain('path/to/my_cert.pem')
  ..usePrivateKey('path/to/my_key.pem', password: 'key_password')
  ..setClientAuthorities('path/to/client.crt', password: 'password');
client.secure = true;
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



## 测试

我们给该项目编写了一个简单的 UI 界面，并配合 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/cn/) 进行以下测试：

- 连接

- 订阅

- 发布

- 取消订阅

- 断开连接

应用界面：

![device.png](https://static.emqx.net/images/9c6e9d500faa607512eaa5d767630474.png)

使用 MQTTX 作为另一个客户端进行消息收发：

![mqttx_flutter.png](https://static.emqx.net/images/ac306b8d6139cdcd2a7446de58c87847.png)


我们可以看到整个过程的日志。

![log.png](https://static.emqx.net/images/d5e2065b8265787de99d1daefd7ba444.png)

## 总结

至此，我们完成了在 Android 平台上利用 Flutter 构建 MQTT 应用，实现了客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

Flutter 通过统一的开发语言和跨平台特性让开发强大的移动应用变得十分容易，它将来可能会是开发移动应用的最佳解决方案。结合 Flutter、MQTT 协议及 [MQTT 云服务](https://cloud.emqx.io/cn/)，我们可以开发更多有趣的应用。

