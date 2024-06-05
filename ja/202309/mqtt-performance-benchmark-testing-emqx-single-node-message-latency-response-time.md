## **背景**

このブログでは、EMQXのメッセージレイテンシと応答時間のベンチマーク結果を提供します。

## **テストシナリオ**

このベンチマークテストは、EMQXに接続する1000のパブリッシャと1000のサブスクライバをシミュレートします。すべての接続が確立された後、各パブリッシャは1秒あたりペイロード50バイトのメッセージを1つ発行し、平均値を取得するために30分間実行します。

- 平行接続: 1000のパブリッシャ、1000のサブスクライバ
- QoS: QoS 0、QoS 1、QoS 2レベルのメッセージをテスト
- ペイロード: 50バイト
- メッセージスループット: 1000/秒

## **テスト環境**

テスト環境はAlibaba Cloud上に構成されており、すべての仮想マシンはVPC(仮想プライベートクラウド)サブネット内にあります。

### **マシンの詳細**

| サービス | デプロイ    | バージョン | OS       | CPU  | メモリ | クラウドホストモデル |
| :------- | :---------- | :--------- | :------- | :--- | :----- | :------------------- |
| EMQX     | single node | 5.0.6      | RHEL 8.5 | 2C   | 4G     | c6.large             |

### **テストツール**

このベンチマークテストでは、[**XMeter**](https://www.emqx.com/en/products/xmeter)を使用してMQTTクライアントをシミュレートします。 XMeterはJMeter上に構築されていますが、スケーラビリティと機能が強化されています。 テスト中に包括的かつリアルタイムのテストレポートを提供します。 さらに、組み込みのモニタリングツールを使用して、EMQXマシンのリソース使用状況を追跡します。

XMeterにはオンプレミス版とパブリッククラウドSaaS版があります。 このテストでは、EMQXと同じVPCにプライベートXMeterをデプロイしています。

![Test Architecture Diagram](https://assets.emqx.com/images/76af39a96c5f485a576a6ee2acb6e86d.png)

## **システムチューニング**

Linuxカーネルのチューニングについては、[**EMQXドキュメント**](https://docs.emqx.com/en/emqx/v5.0/performance/tune.html)を参照してください。

## **ベンチマーク結果**

**定義**

- レイテンシ: ブローカーがパブリッシャからサブスクライバへメッセージを送信するのにかかる時間
- 応答時間: メッセージ受信とメッセージ送信の時間差

### **メトリクス**

|                | **QoS 0** | **QoS 1** | **QoS 2** |
| :------------- | :-------- | :-------- | :-------- |
| レイテンシ(ms) | 0.048     | 0.065     | 0.07      |
| 応答時間 (ms)  | 1.7       | 1.7       | 1.7       |

### **XMeterレポートチャート**

#### QoS 0

![XMeter Report Chart QoS 0](https://assets.emqx.com/images/bca9b0aac84df53ace517f33e62da1c8.png)

#### QoS 1

![XMeter Report Chart QoS 1](https://assets.emqx.com/images/23eb172c8443ec0652ed9830f4db24e4.png)

#### QoS 2

![XMeter Report Chart QoS 2](https://assets.emqx.com/images/000570cf3d4a2c19a44feadc47531df5.png) 

# **まとめ**

これは低負荷のテストであり、結果はEMQXが非常に低いメッセージレイテンシを有していることを示しています。 実際、EMQXは大量のメッセージでもレイテンシを低く保つことができます。 これらの結果は、EMQXが高レベルのリアルタイム応答性を必要とするIoTアプリケーションにおいて価値のあるツールになりうることを示唆しています。



<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
