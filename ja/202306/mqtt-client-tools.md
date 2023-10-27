## はじめに

モノのインターネット（IoT）の急速な発展に伴い、[MQTTプロトコル](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)は多くの企業や開発者に広く使用されています。MQTTの学習と利用の旅では、MQTTクライアントツールを使用して、[MQTTブローカー](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)に接続し、パブリッシング、サブスクライブ、メッセージ送受信を行います。

便利なクライアントツールは、開発者がMQTTの機能を探求し、IoTアプリケーションをデバッグするのを大いに促進し、開発サイクルを短縮することができます。しかし、MQTTクライアントツールには様々な機能があり、初心者やMQTTの専門家にとって、適切なMQTTクライアントツールを選択することは困難です。

2023年に最も便利なMQTTクライアントツールを7つ選び、デスクトップ、ブラウザー、コマンドライン、モバイルのカテゴリー別にリストアップしました。本記事が、MQTT開発に適したものを素早く見つけるための一助となれば幸いです。

## MQTTクライアントをどう選ぶか？

優れたMQTTクライアントツールは、以下の主要な機能を備えている必要があります。

- 一方向および双方向SSL認証のサポート。
- [MQTT 5](https://www.emqx.com/en/blog/introduction-to-mqtt-5)機能のサポート。 
- 機能豊富な基礎の上で使いやすさを維持。
- 同時に複数のクライアントのオンラインサポート。
- クロスプラットフォームで、さまざまなオペレーティングシステムで利用できる。
- MQTT over WebSocketのサポート。
- 高度な機能:カスタマイズされたスクリプト、ロギング、ペイロード形式の変換など。

## 無料公開のMQTTブローカー

MQTTクライアント・デスクトップ・ツールに飛び込む前に、通信とテストを行うための[MQTTブローカー](https://www.emqx.io/)が必要です。ここでは、 `broker.emqx.io` で利用できる無料のパブリックMQTTブローカーを選択します。

>  ***MQTTブローカー情報***
>
> サーバー： `broker.emqx.io`
>
> TCPポート：`1883`
>
> WebSocketポート：`8083`
>
> SSL/TLSポート：`8883`
>
> セキュアWebSocketポート：`8084`

詳しくは、こちらをご確認ください：[無料公開のMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)。

## MQTTデスクトップクライアントツール

### エムキューティーエックス

[MQTTX](https://mqttx.app/)は、macOS、Linux、Windows上で動作するエレガントなクロスプラットフォームMQTT 5.0デスクトップクライアントです。そのユーザーフレンドリーなチャットスタイルのインターフェースにより、ユーザーは簡単に複数のMQTT/MQTTS接続を作成し、MQTTメッセージをサブスクライブ/パブリッシュすることができます。

MQTTXは、MQTTバージョン5.0および3.1.1、MQTT over TLS、MQTT over WebSocket、および一方向および双方向SSL認証に完全対応しています。これらの必須機能に加え、MQTTXは、[MQTT Pub/Sub](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)シミュレーション用のカスタマイズ可能なスクリプトや、Hex、Base64、JSONペイロードなどのコーデックのサポートなど、高度な機能を備えています。

MQTTXは[Electron](https://www.electronjs.org/)で開発されたオープンソースプロジェクトで、[EMQXチーム](https://github.com/emqx)によってメンテナンスされています。最新リリースは2023年4月末までのバージョン1.9.2です。

GitHubプロジェクト：[https://github.com/emqx/mqttx](https://github.com/emqx/mqttx)

![MQTTX](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

####  特徴

- ユーザーフレンドリーで使い勝手の良いUXデザイン
- MQTTメッセージの送受信が可能なチャットボックス
- MQTTバージョン5.0および3.1.1に完全対応
- MQTT over TLS、[MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)に対応。
- 片方向および双方向のSSL認証に対応
- Hex、Base64、JSON、Plaintextペイロードコーデック
- MQTTの契約内容に応じてカラーをカスタマイズ可能
- MQTT Pub/Subシナリオシミュレーション用カスタマイズスクリプト
- Windows、macOS、Linuxで動作するクロスプラットフォーム。

####  インストール

-  **ホームブリュー**

  ```
  brew install --cask mqttx
  ```

-  **ダウンロード**

  [https://mqttx.app/](https://mqttx.app/) 

### MQTTエクスプローラ

MQTT Explorerは、オープンソースのMQTTクライアントツールで、構造化されたトピック概要を持つ使いやすいグラフィカル・ユーザー・インターフェース（GUI）を提供します。階層型のメインビューを採用し、受信したペイロードメッセージのビジュアルチャート表示をサポートします。

MQTT ExplorerはMQTT 5.0と3.1.1プロトコルをサポートしており、開発者は同時に1つのMQTT/MQTTS接続を作成することが可能です。

MQTT ExplorerはTypescriptで書かれ、[Thomas Nordquist](https://github.com/thomasnordquist)によって開発されました。クロスプラットフォームで、Windows、macOS、Linuxで動作させることができます。2020年4月28日にリリースされたバージョン0.4.0-beta1を最後に、開発が終了しているのは残念です。

GitHub: [https://github.com/thomasnordquist/MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer)

![MQTT Explorer](https://assets.emqx.com/images/fd34faa00ea66d846bfd0a9d99040359.png)

####  特徴

>  [MQTT Explorer](http://mqtt-explorer.com/)より引用

- Topicの可視化とTopic変更のダイナミックプレビュー
-  保持したTopicを削除する
-  Topicを検索/フィルタリング
-  Topicを再帰的削除
- 現在および以前に受信したメッセージの差分表示 
- Topicをパブリッシュ
- デジタルTopicを描画
- すべてのTopicの履歴レコードを保持
- ダーク/ライトTopic

#### ダウンロード

[https://mqtt-explorer.com/](https://mqtt-explorer.com/)

## MQTTオンラインクライアントツール

### MQTTX Web

[MQTTX Web](https://mqttx.app/web)は、MQTTアプリケーションをオンラインでデバッグ、開発、テストするための、ユーザーフレンドリーなブラウザベースのツールです。WebSocketクライアントを介してMQTTブローカーに接続し、直感的なインターフェイスを提供します。

[EMQXチーム](https://github.com/emqx)によって開発されたMQTTX Webは、MQTT 3.1.1およびMQTT 5.0のプロトコルとWebSocketトランスポートをサポートするオープンソースのツールです。Apache Version 2.0の下でライセンスされています。

GitHubプロジェクト：[https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web)

今すぐお試しください： [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) 

また、MQTTX WebはDockerを使ったプライベートデプロイをサポートしており、ブラウザしか利用できない場合や、制限のあるイントラネット環境でのテストに有効です。Dockerイメージからデプロイします：

```
docker pull emqx/mqttx-web
docker run -d --name mqttx-web -p 80:80 emqx/mqttx-web
```

![MQTTX Web](https://mqttx-static.emqx.net/img/banner.268d1fa.png)

### MQTT.Coolテストクライアント

MQTT.Cool Test Clientは、MQTT.CoolサーバーとMQTTブローカー間の相互作用をテストすることができる非常にシンプルで直線的なGUI（MQTT.Cool APIをベース）です。ブラウザからMQTT TCP経由でブローカーへの接続をサポートします。

今すぐお試しください：[https://testclient-cloud.mqtt.cool/](https://testclient-cloud.mqtt.cool/)

![MQTT.Cool](https://assets.emqx.com/images/263f0c34a8b93d477acff194ef17d46e.png))

 

## MQTT CLIツール

### MQTTX CLI

[MQTTX CLI](https://mqttx.app/cli)は、軽量で使いやすいMQTT 5.0コマンドラインツールです。MQTTの公開、サブスクライブ、ベンチマーク、IoTデータシミュレーションのための様々なコマンドを備えており、MQTT開発のための最も強力なツールの1つです。

MQTTX CLIは、Node.jsで書かれ、[EMQXチーム](https://github.com/emqx)によって開発されたオープンソースプロジェクトです。クロスプラットフォームで、Windows、macOS、Linuxで動作させることができます。

GitHubプロジェクト：[https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli)

![MQTTX CLI](https://assets.emqx.com/images/21640fc7fa544b56ae41815f390ccee7.png)

 

####  特徴

- MQTT v3.1.1およびMQTT v5.0の両方を完全サポート。
- Windows、MacOS、Linuxとのクロスプラットフォーム互換性
- 依存関係のないセットアップにより、前提条件なしで素早くインストール可能。
- CA証明書、自己署名証明書、片方向および双方向のSSL認証に対応しています。
- MQTTサービスのパフォーマンスを迅速に評価するためのパフォーマンステスト機能。

#### インストール

MQTTX CLIは、Windows、macOS、Linuxと互換性があります。その他のインストールオプションについては、[ドキュメント](https://mqttx.app/docs/cli/downloading-and-installation)を参照してください。

-  **ドッカー**

  ```
  docker pull emqx/mqttx-cli
  docker run -it --rm emqx/mqttx-cli
  ```

-  **ホームブリュー**

  ```
  brew install emqx/mqttx/mqttx-cli
  ```

-  **ダウンロード**

  [https://mqttx.app/cli](https://mqttx.app/cli)

####  使用例

-  接続

  MQTTブローカーへの接続をテストします：

  ```
  mqttx conn -h 'broker.emqx.io' -p 1883 -u 'test' -P 'test'
  ```

-  **サブスクライブ**

  MQTTのトピックを購読する：

  ```
  mqttx sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
  ```

-  **パブリッシュ**

  MQTTトピックにQoS1メッセージを発行する：

  ```
  mqttx pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from MQTTX CLI'
  ```

-  **複数メッセージの公開**

  MQTTX CLIは、複数のメッセージの発行もサポートしています。エディタでコマンドに-Mパラメータと-sパラメータを追加し、各エントリの後に改行します。

  ![複数メッセージの公開](https://assets.emqx.com/images/549a31f8b062f099c0eac8c0c6047f35.png)

-  **ベンチマーク**

  MQTTX CLIについては、 `bench` コマンドが使いやすく、内容も簡潔に出力されます。大量の接続、購読、出版物に対しては、使用中に大量の出力ログに圧倒されないよう、リアルタイムに数値を動的に更新することで表示方法を最適化しました。

  ![Benchmark](https://assets.emqx.com/images/6d942b32742bf859ef66a93abb216860.png)

### Mosquitto CLI

Mosquitto は、人気のある `mosquitto_pub` および `mosquitto_sub` コマンドラインクライアントを持つ、広く使われているオープンソースの MQTT ブローカーです。これらのCLIツールは、MQTTブローカーへの接続、サブスクライブ、およびメッセージの公開を行うための幅広いオプションを提供します。

Mosquittoプロジェクトは、C/C++で書かれ、Eclipse Foundationによってメンテナンスされています。Mosquittoは移植性が高く、Linux、Mac、Windows、Raspberry Piなど様々なプラットフォームで展開することが可能です。

GitHubプロジェクト： [https://github.com/eclipse/mosquitto](https://github.com/eclipse/mosquitto)

####  特徴

- 軽量で使いやすい
- MQTT v3.1.1およびv5.0プロトコルのサポート
- 豊富なコマンドラインパラメーター
- SSL/TLS暗号化/認証のサポート
- MQTT v5.0リクエスト/レスポンス機能

####  インストール

-  ドッカー

  ```
  docker pull eclipse-mosquitto
  ```

-  ホームブリュー

  ```
  brew install mosquitto
  ```

-  ダウンロード

  [https://mosquitto.org/download/](https://mosquitto.org/download/) 

####  使用例

-  **パブリッシュ**

  MQTTトピックにQoS1メッセージを発行する：

  ```
  mosquitto_pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from Mosquitto CLI'
  ```

-  **サブスクライブ**

  MQTTのトピックを購読する：

  ```
  mosquitto_sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
  ```

-  **リクエスト/レスポンス**

  ```
  mosquitto_rr -t 'req-topic' -e 'rep-topic' -m 'request message' -h 'broker.emqx.io'
  mosquitto_pub -t 'rep-topic' -m 'response message' -h 'broker.emqx.io'
  ```

  

## MQTTモバイルクライアントツール

### イージーエムキューティー

EasyMQTTはiPhone、iPad、macOS用のMQTTクライアントで、任意のMQTTブローカーと対話することができます。自宅で自分のセットアップを管理したり、Zigbee2MQTTのようなものを制御したり、リモートブローカーをモニターしたりするために使用します。シンプルでユーザーフレンドリーなインターフェイスが特徴で、ライトモードとダークモードの両方をサポートしています。

<div style="text-align:center;"><img src="https://assets.emqx.com/images/f9118dd8e7c71a668b3667b1c629a1d0.png" width="320px" /></div>

**ダウンロード**

[https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone](https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone) 

## まとめ

最後に、MQTTクライアントツールをカテゴリー別に詳しく紹介しました。

その中でも、MQTTXオープンソースプロジェクトは、モダンなチャットスタイルのインターフェース、MQTT 5.0のフルサポート、優れたユーザー体験を提供する豊富な機能セットを提供する、急成長中のクライアントツールとして際立っています。デスクトップ、コマンドライン、ブラウザの3つのバージョンがあり、MQTTXは多様なシナリオでMQTTテスト要件を満たすことができます。間違いなく、[MQTTX](https://mqttx.app/)は2023年のトップMQTTクライアントツールの1つです。

## 参考文献

- [2023年MQTTデスクトップクライアントツール上位3位](https://www.emqx.com/en/blog/top-3-mqtt-desktop-client-tools-in-2023)
- [2023年、IoT開発者向けMQTT CLIツールトップ5が登場](https://www.emqx.com/en/blog/top-5-mqtt-cli-tools-for-iot-developers-in-2023)
- [2023年MQTTウェブソケットクライアント上位3位](https://www.emqx.com/en/blog/top-3-mqtt-websocket-clients-in-2023)



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
