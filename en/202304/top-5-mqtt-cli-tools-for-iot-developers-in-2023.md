## Introduction

As MQTT continues to gain popularity as a lightweight messaging protocol for the IoT, the need for efficient and user-friendly command line interface (CLI) tools is increasing. In this article, we will take a look at the top **5** MQTT CLI Tools available in 2023.

## Free Public MQTT Broker

Before diving into the MQTT CLI tools, we need an MQTT broker to communicate and test. We choose the free public MQTT broker available on `broker.emqx.io`.

>**MQTT Broker Info**
>
>- Server: broker.emqx.io
>- TCP Port: 1883
>- WebSocket Port: 8083
>- SSL/TLS Port: 8883
>- Secure WebSocket  Port: 8084

For more information, please check out: [Free Public MQTT Broker for IoT Testing](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

<section class="promotion">
    <div>
        Try Serverless MQTT Broker
        <div class="is-size-14 is-text-normal has-text-weight-normal">Get forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Start Free →</a>
</section>

## #1: MQTTX CLI

[MQTTX CLI](https://mqttx.app/cli) is a lightweight and easy-to-use MQTT 5.0 command line tool. With various commands for MQTT publishing, subscribing, benchmarking, and IoT data simulation, it is one of the most powerful tools for MQTT development.

MQTTX CLI is an open-source project written in Node.js and developed by [EMQ](https://www.emqx.com/en). It’s cross-platform and can work on Windows, macOS, and Linux. 

**Official Website:** [https://mqttx.app/cli](https://mqttx.app/cli) 

**GitHub:** [https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli) 

![MQTTX CLI](https://assets.emqx.com/images/21640fc7fa544b56ae41815f390ccee7.png)

### Features

- Fully support for both MQTT v3.1.1 and MQTT v5.0
- Cross-platform compatibility with Windows, MacOS, and Linux
- Dependency-free setup allowing for quick installation without prerequisites
- Supports CA, self-signed certificates, and one-way and two-way SSL authentication
- Performance testing capabilities for quickly evaluating MQTT service performance.

### Installation

#### Docker

```
docker pull emqx/mqttx-cli
docker run -it --rm emqx/mqttx-cli
```

#### Homebrew

```
brew install emqx/mqttx/mqttx-cli
```

#### Download

- [https://mqttx.app/cli](https://mqttx.app/cli) 
- [https://github.com/emqx/MQTTX/releases](https://github.com/emqx/MQTTX/releases) 

### Usage Example

#### Connect

Test connecting to an MQTT broker:

```
mqttx conn -h 'broker.emqx.io' -p 1883 -u 'test' -P 'test'
```

#### Publish

Publish a QoS1 message to an MQTT topic:

```
mqttx pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from MQTTX CLI'
```

#### Subscribe

Subscribe to an MQTT topic:

```
mqttx sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
```

#### Bench

Create 100 connections, bench a pub/sub scenario at 100 msgs/s:

```
mqttx bench pub -c 100 -t bench/%i -h 'broker.emqx.io' -p 1883
mqttx bench sub -c 100 -t bench/%i -h 'broker.emqx.io' -p 1883
```

<section class="promotion">
    <div>
        Download MQTTX CLI
      <div class="is-size-14 is-text-normal has-text-weight-normal">A powerful and easy-to-use MQTT 5.0 command line tool.</div>
    </div>
    <a href="https://mqttx.app/cli#download" class="button is-gradient px-5">Download Now →</a>
</section>

## #2: Mosquitto CLI

Mosquitto is a widely used open-source MQTT broker with the popular `mosquitto_pub` and `mosquitto_sub` command line clients. These CLI tools offer a wide range of options to connect, subscribe to, and publish messages to an MQTT broker.

The Mosquitto project is written in C/C++ and maintained by the Eclipse Foundation. Mosquitto is highly portable and can be deployed on various platforms, including Linux, Mac, Windows, and Raspberry Pi.

### Features

- Lightweight and easy to use
- Support for MQTT v3.1.1 and v5.0 protocols
- Extensive command-line parameters
- Support for SSL/TLS encryption/authentication
- MQTT v5.0 request/response functionality

### Installation

#### Docker

```
docker pull eclipse-mosquitto
```

#### Homebrew

```
brew install mosquitto
```

#### Download

[https://mosquitto.org/download/](https://mosquitto.org/download/) 

### Usage Example

#### Publish

Publish a QoS1 message to an MQTT topic:

```
mosquitto_pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from Mosquitto CLI'
```

#### Subscribe

Subscribe to an MQTT topic:

```
mosquitto_sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
```

#### Request/Response

```
mosquitto_rr -t 'req-topic' -e 'rep-topic' -m 'request message' -h 'broker.emqx.io'
mosquitto_pub -t 'rep-topic' -m 'response message' -h 'broker.emqx.io'
```

## #3: NanoMQ CLI

[NanoMQ](https://github.com/emqx/nanomq) is the latest open-source MQTT broker written in pure C for the IoT edge, initially developed by EMQ in 2020. It is fast and lightweight with multi-threading and asynchronous I/O architecture.

NanoMQ also provides an MQTT client SDK and a command line tool for MQTT benchmarking and debugging, specifically for [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), the next generation of the MQTT protocol standard.

**GitHub:** [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq)

### Features

- Comprehensive MQTT Toolkit with Proto Proxy
- Full support for MQTT v3.1.1 and MQTT v5.0 protocols
- Cross-platform compatibility with Windows, Mac, Linux, POSIX RTOS, and more
- Support for CA, self-signed certificates, and TLS/SSL encryption
- Built-in nanomsg (NNG)/DDS/ZeroMQ/SOME-IP proxy
- Performance benchmarking support

### Installation

#### Docker 

```
docker pull emqx/nanomq
```

#### Download

- [https://nanomq.io/downloads?os=Linux](https://nanomq.io/downloads?os=Linux) 
- [https://github.com/emqx/nanomq/releases](https://github.com/emqx/nanomq/releases) 

### Usage Example

#### Publish

Publish a QoS1 message to a topic:

```
nanomq_cli pub -t 'topic' --url "mqtt-tcp://broker.emqx.io:1883" -q 2 -u nano -m test
```

#### Subscribe

Subscribe to a topic:

```
nanomq_cli sub -t topic --url "mqtt-tcp://broker.emqx.io:1883" -q 1
```

#### Connect

Test connecting to an MQTT broker:

```
nanomq_cli conn --url "mqtt-tcp://broker.emqx.io:1883" -q 1
```

#### Bench

Create 10 connections, publish to a topic at 100 msgs/s: 

```
nanomq_cli bench pub -t topic -h broker.emqx.io -s 16 -q 0 -c 10 -I 10
```

## #4: MQTT.js CLI

[MQTT.js](https://github.com/mqttjs/MQTT.js) is a popular MQTT client library, written in JavaScript for node.js and the browser. MQTT.js also provides a CLI tool that can be used for MQTT testing and debugging in the command line.

MQTT.js CLI depends on Node.js, and Node v12+ is required to run.

**GitHub**: [https://github.com/mqttjs/MQTT.js](https://github.com/mqttjs/MQTT.js)

### Features

- Easy to install and use, even for those who are not familiar with the MQTT protocol
- Support for both MQTT v3.1.1 and MQTT v5.0
- Cross-platform compatibility with Windows, MacOS, and Linux
- Support for CA, self-signed certificates, and TLS/SSL encryption

### Installation

```
npm install mqtt -g
```

### Usage Example

#### Publish

```
mqtt pub -t 'topic' -h broker.emqx.io -m 'Hello from MQTT.js CLI'
```

#### Subscribe

```
mqtt sub -t 'topic' -h broker.emqx.io
```

## #5: HiveMQ CLI

[HiveMQ CLI](https://hivemq.github.io/mqtt-cli/) is a fully MQTT 5.0 and MQTT 3.1.1 compatible command line interface developed by HiveMQ.

HiveMQ CLI is implemented with Java, and Java 8 is required to run.

**GitHub**: [https://github.com/hivemq/mqtt-cli](https://github.com/hivemq/mqtt-cli) 

### Features

- All MQTT 3.1.1 and MQTT 5.0 features are supported
- Interactive, direct, and verbose Modes for all MQTT Commands
- Shell behavior with Syntax Highlighting, Command history
- Ability to connect simultaneously various MQTT Clients to different Broker
- Built on JVM and various distributions available

### Installation

#### Docker

```
docker pull hivemq/mqtt-cli
```

#### Homebrew

```
brew install hivemq/mqtt-cli/mqtt-cli
```

#### Download

[https://github.com/hivemq/mqtt-cli/releases](https://github.com/hivemq/mqtt-cli/releases) 

### Usage Example

#### Publish

Publish a message to an MQTT topic:

```
docker run hivemq/mqtt-cli pub -t 'topic' -h 'broker.emqx.io' -p 1883 -m 'Hello from HiveMQ CLI'
```

#### Subscribe

Subscribe to an MQTT topic:

```
docker run hivemq/mqtt-cli sub -t 'topic' -h 'broker.emqx.io' -p 1883
```

#### Test 

Test features and limitations of an MQTT broker:

```
docker run hivemq/mqtt-cli  test -h 'broker.emqx.io' -p 1883
MQTT 3: OK
	- Maximum topic length: 65535 bytes
	- QoS 0: Received 10/10 publishes in 497.85ms
	- QoS 1: Received 10/10 publishes in 1992.64ms
	- QoS 2: Received 10/10 publishes in 4460.73ms
	- Retain: OK
	- Wildcard subscriptions: OK
	- Shared subscriptions: OK
	- Payload size: >= 100000 bytes
	- Maximum client id length: 15346 bytes
	- Unsupported Ascii Chars: ALL SUPPORTED
MQTT 5: OK
	- Connect restrictions: 
		> Retain: OK
		> Wildcard subscriptions: OK
		> Shared subscriptions: OK
		> Subscription identifiers: OK
		> Maximum QoS: 2
		> Receive maximum: 65535
		> Maximum packet size: 1048576 bytes
		> Topic alias maximum: 65535
		> Session expiry interval: Client-based
		> Server keep alive: Client-based

```

## Wrap up

In short, the MQTT CLI tools mentioned above offer a wide range of options for testing and debugging MQTT. You can choose according to the specific needs of your project. We hope this article provides some helpful insights into the top MQTT CLI tools for 2023.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
