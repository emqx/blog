## Rust 简介

Rust 是一门系统级编程语言，以其卓越的性能、并发能力以及内存安全特性著称。Rust 由 Mozilla 推出，目标是在现代软件开发中提供一种安全高效的编程语言。其设计旨在提供安全、并发和高效的编程体验，同时保持开发效率和代码质量不受影响。

Rust 的核心特性包括：

- 内存安全：Rust 通过所有权系统和借用检查器确保内存安全。所有权系统在编译时追踪每个值的所有权，并负责管理内存释放。借用检查器防止空指针引用和数据竞争等常见的内存问题。
- 并发性：Rust 提供了一组轻量级的并发工具，让开发人员能够轻松编写安全的并发程序。通过 std::thread 模块，可以方便创建和管理线程，而 std::sync 模块则提供了如互斥锁、信号量和通道等同步原语，保证线程之间安全的数据共享和通信。
- 高性能：Rust 强调零成本抽象和极低的运行时开销。它支持内联汇编、无锁编程和异步编程等高级功能，帮助开发者编写高性能的系统应用和网络服务。

总的来说，Rust 是一门功能强大、安全可靠、高性能的编程语言，适用于广泛的应用场景，从嵌入式开发到大规模分布式系统，甚至网络服务等领域。随着其生态系统的不断完善和活跃的社区支持，Rust 正逐渐成为开发人员的热门选择。

## 选择基于 Rust 的 MQTT 库

在 Rust 生态系统中，有几种常见的 [MQTT 库](https://www.emqx.com/zh/mqtt-client-sdk)，其中最受欢迎的是 rumqtt 和 paho-mqtt。

### paho-mqtt

paho-mqtt 是 Eclipse Paho 项目的一部分，它是一个跨平台的 MQTT 客户端库，支持包括 Rust 在内的多种编程语言。paho-mqtt 支持 MQTT v3.1 和 v5.0 协议，以稳定和成熟著称。

**特点**：paho-mqtt 在众多项目中得到了广泛应用，并拥有活跃的社区支持。它提供了同步和异步 API，适用于多种应用场景。

### rumqtt

rumqtt 是一个用 Rust 编写的开源库，旨在实现 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 协议，具有简单、健壮和高性能的特点。该项目包括两个主要组件：rumqttc 和 rumqttd。

- rumqttc

  rumqttc 是一个纯 Rust 实现的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)，设计目标是稳健、高效且易于使用。它基于异步（使用 tokio）的事件循环，使开发者能够方便地发送和接收 MQTT 消息，与 MQTT Broker 进行通信。

- rumqttd

  rumqttd 是一个高性能的 Rust 实现的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，它的设计轻量且可嵌入，可以将其作为库集成到代码中，甚至扩展其功能。

**特点**：rumqtt 采用现代设计，提供符合 Rust 异步编程模型的异步 API。其轻量级和高性能的设计使其即使在资源有限的环境中也能表现出色。此外，rumqtt 的 API 设计简洁明了，遵循 Rust 的语言风格，易于使用和理解。

**选择 rumqtt 的理由**：

- 现代设计
- 轻量级且高性能
- 简洁的 API
- 活跃的社区支持
- 灵活的配置选项

在本文中，我们将使用 rumqttc 进行示例演示。

## 在 Rust 中使用 MQTT 的示例程序

以下示例将演示如何使用 rumqttc 库创建一个 MQTT 客户端，并实现消息的发布和订阅。通过这些示例，您将学习如何初始化客户端、设置选项、连接到 MQTT 服务器，以及发布/订阅消息。

### 准备工作

本示例使用 EMQX 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)进行测试，连接信息如下：

```
Broker：broker.emqx.io
TCP 端口：1883
Websocket 端口：8083
```

1. 创建一个新的 Rust 项目：

   ```shell
   $ cargo new mqtt-rust-example
        Created binary (application) `mqtt-rust-example` package
   ```

2. 修改 Cargo.toml 文件，添加所需的依赖项：

   ```
   [dependencies]
   rumqttc = "0.24.0"
   pretty_env_logger = "0.4"
   tokio = { version = "1", features = ["full"] }
   ```

### 同步订阅和发布 MQTT 消息

下面的内容展示了如何实现同步订阅和发布 MQTT 消息。

1. 修改 Cargo.toml：

   ```toml
   [[bin]]
   name = "syncpubsub"
   path = "src/syncpubsub.rs"
   ```

2. 在项目的 src 目录下创建 syncpubsub.rs 文件，并添加以下代码：

   ```rust
   use rumqttc::{Client, LastWill, MqttOptions, QoS};
   use std::thread;
   use std::time::Duration;
   
   /*
    * 这是程序的主函数。
    * 在该函数中，将初始化 MQTT 客户端、设置连接选项和遗嘱消息。
    * 然后，创建客户端和连接、并在新线程中调用发布函数。
    * 最后，使用 connection.iter() 方法遍历并处理接中的每个通知。
    */
   fn main() {
       // 初始化日志记录器
       pretty_env_logger::init();
   
       // 设置 MQTT 连接选项和遗嘱消息
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       let will = LastWill::new("hello/world", "good bye", QoS::AtMostOnce, false);
       mqttoptions
           .set_keep_alive(Duration::from_secs(5))
           .set_last_will(will);
       // 创建 MQTT 客户端和连接，并启动新线程进行消息发布
       let (client, mut connection) = Client::new(mqttoptions, 10);
       thread::spawn(move || publish(client));
   
       // 遍历并处理连接中的每个通知
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
    * 这是一个用于发布 MQTT 消息的辅助函数。
    * 在该函数中，首先休眠一秒钟，然后订阅一个主题。
    * 接着，循环发送 10 条长度从 0 到 9 不等的消息，每条消息的 QoS 都设置为“至少一次”。
    */
   fn publish(client: Client) {
       // 订阅主题前等待一秒
       thread::sleep(Duration::from_secs(1));
       client.subscribe("hello/+/world", QoS::AtMostOnce).unwrap();
   
   // 发送 10 条消息，长度从 0 到 9 不等，每条消息的 QoS 都设置为“至少一次”
       for i in 0..10_usize {
           let payload = vec![1; i]; 
           let topic = format!("hello/{i}/world");
           let qos = QoS::AtLeastOnce;
   
           client.publish(topic, qos, true, payload).unwrap();
       }
   
       thread::sleep(Duration::from_secs(1));
   }
   ```

3. 编译：

   ```shell
   $ cargo build
   ```

4. 运行 syncpubsub：

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

   
### 异步订阅和发布 MQTT 消息

下面的示例展示了如何使用 tokio 库有效管理异步任务，实现异步订阅和发布 MQTT 消息。

1. 修改 Cargo.toml：

   ```toml
   [[bin]]
   name = "asyncpubsub"
   path = "src/asyncpubsub.rs"
   ```

2. 在项目的 src 目录下创建 asyncpubsub.rs 文件，并添加以下代码：

   ```rust
   /*
    * 这行代码从 tokio 库导入了 task 和 time 模块，
    * 用于管理异步任务和处理与时间相关的操作。
    */
   use tokio::{task, time};
   
   use rumqttc::{AsyncClient, MqttOptions, QoS};
   use std::error::Error;
   use std::time::Duration;
   
   /*
    * 这个宏注解表明使用的是 tokio 运行时，
    * 其中 current_thread 表示异步代码将在单线程上下文中运行。
    */
   #[tokio::main(flavor = "current_thread")]
   /*
    * 这是程序的主函数，是一个异步函数。
    * 在这个函数中，首先初始化一个 MQTT 客户端并设置连接选项。
    * 然后，创建异步客户端和事件循环，并在任务中调用请求函数。
    * 最后，通过事件循环轮询并处理事件。
    */
   async fn main() -> Result<(), Box<dyn Error>> {
       // 初始化日志记录器
       pretty_env_logger::init();
       // color_backtrace::install();
   
       // 设置 MQTT 连接选项
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       mqttoptions.set_keep_alive(Duration::from_secs(5));
   
       // 创建异步 MQTT 客户端和事件循环
       let (client, mut eventloop) = AsyncClient::new(mqttoptions, 10);
     
       /*
        * 创建一个包含闭包的异步任务。
        * 在闭包内部，首先调用 requests(client).await；执行消息发布和订阅操作。
        * 然后，使用 time::sleep(Duration::from_secs(3)).await; 让任务休眠 3 秒。
        */
       task::spawn(async move {
           requests(client).await;
           time::sleep(Duration::from_secs(3)).await;
       }); 
   
       loop {
           // 在事件循环中等待并获取下一个事件。
           let event = eventloop.poll().await;
           // 对检索到的事件执行模式匹配，以确定其类型
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
    * 这是一个异步函数，用于发布和订阅消息。
    * 在此函数中，订阅一个主题，并循环发送长度从 1 到 10 的消息，每秒发送一条信息。
    * 最后，休眠 120 秒，再处理后续事件。
    */
   async fn requests(client: AsyncClient) {
      
       /*
        * 用于订阅 MQTT 服务器上的特定主题（"hello/world"）。
        * 指定服务质量（QoS）为 AtMostOnce，表示最多一次消息传递。
        */
       client
           .subscribe("hello/world", QoS::AtMostOnce)
           .await
           .unwrap();
       /*
        * 向“hello/world”主题发送 10 条消息，每条消息的长度从 1 到 10 递增，发送间隔为 1 秒。
        * 每条消息的服务质量（QoS）设置为 ExactlyOnce。
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

3. 编译：

   ```shell
   $ cargo build
   ```

4. 运行 asyncpubsub：

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

## 结语

通过以上基于 rumqttc 的示例，我们演示了如何实现简单的异步订阅和发布功能。除了基本的 MQTT 功能，rumqttc 还支持 [MQTT v5](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 的新特性，如用户属性等。了解更多信息，请参考 [rumqtt 示例](https://github.com/bytebeamio/rumqtt/tree/main/rumqttc/examples)。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
