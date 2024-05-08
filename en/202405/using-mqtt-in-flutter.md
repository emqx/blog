## Introduction

[Flutter](https://flutter.dev/) is Google’s UI toolkit for building beautiful, natively compiled applications for mobile, web, and desktop from a single codebase. Flutter provides a rich set of components and interfaces, the developer can quickly add native expansion for Flutter. At the same time, Flutter also uses a Native engine to render view. There is no doubt that it can provide a good experience for users.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a **lightweight IoT communication protocol** based on the publish/subscribe model. It can enable stable transmission over severely restricted device hardware and high-latency / low-bandwidth network. Because it is simple and easy to implement, supports QoS, and small size packet, it occupies half market of the Internet of Things protocol.

This article mainly introduces how to use MQTT in the Flutter project to implement the connection between the client and [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), subscribe, unsubscribe, send and receive messages, and other functions.

> *Learn more:* [*How to use MQTT on Android*](https://www.emqx.com/en/blog/android-connects-mqtt-using-kotlin)*.*

## Project Preparation

### Create a project

Create a new project, you can refer to the following links:

- [Set up an editor](https://docs.flutter.dev/get-started/editor?tab=androidstudio)
- [Android Studio and IntelliJ](https://docs.flutter.dev/development/tools/android-studio)

### Install dependencies

We will use [mqtt_client](https://pub.dev/packages/mqtt_client) as our dependency.

Run this command:

```shell
 $ flutter pub add mqtt_client
```

This will add a line like this to your package's `pubspec.yaml` (and run an implicit `dart pub get`):

```yaml
dependencies:
  mqtt_client: ^9.6.8
```

### Import it

Now in your Dart code, you can use:

```dart
import 'package:mqtt_client/mqtt_client.dart';
```

## Use of MQTT

### Connect to MQTT broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

In this guide, we will utilize the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, built on [EMQX ](https://www.emqx.com/en/products/emqx)Platform. The server access details are as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**
- WebSocket Port: 8083
- SSL/TLS Port: 8883
- Secure WebSocket Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

#### TCP Connection

To establish the MQTT connection, it is necessary to set the connection address, port, and client ID. 

We can also set parameters such as username, password, and keep live.

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

#### Websocket

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

Next, we connect to the MQTT Broker.

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
client.secure = true;
client.securityContext = context;
```

### Other MQTT operations

#### Subscribe to topic

```dart
client.subscribe("topic/test", MqttQos.atLeastOnce)
```

#### Publish message

```dart
const pubTopic = 'topic/test';
final builder = MqttClientPayloadBuilder();
builder.addString('Hello MQTT');
client.publishMessage(pubTopic, MqttQos.atLeastOnce, builder.payload);
```

#### Unsubscribe

```dart
client.unsubscribe('topic/test');
```

#### Disconnect

```dart
client.disconnect();
```

### Callback

We can set callback like this

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

- `onConnected`: Client connect callback, called on successful connect.
- `onDisconnected:` Client disconnect callback, called on unsolicited disconnect.
- `onUnsubscribed`: Unsubscribed callback.
- `onSubscribed: `Subscribed callback.
- `onSubscribeFail:` Subscribed failed callback.
- `pongCallback:` Ping response received callback.

We can add s subscription when we received message

```dart
client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
  final recMessage = c![0].payload as MqttPublishMessage;
  final payload = MqttPublishPayload.bytesToStringAsString(recMessage.payload.message);
  print('Received message:$payload from topic: ${c[0].topic}');
});
```

### Complete code

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

## Test

We write a simple UI interface for this project and use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) to do the following tests:

- connect
- subscribe
- publish
- unsubscribe
- disconnect

The interface of the application:

![Flutter MQTT Demo](https://assets.emqx.com/images/e4746996dc57e30222677c5e1146e1bc.png)

Use MQTTX as another client to send and receive messages:

![MQTTX](https://assets.emqx.com/images/ff0c9a63795c23eef7cf114849abebd1.png) We can see the log of the whole process:

![Log](https://assets.emqx.com/images/4aaeb27ac710d2349b1d05b18e47d674.png)

## Q&A

### How do I get notified when a message is published successfully?

You can set a subscription when message published

```dart
client.published!.listen((MqttPublishMessage message) {
  final payload = MqttPublishPayload.bytesToStringAsString(message.payload.message);
  print('Published message: payload $payload is published to ${message.variableHeader!.topicName} with Qos ${message.header!.qos}');
});
```

### How to set up automatic reconnection？

You can set auto reconnect when disconnect and you can set callback

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

- `onAutoReconnect`:  Auto reconnect callback, this callback will be called before auto reconnect processing is invoked to allow the user to perform any pre auto reconnect actions.
- `onAutoReconnected`: Auto reconnected callback, this callback will be called after auto reconnect processing is completed to allow the user to perform any post auto reconnect actions.

## Summary

So far, we have finished that use Flutter to build MQTT applications in the Android platform, implemented the connection between the client and MQTT broker, subscribe, unsubscribe, publish and receive messages, etc.

Flutter makes it easy that develop powerful mobile applications through unified programming language and the feature cross-platform. It may be the most proper solution for developing mobile applications in the future. Using Flutter, MQTT protocol and [MQTT cloud service](https://www.emqx.com/en/cloud), we can develop more interesting applications.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
