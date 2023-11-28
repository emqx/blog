Will Messageは、[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)の重要な機能で、クライアントがオフラインになったことをサーバーだけが知る問題を解決します。これにより、予期せずオフラインになったクライアントに対して、適切なフォローアップアクションを取ることができます。

この記事では、MQTT Will Messageについて、その概要と動作方法を詳しく解説します。なお、この記事の一部内容はセッションやRetain Messageの概念に関わるため、必要に応じて以下の2つのブログを参照してください：

1. [Clean Startとセッション有効期間の紹介](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)
2. [MQTTRetain Message入門](https://www.emqx.com/en/blog/mqtt5-features-retain-message)

## MQTT Will Messageとは何ですか？

現実世界では、人は遺言を作成し、自分の財産がどのように分配され、死後にどのような行動を取るべきかを述べることができます。人が亡くなると、遺言執行者が遺言をパブリッシュし、遺言の指示に従って行動します。

MQTTでは、クライアントは接続時にサーバーにWill Messageを登録できます。通常のメッセージと同様に、Will Messageのトピック、ペイロード、その他のフィールドを設定できます。クライアントが予期せず切断された場合、サーバーはこのWill Messageを対応するトピックに登録している他のクライアントに送信します。したがって、これらの受信者は、ユーザーに通知を送信するか、バックアップデバイスに切り替えるなど、迅速に行動を取ることができます。

例えば、あまり変わらない値を監視するセンサーがあるとします。通常の実装方法は、最新の値を定期的にパブリッシュすることですが、より良い実装方法は、値が変わったときにのみRetain Messageの形で送信することです。これにより、新しいサブスクライバーは、センサーが再度パブリッシュするのを待つことなく、すぐに現在の値を取得できます。

しかし、これはまた、サブスクライバーが時宜に合わせたメッセージの受信に基づいてセンサーがオフラインかどうかを判断できないことを意味します。Will Messageを使用することで、センサーから値がパブリッシュされるのを常に待つことなく、センサーがキープアライブタイムアウトになるとすぐに知ることができます。

### Will Messageまたは遺言（LWT）？

ブログやコードの中で、「遺言（Last Will and Testament）」、またはその略称「LWT」という名前を見ることがあります。これはMQTTのWill Messageを指しています。これら2つの名前が共存している理由は、MQTT 3.1プロトコルの概要で「遺言（Last Will and Testament）」という概念が言及されていたためかもしれません。

MQTTでは、プロトコルの本文では常に「Will Message」という名前が明確に使用されていましたが、ユーザーの間ではこれら2つの名前がしばしば交換可能に使われています。

どちらの使用を正すつもりはありません。異なる名前による混乱を避けたいだけです。

## MQTT Will Messageの動作方法は？

### クライアントは接続時にWill Messageを指定する

Will Messageは、クライアントが接続を開始するときに指定され、クライアントIDやClean Startなどのフィールドと一緒に、クライアントからサーバーへ送信されるCONNECTパケットに含まれます。

通常のメッセージと同様に、Will Messageのトピック（Will Topic）、保持フラグ（Will Retain）、プロパティ（Will Properties）、QoS（Will QoS）、ペイロード（Will Payload）を設定できます。

![mqtt will message fields](https://assets.emqx.com/images/293f990f249a16a5236ed4daaaba5877.jpg)

これらのフィールドの使用法は通常のメッセージと同様です。唯一の区別は、Will Messageで使用可能なプロパティが通常のアプリケーションメッセージとは若干異なることです。以下の表は、それらの具体的な違いをリストしています：

![mqtt will message](https://assets.emqx.com/images/20a001856d5ca98f6c255cc60bd53d0b.jpg)

Will Messageは常にクライアントが「死亡」した後にパブリッシュされます。ある意味で、これはクライアントが送信する最後のメッセージでもあります。したがって、トピックエイリアスはWill Messageには意味がありません。

さらに、Will Messageには独占的なプロパティがあります：**Will Delay Interval**。これは、Will Messageに対して[MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5)が導入した重要な改善点ですが、これについては後で詳しく説明します。

### 接続が予期せず閉じられた場合、サーバーがWill Messageをパブリッシュする

クライアントが接続時にWill Messageを指定する場合、サーバーは対応するセッションにこのWill Messageを保存し、以下のいずれかの条件が満たされてパブリッシュするまで保持します：

- サーバーによって検出されたI/Oエラーまたはネットワーク障害。
- クライアントがキープアライブ時間内に通信に失敗する。
- クライアントが0x00（正常な切断）の理由コードを持つDISCONNECTパケットを送信せずにネットワーク接続を閉じる。
- サーバーが0x00（正常な切断）の理由コードを持つDISCONNECTパケットを受信せずにネットワーク接続を閉じる。例えば、メッセージや行動がプロトコルの要件を満たしていないためにクライアントを切断する場合など。

簡単に言うと、0x00の理由コードを持つDISCONNECTパケットをサーバーが受信せずにネットワーク接続が閉じられた場合、サーバーはWill Messageを送信する必要があります。

クライアントが作業を完了し、積極的にログオフする場合、0x00の理由コードを持つDISCONNECTパケットを送信し、ネットワーク接続を閉じてサーバーがWill Messageをパブリッシュするのを防ぐことができます。

### Will Delay Intervalと遅延パブリッシュ

デフォルトでは、サーバーはネットワーク接続が予期せず閉じられたときにすぐにWill Messageをパブリッシュします。しかし、ネットワーク接続の中断は通常一時的であり、クライアントは接続を回復して前のセッションを続行することができます。これにより、Will Messageが頻繁かつ意味なく送信される可能性があります。

したがって、MQTT 5.0はWill MessageのためにWill Delay Intervalプロパティを特に追加しました。これは、サーバーがネットワーク接続が閉じた後にWill Messageのパブリッシュを遅延する時間を決定します（秒単位）。

![mqtt will delay interval](https://assets.emqx.com/images/ab9a228706332d8f391d537c92b1b369.png)

Will Delay Intervalが指定されていない場合、または0に設定されている場合、サーバーはネットワーク接続が閉じるとすぐにWill Messageをパブリッシュします。

Will Delay Intervalが0より大きい値に設定されている場合、クライアントがWill Delay Intervalが経過する前に接続を回復した場合、Will Messageはパブリッシュされません。

### Will Messageとセッション

Will Messageはサーバーセッションの状態の一部であり、セッションが終了すると、Will Messageは独自に存在し続けることはできません。

Will Messageの遅延パブリッシュ中に、セッションが期限切れになるか、またはクライアントが新しい接続でClean Startを1に設定するためにサーバーが前のセッションを破棄する必要がある場合があります。

Will Messageを失うことを避けるために、サーバーはこの場合、Will Delay Intervalがまだ経過していなくても、Will Messageをパブリッシュする必要があります。

したがって、サーバーが最終的にWill Messageをパブリッシュするのは、Will Delay Intervalの期限切れとセッションの終了のいずれかが先に発生した場合になります。

### MQTT 3.1.1におけるWill Message

MQTT 3.1.1では、サーバーがDISCONNECTパケットを受信せずにネットワーク接続が閉じられた場合、サーバーはWill Messageをパブリッシュする必要があります。

MQTT 3.1.1にはWill Delay Intervalやセッション有効期限の概念がないため、ネットワーク接続が閉じられたときにはWill Messageが常に即時にパブリッシュされます。

## Will Messageがパブリッシュされなかった理由は？

Will Messageの遅延パブリッシュとキャンセルにより、サブスクライバーがWill Messageを受信するかどうかの問題はやや複雑になります。

可能なすべての状況を整理して、より理解しやすくしました：

![when publish will message](https://assets.emqx.com/images/6ebb67496715f5086050d77a2c7924af.jpg)

1. 接続が予期せず閉じられ、Will Delay Intervalが0の場合、ネットワーク接続が閉じられたときにWill Messageは即座にパブリッシュされます。
2. 接続が予期せず閉じられ、Will Delay Intervalが0より大きい場合、Will Messageのパブリッシュは遅延されます。最大遅延時間は、Will Delay Intervalかセッション有効期限のいずれかが先に満了するかによります：
   1. クライアントがWill Delay Intervalまたはセッション有効期限の満了前に接続を回復できなかった場合、Will Messageはパブリッシュされます。
   2. Will Delay Intervalまたはセッション有効期限の満了前に：
      1. クライアントがClean Startを0に設定して接続を回復する場合、Will Messageはパブリッシュされません。
      2. クライアントがClean Startを1に設定して接続を回復する場合、Will Messageは即時にパブリッシュされます。これは、Clean Startを1に設定すれば再接続の瞬間**既存のセッションが終了となります**。

既存のネットワーク接続が閉じられていないが、クライアントが同じクライアントIDで新しい接続を開始した場合、サーバーは既存のネットワーク接続に0x8E（セッション引き継ぎ）の理由コードを持つDISCONNECTパケットを送信し、その後接続を閉じます。これは貧弱なネットワーク状態でよく発生する可能性があり、予期せぬ接続の閉鎖と見なされます。

ここで、この質問を考えてみましょう。既存のネットワーク接続のセッション有効期限が0であり、Will Delay Intervalが0より大きい場合、クライアントがClean Startを0に設定して新しいネットワーク接続を開始したときに、サーバーはWill Messageを送信しますか？

答えは、既存のネットワーク接続が切断されたときにWill Messageが即座にパブリッシュされることです。

サーバーが既存のネットワーク接続を閉じると、セッション有効期限が0であるため、セッションは即座に終了します。Clean Startが0に設定されていても、サーバーは新しいネットワーク接続のために新しいセッションを作成します。したがって、上で述べた2.1のシナリオとして、セッションが終了するためにWill Messageがパブリッシュされます。

## Will Messageの使用に関するヒント

### Retain Messageの使用

サーバーがWill Messageをパブリッシュすると、そのメッセージはセッションから削除されます。このWill Messageに関心を持つクライアントがオンラインでない場合、それはこのWill Messageを見逃すことになります。

この状況を避けるために、Will MessageをRetain Messageとして設定できます。そうすると、Will Messageがパブリッシュされた後も、そのメッセージはRetain Messageの形でサーバーに保存され、クライアントはいつでもこのWill Messageを取得できます。

さらに進んで、特定のクライアントのステータス監視を実装することもできます。

クライアントmyclientが接続するたびに、トピックmyclient/status、ペイロードoffline、そしてWill Retainフラグを設定されたWill Messageを指定します。接続が成功するたびに、トピックmyclient/statusにペイロードonlineのRetain Messageをパブリッシュします。その後、いつでもトピックmyclient/statusにサブスクライブして、クライアントmyclientの最新のステータスを取得できます。

### セッション有効期限通知

セッション有効期限よりも大きなWill Delay Intervalを設定することで、サーバーはWill Messageとしてセッション有効期限の通知を送出することができます。これは、ネットワーク接続の切断よりもセッション有効期限が重要なアプリケーションにとって役立ちます。積極的なオフラインであっても、クライアントは0x04の理由コードでDISCONNECTパケットを送信して、サーバーにWill Messageを送信すること実現できます。

## デモ

### MQTTXを使用して

[MQTTX](https://mqttx.app/ja)をインストールして開き、まず[Free Public MQTT broker](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)にクライアント接続を開始します。この接続では、トピック`mqttx_c7f95fdf/status`、ペイロードofflineのWill Messageを指定し、Will Delay Intervalを5秒、セッション有効期限を300秒に設定しました。クライアントIDをトピックのプレフィックスとして使用することで、公共サーバーで他の人が使用するトピックとの重複を効果的に回避できます：

![MQTTX](https://assets.emqx.com/images/e9873d7e2e2bbeb2faea074e220cf724.png)

新しいクライアント接続を作成し、Public MQTTサーバーに接続してから、トピックmqttx_c7f95fdf/statusをサブスクライブしてWill Messageを受信します：

![new mqtt subscription](https://assets.emqx.com/images/56361c0032b7b6ca8f0b6d4ef4b7c15f.png)

次に、最初のクライアントがトピックエイリアスを設定しているが、トピックが空のメッセージを送信させます。トピックとトピックエイリアスの間にマッピングがまだ確立されていないため、この操作によりサーバーはクライアントの行動がプロトコルのルールに適合していないと判断し、接続を閉じ、Will Messageを送信することになります：

![send mqtt message](https://assets.emqx.com/images/4d04a2baa33ffbd3f3add8979a020c7a.png)

Will Delay Intervalが設定されているため、メッセージを送信してから5秒後にサブスクライバーにWill Messageが到着するのを見ることができます：

![receive mqtt will message](https://assets.emqx.com/images/2c3dfc1f785dad82dffca014cdcba7ad.png)

### MQTTX CLIを使用して

ターミナルで、コマンドラインツール[MQTTX CLI](https://mqttx.app/cli)を使用して、Will Messageの挙動を確認することができます。次に、クライアント接続がWill Messageを公開する前に回復する場合に何が起こるかを見てみましょう。

まず、最初のターミナルウィンドウで接続を開始し、willトピックをサブスクライブします：

```
$ client_id="mqttx_"`date | sha256sum | base64 | head -c 8`
$ echo ${client_id}
mqttx_YzFjZmVj
$ mqttx sub -h broker.emqx.io --topic ${client_id}"/status"
…  Connecting...
✔  Connected
…  Subscribing to mqttx_YzFjZmVj/status...
✔  Subscribed to mqttx_YzFjZmVj/status
```

次に、2番目のターミナルウィンドウでWill Messageを指定してクライアント接続を確立し、Will Delay Intervalを10秒、セッション有効期限を300秒に設定します。

接続が成功したら、Ctrl+Cを押して終了し、クライアントがDISCONNECTパケットを送信せずに直接ネットワーク接続を切断することになります：

```
$ client_id="mqttx_YzFjZmVj"
$ mqttx conn -h broker.emqx.io --client-id ${client_id} --will-topic ${client_id}"/status" --will-message "offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
```

10秒以内に以下のコマンドを実行して再接続します：

```
$ mqttx conn -h broker.emqx.io --client-id ${client_id} --no-clean --session-expiry-interval 300
```

最初のターミナルウィンドウのサブスクライバーはWill Messageを受信しません。

これらは単純な例ですが、MQTTXとFree MQTT公開サーバーを使用して、Will Messageのさらなる特性を検証することができます。たとえば、Will Messageがいつ公開され、いつ公開されないかなどです。

また、[emqx/MQTT-Features-Example](https://github.com/emqx/MQTT-Feature-Examples)でWill MessagesのPythonサンプルコードを提供しており、ぜひご参考になってください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
