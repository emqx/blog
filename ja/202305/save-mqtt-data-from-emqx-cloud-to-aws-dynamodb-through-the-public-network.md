[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)は、高速で予測可能なパフォーマンスとシームレスなスケーラビリティを提供する、フルマネージドのNoSQLデータベースサービスです。DynamoDBは、分散型データベースの運用とスケーリングの管理負担を軽減し、ハードウェアのプロビジョニング、設定と構成、レプリケーション、ソフトウェアのパッチ適用、クラスタのスケーリングに悩まされることがない。また、DynamoDBは静止時の暗号化機能を備えており、機密データの保護に伴う運用負荷や複雑さを解消します。

今回は、温度と湿度のデータをシミュレーションし、MQTTプロトコルでEMQX Cloudに報告した後、EMQX Cloudのデータ統合でNATゲートウェイを有効にして、公衆回線経由でAWS DynamoDBにデータを保存します。


## EMQX Cloudの紹介

[EMQX Cloud](https://www.emqx.com/ja/cloud) は、EMQが提供する世界初のIoT向けフルマネージドMQTT 5.0パブリッククラウドサービスです。EMQX Cloudは、ワンストップのO&Mコロケーションと、MQTTサービスのための独自の隔離された環境を提供します。Internet of Everythingの時代において、EMQX Cloudは、業界アプリケーションを迅速に構築し、IoTデータの収集、送信、計算、永続化を容易に実現することができます。

![MQTT Cloud](https://assets.emqx.com/images/e9d345da71dafee76364773a52aa2d5b.png)

EMQX Cloudは、クラウド事業者が提供するインフラにより、世界数十の国や地域で利用でき、5GやInternet of Everythingのアプリケーションに、低コストで安全かつ信頼性の高いクラウドサービスを提供します。

詳細は、EMQX Cloudのウェブサイトを参照するか、[EMQX Cloudのドキュメント](https://docs.emqx.com/en/cloud/latest/)を参照してください。


## デプロイメントを作成する

### EMQXクラスタの作成

ログイン後、アカウントメニューの「Cloud Console」をクリックすると、新しいデプロイメントを作成するための緑色のボタンが表示されるようになります。EMQX Cloudでは、スタンダードプランとプロフェッショナルプランの14日間の無料トライアルを提供しています。このチュートリアルでは、プロフェッショナルデプロイメントをデモとして使用します。

![Standard and Professional plans](https://assets.emqx.com/images/a677465d0b1e4e3198dd40db0aa41302.png)

EMQX CloudのAWSデプロイメントを作成し、これ以外の設定はデフォルトにします。

![Create an AWS deployment](https://assets.emqx.com/images/6a42f07776ec3ff43bb946c79fef53b4.png)

ステータスが「実行中」になると、配置の作成が完了します。

![status is Running](https://assets.emqx.com/images/8a510a043c0020ba4ba365543d277af6.png)

### DynamoDBインスタンスの作成

初めてDynamoDBインスタンスを作成する場合は、[ヘルプドキュメント](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html)を参照してください。まず、DynamoDBコンソールに移動し、Create Tableをクリックします。

![Create DynamoDB instances](https://assets.emqx.com/images/636f8df7b4a76eb422e38b3b3d4fb799.png)

テーブル名、パーティションキーなどの主要な情報を記入し、実際のビジネスニーズに応じて設定することができます。

![Create DynamoDB Table](https://assets.emqx.com/images/3840e3fe5a6e2b78b51440d23e34fc92.png)

テーブルのステータスがアクティブになるまで、テーブル「temp_hum」の作成が成功したことを意味します。

![the status of the table is active](https://assets.emqx.com/images/7171f7218d31572a1ded15b35cd7b597.png)


## NAT Gatewayを有効にする

[NAT gateways](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html#service-activation) は、ネットワークアドレス変換サービスを提供し、VPCピアリング接続を必要としないパブリックネットワークリソースにアクセスする機能をプロフェッショナル展開に提供することができます。

![Enable NAT Gateway](https://assets.emqx.com/images/2fb42ab1f156ddcc0c68caaf8123a898.png)


## [**データ統合**](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_confluent.html)

1. **DynamoDBリソースの作成**

   「Data Integrations」ページに移動します。データ統合ページで、DynamoDBリソースをクリックします。

   ![Go to the Data Integrations page](https://assets.emqx.com/images/2a86021226602deb01c3798219015c54.png)

   DynamoDB接続の詳細を入力し、testをクリックします。テストに失敗した場合は、DynamoDBサービスを確認してください。テストに合格したらNewボタンをクリックすると、Create Resource successfullyというメッセージが表示されます。

   ![Fill in the DynamoDB connection details](https://assets.emqx.com/images/af520c4f69ab99db72e71751c9d84255.png)

2. **新しいルールを作成する**

   リソースが正常に作成されたら、データ統合ページに戻り、新しく作成したリソースを探し、create ruleをクリックします。我々の目標は、temp_hum/emqxトピックに監視情報がある限り、エンジンがトリガーされるようにすることです。ここでは、特定のSQL処理が必要です：

   - トピック "temp_hum/emqx"のみを対象とする。
   - 必要な3つのデータ（温度、湿度）を取得する

   以上の原則に従えば、最終的に得られるSQLは次のようになるはずです：

   ```
   SELECT 
   id as msgid,
   topic, 
   payload 

   FROM "temp_hum/emqx"
   ```

   ![Create a new rule](https://assets.emqx.com/images/c7306a3bf30d19b001b728fd411654f4.png)

   SQL入力ボックスの下にある「SQLテスト」をクリックすると、データを入力することができます：

   - topic: temp_hum/emqx
   - payload:

   ```
   {
     "temp": 26.3,
     "hum": 46.4
   }
   ```

   Testをクリックすると、取得したデータ結果が表示されます。設定が正しければ、テスト出力ボックスは以下のように完全なJSONデータを取得するはずです：

   ![JSON data](https://assets.emqx.com/images/fb27de726b5ff92095e96d20c4e623ba.png)

   テストが失敗した場合は、SQLが準拠しているか、テストでのトピックと記入されたSQLが一致しているかなどをご確認ください。

3. **ルールにアクションを追加する**

   ルールの設定が完了したら、［次へ］をクリックしてアクションを設定・作成します。次に、以下のようにフィールドとタグを入力します：

   ```
    DynamoDB Table：temp_hum
    Hash Key：msgid
   ```

   ![Add Action to Rule](https://assets.emqx.com/images/ded28a8f05a43995295f78a966b46de4.png)


## 検証

1. **MQTTXを使って、データ報告のシミュレーションを行う。**

   メッセージの購読・発行には、クロスプラットフォームのMQTT 5.0デスクトップクライアントである[MQTTX](https://mqttx.app/)を使用することをお勧めします。

   追加ボタンをクリックし、デプロイメント情報を入力してデプロイメントに接続します。[broker.emqx.io](http://broker.emqx.io/)を作成したデプロイメントの[接続アドレス](https://docs.emqx.com/en/cloud/latest/create/overview.html#view-deployment-information)に置き換える必要があります。EMQX Cloudコンソールに[クライアント認証情報](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication)を追加します。トピック名とペイロードメッセージを入力して、メッセージを発行します。 

   ![MQTTX](https://assets.emqx.com/images/3d3ba6a7cf7228c0661beb4a15c5f20f.png)

2. **ルールモニタリングの表示**

   ルール監視を確認し、成功回数に1回追加する。

   ![View rules monitoring](https://assets.emqx.com/images/06f122a35e4e61e877fb3a9db7681248.png)

3. **で検索した結果を表示しています。**

   Amazon DynamoDBの[NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)は、モダンなデータベース開発と運用のクロスプラットフォームなクライアントサイドGUIアプリケーションです。DynamoDBに接続するために利用できます。

   ![connect to DynamoDB](https://assets.emqx.com/images/77dc1296b979eba6802b06de15d5fa4c.png)

   Operation Builderのページに移動します。テーブル 'temp_hum' を選択します。ここでは、温度と湿度のデータ転送の結果を確認することができます。

   ![Go to the Operation Builder page](https://assets.emqx.com/images/26a7cb6c8ec5196ad5b2c7562d520e3c.png)


## まとめ

これまで、EMQX Cloudデータ統合を使用して、データの全プロセスをパブリックネットワーク経由でAWS DynamoDBに保存しました。その後、AWSサービスと統合して、内蔵ツールを使って分析を実行し、洞察を抽出し、トラフィックの傾向を監視するなど、データでより多くのことを行うことができ、IoTアプリケーションの構築に集中する時間を節約することができます。
