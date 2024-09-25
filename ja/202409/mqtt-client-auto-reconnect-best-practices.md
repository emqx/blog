## 背景

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)はTCP上に構築されたパブリッシュ/サブスクライブプロトコルで、低帯域幅や不安定な接続が一般的なIoTやセンサーネットワークなどの環境で広く使用されています。このようなシナリオでは、ネットワーク接続がしばしば信頼性に欠け、ネットワーク障害、信号の弱さ、パケットロスなどの問題が発生し、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)とサーバー間の接続が切断される可能性があります。IoTアプリケーションでの一般的な切断と再接続の状況には以下があります：

1. ネットワーク状態が悪いか切断され、MQTTクライアントがタイムアウトして接続を失う。
2. サーバー側の活動（アップグレードや意図的なシャットダウンなど）により、接続が切断される。
3. デバイスやクライアントの再起動により、クライアントが積極的に再接続を試みる。
4. その他のネットワーク関連の要因でTCP/IP接続が切断され、MQTT再接続が発生する。

MQTTクライアントとサーバー間の安定した接続を維持するためには、MQTTクライアントが再接続ロジックを実装することが不可欠です。これにより、クライアントは自動的にサーバーに再接続し、以前の購読状態を復元し、セッションの連続性を維持することができます。

## MQTTクライアントの再接続ロジックの重要性

再接続は、MQTTを使用する多くのIoTアプリケーションで避けられません。効果的なMQTTクライアントの再接続ロジックを設計することは非常に重要です。これは、適切なイベントコールバックを使用し、各再接続試行に合理的なランダムバックオフ間隔を設定することを含みます。適切に設計された再接続ロジックは、クライアントとサーバーが長期間安定して動作し、ビジネスがスムーズに運用できるようにします。

不適切に設計された再接続ロジックは、以下のような問題を引き起こす可能性があります：

1. 再接続ロジックの失敗により、クライアントがブローカーからのメッセージを受信しなくなり、警告も発生しない。
2. バックオフメカニズムのない頻繁な再接続試行がブローカーを圧倒し、DDoS攻撃を引き起こす可能性がある。
3. クライアントの切断と再接続が頻繁に発生し、ブローカーのリソースを過度に消費する。

適切に設計された再接続戦略は、MQTTクライアントの安定性と信頼性を向上させ、ネットワーク中断によるデータ損失や遅延などの問題を回避し、頻繁な接続試行を防ぐことでサーバーの負荷を軽減します。

## 効果的なMQTTクライアント再接続ロジックの設計方法

MQTTクライアントの再接続コードを作成する際には、堅牢で安定したパフォーマンスを確保するために、いくつかの重要な要素を考慮する必要があります：

- **適切なキープアライブ時間の設定**：MQTTクライアントのキープアライブ間隔、[Keep Alive](https://www.emqx.com/ja/blog/mqtt-keep-alive)は、接続の健全性を監視するために重要です。キープアライブタイムアウトに達すると、クライアントは再接続を試み、サーバーは接続を閉じます。キープアライブ間隔は、クライアントとサーバーが接続の喪失を検出する速度に影響します。この値は、ネットワーク条件と望ましい最大待機時間に基づいて設定する必要があります。
- **再接続ポリシーとバックオフ戦略**：異なるネットワーク環境では、異なる再接続ポリシーが必要になる場合があります。例えば、ネットワーク接続が切断された場合、最初の待機時間を設定し、各再接続試行後に待機時間を徐々に増やすことができます。このアプローチは、ネットワークがダウンしているときに再接続試行の洪水を防ぎます。指数バックオフアルゴリズムや、ランダムとステップ遅延の組み合わせを使用することが推奨され、適切なバックオフ間隔を確保します。
- **接続状態の管理**：クライアントは、接続状態、切断の理由、購読しているトピックのリストを記録する必要があります。切断時には、切断理由をログに記録し、適切に再接続を試みます。セッション永続化機能を使用する場合、クライアントはこの情報を独立して保存する必要がないかもしれません。
- **例外処理**：サーバーの不在、認証エラー、ネットワーク異常など、接続プロセス中にさまざまな問題が発生する可能性があります。これらの問題に適切に対処するために、クライアント内に例外処理ロジックを含めることが重要です。[MQTT 5](https://www.emqx.com/en/blog/introduction-to-mqtt-5)プロトコルは詳細な切断理由を提供し、クライアントはこの情報に基づいて例外をログに記録し、切断して再接続できます。
- **最大再接続試行回数の制限**：一部の低電力デバイスでは、過度なリソース消費を避けるために、再接続試行の最大回数を制限することが重要です。最大試行回数に達した場合、クライアントは再接続を試みるのを停止し、不要な再接続試行を防ぐためにスリープ状態に入るべきです。
- **バックオフアルゴリズム**：再接続のための一般的なバックオフ方法には、[指数バックオフ](https://ja.wikipedia.org/wiki/指数バックオフ)とランダムバックオフアルゴリズムがあります。指数バックオフ方法は、負のフィードバックメカニズムを通じて待機時間を指数的に増加させ、最適な送信/接続率を見つけます。ランダムバックオフでは、定義された上限と下限内でランダムな遅延を待機し、広く使用され、実装が容易なアプローチです。

## 再接続のコード例

以下は、Paho MQTT Cライブラリを使用して自動再接続機能を実装する例です。その非同期プログラミングモデルを活用しています。Pahoはさまざまなコールバック関数を提供し、それぞれ異なるトリガー条件を持ちます：グローバルコールバック、APIコールバック、および非同期コールバックです。APIコールバックは柔軟性を提供しますが、自動再接続機能を有効にする場合は非同期コールバックを使用することを推奨します。以下の例は、MQTTクライアントの再接続のコンテキストでこれらのコールバックを使用する方法を示しています。

```
// Asyncで使用されるコールバックメソッド
// 接続成功時の非同期コールバック関数で、接続確立後にSubscribe操作を行います。
void conn_established(void *context, char *cause)
{
    printf("client reconnected!\n");
    MQTTAsync client = (MQTTAsync)context;
    MQTTAsync_responseOptions opts = MQTTAsync_responseOptions_initializer;
    int rc;

    printf("Successful connection\n");

    printf("Subscribing to topic %s\nfor client %s using QoS%d\n\n"
           "Press Q<Enter> to quit\n\n", TOPIC, CLIENTID, QOS);
    opts.onSuccess = onSubscribe;
    opts.onFailure = onSubscribeFailure;
    opts.context = client;
    if ((rc = MQTTAsync_subscribe(client, TOPIC, QOS, &opts)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to start subscribe, return code %d\n", rc);
        finished = 1;
    }
}


// 以下はクライアント切断時のグローバルコールバック関数です
void conn_lost(void *context, char *cause)
{
    MQTTAsync client = (MQTTAsync)context;
    MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
    int rc;

    printf("\nConnection lost\n");
    if (cause) {
        printf("     cause: %s\n", cause);
    }
    printf("Reconnecting\n");
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    conn_opts.maxRetryInterval = 16;
    conn_opts.minRetryInterval = 1;
    conn_opts.automaticReconnect = 1;
    conn_opts.onFailure = onConnectFailure;
    MQTTAsync_setConnected(client, client, conn_established);
    if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to start connect, return code %d\n", rc);
        finished = 1;
    }
}

int main(int argc, char* argv[])
{
    // 非同期クライアントに必要な属性構造体を作成
    MQTTAsync client;
    MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
    MQTTAsync_disconnectOptions disc_opts = MQTTAsync_disconnectOptions_initializer;
    int rc;
    int ch;
    // Paho SDKのビルトイン永続化を使用せず、キャッシュされたメッセージを処理する非同期クライアントを作成
    if ((rc = MQTTAsync_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL))
            != MQTTASYNC_SUCCESS)
    {
        printf("Failed to create client, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto exit;
    }

    // 非同期コールバックを設定。ここで設定されるコールバック関数は接続レベルのグローバルコールバックです。
    // conn_lostは接続が失われたときにトリガーされ、成功した接続後の切断時にのみトリガーされます。切断後の再接続に失敗した場合はトリガーされません。
    // msgarrvdはメッセージを受信したときにトリガーされるコールバック関数です。
    // msgdeliverdはメッセージの送信に成功したときにトリガーされるコールバック関数で、通常はNULLに設定します。

    if ((rc = MQTTAsync_setCallbacks(client, client, conn_lost, msgarrvd, msgdeliverd)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to set callbacks, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }

    // 接続パラメータを設定
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    // ここで設定されるコールバックは、API呼び出しが失敗したときにトリガーされます。次の操作がconnect操作であるため、onConnectFailureメソッドに設定します。
    conn_opts.onFailure = onConnectFailure;
    // ここで設定されるコールバックは、クライアント接続のAPI呼び出しが成功したときにトリガーされます。この例では非同期接続APIを使用しているため、これを設定すると両方のコールバックがトリガーされるため、このコールバックは使用しないことをお勧めします。
    //conn_opts.onSuccess = onConnect;
    // 自動再接続は、最初の接続試行が失敗した場合にはトリガーされず、成功した接続後の切断時にのみトリガーされます。
    conn_opts.automaticReconnect = 1;
    // 2〜16秒のランダムバックオフ間隔で自動再接続を有効にする
    conn_opts.maxRetryInterval = 16;
    conn_opts.minRetryInterval = 2;
    conn_opts.context = client;
    // 非同期コールバック関数を設定。これらは前述のAPIコールバックとは異なり、接続が確立または失われるたびにトリガーされます。
    MQTTAsync_setConnected(client, client, conn_established);
    MQTTAsync_setDisconnected(client, client, disconnect_lost);
    // クライアント接続を開始。以前に設定したAPIコールバックはこの操作でのみ有効になります。
    if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to start connect, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }
    ......
}
```

> 完全なコードを見るには、[MQTTAsync_subscribe.c](https://assets.emqx.com/data/MQTTAsync_subscribe.c)ファイルをダウンロードしてください。

## 別のアプローチ：NanoSDKのビルトイン再接続ポリシー

[NanoSDK](https://github.com/emqx/NanoSDK)は、Pahoの代替となるもう一つのMQTT SDKです。[NNG-NanoMSG](https://github.com/nanomsg/nng)プロジェクトに基づいており、MITライセンスの下で開発されているため、オープンソースで商用利用にも適しています。Pahoとの主要な違いの一つは、NanoSDKの完全な非同期I/OとActorプログラミングモデルのサポートで、特にQoS 1/2のメッセージで高いメッセージスループットを可能にします。さらに、NanoSDKはMQTT over QUICプロトコルをサポートしており、大規模なIoTメッセージングサーバーである[EMQX 5.0](https://www.emqx.com/ja/products/emqx)と組み合わせることで、弱いネットワーク条件下でのデータ伝送を改善できます。これらの機能により、NanoSDKは車載ネットワークや産業用シナリオに特に適しています。

NanoSDKでは、再接続ポリシーが完全に統合されているため、ユーザーが手動で実装する必要はありません。

```
// NanoSDKはデフォルトで自動ダイヤラーメカニズムを使用して再接続を処理します
nng_dialer_set_ptr(*dialer, NNG_OPT_MQTT_CONNMSG, connmsg);
nng_dialer_start(*dialer, NNG_FLAG_NONBLOCK);
```

## まとめ

このブログでは、MQTTクライアントの実装における適切な再接続ロジックの重要性を強調し、IoTデバイスの信頼性の高い接続を確保するためのベストプラクティスを提供しました。これらのガイドラインに従うことで、開発者はより効率的なMQTT再接続コードを設計し、クライアントとサーバーの両方のリソースオーバーヘッドを最小限に抑えつつ、IoTアプリケーションで安定した接続を確保できます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
