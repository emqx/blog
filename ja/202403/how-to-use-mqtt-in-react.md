## はじめに

React（React.jsまたはReactJSとも呼ばれます）は、ユーザーインターフェイスやUIコンポーネントを構築するためのオープンソースのフロントエンドJavaScriptライブラリです。Facebookと個人開発者およびカンパニーのコミュニティによって維持されています。Reactは、シングルページアプリケーションやモバイルアプリケーションの開発における基盤として使用できます。ただし、ReactはデータをDOMにレンダリングすることにのみ関心があるため、Reactアプリケーションの作成には通常、状態管理やルーティングのための追加のライブラリが必要になります。ReduxやReact Routerは、そのようなライブラリの代表例です。

本記事では主に、ReactプロジェクトでMQTTを使用して、クライアントと[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)間の接続、サブスクライブ、メッセージング、アンサブスクライブなどを実装する方法を紹介します。

## プロジェクトの初期化

新しいReactプロジェクトを始めるには、適切なツールとフレームワークを選択する必要があります。Create React App（CRA）は新しいReactアプリケーションのブートストラップに広く使用されていましたが、エコシステムは進化しています。公式のReactドキュメントでは、Next.jsやRemixのようなより現代的なフレームワークを使用することが提案されています。

今後のアップデートでは、Next.jsやRemix.jsのようなフレームワークを使って[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)を構築するガイドを提供します。しかし、このブログではSPA（シングルページアプリケーション）のWebアプリを使用するユーザーのガイドに焦点を当てます。

### Viteを使用した新しいReactアプリケーションの作成

より高速な開発エクスペリエンスを求める開発者のために、Viteは現代的で効率的なセットアップを提供します。Viteを使用して新しいプロジェクトを開始する方法は以下の通りです。

- 基本的なReactプロジェクトの場合:

  ```shell
  npm create vite@latest react-mqtt-test --template react
  # Yarnを使用する場合
  yarn create vite react-mqtt-test --template react
  ```

- TypeScriptを使用する場合:

  ```shell
  npm create vite@latest react-mqtt-test --template react-ts
  # 必要なTypeScriptライブラリをインストール
  npm install --save typescript @types/node @types/react @types/react-dom @types/jest
  ```

### 従来の方法: Create React Appの使用

Create React Appは、シングルページアプリケーションを作成するためのオプションとして残っています:

```shell
npx create-react-app react-mqtt-test
# TypeScriptの場合
npx create-react-app react-mqtt-test --template typescript
```

### MQTTクライアントライブラリのインストール

ReactアプリケーションにMQTTを直接組み込むには、[MQTT.js](https://www.emqx.com/ja/blog/mqtt-js-tutorial)ライブラリをインストールすることをお勧めします。

```shell
npm install mqtt --save
# または
yarn add mqtt
```

この方法では、CDNを使用して素早くプロトタイプを作成したり、npm/yarnを使用してより安定した本番環境に適したアプリケーションを作成したりと、Reactプロジェクトへのmqttの統合に柔軟性を持たせることができます。

**CDN経由**

CDNを介してReactとMQTT.jsを統合したい場合は、HTMLに以下のスクリプトタグを含めることができます。

```html
<script src="<https://unpkg.com/mqtt/dist/mqtt.min.js>"></script>
```

## MQTTブローカーの準備

先に進む前に、通信およびテストに使用するMQTTブローカーを用意してください。EMQX Cloudの使用をお勧めします。

[EMQX Cloud](https://www.emqx.com/ja/cloud)は、完全に管理されたクラウドネイティブなMQTTサービスであり、大量のIoTデバイスに接続し、様々なデータベースおよびビジネスシステムと統合することができます。EMQX Cloudを使用すれば、わずか数分で開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行できるため、グローバルな可用性と高速な接続性を保証します。

<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

本記事では、プロセスを簡略化するために[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。

- サーバー: `broker.emqx.io`
- TCPポート: `1883`
- WebSocketポート: `8083`
- SSL/TLSポート: `8883`
- セキュアWebSocketポート: `8084`

## MQTTの使用

### MQTTブローカーへの接続

まず、MQTTクライアントのインスタンスを格納するために`client`ステートを定義します。これは`useState`フックによって管理されます。`mqttConnect`関数はこの接続を確立し、それに応じて接続状態を設定します。

```javascript
const [client, setClient] = useState(null);
const mqttConnect = (host, mqttOption) => {
  setConnectStatus('Connecting');
  setClient(mqtt.connect(host, mqttOption));
};

useEffect(() => {
  if (client) {
    console.log(client);
    client.on('connect', () => {
      setConnectStatus('Connected');
    });
    client.on('error', (err) => {
      console.error('Connection error: ', err);
      client.end();
    });
    client.on('reconnect', () => {
      setConnectStatus('Reconnecting');
    });
    client.on('message', (topic, message) => {
      const payload = { topic, message: message.toString() };
      setPayload(payload);
    });
  }
}, [client]);
```

### トピックへのサブスクライブ

`mqttSub`関数では、クライアントは1つ以上のトピックをサブスクライブできます。クライアントは、提供されたトピックとQoS（Quality of Service）パラメータを使用して、これらのトピックに対するメッセージを受信できます。

```javascript
const mqttSub = (subscription) => {
  if (client) {
    const { topic, qos } = subscription;
    client.subscribe(topic, { qos }, (error) => {
      if (error) {
        console.log('Subscribe to topics error', error);
        return;
      }
      setIsSub(true);
    });
  }
};
```

### アンサブスクライブ

`mqttUnSub`関数は、以前にサブスクライブしたトピックをアンサブスクライブするために使用します。アンサブスクライブが成功すると、クライアントはそのトピックのメッセージを受信しなくなります。

```javascript
const mqttUnSub = (subscription) => {
  if (client) {
    const { topic } = subscription;
    client.unsubscribe(topic, error => {
      if (error) {
        console.log('Unsubscribe error', error);
        return;
      }
      setIsSub(false);
    });
  }
};
```

### メッセージの発行

`mqttPublish`関数を使用すると、クライアントは指定されたトピックにメッセージを発行できます。メッセージの品質（QoS）とretainフラグを設定できます。

```javascript
const mqttPublish = (context) => {
  if (client) {
    const { topic, qos, payload } = context;
    client.publish(topic, payload, { qos }, error => {
      if (error) {
        console.log('Publish error: ', error);
      }
    });
  }
};
```

### 切断

最後に、`mqttDisconnect`関数は、クライアントとMQTTブローカーの接続を切断します。切断に成功すると、関連するリソースがクリーンアップされます。

```javascript
const mqttDisconnect = () => {
  if (client) {
    client.end(() => {
      setConnectStatus('Disconnected');
    });
  }
};
```

## テスト

接続の作成、トピックへのサブスクライブ、メッセージの送受信、アンサブスクライブ、切断の機能を備えたシンプルなブラウザアプリケーションを、Reactを使用して作成しました。

完全なプロジェクトのサンプルコード: [MQTT-Client-Examples/mqtt-client-React at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React) 。

![react mqtt page](https://assets.emqx.com/images/d1c51195c056f3b4afb267edaeb217f0.png)

もう一方のクライアントとして[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を使用し、メッセージの送受信をテストします。

![MQTTX](https://assets.emqx.com/images/621ba9544ea69f9ee7b24203846d0409.png)

MQTTXがブラウザ側からのメッセージを正常に受信できることがわかります。MQTTXを使用してトピックにメッセージを送信すると、それが確認できます。

![react mqtt test](https://assets.emqx.com/images/da008ae3544a83a3efa78266190ea364.png)

## Q&A

### React Nativeモバイルアプリ開発でMQTTを使用できますか？

はい、MQTTはリアルタイム通信のためにReact Nativeと統合できます。詳細な手順については、[React NativeでMQTTを使用する方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-react-native)をご覧ください。

### Reactを使用する場合、MQTTはWebSocketを介してのみ接続できますか？

はい、Webブラウザで実行されているReactアプリケーションの場合、MQTTの接続はWebSocketを介して行われます。これは、ブラウザの制限により直接のTCP接続を防ぐためです。WebSocketはこれらの制約に準拠しつつ、リアルタイム通信に互換性のあるソリューションです。ブローカーがWebSocket接続を受け入れるように設定されていることを確認することが不可欠であり、多くの場合、ホストURLに特定の`path`が必要です。

### ReactでMQTTフックを使用して、より良い状態管理を行うことは可能ですか？

はい、React公式のMQTTフックはありませんが、接続、サブスクライブ、パブリッシュ、メッセージ処理など、MQTTクライアントのロジックをカプセル化するカスタムフックを開発することができます。この方法により、コンポーネントのロジックが合理化され、アプリケーション全体の読みやすさと再利用性が向上します。

### Reactで「モジュールが見つかりません：「mqtt」を解決できません」を解決する方法は？

MQTT.jsがインストールされていることを確認してください（`npm install mqtt`または`yarn add mqtt`）。インポート文が正しいことを確認し、開発サーバーを再起動してください。

### Reactで「MQTT.jsとの"WebSocket接続に失敗しました"」エラーを修正する方法は？

ブローカーのURLが正しいこと（非保護の場合は`ws://`、保護された場合は`wss://`）、およびポートが開いていることを確認します。自己ホスト型のブローカーの場合、WebSocketサポートが有効で、ファイアウォールやネットワークの制限を考慮してアクセス可能であることを確認します。

### MQTT.jsはブラウザベースのReactアプリケーションで相互（双方向）SSL/TLS認証をサポートできますか？

いいえ、JavaScriptは接続用のクライアント証明書を指定できず、ブラウザがCA設定を制御するため、MQTT.jsはブラウザでの相互SSL/TLS認証をサポートできません。

参考：[MQTT.js GitHubのIssue #1515](https://github.com/mqttjs/MQTT.js/issues/1515)

## ReactにおけるMQTTの高度な使用方法

### カスタムフックを使用したReactでのMQTTの高度な使用方法

Reactアプリケーションでのmqttの統合を強化し、クリーンで再利用可能なコードを促進するために、トピックのサブスクライブやメッセージの発行などのMQTT操作にカスタムフックを活用できます。これらのフックの作成と使用方法について簡単に説明します。

**カスタムフック:** `useMQTTSubscribe`

このフックはサブスクライブのロジックを抽象化し、コンポーネントが[MQTTトピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)に簡単にサブスクライブし、受信メッセージを処理できるようにします。

```javascript
function useMQTTSubscribe(client, topic, onMessage) {
  useEffect(() => {
    if (!client || !client.connected) return;
    const handleMsg = (receivedTopic, message) => {
      if (receivedTopic === topic) {
        onMessage(message.toString());
      }
    };
    client.subscribe(topic);
    client.on('message', handleMsg);
    return () => {
      client.unsubscribe(topic);
      client.off('message', handleMsg);
    };
  }, [client, topic, onMessage]);
}
```

**カスタムフック:** `useMQTTPublish`

このフックは、メッセージ発行プロセスを簡素化し、クライアントが接続されている場合にメッセージが送信されるようにします。

```javascript
function useMQTTPublish(client) {
  const publish = (topic, message, options = {}) => {
    if (client && client.connected) {
      client.publish(topic, message, options);
    }
  };
  return publish;
}
```

### 使用例

#### トピックへのサブスクライブ

特定のトピックからのメッセージを表示するコンポーネント:

```javascript
const MessageDisplay = ({ client }) => {
  const [message, setMessage] = useState("");
  useMQTTSubscribe(client, "example/topic", setMessage);

  return <div>Latest message: {message}</div>;
};
```

#### トピックへの発行

ユーザー入力をトピックに発行するコンポーネント:

```javascript
const MessageSender = ({ client }) => {
  const [input, setInput] = useState("");
  const publish = useMQTTPublish(client);

  const sendMessage = () => {
    publish("example/topic", input);
    setInput(""); // 送信後に入力をクリア
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};
```

### 統合のヒント

- **クライアントの初期化**: MQTTクライアントがコンポーネントの外で初期化されていることを確認し、レンダリングのたびに再接続されないようにします。
- **接続状態**: MQTTクライアントの接続状態を管理・監視し、それに応じてUI要素を有効または無効にします。
- **エラー処理**: アプリケーションの信頼性を向上させるために、発行とサブスクライブの操作にエラー処理を実装します。

ReactアプリケーションでMQTT操作にカスタムフックを使用することで、MQTTの接続、サブスクライブ、メッセージを効率的に管理でき、コードがクリーンになり、ユーザーエクスペリエンスが向上します。

## まとめ

まとめると、Reactプロジェクトでのmqtt接続の作成を実装し、クライアントとMQTTブローカー間のサブスクライブ、メッセージの送受信、アンサブスクライブ、切断をシミュレートしました。

本記事ではReact v16.13.1を使用しているため、サンプルコードではHook Componentの機能を使用して説明しています。必要に応じて、完全なサンプルコードのClassMqttコンポーネントを参照して、Class Componentの機能をプロジェクトの構築に使用することもできます。

次に、EMQが提供する[わかりやすいMQTTプロトコルガイド](https://www.emqx.com/ja/mqtt-guide)シリーズの記事をチェックして、MQTTプロトコルの機能を学び、MQTTのより高度な応用を探究し、MQTTのアプリケーションとサービスの開発を始めることができます。

## リソース

- [VueでMQTTを使用する方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-vue)
- [AngularでMQTTを使用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [ElectronでMQTTを使用する方法](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [Node.jsでMQTTを使用する方法](https://www.emqx.com/ja/blog/how-to-use-mqtt-in-nodejs)
- [WebSocket経由でMQTTを使用するクイックスタートガイド](https://www.emqx.com/ja/blog/connect-to-mqtt-broker-with-websocket)



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
