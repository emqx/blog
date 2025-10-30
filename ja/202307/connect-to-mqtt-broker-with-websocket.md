近年、Webフロントエンド技術の急速な発展により、新しいブラウザ機能が登場している。ブラウザのレンダリングエンジンを通じて、ブラウザ側で実装できるアプリケーションも増えてきた。その一つがWebSocketで、Webアプリケーションのインスタント通信手段として広く使われている。

WebSocketは、単一のTCPコネクション上で全二重通信チャネルを提供するコンピュータ通信プロトコルである。IETFは2011年にRFC 6455としてWebSocketプロトコルを標準化し、Web IDLにおけるWebSocket APIは現在W3Cによって標準化されている。

[MQTTプロトコルの第6章](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718127)では、[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)がWebSocket [RFC6455]接続を介して転送されるために満たすべき条件を規定している。このトピックについては、ここでは詳しく説明しない。

## WebSocketとは？

WebSocketは、1つのTCPコネクション上で双方向通信チャネルを可能にするネットワーク通信プロトコルです。HTTPとは異なり、WebSocketはクライアントとサーバーの間にオープンなコネクションを保持するため、即時にインタラクティブにデータを交換できます。これにより、WebSocketはオンラインゲーム、チャットアプリケーション、株式取引システムなどのリアルタイムインタラクティブアプリケーションに理想的です。

WebSocketプロトコルには、ハンドシェイクとデータ転送の2つの部分があります。ハンドシェイクはクライアントとサーバーの間にコネクションを確立し、データ転送はオープンなコネクション上で情報を交換します。

## MQTT over WebSocketを使う理由

MQTT over WebSocketsは急速にIoTインタラクションに不可欠なコンジットとなりつつあり、よりアクセスしやすく、効率的で、豊かなエクスペリエンスを提供しています。あらゆるウェブ・ブラウザを通じて直接MQTTデータ通信を可能にすることで、IoTの世界をより身近なものにします。

WebSocket上でMQTTを使用する理由をいくつか挙げます：

1. 簡素化されたインタラクション：どのウェブブラウザでも、IoTデバイスと直接対話できます。異なるプロトコルを心配する必要はありません - MQTT over WebSocketで簡単です。
2. ユニバーサル・アクセシビリティ：ウェブブラウザがあれば、誰でもIoTデバイスに接続し、操作することができる。これにより、技術的な専門知識を持つ人だけでなく、すべての人にIoTの世界が開かれます。
3. リアルタイム更新：IoTデバイスからリアルタイムでデータを取得し、最新の洞察をブラウザに直接提供します。
4. 効率性と幅広いサポート：MQTTは軽量なプロトコルであり、JavaScriptのWebSocketの広範なサポートと組み合わせることで、ほとんどすべてのWebアプリケーションで効率的なリアルタイムデータ伝送が可能になる。
5. データ可視化の強化：ウェブページは、様々なMQTTデータをより良く、より速く、より豊かに表示することができます。この利点は、ウェブブラウザがMQTTデータを視覚化するための事実上のインターフェイスになるにつれ、特に重要です。

MQTT over WebSocketは、IoTデバイスへのアクセスを民主化し、ウェブブラウザを持つ誰もがリアルタイムで簡単にこれらのデバイスと対話できるようにする。

次に、WebSocket上でMQTTを使用するための包括的なガイドを提供します。

## MQTTブローカーを構築

先に進む前に、通信およびテストするためのMQTTブローカーがあることを確認してください。MQTTブローカーを入手するには、いくつかのオプションがあります：

-  **プライベート展開**

  [EMQX](https://github.com/emqx/emqx)は、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:888 -p 18083:18083 emqx/emqx
  ```

- **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。[EMQX Cloud](https://www.emqx.com/ja/cloud)を利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版の[EMQX Cloud Serverless](https://www.emqx.com/ja/cloud/serverless-mqtt)は、開発者が数秒で簡単にMQTTの導入を開始できるように、永久無料の1Mセッション分/月の無償提供をしています。

-  **無料公開のMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 `broker.emqx.io` の無料公開MQTTブローカーを使用します。

> MQTT Broker Info:
>
> Server: `broker.emqx.io`
>
> TCP Port: `1883`
>
> WebSocket Port: `8083`
>
> SSL/TLS Port: `8883`
>
> Secure WebSocket Port: `8084`

詳細については、[Free Public MQTT Broker](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)をご覧ください。

> *EMQXはデフォルトで、通常の接続にはポート8083を、WebSocket over TLSにはポート8084を使用する。*

## MQTT over WebSocketを始めよう

### MQTT WebSocketクライアントをインストールする

[MQTT.js](https://github.com/mqttjs/MQTT.js)は、JavaScriptで書かれ、Node.jsとブラウザで利用可能な、MQTTプロトコル用の完全にオープンソースのクライアントサイド・ライブラリです。MQTT/TCP、MQTT/TLS、MQTT/WebSocket接続をサポートしています。

この記事では、MQTT.jsライブラリを使ってWebSocket接続について説明する。

MQTT.jsをインストールするには、マシンにNode.jsの実行環境があれば、 `npm` コマンドを使用します。グローバルにインストールし、Node.jsのコマンドラインから接続することができます。

**Node.jsプロジェクトのインストール**

```sh
# npm
npm install mqtt --save

# yarn
yarn add mqtt
```

**CDNリファレンス**

ブラウザで直接作業していて、ライブラリをインストールしたくない場合は、CDNを使うこともできる：

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
   // Globally initializes an mqtt variable
   console.log(mqtt)
</script>
```

### ブラウザでWebSocketを介してブローカーに接続する

簡単にするために、基本的な HTML ファイルを作成することで、 ブラウザに直接実装することにします。このファイルでは、パブリッシュ者とサブスクライブ者の両方を設定します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weboscoket MQTT</title>
  <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>
<body>
  Use WebSocket client to connect to MQTT server
</body>
<script>
    const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)
    const host = 'ws://broker.emqx.io:8083/mqtt'
    const options = {
      keepalive: 60,
      clientId: clientId,
      protocolId: 'MQTT',
      protocolVersion: 4,
      clean: true,
      reconnectPeriod: 1000,
      connectTimeout: 30 * 1000,
      will: {
        topic: 'WillMsg',
        payload: 'Connection Closed abnormally..!',
        qos: 0,
        retain: false
      },
    }
    console.log('Connecting mqtt client')
    const client = mqtt.connect(host, options)
    client.on('error', (err) => {
      console.log('Connection error: ', err)
      client.end()
    })
    client.on('reconnect', () => {
      console.log('Reconnecting...')
    })
</script>
```

### 接続アドレス

接続アドレスの例である `ws://broker.emqx.io:8083/mqtt` には、 `protocol` // `hostname` .`domain` : `port` / `path` が含まれます。 

初心者がよくあるミス:

- MQTT.jsクライアントへの接続時には、接続アドレスにプロトコルの種類を指定することが重要です。これはクライアントが複数のプロトコルをサポートしているためです。さらに、MQTTはWebSocketのポートを指定していません。EMQXのデフォルトは非暗号化コネクションの8083、暗号化コネクションの8084です。
- 接続アドレスからパスを除外: MQTT over WebSocketは一様に `/mqtt` を接続パスとして使用するので、接続時にはこれを指定する必要があります。
- プロトコルとポートが一致していない。MQTTには`mqtt://`を、WebSocket接続には`ws://`または`wss://`を使用し、HTTPS下では暗号化WebSocket接続を使用してください。
- 証明書が接続アドレスと一致していない。

### 接続オプション

前のコード・スニペットでは、 `options` はクライアント接続オプションを指している。これらのオプションには、 `keepalive` 、 `clientId` 、 `username` 、 `password` 、 `clean` 、 `reconnectPeriod` 、 `connectTimeout` 、 `will` といったパラメータが含まれる。各オプションの詳細については、[MQTT.jsのドキュメント](https://github.com/mqttjs/MQTT.js#client)を参照してください。

### サブスクライブ/サブスクライブ解除

サブスクリプションは接続が成功した後にのみ行うことができ、サブスクライブされたトピックは MQTT サブスクリプショントピックルールに従わなければならない。JavaScriptの非同期機能は、'connect'イベントの後、または `client.connected` を使用することによってのみ、成功した接続が保証されることを意味します。

```js
client.on('connect', () => {
  console.log(`Client connected: ${clientId}`)
  // Subscribe
  client.subscribe('testtopic', { qos: 0 })
})
// Unsubscribe
client.unubscribe('testtopic', () => {
  console.log('Unsubscribed');
})
```

### メッセージの**パブリッシュ**／受信

特定のトピックにメッセージをパブリッシュすることができ、そのトピックは MQTT パブリッシュ・トピック・ルールに準拠している必要があります。パブリッシュする前にトピックをサブスクライブする必要はありません。

```js
// Publish
client.publish('testtopic', 'ws connection demo...!', { qos: 0, retain: false })
// Receive
client.on('message', (topic, message, packet) => {
  console.log(`Received Message: ${message.toString()} On topic: ${topic}`)
})
```

より詳細な情報と例については、JavaScript MQTT Clientを参照してください：[A Beginner's Guide to MQTT.js](https://www.emqx.com/ja/blog/mqtt-js-tutorial)をご参照ください。

### SSL/TLS経由でWebSocketを使用する

セキュアなWebSocket接続は、基本的にTLS（以前のSSL）接続上のWebSocketであるWSSプロトコル（WebSocket Secure）を使用して確立することができます。TLSは、接続を介して送信されるデータを暗号化するために使用され、データのプライバシーと完全性、および認証を保証します。

MQTT.js で WebSocket over TLS を使用するには、ブローカーアドレスのプロトコルを `ws` から `wss` に変更する必要があります。 ただし、接続先のブローカーが WSS 接続をサポートしていることと、ポート番号が WSS 用の正しいものであることも確認する必要があります。例えば、EMQX はデフォルトで WSS 接続に `8084` ポートを使用します。

以下は、安全な接続を確立する方法の例である：

```js
const host = 'wss://broker.emqx.io:8084/mqtt'
const options = {
  // other options as before
}

const client = mqtt.connect(host, options)

// rest of your code...
```

HTTPS で提供されるウェブページから WSS 経由でブローカーに接続する場合、ブローカーの証明書がクライアントのブラウザーから信頼されていることを確認する必要があります。これは通常、証明書がよく知られた認証局からパブリッシュされたもので、有効期限が切れていたり、失効していたり、別のドメインで使用されていたりしないことを意味します。ブローカーに自己署名証明書を使用している場合は、ブラウザのトラストストアに手動で追加する必要があります。

WebSocket over TLSの使用に関する詳細や潜在的な問題については、[MQTT.jsのドキュメント](https://github.com/mqttjs/MQTT.js#client)またはMQTTブローカーの適切なチュートリアルを参照してください。

> *注：ブラウザでWebSocket接続を使用する場合、双方向認証接続を確立することはできません。しかし、この機能は他のほとんどのプログラミング言語環境でサポートされています。例えば、Node.jsの場合です：*

```js
const mqtt = require('mqtt')
const fs = require('fs')
const path = require('path')

const KEY = fs.readFileSync(path.join(__dirname, '/tls-key.pem'))
const CERT = fs.readFileSync(path.join(__dirname, '/tls-cert.pem'))
const TRUSTED_CA_LIST = fs.readFileSync(path.join(__dirname, '/crt.ca.cg.pem'))

const host = 'wss://broker.emqx.io:8084/mqtt'
const options = {
    ...
  key: KEY,
  cert: CERT,
  rejectUnauthorized: true,
  ca: TRUSTED_CA_LIST,
}

const client = mqtt.connect(host, options)
```

## テスト

作成したHTMLファイルをウェブ・ブラウザで開いて、セットアップをテストしてみよう。[MQTTX](https://mqttx.app/)のようなツールを使えば、MQTTインタラクションのGUIを提供できる。以下はそのテスト方法である：

1. ブラウザのコンソールを開くと、接続に成功したメッセージが表示され、サブスクライブしているトピックでメッセージを受け取ることができる。

   ![WebSocket MQTT Demo](https://assets.emqx.com/images/bc98a964995202fdfcf363062ba363fd.png)

2. MQTTXを使用してデモの同じアドレスに接続し、サブスクライブしたトピックに「Hello from MQTTX」というメッセージを送信する。

   ![MQTTX](https://assets.emqx.com/images/b87c8ee484061f0be7703458970db92b.png)

3. ブラウザのコンソールで、このメッセージが受信されるのを見ることができる。

   ![Message being received in the browser console](https://assets.emqx.com/images/03ddd11518fd159650487a897f855fee.png)

## Q&A

### MQTTとWebSocketの違いは何ですか？

MQTT（Message Queuing Telemetry Transport）は、パブリッシュ／サブスクライブ・パターンに基づくメッセージ転送プロトコルである。通常、IoTデバイス間の通信に使用される。オーバーヘッドと帯域幅の消費が少ない軽量なプロトコルであるため、リソースに制約のあるデバイスに適している。

WebSocketは、単一のTCPコネクション上で持続的な全二重通信チャネルを提供する双方向通信プロトコルです。WebSocketは通常、Webアプリケーションとサーバー間のリアルタイム通信に使用され、クライアントがリクエストを送信することなく、サーバーがクライアントにデータをプッシュできるようにします。

主な違いは、プロトコルの設計とユースケースにある：MQTTはパブリッシュ/サブスクライブ通信に使用されるメッセージ転送プロトコルであり、WebSocketはリアルタイムの双方向通信に使用される通信プロトコルである。

### WSSはブラウザでの双方向認証接続をサポートできますか？

いいえ、ブラウザで接続を確立する際にJavaScriptのコードを使用してクライアント証明書を指定することは、クライアント証明書がOSの証明書ストアや潜在的にスマートカードに設定されていたとしても不可能です。つまり、MQTT.jsではできません。さらに、認証局（CA）もブラウザによって制御されるため、指定できない。

参考資料：[How to use TLS/SSL two-way authentication connections in browser? · Issue #1515 · mqttjs/MQTT.js](https://github.com/mqttjs/MQTT.js/issues/1515)

### ブラウザ以外の環境でも使用できますか？

はい、ブラウザ以外の環境でもMQTT over WebSocketを使用できます。Python、Node.js、Golangなど、さまざまなプログラミング言語に対応する[MQTTクライアント・ライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)が用意されており、選択した環境でMQTTブローカーに接続し、MQTT over WebSocketを使用して通信することができます。TLS/SSL接続がサポートされている場合、相互証明書認証を使用することもできます。

### EMQXに接続する際にパスを入力する必要があるのはなぜですか？

WebSocket を使用して EMQX に接続する場合は、パスを入力する必要があります。これは、[EMQX](https://github.com/emqx/emqx) が MQTT-WebSocket の統一パス仕様に従っているためです。この仕様では、MQTT over WebSocket トラフィックを識別および区別するために、WebSocket 接続で特定のパスを指定する必要があります。このパスは、MQTT over WebSocket トラフィックを MQTT Broker にルーティングして処理します。

EMQX では、MQTT over WebSocket のデフォルト・パスは `/mqtt` です。これは仕様に従って設定されています。したがって、EMQX に接続する場合は、接続が MQTT ブローカーに正しくルーティングされるように、このパスを WebSocket アドレスに含める必要があります。

### Vue.jsやReactを使用してMQTTウェブ・アプリケーションを開発する場合、WebSocket接続しか使用できないのでしょうか？

ブラウザでアプリケーションを開発している場合、MQTT over WebSocket接続を確立するためにのみWebSocket接続を使用できます。

## まとめ

このクイックスタートガイドでは、MQTT over WebSocket を使用して、MQTT ブローカーと Web ブラウザ間のリアルタイム通信を確立するための基本を説明します。WebSocket 接続の確立、[MQTT クライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)の初期化、メッセージのサブスクライブと公開、接続のテストなど、基本的な手順を説明します。

このプロジェクトの完全なコードは、このGitHubリンクにあります：[MQTT-Client-Examples/mqtt-client-WebSocket at master - emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-WebSocket).

MQTTプロトコルの機能についてもっと知りたい、MQTTの高度なアプリケーションを探求したい、MQTTアプリケーションやサービス開発を始めたいという方は、MQTTガイドの連載記事をご覧ください：EMQが提供する「[Beginner to Advanced](https://www.emqx.com/en/mqtt-guide)」をご覧ください。

## リソース

MQTT over WebSocketの詳細については、以下のリソースを参照してください：

- [MQTTX ウェブ](https://mqttx.app/ja/web)

  MQTTX Webは、MQTTアプリケーションをオンラインでデバッグ、開発、テストするための使いやすいブラウザベースのツールです。WebSocketクライアントを介してMQTTブローカーに接続し、直感的なインターフェースを提供します。

- [2023年MQTTウェブソケットクライアント上位3位](https://www.emqx.com/ja/blog/top-3-mqtt-websocket-clients-in-2023)

  このブログでは、2023年に強く推奨されるMQTT WebSocketクライアント・ツールのトップ3を紹介する。

- [JavaScriptのMQTTクライアント：MQTT.js入門ガイド](https://www.emqx.com/ja/blog/mqtt-js-tutorial)

  このブログでは、JavaScriptのプロジェクトでMQTT.jsを素早く使えるように、MQTT.jsの一般的なAPIの使い方と、使用プロセスの経験を紹介します。

- [VueでMQTTを利用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)

  このブログでは、主にVueプロジェクトでのMQTTの使用方法を紹介し、クライアントとMQTTブローカー間の接続、サブスクリプション、メッセージング、サブスクリプション解除などの機能を実装します。

- [ReactでMQTTを利用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)

  この記事では主に、ReactプロジェクトでMQTTを使用し、クライアントとMQTTブローカー間でコネクト、サブスクライブ、メッセージング、アンサブスクライブなどを実装する方法を紹介する。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
