[Flutter](https://flutter.dev/)は、GoogleのUIツールキットで、1つのコードベースからモバイル、Web、デスクトップの美しいネイティブコンパイルアプリケーションを構築できます。Flutterは豊富なコンポーネントとインターフェースを提供し、開発者はFlutterのネイティブ拡張をすぐに追加できます。同時に、Flutterはネイティブエンジンも使用してビューをレンダリングします。ユーザー体験を良好に提供できることは間違いありません。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく**軽量IoT通信プロトコル**です。厳しく制限されたデバイスハードウェアと高レイテンシー/低帯域幅ネットワークでも安定した転送が可能です。シンプルで実装が容易で、QoSをサポートし、パケットサイズが小さいため、IoTプロトコル市場の半分を占めています。

この記事では、主にFlutterプロジェクトでMQTTを使用して、クライアントと[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)の接続、サブスクライブ、アンサブスクライブ、メッセージの送受信などの機能の実装方法を紹介します。

## プロジェクトの初期化

### プロジェクトの作成

新しいプロジェクトを作成することができます。以下のリンクを参照してください。

- [エディタのセットアップ](https://docs.flutter.dev/get-started/editor?tab=androidstudio)
- [Android StudioとIntelliJ](https://docs.flutter.dev/development/tools/android-studio)

### 依存関係のインストール

`pubspec.yaml`ファイルに依存関係を追加します。

```yaml
dependencies: 
  mqtt_client: ^7.2.1
```

依存関係をインストール:

```shell
flutter pub get
```

インポート

```dart
import 'package:mqtt_client/mqtt_client.dart';
```

## MQTTの使用

### MQTTブローカーへの接続

この記事では、[EMQX Cloud](https://www.emqx.com/ja/cloud)によって運用・管理されている[MQTTブローカー](https://www.emqx.io/ja/mqtt/public-mqtt5-broker)を使用します。 EMQX Cloudは、EMQによってリリースされた[MQTT IoTクラウド](https://www.emqx.com/ja/cloud)サービスプラットフォームで、オールインワンの運用・保守とユニークな分離環境での**MQTT 5.0**へのアクセスサービスを提供します。

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- Websocketポート: **8083**

#### 接続の例

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

#### コールバックメソッドの説明

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

`MqttConnectMessage`: タイムアウトの設定、認証、ラストウィルメッセージなど、接続オプションを設定します。

`client.updates.listen`: サブスクライブしたトピックのメッセージの到着を監視するために使用されます。

#### 証明書接続の例

```dart
/// Security context
SecurityContext context = new SecurityContext()
  ..useCertificateChain('path/to/my_cert.pem')
  ..usePrivateKey('path/to/my_key.pem', password: 'key_password')
  ..setClientAuthorities('path/to/client.crt', password: 'password');
client.secure = true;
client.securityContext = context;
```

### その他のMQTT操作

#### トピックのサブスクライブ

```dart
client.subscribe("topic/test", MqttQos.atLeastOnce)
```

#### メッセージのパブリッシュ

```dart
const pubTopic = 'topic/test';
final builder = MqttClientPayloadBuilder();
builder.addString('Hello MQTT');
client.publishMessage(pubTopic, MqttQos.atLeastOnce, builder.payload);
```

#### アンサブスクライブ

```dart
client.unsubscribe('topic/test');
```

#### 切断

```dart
client.disconnect();
```

## テスト

このプロジェクトのために、シンプルなUIインターフェースを記述し、[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を使用して、以下のテストを行います。

- 接続
- サブスクライブ
- パブリッシュ
- アンサブスクライブ
- 切断

アプリケーションのインターフェース:

![画板1x.png](https://assets.emqx.com/images/4aeb38a0dc6b0329164a91fc38e572cc.png)

MQTTXを別のクライアントとして使用して、メッセージの送受信を行う:

![mqttx_flutter](https://assets.emqx.com/images/b46731e7278ad148a0bfe3cc0890138b.png)

プロセス全体のログが表示されているのがわかります。

![log](https://assets.emqx.com/images/97230919d8c8eddd3c88003e67c9ad1b.png)

## まとめ

これまで、Flutterを使用してAndroidプラットフォームでMQTTアプリケーションを構築し、クライアントとMQTTブローカーの接続、サブスクライブ、アンサブスクライブ、パブリッシュ、メッセージの受信などを実装してきました。

Flutterは、統一されたプログラミング言語とクロスプラットフォームの機能により、強力なモバイルアプリケーションを簡単に開発できるようにします。これは、モバイルアプリケーションを開発するための最適なソリューションになる可能性があります。 Flutter、MQTTプロトコル、[MQTTクラウドサービス](https://www.emqx.com/ja/cloud)を使用することで、より面白いアプリケーションを開発できます。

次に、EMQXが提供する[MQTTプロトコルのわかりやすいガイド](https://www.emqx.com/ja/mqtt-guide)の記事シリーズをチェックして、MQTTプロトコルの機能を学習し、MQTTのさらに高度なアプリケーションを探求し、MQTTアプリケーションとサービスの開発を開始してください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
