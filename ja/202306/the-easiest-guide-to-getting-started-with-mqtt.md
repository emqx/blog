この記事では、MQTTプロトコルを使い始める方法をコード例とともに読者に紹介します。IoTとMQTTの初心者は、この記事でMQTT関連の概念を理解し、MQTTサービスとアプリケーションの開発を素早く始めることができます。

## MQTTとは？

MQTT（Message Queuing Telemetry Transport）は、リソースに制約のあるデバイスや低帯域幅、高遅延、または信頼性の低いネットワーク向けに設計された、軽量でパブリッシュ・サブスクライブに基づくメッセージングプロトコルである。IoT（Internet of Things）アプリケーションで広く使用されており、センサー、アクチュエーター、などのデバイスの効率的な通信プロトコルを提供します。

## MQTTはIoTに最適なプロトコル理由は？

MQTTは、IoTシステムの特定の要求に合わせた機能と性能により、最適なIoTプロトコルの1つとしてよく使用されています。主な理由としては、以下のようなものがあります：

- **軽量**：IoT機器は、処理能力、メモリ、エネルギー消費量に制約があることが多い。MQTTはオーバーヘッドが少なく、パケットサイズも小さいため、これらの機器に最適で、リソースの消費も少なく、限られた機能でも効率的な通信が可能です。
- **信頼性が高い**：IoTネットワークでは、高遅延や不安定な接続が発生することがあります。MQTTは、さまざまなQoSレベル、セッション認識、持続的な接続をサポートしており、厳しい条件下でも信頼性の高いメッセージ配信を実現するため、IoTアプリケーションに適しています。
- **セキュアな通信を実現します**：IoTネットワークでは、機密データを送信することが多いため、セキュリティは極めて重要です。MQTTはTLS（Transport Layer Security）とSSL（Secure Sockets Layer）の暗号化をサポートし、伝送中のデータのセキュリティを確保できます。さらに、ユーザー名/パスワード認証やクライアント証明書による認証のメカニズムを提供し、ネットワークとそのリソースへのアクセスを保護します。
- **双方向性**：MQTTのパブリッシュ・サブスクライブモデルは、デバイス間のシームレスな双方向通信を可能にしています。クライアントは、Topicへのメッセージのパプリッシュと、特定のTopicに関するメッセージの受信の両方を行うことができ、デバイス間を直接結合することなく、多様なIoTエコシステムにおいて効果的なデータ交換を可能にします。また、このモデルは、新しいデバイスの統合を簡素化し、容易なスケーラビリティを保証します。
- **連続性、ステートフル・セッション**：MQTT では、クライアントがブローカーとのステートフルなセッションを維持できるため、切断後でもサブスクリプションや未配信のメッセージをシステムが記憶することができます。また、クライアントは接続中にキープアライブ間隔を指定することができ、これによりブローカーは定期的に接続状態を確認するよう促されます。接続が切れた場合、ブローカーは未配信のメッセージを保存し（QoSレベルによる）、クライアントが再接続したときに配信を試みます。この機能により、信頼性の高い通信を実現し、断続的な接続によるデータ消失のリスクを低減します。
- **大規模なIoTデバイスへの対応**：IoTシステムには多数のデバイスが含まれることが多く、大規模なデプロイメントに対応するプロトコルが必要です。MQTTの軽量性、低帯域幅消費、リソースの効率的な使用は、大規模なIoTアプリケーションに適しています。MQTTは、パブリッシュ・サブスクライブ・パターンにより、送信者と受信者を分離し、ネットワークトラフィックとリソース使用量を削減するため、効果的に拡張することができます。さらに、このプロトコルはさまざまなQoSレベルをサポートしているため、アプリケーションの要件に基づいてメッセージ配信をカスタマイズすることができ、さまざまなシナリオで最適なパフォーマンスを確保することができます。
- **多プログラミング言語に対応**：IoTシステムには、多くのプログラミング言語を使用して開発されたデバイスやアプリケーションが含まれることがよくあります。MQTTの幅広い言語サポートにより、複数のプラットフォームやテクノロジーとの統合が容易になり、多様なIoTエコシステムにおいてシームレスな通信と相互運用性が促進されます。PHP、Node.js、Python、Golang、Node.js、その他のプログラミング言語でのMQTTの使用方法については、[MQTT Client Programming](https://www.emqx.com/en/blog/category/mqtt-programming)のブログシリーズをご覧下さい。

**詳しくは記事でご紹介しています：**[**What is MQTT and Why is it the Best Protocol for IoT?**](https://www.emqx.com/en/blog/what-is-the-mqtt-protocol)

## MQTTの仕組みは？

MQTTの仕組みを理解するためには、まずMQTT クライアント、MQTT Broker、Publish-Subscribeモード、Topic、QoSの概念をマスターする必要があります：

**MQTTクライアント**

[MQTTクライアント・ライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)を実行するアプリケーションやデバイスは、すべてMQTTクライアントとなります。例えば、MQTTを利用するインスタントメッセージングアプリはクライアント、MQTTを利用してデータを報告する各種センサーはクライアント、各種[MQTTテストツール](https://www.emqx.com/en/blog/mqtt-client-tools)もクライアントとなります。

**MQTTブローカー**

MQTT ブローカーは、クライアントの接続、切断、サブスクリプション、およびアンサブスクリプションの要求、およびメッセージのルーティングを処理する。強力なMQTTブローカーは、大量の接続と100万レベルのメッセージスループットをサポートし、IoTサービスプロバイダーがビジネスに集中し、信頼性の高いMQTTアプリケーションを迅速に作成できるようにします。

MQTTブローカーの詳細については、ブログ「[The Ultimate Guide to MQTT Broker Comparison in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)」をご確認ください。

**パブリッシュ・サブスクライブ・パターン**

パブリッシュ・サブスクライブ・パターンは、メッセージを送信するクライアント（パブリッシャー）とメッセージを受信するクライアント（サブスクライバー）を分離するという点で、クライアント・サーバー・パターンとは異なる。パブリッシャーとサブスクライバーは直接接続する必要がなく、MQTT Brokerがすべてのメッセージのルーティングと配布を担当します。

次の図は、MQTTのパブリッシュ/サブスクライブ処理を示しています。温度センサーがクライアントとしてMQTTサーバーに接続し、温度データをTopic（例： 「Temperature」 ）にパブリッシュすると、サーバーはメッセージを受信して 「Temperature」 Topicをサブスクライブしているクライアントに転送する。

![Publish–subscribe pattern](https://assets.emqx.com/images/a6baf485733448bc9730f47bf1f41135.png)

 **Topic**

MQTTプロトコルは、Topicに基づいてメッセージをルーティングします。Topicはスラッシュ `/` で階層を区別し、それはURLパスに似ています：

```
chat/room/1

sensor/10/temperature

sensor/+/temperature
```

MQTT Topicは、以下のワイルドカードをサポートしています： `+` と `#` です。

-  `+` ： `a/+` が `a/x` や `a/y` にマッチするような、1レベルのワイルドカードを示す。
-  `#` ： `a/#` と `a/x` 、 `a/b/c/d` のマッチングのように、複数レベルのワイルドカードを示す。

MQTT Topicの詳細については、ブログ「[Understanding MQTT Topics & Wildcards by Case](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics)」をご確認ください。

**サービス品質（QoS）**

MQTTは3種類のQoSを提供し、異なるネットワーク環境でのメッセージングの信頼性を保証します。

- QoS 0：メッセージは最大1回配信される。クライアントが現在利用できない場合、このメッセージは失われる。
- QoS 1：少なくとも1回はメッセージが届く。
- QoS 2：メッセージは確保して1回のみ届く。

MQTT QoSの詳細については、ブログ「[Introduction to MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)」をご確認ください。

## MQTTワークフロー

MQTTの基本的な構成要素を理解したところで、一般的なワークフローを確認してみましょう：

1. クライアントは、TCP/IPを使用してブローカーへの接続を開始し、オプションでTLS/SSL暗号化により安全な通信を行います。クライアントは認証情報を提供し、クリーンまたは永続的なセッションを指定します。
2. クライアントは、特定のTopicにメッセージを公開するか、Topicにサブスクライブしてメッセージを受信します。パブリッシング・クライアントはブローカーにメッセージを送信し、サブスクライブ・クライアントは特定のTopicに関するメッセージの受信に関心を示す。
3. ブローカーは公開されたメッセージを受信し、関連するTopicをサブスクライブしているすべてのクライアントに転送する。指定されたサービス品質（QoS）レベルに従って信頼性の高いメッセージ配信を保証し、セッションタイプに基づいて切断されたクライアントのメッセージストレージを管理する。

## MQTT入門編：クイックチュートリアル

では、MQTTの使い始め方を簡単なデモを交えて紹介します。始める前に、MQTT BrokerとMQTT Clientを準備する必要があります。

### MQTTブローカーを用意する

プライベートデプロイメントやフルマネージドクラウドサービスを通じてMQTTブローカーを作成することができます。また、テスト用に無料のパブリックブローカーを使用することもできます。

-  **プライベート展開**

  [EMQX](https://github.com/emqx/emqx)は、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始する最も簡単な方法です。以下に示すように、[EMQX Cloud](https://www.emqx.com/en/cloud)は数分で開始し、AWS、Google Cloud、Microsoft Azureの17リージョンで稼働します。

  ![MQTT Cloud](https://assets.emqx.com/images/d019e0dbc27f706eca6256e11720eb9b.png)

-  **無料公開のMQTTブローカー**

  今回は、[フルマネージドMQTTクラウドサービス - EMQX Cloud](https://www.emqx.com/ja/cloud)をベースに作成した、EMQが提供する[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。サーバー情報は以下の通りです。

  -  ブローカーアドレス： `broker.emqx.io`
  -  TCP Port： `1883`
  -  WebSocket Port： `8083` 

### MQTTクライアントを用意する

今回は、[MQTTX](https://mqttx.app/)が提供するブラウザアクセスをサポートするMQTTクライアントツール「[http://mqtt-client.emqx.com/」](http://mqtt-client.emqx.com/)を使用します。MQTTXでは、デスクトップクライアントとコマンドラインツールも提供されています。

MQTTXは、macOS、Linux、Windows上で動作するエレガントなクロスプラットフォームMQTT 5.0デスクトップクライアントです。そのユーザーフレンドリーなチャットスタイルのインターフェースにより、ユーザーは簡単に複数のMQTT/MQTTS接続を作成し、MQTTメッセージをサブスクライブ/パブリッシュすることができます。

![MQTTX](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

<center>MQTTXのプレビュー</center>

<br>

現在、すべてのプログラミング言語用の成熟したオープンソースのMQTTクライアント・ライブラリが存在します。私たちは、様々なプログラミング言語で[人気のあるMQTTクライアントライブラリ＆SDK](https://www.emqx.com/ja/mqtt-client-sdk)を選び、MQTTクライアントの使い方を素早く理解できるようにコード例を提供しました。

### MQTTコネクションの作成

MQTTプロトコルを使用して通信する前に、クライアントはブローカーに接続するためのMQTT接続を作成する必要があります。

ブラウザで [http://mqtt-client.emqx.com/](http://mqtt-client.emqx.com/)  にアクセスし、ページ中央の `New Connection` ボタンをクリックすると、以下のページが表示されます。

![Create an MQTT connection](https://assets.emqx.com/images/5e110d181ce8489c275d5674910fa16d.png)

 

`Name`に `Simple Demo` を入力し、右上の `Connect` ボタンをクリックして、MQTT接続を作成します。以下は、正常に接続が確立されたことを示しています。

![MQTT connection successful](https://assets.emqx.com/images/9583db03a552b24980cf49005e3dc668.png)

 

MQTT接続のパラメータについて詳しくは、ブログ記事をご覧ください：「[How to Set Parameters When Establishing an MQTT Connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)」をご覧ください。

### ワイルドカードのTopicをサブスクライブする

次に、先ほど作成した Simple Demo 接続のワイルドカードTopic `sensor/+/temperature` をサブスクライブし、すべてのセンサーから報告される温度データを受信します。

下図のように、 `New Subscription` ボタンをクリックし、ポップアップボックスのTopicフィールドにTopic `sensor/+/temperature` を入力し、デフォルトのQoSを0に維持します。

![MQTT Subscribe](https://assets.emqx.com/images/79321fd9e22058e27a256152b60908d6.png)

サブスクライブが成功すると、サブスクライブリストに追加のレコードが表示されます。

![MQTT subscription is successful](https://assets.emqx.com/images/3687ba334049a0ca19e3300a2cbc4a98.png)

### MQTTメッセージのパプリッシュ

次に、左メニューの `+` ボタンをクリックして、2つの温度センサーをシミュレートするために、それぞれ `Sensor 1` と `Sensor 2` という2つの接続を作成します。

![Create MQTT connections](https://assets.emqx.com/images/0c96ec70a51ecc605bad4972edd77fb1.png)

 

接続が作成されると、3つの接続が表示され、接続の左側にあるオンライン状態のドットがすべて緑色になることを確認してください。

![MQTT connection created successfully](https://assets.emqx.com/images/70010ba4da8d452ab0f738d36013dd9a.png) 

`Sensor 1`接続を選択し、ページ左下の部分に公開Topic `sensor/1/temperature` を入力し、メッセージボックスに以下のJSON形式のメッセージを入力し、右下の公開ボタンをクリックするとメッセージが送信されます。

```
{
  "msg": "17.2"
}
```

![Publish MQTT messages](https://assets.emqx.com/images/859966556e5649f1d6ec9bf378162def.png)

以下のように、メッセージは正常に送信されます。

![MQTT message is sent successfully](https://assets.emqx.com/images/b1a46d8a415603d87e0c4244ee34bc02.png)

同じ手順で、センサー2接続の `sensor/2/temperature` Topicに以下のJSONメッセージをパプリッシュします。

```
{
  "msg": "18.2"
}
```

Simple Demo接続のための新しいメッセージの数は「２」が表示されます。

![MQTT notification](https://assets.emqx.com/images/f815767a47f234424ae55ea0fe39eb04.png)

Simple Demoの接続をクリックすると、2つのセンサーから送信される2個のメッセージが表示されます。

![MQTT messages](https://assets.emqx.com/images/f88de809773829f6a86dcedc2f612dd5.png)

 

### MQTT機能のデモ

#### Retained Message

MQTTクライアントがサーバーにメッセージを公開する際に、「Retained Message」フラグを設定することができます。「Retained Message」はメッセージサーバーに存在し、後続のサブスクライバーはTopicにサブスクライブする際にメッセージを受信することができます。

下図のように、 `Retain` オプションをチェックしたセンサー1接続の `retained_message` Topicに、2つのメッセージを送信しているところです。

![MQTT Retained Message](https://assets.emqx.com/images/5c7dcb078d223e0b6d33cb66241caa5d.png) 

次に、Simple Demo接続で `retained_message` Topicをサブスクライブします。サブスクライブが成功すると、センサー1が送信した2番目の「Retained Message」を受信することになり、サーバーはTopicに対して最後の「Retained Message」だけを保持することがわかります。

![MQTT Retained Message](https://assets.emqx.com/images/afe8cca62d576404d5f622f362ef3592.png)

Retained Messageの詳細については、ブログ「[The Beginner's Guide to MQTT Retained Messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message)」をご確認ください。

#### Clean Session

一般に、MQTTクライアントは、オンライン状態のときにのみ、他のクライアントからパプリッシュされたメッセージを受信することができます。クライアントがオフラインの後にオンラインになった場合、オフライン期間中のメッセージは受信できません。

しかし、クライアントがClean Sessionをfalseに設定して接続し、同じクライアントIDで再度オンラインになった場合、メッセージサーバーはそのクライアントのために一定量のオフラインメッセージを保持し、再度オンラインになったときにクライアントに送信します。

> *今回のデモに使用した公開MQTTサーバーは、オフラインのメッセージを5分間保持し、最大メッセージ数は1000（QoS 0メッセージなし）に設定されています。*

次に、MQTT 3.1.1接続を作成し、QoS 1による Clean Session を実演します。

> *MQTT 5では、Clean Sessionを改善するためにClean StartとSession Expiry Intervalを使用しています。詳しくは、ブログ「*[*Clean Start and Session Expiry Interval*](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)*」をご参照ください。*

MQTT V3という名前の接続を作成し、Clean Sessionをfalseに設定し、MQTTバージョン3.1.1を選択します。

![MQTT Clean Session](https://assets.emqx.com/images/1472ce0ea8e728647d973cae56e6b1d5.png)

接続に成功したら `clean_session_false` Topicをサブスクライブし、QoSを1に設定します。

![MQTT subscribe](https://assets.emqx.com/images/7a5792040185d956803cb7406b2df3af.png)

加入が完了したら、右上の赤色の「切断」ボタンをクリックします。

![Disconnect MQTT connection](https://assets.emqx.com/images/fd5726bd0e2a5b9d9d73a7095f322ecf.png)

次に、 `MQTT_V3_Publish` という名前の接続を作成し、MQTTのバージョンも3.1.1に設定します。接続に成功したら、 `clean_session_false` Topicに3つのメッセージをパプリッシュします。

![Publish MQTT messages](https://assets.emqx.com/images/0659785e98cb03f9d6e78497e0adb26f.png)

次に、MQTT_V3接続を選択し、接続ボタンをクリックしてサーバーに接続すると、3つのオフラインメッセージが表示されます。

![MQTT messages](https://assets.emqx.com/images/106cc289cbb3a07be2ed294dd97fe420.png)

Clean Sessionの詳細については、ブログ「[MQTT Persistent Session and Clean Session Explained](https://www.emqx.com/en/blog/mqtt-session)」をご確認ください。

#### Last Will

MQTTクライアントがサーバにCONNECTリクエストを行う際に、「Willメッセージ」のフラグを送信するかどうか、TopicとPayloadを送信するかどうかを設定することができます。

MQTTクライアントが異常オフライン（クライアントが切断する前にDISCONNECTメッセージがサーバーに送信されない）になると、MQTTサーバーは「Willメッセージ」をパプリッシュします。

以下のように、 `Last Will` という名前の接続を作成します。

- 効果を早く確認するために、Keep Aliveを5秒に設定しました。
- Last-Will Topicを `last_will` に設定する。
- Set Last-Will QoS to `1`.
- Last-Will Retainを `true` に設定します。
- Last-Will Payloadを `offline` に設定する。

![MQTT Last Will](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png)

接続成功後、コンピュータのネットワークを5秒以上切断し（クライアントの異常切断をシミュレート）、再びネットワークをオンにします。

次にSimple Demo接続を開始し、 `last_will` Topicをサブスクライブしてください。 `Last Will` 接続で設定された「Willメッセージ」を受信することができます。

![MQTT Last Will](https://assets.emqx.com/images/a216808a1ba964bbddc75708bc55c072.png) 

MQTT Will Messageの詳細については、ブログ「[Use of MQTT Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message)」をご確認ください。

## MQTTについてもっと知る

ここまでMQTTの基本概念と使用プロセスについて説明とデモンストレーションを行ってきました。読者の皆さんはこの記事で学んだことをもとに、MQTTプロトコルの利用を試してみてください。

次にEMQが提供する[「MQTT Guide 2023: Beginner to Advanced」](https://www.emqx.com/en/mqtt-guide)の記事シリーズをチェックして、MQTT Topic、ワイルドカード、保持メッセージ、Last-Will、その他の機能について学ぶことができます。MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
