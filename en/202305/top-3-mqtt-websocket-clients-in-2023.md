## Introduction

[MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) enables real-time and two-way communication between IoT devices and web applications. MQTT WebSocket client tools make it easy for developers to debug the implementation of MQTT and WebSocket protocols in their IoT projects. 

![MQTT over WebSocket](https://assets.emqx.com/images/772cccbb5a614e866fe2307691bec38f.png)

This blog post will explore the top 3 MQTT WebSocket client tools highly recommended in 2023.

## Free Public MQTT Broker

Before diving into the MQTT WebSocket tools, we need an MQTT Broker supporting WebSocket to communicate and test. We choose the free public MQTT broker available on `broker.emqx.io`.

>**MQTT Broker Info**
>
>- Server: broker.emqx.io
>- TCP Port: 1883
>- WebSocket Port: 8083
>- SSL/TLS Port: 8883
>- Secure WebSocket  Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker)

<section class="promotion">
    <div>
        Try Serverless MQTT Broker
        <div class="is-size-14 is-text-normal has-text-weight-normal">Get forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Start Free →</a>
</section>

## 1. MQTT.js

MQTT.js is an MQTT client library written in JavaScript and designed to run in both node.js and browser environments. It fully supports MQTT protocol versions 3.1.1 and 5.0, as well as TCP, TLS, and WebSocket transports.

MQTT.js is a simple and lightweight library that allows developers to easily connect to [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and publish/subscribe to MQTT topics via WebSockets.

Additionally, MQTT.js provides good documentation and community support, making it easy for developers to get started and resolve any issues they may encounter.

GitHub Project: [https://github.com/mqttjs/MQTT.js/](https://github.com/mqttjs/MQTT.js/) 

### Features

- MQTT v3.1.1 and v5.0 support
- TCP, TLS/SSL, and WebSocket support
- Automatic topic alias
- Auto reconnection
- Messages buffer

### Installation

```
npm install mqtt -g
```

### Usage Example

Here is an example of connecting to the free public broker via MQTT over WebSocket, subscribing to an [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), and sending and receiving messages.

```
var mqtt = require('mqtt')
// Connect the 8083 port with `ws` protocol.
var client = mqtt.connect('ws://broker.emqx.io:8083/mqtt')

client.on('connect', function () {
  // Subscribe to a topic
  client.subscribe('test/topic', function (err) {
    if (!err) {
      // Publish a message to a topic
      client.publish('test/topic', 'Hello mqtt')
    }
  })
})

// Receive messages
client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})
```

## 2. MQTTX Web

[MQTTX Web](https://mqttx.app/web) is a user-friendly, browser-based tool for online debugging, developing, and testing MQTT applications. It connects to an MQTT broker via a WebSocket client and offers an intuitive interface.

Developed by the [EMQX team](https://github.com/emqx), MQTTX Web is an open-source tool that supports MQTT 3.1.1 and MQTT 5.0 protocols and WebSocket transports. It is licensed under Apache Version 2.0.

**Free Online MQTTX Web:** [http://mqtt-client.emqx.com/](http://mqtt-client.emqx.com/#/recent_connections)

**Official Website:** [https://mqttx.app/web](https://mqttx.app/web) 

**GitHub Project:** [https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web) 

![MQTTX Web](https://assets.emqx.com/images/475a04d5d94250f41941d4c915649422.png)

### Features

- User-friendly interface for beginners and advanced users
- Browser-based, no need to download and install
- Chatbox UI for sending/receiving MQTT messages
- MQTT v3.1.1 and MQTT v5.0 support
- MQTT over WebSocket support
- Using Docker for local deployment

### Usage Example

1. Open [MQTTX Web](http://mqtt-client.emqx.com/) using your web browser.

2. Create an [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) using WebSocket:

   ![Create an MQTT connection](https://assets.emqx.com/images/d2ac378be20377c69c7387c77cd2cf93.png)

3. Subscribe to an MQTT topic and publish messages to the topic:

   ![Subscribe to an MQTT topic and publish messages to the topic](https://assets.emqx.com/images/d20101ab94108f835bcccb21ee2d1688.png)


## 3. Paho JavaScript Client

The Paho JavaScript Client is an MQTT browser-based client library written in Javascript that uses WebSockets to connect to an MQTT Broker.

Paho MQTT is an open-source MQTT client that implements MQTT 3.1.1, developed by the Eclipse Foundation. However, the project has not been actively maintained since June 2019.

**Official Website:** [https://www.eclipse.org/paho/index.php?page=clients/js/index.php](https://www.eclipse.org/paho/index.php?page=clients/js/index.php) 

**GitHub Project:** [https://github.com/eclipse/paho.mqtt.javascript](https://github.com/eclipse/paho.mqtt.javascript) 

Features:

- MQTT 3.1.1 and WebSocket support
- SSL / TLS support
- Message Persistence
- Automatic Reconnect

### Usage Example

Please check out the project [README](https://github.com/eclipse/paho.mqtt.javascript) for examples of usage.

## Wrap up

MQTT.js is the best client library written in Javascript for web applications requiring MQTT over WebSocket, while the Paho JavaScript client is not actively developed. And MQTTX Web is the best client toolbox for debugging and testing MQTT over WebSocket.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
