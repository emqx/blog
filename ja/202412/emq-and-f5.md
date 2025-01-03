## はじめに

IoT技術の急速な進展と産業界への広範な採用に伴い、膨大なデバイス接続性と急増するデータフローを処理するためのセキュアでスケーラブルなソリューションのニーズが極めて重要になっています。この需要に応えるため、エッジ・クラウドデータ接続およびMQTTプラットフォームソリューションの世界的リーダーであるEMQと、アプリケーションデリバリーおよびセキュリティソリューションの市場リーダーであるF5は、共に新興のIoTシナリオ向けにセキュアなデータアクセスソリューションを開発しました。このソリューションは、ミッションクリティカルなIoTアプリケーションに対して信頼性の高いデバイス接続とセキュアなデータ伝送を可能にし、企業のインテリジェントシステムの効率的な運用を確保します。

## ソリューションの構成

### EMQXプラットフォーム: 高い接続性と信頼性

[EMQXプラットフォーム](https://www.emqx.com/ja/products/emqx)は、EMQが開発したエンタープライズグレードのMQTT IoTプラットフォームで、大規模な展開と高い信頼性を必要とするIoTアプリケーション向けに設計されています。EMQXは以下の機能を通じてデータアクセスと管理を強化します：

- **高信頼性とスケーラビリティ**: 分散アーキテクチャに基づき、高可用性と水平スケーリングを提供。
- **多プロトコルサポート**: MQTT以外にも多様なメッセージングプロトコルをサポート。
- **柔軟なデータ統合**: 多様なデータストレージやクラウドプラットフォームとのシームレスな統合。
- **セキュリティと認証**: TLS/SSL暗号化、クライアント認証、アクセス制御を提供。
- **リアルタイムデータ処理**: ルールエンジンによるフィルタリング、変換、集約。
- **モニタリングと管理**: リアルタイムのモニタリングインターフェース。

### NGINX Plus & BIG-IP: トラフィック管理とロードバランシング

NGINX Plusは、F5によって提供されるオールインワンのAPIゲートウェイ、コンテンツキャッシュ、ロードバランサー、ウェブサーバーです。高性能なNGINXのエンタープライズ版として、スケーラブルで信頼性の高い高可用性を提供し、アクティブヘルスチェックとライブダッシュボードを備えています。

BIG-IPはF5の主要製品で、ロードバランシング、ウェブアプリケーションファイアウォール、SSL終端、動的ロードバランシング、グローバルサーバーロードバランシングを提供します。BIG-IP TMOSはハイブリッドおよびマルチクラウドワークロード向けの高度にプログラム可能で自動化可能なアプリサービスを提供し、次世代アプリケーションのニーズに対応しています。

### 統合ソリューション

![EMQXとNGINX PlusおよびBIG-IP](https://assets.emqx.com/images/bec5888d8c37a99e213c7ca6fabb2b74.png)

EMQXをNGINX PlusおよびBIG-IPと組み合わせることで、ロードバランシングとMQTTメッセージアクセスを統合したソリューションが構築されます。主な利点は以下の通りです：

- **グローバルサーバーロードバランシング（GSLB）**: 分散クラスタのロードを監視し、最適なノードへトラフィックを動的にルーティング。
- **TLS、DTLS、GMSSL認証**: 多様なセキュリティ要件に対応。
- **スティッキーセッションとTCP接続の移行**: システムアップグレードやスケーリング中の接続中断を最小限に。
- **セキュリティとログ管理**: 強力なロギングと分析によるシステム監査。
- **MQTT over QUICロードバランシング**: 安定した低遅延接続を提供。

この共同ソリューションにより、スケーラブルなデータアクセス、堅牢なトラフィック管理、セキュアなデータ配信が実現し、企業はより安定的でセキュアなIoTプラットフォームとアプリケーションを構築できます。

## 業界の応用例

### コネクテッドカーとスマートファクトリー

コネクテッドカーや産業用IoTでは、デバイスが広範に分散しており、リアルタイムデータ伝送が不可欠です。GSLB機能により、各地域のユーザーリクエストに基づき最適なノードへトラフィックをルーティングし、低遅延のデータ伝送を確保します。サービスノードが故障した場合も自動フェイルオーバーにより安定したデータ伝送を維持します。



![コネクテッドカー向けの安定したデータインタラクション](https://assets.emqx.com/images/2a4056675e3949391586d4a928a83801.png)

### シームレスなアップグレードとスケーリング

大規模なコネクテッドカーやスマート製造環境では、頻繁なシステムアップグレードやリソース拡張が必要です。TCP接続の移行機能により、システムのアップグレードやスケーリング中の接続中断を最小限に抑え、安定したサービスを提供します。

![シームレスなアップグレードとスケーリング](https://assets.emqx.com/images/5e6f5bc17ea0118ae4482d20c9c1395f.png)

### 複雑なネットワーク環境下での効率的な通信

不安定な信号環境下（高速道路や遠隔地）でも、EMQのMQTT over QUIC技術により低遅延で高信頼性の通信を実現し、F5のロードバランシングと組み合わせることで通信の継続性を向上させます。これにより、高速車両や遠隔地通信に最適なソリューションを提供します。

![MQTT over QUIC](https://assets.emqx.com/images/fb809fcd39ef74109e6530fe1a58f4ca.png)



![効率的な通信](https://assets.emqx.com/images/1e31b9a62d86a8d6bf1824c9b2d0abe8.png)

## まとめ

EMQとF5の共同ソリューションは、EMQXプラットフォームの高い同時接続性とF5の先進的なロードバランシング・セキュリティ技術を組み合わせ、スケーラブルで高性能なデータアクセスソリューションを提供します。このソリューションは、セキュアなデータ伝送とシステムの安定性を確保し、コネクテッドカー、産業用IoT、AIoTなどのミッションクリティカルなシナリオを信頼性高くサポートします。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>