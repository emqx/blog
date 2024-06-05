## イントロダクション

このブログでは、Neuronを使用して[KNX](https://www.emqx.com/en/blog/knx-protocol)デバイスからデータを収集し、集めたデータをEMQXにアップロードしてMQTTXを使用して表示する方法を紹介します。

LinuxマシンでEMQX、MQTTX、Neuronのインストールを行います。ETSとKNX VirtualはWindowsのみサポートしているため、KNXのインストールをシミュレートするWindows VMを実行します。

![The Architecture of KNX to MQTT Bridging](https://assets.emqx.com/images/94d52d2aba496120411cc0d02bde8ad7.png)

## EMQXクイックスタート

EMQXは複数のインストール方法を提供しており、詳細なインストール方法は[ドキュメント](https://docs.emqx.com/en/emqx/v5.0/deploy/install.html)で確認できます。この例では、コンテナデプロイメントを使用してEMQXを素早く体験できます。

Dockerイメージを取得するには以下のコマンドを実行します：

```shell
docker pull emqx/emqx:5.1.0
```

Dockerコンテナを起動するには以下のコマンドを実行します：

```shell
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

ウェブブラウザを使用して`http://localhost:18083/`（"localhost"を実際のIPアドレスに置き換える）でEMQXダッシュボードにアクセスします。デバイス接続の管理と関連するメトリックをモニタリングすることができます。このチュートリアルのためにDockerコンテナを実行状態に保ちます。ダッシュボードのさらなる機能体験には、[ドキュメント](https://docs.emqx.com/en/emqx/v5.0/)を参照してください。

初期ユーザー名: `admin` 初期パスワード: `public`

## ETSを使用したKNX Virtualのセットアップ方法

[KNX Virtualをダウンロードしてインストール](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php)します。ETSとKNX Virtualを使用してKNXのインストールをシミュレートする方法については、[ブログチュートリアル](https://www.ets6.org/ets6-and-knx-virtual/)や[KNX Virtual Basicsビデオチュートリアル](https://www.youtube.com/watch?v=01MO_zmtGv4)を参照できます。

KNX Virtualでは、KLiX（D0）、調光アクチュエータ（D0）、ブラインド/シャッターアクチュエータ（D2）、スイッチアクチュエータ（D7）をシミュレートします。アドレスとグループオブジェクトの関連図は以下の通りです：

![KNX Virtual](https://assets.emqx.com/images/6d36e1efa508eca48c39832c7954f57c.png)

## Neuronクイックスタート

Neuronのインストール手順は[こちら](https://neugates.io/docs/en/latest/installation/installation.html)です。インストール後、ブラウザで`http://localhost:7000`（"localhost"を実際のIPアドレスに置き換える）からダッシュボードにアクセスできます。

### ステップ1: ログイン

初期ユーザー名とパスワードでログイン:

- ユーザー名: `admin`
- パスワード: `0000`

### ステップ2: 南側デバイスを追加

Neuronダッシュボードで **Configuration -> South Devices -> Add Device** をクリックし、*knx*ノードを追加します。

![Add a south device](https://assets.emqx.com/images/769435a4caf26298e8e0cb924de59a20.png)

### ステップ3: *knx*ノードを設定

新しく作成された*knx*ノードを設定します。

![Configure the *knx* node](https://assets.emqx.com/images/8b93dfd897e88acba6d51f129f0426d5.png)

### ステップ4: *knx*ノード内にグループを作成

*knx*ノードをクリックして**Group List**ページに入り、**Create**をクリックして**Create Group**ダイアログを開きます。パラメータを入力し、提出します：

- グループ名: `grp`
- インターバル: `1000`

![Create a group in the *knx* node](https://assets.emqx.com/images/b3ce997da0687c578dfc8ed850744627.png)

### ステップ5: グループにタグを追加する

KNX Virtualの設定に合わせて、調光アクチュエータ、シャッターアクチュエータ、スイッチアクチュエータに対応する4つのタグをグループに追加します。

![Add tags to the group](https://assets.emqx.com/images/17ecb2eba0fbbe000112872f8833e374.png)

### ステップ6: データ監視

Neuronダッシュボードで**Monitoring -> Data Monitoring**をクリックし、タグの値が正しく読み取られることを確認します。

![Data monitoring 1](https://assets.emqx.com/images/8f5dd1e3c15a5c4a2f515e6e8c5b2e4f.png)

![Data monitoring 2](https://assets.emqx.com/images/2b09ae4a02367b3c2b8c3221902b6b06.png)

### ステップ7: MQTT Northアプリを追加する

Neuronダッシュボードで**Configuration -> North Apps -> Add App**をクリックし、*mqtt*ノードを追加します。

![Add an MQTT North app](https://assets.emqx.com/images/6dc854ceedafc6615e71b5fa275c1699.png)

### ステップ8: *mqtt*ノードを設定する

*mqtt*ノードを設定して、以前にセットアップしたEMQXブローカーに接続します。

![Configure the *mqtt* node](https://assets.emqx.com/images/c6725171f15e8529492588ae3693af98.png)

### ステップ9: *mqtt*ノードを*knx*ノードにサブスクライブする

新しく作成された*mqtt*ノードをクリックして**Group List**ページに入り、**Add subscription**をクリックします。成功するとNeuronが`/neuron/mqtt/knx/grp`トピックにデータを公開します。

![Subscribe the *mqtt* node to the *knx* node](https://assets.emqx.com/images/b673b0c1b5b23f682065d2beab900d6d.png)

## MQTTXを使用したデータの確認

MQTTクライアントを使用してEMQXに接続し、報告されたデータを表示できます。ここでは、[公式サイト](https://mqttx.app/ja)からダウンロードできる[MQTTX、強力なクロスプラットフォームMQTTクライアントツール](https://mqttx.app/ja)を使用します。

MQTTXを起動し、以前にセットアップしたEMQXブローカーに新しい接続を追加し、トピック`/neuron/mqtt/knx/grp`にサブスクリプションを追加します。サブスクリプションが成功すると、MQTTXはNeuronによって収集され報告されたデータを継続的に受け取ります。以下の図のようです：

![MQTTX](https://assets.emqx.com/images/9beb4e4d3514aff1b659067c42be9084.png)

## 結論

このブログでは、KNXプロトコルを紹介し、Neuronを使用してKNXデータをMQTTにブリッジする全体的なプロセスをデモンストレーションしました。

KNXは家庭および建物のオートメーションのための堅牢で柔軟なプラットフォームを提供し、産業用IoT用の強力な接続機能を持つNeuronは、KNXデバイスからのデータ収集と取得したデータのクラウドへのシームレスな伝送を容易にし、便利なリモートコントロールと監視を必要に応じて提供します。

NeuronはModbus、OPC UA、SIEMENSなど他の産業プロトコルもサポートしています。他のブリッジングチュートリアルについては、私達の投稿を読むことをお勧めします：

- [IIoT向けModbusデータをMQTTにブリッジする：ステップバイステップチュートリアル](https://www.emqx.com/en/blog/bridging-modbus-data-to-mqtt-for-iiot#the-architecture-of-modbus-to-mqtt-bridging)
- [IIoT向けのOPC UAデータをMQTTにブリッジする：ステップバイステップチュートリアル](https://www.emqx.com/ja/blog/bridging-opc-ua-data-to-mqtt-for-iiot)
- [TwinCATデータをMQTTにブリッジする：イントロダクションとハンズオンチュートリアル](https://www.emqx.com/ja/blog/bridging-twincat-data-to-mqtt)
- [FINSデータをMQTTにブリッジする：プロトコル解説とハンズオンチュートリアル](https://www.emqx.com/en/blog/bridging-fins-data-to-mqtt)



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
