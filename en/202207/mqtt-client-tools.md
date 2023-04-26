With the rapid development of the Internet of Things (IoT), the MQTT protocol is being widely used by many companies and developers. In the journey of [learning and using MQTT](https://www.emqx.com/en/mqtt), a handy client tool can greatly facilitate developers to explore MQTT features and debug IoT applications, shortening the development cycle.

There are a variety of MQTT client tools with different functional focuses. Choosing a suitable MQTT client tool is challenging for beginners and even MQTT experts.

We have selected seven of the most useful MQTT client tools in 2022 and listed them by desktop, browser, and command line categories. We hope this article will help you quickly find a suitable client tool for MQTT development.

## How to Choose an MQTT Client?

MQTT client tools are used to connect to [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for publishing, subscribing, and messages sending and receiving. A good MQTT client tool should have the following features.

- Support for one-way and two-way SSL authentication.
- Support for [MQTT 5](https://www.emqx.com/en/mqtt/mqtt5) features.
- Maintain ease of use on a full-featured basis.
- Support for multiple clients online at the same time.
- Cross-platform, available under different operating systems.
- Support MQTT over WebSocket.
- Advanced features: Customized script, logging, payload format conversion, etc.


## MQTT Desktop Client

### MQTTX

[MQTTX](https://mqttx.app/) is a cross-platform MQTT 5.0 client tool open-sourced by EMQ, which can run on macOS, Linux and Windows, and supports formatting MQTT payload.

It simplifies test operations with a user-friendly, chat-like interface. Creating multiple, simultaneous online MQTT client connections is easy and quick. It can test the connecting, publishing, and subscribing functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket, and other MQTT protocol features.

MQTTX is dedicated to building an elegant, easy-to-use, full-platform MQTT client and has recently released both MQTTX CLI and MQTTX Web. MQTTX has reached 2K stars on GitHub and is loved by increasingly more IoT developers.


#### Features

- Cross-platform for Windows, macOS, Linux
- Support MQTT v3.1.1 and MQTT v5.0 protocols
- Support CA, self-signed certificate, and single and two-way SSL /TLS authentication
- Support theme switching between Light, Dark, and Night
- Support MQTT over WebSocket
- Support Hex, Base64, JSON, Plaintext
- Support English, Japanese, Simplified Chinese, Turkish, and Hungarian
- Support custom color marking when subscribing to topics
- Support for automatic subscription to $SYS and view bytes statistics
- Customizable script to simulate data testing
- Full logging capabilities

![MQTT X](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

#### Download

Website: [https://mqttx.app/](https://mqttx.app/)

GitHub: [https://github.com/emqx/MQTTX/releases](https://github.com/emqx/MQTTX/releases)

### MQTT Explorer

MQTT Explorer is a comprehensive MQTT client that provides a structured overview of your MQTT topics, making working with devices/services on your broker dead simple.

MQTT Explorer supports difference comparison and visual chart display of received payload messages. Similar to MQTT.fx, MQTT Explorer can only create a single connection and cannot have multiple clients online simultaneously.

#### Features

- Visualize topics and a dynamic preview of the change of topic
- Delete the retained topics
- Search/filter topics
- Recursive delete topics
- Difference view of current and previously  received messages
- Publish topics
- Draw digital topics
- Retain the historic record of every topic
- Dark/Light topic

![mqtt-explorer](https://assets.emqx.com/images/7be0606fdbb16f93359429dba0cc3e6e.png)

#### Download

[https://github.com/thomasnordquist/MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer)

### MQTT.fx

MQTT.fx was developed by Jens Deters. Since January 2021, MQTT.fx has moved to Softblade - a newly founded German company now taking care of further development of MQTT.fx, and released the commercial version MQTT.fx® 5.0. The MQTT.fx described in this article is the free 1.x version.

MQTT.fx, written in JavaFX, supports saving multiple connection configurations and encryption methods. It can set an HTTP proxy server when creating a connection.

In general, MQTT.fx has rich and mature functions and supports many configuration items in TCP connections, but users can only establish one MQTT connection at a time. In addition, it does not implement support for WebSocket and cannot be used in the test scenario of MQTT over WebSocket.

#### Features

- Predefine message template
- Get the status of the broker through the system topic `$SYS`
- Support for JavaScript scripts through Nashorn Engine
- Support log display, display log information in the connection
- Cross-platform desktop with support for Windows, macOS, and Linux

![MQTT.fx](https://assets.emqx.com/images/4f592bb17cbbfe3adf0d13e07277c0dd.png)

#### Download

[https://mqttfx.jensd.de/](https://mqttfx.jensd.de/)


## MQTT Online Client

### MQTTX Web

[MQTTX Web](https://mqttx.app/web) is an open-source MQTT 5.0 browser client and an online MQTT WebSocket client tool. Developers can use WebSockets to quickly connect to MQTT servers in the browser and debug MQTT services and applications faster without installing MQTTX.

![MQTTX Web](https://mqttx-static.emqx.net/img/banner.268d1fa.png)

Try now：[http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client)

For more information, please check out: [https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web)


## MQTT CLI

### MQTTX CLI

[MQTTX CLI](https://mqttx.app/cli) is a lightweight and open-source MQTT 5.0 command line client tool. It allows developers to develop and debug MQTT services and applications faster using the command line without the graphical interface.

#### Features

- **Dependency-free**: Get up and run with no prerequisites required
- **MQTT Benchmark testing**: Out-of-box MQTT benchmark tool
- **Configuration file**: Support saving and loading config files for `conn` / `sub` / `pub`
- **User-friendly output**: easy-to-understand command line output for viewing

#### Download

The MQTTX CLI can be quickly downloaded and installed on macOS, Linux, and Windows systems without environmental dependencies.

Try Now: [https://mqttx.app/cli]( https://mqttx.app/cli)

#### Usage

Connect

```
mqttx conn -h 'broker.emqx.io' -p 1883 -u 'admin' -P 'public'
```

Subscribe

```
mqttx sub -t 'hello' -h 'broker.emqx.io' -p 1883
```

Publish

```
mqttx pub -t 'hello' -h 'broker.emqx.io' -p 1883 -m 'from MQTTX CLI'
```

Publish multiple messages

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -s -M
```

Benchmark

```
# Connect Benchmark
mqttx bench conn -c 5000

# Subscribe Benchmark
mqttx bench sub -c 5000 -t bench/%i

# Publish Benchmark
mqttx bench pub -c 5000 -t bench/%i
```

The MQTTX CLI also supports publishing multiple messages. Add a -M parameter and a -s parameter to the command in the editor, and newline it after each entry.

![MQTTX CLI](https://assets.emqx.com/images/549a31f8b062f099c0eac8c0c6047f35.png)

### NanoMQ CLI

[NanoMQ](https://nanomq.io/) is an ultra-lightweight and blazing-fast MQTT broker for IoT edge, which carries a command line tool with commands including `conn`, `pub` `sub` , and `bench`.

#### Features

- Support performance testing
- Support MQTT 5.0
- Ability to run on edge devices
- Support reading file content as payload

#### Download

[https://nanomq.io/downloads](https://nanomq.io/downloads)

#### Usage

Bench

```
# Start 10 connections and send 100 Qos0 messages to the topic t every second, 
# where the size of each message payload is 16 bytes
nanomq_cli bench pub -t t -h broker.emqx.io -s 16 -q 0 -c 10 -I 10

# Start 500 connections, and each subscribes to the t topic with Qos0
nanomq_cli bench sub -t t -h broker.emqx.io -c 500

# Start 100 connections
nanomq_cli bench conn -h broker.emqx.io -c 100
```

Pub/Sub

```
# Send 100 Qos2 messages test to the topic t
nanomq_cli pub -t t -h broker.emqx.io -q 2 -L 100 -m test

# Subscribe
nanomq_cli sub -t t -h broker.emqx.io -q 1
```

### Mosquitto CLI

Mosquitto is an open-source implementation of a server for versions 5.0, 3.1.1, and 3.1 of the MQTT protocol. It also includes a C and C++ client library and the `mosquitto_pub` and `mosquitto_sub` utilities for publishing and subscribing.

Mosquitto CLI has multiple configuration options, supports connections through a TLS certificate and a proxy server, supports debug mode, and can get more detailed message information in debug mode.

#### Features

- Lightweight and easy to use, support debug mode
- SSL/TLS encryption/authentication support
- Easy to test in the remote server

#### Download

[https://github.com/eclipse/mosquitto](https://github.com/eclipse/mosquitto)

#### Usage

Subscribe

```
mosquitto_sub -t 'test/topic' -v
```

Publish

```
mosquitto_pub -t 'test/topic' -m 'hello world'
```



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
