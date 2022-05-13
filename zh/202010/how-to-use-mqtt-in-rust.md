[Rust](https://www.rust-lang.org/zh-CN/)  是由 Mozilla 主导开发的通用、编译型编程语言。该语言的设计准则为：安全、并发、实用，支持 [函数式](https://zh.wikipedia.org/wiki/函數程式語言)、[并发式](https://zh.wikipedia.org/wiki/演员模型)、[过程式](https://zh.wikipedia.org/wiki/程序編程)以及[面向对象](https://zh.wikipedia.org/wiki/面向对象程序设计)的编程风格。Rust 速度惊人且内存利用率极高。由于没有运行时和垃圾回收，它能够胜任对性能要求特别高的服务，可以在嵌入式设备上运行，还能轻松和其他语言集成。Rust 丰富的类型系统和所有权模型保证了内存安全和线程安全，让您在编译期就能够消除各种各样的错误。

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。

本文主要介绍如何在 Rust 项目中使用 **paho-mqtt** 客户端库 ，实现客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。



## 项目初始化

本项目使用 Rust 1.44.0 进行开发测试，并使用 Cargo 1.44.0 包管理工具进行项目管理，读者可用如下命令查看当前的 Rust 版本。

```bash
~ rustc --version
rustc 1.44.0 (49cae5576 2020-06-01)
```

### 选择 MQTT 客户端库

paho-mqtt 是目前 Rust 中，功能完善且使用较多的 MQTT 客户端，最新的 `0.7.1` 版本支持 MQTT v5、3.1.1、3.1，支持通过标准 TCP、SSL / TLS、WebSockets 传输数据，QoS 支持 0、1、2 等。

### 初始化项目

执行以下命令创建名为 `mqtt-example` 的 Rust 新项目。

```bash
~ cargo new mqtt-example
    Created binary (application) `mqtt-example` package
```

编辑项目中的 `Cargo.toml` 文件，在 `dependencies` 中添加 `paho-mqtt` 库的地址，以及指定订阅、发布代码文件对应的二进制文件。

```toml
[dependencies]
paho-mqtt = { git = "https://github.com/eclipse/paho.mqtt.rust.git", branch = "master" }

[[bin]]
name = "sub"
path = "src/sub/main.rs"

[[bin]]
name = "pub"
path = "src/pub/main.rs"
```



## Rust MQTT 的使用

### 创建客户端连接

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为测试连接的 MQTT 服务器，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

### 配置 MQTT Broker 连接参数

配置 MQTT Broker 连接地址(包括端口)、topic (这里我们配置了两个 topic )，以及客户端 id。

```rust
const DFLT_BROKER:&str = "tcp://broker.emqx.io:1883";
const DFLT_CLIENT:&str = "rust_publish";
const DFLT_TOPICS:&[&str] = &["rust/mqtt", "rust/test"];
```

### 编写 MQTT 连接代码

编写 MQTT 连接代码，为了提升使用体验，可在执行二进制文件时通过命令行参数的形式传入连接地址。通常我们需要先创建一个客户端，然后将该客户端连接到 `broker.emqx.io`。

```rust
let host = env::args().nth(1).unwrap_or_else(||
    DFLT_BROKER.to_string()
);

// Define the set of options for the create.
// Use an ID for a persistent session.
let create_opts = mqtt::CreateOptionsBuilder::new()
    .server_uri(host)
    .client_id(DFLT_CLIENT.to_string())
    .finalize();

// Create a client.
let cli = mqtt::Client::new(create_opts).unwrap_or_else(|err| {
    println!("Error creating the client: {:?}", err);
    process::exit(1);
});

// Define the set of options for the connection.
let conn_opts = mqtt::ConnectOptionsBuilder::new()
    .keep_alive_interval(Duration::from_secs(20))
    .clean_session(true)
    .finalize();

// Connect and wait for it to complete or fail.
if let Err(e) = cli.connect(conn_opts) {
    println!("Unable to connect:\n\t{:?}", e);
    process::exit(1);
}
```

### 发布消息

这里我们总共发布五条消息，根据循环的奇偶性，分别向 `rust/mqtt`、 `rust/test` 这两个主题发布。

```rust
for num in 0..5 {
    let content =  "Hello world! ".to_string() + &num.to_string();
    let mut msg = mqtt::Message::new(DFLT_TOPICS[0], content.clone(), QOS);
    if num % 2 == 0 {
        println!("Publishing messages on the {:?} topic", DFLT_TOPICS[1]);
        msg = mqtt::Message::new(DFLT_TOPICS[1], content.clone(), QOS);
    } else {
        println!("Publishing messages on the {:?} topic", DFLT_TOPICS[0]);
    }
    let tok = cli.publish(msg);

			if let Err(e) = tok {
					println!("Error sending message: {:?}", e);
					break;
			}
}
```

### 订阅消息

在客户端连接之前，需要先初始化消费者。这里我们会循环处理消费者中的消息队列，并打印出订阅的 topic 名称及接收到的消息内容。

```rust
fn subscribe_topics(cli: &mqtt::Client) {
    if let Err(e) = cli.subscribe_many(DFLT_TOPICS, DFLT_QOS) {
        println!("Error subscribes topics: {:?}", e);
        process::exit(1);
    }
}

fn main() {
  	...
    // Initialize the consumer before connecting.
    let rx = cli.start_consuming();
  	...
    // Subscribe topics.
    subscribe_topics(&cli);

    println!("Processing requests...");
    for msg in rx.iter() {
        if let Some(msg) = msg {
            println!("{}", msg);
        }
        else if !cli.is_connected() {
            if try_reconnect(&cli) {
                println!("Resubscribe topics...");
                subscribe_topics(&cli);
            } else {
                break;
            }
        }
    }
  	...
}
```



## 完整代码

### 消息发布代码

```rust
use std::{
    env,
    process,
    time::Duration
};

extern crate paho_mqtt as mqtt;

const DFLT_BROKER:&str = "tcp://broker.emqx.io:1883";
const DFLT_CLIENT:&str = "rust_publish";
const DFLT_TOPICS:&[&str] = &["rust/mqtt", "rust/test"];
// Define the qos.
const QOS:i32 = 1;

fn main() {
    let host = env::args().nth(1).unwrap_or_else(||
        DFLT_BROKER.to_string()
    );

    // Define the set of options for the create.
    // Use an ID for a persistent session.
    let create_opts = mqtt::CreateOptionsBuilder::new()
        .server_uri(host)
        .client_id(DFLT_CLIENT.to_string())
        .finalize();

    // Create a client.
    let cli = mqtt::Client::new(create_opts).unwrap_or_else(|err| {
        println!("Error creating the client: {:?}", err);
        process::exit(1);
    });

    // Define the set of options for the connection.
    let conn_opts = mqtt::ConnectOptionsBuilder::new()
        .keep_alive_interval(Duration::from_secs(20))
        .clean_session(true)
        .finalize();

    // Connect and wait for it to complete or fail.
    if let Err(e) = cli.connect(conn_opts) {
        println!("Unable to connect:\n\t{:?}", e);
        process::exit(1);
    }

    // Create a message and publish it.
    // Publish message to 'test' and 'hello' topics.
    for num in 0..5 {
        let content =  "Hello world! ".to_string() + &num.to_string();
        let mut msg = mqtt::Message::new(DFLT_TOPICS[0], content.clone(), QOS);
        if num % 2 == 0 {
            println!("Publishing messages on the {:?} topic", DFLT_TOPICS[1]);
            msg = mqtt::Message::new(DFLT_TOPICS[1], content.clone(), QOS);
        } else {
            println!("Publishing messages on the {:?} topic", DFLT_TOPICS[0]);
        }
        let tok = cli.publish(msg);

				if let Err(e) = tok {
						println!("Error sending message: {:?}", e);
						break;
				}
    }


    // Disconnect from the broker.
    let tok = cli.disconnect(None);
    println!("Disconnect from the broker");
    tok.unwrap();
}
```

### 消息订阅代码

为了提升使用体验，消息订阅做了断开重连的处理，并在重新建立连接后对主题进行重新订阅。

```rust
use std::{
    env,
    process,
    thread,
    time::Duration
};

extern crate paho_mqtt as mqtt;

const DFLT_BROKER:&str = "tcp://broker.emqx.io:1883";
const DFLT_CLIENT:&str = "rust_subscribe";
const DFLT_TOPICS:&[&str] = &["rust/mqtt", "rust/test"];
// The qos list that match topics above.
const DFLT_QOS:&[i32] = &[0, 1];

// Reconnect to the broker when connection is lost.
fn try_reconnect(cli: &mqtt::Client) -> bool
{
    println!("Connection lost. Waiting to retry connection");
    for _ in 0..12 {
        thread::sleep(Duration::from_millis(5000));
        if cli.reconnect().is_ok() {
            println!("Successfully reconnected");
            return true;
        }
    }
    println!("Unable to reconnect after several attempts.");
    false
}

// Subscribes to multiple topics.
fn subscribe_topics(cli: &mqtt::Client) {
    if let Err(e) = cli.subscribe_many(DFLT_TOPICS, DFLT_QOS) {
        println!("Error subscribes topics: {:?}", e);
        process::exit(1);
    }
}

fn main() {
    let host = env::args().nth(1).unwrap_or_else(||
        DFLT_BROKER.to_string()
    );

    // Define the set of options for the create.
    // Use an ID for a persistent session.
    let create_opts = mqtt::CreateOptionsBuilder::new()
        .server_uri(host)
        .client_id(DFLT_CLIENT.to_string())
        .finalize();

    // Create a client.
    let mut cli = mqtt::Client::new(create_opts).unwrap_or_else(|err| {
        println!("Error creating the client: {:?}", err);
        process::exit(1);
    });

    // Initialize the consumer before connecting.
    let rx = cli.start_consuming();

    // Define the set of options for the connection.
    let lwt = mqtt::MessageBuilder::new()
        .topic("test")
        .payload("Consumer lost connection")
        .finalize();
    let conn_opts = mqtt::ConnectOptionsBuilder::new()
        .keep_alive_interval(Duration::from_secs(20))
        .clean_session(false)
        .will_message(lwt)
        .finalize();

    // Connect and wait for it to complete or fail.
    if let Err(e) = cli.connect(conn_opts) {
        println!("Unable to connect:\n\t{:?}", e);
        process::exit(1);
    }

    // Subscribe topics.
    subscribe_topics(&cli);

    println!("Processing requests...");
    for msg in rx.iter() {
        if let Some(msg) = msg {
            println!("{}", msg);
        }
        else if !cli.is_connected() {
            if try_reconnect(&cli) {
                println!("Resubscribe topics...");
                subscribe_topics(&cli);
            } else {
                break;
            }
        }
    }

    // If still connected, then disconnect now.
    if cli.is_connected() {
        println!("Disconnecting");
        cli.unsubscribe_many(DFLT_TOPICS).unwrap();
        cli.disconnect(None).unwrap();
    }
    println!("Exiting");
}
```



## 运行与测试

### 编译二进制文件

执行以下命令，会在 `mqtt-example/target/debug` 目录下生成消息订阅、发布对应的 `sub`、`pub` 二进制文件。

```bash
cargo build
```

![rustmqttbin.png](https://assets.emqx.com/images/7e95c531f0a3534bb48dcb9f17b778c6.png)

### 消息订阅

执行 `sub` 二进制文件，等待消费发布。

![rustmqttsub1.png](https://assets.emqx.com/images/bb040cf5a869a301023e7167895b4d4a.png)

### 消息发布

执行 `pub` 二进制文件，可以看到分别往 `rust/test` 、`rust/mqtt` 这两个主题发布了消息。

![rustmqttpub.png](https://assets.emqx.com/images/28949361d916b71fb10f083852a9bbe1.png)
同时在消息订阅中可看到发布的消息

![rustmqttsub2.png](https://assets.emqx.com/images/e71402d26419eff673247c1c7db81e9b.png)

至此，我们完成了使用 **paho-mqtt** 客户端连接到 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
