## Mosquitto_pub/subの紹介

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は軽量のメッセージングプロトコルで、IoTプロジェクトにおけるデバイス通信に不可欠です。

MosquittoにはMQTTテストとトラブルシューティングを強化するために設計された`mosquitto_pub`と`mosquitto_sub`のコマンドラインユーティリティが付属しています。これらのツールは、[MQTTトピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)との効率的なやりとりを可能にします。`mosquitto_pub`はメッセージの公開に、`mosquitto_sub`はトピックのサブスクライブに使用されます。このストリームラインのアプローチにより、MQTTベースのアプリケーションの迅速な開発とデバッグが容易になります。

MQTTブローカーとクライアントツールを含むMosquittoパッケージを公式サイトからダウンロードしてください：[![img](https://mosquitto.org/favicon-16x16.png)Download](https://mosquitto.org/download/) 

## Mosquitto_pub/subの利点

- **MQTTテストに不可欠な機能**：Mosquitto_pub/subは、サブスクライブ（sub）とメッセージの公開（pub）を含む様々なテストシナリオに適したMQTTテストの必須機能を提供します。

  例：

  ```shell
  mosquitto_sub -h broker.emqx.io -p 1883 -t 'testtopic/#'
  mosquitto_pub -h broker.emqx.io -p 1883 -t 'testtopic/1' -m 'hello'
  ```

- **軽量でユーザーフレンドリー**：迅速な開発ニーズに対応し、インストールと開始が容易な軽量ツールとして設計されています。

- **オープンソースでコミュニティサポートあり**：[GitHub](https://github.com/eclipse/mosquitto)でホストされており、オープンソースプロジェクトに特有の活発なコミュニティサポートの恩恵を受けています。

- **MQTT 5.0完全対応**：最新の機能を含む[MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5)プロトコルに対応しています。

- **デバッグモード**：デバッグモードをサポートし、開発者が問題を効率的に診断・解決できるようにします。

## Mosquitto_pub/subの主な機能

C/C++で開発されたMosquitto_pub/subは、より広範なMosquittoエコシステムの一部であり、シンプルなpublishとsubscribeの機能でMQTTメッセージングを容易にし、IoTプロジェクトに最適です。以下はその主な機能です：

- **統合ブローカーとクライアントツール**：Mosquittoは、統合ブローカーとクライアントユーティリティ（`sub`と`pub`）を備えた包括的なMQTTソリューションを提供し、MQTT通信のセットアップと管理を簡素化します。

- **リクエスト-レスポンスコマンド**（`mosquitto_rr`）：Mosquittoは、`sub`と`pub`の主要機能に加えて、MQTTv5/3.1.1用の`mosquitto_rr`を含んでいます。このコマンドは、メッセージを公開し、応答を待つためのリクエスト-レスポンス機能を利用します。

  **例：**

  ```shell
  mosquitto_rr -t request-topic -e response-topic -m message
  ```

  このクライアント側の機能は、ダイナミックなデータ交換とIoTインタラクションに役立つ直接のリクエスト-レスポンス通信パターンをサポートすることにより、MQTTメッセージングを強化します。

- **高度なTLSサポート**：Mosquitto_pub/subは、包括的なSSL/TLSセットアップのための`mosquitto-tls`コマンドで基本的なTLSを拡張し、安全なMQTT通信を強調しています。暗号化された接続と認証のためのSSL証明書の生成と適用について詳細なガイダンスを提供し、競合を避けるためにCA、サーバー、クライアントに固有の証明書パラメータが必要であることを強調しています。`mosquitto-tls`を利用することでセキュリティが強化され、Mosquittoを安全なMQTTデプロイの強力な選択肢にしています。

- **Mosquitto_pub/subの拡張接続機能：** Mosquitto_pub/subは、高度なネットワーク機能でMQTT通信を充実させます。

  - **-A bind-address**は、トラフィックフローを目的としたネットワークインターフェースの指定を可能にし、データセキュリティと伝送効率を高めます。`mosquitto_pub -A 192.168.1.5...`のように使用します。
  - **-L, --url**は、接続の詳細を1つのURLに統合し、セットアッププロセスを合理化します。`mosquitto_sub -L mqtt://...`で示されるように使用します。
  - **--proxy**は、SOCKS5プロキシの使用を可能にし、プライバシーを高め、ネットワークの適応性を提供します。`mosquitto_sub --proxy socks5h://...`で例示されるように使用します。

  これらのオプションは、MQTTネットワーク構成の制御を拡張し、通信を簡素化し、セキュリティを高めます。

- **Mosquitto_pub/subの高度なメッセージング機能**：Mosquitto_pub/subは、メッセージ管理のための強力なオプションを導入しています。

  - **--stdin-file | --file（pub）**は、ファイルやstdinからの公開を可能にし、自動化や大きなペイロードの処理を簡素化します。mosquitto_pub --file /path/to/message.txt...のように使用します。
  - **--repeat（pub）**は、メッセージの定期的な再公開を可能にし、定期的な更新やテストに役立ちます。Mosquitto_pub... -repeat 5 -repeat-delay 10で例示されるように使用します。
  - **--filter-out | --random-filter（sub）**は、トピックやランダム性に基づくメッセージのフィルタリングを提供し、サブスクリプションの関連性を高めます。mosquitto_sub --filter-out 'testtopic/ignore'で示されるように使用します。

  これらの機能は、公開とサブスクライブを合理化し、MQTTワークフローの効率を向上させます。

主要な機能に加えて、Mosquitto_pub/subは、保持されたメッセージの処理、動的なアンサブスクライブ、出力フォーマットの強化など、メッセージとサブスクリプションの管理を洗練するための追加オプションを提供し、様々なMQTTタスクに対するその有用性を高めています。

## Mosquitto_pub/subの適用シナリオ

Mosquitto_pub/subは、安全で効率的なMQTTメッセージングに最適で、Mosquittoブローカーを補完します。TLSサポートと汎用ネットワーキングを提供し、IoTセキュリティプロジェクトに最適です。デバイス通信を超えて、その強みはテストと開発にあります。メッセージフィルタリングや自動化などのオプションを使用して、詳細なシステムテストを容易にします。

- **デバイステスト**：スマートデバイスがMQTTメッセージを確実に公開および受信することを確認します。
- **システムデバッグ**：`-repeat`と`--filter-out`を使用して、IoTプラットフォームの反復的なテストと微調整を行います。

これらの機能により、Mosquitto_pub/subは多くのMQTTアプリケーションに役立つ貴重なツールとなり、開発プロセスとシステム機能を強化します。

## Mosquitto_pub/subの制限事項

Mosquitto_pub/subはMQTTメッセージングの強力なツールですが、特定のシナリオでの使用に影響を与える可能性のある制限事項があります：

- **機能セット**：基本的なpublish/subscribe操作には優れていますが、詳細なメッセージフィルタリングや入門者向けのテキスト以外の複数のデータフォーマットのサポートなど、より高度なデータ処理とメッセージングパターンの機能が不足している可能性があります。
- **バンドルインストール**：Mosquitto_pub/subはブローカーを含むMosquittoパッケージの一部です。つまり、テスト目的でスタンドアロンのクライアントを求めているユーザーは、意図せずにブローカーコンポーネントをインストールし、セットアップに不必要な複雑さを持ち込む可能性があります。
- **カスタマイズと拡張性**：そのカスタマイズオプションは主にコマンドライン引数であり、高度に特化したユースケースやより複雑なシステムへの統合に必要な柔軟性を提供できない可能性があります。

Mosquitto_pub/subは信頼性が高く軽量なツールであり、強力なセキュリティ機能を提供していますが、その制限は、高度な要件を持っているユーザーやスタンドアロンのクライアント機能を必要とするユーザーにとって適切でない可能性があることを意味します。そのような場合、ユーザーは他のオプションを探索したり、特定のニーズを満たすための回避策を利用したりする必要があるかもしれません。

## MQTTX CLI：Mosquitto_pub/subの代替案

[MQTTX CLI](https://mqttx.app/ja/cli)は、MQTTXのコマンドライン版であり、MQTTサービスとアプリケーションの迅速な開発とデバッグに特化した強力なオープンソースのMQTT 5.0 CLIクライアントです。パブリッシュ、サブスクライブ、ベンチマーク、デバッグモード、IoTデータのシミュレーションなど、さまざまなコマンドを提供し、MQTT開発に不可欠なツールとして確立されています。

純粋なクライアントツールであるMQTTX CLIには、[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)コンポーネントは含まれていません。ネイティブシステムのインストール、Docker、Homebrew、npmをサポートしており、さまざまなオペレーティングシステムに簡単に展開できます。

ダウンロードはこちら：[MQTTX Download](https://mqttx.app/ja/downloads) 

### MQTTX CLIの高度な機能

MQTTX CLIはMosquitto_pub/subと同じ利点を共有しています。さらに、以下のような高度な機能もサポートしています：

- **接続コマンド**：Mosquitto_pub/subが主要な`sub`と`pub`の機能に重点を置いているのに対し、MQTTX CLIは接続をテストするための直接の接続コマンドを提供しています。

  **例：**

  ```shell
  mqttx conn -h 'broker.emqx.io' -p 1883 -u 'admin' -P 'public
  ```

  この特別なコマンドは、ブローカーとの接続を検証するプロセスを簡素化し、開発者がさらなるMQTT操作を行う前にセットアップが正しく構成されていることを確認するための迅速で効率的なステップにしています。

- **設定管理**：MQTTX CLIは、設定のインポートとエクスポートをサポートする強力な機能を導入しています。この機能により、ユーザーはコマンドパラメータをローカルファイルに保存して、将来使用することができます。

  例：

  ```shell
  mqttx conn --save ../custom/mqttx-cli.json
  mqttx conn --config ../custom/mqttx-cli.json
  ```

  これにより、再利用可能な設定を通じて、異なる環境やプロジェクトの迅速なセットアップが可能になり、効率が向上します。JSONとYAMLフォーマットのサポートは、アクセスを容易にするためのデフォルトパスとともに、複数の設定の管理と利用を直感的かつ柔軟にします。

- **出力とログの強化**：MQTTX CLIは、明確なログスタイルの出力で、MQTT通信に関する正確な洞察を提供し、ユーザーエクスペリエンスを向上させます。

  例：

  ```shell
  ❯ mqttx sub -h broker.emqx.io -p 1883 -t 'testtopic/#'
  [3/1/2024] [3:59:44 PM] › …  Connecting...
  [3/1/2024] [3:59:45 PM] › ✔  Connected
  [3/1/2024] [3:59:45 PM] › …  Subscribing to testtopic/#...
  [3/1/2024] [3:59:45 PM] › ✔  Subscribed to testtopic/#
  [3/1/2024] [3:59:45 PM] › topic: testtopic/SMH/Yam/Home/GartenLicht/stat/POWER1
  qos: 0
  retain: true
  payload: { "msg": "hello" }
  ```

  詳細で構造化されたロギングフォーマットは、問題の特定を簡素化し、全体的な開発とデバッグの経験を向上させます。この詳細レベルにより、開発者はトラブルシューティングプロセスを合理化するために必要なすべての情報を手元に持つことが保証されます。

- **ベンチマークツール**：MQTTX CLIの接続、サブスクライブ、パブリッシュのベンチマークツールは、ボックスから直接詳細なパフォーマンス分析を可能にします。

  例：

  ```shell
  mqttx bench pub -h broker.emqx.io -t 'testtopic' -m 'hello' -c 100
  ```

  これらのツールは、MQTT操作のスループットとレイテンシーに関する洞察を提供することで、パフォーマンスの最適化を可能にします。これは、システムのパフォーマンスを微調整するために不可欠です。

- **シミュレーション機能**：MQTTX CLIは、MQTTアプリケーションの高度なシミュレーションをサポートし、ユーザーが組み込みのシナリオから選択するか、スクリプトを通じてカスタムシナリオを定義できるようにします。

  例（組み込みシナリオの使用）：

  ```shell
  mqttx simulate -h broker.emqx.io -p 1883 --scenario tesla -c 10
  ```

  例（カスタムスクリプトの使用）：

  ```shell
  mqttx simulate -h broker.emqx.io -p 1883 -c 10 --file ./customScenario.js
  ```

  これにより、詳細なMQTTトラフィックパターンをシミュレートすることで、包括的なテスト環境が可能になります。これは、さまざまなシナリオでのアプリケーションの回復力とパフォーマンスを評価するために不可欠です。これにより、アプリケーションが意図された実際の使用に十分に準備されていることが保証されます。

- **データパイプライン**：MQTTX CLIは、クリーンモードや `jq` との統合など、MQTTデータの管理とパイプラインを簡素化し、データ処理を簡単にします。

  例（MQTTパケットからペイロードを抽出）：

  ```shell
  mqttx sub -t topic --output-mode clean | jq '.payload'
  ```

  例（追加の詳細でデータを再構築）：

  ```shell
  mqttx sub -t topic --output-mode clean | jq '{topic, payload, retain: .packet.retain, userProperties: .packet.properties.userProperties}'
  ```

  これらの例は、MQTTX CLIを `jq` やその他のユーティリティと組み合わせることで、IoTデータの取得と操作のための効率的なパイプラインを構築する際の使いやすさを示しています。この機能は、MQTTデータを処理するための複雑なコーディングを必要とせずに、データパイプラインを迅速かつ効果的に構築するのに大いに役立ちます。

- **多様なデータフォーマット**：MQTTX CLIは、JSON、Hex、Base64、Protobuf、CBORなど、複数のデータフォーマットをサポートし、データ処理の柔軟性を提供します。

  例：

  ```shell
  mqttx sub -h broker.emqx.io -p 1883 -t 'testtopic/json/data' --format json
  ```

  これにより、多様なデータ解釈と操作が可能になり、幅広いIoTアプリケーションの要件に対応できます。

## MQTTプロジェクトに適したツールの選択

まとめると：

- **Mosquitto_pub/sub**は、軽量で安全な[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)とブローカーの統合が必要なシナリオで優れています。その強みは、パフォーマンスと強化されたセキュリティ機能にあり、包括的なMQTTソリューションに最適です。
- **MQTTX CLI**は、ユーザーの利便性と高度な設定に重点を置き、より広範な機能を提供します。多様なデータ処理と広範なカスタマイズが必要な環境で輝きます。

基本的なMQTTクライアントのタスクと、より高度な機能を必要とするシナリオでは、MQTTX CLIが好ましい選択肢として浮上します。現代のIoT開発の課題に対応する包括的で適応性の高いツールキットを提供します。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
