## Rustの紹介

Rustは、高性能、並行処理、メモリ安全性で知られるシステムレベルのプログラミング言語です。Mozillaによって開発されたRustは、現代のソフトウェア開発の優先言語の1つになることを目指しています。Rustの設計目標には、開発者の生産性とコードの品質を維持しながら、安全で並行性があり、効率的なプログラミング体験を提供することが含まれています。

Rustの主な特徴は次のとおりです。

- メモリ安全性：Rustは、所有権システムと借用チェッカーを通じてメモリ安全性を確保します。所有権システムは、コンパイル時に各値の所有権を追跡し、値が不要になったときにメモリを解放する責任があります。借用チェッカーは、コンパイル時にヌルポインタ参照やデータ競合などの一般的なメモリエラーを防ぎます。
- 並行性：Rustは、軽量な並行性プリミティブのセットを提供し、並行プログラムの作成を容易かつ安全にします。std::threadモジュールは、基本的なスレッドの作成と管理を提供し、std::syncモジュールは、ミューテックス、セマフォ、チャネルなどのさまざまな同期プリミティブを提供して、スレッド間の安全な通信とデータ共有を行います。
- パフォーマンス：Rustは、ゼロコストの抽象化と最小限のランタイムオーバーヘッドでパフォーマンスを優先します。インラインアセンブリ、ロックフリープログラミング、非同期プログラミングなどの高度な機能をサポートし、開発者が高性能なシステムレベルのアプリケーションとネットワークサービスを作成できるようにします。

要約すると、Rustは、システムプログラミングからネットワークサービス、組み込みデバイスから大規模な分散システムまで、さまざまなシナリオに適した強力で安全で高性能なプログラミング言語です。そのエコシステムは、活発なコミュニティとともに継続的に改善されており、開発者からますます好まれ、歓迎されるようになっています。

## RustベースのMQTTライブラリの選択

Rustでは、一般的に使用される[MQTTライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)はほとんどなく、rumqttとpaho-mqttが主な選択肢となっています。

### rumqtt

rumqttは、シンプルでロバストでパフォーマンスの高いことを目指して[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)標準を実装するために、rust-langで書かれたオープンソースのライブラリセットです。rumqttcとrumqttdが含まれます。

- rumqttc

  堅牢で効率的で使いやすいことを目指した純粋なrust[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)。このライブラリは、async（tokioを使用）イベントループによってバックアップされ、ユーザーがブローカーに対応してMQTTメッセージを送受信できるようにします。

- rumqttd

  Rumqttdは、Rustで書かれた高性能な[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)です。軽量で組み込み可能であり、コードでライブラリとして使用し、機能を拡張できることを意味します。

**特徴**：

rumqttは現代的な設計を採用しており、Rustの非同期プログラミングモデルに沿った非同期APIスタイルを提供しています。その軽量で高性能な設計により、リソースに制約のある環境でも優れた性能を発揮します。さらに、rumqttの簡潔で明確なAPI設計は、Rust言語の規則に準拠しているため、使いやすく理解しやすくなっています。

**選択の理由**：

- モダンなデザイン
- 軽量で高性能
- 簡潔なAPI
- アクティブなコミュニティサポート
- 柔軟な設定オプション

### paho-mqtt

paho-mqttは、Eclipse Pahoプロジェクトの一部であり、Rustを含む複数のプログラミング言語をサポートするクロスプラットフォームのMQTTクライアントライブラリです。MQTTv3.1とv5.0プロトコルをサポートし、安定性と成熟度で知られています。

**特徴**：

paho-mqttは、さまざまなプロジェクトで広く使用されており、コミュニティから積極的な貢献とサポートを受けています。さまざまなアプリケーションシナリオに適した同期および非同期のAPIスタイルを提供します。

このブログでは、MQTTライブラリの例としてrumqttcを選択します。

## RustでMQTTを使用する例プログラム

次のプログラムは、rumqttcライブラリを使用してMQTTクライアントを作成し、メッセージを公開/サブスクライブする方法を示しています。これらの例を通じて、クライアントの初期化、オプションの設定、MQTTサーバーへの接続、メッセージのパブリッシュ/サブスクライブ方法を学ぶことができます。

### 準備

この例では、接続のテストにEMQXが提供する無料のパブリックMQTTサーバーを使用します。サーバーアクセス情報は次のとおりです。

```
Broker: broker.emqx.io
TCP Port: 1883
Websocket Port: 8083
```

1. Rustプロジェクトを作成します。

   ```shell
   $ cargo new mqtt-rust-example
        Created binary (application) `mqtt-rust-example` package
   ```

2. Cargo.tomlを変更して依存関係を追加します。

   ```
   [dependencies]
   rumqttc = "0.24.0"
   pretty_env_logger = "0.4"
   tokio = { version = "1", features = ["full"] }
   ```

### MQTTメッセージの同期的なサブスクライブとパブリッシュ

この例の一部では、MQTTメッセージを同期的にサブスクライブおよびパブリッシュする方法を示します。

1. Cargo.tomlを変更します。

   ```toml
   [[bin]]
   name = "syncpubsub"
   path = "src/syncpubsub.rs"
   ```

2. プロジェクトのsrcフォルダにsyncpubsub.rsを作成し、次のコードを追加します。

   ```rust
   use rumqttc::{Client, LastWill, MqttOptions, QoS};
   use std::thread;
   use std::time::Duration;
   
   /*
    * これはプログラムのメイン関数です。この関数では、MQTTクライアントを初期化し、
    * 接続オプションとラストウィルメッセージを設定します。次に、クライアントと接続を作成し、
    * 新しいスレッドでパブリッシュ関数を呼び出します。次に、connection.iter()メソッドを使用して
    * 接続内の通知を反復処理し、各通知を処理します。
    */
   fn main() {
       // ロガーを初期化する
       pretty_env_logger::init();
   
       // MQTT接続オプションとラストウィルメッセージを設定する
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       let will = LastWill::new("hello/world", "good bye", QoS::AtMostOnce, false);
       mqttoptions
           .set_keep_alive(Duration::from_secs(5))
           .set_last_will(will);
       // MQTTクライアントと接続を作成し、新しいスレッドでパブリッシュ関数を呼び出す
       let (client, mut connection) = Client::new(mqttoptions, 10);
       thread::spawn(move || publish(client));
   
       // 接続内の通知を反復処理し、各通知を処理する
       for (i, notification) in connection.iter().enumerate() {
           match notification {
               Ok(notif) => {
                   println!("{i}. Notification = {notif:?}");
               }
               Err(error) => {
                   println!("{i}. Notification = {error:?}");
                   return;
               }
           }
       }   
   
       println!("Done with the stream!!");
   }
   
   /*
    * これはMQTTメッセージをパブリッシュするためのヘルパー関数です。この関数では、まず
    * 1秒間スリープしてから、トピックをサブスクライブします。
    * 次に、ループして0から9までの長さの10個のメッセージを送信します。
    * 各メッセージのQoSは少なくとも1回です。
    */
   fn publish(client: Client) {
       // トピックをサブスクライブする前に1秒待つ
       thread::sleep(Duration::from_secs(1));
       client.subscribe("hello/+/world", QoS::AtMostOnce).unwrap();
   
       // 0から9までの長さの10個のメッセージを送信し、各メッセージのQoSは少なくとも1回
       for i in 0..10_usize {
           let payload = vec![1; i]; 
           let topic = format!("hello/{i}/world");
           let qos = QoS::AtLeastOnce;
   
           client.publish(topic, qos, true, payload).unwrap();
       }
   
       thread::sleep(Duration::from_secs(1));
   }
   ```

3. コンパイルします。

   ```
   $ cargo build
   ```

   

4. syncpubsubを実行します。

   ```shell
   $ ./target/debug/syncpubsub
   0. Notification = Incoming(ConnAck(ConnAck { session_present: false, code: Success }))
   1. Notification = Outgoing(Subscribe(1))
   2. Notification = Outgoing(Publish(2))
   3. Notification = Outgoing(Publish(3))
   4. Notification = Outgoing(Publish(4))
   5. Notification = Outgoing(Publish(5))
   6. Notification = Outgoing(Publish(6))
   7. Notification = Outgoing(Publish(7))
   8. Notification = Outgoing(Publish(8))
   9. Notification = Outgoing(Publish(9))
   10. Notification = Outgoing(Publish(10))
   11. Notification = Outgoing(Publish(11))
   12. Notification = Incoming(Publish(Topic = hello/9/world, Qos = AtMostOnce, Retain = true, Pkid = 0, Payload Size = 9))
   13. Notification = Incoming(Publish(Topic = hello/8/world, Qos = AtMostOnce, Retain = true, Pkid = 0, Payload Size = 8))
   14. Notification = Incoming(Publish(Topic = hello/7/world, Qos = AtMostOnce, Retain = true, Pkid = 0, Payload Size = 7))
   15. Notification = Incoming(Publish(Topic = hello/6/world, Qos = AtMostOnce, Retain = true, Pkid = 0, Payload Size = 6))
   ...
   ```

### MQTTメッセージの非同期サブスクライブとパブリッシュ

この例の一部では、tokioライブラリを使用して非同期タスクを管理し、MQTTメッセージを非同期にサブスクライブおよびパブリッシュする方法を示します。

1. Cargo.tomlを変更します。

   ```toml
   [[bin]]
   name = "asyncpubsub"
   path = "src/asyncpubsub.rs"
   ```

2. プロジェクトのsrcフォルダにasyncpubsub.rsを作成し、次のコードを追加します。

   ```rust
   /*
    * このコードの行は、tokioライブラリからtaskとtimeモジュールをインポートしています。
    * これらは、非同期タスクの管理と時間関連の操作の処理に使用されます。
    */
   use tokio::{task, time};
   
   use rumqttc::{AsyncClient, MqttOptions, QoS};
   use std::error::Error;
   use std::time::Duration;
   
   /*
    * このマクロアノテーションは、tokioランタイムを使用していることを示しています。
    * current_threadは、非同期コードがシングルスレッドのコンテキストで実行されることを意味します。
    */
   #[tokio::main(flavor = "current_thread")]
   /*
    * これはプログラムのメイン関数であり、非同期関数です。この関数では、
    * まずMQTTクライアントを初期化し、接続オプションを設定します。
    * 次に、非同期クライアントとイベントループを作成し、タスクでrequests関数を呼び出します。
    * 最後に、イベントループを通じてイベントをポーリングし、それらを処理します。
    */
   async fn main() -> Result<(), Box<dyn Error>> {
       // ロガーを初期化する
       pretty_env_logger::init();
       // color_backtrace::install();
   
       // MQTT接続オプションを設定する
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       mqttoptions.set_keep_alive(Duration::from_secs(5));
       
       // 非同期MQTTクライアントとイベントループを作成した
       let (client, mut eventloop) = AsyncClient::new(mqttoptions, 10);
       /*
        * クロージャを含む非同期タスクを作成しました。
        * クロージャ内で、最初にrequests(client).awaitを呼び出します。 
        * メッセージのパブリッシュとサブスクライブ操作を実行し、
        * 次にtime::sleep(Duration::from_secs(3)).awaitを使用して
        * タスクを3秒間スリープします。
        */
       task::spawn(async move {
           requests(client).await;
           time::sleep(Duration::from_secs(3)).await;
       }); 
       
       loop {
           // イベントループ内の次のイベントを待機して取得します。
           let event = eventloop.poll().await;
           // 取得したイベントでパターンマッチングを実行して、そのタイプを判別する
           match &event {
               Ok(v) => {
                   println!("Event = {v:?}");
               }
               Err(e) => {
                   println!("Error = {e:?}");
                   return Ok(());
               }
           }
       }   
   }
   
   /*
    * これは、メッセージをパブリッシュおよびサブスクライブするための非同期関数です。この関数では、
    * トピックをサブスクライブし、1から10までのメッセージを1秒に1つずつ送信するループを実行します。
    * 最後に、120秒間スリープして、後続のイベントを処理します。
    */
   async fn requests(client: AsyncClient) {
       /*
        * MQTTサーバー上の特定のトピック（ "hello/world"）をサブスクライブするために使用されます。
        * Quality of Service（QoS）をAtMostOnceに指定し、最大1回のメッセージ配信を示します。
        */
       client
           .subscribe("hello/world", QoS::AtMostOnce)
           .await
           .unwrap();
   
       /*
        * "hello/world"トピックに10個のメッセージを送信します。各メッセージの長さは
        * 1から10まで増加し、間隔は1秒です。
        * 各メッセージのQuality of Service（QoS）はExactlyOnceです。
        */
       for i in 1..=10 {
           client
               .publish("hello/world", QoS::ExactlyOnce, false, vec![1; i]) 
               .await
               .unwrap();
       
           time::sleep(Duration::from_secs(1)).await;
       }
       
       time::sleep(Duration::from_secs(120)).await;
   }
   ```

3. コンパイルします。

   ```shell
   $ cargo build
   ```

4. asyncpubsubを実行します。

   ```shell
   $ ./target/debug/asyncpubsub
   Event = Incoming(ConnAck(ConnAck { session_present: false, code: Success }))
   Event = Outgoing(Subscribe(1))
   Event = Outgoing(Publish(2))
   Event = Incoming(SubAck(SubAck { pkid: 1, return_codes: [Success(ExactlyOnce)] }))
   Event = Outgoing(PubRel(2))
   Event = Incoming(PubRec(PubRec { pkid: 2 }))
   Event = Incoming(Publish(Topic = hello/world, Qos = AtMostOnce, Retain = false, Pkid = 0, Payload Size = 1))
   Event = Incoming(PubComp(PubComp { pkid: 2 }))
   Event = Outgoing(Publish(3))
   Event = Outgoing(PubRel(3))
   ...
   ```

## まとめ

rumqttに基づく上記の例は、簡単なサブスクリプションとパブリッシュのコードを示しています。rumqttは、[MQTT v5](https://www.emqx.com/en/blog/introduction-to-mqtt-5)とプロパティなど、他のMQTT機能もサポートしています。詳細については、[rumqttの例](https://github.com/bytebeamio/rumqtt/tree/main/rumqttc/examples)を参照してください。

以上で、Rustプログラミング言語とrumqttcライブラリを使用したMQTTの基本的な使用方法の紹介は完了です。MQTTはIoTアプリケーションで広く使用されている軽量メッセージングプロトコルであり、Rustの高性能と安全性と組み合わせることで、効率的で信頼性の高いMQTTベースのサービスを構築できます。

ここで紹介したサンプルコードを出発点として、実際のユースケースに合わせて機能を拡張していくことをおすすめします。また、rumqttドキュメントやコミュニティリソースを参照して、より高度なトピックを学ぶのも良いでしょう。RustとMQTTを組み合わせることで、IoTの世界に新たな可能性を切り開くことができるはずです。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
