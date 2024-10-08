## はじめに

IoT（Internet of Things）技術の急速な進化により、その応用範囲は継続的に拡大しています。しかし、IoTの本質はデータ伝送にあり、デバイス間の通信プロトコルの慎重かつ戦略的な選択が不可欠です。

MQTTとHTTPは、それぞれ固有の強みと適した環境を持つ2つの主要な通信プロトコルです。MQTTはIoT向けに特別に設計され、より適応性の高いアプローチと多数のIoT向け機能を提供します。一方、HTTPはMQTTよりも古く、IoT以外の幅広いアプリケーションで広く使用されており、ユーザーはより豊富な開発および運用経験を持っている可能性があります。

このブログでは、IoTの文脈におけるMQTTとHTTPの詳細な検討を行い、それぞれの特徴、適したシナリオ、実際の展開パフォーマンスを強調します。これらを比較・分析することで、読者はIoTシステムの効率性と信頼性を向上させるための最適な通信プロトコルの選択方法をより明確に理解できるでしょう。

## MQTTとは

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルで動作する軽量なメッセージングプロトコルで、IoTデバイスの複雑で不安定なネットワーク条件、および限られたメモリ、ストレージ、処理能力に対応するように特別に設計されています。最小限のコーディング要件で、ネットワーク接続されたデバイスにリアルタイムで信頼性の高いメッセージングサービスを提供します。

標準的なMQTTセットアップでは、通信が必要なすべてのクライアント（通常はハードウェアデバイスとアプリケーションサービス）が単一のMQTTサーバー（MQTTブローカー）と継続的なTCP接続を維持します。メッセージを送信するクライアント（パブリッシャー）とメッセージを受信するクライアント（サブスクライバー）の間に直接のリンクは必要ありません。MQTTサーバーがメッセージのルーティングと配信を処理します。

このプロセスの中核となるのは**トピック**の概念です。トピックはMQTTのメッセージルーティングの基礎となり、URLパスに似た構造を持ち、階層構造には`/`を使用します。例えば、`sensor/1/temperature`のような形式です。サブスクライバーは関心のあるトピックを購読し、パブリッシャーがそのトピックにメッセージを投稿すると、トピックの構造に従って転送されます。

MQTTトピックは複数のサブスクライバーが購読でき、サーバーはトピック固有のメッセージをすべてのサブスクライバーに転送します。同様に、トピックは複数のパブリッシャーを持つことができ、メッセージは到着順に転送されます。クライアントはパブリッシャーとサブスクライバーの両方の機能を持つことができ、トピックに基づいてメッセージの通信を可能にし、これによりMQTTは一対一、多対一、一対多の双方向通信をサポートできます。

## HTTPとは

HTTPは、リクエスト/レスポンスパラダイムに基づくアプリケーション層プロトコルで、従来のクライアント-サーバーモデルだけでなく、IoTアプリケーションにおいても重要な役割を果たします。

> 明確にするために、このブログの比較は従来のリクエスト/レスポンスモードのHTTPに特化しています。[WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)や[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)などのHTTPプロトコルの拡張は、この比較から除外されています。

標準的なHTTP実践では、クライアント（通常はブラウザやWebアプリケーション）がリソースの取得やデータの送信のためにサーバーにリクエストを開始します。リクエストを受信すると、サーバーは処理して適切に応答します。例えば、送信されたデータを保存して後のクライアントアクセスに備えるなどです。

HTTPはリソースの場所を示すために**URL**を使用し、MQTTがトピックを使用するのと似ています。例えば、`http://example.com/api/sensor`というHTTPリクエストURLは、`sensor/1/temperature`というMQTTトピックと同様の階層形式を持っています。

HTTPを介する各通信は異なるリクエストとレスポンスのプロセスを通じて行われるため、追加のオーバーヘッドが必要であり、2つのクライアントが直接通信できないため、リアルタイム性に欠けます。

## リソース消費の比較

MQTTとHTTPは、多くのIoTハードウェアデバイスや組み込みシステムでサポートされている簡単なプロトコルです。通常、そのリソースフットプリントとランタイムメモリは使用を制限するものではありません。しかし、MQTTはIoT特有の設計哲学と機能を持つため、長期的な使用ではよりリソース効率が高い傾向があります。

まず、MQTTは接続性の観点でオーバーヘッドが低くなっています。プロトコルの追加消費を最小限に抑え、メッセージヘッダーは2バイトという小ささにすることができます。接続確立のためのハンドシェイクプロセスは比較的単純で、帯域幅の限られたネットワークでも安定した動作を保証します。

接続が確立されると、クライアントとサーバー間で長時間維持でき、複数のメッセージが同じ接続を通過できます。これにより、頻繁な接続の確立と終了に関連するコストが大幅に削減されます。例えば、"HelloWorld"というメッセージを`topic/1`というトピックにパブリッシュすると、以下のようなパケット情報になります：

| **フィールド** | **サイズ（バイト）** | **説明**           |
| :------------- | :------------------- | :----------------- |
| 固定ヘッダー   | 1                    | 0b0011xxxxに設定   |
| トピック長     | 2                    | 0x00 0x08          |
| トピック       | 9                    | "topic/1"          |
| メッセージ長   | 2                    | "HelloWorld"の長さ |
| メッセージ内容 | 10                   | "HelloWorld"       |
|                | 合計: 24             |                    |

対照的に、HTTPは各リクエスト-レスポンスサイクルごとに接続の確立と終了が必要であり、これにより追加のサーバーリソース消費が発生します。HTTPは比較的複雑で、より大きなメッセージヘッダーを持ちます。ステートレスプロトコルであるため、クライアントは各接続で追加の識別情報を持つ必要があり、これによりさらに帯域幅の使用が増加します。

例えば、"HelloWorld"という内容を`http://localhost:3000/topic`というURLに、識別情報なしで送信すると、以下のようなパケット情報になります：

| **フィールド** | **サイズ（バイト）** | **説明**                 |
| :------------- | :------------------- | :----------------------- |
| リクエスト行   | 17                   | POST /topic HTTP/1.1     |
| ホスト         | 20                   | Host: localhost:3000     |
| Content-Type   | 24                   | Content-Type: text/plain |
| Content-Length | 18                   | Content-Length: 10       |
| 空行           | 2                    | ヘッダーと本文を区切る   |
| リクエスト本文 | 10                   | "HelloWorld"             |
|                | 合計: 91 バイト      |                          |

**まとめ：**

- MQTTは接続オーバーヘッドが低く、接続確立が簡単で、パケットヘッダーが最小限であり、頻繁な通信や持続的な接続が必要なシナリオに適しています。
- 一方、HTTPは各リクエスト-レスポンスサイクルごとに接続の確立と終了が必要で、メッセージヘッダーも大きいため、特に帯域幅が制限された環境では、伝送の遅延や負荷が増大する可能性があります。

パケットサイズと接続オーバーヘッドの観点から、MQTTは通常HTTPよりも優れており、特に頻繁な通信、持続的な接続、または帯域幅が制限された環境での操作が必要なIoTコンテキストで有効です。

## セキュリティの比較

MQTTとHTTPは両方ともTCPベースのプロトコルであり、セキュリティに重点を置いて設計されています。

**SSL/TLS暗号化**

両プロトコルともSSL/TLS暗号化を用いた安全な通信をサポートしています：

- これにより、転送中のデータの機密性と整合性が確保されます。
- データの傍受、改ざん、偽造を防ぎます。

**様々な認証と認可メカニズム**

- MQTTはユーザー名/パスワード認証、JWT認証の拡張サポート、クライアント-サーバー間のX.509証明書認証を提供します。MQTTサーバーの機能に応じて、トピックベースのパブリッシュ/サブスクライブ権限チェックなどの認可も含めることができます。
- HTTPはより広範なオプションを提供し、Basic認証、トークン認証、OAuth等が含まれます。リソースへのアクセスはアプリケーション層のメカニズムを通じて制御でき、アクセストークン、セッション管理などを利用してより堅牢なアクセス制御を実現できます。

## IoT機能の比較

MQTTプロトコルはIoT向けに特別に設計されており、IoTシナリオに適した一連の機能を備えています。これにより、安定で信頼性の高いデバイス通信とリアルタイムデータ転送が可能となり、様々なビジネスコンテキストの要求を満たします。

**再接続と永続セッション**

MQTTは永続的な接続と再接続をサポートし、不安定なネットワーク状況下でもデバイスとサーバー間の一貫した通信を保証します。クライアントは永続セッションを確立するオプションがあり、再接続時にこれを復元してメッセージの損失を防ぐことができます。

**サービス品質（QoS）レベル**

MQTTは3つのQoSレベルを提供します：

- **QoS 0**：最大1回のメッセージ配信で、損失の可能性があります。
- **QoS 1**：少なくとも1回の配信を保証しますが、メッセージの重複の可能性があります。
- **QoS 2**：正確に1回の配信を保証し、メッセージの損失や重複はありません。

クライアントは、信頼性の高いメッセージ配信に対する特定のニーズに合わせて適切なQoSレベルを選択できます。

[**共有サブスクリプション**](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription)

複数のクライアントが同じトピックを購読し、同一のメッセージを受信できます。これは、複数のデバイス間でデータ共有やイベント購読が必要なシナリオに理想的です。

[**保持メッセージ**](https://www.emqx.com/en/blog/mqtt5-features-retain-message)

サーバーは特定のトピックの最新メッセージを保持し、新しいサブスクライバーに即座に配信することができ、最新の情報を確実に受け取ることができます。

[**ラストウィルメッセージ**](https://www.emqx.com/en/blog/use-of-mqtt-will-message)

クライアントは予期せず切断された場合にサーバーが公開する「ラストウィル」メッセージを設定でき、他のサブスクライバーに切断を通知します。

[**メッセージ有効期限**](https://www.emqx.com/en/blog/mqtt-message-expiry-interval)

メッセージに有効期限を設定でき、指定された時間内に消費されることを保証し、古いメッセージがシステムに負担をかけるのを防ぎます。

HTTPはWebアプリケーションで広く採用されているプロトコルですが、ユーザーは成熟したツールチェーンと機能設計経験に基づいてIoT固有の機能の一部を実装できますが、追加の開発作業が必要です。MQTTの本質的な設計は、多数のIoTに適した機能を統合しているため、開発コストを削減し通信効率を向上させることができ、IoTアプリケーションにより適しています。

## 比較分析

要約すると、MQTTとHTTPは通信モデルとIoT中心の属性に大きな違いがあります：

- MQTTはパブリッシュ-サブスクライブモデルで動作し、双方向通信を可能にしますが、HTTPはリクエスト-レスポンスモデルに従います。
- MQTTではメッセージがリアルタイムでプッシュされますが、HTTPではデータの更新を取得するためにポーリングが必要です。
- MQTTはステートフルで、接続コンテキストを維持しますが、HTTPはステートレスです。
- MQTTは異常切断を処理し、スムーズに回復できますが、HTTPにはこの機能がありません。
- MQTTには多様な組み込みIoT機能が備わっていますが、HTTPの設計にはこの特定の焦点がありません。

これらの違いはIoTコンテキストでの適用可能性に重要な意味を持ちます：

- **リアルタイム通信：** MQTTは高いリアルタイム応答性が求められるシナリオで優れています。そのパブリッシュ-サブスクライブモデルにより、デバイスはリクエストを待たずに即座にサーバーや他のデバイスにメッセージをプッシュできます。これにより、MQTTはセンサーデータのリアルタイムモニタリングやデバイスの即時制御など、迅速な応答が重要な場面に理想的です。
- **軽量で頻繁な通信：** 帯域幅とリソースが限られた環境では、MQTTは通常HTTPよりも効率的です。MQTTは頻繁な接続セットアップを避け、小さなメッセージヘッダーを使用することで通信オーバーヘッドを最小限に抑えます。対照的に、HTTPの同期リクエスト-レスポンスモデルはそれほど効率的ではなく、各対話に完全なリクエストとレスポンスヘッダーが必要であり、帯域幅とリソースを浪費する可能性があります。
- **ネットワーク変動のあるシナリオ：** MQTTはクライアントとサーバー間の永続的な接続を維持し、接続の中断から回復できます。ネットワークが切断されても、MQTTは再接続時に通信を再開できます。HTTPはステートレスであるため、各通信を独立して処理し、同様の方法で切断から回復することはできません。

## もう一つの考察：MQTTとHTTPの統合

IoTデバイスに最適なプロトコルについて探ってきましたが、実際には複雑なIoTアプリケーションはハードウェア、クライアント、ビジネスプロセスの組み合わせを含むことがよくあります。MQTTとHTTPは、IoTとより広範なインターネットで最も広く使用されている2つのプロトコルとして、多くのシナリオで互いに補完し合い、システムの効率性と柔軟性を向上させることができます。

例えば、典型的なIoV（Internet of Vehicles）アプリケーションでは、HTTPはユーザーとの対話に適しています。ユーザーがアプリの「ドアを開ける」ボタンを使ってガレージの車を制御する場合を想像してみてください。この動作はアプリとサーバー間の双方向通信ではなく、HTTPを使用することでより複雑で柔軟なセキュリティと権限チェックが可能になります。一方、サーバーと車両間の通信にはリアルタイムの双方向通信が必要です：車両はユーザーの操作に迅速に応答する必要があります。

車両は定期的にMQTTを通じてステータスを報告し、サーバーがそれを記録します。ユーザーがこの情報を必要とする場合、アプリはHTTPを使用してそれを取得します。

世界をリードするMQTTブローカーであるEMQXは、MQTTプロトコルとHTTPプロトコルを容易かつ柔軟に統合することでこのプロセスを可能にします。

**HTTP → MQTT：**

アプリケーションシステムは、EMQXが提供するAPIを呼び出すことで、HTTPリクエストを特定のデバイスに送信されるMQTTメッセージに変換できます。これにより、システムはデバイスに制御コマンドや通知を送信できます。

```shell
curl -X POST 'http://localhost:18083/api/v5/publish' \
  -H 'Content-Type: application/json' \
  -u '<appkey>:<secret>'
  -d '{
  "payload_encoding": "plain",
  "topic": "cmd/{CAR_TYPE}/{VIN}",
  "qos": 1,
  "payload": "{ \"oper\": \"unlock\" }",
  "retain": false
}'
```

**MQTT → HTTP：**

デバイスがEMQXにMQTTメッセージを送信すると、Webhook機能がこのメッセージをHTTPサーバーに転送し、デバイスデータを即座にアプリケーションシステムに伝送できます。

![MQTT → HTTP](https://assets.emqx.com/images/6cd9b05a099b1a6063efc2e29ab3886d.png)

設定インターフェースは以下のようになります：

![Create webhook](https://assets.emqx.com/images/d2b7002a90294a511e0931d034c2f7a4.png)

EMQXの将来のバージョンでは、このプロセスをさらに強化し、リアルタイムMQTTメッセージを統合されたメッセージキューとストリームに保存し、ユーザーがHTTP経由でこれらのメッセージを消費できるようにする予定です。これにより、複雑なIoTシナリオをよりよくサポートし、より堅牢なメッセージ処理機能を提供します。

## まとめ

最終的に、MQTTとHTTPの選択は、特定のアプリケーションのニーズとシナリオの特性に依存します。リアルタイムの双方向通信と低リソース消費が必要な場合は、MQTTが理想的です。クライアントのデータ収集と送信、サーバーからのデータの積極的な取得、または既存のWebインフラストラクチャの活用など、単純なリクエスト/レスポンスのやり取りには、HTTPがより適切です。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
