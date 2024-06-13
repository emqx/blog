## はじめに

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ／サブスクライブモデルに基づく軽量[のIoTメッセージング](https://www.emqx.com/en/solutions/reliable-mqtt-messaging)プロトコルです。非常に少ないコードと帯域幅で、ネットワークデバイスにリアルタイムかつ信頼性の高いメッセージングサービスを提供することができます。IoT、モバイルインターネット、スマートハードウェア、[Internet of Vehicles](https://www.emqx.com/en/use-cases/internet-of-vehicles)、電力エネルギーなどの産業で広く利用されている。

Node.jsは、イベント駆動型のアーキテクチャとリアルタイムのデータハンドリングにより、IoTで広く利用されています。デバイス、サーバ、APIを簡単に接続することができます。Node.jsとMQTTを組み合わせることで、開発者は、デバイスとリアルタイムで通信し、情報を交換し、複雑なデータ分析を行う、スケーラブルで安全なIoTアプリケーションを構築できます。

この記事では、Node.jsプロジェクトでMQTTを使用して、クライアントと[MQTTブローカー](https://github.com/emqx/emqx)間のシームレスな通信を実現するための包括的なガイドを提供します。接続の確立、トピックのサブスクライブとアンサブスクライブ、メッセージの公開、およびリアルタイムでのメッセージの受信方法について学びます。このガイドでは、MQTTを活用してスケーラブルで効率的なIoTアプリケーションを構築するためのスキルを身につけることができます。

## Node.js MQTTプロジェクト準備編

### Node.jsのバージョン確認

このプロジェクトでは、開発およびテストに Node.js v16.20.0 を使用しています。正しいバージョンのNode.jsがインストールされていることを確認するために、読者は以下のコマンドを使用することができます：

```
node --version

v16.20.0
```

### MQTT.jsをインストールする

MQTT.jsは、MQTTプロトコルのクライアントライブラリで、node.jsとブラウザ用にJavaScriptで書かれています。JavaScriptのシングルスレッド機能により、MQTT.jsは完全な非同期型MQTTクライアントとなります。現在、JavaScriptエコシステムで最も広く使われている[MQTTクライアントライブラリ](https://www.emqx.com/en/mqtt-client-sdk)です。

MQTT.jsのインストールには、NPMやYarnを使用します。

-  **NPM**

  ```
  # create a new project
  npm init -y
  
  # Install dependencies
  npm install mqtt --save
  ```

-  **YARN**

  ```
  yarn add mqtt
  ```

インストールしたら、カレントディレクトリに新しいindex.jsファイルを作成し、これがプロジェクトのエントリファイルとして機能します。ここで、MQTT接続テストの完全なロジックを実装することができます。

## MQTTブローカー実装の準備

先に進む前に、通信とテストを行うためのMQTTブローカーがあることを確認してください。MQTTブローカーを入手するには、いくつかのオプションがあります：

-  **プライベート展開**

  [EMQX](https://github.com/emqx/emqx)は、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

-  **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。[EMQX Cloud](https://www.emqx.com/en/cloud)を利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版の[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)は、開発者が数秒で簡単にMQTTの導入を開始できるように、永久無料の1Mセッション分/月の無償提供をしています。

-  **無料公開のMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 `broker.emqx.io` の無料公開MQTTブローカーを使用することにします。

>  ***MQTTブローカー情報***
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

詳しくは、こちらをご確認ください：[無料公開のMQTTブローカー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)。

## Node.js MQTTの使用法

### MQTTコネクションの作成

#### TCPコネクション

MQTT.jsクライアントライブラリのインポート

> *注）Node.js環境では、依存モジュールのインポートにcommonjs仕様を使用してください。*

```
const mqtt = require('mqtt')
```

MQTT接続を確立するために、接続アドレス、ポート、クライアントIDを設定する必要がある。この例では、クライアントIDの生成にJavaScriptに内蔵されている乱数生成関数を利用しています。

```
const protocol = 'mqtt'
const host = 'broker.emqx.io'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `${protocol}://${host}:${port}`
```

次に、ホストとポートをつなげて作成した URL を使って接続を確立する。これを実現するために、MQTTモジュールの組み込みconnect関数を呼び出し、接続が確立されると、Clientインスタンスを返します。

```
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
})

client.on('connect', () => {
  console.log('Connected')
})
```

詳しくは、ブログ「[MQTT接続の確立時にパラメータを設定する方法](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)」をご確認ください。

#### ウェブソケット

MQTT over WebSocketを使ってブローカーに接続する場合、いくつか注意しなければならないことがあります：

- WebSocketの接続URLは、 `ws` プロトコルで始まる必要があります。
- ポートを正しいWebSocketポートに更新します（例： `broker.emqx.io` の場合は8083）。
- 接続URLの末尾にpathパラメータを付加するようにしてください（例： `broker.emqx.io` の場合は `/mqtt` のように）。

```
const protocol = 'ws'
const host = 'broker.emqx.io'
const port = '8083'
const path = '/mqtt'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `${protocol}://${host}:${port}${path}`
```

#### TLS/SSL

MQTTでTLSを使用することで、情報の機密性と完全性を確保し、情報の漏洩や改ざんを防止することができます。TLS認証は、一方向性認証と双方向性認証に分類される。

**一方的な認証**

```
const fs = require('fs')

const protocol = 'mqtts'
const host = 'broker.emqx.io'
const port = '8883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `${protocol}://${host}:${port}`

const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,

  // If the server is using a self-signed certificate, you need to pass the CA.
  ca: fs.readFileSync('./broker.emqx.io-ca.crt'),
})
```

**双方向認証**

```
const fs = require('fs')

const protocol = 'mqtts'
const host = 'broker.emqx.io'
const port = '8883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `${protocol}://${host}:${port}`

const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,

  // Enable the SSL/TLS, whether a client verifies the server's certificate chain and host name
  rejectUnauthorized: true,
  // If you are using Two-way authentication, you need to pass the CA, client certificate, and client private key.
  ca: fs.readFileSync('./broker.emqx.io-ca.crt'),
  key: fs.readFileSync('./client.key'),
  cert: fs.readFileSync('./client.crt'),
})
```

### MQTTトピックを購読する

返されたClientインスタンスの `on` 関数を使って接続状態を監視し、接続成功後のコールバック関数でトピック `/nodejs/mqtt` にサブスクライブしています。

```
const topic = '/nodejs/mqtt'

client.on('connect', () => {
  console.log('Connected')
  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
})
```

トピックの購読に成功すると、 `on` 関数を使用して受信メッセージを監視することができます。新しいメッセージが到着すると、この関数のコールバック関数内で関連するトピックとメッセージを取得することができます。これにより、受信したメッセージを効果的に処理し、それに応じて応答することができます。

> *注：コールバック関数内で受信したメッセージはBuffer型であり、toString関数で文字列に変換する必要があります。*

```
client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})
```

### MQTTメッセージの発行

以上のトピック購読とメッセージ監視が完了したら、メッセージを公開するための関数を書きます。

> *注：メッセージはMQTT接続が成功した後に公開する必要があるので、接続が成功した後のコールバック関数に記述しています。*

```
client.on('connect', () => {
  client.publish(topic, 'nodejs mqtt test', { qos: 0, retain: false }, (error) => {
    if (error) {
      console.error(error)
    }
  })
})
```

### MQTT接続を切断する

MQTT.js では、ブローカーとの接続を解除するために、 `mqtt.Client` オブジェクトの `end()` メソッドを使用する必要があります。このメソッドはリソースを解放し、接続を閉じます。このメソッドに `true` というパラメータを渡すと強制的に切断され、 `DISCONNECT` メッセージは送信されず、代わりに接続が直接切断されます。また、切断が完了した時点で呼び出されるコールバック関数を渡すことも可能です。

```
// Disconnect
client.end()

// Force disconnect
client.end(true)

// Callback for disconnection
client.end(false, {}, () => {
  console.log('client disconnected')
})
```

`end()` メソッドの詳細については、[公式ドキュメント](https://github.com/mqttjs/MQTT.js#mqttclientendforce-options-callback)を参照してください。

###  エラー処理

-  接続エラー処理

  ```
  client.on('error', (error) => {
    console.error('connection failed', error)
  })
  ```

-  再接続のエラー処理

  ```
  client.on('reconnect', (error) => {
    console.error('reconnect failed', error)
  })
  ```

-  サブスクリプションのエラー処理

  ```
  client.on('connect', () => {
    client.subscribe('topic', subOpts, (error) => {
      if (error) {
        console.error('subscription failed', error)
      }
    })
  })
  ```

-  パブリッシングエラー処理

  ```
  client.on('connect', () => {
    client.publish('topic', 'hello mqtt', (error) => {
      if (error) {
        console.error('publish failed', error)
      }
    })
  })
  ```

## コンプリートコード

サーバー接続、トピック購読、メッセージ公開、受信のコードは以下の通りです。

```
const mqtt = require('mqtt')

const host = 'broker.emqx.io'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `mqtt://${host}:${port}`

const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
})

const topic = '/nodejs/mqtt'

client.on('connect', () => {
  console.log('Connected')

  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`)
    client.publish(topic, 'nodejs mqtt test', { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error(error)
      }
    })
  })
})

client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})
```

このプロジェクトの完全なコードについては、[GitHub](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Node.js)で確認してください。

## テスト

package.jsonファイルのscriptフィールドに起動スクリプトを1行追加します。

```
"scripts": {
  "start": "node index.js"
}
```

単純に `npm start` でプロジェクトを実行すればいいのです。

```
npm start
```

すると、コンソールの出力情報が以下のように表示されます：

![NodeJS MQTT Start](https://assets.emqx.com/images/9897e6cd56163dfe7139cf6d84361e63.png)

クライアントがMQTTブローカーに正常に接続し、トピックをサブスクライブし、メッセージを受信し、正常にパブリッシュしたことがわかります。このとき、もう1つのクライアントとしてMQTT Client Tool - MQTTXを使用して、メッセージの公開と受信のテストを行うことにします。

![MQTTX](https://assets.emqx.com/images/5c841598f78eed0b186572165832f861.png)

MQTTXで送信されたメッセージがコンソールに出力されていることが確認できます。

![MQTT messages](https://assets.emqx.com/images/02d8a35312ca1309f18a628dacca8910.png)

## Q&A

### **MQTTメッセージはどのようなフォーマットで送られてくるのですか？**

Node.jsでMQTTを使用する場合、MQTTメッセージはBufferとして提供されます。これは、生のバイナリデータを扱うように設計されているためで、テキストだけでなく、あらゆる形式のデータを含む可能性があります。

### **Node.jsでBufferとして受信したMQTTメッセージをどのように扱えばよいですか？**

Node.jsでBufferを扱うには、 `toString()` メソッドを使用して文字列に変換します。元のメッセージがJSONオブジェクトだった場合、 `JSON.parse()` で文字列をパースしてオブジェクトに戻す必要があるかもしれません。以下はその例です：

```
client.on('message', (topic, message) => {
  // message is a Buffer
  let strMessage = message.toString();
  let objMessage = JSON.parse(strMessage);
  console.log(objMessage);
})
```

### **送信されたMQTTメッセージがJSON形式でない場合はどうすればよいですか？**

MQTTメッセージがJSONでない場合でも、 `toString()` メソッドを使って文字列に変換することができます。ただし、内容がもともと文字列でない場合（例えばバイナリデータの場合）には、データの性質に応じて異なる処理をする必要があるかもしれません。

### **Node.jsのMQTTクライアントがメッセージを受信しない場合の対処法とは？**

- 正しいトピックを購読していることを確認してください。MQTTのトピックは大文字と小文字が区別され、完全に一致する必要があります。
- ブローカーが起動していること、接続できることを確認します。
- [MQTT QoS](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)レベル1または2を使用している場合、メッセージが同じQoSレベルで発行されることを確認してください。
- クライアントで `error` イベントをリッスンして、エラーが投げられたかどうかを確認します。

### **Node.js MQTTアプリケーションの問題をデバッグするにはどうすればよいですか？**

- MQTTクライアントで「エラー」イベントを聞いてください。これは、問題についての有益な情報を提供することが多い。
- コードの中でconsole.log文を使い、流れを確認したり、変数の内容を見たりします。
- MQTTメッセージに問題がある場合は、'#'トピックを購読してみてください。これは、すべてのメッセージにマッチするワイルドカードトピックなので、公開されているすべてのメッセージを見ることができます。
- 接続に問題がある場合は、ブローカーのログを確認し、そこに手がかりがないかどうか確認してください。
- [MQTTX](https://mqttx.app/)のようなツールを使って、ブローカーに手動で接続し、トピックを発行/購読することを検討してください。これは、問題がNode.jsのコードにあるのか、ブローカーにあるのかを判断するのに役立ちます。

## Node.js MQTTアドバンス

### **Express.jsなどのWebフレームワークでMQTTを利用する方法**

> *Express.jsは、Node.jsを使用してWebアプリケーションやAPIを構築する、オープンソースのWebアプリケーションフレームワークです。現在、最も人気のあるNode.jsのWebフレームワークの1つで、Webアプリケーションを作成する際に高い柔軟性とスケーラビリティを備えています。*

MQTTをExpress.jsに組み込むには、そのミドルウェアでMQTTの接続、公開、購読の操作を行うことができます。以下は簡単なサンプルコードです：

```
import express from 'express'
import * as mqtt from 'mqtt'

const app = express()
const mqttClient = mqtt.connect('mqtt://localhost:1883')

// Connect to the MQTT broker
mqttClient.on('connect', function () {
  console.log('Connected to MQTT broker')
})

// MQTT middleware for publishing and subscribing
app.use(function (req, res, next) {
  // Publish messages
  req.mqttPublish = function (topic, message) {
    mqttClient.publish(topic, message)
  }

  // Subscribe to topic
  req.mqttSubscribe = function (topic, callback) {
    mqttClient.subscribe(topic)
    mqttClient.on('message', function (t, m) {
      if (t === topic) {
        callback(m.toString())
      }
    })
  }
  next()
})

app.get('/', function (req, res) {
  // Publish
  req.mqttPublish('test', 'Hello MQTT!')

  // Subscribe
  req.mqttSubscribe('test', function (message) {
    console.log('Received message: ' + message)
  })

  res.send('MQTT is working!')
})

app.listen(3000, function () {
  console.log('Server is running on port 3000')
})
```

上記のコードでは、Express.jsアプリケーションを作成し、MQTTのパブリッシュとサブスクライブを処理するための `req.mqttPublish()` と `req.mqttSubscribe()` 関数を定義しています。これらの関数は、MQTTトピックへのメッセージのパブリッシュとサブスクライブを行うためのルート処理で使用することができます。この例では、ルートパスにアクセスすると、「Hello MQTT！」メッセージが「test」トピックに公開され、その後、受信したメッセージを受信して処理するために購読されます。

これはあくまで簡単な実装例であり、実際のアプリケーションでは、複数のトピックの処理やリクエストパラメータの検証など、より複雑な処理が必要となる場合があります。

### **Node.jsでコマンドラインツールを構築する方法**

Node.jsは堅牢なオープンソースエコシステムを誇り、開発者は様々なオープンソースライブラリを活用することで、特定のビジネス要件を満たすMQTTクライアントツールを迅速に作成することが可能です。さらに、Node.js は、 `pkg` ツールを使用してプロジェクトを実行可能なファイルに簡単にパッケージ化できるため、クロスプラットフォームでの展開が可能です。例えば、Node.jsのコマンドラインツールライブラリであるCommander.jsを利用すれば、カスタマイズしたコマンドラインツールを構築して、ビジネス環境に統合することができます。

次に、Commander.jsを使用して、簡単なMQTTコマンドラインツールを構築する方法を説明します。このツールの特徴は、2つのコマンドです： `pub` と `sub` です。

- `pub` コマンドは、ユーザーが指定したトピックにメッセージを公開することができます。
- `sub` コマンドは、指定されたトピックを購読し、受信したメッセージを表示することを許可します。

```
// mqtt-cli.js

import { program } from 'commander'
import mqtt from 'mqtt'

// MQTT Broker URL
const brokerUrl = 'mqtt://localhost:1883'

// Define CLI commands
program
  .command('pub')
  .description('Publish message to the given topic')
  .option('-t, --topic <TOPIC>', 'the message topic')
  .option('-m, --message <BODY>', 'the message body')
  .action((options) => {
    const { topic, message } = options

    const client = mqtt.connect(brokerUrl)

    client.on('connect', () => {
      client.publish(topic, message, () => {
        console.log(`Published message "${message}" to topic "${topic}"`)
        client.end()
      })
    })
  })

program
  .command('sub')
  .description('Subscribe to the given topic and log incoming messages')
  .option('-t, --topic <TOPIC>', 'the message topic')
  .action((options) => {
    const { topic } = options

    const client = mqtt.connect(brokerUrl)

    client.on('connect', () => {
      console.log(`Subscribed to topic "${topic}"`)

      client.subscribe(topic, () => {
        client.on('message', (topic, message) => {
          console.log(`Received message "${message.toString()}" on topic "${topic}"`)
        })
      })
    })
  })

program.parse(process.argv)
```



```
# Subscribe to test topic
node mqtt-cli.js sub -t test

# Publish an MQTT message
node mqtt-cli.js pub -t test -m 'Hello MQTT!'
```

## まとめ

これまで、Node.jsを[MQTTクライアント](https://www.emqx.com/en/blog/mqtt-client-tools)として、[パブリックなMQTTブローカー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)に接続し、テストクライアントとMQTTサーバー間の接続、メッセージ発行、購読を実現してきました。

次に、MQTTガイドをチェックすることができます：EMQが提供する「[Beginner to Advanced](https://www.emqx.com/en/mqtt-guide)」シリーズで、MQTTプロトコルの機能を学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
