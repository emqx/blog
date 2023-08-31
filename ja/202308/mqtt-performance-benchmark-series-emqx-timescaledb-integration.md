> IoTシナリオでは、多数のデバイス、高いデータ生成レート、そして膨大なデータ量の課題がよくあります。そのため、これら大量のデータにアクセスし、保存、処理する方法は重要な課題となっています。
> 
> EMQXは、IoTのための高スケーラブルでパワフルなMQTTブローカーで、単一クラスターで数十億の同時接続と1秒間に数百万のメッセージを処理できます。さらに、組み込みの[データインテグレーション](https://www.emqx.com/en/solutions/mqtt-data-integration)機能により、Kafka、SQL、NoSQL、時系列データベースなど、40を超えるクラウドサービスとエンタープライズシステムとのシームレスなインテグレーションが可能です。
> 
> このブログシリーズでは、単一ノードEMQXサーバーとのインテグレーションのベンチマークテスト結果を紹介します。
> 
> 本記事では、TimescaleDBとのインテグレーションの結果をご紹介します。単一ノードのEMQXが1秒間に10万件のQoS1メッセージを処理し、TimescaleDBに挿入する性能を達成しました。

## テストシナリオ

このベンチマークテストは、10万のMQTTクライアントが1秒間に5000の接続レートでEMQXに接続することをシミュレートしています。すべての接続が確立された後、各クライアントは1秒間にペイロード200バイトのQoS1メッセージを1つパブリッシュし、すべてのメッセージはルールエンジンによってTimeScaleDBに書き込まれます。

- 同時接続数: 100,000

- トピック数: 100,000

- CPS(新規接続数/秒): 5000

- QoS: 1

- キープアライブ: 300s

- ペイロード: 200 bytes

- メッセージ送信TPS: 100,000/second

## テスト環境

テスト環境はAlibaba Cloud上に構築されており、すべての仮想マシンはVPC(Virtual Private Cloud)サブネット内にあります。

### マシンの詳細

| サービス                   | デプロイメント  | バージョン | OS         | CPU | メモリ | クラウドホスト                                                                                                                                                     |
| ---------------------- | -------- | ----- | ---------- | --- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EMQX                   | 単一ノード    | 5.1.0 | Centos 7.8 | 32C | 64G | [c6.8xlarge](https://www.alibabacloud.com/help/ja/ecs/user-guide/general-purpose-instance-families?spm=a2c63.p38356.0.0.799a4cc3YHrHpa#section-gck-bi6-q6l) |
| PostgreSQL/TimescaleDB | スタンドアローン | 13.5  | Centos 7.8 | 16C | 64G | [c6.4xlarge](https://www.alibabacloud.com/help/ja/ecs/user-guide/general-purpose-instance-families?spm=a2c63.p38356.0.0.799a4cc3YHrHpa#section-gck-bi6-q6l) |

### テストツール

このベンチマークテストでは、MQTTクライアントをシミュレートするために[XMeter](https://www.emqx.com/en/products/xmeter)を使用しています。XMeterはJMeter上に構築されていますが、スケーラビリティと機能面で強化されています。テスト中に包括的かつリアルタイムのテストレポートを提供します。また、組み込みのモニタリングツールを使用して、EMQXとTimescaleDBのリソース使用状況を追跡できます。

XMeterにはプライベートデプロイメントバージョンとパブリッククラウドSaaSバージョンがあります。このテストでは、EMQXとTimescaleDBと同じVPCにプライベートXMeterをデプロイしています。

## 準備

EMQXとTimescaleDBのインテグレーション設定の詳細な手順は、[EMQXドキュメント](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-pgsql.html)を参照してください。以下の3つの図は、このベンチマークテストで使用されたTimescaleDBブリッジの設定です。

### TimescaleDBブリッジとルールの設定

![TimescaleDB Bridge 1](https://assets.emqx.com/images/b93ee201a6ec334adab2b91b27fbf2db.png)

![TimescaleDB Bridge 2](https://assets.emqx.com/images/f94005a571fc3c226f3729764d6b03ba.png)

![Rule Config](https://assets.emqx.com/images/d9bbcc86a38ed5210ca4a5262f812f5f.png)

ブリッジとルールが作成されると、ダッシュボードから以下のようなデータフローが確認できます。

![data flow](https://assets.emqx.com/images/1f0e3e51b581c7b5ed22c3dbeac8e600.png)

### システムチューニングベンチマーク結果

Linuxカーネルチューニングの詳細は[EMQXドキュメント](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html)を参照してください。

## ベンチマーク結果

### テスト結果

- CPUとメモリの使用率は安定

- CPU使用率平均: 77%

- メモリ使用量最大: 13GB

- パブリッシュ応答時間平均: 2.39ミリ秒

テスト完了後、EMQXダッシュボードのデータブリッジ統計とデータベースの対応するテーブルのクエリ数を比較したところ、すべてのメッセージがリアルタイムでTimescaleDBに書き込まれ、正常に処理されたことが確認できました。

### 結果グラフ

**テスト中のEMQXダッシュボードとルールエンジンのスクリーンショット**

![EMQX Dashboard](https://assets.emqx.com/images/f1cdf8038de2f9e974bd132d4edf8153.png)

![Rule Engine](https://assets.emqx.com/images/c2f61266a4c8171166aaa810f2c4e823.png)

> *上記2つのスクリーンショットは、入力メッセージレートとデータブリッジによる処理レートが共に10万/秒を超えており、ルールにマッチしたすべてのメッセージがリアルタイムでデータベースに書き込まれていることを示しています。*

**テスト完了後のスクリーンショット**

![Screenshots 1](https://assets.emqx.com/images/5789ed6721ba567796501bd39b27ff87.png)

![Screenshots 2](https://assets.emqx.com/images/d896c7b04f38863995687b96c2b58783.png)

> *上記のスクリーンショットは、EMQXが受信したすべてのメッセージがTimeScaleDBに正常に転送されたことを示しています。*

**XMeterレポートチャート**

![XMeter report chart](https://assets.emqx.com/images/acb5ca296cd4c995916b9c791a440e59.png)

## まとめ

TimescaleDBは時系列データベース分野において、使いやすさ、高速クエリ、コスト効率の高さが認められています。EMQXとTimescaleDBの統合により、両者の強みが活かされ、IoTアプリケーションに対する包括的なソリューションが提供されます。

さらに、EMQXとTimescaleDBはそれぞれクラウドサービスを提供しています。クラウドの一元管理、水平スケーリングなどの機能を活用することで、簡単にEMQX CloudとTimescale Cloudサービスをデプロイおよび統合し、既存のクラウドネイティブインフラストラクチャに接続できます。詳細は当社の[ブログ](https://www.emqx.com/en/blog/seamlessly-integrating-emqx-cloud-with-the-new-timescale-service)をご参照ください。


<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
