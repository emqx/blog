## QoSとは何ですか

ネットワーク環境では、MQTT デバイスは、TCP トランスポート プロトコルのみを使用して信頼性の高い通信を確保するのに苦労する可能性があります。この問題に対処するために、MQTT には、さまざまなレベルのサービスを提供するさまざまなメッセージ対話オプションを提供するサービス品質 (QoS) メカニズムが組み込まれており、さまざまなシナリオで信頼性の高いメッセージ配信に対するユーザーの特定の要件に応えます。

MQTT には 3 つの QoS レベルがあります。

- QoS 0、最大 1 回。
- QoS 1、少なくとも 1 回。
- QoS 2、正確に 1 回。

これらのレベルは、メッセージ配信の信頼性レベルの増加に対応します。QoS 0 はメッセージを失う可能性があり、QoS 1 はメッセージの配信を保証しますが重複メッセージが存在する可能性があり、QoS 2 はメッセージが重複せずに 1 回だけ配信されることを保証します。QoS レベルが増加すると、メッセージ配信の信頼性も高まりますが、送信プロセスの複雑さも増加します。

パブリッシャーからサブスクライバーへの配信プロセスでは、パブリッシャーは PUBLISH パケット内のメッセージの QoS レベルを指定します。通常、ブローカーは同じ QoS レベルでメッセージを加入者に転送します。ただし、場合によっては、加入者の要件により、転送されるメッセージの QoS レベルの低下が必要になる場合があります。

たとえば、サブスクライバが QoS レベル 1 以下のメッセージのみを受信するように指定した場合、ブローカは QoS 2 メッセージをこのサブスクライバに転送する前に QoS 1 にダウングレードします。QoS 0 および QoS 1 のメッセージは、元の QoS レベルが変更されないまま加入者に送信されます。

![MQTT QoS Downgrade](https://assets.emqx.com/images/6a5e702f5621af6974e0785b1bbbdb43.png)

QoS がどのように機能するかを見てみましょう。

## QoS 0 - 最大 1 回

QoS 0 は最低レベルのサービスであり、「ファイア アンド フォーゲット」とも呼ばれます。このモードでは、送信者は確認応答を待ったり、メッセージを保存して再送信したりしないため、受信者は重複したメッセージを受信することを心配する必要がありません。

![MQTT QoS 0](https://assets.emqx.com/images/2c36da33012fac0e6943c7f6f8b5aa7f.png)

### QoS 0 メッセージが失われるのはなぜですか?

QoS 0 メッセージ送信の信頼性は、TCP 接続の安定性に依存します。接続が安定している場合、TCP はメッセージを確実に正常に配信できます。ただし、接続が閉じられたりリセットされたりすると、転送中のメッセージやオペレーティング システム バッファ内のメッセージが失われ、QoS 0 メッセージの配信が失敗する可能性があります。

## QoS 1 - 少なくとも 1 回

メッセージ配信を確実にするために、QoS 1 には確認応答および再送信メカニズムが導入されています。送信者が受信者から PUBACK パケットを受信すると、メッセージは正常に配信されたと見なされます。それまで、送信者は再送信に備えて PUBLISH パケットを保存する必要があります。

送信者は各パケットのパケット ID を使用して、PUBLISH パケットと対応する PUBACK パケットを照合します。これにより、送信者は正しい PUBLISH パケットを識別し、キャッシュから削除できるようになります。

![MQTT QoS 1](https://assets.emqx.com/images/5affbdf88707c5596e0fc5d16045b4ac.png)

### QoS 1 メッセージが重複するのはなぜですか?

送信者が PUBACK パケットを受信しないケースが 2 つあります。

1. PUBLISH パケットは受信者に届きませんでした。
2. PUBLISH パケットは受信者に到着しましたが、受信者の PUBACK パケットはまだ送信者に受信されていません。

最初のケースでは、送信者は PUBLISH パケットを再送信しますが、受信者はメッセージを 1 回しか受信しません。

2 番目のケースでは、送信者が PUBLISH パケットを再送信し、受信者がそれを再度受信することになり、メッセージが重複します。

![MQTT QoS 1 duplicated](https://assets.emqx.com/images/9ca3130db4fdcadf1ca2a6fe75240eb0.png)

再送信された PUBLISH パケットの DUP フラグが 1 に設定されて重複メッセージであることを示しても、受信側はメッセージをすでに受信しているとは想定できず、依然として新しいメッセージとして扱う必要があります。

これは、受信者が DUP フラグが 1 の PUBLISH パケットを受信した場合、次の 2 つのシナリオが考えられるためです。

![MQTT QoS 1 DUP](https://assets.emqx.com/images/72015dc94b030ba7f8b9ed6af7300881.png)

最初のケースでは、送信者は PUBACK パケットを受信しなかったため、PUBLISH パケットを再送信します。受信者は同じパケット ID を持つ 2 つの PUBLISH パケットを受信し、2 番目の PUBLISH パケットの DUP フラグは 1 です。2 番目のパケットは確かに重複メッセージです。

2 番目のケースでは、元の PUBLISH パケットが正常に配信されました。次に、このパケット ID は、無関係な新しいメッセージに使用されます。しかし、この新しいメッセージは最初に送信されたときにピアに正常に配信されなかったため、再送信されました。最後に、再送信された PUBLISH パケットは同じパケット ID と 1 の DUP フラグを持ちますが、これは新しいメッセージです。

これら 2 つのケースを区別することはできないため、受信側は DUP フラグが 1 のすべての PUBLISH パケットを新しいメッセージとして扱う必要があります。これは、QoS 1 を使用する場合、プロトコル レベルで重複メッセージが存在することは避けられないことを意味します。

まれに、ブローカーがパブリッシャーから重複した PUBLISH パケットを受信し、サブスクライバーに転送するプロセス中に、それらのパケットを再度再送信することがあります。これにより、サブスクライバが追加の重複メッセージを受信する可能性があります。

たとえば、発行者は 1 つのメッセージしか送信しませんが、受信者は最終的に 3 つの同一のメッセージを受信する可能性があります。

![MQTT QoS 1 duplicated](https://assets.emqx.com/images/576568b549516c44969bcb12f442ed19.png)

これらは QoS 1 を使用する場合の欠点です。

## QoS 2 - 1 回だけ

QoS 2 は、QoS 0 や 1 とは異なり、メッセージが失われたり重複したりしないことを保証します。ただし、メッセージごとに送信者と受信者の間で少なくとも 2 つの要求/応答フローが必要となるため、最も複雑な対話と最も高いオーバーヘッドも発生します。配達。

![MQTT QoS 2](https://assets.emqx.com/images/7a29e2c1e65bb68b10f596e10f60be35.png)

1. QoS 2 メッセージの送信を開始するには、送信者はまず QoS 2 を使用して PUBLISH パケットを保存して送信し、次に受信者からの PUBREC 応答パケットを待ちます。このプロセスは QoS 1 と似ていますが、応答パケットが PUBACK ではなく PUBREC である点が異なります。
2. PUBREC パケットを受信すると、送信者は PUBLISH パケットが受信者によって受信されたことを確認し、ローカルに保存されているそのコピーを削除できます。このパケットは**もう必要ないため、再送信することはできません**。次に、送信者は PUBREL パケットを送信して、パケット ID を解放する準備ができていることを受信者に通知します。PUBLISH パケットと同様、PUBREL パケットは受信者に確実に配信される必要があるため、再送信に備えて保存され、応答パケットが必要となります。
3. 受信機は、PUBREL パケットを受信すると、この送信フローで追加の再送信された PUBLISH パケットが受信されないことを確認できます。その結果、受信側は PUBCOMP パケットで応答し、現在のパケット ID を新しいメッセージに再利用する準備ができていることを知らせます。
4. 送信者が PUBCOMP パケットを受信すると、QoS 2 フローが完了します。その後、送信者は現在のパケット ID を使用して新しいメッセージを送信でき、受信者はそれを新しいメッセージとして扱います。

### QoS 2 メッセージが重複しないのはなぜですか?

QoS 2 メッセージが失われないようにするために使用されるメカニズムは、QoS 1 で使用されるメカニズムと同じであるため、ここでは再度説明しません。

QoS 1 と比較して、QoS 2 では、PUBREL パケットと PUBCOMP パケットに関連する新しいプロセスを追加することで、メッセージが重複しないようにします。

先に進む前に、QoS 1 がメッセージの重複を回避できない理由を簡単に確認しましょう。

QoS 1 を使用すると、受信側では、応答が送信側に届いたかどうかに関係なく、PUBACK パケットの送信後にパケット ID が再び利用可能になります。これは、受信者は、後で受信した同じパケット ID を持つ PUBLISH パケットが、PUBACK 応答を受信していないことによる送信者からの再送信なのか、それとも送信者がパケット ID を再利用して新しいメッセージを送信したのかを判断できないことを意味します。 PUBACK 応答を受信しています。これが、QoS 1 がメッセージの重複を回避できない理由です。

![MQTT PUBACK](https://assets.emqx.com/images/fe56d9ac55db01422077f9b311aae302.png)

QoS 2 では、送信者と受信者は PUBREL パケットと PUBCOMP パケットを使用してパケット ID のリリースを同期し、送信者がメッセージを再送信するか新しいメッセージを送信するかについて合意が得られるようにします。これは、QoS 1 で発生する可能性のある重複メッセージの問題を回避するための鍵です。

![MQTT PUBREL and PUBCOMP](https://assets.emqx.com/images/cc67a5f9b3c583019aecf920e0cfd0ca.png)

QoS 2 では、送信者は受信者から PUBREC パケットを受信する前に PUBLISH パケットを再送信することが許可されます。送信者が PUBREC を受信し、PUBREL パケットを送信すると、パケット ID 解放プロセスに入ります。送信者は、受信者から PUBCOMP パケットを受信するまで、PUBLISH パケットを再送信したり、現在のパケット ID を使用して新しいメッセージを送信したりすることはできません。

![MQTT PUBREC](https://assets.emqx.com/images/74c4210e7750c0bbda1d771bb2775c32.png)

その結果、受信側は PUBREL パケットを境界として使用し、その前に到着するすべての PUBLISH パケットを重複とみなし、その後に到着するすべての PUBLISH パケットを新しいものとみなすことができます。これにより、QoS 2 を使用するときにプロトコル レベルでメッセージの重複を回避できます。

## シナリオと考慮事項

### QoS0

QoS 0 の主な欠点は、ネットワークの状態によってはメッセージが失われる可能性があることです。つまり、接続が切断されているとメッセージを見逃す可能性があります。ただし、QoS 0 の利点は、メッセージ配信の効率が高いことです。

したがって、定期的なセンサーの更新など、いくつかの更新を見逃すことが許容される、高頻度で重要度の低いデータを送信するためによく使用されます。

### QoS1

QoS 1 では、メッセージが少なくとも 1 回配信されることが保証されますが、メッセージが重複する可能性があります。これにより、重要な指示や重要なステータスのリアルタイム更新などの重要なデータの送信に適しています。ただし、重複排除なしで QoS 1 を使用することを決定する前に、そのような重複を処理または許可する方法を検討することが重要です。

たとえば、パブリッシャがメッセージを 1、2 の順序で送信し、サブスクライバがメッセージを 1、2、1、2 の順序で受信する場合、1 は照明をオンにするコマンドを表し、2 はライトをオフにするコマンドを表します。 、メッセージの重複により、ライトが繰り返し点灯したり消灯したりすることは望ましくない場合があります。

![MQTT QoS](https://assets.emqx.com/images/3ab6255134132b2edb019056ccb74f00.png)

### QoS2

QoS 2 は、メッセージが失われたり重複したりしないことを保証します。ただし、オーバーヘッドも最も高くなります。ユーザーがメッセージの重複を自分で処理することを望まず、QoS 2 の追加のオーバーヘッドを受け入れることができる場合は、これが適切な選択です。QoS 2 は、信頼性の高いメッセージ配信を確保し、重複を避けることが重要な金融や航空などの業界でよく使用されます。

## Q&A

### QoS 1 メッセージの重複を排除するにはどうすればよいですか?

QoS 1 メッセージの重複はプロトコル レベルで本質的に発生するため、この問題はビジネス レベルでのみ解決できます。

QoS 1 メッセージの重複を排除する 1 つの方法は、各 PUBLISH パケットのペイロードにタイムスタンプまたは単調に増加するカウントを含めることです。これにより、現在のメッセージのタイムスタンプまたはカウントを最後に受信したメッセージのタイムスタンプまたはカウントと比較することで、そのメッセージが新しいかどうかを判断できます。

### QoS 2 メッセージを加入者にいつ転送する必要がありますか?

これまでに学んだように、QoS 2 には高いオーバーヘッドがあります。QoS 2 メッセージのリアルタイム性への影響を回避するには、QoS 2 PUBLISH パケットを初めて受信したときに、加入者にメッセージを転送するプロセスを開始するのが最善です。ただし、このプロセスが開始されると、メッセージの重複を防ぐために、PUBREL パケットより前に到着する後続の PUBLISH パケットは再度転送されるべきではありません。

### QoSごとにパフォーマンスに違いはありますか?

ピアツーピア通信に同じハードウェア構成で EMQX を使用する場合、QoS 0 と QoS 1 は通常、同様のスループットを持ちますが、QoS 1 の方が CPU 使用率が高くなる可能性があります。さらに、高負荷では、QoS 1 のメッセージ遅延は QoS 0 に比べて長くなります。一方、QoS 2 のスループットは、通常、QoS 0 および 1 の約半分しかありません。

## まとめ

[MQTT について学習を続けるには、EMQ のMQTT Getting Started および Advanced](https://www.emqx.com/en/mqtt-guide)シリーズを参照してください。これらのシリーズでは、ワイルドカード、保持メッセージ、意志メッセージなどのトピックが取り上げられています。これらのリソースは、MQTT をさらに深く掘り下げ、高度な MQTT アプリケーションとサービスを開発するのに役立ちます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
