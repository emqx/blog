## MQTTブローカーとは？

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、インターネット・オブ・シングス(IoT)の領域を支える軽量で効率的なプロトコルです。この記事では、通信を仲介する中央ハブ、つまりMQTTブローカーの機能を深掘りし、その実装の比較、使用例、特性、そしてベストプラクティスを詳細にレビューします。

MQTTブローカーとは、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)間で通信を可能にするための中間エンティティです。具体的には、MQTTブローカーは、クライアントから送信されたメッセージを受け取り、トピックごとにメッセージをフィルタリングし、サブスクライバーに配信します。

MQTTブローカーの活用により、パブリッシュ/サブスクライブ(pub/sub)通信モデルを効果的に実現することができます。これにより、MQTTは非常に効率的でスケーラブルなプロトコルとして機能します。

## なぜMQTTブローカーが重要ですか？

MQTTブローカーは、MQTTクライアント（パブリッシャーとサブスクライバー）間の通信を促進し、MQTTアーキテクチャの中心的な役割を果たします。MQTTブローカーの重要性は以下の要素に由来します：

- メッセージのルーティング：MQTTブローカーはパブリッシャーからメッセージを受け取り、それをトピックのサブスクリプションに基づいて適切なサブスクライバーにルーティングします。これにより、クライアント間の直接の接続が不要となり、メッセージの配信が効率的かつ正確に行われます。
- スケーラビリティ：MQTTブローカーは、大量の同時接続を処理する能力を持ちます。これは、IoTやM2M通信シナリオで数千から数百万のデバイスが存在する可能性がある状況で必要となる能力です。この接続とメッセージの管理能力により、MQTTプロトコルは効果的にスケールアップできます。
- セキュリティ：MQTTブローカーは認証や暗号化などのセキュリティ機能を提供し、IoTデバイスとアプリケーション間でデータの安全性を確保します。詳細はこちら：「[MQTTセキュリティについて知っておくべき7つの重要事項 2023](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security)」。
- 統合：MQTTブローカーは、他の通信プロトコルやクラウドプラットフォームと統合し、全体的なIoTソリューションを提供します。たとえば、MQTTブローカーは、AWS IoT、Google Cloud IoT、またはMicrosoft Azure IoT Hubと統合し、シームレスなIoTエコシステムを構築します。
- セッション管理：MQTTブローカーは、クライアントのサブスクリプション情報の維持や、クライアントがオンラインになったときに配信するために保存されるメッセージの管理など、クライアントのセッション管理を担当します。このセッション管理機能により、クライアントが接続を切断して後にブローカーに再接続しても、メッセージが失われることはありません。詳細はこちら：「[MQTT Persistent SessionとClean Sessionの説明](https://www.emqx.com/en/blog/mqtt-session)」。

## MQTTブローカーアーキテクチャの概要

MQTTブローカーアーキテクチャは、メッセージプロデューサー（パブリッシャー）とメッセージコンシューマー（サブスクライバー）を分離する[パブリッシュ/サブスクライブメッセージングパターン](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)に基づいています。このアーキテクチャは、クライアント、トピック、ブローカーの3つの主要コンポーネントから成り立ちます。

![MQTT Broker Architecture](https://assets.emqx.com/images/cf73c3b847af7b4743993c87f82942e1.png)

-  **MQTTブローカー・サーバー**

  MQTT ブローカーは、パブリッシャーからメッセージを受信し、トピックのサブスクリプションに基づいてサブスクライバーに配信するサーバーである。クライアント接続を管理し、サブスクリプションとアンサブスクリプションを処理し、指定された [QoS (Quality of Service) ](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)レベルに従ってメッセージ配信を保証する。

-  **MQTTクライアント**

  MQTT クライアントは、パブリッシャー、サブスクライバー、またはその両方になることができる。パブリッシャは MQTT ブローカにメッセージを送信し、サブスクライバはブローカからメッセージを受信する。クライアントは、IoT デバイス、モバイルアプリケーション、その他のサーバーなど、MQTT プロトコルを使用して MQTT ブローカーへの接続を確立できるデバイスまたはアプリケーションであれば何でもよい。

-  **トピックス**

  トピックはメッセージのサブジェクトやカテゴリを定義する階層的な文字列です。パブリッシャーがブローカーにメッセージを送信する際、特定のトピックに関連付ける。サブスクライバは、1 つまたは複数の [MQTT トピック](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics)をサブスクライブすることで、メッセージの受信に関心を示す。ブローカーは、トピックのサブスクリプションに基づいて、適切なサブスクライバーにメッセージをルーティングします。

MQTT ブローカー・アーキテクチャには、集中型と分散型がある。集中型アーキテクチャでは、単一のブローカーがクライアント間のすべての通信を処理する。分散アーキテクチャでは、複数のブローカーが連携してスケーラブルでフォールトトレラントなメッセージングインフラストラクチャを提供します。分散アーキテクチャの各ブローカーは、他のブローカーと協調してメッセージルーティングを管理し、メッセージが意図した受信者に確実に配信されるようにすることができます。

全体として、MQTTブローカー・アーキテクチャは、柔軟で効率的なメッセージング・インフラストラクチャを提供し、デバイスとアプリケーションのセキュアで効率的なスケールの通信を可能にします。

## 人気のオープンソースMQTTブローカー

### EMQX

[EMQX](https://www.emqx.io/)は現在、IoTアプリケーション向けの最もスケーラブルなMQTTブローカーである。ミリ秒以下のレイテンシーで1秒間に数百万のMQTTメッセージを処理し、単一のクラスタ内で1億以上のクライアント間のメッセージングを可能にする。EMQXはMQTT 5.0および3.xに準拠しており、分散IoTネットワークに最適で、クラウド、Microsoft Azure、Amazon Web Services、Google Cloud上で実行できる。このブローカーはTLS/SSL上でMQTTを実装でき、PSK、JWT、X.509などの認証メカニズムをサポートしている。Mosquittoとは異なり、EMQXはCLI、HTTP API、ダッシュボードによるクラスタリングをサポートしている。

<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

### Mosquitto

[Eclipse Mosquitto](https://github.com/eclipse/mosquitto)は、MQTTプロトコル・バージョン5.0、3.1.1、3.1に対応したオープンソースのMQTTブローカーです。Mosquittoは軽量で、低消費電力のシングルボードコンピュータやエンタープライズサーバーにインストールできる。ブローカーはCプログラミング言語で書かれており、Cライブラリを使ってMQTTクライアントに実装できる。Windows、Mac、Linux、Raspberry Pi用にダウンロードできる。すぐにインストール可能なバイナリファイルは、すべてのオペレーティング・システムで利用可能です。最新バージョンには、認証・認可プラグイン "mosquitto-go-auth "が含まれており、Mosquittoインスタンスを管理するためのウェブ・ユーザー・インターフェイスとなっている。また、PHPでMQTTクライアントを作成するためのPHPラッパー "Mosquitto-PHP "も提供されています。

### NanoMQ

[NanoMQ](https://nanomq.io/)はIoTエッジ向けに設計された軽量で高速なMQTTブローカーです。NanoMQは純粋なC言語で実装され、NNGの非同期I/Oとマルチスレッド・[アクター・モデル](https://en.wikipedia.org/wiki/Actor_model)をベースにしており、MQTT 3.1.1とMQTT 5.0のプロトコル・バージョンを完全にサポートしています。NanoMQはスタンドアロン・ブローカーとしては高性能です。魅力的な利点はその移植性です。どのようなPOSIX互換のプラットフォームにもデプロイでき、x86_64、ARM、MIPS、RISC-Vなどの異なるCPUアーキテクチャ上で動作します。

<section class="promotion">
    <div>
        NanoMQを無料で試す
    </div>
    <a href="https://www.emqx.com/ja/try?product=nanomq" class="button is-gradient px-5">スタートアップ →</a>
</section>

### VerneMQ

[VerneMQ](https://github.com/vernemq/vernemq)プロジェクトは2014年に発足し、当初は[Erlio GmbH](https://vernemq.com/company.html)によって開発された。Erlang/OTPで書かれた2番目のブローカーとして、このプロジェクトはApacheバージョン2.0でライセンスされ、EMQXプロジェクトから[いくつかのコード](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl)を借用している。アーキテクチャ設計に関しては、VerneMQはLevelDBでのMQTTメッセージの永続化をサポートし、[Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf)アルゴリズムを実装した[Plumtree](https://github.com/lasp-lang/plumtree)ライブラリに基づくクラスタリングアーキテクチャを使用している。

## MQTTブローカーを選ぶ方法と、評価プロセスをサポートするリソースについて説明します。

MQTTブローカーを選ぶ際のポイントや評価プロセスを支援するリソースについて、以下の記事が役立ちます。組織のニーズに合った最適なMQTTブローカーを選ぶために、ぜひ参考にしてください。

### 評価基準

- [**MQTTブローカー2023を選ぶ際に考慮すべき7つの要素**](https://www.emqx.com/en/blog/7-factors-to-consider-when-choosing-mqtt-broker-2023)

  2023年に完璧なMQTTブローカーをお探しですか？選択する前に、以下の7つの重要な要素を考慮してください。詳しくはガイドをお読みください。

### MQTTブローカーの比較

- [**2023年におけるオープンソースMQTTブローカーの包括的比較**](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)

  この記事では、2023年におけるオープンソースのトップMQTTブローカーを探り、顧客のニーズに最適なものを選ぶのに役立つよう、それらを徹底的に比較する。

- [**2023年の産業用IoT向けオープンソースMQTTブローカーのトップ3**](https://www.emqx.com/ja/blog/top-3-open-source-mqtt-brokers-for-industrial-iot-in-2023)

  この記事では、2023年のIIoT向けMQTTブローカーのトップ3を比較し、各ブローカーのメリット、デメリット、ユースケースを紹介する。

- [**EMQX vs Mosquitto｜2023年MQTTブローカーの比較**](https://www.emqx.com/ja/blog/emqx-vs-mosquitto-2023-mqtt-broker-comparison)

  2023年に人気のオープンソースMQTTブローカーとしてEMQXとMosquittoの違いをご覧ください。

- [**EMQX vs NanoMQ｜2023年MQTTブローカーの比較**](https://www.emqx.com/en/blog/emqx-vs-nanomq-2023-mqtt-broker-comparison)

  2023年のEMQXとNanoMQ MQTTブローカーを比較して、IoTプロジェクトに最適なものを選びましょう。拡張性、セキュリティ、信頼性については、ガイドをご覧ください。

- [**EMQX vs VerneMQ｜2023年MQTTブローカーの比較**](https://www.emqx.com/en/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison)

  EMQXとVerneMQのMQTTブローカーを包括的に分析し、IoTプロジェクトに適した選択をしましょう。

- [**MosquittoとNanoMQの比較｜2023 MQTTブローカーの比較**](https://www.emqx.com/en/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison)

  このブログ記事では、MosquittoとNanoMQをMQTTブローカーとして比較し、2023年のさまざまなユースケースに適したものを読者が判断するのに役立てます。

- [**人気のオンライン公開MQTTブローカーの評価**](https://www.emqx.com/en/blog/popular-online-public-mqtt-brokers)

  この記事では、いくつかの人気のある無料オンラインMQTTブローカーを整理し、選択する際の参考になれます。

### MQTTブローカーのベンチマークテスト

- [**オープンMQTTベンチマーク・スイート：MQTTパフォーマンス・テストのガイド**](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing)

  EMQによって提供されているOpen MQTTベンチマークスイートを紹介します。このベンチマークスイートにより、MQTTブローカーのスケーラビリティとパフォーマンスを偏見なく評価することができます。

- [**オープンMQTTベンチマーク比較：2023年のMQTTブローカー**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mqtt-brokers-in-2023)

  当社の網羅的なベンチマーク解析からあなたの理想のMQTTブローカーを見つけてください。今すぐベンチマークインサイトにアクセスできます

- [**オープンMQTTベンチマーク比較：MosquittoとNanoMQの比較**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mosquitto-vs-nanomq)

  この包括的な分析で、MosquittoとNanoMQのパフォーマンスをOpen MQTT Benchmarkingで比較してください。あなたのニーズに合ったMQTTブローカーを見つけましょう。

- [**オープンMQTTベンチマーク比較：EMQX vs NanoMQ**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-nanomq)

  Open MQTTベンチマークスイートのパフォーマンス結果から、適切なMQTTブローカーの選択を補助します。

- [**オープンMQTTベンチマーク比較：EMQXとMosquittoの比較**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-mosquitto)

  この包括的な分析で、EMQXとMosquittoのパフォーマンスをOpen MQTT Benchmarkingで比較する記事です。

- [**オープンMQTTベンチマーク比較：EMQX vs VerneMQ**](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-vernemq)

  この包括的な分析で、EMQXとVerneMQのパフォーマンスをOpen MQTT Benchmarkingで比較する記事です。

- [**EMQX 5.0による100M MQTT接続の実現**](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

  MQTTブローカーEMQXのスケーラビリティをストレステストするために、23台のEMQXノードのクラスタに100万のMQTT接続を確立し、EMQXのパフォーマンスを述べる記事です。

## MQTTブローカーをスタートすることに役立つリソース

- [**EMQX Cloudを始めよう：MQTTサービスを始める最も簡単な方法**](https://docs.emqx.com/en/cloud/latest/quick_start/introduction.html)

  このページでは、フルマネージドMQTTサービスであるEMQX Cloudのアカウント作成から、EMQX Cloudの機能や特徴について、ステップ・バイ・ステップでご紹介します。

- [**UbuntuにMQTTブローカーをインストールする方法**](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu)

  この記事ではEMQXを例に、Ubuntu上でシングルノードのMQTTブローカーを構築する方法を紹介する。

- [**EMQX MQTTブローカーのSSL/TLSを有効化する**](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)

  EMQX MQTTブローカーは複数のセキュリティ認証をサポートしています。この記事では、EMQXでMQTTのSSL/TLSを有効にする方法を紹介します。

###  MQTTブローカーの統合

- [**PrometheusとGrafanaでMQTTブローカーを監視する**](https://www.emqx.com/en/blog/emqx-prometheus-grafana)

  この記事では、EMQX 5.0の監視データをPrometheusに統合する方法、EMQXの監視データを表示するためにGrafanaを使用する方法を紹介し、最後にシンプルなMQTTブローカー監視システムを構築します。

- [**EMQX + ClickHouseがIoTデータ収集と分析を実装**](https://www.emqx.com/en/blog/emqx-and-clickhouse-for-iot-data-access-and-analysis)

  IoTデータ収集には大量の機器とデータが含まれるため、EMQX + ClickHouseはIoTデータへのアクセス、保存、分析、処理が完全に可能です。

- [**ThingsBoardでMQTTデータにアクセスする方法**](https://www.emqx.com/en/blog/how-to-use-thingsboard-to-access-mqtt-data)

  ここでは、ThingsBoard CloudとEMQX Cloudを組み合わせて使用し、サードパーティのMQTTブローカーをThingsBoardに統合してMQTTデータにアクセスする方法を説明します。

- [**Node-REDでMQTTデータを処理する**](https://www.emqx.com/en/blog/using-node-red-to-process-mqtt-data)

  今回は、Node-REDを使ってMQTTブローカーにアクセスし、MQTTデータを加工してからブローカーに送信するまでの操作手順を紹介した。

## EMQX: 世界で最もスケーラブルなMQTTブローカー

[EMQX](https://www.emqx.io/) は1.15万のスターを獲得している人気のMQTTブローカーの一つで、GitHub上にあるEMQXプロジェクトは2012年に立ち上げられ、Apache version 2.0のライセンス下にある。EMQXは大規模にスケーラブルなソフトリアルタイムシステムを構築するためのErlang/OTPプログラミング言語で書かれている。

EMQXはMQTT 5.0、MQTT-SN、[MQTT over QUIC](https://www.emqx.com/ja/blog/mqtt-over-quic)のような高度な機能をサポートする世界で最もスケーラブルなMQTTブローカーです。ハイアベイラビリティと水平方向スケーラビリティのためにマスタレスクラスタリングをサポートしています。最新版のEMQX 5.0は、23ノードのシングルクラスタで100万の同時MQTT接続を確立することができます

EMQXは豊富なエンタープライズ機能、データインテグレーション、クラウドホスティングサービス、[EMQ Technologies Inc.](https://www.emqx.com/ja)からの商用サポートを提供しています。年間を通じて高いパフォーマンス、信頼性、スケーラビリティのためにエンタープライズ、スタートアップ、個人の間で評判を得ています。特に、インダストリアルIoT、コネクテッドカー、製造業、通信業などの各種ビジネスクリティカルなアプリケーションで広く活用されています。





<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
