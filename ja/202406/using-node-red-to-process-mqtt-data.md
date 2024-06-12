## Node-REDとは？

Node-REDは、ハードウェアデバイス、API、オンラインサービスをつなぐためのプログラミングツールです。さまざまなノードを使ってフローを作成できるブラウザベースのエディタを提供しています。フローは1クリックでランタイムにデプロイできます。

Node-REDは、データ入力用の `mqtt-in` ノードとデータ出力用の `mqtt-out` ノードでMQTTプロトコルをサポートしています。

**Node-REDの主な特長：**

- **フローベースのプログラミング：** ノードを視覚的に配線することでアプリケーションを作成できます。
- **幅広いノード：** 様々な入力、出力、処理タスク用のノードが含まれています。
- **メッセージパッシング：** ノードはワイヤに沿ってメッセージを渡すことで通信します。
- **ブラウザベースのエディタ：** フローの構築とデプロイに使いやすいインターフェイスです。
- **拡張性：** カスタムノードを作成して機能を拡張できます。
- **ソーシャル開発：** JSONベースのフローにより、オンラインフローライブラリを通じて簡単にインポート、エクスポート、共有できます。

## MQTTとは？

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) は、リソース制約のあるデバイスや低帯域、高遅延、または信頼性の低いネットワークのための、パブリッシュ・サブスクライブ型の軽量メッセージングプロトコルです。IoT(モノのインターネット)アプリケーションで広く使用されており、センサー、アクチュエータ、その他のデバイス間の効率的な通信を提供します。

MQTTを使用するには、中央のブローカーが必要です。例えば、[EMQX](https://github.com/emqx/emqx)は、確実なメッセージ配信とシステムの効率的なスケーリングを保証する機能を持つブローカーとして考えられます。

![MQTT PUB SUB](https://assets.emqx.com/images/f9a84128b10250dcd609b1748c5ef4dd.png)

## Node-REDでMQTTを使う理由

MQTTとNode-REDを組み合わせることで、特にIoTやリアルタイムデータ処理などの様々なアプリケーションに強力なソリューションを提供します。その理由は以下の通りです。

1. **効率的なデータ処理：** Node-REDはMQTTメッセージをリアルタイムで処理するため、センサーデータなどの入力に即座に対応できます。
2. **使いやすさ：** Node-REDの視覚的なプログラミングインターフェースにより、高度なコーディング知識がなくても複雑なワークフローの作成とデプロイが容易になります。
3. **IoTに最適化：** Node-REDの柔軟性と幅広いノードライブラリにより、様々なIoTデバイスとのシームレスな接続とデータ処理が可能です。MQTTは、[Quality of Service (QoS)](https://www.emqx.com/ja/blog/introduction-to-mqtt-qos) レベル、[保持メッセージ](https://www.emqx.com/en/blog/mqtt5-features-retain-message)、[last will (LWT)](https://www.emqx.com/ja/blog/use-of-mqtt-will-message)などの機能を使って、低帯域、高遅延、または信頼性の低いネットワークでの効率的な通信を保証します。
4. **汎用性：** Node-REDはIoTに限定されません。ホームオートメーション、産業オートメーション、データ可視化、クラウドサービスとの統合などにも役立ちます。
5. **スケーラビリティ：** Node-REDとMQTTは、多数のデバイスと大量のデータを効率的に処理し、スケーラブルなソリューションをサポートします。

Node-REDの視覚的なフローベースの開発環境とMQTTの堅牢な機能と軽量性を組み合わせることで、様々な領域でスケーラブルで信頼性が高く効率的なアプリケーションを迅速に構築できます。

## Node-REDのインストール

Node-REDは、PCやRaspberry Piなどのデバイス、クラウドサーバーにインストールでき、素早くインストールして使用できます。インストールの一般的な方法は2つあります。

`npm` を使ってグローバルにインストールする：

```shell
npm install -g --unsafe-perm node-red
```

`Docker` を使ってインストールする：

```shell
docker run -it -p 1880:1880 --name mynodered nodered/node-red  
```

## Node-REDの環境起動

npmでグローバルインストールした場合、インストールが成功したとプロンプトが表示されたら、node-redコマンドをグローバルに実行するだけで、すぐにNode-REDを起動できます。

DockerでもnpmでもNode-REDの起動に成功すると、ブラウザを開いて現在のアドレスに1880ポート番号を加えるだけで、Node-REDのブラウザエディタページを開くことができます。例えばローカルで実行している場合は、ブラウザを開いて `http://127.0.0.1:1880` と入力します。次の図のようなページが表示されたら、Node-REDが正常に起動したことを意味します。

![Node-RED](https://assets.emqx.com/images/cd66e004a35d9588c000d3f7e21ab5c2.png)

## Node-REDでのMQTTの使用

このガイドでは、EMQが提供する[EMQX ](https://www.emqx.com/ja/products/emqx)プラットフォームで構築された[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を利用します。サーバーのアクセス詳細は以下の通りです。

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**
- WebSocket Port: 8083
- SSL/TLS Port: 8883
- Secure WebSocket Port: 8084

この記事では、Node-REDでのMQTTを2つのパートで紹介します。基本的なパートではMQTTノードの設定と[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)への接続を、応用的なパートではデータ処理に焦点を当てています。

### 基本パート: MQTTノードの設定とMQTTブローカーへの接続

まず、ブラウザで `http://host:1880` を開き、デフォルトの `Flow 1` を作成します。次に、以下の手順を実行します。

#### 1. サブスクリプションノードの設定: Message In

1.1. **MQTT-inノードの追加:** パレットから `mqtt-in` ノードを中央のキャンバスにドラッグし、ダブルクリックして設定ページを開きます。

1.2. **MQTTブローカーの設定:** "Server" フィールドの横にある編集ボタンをクリックして新しいMQTTブローカーを追加し、ブローカーのアドレス `broker.emqx.io` やその他の接続詳細を入力し、Addをクリックしてブローカーの設定を保存します。

![Configure MQTT Broker](https://assets.emqx.com/images/f8fa66022aa1f0491b177e84a4245b07.png)

1.3. **トピックのサブスクライブ:** サブスクライブするトピックを入力します(例: `test/node_red/in`)。希望のQoSレベルを選択し、Doneをクリックしてノードの設定を保存します。

 ![Subscribe to a Topic](https://assets.emqx.com/images/118fb4eeca1cb5878feaef57aa9051e4.png)

#### 2. パブリッシュノードの設定: Message Out

2.1. **MQTT-outノードの追加:** `mqtt-out` ノードを中央のキャンバスにドラッグし、ノードをダブルクリックして設定ページを開きます。

2.2. **MQTTブローカーの設定:** 前に設定したMQTTブローカーが選択されていることを確認します。

2.3. **トピックへのパブリッシュ:** パブリッシュするトピックを入力します(例: `test/node_red/out`)。希望のQoSレベルを選択し、メッセージを保持するかどうかを設定し、Doneをクリックしてノードの設定を保存します。

![Publish to a Topic](https://assets.emqx.com/images/e88d164bd19825d95579dea943b6570b.png)

#### 3. デプロイとテスト

3.1. **ノードの接続:** キャンバス上で `mqtt-in` ノードを `mqtt-out` ノードに接続し、右上のDeployボタンをクリックしてフローをデプロイします。

![Connect Nodes](https://assets.emqx.com/images/32a9d4ac3509a86ae3b2c53bf9c9f6d0.png)

3.2. **接続の確認:** デプロイ後、各ノードの下に "connected" というステータスが表示され、MQTTブローカーへの接続が成功したことを示します。

3.3. **MQTTXクライアントでのテスト:** [MQTTX](https://mqttx.app/ja)を[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)として使用してセットアップをテストします。test/node_red/inトピックにメッセージをパブリッシュし、test/node_red/outトピックをサブスクライブして、メッセージが受信されることを確認します。

![Test with MQTTX Client](https://assets.emqx.com/images/ea54db1af038429058dce11a315e6410.png)

以上の手順で、Node-REDでMQTTノードを設定し、メッセージの受信と送信を処理できるようになりました。次に、受信データの処理についてのより高度なチュートリアルに進みます。

### 応用パート: MQTTデータの処理

#### 1. データアクセス

1.1. **JSONノードの追加:** JSONノードをキャンバスにドラッグ＆ドロップし、ダブルクリックして設定ページを開きます。

1.2. **JSON変換の設定:** アクションを "Always Convert to JavaScript Object" に設定し、受信メッセージがJSON形式に変換されるようにします。

1.3. **ノードの接続:** JSONノードを `mqtt-in` ノードに接続します。

![Connect Nodes](https://assets.emqx.com/images/2ac771a50e8247483530e0435631e8e1.png)

#### 2. データフィルタリング

2.1. **フィルターノードの追加:** フィルターノードをキャンバスにドラッグ＆ドロップし、ダブルクリックして設定ページを開きます。

2.2. **フィルターのルール設定:** モードを "block unless value changes" に設定し、プロパティを `msg.payload.temperature` に設定して、温度値に基づいてメッセージをフィルタリングします。

2.3. **ノードの接続:** フィルターノードをJSONノードに接続します。

![Connect the filter node to the JSON node](https://assets.emqx.com/images/41175ed585059d2141d46cde5eeeb753.png)

#### 3. テンプレートの使用

3.1. **テンプレートノードの追加:** テンプレートノードをキャンバスにドラッグ＆ドロップし、ダブルクリックして設定ページを開きます。

3.2. **テンプレートの設定:** テンプレートの内容を入力し、フィルタリングされたデータをフォーマットします。

3.3. **オプションのステップ:** 直接出力する場合は、テンプレートノードを追加せずにスキップできます。

![Optional Step](https://assets.emqx.com/images/9fdd854b48233c53ad13dfe91eca084d.png)

#### 4. 処理したデータの送信

4.1. **MQTT-outノードの追加:** `mqtt-out` ノードをキャンバスにドラッグ＆ドロップし、ダブルクリックして設定ページを開きます。

4.2. **MQTTブローカーの設定:** 前に設定したMQTTブローカーが選択されていることを確認します。

4.3. **トピックの設定:** 処理したデータをパブリッシュするトピックを入力します(例: `test/node_red/out`)。希望のQoSレベルを選択します。

4.4. **ノードの接続:** MQTT-outノードをテンプレートノードに接続します。

![Connect the MQTT-out node to the template node](https://assets.emqx.com/images/4c0918593a74410bdfadc874468215cf.png)

#### 5. デプロイとテスト

5.1. **フローのデプロイ:** 右上のDeployボタンをクリックしてフローをデプロイします。

5.2. **MQTTXクライアントでのテスト:**

- `test/node_red/in` トピックにメッセージをパブリッシュし、Node-REDがデータを受信できるようにします。
- `test/node_red/out` トピックをサブスクライブし、設定したテンプレートに従って処理されたメッセージが受信されることを確認します。
- Node-REDのフィルタリングロジックを検証し、同じメッセージを複数回送信しても受信されないことを確認します。温度値が変更された場合は、変更を示す新しいメッセージを受信するはずです。

![Test with MQTTX Client](https://assets.emqx.com/images/c9af327ef1496f6e630c26fb84f766f0.png)

以上の手順で、Node-REDでMQTTデータを処理・フィルタリングし、処理したデータをMQTTで送信するように設定できました。

## まとめ

これで、Node-REDを使ってMQTTクラウドサービスとのインストールと接続、MQTTメッセージデータのフィルタリングと処理、最終的に処理したデータメッセージの送信までの一連の流れが完了しました。Node-REDのUIを使って一般的なビジネスロジックを記述することで、非専門の開発者でも取り組みやすい敷居の低さを実現しています。ユーザーは、視覚的なツールを使って単純なノードをつなぐだけで、複雑な実行タスクを素早く作成できます。これは、特にIoTアプリケーションのシナリオに役立ちます。

次に、EMQが提供する[The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/ja/mqtt-guide)シリーズの記事をチェックして、MQTTプロトコルの機能について学び、MQTTのより高度な応用例を探り、MQTTアプリケーションとサービス開発を始めることができます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
