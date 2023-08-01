## はじめに

[Sparkplug](https://www.emqx.com/ja/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot)は、産業用デバイスやアプリケーションと通信するための標準化された方法を提供する産業用IoTプロトコルです。効率的で包括的なSparkplugソリューションは、デバイスとアプリケーション間の通信を促進し、データからの洞察を通じてIIoT採用企業の意思決定を強化することができます。

このブログでは、EMQXとNeuronを使った[MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0)ソリューションの実践例を紹介します。

## EMQXとNeuron：不可欠なコンポーネント

[EMQX](https://www.emqx.io/)はSparkplugプロトコルをサポートする人気的な[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)であり、Neuronは産業用デバイスからデータを収集し、アプリケーション用にSparkplugメッセージを生成するために使用できる産業用IoTプラットフォームである。

[Neuron](https://neugates.io/)はデバイスからデータを収集し、そのデータに基づいてEMQXブローカにSparkplugメッセージを発行して変更を報告します。EMQXは、関連するSparkplugトピックをサブスクライブしているアプリケーションにメッセージを転送します。しかし、EMQXはルールエンジンを通してSparkplugメッセージをデコードすることができる。メッセージはその後、データプラットフォームや履歴の永続ストレージなどに使用される。

> *Sparkplugソリューションのアーキテクチャについては、こちらの記事をご覧ください：*[*EMQXとNeuronを使用した産業用IoT向けMQTT Sparkplugソリューション*](https://www.emqx.com/ja/blog/mqtt-sparkplug-solution-for-industrial-iot-using-emqx-and-neuron)

![MQTT Sparkplug solution](https://assets.emqx.com/images/eca65d9a9ab24cb2bc02ce929162d1b5.png)

このブログでは、EMQXとNeuronを使ってMQTT Sparkplugを始める方法を、以下の手順で紹介します：

1.  EMQXのインストール
2.  EMQXの設定
3.  ニューロンをインストールする
4. Neuronでデバイスを設定する
5. NeuronとEMQXの接続
6. MQTT Xで結果を確認する

 始めよう！

## EMQXのインストール

EMQX MQTTブローカーをダウンロードし、サーバーまたはマシンにインストールする。EMQXはコミュニティ版を提供しており、ウェブサイトから無料でダウンロードできる。ウェブサイト[https://www.emqx.io/](https://www.emqx.io/)、ドキュメントに従ってください。

<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

## EMQXの設定

EMQXをインストールしたら、Sparkplugプロトコルをサポートするように設定する必要がある。

### EMQXでスキーマ・レジストリを作成する

スキーマレジストリの作成ボタンをクリックします。

![Schema Registry](https://assets.emqx.com/images/414d1d19937f7b127bf078022516db5b.png)

Parse Typeにprotobufを選択し、Sparkplugスキーマでスキーマを埋める。

![Select the protobuf for **Parse Type**](https://assets.emqx.com/images/92713344955371feef0f189c2714564e.png)

### EMQXでルールを作成する

デコードに使用されるSQL文。

```
SELECT
 schema_decode('neuron', payload, 'Payload') as SparkPlugB
FROM
 "spBv1.0/group1/DDATA/node1/modbus"

```

ここでのキーポイントは、 schema_decode('neuron', payload, 'Payload') ：

- `schema_decode()` はペイロードフィールドの内容をスキーマ'protobuf_person'に従ってデコードする。
- `as SparkPlugB` はデコードした値を変数 "SparkPlugB "に格納する。
- 最後のパラメータ `Payload` は、ペイロードのメッセージタイプがprotobufスキーマで定義された「Payload」タイプであることを示す。

![Edit rules](https://assets.emqx.com/images/c86eaf113839e16ac2ef47fe65866ee2.png)

次に、以下のパラメータを持つアクションを追加する：

- アクションの種類メッセージの再投稿
- 目的のトピックSparkPlugB/test

このアクションは、デコードされた "Payload "をJSON形式でSparkPlugB/testトピックに送信します。

![Edit action](https://assets.emqx.com/images/a11c438376914cc10bda248d9dbace96.png)

## ニューロンをインストールする

Neuronは、産業用デバイスからデータを収集、保存、分析するために使用できる産業用IoTプラットフォームである。Neuronは同社のウェブサイトからダウンロードしてインストールできる。ウェブサイト[https://www.neugates.io/](https://www.neugates.io/)、ドキュメントに従ってください。

## Neuronでデバイスを設定する

Sparkplug デバイスは、その機能やプロパティを定義するデータ・ポイントのセットで構成されます。データ・ポイントを定義し、特定のデバイスに割り当てることで、Neuron プラットフォームを使用して Sparkplug デバイスを構成できます。

デバイス用ドライバープラグインモジュールを選択します。

![Select the driver plugin module for devices](https://assets.emqx.com/images/dee478a56cabf28982d95bc30d15c440.png)

デバイス通信用のドライバパラメータを設定する。

![Set up the driver parameters](https://assets.emqx.com/images/95ddaf88bdb5cc305bf8110b9f1ca87c.png)

![Device config](https://assets.emqx.com/images/2da88ff4dddec3ae4ffaca60fa384170.png)

グループを作成し、ポーリング間隔を設定する。

![Create group](https://assets.emqx.com/images/aa91471395538ceb7a7edb054f4bff59.png)

グループにタグを追加し、各タグにアドレスを設定します。

![Add tags](https://assets.emqx.com/images/fb215e69ffcbe4e8ec6d52ac23351935.png)

## NeuronとEMQXの接続

Neuron をインストールしたら、EMQX ブローカに接続する必要があります。このためには、Neuron の MQTT 接続設定を EMQX ブローカに設定します。

ノースバウンド通信ドライバ（SparkplugB）を選択します。

![Add app](https://assets.emqx.com/images/8a9ee5ab1a09cb5d70a62999e745722c.png)

EMQX接続用のドライバ・パラメータを設定する。

![Set up the driver parameters](https://assets.emqx.com/images/c629e130b36ac53f66a21d9adfd8689a.png)

![App config](https://assets.emqx.com/images/64cbe0d49c98ab3dc482b6686f337223.png)

指定のグループにご登録します。

![Add subscription](https://assets.emqx.com/images/a0f825a4446a6ab52153ec0a5da06efd.png)

## MQTTXで結果を確認する

EMQX と Neuron を設定して接続すると、Sparkplug データのパブリッシュとサブスクライブが可能になります。Neuron プラットフォームを使用して、Sparkplug デバイスにデータをパブリッシュし、それらのデバイスからデータをサブスクライブできます。

[MQTTX](https://mqttx.app/ja)ツールは、EMQXルールエンジンのコーデック機能によってデコードされたデータをサブスクライブするために使用される：

![MQTTX SparkplugB](https://assets.emqx.com/images/38691752e5463c39951eddec129f91be.png)

## まとめ

上記の手順に従って、EMQX と Neuron を使用して MQTT Sparkplug を始めることができます。これは基本的な概要に過ぎず、セットアップをカスタマイズするためにさらに多くの高度な機能や設定があることに留意してください。あなたのIIoT開発を加速するために、EMQXとNeuronの強力な機能を探求することを強くお勧めします。



<section class="promotion">
    <div>
        ソリューション専門家に問い合わせ
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
