[Dart](https://dart.dev/) 是一种为客户端开发而设计的编程语言，比如用于 Web 和移动应用，它由 Google 主导开发，于 2011 年 10 月公开。它的开发团队由 Google Chrome 浏览器 V8 引擎团队的领导者拉尔斯·巴克主持，目标在于成为下一代结构化 Web 开发语言。类似 JavaScript，Dart 也是一种面向对象语言，但是它采用基于类的编程。它只允许单一继承继承，语法风格接近 C 语言。Dart 可在任何平台上开发快速的应用程序。其目标是为多平台开发提供最高效的编程语言，并为应用程序框架搭配了[灵活的运行时执行平台](https://dart.cn/overview#platform)。

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

本文主要介绍如何在 Dart 项目中使用 [mqtt_client](https://pub.dev/packages/mqtt_client) 库 ，实现客户端与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、收发消息等功能。

## 准备工作

本文实例基于 macOS 环境。

### 获取 SDK

参考 [获取 SDK](https://dart.cn/get-dart)

```bash
$ brew tap dart-lang/dart
$ brew install dart
$ dart --version
Dart SDK version: 2.13.0 (stable) (Wed May 12 12:45:49 2021 +0200) on "macos_x64"
```

### 初始化项目

```bash
$ dart create -t console-full mqtt_demo
$ cd mqtt_demo
```

目录结构如下

```
├── CHANGELOG.md
├── README.md
├── analysis_options.yaml
├── bin
│   └── mqtt_demo.dart
├── pubspec.lock
└── pubspec.yaml
```

### 安装依赖

本文使用 [mqtt_client](https://pub.dev/packages/mqtt_client)  作为 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)，运行如下命令安装：

```bash
$ dart pub add mqtt_client
```

这将在项目的 `pubspec.yaml` 文件中添加这样一行：

```yaml
dependencies:
  mqtt_client: ^9.6.2
```



## MQTT 的使用

本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 物联网云平台 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

### 连接 MQTT 服务器

编辑 `bin/mqtt_demo.dart` 文件

```dart
import 'dart:async';
import 'dart:io';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

final client = MqttServerClient('broker-cn.emqx.io', '1883');

Future<int> main() async {
  client.logging(on: true);
  client.keepAlivePeriod = 60;
  client.onDisconnected = onDisconnected;
  client.onConnected = onConnected;
  client.pongCallback = pong;

  final connMess = MqttConnectMessage()
      .withClientIdentifier('dart_client')
      .withWillTopic('willtopic') 
      .withWillMessage('My Will message')
      .startClean() 
      .withWillQos(MqttQos.atLeastOnce);
  print('client connecting....');
  client.connectionMessage = connMess;

  try {
    await client.connect();
  } on NoConnectionException catch (e) {
    print('client exception - $e');
    client.disconnect();
  } on SocketException catch (e) {
    print('socket exception - $e');
    client.disconnect();
  }

  if (client.connectionStatus!.state == MqttConnectionState.connected) {
    print('client connected');
  } else {
    print('client connection failed - disconnecting, status is ${client.connectionStatus}');
    client.disconnect();
    exit(-1);
  }
  return 0;
}


/// The unsolicited disconnect callback
void onDisconnected() {
  print('OnDisconnected client callback - Client disconnection');
  if (client.connectionStatus!.disconnectionOrigin ==
      MqttDisconnectionOrigin.solicited) {
    print('OnDisconnected callback is solicited, this is correct');
  }
  exit(-1);
}

/// The successful connect callback
void onConnected() {
  print('OnConnected client callback - Client connection was sucessful');
}

/// Pong callback
void pong() {
  print('Ping response client callback invoked');
}

```

然后执行

```bash
$ dart run bin/mqtt_demo.dart
```

通过控制台输出，我们看到客户端已经成功的连上了 MQTT 服务器

![连接 MQTT 服务器](https://assets.emqx.com/images/823456b44224b32df25eb2cc77d30cc3.png)

**说明**

`MqttConnectMessage`：设置连接选项，包含超时设置，认证以及遗愿消息等。

 **证书连接示例**

```dart
/// Security context
SecurityContext context = new SecurityContext()
  ..useCertificateChain('path/to/my_cert.pem')
  ..usePrivateKey('path/to/my_key.pem', password: 'key_password')
  ..setClientAuthorities('path/to/client.crt', password: 'password');
client.secure = true;
client.securityContext = context;
```

### 订阅

添加以下代码

```dart
client.onSubscribed = onSubscribed;

const topic = 'topic/test';
print('Subscribing to the $topic topic');
client.subscribe(topic, MqttQos.atMostOnce);
client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
  final recMess = c![0].payload as MqttPublishMessage;
  final pt = MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
  print('Received message: topic is ${c[0].topic}, payload is $pt');
});

/// The subscribed callback
void onSubscribed(String topic) {
  print('Subscription confirmed for topic $topic');
}
```

然后执行

```bash
$ dart run bin/mqtt_demo.dart
```

我们看到已成功订阅 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)

![成功订阅 MQTT 主题](https://assets.emqx.com/images/bb9a85e75c2b88e8c14cce06f9eb90f1.png)

### 发布消息

```dart
client.published!.listen((MqttPublishMessage message) {
  print('Published topic: topic is ${message.variableHeader!.topicName}, with Qos ${message.header!.qos}');
});

const pubTopic = 'test/topic';
final builder = MqttClientPayloadBuilder();
builder.addString('Hello from mqtt_client');

print('Subscribing to the $pubTopic topic');
client.subscribe(pubTopic, MqttQos.exactlyOnce);

print('Publishing our topic');
client.publishMessage(pubTopic, MqttQos.exactlyOnce, builder.payload!);
```

我们看到已经成功发布消息并收到该消息

![发布 MQTT 消息](https://assets.emqx.com/images/0d01872c4136f6e62539620c5f115e8a.png)

### 完整测试

我们使用以下代码进行完整测试

```dart
import 'dart:async';
import 'dart:io';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

final client = MqttServerClient('broker-cn.emqx.io', '1883');

Future<int> main() async {
  client.logging(on: false);
  client.keepAlivePeriod = 60;
  client.onDisconnected = onDisconnected;
  client.onConnected = onConnected;
  client.onSubscribed = onSubscribed;
  client.pongCallback = pong;

  final connMess = MqttConnectMessage()
      .withClientIdentifier('dart_client')
      .withWillTopic('willtopic') 
      .withWillMessage('My Will message')
      .startClean() 
      .withWillQos(MqttQos.atLeastOnce);
  print('Client connecting....');
  client.connectionMessage = connMess;

  try {
    await client.connect();
  } on NoConnectionException catch (e) {
    print('Client exception: $e');
    client.disconnect();
  } on SocketException catch (e) {
    print('Socket exception: $e');
    client.disconnect();
  }

  if (client.connectionStatus!.state == MqttConnectionState.connected) {
    print('Client connected');
  } else {
    print('Client connection failed - disconnecting, status is ${client.connectionStatus}');
    client.disconnect();
    exit(-1);
  }

  const subTopic = 'topic/sub_test';
  print('Subscribing to the $subTopic topic');
  client.subscribe(subTopic, MqttQos.atMostOnce);
  client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
    final recMess = c![0].payload as MqttPublishMessage;
    final pt = MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
    print('Received message: topic is ${c[0].topic}, payload is $pt');
  });

  client.published!.listen((MqttPublishMessage message) {
    print('Published topic: topic is ${message.variableHeader!.topicName}, with Qos ${message.header!.qos}');
  });

  const pubTopic = 'topic/pub_test';
  final builder = MqttClientPayloadBuilder();
  builder.addString('Hello from mqtt_client');

  print('Subscribing to the $pubTopic topic');
  client.subscribe(pubTopic, MqttQos.exactlyOnce);

  print('Publishing our topic');
  client.publishMessage(pubTopic, MqttQos.exactlyOnce, builder.payload!);
  
  print('Sleeping....');
  await MqttUtilities.asyncSleep(80);

  print('Unsubscribing');
  client.unsubscribe(subTopic);
  client.unsubscribe(pubTopic);

  await MqttUtilities.asyncSleep(2);
  print('Disconnecting');
  client.disconnect();
  
  return 0;
}

/// The subscribed callback
void onSubscribed(String topic) {
  print('Subscription confirmed for topic $topic');
}

/// The unsolicited disconnect callback
void onDisconnected() {
  print('OnDisconnected client callback - Client disconnection');
  if (client.connectionStatus!.disconnectionOrigin ==
      MqttDisconnectionOrigin.solicited) {
    print('OnDisconnected callback is solicited, this is correct');
  }
  exit(-1);
}

/// The successful connect callback
void onConnected() {
  print('OnConnected client callback - Client connection was sucessful');
}

/// Pong callback
void pong() {
  print('Ping response client callback invoked');
}

```

控制台完整完整输出

![Dart MQTT 测试](https://assets.emqx.com/images/038cd813b42f010286df5f802b511ea4.png)

## 总结

至此，我们完成了在 Dart 中使用 [mqtt_client](https://pub.dev/packages/mqtt_client)  库连接到 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。

接下来我们将会陆续发布更多关于物联网开发及 [MQTT](https://www.emqx.com/zh/mqtt-guide) 的相关文章，敬请关注。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
