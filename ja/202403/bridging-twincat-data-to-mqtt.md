このブログでは、TwinCATデータをMQTTにブリッジングする包括的なガイドを提供します。TwinCATからデータを収集し、収集したデータをEMQXにアップロードし、MQTTXを使用してデータを表示します。

## TwinCATからMQTTへのブリッジングのアーキテクチャ

![The Architecture of TwinCAT to MQTT Bridging](https://assets.emqx.com/images/f7b81bd0ef7ed7c4661b4a388f681b37.png)

### TwinCATをMQTTに変換するためのNeuronEX

[NeuronEX](https://neugates.io/)は、産業用IoTゲートウェイソフトウェアであり、産業用デバイスに重要なIoT接続機能を提供します。NeuronEXはリソースの最小限の利用で、標準または専用のプロトコルを介してさまざまな産業用デバイスと通信し、[工業用IoTプラットフォーム](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions)に複数のデバイス接続を実現します。

NeuronEXは、最初からMQTTをその通信プロトコルの1つとしてサポートしています。NeuronEX [MQTTプラグイン](https://neugates.io/docs/en/latest/configuration/north-apps/mqtt/overview.html)を使用すると、デバイスとクラウド間のMQTT通信を素早く構築できます。

NeuronEXは、バージョン2.2.0から[Beckhoff ADSプラグイン](https://neugates.io/docs/en/latest/configuration/south-devices/ads/ads.html)を提供しています。NeuronEX Beckhoff ADSプラグインは、TCP上でADSプロトコルを実装しています。これにより、[Beckhoff TwinCAT](https://www.beckhoff.com/en-us/products/automation/twincat/#stage-special-item-s320986-2_t0) PLCとの通信をサポートし、NeuronEXの接続能力をさらに豊かにし、ユーザーのニーズを解決します。

Beckhoff ADSプラグインを使用すると、ユーザーはTwinCAT PLCから簡単にデータを収集できます。MQTTプラグインと組み合わせることで、収集したデータを[EMQXプラットフォーム](https://www.emqx.com/ja/products/emqx)などの産業用IoTプラットフォームにプッシュしたり、TwinCAT PLCにメッセージを公開してライト、モーター、およびその他の機器のオン/オフなどのデバイスアクションをトリガーすることができます。

### MQTTメッセージの処理にはEMQXを使用します

[EMQX](https://www.emqx.io/ja)は、高性能でスケーラブルな世界最先端のオープンソース分散型IoT [MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)です。EMQXは、大量のIoTデバイスに効率的で信頼性の高い接続を提供し、メッセージとイベントフローデータの高性能なリアルタイム移動と処理を可能にし、ユーザーが迅速に重要なビジネス向けのIoTプラットフォームとアプリケーションを構築できるよう支援します。

EMQXはブリッジングアーキテクチャのブローカーコンポーネントであり、NeuronEXはTwinCAT PLCからデータを収集し、データをMQTTメッセージとしてブローカーに転送します。NeuronEXからMQTTメッセージを受信した後、EMQXはデータを転送したり、さらなる処理を行ったりします。

EMQXには、SQLベースの[ルールエンジン](https://www.emqx.com/en/solutions/mqtt-data-processing)やデータ統合などの豊富でパワフルな機能セットがあり、リアルタイムでIoTデータを抽出し、フィルタリング、豊富にするためのもので、データ統合を使用してEMQXをデータベースなどの外部データシステムに接続することができます。

## NeuronEXを使用したTwinCATからMQTTへのブリッジング

ここでは、ローカルエリアネットワークに接続された2つのPCを使用します。1つはEMQX、MQTTX、およびNeuronEXをインストールするためのLinuxマシンで、もう1つはTwinCAT 3がインストールされたWindowsマシンです。

|                          | PC 1                  | PC 2              |
| :----------------------- | :-------------------- | :---------------- |
| オペレーティングシステム | Linux                 | Windows           |
| IPアドレス               | 192.168.1.152         | 192.168.1.107     |
| AMS Net ID               | 192.168.1.152.1.1     | 192.168.1.107.1.1 |
| ソフトウェア             | EMQX、MQTTX、NeuronEX | TwinCAT 3         |
| ネットワーク             | 接続済み              | 接続済み          |

### EMQXクイックスタート

EMQXは複数のインストールメソッドを提供しており、詳細なインストール方法は[ドキュメンテーション](https://docs.emqx.com/en/emqx/v5.0/deploy/install.html?__hstc=3614191.b33d76295d5ea0e3bb7790a771a4b313.1683685186356.1707915189318.1707973897021.539&__hssc=3614191.1.1707973897021&__hsfp=697508886)で確認できます。この例では、Dockerコンテナのデプロイメントを使用してEMQXを素早く体験します。

次のコマンドでDockerイメージを取得します：

```shell
docker pull emqx/emqx:5.1.0
```

次のコマンドでDockerコンテナを起動します：

```shell
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

EMQXダッシュボードにアクセスするには、ウェブブラウザを使用して`http://localhost:18083/`にアクセスします（「localhost」を実際のIPアドレスに置き換えてください）。これにより、デバイスの接続を管理し、関連するメトリクスを監視できます。このチュートリアルではDockerコンテナを実行したままにしておいてください。[ドキュメンテーション](https://docs.emqx.com/en/emqx/v5.0/)を参照して、ダッシュボードの他の機能を体験できます。

初期のユーザー名：`admin`、初期のパスワード：`public`

### TwinCATのセットアップ

[Beckhoff TwinCATのウェブサイト](https://www.beckhoff.com/en-us/products/automation/twincat)を参照して、TwinCATをダウンロードしてインストールしてください。

NeuronEXとTwinCAT PLCが互いに通信できるようにするためには、まずTwinCATにNeuronEXのための静的ルートを追加する必要があります。**TwinCAT Static Routes**ダイアログを開き、次の画像でハイライトされている情報を提供します。**AmsNetId**はNeuronEX PCのIPアドレスに".1.1"を追加したものです。

![Add Route Dialog](https://assets.emqx.com/images/76fa1bf6823b3922ec91a5e8ad908e71.png)

デモンストレーション目的の十分な変数を定義するTwinCAT PLCプログラムを使用します。

![TwinCAT PLC program](https://assets.emqx.com/images/5dbe48a09eeab228f8e15a3e73e45b92.png)

TwinCATプロジェクトディレクトリ内のTPYファイルを開きます。このファイルにはPLCプログラムで定義された各変数のインデックスグループとインデックスオフセットが含まれており、これはNeuronEXでのタグアドレスに使用されます。

![Open the TPY file in the TwinCAT project directory](https://assets.emqx.com/images/9084517cef1d7754bc4edd3e3b9c55af.png)

### NeuronEXクイックスタート

NeuronEXのインストール方法については、[インストール手順](https://neugates.io/docs/en/latest/installation/installation.html)を参照してください。NeuronEXがインストールされたら、ブラウザを使用して`http://localhost:7000`にアクセスしてダッシュボードにアクセスできます。

#### ステップ1. ログイン

初期のユーザー名とパスワードでログインします：

- ユーザー名：`admin`
- パスワード：`0000`

#### ステップ2. 「Southbound」デバイスを追加

NeuronEXダッシュボードで、**Configuration -> South Devices -> Add Device** をクリックして*ads*ノードを追加します。

![Add Device](https://assets.emqx.com/images/5187bdf877d941bfe0d64c833c566094.png)

#### ステップ3. *ads*ノードを設定

次に示すように、新しく作成された*ads*ノードを設定します。

![Configure the *ads* node](https://assets.emqx.com/images/3f274010fdfacf9171e41e3946fbaaca.png)

#### ステップ4. *ads*ノードにグループを作成

*ads*ノードをクリックして**Group List**ページに入り、**Create**をクリックして**Create Group**ダイアログを表示します。パラメータを入力して送信します：

- グループ名：grp。
- インターバル：1000。

#### ステップ5. グループにタグを追加

前述のTwinCAT PLCプログラムのいくつかの変数に対して、*ads*ノードの*grp*グループに対応するタグを追加します。タグアドレスは、変数のインデックスグループとインデックスオフセットで構成されます。

![Tag list](https://assets.emqx.com/images/20c416184399e49f214f18bdaeff3ace.png)

#### ステップ6. データ監視

NeuronEXダッシュボードで、**Monitoring -> Data Monitoring**をクリックし、タグ値が正しく読み取られていることを確認します。

![Data monitoring](https://assets.emqx.com/images/580560b0c1def328487505dd9b35b48a.png)

#### ステップ7. 「Northbound」アプリにMQTTを追加

NeuronEXダッシュボードで、**Configuration -> North Apps -> Add App**をクリックして*mqtt*ノードを追加します。

![Add an MQTT north app](https://assets.emqx.com/images/1b1709864d898c7ef3109abd718ffdce.png)

#### ステップ8. *mqtt*ノードを設定

先にセットアップしたEMQXブローカーに接続するために、*mqtt*ノードを設定します。

![Configure the *mqtt* node](https://assets.emqx.com/images/6ed2b023bb6392192fc365b0bb8300e6.png)

#### ステップ9. *mqtt*ノードを*ads*ノードにサブスクライブ

新しく作成された*mqtt*ノードをクリックして**Group List**ページに入り、**Add subscription**をクリックします。成功したサブスクリプションの後、NeuronEXはトピック`/neuron/mqtt/ads/grp`にデータを公開します。

![Subscribe the *mqtt* node to the *ads* node](https://assets.emqx.com/images/508ebc7537ed6e2adb716f8d07cac98d.png)

### MQTTXを使用してデータを表示

これで、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)を使用してEMQXに接続し、報告されたデータを表示できます。ここでは、[公式ウェブサイト](https://mqttx.app/ja)からダウンロードできる強力なクロスプラットフォームMQTTクライアントツールである[MQTTX](https://mqttx.app/ja)を使用します。

MQTTXを起動し、先に設定したEMQXブローカーに新しい接続を追加し、トピック`/neuron/mqtt/ads/grp`にサブスクリプションを追加します。サブスクリプションが成功すると、MQTTXはNeuronEXが収集し、報告したデータを継続的に受信します。次の図に示すように。

![image.png](https://assets.emqx.com/images/8c13e03467125f36738a42db5256a4de.png)

## まとめ

このブログでは、NeuronEXを使用してTwinCATデータをMQTTにブリッジングする全体的なプロセスを紹介しました。

産業用オートメーションの広く使用されているプラットフォームであるTwinCATは、自動車、航空宇宙、食品および飲料などのさまざまな業界で採用されています。産業用IoTのための強力な接続性を備えたNeuronEXは、TwinCAT PLCからのデータ収集と、必要に応じてリモート制御および監視のためのクラウドへの取得データのシームレスな転送を容易にします。

NeuronEXは、[Modbus](https://www.emqx.com/ja/blog/modbus-protocol-the-grandfather-of-iot-communication)、[OPC UA](https://www.emqx.com/ja/blog/opc-ua-protocol)、SIEMENSなどの他の産業用プロトコルもサポートしています。他のブリッジングチュートリアルについては、当社の投稿をお読みください：[IIoTのためのModbusデータをMQTTにブリッジングする：ステップバイステップチュートリアル](https://www.emqx.com/ja/blog/bridging-modbus-data-to-mqtt-for-iiot)。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
