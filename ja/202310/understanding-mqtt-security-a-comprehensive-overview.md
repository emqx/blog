ヘルスケア、スマートホーム、スマートシティ、自動運転車などの分野でIoTが私たちの生活にますます浸透するにつれ、デバイスのセキュリティがより重要になっている。何十億ものデバイスが送信するデータを保護するだけでなく、これらのデバイスを使用する個人の安全にも気を配る必要がある。IoTシステムに侵入した侵入者は、人間に深刻な身体的危害を与える可能性がある。

そのため、IoTセキュリティはIoT開発において避けられないテーマとなっている。

## IoT システムにとってセキュリティがそれほど重要なのはなぜですか?

子供用のスマートおもちゃなどの IoT システムの脆弱性を悪用するハッカーについてのニュースを耳にします。侵入者はおもちゃのカメラ、スピーカー、マイクにアクセスし、子供を監視することができます。別の例では、ハッカーがペースメーカーをハッキングして心拍数を操作し、バッテリーを消耗させ、患者に重大な危害を与える可能性がありました。

これらの IoT システムが侵害された理由は、セキュリティの欠如でした。パスワードが弱く、暗号化がないため、侵入者がこれらのシステムを侵害することが容易になりました。セキュリティ対策が講じられていれば、こうした侵入が発生する可能性は減少したでしょう。

セキュリティがいかに無視され得るかは簡単にわかります。システムはセキュリティなしでも問題なく動作しますが、なぜわざわざセキュリティを設定する必要があるのでしょうか? さらに、システムが設計、テストされ、動作したら、製品を市場に投入したいと思いますよね? ただし、IoT システムのセキュリティを無視すると、短絡的でコストがかかる可能性があります。クライアントにとって、それは財産、データプライバシーの喪失、さらには最悪の場合、個人の安全や生命の喪失を意味する可能性があります。あなたの会社にとって、それは製品リコールのコスト、訴訟費用の可能性、ブランドの評判と信頼の損失を意味する可能性があります。これらはすべて、事前にいくつかの簡単なセキュリティ対策を講じることで回避または軽減できる結果です。

## IoT ネットワークにおける一般的なセキュリティリスク

IoT ネットワークを構築する際に留意する必要がある一般的なセキュリティ リスクをいくつか紹介します。

- 不十分な認証および認可メカニズム: 認証メカニズムが弱いかまったくない IoT デバイスは、不正アクセスに対して脆弱になる可能性があります。デバイスのアクセスを制御するだけでなく、デバイスがネットワークに接続された後に実行できることを制御することも重要です。
- 弱いパスワード: 一部のベンダーは、同じデバイス モデルに同じパスワードを使用する場合があります。他のベンダーは、「admin」や「password」など、推測しやすい弱いパスワードを使用している場合があります。後の記事で説明するように、最も高度な暗号化アルゴリズムは、パスワードをユーザー名と同じにするなど、簡単に推測できるパスワードを克服することはできません。パスワードが弱いと、攻撃者がデバイスとそのデータに簡単にアクセスできます。IoT ベンダーは、強力なパスワード ポリシーを適用し、ユーザーにデフォルトのパスワードの変更を要求する必要があります。
- 安全でない通信プロトコル: IoT 通信で TLS ではなく TCP などの平文通信を使用すると、攻撃者がデータを傍受しやすくなります。たとえば、中間者攻撃では、攻撃者が IoT 通信を盗聴して、パスワード、健康情報、その他の個人データなどの個人データを収集できます。
- ユーザートレーニングの欠如: IoT ベンダーは、ユーザーに適切なセキュリティ意識を提供していない可能性があります。これにより、教育を受けていないユーザーは攻撃に対して脆弱になります。IoT ベンダーがユーザーに適切なセキュリティ トレーニングを提供することが重要です。
- サービス拒否 (DoS) 攻撃: IoT ネットワークは、多数のデバイスを使用してソフトウェアの欠陥を悪用したり、単純に悪意のあるトラフィックでネットワークをフラッディングしたりする DoS または分散型 DoS 攻撃に対して脆弱になる可能性があります。このような攻撃を防ぐために、IoT ネットワークにはファイアウォール、侵入検知および防御システム、アクセス制御などの堅牢なセキュリティ対策を導入する必要があります。さらに、IoT ネットワークは、多大な管理労力を必要とせずに、攻撃を自動的に検出して軽減できる機能を備え、回復力が高くなるように設計する必要があります。

IoT ベンダーは、デバイスの安全性と攻撃に対する耐性を確保するために、初期設計段階から、販売後を含む導入まで、IoT 設計のあらゆる側面でセキュリティを優先する必要があります。

## IoT システムを保護するために MQTT で何ができるでしょうか?

IoT システムを構築する際には、セキュリティについて考慮する必要がある側面がいくつかあります。これらは、存在するさまざまなプロトコル層ごとに分類できます。つまり、ネットワーク層、トランスポート層、アプリケーション層です。

**ネットワーキング層**: MQTT は IP ネットワークで実行されるため、ネットワーキング層のセキュリティのベスト プラクティスはすべて MQTT に適用されます。つまり、ファイアウォール、VPN、IPsec を適切に使用して、侵入者が IoT ネットワーク上のデータにアクセスするのを防ぎます。

**トランスポート層:**トランスポート層では、TCP や WebSocket などのプロトコルを介してプレーンテキスト データを直接送信することはお勧めしません。たとえば、アプリケーション層での認証に使用されるユーザー名やパスワードなどの機密データにより、アプリケーション層のセキュリティ メカニズムが役に立たなくなる可能性があります。なぜなら、侵入者がトランスポート層から直接データを盗むと、私たちが使用しているユーザー名とパスワードを直接知ることができるからです。

TLS 暗号化プロトコルを利用して、データにエンドツーエンドのセキュリティを提供することをお勧めします。TLS は、データを解読が困難な暗号文データに変換するだけでなく、クライアントによるサーバー ID の合法性の確認のサポートなど、複数の保護も提供します。クライアントが証明書を使用する必要がある場合、サーバーはクライアントが合法であるかどうかを確認することもできます。これにより、中間者攻撃を効果的に回避できます。

**アプリケーション層:**トランスポート層では十分なセキュリティ保護が提供されているように見えますが、すべてのシステムが TLS をサポートしているわけではありません。アプリケーション層で実行される MQTT プロトコルは、ユーザー名とパスワードのフィールドによるパスワード認証とトークン認証のサポートも提供し、正当なデバイスのみが MQTT ブローカーにアクセスできるようにします。MQTT 5.0 では、双方向の ID 確認を提供する拡張認証メカニズムも導入されています。

一方、アプリケーション層のセキュリティ メカニズムは通常、セキュリティ保証の最後の層です。アクセサーの ID を検証することに加えて、アクセサーがどのトピックにメッセージを公開できるか、どのトピックからメッセージを消費できるかなど、アクセサーが実行できる操作を確認することをお勧めします。

## まとめ

全体として、MQTT セキュリティは、IoT システムをさまざまな攻撃や脅威から保護する上で重要な要素です。この記事では、MQTT セキュリティの重要性と、開発者やシステム管理者が遭遇する可能性のある一般的なセキュリティ課題を取り上げ、MQTT セキュリティの包括的な概要を説明しました。また、記事で述べたように、IoT システム デバイスのセキュリティを強化するために MQTT を使用して実装できる対策は数多くあります。このシリーズの次の記事を読むことで、MQTT セキュリティに対してより包括的かつ積極的なアプローチを採用し、システムの長期的な安定性と信頼性を確保できると信じています。

次回は、[**パスワードによる認証**](https://www.emqx.com/ja/blog/securing-mqtt-with-username-and-password-authentication)方法について紹介します。ご期待ください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
