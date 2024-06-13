## Subscription Identifier が必要なのはなぜですか?

[MQTT クライアント](https://www.emqx.com/ja/mqtt-client-sdk)のほとんどの実装では、コールバック メカニズムを使用して受信メッセージを処理します。

コールバック関数内では、メッセージのトピック名にのみアクセスできます。非ワイルドカード サブスクリプションの場合、サブスクリプション中に使用されるトピック フィルターは、メッセージ内のトピック名と同じになります。したがって、サブスクライブされたトピックとコールバック関数の間のマッピングを直接確立できます。その後、メッセージが到着すると、メッセージ内のトピック名に基づいて対応するコールバックを検索し、実行できます。

ただし、ワイルドカード サブスクリプションの場合、メッセージ内のトピック名は、サブスクリプション中に使用された元のトピック フィルターとは異なります。この場合、メッセージ内のトピック名と元のサブスクリプションを 1 つずつ照合して、どのコールバック関数を実行するかを決定する必要があります。これは明らかにクライアントの処理効率に影響を与えます。

![MQTT Subscription](https://assets.emqx.com/images/5b3b24a4406e4d342355138f90dd438b.png)

さらに、[MQTT では](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)クライアントが複数のサブスクリプションを確立できるため、ワイルドカード サブスクリプションを使用すると、1 つのメッセージが複数のクライアント サブスクリプションと一致する可能性があります。

このような場合、MQTT を使用すると、サーバーは重複するサブスクリプションごとに個別のメッセージを送信したり、重複するすべてのサブスクリプションに対して 1 つのメッセージだけを送信したりできます。前者のオプションは、クライアントが複数の重複メッセージを受信することを意味します。

前者のオプションであるか後者のオプションであるかに関係なく、クライアントはメッセージの発信元のサブスクリプションを判断できません。たとえば、クライアントがメッセージが 2 つのサブスクリプションと一致することを発見した場合でも、サーバーがメッセージをクライアント自体に転送するときに両方のサブスクリプションが正常に作成されたことを保証できません。したがって、クライアントはメッセージに対して正しいコールバックをトリガーできません。

![MQTT Subscription](https://assets.emqx.com/images/3a86d62e52c9bfcef85ba590d14c4a19.png)

## Subscription Identifier はどのように機能しますか?

この問題に対処するために、MQTT 5.0 では Subscription Identifier が導入されました。その使用法は非常に簡単です。クライアントはサブスクライブ時に Subscription Identifier を指定でき、サーバーはサブスクリプションと Subscription Identifier の間のマッピング関係を保存する必要があります。PUBLISH パケットがサブスクリプションと一致し、クライアントに転送する必要がある場合、サーバーはサブスクリプションに関連付けられた Subscription Identifier を PUBLISH パケットとともにクライアントに返します。

![Subscription Identifier](https://assets.emqx.com/images/f9f1cf19de90a4e03647dbe52d69f7e7.png)

サーバーが重複するサブスクリプションに対して個別のメッセージを送信することを選択した場合、各 PUBLISH パケットにはサブスクリプションと一致するサブスクリプション ID が含まれている必要があります。サーバーが重複するサブスクリプションに対して 1 つのメッセージのみを送信することを選択した場合、PUBLISH パケットには複数のサブスクリプション ID が含まれます。

クライアントは、 Subscription Identifier とコールバック関数の間のマッピングを確立するだけで済みます。メッセージ内の Subscription Identifier を使用することにより、クライアントはメッセージの発信元のサブスクリプションと、どのコールバック関数を実行する必要があるかを決定できます。

![MQTT Subscription](https://assets.emqx.com/images/7ba966d802c9ee39683870366f5fd7c7.png)

クライアントでは、 Subscription Identifier はセッション状態の一部ではなく、コンテンツとの関連付けは完全にクライアントによって決定されます。したがって、コールバック関数のほかに、 Subscription Identifier とサブスクライブされたトピックの間、または Subscription Identifier とクライアント ID の間のマッピングを確立することもできます。後者は、ゲートウェイがサーバーからメッセージを受信し、それらを適切なクライアントに転送する必要があるゲートウェイ シナリオで特に役立ちます。サブスクリプション ID を使用すると、ゲートウェイはトピックの再照合やルーティングを行わずに、どのクライアントがメッセージを受信すべきかを迅速に判断できます。

SUBSCRIBE パケットには、 Subscription Identifier を 1 つだけ含めることができます。SUBSCRIBE パケットに複数のサブスクリプションが含まれる場合、同じサブスクリプション ID がそれらすべてのサブスクリプションに関連付けられます。したがって、複数のサブスクリプションを同じコールバック関数に関連付けることが意図的であることを確認してください。

## デモ

1. Web ブラウザで[MQTTX Web](https://mqttx.app/ja)にアクセスします。

2. [MQTT over WebSocket](https://www.emqx.com/ja/blog/connect-to-mqtt-broker-with-websocket)接続を作成し、[無料のパブリック MQTT サーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続します。

   ![MQTT over WebSocket](https://assets.emqx.com/images/e1c10cbd018d0742f21f3b371ec89c6a.png)

3. 接続が成功した後、トピックをサブスクライブ`mqttx_4299c767/home/+`し、サブスクリプション ID を 1 に指定します。次に、トピックをサブスクライブし`mqttx_4299c767/home/PM2_5`、サブスクリプション ID を 2 に指定します。パブリック サーバーは多くの人が同時に使用できるため、トピックの競合を避けるために、トピックのプレフィックスとしてクライアント ID を使用します。

   ![New Subscription 1](https://assets.emqx.com/images/f3c0aed851e02f20aae69cf100b167d6.png)

   ![New Subscription 2](https://assets.emqx.com/images/212728b6ae71b5baf73a860f75d4545a.png)

4. サブスクリプションが成功すると、トピックにメッセージを公開します`mqttx_4299c767/home/PM2_5`。現在のクライアントが 2 つのメッセージを受信し、メッセージ内のサブスクリプション ID がそれぞれ 1 と 2 であることがわかります。これは、EMQX の実装が重複するサブスクリプションに対して個別のメッセージを送信するためです。

   ![Receive MQTT Messages](https://assets.emqx.com/images/fd38994dea83422bb31a85b5c14711b1.png)

5. そして、トピックにメッセージをパブリッシュすると`mqttx_4299c767/home/temperature`、受信したメッセージの Subscription Identifier が 1 であることがわかります。

   ![image.png](https://assets.emqx.com/images/f0a2dba909a1efa8fab0b07ea961a959.png)



[MQTTX](https://mqttx.app/ja)を介してサブスクリプションの Subscription Identifier を設定する方法を説明してきました。 Subscription Identifier に基づいてさまざまなコールバックをトリガーする方法についてまだ興味がある場合は、[ここで](https://github.com/emqx/MQTT-Feature-Examples) Subscription Identifier の Python サンプル コードを入手できます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
