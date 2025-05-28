## **MQTTの概要**

MQTT は現在、IoT 分野で最も広く利用されている通信プロトコルです。コネクテッドカー（IoV）をはじめ、製造業、エネルギー、公共インフラ、スマートホームなど、さまざまな業界で活用されています。

![image.png](https://assets.emqx.com/images/cbb09718f40e6a56427291cb994a95ee.png)

MQTT はパケットの構造が極めてコンパクトで、帯域コストがシビアな環境に最適です。
バイナリプロトコルであるため、JSON や XML などのテキストデータはもちろん、Protobuf のようなバイナリデータ、さらには圧縮画像データまで柔軟に運べます。

また、発行 ― 購読モデルによる疎結合設計により、ビジネスロジックに集中でき、トピックや Publisher／Subscriber を後から簡単に追加・削除できます。

さらに MQTT には 3 段階の QoS があり、劣悪なネットワークでもメッセージを確実に届けられるため、通信品質が不安定な車載ネットワークでも威力を発揮します。

![image.png](https://assets.emqx.com/images/5edc46c4820c8f002ba4b6c019694a98.png)

MQTT エコシステムは成熟しており、プラットフォームやハードウェアを問わず対応ライブラリが豊富です。ほかのプロトコルと比べ、導入コストが低い点も魅力です。

![image.png](https://assets.emqx.com/images/06f2b021c0b556ba5f3fc0edee1f2e05.png)

ただし MQTT が普及するにつれ、ブローカーに大量データが流入するシナリオでは、コンシューマー側がボトルネックとなる場面も見られました。EMQ はこれを解消するため「共有購読（Shared Subscription）」を導入し、MQTT 5.0 で標準化されました。

同バージョンではリクエスト／レスポンスやトピックエイリアスなど、IoT シナリオに適した機能も追加されています。

![image.png](https://assets.emqx.com/images/860c70a7d220251d80a8d57ff1a5c6ab.png)

**TCP 上で MQTT を用いる際の課題**

MQTT 5.0 で多くの改善が行われましたが、TCP というトランスポート層に起因する問題は依然として残っています。本稿ではそれらの課題を詳しく解説します。

MQTT は下位プロトコルを特に規定しておらず、「順序保証・信頼性・双方向バイトストリーム」が満たされれば利用できます。実際には TCP と WebSocket がデフォルトとして推奨され、ほぼすべてのブローカー／クライアントが対応しています。

![image.png](https://assets.emqx.com/images/4067792312d8bae8ade6c2ad063e9fd6.png)

### **接続フェーズの問題点**

TCP（WebSocket）は「送信元 IP・送信元ポート・宛先 IP・宛先ポート」という 4 要素（4 タプル）でコネクションを識別します。一度確立した接続ではこの 4 要素が固定され、通信のたびにパケットへ付与されます。いずれか 1 つでも変化すると、受信側は「別コネクション」と見なしパケットを破棄します。

------

#### IP 変更による切断

- 帰宅時にスマホがセルラーから Wi-Fi へ自動切替
- 自動車が移動し別の基地局へハンドオーバー

いずれも端末 IP が変わるため旧 TCP コネクションは切断扱いとなり、再接続が必要になります。

![image.png](https://assets.emqx.com/images/f972527dce9be5154065e7cfaed08e23.png)

再接続には

1. **TCP 3 ウェイハンドシェイク**
2. **MQTT CONNECT／CONNACK**（多くの SDK はパイプライン送信を未実装）

少なくとも 2 RTT が必要です。TLS 1.2 を使うとさらに 4 RTT が追加され、合計 8 往復＝4 RTT。
ネットワーク遅延が 50 ms なら、接続確立だけで 400 ms になります。接続再構築中はアプリケーションデータを送れず、レイテンシにシビアなシーンでは致命的です。

![image.png](https://assets.emqx.com/images/16026eb08d82e36144c17239d84950ba.png)

#### パケット損失と再送

ネットワーク切替中に送信されたパケットは失われます。QoS 0 はそのまま欠落し、QoS 1/2 も再送が必要となり帯域と時間を消費します。再接続後も TCP のスロースタートで帯域をすぐには使い切れず、大きなメッセージは分割送信→複数 RTT が必要です。

![image.png](https://assets.emqx.com/images/e7e4ba1d46f2bc6b39ab250f91f988e8.png)

### **データ転送フェーズの問題点**

#### ヘッドオブラインブロッキング（HOL）

TCP は順序保証のため、欠落したパケットが再送されるまで後続パケットを上位層へ渡せません。バッテリ残量と緊急アラートのように無関係なメッセージでも同一ストリーム上ではブロックされます。

![image.png](https://assets.emqx.com/images/6241d413acd06296e95ff117452e30cb.png)

#### 輻輳制御アルゴリズムの更新難度

TCP は OS カーネル実装であり、アルゴリズムを変更するにはサーバーだけでなく全クライアントのアップグレードが必要になります。また正確な RTT 計測のため導入された TCP タイムスタンプは毎パケット 10 B のオーバーヘッドを招きます。

![image.png](https://assets.emqx.com/images/12b5daf0a4bbe1b86f73efe789084f92.png)

## **QUIC のメリット**

上記課題を解決すべく、EMQ は **QUIC (Quick UDP Internet Connections)** を採用しました。Google が 2013 年に開発を開始したプロトコルで、UDP 上に TCP の機能（損失検知・再送・輻輳制御など）を再構築しつつ、以下を追加しています。

- **0-RTT／1-RTT ハンドシェイク**（TLS 1.3 組込）
- **多重化ストリーム & 優先度制御**
- **プラガブル輻輳制御**（動的切替可）
- **コネクションマイグレーション**（64bit Connection ID）

![image.png](https://assets.emqx.com/images/ce3d9b44d487f776c5ecb9957bb787cd.png)

2022 年 6 月に HTTP/3 が RFC 化され、Google・Microsoft・Apple・Meta・Alibaba・Huawei などが本番導入しています。

### **TLS 1.3 組み込み**

QUIC はアプリケーション層実装で TLS 1.3 を内蔵。TLS と同時にハンドシェイクでき、初回 1 RTT、再接続は 0 RTT（Early Data）。旧 TLS 互換も切り捨てられ、常に最新暗号スイートが強制されます。

### **プラガブル輻輳制御**

CUBIC や BBR を接続単位で切替えたり、自作アルゴリズムを投入可能。サービス停止なしにオンライン変更できます。

![image.png](https://assets.emqx.com/images/50588439ac4c11e9ddaeaa151a283b7c.png)

### **正確な RTT 計測**

再送パケットも新しい Packet Number を付与し、RTT 誤検出を回避。追加オーバーヘッドは不要です。

![image.png](https://assets.emqx.com/images/82921f422de1a1b18e3f04317ac2b857.png)

### **コネクションマイグレーション**

4 タプルではなく 64bit Connection ID で識別。ネットワーク切替時も接続維持が可能です。NAT 再バインド程度なら輻輳ウィンドウを維持し、高速に転送レートを回復できます。

![image.png](https://assets.emqx.com/images/88c4cab4aee0ad4dd2370da5d92dc936.png)

### **多重化と優先度**

1 接続に複数ストリームを張り、独立して輻輳制御。あるストリームで損失が起きても他ストリームは影響を受けません。緊急データを高優先度ストリームで送れば「割込み送信」が可能です。

![image.png](https://assets.emqx.com/images/b304e40cbe842c0d4fb4a050137a8a3a.png)

## **IoV でのユースケース**

走行中の車両は都市部・郊外・トンネルなど品質の異なるネットワークを行き来します。QUIC の 0-RTT 接続復旧とコネクションマイグレーションにより、サービス断を最小化できます。

緑波走行支援など遅延に敏感なメッセージも、ストリーム優先度で確実かつ迅速に配送できます。

![image.png](https://assets.emqx.com/images/237d6e925f96f64c41acd7987b2aae34.png)

![image.png](https://assets.emqx.com/images/0b343d9391069a70bac79258feafe5db.png)

## **EMQX における MQTT over QUIC の性能**

### 製品対応

- **EMQX 5.0**：業界初の MQTT over QUIC 実装
- **EMQX 5.1（2023/06）**：プロダクションレディ

![image.png](https://assets.emqx.com/images/4d8a7b10d79f5f33c8f1994921f45f75.png)

#### ストリーム活用例

- トピック単位や QoS レベル単位でストリーム分離
- QoS 1/2 の ACK とアプリメッセージを別ストリームに分け、ブロック回避

![image.png](https://assets.emqx.com/images/618f2094e0a8794bcd94b03ee2ccf09f.png)

#### ベンチマーク環境

- EMQX 5.0（単一ノード）
- AWS EC2 M4.2xlarge（8 vCPU／32 GB）
- Ubuntu 20.04
- MQTT クライアント 5,000 台（LoadGen 8 並列）
- 遅延指標：P95
- 初回接続：TLS とほぼ同等の RTT
- 再接続：QUIC は 0-RTT で MQTT CONNECT を Early Data 送信

CPU 使用率は TLS より 20 % 低く、メモリピークは 3 GB 削減しました。

![image.png](https://assets.emqx.com/images/96097f7c25bf29de51717ed2e744e9a7.png)

#### コネクションマイグレーション試験

NAT 再バインド環境で比較したところ、TLS はメッセージ断が多数発生する一方、QUIC は途切れなく送信を継続しました。

![image.png](https://assets.emqx.com/images/a6721c1f3ec23cc87a5bf5e79bd938ae.png)

#### 劣悪ネットワーク試験

20 K PPS・20 % ノイズ・10 % パケットロス＋30 秒ごとにネットワーク切替。TLS は想定半分のスループットしか出せず、QUIC は 20 K PPS を維持しました。

![image.png](https://assets.emqx.com/images/930ca2791f3b37ddcfe37c822ec81dc5.png)

結果として、ネットワーク切替や品質劣化が頻発する環境では QUIC が TCP/TLS を大幅に上回ることが確認できました。

## **デバイス側で MQTT over QUIC を利用するには？**

現時点では MQTT over QUIC に対応した SDK は多くありません。そこで EMQ は以下のソリューションを提供しています。

| 層           | ソリューション  | 概要                                                      |
| :----------- | :-------------- | :-------------------------------------------------------- |
| クライアント | **NanoSDK**     | C/C++/Java/Python 対応。今後さらに追加予定                |
| テスト       | **emqtt-bench** | QUIC 対応の負荷試験ツール                                 |
| エッジ       | **NanoMQ**      | 超軽量ブローカー。TCP→QUIC ブリッジで既存デバイス改修不要 |

![image.png](https://assets.emqx.com/images/bddea3bdfc08fa62dd20664f5cb4f7c5.png)

これらにより、自動車 OEM やティア 1 サプライヤーはファームウェア変更なしに QUIC の利点を享受でき、パケットロス率・切断頻度を大幅に削減できています。

## **まとめ**

本記事では TCP が抱える課題と、QUIC がそれをどのように解決するかを解説しました。

**QUIC の主な利点**

1. **高速接続** — 1 RTT／0 RTT ハンドシェイク
2. **高いセキュリティ** — TLS 1.3 強制 & エンドツーエンド暗号化
3. **多重化** — ストリーム毎に優先度設定、HOL 解消
4. **プラガブル輻輳制御** — BBR など動的切替・自作も可
5. **コネクションマイグレーション** — IP 変更でも通信継続

EMQ は MQTT over QUIC の標準化を推進し、業界全体での採用を加速させたいと考えています。ぜひ皆さまのプロジェクトでも QUIC をご検討ください。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
