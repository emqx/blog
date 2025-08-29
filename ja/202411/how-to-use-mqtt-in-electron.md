[Electron](https://www.electronjs.org/)はGitHubによって開発・メンテナンスされているオープンソースのソフトウェアフレームワークです。これはChromiumレンダリングエンジンとNode.jsランタイムを組み合わせることで、ウェブ技術を使用したデスクトップGUIアプリケーションの開発を可能にします。ElectronはAtom、GitHub Desktop、Light Table、Visual Studio Code、WordPress Desktopなどの注目すべきオープンソースプロジェクトの主要なGUIフレームワークです。

基本的なElectronは、`package.json`(メタデータ)、`main.js`(コード)、`index.html`(グラフィカルユーザーインターフェイス)の3つのファイルで構成されています。フレームワークはElectron実行ファイル(Windowsではelectron.exe、macOSではelectron.app、Linuxではelectron)によって提供されます。開発者はフラグを追加したり、アイコンをカスタマイズしたり、Electron実行ファイルの名前を変更または編集することができます。

この記事では、主にElectronプロジェクトでの[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)の使用方法について紹介し、シンプルなMQTTデスクトップクライアントを完成させ、クライアントと[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)間の接続、サブスクリプション、アンサブスクリプション、メッセージングなどの機能を実装します。

## プロジェクトの初期化

### 新しいプロジェクトの作成

新しいプロジェクトを構築する方法は多数ありますが、ここでは簡単にいくつかを紹介します:

- 手動で以下のように作成

  ```shell
  cd your-project
  
  npm init
  
  npm i -D electron@lates
  
  ```

  また、プロジェクトの構築手順は以下のドキュメントを参照してください。

  URL: https://www.electronjs.org/docs/tutorial/first-app

- 公式テンプレートプロジェクト `electron-qucik-start` を使用した高速開発。

  URL: [GitHub - electron/electron-quick-start: Clone to try a simple Electron app](https://github.com/electron/electron-quick-start) 

  ```shell
    # Clone this repository
    git clone https://github.com/electron/electron-quick-start
    # Go into the repository
    cd electron-quick-start
    # Install dependencies
    npm install
    # Run the app
    npm start
  ```

- テンプレートプロジェクト `electron-react-bolierplate` を使用した高速開発ビルドは、`React.js`を使用して開発できます。

  URL: [GitHub - electron-react-boilerplate/electron-react-boilerplate: A Foundation for Scalable Cross-Platform Apps](https://github.com/electron-react-boilerplate/electron-react-boilerplate) 

  ```shell
  git clone --depth 1 --single-branch https://github.com/electron-react-boilerplate/electron-react-boilerplate.git your-project-name
  cd your-project-name
  yarn
  ```

- `electron-vue` 経由のプロジェクトの高速開発ビルドは、 `vue-cli` ツールを使用したプロジェクトの初期化とともに行われ、`Vue.js` を使用して開発できます。

  URL: [GitHub - SimulatedGREG/electron-vue: An Electron & Vue.js quick start boilerplate with vue-cli scaffolding, common Vue plugins, electron-packager/electron-builder, unit/e2e testing, vue-devtools, and webpack.](https://github.com/SimulatedGREG/electron-vue) 

  ```shell
  # Install vue-cli and scaffold boilerplate
  npm install -g vue-cli
  vue init simulatedgreg/electron-vue my-project
  
  # Install dependencies and run your app
  cd my-project
  yarn # or npm install
  yarn run dev # or npm run dev
  ```

この記事では、プロジェクトを素早く構築するために、公式のelectron quick startプロジェクトテンプレートを使用してプロジェクトを初期化します。

### 依存関係のインストール

コマンドライン経由でインストール

```shell
npm install mqtt --save
```

依存関係がインストールされたら、デバッグのためにコンソールを開く必要がある場合は、`main.js` のコードを変更し、`win.webContents.openDevTools()`をアンコメントする必要があります。

```javascript
// Open the DevTools.
mainWindow.webContents.openDevTools()
```

この場合、フロントエンドビルダーを使用してフロントエンドページをパッケージ化しない限り、ローカルにインストールされた `MQTT.js` モジュールを `renderer.js` に直接読み込むことはできません。上記のコードを変更することに加えて、この問題を解決するための他の2つの方法があります。

1. `webPreferences` で `nodeIntegration` を true に設定できます。このプロパティが存在する場合、`webview` はノード統合を持ち、 `require` や `process` などのノードAPIにアクセスして低レベルのシステムリソースにアクセスできます。ノード統合はデフォルトで無効になっています。

   ```javascript
   const mainWindow = new BrowserWindow({
     width: 800,
     height: 600,
     webPreferences: {
       nodeIntegration: true,
       preload: path.join(__dirname, 'preload.js'),
     },
   })
   ```

2. [MQTT.js](https://www.emqx.com/ja/blog/mqtt-js-tutorial) モジュールは、preload.jsでインポートできます。ノード統合がない場合でも、このスクリプトは引き続きすべてのNode APIにアクセスできます。ただし、このスクリプトの実行が完了すると、Nodeを介してインジェクトされたグローバルオブジェクトは削除されます。

3. メインプロセスで [MQTT.js](https://www.emqx.com/ja/blog/mqtt-js-tutorial) モジュールをインポートし、接続します。Electronでは、プロセスは開発者定義の「チャネル」を介してメッセージを渡すことで通信します。これは、 `ipcMain` と `ipcRenderer` モジュールを使用して実現されます。これらのチャネルは **任意の** (名前は何でも付けられます) ものと **双方向の** (両方のモジュールで同じチャネル名を使用できます) ものです。 使用例は、[IPC チュートリアル](https://www.electronjs.org/docs/latest/tutorial/ipc)をご覧ください。

   たとえば、メインプロセスではipcMainが接続操作をリッスンします。 ユーザーが接続をクリックすると、レンダリングプロセスで収集された対応する構成情報がipcRendererを介してメインプロセスに転送され、接続が行われます。

   - メインプロセスでレンダリングプロセスから送信された接続データを受信し、MQTT接続を実行

   ```javascript
   // main.js
   ipcMain.on('onConnect', (event, connectUrl, connectOpt) => {
     client = mqtt.connect(connectUrl, connectOpt)
     client.on('connect', () => {
       console.log('Client connected:' + options.clientId)
     })
     client.on('message', (topic, message) => {
       console.log(`${message.toString()}\nOn topic: ${topic}`)
     })
   })
   ```

   

   - レンダリングプロセスで接続をクリックし、ページから接続データを取得してメインプロセスに送信

   ```javascript
   // render.js
   function onConnect() {
     const { host, port, clientId, username, password } = connection
     const connectUrl = `mqtt://${host.value}:${port.value}`
     const options = {
       keepalive: 30,
       protocolId: 'MQTT',
       clean: true,
       reconnectPeriod: 1000,
       connectTimeout: 30 * 1000,
       rejectUnauthorized: false,
       clientId,
       username,
       password,
     }
     console.log('connecting mqtt client')
     window.electronAPI.onConnect(connectUrl, options)
   }
   ```

   - preload.jsでは、プロセス間IPCコミュニケーションのためのAPIメソッドが実装され、チャネルが確立されます。

   ```javascript
   // preload.js
   contextBridge.exposeInMainWorld('electronAPI', {
     onConnect: (data) => ipcRenderer.send('onConnect', data),
   })
   
   ```

## MQTTの使用

### MQTTブローカーへの接続

この記事では、EMQXが提供する[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。このサービスは、EMQXの[MQTT IoTクラウドプラットフォーム](https://www.emqx.com/ja/cloud)に基づいて作成されました。ブローカーへのアクセスに関する情報は以下のとおりです。

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- Websocketポート: **8083**

より直感的に説明するために、例の主な接続コードはrenderer.jsファイルに記述します。 セキュリティを考慮して、インストールされたMQTTモジュールは、Node.js APIのrequireメソッドを介してpreload.jsファイルで読み込まれます(上記の方法2を使用)。 また、これによりグローバルwindowオブジェクトにインジェクトされます。

> **注:** [コンテキスト分離(contextIsolation)](https://www.electronjs.org/docs/latest/tutorial/context-isolation) はElectron 12以降、デフォルトで有効になっています。プリロードスクリプトは、アタッチされているレンダラと `window` グローバルを共有しますが、 `contextIsolation` のデフォルト設定のため、プリロードスクリプトから `window` に直接変数をアタッチすることはできません。

したがって、これを閉じるためにwebPreferencesで `contextIsolation: false` を設定する必要があります。

```javascript
const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false; // Version 12.0.0 above are enabled by default
    }
  })
```

これにより、読み込んだモジュールに `renderer.js` から直接アクセスできます。

- MQTTモジュールのインポート

```javascript
// preload.js
const mqtt = require('mqtt')
window.mqtt = mqtt
```

- MQTTモジュールの設定とテスト

```javascript
// renderer.js
const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'mqtt://broker.emqx.io:1883'

const options = {
  keepalive: 30,
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
    retain: false,
  },
  rejectUnauthorized: false,
}

// Information about the mqtt module is available
console.log(mqtt)

console.log('connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})

client.on('reconnect', () => {
  console.log('Reconnecting...')
})

client.on('connect', () => {
  console.log('Client connected:' + clientId)
  client.subscribe('testtopic/electron', {
    qos: 0,
  })
  client.publish('testtopic/electron', 'Electron connection demo...!', {
    qos: 0,
    retain: false,
  })
})

client.on('message', (topic, message, packet) => {
  console.log(
    'Received Message: ' + message.toString() + '\nOn topic: ' + topic
  )
})
```

上記のコードを記述してプロジェクトを実行すると、コンソールに次の出力が表示されます。

![electronconsole.png](https://assets.emqx.com/images/eb708f312630c441bd6f2453af36372e.png)

MQTTモジュールは正常に機能しています。 モジュールの設定が完了したら、MQTT接続に必要な構成を手動で入力するためのシンプルなUIインターフェースを記述し、接続ボタンをクリックしてMQTTサーバーに接続したり、接続を切断したり、トピックをサブスクライブしたり、メッセージの送受信を行ったりできます。

**アプリケーションのインターフェース**

![electronui.png](https://assets.emqx.com/images/f628816b73b31e6d3c695cd39c439ca6.png)

完全なコードはこちらで入手できます: [MQTT-Client-Examples/mqtt-client-Electron at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron) 

### キーコード

#### 接続設定

```javascript
let client = null

const options = {
  keepalive: 30,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false,
  },
}

function onConnect() {
  const { host, port, clientId, username, password } = connection
  const connectUrl = `mqtt://${host.value}:${port.value}`
  options.clientId =
    clientId.value || `mqttjs_${Math.random().toString(16).substr(2, 8)}`
  options.username = username.value
  options.password = password.value
  console.log('connecting mqtt client')
  client = mqtt.connect(connectUrl, options)
  client.on('error', (err) => {
    console.error('Connection error: ', err)
    client.end()
  })
  client.on('reconnect', () => {
    console.log('Reconnecting...')
  })
  client.on('connect', () => {
    console.log('Client connected:' + options.clientId)
    connectBtn.innerText = 'Connected'
  })
}
```

#### トピックをサブスクライブ

```javascript
function onSub() {
  if (client.connected) {
    const { topic, qos } = subscriber
    client.subscribe(
      topic.value,
      { qos: parseInt(qos.value, 10) },
      (error, res) => {
        if (error) {
          console.error('Subscribe error: ', error)
        } else {
          console.log('Subscribed: ', res)
        }
      }
    )
  }
}
```

#### アンサブスクライブ

```javascript
function onUnsub() {
  if (client.connected) {
    const { topic } = subscriber
    client.unsubscribe(topic.value, (error) => {
      if (error) {
        console.error('Unsubscribe error: ', error)
      } else {
        console.log('Unsubscribed: ', topic.value)
      }
    })
  }
}
```

#### メッセージのパブリッシュ

```javascript
function onSend() {
  if (client.connected) {
    const { topic, qos, payload } = publisher
    client.publish(topic.value, payload.value, {
      qos: parseInt(qos.value, 10),
      retain: false,
    })
  }
}
```

#### メッセージの受信

```javascript
// In the onConnect function
client.on('message', (topic, message) => {
  const msg = document.createElement('div')
  msg.setAttribute('class', 'message-body')
  msg.innerText = `${message.toString()}\nOn topic: ${topic}`
  document.getElementById('article').appendChild(msg)
})
```

#### 切断

```javascript
function onDisconnect() {
  if (client.connected) {
    client.end()
    client.on('close', () => {
      connectBtn.innerText = 'Connect'
      console.log(options.clientId + ' disconnected')
    })
  }
}
```

### クライアントのテスト

この時点で、[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を使用して、クライアントとのメッセージ送受信をテストします。MQTTXもElectronで記述されています。

MQTTXを使用してクライアントにメッセージを送信すると、メッセージが適切に受信されていることがわかります。

![electronmessage.png](https://assets.emqx.com/images/bfb62b9f23f6836627d8e129d38b9160.png)

自分で記述したクライアントを使用してMQTTXにメッセージを送信すると、今度はMQTTXもメッセージを適切に受信していることが確認できます。

![mqttx.png](https://assets.emqx.com/images/cc97fe533fcce20765530970d7696f58.png)

## まとめ

これまでに、Electronを使用してシンプルなMQTTデスクトップクライアントを作成し、クライアントとMQTTブローカー間の接続、メッセージング、アンサブスクライブ、切断のシナリオをシミュレートしました。また、Electronプロジェクトにはブラウザ環境とNode.js環境の両方が含まれているため、上記のコードの接続プロトコルとポート番号を変更することで、ブラウザのWebSocket APIを使用してWebSocket経由のMQTT接続を実装できることにも注意が必要です。

## リソース

- [VueでのMQTTの使用方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-vue)
- [ReactでのMQTTの使用方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-react)
- [AngularでのMQTTの使用方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [Node.jsでのMQTTの使用方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-nodejs)
- [WebSocketを使用したMQTTのクイックスタートガイド](https://www.emqx.com/ja/blog/connect-to-mqtt-broker-with-websocket)



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
