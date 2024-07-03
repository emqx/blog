## はじめに

Datadog は、自動化されたインフラストラクチャ監視、アプリケーションパフォーマンス監視、ログ管理、リアルユーザー監視を提供するクラウドベースの可観測性およびセキュリティプラットフォームです。これらの機能をリアルタイムアプリケーションソリューションに統合することで、開発者はパフォーマンスと信頼性を簡単に監視、分析、最適化できます。

最近、EMQXは公式にDatadogと[統合](https://docs.datadoghq.com/integrations/emqx/)し、ユーザーがDatadogを使用してデバイスの接続性、メッセージスループット、レイテンシー、ノードのパフォーマンスに関連するメトリクスを収集できるようになりました。この統合により、ユーザーはサービスの現状を理解し、システムのパフォーマンスの問題をトラブルシューティングする能力が向上し、効率的で信頼性の高いIoTアプリケーションの開発が容易になります。

このブログでは、4つの簡単なステップでEMQXとDatadogを統合するプロセスをガイドします。

## ステップ1：Datadog Agentのインストール

まず、[Datadog](https://www.datadoghq.com/)アカウントを作成し、Datadogコンソールにログインします。

次に、EMQXがホストされているサーバーに[Datadog Agent](https://docs.datadoghq.com/getting_started/agent/)をインストールします。AgentはEMQXのメトリクスを収集し、Datadogクラウドに送信します。

EMQXクラスターが存在するサーバーまたはEMQXノードにアクセスできるサーバーにDatadog Agentをデプロイします。まだAgentをインストールしていない場合は、次の手順に従ってください：

1. メニューバーの **Integrations** → **Agent** に移動して、Agent インストール手順ページにアクセスします。

2. オペレーティングシステムのバージョンを選択し、提供される指示に従います。

   ![Integrations → Agent](https://assets.emqx.com/images/f5dc4443f90dc32752c60012042d0c48.png)

## ステップ2：DatadogにEMQX統合を追加する

EMQXは[Datadog統合](https://docs.datadoghq.com/integrations/emqx/)をすぐに使用できる状態で提供しており、以下の手順に従ってDatadogコンソールに簡単に組み込むことができます：

1. Datadogコンソールを開き、メニューバーの **Integrations** → **Integrations** に移動します。

2. **Search Integrations** ボックスに "EMQX" と入力して、同じ名前と作成者の統合を見つけます。

3. ポップアップボックスの右上隅にある **Install Integration** ボタンをクリックして、EMQX統合をDatadogに追加します。

   ![Click the Install Integration](https://assets.emqx.com/images/e2caea6a2bc01590b403b2c3bd271cbb.png)

4. インストールが完了したら、**Configure** タブに移動してEMQX統合の設定ガイドラインにアクセスします。必要な設定手順はDatadog Agent内で行われます。

   ![Configure tab](https://assets.emqx.com/images/a46f1e6438b018cbf461ae24567cfcde.png)

## ステップ3：Datadog AgentでEMQX統合を追加して有効にする

設定ガイドラインに従って、Datadog AgentにEMQX統合を追加し、EMQXメトリクスの収集と報告を設定します。

1. Datadog Agentがホストされているサーバーで次のコマンドを実行して、EMQX統合を追加します。このサンプルではバージョン1.1.0を使用していますが、常に最新のガイドラインで適切なバージョンを参照してください：

   ```
   datadog-agent integration install -t datadog-emqx==1.1.0
   ```

2. インストールが完了したら、Agent設定ファイルを変更してEMQX統合を有効にします：

   Agent設定ディレクトリ（通常は /opt/datadog-agent/etc/conf.d/）に移動します。このディレクトリ内にemqx.dディレクトリを見つけます。emqx.dディレクトリ内にconf.yaml.exampleというサンプル設定ファイルがあります。

   このファイルのコピーを同じディレクトリに作成し、conf.yamlにリネームします。conf.yamlファイルを編集し、次の設定項目を調整します：

   ```
   instances:
     - openmetrics_endpoint: http://localhost:18083/api/v5/prometheus/stats?mode=all_nodes_aggregated
   
   ```

   `openmetrics_endpoint`は、Datadog AgentがOpenMetrics形式でメトリクスデータを抽出するアドレスを指定します。この場合、EMQXのHTTP APIアドレスに設定されています。Datadog Agentがアクセス可能なアドレスに置き換えてください。

   APIでは、`mode`クエリパラメータを使用して取得するメトリクスの範囲を指定することもできます。各パラメータの意味は次のとおりです：

   統一されたビューのために、`mode=all_nodes_aggregated`オプションを使用します。これにより、Datadog制御がEMQXクラスタ全体の値を見ることができます。

   ![The meaning of each parameter](https://assets.emqx.com/images/90e6fd142c844c160d492c6f713265f2.png)

3. macOSで[Datadog Agentを再起動する](https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent)には、次の手順に従います：

   ```
   launchctl stop com.datadoghq.agent
   launchctl start com.datadoghq.agent
   ```

4. システムを再起動した後、次のコマンドを使用してEMQX統合が正常に有効になっているか確認します。"Instance ID: ... [OK]" が表示されれば、統合が正常に有効になっています。

   ```
   $ datadog-agent status | grep emqx -A 4
       emqx (1.1.0)
       ------------
         Instance ID: emqx:1865f3a06d300ccc [OK]
         Configuration Source: file:/opt/datadog-agent/etc/conf.d/emqx.d/conf.yaml
         Total Runs: 17
         Metric Samples: Last Run: 166, Total: 2,822
         Events: Last Run: 0, Total: 0
         Service Checks: Last Run: 1, Total: 17
         Average Execution Time : 43ms
         Last Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
         Last Successful Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
   ```

これで、Datadog Agentでの必要な設定はすべて完了しました。Agentは定期的にEMQXのランタイムデータを収集し、Datadogに送信します。次に、Datadogコンソールをチェックして、メトリクスが正しく収集されていることを確認しましょう。

## ステップ4：DatadogコンソールでEMQXメトリクスを表示する

Datadog AgentのEMQX統合は、ノードの状態、メッセージの状態、その他の詳細な可観測性メトリクスを表示する、すぐに使用できるダッシュボードチャートを提供します。以下の手順でそれを利用できます：

1. Datadogコンソールを開き、メニューバーの **Integrations** → **Integrations** に移動します。
2. インストールされたEMQX統合を見つけてクリックして開きます。
3. ポップアップボックス内の **Monitoring Resources** タブに切り替えて、**Dashboards** の下にある **EMQX Overview** チャートを開きます。

![Monitoring Resources tab](https://assets.emqx.com/images/330598b3ec6536a48a028143de23883c.png)

**チャートは以下の情報を提供します：**

- OpenMetrics Health：アクティブなメトリクスコレクターの数。
- Total Connections：接続の総数（切断されていてもセッションを維持しているものを含む）。
- NodeRunning：クラスター内の実行中のノードの数。
- Active Topics：現在アクティブなトピックの数。
- NodeStopped：クラスター内の停止したノードの数。
- Connection
  - Total：接続の総数（切断されていてもセッションを維持しているものを含む）。
  - Live：アクティブに維持されているTCP接続の数。
- Topic
  - Total：トピックの総数。
  - Shared：共有トピックの数。
- Session：セッションの総数。
- Erlang VM：Erlang仮想マシンのCPU、メモリ、キューの使用状況。
- Retainer & Delayed
  - Retained：保持されたメッセージの数。
  - Delayed：遅延メッセージの数。
- Message
  - Sent & Received：送受信されたメッセージのレート。
  - Delayed & Retained：遅延および保持されたメッセージのレート。
  - Publish & Delivered：メッセージの公開と配信のレート。
  - Delivery Dropped：ドロップされた配信メッセージの数。
- Client
  - Connected & Disconnected：接続の確立と終了のレート。
  - Sub & UnSub：サブスクリプションと解除のレート。
  - AuthN & AuthZ：認証と認可のレートに関する情報。
  - Delivery Dropped：ドロップされた配信メッセージの数。
- Mria：Mriaトランザクションの総数。

以下は一部のチャートのスクリーンショットです。値はEMQXの負荷とクライアントのアクティビティに基づいて動的に変化します。

![Metrics Overview](https://assets.emqx.com/images/4ff04f0ce8a1195c5dcc6026060b2cd6.png)

<center>Metrics Overview</center>



![Connection, Topic, and Session](https://assets.emqx.com/images/c45ccd37fb0dbaaf90951e071c92d565.png)

<center>Connection, Topic, and Session</center>

![The Rate of Sent and Received Messages, the Number of Retained/Delayed/Dropped Messages](https://assets.emqx.com/images/4be20e313d51ed7477d6117fa3c05b13.png)

<center>The Rate of Sent and Received Messages, the Number of Retained/Delayed/Dropped Messages</center>



![Client Event](https://assets.emqx.com/images/affbe7832fe71e29334c3e915c7744bc.png)

<center>Client Event</center>

## さらに運用保守をアップグレード

DatadogのEMQX統合に組み込まれたチャートは、主要なメトリクスの一部のみを示しています。[このドキュメント](https://docs.datadoghq.com/integrations/emqx/#metrics)を参照して、報告されるすべてのEMQXメトリクスにアクセスし、それに基づいて独自の監視チャートを作成することもできます。

次に、これらのメトリクスに基づいてDatadogでアラートルールを設定できます。特定のメトリクスが事前設定された閾値に達したり、異常な状況が発生したりした場合、Datadogは通知を送信して、必要な行動を迅速に取るよう促し、システム障害がビジネスに与える影響を最小限に抑えます。

## まとめ

このブログでは、EMQXとDatadogをシームレスに統合し、EMQXの運用状態をリアルタイムで監視する方法を紹介しました。EMQXの確立されたメトリクスとDatadogの強力な機能を活用することで、ユーザーは接続数、メッセージレート、ノードの状態などの重要な側面を追跡できます。潜在的な問題を迅速に特定することで、適時に是正措置を講じ、システムの安定性と信頼性を確保することができます。この記事が、Datadogを使用してEMQXを監視するユーザーにとって貴重な参考資料となることを願っています。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
