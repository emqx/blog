## ジオディストリビューションの概念

EMQXについて語る時、最初に挙げられるのは通常、その印象的なスケーラビリティです。EMQXは投入されるハードウェアの量にほぼ線形にスケールしますが、単一のコンピューティングインスタンスでのスケーラビリティには必然的に限界があります：インスタンスのリソースが枯渇し、アップグレードのコストが指数関数的に増加します。ここで*分散*が重要になります。複数のコンピューティングインスタンスにEMQXノードのクラスターを展開することで、さらなるスケーリングが可能になります。EMQXの豊富なクラスタリング機能のおかげで、この作業は比較的簡単です。

分散により、単一の地理的位置に制限されることはなくなります。異なる大陸にある複数のデータセンターにEMQXクラスターを展開することさえ可能で、これを*ジオディストリビューション*と呼びます。ジオディストリビューションの主な利点は、クライアントが大陸全体に散らばっている場合に、クライアントにより近い位置にいられることです。各クライアントは最も近いEMQXインスタンスに接続でき、より低いレイテンシー、より高い信頼性、そして結果としてより高いスループットを享受できます。もう一つの価値ある利点は耐障害性です：データセンターの停止がサービス全体ではなく、一部分にのみ影響を与えます。

## 課題

しかし、よくあることですが、どんな分散にも固有のコストがあります。そしてジオディストリビューションのコストは特に高くなります。

1. インスタンスはネットワークで分離され、ネットワークは遅い。

   実際には特別遅いわけではありませんが、同じインスタンス上のCPUコア間の通信（レイテンシーがナノ秒単位で測定される）に比べればはるかに遅いです。ネットワークは*レイテンシー*をもたらします。インスタンス同士が離れれば離れるほど、レイテンシーは高くなります。これは物理法則に従うため、最適化して取り除くことはできません。したがって、誰かがそのコストを支払わなければなりません。オーストラリアやブラジルのクライアントにより近づけば、一方でいくつかのEMQXノードは必然的に互いに遠く離れることになり、それらの間の通信は遅くなります。その場合、数十ミリ秒遅くなります。

2. ネットワークは信頼性が低い。

   ネットワーク輻輳、ハードウェア障害、設定ミス、さらには悪意のある活動により、パケットが失われ、接続が切断されます。EMQXノード同士が遠く離れるほど、通過しなければならない中間ネットワーク機器が増え、通過するワイヤも長くなり、障害が発生する可能性が高くなります。これらの一部はネットワークスタックによって処理され、レイテンシースパイクとしてのみ現れますが、他のものはアプリケーション層に伝播し、多くの不確実性をもたらします。このような障害の存在下では、EMQXノードはリモートノードがダウンしているのか、ネットワークが異常に信頼性が低いだけなのかを判断できません。これは*部分的障害*として知られるものの現れであり、*可用性*の低下につながる可能性があります。

厳密に言えば、レイテンシーについて話す際には、*スループット*も考慮に入れる必要があります。高レイテンシーのネットワークでも、十分に高いスループットを持つことができます。しかし、ネットワークの信頼性の低さは通常、高スループットの達成を困難にします。TCPコネクションの場合、単一のパケット損失でさえスループットの大幅な低下を引き起こす可能性があります。なぜなら、TCPスタックはパケットを再送信し、送信ウィンドウを大幅に縮小しなければならないからです。ここでも、通信ピア同士が離れれば離れるほど、これはより頻繁に起こります。

問題をさらに複雑にしているのは、多くのクライアントにとって生のネットワークスループットは通常重要ではないということです。むしろ、[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)上で行われる様々な*操作*のスループットが重要です。例えば、メッセージのパブリッシュのスループット、または`SUBSCRIBE`操作のスループットです。ここで*共有状態*が関係してきます。そして、より重要なのは、この状態の更新を*調整*する必要性です。

MQTTプロトコルの性質上、非同期的に動作し、クライアントが比較的独立しているため、共有状態の厄介さはそれほど目立ちません。しかし、それでも存在します。しかし、まず問題をよりよく理解するために、基本的なジオ分散EMQXクラスターのセットアップから始めましょう。

## 12600 km幅のクラスター

すでにご存知かもしれませんが、EMQX 5は新しいデプロイメントモデルに従っています。クラスターは*コア*と*レプリカント*の2種類のノードで構成されています。このモデルは、ジオディストリビューションを含む、より広範なデプロイメントシナリオをサポートするために特別に設計されました。ただし、後で探索する落とし穴もあります。このモデルの下では、クラスターは2種類のノードで構成されます：共有状態の重要な部分を管理するコアノードと、状態管理には参加せず、単にコアノードが行った状態変更を複製するレプリカントノードです。

しかし、まずはより伝統的な方法でクラスターをデプロイしてみましょう。そうすることで、新しいモデルの利点がどこから来るのかをよりよく理解できます。私たちの「伝統的な」クラスターは、3大陸に地理的に分散された3つのコアノードで構成されます。

| **場所**                      | **ノード名**         |
| :---------------------------- | :------------------- |
| フランクフルト (eu-central-1) | `emqx@euc1.emqx.dev` |
| 香港 (ap-east-1)              | `emqx@ape1.emqx.dev` |
| ケープタウン (af-south-1)     | `emqx@afs1.emqx.dev` |

![EMQX Geo-Distribution 1](https://assets.emqx.com/images/3f0d2c80af41b939f5e2b82050ba9f2d.png)

問題空間をよりよく理解し、我々が行った改善を示すのに役立つ、もう一つの「伝統的な」ことは、この小さな設定スニペットです：

```
broker.routing.storage_schema = v1  # 5.4.0以前のルーティングテーブルスキーマを使用
```

これが最良のアイデアではなかったことを示唆し始める最初のものは、クラスターが運用可能になるまでにかかった時間です。ログは、特定の`mria`初期化ステップに**丸々数秒**かかることを示しています。

```
15:11:42.654445 [notice] msg: Starting mria, mfa: mria_app:start/2
15:11:42.657445 [notice] msg: Starting shards, mfa: mria_app:start/2
15:11:47.253059 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: '$mria_meta_shard', tables: ['$mria_rlog_sync',mria_schema]
15:11:48.714293 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_common_shard, tables: [bpapi,emqx_app,emqx_banned,emqx_trace]
15:11:50.188986 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
15:11:51.662162 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
...
```

なぜでしょうか？ノードは**それほど**遠く離れているわけではありません。ping時間を見れば簡単にわかります。

```
v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@afs1.emqx.dev']). {161790,pong} v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@ape1.emqx.dev']). {202801,pong}
```

確かに、パケットがフランクフルトからケープタウンまで往復するのに~160ミリ秒、香港まで往復するのに~200ミリ秒かかります。実は、`mria`が内部で`mnesia`を使用しているのが理由です。`mnesia`は*分散データベース*です。各初期化ステップは本質的にデータベーストランザクションであり、各トランザクションはクラスターノードの（少なくとも）過半数との調整が必要です。各調整ステップは、参加ノード間で1回以上の往復を必要とします。この場合、共有状態はデータベーススキーマであり、この調整はクラスター内のすべてのノードでスキーマが*一貫して*いることを確保するために必要です。

このことを念頭に置いて、これが単一クラスの操作：`SUBSCRIBE`のパフォーマンスにどのように影響するかを見てみましょう。

## レイテンシーの影響

痛ましい数分後、クラスターはついに負荷をかける準備ができました。[mqttx-cli](https://mqttx.app/ja)を武器に、クラスターへの接続を開き、単一のトピックをサブスクライブするのにどれくらいの時間がかかるかを見てみましょう。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/%i
[9:14:29 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/%i
✔  success   [1/1] - Subscribed to t/mqttx/1
[9:14:30 AM] › | Created 1 connections in 0.89s

```

ほぼ1秒。160ミリ秒や200ミリ秒よりもはるかに長いです。なぜなのかを理解するには、MQTTクライアントとブローカーがどのように接続とサブスクリプションを交渉するかを考慮する必要があります：

1. クライアントがEMQXへの接続を開き、`CONNECT`パケットを送信します。

   パケットにはClient IDプロパティが含まれており、仕様ではブローカーはクラスター内にそのようなIDを持つクライアントを1つしか持てないと定められています。ここでの「1つだけ」という部分が重要です。同じClient IDを持つ複数のクライアントが同時に異なるノードに接続しようとすると、解決すべき*コンフリクト*が発生します。ブローカーは接続されているすべてのクライアントについて[強い一貫性](https://jepsen.io/consistency/models/strict-serializable)のあるビューを持つ必要があり、これは行われた変更がノードの過半数と調整されなければならないことを意味します。さらに、傷口に塩を塗るように、強い一貫性はグローバルロックを通じて強制され、これらのロックはまず獲得され、その後解放される必要があります。したがって、クラスターノードはこの操作を完了するために、過半数との2回の通信ラウンドを連続して実行する必要があります。不運にも、最も遠いノードが過半数の一部となった場合、この操作にはそのノードとの2回の往復のコストがかかります。

2. クライアントが`SUBSCRIBE`パケットを送信します。

   これはより単純です。EMQXは、このノード上の誰かが`t/mqttx/1`をサブスクライブしたことを過半数に伝えるだけで良く、これによって後でメッセージを正しい場所に正確にルーティングできます。この種の変更は複雑な調整を必要とせず、ここでは競合が発生する可能性がないからです。しかし、クラスターピアとの1回の往復は依然として必要です。

全体として、この操作は~600ミリ秒かかるはずですが、私たちは完璧ではない世界と完璧ではないネットワークに生きています。クライアントを1秒待たせるのは良くありませんが、スループットはどうでしょうか？

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/%i
[9:32:19 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/%i
✔  success   [100/100] - Subscribed to t/mqttx/100
[9:32:21 AM] › | Created 100 connections in 1.706s
```

100倍多くのクライアントを処理するのに2倍の時間がかかりました。良いニュースです！このワークロードでは、各クライアントが一意のClient IDで接続し、一意のトピックをサブスクライブするため、クライアントは本質的に互いに独立しています。競合はないので、時間係数は1倍であるはずです。しかし、実際にはそうではありません。なぜなら、EMQXはデフォルトで安全対策として*並行性*を人為的に制限し、負荷下でより予測可能に動作するようにしているからです。内部的に、EMQXはデータ競合を避け、不必要な作業を最適化するために、トピックごとにサブスクリプションをシリアル化します。デフォルトでは、シリアル化ポイントとして機能するプロセスの数が限られています。しかし、良いニュースがあります：この制限は[現在設定可能](https://github.com/emqx/emqx/pull/11390)になり、このような広範なデプロイメントに対応するために増やすことができます。

## EMQXノード競合はより大きな影響を与える

ここで、ワークロードを少し変更した場合に何が起こるかを見てみましょう：各クライアントは一意のトピックフィルターをサブスクライブしますが、共通のプレフィックスを持つものとします。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[9:48:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[9:48:47 AM] › | Created 1 connections in 2.938s

```

無理だ！ほぼ3秒です。何が起こったのでしょうか？トピックフィルターが原因です。EMQXは now メッセージを効率的にマッチングしてルーティングするために、クラスター全体でトピックフィルターの*インデックス*を維持する必要があります。このインデックスは、クライアントがトピックをサブスクライブまたはアンサブスクライブするたびに更新される必要があり、この更新は全てのノードでこのインデックスが同一になるように一貫して適用される必要があります。再び、これにはトランザクションが必要で、トランザクションには調整が必要で、調整にはクラスターノード間の多くの通信ラウンドが必要で、それは多くのネットワーク往復に値します。

希望的に、レイテンシーは高くても、スループットは良くなるはずです。そうですよね？

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:44:43 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:25 AM] › | Created 100 connections in 101.958s

```

100クライアントに102秒かかりました。ワークロードはまだほぼ同じに見えるにもかかわらず、並行性のすべての利点を失いました：一意のClient IDを持つクライアントが一意のトピックフィルターをサブスクライブしています。実は、犯人はレガシーの*v1*インデックスの設計です。メッセージをトピックフィルターに迅速にマッチングするために、インデックスは*トライ*として編成され、EMQXは共通のプレフィックスを追跡することでそれをコンパクトに保とうとします。クライアントが`t/mqttx/+/42/sub/+/#`をサブスクライブすると、EMQXは`t/mqttx/+/42/sub/+`と`t/mqttx/+`のレコードに触れる必要があります。問題は、他のすべてのクライアントのサブスクリプションも`t/mqttx/+`レコードの更新を引き起こし、ここで*競合*が発生することです。競合が発生すると、`mnesia`はクラシックなデータベースのように対処します：レコードをロックし、効果的に更新をシリアル化します。より多くのクライアントがサブスクライブすると、競合の数が増加し、それらを解決するのにより多くの時間がかかります。

接続の問題があったとしても、TCPスタックで処理できるほど軽微なものでした。ネットワークがより深刻な不安定性を示し、ノードの1つが到達不能になった場合、トランザクションはタイムアウトし始めたでしょう。この性質のトランザクションは、レコードにロックを獲得し、そのロックはトランザクションがタイムアウトするまで保持されたままになったかもしれません。このシナリオは、競合するレコードを含む他のすべてのトランザクションを効果的にブロックし、そしてサブスクリプションを完全に停止させたでしょう。

## EMQXノード競合の回避

幸いなことに、私たちが手動で有効にしたこの*v1*スキーマはもはやデフォルトではなく、新しい[*v2*](https://github.com/emqx/emqx/pull/11524)スキーマが[EMQX 5.4.0](https://github.com/emqx/emqx/releases/tag/v5.4.0)からデフォルトとして十分に堅牢でパフォーマンスが高いと考えられるようになりました。状況を根本的に改善する主な違いは、それが*競合フリー*であることです：クライアントがどれほど複雑で混沌としたトピックフィルターを使用していても、それらを管理することが書き込み競合を引き起こす可能性はゼロです。サブスクリプションパターンの潜在的な衝突について心配する必要はもうありません。

使用していたこの設定を捨てて、*v2*が「伝統的な」ものに比べてどのように機能するか見てみましょう。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:46:54 PM] › ℹ  Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:55 PM] › ℹ  Created 100 connections in 1.673s

```

印象的です！これは予想以上に良かったです：100クライアントが前のシナリオで1クライアントにかかった時間よりも少ない時間で処理されました。

しかし、私たちはまだ理論的な限界である600ミリ秒程度からは遠いです。確かに、ネットワークが完璧でない限り、この限界に到達するのは非現実的です。しかし、改善の余地はあります。レイテンシーをより耐えやすくする他の方法を探ってみましょう。

## レプリカントの救済

明らかに、私たちのワークロードをデプロイメントモデルにより適合するように最適化することはできますが、レイテンシーのコストは依然として支払われる必要があります。代わりに、「伝統的な」デプロイメントを捨てて、3つの同一場所のコアノードと3つのレプリカントで構成され、同じ3大陸に地理的に分散されたクラスターにEMQXをデプロイしてみましょう。

![EMQX Geo-Distribution 2](https://assets.emqx.com/images/460cdbd66a7e51e84f988f1574874025.png)

このように、コストのかかる状態変更はレイテンシーの低いコアノードによってのみ実行され、レプリカントは状態変更に追随するだけで済みます。以前と同様に、クライアントはコアノードかレプリカントかに関係なく、最も近いノードに接続します。

| **場所**                      | **ノード名**                                                 |
| :---------------------------- | :----------------------------------------------------------- |
| ムンバイ (ap-south-1)         | `emqx@core1.emqx.dev` `emqx@core2.emqx.dev` `emqx@core3.emqx.dev` |
| フランクフルト (eu-central-1) | `emqx@euc1.emqx.dev`                                         |
| 香港 (ap-east-1)              | `emqx@ape1.emqx.dev`                                         |
| ケープタウン (af-south-1)     | `emqx@afs1.emqx.dev`                                         |

起動完了！以前のように数分待つ必要はありません。

このデプロイメントモデルの利点をすぐに見ることができます：もはやトランザクションごとに地球の半分を横断する数回の往復を支払う必要はありません。レイテンシーはまだ存在します。EMQXは`CONNECT`と`SUBSCRIBE`パケットを連続して処理する必要があるからですが、今ははるかに良くなっています。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[10:57:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[10:57:45 AM] › | Created 1 connections in 0.696s

```

スループットも大幅に向上しています。トランザクション処理はお互いに非常に近いコアノードによってのみ実行されるからです。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:04:35 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[11:04:37 AM] › | Created 100 connections in 1.091s

```

これは注目に値する改善です。100クライアントが同じことを行うのに100秒以上かかっていたことを思い出してください。

## レイテンシーの隠蔽

以前、スループットが実際にはデフォルトのプールプロセス数によって人為的に制限されている可能性があることを簡単に言及しました。これらのプロセスは競合条件を避けるためのシリアル化ポイントとして機能します。負荷を10倍に増やすことで、この制限の影響をより明確に観察できるでしょう。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:42:39 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:42:43 PM] › ℹ  Created 1000 connections in 4.329s

```

ネットワークトラフィックが10倍になったため、異常なネットワークが主な原因である可能性が高いですが、合計時間はまだ4倍悪化しています。もっと良くできるでしょうか？幸いなことに、私たちが取り組んできた別の改善が[EMQX 5.5.0](https://github.com/emqx/emqx/releases/tag/v5.5.0)リリースで導入されました：ルーティングテーブル更新の[バッチ同期](https://github.com/emqx/emqx/pull/12329)です。これは、通信が信頼できる場合に利用可能なネットワークスループットをより良く活用し、すでに高すぎる場合には操作のレイテンシーを増加させないように設計されています。

この機能はまだデフォルトで有効になっていませんが、オンにするのは非常に簡単です。

```
broker.routing.batch_sync.enable_on = replicant
```

このスニペットは、レプリカントノードでのみバッチ同期を有効にします。これを `all` に設定すると、すべてのノードで有効になり、一般的に幅広いワークロードに有益でしょう。主にブローカープールが追加の同期作業から解放されるためです。我々のケースでは、効果はそれほど顕著ではなく、説明するのが難しいでしょう。

デフォルトは `none` で、その理由は安全性です。我々はスムーズなローリングアップグレード体験を提供したいと考えており、例えば5.4.1から EMQX 5.7.0 にアップグレードする前にこれを有効にすると、一時的な利用不可能性につながる可能性があります。EMQX 5.5.0以降からアップグレードする場合は、すぐに有効にすることについて心配する必要はありません。

では、これでどうなるか見てみましょう。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:46:21 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:46:24 PM] › ℹ  Created 1000 connections in 2.585s

```

かなり大きな改善です。ネットワークスループットがより効率的に使用されており、それが `SUBSCRIBE` スループットの向上につながっています。おそらく同様の効果は、より多くのブックキーピングとメモリ使用量の増加を犠牲にしてプロセスプールを膨らませることでも達成できるでしょうが、この新機能はより柔軟で使いやすいです。

なぜまだ理論的な限界である~600ミリ秒からは遠いのでしょうか？最も妥当な説明は、一時的なネットワークの問題がどのように処理されるかです。リンクが一瞬だけ輻輳する可能性があり、それによってパケットがいくつか失われ、TCP スタックは *RTO (再送タイムアウト)* が経過した後にそれらを再送する必要があります。これは通常、すでに確立された接続ではほとんど気づかれませんが、初期のSYNパケットが失われた場合には大きな違いがあることがよくあります。この場合、TCPスタックはまだ最適なRTOを推定する機会がなかったので、保守的なデフォルトである *1秒* から始める必要があります。我々のワークロードに戻ると、ほとんどのクライアントが1秒未満で接続とサブスクライブできたのに対し、数台がSYNパケット損失につまずき、それによって合計時間が1秒増加した可能性が高いです。または、極端に運が悪ければ2秒です。

このデプロイメントモデルには明らかなトレードオフがあることを言及することが重要です：クラスターはより多くのコンピューティングリソースを必要とし、すべてのコアノードが同じデータセンターに存在するため、障害に対する回復力が低下します。それでも、そのメリットを考えると、価値のあるトレードオフです。さらに、新しい設定オプションと新しいトピックインデックス設計のおかげで、サブスクリプションの遅延の悪さが（理論的にはほぼ無制限の）スループット向上によって相殺されると合理的に予想できます。これらの機能がすべて設定可能で十分にテストされた最新の[EMQX 5.7.0](https://github.com/emqx/emqx/releases/tag/v5.7.0)リリースを試してみることを検討してください。

地理的に分散されたアプリケーション用にこの種のクラスターをデプロイする場合は、[設定のさらなるチューニング](https://docs.emqx.com/en/emqx/v5.7/configuration/configuration.html)を必ず検討してください。マルチリージョンEMQXクラスターのパフォーマンスを向上させるための追加の設定パラメータがいくつかあります。ここでは、簡略化のためにコアノードとレプリカントノードの両方に適用可能なパラメータを組み合わせた `emqx.conf` の例を示します。

```shell
# Core nodes
node.default_bootstrap_batch_size = 10000
# Replicants
node.channel_cleanup_batch_size = 10

```

これらのパラメータが何に影響するかを簡単に説明します。

- `node.channel_cleanup_batch_size`

  レプリカントノードに関連します。ネットワークレイテンシーが高い場合、この値をデフォルトの10,000から大幅に減らすと、多数のクライアントが突然切断された際のパフォーマンスが向上します。

- `node.default_bootstrap_batch_size`

  コアノードに関連します。デフォルト値は500ですが、大幅に増やすことで、多数のアクティブなサブスクリプションを持つクラスターにレプリカントノードが参加するのにかかる時間を短縮できます。

## 代替案

それでも、このような高いレイテンシーが許容できない状況があります。EMQXはこのような状況に対するソリューションを持っています：地理的に分散されたクラスターをセットアップする代わりに、リージョンごとに独立したクラスターを展開し、それらのクラスターを[非同期MQTTブリッジ](https://docs.emqx.com/en/emqx/v5.7/data-integration/data-bridge-mqtt.html)を通じて接続することが可能です。これは根本的に異なるデプロイメントモデルであり、追加のコンピューティングリソースと運用オーバーヘッドを要求します。しかし、明確な利点があります：共有状態を3大陸にわたって一貫して維持する必要がありません。各クラスターは独自の状態を持ち、サブスクリプションによって引き起こされる変更はローカルで処理され、レイテンシーが低くなります。

非同期モードのイグレスMQTTブリッジは*外部*リソースとやり取りするように設計されており、ある意味で地球の反対側にあるリモートEMQXクラスターもまさにそのようなものです。ブリッジはメモリまたは永続的ストレージによってバックアップされたバッファを持ち、信頼性の低いネットワークでよく遭遇する断続的な接続問題を処理できます。

接続されたクライアントとそのサブスクリプションの単一のグローバルビューがないため、特定のリージョンにメッセージのサブセットのみをルーティングすることはもはや不可能です。各ノードの各MQTTブリッジは**全ての**メッセージフローを各リモートロケーションにストリーミングする必要があり、出力帯域幅を飽和させます。また、情報の損失も避けられません：ブリッジされたメッセージは元のクライアントに関する情報を持たなくなります。さらに、同じブリッジされたメッセージが大陸間を行ったり来たりしないようにするには、いくらかの努力が必要です。しかし、[ルールエンジン](https://docs.emqx.com/en/emqx/v5.7/data-integration/rule-sql-syntax.html)はこれを処理するのに十分表現力があるはずです。

これらの短所が、最近私たちにより柔軟な別のソリューションに取り組ませるきっかけとなりました：[クラスターリンキング](https://github.com/emqx/emqx/pull/13126)です。設計目標は、外部リソースとの通信の信頼性と堅牢性と、特定のリージョンが関心を持つメッセージのみをルーティングする能力を組み合わせることでした。これにより、帯域幅とコンピューティングリソースの不必要な浪費を避けることができます。この機能は、今後のEMQX Enterprise 5.8.0リリースで登場する予定です。

## まとめ

結局のところ、いつものように、許容可能なトレードオフを選択することに帰着します。私たちが知る限り、光速を超える方法はないので、増加したレイテンシーのコストを支払わなければなりません。しかし、適切なデプロイメントモデルを選択し、ワークロードを最適化することで、それをより耐えられるものにすることはできます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
