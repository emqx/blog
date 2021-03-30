
Rust is a multi-paradigm programming language designed for performance and safety, especially safe concurrency. Rust is syntactically similar to C++, but can guarantee memory safety by using a borrow checker to validate references. Rust achieves memory safety without garbage collection, and reference counting is optional.[^1]

[MQTT](https://www.emqx.io/mqtt) is a kind of **lightweight IoT messaging protocol** based on the publish/subscribe model. It can use very little code and bandwidth to provide a real-time reliable message service for networked equipment. Also, it is widely used in the IoT, mobile Internet, smart hardware, IoV, power and energy industries.

This article mainly introduces how to use the **paho-mqtt** client library in the Rust project, and how to implement connect, subscribe, messaging and unsubscribe, etc., between the client and MQTT broker. 



## Project initialisation

This project uses Rust 1.44.0 to develop and test, and is managed using the Cargo 1.44.0 package management tool, and the reader can check the current version of Rust using the following command.

```bash
~ rustc --version
rustc 1.44.0 (49cae5576 2020-06-01)
```

### Selecting the MQTT client library

paho-mqtt is the most versatile and widely used MQTT client in the current Rust. The latest version `0.7.1` supports MQTT v5, 3.1.1, 3.1, and also supports data transfer via standard TCP, SSL / TLS, WebSockets, and QoS support 0, 1, 2, etc.

### Initialisation project

Execute the following command to create a new Rust project called `mqtt-example`.

```bash
~ cargo new mqtt-example
    Created binary (application) `mqtt-example` package
```

Edit the `Cargo.toml` file in the project, and add the address of the `paho-mqtt` library to the `dependencies` and specify the binary file corresponding to the subscribe, publish code file.

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



## The use of Rust MQTT

### Create a client connection

This article will use [the free public MQTT broker](https://www.emqx.io/mqtt/public-mqtt5-broker) which is provided by EMQ X as the MQTT broker of the test connection. This service is based on EMQ X's [MQTT IoT cloud platform](https://cloud.emqx.io/) to create. The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

### Configure the MQTT Broker connection parameters

Configure the MQTT Broker connection address (including the port), the topic (here we have configured two topics), and the client id.

```rust
const DFLT_BROKER:&str = "tcp://broker.emqx.io:1883";
const DFLT_CLIENT:&str = "rust_publish";
const DFLT_TOPICS:&[&str] = &["rust/mqtt", "rust/test"];
```

### Write MQTT connection code

Write the MQTT connection code, and the connection address can be passed as a command-line argument when executing the binary file to improve the user experience. Usually, we need to create a client and then connect it to `broker.emqx.io`.

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

### Publish messages

Here we publish a total of five messages to the two topics `rust/mqtt` and `rust/test`, depending on the parity of the loop.

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

### Subscribe

Before the client connected, the consumer needs to be initialized. Here we loop processing the queue of messages in the consumer and print out the subscribed topic name and the content of the messages received.

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



## Complete code

### The code for publishing messages

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

### The code for subscribe

To improve the user experience, message subscriptions are disconnected, and topics are re-subscribed after the connection is re-established.

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



## Running and testing

### Compile binary files

The following command generates the `sub`, `pub` binary file  in the `mqtt-example/target/debug` directory.

```bash
cargo build
```

![rustmqttbin.png](https://static.emqx.net/images/7e95c531f0a3534bb48dcb9f17b778c6.png)

### Message subscription

Execute the `sub` binary file and wait for the message to be published.

![rustmqttsub1.png](https://static.emqx.net/images/bb040cf5a869a301023e7167895b4d4a.png)

### Message publishing

Executing the `pub` binary file, you can see that messages have been published to the topics `rust/test` and `rust/mqtt`, respectively.

![rustmqttpub.png](https://static.emqx.net/images/28949361d916b71fb10f083852a9bbe1.png)
Meanwhile, the published messages are also visible in the message subscription.

![rustmqttsub2.png](https://static.emqx.net/images/e71402d26419eff673247c1c7db81e9b.png)

So far, we have completed using the **paho-mqtt** client to connect to the [public MQTT broker](https://www.emqx.io/mqtt/public-mqtt5-broker), and implemented connection, message publishing and subscription between the test client and  MQTT broker.



[^1]: https://en.wikipedia.org/wiki/Rust_(programming_language)

