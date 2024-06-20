## Introduction to Rust

Rust is a system-level programming language known for its high performance, concurrency, and memory safety. Developed by Mozilla, Rust aims to become one of the preferred languages for modern software development. Rust's design goals include providing a safe, concurrent, and efficient programming experience while maintaining developer productivity and code quality.

Key features of Rust include:

- Memory Safety: Rust ensures memory safety through its ownership system and borrow checker. The ownership system tracks the ownership of each value at compile time and is responsible for memory deallocation when values are no longer needed. The borrow checker prevents common memory errors like null pointer references and data races at compile time.
- Concurrency: Rust provides a lightweight set of concurrency primitives, making it easier and safer to write concurrent programs. Its std::thread module offers basic thread creation and management, while the std::sync module provides various synchronization primitives such as mutexes, semaphores, and channels for safe communication and data sharing between threads.
- Performance: Rust prioritizes performance with its zero-cost abstractions and minimal runtime overhead. It supports advanced features like inline assembly, lock-free programming, and asynchronous programming, enabling developers to write high-performance system-level applications and network services.

In summary, Rust is a powerful, safe, and high-performance programming language suitable for various scenarios, from system programming to network services, from embedded devices to large-scale distributed systems. Its ecosystem is continually improving, with an active community, making it increasingly favored and welcomed by developers.

## Choosing a Rust-Based MQTT Library

In Rust, there are few commonly used [MQTT libraries](https://www.emqx.com/en/mqtt-client-sdk), with rumqtt and paho-mqtt being the primary choices.

### rumqtt

rumqtt is an opensource set of libraries written in rust-lang to implement the [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) standard while striving to be simple, robust and performant. It includes rumqttc and rumqttd.

- rumqttc

  A pure rust [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) that strives to be robust, efficient, and easy to use. This library is backed by an async (using tokio) eventloop which enables users to send and receive MQTT messages in correspondence with a broker.

- rumqttd

  Rumqttd is a high-performance [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) written in Rust. It's lightweight and embeddable, meaning you can use it as a library in your code and extend the functionality.

**Features**: 

rumqtt adopts a modern design, offering an asynchronous API style that aligns with Rust's asynchronous programming model. Its lightweight and high-performance design makes it excel even in resource-constrained environments. Additionally, rumqtt's concise and clear API design conforms to Rust language conventions, making it easy to use and understand.

**Reasons for Choice**: 

- Modern design
- Lightweight and high performance
- Concise API
- Active community support
- Flexible configuration options

### paho-mqtt

paho-mqtt is part of the Eclipse Paho project, a cross-platform MQTT client library supporting multiple programming languages, including Rust. It supports MQTT v3.1 and v5.0 protocols and is known for its stability and maturity.

**Features**: 

paho-mqtt has been widely used in various projects and has received active contributions and support from the community. It provides both synchronous and asynchronous API styles suitable for different application scenarios.

In this blog, we choose rumqttc as the example MQTT library. 

## Example Programs of Using MQTT in Rust

The following programs demonstrate how to create MQTT clients using the rumqttc library and publish/subscribe to messages. Through these examples, you can learn how to initialize clients, set options, connect to MQTT servers, and publish/subscribe to messages.

### Preparation

The example uses the free public MQTT server provided by EMQX for testing connections. The server access information is as follows:

```
Broker: broker.emqx.io
TCP Port: 1883
Websocket Port: 8083
```

1. Create a Rust project:

   ```shell
   $ cargo new mqtt-rust-example
        Created binary (application) `mqtt-rust-example` package
   ```

1. Modify Cargo.toml to add dependencies:

   ```toml
   [dependencies]
   rumqttc = "0.24.0"
   pretty_env_logger = "0.4"
   tokio = { version = "1", features = ["full"] }
   ```

### Subscribing and Publishing MQTT Messages Synchronously

This part of the example demonstrates subscribing to and publishing MQTT messages synchronously.

1. Modify Cargo.toml:

   ```toml
   [[bin]]
   name = "syncpubsub"
   path = "src/syncpubsub.rs"
   ```

1. Create syncpubsub.rs in the src folder of the project and add the following code:

   ```rust
   use rumqttc::{Client, LastWill, MqttOptions, QoS};
   use std::thread;
   use std::time::Duration;
   
   /*
    * This is the main function of the program. In this function, we initialize an MQTT client,
    * set connection options and last will message. Then we create a client and a connection,
    * and call the publish function in a new thread. Next, we use connection.iter()
    * method to iterate through the notifications in the connection and handle each notification.
    */
   fn main() {
       // Initialize the logger
       pretty_env_logger::init();
   
       // Set MQTT connection options and last will message
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       let will = LastWill::new("hello/world", "good bye", QoS::AtMostOnce, false);
       mqttoptions
           .set_keep_alive(Duration::from_secs(5))
           .set_last_will(will);
       // Create MQTT client and connection, and call the publish function in a new thread
       let (client, mut connection) = Client::new(mqttoptions, 10);
       thread::spawn(move || publish(client));
   
       // Iterate through the notifications in the connection and handle each notification
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
    * This is a helper function for publishing MQTT messages. In this function, we first sleep
    * for one second, then subscribe to a topic. Then we loop and send ten messages with lengths
    * ranging from 0 to 9, with each message's QoS being at least once.
    */
   fn publish(client: Client) {
       // Wait for one second before subscribing to a topic
       thread::sleep(Duration::from_secs(1));
       client.subscribe("hello/+/world", QoS::AtMostOnce).unwrap();
   
   // Send ten messages with lengths ranging from 0 to 9, each message's QoS being at least once
       for i in 0..10_usize {
           let payload = vec![1; i]; 
           let topic = format!("hello/{i}/world");
           let qos = QoS::AtLeastOnce;
   
           client.publish(topic, qos, true, payload).unwrap();
       }
   
       thread::sleep(Duration::from_secs(1));
   }
   ```

1. Compile:

   ```shell
   $ cargo build
   ```

1. Execute syncpubsub:

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

### Subscribing and Publishing MQTT Messages Asynchronously

This part of the example demonstrates subscribing to and publishing MQTT messages asynchronously using the tokio library to manage asynchronous tasks.

1. Modify Cargo.toml:

   ```toml
   [[bin]]
   name = "asyncpubsub"
   path = "src/asyncpubsub.rs"
   ```

1. Create asyncpubsub.rs in the src folder of the project and add the following code:

   ```rust
   /*
    * This line of code imports the task and time modules from the tokio library,
    * which are used for managing asynchronous tasks and handling time-related operations.
    */
   use tokio::{task, time};
   
   use rumqttc::{AsyncClient, MqttOptions, QoS};
   use std::error::Error;
   use std::time::Duration;
   
   /*
    * This macro annotation indicates that we are using the tokio runtime,
    * where current_thread means our asynchronous code will run in a single-threaded context.
    */
   #[tokio::main(flavor = "current_thread")]
   /*
    * This is the main function of the program, which is an asynchronous function. In this function,
    * we first initialize an MQTT client and set connection options.
    * Then we create an asynchronous client and an event loop, and call the requests function in a task.
    * Finally, we poll events through the event loop and handle them.
    */
   async fn main() -> Result<(), Box<dyn Error>> {
       // Initialize the logger
       pretty_env_logger::init();
       // color_backtrace::install();
   
       // Set MQTT connection options
       let mut mqttoptions = MqttOptions::new("test-1", "broker.emqx.io", 1883);
       mqttoptions.set_keep_alive(Duration::from_secs(5));
   
       // Created an asynchronous MQTT client and event loop
       let (client, mut eventloop) = AsyncClient::new(mqttoptions, 10);
       /*
        * Created an asynchronous task containing a closure. 
        * Inside the closure, it first calls requests(client).await;
        * to perform message publishing and subscription operations,
        * then sleeps the task for 3 seconds using
        * time::sleep(Duration::from_secs(3)).await;
        */
       task::spawn(async move {
           requests(client).await;
           time::sleep(Duration::from_secs(3)).await;
       }); 
   
       loop {
           // Waits for and retrieves the next event in the event loop.
           let event = eventloop.poll().await;
           // Performs pattern matching on the retrieved event to determine its type
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
    * This is an asynchronous function for publishing and subscribing to messages. In this function,
    * we subscribe to a topic and loop through sending messages from 1 to 10,
    * one message per second. Finally, we sleep for 120 seconds to handle subsequent events.
    */
   async fn requests(client: AsyncClient) {
       /*
        * Used to subscribe to a specific topic ("hello/world") on the MQTT server,
        * specifying the Quality of Service (QoS) as AtMostOnce, indicating at most
        * once message delivery.
        */
       client
           .subscribe("hello/world", QoS::AtMostOnce)
           .await
           .unwrap();
   
       /*
        * Send 10 messages to the "hello/world" topic, with the length
        * of each message increasing from 1 to 10, with an interval of
        * 1 second. Each message has a Quality of Service (QoS) of ExactlyOnce.
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

1. Compile:

   ```shell
   $ cargo build
   ```

1. Execute asyncpubsub:

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

## Summary

The above examples based on rumqtt demonstrate simple subscription and publishing code. rumqtt also supports [MQTT v5](https://www.emqx.com/en/blog/introduction-to-mqtt-5) and properties, among other MQTT features. For more information, refer to the [rumqtt examples](https://github.com/bytebeamio/rumqtt/tree/main/rumqttc/examples).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
