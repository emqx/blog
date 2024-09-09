## はじめに

MQTT over WebSocketは、IoTデバイスとWebアプリケーション間のリアルタイムかつ双方向の通信を可能にします。MQTT WebSocketクライアントツールは、開発者がIoTプロジェクトにおけるMQTTおよびWebSocketプロトコルの実装を容易にデバッグできるようにします。

![MQTT over WebSocket](https://assets.emqx.com/images/772cccbb5a614e866fe2307691bec38f.png)

このブログ記事では、2023年に強く推奨されるMQTT WebSocketクライアントツールの上位3つを探ります。

## 無料公開のMQTTブローカー

MQTT WebSocketツールに飛び込む前に、通信とテストのためにWebSocketをサポートするMQTTブローカーを必要とします。ここでは、 `broker.emqx.io` で利用できる無料のパブリックMQTTブローカーを選びました。

> ***MQTT Broker Info MQTTブローカー情報***
>
> *サーバー：broker.emqx.io*
>
> *TCPポート：1883*
>
> *WebSocketポート：8083*
>
> *SSL/TLSポート：8883*
>
> *セキュアWebSocketポート：8084*


詳しくは、こちらをご確認ください： [無料公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)

## 1. MQTT.js

MQTT.jsは、JavaScriptで書かれたMQTTクライアントライブラリで、node.jsとブラウザの両方の環境で動作するよう設計されています。MQTTプロトコルバージョン3.1.1、5.0、TCP、TLS、WebSocketトランスポートを完全にサポートしています。
MQTT.jsは、WebSocketを介してMQTTブローカーへの接続やMQTTトピックの公開・購読を簡単に行うことができるシンプルかつ軽量なライブラリです。
さらに、MQTT.jsは優れたドキュメントとコミュニティ・サポートを提供しているため、開発者は容易に開発を開始し、遭遇した問題を解決することができます。

GitHubプロジェクトです： [https://github.com/mqttjs/MQTT.js/](https://github.com/mqttjs/MQTT.js/) 

### Features 特徴

- MQTT v3.1.1およびv5.0対応
- TCP、TLS/SSL、WebSocketに対応。
- 自動トピックエイリアス
- 自動再接続
- メッセージバッファ

### Installation インストール

```
npm install mqtt -g
```

### 使用例

ここでは、MQTT over WebSocketで無料公開ブローカーに接続し、MQTTトピックを購読して、メッセージを送受信する例を紹介します。

```
var mqtt = require('mqtt')
// Connect the 8083 port with `ws` protocol.
var client = mqtt.connect('ws://broker.emqx.io:8083/mqtt')

client.on('connect', function () {
  // Subscribe to a topic
  client.subscribe('test/topic', function (err) {
    if (!err) {
      // Publish a message to a topic
      client.publish('test/topic', 'Hello mqtt')
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


## 2. MQTTX Web

[MQTTX Web](https://mqttx.app/web)は、MQTTアプリケーションをオンラインでデバッグ、開発、テストするための、ユーザーフレンドリーなブラウザベースのツールです。WebSocketクライアントを介してMQTTブローカーに接続し、直感的なインターフェイスを提供します。
EMQX チームによって開発された MQTTX Web は、MQTT 3.1.1 および MQTT 5.0 プロトコルと WebSocket トランスポートをサポートするオープンソースのツールです。Apache Version 2.0の下でライセンスされています。

フリーオンラインMQTTXのWeb： [https://mqttx.app/web-client/](https://mqttx.app/web-client/#/recent_connections)

公式サイトです： [https://mqttx.app/web](https://mqttx.app/web) 

GitHubプロジェクトです： [https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web) 

![MQTTX Web](https://assets.emqx.com/images/475a04d5d94250f41941d4c915649422.png)

### 特徴

- 初心者から上級者まで、使いやすいインターフェイス
- ブラウザベースのため、ダウンロードやインストールは必要なし
- MQTTメッセージの送受信を行うチャットボックスUI
- MQTT v3.1.1およびMQTT v5.0対応
- MQTT over WebSocketのサポート
- ローカルデプロイメントにDockerを使用する

### 使用例

1. Web ブラウザで [MQTTX Web](https://mqttx.app/web-client/) を開きます。

2. WebSocketを使用して[MQTT接続](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)を作成します：

   ![Create an MQTT connection](https://assets.emqx.com/images/d2ac378be20377c69c7387c77cd2cf93.png)

3. MQTTトピックにサブスクライブし、トピックにメッセージをパブリッシュします：

   ![Subscribe to an MQTT topic and publish messages to the topic](https://assets.emqx.com/images/d20101ab94108f835bcccb21ee2d1688.png)


## 3. Paho JavaScriptクライアント

Paho JavaScript Clientは、Javascriptで書かれたMQTTブラウザベースのクライアントライブラリで、WebSocketを使用してMQTT Brokerに接続することができます。


Paho MQTTは、Eclipse Foundationによって開発されたMQTT 3.1.1を実装するオープンソースのMQTTクライアントです。ただし、2019年6月以降、プロジェクトの積極的なメンテナンスは行われていません。

公式サイトです： [https://www.eclipse.org/paho/index.php?page=clients/js/index.php](https://www.eclipse.org/paho/index.php?page=clients/js/index.php) 

GitHubプロジェクトです： [https://github.com/eclipse/paho.mqtt.javascript](https://github.com/eclipse/paho.mqtt.javascript)

Features: 特徴

- MQTT 3.1.1およびWebSocketのサポート

- SSL / TLS対応

- メッセージの永続性

- 自動再接続


### 使用例

使用例については、プロジェクトの[README](https://github.com/eclipse/paho.mqtt.javascript)をご確認ください。

## Wrap up ラップアップ

MQTT.jsは、MQTT over WebSocketを必要とするWebアプリケーションのためのJavascriptで書かれた最高のクライアント・ライブラリですが、Paho JavaScriptクライアントは活発に開発されていません。また、MQTTX Webは、MQTT over WebSocketのデバッグとテストに最適なクライアント・ツールボックスです。
