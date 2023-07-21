Sparkplug 3.0のリリースにより、産業用モノのインターネット（IIoT）アプリケーション向けの[MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0)プロトコルが大幅に進化し、正式になりました。Eclipse Sparkplug Working Groupによって開発されたこの新バージョンは、v2.2仕様の全体的な意図を維持しながら、以前の2.2仕様に存在した曖昧さを明確にすることを目的としています。

## **Sparkplug 3.0の主な強化点**

### より明確な仕様構成

新しい仕様では、v2.2仕様の「背景」の章が「原則」の章に置き換えられています。この章では、Sparkplugの基礎となる基本原則を詳細に説明しています。さらに、"Operational Behavior "の章では、Sparkplug環境の運用面を広くカバーしています。

### より明確な規範と目的

Sparkplug 3.0の主な目的は、明確で正式な仕様を提供し、旧バージョンに存在した曖昧さに対処することである。そうすることで、プロトコルの明確な規範を確立し、一貫性と実装の容易さを保証することを目的としています。

### MQTT 5.0仕様の組み込み

Sparkplug 3.0には、MQTT 5.0に関連する特定の設定が含まれており、特にMQTT 3.1.1の「[Clean Session](https://www.emqx.com/en/blog/mqtt-session)」と比較して、MQTT 5.0の「Clean Start」のような異なるセッション設定に対応しています。これらの追加により、SparkplugはMQTT 5.0で導入された機能拡張に対応します。

### MQTTサーバーのサブセット要件

Sparkplugインフラストラクチャには、[MQTTサーバー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)に対する特定の要件のサブセットがあります。完全な仕様に準拠したMQTT 3.1.1サーバーまたはブローカーであれば、Sparkplugインフラの要件を満たします。

MQTTサーバーに関しては、Sparkplug仕様の中で2つの要件レベルに明確に定義されている。1つ目のレベルは、MQTTサーバーがMQTT 3.1.1を満たしていれば、概ねこれらの要件を満たしているというものです。2つ目のレベルでは、さらなる機能が要求される。

***レベル1：Sparkplug準拠のMQTTサーバー***

Sparkplug 準拠の MQTT サーバーは、以下をサポートしなければならない（MUST）：

- QoS 0 (最大1回) データ用
- 状態管理のためのQoS 1（少なくとも1回
- メッセージのサポート
- 国家管理のための遺言（LWT）
-  ワイルドカードあり

***レベル2：Sparkplug Aware MQTTサーバー***

Sparkplug 準拠の MQTT サーバーの要件に加え、Sparkplug Aware MQTT サーバーには以下の追加機能が必要です：

- MQTT サーバーを通過する NBIRTH および DBIRTH メッセージを保存する。
- トピックで NBIRTH メッセージが利用できるようにする： `$sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id}` 例えば、 `group_id=GROUP1` と `edge_node_id=EON1` の場合、NBIRTHメッセージはトピック上で利用可能でなければならない： `$sparkplug/certificates/spBv1.0/GROUP1/NBIRTH/EON1`
- NBIRTH メッセージをトピックで利用可能にする：sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id}、MQTT retain フラグを true に設定。
- DBIRTHメッセージを以下のフォーマットでトピック上で利用できるようにする： `$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}` 例えば、 `group_id=GROUP1` 、 `edge_node_id=EON1` 、 `device_id=DEVICE1` の場合、DBIRTH メッセージはトピック上で利用可能でなければならない： `$sparkplug/certificates/spBv1.0/GROUP1/DBIRTH/EON1/DEVICE1`
- DBIRTH メッセージをトピックで利用可能にする： `$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}` のトピックで、MQTT retain フラグを true に設定して、DBIRTH メッセージを利用できるようにします。
- NDEATH メッセージのタイムスタンプを置き換える。MQTT サーバーがタイムスタンプを置き換える場合、NDEATH をサブスクライブしているクライアントに配信しようとする UTC 時間に設定する必要があります。

Sparkplug Aware MQTTサーバーは、Sparkplugの状態管理アプローチを拡張している。要するに、出生証明書と死亡証明書は保持されたメッセージとして保存され、新しく導入されたトピック構造 `$sparkplug/certificates/#` を使用してアクセスできます。

NDEATHメッセージのタイムスタンプを更新する機能は、このバージョンの注目すべき機能である。Last Will 機能により、これらのタイムスタンプはブローカーに保存されます。Last Will メッセージは [MQTT 接続](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)試行に含まれ、無条件のクライアント切断の実際の時刻が不明であるため、無効なタイムスタンプを含んでいます。LWTメッセージの発行を通じてこのタイムスタンプを更新することで、この問題に対処できます。

## **IIoTアプリケーション向けSparkplug 3.0のメリット**

### 相互運用性の強化

より正式化され明確化された仕様により、Sparkplug 3.0はIIoTデバイス、システム、プラットフォーム間の相互運用性の向上を促進します。これにより、産業環境内でのシームレスな統合と通信が可能になります。

### 効率的なデータ同期

MQTT Sparkplug 3.0の拡張された状態管理機能は、接続されたデバイス間の効率的で同期されたデータ更新を保証する。この機能は、大規模なIIoTデプロイメントを扱う場合に特に価値が高くなります。

### 合理化された展開

MQTTサーバーのサブセット要件は、既存のMQTT v3.1.1サーバーを活用できることを保証し、Sparkplug 3.0を採用する際の大規模なインフラ変更の必要性を低減します。

## **スパークプラグ互換性プログラム**

Sparkplug Compatibility Programは、ソフトウェアおよびハードウェアベンダーがEclipse SparkplugおよびMQTTベースのIoTインフラストラクチャとの互換性を証明することを可能にします。このプログラムは、産業用IoTにおける一般的なデバイスやネットワークとのシームレスな統合を促進し、認定されたソリューションと容易な調達を保証します。

認定ベンダーは、製品がSparkplug仕様に準拠していることを保証し、スムーズな相互運用性と合理的な実装を可能にします。ベンダーはオープンソーステストを受け、Sparkplug Technical Compatibility Kit（TCK）への準拠を確認します。テストに合格した製品は、[Sparkplugワーキンググループのウェブサイト](https://www.eclipse.org/org/workinggroups/eclipse_sparkplug_charter.php)に掲載される公式互換製品リストに追加されます。Sparkplug Compatibleのロゴは互換性を示しています。

顧客は、認証製品が厳格な試験を受け、要求される基準を満たしていることを信頼できる。

このプログラムは、ベンダーと顧客の双方にメリットをもたらす：

- シームレスな統合の促進

  このプログラムは相互運用性を促進し、システムインテグレーターとエンドユーザーの統合を簡素化します。認定されたコンポーネントはシームレスに連携するため、企業は自信を持って堅牢なIoTソリューションを構築することができます。

- イノベーションとコラボレーションの促進

  認証はイノベーションとコラボレーションを促進します。ベンダーは自社製品をSparkplugと連携させることで、豊富な機能を備えた相互運用可能なソリューションを育成します。ベンダー間の知識の共有とコラボレーションにより、活気あるエコシステムが構築されます。

## **まとめ**

Sparkplug 3.0は、IIoTアプリケーション向けのMQTT Sparkplugプロトコルに大幅な進化と正式化をもたらします。改善された明快さ、明確な仕様、MQTT 5.0との整合性により、Sparkplug 3.0は、相互運用性の強化、効率的なデータ同期、産業環境への合理的な導入を実現します。IIoTエコシステムが進化し続ける中、Sparkplug 3.0はIIoTネットワーク内で信頼性が高くスケーラブルな通信を行うための堅牢で標準化されたソリューションを提供します。

世界有数の[オープンソースMQTTブローカー](https://www.emqx.io/)であるEMQXは、すべてのSparkplug 3.0メッセージトラフィックを管理するインフラの主要コンポーネントです。IIoTコネクティビティ・サーバーである[Neuronは、エッジ・ノード](https://neugates.io/)として機能し、OTデバイスのスマート化を支援し、非同期でSparkplug 3.0メッセージを報告することができます。



<section class="promotion">
    <div>
        EMQX Enterprise を無料トライアル
      <div class="is-size-14 is-text-normal has-text-weight-normal">任意のデバイス、規模、場所でも接続可能です。</div>
    </div>
    <a href="https://www.emqx.com/ja/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
