## はじめに

MQTT（Message Queuing Telemetry Transport）は、IoT（Internet of Things）のデファクトスタンダードなメッセージングプロトコルである。IoTの発展に伴い、[MQTTブローカー](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)はIoT機器の接続や、接続された機器とクラウドサービス間のデータ移動に不可欠になっています。

[EMQX](https://github.com/emqx/emqx)と[Mosquitto](https://mosquitto.org/)は、最も人気のあるオープンソースのMQTTブローカーの2つです。EMQXは、拡張性の高い分散型MQTTブローカーで、クラスタリングをサポートしています。Mosquittoは、フットプリントが小さく、シングルスレッド・アーキテクチャの軽量なMQTTブローカーです。

このブログ記事では、2023年の2つのブローカーを詳細に比較します。

## Mosquittoの概要

Mosquittoプロジェクトは、2009年にRoger Lightによって最初に開発され、その後Eclipse Foundationに寄贈され、Eclipse Public License（EPL/EDLライセンス）の下でライセンスされています。世界で最も広く使われているMQTTブローカーの1つとして、Mosquittoは2023年3月現在で7k以上のGitHubスターを持っています。

MosquittoはC/C++で書かれており、シングルスレッド・アーキテクチャを使用しています。MosquittoはMQTTプロトコルバージョン5.0、3.1.1、3.1を実装し、SSL/TLSとWebSocketをサポートしています。軽量設計のため、Mosquittoは組み込み機器やリソースの限られたサーバーへの導入に適しています。

![Mosquitto](https://assets.emqx.com/images/82027ea30acf44e5e1ba3e0a68f8bd4f.png)

 **長所です：**

- 簡単な設定と使用方法
-  MQTT 5.0プロトコル対応
-  軽量で効率的
-  積極的なコミュニティサポート

 **Cons：**

- 拡張性が低い（10万人未満）
-  クラスタリングサポートなし
-  エンタープライズ向け機能を欠く
-  Cloud-Nativeのサポートは限定的です。

## EMQXの概要

EMQXプロジェクトは2012年にGitHubで開始され、Apacheバージョン2.0の下でライセンスされています。EMQXは現在、MQTT 5.0、MQTT-SN、MQTT over QUICなどの先進機能をサポートする、世界で最もスケーラブルなMQTTメッセージングサーバーです。IoT、産業用IoT（IIoT）、車両インターネット（IoV）のビジネスクリティカルなアプリケーションで広く利用されています。

EMQXは、大規模スケーラブルなソフトリアルタイムシステムを構築するためのプログラミング言語であるErlang/OTPで書かれています。EMQXは、Mosquittoとは異なり、設立当初からマスターレス分散アーキテクチャを採用し、高可用性と水平スケーラビリティを実現しています。最新版のEMQX 5.0では、23ノードの単一クラスターで1億の同時MQTT接続を確立する規模となっています。

ご覧ください：[EMQX 5.0による100M MQTT接続の達成](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

![EMQX](https://assets.emqx.com/images/c0ef403f8b9207ebffa1bf228bc7f3a7.png)

 **長所です：**

- 大規模なデプロイメントに対応
-  高可用性
-  水平方向のスケーラビリティ
-  高性能・高信頼性
-  豊富なエンタープライズ機能
-  MQTT over QUICの先駆け。

 **Cons：**

- 設定や構成が複雑
-  効果的なマネジメントが難しい
-  ログが乱れる場合があります

##  コミュニティとポピュラリティ

[EMQX](https://github.com/emqx/emqx)はGitHubで最も評価が高く、最もアクティブなMQTT Brokerプロジェクトで、過去12ヶ月で11.4スター、3,000以上のコミットが行われています。

[Mosquitto](https://github.com/eclipse/mosquitto)は、軽量なシングルスレッドアーキテクチャを持つEMQXよりも、特にリソースの限られた組込み機器での導入が進んでいるようです。

|                                     | **EMQX**                                    | **Mosquitto**                                            |
| :---------------------------------- | :------------------------------------------ | :------------------------------------------------------- |
| **GitHub Project**                  | [EMQX GitHub](https://github.com/emqx/emqx) | [Mosquitto GitHub](https://github.com/eclipse/mosquitto) |
| **Project Created**                 | 2012                                        | 2009                                                     |
| **License**                         | Apache License 2.0                          | EPL/EDL License                                          |
| **Programming Language**            | Erlang                                      | C                                                        |
| **Latest Release**                  | v5.0.21 (March 2023)                        | 2.0.15 (Aug 2022)                                        |
| **GitHub Stars**                    | 11.4k                                       | 7.2 k                                                    |
| **GitHub Forks**                    | 2k                                          | 2.1k                                                     |
| **GitHub Commits**                  | 14k+                                        | 2.8k+                                                    |
| **GitHub Commits (Last 12 Months)** | 3000+                                       | 500+                                                     |
| **GitHub Issues**                   | 3500+                                       | 2200+                                                    |
| **GitHub Releases**                 | 260+                                        | 60+                                                      |
| **GitHub PRs**                      | 6000+                                       | 600                                                      |
| **GitHub Contributors**             | 100+                                        | 110+                                                     |

<p style="text-align: center">コミュニティと人気者（2023年3月24日）</p>

## スケーラビリティとパフォーマンス

Mosquittoは軽量なMQTTブローカーとして、クラスタリングアーキテクチャをサポートしませんが、シングルノードのパフォーマンスは優れています。小さなリソースフットプリントのサーバーで、100kを超える同時MQTT接続をサポートすることができます。

EMQXは、拡張性の高い分散型MQTTメッセージングブローカーとして、単一ノードで数百万、単一クラスタで1億の同時接続をサポートできますが、CPUとメモリの使用量ははるかに高くなります。

ご覧ください：EMQX vs Mosquitto パフォーマンスベンチマークレポートをご覧ください。

|                                           | **EMQX**                                                     | **Mosquitto**                                                | **参考リンク**                                               |
| :---------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **スケーラビリティ**                      | 1ノードあたり4M MQTTコネクション<br>1クラスタあたり100M MQTTコネクション | <1ノードあたり160K MQTT接続数                                | [EMQX 5.0による100M MQTT接続の達成](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) |
| **パフォーマンス**                        | ノードあたり200万QoS0 MQTT msgs/sec<br>800k QoS1 msg/秒<br>200k QoS2 msg/秒 | ノードあたり最大120k QoS0 MQTT msg/秒<br>80k QoS1 msg/秒<br>60k QoS2 msg/秒 |                                                              |
| **レイテンシー**                          | 1桁ミリ秒のレイテンシーをスケールアップで実現                | シナリオによっては最大数秒のレイテンシーが発生します。       |                                                              |
| **クラスター化**                          | 20ノード以上のクラスタ                                       | ❌                                                            | [クラスターのスケーラビリティ](https://docs.emqx.com/en/emqx/v5.0/deploy/cluster/db.html#node-roles) |
| **スケーリング**                          | ✅                                                            | ❌                                                            |                                                              |
| **オートクラスタリング**                  | ✅                                                            | ❌                                                            | [EMQX ノードの発見とオートクラスター](https://docs.emqx.com/en/emqx/v5.0/deploy/cluster/intro.html#emqx-node-discovery-and-autocluster) |
| **ダウンタイムゼロ/ホットアップグレード** | ✅                                                            | ❌                                                            | [リリースアップグレード](https://docs.emqx.com/en/enterprise/v4.4/advanced/relup.html#release-upgrade) |

##  MQTTとコネクティビティ

Mosiquittoは、MQTTプロトコルバージョン3.1/3.1/5.0を実装し、意志メッセージ、保持メッセージ、共有サブスクリプションなどのプロトコル仕様をサポートし、MQTT over WebSocketをサポートします。

EMQXは、MQTT 3.1/3.1/5.0と[MQTT over Websocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)プロトコルを完全にサポートしています。EMQX 5.0では、[MQTT Over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)の画期的なサポートも導入しています。多重化、接続確立と移行の高速化により、次世代のMQTT標準となる可能性を秘めています。

さらにEMQXは、MQTT-SN、CoAP、LwM2M、STOMPといった複数のプロトコルゲートウェイをサポートするように拡張することができます。

|                              | **EMQX**                                                     | **Mosquitto** | **参考リンク**                                               |
| :--------------------------- | :----------------------------------------------------------- | :------------ | :----------------------------------------------------------- |
| **MQTT 3.1/3.1.1**           | ✅                                                            | ✅             | [MQTTプロトコルのわかりやすい解説書](https://www.emqx.com/en/mqtt-guide) |
| **MQTT 5.0**                 | ✅                                                            | ✅             | [MQTT 5 エクスプロア](https://www.emqx.com/en/blog/introduction-to-mqtt-5)    |
| **MQTT Shared Subscription** | ✅                                                            | ✅             |                                                              |
| **MQTT Add-ons**             | 独占配信<br>ディレイパブリッシュ<br>オートサブスクリプション<br>トピックのリライト | ❌             |                                                              |
| **MQTT over TCP**            | ✅                                                            | ✅             | [EMQX入門編](https://docs.emqx.com/en/emqx/v5.0/getting-started/getting-started.html#quick-verification-using-an-mqtt-client) |
| **MQTT over TLS**            | ✅                                                            | ✅             | [EMQX MQTTブローカーのSSL/TLSを有効化する。](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) |
| **MQTT over WebSocket**      | ✅                                                            | ✅             | [WebsocketでMQTTブローカーに接続する。](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) |
| **MQTT over QUIC**           | ✅                                                            | ❌             | EMQXは現在、世界で唯一、QUICトランスポートをサポートするMQTTブローカーです。( [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic)) |
| **LB (Proxy Protocol)**      | ✅                                                            | ✅             | Proxy Protocol v1、v2（[クラスターロードバランサー](https://docs.emqx.com/en/emqx/v5.0/deploy/cluster/lb.html)） |
| **IPv6 Support**             | ✅                                                            | ✅             |                                                              |
| **Multi-protocol Gateway**   | ✅                                                            | ❌             | [Extended protocol gateway](https://docs.emqx.com/en/emqx/v5.0/gateway/gateway.html#design) |
| **MQTT-SN**                  | ✅                                                            | ❌             | [MQTT-SN gateway](https://docs.emqx.com/en/emqx/v5.0/gateway/mqttsn.html) |
| **CoAP**                     | ✅                                                            | ❌             | [CoAP protocol gateway](https://docs.emqx.com/en/emqx/v5.0/configuration/configuration-manual.html#coap) |
| **LwM2M**                    | ✅                                                            | ❌             | [LwM2M protocol gateway](https://docs.emqx.com/en/emqx/v5.0/configuration/configuration-manual.html#lwm2m) |
| **STOMP**                    | ✅                                                            | ❌             | [STOMP Gateway](https://docs.emqx.com/en/emqx/v5.0/gateway/stomp.html) |

## セキュリティ

IoTデバイスの接続や、接続されたデバイスとクラウドサービス間でやり取りされるデータには、セキュリティが重要です。MosquittoとEMQXはともに、TLS/SSLに基づくセキュアな接続をサポートしています。さらにEMQXは、QUICトランスポート、OCSPステープリング、監査ログ、Black Duckによるソースコードスキャンをサポートしています。

|                   | **EMQX** | **Mosquitto** | **参考リンク**                                               |
| :---------------- | :------- | :------------ | :----------------------------------------------------------- |
| **TLS/SSL**       | ✅        | ✅             | EMQX: TLS 1.1, 1.2, 1.3 ( [EMQX MQTT ブローカーの SSL/TLS を有効にする](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) ) |
| **QUIC**          | ✅        | ❌             | [MQTT over QUIC：次世代IoT標準プロトコル](https://www.emqx.com/en/blog/mqtt-over-quic) |
| **OCSP Stapling** | ✅        | ✅             | [EMQX OCSPステープリング対応](https://www.youtube.com/watch?v=e9SiF7ptvpU) |
| **Audit ログ**    | ✅        | ❌             |                                                              |

## 認証と認可

MQTTクライアントの認証やアクセス制御については、Mosiquittoが提供するダイナミックセキュリティプラグインにより、ユーザー名/パスワードによる認証やアクセス制御を柔軟に対応することができます。

EMQXには、[ユーザー名-パスワード認証](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication)、JWT認証、MQTT 5.0プロトコルに基づく拡張認証など、複数の認証メカニズムに対するサポートが組み込まれています。EMQXの認証は、ファイル、Redis、MySQL、PostgreSQL、MongoDBなど、さまざまなデータバックエンドと統合されています。

また、EMQXはフラッピング検知やブロックリスト機能を備えており、DashboardやHTTP APIを介して、IPアドレス、clientId、ユーザー名をブロックリストに追加することで、特定のクライアントをブロックすることが可能です。

|                                    | **EMQX** | **Mosquitto** | **参考リンク**                                               |
| :--------------------------------- | :------- | :------------ | :----------------------------------------------------------- |
| **ユーザー名/パスワード**          | ✅        | ✅             | [EMQX：AuthN の紹介](https://docs.emqx.com/en/emqx/v5.0/security/authn/authn.html)<br>[Mosquitto：認証方法について](https://mosquitto.org/documentation/authentication-methods/#:~:text=In Mosquitto 2.0 and up%2C you must choose,authentication%3A password files%2C authentication plugins%2C and unauthorised%2Fanonymous access.) |
| **JWT**                            | ✅        | ✅             | EMQX： [JWT認証システム](https://docs.emqx.com/en/emqx/v5.0/security/authn/jwt.html)<br>Mosquitto: [mosquittoのAuthプラグイン](https://github.com/iegomez/mosquitto-go-auth)。 |
| **MQTT 5.0 認証の強化**            | ✅        | ❌             | [SCRAM認証](https://docs.emqx.com/en/emqx/v5.0/security/authn/scram.html) |
| **PSK**                            | ✅        | ✅             | [SSL/TLS](https://docs.emqx.com/en/emqx/v5.0/security/ssl.html#psk-authentication) |
| **X.509証明書**                    | ✅        | ✅             |                                                              |
| **LDAP**                           | ✅        | ✅             | [LDAP認証/ACL](https://docs.emqx.com/en/enterprise/v4.4/modules/ldap_authentication.html) |
| **きめ細かなアクセスコントロール** | ✅        | ✅             | [EMQXのオーソライズ](https://docs.emqx.com/en/emqx/v5.0/security/authz/authz.html) |
| **認証用バックエンド**             | ✅        | ✅             | [認証の紹介](https://docs.emqx.com/en/emqx/v5.0/security/authn/authn.html) |
| **ACLデータベースバックエンド**    | ✅        | ✅             | EMQX：ファイル、MySQL、PostgreSQL、MongoDB、組込みデータベース、HTTP [EMQX認証の紹介](https://docs.emqx.com/en/emqx/v5.0/security/authz/authz.html) |
| **フラッピングディテクト**         | ✅        | ❌             |                                                              |
| **ブロックリスト**                 | ✅        | ❌             |                                                              |

##  データインテグレーション

軽量ブローカーであるMosquittoは、データ統合をサポートしません。ユーザーは、MosquittoからMQTTメッセージを消費して、外部のデータベースやクラウドサービスに取り込むためのコードを書くことができます。

EMQXにはSQLベースのルールエンジンが組み込まれており、ブローカー内でリアルタイムにMQTTメッセージを抽出、フィルタリング、エンリッチ、変換するのに役立ちます。

EMQXのEnterprise Editionは、ルールエンジンとすぐに使えるデータブリッジを使って、Kafka、データベース、クラウドサービスとシームレスに統合することができます。

|                     | **EMQX**               | **Mosquitto** | **参考リンク**                                               |
| :------------------ | :--------------------- | :------------ | :----------------------------------------------------------- |
| **Webhook**         | ✅                      | ✅             | [Webhook](https://docs.emqx.com/en/emqx/v5.0/data-integration/data-bridge-webhook.html#example-setup-webhook-using-config-files) |
| **Rule Engine**     | ✅                      | ❌             | [Rule Engine](https://docs.emqx.com/en/emqx/v5.0/data-integration/rules.html) |
| **Message Codec**   | ✅                      | ❌             |                                                              |
| **Data Bridge**     | ✅                      | ❌             | [Data bridges](https://docs.emqx.com/en/emqx/v5.0/data-integration/data-bridges.html) |
| **Confluent/Kafka** | ✅ (Enterprise Edition) | ❌             | [Stream Data into Kafka](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_kafka.html) |
| **SAP Event Mesh**  | ✅(Enterprise Edition)  | ❌             | [Ingest Data into SAP Event Mesh](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_sap_event_mesh.html#bridge-data-to-sap-event-mesh) |
| **Apache Pulsar**   | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Pulsar](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_pulsar.html) |
| **RabbitMQ**        | ✅(Enterprise Edition)  | ❌             | [Ingest Data into RabbitMQ](https://docs.emqx.com/en/enterprise/v4.4/rule/bridge_rabbitmq.html) |
| **MySQL**           | ✅(Enterprise Edition)  | ❌             | [Ingest Data into MySQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mysql.html) |
| **PostgreSQL**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into PostgreSQL](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_pgsql.html) |
| **SQL Server**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into SQL Server](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_sqlserver.html) |
| **MongoDB**         | ✅(Enterprise Edition)  | ❌             | [Ingest Data into MongoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_mongodb.html) |
| **Redis**           | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Redis](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_redis.html) |
| **Cassandra**       | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Cassandra](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_cassandra.html) |
| **AWS DynamoDB**    | ✅(Enterprise Edition)  | ❌             | [Ingest Data into DynamoDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_dynamodb.html) |
| **ClickHouse**      | ✅(Enterprise Edition)  | ❌             | [Ingest Data into ClickHouse](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_clickhouse.html) |
| **InfluxDB**        | ✅(Enterprise Edition)  | ❌             | [Ingest Data into InfluxDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_influxdb.html) |
| **TimeScaleDB**     | ✅(Enterprise Edition)  | ❌             | [Ingest Data into TimescaleDB](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_timescaledb.html) |
| **Oracle**          | ✅(Enterprise Edition)  | ❌             | [Ingest Data into Oracle](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_oracle.html) |

 

## 操作性・観察性

Mosquittoは、ブローカーの状態を監視し、問題のトラブルシューティングを行うための基本的なロギングとデバッグ機能を備えています。しかし、高度な管理・監視機能がないため、実行中の状態を把握し、パフォーマンスを最適化することが困難です。

EMQXは、HTTP APIとDashboardを通じて、リッチでビジュアルな監視機能を提供し、監視と管理を容易にする。また、EMQXはPrometheusやDatadogとの連携をサポートしており、O&Mチームはサードパーティの監視プラットフォームを容易に利用することができます。

|                                    | **EMQX**          | **Mosquitto**   | **参考リンク**                                               |
| :--------------------------------- | :---------------- | :-------------- | :----------------------------------------------------------- |
| **Dashboard**                      | ✅                 | ❌               | [EMQXダッシュボード](https://docs.emqx.com/en/emqx/v5.0/getting-started/dashboard.html) |
| **Configuration**                  | HOCONフォーマット | Key-Value Fomat |                                                              |
| **HTTP API**                       | ✅                 | ❌               | [EMQX REST API](https://docs.emqx.com/en/emqx/v5.0/admin/api.html) |
| **CLI**                            | ✅                 | ✅               | [コマンドラインインターフェイス](https://docs.emqx.com/en/emqx/v5.0/admin/cli.html) |
| **Config Hot update**              | ✅                 | ❌               | [コンフィギュレーションファイル](https://docs.emqx.com/en/emqx/v5.0/admin/cfg.html) |
| **Metrics**                        | ✅                 | ✅               | ノードのメトリクス： [Metrics](https://docs.emqx.com/en/emqx/v5.0/observability/metrics-and-stats.html)<br>Mosquitto - $SYS topic |
| **Grafana**                        | ✅                 | ✅               | [Prometheusとの連携](https://docs.emqx.com/en/emqx/v5.0/observability/prometheus.html) |
| **Cluster Metrics**                | ✅                 | ❌               | [メトリックス](https://docs.emqx.com/en/emqx/v5.0/observability/metrics-and-stats.html) |
| **アラームアラート**               | ✅                 | ❌               | [システムトピック](https://docs.emqx.com/en/emqx/v5.0/advanced/system-topic.html#alarms-system-alarms) |
| **サブスクリプションの監視が遅い** | ✅                 | ❌               | [加入者数の統計が遅い](https://docs.emqx.com/en/emqx/v5.0/observability/slow_subscribers_statistics.html) |
| **Prometheus**                     | ✅                 | ✅               | [Prometheusとの連携](https://docs.emqx.com/en/emqx/v5.0/observability/prometheus.html#dashboard-update) |

## クラウドネイティブとKubernetes

EMQXとMosquittoは、どちらもDockerベースのコンテナ型デプロイメントをサポートしています。EMQXはKubernetes OperatorやTerraformのサポートに優れており、パブリッククラウドプラットフォームへのデプロイや運用が容易になります。

また、EMQXは、世界中のAWS、Google Cloud、Microsoft Azureの17以上のリージョンで、[Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)、[専用](https://www.emqx.com/en/cloud/dedicated)、[BYOC](https://www.emqx.com/en/cloud/byoc)のMQTTメッセージングサービスを提供しています。

|                         | **EMQX**                   | **Mosquitto** | **参考リンク**                                               |
| :---------------------- | :------------------------- | :------------ | :----------------------------------------------------------- |
| **Docker**              | ✅                          | ✅             | [EMQX Docker](https://hub.docker.com/r/emqx/emqx)            |
| **Kubernetes Operator** | ✅                          | ❌             | [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) |
| **Terraform**           | ✅                          | ❌             | [EMQX Terraform](https://www.emqx.com/en/emqx-terraform)     |
| **Cloud Service**       | ServerlessHosting/専用BYOC | Hosting       |                                                              |

EMQX Kubernetes Operator: [https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator) 

![EMQX Kubernetes Operator](https://assets.emqx.com/images/f8483728a4241191e4f49ac3f8fa5740.png)

##  MosquittoからEMQXへのブリッジ接続

EMQXとMosquittoは全く異なるMQTTブローカーですが、MQTTブリッジングアプローチで完全に動作させることができます。

IoTエッジの組み込みハードウェアやゲートウェイにMosquittoを導入し、MQTTブリッジを介してクラウド上の大規模EMQXクラスタにIoTデータを集約・インジェストすることができます。

Mosquitto MQTTメッセージのEMQXへの橋渡し」を参照してください。

![Bridging Mosquitto to EMQX](https://assets.emqx.com/images/35635ecd1ac7c7453bce2d7c46ee1511.png)

## まとめ

上記の比較から、EMQXとMosquittoは、異なるニーズやユースケースに対応する人気のMQTTブローカーであることがわかります。

Mosquittoは、シングルスレッドで軽量なMQTT Brokerとして、IoTエッジのための組み込みハードウェア、産業用ゲートウェイ、小型サーバーへの導入に適しています。

EMQXは、高可用性と水平方向のスケーラビリティをサポートする、拡張性の高い分散型MQTTサーバーです。クラウド展開、大規模なIoT、IIoT、コネクテッドカーなどのアプリケーションにより適しています。

つまり、組み込みハードウェアやIoTエッジのデプロイメントにはMosquittoを選び、クラウドではEMQXを大規模スケーラブルで高可用性のMQTTメッセージングサービスとして利用することができます。

## 参考文献

- [Eclipse Mosquitto](https://mosquitto.org/)
- [Eclipse Mosquitto Documentation](https://mosquitto.org/documentation/)
- [EMQX: The World's #1 Open Source Distributed MQTT Broker](https://github.com/emqx/emqx)
- [EMQX 5.0 Documentation](https://docs.emqx.com/en/emqx/v5.0/)
- [EMQX Enterprise Documentation](https://docs.emqx.com/en/enterprise/v5.0/)
- [EMQX Operator Documentation](https://docs.emqx.com/en/emqx-operator/latest/)
- [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic)



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
