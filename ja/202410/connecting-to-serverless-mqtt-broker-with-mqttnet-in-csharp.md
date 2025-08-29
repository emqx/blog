## はじめに

IoTの普及に伴い、.NETフレームワークはIoTアプリケーションの構築においてますます人気が高まっています。[Microsoftの.NET](http://xn--microsoft-8f4h.net/) [Coreと.NET](http://xn--core-ec4c.net/) Frameworkは、開発者にRaspberry Pi、HummingBoard、BeagleBoard、Pine A64などで動作するIoTアプリケーションを構築するためのツールとライブラリを提供します。

**MQTTnet**は、[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)を実装した高性能な.NETライブラリです。[GitHub](https://github.com/dotnet/MQTTnet)でオープンソース化されており、MQTT 5.0プロトコルやTLS/SSLのサポートなど豊富な機能を備えています。

この記事では、MQTTnetライブラリを使用してサーバーレスのMQTTブローカーに接続する方法を説明します。プロジェクト全体のコードは[MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet)からダウンロードできます。

## MQTTブローカーの準備

[EMQX Serverless](https://www.emqx.com/ja/cloud/serverless-mqtt)は、すべてのサーバーレスの利点を備えたパブリッククラウド上の[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)サービスです。数回のクリックで数秒以内にサーバーレスデプロイメントを開始できます。さらに、ユーザーは毎月100万の無料セッション分を獲得でき、23台のデバイスが1か月間オンラインになるのに十分であり、小規模なIoTテストシナリオに最適です。

[このブログのガイド](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service)に従って、無料でサーバーレスデプロイメントを作成できます。オンラインガイドの登録プロセスを完了すると、デプロイメントの「概要」に次のようなインスタンス情報が表示されます。後ほど接続情報とCA証明書を使用します。

![EMQX MQTT Cloud](https://assets.emqx.com/images/b7f54f0922422779d30df5ede63e66fb.png)

## MQTT C#デモ

### 1. .NETとVisual Studioのインストール

まだコンピュータに.NET環境をインストールしていない場合は、[Microsoftの公式ドキュメント](https://learn.microsoft.com/ja-jp/dotnet/core/install/)を参照して詳細なインストール手順を確認してください。

Visual Studioは、.NET開発者向けの総合的なIDEで、.NETアプリケーションの開発、デバッグ、デプロイのための豊富な機能を提供します。お使いのコンピュータのシステムとバージョンに応じて[こちら](https://visualstudio.microsoft.com/ja/downloads/)からダウンロードしてインストールできます。

### 2. MQTTnetパッケージのインストール

MQTTnetはNuGetパッケージマネージャー経由で提供されます。インストールするには、コンソールアプリケーションを作成し、NuGetを使用してMQTTnetパッケージをインストールします。Visual StudioでNuGetを使用する方法の詳細については、[公式ドキュメント](https://learn.microsoft.com/ja-jp/nuget/consume-packages/install-use-packages-visual-studio)を参照してください。Visual Studio for Macを使用している場合は、[Visual Studio for MacでのNuGetパッケージのインストールと管理](https://learn.microsoft.com/ja-jp/visualstudio/mac/nuget-walkthrough?toc=/nuget/toc.json)を参照してください。

### 3. MQTT接続の設定

EMQX Serverlessブローカーに接続するには、`MqttClientOptionsBuilder`クラスのインスタンスを作成し、ブローカーのアドレス、ポート、ユーザー名、パスワードなど必要なオプションを設定する必要があります。以下のコードスニペットは、`MqttClientOptionsBuilder`のインスタンスを作成する方法を示しています。

```c#
        string broker = "******.emqxsl.com";
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = "emqxtest";
        string password = "******";

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .Build();
```

接続パラメータは、ご自身のEMQX接続情報とログイン資格情報に置き換えてください。

- **ブローカーとポート**：サーバーデプロイメントの概要ページから接続アドレスとポート情報を取得します。
- **トピック**：トピックは異なるメッセージを識別・区別するために使用され、MQTTメッセージルーティングの基礎となります。
- **クライアントID**：各MQTTクライアントは一意のクライアントIDを持つ必要があります。.NETの`Guid.NewGuid()`を使用して新しい一意の識別子を生成できます。
- **ユーザー名とパスワード**：クライアント接続を確立するために、正しいユーザー名とパスワードを提供してください。以下の画像は、サーバー側の「認証とACL」の下でこれらの資格情報を設定する方法を示しています。

![Authentication & ACL](https://assets.emqx.com/images/d8f21d98e7330420f48323bada622839.png)

### 4. TLS/SSLの使用

EMQX Serverlessに接続する際、これはマルチテナントアーキテクチャに依存しており、複数のユーザーが単一のEMQXクラスターを共有できることに注意が必要です。このマルチテナント環境でのデータ転送のセキュリティと信頼性を確保するために、TLSが必要です。サーバーが自己署名証明書を使用している場合、デプロイメントの概要パネルから対応するCAファイルをダウンロードし、接続設定プロセス中に提供する必要があります。

TLSを追加し、証明書ファイルを`MqttClientOptionsBuilder`インスタンスに設定するには、`WithTls()`を使用します。以下のコードスニペットは、TLSを使用した`MqttClientOptionsBuilder`のインスタンスを作成する方法を示しています。

```c#
        string broker = "******.emqxsl.com";
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = "emqxtest";
        string password = "******";

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .WithTls(
                o =>
                {
                    // The used public broker sometimes has invalid certificates. This sample accepts all
                    // certificates. This should not be used in live environments.
                    o.CertificateValidationHandler = _ => true;

                    // The default value is determined by the OS. Set manually to force version.
                    o.SslProtocol = SslProtocols.Tls12; ;

                    // Please provide the file path of your certificate file. The current directory is /bin.
                    var certificate = new X509Certificate("/opt/emqxsl-ca.crt", "");
                    o.Certificates = new List<X509Certificate> { certificate };
                }
            )
            .Build();
```

### 5. MQTTブローカーへの接続

これでMQTTクライアントを作成し、接続オプションを設定したので、ブローカーに接続する準備ができました。MQTTクライアントの`ConnectAsync`メソッドを使用して接続を確立し、メッセージの送受信を開始します。

```c#
var connectResult = await mqttClient.ConnectAsync(options);
```

ここでは非同期プログラミングを使用しています。これにより、ブロッキングを防ぎつつメッセージのパブリッシュとサブスクライブが可能です。

### 6. トピックの購読

ブローカーに接続したら、`ResultCode`の値を確認して接続の成功を確認できます。接続が成功した場合、[MQTTトピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)を購読してメッセージを受信できます。

```c#
if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
        {
            Console.WriteLine("Connected to MQTT broker successfully.");

            // Subscribe to a topic
            await mqttClient.SubscribeAsync(topic);

            // Callback function when a message is received
            mqttClient.ApplicationMessageReceivedAsync += e =>
            {
                Console.WriteLine($"Received message: {Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment)}");
                return Task.CompletedTask;
            };
```

この関数内で、受信した対応するメッセージを表示することもできます。これにより、必要に応じて受信データを表示および処理できます。

### 7. メッセージのパブリッシュ

ブローカーにメッセージを送信するには、MQTTクライアントの`PublishAsync`メソッドを使用します。以下は、ループ内でブローカーにメッセージを送信する例で、1秒ごとにメッセージを1つ送信します。

```c#
for (int i = 0; i < 10; i++)
            {
                var message = new MqttApplicationMessageBuilder()
                    .WithTopic(topic)
                    .WithPayload($"Hello, MQTT! Message number {i}")
                    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
                    .WithRetainFlag()
                    .Build();

                await mqttClient.PublishAsync(message);
                await Task.Delay(1000); // Wait for 1 second
            }
```

### 8. 購読の解除

購読を解除するには、以下を呼び出します。

```c#
await mqttClient.UnsubscribeAsync(topic);
```

### 9. 接続の切断

接続を切断するには、以下を呼び出します。

```c#
await mqttClient.DisconnectAsync();
```

## 完全なコード

以下のコードは、サーバーへの接続、トピックの購読、メッセージのパブリッシュと受信方法を示しています。すべての機能の完全なデモについては、プロジェクトの[GitHubリポジトリ](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet)を参照してください。

```c#
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;

class Program
{
    static async Task Main(string[] args)
    {
        string broker = '******.emqxsl.com';
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = 'emqxtest';
        string password = '**********';

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .WithTls(
                o =>
                {
                    // The used public broker sometimes has invalid certificates. This sample accepts all
                    // certificates. This should not be used in live environments.
                    o.CertificateValidationHandler = _ => true;

                    // The default value is determined by the OS. Set manually to force version.
                    o.SslProtocol = SslProtocols.Tls12; 

                    // Please provide the file path of your certificate file. The current directory is /bin.
                    var certificate = new X509Certificate("/opt/emqxsl-ca.crt", "");
                    o.Certificates = new List<X509Certificate> { certificate };
                }
            )
            .Build();

        // Connect to MQTT broker
        var connectResult = await mqttClient.ConnectAsync(options);

        if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
        {
            Console.WriteLine("Connected to MQTT broker successfully.");

            // Subscribe to a topic
            await mqttClient.SubscribeAsync(topic);

            // Callback function when a message is received
            mqttClient.ApplicationMessageReceivedAsync += e =>
            {
                Console.WriteLine($"Received message: {Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment)}");
                return Task.CompletedTask;
            };

            // Publish a message 10 times
            for (int i = 0; i < 10; i++)
            {
                var message = new MqttApplicationMessageBuilder()
                    .WithTopic(topic)
                    .WithPayload($"Hello, MQTT! Message number {i}")
                    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
                    .WithRetainFlag()
                    .Build();

                await mqttClient.PublishAsync(message);
                await Task.Delay(1000); // Wait for 1 second
            }

            // Unsubscribe and disconnect
            await mqttClient.UnsubscribeAsync(topic);
            await mqttClient.DisconnectAsync();
        }
        else
        {
            Console.WriteLine($"Failed to connect to MQTT broker: {connectResult.ResultCode}");
        }
    }
}
```

## テスト

Visual Studioでプロジェクトを実行すると、以下のようにターミナルウィンドウに出力情報が表示されます。クライアントはMQTTブローカーへの接続に成功し、毎秒メッセージを受信しています。

![Run the project in Visual Studio](https://assets.emqx.com/images/531eee4b26982772feee05e14fc57e23.png)

また、別のクライアントとして[MQTTクライアントツール - MQTTX](https://mqttx.app/ja)を使用してメッセージの送受信テストを行うこともできます。MQTTXで「`Csharp/mqtt`」トピックを購読すると、毎秒メッセージを受信します。

![MQTTX](https://assets.emqx.com/images/49c1df9fd56d1a1301b6075ac34f3dda.png)

このトピックにメッセージをパブリッシュすると、サーバーがメッセージを受信し、MQTTXとコンソールの両方で確認できます。

![Received message displayed on MQTTX](https://assets.emqx.com/images/d803214cd47bc6656b1da92f4540827b.png)

<center>*MQTTXで受信したメッセージを表示*</center>

![Received message displayed on terminal](https://assets.emqx.com/images/23b4c6370911dfe7d91b5f2339b46333.png)

<center>*ターミナルで受信したメッセージを表示*</center>

## まとめ

この記事では、MQTTnetライブラリを使用してサーバーレスMQTTデプロイメントに接続するためのステップバイステップガイドを提供しました。これらの手順に従うことで、サバーレスのMQTTサービスを使用してパブリッシュおよびサブスクライブできる.NETアプリケーションを作成することに成功しました。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
