MQTT v5 には多くの新機能があります。これらの機能をわかりやすい方法で示し、これらの機能が開発者に与える影響について説明します。これまで、[MQTT V5 ](https://www.emqx.com/en/blog/introduction-to-mqtt-5)の新機能について説明してきました。本文は引き続き、「**User Properties」**について説明します。

## User Properties とは何ですか?

User Properties は、ユーザーがメタデータを MQTT メッセージに追加し、追加のユーザー定義情報を送信して、より多くのアプリケーション シナリオを拡張できるようにするユーザー定義のプロパティです。

User Properties は、メッセージ プロパティ フィールドで構成されたユーザー定義の UTF-8 key-value ペア配列で構成されます。最大メッセージ サイズを超えない限り、無制限のUser Properties を使用して MQTT メッセージにメタデータを追加し、パブリッシャー、MQTT ブローカー、およびサブスクライバー間で情報を転送できます。

HTTP プロトコルに精通している場合、この関数は HTTP ヘッダーの概念に非常に似ています。User Properties を使用すると、ユーザーは MQTT [プロトコル](https://www.emqx.com/en/mqtt-guide)を効果的に拡張でき、すべてのメッセージと応答に表示できます。User Properties はユーザーによって定義されるため、ユーザーのアクションに対してのみ意味を持ちます。

## なぜ User Properties が必要なのでしょうか?

User Properties は、MQTT 3 のスケーラビリティの低さを解決するために使用されます。メッセージ内であらゆる情報を送信できる可能性がある場合、ユーザーは自分のニーズを満たすために標準プロトコルの機能を拡張できます。

さまざまなオプションまたは構成を持つメッセージ タイプの場合、User Properties はクライアントと MQTT ブローカー間、またはクライアント間で送信できます。たとえば、接続されたクライアントでUser Properties が設定されている場合、それらは MQTT ブローカーでのみ受信でき、クライアントでは受信できません。メッセージの送信時に User Properties が設定されている場合、他のクライアントがメッセージを受信できます。一般的に使用される User Properties の設定は次の 2 種類です。

### 接続されたクライアントの User Properties 

クライアントが MQTT ブローカーとの接続を開始するとき、ブローカーは使用できるいくつかの必須メタデータ情報 (User Properties ) を事前定義できます。接続が成功すると、MQTT サービスは接続によって送信された関連情報を取得して使用できます。したがって、接続されたクライアントのUser Properties は MQTT ブローカーに依存します。

### メッセージパブリッシュ時のUser Properties 

メッセージ発行中のUser Properties は、クライアント間でメタデータ情報を転送できるため、より一般的に使用される場合があります。たとえば、メッセージをパブリッシュするときに、メッセージ番号、タイムスタンプ、ファイル、クライアント情報、ルーティング情報などの一般的な情報を追加できます。

前述のUser Properties 設定に加えて、トピックの購読時、購読解除時、または切断時にUser Properties を構成することもできます。

## User Properties の使用

### ファイル転送

[MQTT V5](https://www.emqx.com/en/blog/introduction-to-mqtt-5) のUser Properties は、メッセージ本文のペイロードにデータを入れて、以前の MQTT 3 のUser Properties にキーと値のペアを使用する代わりに、ファイル転送用に拡張できます。これは、ファイルをバイナリとして保持できることも意味します。ファイルのメタデータはUser Properties にあります。例えば：

```
{
  "filename": "test.txt",
  "content": "xxxx"
}
```

### リソース分析

クライアントが MQTT ブローカーに接続すると、さまざまなクライアントと、さまざまなベンダーのプラットフォームまたはシステムがさまざまな方法でメッセージ データを送信します。メッセージ データ形式には構造的な違いがある可能性があり、一部のクライアントは異なる地域に分散されています。たとえば、地域 A のデバイスによって送信されるメッセージ形式は JSON で、地域 B のデバイスによって送信されるメッセージ形式は XML です。このとき、サーバーは、データ分析に適切なパーサーを見つけるために、メッセージを受信した後、1 つずつ判断して比較する必要がある場合があります。

効率を向上させ、計算負荷を軽減するために、User Properties 機能を使用してデータ形式情報と地理情報を追加できます。サーバーはメッセージを受信すると、User Properties のメタデータを使用してデータを分析できます。さらに、エリア A のクライアント サブスクリプションがエリア B からクライアント メッセージを受信すると、特定のメッセージがどのエリアから来たのかをすぐに知ることができるため、メッセージを追跡できます。

```
{
  "region": "A",
  "type": "JSON"
}
```

![MQTT リソース分析](https://assets.emqx.com/images/c2f4e34d2ff553f12a81826382846366.png)

### メッセージルーティング

User Properties を使用して、アプリケーション レベルのルーティングを行うこともできます。上で述べたように、さまざまなシステムやプラットフォームがあり、各領域にはさまざまなデバイスがあります。複数のシステムが同じデバイスからメッセージを受信する場合があります。一部のシステムではデータをリアルタイムで表示する必要があり、別のシステムではこれらのデータを時系列で保存する場合があります。したがって、MQTT サーバーは、報告されたメッセージに設定されたUser Properties によって、メッセージを保存するシステムにメッセージを配布するか、データを提示するシステムに配布するかを決定できます。

```
{
  "type": "real-time",
  "timestamp": 1636620444
}
```

![MQTT メッセージルーティング](https://assets.emqx.com/images/39dfdc8de0b0251bab3697d72169dfef.png)

## MQTTクライアントでの設定方法

[MQTT.js](https://github.com/mqttjs/MQTT.js)クライアントを使用した、JavaScript によるプログラミングの例を見てみましょう。クライアントに接続するときに、最初に MQTT のバージョンを MQTT 5.0 として指定できます。

### 接続

接続時に、プロパティ オプションで User Properties を設定し、タイプとリージョンのプロパティを追加します。接続が成功すると、MQTT ブローカーはこのユーザー定義メッセージを受信します。

```
// connect options
const OPTIONS = {
  clientId: 'mqtt_test',
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
  protocolVersion: 5,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}
const client = mqtt.connect('mqtt://broker.emqx.io', OPTIONS)
```

### メッセージをパブリッシュする

接続が成功したら、サブスクライブしてメッセージのパブリッシュを選択し、メッセージのパブリッシュ構成で User Properties を設定します。次に、メッセージの受信を監視します。パブリッシュ機能では、 User Properties を構成します。パケットを出力して、メッセージをリッスンして受信する関数で構成された User Properties を確認します。

```
client.publish(topic, 'nodejs mqtt test', {
  qos: 0,
  retain: false,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}, (error) => {
  if (error) {
    console.error(error)
  }
})
client.on('message', (topic, payload, packet) => {
  console.log('packet:', packet)
  console.log('Received Message:', topic, payload.toString())
})
```

この時点で、パブリッシュ直前に設定した User Properties が出力され、コンソールに出力されていることがわかります。

他のクライアントについては、まず、[クロスプラットフォームMQTT 5.0 デスクトップ クライアント ツール - MQTTX](https://mqttx.app/ja)は User Properties のユーザー定義構成機能をサポートします。これにより、ユーザーは MQTT 5.0 のいくつかの新機能を迅速にテストできます。ぜひ試してください！



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
