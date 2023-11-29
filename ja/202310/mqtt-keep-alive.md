## Keep Alive が必要な理由

[MQTT プロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、接続指向の TCP プロトコル上でホストされ、接続された 2 つのパーティ間で安定した規則正しいバイト フローを提供します。ただし、場合によっては、TCP で半接続の問題が発生する可能性があります。半接続とは、一方の側では切断されているか確立されていない接続ですが、もう一方の接続はまだ維持されている状態です。この場合、半分接続された側は、明らかに相手側に到達しないデータを送信し続ける可能性があります。半接続によって引き起こされる通信のブラック ホールを回避するために、MQTT プロトコルは、クライアントと MQTT サーバーが半接続の問題があるかどうかを判断し、対応する接続を閉じることができる Keep Alive メカニズムを提供します。

## MQTT Keep Alive の仕組みと使い方

### コネクション作成の時

[MQTT Client](https://www.emqx.com/ja/blog/mqtt-client-tools)が[MQTT Broker](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)へに接続を作成するとき、接続要求プロトコル パケットの Keep Alive 変数ヘッダー フィールドをゼロ以外の値に設定することで、通信当事者間で Keep Alive メカニズムを有効にすることができます。Keep Alive は 0 ～ 65535 の整数で、クライアントによって送信される MQTT プロトコル パケット間の経過許容最大時間を秒単位で表します。

ブローカーはクライアントから接続リクエストを受信すると、変数ヘッダーの Keep Alive フィールドの値をチェックします。値がある場合、ブローカーは Keep Alive メカニズムを有効にします。

### MQTT 5.0 サーバーの Keep Alive 

[MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) 標準では、サーバー  Keep Alive の概念も導入され、実装やその他の要因に応じて、ブローカーがクライアント リクエストに含まれる Keep Alive 値を受け入れるか、オーバーライドするかを選択できるようになりました。ブローカーがこの値をオーバーライドすることを選択した場合、接続確認パケット (CONNACK) のサーバー  Keep Alive  フィールドに新しい値を設定する必要があり、クライアントは、この値を使用して、読み取り時に独自の以前の Keep Alive 値をオーバーライドする必要があります。それはCONNACKにあります。

### Keep Alive プロセス

**クライアントプロセス**

接続が確立された後、クライアントは、送信する 2 つの MQTT プロトコル パケット間の間隔が Keep Alive 値を超えていないことを確認する必要があります。クライアントがアイドル状態で、送信するパケットがない場合は、代わりに PINGREQ プロトコル パケットを送信できます。

クライアントが PINGREQ パケットを送信すると、ブローカーは PINRESP パケットを返す必要があります。クライアントが信頼できる時間内にサーバーから PINGRESP パケットを受信しない場合は、接続が半分であるか、ブローカーがオフラインであるか、ネットワーク障害が発生していることを意味するため、クライアントは接続を閉じる必要があります。

**ブローカーのプロセス**

接続が確立された後、ブローカーが Keep Alive 時間の 1.5 倍以内にクライアントからパケットを受信しない場合、クライアントへの接続に問題があるとみなされ、ブローカーはクライアントから切断されます。

ブローカーがクライアントから PINGREQ プロトコル パケットを受信した場合、確認のために PINGRESP プロトコル パケットで応答する必要があります。

**クライアント引き継ぎメカニズム**

ブローカー内にハーフ接続があり、対応するクライアントが再接続または新しい接続を開始すると、ブローカーはクライアント引き継ぎメカニズムを開始します。古いハーフ接続を閉じて、クライアントとの新しい接続を確立します。

このメカニズムにより、半接続の問題によりクライアントが再接続できなくなることがなくなります。

## Keep Alive & Will Message

Keep Alive は通常、Will Message と組み合わせて使用されます。これにより、予期しないオフライン イベントが発生した場合に、デバイスが他のクライアントに即座に通知できるようになります。

図に示すように、このクライアントが接続すると、Keep Alive が 5 秒に設定され、Will メッセージが設定されます。サーバーが 7.5 秒 ( Keep Alive の 1.5 倍) 以内にクライアントからパケットを受信しない場合、サーバーはペイロード「offline」を持つ will メッセージを「last_will」トピックに送信します。

![MQTT Will Message](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png)

MQTT Will Message の詳細については、ブログ「[MQTT Will Message の使用」](https://www.emqx.com/en/blog/use-of-mqtt-will-message)を参照してください。

## EMQX で Keep Alive を使用する方法

[EMQX](https://www.emqx.com/ja/products/emqx)では、構成ファイルを通じてサーバー  Keep Alive  メカニズムの動作をカスタマイズできます。関連するフィールドは次のとおりです。

**zone.external.server_keepalive**

| Type    | Default |
| :------ | :------ |
| integer | -       |

この値が設定されていない場合、 Keep Alive 時間は接続の作成時にクライアントによって決定されます。

この値が設定されている場合、ブローカーはそのゾーン内のすべての接続に対してサーバー  Keep Alive  メカニズムを強制的に有効にし、その値を使用してクライアント接続リクエストの値をオーバーライドします。

**zone.external.keepalive_backoff**

| Type  | Optional Value | Default |
| :---- | :------------- | :------ |
| float | > 0.5          | 0.75    |

MQTT プロトコルでは、ブローカーは、 Keep Alive 時間の 1.5 倍以内にクライアントからプロトコル パケットを受信しない場合、クライアントが切断されたとみなす必要があります。

EMQX では、ユーザーがブローカー側で Keep Alive の動作をより柔軟に制御できるようにするために、 Keep Alive  バックオフ要素を導入し、構成ファイルを通じてこの要素を公開しました。

バックオフ係数を導入した後、EMQX は次の式を使用して最大タイムアウトを計算します。

```
Keepalive * backoff * 2
```

バックオフのデフォルト値は 0.75 です。したがって、ユーザーがこの構成を変更しない場合、EMQX の動作は MQTT 標準に完全に準拠します。

詳細については、[EMQX configuration documentation](https://www.emqx.io/docs/en/v4.3/configuration/configuration.html) を参照してください。

> ***注: WebSocket 接続の Keep Alive の設定***
>
> *EMQX は、WebSocket を介したクライアント アクセスをサポートします。クライアントが WebSocket を使用して接続を開始する場合、必要なのはクライアント接続パラメーターに Keep Alive 値を設定することだけです。*[*「WebSocket 上で MQTT を使用するためのクイックスタート ガイド」*](https://www.emqx.com/ja/blog/connect-to-mqtt-broker-with-websocket)*を参照してください。*

## まとめ

この記事では、MQTT プロトコルの Keep Alive  メカニズムと、それを EMQX で使用する方法を紹介します。この機能を使用すると、[ MQTT コネクション](https://www.emqx.com/ja/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)の安定性を確保し、より堅牢な IoT アプリケーションを構築できます。

次に、EMQ が提供する「MQTT プロトコルの[わかりやすいガイド](https://www.emqx.com/en/mqtt-guide)」シリーズの記事を参照して、MQTT プロトコルの機能について学び、MQTT のより高度なアプリケーションを探索し、MQTT アプリケーションとサービスの開発を始めることができます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
