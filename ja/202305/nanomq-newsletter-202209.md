NanoMQは9月も順調にアップデートを続け、先日、最新のv0.12.1が正式リリースされました。このバージョンでは、ブリッジング機能でオンライン/オフラインのイベントや接続状態を監視する機能が追加され、オリジナルのログシステムが再構築されてアップグレードされ、設定ファイルが簡素化されて統一された単一ファイルに統合されるなど、依然として豊富な更新が行われています。

## ブリッジ接続状態イベントメッセージ

IoTアプリケーションでは、ネットワークの状態が弱く不安定になることが多いため、現在のデバイスのネットワーク状態やクラウドとの接続性を検出する信頼性の高い方法が必要です。そのため、NanoMQはブリッジ接続を使用してネットワーク接続状態を検出する機能を提供します。ユーザがエッジでNanoMQを使用してクラウドにブリッジ接続する場合、NanoMQは指定されたクラウドブローカーへのMQTT接続を作成します。MQTTのロングコネクション機能に基づいて、ローカルネットワーク内のデバイスはこのコネクションを使用してネットワークステータスを判断することができます。


ローカルネットワークの停止やその他の障害によりブリッジ接続が切断されると、NanoMQはブリッジ接続の切断を検出し、クライアントのオンライン/オフラインのイベントメッセージに変換してシステムトピックに公開します。ネットワークが復旧すると、ブリッジ接続は自動的に再接続され、オンライン・イベント・メッセージもシステム・トピックに公開されます。ローカルクライアントや他のサービスは、受信したメッセージに従って対応する緊急処理を行うことができ、また、クラウドサービスの停止による誤判定を避けるために、複数のブリッジターゲットを代替サービスとして設定することができます。

### ブリッジオンライン/オフラインのイベントメッセージの入手方法

現在、NanoMQのブリッジ・ステータス・イベントは、MQTT 3.1.1/5.0 および MQTT over QUIC を含むすべてのブリッジ・モードをサポートしています。オンライン/オフラインのイベントメッセージのシステムトピックはそれぞれ $SYS/brokers/connected と $SYS/brokers/disconnected です。イベント・メッセージは、WebHookの方法で標準のPublishメッセージとして取得することも可能です。ここでは、MQTT over QUICブリッジ構成を例にして、ブリッジ接続のオンライン/オフライン・メッセージを取得する方法を示します：

としてブリッジが構成されている場合（該当する部分のみ抜粋）：

```
bridge.mqtt.emqx.clientid=quic_client
bridge.mqtt.emqx.keepalive=5
bridge.mqtt.emqx.quic_keepalive=120
bridge.mqtt.emqx.clean_start=false
bridge.mqtt.emqx.username=quic_bridge
bridge.mqtt.emqx.password=passwd
```

NanoMQ コマンドラインツールを使用して、対応するトピックを購読してください。ブリッジブレークは、ローカルネットワークがダウンしたときに発生します：

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/connected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/connected: {"username":"quic_bridge", "ts":1664277443551,"proto_name":"MQTT","keepalive":5,"return_code":"0","proto_ver":4,"client_id":"quic_client", "clean_start":0}
```

ローカルネットワークが復旧すると、ブリッジ再接続が発動します：

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/disconnected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/disconnected: {"username":"quic_bridge","ts":1664277394014,"reason_code":"8b","client_id":"quic_client"}
```

オンライン/オフラインのイベントメッセージに含まれるクライアントIDやユーザー名/パスワードは、ブリッジの設定に含まれるものと一致しており、ローカルクライアントとブリッジクライアントを区別するために使用できることがわかります。現時点では、ブリッジ接続のステータスは、通常のMQTTクライアントと同じシステムトピックを共有しています。NanoMQでは、ブリッジ・ネットワーク・ステータスのために別のシステム・トピックを設定し、クラウドエッジ・メッセージバスとして標準的なネットワークのヘルスモニタリング機能を追加することも検討しています。ユーザーの皆様は、関連する課題や機能アプリケーションの提出をお願いします。

### QUICトランスポート層におけるKeep Aliveパラメータの新規設定について

QUICは接続維持機構を内蔵しています。MQTTとQUICのタイムアウトをより細かく制御できるように、NanoMQのブリッジング機能では両方のタイムアウト設定を公開し、さらにQUICのトランスポート層のパラメータを後ほど公開し、ユーザが調整できるようにする予定です。

```
## Ping: interval of a downward bridging connection via QUIC.
bridge.mqtt.emqx.quic_keepalive=120
```

## コンフィギュレーションファイルの簡素化

v0.12以前は、NanoMQの各モジュールが独立した設定ファイルを持ち、設定を変更するためにはそれぞれのファイルを個別に開く必要があり、起動が面倒だった。v0.12からは、正式にすべての設定項目をnanomq.confに集約し、モジュールごとに個別のグループを追加することにしました。


なお、これまでのコマンドラインパラメータでブリッジコンフィグレーションファイルのパスとユーザー名とパスワードのファイルを指定する機能は廃止されました。

```
--bridge <path>           The path of a specified bridge configuration file 
--auth <path>             The path of a specified authorize configuration file
```

なお、この修正は、ZeroMQ Gatewayの設定ファイル（nanomq_gatewaty.confはnanomq_cliに属する）およびコンテナのデプロイ時に環境変数で設定ファイルを指定する方法には影響しません。

## ログシステム再構築

NanoMQの旧来のログシステムは、コマンドライン、ファイル、Syslogの3つのモードをサポートしています。しかし、コンフィギュレーションによる切り替えができない、階層的な出力に対応していない、コンパイル段階でCMakeパラメータを変更して有効にする必要があるなど、デバッグやO&Mの解析が困難な状況でした。v0.12では、ログシステム全体の再構築を行いました。当初の3つの出力対象やSyslog規格との互換性を保つことに加え、5つのログレベル（trace、debug、info、warn、error、fatal）、ログファイルのパスやログファイルのロールアップを追加しました。

ログ構成例：
```
## ------------------ Logging Config ------------------ ##
## - file: output logs to file
## - console: output logs to the command line
## - syslog: output logs to the syslog system
## Value: file | console | syslog supports parallel configuration
log.to=file,console,syslog

## Value: trace | debug | info | warn | error | fatal
## Set log level
##
## Default: warn
log.level=warn

## If "Output Log to File" is configured, specify the file path here
log.dir=/tmp

## If "Output Log to File" is configured, specify the file name here
log.file=nanomq.log

## The maximum size of a single log file. Rolling update will be performed if it exceeds the limit
## Supported parameters unit: KB | MB | GB
log.rotation.size=10MB

## Maximum number of saved rolling update log files
log.rotation.count=5
```

## NanoSDKがAPIを追加

これまで、NanoSDKのAPIはほとんどがNNGスタイルで、サブスクリプションやコンタクトのサブスクリプションを完了するために、ユーザ自身がMQTTメッセージを組み立て、送信することが必要でした。NanoSDK 0.7.5 からは、より便利でカプセル化された以下の MQTT API が NanoSDK に追加されています：
| nng_mqtt_subscribe()         | シンクロナイズドにサブスクライブリクエストを実行する     |
| ---------------------------- | ------------------------------------------- |
| nng_mqtt_subscribe_async()   | 非同期でサブスクライブ要求を実行する    |
| nng_mqtt_unsubscribe()       | シンクロナイズドで配信停止要求を行う    |
| nng_mqtt_unsubscribe_async() | 非同期で配信停止要求を実行する。       |
| nng_mqtt_disconnect()        | MQTTクライアントの接続を解除する      |


具体的な使用方法については、[NanoSDK Doc](https://github.com/emqx/NanoSDK/blob/0.7.5/docs/man/libnng.3.adoc#mqtt-message-handling)を参照してください。

## 今後の予定

メッセージの再発行機能とルールエンジンのルールホットアップデートは、次のバージョンで正式にリリースされる予定です。同時に、NanoMQにReloadコマンドが追加され、設定ファイルのホットアップデートが可能になる予定です。MQTT over QUICブリッジにおいて、QUICをサポートしないネットワークでもブリッジ接続が正常に行われるように、再接続に複数回失敗した場合にTCPへのフォールバックが自動的に切り替わるようになります。
