本記事では、EMQXの接続性能のベンチマーク結果を紹介します。単一ノードのEMQXが500万の同時接続を処理できることが実証されています。

## テストシナリオ

このベンチマークテストは、500万のMQTTクライアントが1秒間に5000の接続レートでEMQXに接続することをシミュレートしています。

- 同時接続数: 500万

- 接続レート: 5000回/秒

- 認証: なし

- キープアライブ: 300秒

- クリーンセッション: true

## テスト環境

テスト環境はAlibaba Cloud上に構築されており、すべての仮想マシンはVPC(Virtual Private Cloud)サブネット内にあります。

マシンの詳細:

| ブローカー                        | デプロイメント | バージョン  | OS       | CPU | メモリ  | クラウドホストモデル                                                                                                                        |
| ---------------------------- | ------- | ------ | -------- | --- | ---- | --------------------------------------------------------------------------------------------------------------------------------- |
| [EMQX](https://github.com/emqx/emqx) | 単一ノード   | 5.0.21 | RHEL 8.5 | 64C | 128G | [hfc6.16xlarge](https://www.alibabacloud.com/help/ja/ecs/user-guide/cpu-options-of-instance-families-with-high-clock-speeds#hfc6) |

## テストツール

このベンチマークテストでは、MQTTクライアントをシミュレートするために[XMeter](https://www.emqx.com/en/products/xmeter)を使用しています。XMeterはJMeter上に構築されていますが、拡張性と機能面で強化されています。テスト中に包括的かつリアルタイムのテストレポートを提供します。また、組み込みのモニタリングツールを使用してEMQXマシンのリソース使用状況を追跡できます。

XMeterにはプライベートデプロイメントバージョン(オンプレミス)とパブリッククラウドSaaSバージョンがあります。今回のテストでは、EMQXと同じVPCにプライベートXMeterをデプロイしています。

![MQTT Benchmark Architecture](https://assets.emqx.com/images/01563837a66a84243aea056c6958bb4c.png)

## システムチューニング

Linuxカーネルチューニングについては、[EMQXドキュメント](https://docs.emqx.com/en/emqx/v5.0/performance/tune.html)を参照してください。

## ベンチマーク結果

EMQXダッシュボードは、500万以上の同時接続が達成されており、30分間のテスト全体を通して接続が非常に安定していることを示しています。

![Benchmark Results](https://assets.emqx.com/images/ab44a93747aad0727714ce6a58897576.png)

## メトリクス

| 接続応答時間の平均            | 2.93ms |
| -------------------- | ------ |
| CPU使用率の平均            | 14%    |
| CPU使用率の最大値           | 40%    |
| 全クライアント接続後のメモリ使用量の平均 | 48.7GB |
| メモリ使用量の最大値           | 51.4GB |

## まとめ

このベンチマークレポートは、単一ノードのデプロイメントでのEMQXの同時接続性能を示しています。EMQXは、より少ないマシンを使用して、より大規模なIoTアプリケーションを構築するのをユーザーに支援し、総コストを削減するのに役立ちます。


<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
