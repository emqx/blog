最近、[MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5)用のクロスプラットフォームデスクトップクライアントである[MQTTX](https://mqttx.app/)がバージョン1.8.0でリリースされました。MQTTXは、[EMQX](https://www.emqx.com/ja/products/emqx)などのMQTTブローカーに接続するために設計されています。複数の同時[オンラインMQTTクライアント](http://mqtt-client.emqx.com/)接続を簡単かつ迅速に作成し、MQTT/TCP、MQTT/TLS、MQTT/WebSocketの接続、パブリッシュ、サブスクリプション機能、およびその他のMQTTプロトコル機能をテストできます。

v1.8.0の最新リリースでは、クイック接続複製機能によるエクスペリエンスの最適化だけでなく、CLI（コマンドライン）とブラウザーという2つの新しいインタラクション方法を追加することで、新しいユースケースをサポートしています。これにより、MQTTX 1.8.0は、サポートされているシナリオの点で最も完全なMQTTテストクライアントになります。ニーズに応じて、デスクトップクライアントをダウンロードするか、ターミナルコマンドラインを使用するか、Webブラウザで簡単にMQTT接続をテストすることを選択できます。

## MQTTX CLI：ターミナルでMQTTサービスとアプリケーションを迅速に開発およびデバッグ

MQTTプロトコルがIoT業界で広く使用されるようになり、より多くの開発者が接続テストにMQTTXを選択するようになりました。

ユーザーがMQTT接続テストを実装するためのより多くの選択肢と利便性を提供するために、MQTTX v1.8.0ではコマンドラインをインタラクションの形式として追加しました。これが、完全にオープンソースのMQTT 5.0コマンドラインクライアントツールである[MQTTX CLI](https://mqttx.app/ja/cli)です。**これにより、開発者はグラフィカルインターフェイスなしでコマンドラインを使用してMQTTサービスとアプリケーションをより迅速に開発およびデバッグできます。** これにより、次の使用目標が可能になります。

- サーバーターミナルでデプロイされたMQTTサービスをテストする
- コマンドラインスクリプトを編集して使用することにより、MQTTサービスを迅速にテストする
- コマンドラインスクリプトを使用して、単純なストレステストまたは自動テストを実行する

> MQTTX CLIウェブサイト：[MQTTX CLI: A Powerful and Easy-to-use MQTT CLI Tool](https://mqttx.app/cli) 
>
> MQTTX CLI 1.8.0ダウンロード：[Release v1.8.0 · emqx/MQTTX](https://github.com/emqx/MQTTX/releases/tag/v1.8.0) 
>
> MQTTX CLI GitHubリポジトリ：[MQTTX/cli at main · emqx/MQTTX](https://github.com/emqx/MQTTX/tree/main/cli) 

![MQTTX CLI](https://assets.emqx.com/images/ee9ee7ee619f209c725ef1c67f59d4ae.png)

## 依存関係なし：前提条件なしですぐに使用可能

### インストール

MQTTX CLIは、ターミナルでコマンドを実行するだけで、macOS、Linux、Windowsシステムに環境依存なしで迅速にダウンロードしてインストールできます。

macOSとLinuxのユーザーには、コマンドラインを使用したクイックインストール方法を提供しており、バイナリを迅速にダウンロードし、オペレーティングシステムに最新の安定版のMQTTX CLIをインストールできます。Windowsユーザーは、MQTTXリリースページに移動して、対応するシステムアーキテクチャのexeパッケージを見つけ、手動でダウンロードして使用できます。

> 注意：ダウンロードとインストールの際は、現在のシステム環境のCPUアーキテクチャを区別するように注意してください。

#### macOS

- **Homebrew**

  macOSユーザーは、Homebrewを介してMQTTX CLIをすばやくインストールして使用できます。

  ```shell
  brew install emqx/mqttx/mqttx-cli
  ```

- **Intel Chip**

  ```shell
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-x64
   sudo install ./mqttx-cli-macos-x64 /usr/local/bin/mqttx
  ```

- **Apple Silicon**

  ```shell
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-arm64
   sudo install ./mqttx-cli-macos-arm64 /usr/local/bin/mqttx
  ```

#### Linux

- **x86-64**

  ```shell
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-x64
   sudo install ./mqttx-cli-linux-x64 /usr/local/bin/mqttx
  ```

- **ARM64**

  ```shell
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-arm64
   sudo install ./mqttx-cli-linux-arm64 /usr/local/bin/mqttx
  ```

#### Windows

Windowsユーザーは、MQTTXダウンロードページ（[Release v1.8.0 · emqx/MQTTX](https://github.com/emqx/MQTTX/releases/tag/v1.8.0) ）から対応するexeファイルを手動でダウンロードする必要があります。

![MQTTX CLI Windows](https://assets.emqx.com/images/dccac8ea2f04693c55e77623ad507eba.png)

#### NPM

上記に加えて、npmを使用したインストール方法も提供しているため、Node.js環境がシステムにあれば、現在のオペレーティングシステム環境に関係なく、すばやくインストールして使用できます。

```shell
npm install mqttx-cli -g
```

### クイックスタート

ダウンロードとインストールが完了したら、ターミナルに直接`mqttx`コマンドを入力して実行して使用できます。-Vパラメーターを追加してMQTTX CLIが正常にインストールされたことを確認できます。バージョン番号が出力されたら、MQTTX CLIが正常にインストールされています。

```shell
$ mqttx -V
1.8.0
```

MQTTX CLIの動作をテストするには、まずMQTTサーバーに接続する必要があります。この記事では、EMQの[フリーのパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。これは、フルマネージドの[MQTTクラウド](https://www.emqx.com/ja/cloud)であるEMQX Cloud上で実行されており、次のアクセス情報を使用します。

- ブローカー：`broker.emqx.io`
- TCPポート：**1883**
- WebSocketポート：**8083**

コマンドラインを使用してMQTTサーバーに接続し、ターミナル内からメッセージをパブリッシュまたはサブスクライブできます。まず、ターミナルウィンドウ内のトピックをサブスクライブするコマンドを編集します。

**サブスクライブ**

```shell
mqttx sub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883
```

次に、先ほどサブスクライブしたトピックにメッセージをパブリッシュしてみましょう。リスニングサブスクライバーを実行したままにし、新しいターミナルウィンドウを作成して、以下のコマンドを入力します。

**パブリッシュ**

```shell
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -m 'hello from MQTTX CLI!'
```

この時点で、トピックをサブスクライブするコマンドのウィンドウに、先ほどパブリッシュされたメッセージが表示されます。

![MQTTX CLI Publish](https://assets.emqx.com/images/db6f9c76559376f3e490c1cf46e6eff2.png)

**複数のメッセージをパブリッシュする**

MQTTX CLIは、pubコマンドを使用して複数のメッセージをパブリッシュすることもサポートしています。エディターのコマンドに-Mパラメーターと-sパラメーターを追加し、各エントリを改行で区切るだけです。

```shell
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -s -M
```

![Publishing multiple messages](https://assets.emqx.com/images/3d565168651086abf2540de4a826af55.png)

最後に、MQTTX CLIと同じMQTTサービスにMQTTXデスクトップクライアントを接続することで、MQTTX CLIの機能をテストおよび検証します。MQTTX CLIを使用してメッセージをパブリッシュし、MQTTXデスクトップクライアントを介してそれを受信し、その逆のプロセスでMQTTXデスクトップクライアントを使用してMQTTX CLIにメッセージを送信します。この時点で、両側がそれぞれの送受信メッセージを受信していることがわかります。

![MQTTX desktop client ](https://assets.emqx.com/images/2a79737764ec04f5a1344ad84a06c3e5.png)

<center>MQTTXデスクトップクライアント</center>

<br>

Open 1520x

![MQTTX CLI](https://assets.emqx.com/images/4eff2f4b27c0de96b15bfb7878c9401a.png)

<center>MQTTX CLI</center>

## まとめ

以上で、MQTTX CLIを使用したMQTTメッセージパブリッシュ・サブスクライブ機能のテストと検証が完了しました。上記の一般的な機能に加えて、MQTTX CLIは、[ラストウィルメッセージ](https://www.emqx.com/en/blog/use-of-mqtt-will-message)の設定、SSL/TLSを使用したmqtts接続のテストなどもサポートしています。将来的にはMQTT 5.0接続もサポートされます。

MQTTX CLIのリリースにより、IoT開発者がMQTT接続をテストするための新しいオプションが提供されました。コマンドラインの呼び出し、デスクトップクライアントのダウンロード、オンラインブラウザを完全にサポートすることで、MQTTX 1.8.0は、さまざまなユースケースを持つユーザーがMQTTサービスまたはアプリケーションの開発とデバッグを完了し、独自のビジネス機能と安定性を向上させるのに役立ちます。使いやすいテストクライアントツールであるMQTTXと、効率的で信頼性の高いMQTTブローカーであるEMQXの組み合わせにより、IoT開発者は競争力のあるIoTプラットフォームとアプリケーションを構築できます。

## 付録：ユーザーヘルプ

コマンドラインに--helpパラメーターを入力してヘルプを取得したり、以下の使用法パラメーター表を確認してMQTTX CLIを使用したりできます。

```shell
# mqttxコマンドのヘルプを取得
mqttx --help
# subコマンドのヘルプを取得
mqttx sub --help
# pubコマンドのヘルプを取得
mqttx pub --help
```

| コマンド | 説明                       |
| :------- | :------------------------- |
| pub      | トピックにメッセージを発行 |
| sub      | トピックをサブスクライブ   |

**サブスクライブ**

| オプション         | 説明                                                        |
| :----------------- | :---------------------------------------------------------- |
| -h, --hostname     | ブローカーのホスト名（デフォルト："localhost"）             |
| -p, --port         | ブローカーのポート番号                                      |
| -i, --client-id    | クライアントID                                              |
| -q, --qos <0/1/2>  | メッセージのQoS（デフォルト：0）                            |
| --clean            | 指定されたIDの保留中のメッセージを破棄（デフォルト：true）  |
| -t, --topic        | メッセージのトピック                                        |
| -k, --keepalive    | SEC秒ごとにpingを送信（デフォルト：30）                     |
| -u, --username     | ユーザー名                                                  |
| -P, --password     | パスワード                                                  |
| -l, --protocol     | 使用するプロトコル（mqtt、mqtts、ws、wss）                  |
| --key              | 鍵ファイルのパス                                            |
| --cert             | 証明書ファイルのパス                                        |
| --ca               | CA証明書のパス                                              |
| --insecure         | サーバー証明書を検証しない                                  |
| --will-topic       | ラストウィルのトピック                                      |
| --will-message     | ラストウィルのメッセージ                                    |
| --will-qos <0/1/2> | ラストウィルのQoS                                           |
| --will-retain      | ラストウィルを保持メッセージとして送信（デフォルト：false） |
| -v, --verbose      | メッセージの前にトピックを表示                              |
| --help             | subコマンドのヘルプを表示                                   |

**パブリッシュ**

| オプション         | 説明                                                        |
| :----------------- | :---------------------------------------------------------- |
| -h, --hostname     | ブローカーのホスト名（デフォルト："localhost"）             |
| -p, --port         | ブローカーのポート番号                                      |
| -i, --client-id    | クライアントID                                              |
| -q, --qos <0/1/2>  | メッセージのQoS（デフォルト：0）                            |
| -t, --topic        | メッセージのトピック                                        |
| -m, --message      | メッセージの本文（デフォルト："Hello From MQTTX CLI"）      |
| -r, --retain       | 保持メッセージを送信（デフォルト：false）                   |
| -s, --stdin        | 標準入力からメッセージ本文を読み取る                        |
| -M, --multiline    | 標準入力から複数のメッセージとして行を読み取る              |
| -u, --username     | ユーザー名                                                  |
| -P, --password     | パスワード                                                  |
| -l, --protocol     | 使用するプロトコル（mqtt、mqtts、ws、wss）                  |
| --key              | 鍵ファイルのパス                                            |
| --cert             | 証明書ファイルのパス                                        |
| --ca               | CA証明書のパス                                              |
| --insecure         | サーバー証明書を検証しない                                  |
| --will-topic       | ラストウィルのトピック                                      |
| --will-message     | ラストウィルのメッセージ                                    |
| --will-qos <0/1/2> | ラストウィルのQoS（デフォルト：0）                          |
| --will-retain      | ラストウィルを保持メッセージとして送信（デフォルト：false） |
| --help             | pubコマンドのヘルプを表示                                   |
