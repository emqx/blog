[「MQTT パブリッシュ/サブスクライブ パターンの概要」](https://www.emqx.com/ja/blog/mqtt-5-introduction-to-publish-subscribe-model)では、サーバーから対応するメッセージを受信するには、サーバーとのサブスクリプションを開始する必要があることを学びました。サブスクライブ時に指定したトピック フィルターによって、サーバーがどのトピックを転送するかが決まります。サブスクライブオプションを使用すると、サーバーの転送動作をさらにカスタマイズできます。

この記事では、[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)で利用可能なサブスクリプション オプションとその使用法を調べることに詳しく説明します。

## サブスクライブ オプション

MQTT のサブスクリプションは、トピック フィルターと対応するサブスクリプション オプションで構成されます。したがって、サブスクリプションごとに異なるサブスクリプション オプションを設定できます。

MQTT 5.0 では、QoS、No Local、Retain As Published、および Retain Handling の 4 つのサブスクリプション オプションが導入されています。一方、MQTT 3.1.1 は QoS サブスクリプション オプションのみを提供します。ただし、MQTT 5.0 のこれらの新しいサブスクリプション オプションのデフォルトの動作は、MQTT 3.1.1 と一貫性があります。これにより、MQTT 3.1.1 から MQTT 5.0 にアップグレードする場合に使いやすくなります。

ここで、これらのサブスクリプション オプションの機能を一緒に研究しましょう。

### QoS

QoS は最も一般的に使用されるサブスクリプション オプションであり、サーバーがサブスクライバにメッセージを送信するときに使用できる最大 QoS レベルを表します。

クライアントの実装が QoS 1 または 2 をサポートしていない場合、クライアントはサブスクリプション中に 2 未満の QoS レベルを指定できます。

さらに、サーバーがサポートする最大 QoS レベルが、サブスクリプション中にクライアントが要求した QoS レベルよりも低い場合、サーバーがクライアントの要件を満たすことができないことが明らかになります。このような場合、サーバーは加入者に許可された最大 QoS レベルを加入応答パケット (SUBACK) を通じて通知します。加入者は、付与された QoS レベルを受け入れて通信を継続するかどうかを評価できます。

![image.png](https://assets.emqx.com/images/fa5915cb9df598965881cc08585c1fe7.png)

簡単な計算式:

```
QoS in the forwarded message = min ( The original QoS of the message, The maximum QoS granted by the server )
```

ただし、サブスクリプション中に要求された最大 QoS レベルは、メッセージ送信時に発行側で使用される QoS レベルを制限しません。サブスクリプション中に要求された最大 QoS レベルが、メッセージの発行に使用される QoS レベルよりも低い場合、サーバーはこれらのメッセージを無視しません。メッセージ配信を最大化するために、転送前にこれらのメッセージの QoS レベルをダウングレードします。

![image.png](https://assets.emqx.com/images/b0f2a8b2c655ec59cf5c6338eb1217cc.png)

同様に、簡単な計算式があります。

```
QoS in the forwarded message = min ( The original QoS of the message, The maximum QoS granted by the server )
```

### No Local

「No Local」オプションには、0 と 1 の値しかありません。値 1 は、サーバーがメッセージを発行したクライアントにメッセージを転送してはならないことを示し、0 はその逆を意味します。

このオプションは通常、ブリッジング シナリオで使用されます。ブリッジングは基本的に 2 つの MQTT サーバーが[MQTT 接続](https://www.emqx.com/ja/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)を確立し、相互にいくつかのトピックをサブスクライブします。サーバーはクライアント メッセージを別のサーバーに転送し、別のサーバーはクライアントへのメッセージの転送を続けることができます。

![image.png](https://assets.emqx.com/images/84ceaaf5c2e513e6d775d6d3929e672b.png)

サーバー A とサーバー B という 2 つの MQTT サーバーを想定した最も単純な例を考えてみましょう。

`#`AとBはお互いからトピックをサブスクライブしています。ここで、サーバー A はクライアントからのメッセージをサーバー B に転送し、サーバー B が一致するサブスクリプションを探すと、サーバー A もそこに存在します。サーバー B がメッセージをサーバー A に転送すると、サーバー A はメッセージを受信した後に再びサーバー B に転送するため、無限の転送ストームに陥ります。

ただし、サーバー A とサーバー B の両方がトピックのサブスクライブ中に「No Local」オプションを 1 に設定すると`#`、この問題は理想的には回避できます。

### Retain As Published (保持メッセージフラグ)

「Retain As Published フラグ」 オプションにも、0 と 1 の 2 つの値があります。これを 1 に設定すると、サーバーはアプリケーション メッセージをサブスクライバに転送するときに保持フラグを変更せずに保持する必要があり、0 に設定すると、保持フラグをクリアする必要があることを意味します。

「No Local」 オプションと同様、「Retain As Published」 は主にブリッジ シナリオに適用されます。

サーバーは、保持されたメッセージを受信すると、それを保存するだけでなく、通常のメッセージと同様に既存のサブスクライバにも転送し、転送時にメッセージの保持フラグがクリアされることがわかっています。

これはブリッジのシナリオに課題をもたらします。前の設定を続けて、サーバー A が保持メッセージをサーバー B に転送すると、保持フラグがクリアされるため、サーバー B はそれを保持メッセージとして認識せず、保存しません。これにより、保持されたメッセージはブリッジを越えて使用できなくなります。

MQTT 5.0 では、この問題を解決するために、サブスクライブ時にブリッジ サーバーに「Retain」パブリッシュ オプションを 1 に設定させることができます。

![image.png](https://assets.emqx.com/images/ef5ed6d09cc7f52e5e4ea7ae123218e2.png)

### Retain Handling

「Retain Handling」 サブスクリプション オプションは、サブスクリプションが確立されたときに保持されたメッセージを送信するかどうかをサーバーに示します。

サブスクリプションが確立されると、サーバー内のサブスクリプションと一致する保持メッセージがデフォルトで配信されます。

ただし、クライアントが保持されたメッセージの受信を望まない場合もあります。たとえば、クライアントが接続中にセッションを再利用しても、前の接続でサブスクリプションが正常に作成されたかどうかを確認できない場合、クライアントは再度サブスクライブを試みる可能性があります。サブスクリプションがすでに存在する場合は、保持されているメッセージが消費されているか、クライアントのオフライン期間中に到着した一部のメッセージがサーバーによってキャッシュされている可能性があります。このような場合、クライアントは、サーバーが公開した保持メッセージの受信を望まない可能性があります。

さらに、クライアントは、最初のサブスクリプション中であっても、いつでも、保持されたメッセージの受信を希望しない場合があります。たとえば、スイッチの状態を保持メッセージとして送信しますが、特定のサブスクライバの場合、スイッチ イベントによって一部の操作がトリガーされるため、この場合は保持メッセージを送信しないと便利です。

Retain Handling を使用すると、次の 3 つの異なる動作から選択できます。

- Retain Handling を 0 に設定すると、サブスクリプションが確立されるたびに、保持されたメッセージが送信されます。
- Retain Handling を 1 に設定すると、保持されたメッセージは繰り返し送信されるのではなく、新しいサブスクリプションを確立するときにのみ送信されます。
- Retain Handling を 2 に設定すると、サブスクリプションが確立されたときに、保持されたメッセージは送信されません。

## デモ

### QoSサブスクリプションオプションのデモ

1. Web ブラウザで[MQTTX Web](http://mqtt-client.emqx.com/)にアクセスします。

2. WebSocket を使用して MQTT 接続を作成し、[無料のパブリック MQTT サーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続します。

   ![MQTTX](https://assets.emqx.com/images/1eff007c799cd5e9ed9d65c3a2b1d826.png)

3. `mqttx_4299c767/demo`接続が成功した後、QoS 0 でトピックをサブスクライブします。パブリック サーバーは多くの人が同時に使用する可能性があるため、他のサーバーとのトピックの競合を避けるために、トピックのプレフィックスとしてクライアント ID を使用できます。

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/7d6598089ff051feadae673734b5be68.png)

1. サブスクリプションが成功すると、QoS 1 メッセージをトピックに発行します`mqttx_4299c767/demo`。この時点で、QoS 1 メッセージを送信している間に QoS 0 メッセージを受信していることがわかります。これは、QoS の低下が発生したことを示しています。

   ![Publish a QoS 1 message](https://assets.emqx.com/images/4b1a7d69d8344ba6efc2c7fe22370b17.png)

### No Localサブスクリプションなしオプションのデモ

1. Web ブラウザで[MQTTX Web](http://mqtt-client.emqx.com/)にアクセスします。

2. WebSocket を使用して MQTT 接続を作成し、[無料のパブリック MQTT サーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続します。

3. 接続が成功したら、トピックをサブスクライブし`mqttx_4299c767/demo`、No Local オプションを true に設定します。

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/9255fa97ed59e71be6b7fac0e7d2fed4.png)

1. サブスクリプションが成功した後も、前述の QoS デモと同様に、サブスクライバーにメッセージを公開させます。ただし、今回はサブスクライバーがメッセージを受信できないことがわかります。

   ![Publish MQTT Message](https://assets.emqx.com/images/933d4e0147c2b1720124d8d3e36c55a1.png)

### Retain as Published サブスクリプション オプションのデモ

1. Web ブラウザで[MQTTX Web](http://mqtt-client.emqx.com/)にアクセスします。

2. WebSocket を使用して MQTT 接続を作成し、[無料のパブリック MQTT サーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続します。

3. 接続が成功したら、`mqttx_4299c767/rap0`「Retain as Published」を false に設定してトピックをサブスクライブします。次に、`mqttx_4299c767/rap1`「Retain As Published」を true に設定してトピックをサブスクライブします。

   ![Subscribe to the topic "mqttx_4299c767/rap0"](https://assets.emqx.com/images/3d9cb0512df37e95a1be40ec82384f93.png)

   ![Subscribe to the topic "mqttx_4299c767/rap1"](https://assets.emqx.com/images/627c5a3984d401f7e3cb01a160e593a0.png)

1. サブスクリプションが成功した後、保持されたメッセージをトピック`mqttx_4299c767/rap0`と`mqttx_4299c767/rap1,`それぞれに公開します。前者が受信したメッセージの Retain フラグがクリアされ、後者が受信したメッセージの Retain フラグが保持されていることがわかります。

   ![Receive messages](https://assets.emqx.com/images/8e23176543eb78b1f5ee77f6ba98add1.png)

### Retain Handlingサブスクリプション オプションのデモ

1. Web ブラウザで[MQTTX Web](http://mqtt-client.emqx.com/)にアクセスします。

2. WebSocket を使用して MQTT 接続を作成し、[無料のパブリック MQTT サーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続します。

3. 接続が成功したら、保持されたメッセージをトピックに公開します`mqttx_4299c767/rh`。次に、トピックをサブスクライブし`mqttx_4299c767/rh`、「Retain Handling」オプションを 0 に設定します。

   ![Publish a retained message to the topic "mqttx_4299c767/rh"](https://assets.emqx.com/images/9b0a0bfa76836e9e4bfc30d6576b25f6.png)

1. サブスクリプションが成功すると、サーバーから送信された保持メッセージを受信します。

   ![Receive the retained message](https://assets.emqx.com/images/1630db5d1e44c7eec81fcd37e7ca0969.png)

1. サブスクライブを解除し、保持処理を 2 に設定して再サブスクライブします。今回はサブスクリプションが成功すると、サーバーから送信された保持メッセージは受信されません。

   ![Retain Handling set to 2](https://assets.emqx.com/images/2032a4e178b18b0bcfd2866b9f377f75.png)

MQTTX では、Retain Handling を 1 に設定した場合の効果を実証することはできません。サブスクリプション オプションの Python サンプル コードは、[ここから](https://github.com/emqx/MQTT-Feature-Examples)入手できます。





<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
