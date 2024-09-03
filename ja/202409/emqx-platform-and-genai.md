## はじめに

人工知能は急速に進歩しており、特に大規模言語モデル（LLM）と生成AI（GenAI）が注目されています。これらの技術は、データ分析、意思決定、自動化に大きな利益をもたらし、運用コストを削減し、産業効率を向上させています。

大量のIoTデータを転送できる[EMQXプラットフォーム](https://www.emqx.com/ja)は、GenAIとシームレスに組み合わせることで新たな可能性を切り開きます。この強力な統合により、リアルタイムデータ処理、インテリジェントな異常検出、予測分析が可能になり、生のIoTデータを実用的な洞察に変換します。EMQXとGenAIを活用することで、企業はIoTアプリケーションを強化し、運用を最適化し、スマート製造から都市管理まで幅広い分野でイノベーションを推進することができます。

このブログでは、EMQXをGenAIと統合する方法を探り、実践的なデモでその可能性を示します。

## RAG + LLMソリューションの概要

生成AIと大規模言語モデルは、さまざまなアプリケーションで驚くべき能力を示しています。しかし、IoTシナリオに適用する際には、重要な課題に直面します：

1. リアルタイムデータへのアクセス不足：LLMは過去のデータで訓練されており、最新の情報を取り込むのに苦労します。
2. 幻覚は不正確または架空の情報を生成する可能性があり、事実に基づいた最新の洞察が必要なIoTコンテキストでは特に問題となります。

これらの課題に対処するために、検索拡張生成（RAG）とLLMを組み合わせたソリューションが登場しました。RAGは、知識ベースやリアルタイムデータソースから取得した関連性の高い最新情報をLLMに提供することで、LLMを強化する技術です。

RAG + LLMアプローチには以下のような利点があります：

1. **リアルタイムデータ統合**：RAGシステムはIoTデータストリームから現在の関連情報を取得します。
2. **精度の向上**：RAGは、LLMに事実に基づいたコンテキスト固有のデータを提供することで、幻覚を大幅に減少させます。
3. **コンテキストの理解**：このアプローチにより、AIシステムは、現在の実世界のデータに基づいた膨大な事前訓練された知識に基づいて応答を生成できます。

## EMQX プラットフォームが IoT 向けの効果的な RAG + LLM ソリューションを実現

EMQX は、IoT メッセージングプラットフォームの先駆者として、IoT 向けの効果的な RAG + LLM ソリューションを実現する上で重要な役割を果たします。大規模なリアルタイム IoT データを処理およびルーティングする能力は、強力な AI 駆動型 IoT システムを構築するための堅固な基盤を提供します：

1. **堅牢なデータ処理**: EMQX は大規模な IoT データストリームの処理に特化しており、GenAI アプリケーションの強固な基盤を提供します。そのルールエンジンにより、タイムリーな AI インサイトに不可欠なリアルタイムデータの効率的な変換とルーティングが可能になります。
2. **効率的な ETEL アーキテクチャ**: EMQX は、Extract, Transform, Embed, Load (ETEL) アーキテクチャを通じて RAG GenAI アプリの開発を効率化します。このアプローチは、IoT データを GenAI モデル用に準備する複雑さを軽減するのに役立ちます。例えば、受信した**汚れたデータ**を迅速にクリーンアップし、AI 分析のためのデータの有効性を維持します。
3. **多様なユースケースのサポート**: EMQX プラットフォームは、以下のような複雑なシナリオを効果的にサポートします：
   - マルチモーダルデータ統合による予測保守
   - 製造プロセスにおけるリアルタイムの異常検出
   - 生産レシピの動的最適化
   - 機器ログのセマンティック検索によるトラブルシューティングの高速化
4. **高性能**: EMQX は、高いデータスループットを必要とするシナリオで強力なデータ処理能力を発揮し、AI 駆動の意思決定を促進します。
5. **多様な統合**: EMQX の包括的なデータ統合機能により、様々なデータソースや AI サービスとのスムーズな接続が可能になり、GenAI アプリケーションのための統一されたデータパイプラインをサポートします。

EMQX プラットフォームを活用することで、組織は IoT エコシステム内でリアルタイムのインサイトとインテリジェントな相互作用を提供する GenAI ソリューションを効率的に展開し、複雑な産業課題に対処しながら開発プロセスを最適化することができます。

![Effective RAG + LLM Solutions for IoT](https://assets.emqx.com/images/3599ef5415f0401bda5425f24e0f08af.png)

## デモケース：スマート製造デバイスモニタリング

次に、EMQX と GenAI を使用して製造業務を改善する実践的な例を示します。EMQX を活用して、リアルタイムのデバイスモニタリングと予測保守機能を備えたインテリジェントファクトリーデモを作成します。

このデモの主要コンポーネントには以下が含まれます：

1. EMQX プラットフォーム：製造デバイスからリアルタイムの IoT データを受信および処理する中央メッセージングプラットフォームとして機能します。
2. Chroma：ベクトル化されたデバイスデータを効率的に保存および取得するためのベクターデータベース。
3. OpenAI Embedding モデル：デバイスデータをベクトル化するために使用されます。
4. OpenAI GPT モデル：インサイトと予測を生成するために使用されます。

### 実装手順

#### ステップ 1：EMQX プラットフォームで無料の EMQX インスタンスを取得する

まず、EMQX Enterprise をローカルにインストールして、スマート製造デモを開始します。EMQX Enterprise は、Kafka、RabbitMQ、MySQL、PostgreSQL、InfluxDB、TimescaleDB など、一般的に使用されるデータベースやストリーム処理ミドルウェアのサポートを含む豊富なデータ統合機能を備えているため、推奨されます。

以下のコマンドを使用して Docker で EMQX Enterprise をインストールできます：

```shell
docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.7.2
```

インストール後、EMQX ダッシュボードにアクセスします：

1. ブラウザで `<http://<your-host-address>:18083` を開きます
2. デフォルトのユーザー名とパスワードでログインします

EMQX にはベクターデータベースストレージと LLM 相互作用の組み込みサポートはありませんが、その強力な拡張機能を活用できます。HTTP をブリッジとして使用して、EMQX をカスタム RAG サーバーに接続します。

#### ステップ 2：RAG サーバーの構築

以下は、Python と FastAPI を使用した RAG サーバーの簡略版です。これはコードの主要部分のみであり、完全な実装ではないことに注意してください：

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
import chromadb
import openai

app = FastAPI()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("device_data")

openai.api_key = "your-openai-api-key"  # 実際の API キーに置き換えてください

@app.post("/process")
async def process_data(request: Request):
    data = await request.json()
    # データのベクトル化と保存
    embedding = openai.Embedding.create(input=str(data), model="text-embedding-ada-002")
    collection.add(
        embeddings=[embedding['data'][0]['embedding']],
        documents=[str(data)],
        ids=[f"doc_{len(collection.get()['ids'])}"]
    )
    return {"status": "processed"}

class ChatQuery(BaseModel):
    query: str
    system_template: str

@app.post("/chat")
async def chat(chat_query: ChatQuery):
    # 類似性検索と応答生成を実行
    embedding = openai.Embedding.create(input=chat_query.query, model="text-embedding-ada-002")
    results = collection.query(query_embeddings=[embedding['data'][0]['embedding']], n_results=5)
    context = "\n".join(results['documents'][0])

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": chat_query.system_template},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {chat_query.query}"}
        ]
    )
    return {"response": response.choices[0].message['content'].strip()}
```

- `/process` エンドポイントはデバイスデータを受信し、OpenAI の API を使用してエンベディングを作成し、Chroma ベクターデータベースに保存します。
- `/chat` エンドポイントはクエリとシステムテンプレートを受け取り、データベース内の類似データを検索し、取得されたコンテキストに基づいて OpenAI の ChatGPT を使用して応答を生成します。

このコードは、IoT データを処理し LLM を使用してインサイトを生成するための基本的なフレームワークを提供します。エラー処理の実装、適切な認証の実装、および本番環境での使用のための最適化を忘れないでください。

#### ステップ 3：EMQX を RAG サーバーに接続する

RAG サーバーを起動した後、EMQX で HTTP コネクタを作成します：

1. EMQX ダッシュボードで、**データ統合** -> **コネクタ** に移動します
2. **作成** をクリックし、**HTTP サーバー** を選択します
3. コネクタを設定します：
   - 名前：`RAG_server`
   - ベース URL：`http://your-rag-server-ip:8000`
4. **作成** をクリックしてコネクタを保存します

![Create an HTTP connector](https://assets.emqx.com/images/3dcf28eb85030c30d921f373c8b804b1.png)

#### ステップ 4：EMQX でのデータ統合フローの作成

スマート製造シナリオのデータ統合を迅速に設定するために、EMQX のフローデザイナーを使用します。工場データをフィルタリング、抽出し、ベクターデータベースに保存するフローを作成するには、以下の手順に従ってください：

1. EMQX ダッシュボードの **データ統合** -> **フローデザイナー** に移動します。

2. "作成" をクリックして新しいフローを開始します。"ベクターデータベースにデータを保存する" などの説明を追加します。

3. フローキャンバスには、ソース、処理、シンクの 3 つの主要セクションが表示されます。

4. ソースの場合：

   - "メッセージ" ノードをキャンバスにドラッグします。

   - 工場関連のすべてのメッセージをキャプチャするために、トピック `factory/#` をリッスンするように設定します。

     ![Flow Designer](https://assets.emqx.com/images/45600a98250993d6605e2d35fa588701.png)

5. 処理の場合：

   - "データ処理" ノードを追加し、メッセージソースに接続します。

   - データ処理ノードで 2 つのフィールドを設定します：このステップは、受信メッセージから必要な情報を抽出します。

     ![Data Processing](https://assets.emqx.com/images/ada2d1ee466f5fe5ed3b93fd396bb3ad.png)

6. シンクの場合：

   - "HTTP サーバー" ノードを追加し、データ処理ノードに接続します。

   - HTTP サーバーノードを設定します：

     - アクション：store_data_to_chroma

     - コネクタ：RAG_Server（先ほど作成した HTTP コネクタを選択）

     - URL パス：/process

     - メソッド：POST

     - ボディ：

       ```json
       {
         "data": ${data},
         "topic": "${original_topic}"
       }
       ```

   このステップは、処理されたデータを RAG サーバーに送信してベクトル化と保存を行います。

   ![Flows](https://assets.emqx.com/images/3aee576e9f7f167a56c883d9a22c02fb.png)

このフローは、工場トピックからのメッセージを自動的にキャプチャし、処理し、Chroma ベクターデータベースに保存するために RAG サーバーに送信します。

#### ステップ 5：EMQX でのクエリフローの作成

GenAI を使用してデバイスのステータスをクエリし、インサイトを生成するフローを作成するには、以下の手順に従ってください：

1. ソースの設定：

   - "メッセージ" ノードを追加して、トピック `query/#` をリッスンします。

     ![Set up the Source](https://assets.emqx.com/images/b8bcc21eac53e979351d1adcb18611ce.png)

2. データ処理ノードの追加：

   - メッセージソースに接続します。

   - メッセージペイロードからデバイス ID を取得します。

     ![Add a Data Processing node](https://assets.emqx.com/images/c1babb55148d8c38ea783c2d563bfa80.png)

3. 2 つの HTTP サーバーノードをシンクとして追加し、両方をデータ処理ノードに接続します：

   a. 最初の HTTP サーバー（check_device_status）：

   - アクション：check_device_status

   - コネクタ：RAG_Server

   - URL パス：/chat

   - メソッド：POST

   - ボディ：

     ```json
     {
       "query": "Provide a concise status update for device ${device_id}",
       "system_template": "You are an AI assistant for a smart factory..."
     }
     ```

   b. 2 番目の HTTP サーバー（data_trends）：

   - アクション：data_trends

   - コネクタ：RAG_Server

   - URL パス：/chat

   - メソッド：POST

   - ボディ：

     ```json
     {
       "query": "Predict future trends for device ${device_id} based on its historical data",
       "system_template": "You are an AI assistant for a smart factory..."
     }
     ```

     ![Flows](https://assets.emqx.com/images/e0e4acb64e55c22fe51d9e3e6538fe9b.png)

このフローは、**カスタムビルトのプロンプト**を組み込むことでデバイスクエリを強化します。"query/#"トピックをリッスンし、device_idを抽出し、RAGサーバーにリクエストを送信します。主な特徴は、フローのHTTPサーバーシンク内でカスタマイズされた**プロンプト**を構築する能力です。抽出されたdevice_idを事前定義されたテンプレートと組み合わせることで、これらのカスタムプロンプトはLLMを導いて、特定のコンテキストに応じた応答を生成します。このアプローチにより、ベクターデータベースからのデータに基づいてGenAIの力を活用し、デバイスのステータスと将来のトレンドに関する柔軟で的を絞ったクエリが可能になります。

### EMQX + RAGサーバーシステムのテスト

上記の手順に従って、EMQX + RAGサーバーシステムをセットアップしました。このシステムにより、デバイスデータをベクターデータベースに保存し、自然言語を使用してクエリを実行し、大規模言語モデルの力を活用することができます。

![EMQX + RAG Server system](https://assets.emqx.com/images/f005616469a1864b52d9391dbbdbaff2.png)

#### ステップ1：テストデータの送信

まず、MQTTXを使用して"factory"トピックにテストデータを送信します。このデータはベクターデータベースに保存されます。以下は送信するデータの例です：

```json
{
  "deviceId": "DEV6a_2",
  "timestamp": 1723191649992,
  "status": "maintenance",
  "maintenance": {
    "last": "2024-07-26T18:57:44.151Z",
    "next_scheduled": "2024-08-23T22:08:34.408Z"
  },
  "data": {
    "temperature": 76.6,
    "vibration": 2.24,
    "energy_consumption": 148.3,
    "production_data": {
      "rate": 10,
      "total_produced": 469
    },
    "quality_data": {
      "pass_rate": 0.92
    }
  },
  "log": "スケジュールされたメンテナンスが進行中。最後に記録された統計 - 温度：76.6°C、振動：2.24g。次回予定メンテナンス：2024-08-23T22:08:34.408Z"
}
```

MQTTXを使用して、このデータを"factory"トピックに送信します。ベクターデータベースにさまざまなデバイスの状態と読み取り値を入力するために、データを変えて複数のメッセージを送信することができます。

![MQTTX](https://assets.emqx.com/images/009b3d4756d42039ff823bf66e3ebcc4.png)

#### ステップ2：デバイスステータスのクエリ

次に、デバイスのステータスと予測についてシステムに問い合わせます。これを行うには、デバイスIDをペイロードとして"query"トピックにメッセージを送信します。例えば：

```json
Topic: query/device_status
Payload: {
  "device_id": "DEV6a_2"
}
```

![Querying Device Status](https://assets.emqx.com/images/7bdf91ad2887bdd739bf2978bb12b114.png)

#### ステップ3：結果の分析

クエリを送信した後、コンソール出力を確認するか、結果を表示するWebUIを作成します。2つの応答が表示されるはずです：

1. デバイスステータス分析は、デバイスの現在の状態の要約を提供します。

   ![device status analysis](https://assets.emqx.com/images/4dd47e768b3734b6c7816622b193d1a3.png)

   最後の実際のデータと比較すると、デバイスステータスレポートの内容が完全に正確であることがわかります。単位、カスタム値変換などを使用して、複雑で理解しにくいデータ構造をより読みやすい形式に変換しています。

2. データ予測は、過去のデータに基づいて潜在的な将来のトレンドに関する洞察を提供します。

   ![image.png](https://assets.emqx.com/images/42465f144db05b49ca5e5bc39e6a251a.png)

このセクションでは、過去のデータに基づいて潜在的な将来のトレンドに関する洞察を提供しています。例えば、温度は通常の操作中に60-70°C周辺で安定すると予想され、高い確信度を示しています。振動とエネルギー消費も分析されており、予測では振動は通常の操作中に6g未満に留まる可能性が高く、エネルギー消費は平均して約300単位になると示されています。

これらの予測は、保存されたベクターデータとLLMを組み合わせて生成されており、システムが将来の状況とトレンドを効果的に予測する能力を示しています。

これらの応答は、システムが保存されたベクターデータをLLMと組み合わせて、意味のある洞察を生成する方法を示しています。

### さらなる拡張

システムをさらに強化するために、結果を特定のMQTTトピックに転送したり、ユーザーフレンドリーなウェブインターフェースを開発したり、定期的な自動クエリを実装することを検討してください。これらの改善により、EMQXとGenAIの統合の可能性を最大限に活用した、より包括的なIoTモニタリングと予測ソリューションが作成されます。

## 将来の可能性

EMQXとGenAIをIoTアプリケーションに統合する探求を締めくくるにあたり、このアプローチが有望である一方で課題にも直面していることは明らかです。ChromaとHTTPブリッジを使用する現在の実装は、時系列データに理想的ではなく、高スループットのシナリオでパフォーマンスのボトルネックを引き起こす可能性があります。さらに、このソリューションは大量のカスタム開発を必要とし、アクセシビリティを制限する可能性があります。

しかし、これらの課題はEMQXにとってイノベーションの機会を提示しています。潜在的な最適化には、簡素化されたUIを通じてベクターデータベースやLLMサービスとのシームレスな統合を可能にする、ビルトインのデータ統合設定が含まれます。これらの強化により、IoTとGenAIの統合が大幅に合理化され、より広範なユーザーやユースケースに高度なAIアプリケーションがアクセス可能になる可能性があります。

現在の制限にもかかわらず、EMQXのスケーラビリティ、リアルタイム処理、柔軟な統合における中核的な強みは、IoTとAIの統合のための強力な基盤としての位置付けを確立しています。その堅牢なアーキテクチャ、強力なルールエンジン、強力なセキュリティ機能は、洗練されたAI駆動型IoTソリューションを構築するための堅固な基盤を提供します。

EMQXは、IoTとAIの統合の進化する景観において重要な役割を果たす準備ができています。プラットフォームの開発と改良を続ける中で、この旅に参加することをお勧めします。特定の要件、革新的なアイデア、あるいはIoTとGenAIの交差点での可能性を探求したいだけでも、私たちはお手伝いする準備ができています。[Contact Us](https://www.emqx.com/ja/contact)  にアクセスして、あなたの独自のシナリオでこれらの技術の可能性を最大限に活用する方法についてご相談ください。一緒に、IoTの可能性の境界を押し広げ、次世代のインテリジェントな接続システムを創造しましょ



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
