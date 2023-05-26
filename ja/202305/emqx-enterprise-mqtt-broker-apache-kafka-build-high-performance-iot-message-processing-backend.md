## 背景

各種IoTプロジェクトでは、デバイスが生成するメッセージをデバイスに影響するだけでなく、業務システムで利用して、セキュリティ監査、トラフィックアカウンティング、データ統計、通知トリガーなどの機能を実装する必要がありますが、以下のプロトタイプシステムによって容易に実現できます：


![Artboard.png](https://assets.emqx.com/images/f0c97d9ba28f904ae5c550f2256368d7.png)

このプロトタイプでは、各ビジネスリンクが自分のニーズに応じてEMQXからメッセージデータを取得するために、EMQX上で複数のデータチャネルを維持する必要がある。このソリューションの問題点は

- 各ビジネスは、EMQXとデータチャネルを確立する必要があります。データチャネルの確立と維持は、追加のリソースオーバーヘッドを必要とし、データ同期の速度は、EMQXの高速メッセージ交換に深刻な影響を与えます；
- ビジネスが成長するにつれて、新しいビジネスリンクのたびに、システム全体の変更を伴う必要があります；
- 各リンクの処理速度やタイミングが異なるため、メッセージが大量にある場合、一部のサービスがブロックされ、さらにデータの損失やシステムの安定性低下など深刻な事態を招きます。

上記の問題は、現在のインターネットアプリケーションで遭遇する問題、すなわち複数のビジネスシステム間のデータ統合とデータ同期の問題と非常に一致している。インターネットアプリケーションでは、一般的にメッセージキューを統合して、ピーククリッピング、電流制限、キュー処理などのオペレーションを行い、データとサービスの切り離しを行う。EMQXが提供するRabbitMQ、Kafka、RocketMQ、Pulsarなどのメッセージ・ストリーム・ミドルウェアのブリッジ機能を利用すれば、IoTプロジェクトもこのモデルを使って上記の問題を解決することができます。

本稿では、一般的なIoTの利用シーンを例に、EMQXメッセージミドルウェアとオープンソースのフロー処理プラットフォームKafkaを使って、モノのインターネットの膨大なメッセージデータを処理し、膨大なデータストリームを高い信頼性と耐障害性で保存してデータストリームの順序を確保し、メッセージデータを保存して複数のビジネスリンクに同時に効率よくメッセージデータを提供する方法を紹介する。

## ビジネスシナリオ

現在、インテリジェントなドアロックプロジェクトがあるとすると、すべてのドアロックは、1分ごと、またはオン／オフなどドアロックの状態が変化したときに、ドアロック情報を報告し、MQTTトピックは次のように報告されます（QoS = 1）：

```bash
devices/{client_id}/state
```

各機器から送信されるデータの形式はJSONで、ドアロックの電源、解錠状態、操作結果などのデータが含まれます。その内容は以下の通りです：

```json
{
  "process_id": "7802441525528958",
  "action": "unlock",
  "battery": 83.4,
  "lock_state": 1,
  "version": 1.1,
  "client_id": "10083618796833171"
}
```

各ドアロックは、固有のトピックを購読する。遠隔解錠コマンドとして、以下のようにMQTTトピックを発行する（QoS＝1）：

```bash
devices/{client_id}/command
```

発行されるデータには、ロック解除指示、メッセージ暗号化検証情報などが含まれます。

```json
{
  "process_id": "7802441525528958",
  "action": "unlock",
  "nonce_str": "u7u4p0n8",
  "ts": 1574744434,
  "sign": "e9f5af7deaa28563"
}
```

上流と下流のメッセージデータは、次の3つのビジネスリンクで使用する必要があります：

- メッセージを通知する：ドアロック利用者が設定した通知手段（携帯電話メッセージ、メール）に解錠状態を通知する；
- ステータスを監視する：ドアがロックされたときに報告されるステータス情報を分析し処理する。電源やステータスが異常な場合は、アラームを発生させてユーザーに通知すること；
- セキュリティ監査を行います：アップリンクとダウンリンクのメッセージデータを分析し、ユーザーのロック解除動作を記録し、ダウンリンク命令の改ざんやリプレイなどの攻撃を防止する。

このソリューションでは、EMQXが上記トピックのメッセージを業務システムで利用するためのKafkaに統一的にブリッジし、業務システムをEMQXから切り離します。

> *client_idはドアロックのIDで、ドアロックとEMQXの接続に使用するMQTTクライアントIDです。*


## プランの紹介

Kafkaは、Apache Software Foundationが開発したオープンソースのストリーム処理プラットフォームで、ScalaとJavaで書かれています。リアルタイムデータを処理するための統一された高スループット、低レイテンシーのプラットフォームを提供することを目的としています。

kafkaは以下のような特徴があります：

- 高いスループットを実現：スループットは最大数十万、高い並列性を持ち、数千のクライアントが同時に読み書きできるようサポートします；
- 低レイテンシー：最小レイテンシは数ミリ秒であり、リアルタイムストリーミングアプリケーションを容易に構築することができます；
- データの信頼性メッセージデータはフォールト・トレラント・クラスタに安全に分散保存され、キュー・オーダーに厳格に従って処理され、データの整合性と消費の信頼性を確保するためにメッセージ・トランザクション・サポートを提供します；
- クラスタフォールトトレランス：マルチノードレプリカでn-1個のノードが故障することを許容する。
- スケーラビリティを実現：クラスタの動的な拡張をサポートします。

このソリューションでは、EMQXメッセージサーバーとアプリケーション間のメッセージ受け渡しのために、メッセージキューとメッセージバスを提供するKafkaが統合されています。プロデューサー（EMQX）はキューの末尾にデータを追加するだけで、各コンシューマー（ビジネスリンク）は順番にデータを読み込んで独自に処理する。このアーキテクチャは、パフォーマンスとデータの信頼性を考慮し、効果的にシステムの複雑さを軽減し、システムの拡張性を高めています。このソリューションのプロトタイプは以下の通りです：

![Artboard Copy 12.png](https://assets.emqx.com/images/8d4e5233ef300864af34dc150c3d77fe.png)


## EMQX Enterpriseのインストール

### インストール

> EMQXを初めて使う場合は、EMQXガイドで始めることをお勧めします。

[EMQ](https://www.emqx.com/ja/try) の Web サイトから、お使いの OS に適したインストールパッケージをダウンロードしてください。データ永続化は企業向け機能であるため、EMQX Enterprise Editionをダウンロードする必要があります（ライセンストライアルを申し込むことができます）。本稿執筆時点のEMQX Enterprise Editionの最新バージョンは、v3.4.4です。zipパッケージのダウンロードの起動手順は、以下の通りです：

```bash
## Extract the downloaded installation package
unzip emqx-ee-macosx-v3.4.4.zip
cd emqx

## Copy the license file to the EMQX designated directory etc /. In terms of the license , you need to apply for a trial or obtain it through a purchase authorization
cp ../emqx.lic ./etc

## Launch EMQX in console mode
./bin/emqx console
```



### コンフィギュレーションを変更する

今回必要な設定ファイルは以下の通りです：

1. ライセンスファイル、EMQX Enterprise License file、利用可能なライセンスでカバーされています：

```
etc/emqx.lic
```

2. EMQX Kafkaメッセージストレージプラグイン設定ファイルは、Kafka接続情報およびデータブリッジトピックを設定するために使用します：

```bash
etc/plugins/emqx_bridge_kafka.conf
```

実際の導入状況に応じて、以下のようにプラグインの設定情報を記入してください。その他の設定項目については、設定ファイルをよく読んで調整するか、デフォルトの設定をそのまま使用してください。

```bash
## Connection address
bridge.kafka.servers = 127.0.0.1:9092

## The hooks that need to be processed are used for message transmission by QoS 1, and ACK hooks can be used
## Comment other unrelated events and messages hooks

## bridge.kafka.hook.client.connected.1     = {"topic":"client_connected"}
## bridge.kafka.hook.client.disconnected.1  = {"topic":"client_disconnected"}
## bridge.kafka.hook.session.subscribed.1   = {"filter":"#", "topic":"session_subscribed"}
## bridge.kafka.hook.session.unsubscribed.1 = {"filter":"#", "topic":"session_unsubscribed"}
## bridge.kafka.hook.message.deliver.1      = {"filter":"#", "topic":"message_deliver"}

## filter is the MQTT topic to be processed, and topoc is the Kafka topic to be written
## Register multiple Hooks for upstream and downstream message processing

## Select publish hooks for reporting instructions
bridge.kafka.hook.message.publish.1        = {"filter":"devices/+/state", "topic":"message_state"}

## Select acked hooks as issue instructions to ensure that messages arrive before they are stored
bridge.kafka.hook.message.acked.1       = {"filter":"devices/+/command", "topic":"message_command"}
```



## Kafkaのインストールと初期化

DockerでKafkaをインストールし、接続用のdata `9092` ポートをマッピングします。KafkaはZookeeperに依存しています。完全なインストールコマンドは以下に提供されます：

```bash
## Install Zookeeper
docker run -d --name zookeeper -p 2181 -t wurstmeister/zookeeper

## Install and configure Kafka
docker run -d --name kafka --publish 9092:9092 \
		--link zookeeper --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
		--env KAFKA_ADVERTISED_HOST_NAME=127.0.0.1 \
		--env KAFKA_ADVERTISED_PORT=9092 \
		wurstmeister/kafka:latest
```

**あらかじめKafkaに必要なトピックを作成しておく：**

```bash
## Enter Kafka Docker container
docker exec -it kafka bash

## Upstream data topic message_state
kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic message_state

## Downstream data topic message_command
kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic message_command
```



**この時点でEMQXを再起動し、プラグインを起動することで、上記の設定を適用することができます：**:

```bash
./bin/emqx stop

./bin/emqx start

## Or use console mode for more information
./bin/emqx console

## Launch plugin
./bin/emqx_ctl plugins load emqx_bridge_kafka

## After successful startup, there will be the following prompt
Plugin load emqx_bridge_kafka loaded successfully.
```



## 模擬試験

### kafka-console-consumerを使用して消費を開始します。

本ソリューションにおける3つのビジネスリンクの詳細な実装については、本記事では説明しません。この記事では、メッセージがKafkaに書き込まれることだけを確認する必要があります。トピック内のデータを表示するには、Kafka独自の消費コマンドを使用することができます：

```bash
## Enter Kafka Docker container
docker exec -it kafka bash

## Upstream data topic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic message_state --from-beginning

## Open another window to view the topic of downstream data
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic message_command --from-beginning
```

コマンドが正常に実行された後、ブロックしてトピックのデータが消費されるのを待ちます。以下の操作を続けていきます。





### テストデータの送受信シミュレーション

EMQX管理コンソールのWebSocketツールを介して、あなたは、スマートなドアロックアップ/ダウンストリームビジネスデータをシミュレートすることができます。ブラウザで `http: //127.0.0.1: 1883` を開き、EMQX管理コンソールに入り、ツール→WebSocket機能を開き、接続情報を入力してMQTT接続を確立し、ドアロックデバイスをシミュレートすることができます.接続情報のクライアントIDは、業務上の指定に基づき指定します。本記事では `10083618796833171` を使用します。

### ダウンストリームコントロールのトピックスを購読する

ビジネスニーズに応じて、ドアロック専用ダウンストリーム制御トピック `devices / {client_id} / command` を購読する必要があり、ここではトピック `devices / 10083618796833171 / command` を購読してQoS = 1に設定する必要があります：

![](https://assets.emqx.com/images/e2c378c21ebd145a1f1911501b7469d1.png)



### 発行指示のシミュレート



ドアロック制御トピック `devices / {client {ID} / command` にロック解除コマンドを送信する。ここでは、そのデータを

- トピック `devices/10083618796833171/command`
- QoS：1
- payload: ペイロードを使用します：

  ```json
  {
    "process_id": "7802441525528958",
    "action": "unlock",
    "nonce_str": "u7u4p0n8",
    "ts": 1574744434,
    "sign": "e9f5af7deaa28563"
  }
  ```

発行に成功すると、マネジメントコンソールのパブリッシュインターフェースでメッセージを受信することができます：

![image20191126150044511.png](https://assets.emqx.com/images/022305f2b4d9418738e6813e969afec8.png)

同時に、Kafka `message_command` トピックコンシューマーは1つ以上のメッセージを受信します（EMQX ack hooksのトリガーの数は、実際のメッセージクライアントの数に従います）。メッセージはJSON形式である。フォーマットされた内容は以下の通りです：

```json
{
  "client_id": "10083618796833171",
  "username": "",
  "from": "10083618796833171",
  "topic": "devices/10083618796833171/command",
  "payload": "eyAgICJwcm9jZXNzX2lkIjogIjc4MDI0NDE1MjU1Mjg5NTgiLCAgICJhY3Rpb24iOiAidW5sb2NrIiwgICAibm9uY2Vfc3RyIjogInU3dTRwMG44IiwgICAidHMiOiAxNTc0NzQ0NDM0LCAgICJzaWduIjogImU5ZjVhZjdkZWFhMjg1NjMiIH0=",
  "qos": 1,
  "node": "emqx@127.0.0.1",
  "ts": 1574751635845
}
```

このメッセージには、MQTT受信/公開クライアント情報とBase64エンコードされたPayloadデータが含まれています：

- client_id：受信クライアントclient_id
- username: クライアントのユーザー名を受け入れる
- from：パブリッシュクライアント client_id
- topic: メッセージの発行対象トピック
- payload: Base64でエンコードされたメッセージペイロード
- qos: メッセージ QoS
- node: メッセージ処理ノード
- ts: トリガーのタイムスタンプをミリ秒単位でフックします。

### シミュレーションの報告状況

ドアロック制御トピック `devices / {client {ID} / state` にステータスデータを送信します。ここで公開されるデータは

- Topic:`devices/10083618796833171/state` 
- QoS: 
- payload: ペイロードを使用します：

  ```json
  {
    "process_id": "7802441525528958",
    "action": "unlock",
    "battery": 83.4,
    "lock_state": 1,
    "version": 1.1,
    "client_id": "10083618796833171"
  }
  ```


レポートが成功すると、Kafka `message_state` コンシューマーはメッセージを受け取ります（EMQX publish hooksのトリガー数は、メッセージのサブジェクトが購読されているかどうかや購読数に関係なく、メッセージの公開に関連しています）。メッセージはJSON形式で、内容は以下のようにフォーマットされています：

```json
{
  "client_id": "10083618796833171",
  "username": "",
  "topic": "devices/10083618796833171/state",
  "payload": "eyAgICJwcm9jZXNzX2lkIjogIjc4MDI0NDE1MjU1Mjg5NTgiLCAgICJhY3Rpb24iOiAidW5sb2NrIiwgICAiYmF0dGVyeSI6IDgzLjQsICAgImxvY2tfc3RhdGUiOiAxLCAgICJ2ZXJzaW9uIjogMS4xLCAgICJjbGllbnRfaWQiOiAiMTAwODM2MTg3OTY4MzMxNzEiIH0=",
  "qos": 1,
  "node": "emqx@127.0.0.1",
  "ts": 1574753026269
}
```

このメッセージには、MQTT発行クライアント情報とBase64エンコードされたPayloadデータのみが含まれています：

- client_id: 発行クライアントclient_id
- username: パブリッシングクライアントのユーザー名
- topic: メッセージの発行対象トピック
- payload: Base64でエンコードされたメッセージペイロード
- qos: メッセージ QoS
- node: メッセージ処理ノード
- ts:トリガーのタイムスタンプをミリ秒単位でフックします。

この時点で、EMQXによるKafkaへのメッセージの橋渡しの全ステップが完了したことになります。Kafkaにアクセスした業務システムは、消費したメッセージの数、メッセージ発行者/購読者のclient_id、メッセージペイロードの内容から業務判断を行い、必要な業務機能を実現することができます。

## パフォーマンステスト

読者がこのソリューションのパフォーマンスに興味がある場合は、MQTT-JMeterプラグインを使用してテストすることができます。なお、読者は、EMQクラスタ、Kafkaクラスタ、Kafkaコンシューマ、JMeterテストクラスタに関連する最適化および構成が、関連する構成の下で正しく最適な性能テスト結果を得るために性能テストプロセス中に行われることを確認する必要があることに注意する必要があります。



## 概要
本記事を通じて、読者はメッセージ通信と業務処理のためのEMQX + Kafka IoTメッセージ処理ソリューションの重要な役割を理解できます。このソリューションを使用すると、疎結合、高性能、高故障耐性のIoTメッセージ処理プラットフォームを構築し、効率的なデータ処理を安全に実現できます。

本稿のコードは具体的なビジネスロジックを実装したものであり、読者は本稿で提供するビジネスプロトタイプやシステムアーキテクチャに従って拡張することができる。また、EMQXでサポートされているRabbitMQ、RocketMQ、Pulsarのメッセージ／ストリーム処理におけるIoTプロジェクトでの統合アーキテクチャはKafkaに近いため、読者は本稿を参考に、自身の技術スタックに応じてソリューション統合のための関連部品を自由に選択することもできる。
