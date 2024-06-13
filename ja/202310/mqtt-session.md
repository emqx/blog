## MQTT Persistent Session 

不安定なネットワークと限られたハードウェア リソースは、IoT アプリケーションが直面する必要がある 2 つの大きな問題です。MQTT クライアントとブローカー間の接続は、ネットワークの変動やリソースの制約により、いつでも異常切断される可能性があります。ネットワーク切断による通信への影響に対処するために、MQTT プロトコルは Persistent Session を提供します。

[MQTT クライアントは、](https://www.emqx.com/ja/blog/mqtt-client-tools)サーバーへの接続を開始するときに Persistent Session を使用するかどうかを設定できます。 Persistent Session には、複数のネットワーク接続上でセッションを継続できるようにするための重要なデータが保持されます。 Persistent Session には、次の 3 つの主な機能があります。

- ネットワークの停止により繰り返しサブスクライブする必要があるという追加のオーバーヘッドを回避します。
- オフライン期間中にメッセージを見逃さないようにします。
- QoS 1 および QoS 2 メッセージがネットワーク停止の影響を受けないようにします。

##  Persistent Session のために保存する必要があるデータは何ですか?

上記のことから、セッションを回復するには Persistent Session に重要なデータを保存する必要があることがわかります。このデータの一部はクライアント側に保存され、一部はサーバー側に保存されます。

クライアントに保存されるセッション データ:

- QoS 1 および QoS 2 メッセージはサーバーに送信されましたが、まだ確認が完了していません。
- サーバーから受信したが、まだ確認が完了していない QoS 2 メッセージ。

サーバーに保存されるセッション データ:

- 残りのセッション ステータスが空であっても、セッションが存在するかどうか。
- クライアントに送信されたものの、確認がまだ完了していない QoS 1 および QoS 2 メッセージ。
- QoS 0 メッセージ (オプション)、クライアントへの送信を待機している QoS 1 および QoS 2 メッセージ。
- クライアントから受信したがまだ確認応答が完了していない QoS 2 メッセージ、Will Messages、および Will Delay Intervals。

## MQTT Clean Session の使用

Clean Session は、セッション状態のライフサイクルを制御するために使用されるフラグ ビットです。値 1 は、接続時に新しいセッションが作成され、クライアントが切断されるとセッションが自動的に破棄されることを意味します。0 の場合は、接続時に前のセッションの再利用を試みることを意味します。対応するセッションがない場合は、新しいセッションが作成され、クライアントが切断された後も常に存在します。

> ***注:** Persistent Session は、クライアントが固定クライアント ID を使用して再度接続した場合にのみ再開できます。クライアント ID が動的である場合、接続が成功した後に新しい Persistent Session が作成されます。*

以下は、[オープンソースの MQTT ブローカー EMQX ](https://github.com/emqx/emqx)のダッシュボードです。図の接続は切断されていることがわかりますが、 Persistent Session であるため、ダッシュボードには引き続き表示できます。

![MQTT Connections](https://assets.emqx.com/images/f66ac8daa11ef2ff5df6b466cd81b510.png)

EMQX は、ダッシュボードでのセッション関連のパラメーターの設定もサポートしています。

![MQTT Session](https://assets.emqx.com/images/b1a0e23bf46e46762ce8dd9fc4a38bef.png)

MQTT 3.1.1 では、 Persistent Session がいつ期限切れになるかは指定されていません。プロトコル レベルだけで理解される場合、この Persistent Session は永続的である必要があります。ただし、これはサーバー側で多くのリソースを消費するため、実際のシナリオでは現実的ではありません。したがって、サーバーは通常、プロトコルに正確に従いませんが、セッションの有効期限を制限するグローバル構成をユーザーに提供します。

たとえば、 EMQ が提供する[Free Public MQTT Broker は、](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)セッションの有効期限を 5 分、最大メッセージ数を 1000 に設定し、QoS 0 メッセージを保存しません。

次に、オープンソースのクロスプラットフォーム[MQTT 5.0 デスクトップ クライアント ツール MQTTX](https://mqttx.app/ja)を使用したクリーン セッションの使用方法を示します。

MQTTX を開いた後、以下に示すように`New Connection`ボタンをクリックして[MQTT 接続](https://www.emqx.com/ja/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)を作成します。

![Click New Connection](https://assets.emqx.com/images/905a669d634a4438a7bdcc6cad90b975.png)

Clean Session をオフ (つまり false) にして名前付きの接続を作成し`MQTT_V3`、MQTT バージョン 3.1.1 を選択して、`Connect`右上隅の ボタンをクリックします。

> *接続されるデフォルトのサーバーは、 EMQ が提供する*[*無料のパブリック MQTT ブローカー*](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)*です。*

![Create a connection](https://assets.emqx.com/images/fb8b1986a743b061cab5028c353016c9.png)

`clean_session_false`接続が成功し、QoS が 1 に設定されたら、トピックをサブスクライブします。

![Subscribe to clean_session_false topic](https://assets.emqx.com/images/5fa0b38984c1f199bbd6f875a6a65bd4.png)

購読が成功したら、`Disconnect`右上隅にある ボタンをクリックします。次に、再び MQTT バージョンを 3.1.1 に設定して という名前の接続を作成し`MQTT_V3_Publish`、`clean_session_false`接続が成功した後に 2 つの QoS 1 メッセージをトピックにパブリッシュします。

![Publish MQTT Messages](https://assets.emqx.com/images/1590dd170d31a0576110dd2790a8eabd.png)

次に、MQTT_V3 接続を選択し、`Connect`ボタンをクリックしてサーバーに接続します。オフライン期間中に発行された 2 つのメッセージを正常に受信できます。

![Receive MQTT Messages](https://assets.emqx.com/images/3797fb43e05558eca50e41596e307fde.png)

## MQTT 5.0 でのセッションの改善

MQTT 5.0 では、クリーン セッションはクリーン スタートとセッション有効期限間隔に分割されます。Clean Start は、接続時に新しいセッションを作成するか、既存のセッションの再利用を試行するかを指定します。セッション有効期限間隔は、ネットワーク接続が切断された後にセッションが期限切れになるまでの時間を指定するために使用されます。

Clean Start of は`true`、既存のセッションをすべて破棄し、完全に新しいセッションを作成することを意味します。`false`クライアントとの通信を再開するには、クライアント ID に関連付けられたセッションを使用する必要があることを示します (セッションが存在しない場合を除く)。

Session Expiry Interval は、MQTT 3.1.1 に永続的に存在する Persistent Session によって引き起こされるサーバー リソースの浪費問題を解決します。0 または none に設定すると、切断時にセッションが期限切れになることを示します。0 より大きい値は、ネットワーク接続が閉じられた後にセッションが残る秒数を示します。に設定すると、`0xFFFFFFFF`セッションが期限切れにならないことを意味します。

詳細については、ブログ「[Clean Start and Session Expiry Interval」](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)を参照してください。

## MQTTセッションに関するQ&A

### セッションが終了しても、保持されたメッセージはまだ存在しますか?

[MQTT 保持メッセージ](https://www.emqx.com/en/blog/mqtt5-features-retain-message)はセッション状態の一部ではないため、セッションの終了時に削除されません。

### クライアントは、現在のセッションが再開されたセッションであることをどのようにして知るのでしょうか?

MQTT プロトコルは、v3.1.1 以降、CONNACK メッセージの Session Present フィールドを設計しました。サーバーがこのフィールドの値 1 を返した場合、現在の接続はサーバーによって保存されたセッションを再利用することを意味します。クライアントは、このフィールド値を使用して、接続が成功した後に再サブスクライブするかどうかを決定できます。

###  Persistent Session を使用するベスト プラクティス

- 動的なクライアント ID は使用できません。クライアント ID がクライアント接続ごとに固定されていることを確認する必要があります。
- サーバーのパフォーマンス、ネットワークの状態、クライアントの種類に基づいて、セッションの有効期限を適切に評価します。設定が長すぎると、サーバー側のリソースがより多く消費されます。また、設定が短すぎると、正常に再接続する前にセッションが期限切れになります。
- クライアントがセッションが必要ないと判断した場合は、Clean Session を true として使用して再接続し、再接続が成功した後に切断できます。MQTT 5.0 の場合、切断時にセッション有効期限間隔を直接 0 に設定して、接続が切断されたときにセッションが期限切れになることを示すことができます。

## まとめ

この時点で、MQTT Persistent Session の紹介は完了し、デスクトップ クライアントを介した Clean Session の使用方法を示しました。この記事を参照して、MQTT  Persistent Session を使用してオフライン メッセージを受信し、サブスクリプションのオーバーヘッドを削減できます。

次に、 EMQ が提供する[MQTT プロトコルのわかりやすいガイド](https://www.emqx.com/en/mqtt-guide)シリーズの記事を参照して、MQTT トピック、ワイルドカード、保持メッセージ、ウィル メッセージ、およびその他の機能について学ぶことができます。MQTT のより高度なアプリケーションを探索し、MQTT アプリケーションとサービスの開発を始めましょう。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
