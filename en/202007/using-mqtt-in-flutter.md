[Flutter](https://flutter.dev/) is Google’s UI toolkit for building beautiful, natively compiled applications for mobile, web, and desktop from a single codebase. Flutter provides a rich set of components and interfaces, the developer can quickly add native expansion for Flutter. At the same time, Flutter also uses a Native engine to render view. There is no doubt that it can provide a good experience for users.

[MQTT](https://www.emqx.com/en/mqtt) is a **lightweight IoT communication protocol** based on the publish/subscribe model. It can enable stable transmission over severely restricted device hardware and high-latency / low-bandwidth network. Because it is simple and easy to implement, support for QoS, and small size of the packet, it occupies half market of the Internet of Things protocol.

This article mainly introduces how to use MQTT in the Flutter project to implement the connection between client and MQTT broker, subscribe, unsubscribe, send and receive messages and other functions.



## Project initialization

### Create a project

Create a new project, can refer to the following links:

- [Set up an editor](https://flutter.dev/docs/get-started/editor?tab=androidstudio)
- [Android Studio and IntelliJ](https://flutter.dev/docs/development/tools/android-studio)

### Install dependencies

Add dependencies into file `pubspec.yaml` 

```yaml
dependencies: 
  mqtt_client: ^7.2.1
```

Install dependencies:

```bash
flutter pub get
```

Import

```dart
import 'package:mqtt_client/mqtt_client.dart';
```



## Use of MQTT

### Connect to MQTT broker

This article will use the [MQTT broker](https://www.emqx.com/en/products/emqx) which is operated and maintained by EMQ X Cloud. EMQ X Cloud is the [MQTT IoT cloud](https://www.emqx.com/en/cloud) service platform released by [EMQ](https://www.emqx.com/en), it provides the service for accessing **MQTT 5.0** with all-in-one operation and maintenance and unique isolation environment.

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

#### The example of connection

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

#### The description of callback method 

```dart
// connection succeeded
void onConnected() {
  print('Connected');
}

// unconnected
void onDisconnected() {
  print('Disconnected');
}

// subscribe to topic succeeded
void onSubscribed(String topic) {
  print('Subscribed topic: $topic');
}

// subscribe to topic failed
void onSubscribeFail(String topic) {
  print('Failed to subscribe $topic');
}

// unsubscribe succeeded
void onUnsubscribed(String topic) {
  print('Unsubscribed topic: $topic');
}

// PING response received
void pong() {
  print('Ping response client callback invoked');
}
```

`MqttConnectMessage`: set connection options, including timeout settings, authentication, last wish messages, etc.

`client.updates.listen`: used for monitoring the arrival of messages of the subscribed topics 

#### The example of certificate connection

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



## Test

We write a simple UI interface for this project and use [MQTT 5.0 client tool - MQTT X](https://mqttx.app/) to do the following tests:

- connect

- subscribe

- publish

- unsubscribe

- disconnect

The interface of the application:

![画板1x.png](https://static.emqx.net/images/4aeb38a0dc6b0329164a91fc38e572cc.png)

Use MQTT X as another client to send and receive messages:

![mqttx_flutter.png](https://static.emqx.net/images/b46731e7278ad148a0bfe3cc0890138b.png)


We can see the log of the whole process

![log.png](https://static.emqx.net/images/97230919d8c8eddd3c88003e67c9ad1b.png)

## Summary

So far, we have finished that use Flutter to build MQTT applications in the Android platform, implemented the connection between the client and MQTT broker, subscribe, unsubscribe, publish and receive messages, etc.

Flutter makes it easy that develop powerful mobile applications through unified programming language and the feature cross-platform. It may be the most proper solution for developing mobile applications in the future. Using Flutter, MQTT protocol and [MQTT cloud service](https://www.emqx.com/en/cloud), we can develop more interesting applications.

