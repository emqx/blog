React Nativeは、Facebookのオープンソースのクロスプラットフォームなモバイルアプリ開発フレームワークで、ネイティブモバイルアプリケーションプラットフォームのためのReactの派生物です。React Nativeは、ウェブフロントエンド開発に精通している技術スタッフが、最小限の学習曲線でモバイルアプリケーション開発を始めることができるように、JavascriptとHTML JSX、CSSを使用してモバイルアプリケーションを開発します。 React Nativeはまた、ネイティブアプリケーションに近いパフォーマンスとエクスペリエンスを提供します。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく**軽量なIoTメッセージングプロトコル**であり、厳しく制約されたハードウェアデバイスと低帯域幅、高レイテンシーネットワーク上で安定した転送を可能にします。 簡単な実装、QoSサポート、小さいメッセージサイズなどにより、IoT業界で広く使用されています。

この記事では、クライアントから[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)へのメッセージの送受信のためのReact NativeプロジェクトでのMQTTの使用に焦点を当てています。

## 新しいReact Nativeプロジェクトの作成

ここでは、macOS開発環境とiOSアプリケーションプラットフォームでRNMQTTDemoという名前のプロジェクトを作成する例を示します。 詳細は、[開発環境の設定](https://reactnative.dev/docs/environment-setup)を参照してください。

プロジェクトが作成された後、プロジェクトルート環境で次のコマンドを実行して、必要な依存関係をプロジェクトにインストールします。

```shell
npm install @react-native-async-storage/async-storage @rneui/base @rneui/themed
```

## MQTTクライアントモジュールのインストール

```shell
npm install react_native_mqtt
```

react_native_mqttは、iOSとAndroidをサポートするReact Nativeプロジェクトに使用されるMQTTクライアントモジュールです。

## MQTTクライアントモジュールの使用方法

**MQTTサーバーへの接続**

EMQXの[無料のパブリックMQTTサーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。これは、EMQXの[MQTTクラウド](https://www.emqx.com/ja/cloud)に基づいています。 サーバーアクセス情報は以下のとおりです。

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- Websocketポート: **8083**

**クライアントインスタンスの作成**

```javascript
init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  sync : {}
});
const options = {
  host: 'broker.emqx.io',
  port: 8083,
  path: '/testTopic',
  id: 'id_' + parseInt(Math.random()*100000)
};
client = new Paho.MQTT.Client(options.host, options.port, options.path);
```

#### MQTTサーバーへの接続

```javascript
  connect = () => {
    this.setState(
      { status: 'isFetching' },
      () => {
        client.connect({
          onSuccess: this.onConnect,
          useSSL: false,
          timeout: 3,
          onFailure: this.onFailure
        });
      }
    );
  }
```

#### サブスクライブ

```javascript
  subscribeTopic = () => {
    this.setState(
      { subscribedTopic: this.state.topic },
      () => {
        client.subscribe(this.state.subscribedTopic, { qos: 0 });
      }
    );
  }
```

#### パブリッシュ

```javascript
  sendMessage = () =>{
    var message = new Paho.MQTT.Message(options.id + ':' + this.state.message);
    message.destinationName = this.state.subscribedTopic;
    client.send(message);
  }
```

#### アンサブスクライブ

```javascript
  unSubscribeTopic = () => {
    client.unsubscribe(this.state.subscribedTopic);
    this.setState({ subscribedTopic: '' });
  }
```

### プロジェクトの実行

完全なRNMQTTDemoプロジェクトは、[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React-Native](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React-Native)  にあります。

プロジェクトのルート環境で、2つの新しいターミナルウィンドウを作成し、次のコマンドを実行します。

```shell
npx react-native start
npx react-native run-ios
```

すると、iOSエミュレーターでアプリケーションが実行されます。トップにクライアントIDが表示されます。

![MQTT React Native](https://assets.emqx.com/images/bbdb1456750727915df96cb60d4f4d0a.png)

## MQTT接続テスト

[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を使用して、関連するテストを実行します。 react-native-demoという名前の接続を作成し、すべての構成項目でデフォルト値を使用し、接続に成功した後に、トピック名`testTopic`でサブスクリプションを追加するために、接続ボタンをクリックします。

![MQTT Client - MQTTX](https://assets.emqx.com/images/b5953d65971448432bd25f305b410fb3.png)

#### 接続

APPのCONNECTボタンをクリックすると、インターフェースが次のように表示されます。 接続に成功すると、上部のClientID行の内容が緑色に変わり、MQTTサーバーに正常に接続されたことを示します。

![React Native connect MQTT](https://assets.emqx.com/images/1dc2b1675ae2a035048a9412600b0f97.png)

#### サブスクライブ

サブスクライブしたいトピックを入力します。ここでは、testTopicを例として使用します。 次に、SUBSCRIBEボタンをクリックします。 サブスクリプション後のインターフェースは、次のように表示されます。

 ![React Native MQTT subscribe](https://assets.emqx.com/images/01f7c6408f82dd04dcbdba47d3614c33.png)

#### パブリッシュ

公開するメッセージの内容を入力し、入力が終わったらPUBLISHボタンをクリックします。 現在サブスクライブされているトピックで受信したメッセージが下部にリストされ、黒背景のメッセージは現在のクライアントによって送信されたものです。 現在のクライアントのIDはid_67485で、インターフェースは次のように表示されます。

![React Native MQTT publish](https://assets.emqx.com/images/20159b246e15ba5ef5a2b24fa85f75e0.png)

同時に、MQTTXのreact-native-demo接続のもとで、`testTopic`トピックにいくつかのメッセージを公開します。 クライアントID id_67458によってトピックに公開されたメッセージも表示されます。

![MQTT Client - MQTTX](https://assets.emqx.com/images/8be70d496c3332a2481dde78a9962087.png)

#### アンサブスクライブ

APPのUNSCRIBEボタンをクリックします。その後、`{ "msg": "hello test" }`をtestTopicトピックにMQTTXで投稿すると、次のように表示されます。

![MQTT Client - MQTTX](https://assets.emqx.com/images/d3ad89861b5683f3a9c0ca0da1354f4f.png)

testTopicトピックからアンサブスクライブすると、このトピックのMQTTXからのメッセージは受信されません `{ "msg": "hello test" }`。

![React Native MQTT unsubscribe](https://assets.emqx.com/images/9dedf4b4b26b55e4c90d835741bcba07.png)

## まとめ

ここまでで、React Nativeを使用してiOSプラットフォーム上にMQTTアプリを構築し、クライアントをMQTTサーバーに接続し、トピックをサブスクライブし、メッセージの送受信を実装し、サブスクライブを解除する機能を実装しました。

React Nativeを使用することで、開発者は標準のiOSプラットフォームコンポーネントを使用して、ネイティブアプリとほぼ同等のパフォーマンスを発揮するアプリを開発できます。 シームレスなクロスプラットフォームにより、チームは開発中の変更を保存するだけでより速く作業でき、iOSシミュレーターでの実際の結果が示したとおりです。 効率的なネイティブに近いパフォーマンス、ホットリローディング、広範なコミュニティのサポートが、多くのモバイルアプリ開発者にとってReact Nativeを最良の選択肢にしています。 React NativeとMQTTプロトコル、MQTTクラウドサービスを組み合わせることで、ユーザーはさまざまな興味深く革新的なアプリも開発できます。

次に、EMQXが提供する[MQTTプロトコルのわかりやすいガイド](https://www.emqx.com/ja/mqtt-guide)の記事シリーズをチェックして、MQTTプロトコルの機能を学び、MQTTのより高度なアプリケーションを探索し、MQTTアプリケーションとサービスの開発を開始してください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
