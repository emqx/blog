[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、現在IoT分野で最も一般的な通信プロトコルです。最新バージョンの5.0は、すでに2019年にリリースされています。以前のバージョンと比較すると、5.0はセッション期限、理由コード、共有サブスクリプション、リクエスト/レスポンスなど、現代のIoTアプリケーションのニーズに合った新機能が追加されており、今ではほとんどのIoT企業が選択するバージョンとなっています。

MQTT 5.0の全機能を包括的に理解していただくために、この記事では5.0で導入されたそれぞれの新機能を順に説明し、[EMQX](https://github.com/emqx/emqx)での使用方法を[MQTTX CLI](https://mqttx.app/ja)ツールを使用してデモンストレーションします。コマンドをコピー&ペーストすることで、記事のサンプルを簡単に実行できます。

める前に、以下の準備が必要です:

- Dockerを使用して、基本的なEMQXインスタンスをデプロイします。次のコマンドを実行してEMQXを起動できます：

  ```
  docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx:5.1.3
  ```

- [MQTTX CLI](https://mqttx.app/ja/downloads) 1.9.4をダウンロードおよびインストールします。これは、この記事のすべてのサンプルを実行するために使用する、オープンソースのMQTT 5.0コマンドラインクライアントツールです。
- [Wireshark](https://www.wireshark.org/) をインストールします。いくつかのサンプルでこれを使用してMQTTパケットをキャプチャおよび分析することで、何が起こっているのかをより良く理解できます。

## 機能1: セッション有効期限

MQTT 5.0では、クライアントはCONNECTパケットでセッション有効期限インターバルを指定できます。これは、ネットワーク接続が切断された後にセッションを保持する時間(秒数)を示します。サーバーがこの有効期限を受け入れられない場合は、CONNACKパケットで新しい有効期限を示すことができ、クライアントはサーバーの要求に従う必要があります。

セッション有効期限が切れる前に、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)とサーバーはそれぞれ適切なセッションステートを保持する必要があります。たとえば、サーバーはまだ確認されていない送信済みメッセージ、まだ送信されていないメッセージ、クライアントのサブスクリプションリストなどを保存する必要があります。

クライアントとサーバーの接続がセッション有効期限切れる前に回復すれば、中断されることなく通信を継続できます。

### サンプル1:

クライアントsub1がトピックt1をサブスクライブし、セッション有効期限を60秒に設定します。サブスクライブ後、ターミナルでCtrl + Cを押してクライアント接続を切断します。

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
```

60秒以内にトピックt1にメッセージを1つパブリッシュします。

```
mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

クライアントsub1を再接続しますが、ここでは--no-cleanオプションを指定して以前のセッションを再利用することを示します。接続する前にパブリッシュしたメッセージが受信されるはずです。

```
mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
payload: Hello World
✔  Subscribed to t1
```

### サンプル2:

EMQXのデフォルトの最大セッション有効期限は2時間です。EMQX Dashboard(ブラウザで `http://localhost:18083` )の**Management** -> **MQTT Settings** -> **Session**ページの**Session Expiry Interval**設定でこれを変更できます。

このサンプルでは、それを0秒に設定して、ネットワーク接続が切断されたときにセッションが即座に期限切れになるようにします。

![MQTT Session Expiry Interval](https://assets.emqx.com/images/84a3d445ad64b2bb5c0ac0d7575637cf.png?imageMogr2/thumbnail/1520x)

その後、サンプル1の手順を繰り返しますが、今回クライアントsub1は再接続時にメッセージを受信しません。

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1

mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published

mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
```

## 機能2: メッセージ有効期限

MQTT 5.0では、各メッセージに有効期限インターバル(秒数)を設定できます。メッセージがサーバーに保存されている時間がこの間隔を超えると、そのメッセージはクライアントに配信されなくなります。

これは、セッションを長期に保持したいが、時限メッセージを送信したい場合に非常に便利です。

また、クライアントがメッセージをパブリッシュするときに有効期限インターバルを設定した場合、サーバーはそのメッセージを転送するときに有効期限インターバルも含めますが、値はサーバーが受信した値からメッセージがサーバーに留まった時間を差し引いたものに更新されます。

これにより、受信者はそのメッセージが期限切れになることと、その期限がいつなのかを知ることができます。

### サンプル1

クライアントsub2がトピックt2をサブスクライブし、セッション有効期限を300秒に設定します。サブスクライブ後、Ctrl + Cで接続を切断します。

```
mqttx sub --client-id sub2 --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
```

同じトピックに5秒のメッセージ有効期限を設定してメッセージを1つパブリッシュします。

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 5
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

10秒待ってから、クライアントsub2を再接続しますが、直前にパブリッシュしたメッセージは受信されません。

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
```

### サンプル 2

トピックt2にメッセージをパブリッシュし、今度はメッセージ有効期限を60秒に設定します。

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 60
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

0秒待ってから、クライアントsub2を再接続すると、直前にパブリッシュしたメッセージが受信され、メッセージ有効期限は50秒になります。

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 0 --topic t2 --output-mode clean
{
  "topic": "t2",
  "payload": "Hello World",
  "packet": {
      ...
    "properties": {
      "messageExpiryInterval": 50
    }
  }
}
```

## 機能3: すべての応答パケットで理由コードをサポート

MQTT 5.0では、すべての応答パケットに理由コードフィールドが追加されると同時に、使用可能な理由コードも拡張されています。これにより、サーバーとクライアントは相手にエラーの理由をより明確に示すことができます。

たとえば、メッセージが到着したが、現在それにマッチするサブスクリプションがない場合、サーバーはそのメッセージを破棄します。ただし、メッセージの送信者にこの状況を知らせるために、サーバーは応答パケットのReason Codeを0x10に設定します。これは、マッチするサブスクライバがないことを示しています。

> *さまざまな理由コードに関する知識は、*[*MQTT 5.0 Reason Code チートシート*](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack) *を参照してください。*

### サンプル

Wiresharkを起動して正しいネットワークインタフェースを選択し、EMQXとMQTTX CLIが同じマシンで実行されている場合は、次のフィルタを入力してパケットをキャプチャします。

```
tcp.port == 1883
```

トピックt3にQoS 1メッセージをパブリッシュします。

```
mqttx pub --topic t3 --message "Hello World" --qos 1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

Wiresharkで、EMQXが返したPUBACKパケットのReason Codeが0x10に設定されているのが確認できます。

![Wireshark](https://assets.emqx.com/images/dc6b0ade500c1df276114bd14d4792fe.png?imageMogr2/thumbnail/1520x)

## 機能4: サーバー側での接続切断

MQTT 5.0では、サーバーはネットワーク接続を切断する前にDISCONNECTパケットを送信できるようになりました。これにより、クライアントに接続が切断された理由を示すことができます。

### サンプル

Wiresharkで次のフィルタを入力してパケットをキャプチャします。

```
tcp.port == 1883
```

MQTT接続を確立します。

```
mqttx conn --client-id conn4
…  Connecting...
✔  Connected
```

別のターミナルウィンドウで、EMQXのCLIコマンドを使用してクライアントを手動でキックアウトします。

```
docker exec emqx emqx ctl clients kick conn4
ok
```

1つ目のターミナルウィンドウで、接続が切断されたことを確認できます。

```
✖  Connection closed
```

EMQXが送信したDISCONNECTパケットのReason Codeは0x98に設定されており、この接続が管理操作によって閉じられたことを示しています。

![Wireshark](https://assets.emqx.com/images/05744c8ecd86b07215cff789c10425cb.png?imageMogr2/thumbnail/1520x)

## 機能5: ペイロードフォーマットとコンテンツタイプ

MQTT 5.0では、メッセージの送信者はPayload Format Indicatorを使用して、メッセージのコンテンツがUTF-8エンコードの文字データか、未指定のバイナリデータかを示すことができます。

Content Typeでは、受信者がメッセージのコンテンツの具体的なフォーマットをより簡単に知ることができるように、メッセージコンテンツの形式をさらに指示できます。一般的な慣例は、MIMEコンテンツタイプ(application/jsonなど)に設定することです。もちろん、これは必須ではなく、カスタムメッセージタイプを示すために任意のUTF-8文字列を使用することもできます。

### サンプル

トピックt6をサブスクライブします。

```
mqttx sub --topic t6 --output-mode clean
```

別のターミナルウィンドウで、トピックt6にメッセージをパブリッシュし、Payload Format Indicatorを設定してこのメッセージのコンテンツがUTF-8エンコードの文字データであることを示し、Content Typeをapplication/jsonに設定してJSONフォーマットのメッセージであることを示します。

```
mqttx pub --topic t6 --message "{\"content\": \"Hello World\"}" --payload-format-indicator --content-type application/json 
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

最初のターミナルウィンドウでは、受信したメッセージにContent TypeとPayload Format Indicatorが含まれているのが確認できます。

```
{
  "topic": "t6",
  "payload": "{\"content\": \"Hello World\"}",
  "packet": {
        ...
    "properties": {
      "contentType": "application/json",
      "payloadFormatIndicator": true
    }
  }
}
```

## 機能6: リクエスト/レスポンス

MQTTは、リクエスト側のリクエストが必ずレスポンス側に受信されることや、その逆も保証できません。したがって、リクエスト側は自身が送信したリクエストと受信したレスポンスを適切に関連付けることができなければなりません。MQTT 5.0では、リクエストメッセージに対比データ(Correlation Data)を設定できます。レスポンス側はこの対比データをそのままレスポンスメッセージに戻します。これによりリクエスト側は、それがどのリクエストのレスポンスかを知ることができます。

### サンプル

1つ目のターミナルウィンドウで、レスポンス側はリクエストトピックをサブスクライブします。

```
mqttx sub --client-id responder --topic request --session-expiry-interval 300 --output-mode clean
```

2つ目のターミナルウィンドウで、リクエスト側はリクエストメッセージをパブリッシュし、レスポンストピックを response/requester1 に設定します。

```
mqttx pub --client-id requester1 --session-expiry-interval 300 --topic request --message "This is a reuqest" --response-topic response/requester1 --correlation-data request-1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

1つ目のターミナルウィンドウで、レスポンス側はリクエストメッセージを受信し、レスポンストピックと対比データが含まれているのを確認できます。

```
{
  "topic": "request",
  "payload": "This is a reuqest",
  "packet": {
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      },
      "responseTopic": "response/requester1"
    }
  }
}
```

2つ目のターミナルウィンドウで、リクエスト側はレスポンストピックをサブスクライブします(実際のアプリケーションでは、リクエストをパブリッシュする前にレスポンストピックをサブスクライブする必要があります)。

```
mqttx sub --client-id requester1 --no-clean --session-expiry-interval 300 --topic response/requester1 --output-mode clean
```

1つ目のターミナルウィンドウで、レスポンス側はレスポンストピックにレスポンスをパブリッシュし、対比データを含めます。

```
mqttx pub --client-id responder --topic response/requester1 --message "This is a response" --correlation-data request-1
```

2つ目のターミナルウィンドウで、リクエスト側はレスポンスを受信します。

```
{
  "topic": "response",
  "payload": "This is a response",
  "packet": {
      ...
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      }
    }
  }
}
```

## 機能7: 共有サブスクリプション

MQTT 5.0では、サブスクライバーを複数のサブスクリプショングループに分割する共有サブスクリプションがサポートされ、メッセージはすべてのサブスクリプショングループに転送されますが、グループ内のクライアントはラウンドロビンなどの戦略でメッセージを受信します。これらの戦略はサーバー側で完全に実装されるので、クライアント側の変更は必要ありません。必要なのは、$share/{ShareGroup}/{Topic}を使用して共有サブスクリプションを開始することだけです。

### サンプル

1つ目のターミナルウィンドウで、トピック $share/g1/t7 をサブスクライブします。

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

2つ目のターミナルウィンドウで、同じトピック $share/g1/t7 をサブスクライブします。

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

3つ目のターミナルウィンドウで、代わりにトピック $share/g2/t7 をサブスクライブします。

```
mqttx sub --topic '$share/g2/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g2/t7...
✔  Subscribed to $share/g2/t7
```

4つ目のターミナルウィンドウで、トピック t7にメッセージをパブリッシュします。ここでは --multiline オプションを使用して、改行ごとに複数のメッセージを送信します。

```
mqttx pub --topic t7 -s --stdin --multiline
…  Connecting...
✔  Connected, press Enter to publish, press Ctrl+C to exit
Message 1
Message 2
Message 3
Message 4
Message 5
Message 6
```

EMQXのデフォルトの共有サブスクリプション戦略はround_robinなので、メッセージは同じサブスクリプショングループ内のサブスクライバにラウンドロビンで配信されます。したがって、1つ目と2つ目のターミナルウィンドウのサブスクライバはメッセージを交互に受信します。

```
payload: Message 1

payload: Message 3

payload: Message 5
payload: Message 2

payload: Message 4

payload: Message 6
```

一方、グループg2にはサブスクライバが1つしかないため、3つ目のターミナルウィンドウではすべてのメッセージが受信されます。

```
payload: Message 1

payload: Message 2

payload: Message 3

payload: Message 4

payload: Message 5

payload: Message 6
```

## 機能8: サブスクリプション識別子

MQTT 5.0では、クライアントはサブスクライブ時にサブスクリプション識別子を設定できます。サーバーはこの識別子をサブスクリプションにバインドし、そのサブスクリプションにメッセージを転送するときは対応する識別子をメッセージに追加します。クライアントはメッセージのサブスクリプション識別子を使用して、どのコールバックを起動するか、または他の操作を実行するかを決定できます。

### サンプル

同じクライアントがトピックt8/1とt8/#をサブスクライブし、異なるサブスクリプション識別子を設定します。

```
mqttx sub --client-id sub8 --session-expiry-interval 300 --topic t8/1 --subscription-identifier 1
…  Connecting...
✔  Connected
…  Subscribing to t8/1...
✔  Subscribed to t8/1

mqttx sub --client-id sub8 --no-clean --session-expiry-interval 300 --topic t8/# --subscription-identifier 2 --output-mode clean
```

2つ目のターミナルウィンドウで、トピックt8/1にメッセージをパブリッシュします。

```
mqttx pub --topic t8/1 --message "Hello World"
```

1つ目のターミナルウィンドウのサブスクライバは2つのメッセージを受信し、メッセージのサブスクリプション識別子から、1つ目はトピックt8/#のサブスクリプションからのメッセージで、2つ目はトピックt8/1のサブスクリプションからのメッセージであることがわかります。

```
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "subscriptionIdentifier": 2
    }
  }
}
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "subscriptionIdentifier": 1
    }
  }
}
```

> *MQTTサーバーは、メッセージがクライアントの複数のサブスクリプションとマッチする場合、それらの重複するサブスクリプションに対してメッセージを1つずつ送信することも、1つのメッセージのみを送信することもできます。EMQXは前者の挙動を取ります。*

## 機能9: トピックエイリアス

MQTT 5.0では、パブリッシュ時に2バイトの整数型のトピックエイリアスを使用してトピック名を置き換えることができます。これにより、トピック名が長い場合にPUBLISHパケットのサイズを効果的に削減できます。

トピックエイリアスを使用するには、最初にトピック名とトピックエイリアスの両方を含むメッセージを送信して、マッピングを確立する必要があります。その後、トピックエイリアスのみを含むメッセージを送信できます。

トピックエイリアスのマッピングはセッションステートの一部ではないので、クライアントが再接続してもセッションを回復しても、クライアントとサーバーはトピックエイリアスのマッピングを再確立する必要があります。

一般に、クライアントとサーバーが使用するトピックエイリアスのマッピングは相互に独立しています。したがって、クライアントがサーバーに送信するトピックエイリアス1のメッセージと、サーバーがクライアントに送信するトピックエイリアス1のメッセージは、通常は異なるトピックにマッピングされます。

クライアントとサーバーは、接続時に互いに送信できるトピックエイリアスの最大値について合意できます。EMQXのデフォルトでは、トピックエイリアスの最大値は65535です。EMQX Dashboard(ブラウザで [http://localhost:18083](http://localhost:18083/) )の**Management** -> **MQTT Settings** -> **General**ページの**Max Topic Alias**設定でこれを変更できます。

![MQTT 主题别名](https://assets.emqx.com/images/c853659e22cf620edc4eadb562cf7633.png?imageMogr2/thumbnail/1520x)

## 機能10: トラフィック制御

MQTT 5.0では、クライアントとサーバーは接続時に受信最大値(Receive Maximum)を使用して、同時に処理できる未確認のQoS 1およびQoS 2メッセージの最大数を相手に示すことができます。

送信済みでまだ完全に確認されていないメッセージの数が受信最大値の制限に達した場合、送信側は受信側にさらにメッセージを送信できなくなります(QoS 0メッセージはこの制限の対象外)。これにより、送信側の送信が受信側の処理能力を超えるのを効果的に回避できます。

## 機能11: ユーザプロパティ

MQTT 5.0のほとんどのパケットにユーザプロパティを含めることができます。ユーザプロパティは、UTF-8でエンコードされた文字列からなる名前と値のペアであり、名前と値の具体的な内容はクライアントとサーバーの実装によって自由に定義できます。パケットの最大長を超えない範囲で、任意の数のユーザプロパティを指定できます。

CONNECTやSUBSCRIBEなどのパケットのユーザプロパティは、通常その[MQTTサーバー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)の実装に依存します。

一方、PUBLISHパケットのユーザプロパティは、サーバーによってそのままサブスクライバに転送されるので、メッセージの発行側とサブスクライバ側でユーザプロパティの内容について合意していれば問題ありません。たとえば、アプリケーションメッセージのユーザプロパティに発行側のクライアントIDを付加することで、サブスクライバ側はメッセージの送信元を知ることができます。

サンプル:

トピックt11をサブスクライブします。

```
mqttx sub --topic t11 --output-mode clean
```

別のターミナルウィンドウで、トピックt11にメッセージをパブリッシュし、メッセージの送信元と送信日時を示す2つのユーザプロパティを設定します。

```
mqttx pub --client-id pub11 --topic t11 --message "Hello World" --user-properties "from: pub11" --user-properties "timestamp: 1691046633"
```

最初のターミナルウィンドウでは、サブスクライバが設定したユーザプロパティを含むメッセージを受信しました。

```
{
  "topic": "t11",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "userProperties": {
        "from": "pub11",
        "timestamp": "1691046633"
      }
    }
  }
}
```

## 機能12: 最大パケットサイズ

MQTT 5.0では、クライアントとサーバーは接続時に最大パケットサイズ「Maximum Packet Size」属性で、処理できる最大パケットサイズを互いに通知できます。その後、双方ともに合意された制限を超えるサイズのパケットを送信してはなりません。そうしないと、接続はプロトコルエラーで切断されます。

したがって、PUBLISHパケットが大きすぎて転送できない場合、サーバーはそのパケットを単に破棄します。

### サンプル1:

1つ目のターミナルウィンドウで、クライアントはサーバーに対して自身が受け入れ可能な最大パケットサイズが128バイトであることを宣言し、トピックt12をサブスクライブします。

```
mqttx sub --maximum-packet-size 128 --topic t12
…  Connecting...
✔  Connected
…  Subscribing to t12...
✔  Subscribed to t12
```

2つ目のターミナルウィンドウで、128バイト未満のメッセージをパブリッシュします。

```
payload=$(head -c 10 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "$payload"
```

1つ目のターミナルウィンドウのサブスクライバはメッセージを受信します。

```
payload: 0000000000
```

次に2つ目のウィンドウで128バイトを超えるメッセージをパブリッシュすると、1つ目のウィンドウのサブスクライバはそのメッセージを受信しません。

```
payload=$(head -c 128 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "${payload}"
```

今回、1つ目のターミナルウィンドウのサブスクライバはメッセージを受信しませんでした。サブスクライバの接続をCtrl + Cで切断した後、以下のコマンドを実行してEMQXのログを確認します。

```
docker logs emqx
```

frame_is_too_large のためメッセージが破棄されたというログが表示されます。

```
2023-08-03T06:17:52.538541+00:00 [warning] msg: packet_is_discarded, mfa: emqx_connection:serialize_and_inc_stats_fun/1, line: 872, peername: 172.17.0.1:39164, clientid: mqttx_f0a3847c, packet: PUBLISH(Q0, R0, D0, Topic=t12, PacketId=undefined, Payload=******), reason: frame_is_too_large
```

### サンプル2:

EMQXのデフォルトの最大パケットサイズは1MBですが、これはEMQX Dashboard(ブラウザで `http://localhost:18083` )の**Management** -> **MQTT Settings** -> **General**ページのMax Packet Sizeの設定画面から変更できます。本サンプルでは1024バイトに設定します。

注意: 制限されるのはすべてのパケットの最大長です。そのため、最大パケット長を小さく設定しすぎると、接続できなくなる可能性があります。これは避ける必要があります。

本サンプルでは、最大長を1024バイトに変更します:

![图片.png](https://assets.emqx.com/images/512963490e383148c2288bf5255f8751.png?imageMogr2/thumbnail/1520x)

そして、Wiresharkでパケットをキャプチャします。

```
tcp.port == 1883
```

1024バイトを超えるメッセージをパブリッシュすると、EMQXはDISCONNECTパケットを返し、Reason Codeを0x95に設定します。これは、大きすぎるパケットを受信したために、接続が閉じられたことを示しています。

```
payload=$(head -c 1024 < /dev/zero | tr '\0' 0)
mqttx pub --client-id pub12 --topic t12 -m "${payload}"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

![Wireshark](https://assets.emqx.com/images/3ac6a07014588cc82ea14365795e8843.png?imageMogr2/thumbnail/1520x)

## 機能13: オプションのサーバ機能

MQTTでは、サーバーはプロトコルで定義された機能や特性の一部を完全にサポートしていなくても良いが、サポートしていない機能をCONNACKパケットでクライアントに通知する必要があります。これにより、クライアントは使用不可の機能を使用しないようにできます。オプションのサーバ機能には、

- サポートする最大QoSレベル
- 保留メッセージ
- ワイルドカードサブスクリプション
- サブスクリプション識別子
- 共有サブスクリプション

クライアントがサーバーが使用不可であると通知した機能を使用した場合、プロトコルエラーが発生してサーバーは接続を閉じます。

### サンプル

EMQXの設定ページから、ワイルドカードサブスクリプション、共有サブスクリプション、保留メッセージなどの機能を手動で無効にできます。本サンプルでは、保留メッセージを無効にします。

![MQTT 关闭保留消息](https://assets.emqx.com/images/16873e4be8c387d5766c68b69d2a51f1.png?imageMogr2/thumbnail/1520x)

そして、Wiresharkでパケットをキャプチャします。

```
tcp.port == 1883
```

保留メッセージをパブリッシュすると、EMQXはCONNACKパケットで保留メッセージが使用不可であることを通知しました。

```
mqttx pub --topic t13 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

その後、クライアントが保留メッセージを送信すると、EMQXはDISCONNECTパケットを返し、Reason Codeを0x9Aに設定します。これは、サーバーが保留メッセージをサポートしていないことを示しています。

![Wireshark](https://assets.emqx.com/images/e79cda1541771f559068a4813d1d3ded.png?imageMogr2/thumbnail/1520x)

このサンプル後は、EMQXの保留メッセージ機能を再び有効にしてください。

## 機能14: サブスクリプションオプション

MQTT 5.0は、QoSに加えて、No Local、Retain As Published、Retain Handlingの3つの新しいサブスクリプションオプションを提供します。

1. No Local：メッセージを、そのメッセージを発行したクライアントに転送してよいかどうかを指示します。
2. Retain As Published: サーバーがメッセージをそのサブスクリプションに転送するときに、Retainフラグを保持する必要があるかどうかを指示します。
3. Retain Handling：サブスクリプションの確立時に、サーバーが保留メッセージをそのサブスクリプションに送信する必要があるかどうかを指示します。値は0、1、2のいずれかです。
   1. 0を設定: サブスクリプションが確立したら、保留メッセージを送信する。
   2. 1を設定: サブスクリプションが確立したときに、そのサブスクリプションがまだ存在しない場合のみ、保留メッセージを送信する。
   3. 2を設定: サブスクリプションの確立時には保留メッセージを送信しない。

[MQTTのサブスクリプションオプション](https://www.emqx.com/en/blog/an-introduction-to-subscription-options-in-mqtt)の使い方 を参照して、これらのオプションの詳細を理解してください。

### サンプル1 - No Local:

クライアントsub14とpub14がそれぞれトピックt14にメッセージをパブリッシュします。EMQXの[遅延パブリッシュ](https://docs.emqx.com/zh/emqx/v5.1/messaging/mqtt-delayed-publish.html#延迟发布)機能を利用して、メッセージを10秒遅延させます。

```
mqttx pub --client-id sub14 --topic '$delayed/10/t14' --message "You will not receive this message"
mqttx pub --client-id pub14 --topic '$delayed/10/t14' --message "You will receive this message"
```

そして、クライアントsub14はトピックt14をサブスクライブし、No Localオプションを設定します。これにより、sub14はpub14が発行したメッセージのみを受信し、自身が発行したメッセージは受信しません。

```
mqttx sub --client-id sub14 --topic t14 --no_local
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: You will receive this message
```

### サンプル2 - Retain As Published:

1つ目のターミナルウィンドウで、トピックt14をRetain As Publishedオプションを設定してサブスクライブします。

```
mqttx sub --topic t14 --retain-as-published --output-mode clean
```

2つ目のターミナルウィンドウで、トピックt14に保留メッセージをパブリッシュします。

```
mqttx pub --topic t14 --message "Hello World" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

1つ目のウィンドウのサブスクライバは、Retainフラグが設定されたメッセージを受信しました。

```
{
  "topic": "t14",
  "payload": "Hello World",
  "packet": {
      ...
    "retain": true,
        ...
  }
}
```

保留メッセージのクリア

```
mqttx pub --topic t14 --message '' --retain
```

### サンプル3 - Retain Handling

トピックt14に保留メッセージを1つパブリッシュします。

```
mqttx pub --topic t14 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

その後、同じトピックをサブスクライブし、Retain Handlingを0に設定すると、保留メッセージが受信されます。

```
mqttx sub --client-id sub14 --session-expiry-interval 300 --topic t14 --retain-handling 0
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: This is a retained message
retain: true
```

接続をCtrl + Cで切断して再接続し、Retain Handlingを1に設定すると、保留メッセージは受信されません。

```
mqttx sub --client-id sub14 --no-clean --session-expiry-interval 300 --topic t14 --retain-handling 1
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
```

さらにCtrl + Cで切断して完全に新しいセッションで再接続し、Retain Handlingを2に設定すると、今度も保留メッセージは受信されません。

```
mqttx sub --client-id sub14 --topic t14 --retain-handling 2
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
```

最後に、保留メッセージをクリアしておきます。

```
mqttx pub --topic t14 --message '' --retain
```

## 機能15: ラストウィル遅延

MQTT 5.0では、クライアントは遺言メッセージに遅延インターバルを設定できるようになりました。これにより、ネットワーク接続が切断された直後に遺言メッセージが送信されるのではなく、遅延インターバルが経過するまで保留されます。接続がその間に回復すれば、遺言メッセージは送信されません。これにより、接続の短期的な中断によって不要な遺言メッセージが送信されることが回避できます。

遺言メッセージの遅延インターバルがセッション有効期限よりも長い場合、セッション有効期限が切れたときに遺言メッセージがただちに送信されるので、セッション有効期限切れ通知に遺言メッセージを使うこともできます。

### サンプル1:

1つ目のターミナルウィンドウで、トピックt15をサブスクライブします。

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
```

2つ目のターミナルウィンドウで、遺言メッセージと10秒の遅延インターバルを設定してMQTT接続を確立します。接続後、Ctrl+Cで切断します。

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
```

1つ目のウィンドウのサブスクライバは10秒後に遺言メッセージを受信します。

```
payload: I'm offline
```

### サンプル2:

2つ目のターミナルウィンドウで、同じ遺言メッセージ設定で再接続します。

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
```

Ctrl+Cで切断した後、10秒以内に再接続すると、1つ目のウィンドウでは遺言メッセージは受信されませんでした。

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --no-clean --session-expiry-interval 300
```

### サンプル3:

遺言メッセージに Will Retain フラグを設定することで、保留メッセージとすることができます。これにより、サブスクライバがオフラインのために遺言メッセージを見逃すことを防げます。

2つ目のターミナルウィンドウで、遺言メッセージの遅延インターバルを0に設定したMQTT接続を再確立します。Ctrl + Cで切断すると、遺言メッセージはただちに発行されます。

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 0 --will-retain --session-expiry-interval 300
…  Connecting...
✔  Connected
```

1つ目のターミナルウィンドウでトピックt15をサブスクライブすると、前に発行された遺言メッセージが受信されます。

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
payload: I'm offline
retain: true
```

## 機能16: サーバーがキープアライブ時間を指定

キープアライブ時間は、クライアントが連続する2つのコントロールパケットの送信間隔の最大値を決定します。サーバーは、この間隔内にクライアントからレポートがあるかどうかによって、そのクライアントがまだアクティブかどうかを判断できます。

MQTT 5.0では、サーバーはクライアントが指定したキープアライブ時間を拒否し、CONNACKパケットでクライアントに使用するキープアライブ時間を指示できます。クライアントは、通信を維持するためにそのキープアライブ時間を使用しなければなりません。

### サンプル:

EMQXのデフォルトはクライアント指定のキープアライブ時間ですが、これは EMQX Dashboard(ブラウザで [http://localhost:18083](http://localhost:18083/) )の**Management** -> **MQTT Settings** -> **General**ページのServer Keep Alive設定でこれを変更できます。

本サンプルでは、Server Keep Alive を10秒に設定します。

![MQTT 保活时间](https://assets.emqx.com/images/db10dece7733daaa0bde63bdda8e314e.png?imageMogr2/thumbnail/1520x)

そして、Wiresharkでパケットをキャプチャします。

```
tcp.port == 1883
```

クライアントが30秒のキープアライブ時間を指定して接続すると、EMQXはCONNACKパケットで10秒のServer Keep Aliveを返しました。その後、クライアントは10秒ごとにキープアライブパケットを送信します。

```
mqttx conn --keepalive 30
…  Connecting...
✔  Connected
```



## 機能17: サーバーが割り当てたクライアントIDをリプライ

MQTT 5.0では、クライアントが長さ0のクライアントIDで接続すると、サーバーがそのクライアントに一意のIDを割り当てます。この割り当てられたIDは、CONNACKパケットでクライアントに返されます。これにより、クライアントは次回の接続でセッションを回復するために必要なクライアントIDがわからないという問題が解決します。

### サンプル

Wiresharkでパケットをキャプチャします。

```
tcp.port == 1883
```

クライアントが長さ0のクライアントIDで接続すると、EMQXのCONNACKパケットにAssigned Client Identifier属性が含まれ、そこに割り当てられたIDが設定されています。

ターミナルウィンドウに戻り、長さ0の文字列をClient IDに設定してMQTT接続を開始します。

```
mqttx conn --client-id ''
```

Wiresharkで、EMQXが返したCONNACKパケットにAssigned Client Identifier属性が含まれているのが確認できます。その値がEMQXによってクライアントに割り当てられたClient IDです。

## まとめ

以上が、MQTT 5.0の全機能の基本的な紹介とデモンストレーションです。ぜひこれらの手順をコードに変換してクライアントで再現してみてください。MQTT 5.0の新機能についてさらに詳細を知りたい場合は、[MQTTガイド](https://www.emqx.com/en/mqtt-guide)をご覧ください。MQTTに関する必要なすべての知識が揃っています。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
