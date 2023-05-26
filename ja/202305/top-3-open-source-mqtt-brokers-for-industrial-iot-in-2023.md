MQTTは、当初は軽量の[パブリッシュ／サブスクライブ・メッセージング・プロトコル](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)として設計されましたが、現在では産業用IoT（IIoT）およびインダストリー4.0に不可欠になっています。その意義は、多様な産業機器とクラウドをシームレスに接続し、運用技術（OT）と情報技術（IT）の融合を可能にすることにある。


本記事では、2023年のIIoTに向けたMQTTブローカーのトップ3を、各ブローカーのメリット、デメリット、ユースケースを含めて比較します。また、これら3つのMQTTブローカーの機能を活用して、IIoTソリューションのUnified Namespace（UNS）アーキテクチャを構築する方法を紹介しています。

## 一目でわかる：3つの優れたプロジェクト

この2つの基準に基づき、産業用IoT向けの[オープンソースMQTTブローカー](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)の上位機種を選定しています：

- オープンソースプロジェクトのコミュニティ、人気、プロジェクト活動。
- リソースに制約のある産業用機器やゲートウェイとの親和性。

この基準に基づき、オープンソースのMQTTブローカーとして人気のある3つのブローカーを選びました：

- EMQX: GitHubで最もスターが多いMQTTブローカーで、11.4kスターを獲得しています。EMQXは50Mの起動フットプリントを持ち、クラスタリング機能をサポートしています。
- Mosquitto: MQTTブローカーの中で2番目に星が多いが、最も普及しているブローカーである。シングルスレッド・アーキテクチャの場合、Mosquittoの起動フットプリントは1M未満です。
- NanoMQ: 最新かつ最もアクティブなMQTTブローカーの1つです。マルチスレッドとasync-ioをサポートし、NanoMQは約2Mのスタートアップスペースを持っています。

GitHubでホストされている3つのプロジェクトの概要は以下の通りです：

|                                     | **EMQX**                                    | **Mosquitto**                                            | **NanoMQ**                                      |
| :---------------------------------- | :------------------------------------------ | :------------------------------------------------------- | :---------------------------------------------- |
| **Official Website**                | [EMQX](https://www.emqx.io/)                | [Eclipse Mosquitto](https://mosquitto.org/)              | [NanoMQ](https://nanomq.io/)                    |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) | [NanoMQ GitHub](https://github.com/emqx/nanomq) |
| **Project Created**                 | 2012                                        | 2009                                                     | 2020                                            |
| **License**                         | Apache License 2.0                          | EPL/EDL License                                          | MIT License                                     |
| **Programming Language**            | Erlang                                      | C/C++                                                    | C                                               |
| **Latest Release**                  | v5.0.23 (April 2023)                        | 2.0.15 (Aug 2022)                                        | v0.17.0 (March 2023)                            |
| **GitHub Stars**                    | **11.5k**                                   | **7.2k**                                                 | **800+**                                        |
| **GitHub Releases**                 | 260+                                        | 60+                                                      | 75+                                             |
| **GitHub Commits**                  | 14k+                                        | 2800+                                                    | 2000+                                           |
| **GitHub Commits (Last 12 Months)** | **3000+**                                   | **500+**                                                 | **1200+**                                       |
| **GitHub PRs**                      | 6000+                                       | 600                                                      | 780+                                            |
| **GitHub Contributors**             | 100+                                        | 110+                                                     | 20+                                             |

## 1. EMQX

[EMQX](https://www.emqx.io/)は、企業のIIoT展開のための高度にスケーラブルな分散型MQTTブローカーです。MQTT 5.0、MQTT-SN、SSL/TLS暗号化、[MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)を幅広くサポートしています。さらに、マスターレスクラスタリングにより、高可用性と水平スケーラビリティを実現します。

EMQXはGitHubで11.5kのスターを獲得しており、[最も人気のあるMQTTブローカー](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)の1つとしての地位を確立しています。EMQXプロジェクトは2012年に開始され、Apacheバージョン2.0の下でライセンスされています。EMQXは、大規模なスケーラブルソフトリアルタイムシステムを構築するためのプログラミング言語であるErlang/OTPで書かれています。

EMQXは、クラウドとエッジでの展開に適しています。エッジでは、[N3uron](https://n3uron.com/)、[Neuron](https://neugates.io/)、[Kepware](https://www.ptc.com/en/products/kepware)など、さまざまな産業用ゲートウェイと統合することができます。クラウド環境では、EMQXはAWS、GCP、Azureなどの主要なパブリッククラウドプラットフォーム上でKafka、データベース、クラウドサービスなど、さまざまなテクノロジーとシームレスに統合することが可能です。

エンタープライズグレードの包括的な機能、データ統合機能、クラウドホスティングサービス、[EMQ Technologies Inc](https://www.emqx.com/en)の商用サポートにより、EMQXはIIoT領域のミッションクリティカルアプリケーションに広く利用されています。ユースケースで詳しく見る

![EMQX MQTT Cluster](https://assets.emqx.com/images/5063b00be9fc0e46ee1431793dc33d24.png)

### メリット

- マスターレスクラスタリングと高可用性
- 高性能・低遅延
- 豊富な認証機構
- エッジ・トゥ・クラウドの展開
- [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)の先駆け。

### デメリット

- 設定や構成が複雑
- CPU/Memの使用率が高い

### 使用例

- 自動車製造
- 製鉄・鉄鋼業
- オイル＆ガス
- 半導体製造
- の供給

## 2. Mosquitto

[Mosquitto](https://mosquitto.org/)は、Eclipse Public License（EPL/EDLライセンス）のもとでライセンスされた、Eclipse Foundationのもとで広く使われているオープンソースのMQTTブローカーです。2023年3月現在、GitHubで7k以上のスターを獲得しています。MQTTプロトコルバージョン5.0、3.1.1、3.1を実装しており、SSL/TLSとWebSocketをサポートしています。

MosquittoはC/C++で記述され、シングルスレッド・アーキテクチャを採用しています。軽量設計のため、Mosquittoはリソースが限られた組み込み機器や産業用ゲートウェイへの導入に適しています。Mosquittoはクロスプラットフォームであり、Linux、Windows、macOSなど、さまざまなプラットフォームで実行することができます。

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

### メリット

- 軽量でフットプリントが小さい
- シンプルで使い勝手が良い

### デメリット

- マルチスレッドおよびクラスタリングサポートなし
- クラウドへの展開に適さない

### 使用例

- ファクトリーオートメーション
- スマートマニュファクチャリング
- Smart Hardware

## 3. NanoMQ

[NanoMQ](https://nanomq.io/) は、2020年にリリースされた最新のオープンソースのMQTTブローカープロジェクトです。NanoMQは、NNGの非同期I/Oとマルチスレッ[ドアクターモデル](https://en.wikipedia.org/wiki/Actor_model)に基づき、ピュアCで実装されています。MQTTバージョン3.1.1および5.0、SSL/TLS、MQTT over QUICを完全にサポートしています。

NanoMQの際立った特徴の1つは、最小限のメモリフットプリントで軽量かつ高速であることです。このため、効率とリソースの最適化が最も重要なIIoTアプリケーションのための優れたMQTTブローカーとなります。さらに、NanoMQは、DDS、NNG、ZeroMQなどのプロトコルをMQTTに変換し、MQTTメッセージをクラウドに橋渡しするメッセージングゲートウェイとして機能することができます。

NanoMQは、ネイティブのPOSIX APIのみに依存し、高い互換性と移植性を持っています。このため、POSIX互換のプラットフォームへの導入が容易で、x86_64、ARM、MIPS、RISC-Vなど様々なCPUアーキテクチャ上でスムーズに動作します。

![NanoMQ MQTT Broker](https://assets.emqx.com/images/44a45e8732eef0076a95f095f6551d2e.png)

### メリット

- マルチスレッドと非同期IO
- 小さなブートフットプリント
- ブローカーレスプロトコルによるブリッジング

### デメリット

- プロジェクトは初期段階
- クラスタリングサポートなし

### 使用例

- オートモーティブ・マニュファクチャリング
- ロボティクス：エッジサービスコンバージェンス
-  IIoTエッジゲートウェイ

## サイドバイサイドの比較

次のグラフは、オープンソースのMQTTブローカー上位3社を並べて比較したものです：



|                       | **EMQX**                         | **Mosquitto**  | **NanoMQ**                                           |
| :-------------------- | :------------------------------- | :------------- | :--------------------------------------------------- |
| **Protocols**         | MQTT 5.0/3.1.1<br>MQTT over QUIC | MQTT 5.0/3.1.1 | MQTT 5.0/3.1.1<br>MQTT over QUIC<br>ZeroMQ & NanoMSG |
| **Scalability**       | Excellent                        | Moderate       | Good                                                 |
| **Availability**      | Excellent                        | Moderate       | Moderate                                             |
| **Performance**       | Excellent                        | Good           | Excellent                                            |
| **Latency**           | Excellent                        | Good           | Excellent                                            |
| **Reliability**       | High                             | High           | High                                                 |
| **Security**          | Excellent                        | Excellent      | Good                                                 |
| **Integrations**      | Excellent                        | Moderate       | Moderate                                             |
| **Compatibility**     | Good                             | Excellent      | Excellent                                            |
| **Ease of Use**       | Good                             | Excellent      | Good                                                 |
| **Community Support** | Excellent                        | Excellent      | Excellent                                            |

## IIoTプロジェクトにおけるブローカー導入の最適化

Unified Namespace（UNS）は、産業用IoTおよびインダストリー4.0向けのMQTTブローカーをベースに構築されたソリューションアーキテクチャーです。[MQTTトピック](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics)の統一ネームスペースと、メッセージや構造化データの一元的なリポジトリを提供します。

3つのMQTTブローカーが連携して、UNSアーキテクチャを構築することができます。産業用ゲートウェイにMosquittoとNanoMQを導入しつつ、クラウドに集中型ハブとしてEMQXを導入することで、まとまりのあるシステムを構築することができます。この構成により、エッジからクラウドまで、MQTTブリッジを介してIIoTデータのシームレスな集約と取り込みが可能になります。

![MQTT Unified Namespace](https://assets.emqx.com/images/f7031dc2592e6a32a061b78378821086.png)

## 結論

これまでの紹介と比較から、各MQTTブローカーは異なる展開シナリオに対して明確な強みを提供することができます。  [EMQX](https://www.emqx.io/) は、エンタープライズ向けの機能で拡張性が高く、クラウド展開に適しています。 [Mosquitto](https://mosquitto.org/)と[NanoMQ](https://nanomq.io/)は、高速かつ軽量で、産業用ゲートウェイに最適です。


これら3つのMQTTブローカーは、産業用IoTアプリケーションにおいて重要な役割を果たし、UNSアーキテクチャの実装を先導し、ITとOTドメインの融合を促進する。具体的なIIoTプロジェクトを検討する際には、要件に応じてこれらのMQTTブローカーのうち1つまたは2つを選択することができます。それぞれの強みを生かすことで、MQTTブローカーが連携し、それぞれの能力を相乗的に発揮する、まとまったシステムを構築することができます。
