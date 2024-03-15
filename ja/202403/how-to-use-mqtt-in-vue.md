[Vue](https://vuejs.org/)は、ユーザーインターフェイスを構築するためのプログレッシブなフレームワークです。他の一枚岩のフレームワークとは異なり、Vueは段階的に採用可能な設計がなされています。コアライブラリはビューレイヤーにのみ焦点を当てており、他のライブラリや既存のプロジェクトと簡単に統合して使用することができます。一方で、現代的なツールとサポートライブラリと組み合わせることで、洗練されたシングルページアプリケーションを動かすこともできます。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、公開/購読モデルに基づいた**軽量IoTメッセージングプロトコル**です。このプロトコルは、一対多のメッセージ配布とアプリケーションの非結合を提供します。低い伝送消費とプロトコルデータ交換、最小化されたネットワークトラフィック、異なる配信ニーズに対応できる3つの異なるサービス品質レベルのメッセージがその主な利点です。

この記事では、VueプロジェクトでMQTTを使用する方法を主に紹介し、クライアントとMQTTブローカー間の接続、購読、メッセージ送信、購読解除などの機能を実装します。

> Vue 3アプリケーションでMQTT.jsを使用してMQTT接続を作成するには、[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue3.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue3.js)を参照してください。

## プロジェクトの初期化

### プロジェクトの作成

参考リンクは以下の通りです:

- [Vue CLIを使ってVueプロジェクトを作成する](https://cli.vuejs.org/guide/creating-a-project.html#vue-create)
- [Vue.jsを導入してVueプロジェクトを作成する](https://vuejs.org/v2/guide/installation.html)

例：

```shell
vue create vue-mqtt-test 
```

### MQTTクライアントライブラリのインストール

> 以下の方法2と3は、直接Vue.jsを導入するプロジェクトにより適しています。

1. コマンドラインからインストールする、npmまたはyarnのどちらかを使用

   ```shell
   npm install mqtt --save
   # or yarn
   yarn add mqtt
   ```

2. CDN経由でインポートする

   ```html
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
   ```

3. ローカルにダウンロードして、相対パスを使用してインポートする

   ```html
   <script src="/your/path/to/mqtt.min.js"></script>
   ```

## MQTTの使用

### MQTTブローカーへの接続

この記事では、EMQXが提供する[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。このサービスは、EMQXの[MQTT IoTクラウドプラットフォーム](https://www.emqx.com/ja/cloud)に基づいて作成されました。ブローカーへのアクセス情報は以下の通りです：

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- WebSocketポート: **8083**
- WebSocketセキュアポート: **8084**

接続にメインのコード：

```javascript
<script>
import mqtt from "mqtt";

export default {
  data() {
    return {
      connection: {
        protocol: "ws",
        host: "broker.emqx.io",
        // ws: 8083; wss: 8084
        port: 8083,
        endpoint: "/mqtt",
        // for more options, please refer to https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options
        clean: true,
        connectTimeout: 30 * 1000, // ms
        reconnectPeriod: 4000, // ms
        clientId: "emqx_vue_" + Math.random().toString(16).substring(2, 8),
        // auth
        username: "emqx_test",
        password: "emqx_test",
      },
      subscription: {
        topic: "topic/mqttx",
        qos: 0,
      },
      publish: {
        topic: "topic/browser",
        qos: 0,
        payload: '{ "msg": "Hello, I am browser." }',
      },
      receiveNews: "",
      qosList: [0, 1, 2],
      client: {
        connected: false,
      },
      subscribeSuccess: false,
      connecting: false,
      retryTimes: 0,
    };
  },

  methods: {
    initData() {
      this.client = {
        connected: false,
      };
      this.retryTimes = 0;
      this.connecting = false;
      this.subscribeSuccess = false;
    },
    handleOnReConnect() {
      this.retryTimes += 1;
      if (this.retryTimes > 5) {
        try {
          this.client.end();
          this.initData();
          this.$message.error("Connection maxReconnectTimes limit, stop retry");
        } catch (error) {
          this.$message.error(error.toString());
        }
      }
    },
    createConnection() {
      try {
        this.connecting = true;
        const { protocol, host, port, endpoint, ...options } = this.connection;
        const connectUrl = `${protocol}://${host}:${port}${endpoint}`;
        this.client = mqtt.connect(connectUrl, options);
        if (this.client.on) {
          this.client.on("connect", () => {
            this.connecting = false;
            console.log("Connection succeeded!");
          });
          this.client.on("reconnect", this.handleOnReConnect);
          this.client.on("error", (error) => {
            console.log("Connection failed", error);
          });
          this.client.on("message", (topic, message) => {
            this.receiveNews = this.receiveNews.concat(message);
            console.log(`Received message ${message} from topic ${topic}`);
          });
        }
      } catch (error) {
        this.connecting = false;
        console.log("mqtt.connect error", error);
      }
    },
  },
};
</script>
```

### トピックのサブスクライブ

```javascript
doSubscribe() {
  const { topic, qos } = this.subscription
  this.client.subscribe(topic, { qos }, (error, res) => {
    if (error) {
      console.log('Subscribe to topics error', error)
      return
    }
    this.subscribeSuccess = true
    console.log('Subscribe to topics res', res)
  })
}
```

### サブスクライブ解除

```javascript
doUnSubscribe() {
  const { topic } = this.subscription
  this.client.unsubscribe(topic, error => {
    if (error) {
      console.log('Unsubscribe error', error)
    }
  })
}
```

### メッセージの送信

```javascript
doPublish() {
  const { topic, qos, payload } = this.publish
  this.client.publish(topic, payload, { qos }, error => {
    if (error) {
      console.log('Publish error', error)
    }
  })
}
```

### 接続の切断

```javascript
destroyConnection() {
  if (this.client.connected) {
    try {
      this.client.end(false, () => {
        this.initData()
        console.log('Successfully disconnected!')
      })
    } catch (error) {
      console.log('Disconnect failed', error.toString())
    }
  }
}
```

## テスト

以下のような簡単なブラウザアプリケーションをVueで書きます。このアプリケーションには、接続の作成、トピックの購読、メッセージング、購読解除、切断などの機能があります。

完全なコード：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js%E3%80%82](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js)。 

![vueui.png](https://assets.emqx.com/images/b6563b0eb66eb51a2a02776889016a18.png)

[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を別のクライアントとして使用し、メッセージングをテストします。

![vuemqttx.png](https://assets.emqx.com/images/2013cbab1bdffcae69b817bfebb4a33f.png)

ブラウザ側でサブスクライブを解除し、MQTTXが2番目のメッセージを送信する前に行うと、その後のMQTTXからのメッセージはブラウザに届きません。

## まとめ

まとめると、VueプロジェクトでMQTT接続を作成し、クライアントとMQTTブローカー間での購読、メッセージの送受信、購読解除、切断を実装しました。

Vueは3つの最も人気のあるフロントエンドフレームの一つとして、ブラウザサイドで使用されるだけでなく、モバイルサイドでも使用されます。MQTTプロトコルと[MQTTクラウドサービス](https://www.emqx.com/ja/cloud)を組み合わせることで、カスタマーサービスのチャットシステムや、リアルタイムでIoTデバイス情報を監視する管理システムなど、多くの興味深いアプリケーションを開発することができます。

次に、EMQが提供する[MQTTプロトコルの易しい理解ガイド](https://www.emqx.com/ja/mqtt-guide)シリーズの記事をチェックして、MQTTプロトコルの特徴を学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めてみてください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
