これまでのこのシリーズの[前記事](https://www.emqx.com/ja/blog/category/security)では、暗号化、認証、セキュリティプロトコルなど、サイバー攻撃からIoTデバイスを保護するさまざまな方法を探ってきました。しかし、定期的な更新とメンテナンスは、IoTデバイスの継続的なセキュリティを確保するために同等に重要であることを認識することが欠かせません。さらに、システムとサービスのクラウドへの移行が増えていることから、基盤となるオペレーティングシステムのセキュリティがより重要になっています。この記事では、オペレーティングシステムセキュリティを強化するための戦略を多角的に包括的に概説します。

## OSとソフトウェアの定期的なアップデート

最新のオペレーティング・システムとソフトウェアを維持することは、システムのセキュリティを維持する上で極めて重要です。オペレーティング・システムやソフトウェアの新しいバージョンは、セキュリティ上の問題に対処し、バグを修正し、全体的なセキュリティ性能を向上させることがよくあります。そのため、タイムリーなアップデートを行うことで、システム攻撃のリスクを大幅に軽減することができます。

オペレーティング・システムやソフトウェアを更新する際は、以下の手順を考慮すること：

- アップデートソースの信頼性を確認します：このステップでは、信頼できるソースからのみアップデートをダウンロードするようにし、信頼できないソースからマルウェアをダウンロードするリスクを軽減します。
- 更新されたシステムをテストする：更新されたシステムを本番環境に配備する前に、その安定性と安全性を検証するために、制御された環境での徹底的なテストが必要である。
- セキュリティ・パッチをインストールする：セキュリティ・パッチをインストールすることで、最新の脆弱性やバグを修正し、システムのセキュリティを強化することができる。

### OpenSSLによるセキュリティ強化

OpenSSLは、SSLとTLSプロトコルの暗号化と復号化機能を提供する、広く利用されているオープンソース・ソフトウェア・ライブラリです。OpenSSLが広く採用されていることから、OpenSSLのセキュリティを確保することは依然として最重要課題となっています。近年、OpenSSL は深刻な脆弱性と攻撃に遭遇しています。その結果、OpenSSLのセキュリティを強化するために、以下の対策を実施することができます。

1. OpenSSLバージョンの更新

   OpenSSLのバージョンを常に最新に保つことは、セキュリティを確保するために不可欠です。OpenSSLの新しいバージョンには、既知の脆弱性の修正と新しいセキュリティ機能の導入が含まれていることがよくあります。あなたのアプリケーションやシステムが攻撃を受けたかどうかに関係なく、OpenSSLのバージョンを優先的に更新することは非常に重要です。現在、古いバージョンを使用している場合は、速やかに利用可能な最新バージョンにアップグレードすることを強くお勧めします。OpenSSLの公式ウェブサイトでは、最新バージョンのダウンロードを提供しています。

2. 堅牢なパスワードポリシーの導入

   鍵や証明書を保護するために、OpenSSLはパスワードの使用をサポートしている。セキュリティを強化するには、強力なパスワードを利用し、定期的に更新することが不可欠である。パスワード管理ツールを使用することで、異なるシステム間で弱いパスワードや繰り返し使用されるパスワードを防ぐことができる。パスワードが流出した場合は、直ちにパスワードを変更することが不可欠である。また、パスワード生成ツールを使って、ランダムで強固なパスワードを作成することもできる。異なるシステムが使用されている場合、シングルサインオンツールを使用することで、複数のシステム間でパスワードが再利用されることによるパスワード流出のリスクを軽減することができる。

3. アクセス・コントロールの強化

   OpenSSLへのアクセスは、最小特権の原則に従い、許可されたユーザーに制限されるべきである。OpenSSLへのアクセスを保護するために、VPNのような安全な経路を採用すべきである。システムへの攻撃が続いている場合は、OpenSSLへのアクセスを速やかに制限することが重要です。ファイアウォールのようなセキュリティ・ツールでアクセスを制限し、二要素認証ツールでアクセス制御を強化することができます。

4.  証明書の検証

   OpenSSLを利用する場合、証明書の有効性を検証することが不可欠です。証明書を検証することで、セキュリティの脅威から保護し、中間者攻撃のリスクを軽減します。証明書の有効性を確認するには、証明書失効リスト（CRL）と証明書チェーンを使用する必要がある。証明書が失効した場合、直ちに更新する必要がある。証明書管理ツールは証明書の管理を支援し、信頼できる証明書の取得は認証局（CA）を通じて行うことができる。

5.  ロギングとモニタリング

   OpenSSL の活動をログに記録し、監視することは、セキュリティ上の問題を特定し、対処するために極めて重要です。OpenSSL のログ機能を有効にし、セキュリティ上の懸念がないか、定期的にログを確認することを推奨します。セキュリティ監視ツールを使用することで、OpenSSL の活動をリアルタイムで監視することができ、セキュリティインシデントへの迅速な対応が可能になります。OSSECやSNORTのようなオープンソースのセキュリティ監視ツールを利用することができ、人工知能や機械学習手法を適用することで、ログ分析やデータ監視を支援することができる。

まとめると、OpenSSLのセキュリティを強化するには、多面的なアプローチを採用することが不可欠です。OpenSSLの迅速なアップデート、強固なパスワード・ポリシーの導入、アクセス制御の強化、証明書の検証、ロギングと監視の有効化などが、OpenSSLを保護するための重要なステップです。OpenSSLのセキュリティの詳細については、OpenSSLの公式ドキュメントを参照するか、OpenSSLのセキュリティ・トレーニング・コースに参加して、セキュリティとシステム保護の知識を深めることを検討してください。

## 未使用のサービスとポートを無効化

オペレーティング・システムは、デフォルトでさまざまなサービスやポートが有効になっているが、その多くは不要なものだ。システムのセキュリティを強化するためには、使われていないサービスやポートを無効にすることが重要である。systemd、inetd、xinetdなどのコマンドラインツールがこの目的に使える。

不要なサービスやポートを無効にする場合は、以下の点を考慮すること：

- システム機能の維持：サービスやポートを無効にする前に、その目的と潜在的な影響を理解し、通常のシステム運用を妨げないようにすることが重要です。
- サービスとポートを定期的に監視する：システムの変更によって新しいサービスやポートが導入される可能性があるため、システムのセキュリティを確保するために定期的なチェックが必要となる。

### EMQXノードにおけるサービスポートの設定例

1. クラスターノード発見ポート

   環境変数 WITH_EPMD が設定されていない場合、EMQX 起動時に epmd は有効化されず、EMQX ekka がノード検出に使用されます。これは4.0以降のデフォルトのノード発見方法で、ekkaモードと呼ばれる。

   ekkaモードでは、ノード検出のポートマッピング関係が固定されています。node.dist_listen_min と node.dist_listen_max の設定は ekka モードでは適用されません。

   クラスタ・ノード間にファイアウォールがある場合は、この固定ポートを許可する必要があります。固定ポートのルールは以下のとおりです：ListeningPort = BasePort + Offset.

   - BasePortは常に4370に設定され、変更することはできない。
   - オフセットはノード名の末尾の数字によって決まる。ノード名の末尾に数字がない場合、オフセットは0になります。

   例えば、emqx.confのノード名が `node.name` = `emqx@192.168.0.12` に設定されている場合、リスニングポートは4370です。emqx1(またはemqx-1)の場合、ポートは4371となります。

2. クラスタRPCポート

   各ノードにはRPCポートが必要で、これもファイアウォールで許可する必要があります。ekkaモードのクラスタ発見ポートと同様に、このRPCポートは固定です。

   RPCポートはekkaモードと同じルールに従いますが、BasePort = 5370となります。例えば、emqx.confのノード名が `node.name` = `emqx@192.168.0.12` の場合、RPCポートは5370です。emqx1（またはemqx-1）の場合、ポートは5371です。

3. MQTT外部サービスポート

   [MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は2つのデフォルト・ポートを使用する：暗号化されていないトランスポートには 1883、暗号化されたトランスポートには 8883 を使用する。クライアントが [MQTT ブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続する際には、適切なポートを選択することが重要である。

   さらに、MQTTは、WebSocket接続やSSLプロキシ接続によく使用される8083や8084などの代替ポートをサポートしている。これらの代替ポートは、通信オプションの拡張とセキュリティ機能の追加を提供する。

## アクセス・コントロールの実装

アクセス・コントロールは、システムのセキュリティを確保するための重要な手段のひとつである。アクセス・コントロールは、以下のような方法で実施することができる：

- パスワードの使用を義務付ける：ユーザーにパスワードの使用を義務付けることで、システムを不正アクセスから守ることができる。
- ログイン試行を制限する：ログイン試行を制限することで、間違ったパスワードでシステムにログインしようとするような総当たり攻撃を抑止することができる。
- ファイアウォールを採用する：ファイアウォールを採用することで、ネットワーク・トラフィックをフィルタリングし、不正アクセスを防ぐことができる。

アクセス制御の方法を導入する場合、以下の点に注意する必要がある：

- パスワードの複雑性を高める：パスワードは、推測されたりクラックされたりしないよう、十分に複雑でなければならない。
- パスワードを定期的に更新する：パスワードを定期的に更新することで、パスワードが流出する可能性を低くすることができる。
- ファイアウォールルールの設定セキュリティとパフォーマンスを最適化するために、実際の状況に応じてファイアウォールルールを設定する必要があります。

## その他のセキュリティ設定

上記の対策に加え、システムを保護するためにいくつかのセキュリティ設定を実施することができる：

- ファイルシステムの暗号化：ファイルシステムを暗号化することで、データの機密性を確保し、データが盗難にあった場合でも漏洩を防ぎます。
- SELinuxの活用SELinuxはセキュリティを強化したLinuxカーネルモジュールで、プロセスのパーミッションを効果的に制限し、システムの脆弱性や潜在的な攻撃のリスクを低減します。
- ロギングの有効化：ロギング機能を有効にすることで、システムとアプリケーションの活動を監視できるようになり、セキュリティ・インシデントの検出と対応が容易になる。
- セキュリティ・ハードニング・ツールの採用：セキュリティ・ハードニング・ツールは、セキュリティ・チェックと修正を自動化し、システム・セキュリティを強化する。OpenSCAPやLynisのようなツールは、脆弱性検出とシステム・ハードニングのための貴重なリソースである。

## セキュリティ意識の構築

システムを保護するためには、技術的な対策に加え、セキュリティ意識の醸成が極めて重要である。セキュリティ意識は、以下のような方法で醸成することができる：

- 従業員教育：従業員にセキュリティ対策を教育し、意識とスキルを向上させる。
- セキュリティポリシーの策定従業員の行動と責任を規定するセキュリティ方針を策定し、実施する。
- 定期的な訓練：セキュリティ事故を想定した訓練を定期的に実施し、従業員の緊急対応能力を高める。

## まとめ

この記事を通して、システムセキュリティを改善するための方法とツールを紹介した。もちろん、システムセキュリティは一度限りの作業ではなく、継続的な注意と更新が必要です。また、[EMQX](https://www.emqx.com/ja/products/emqx)などの安全で信頼できる製品を使用することもお勧めします。EMQXには強力なセキュリティ機能と優れた信頼性があり、システム全体のセキュリティを向上させることができます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
