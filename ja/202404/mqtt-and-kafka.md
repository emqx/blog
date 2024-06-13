## MQTTはKafkaとどのように使われるのか？

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)（Message Queuing Telemetry Transport）は、制約のあるネットワークにおけるデバイス間の効率的な通信のための軽量メッセージングプロトコルです。Apache Kafkaは分散ストリーミングプラットフォームです。大規模なリアルタイムのデータストリーミングと処理を扱うように設計されています。

KafkaとMQTTは相互補完的なテクノロジーであり、IoTデータのエンドツーエンドの統合を可能にします。KafkaとMQTTを統合することで、企業はデバイスとIoTプラットフォーム間の信頼性の高い接続性と効率的なデータ交換を保証する堅牢なIoTアーキテクチャを確立できます。同時に、IoTシステム全体にわたる高スループットのリアルタイムデータ処理と分析も容易になります。

MQTTとKafkaの統合が大きな価値を提供するIoTのユースケースは、[コネクテッドカー](https://www.emqx.com/ja/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know)とテレマティクス、スマートシティインフラ、[産業用IoT](https://www.emqx.com/ja/blog/iiot-explained-examples-technologies-benefits-and-challenges)のモニタリング、物流管理など、多数あります。このブログ記事では、IoTアプリケーションのためのMQTTデータとKafkaのシームレスな統合について探求します。

## KafkaとMQTTはどのようなIoTの課題に対処できるのか？

IoTプラットフォームアーキテクチャを設計する際には、いくつかの課題が発生します：

- **接続性とネットワークの回復力：** コネクテッドカーなどの重要なIoTシナリオでは、データをプラットフォームに送信するためにネットワーク接続に依存しています。アーキテクチャは、断続的な接続、ネットワークの遅延、さまざまなネットワーク条件を処理するように設計されるべきです。
- **スケーリング：** デバイスの数が増えるにつれて、アーキテクチャは、IoTデバイスによって生成されるデータの増加する量を処理するためにスケーラブルでなければなりません。
- **メッセージスループット：** IoTデバイスは、センサーの読み取り値、位置情報などを含む、膨大な量のデータをリアルタイムで生成します。プラットフォームアーキテクチャは、すべてのデータが効率的に収集、処理、適切なコンポーネントに配信されるように、高いメッセージスループットを処理できる必要があります。
- **データ保存：** IoTデバイスは絶え間ないデータストリームを生成し、それを効果的に保存・管理する必要があります。

## IoTアーキテクチャでMQTTをKafkaと統合する必要性

Kafkaは、企業システム間のデータ共有を促進するための信頼性の高いストリーミングデータ処理プラットフォームとしての役割において優れていますが、IoTのユースケースにはあまり理想的ではない特定の制限があります：

- **クライアントの複雑さとリソース集中性：** Kafkaクライアントは、その複雑さとリソース要件で知られています。これは、リソースが制約された小さなIoTデバイスにとって難しい問題で、そのようなデバイスでKafkaクライアントを実行することは、非現実的または非効率的である可能性があります。
- **トピックのスケーラビリティ：** Kafkaは、多数のトピックを処理する際に制限があります。これは、特に多数のデバイスと各デバイスの複数のトピックを伴うシナリオにおいて、大規模なトピック定義を伴うIoVの展開にとって問題となり得ます。
- **信頼性の低い接続性：** Kafkaクライアントは安定したIP接続を必要とし、これは信頼性の低いモバイルネットワーク上で動作するIoTデバイスにとっては難しい点です。これらのネットワークは、断続的な接続の問題を引き起こし、Kafkaが必要とする一貫した通信を妨げる可能性があります。

MQTTをKafkaと統合することで、IoTデバイスの接続シナリオにおけるKafkaの制限の大部分に対処できます：

- **直接アドレス指定：** MQTTはロードバランシングをサポートし、IoTデバイスがロードバランサーを介してKafkaブローカーに間接的に接続できるようにします。
- **トピックのスケーラビリティ：** MQTTは多数のトピックの処理に適しており、大規模なトピック設計を伴うIoTプラットフォームの展開に最適な候補となります。
- **信頼性の高い接続性：** MQTTは信頼性の低いネットワーク上で動作するように設計されており、IoTデバイスと接続のための信頼性の高いメッセージングプロトコルとなります。
- **軽量なクライアント：** [MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)は軽量であるように設計されており、リソースに制約のあるIoVデバイスに適しています。

## 実行可能なMQTT-Kafka統合ソリューションの比較

IoTプラットフォームでMQTTとKafkaを統合する際には、いくつかの実行可能なソリューションが利用可能です。各ソリューションには、それぞれの利点と考慮事項があります。人気のあるMQTT + Kafka統合オプションのいくつかを見ていきましょう：

### EMQX Kafkaデータ統合

[EMQX](https://github.com/emqx/emqx)は、Kafkaデータ統合機能を通じてKafkaとのシームレスな統合を提供する人気の[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)です。MQTTとKafkaの間のブリッジとして、EMQXは2つのプロトコル間のスムーズな通信を可能にします。

この統合により、プロデューサー（Kafkaへのメッセージ送信）とコンシューマー（Kafkaからのメッセージ受信）の2つの役割でKafkaへのデータブリッジを作成できます。EMQXでは、これらの役割のいずれかでデータブリッジを確立できます。双方向のデータ伝送機能により、EMQXはアーキテクチャ設計の柔軟性を提供します。さらに、低遅延と高スループットを提供し、効率的で信頼性の高いデータブリッジ操作を保証します。

EMQX Kafkaデータ統合の詳細については、[Kafkaへのデータストリーム](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html)を参照してください。

### Confluent MQTT Proxy

Confluentは、Kafkaを開発した会社です。そのMQTT ProxyはMQTTクライアントとKafkaブローカーを接続し、Kafkaトピックへのパブリッシュとサブスクライブをできるようにします。このソリューションは、Kafkaブローカーとの直接通信の複雑さを抽象化することで統合プロセスを簡素化します。

現在、このソリューションはMQTTバージョン3.1.1のサポートに限定されており、MQTTクライアントの接続のパフォーマンスがスループットに影響を与える可能性があります。

### オープンソースのMQTTブローカーとKafkaを使用したカスタム開発

[オープンソースのMQTTブローカー](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)を使用することで、ユーザーはMQTTとKafkaを接続する独自のブリッジサービスを開発する柔軟性があります。このブリッジサービスは、MQTTクライアントを使用してMQTTブローカーからデータをサブスクライブし、Kafkaプロデューサー APIを利用してデータをKafkaにパブリッシュすることで構築できます。

このソリューションには、信頼性とスケーラビリティを確保するための開発と保守の努力、および多大な作業が必要です。

## EMQXを使ったMQTTデータのKafkaへの統合

EMQXは、高度にスケーラブルなMQTTブローカーで、IoTプラットフォームのための広範な機能と能力を提供します。EMQXのデータ統合機能により、MQTTデータをApache Kafkaへまたは、Kafkaからの簡単かつ効率的なストリーミングが可能になります。

![Integrating MQTT Data to Kafka with EMQX](https://assets.emqx.com/images/5b982a838b7bb7388ace8fe90500282b.png)

EMQXは、大規模なデバイス接続性を提供します。Kafkaからの高スループットで耐久性のあるデータ処理能力と合わせて、IoTのための完璧なデータインフラストラクチャを提供します。

**EMQXが提供するMQTTからKafkaへの機能には以下のようなものがあります：**

- **双方向の接続：** EMQXは、デバイスからKafkaへのMQTTメッセージのバッチ処理と、バックエンドシステムからKafkaメッセージをフェッチして接続されたIoTクライアントに公開することをサポートします。
- **柔軟なMQTTからKafkaへのトピックマッピング：** 例えば、1対1、1対多、多対多、[MQTTトピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)フィルター（ワイルドカード）を含みます。
- **EMQX Kafkaプロデューサー**は、同期/非同期の書き込みモードをサポートし、レイテンシーとスループットのどちらを優先するかを柔軟に選択できます。
- **リアルタイムのメトリクス**には、メッセージの総数、成功/失敗した配信の数、メッセージレートなどがあり、SQL IoTルールと統合して、メッセージをKafkaやデバイスにプッシュする前にデータを抽出、フィルタリング、エンリッチ、変換します。

### ユースケース例：コネクテッドカーとIoVのためのMQTTとKafkaの活用

MQTT + Kafkaのアーキテクチャは、さまざまな業界のIoTプラットフォームに利点をもたらしますが、コネクテッドカーとInternet of Vehicles（IoV）の分野は、特に魅力的なユースケースです。

![The architecture of MQTT + Kafka](https://assets.emqx.com/images/2ffab2dcda85974f221d815acd9a5972.png)

このアーキテクチャの主なユースケースは以下の通りです：

- **テレマティクスと車両データ分析：** MQTT + Kafkaアーキテクチャは、センサーの読み取り値、GPS位置、燃料消費量、ドライバーの行動など、大規模なリアルタイムの車両データの収集、ストリーミング、分析を可能にします。このデータは、車両の性能モニタリング、予知保全、フリート管理、全体的な運用効率の向上に利用できます。

- **インテリジェントな交通管理：** MQTTとKafkaを統合することで、コネクテッドカー、交通センサー、インフラストラクチャなど、さまざまな交通情報源からのデータを取得・処理できるようになります。これにより、リアルタイムの交通モニタリング、渋滞検知、ルート最適化、スマートな交通信号制御など、インテリジェントな交通管理システムの開発が可能になります。

- **リモート診断：** MQTT + Kafkaアーキテクチャは、コネクテッドカーの高スループットデータ伝送を容易にします。これは、

- プロアクティブなメンテナンスと効率的な問題解決を可能にするリモート診断とトラブルシューティングに活用できます。

  - **エネルギー効率と環境への影響：** MQTT + Kafkaアーキテクチャは、双方向のデータ伝送により、コネクテッドカーをスマートグリッドシステムとエネルギー管理プラットフォームと統合することを可能にします。このユースケースには、リアルタイムのエネルギー消費モニタリング、デマンドレスポンスメカニズム、電気自動車の充電最適化が含まれます。
  - **予知保全：** MQTT + Kafkaアーキテクチャは、車両の健全性とパフォーマンスデータの継続的なモニタリングを可能にします。このユースケースには、高スループットのリアルタイムテレメトリデータ収集、異常検知、予知保全アルゴリズムが含まれます。車両の所有者は、潜在的な問題を事前に特定し、メンテナンス作業をスケジュールすることができます。

## MQTTとKafkaを使ったコネクテッドビークルのストリーミングデータパイプラインを構築する3分ガイド

  このセクションでは、車両デバイスとそのダイナミックなテレマティクスデータをシミュレートし、[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)に接続し、そのデータをApache Kafkaに送信します。組み込みのKafkaデータ統合機能を備えているため、プロセスが簡素化される[EMQX](https://www.emqx.com/ja/products/emqx)をMQTTブローカーとして選択しました。

### 前提条件

  - Git
  - Docker Engine：v20.10+
  - Docker Compose：v2.20+

### 動作の仕組み

![MQTT to Kafka Architecture](https://assets.emqx.com/images/414774fb7f5b20256d52eaf70196798a.jpg)

<center>MQTTからKafkaへのアーキテクチャ</center>

<br>

これは、複雑なコンポーネントを避けたシンプルで効果的なアーキテクチャです。以下の3つの主要コンポーネントを利用します：

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | シミュレートされた車両とテストデータを生成するためのコマンドラインツール。 |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | 車両とKafkaシステム間のメッセージ交換に使用されるMQTTブローカー。 |
| [Kafka](https://kafka.apache.org/)                       | 2.8.0+  | Apache Kafkaは、車両データの取り込み、保存、処理のための分散ストリーミングプラットフォームとして機能します。 |

基本コンポーネントに加えて、EMQXは包括的な観測可能性機能を提供します。システムの実行時に、以下のコンポーネントを使用してEMQXのメトリクスと負荷を監視できます：

| Component Name                                         | Version | Description                                                  |
| :----------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | EMQXのためのPrometheusエクスポーター。                       |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | オープンソースのシステム監視とアラートのツールキット。       |
| [Grafana](https://grafana.com/)                        | 9.5.1+  | 収集されたデータを表示・分析するために利用される可視化プラットフォーム。 |

このプロジェクトの基本的なアーキテクチャを理解したところで、車両を始動させましょう！

### プロジェクトをローカルにクローンする

[emqx/mqtt-to-kafka](https://github.com/emqx/mqtt-to-kafka)リポジトリをローカルにクローンし、サブモジュールを初期化してEMQX Exporter（オプション）を有効にします：

```shell
git clone https://github.com/emqx/mqtt-to-kafka
cd mqtt-to-kafka

# Optional
git submodule init
git submodule update
```

コードベースは3つの部分で構成されています：

- `emqx`フォルダには、EMQXの起動時にルールとデータブリッジを自動的に作成するためのEMQX-Kafka統合設定が含まれています。
- `emqx-exporter`、`prometheus`、`grafana-provisioning`フォルダには、EMQXの観測可能性の設定が含まれています。
- `docker-compose.yml`は、ワンクリックでプロジェクトを起動するために複数のコンポーネントを編成します。

### MQTTX CLI、EMQX、Kafkaの起動

[Docker](https://www.docker.com/)がインストールされていることを確認し、Docker Composeをバックグラウンドで実行してデモを開始します：

```shell
docker-compose up -d
```

これで、MQTTX CLIによってシミュレートされた10台のテスラ車両が、EMQXに接続し、1秒に1回の頻度でトピック`mqttx/simulate/tesla/{clientid}`にステータスを報告します。

実際、EMQXはTeslaからメッセージを取り込むためのルールを作成します。EMQXの[組み込みSQLファンクション](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html)を使用してカスタム処理を追加するために、このルールを後で変更することもできます。

```shell
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

EMQXは、以下の主要な設定で、車両データをKafkaにプロデュースするデータブリッジも作成します：

- Kafkaの`my-vehicles`トピックにメッセージをパブリッシュする
- 各車両のクライアントIDをメッセージキーとして使用する
- メッセージ発行時刻をメッセージのタイムスタンプとして使用する

![Kafka Config](https://assets.emqx.com/images/ad15e9decf2e5be01d712ec0b3aa2090.png)

### EMQXから車両データをサブスクライブ

> このステップはデモにとって特別な意味はなく、MQTTX CLIとEMQXが機能しているかどうかを確認するためだけのものです。

Docker Composeには、すべての車両データを出力するサブスクライバーが含まれています。このコマンドでデータを表示できます：

```shell
$ docker logs -f mqttx
[8/4/2023] [8:56:41 AM] › topic: mqttx/simulate/tesla/mqttx_063105a2
payload: {"car_id":"WLHK53W2GSL511787","display_name":"Roslyn's Tesla","model":"S...
```

任意のMQTTクライアントを使ってデータをサブスクライブ・受信するには：

```shell
mqttx sub -t mqttx/simulate/tesla/+
```

### Kafkaから車両データをサブスクライブ

すべてが正常に機能していれば、EMQXは車両からのデータをリアルタイムでKafkaの`my-vehicles`トピックにストリーミングしています。以下のコマンドを使用して、Kafkaからデータを消費できます：

```shell
docker exec -it kafka \
  kafka-console-consumer.sh \
  --topic my-vehicles \
  --from-beginning \
  --bootstrap-server localhost:9092
```

次のようなJSONデータを受信します：

```shell
{"vin":"EDF226K7LZTZ51222","speed":39,"odometer":68234,"soc":87,"elevation":4737,"heading":33,"accuracy":24,"power":97,"shift_state":"D","range":64,"est_battery_range":307,"gps_as_of":1681704127537,"location":{"latitude":"83.3494","longitude":"141.9851"},"timestamp":1681704127537}
```

このデータは、強力な自己ホスト型のTeslaデータロガーである[TeslaMate](https://github.com/adriankumpf/teslamate)に触発されたものです。データの生成方法については、MQTTX CLIの[スクリプト](https://github.com/emqx/MQTTX/blob/main/scripts-example/IoT-data-scenarios/tesla.js)を参照してください。

### EMQXメトリクスの表示（オプション）

ステップ1でEMQX Exporterを有効にしている場合、クライアント接続、メッセージレート、ルール実行などのEMQXのすべてのメトリクスを忠実に収集します。これはシステムに貴重な洞察を提供します。

EMQXメトリクスをGrafanaダッシュボードで表示するには、ブラウザで`http://localhost:3000`を開き、ユーザー名`admin`、パスワード`public`でログインします。

## まとめ

EMQXをMQTTブローカーとして活用し、EMQXデータ統合を利用してデータをKafkaにストリーミングすることで、ストリーミングデータを蓄積・処理するためのエンドツーエンドのソリューションを作成しました。次に、アプリケーションをKafkaに直接統合して、車両データを消費し、それらを分離することができます。また、Kafka Streamsを活用して、車両データのリアルタイムストリーム処理を実行し、統計分析と異常検知を行うこともできます。その結果は、Kafka Connectを介して他のシステムに出力できます。

MQTT + Kafkaアーキテクチャは、IoTにおいてリアルタイムのデータ収集、スケーラビリティ、信頼性、統合機能を必要とするユースケースに適しています。データのスムーズな流れ、効率的な通信、そしてコネクテッドビークルのエコシステムのためのアプリケーションやサービスなどの革新的なユースケースを可能にします。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
