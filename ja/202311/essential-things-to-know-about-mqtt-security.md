モノのインターネット (IoT) は、周囲の環境と連携する方法を変革しました。スマート ホームからコネクテッド カーに至るまで、IoT デバイスは私たちの日常生活に不可欠な部分になっています。しかし、IoT の普及により、新たなセキュリティ上の課題も生じています。IoT デバイスは、処理能力、メモリ、ストレージ機能が限られているため、サイバー攻撃に対して脆弱であることがよくあります。攻撃者はこれらの脆弱性を悪用して、デバイスへの不正アクセスを取得したり、データを盗んだり、物理的な損傷を引き起こしたりする可能性があります。さらに、デバイスの数が膨大で相互接続されているため、大規模な攻撃を仕掛けようとするハッカーにとって魅力的な標的となります。

MQTT セキュリティは、デバイス間で交換されるデータの機密性、完全性、可用性を確保するために非常に重要です。だからこそ、私たちはこのブログシリーズを皆さんに提供しています。認証、暗号化、アクセス制御などを含む、MQTT セキュリティのさまざまな側面を詳しく掘り下げていきます。このシリーズは、潜在的な脅威や攻撃からシステムを保護するための貴重な洞察を提供するため、MQTT ベースの IoT ソリューションに取り組むすべての人にとって必読の書であると考えられています。

## MQTT セキュリティに関する EMQ シリーズ ブログ

この一連の記事では、MQTT セキュリティの重要な側面と、設計プロセスの最初からセキュリティを IoT システムに組み込む方法について説明します。

このシリーズには次のものが含まれます。

- [**MQTTセキュリティについて：理解しやすい概要**](https://www.emqx.com/ja/blog/understanding-mqtt-security-a-comprehensive-overview)
- **認証**
  - [**パスワードベースの認証**](https://www.emqx.com/ja/blog/securing-mqtt-with-username-and-password-authentication): MQTT におけるパスワードベースの認証について説明します。それがどのように機能し、どのようなセキュリティリスクを解決するか。
  - [**SCRAM を使用した強化された認証**](https://www.emqx.com/ja/blog/leveraging-enhanced-authentication-for-mqtt-security): ユーザー名/パスワードの認証情報がプレーン テキストで送信されることを回避するための SCRAM (Salted Challenge Response Authentication Mechanism) について説明します。
  - [**追加の認証方法**](https://www.emqx.com/ja/blog/a-deep-dive-into-token-based-authentication-and-oauth-2-0-in-mqtt): JWT トークン、HTTP フックなどの追加の認証方法。
- [**認可**](https://www.emqx.com/ja/blog/authorization-in-mqtt-using-acls-to-control-access-to-mqtt-messaging): 認可とは何ですか?また認証との違いは何ですか? ACL とは何ですか? ACL によって何が達成できるのでしょうか?
- [**TLS/SSL**](https://www.emqx.com/ja/blog/fortifying-mqtt-communication-security-with-ssl-tls) : 一方向 TLS と双方向 TLS の違い。PSK とは何か、また新しい安全な暗号スイートの使用方法。
- [**レート制限**](https://www.emqx.com/ja/blog/improve-the-reliability-and-security-of-mqtt-broker-with-rate-limit): レート制限によってセキュリティが確保される方法と、一般的なレート制限戦略。
- [**インフラセキュリティの強化**](https://www.emqx.com/ja/blog/five-strategies-for-strengthening-mqtt-infrastructure-security)：インフラ面からセキュリティを強化する方法。
- **メッセージ暗号化**: リソースに制約のあるデバイスの TLS の代替としてメッセージ暗号化を使用する方法。利用可能な暗号化方式とその長所と短所。
- **MQTT によるファジング**: ファジング テストとは何ですか? IoT システムの脆弱性を見つけるためにファジング テストをどのように使用できますか? MQTT ブローカーをファジングする方法。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
