## OPC UAプロトコルとは

OPC UA（OPC Unified Architecture）は、プラットフォームに依存しない、サービス指向の、オープンで安全な通信アーキテクチャです。異なるベンダーの産業用オートメーションデバイス、システム、およびソフトウェアアプリケーションの相互運用性を実現するように設計されています。OPC UA情報モデルは、さまざまなトランスポートプロトコルを使用してデータを交換するためのコードとフォーマットを定義します。

OPC UAとその前身であるOpen Platform Communications（OPC）は、同じ財団によって開発されましたが、大きく異なります。財団は、元のOPC通信よりも望ましいアーキテクチャを作成し、進化する産業オートメーションのニーズにより合致するようOPC UAの開発を続けています。

## OPC UAプロトコルの歴史

![OPC UA](https://assets.emqx.com/images/f4582b4676a6867f6beefa40c055fae2.png)

OPC UA仕様のリリース前には、業界のベンダー、エンドユーザー、ソフトウェア開発者が協力して、産業プロセスデータ、アラーム、および履歴データを定義するための仕様セットを開発しました。この仕様セットはOPC Classicとして知られており、1995年に最初にリリースされ、Microsoft WindowsのCOM/DCOM技術スタックに基づいています。これには以下の3つの部分が含まれます：

1. OPCデータアクセスは、OPC DAとして最もよく知られています。OPC DA仕様は、値、時間、および品質情報を含むデータの交換を定義します。
2. OPCアラーム＆イベント、またはOPC A＆E、OPC A＆E仕様は、アラームおよびイベントタイプのメッセージ情報の交換、および変数の状態と状態の管理を定義します。
3. OPC履歴データアクセス、すなわちOPC HAD、OPC HDA仕様は、履歴および時間データのクエリと分析に適用できる方法を定義します。

OPC Classicは、プロセス制御において優れたパフォーマンスで知られています。しかし、技術の進歩と外部要因の変化により、もはや人々のニーズを完全に満たすことはできなくなりました。この問題に対処するため、OPC財団は2006年にOPC UAを導入しました。この新技術は、クロスプラットフォームのデータ転送、改善されたデータセキュリティ、および大量データのより良い処理を提供します。OPC UAは、既存のOPC Classic仕様のすべての機能を統合し、OPC Classicに存在した問題を解決しています。

現在、OPC UAの最新バージョンは1.05です。クライアントサーバーモデル（サブスクリプション）に加えて、OPC UAにはPub-Subメカニズムが含まれており、UDPプロトコル、[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)、または[AMQPプロトコル](https://www.emqx.com/en/blog/mqtt-vs-amqp-for-iot-communications)を使用してJSON仕様（標準定義のバイナリ仕様 - UADPも使用）をプッシュすることができます。

## OPC UAプロトコルの特徴

**機能の等価性:** すべてのOPC Classic仕様はUAにマッピングされ、OPC UAにはOPC Classicで見つかったDA、A＆E、およびHDAの機能が含まれます：

| **機能**           | **説明**                                                     |
| :----------------- | :----------------------------------------------------------- |
| 発見               | ローカルPCおよび/またはネットワーク上で利用可能なOPCサーバーを見つけます |
| アドレス空間       | すべてのデータは階層的に表されます（例：ファイルとフォルダー）、これによりOPCクライアントは、シンプルおよび複雑なデータ構造を発見して利用できます |
| オンデマンド       | アクセス権に基づいてデータ/情報を読み書きします              |
| サブスクリプション | データ/情報を監視し、クライアントの設定を超える値が変更された場合に例外を報告します |
| イベント           | 重要な情報をクライアントベースの設定で通知します             |
| メソッド           | クライアントは、サーバー上で定義されたメソッドに基づいてプログラムを実行できます等 |

**プラットフォームの独立性:** 埋め込みマイクロコントローラからクラウドベースのインフラまで、OPC UAはWindowsプラットフォームに依存せず、任意のプラットフォームでの使用に適しています。

**セキュリティ:** メッセージの暗号化、認証、および監査、組織が技術標準を選択する際に最も重要な考慮事項の1つはセキュリティです。OPC UAは、ファイアウォールを通過する際の一連の制御を提供することによってセキュリティに対処します：

| **機能**                   | **説明**                                                     |
| :------------------------- | :----------------------------------------------------------- |
| トランスポート             | 超高速OPCバイナリ転送などのオプションを提供するいくつかのプロトコルが定義されています |
| セッションの暗号化         | 情報は128ビットまたは256ビットの暗号化レベルで安全に送信されます |
| メッセージ署名             | メッセージが送信されたときと同じでなければならない署名       |
| シーケンスデータパッケージ | シーケンスにより特定されたメッセージリプレイ攻撃を排除       |
| 認証                       | 各UAクライアントとサーバーは、アプリケーションとシステムが互いに接続する方法を制御するOpenSSL証明書によって識別されます |
| ユーザーコントロール       | アプリケーションはユーザー認証（ログイン認証情報、証明書など）を要求でき、さらにユーザーアクセスを権限とアドレススペースの「ビュー」に制限または拡張できます |
| 監査                       | アクセス監査のためのユーザーおよび/またはシステム活動の記録  |

**拡張性:** OPC UAのマルチレイヤーアーキテクチャにより、新しいトランスポートプロトコル、セキュリティアルゴリズム、コーディング標準、およびアプリケーションサービスなどの革新的な技術とアプローチを組み込むことが可能になりますが、既存のアプリケーションに影響を与えません。新しい機能を追加するこの能力により、OPC UAは「未来に対応する」フレームワークとなります。同時に、OPC UAは既存の製品との互換性を維持します。これは、今日のUA製品が将来のUA製品と相互運用可能であることを意味します。

**包括的な情報モデリング:** 複雑な情報を定義するために使用されるOPC UA情報モデリングフレームワークは、データを情報に変換し、最も複雑なマルチレベル構造でさえもモデル化し、完全にオブジェクト指向の機能を介して拡張できるようにします。データタイプと構造は設定ファイルで定義されます。

![OPC UA Information Modelling Framework](https://assets.emqx.com/images/1161f4a8f02d771efa813f234c8515a9.png)

## OPC UAプロトコルの使用

OPC UAは、産業オートメーションとIoTの幅広いアプリケーションで使用され、異なる業界に多くの利点をもたらします。これには、データ収集、デバイス統合、リモートモニタリング、履歴データアクセスなどが含まれます。

### 製造業

- データ収集と監視: 製造業の設備と生産ラインは、OPC UAを介して簡単にデータを収集し、生産プロセスをリアルタイムで監視し、生産性を最適化することができます。
- デバイス統合と相互運用性: 異なるメーカーが製造したデバイスは、センサーからロボットまで、シームレスに統合され、デバイス間のデータ交換を可能にします。

### ビルディングオートメーション

- インテリジェントビルディング管理: OPC UAは、照明、空調、およびセキュリティシステムなどのビルオートメーションシステムを接続するために使用され、インテリジェントなエネルギー管理と機器制御を実現します。
- 設備監視と保守: OPC UAを通じてビル設備の状態監視と保守を実現し、設備の信頼性と効率を向上させます。

### 石油・ガス

- リモート監視と制御: OPC UAを介して、油田、パイプライン、精製所の設備をリモートで監視および制御し、手動介入を減らします。
- データ履歴: OPC UAの履歴データアクセス機能は、設備の運転データを記録し、分析および最適化を容易にするために使用されます。

### 再生可能エネルギー

- 風力および太陽光発電所: OPC UAは、風力および太陽光発電所の運転状況を監視し、リモート制御およびトラブルシューティングを実現するために使用されます。
- グリッド管理: 再生可能エネルギーのアクセスおよびグリッド管理にはリアルタイムのデータ交換が必要であり、OPC UAは信頼性の高い通信メカニズムを提供します。

### ユーティリティ

- 水処理および給水システム: OPC UAは、水処理設備、ポンプステーション、および給水システムを監視し、安定した水質と供給を確保するために使用されます。
- 電力システム: 電力設備の監視、故障検出、およびリモート操作は、OPC UAを使用して実現できます。

## OPC UAプロトコルの情報モデル

OPC UA情報モデルは、ノードと参照で構成される構造化グラフ、またはノードのネットワークであり、これをOPC UAアドレス空間と呼びます。アドレス空間は、標準形式のオブジェクトを表します - アドレス空間のモデル要素はノードと呼ばれ、オブジェクトとそのコンポーネントはアドレス空間内でノードのコレクションとして表され、属性によって説明され、参照によって接続されます。OPC UAのモデリングは、ノードを作成し、ノード間の参照を作成することについてです。

### オブジェクトモデル

OPC UAは、プロセスシステム内のデータとアクティビティを表すためにオブジェクトを使用します。オブジェクトには、参照によって相互接続された変数、イベント、およびメソッドが含まれます。

![OPC UA Object Model](https://assets.emqx.com/images/313bb04eebc2beaacc6c359eba0e17d8.png)

### ノードモデル

![OPC UA Node Model](https://assets.emqx.com/images/185c6a8d55d470c5e558bd3afd76a0ca.png)

- 属性はノードを記述するために使用され、異なるノードクラスには異なる属性（属性のセット）があります。ノードクラスの定義には属性の定義が含まれるため、属性はアドレス空間に含まれません。

- 参照はノード間の関係を表します。参照は、アドレス空間に存在する参照タイプのノードのインスタンスとして定義されます。

- ノードモデルの一般的なプロパティ

  ![Generic properties of the node model](https://assets.emqx.com/images/21e683edc5e34b7e2da17b662b99a421.png)

### 参照モデル

参照を含むノードはソースノードと呼ばれ、参照されるノードはターゲットノードと呼ばれます。参照されるターゲットノードは、ソースノードと同じアドレス空間にある場合もあれば、別のOPCサーバーのアドレス空間にある場合もあります。また、ターゲットノードが存在しない場合もあります。

![OPC UA Reference Model](https://assets.emqx.com/images/3b484967bea36515325de244dda332bd.png)

### ノードタイプ

OPC UAで最も重要なノードカテゴリーは、オブジェクト、変数、およびメソッドです。

- オブジェクトノード：オブジェクトノードはアドレス空間を形成するために使用され、データを含みません。オブジェクトの値を公開するために変数を使用します。オブジェクトノードは、管理オブジェクト、変数、またはメソッドをグループ化するために使用できます（変数とメソッドは常にオブジェクトに属します）。
- 変数ノード：変数ノードは値を表します。値のデータタイプは変数に依存します。クライアントは値を読み取り、書き込み、サブスクライブすることができます。
- メソッドノード：メソッドノードは、クライアントが呼び出し、結果を返すサーバー内のメソッドを表します。入力パラメータと出力結果は、メソッドノードの一部として変数の形であります。クライアントは入力パラメータを指定し、呼び出し後に出力結果を取得します。

## OPC UAプロトコルの動作原理

ハードウェアプロバイダーは、デバイスにOPC UAサーバーを組み込むか、プライベートプロトコルを介してPC上のソフトウェアでデータを取得し、他のプラットフォームにOPC UA経由で公開することによって、2つの方法でOPC UAをサポートします。一部の中間および高級PLCでは、Siemens S71200/1500などのOPC UAサーバー統合がありますが、SiemensはWINCCのようなソフトウェアも提供しており、他のデバイスからのデータを間接的に第三者に提供します。

![opc ua client and server](https://assets.emqx.com/images/e9398279706d0e493388a5c60fede41f.png)

データがOPC UAサーバーを介して公開されると、OPC UAプロトコルによって指定された2つのアクセスモードを使用してアクセスできます：リクエスト/レスポンスモードとパブリッシュ/サブスクライブモード。まず、クライアントはサーバーに接続する必要があります。これにより、クライアントとサーバーの間にセッションチャネルが作成されます。

リクエエスト/レスポンスモードでは、クライアントアプリケーションはセッションチャネルを介してサーバーにいくつかの標準サービスを要求できます。例えば、ノードからの生データの読み取り、ノードへのデータの書き込み、リモートメソッドの呼び出しなどです。

![request/response mode](https://assets.emqx.com/images/f7c47ebeb1f5da8bc6290b6b014b106e.png)

パブリッシュ/サブスクライブモードでは、各クライアントは任意の数のサーバーサブスクリプションを作成でき、サーバーのノードデータが変更されると、通知メッセージが即座にクライアントにプッシュされます。

![publish/subscribe mode](https://assets.emqx.com/images/16eedf2be88eb090746d9a7de6ad40e5.png)

通常、エンドユーザーは上記のプロセスについて心配する必要はありません。主な関心事は、OPC UAサーバーのアドレス、ユーザーログインポリシー、通信セキュリティポリシー、およびデータにアクセスできるアドレスです。

### OPC UAサーバーエンドポイント

| **プロトコル**    | **URL**                                |
| :---------------- | :------------------------------------- |
| OPC UA TCP        | `opc.tcp://localhost:4840/UADiscovery` |
| OPC UA Websockets | `opc.wss://localhost:443/UADiscovery`  |
| OPC UA HTTPS      | `https://localhost:443/UADiscovery`    |

### ユーザー認証方法

1. 匿名
2. ユーザー名＆パスワード
3. 証明書

### セキュリティモード

1. なし
2. 署名
3. 署名＆暗号化

### セキュリティポリシー

1. Basic128Rsa15
2. Basic256
3. Basic256Sha256
4. Aes128Sha256RsaOaep
5. Aes256Sha256RsaPass

### ノードアドレス

| **アドレスタイプ** | **アドレス** |
| :----------------- | :----------- |
| バイト文字列       | ns=x;b=      |
| GUID               | ns=x;g=      |
| 整数               | ns=x;i=x     |
| 文字列             | ns=x;s=      |

## OPC UAプロトコルとMQTTの活用

MQTT（Message Queuing Telemetry Transport）は、パブリッシュ/サブスクライブモデルを使用し、軽量、効率的、信頼性が高く、リアルタイム通信をサポートするIoTデバイスおよびアプリケーション向けのメッセージングプロトコルです。MQTTは、リソースが制約された環境に特に適しており、特に電力と帯域幅の使用を効率的にするシナリオで優れています。

産業界は、MQTT 3.1.1の上に産業IoTデータ仕様であるSparkplugBを構築しました。これは、基本的なデータ統一モデリング機能を提供すると同時に、柔軟性と効率を保証します。MQTTプロトコルの優れた設計のおかげで、SparkPlugBは良好なネットワーク状態認識を提供し、デバイスおよびシステム間で強力な相互運用性を提供します。

OPC UAとMQTTはある程度機能が重複していますが、使用シナリオは非常に異なります。

- **OPC UA**は、異なる機器やシステムが標準化された言語を使用してシームレスに通信できるようにする、産業シナリオで使用される通信プロトコルです。
- **MQTT**は、センサーのインターネットベースのデータ伝送に適しており、帯域幅が低く、ネットワーク条件が不安定な状況でも、リアルタイムデータの効率的な取り扱いを実現します。その読み取り/公開メカニズムは、使用上の類まれな柔軟性を提供します。

産業シナリオにおいて、MQTTは分散システムでのメッセージングに優れ、OPC UAは相互運用性を提供することに焦点を当てています。両方を組み合わせることで、ビジネスデータをOPC UAを使用して抽象化し集約し、MQTTを使用して分散された方法でこのデータをシームレスに交換することができ、強力な接続性を活用できます。

## OPC UA over MQTT

OPC財団がOPC UAの最新仕様で提案したPub-Subモデルでは、[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)を使用してデータ変更をサブスクライバーにプッシュすることが可能です。

![OPC UA over MQTT](https://assets.emqx.com/images/e3772239f0f42b2f622996c721d7e57f.png)

Pub-Subのセキュリティはクライアント/サーバーよりも少し複雑で、仕様は詳細ではありません。MQTTネットワークでは、セキュリティはSSL/TLSに基づいており、ブローカーはSSL/TLSをトランスポートに有効にすることに加えて、アプリケーションレベルで認証を定義できます。原則として、これらのセキュリティモデルは、ネットワークに参加できるすべてのサブスクライバーとパブリッシャーに対して全てまたは無しのものです。新しいOPC UAの標準化はまだ進行中であり、豊富なOPC UA情報モデルをMQTTに最適にマッピングする方法はまだ明確ではありません。

## EMQXおよびNeuronを使用してOPC UAプロトコルをMQTTにブリッジングする

[Neuron](https://github.com/emqx/neuron)は、標準プロトコルまたはデバイス固有のプロトコルを使用して幅広い産業デバイスに接続できる最新の産業用IoT接続サーバーです。Neuronは、リソースが限られたさまざまなIoTエッジハードウェアデバイスで動作するように設計された軽量の産業プロトコルゲートウェイソフトウェアであり、データ中心の自動化装置からのデータアクセスに関する課題を解決することを主な目的としています。

[EMQX](https://github.com/emqx/emqx) は、分散型の[オープンソースMQTTブローカー](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)です。世界で最もスケーラブルなMQTTメッセージングサーバーとして、EMQXは大量のIoTデバイスへの効率的で信頼性の高い接続を提供し、メッセージとイベントストリームの高性能でリアルタイムな移動と処理を可能にし、ビジネスクリティカルなIoTプラットフォームやアプリケーションの迅速な構築をユーザーに支援します。

Neuronの南向きOPC UAドライバーによって収集および集約されたOPC UAデータソースは、MQTTプロトコルに変換され、EMQX MQTTブローカーに伝送されます。後者はそれらをさまざまな分散アプリケーションに配布します。

OPC UAからMQTTへのブリッジングについては、次のステップバイステップガイドを参照してください：[IIoTのためのOPC UAデータをMQTTにブリッジングする：ステップバイステップチュートリアル](https://www.emqx.com/ja/blog/bridging-opc-ua-data-to-mqtt-for-iiot)。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
