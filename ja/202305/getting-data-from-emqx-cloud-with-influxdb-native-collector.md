## はじめに

InfluxDataは先日、Native Collectorsの提供を発表し、InfluxDB Cloudにネイティブなデータ収集機能をもたらしました。これにより、開発者は、追加のソフトウェアや新しいコードを必要とせずに、EMQX Cloudなどのサードパーティ製MQTTブローカーからInfluxDB Cloudにデータを取得する最速の方法を得ることができるようになります。
プライベートなMQTTブローカーと統合することは常に可能ですが、これはクラウド間の統合をより簡単に行うための方法です。
このチュートリアルでは、この新しいネイティブコレクターを使用して、InfluxDB Cloudと主要なMQTTサービスプロバイダーであるEMQX Cloudを統合する方法を、ステップバイステップで紹介します。

## 4ステップの統合

統合に必要なのは4つのステップだけです：

1. EMQX CloudでMQTTブローカーを作成する - 3分
2. InfluxDB Cloudでバケットを作成する - 3分
3. ネイティブコレクターの設定 - 2分
4. 検証 - 1分

はい！10分以内にEMQX CloudからInfluxDB Cloudにデータを取得します！

では、確認してみましょう。

## ステップ1：EMQX Cloud上にMQTTブローカーを作成します。

EMQX Cloud上で専用のMQTTブローカーを作成するのは、数クリックで簡単にできます。

#### アカウントを取得する

[EMQX Cloud](https://www.emqx.com/ja/cloud)にアクセスし、EMQX Cloudを初めて利用する場合は、start freeをクリックしてアカウントを登録します。

#### MQTTクラスタの作成

ログイン後、アカウントメニューの「Cloud Console」をクリックすると、新しいデプロイメントを作成するための緑色のボタンが表示されるようになります。

![Create an MQTT instance on EMQX Cloud](https://assets.emqx.com/images/91dd6aab2d0f99a82bc45bd13fd409b0.jpeg)

<center>EMQX CloudでMQTTインスタンスを作成する。</center>

EMQX Cloudは、StandardプランとProfessionalプランの14日間の無料トライアルを提供しています。Proプランはより多くの機能を提供しますが、Standardプランはこのチュートリアルには十分すぎるほどです。

![This tutorial uses Standard Plan](https://assets.emqx.com/images/b493525c1d7348fd74e22c077ec89b0a.jpeg)

<center>このチュートリアルでは、スタンダードプラン</center>

今すぐ作成」をクリックし、ステップバイステップのウォークスルーに従ってデプロイを完了します。最後の「Deploy」ボタンをクリックすると、以下のようにインスタンスが作成されていることが確認できます：

![Creating MQTT instance](https://assets.emqx.com/images/312366cddaeb3ab4e17f6fceb3ab2397.jpeg)

<center>インスタンスの作成</center>

実行中のインスタンスを取得するのに数分かかるでしょう。

![Instance in running status](https://assets.emqx.com/images/f1dabe608d193b5d699affe040621975.jpeg)

<center>ランニング状態のインスタンス</center>

ステータスがRunningに変わったら、カードをクリックしてクラスタの概要に移動します。

#### 接続先アドレスとポートを取得する

概要ページでは、インスタンスの詳細が表示されます。ここでは、InfluxDB Cloud上で統合を構成する際に必要となる、接続アドレスと接続ポートに注目してください。

![MQTT Broker Connection Details](https://assets.emqx.com/images/ace95719204e18152b1d139de3c985e0.jpeg)

<center>ブローカー接続の詳細</center>

EMQX Cloudの各インスタンスは、MQTT接続用の4つのリスナーを作成します（MQTT、MQTT with TLS、MQTT over WebSocket、MQTT over WebSocket with TLS）。ただし、InfluxDB Cloudは現在MQTTプロトコルのみをサポートしているため、最初のポートにのみ注意する必要があります。

#### MQTT接続のための認証情報を追加する

EMQX Cloud の最後の作業は、MQTT 接続のための認証情報を作成することです。左メニューの Authentication and ACLs をクリックし、サブメニューの Authentication をクリックします。

![Authentication Page](https://assets.emqx.com/images/cb71dc1a319b30d99ff8ef4159fdcc9f.jpeg)

<center>認証ページ</center>

右の「追加」ボタンをクリックし、後でmqtt接続するためのユーザー名とパスワードを指定します。ここでは、ユーザー名とパスワードに「test」と「influxdb」を使用することにします。

![Add Credentials](https://assets.emqx.com/images/d79d927ff838b1f3cbf29406b5a096ee.jpeg)

<center>クレデンシャルを追加する</center>

「Confirm」をクリックすると、EMQXクラウド側ですべて決済されます。
これで、EMQX Cloudが提供するMQTTブローカーが動作するようになりました。ステップ2に進みましょう。

## ステップ2：InfluxDBクラウド上にバケットを作成する
#### InfluxDB Cloudのアカウントを作成する

[InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/)を初めて利用する場合は、アカウントも作成する必要があります`。

#### データ永続化のためのBucketを作成する

ログイン後、コンソールページに移動し、メニューの「バケツ」ボタンをクリックします。

![Go to the Buckets page](https://assets.emqx.com/images/45df0c7d8cd9862cee8a742605952c31.jpeg)

<center>バケツのページに移動します</center>

右側の「Create Bucket」をクリックし、フォームに必要事項を入力します。

![Create a new bucket](https://assets.emqx.com/images/11e74c950c499393f1b1bb7581c49feb.jpeg)

<center>新しいバケットを作成する</center>

ここでは、バケット名を「emqxcloud」とします。「Create」をクリックします。

よし、これでバケツの準備ができたぞ。新しいNative Collectorを試してみましょう。

## ステップ3：ネイティブコレクターの設定

#### ネイティブサブスクリプションのページに移動します

バケットページで「NATIVE SUBSCRIPTIONS」タブをクリックします。

![Native subscriptions page](https://assets.emqx.com/images/f41ca2ca97beec67f4d3870cf8733e1d.jpeg)

<center>ネイティブサブスクリプションページに移動します</center>

*なお、この機能は使用量に応じたプランでのみ利用可能です。そのため、クレジットカードをリンクしてアカウントをアップグレードする必要があります。幸い、InfluxDB Cloudは新規ユーザー向けに250ドルのクレジットを提供しています。*

#### サブスクリプションの作成

先に進み、Create Subscriptionをクリックします。

![Create an MQTT subscription](https://assets.emqx.com/images/a40642c4d132d380f81df3ad4b1a6fce.jpeg)

<center>MQTTサブスクリプションの作成</center>

統合設定ページには、5つのセクションがあります：

- コンフィグブローカー詳細
- コンフィグセキュリティの詳細
- トピックを購読する
- 書き込み先を設定する
- データ解析のルールを定義する。

ご心配なく、ひとつずつ見ていきましょう。

#### コンフィグブローカー接続

サブスクリプションを作成するには、まずInfluxDBがEMQX Cloud上のターゲットMQTTブローカーに接続する必要があります。

ここでは、EMQX Cloudで作成した接続先を使用します。

![Config Broker Details](https://assets.emqx.com/images/12da6b51e9307af46ac448960a4953d1.jpeg)

<center>コンフィグブローカー詳細</center>

この部分には4つの入力があります：

1. サブスクリプション名：サブスクリプションの名前を任意に設定します。この例では'EMQX'を使用しています。
2. 説明：（オプション）このサブスクリプションに短い説明を付けます。
3. ホスト名またはIPアドレス：Step 1でEMQX Cloudから取得した接続先アドレスです。
4. Port: Step 1でEMQX Cloudから取得した接続ポートです。

#### Config Security Details コンフィグセキュリティの詳細

「SECURITY DETAILS」でBASICを選択し、EMQX Cloudで作成したユーザー名とパスワードを設定します。

![Add credentials for the MQTT connection](https://assets.emqx.com/images/e2293fc6db0b1087bacf506de9def0d6.jpeg)

<center>MQTT接続のための認証情報を追加する</center>

***アドレス、ポート、およびユーザー名/パスワードをダブルチェックします。これらはEMQXクラウドへのMQTT接続を成功させるために不可欠です。***

#### トピックを購読する

接続を設定したら、InfluxDB Cloudにどのトピックをリッスンすべきかを指示する必要があります。

![Add a subscription topic](https://assets.emqx.com/images/96639440a9c149d889241723997f1123.jpeg)

<center>購読トピックを追加する</center>

ここでは、トピック名を指定するだけです。今回のデモでは「influxdb」を使いました。わかりやすいですね。このトピックに送られたデータはすべてInfluxDBクラウドに転送されます。

ここでは明示的なトピック名を使用していますが、InfluxDB Cloud Native Collectorは「+」や「#」などのワイルドカードをサポートしています。実際の使用例ではワイルドカードを使用する方が実用的です。詳しくは[InfluxDB Cloudのドキュメント](https://docs.influxdata.com/influxdb/v2.6/cloud/)をご確認ください。

#### 書き込み先を設定する

「WRITE DESTINATION」の項目は、Bucketが1つしかないため、デフォルトのままにしておいてください。ただし、複数のバケットがある場合は、必ず正しいバケットを選択してください。

![Select the write destination bucket](https://assets.emqx.com/images/6c3d7d76d22438018f5c7e6a1577b4b5.jpeg)

<center>書き込み先のバケットを選択する</center>

#### データ解析ルールの定義

さて、最後のパートです：データ解析ルールを定義する。
InfluxDB Cloud Native Collectorは、3つのデータ形式をサポートしています。このデモでは、JSON形式を使用します。デモではその方が読みやすいからです。


![Define a data parsing rule](https://assets.emqx.com/images/0f6dbc2b7ce34fcfb5c58acd20a3adad.jpeg)

<center>データパースルールを定義する</center>

データ解析ルールでは、JSONデータをInfluxDBの測定値やフィールドに変換する方法について情報を提供する必要があります。

デモでは、温度データが1つしかない非常にシンプルなメッセージを使用することにします。

JSONペイロードのサンプルです：

```
{
  "temperature":25
}
```

TこのJSONメッセージをInfluxDB Cloudのmericに変換するために、以下のマッピングを行う必要があります：

#### TIMESTAMP: 

Timestamp is optional. If not provided, it will use the server's timestamp as default value when inserting data.

#### MEASUREMENT（計測）：

Measurementは、JSONまたは静的な名前からパースすることができます。このデモでは、できるだけシンプルにするために、静的な名前「room_temperature」を使用しています。

#### FIELD:

今回のデモでは、温度だけを含むJSONメッセージを使用したので、名前に「temperature」、JSONパス「$.temperature」を使用して、JSON本体からデータを取得しました。InfluxDB Cloudでは、JSONオブジェクトからデータを取得するためにJSONPathを使用しています。その構文はJSONPathのドキュメントを確認してください。

#### セーブサブスクリプション

最後に、定期購読の保存をお忘れなく。

![Save the subscription](https://assets.emqx.com/images/0a3d895cf64f951194b56769fc635e38.jpeg)

<center>サブスクリプションを保存する</center>

「SAVE SUBSCRIPTION」をクリックし、「THAT'S IT」をクリックします！

#### サブスクリプションが実行されていることを確認する

![Native subscription is running](https://assets.emqx.com/images/472905ccc18a0a057f482b26e139e466.jpeg)

<center>ネイティブサブスクリプションを実行中</center>

ネイティブのサブスクリプションリストに実行中であることが表示されるはずです。

#### 統合の最後ステップ

おめでとうございます！InfluxDB CloudとEMQX Cloudの統合が成功したはずです。EMQX Cloudに送信された温度データは、InfluxDB Cloudのターゲットバケットに継続的に永続化されているはずです。

では、最後のStepに進みましょう。期待通りに動作しているかどうかをチェックします。

## ステップ4：検証

統合が成功したかどうかを知るにはどうしたらいいのでしょうか？簡単な答えです：EMQX Cloud上のMQTTブローカーにメッセージを送り、それがInfluxDBクラウドのダッシュボードに表示されるかどうかを見てみましょう！

#### MQTTクライアントを選択する

適用なMQTTクライアントを使用することができます。このチュートリアルでは、テスト目的に適したユーザーフレンドリーなMQTTデスクトップ・アプリケーションであるMQTTXを使用することにします。

![Create New Connection](https://assets.emqx.com/images/0a1b227fb93b3a9c9a39cde30f00cf9f.jpeg)

<center>新規接続の作成</center>

#### EMQXクラウドに接続する

MQTTXの「New Connection」をクリックし、接続フォームに必要事項を入力します：

![Set Connection Details](https://assets.emqx.com/images/006caa8977541d5da34f6887adf99dac.jpeg)

<center>接続の詳細を設定する</center>

1. 名前：接続名です。お好きな名前をお使いください。
2. ホスト：MQTTブローカーの接続アドレスです。InfluxDB Cloudのセットアップで使用したものと同じです。
3. ポートです：MQTTブローカー接続ポート。InfluxDB Cloudのセットアップで使用したものと同じです。
4. ユーザー名/パスワード：デモでは、「InfluxDB Cloud Configuration」と同じ認証情報を使用しています。必要であれば、EMQX Cloudで新しい認証情報を追加することができます。

右上の「接続」ボタンをクリックすると、接続が設定されるはずです。

#### Cloud EMQX Cloudにメッセージを送る

これで、このツールを使ってEMQX Cloud上のMQTTブローカーにメッセージを送ることができるようになりました。

![Send messages to EMQX Cloud](https://assets.emqx.com/images/c1eb827964cb4cd76ddf6315415ea4cd.jpeg)

<center>EMQX Cloudにメッセージを送る</center>

入力：

1. ペイロードフォーマットを "JSON "に設定する。
2. トピック：influxdb（先ほど設定したInfluxDBサブスクリプションのトピック）を設定します。
3. JSON本体です：

   ```
   {"temperature": 25}
   ```

右側の「送信」アイコンをクリックします。温度の値を変更し、より多くのデータをMQTTブローカーに送信することができます。データが多いほど、ダッシュボードに表示されるチャートはリッチなものになります。



#### InfluxDB Cloud上のデータを確認する。

さて、いよいよInfluxDB Cloud上でデータを表示します。MQTTXを使って送信したデータは、EMQX Cloudに入り、InfluxDB Cloudのターゲットバケットに永続化されるのが理想的です。

![Go to Data Explorer](https://assets.emqx.com/images/9637a3dd3ff93d0afa9784221b8f833c.jpeg)

<center>データエクスプローラーに移動する</center>

InfluxDB Cloudに戻り、左メニューの「Data Explorer」アイコンをクリックして、データエクスプローラーを開いてみましょう。

![Make a Query to Fetch the Data](https://assets.emqx.com/images/8f9e088b096f9357b8e54e9a9aa10b76.jpeg)

<center>データを取得するためのクエリーを作成する</center>

UI上でFROM, MEASUREMENTを設定してクエリを作成し、送信ボタンをクリックすると、データのグラフが表示されるはずです。これでEMQX Cloudに送ったデータがInfluxDB Cloudに正常に永続化されたことが証明されました。

## 概要

EMQX Cloud を使えば、1行のコードも書かずに、標準のMQTTプロトコルを使ってあらゆるデバイスやクライアントからデータを取得し、InfluxDBクラウドにデータを保存してIoTアプリケーションの作成に集中することができるのです。

EMQX CloudやInfluxDB Cloudのサービスを、新しいNative MQTTコレクターで活用すれば、10分もかからずに、取り込みから永続化までの完全なデータフローを実現できます。
