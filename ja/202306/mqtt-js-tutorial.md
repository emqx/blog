## はじめに

[MQTT.js](https://github.com/mqttjs/MQTT.js)は、MQTTプロトコルのクライアントライブラリで、Node.jsとブラウザ用のJavaScriptで書かれています。現在、JavaScriptエコシステムで最も広く使われている[MQTTクライアント・ライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)です。

> *MQTTは、パブリッシュ／サブスクライブモデルに基づく軽量のIoTメッセージングプロトコルです。非常に少ないコードと帯域幅で、ネットワークデバイスにリアルタイムかつ信頼性の高いメッセージングサービスを提供することができます。IoT、モバイルインターネット、スマートハードウェア、Internet of Vehicles、電力エネルギーなどの産業で広く利用されている。*

JavaScriptのシングルスレッド機能により、MQTT.jsは完全に非同期なMQTTクライアントです。MQTT/TCP、MQTT/TLS、MQTT/WebSocketをサポートしています。異なる動作環境での対応度は以下の通りです：

-  ブラウザ：[MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- Node.js：MQTTとMQTT over WebSocket

> *注）他のAPIは、接続パラメータが若干異なる以外は、異なる環境でも同じです。MQTT.js v3.0.0以降のバージョンでは、MQTT 5.0を完全サポートしています。*

## インストール

### NPMまたはYarnを使用してMQTT.jsをインストールする。

NPMまたはYarnを使用してMQTT.jsをインストールするには、以下のコマンドを実行します：

```
npm install mqtt --save

# Alternatively, use yarn
yarn add mqtt
```

> *注）v4.0.0（2020/04リリース）より、MQTT.jsはnodeの終息バージョンをサポートしなくなり、node v12とv14をサポートするようになりました。*

### CDNを利用したMQTT.jsのインストール

ブラウザでは、CDNを利用してMQTT.jsをインポートすることもできます。MQTT.jsのバンドルパッケージは[http://unpkg.com](http://unpkg.com)、直接[unkg.com/mqtt/dist/mqtt.min.js](https://unpkg.com/mqtt/dist/mqtt.min.js)を追加して使用することができます。

```
<script src="<https://unpkg.com/mqtt/dist/mqtt.min.js>"></script>
<script>
  // An mqtt variable will be initialized globally
  console.log(mqtt)
</script>
```

### グローバルインストール

上記のインストール方法に加えて、MQTT.jsは、コマンドラインツールを使用してMQTT接続、公開、購読を完了するグローバルインストール方法を提供しています。MQTT.jsのコマンドラインツールの使用方法については、以下のいくつかのチュートリアルで詳しく説明します。

NPMを使用してMQTT.jsをグローバルにインストールするには、以下のコマンドを実行します：

```
npm install mqtt -g
```

##  MQTTブローカーを準備する

先に進む前に、通信とテストを行うためのMQTTブローカーがあることを確認してください。MQTTブローカーを入手するには、いくつかのオプションがあります：

-  **プライベート展開**

  [EMQX](https://www.emqx.io/)は、IoT、IIoT、コネクテッドビークルのための最もスケーラブルなオープンソースのMQTTブローカーです。EMQXをインストールするには、以下のDockerコマンドを実行します：

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

-  **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。[EMQX Cloud](https://www.emqx.com/ja/cloud)を利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版の[EMQX Cloud Serverless](https://www.emqx.com/ja/cloud/serverless-mqtt)では、開発者が数秒で簡単にMQTTの導入を開始できるように、1Mセッション分/月を無償で提供します。

-  **無料公開のMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 `broker.emqx.io` の無料公開MQTTブローカーを使用することにします。

>  *MQTTブローカー情報*
>
>  *サーバー：* `broker.emqx.io`
>
>  *TCPポート：* `1883`
>
>  *WebSocketポート：* `8083`
>
>  *SSL/TLSポート：* `8883`
>
> *セキュアWebSocketポート：* `8084`

詳しくは、こちらをご確認ください：[無料公開のMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)。

## MQTT.jsの簡単な例

MQTT.jsを使用して、EMQX Cloudへの接続、トピックの購読、メッセージの送受信を行う例を紹介します。

> *注意：WebSocket接続は、ブラウザでのみサポートされています。そのため、ブラウザとNode.jsの環境で異なる接続パラメータを使用することになります。しかし、接続URL以外のパラメータはすべて同じです。読者は、自分のニーズに最も適したパラメータを使用することができます。*

```
const mqtt = require('mqtt')

/***
    * Browser
    * This document explains how to use MQTT over WebSocket with the ws and wss protocols.
    * EMQX's default port for ws connection is 8083 and for wss connection is 8084.
    * Note that you need to add a path after the connection address, such as /mqtt.
    */
const url = 'ws://broker.emqx.io:8083/mqtt'
/***
    * Node.js
    * This document explains how to use MQTT over TCP with both mqtt and mqtts protocols.
    * EMQX's default port for mqtt connections is 1883, while for mqtts it is 8883.
    */
// const url = 'mqtt://broker.emqx.io:1883'

// Create an MQTT client instance
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Authentication
  clientId: 'emqx_test',
  username: 'emqx_test',
  password: 'emqx_test',
}
const client  = mqtt.connect(url, options)
client.on('connect', function () {
  console.log('Connected')
  // Subscribe to a topic
  client.subscribe('test', function (err) {
    if (!err) {
      // Publish a message to a topic
      client.publish('test', 'Hello mqtt')
    }
  })
})

// Receive messages
client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})
```

## MQTT.jsのコマンドライン

MQTT.jsをグローバルにインストールした後、コマンドラインツールを使ってトピックの購読やメッセージの送受信を行うことができます。

例： `broker.emqx.io` に接続し、 `testtopic/#` のトピックを購読する：

```
mqtt sub -t 'testtopic/#' -h 'broker.emqx.io' -v
```

例： `broker.emqx.io` に接続し、 `testtopic/hello` のトピックにメッセージを送信する。

```
mqtt pub -t 'testtopic/hello' -h 'broker.emqx.io' -m 'from MQTT.js'
```

より包括的なMQTTコマンドラインツールが必要な場合は、[MQTTX CLI](https://mqttx.app/cli)を参照することができます。

## MQTT.jsのAPI紹介

### mqtt.connect([url], options)

本APIは、指定されたMQTT Broker関数に接続し、常に `Client` オブジェクトを返します。第1パラメータは、以下のプロトコルを使用できるURLの値を渡します： `mqtt` , `mqtts` , `tcp` , `tls` , `ws` , `wss` .あるいは、URLは `URL.parse()` によって返されるオブジェクトとすることもできる。

次に、本APIはMQTT接続のオプションを設定するために `Options` オブジェクトを渡します。WebSocket接続を使用する場合は、 `/mqtt` のようにアドレスの後にパスを追加するかどうかを検討する必要があります。

Optionsオブジェクトでよく使われる属性値を紹介します：

-  オプション

  - `keepalive` ：単位は `seconds` 、タイプは整数、デフォルトは60秒、0に設定すると無効になります。

  - `clientId` : デフォルトは `'mqttjs_' + Math.random().toString(16).substr(2, 8)` で、カスタム修正文字列をサポートすることができる

  - `protocolVersion` ：MQTTプロトコルのバージョン番号。デフォルトは4（v3.1.1）で、3（v3.1）および5（v5.0）に変更することができます。

  - `clean` を指定します：セッションをクリアするかどうかで、デフォルトは `true` です。 `true` に設定すると，切断後にセッションがクリアされ，購読していたトピックも無効となる。 `false` に設定すると、QoSが1、2のメッセージもオフラインで受信できるようになります。

  - `reconnectPeriod` を指定します：再接続間隔時間、単位はミリ秒、デフォルトは1000ミリ秒です。注：0に設定すると、自動再接続は無効になる

  - `connectTimeout` ：CONNACK受信までの待ち時間で、単位はミリ秒、デフォルトは30000ミリ秒です。

  - `username` ：認証用ユーザー名。ブローカーがユーザー名認証を必要とする場合、この値を設定してください。

  - `password` : 認証パスワード。ブローカーがパスワード認証を必要とする場合、この値を設定してください。

  - `will`

    :Willメッセージ、設定可能なオブジェクト値です。クライアントが異常切断した場合、ブローカーは以下のフォーマットでwillトピックにメッセージを発行します：

    - `topic` ：遺言で送られたトピック
    - `payload` ：遺言で公開されたメッセージ
    - `QoS` となります：意志によって送信されるQoS値
    - `retain` ：意志によって公開されたメッセージの保持記号

  - `properties` : MQTT 5.0 で新たに追加された設定可能なオブジェクトのプロパティ値です。詳細については、[GitHub - mqttjs/MQTT.js](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options)  を参照してください。

- SSL/TLS接続の設定が必要な場合は、 `tls.connect()` にOptionオブジェクトが渡され、optionに以下のプロパティを設定することができます。

  - `rejectUnauthorized` を指定します：サーバー証明書のチェーンとアドレス名を検証するかどうか。falseに設定すると、検証が省略され、中間者攻撃にさらされることになります。そのため、本番環境ではこの設定は推奨しません。trueに設定すると、強力な認証モードが有効になります。自己署名証明書の場合は、証明書設定時に Alt 名を設定してください。
  - `ca` ：自己署名証明書で生成されたCAファイルです。サーバーが自己署名証明書を使用する場合のみ必要です
  - `cert` ：クライアント証明書です。サーバーがクライアント証明書による認証（双方向認証）を必要とする場合のみ必要です、
  - `key` ：クライアント鍵です。サーバーがクライアント証明書による認証を必要とする場合のみ必要です（双方向認証）。

### クライアントイベント

接続が成功すると、返されたクライアントオブジェクトはon関数を使用して複数のイベントをリッスンすることができます。ビジネスロジックは、モニタのコールバック関数内で完結させることができます。以下は、一般的なイベントです：

- `connect`

  接続に成功し、パラメータがconnackのときにトリガーされます。

  ````
  client.on('connect', function (connack) {
    console.log('Connected')
  })
  ````

- `reconnect`

  ブローカーが切断されたとき、再接続間隔をおいて自動的に再接続されたときにトリガーされる

  ```
  client.on('reconnect', function () {
    console.log('Reconnecting...')
  })
  ```

- `close`

  切断後、トリガーされる

  ```
  client.on('close', function () {
    console.log('Disconnected')
  })
  ```

- `disconnect`

  ブローカーが送信した切断パケットを受信したときにトリガーされ、パラメータパケットは切断時に受信したパケットである。MQTT 5.0の新機能である。

  ```
  client.on('disconnect', function (packet) {
    console.log(packet)
  })
  ```

- `offline`

  クライアントがオフラインになったときにトリガーされる

  ```
  client.on('offline', function () {
    console.log('offline')
  })
  ```

- `error`

  クライアントが正常に接続できないか、パースエラーが発生した場合にトリガーされます。パラメータエラーは、エラーメッセージ

  ```
  client.on('error', function (error) {
    console.log(error)
  })
  ```

- `message`

  このイベントは、クライアントが、トピック、ペイロード、パケットという3つのパラメータを含む公開ペイロードを受信したときにトリガーされる。topicは受信したメッセージのトピック、payloadは受信したメッセージの内容、packetはQoSやretainなどの情報を含むMQTTパケットを指します。

  *注）受信したペイロードはBuffer型の値である。必要に応じて、JSON.parse、JSON.stringify、toString()メソッドを使用し、最終的なフォーマットを表示することができます。*

  ```
  client.on('message', function (topic, payload, packet) {
    // Payload is Buffer
    console.log(`Topic: ${topic}, Message: ${payload.toString()}, QoS: ${packet.qos}`)
  })
  ```

### クライアント機能

イベントをリッスンするだけでなく、クライアントにはパブリッシュとサブスクライブのためのいくつかの組み込み関数があります。ここでは、よく使われる関数をいくつか紹介します。

- `Client.publish(topic, message, [options], [callback])`

  トピックにメッセージを公開するための関数で、4つのパラメータを持つ：

  - topic：送信するトピック（文字列
  - メッセージ送信するトピック下のメッセージで、文字列またはBufferを指定します。
  - オプションを指定します：オプションの値。メッセージ公開時の設定情報を指し、主にメッセージ公開時のQoSやRetainの値を設定するために使用される。
  - callback: メッセージが公開された後のコールバック関数。パラメータはerrorです。このパラメータは、公開に失敗した場合のみ存在する

  ```
  // Send a test message with QoS of 0 to the testtopic
  client.publish('testtopic', 'Hello, MQTT!', { qos: 0, retain: false }, function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Published')
    }
  }
  ```

- `Client.subscribe(topic/topic array/topic object, [options], [callback])`

  1つまたは複数のトピックを購読する機能です。接続に成功したら、メッセージを取得するためにトピックを購読する必要があります。この関数には3つのパラメータがあります：

  - トピックを指定します：文字列、文字列の配列、トピックオブジェクト、 `{'test1': {qos: 0}, 'test2': {qos: 1}}` を渡すことができる。
  - オプションを指定します：オプションの値。トピックを購読する際の設定情報です。主に購読するトピックのQoSレベルを記入するために使用される
  - callback: トピックを購読した後のコールバック関数。パラメータはerrorとgrassedです。errorパラメータは購読に失敗したときのみ存在します。grantedは{topic, QoS}の配列で、topicは購読したトピック、QoSはそのトピックに付与されたQoSレベルです。

  ```
  // Subscribe to a topic named testtopic with QoS 0
  client.subscribe('testtopic', { qos: 0 }, function (error, granted) {
    if (error) {
      console.log(error)
    } else {
      console.log(`${granted[0].topic} was subscribed`)
    }
  })
  ```

- `Client.unsubscribe(topic/topic array, [options], [callback])`

  1つのトピックまたは複数のトピックの購読を解除します。この関数には3つのパラメータがあります：

  - トピック文字列や文字列の配列を渡すことができる
  - オプションです：オプションの値です。配信停止時の設定情報を参照する。
  - Callback: 配信停止時のコールバック関数です。パラメータはerrorです。errorパラメータは、配信停止に失敗した場合のみ存在します。

  ```
  // Unsubscribe to a topic named testtopic
  client.unsubscribe('testtopic', function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Unsubscribed')
    }
  })
  ```

- `Client.end([force], [options], [callback])`

  クライアントを閉じます。この関数には3つのパラメータがあります：

  - を強制します：trueを指定すると、切断メッセージの受け付けを待たずに、クライアントを即座に終了させます。このパラメータはオプションで、デフォルトはfalseです。注意：trueに設定すると、Brokerは切断パケットを受信できなくなります
  - オプションを指定します：オプション値、クライアントを閉じる際の設定情報、
  - オプション：オプションの値。クライアントが終了した際の設定情報を指す。主に切断時のreasonCodeを設定するために使用される。
  - callback: クライアントが終了したときのコールバック関数

  ```
  client.end()
  ```

JavaScriptでMQTT.jsを使用する完全な例は、以下をご覧ください： [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-JavaScript](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-JavaScript) 

## MQTT.js Q&A

### ブラウザで双方向認証接続を実現できますか？

OSの証明書ストアやスマートカードにクライアント証明書が設定されている場合でも、ブラウザで接続を確立する際にJavaScriptのコードを使用してクライアント証明書を指定することはできません。つまり、MQTT.jsはこれを行うことができません。また、認証局（CA）もブラウザによって制御されるため、指定することができない。

Reference: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-JavaScript](https://github.com/mqttjs/MQTT.js/issues/1515) 

### TypeScriptでMQTT.jsを使うことはできますか？

はい、MQTT.jsはTypeScriptで使用することができます。ライブラリにはTypeScriptの型定義が含まれています。

型式ファイルはこちらでご覧いただけます：[https://github.com/mqttjs/MQTT.js/tree/main/types](https://github.com/mqttjs/MQTT.js/tree/main/types) 

TypeScriptを使用した場合のコード例です：

```
import * as mqtt from "mqtt"
const client: mqtt.MqttClient = mqtt.connect('mqtt://broker.emqx.io:1883')
```

### 1つのMQTT.jsクライアントで複数のブローカーに接続することは可能ですか？

いいえ、各MQTT.jsクライアントは、一度に1つのブローカーにしか接続できません。複数のブローカーに接続したい場合は、複数のMQTT.jsクライアントインスタンスを作成する必要があります。

### **Vue、React、AngularのアプリケーションでMQTT.jsを使用することはできますか？**

はい、MQTT.jsは、Vue、React、Angularフレームワークを使用したものを含む、あらゆるJavaScriptベースのアプリケーションに統合することができるライブラリです。

### WebSocketの接続が確立できない？

WebSocketに接続する場合、プロトコル、ポート、Hostが全て正しい場合、必ずパスを追加してください。

## MQTT.jsアドバンス

### MQTT.jsのアプリケーションをデバッグする方法

MQTT.jsアプリケーションのデバッグは、開発プロセスにおいて不可欠な要素です。このガイドでは、Node.jsとブラウザ環境でMQTT.jsのデバッグログを有効にする方法と、より深いトラブルシューティングのためにWiresharkなどのネットワークプロトコルアナライザを使用する場合について説明します。

**Node.jsでMQTT.jsのデバッグを行う。**

Node.js環境では、 `DEBUG` 環境変数でMQTT.jsのデバッグログを有効にすることができます：

```
DEBUG=mqttjs* node your-app.js
```

デバッグ情報が出力されるので、各ステップを比較して、送信中にMQTTメッセージに何が起こったかを確認することができます。

```
DEBUG=mqttjs* node index.js
mqttjs connecting to an MQTT broker... +0ms
mqttjs:client MqttClient :: options.protocol mqtt +0ms
mqttjs:client MqttClient :: options.protocolVersion 4 +0ms
mqttjs:client MqttClient :: options.username emqx_test +1ms
mqttjs:client MqttClient :: options.keepalive 60 +0ms
mqttjs:client MqttClient :: options.reconnectPeriod 1000 +0ms
mqttjs:client MqttClient :: options.rejectUnauthorized undefined +0ms
mqttjs:client MqttClient :: options.topicAliasMaximum undefined +0ms
mqttjs:client MqttClient :: clientId emqx_nodejs_986165 +0ms
mqttjs:client MqttClient :: setting up stream +0ms
mqttjs:client _setupStream :: calling method to clear reconnect +1ms
mqttjs:client _clearReconnect : clearing reconnect timer +0ms
mqttjs:client _setupStream :: using streamBuilder provided to client to create stream +0ms
mqttjs calling streambuilder for mqtt +3ms
mqttjs:tcp port 1883 and host broker.emqx.io +0ms
mqttjs:client _setupStream :: pipe stream to writable stream +3ms
mqttjs:client _setupStream: sending packet `connect` +2ms
mqttjs:client sendPacket :: packet: { cmd: 'connect' } +0ms
mqttjs:client sendPacket :: emitting `packetsend` +1ms
mqttjs:client sendPacket :: writing to stream +0ms
mqttjs:client sendPacket :: writeToStream result true +11ms
...
```

このコマンドを実行すると、コンソールにデバッグログが生成され、接続、メッセージの公開と購読、潜在的なエラーなど、MQTTクライアントの操作に関する詳細情報が提供されます。

 **ブラウザでMQTT.jsをデバッグする**

ブラウザ環境でのデバッグのためには、JavaScriptのコードでlocalStorageオブジェクトに特定の値を設定する必要があります：

```
localStorage.debug = 'mqttjs*'
```

この設定でブラウザを更新すると、MQTT.jsはブラウザのコンソールに詳細なデバッグ情報のログを記録し始めます。

MQTT.jsのデバッグログを使用しても問題を解決できない場合は、Wiresharkなどのネットワークプロトコルアナライザーを使用してみてください。Wiresharkは、MQTT.jsアプリケーションとMQTTブローカー間のネットワークトラフィックをキャプチャして解釈し、MQTT通信の詳細、IPアドレス、ポート番号、TCPハンドシェイクを表示することができます。MQTT.jsのデバッグログから始めて、必要に応じてWiresharkに切り替えることで、MQTT.jsアプリケーションを包括的にトラブルシューティングすることができます。

### RxJSによるMQTT.jsのメッセージ処理の最適化

> *RxJSは、オブザーバーパターンと関数型プログラミングの原則に従ったJavaScript用のリアクティブプログラミングライブラリです。非同期データストリームやイベントストリームの取り扱いを簡素化し、これらのストリームを変換・結合するためのmap、filter、reduceなどの様々な演算子を提供しています。*

実際の開発では、MQTTサーバーからクライアントに様々な種類のメッセージを送信し、それを処理する必要があります。例えば、メッセージをデータベースに保存したり、処理後にUIにレンダリングしたりする必要がある場合があります。しかし、MQTT.jsでは、これらのメッセージを処理するためにコールバックに依存しなければならず、受信したメッセージごとにコールバック関数がトリガーされます。このため、特に高頻度のメッセージを扱う場合、コールバックを頻繁に呼び出すとパフォーマンスの問題につながる可能性があります。

RxJSの強力な機能を活用することで、MQTT.jsのメッセージをより便利かつ効率的に扱うことができます。RxJSは、MQTT.jsメッセージの購読をobservableに変換することができるので、非同期のデータストリームやイベントストリームを簡単に扱うことができます。さらに、RxJSは、メッセージの変換やフィルタリングを可能にするさまざまな演算子を提供しており、より効率的にメッセージを処理することができます。また、RxJSは、複数のストリームのマージやパーティショニングなどの高度な機能の実装を支援することができます。さらに、RxJSは、メッセージのキャッシュや処理の遅延機能を提供し、複雑なデータストリームをより便利で柔軟に扱えるようにします。

ここでは、RxJSを使ってMQTT.jsのメッセージ処理を最適化する方法を、簡単な例を通して説明します。

```
import { fromEvent } from 'rxjs'
import { bufferTime, map, takeUntil } from 'rxjs/operators'

// Convert the connection close event to an Observable
const unsubscribe$ = fromEvent(client, 'close')

// Convert message subscription to Observable, continue receiving and processing messages until the connection is closed
const message$ = fromEvent(client, 'message').pipe(takeUntil(unsubscribe$)).pipe(
  map(([topic, payload, packet]: [string, Buffer, IPublishPacket]) => {
    return processMessage(topic, payload, packet)
  }),
)

// Use filter to filter out system messages
const nonSYSMessage$ = message$.pipe(filter((message: MessageModel) => !message.topic.includes('$SYS')))

// Use bufferTime to cache messages, and save them to the database in batches at a frequency of once per second.
nonSYSMessage$.pipe(bufferTime(1000)).subscribe((messages: MessageModel[]) => {
  messages.length && saveMessage(id, messages)
})

// Use bufferTime to cache messages and render them on the UI at a rate of twice per second.
nonSYSMessage$.pipe(bufferTime(500)).subscribe((messages: MessageModel[]) => {
  messages.length && renderMessage(messages)
})
```

## 概要

本記事では、MQTT.jsの一般的なAPIのうち、いくつかの利用機能を簡単に紹介しました。MQTTのトピック、ワイルドカード、リテインメッセージ、ラストウィルなどの機能については、「[MQTTガイド2023](https://www.emqx.com/en/mqtt-guide)」をご覧ください：EMQが提供する一連の記事「Beginner to Advanced」をご覧ください。MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。

実際のプロジェクトでの具体的な使用方法については、以下のリンクをご参照ください。

- [VueでMQTTを利用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [ReactでMQTTを利用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [ElectronでMQTTを使うには](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [Node.jsでMQTTを利用する方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-nodejs)
- [WebSocketでMQTTサーバに接続する。](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
