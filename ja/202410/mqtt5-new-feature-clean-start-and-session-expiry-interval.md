この記事では、[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)のセッションメカニズムと、セッションライフサイクルを管理するために使用される2つの接続パラメータである**クリーンスタート**と**セッション有効期限間隔**について紹介します。

> MQTT 5.0を初めてご利用ですか？ぜひご覧ください
>
> [MQTT 5.0：7つの新機能と移行チェックリスト](https://www.emqx.com/ja/blog/introduction-to-mqtt-5)

## なぜMQTTはセッションメカニズムをサポートしているのか？

IoTシナリオでは、ネットワークや電源の問題によりデバイスが頻繁に切断されることがあります。クライアントとサーバーが常に新しいコンテキストで接続を確立する場合、以下の問題が発生します：

1. クライアントは再接続後にすべての関連トピックに再サブスクライブする必要があり、サーバーに追加のオーバーヘッドをもたらします。
2. クライアントはオフライン期間中のメッセージを見逃します。
3. QoS 1およびQoS 2のサービス品質が保証されません。

これらの問題を回避するために、MQTTプロトコルはセッションメカニズムを設計しました。これがMQTT通信の基盤を形成しています。

## MQTTセッションとは？

[MQTTセッション](https://www.emqx.com/ja/blog/mqtt-session)は、本質的にはサーバーとクライアントによって追加のストレージが必要なコンテキストデータのセットです。一部のセッションはネットワーク接続が確立されている間のみ持続し、他のセッションは複数の連続するネットワーク接続にわたって存在することができます。クライアントとサーバーがこのセッションデータの助けを借りて通信を再開すると、ネットワークの中断はまるで発生しなかったかのようになります。

サーバーを例に取ると、クライアントのサブスクリプションリストを保存する必要があります。クライアントが現在接続されているかどうかに関係なく、セッションが有効期限切れでない限り、サーバーはクライアントがサブスクライブしているメッセージを把握し、それらのメッセージをキャッシュすることができます。さらに、クライアントは再接続時にサブスクリプションを再初期化する必要がなくなり、サーバーのパフォーマンスオーバーヘッドも削減されます。

MQTTは、サーバーレベルとクライアントレベルで保存する必要があるセッション状態を定義しています。

**サーバーの場合、以下を保存する必要があります：**

1. セッションの存在。
2. クライアントのサブスクリプション。
3. クライアントに送信されたが完全に確認されていないQoS 1およびQoS 2メッセージ。
4. クライアントに送信が保留されているQoS 1およびQoS 2メッセージ、およびオプションでQoS 0メッセージ。
5. クライアントから受信したが完全に確認されていないQoS 2メッセージ。
6. [ウィルメッセージ](https://www.emqx.com/ja/blog/use-of-mqtt-will-message)とウィルディレイ間隔。
7. セッションが現在接続されていない場合、セッションが終了しセッション状態が破棄される時刻。

**クライアントの場合、以下を保存する必要があります：**

1. サーバーに送信されたが完全に確認されていないQoS 1およびQoS 2メッセージ。
2. サーバーから受信したが完全に確認されていないQoS 2メッセージ。

これらのセッションデータをサーバーとクライアントに恒久的に保存させることは、多くの追加ストレージコストをもたらすだけでなく、多くのシナリオでは不要です。例えば、ネットワーク接続の一時的な中断によるメッセージの損失を避けたい場合、接続が切断された後にセッションデータを数分間保持するように設定するのが一般的です。

さらに、クライアントとサーバーのセッション状態が一致しない場合、例えばクライアントデバイスが再起動によりセッションデータを失った場合、接続時にサーバーに元のセッションを破棄し新しいセッションを作成するように通知する必要があります。

これらの2点に対して、[MQTT 5.0](https://www.emqx.com/ja/blog/introduction-to-mqtt-5)では、**クリーンスタート**と**セッション有効期限間隔**という2つの接続フィールドを提供し、セッションのライフサイクルを制御します。

## クリーンスタートの紹介

**クリーンスタート**は、CONNECTパケットの[バリアブルヘッダー](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets)に位置しています。クライアントは、接続時にこのフィールドを通じて既存のセッションを再利用するかどうかを指定します。値は0と1の2つだけです。

**クリーンスタートが0に設定されている場合**、サーバーにクライアントが接続されているときに指定されたクライアントIDに関連付けられたセッションが存在する場合、サーバーはこのセッションを使用して通信を再開しなければなりません。

クライアントIDに関連付けられたセッションが存在しない場合、サーバーは完全に新しいセッションを作成しなければなりません。この場合、クライアントは古いセッションを使用しており、サーバーは全く新しいセッションを使用しています。両者のセッション状態が不一致となります。したがって、サーバーはCONNACKパケットでSession Presentフラグを0に設定し、クライアントに期待していたセッションが存在しないことを知らせる必要があります。クライアントがこのネットワーク接続を続行したい場合、保存されているセッション状態を破棄しなければなりません。

**クリーンスタートが1に設定されている場合**、クライアントとサーバーは既存のセッションをすべて破棄し、新しいセッションを開始しなければなりません。対応して、サーバーはCONNACKパケットでSession Presentフラグを0に設定します。

![MQTT Clean Start](https://assets.emqx.com/images/5aa78a5c038aacafdbd314930e060c67.jpg)

## セッション有効期限間隔の紹介

**セッション有効期限間隔**もCONNECTパケットのバリアブルヘッダーに位置していますが、これはオプションの[プロパティ](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets)です。これは、ネットワークが切断された後、サーバー上でセッションが保持される最大時間を指定するために使用されます。期限が切れると、ネットワーク接続が回復していなくても、サーバーは対応するセッション状態を破棄します。典型的な値は以下の3つです：

1. **このプロパティが指定されていないか0に設定されている場合**、ネットワーク接続が失われるとセッションは直ちに終了します。
2. **0より大きい値に設定**されている場合、セッションが期限切れになる前にネットワーク接続が切断された後にセッションが持続できる秒数を示します。
3. **0xFFFFFFFFに設定**されている場合、これは**セッション有効期限間隔**プロパティに設定できる最大値であり、セッションが決して期限切れにならないことを意味します。

各[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)は、独立して自身の**セッション有効期限間隔**を設定できます。実際のニーズに応じて、期限時間を柔軟に設定できます。例えば、永続的なセッションが不要なクライアントもあれば、ネットワークの変動の影響を避けるためにセッションを数分間保持するだけで十分なクライアント、さらにセッションを長期間保持する必要があるクライアントもあります。

MQTTは、クライアントが切断時に**セッション有効期限間隔**を更新することも許可しています。これは主にDISCONNECTパケットの同名プロパティに依存します。一般的なアプリケーションシナリオとして、クライアントがオンライン時に**セッション有効期限間隔**を0より大きい値に設定し、ネットワークの中断が通常のビジネスに影響を与えないようにします。そして、クライアントがすべてのビジネスを完了し積極的にログオフすると、**セッション有効期限間隔**を0に更新し、サーバーがセッションをタイムリーに解放できるようにします。

![MQTT Session Expiry Interval](https://assets.emqx.com/images/da0627af8aaeb1bd7ea152f0b0eeee39.jpg)

## セッションとクライアントID

サーバーはクライアントIDを使用して各セッションを一意に識別します。クライアントが接続時に以前のセッションを再利用したい場合、以前と同じクライアントIDを使用しなければなりません。したがって、サーバーでクライアントIDを自動割り当てる機能を使用する場合、クライアントはCONNACKパケットで返される割り当てられたクライアント識別子を次回使用のために保存する必要があります。

なお、MQTT 5.0以前のプロトコルバージョンでは、サーバーが自動的に割り当てたクライアントIDを返すことをサポートしていないため、サーバーによってクライアントIDが自動的に割り当てられるか、永続的なセッションを使用するかの選択をする必要があります。

## MQTT 3.1.1におけるクリーンセッション

MQTT 3.1.1のセッションメカニズムは、5.0に比べてはるかに柔軟性が低いです。3.1.1には**クリーンセッション**フィールドが1つしかなく、その値も0と1の2つだけです。

MQTT 3.1.1で**クリーンセッション**を0に設定することは、MQTT 5.0で**クリーンスタート**を0に設定し、**セッション有効期限間隔**を0xFFFFFFFF（セッションが決して期限切れにならない）に設定することと同等です。

MQTT 3.1.1で**クリーンセッション**を1に設定することは、MQTT 5.0で**クリーンスタート**を1に設定し、**セッション有効期限間隔**を0（セッションのライフサイクルがネットワーク接続と一致する）に設定することと同等です。

![MQTT Clean Session](https://assets.emqx.com/images/4c5f9c5d6c0693d468441f1d2f81d6b0.jpg)

ご覧の通り、MQTT 3.1.1ではセッションのライフサイクルに対して「期限切れなし」または「ネットワーク接続と一致」の2つのオプションしかありません。

しかし、すべてのクライアントのセッションを恒久的に保存することは、間違いなくサーバーのリソースを無駄にします。これはMQTT 3.1.1のプロトコル設計における見落としのようです。したがって、EMQXは`mqtt.session_expiry_interval`設定項目を提供し、MQTT 3.1.1クライアントのグローバルなセッション有効期限間隔を設定できるようにし、サーバーのリソース消費を許容範囲内に制御できるようにしています。

さらに、新しいセッションを作成するかどうかもセッションのライフサイクルに強制的に結びつけられます。MQTT 3.1.1では、新しい永続的なセッションをサーバーに作成させるために、**クリーンセッション**を1と0にそれぞれ指定して接続する必要があります。

したがって、MQTT 3.1.1に比べて、MQTT 5.0はセッションにおいて大幅な改善を遂げています。

## MQTT永続セッションの実践的な提案

MQTTでは、ライフサイクルがネットワーク接続よりも長いセッションを通常、永続セッションと呼びます。しかし、永続セッションを使用する際にはいくつか注意すべき点があります。

例えば、永続セッションがサーバーリソースに与える影響を正しく評価する必要があります。セッションの有効期限が長くなるほど、サーバーが必要とするストレージリソースが増える可能性があります。サーバーは通常、クライアントのメッセージを無制限にキャッシュしないため、[EMQX](https://github.com/emqx/emqx)を例に取ると、各クライアントセッションにキャッシュできるメッセージの最大数はデフォルトで1000ですが、クライアント数を考慮すると、これは客観的なストレージコストとなる可能性があります。サーバーのリソースが限られている場合、セッションの有効期限時間とセッションキャッシュの最大数の設定にもっと注意を払う必要があります。

さらに、クライアントが長時間オフラインになった後に到着するメッセージを処理し続ける必要があるかどうかも評価する必要があります。もちろん、可能な限り多くのメッセージを保存するために大きなキャッシュを設定するか、最近到着したメッセージのみを処理できるように小さなキャッシュを設定するかは、実際のシナリオに依存します。

## デモ

1. [MQTTX](https://mqttx.app/ja)をインストールして開きます。MQTTのセッションメカニズムをよりよく示すために、まずMQTTXの設定ページに移動し、`Auto resubscribe`機能をオフにします：

   ![MQTTX](https://assets.emqx.com/images/3c9de957f47a29255265e3c194f5c050.png)

2. `sub`という名前のクライアント接続を作成し、MQTTバージョンを5.0に設定、**クリーンスタート**を有効にし、**セッション有効期限間隔**を300秒に設定します。その後、[無料のパブリックMQTTサーバー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)に接続し、トピック`mqttx_290c747e/test`にサブスクライブします：

   ![MQTTX New Connection](https://assets.emqx.com/images/2e21f2a679152c5a59d21ed8b5c26777.png)

3. `pub`という名前のクライアント接続を作成し、トピック`mqttx_290c747e/test`にメッセージを発行します。メッセージ内容は任意に設定できます。クライアント`sub`がこれらのメッセージを受信するのを確認します。その後、クライアント`sub`を切断し、クライアント`pub`を通じてメッセージの発行を続けます：

   ![MQTTX publish messages](https://assets.emqx.com/images/46210f16fd8327e7ba968bb0cb2b18c0.png)

4. 次に、クライアント`sub`の**クリーンスタート**オプションを無効にし、**セッション有効期限間隔**を300秒のままにして再接続します。クライアント`sub`がオフライン期間中に発行されたメッセージを受信するのを確認します：

   ![disable the Clean Star](https://assets.emqx.com/images/2b2aa5ec17a6ea935ebbc3d36fc0d7c2.png)

   ![connect again](https://assets.emqx.com/images/40129a8bb1eb363b7a6d8076f2673d4e.png)

上記は、MQTTセッションがオフラインのクライアントのためにメッセージをキャッシュする能力です。ターミナルインターフェースでは、コマンドラインツールの[MQQTX CLI](https://mqttx.app/cli)を使用して上記の操作を完了することもできます。まず、以下のコマンドを使用してトピックにサブスクライブします。サブスクリプションが成功した後、ターミナルで`Ctrl+C`を入力してクライアントを切断します：

```shell
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting...
✔  Connected
…  Subscribing to mqttx_290c747e/test...
✔  Subscribed to mqttx_290c747e/test
^C
```

次に、以下のコマンドを使用してトピック`mqttx_290c747e/test`にメッセージを発行します：

```shell
mqttx pub -h 'broker.emqx.io' --topic mqttx_290c747e/test --message "hello world"
```

発行が成功した後、サブスクライバーへの接続を復元します。以下のコマンドでは、以前と同じクライアントIDを維持し、`--no-clean`オプションを設定しています。これにより、サブスクライバーが接続前に発行されたメッセージを即座に受信するのが確認できます：

```shell
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--no-clean --session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting...
✔  Connected
…  Subscribing to mqttx_290c747e/test...
payload: hello world 

✔  Subscribed to mqttx_290c747e/test
```

[MQTTX](https://mqttx.app/ja)や[MQTTX CLI](https://mqttx.app/ja/cli)などのMQTTクライアントツールは、主に誰もが迅速にMQTTを始められるようにすることを目的としているため、サーバーから返されるSession Presentの表示や、切断時に**セッション有効期限間隔**を更新するなどの不要な機能は提供していません。したがって、この部分に興味がある場合は、対応するPythonのサンプルコードを[こちら](https://github.com/emqx/MQTT-Feature-Examples)で入手し、詳細を学ぶことができます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
