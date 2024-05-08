## はじめに

今日の高速で変化の激しい世界では、リアルタイムでデータを取得・処理する能力は、企業が業務を最適化し、情報に基づいた意思決定を行うために不可欠です。ここで、MQTT（Message Queuing Telemetry Transport）とオープンソースのカラムナ型データベース管理システムであるClickHouseの強力な組み合わせが役立ちます。

このブログ記事では、MQTTとClickHouseの統合がいかにしてデータ分析の力を解き放ち、これらの多様な業界でパフォーマンスの向上を促進できるかを探ります。

## MQTTとClickHouseについて

[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、IoTアプリケーション向けに特別に設計されており、デバイス間の効率的で信頼性の高い通信を可能にします。軽量のパブリッシュ・サブスクライブ・モデルを採用しているため、リソースが制限された環境でもシームレスなデータ伝送を確保できます。MQTTの低オーバーヘッドとリアルタイムデータ・ストリーミングのサポートにより、IoTデータを様々なエンドポイントからデータ処理プラットフォームへ取り込み、伝送するのに理想的な選択肢となります。

ClickHouseは、オンライン分析処理（OLAP）用の高性能なカラム指向のSQLデータベース管理システム（DBMS）で、最小限のレイテンシーで大量のデータを処理・分析することに優れています。カラムナ型のストレージ形式と並列クエリ実行により、データの取得と集計が最適化され、超高速の分析機能を実現しています。ClickHouseは拡張性に優れていることで知られており、組織がIoTデバイスから生成される増大し続けるデータ量を処理しながら、卓越したパフォーマンスを維持できるようにします。

## MQTTとClickHouseの統合によるメリット

MQTTを通信レイヤーとすることで、IoTデバイスからのデータをClickHouseに簡単に転送し、その高性能な分析機能で効率的に保存・処理することができます。

[EMQX](https://www.emqx.com/ja/products/emqx)は最も人気のある[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)です。そのすぐに使えるデータ統合機能により、MQTT-ClickHouseソリューションをシームレスに実現し、いくつかのメリットをもたらすことができます。

- **リアルタイムのデータストリーミング**: EMQXは、リアルタイムのデータストリームを処理するために構築されており、ソースシステムからClickHouseへの効率的で信頼性の高いデータ伝送を確保します。これにより、企業はリアルタイムでデータを取得・分析できるため、即時の洞察とアクションが必要なユースケースに最適です。
- **高性能とスケーラビリティ**: EMQXの分散アーキテクチャとClickHouseのカラムナ型ストレージ形式により、データ量の増加に合わせてシームレスにスケーリングできます。これにより、大規模なデータセットを扱う場合でも、一貫したパフォーマンスと応答性が保証されます。
- **データ変換の柔軟性**: EMQXは強力なSQLベースのルールエンジンを提供し、ClickHouseにデータを保存する前にデータを前処理することができます。フィルタリング、ルーティング、集計、エンリッチメントなど、様々なデータ変換メカニズムをサポートしているため、組織のニーズに合わせてデータを整形できます。
- **導入と管理が容易**: EMQXは、データソース、データの前処理ルール、ClickHouseのストレージ設定を構成するためのユーザーフレンドリーなインターフェイスを提供します。これにより、データ統合プロセスの設定と継続的な管理が簡素化されます。
- **高度な分析**: ClickHouseの強力なSQLベースのクエリ言語と複雑な分析関数のサポートにより、ユーザーはIoTデータから貴重な洞察を得ることができ、予測分析、異常検知などを実現できます。

![MQTT to ClickHouse](https://assets.emqx.com/images/dd545e1d69ce3b4ba3f63ca4287da992.png)

EMQXのデータ統合機能を活用することで、組織はデータ統合ワークフローを合理化し、リアルタイムのデータを取得し、データのセキュリティを確保し、ClickHouseで効率的にデータを保存・分析することができます。これは、データの潜在力を最大限に活用し、データ主導の洞察と意思決定を推進しようとする人々にとって強力なツールとなります。

## 様々な業界におけるユースケース

1. **産業用IoTと予知保全**: MQTTとClickHouseの統合により、機械、センサー、生産ラインからのデータをリアルタイムに監視・分析できます。温度、振動、稼働状況などのデータを収集・分析することで、機器の故障やメンテナンスの必要性を示す異常やパターンを検出できます。これにより、予防保全、ダウンタイムの短縮、生産プロセスの最適化が可能になります。
2. **環境モニタリング**: MQTTとClickHouseの統合により、環境センサー、気象ステーション、大気質モニタリング機器からリアルタイムにデータを収集・分析できます。このユースケースは、農業、林業、汚染管理、気候モニタリングの分野で応用されています。組織は、このデータを活用して、灌漑、作物の健康状態、資源管理、環境保全に関する情報に基づいた意思決定を行うことができます。
3. **エネルギー管理とグリッド最適化**: MQTTとClickHouseの統合により、スマートメーター、再生可能エネルギー源、グリッドインフラからのエネルギー消費データをリアルタイムに監視・分析できます。これにより、効果的なエネルギー管理、負荷分散、デマンドレスポンス、再生可能エネルギー源のグリッドへの統合が可能になります。
4. **物流とサプライチェーンの最適化**: MQTTとClickHouseの統合は、GPSトラッカー、温度センサー、在庫管理システムなどのIoTデバイスからのデータを監視・分析するために、物流とサプライチェーン管理に適用できます。これにより、リアルタイムの追跡、ルート最適化、需要予測、効率的な在庫管理が可能となり、業務の合理化とコスト削減につながります。

## EMQXを使ってMQTTをClickHouseに統合する

これは、IoTベースの車の充電ステーションのデモです。EMQXを使用して充電ステーションに接続し、MQTTを使用してそれらの状態とデータを送信します。データはClickHouseに保存され、注文数、充電時間、充電状態のリアルタイムなモニタリングと分析に使用され、充電ステーションの使用頻度と充電需要に関する洞察を提供します。

また、充電ステーションの稼働率を追跡して、その運用効率を評価することもできます。これは、市場運営のための貴重な意思決定情報となります。

EMQX、ClickHouse、関連するデータ分析・可視化ツールを統合することで、充電ステーションの状態とデータをリアルタイムで監視し、データ分析と意思決定をサポートする強力な車の充電ステーション管理システムを構築できます。

### 前提条件

- Git
- Docker Engine：v20.10以上
- Docker Compose：v2.20以上

### 仕組み

これは、以下の主要コンポーネントを利用したシンプルで効果的なアーキテクチャです。

| 名称                                                     | バージョン | 説明                                                         |
| :------------------------------------------------------- | :--------- | :----------------------------------------------------------- |
| [EMQX Enterprise](https://www.emqx.com/ja/products/emqx) | 5.5.1+     | MQTTクライアントとClickHouseの間のメッセージ交換に使用されるMQTTブローカー。 |
| [MQTTX CLI](https://mqttx.app/ja/cli)                    | 1.9.9+     | テスト用のシミュレーションデータを生成するために使用されるコマンドラインツール。 |
| [ClickHouse](https://clickhouse.com/)                    | 23.6.1     | 充電ステーションのIoTデータの保存と管理、およびGrafanaに時間集計と分析機能を提供する。 |
| [Grafana](https://grafana.com/)                          | 9.5.1+     | 収集したデータを表示・分析するために利用される可視化プラットフォーム。 |

### プロジェクトをローカルにクローンする

Gitを使って、[emqx/mqtt-to-clickhouse](https://github.com/emqx/mqtt-to-clickhouse)リポジトリをローカルにクローンします。

```shell
git clone https://github.com/emqx/mqtt-to-clickhouse
cd mqtt-to-clickhouse
```

コードベースは4つの部分で構成されています。

- `emqx`フォルダには、EMQXの起動時にルールとデータブリッジを自動的に作成するためのEMQX-Clickhouse統合設定が含まれています。
- `clickhouse`フォルダには、テーブル初期化用のSQLファイルが含まれています。
- `mqttx/charging.js`ファイルには、充電と輸送の車両をシミュレートして実際のデータを公開するためのスクリプトが含まれています。
- `docker-compose.yml`は、ワンクリックでプロジェクトを起動するために、すべてのコンポーネントを編成します。

### MQTTX CLI、EMQX、ClickHouseの起動

[Docker](https://www.docker.com/)がインストールされていることを確認し、Docker Composeをバックグラウンドで実行してデモを開始します。

```shell
docker-compose up -d
```

MQTTX CLIは、OCPPプロトコルに基づく5つの充電ガンのEMQXへの接続をシミュレートします。48時間前からシミュレーションを開始し、MQTTを介して充電開始と終了のメッセージ（充電オーダー）を公開し、充電プロセス中に各オーダーの電力、電圧、メーター値、充電時間などのデータを定期的に報告します。EMQXは2つのルールを作成して、充電ステーションとClickHouseを統合します。

![EMQX Flows](https://assets.emqx.com/images/309789c5489dbae7b853565978bff37d.png)

次に、これらのメッセージの構造と、EMQXがルールエンジンとデータ統合機能を通じてそれらをClickHouseに書き込む方法を示します。

### 充電開始メッセージの処理

**トピック**

```
mqttx/simulate/charge/{clientId}/StartTransaction
```

**メッセージ例**

```json
{"messageType":"Call","action":"StartTransaction","payload":{"connectorId":"f788a12a-1b7d-4205-9d8e-37307aae366a","transactionId":"6b738341-b9f3-4d42-adb8-9696e0b8aba6","idTag":"No. 2","timestamp":1710801744456,"reservationId":null,"stackLevel":0,"meterStart":20184.628600000484}}
```

ClickHouseはこのイベントを保存する必要はなく、充電プロセスが完了した後に保存を実行します。そのため、このステップでは対応するルールを作成する必要はありません。

### メーター値メッセージの処理

**トピック**

```
mqttx/simulate/charge/{clientId}/MeterValues
```

**メッセージ例**

```json
{"messageType":"Call","action":"MeterValues","payload":{"connectorId":"96b44678-186a-46b1-8c33-ef0be75600bb","transactionId":"45cb5c1a-f5f7-4dd9-b0ad-9e322e1cacd0","timestamp":1710811934439,"meterValue":{"voltage":450,"currentInput":126.67,"power":57,"meter":0.1583,"currentTemperature":97}}}
```

**EMQXルールSQL**

充電プロセスの間、充電設備は定期的にMeterValuesデータを送信し、充電量、電圧、電流などの計量データを提供します。EMQXは、MeterValuesデータを処理し、電力使用パターンを分析するためにClickHouseに書き込むルールを作成します。ブラウザで`http://localhost:18083`を開いてEMQX Dashboardにアクセスし、Integration→Rulesページに移動して、EMQXの[組み込みSQL関数](https://docs.emqx.com/en/enterprise/v5.5/data-integration/rule-sql-builtin-functions.html)を利用してカスタム処理を行うようにこのルールを変更することもできます。

```sql
SELECT
  payload.payload as record,
  record.meterValue as meterValue
FROM
  "mqttx/simulate/charge/+/MeterValues"
```

**EMQX ClickHouseデータ統合**

ルールを通じてデータを処理した後、EMQXはルールアクションを使用して、メーター値データをリアルタイムでClickHouseに書き込みます。

EMQXは、データ挿入用のSQLテンプレートを使用してClickHouseとのデータ統合をサポートしており、複雑なデータ構造に適応し、柔軟なデータ書き込みとビジネス開発を実現できます。

EMQXは、以下のSQLテンプレートを使用して、充電ガンと充電オーダーに基づいて各充電データを保存します。

```sql
INSERT INTO charging_record (
  connectorId,
  transactionId,
  timestamp,
  voltage,
  currentInput,
  power,
  meter,
  currentTemperature
) VALUES (
  '${record.connectorId}',
  '${record.transactionId}',
  toDateTime(${record.timestamp}/1000),
  ${meterValue.voltage},
  ${meterValue.currentInput},
  ${meterValue.power},
  ${meterValue.meter},
  ${meterValue.currentTemperature}
)
```

### 充電停止メッセージの処理

**トピック**

```
mqttx/simulate/charge/{clientId}/StopTransaction
```

**メッセージ例**

```json
{"messageType":"Call","action":"StopTransaction","payload":{"lastChargeStart":null,"startPower":160,"power":152,"voltage":650,"startTimestamp":1710733474521,"endTimestamp":1710814724521,"timePercentage":1.000123076923077,"currentTimestamp":1710814734521,"pauseDuration":0,"isPaused":false,"counter":272,"meterStart":26987.776999999107,"meter":2634.7483999998626,"connectorId":"829f3fad-2cb0-4dc3-8dac-e703a9d74fe1","currentTemperature":94,"transactionId":"9f1c88c1-6bc5-4cf5-afdc-bd0bb63d861c","idTag":"No. 4","timestamp":1710814734521,"meterStop":29622.52539999897,"duration":81250,"reason":"SoftStop"}}
```

**EMQXルールSQL**

EMQXは、充電停止メッセージデータを処理し、ClickHouseでオーダーを作成できるルールを作成します。ブラウザで`http://localhost:18083`を開いてEMQX Dashboardにアクセスし、Integration→Rulesページに移動して、EMQXの組み込みSQL関数を利用してカスタム処理を行うようにこのルールを変更することもできます。

```sql
SELECT
  payload.payload as record
FROM
  "mqttx/simulate/charge/+/StopTransaction"
```

**EMQX ClickHouseデータ統合**

ルールを通じてデータを処理した後、EMQXは以下のテンプレートを使用してルールアクションでオーダーをClickHouseに書き込みます。

```sql
INSERT INTO charging_order (
  idTag, 
  connectorId,
  transactionId,
  startTimestamp,
  endTimestamp,
  duration,
  reservationId,
  stackLevel,
  meterStart,
  meterStop,
  meter,
  stopReason
) VALUES (
  '${record.idTag}', 
  '${record.connectorId}',
  '${record.transactionId}',
  toDateTime(${record.startTimestamp} / 1000),
  toDateTime(${record.endTimestamp} / 1000),
  ${record.duration},
  '',
  0,
  ${record.meterStart},
  ${record.meterStop},
  ${record.meter},
  '${record.reason}'
)
```

### EMQXからデータをサブスクライブする

Docker Composeには、すべての充電データを出力するサブスクライバーが含まれています。以下のコマンドでデータを表示できます。

```shell
$ docker logs -f mqttx [3/20/2024] [4:05:01 AM] › topic: mqttx/simulate/charge/mqttx_0f8a625b_1/MeterValues payload: {"messageType":"Call","action":"MeterValues","payload":{"connectorId":"d04890fe-76ef-43de-a31b-4e6362bd872f","transactionId":"5a281373-6faa-4ab0-b6d5-56915716a528","timestamp":1710851484421,"meterValue":{"voltage":650,"currentInput":365.38,"power":237.5,"meter":0.6597,"currentTemperature":92}}}
```

任意の[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)（MQTTX CLIなど）を使用して、データをサブスクライブおよび受信できます。

```shell
mqttx sub -t mqttx/simulate/charge/+/+
```

### Grafanaで充電ステーションのデータを表示する

Grafanaダッシュボードで充電ステーションのデータを表示するには、ブラウザで`http://localhost:3000/`を開き、ユーザー名`admin`とパスワード`public`でログインしてください。

ログインに成功したら、ホームページのナビゲーションバーにある「Dashboards」ページをクリックします。次に、「ClickHouse - Charging Station」ダッシュボードを選択します。このダッシュボードには、充電ステーションの現在のオーダー数、収益状況、消費電力、切断された充電ガンの統計、1時間ごとの消費電力など、主要な指標が表示されます。

これらの指標により、充電ステーションの運用状況を可視化して監視し、効率と収益性を向上させるために必要な調整や最適化を行うことができます。リアルタイムの監視でも、過去のデータを表示する場合でも、このダッシュボードは充電ステーションの運用に関するより良い洞察を得るのに役立ち、意思決定プロセスを強力にサポートします。

![Charging Station Data in Grafana](https://assets.emqx.com/images/07736d084a67b500cc10f753c638db15.png)

## まとめ

MQTTの汎用性とリアルタイム性に、ClickHouseのデータ保存と分析力を組み合わせることで、様々な業界がIoTデータを活用して運用効率の向上、コスト削減、データ主導の意思決定を実現できます。EMQXのデータ統合機能により、組織は信頼性が高くスケーラブルで機能豊富なMQTTブローカーの恩恵を受け、この強力な組み合わせを簡単に実現できます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
