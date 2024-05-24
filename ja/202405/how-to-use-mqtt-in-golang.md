## はじめに

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく軽量な[IoTメッセージング](https://www.emqx.com/ja/solutions/reliable-mqtt-messaging)プロトコルです。非常に少ないコードと帯域幅で、ネットワーク接続されたデバイスにリアルタイムかつ信頼性の高いメッセージングサービスを提供できます。IoT、モバイルインターネット、スマートハードウェア、[自動車のインターネット](https://www.emqx.com/ja/use-cases/internet-of-vehicles)、電力エネルギーなどの産業で広く使用されています。

Goは、クロスプラットフォームのオープンソースプログラミング言語です。高性能のアプリケーションを作成するために使用できます。GolangとMQTTを組み合わせることで、開発者はスケーラブルで安全なIoTアプリケーションを構築し、リアルタイムでデバイスと通信し、情報を交換し、複雑なデータ分析を実行できます。

この記事では、GolangプロジェクトでMQTTを使用して、クライアントと[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)間のシームレスな通信を実現する方法について包括的なガイドを提供します。接続の確立、トピックの購読と購読解除、メッセージの公開、リアルタイムでのメッセージの受信方法を学びます。このガイドは、MQTTを活用してスケーラブルで効率的なIoTアプリケーションを構築するためのスキルを身につけるのに役立ちます。

## Golang MQTTプロジェクトの準備

### Golangバージョンの確認

このプロジェクトでは、開発とテストにgo **v1.21.1**を使用します。正しいバージョンのGolangがインストールされていることを確認するには、次のコマンドを使用します。

```shell
$ go version
go version go1.21.1 darwin/amd64
```

### Golang MQTTクライアントのインストール

このプロジェクトでは、[MQTT クライアントライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)として [paho.mqtt.golang](https://github.com/eclipse/paho.mqtt.golang) を使用します。インストール方法は次のとおりです。

```shell
go get github.com/eclipse/paho.mqtt.golang
```

## MQTTブローカーの準備

続行する前に、通信およびテストに使用するMQTTブローカーがあることを確認してください。EMQX Cloudの使用をお勧めします。

[EMQX Cloud](https://www.emqx.com/ja/cloud)は、完全に管理されたクラウドネイティブのMQTTサービスであり、大量のIoTデバイスに接続し、さまざまなデータベースとビジネスシステムを統合できます。EMQX Cloudを使用すると、わずか数分で開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行できるため、グローバルな可用性と高速な接続が保証されます。

- サーバー：`broker.emqx.io`
- TCPポート：`1883`
- WebSocketポート：`8083`
- SSL/TLSポート：`8883`
- セキュアWebSocketポート：`8084`

## Golang MQTTの使用

### MQTT接続の作成

#### TCP接続

MQTT接続を確立するには、接続アドレス、ポート、クライアントIDを設定する必要があります。

```go
package main

import (
    "fmt"
    mqtt "github.com/eclipse/paho.mqtt.golang"
    "time"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
    fmt.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
    fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
    fmt.Printf("Connect lost: %v", err)
}

func main() {
    var broker = "broker.emqx.io"
    var port = 1883
    opts := mqtt.NewClientOptions()
    opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
    opts.SetClientID("go_mqtt_client")
    opts.SetUsername("emqx")
    opts.SetPassword("public")
    opts.SetDefaultPublishHandler(messagePubHandler)
    opts.OnConnect = connectHandler
    opts.OnConnectionLost = connectLostHandler
    client := mqtt.NewClient(opts)
    if token := client.Connect(); token.Wait() && token.Error() != nil {
        panic(token.Error())
  }
}
```

- ClientOptions：ブローカー、ポート、クライアントID、ユーザー名、パスワードなどのオプションを設定するために使用します。
- messagePubHandler：グローバルなMQTTパブリッシュメッセージ処理
- connectHandler：接続のコールバック
- connectLostHandler：接続が失われた場合のコールバック

#### TLS/SSL

[MQTTでTLSを使用する](https://www.emqx.com/ja/blog/fortifying-mqtt-communication-security-with-ssl-tls)と、情報の機密性と完全性を確保し、情報の漏洩や改ざんを防ぐことができます。TLS認証は、一方向認証と双方向認証に分類できます。

TSL接続を使用する場合は、次の設定を使用できます。

```go
func NewTlsConfig() *tls.Config {
    certpool := x509.NewCertPool()
    ca, err := ioutil.ReadFile("ca.pem")
    if err != nil {
        log.Fatalln(err.Error())
    }
    certpool.AppendCertsFromPEM(ca)
    // Import client certificate/key pair
    clientKeyPair, err := tls.LoadX509KeyPair("client-crt.pem", "client-key.pem")
    if err != nil {
        panic(err)
    }
    return &tls.Config{
        RootCAs: certpool,
        ClientAuth: tls.NoClientCert,
        ClientCAs: nil,
        InsecureSkipVerify: true,
        Certificates: []tls.Certificate{clientKeyPair},
    }
}
```

クライアント証明書が設定されていない場合は、次のように設定できます。

```go
func NewTlsConfig() *tls.Config {
    certpool := x509.NewCertPool()
    ca, err := ioutil.ReadFile("ca.pem")
    if err != nil {
        log.Fatalln(err.Error())
    }
    certpool.AppendCertsFromPEM(ca)
    return &tls.Config{
        RootCAs: certpool,
        }
}
```

次に、TLSを設定します。

```go
var broker = "broker.emqx.io"
var port = 8883
opts := mqtt.NewClientOptions()
opts.AddBroker(fmt.Sprintf("ssl://%s:%d", broker, port))
tlsConfig := NewTlsConfig()
opts.SetTLSConfig(tlsConfig)
// other options
```

### MQTTトピックのサブスクライブ

MQTTブローカーからトピックをサブスクライブするには、次のコードを使用します。

```go
func sub(client mqtt.Client) {
    topic := "topic/test"
    token := client.Subscribe(topic, 1, nil)
    token.Wait()
    fmt.Printf("Subscribed to topic %s", topic)
}
```

### MQTTメッセージのパブリッシュ

上記のトピックのサブスクライブとメッセージの監視が完了したら、メッセージをパブリッシュするための関数を作成します。

```go
func publish(client mqtt.Client) {
    num := 10
    for i := 0; i < num; i++ {
        text := fmt.Sprintf("Message %d", i)
        token := client.Publish("topic/test", 0, false, text)
        token.Wait()
        time.Sleep(time.Second)
    }
}
```

### テスト

テストには次のコードを使用します。

```go
package main

import (
    "fmt"
    mqtt "github.com/eclipse/paho.mqtt.golang"
    "log"
    "time"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
    fmt.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
    fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
    fmt.Printf("Connect lost: %v", err)
}

func main() {
    var broker = "broker.emqx.io"
    var port = 1883
    opts := mqtt.NewClientOptions()
    opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
    opts.SetClientID("go_mqtt_client")
    opts.SetUsername("emqx")
    opts.SetPassword("public")
    opts.SetDefaultPublishHandler(messagePubHandler)
    opts.OnConnect = connectHandler
    opts.OnConnectionLost = connectLostHandler
    client := mqtt.NewClient(opts)
    if token := client.Connect(); token.Wait() && token.Error() != nil {
        panic(token.Error())
    }

    sub(client)
    publish(client)

    client.Disconnect(250)
}

func publish(client mqtt.Client) {
    num := 10
    for i := 0; i < num; i++ {
        text := fmt.Sprintf("Message %d", i)
        token := client.Publish("topic/test", 0, false, text)
        token.Wait()
        time.Sleep(time.Second)
    }
}

func sub(client mqtt.Client) {
    topic := "topic/test"
    token := client.Subscribe(topic, 1, nil)
    token.Wait()
  fmt.Printf("Subscribed to topic: %s", topic)
}
```

コードを実行すると、MQTT接続とサブスクリプションに成功し、サブスクライブしたトピックのメッセージを正常に受信できることがわかります。

![Run code](https://assets.emqx.com/images/8882115bb9e0154ccfab16c26dd47566.png)

## Q&A

### **送信されたMQTTメッセージがJSON形式ではない場合はどうなりますか？**

MQTTメッセージがJSONではない場合でも、`toString()`メソッドを使用して文字列に変換できます。ただし、コンテンツが元々文字列ではない場合（たとえば、バイナリデータの場合）、データの性質に応じて異なる処理が必要になる場合があります。

### **メッセージのパブリッシュまたはサブスクライブ中に接続が切断された場合はどうなりますか？**

**paho.mqtt.golang**クライアントは、メッセージのパブリッシュまたはサブスクライブ中にブローカーに自動接続するオプションを提供します。また、自動再接続機能はデフォルトで有効になっています。

### **複数の接続を確立すると、なぜMQTTクライアント接続が切断されるのですか？**

複数のMQTT接続を確立するときは、異なるクライアントIDを使用してください。クライアントIDは、MQTT接続をMQTTブローカーに識別するために重要です。さらに、特定のデバイスまたはクライアントを識別します。トレーサビリティの観点から、デバイスのブローカーへの接続を明確に識別するクライアントIDを設定すると便利です。**MQTTブローカーは通常、既存の（古い）接続と同じクライアントIDを持つ新しい接続要求を受信したときに古い接続を閉じるメカニズムを実装し、その後、新しい接続を受け入れます。**

## まとめ

**paho.mqtt.golang**クライアントを使用して[パブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続し、テストクライアントとMQTTブローカー間の接続、メッセージのパブリッシュとサブスクリプションを実装しました。

次に、EMQが提供する[わかりやすいMQTTプロトコルガイド](https://www.emqx.com/ja/mqtt-guide)シリーズの記事をチェックして、MQTTプロトコルの機能について学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を開始できます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
