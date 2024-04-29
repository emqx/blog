## はじめに

IoTの世界では、デバイスの運用の安全性と効率性を確保するために、さまざまなデバイスデータやイベントをリアルタイムで監視することが重要です。

このブログでは、MQTTを活用してさまざまなタイプのデバイスデータを収集し、Webhookとシームレスに統合するプロセスを詳しく説明します。この統合により、リアルタイムデータのシームレスな送信と処理を実現します。

## IoTにおけるMQTTからWebhookへの統合のメリット

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、軽量なpublish/subscribeメッセージングプロトコルで、特に帯域幅が制限されていたり、接続が不安定だったりする環境でのネットワーク間の効率的な通信に適しています。

Webhookは、トランスポートプロトコルにHTTPを利用するコールバックメカニズムです。Webhookを通じて、MQTTメッセージやクライアントイベントを指定されたサーバーにリアルタイムで迅速にプッシュできます。この動的なデュオは、デバイスデータのリアルタイム監視を促進するだけでなく、障害発生時のアラーム発信など、デバイスの状態に基づいてさまざまなビジネスプロセスを自動化することを可能にします。

IoTアプリケーションにおいて、Webhookは独特の利点を持っています：

- **広範なデータ配信：** Webhookは、分析プラットフォームやクラウドサービスなど、多様な外部システムにMQTTデータをシームレスに統合し、複数システムへのデータ配信を容易にします。
- **リアルタイム応答とビジネストリガー：** Webhookを活用することで、外部システムはMQTTデータを迅速に受信し、リアルタイムのビジネスプロセスをトリガーできます。特にアラームデータの受信やビジネスワークフローの開始など、この迅速な応答能力は非常に価値があります。
- **カスタマイズされたデータ処理：** 外部システムは、受信したデータを独自の要件に応じて処理することが可能になります。これにより、MQTTブローカーの機能の制限に縛られることなく、複雑なビジネスロジックを実装できます。
- **疎結合の統合：** Webhookは、シンプルなHTTPインターフェースを利用した疎結合のシステム統合アプローチを採用し、シームレスな統合を実現し、システム全体の相互運用性を高めます。

本質的に、MQTTとWebhookの融合は、IoTアプリケーションに堅牢で柔軟かつリアルタイムのデータ処理と送信ソリューションを提供します。データ統合方法を適切に選択し、設定することで、多様なIoTアプリケーションのニーズを満たし、IoT全体の効率性と使いやすさを向上させることができます。

## EMQXを使ったMQTTからWebhookへの統合

[EMQX MQTTプラットフォーム](https://www.emqx.com/ja/products/emqx)は、Webhookデータ統合に強力な機能を提供し、MQTTデバイスのイベントとデータを分析プラットフォームやクラウドサービスなどの外部システムにシームレスに統合します。これにより、複数システムへのデータ配信が可能となり、リアルタイムモニタリングやイベント応答の要求に対応できます。

リクエストメソッドやリクエストデータフォーマットの柔軟な設定をサポートし、HTTPSを介した安全な通信や認証メカニズムを提供します。クライアントのメッセージやイベントデータをリアルタイムで効率的かつ柔軟に送信できるため、IoTデバイスの状態通知、アラート通知、データ統合などのシナリオを実現できます。

webhookを使用することで、ユーザーは好みのプログラミング言語やフレームワークでコードを記述し、カスタマイズされた柔軟で複雑なデータ処理ロジックを実装できます。

![MQTT to Webhook](https://assets.emqx.com/images/8fde6a1aecf0cda8229181030c4d0549.png)

## MQTTからWebhookへの統合デモの準備

### 前提条件

- Git
- Docker Engine：v20.10+
- Docker Compose：v2.20+

### 仕組み

これは、以下の主要コンポーネントを使用したシンプルで効果的なアーキテクチャです：

| コンポーネント名                                         | バージョン | 説明                                                         |
| :------------------------------------------------------- | :--------- | :----------------------------------------------------------- |
| [EMQX Enterprise](https://www.emqx.com/ja/products/emqx) | 5.5.0+     | MQTTデバイスを接続し、デバイスイベントとメッセージデータをWebhookサービスに送信するためのMQTTブローカー。 |
| [MQTTX CLI](https://mqttx.app/ja/cli)                    | 1.9.3+     | EMQXへのデバイス接続をシミュレートし、メッセージを発行するためのコマンドラインツール。 |
| [Node.js](https://nodejs.org/)                           | 18.17      | EMQXからのデータリクエストを処理するWebhookサービスを実行するためのランタイム環境。 |

### プロジェクトをローカルにクローンする

Gitを使って[emqx/mqtt-to-webhook](https://github.com/emqx/mqtt-to-webhook)リポジトリをローカルにクローンします：

```shell
git clone https://github.com/emqx/mqtt-to-webhook
cd mqtt-to-webhook
```

コードベースは3つの部分で構成されています：

- `emqx`フォルダには、EMQXの起動時にルールとデータブリッジを自動的に作成するためのEMQX-Webhook統合設定が含まれています。
- `webserver`フォルダには、サンプルWebhookサービス用のNode.jsコードが含まれています。
- `docker-compose.yml`は、ワンクリックでプロジェクトを起動するためにすべてのコンポーネントを編成します。

## MQTTX CLI、EMQX、Webhookの起動

[Docker](https://www.docker.com/)がインストールされていることを確認し、Docker Composeをバックグラウンドで実行してデモを開始します：

```shell
docker-compose up -d
```

このサンプルサービスにはいくつかの主要なコンポーネントが含まれており、以下でより詳しく説明します。

### デバイスのサブスクリプションとメッセージのパブリッシュをシミュレート

このサンプルでは、[MQTTX CLI](https://mqttx.app/cli)を使用して、テスト目的でデバイスのサブスクリプションとメッセージのパブリッシュをシミュレートしています。

1. デバイスが2つのトピック（t/1とt/2）をサブスクライブしているようにシミュレートします。使用するコマンドは以下の通りです：

   ```shell
   mqttx sub -t t/1 t/2
   ```

2. [simulate](https://mqttx.app/docs/cli/get-started#simulate)コマンドを使用して、デバイスがEMQXに接続し、5秒間隔でトピックmqttx/simulate/tesla/{clientid}にメッセージを定期的にパブリッシュするようにシミュレートします。コマンドは以下のようになります：

   ```shell
   mqttx simulate -sc tesla -c 1 -im 5000
   ```

   任意の[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)は、以下のコマンドを使用して、これらのシミュレートされたメッセージをサブスクライブして受信できます：

   ```shell
   mqttx sub -t mqttx/simulate/tesla/+
   ```

これで、デバイスの動作を正常に再現できました。次のセクションでは、EMQX上でこれらのメッセージやイベントを処理する方法について詳しく説明します。

### デバイスイベントとメッセージの処理

デバイスのサブスクリプションとメッセージのパブリッシュをシミュレートした後は、EMQX上でこれらのデバイスから送信されたメッセージやイベントを処理する番です。この作業は、EMQXのWebhookデータ統合機能によって実現されます。

EMQXは、デバイスから送信されたメッセージと、接続/切断およびサブスクリプション/アンサブスクリプションのイベントを処理するために、2つのWebhookを設定します。その他のクライアントイベントについては、[Webhookのドキュメント](https://docs.emqx.com/en/enterprise/latest/data-integration/webhook.html)を参照してください。

これらの設定を表示または変更するには、ブラウザで次のURLを開きます：`http://localhost:18083`。デフォルトのユーザー名「admin」とパスワード「public」を使用してログインします。その後、Integration → Webhookページに移動します。

![EMQX Webhook](https://assets.emqx.com/images/dfda83a903065e4819540cabdb0db1fd.png)

主な設定は以下の通りです：

- **トリガー：** Webhookを起動するイベントです。メッセージの場合は、「Message Publish」を選択し、トピックmqttx/simulate/#を追加してメッセージをフィルタリングする必要があります。デバイスイベントの場合は、「Connection Established」、「Connection Disconnected」、「Subscription Completed」、「Unsubscription」をチェックします。
- **リクエストメソッド：** 「POST」メソッドを選択します。
- **URL：** Webhookサービスのアドレスで、`http://webserver:3000/events/${event}`と入力する必要があります。ここで、`${event}`は、トリガーされた特定のイベントに基づいて動的に置き換えられるプレースホルダーです。
- **リクエストヘッダー：** リクエストヘッダーを追加し、キーを`Authorization`、値を`Bearer B53498D3-1752-4AA7-BACA-7013309B7468`とします。これは、リクエストでWebhookサービスを認証するために使用されます。

![EMQX Webhook Settings](https://assets.emqx.com/images/5f448e80b5f7aadac95cb44662874766.png)

これらのパラメータが設定されると、WebhookはMQTTクライアントからのイベントとメッセージを正しく受信および処理できるようになります。

EMQXは、Webhookデータ統合機能を通じて、イベントおよびメッセージデータをリアルタイムでWebhookサービスに送信します。Webhookデータ統合は、URL、認証方法、リクエストヘッダー、リクエストメソッド、リクエストボディなど、HTTPリクエストパラメータの動的な設定機能を提供し、さまざまなWebhookサービスとの柔軟なインターフェースを可能にします。

### Webhookサービスによるデータ処理

このブログ記事では、EMQXからのリクエストを受信し、データを効率的に処理するNode.jsベースのWebhookサービスのセットアップ方法を説明します。

1. 接続されたデバイスの追跡。このサービスは、接続したデバイスをログに記録し、接続または切断時にそのオンラインステータスを更新します。
2. デバイスイベント履歴の記録。接続、切断、サブスクリプション、アンサブスクリプションの記録を含むデバイスイベントの履歴を維持します。

完全なコードについては、[こちら](https://github.com/emqx/mqtt-to-webhook/blob/main/webserver/index.js)を参照してください。

これで、EMQX MQTTとWebhookの設定プロセスが完了しました。Webhookサービスは、EMQX上のMQTTデバイスのメッセージとイベントから処理したデータをローカルファイルに保存します。次に、このデータを表示および解釈する方法を説明します。

## Webhookサービスによって記録されたデータへのアクセス

以下のコマンドを使用して、Webhookサービスが提供するインターフェースを通じてデータを表示できます：

```shell
curl http://localhost:3000/events
```

返される例示データは以下のようになります：

```json
{
  "devices": [
    {
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "connected": true,
      "ip": "192.168.228.4:43912",
      "connectedAt": "2024-02-19T09:42:12.952Z"
    },
    {
      "clientId": "mqttx_baf18c96_1",
      "username": "undefined",
      "connected": true,
      "ip": "192.168.228.5:58340",
      "connectedAt": "2024-02-19T09:42:13.020Z"
    }
  ],
  "eventsHistory": [
    {
      "event": "client.connected",
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "peername": "192.168.228.4:43912",
      "options": {
        "proto_ver": 5,
        "keepalive": 60,
        "clean_start": true,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:12.952Z"
    },
    {
      "event": "session.subscribed",
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "options": {
        "topic": "t/2",
        "qos": 0,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:12.963Z"
    },
    {
      "event": "client.connected",
      "clientId": "mqttx_baf18c96_1",
      "username": "undefined",
      "peername": "192.168.228.5:58340",
      "options": {
        "proto_ver": 5,
        "keepalive": 30,
        "clean_start": true,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:13.020Z"
    }
  ],
  "messages": [
    {
      "topic": "mqttx/simulate/tesla/mqttx_baf18c96",
      "payload": "{\"car_id\":\"ZTGZJC1XPFN643051\",\"display_name\":\"Nova's Tesla\",\"model\":\"S\",\"trim_badging\":\"ad\",\"exterior_color\":\"lime\",\"wheel_type\":\"cumque\",\"spoiler_type\":\"aspernatur\",\"geofence\":\"West Ransom\",\"state\":\"online\",\"since\":\"2024-02-18T21:05:53.133Z\",\"healthy\":false,\"version\":\"9.6.6\",\"update_available\":true,\"update_version\":\"2.7.2\",\"latitude\":\"52.1216\",\"longitude\":\"78.0590\",\"shift_state\":\"R\",\"power\":-908,\"speed\":20,\"heading\":96,\"elevation\":1373,\"locked\":true,\"sentry_mode\":true,\"windows_open\":true,\"doors_open\":false,\"trunk_open\":true,\"frunk_open\":true,\"is_user_present\":false,\"is_climate_on\":true,\"inside_temp\":9.1,\"outside_temp\":29,\"is_preconditioning\":false,\"odometer\":744655,\"est_battery_range_km\":394.1,\"rated_battery_range_km\":281.3,\"ideal_battery_range_km\":138.5,\"battery_level\":47,\"usable_battery_level\":43,\"plugged_in\":true,\"charge_energy_added\":94.03,\"charge_limit_soc\":44,\"charge_port_door_open\":false,\"charger_actual_current\":72.98,\"charger_power\":43,\"charger_voltage\":234,\"charge_current_request\":36,\"charge_current_request_max\":25,\"scheduled_charging_start_time\":\"2028-04-25T11:27:22.090Z\",\"time_to_full_charge\":5.34,\"tpms_pressure_fl\":3,\"tpms_pressure_fr\":2.8,\"tpms_pressure_rl\":3.4,\"tpms_pressure_rr\":2.8,\"timestamp\":1708335738038}",
      "qos": 0,
      "clientId": "mqttx_baf18c96_1",
      "createdAt": "2024-02-19T09:42:18.046Z"
    }
  ]
}
```

- **deviceCount：** EMQXサーバーに接続されているデバイスの総数。
- **messageCount：** EMQXサーバーが受信したメッセージの総数。
- **eventsHistoryCount：** EMQXサーバーが記録したイベント履歴の数。
- **devices：** EMQXサーバーに接続されているすべてのデバイスの包括的な詳細を含む配列。
- **eventsHistory：** EMQXサーバーが受信したすべてのデバイスイベント履歴を含む配列。
- **messages：** MQTTサーバーが受信したすべてのメッセージを保持する配列。

これらのデータを使用することで、デバイスの接続性、メッセージの受信、デバイスの動作記録など、アプリケーションの運用状態を全体的に把握することができます。この情報は、EMQXの設定を理解および最適化し、クライアントデータを活用し、デバイスを管理し、動作監査を実施するために重要です。

## WebhookとEMQXの他の統合との比較

Webhookは、リアルタイムのデータ送信と適応性の高いインターフェースを提供し、多様なサービスとの統合を容易にします。開発者は、複雑なプログラミングを必要とせずに、リアルタイムのイベントを処理したり、クラウドストレージ、関数、アラートサービスなどのサードパーティサービスと接続したりすることができます。

しかし、大規模なイベント管理の場合、Webhookは必ずしも最適な選択肢ではないかもしれません。HTTPプロトコルに依存しているため、大量のデータを扱う際にネットワークの遅延や帯域幅の制約に直面する可能性があります。また、サーバーの処理能力が十分でない場合、データ処理の遅延や、データの損失さえも発生する可能性があります。

そのため、大規模なデータ転送やメッセージ保存を検討する際は、EMQXの他のデータ統合方法、例えばデータをデータベースに直接保存する方法などが、より適している可能性があります。この方法は、ネットワークの遅延や帯域幅の問題を回避し、データベースの処理能力を活用して、データを安全に保存し、効率的に処理することができます。運用効率を向上させつつ、システムの安定性とセキュリティを確保するwin-winの方法です。

## 結論

このブログでは、MQTTとWebhookを統合してIoTアプリケーションを拡張する方法を探りました。EMQXをリアルタイムの[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)として活用し、Webhookを利用して外部システムへのデータ転送を行うことで、デバイスデータの収集と処理を包括的に解決しました。

現実の世界では、EMQXとWebhookの設定を調整して、独自の要件に合わせることができます。デバイスデータを分類するために異なる[MQTTトピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)を設定したり、Webhookを設定して深い分析やアクションのためにデータを様々な外部システムに送信したりと、可能性は広がります。

全体的に、EMQX、MQTT、Webhookの組み合わせは、強力で適応性の高いソリューションを提供し、ユーザーがIoTアプリケーションを効果的にスケーリングできるようにします。これらのツールを活用して、IoTの取り組みに新たな可能性を開くためにどのように活用されるのか、楽しみにしています。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
