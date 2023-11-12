## オーソライズとは何ですか?

ユーザー、デバイス、またはアプリケーションの ID と権限に基づいて、特定のリソース、アクション、または情報へのアクセスを許可または拒否するプロセスです。これは、コンピュータ システム、ネットワーク、Web アプリケーション、および機密データやリソースの保護が必要なその他の環境におけるセキュリティとアクセス制御にとって非常に重要です。

承認が必要な主な理由は次のとおりです。

1. **データ セキュリティ**: 承認は、機密データを不正アクセスから保護するのに役立ちます。アクセス制御を強制することにより、許可されたユーザーまたはエンティティのみが機密情報の表示、変更、削除を許可されます。
2. **未承認のアクションの防止**: 承認により、ユーザーは明示的に許可されているアクションのみを実行できるようになります。これにより、権限のないユーザーが悪意のあるアクションを実行したり、重要な操作を妨害したりすることが防止されます。
3. **プライバシー保護**: 個人情報や機密情報を保存するアプリケーションやシステムでは、オーソライズにより、許可された担当者のみがそのデータにアクセスして管理できるようになり、ユーザーのプライバシーが保護されます。
4. **リソース保護**: 承認は、ファイル、データベース、デバイス、サービスなどの貴重なリソースへの不正アクセスを防止するのに役立ちます。これらのリソースへの不正アクセスは、データ侵害、システム侵害、またはサービスの中断につながる可能性があります。
5. **コンプライアンスと規制要件**: 多くの業界や部門には、データ保護とアクセス制御に関して厳格なコンプライアンスと規制要件があります。適切な承認メカニズムは、組織がこれらの要件を満たし、法的結果を回避するのに役立ちます。
6. **ビジネス ロジックの適用**: 承認により、組織はアプリケーションまたはシステム内の特定の機能へのアクセスを制御することにより、ビジネス ルールとロジックを適用できます。
7. **侵害されたアカウントによる被害の制限**: アカウントが侵害された場合、適切な認証により攻撃者が実行できるアクションを制限することで被害を制限できます。
8. **マルチテナントのサポート**: マルチテナント環境では、承認により、各テナントが他のテナントのデータに干渉することなく、自分のデータとリソースのみにアクセスして管理できるようになります。
9. **スケーラビリティとユーザー管理**: オーソライズシステムにより、多数のユーザーおよびリソースにわたるユーザー アクセスの集中制御が可能になり、ユーザー管理とアクセス制御管理が簡素化されます。

全体として、組織のインフラストラクチャ内でデータとリソースの機密性、整合性、可用性を維持するには、承認が不可欠です。信頼されオーソライズされたエンティティのみが特定のリソースにアクセスし、その役割や権限に必要なアクションを実行できるようにすることが重要です。

## 認証とオーソライズの違い

アクセス コントロール リスト (ACL) について詳しく説明する前に、承認と認証の違いを理解することが重要です。認証は、ユーザーまたはシステムの身元を確認するプロセスです。これは通常、ユーザー名とパスワードを使用して行われますが、生体認証やその他の方法を使用することもできます。逆に、承認は、ユーザーまたはシステムがどのようなアクションを実行できるかを決定するプロセスです。オーソライズは多くの場合、ユーザーの役割またはグループのメンバーシップに基づいて行われます。

## 一般的な認証方法

ここでは、コンピューター システムや Web アプリケーションのリソースへのアクセスを制御するために使用される標準的な認証方法をいくつか紹介します。これらの方法は、承認されたユーザーまたはエンティティのみが特定のアクションを実行したり、特定の情報にアクセスしたりできるようにするのに役立ちます。

1. **Role-Based Access Control ロールベースのアクセス制御 (RBAC):** RBAC は、アクセス許可が特定のロールに割り当てられ、ユーザーが職務や責任に基づいてこれらのロールに割り当てられる、広く使用されている方法です。ユーザーは、関連付けられた役割に基づいてリソースにアクセスできるため、大規模な権限の管理が容易になります。
2. **Attribute-Based Access Control 属性ベースのアクセス制御 (ABAC):** ABAC は、アクセス制御の決定を行う際に、ユーザー、リソース、環境のさまざまな属性や特性を考慮する、よりきめ細かいオーソライズ方法です。これらの属性には、ユーザーの役割、場所、アクセス時間、その他のユーザー定義要素を含めることができます。
3. **Discretionary Access Control 制限なしのアクセス制御 (DAC):** DAC は、各リソース所有者が自分のリソースにアクセスできるユーザーとそのアクセス レベルを決定できるシンプルな承認モデルです。このアプローチにより、ユーザーはファイルやディレクトリへのアクセスをきめ細かく制御できるようになります。
4. **Mandatory Access Control 必須アクセス制御 (MAC):** MAC は、高セキュリティ環境でよく使用される、より厳格な認証モデルです。アクセスの決定は管理者が定義したシステムレベルのポリシーに基づいており、ユーザーはアクセス許可を変更できません。このモデルは通常、政府や軍事施設で見られます。
5. **Rule-Based Access Control ルールベースのアクセス制御:**この方法では、if-then ステートメントを使用してアクセス制御ルールを明示的に定義します。これらのルールは、どのユーザーまたはエンティティが特定のリソースまたはアクションにアクセスできるかを決定します。
6. **XML Access Control Markup LanguageXMLベースのマークアップのアクセス制御 (XACML):** XACML は、ABAC 原則を使用して属性に基づいてアクセス制御ポリシーを定義するオーソライズ標準です。これは、複雑なアクセス制御の決定を表現するための標準化された方法を提供します。
7. **OAuth:** OAuth は、ユーザーの資格情報を共有せずに、サードパーティのアプリケーションにサーバー上のユーザーのリソースへの制限付きアクセスを許可するために広く使用されている承認フレームワークです。これは、最新の Web アプリケーションやモバイル アプリケーションでの認証によく使用されます。
8. **OpenID Connect:** OpenID Connect は、OAuth 2.0 上に構築された認証およびオーソライズプロトコルです。これにより、アプリケーションはユーザー認証を ID プロバイダーに委任しながら、ユーザーを認証し、基本的なプロファイル情報を取得できるようになります。
9. **JSON Web Tokens (JWT):** JWT は、当事者間の承認情報を JSON オブジェクトとして表現するコンパクトで自己完結型の方法です。これは、ステートレスな認証とオーソライズのために最新の Web アプリケーションでよく使用されます。
10. **生体認証:**この方法では、生体特徴 (指紋、顔認識など) を使用して、特定のリソースまたはアクションへのアクセスを許可します。

使用される認証方法は、システムまたはアプリケーションの特定の要件とセキュリティのニーズに応じて異なる場合があることに注意することが重要です。

## ACLとは何ですか?

アクセス制御リスト (ACL) は、随意アクセス制御 (DAC) モデルのより具体的な実装であり、各リソースに関連付けられたルールのリストに基づいてアクセス許可が付与または拒否されます。

ACL では、各リソース (ファイル、ディレクトリ、ネットワーク デバイスなど) に、ユーザーまたはグループとその特定のリソースへのアクセス レベルを指定する関連リストがあります。通常、アクセス レベルには、読み取り、書き込み、実行、削除などの権限が含まれます。

## ACL を使用して MQTT メッセージングへのアクセスを制御する

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt) (メッセージ キュー テレメトリ トランスポート) のコンテキストでは、アクセス コントロール リスト (ACL) を使用して、 [MQTT ブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)内のさまざまなトピックやアクションへのアクセスを制御します。MQTT は、モノのインターネット (IoT) アプリケーションやその他のメッセージング シナリオで一般的に使用される軽量のメッセージング プロトコルです。MQTT は、従来のクライアント/サーバー モデルとは異なるパブリッシュ/サブスクライブ モデルを使用します。メッセージを送信するクライアント (パブリッシャー) とメッセージを受信するクライアント (サブスクライバー) が分離され、パブリッシャーとサブスクライバーの間に直接接続を構築する必要はありません。

![MQTT Publish-subscribe Architecture](https://assets.emqx.com/images/b9575ac3d6916dc629c12aa2de5ce5c3.png)

<center>EMQX MQTT ブローカーを使用したパブリッシャー/サブスクライバー モデルの例</center>

MQTT ブローカーは ACL を使用してセキュリティを強化し、定義されたルールに基づいて特定のトピックへのアクセスを制限します。ACL は、どのクライアントが特定のトピックへのメッセージのパブリッシュを許可されるか、またどのクライアントが特定のトピックへのサブスクライブを許可されるかを定義します。ACL を構成することにより、MQTT ブローカーは、許可されたデバイスまたはクライアントのみが特定のトピックをパブリッシュおよびサブスクライブできるようにし、制御された通信環境を提供することができます。

### MQTT ACL の一般的なコンポーネント

1. **トピック パターン**: [MQTT トピック](https://www.emqx.com/ja/blog/advanced-features-of-mqtt-topics)名は階層的に編成されており、ACL はワイルドカードを利用して複数のトピックを照合するためのパターンを定義できます。MQTT で使用される 2 つの主なワイルドカードは、プラス記号 (+) とハッシュ記号 (#) です。プラス記号は階層内の単一レベルを表し、ハッシュ記号は任意の数のレベル (ゼロ レベルを含む) を表します。
2. **クライアント識別子**:ブローカーに接続する[MQTT クライアントは、一意のクライアント識別子によって識別されます。](https://www.emqx.com/ja/blog/mqtt-client-tools)ACL はこれらの識別子を使用して、どのクライアントが特定のアクションを実行できるかを決定できます。
3. **アクション許可**: MQTT ACL は、特定のトピックに関して各クライアントに許可されるアクションを指定します。アクションには、PUBLISH (メッセージの送信) 権限と SUBSCRIBE (メッセージの受信) 権限を含めることができます。

### MQTT ACL ルールの例

1. 識別子「sensor001」を持つ特定のクライアントがトピック「センサー/温度」に関するメッセージを公開できるようにします。

   ```
   allow client sensor001 to publish to sensors/temperature
   ```

2. すべてのクライアントが「センサー」階層の下のトピックにサブスクライブできるようにします。

   ```
   allow all clients to subscribe to sensors/#
   ```

3. 識別子「guest123」を持つ特定のクライアントがトピックにサブスクライブすることを拒否します。

   ```
   deny client guest123 to subscribe to #
   ```

## まとめ

アクセス制御リスト (ACL) は、IoT システムにとって重要です。これらは、リソースへのアクセスを制御し、認証および許可されたユーザーのみが制限されたデータにアクセスできるようにする方法を提供します。MQTT ブローカーは ACL の実装が異なる場合があり、ACL 設定の正確な構文と機能は MQTT ブローカー ソフトウェアごとに異なる可能性があることに注意することが重要です。

MQTT ACL を適切に構成することは、セキュリティを維持し、MQTT 通信の安全性を確保し、許可された参加者に限定するために重要です。

EMQX が IoT インフラストラクチャのセキュリティ保護にどのように役立つかを引き続き調査してください。

- [EMQX アクセス制御の概要](https://www.emqx.io/docs/en/v5.0/access-control/overview.html)
- [EMQX Cloud を使用した Redis および JWT 認証および ACL メソッド](https://www.emqx.com/en/blog/emqx-cloud-redis-and-jwt-authentication-authorization)

EMQX の詳細については、[ドキュメント](https://www.emqx.io/docs/en/v5.0/)、[GitHub](https://github.com/emqx/emqx)、[Slack チャネル](https://slack-invite.emqx.io/)、および[フォーラム](https://www.emqx.io/forum/)を確認してください。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>