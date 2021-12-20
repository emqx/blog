## Introduction

[MQTT.js](https://github.com/mqttjs/MQTT.js) is a client library for the [MQTT protocol](https://www.emqx.com/en/mqtt) protocol, written in JavaScript for node.js and the browser. It is currently the most widely used [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk) in the JavaScript ecosystem.

> MQTT is a lightweight IoT messaging protocol based on the publish/subscribe model. It can provide real-time and reliable messaging services for networked devices with very little code and bandwidth. It is widely used in the industries such as the IoT, mobile Internet, smart hardware, Internet of Vehicles and power energy.

Due to the single-thread feature of JavaScript, MQTT.js is a fully asynchronous MQTT client. MQTT.js supports MQTT/TCP, MQTT/TLS, MQTT/WebSocket, and the degree of support in different operating environments is as follows:

- Browser: MQTT over WebSocket
- Node.js: MQTT, MQTT over WebSocket

In different environments, except for a few different connection parameters, other APIs are the same. For MQTT.js v3.0.0 and later versions, MQTT 5.0 has been fully supported.

## Installation

### Install using NPM or yarn

```shell
npm install mqtt --save

# or use yarn

yarn add mqtt
```

**Note**: **v4.0.0** (Released 04/2020) removes support for all end of life node versions, and now supports node v12 and v14.

### Install using CDN

In the browser, we can also use CDN to introduce MQTT.js. The bundle package of MQTT.js is managed by [http://unpkg.com](http://unpkg.com/), and we can directly add [unpkg.com/mqtt/dist/mqtt.min.js](https://unpkg.com/mqtt/dist/mqtt.min.js) to use it.

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<script>
  // An mqtt variable will be initialized globally
  console.log(mqtt)
</script>
```

### Global installation

In addition to the above installation methods, MQTT.js also provides a global installation method that uses command-line tools to complete MQTT connection, publishing, and subscription.

```shell
npm install mqtt -g
```

We will describe in detail how to use the command-line tool of MQTT.js in some tutorials below.

## Usage

This article will use the [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ X Cloud as the MQTT server address for this test. The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

For more details, please visit [EMQ X Cloud website](https://www.emqx.com/en/cloud), or check [EMQ X Cloud documentation](https://docs.emqx.io/en/cloud/latest/ ).

### Simple example

We simply write a piece of code to connect to EMQ X Cloud and complete an example of subscribing to topics and sending and receiving messages:

```javascript
const mqtt = require('mqtt')
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Auth
  clientId: 'emqx_test',
  username: 'emqx_test',
  password: 'emqx_test',
}
const client  = mqtt.connect('mqtt://broker.emqx.io:1883', options)
client.on('connect', function () {
  console.log('Connected')
  client.subscribe('test', function (err) {
    if (!err) {
      client.publish('test', 'Hello mqtt')
    }
  })
})

client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})
```

### Command Line

After the global installation of MQTT.js, we can also use the command-line tool to complete the action of subscribing to topics and sending and receiving messages.

Example: connect to `broker.emqx.io` and subscribe to the `testtopic/#` topic:

```shell
mqtt sub -t 'testtopic/#' -h 'broker.emqx.io' -v
```

Example: connect to `broker.emqx.io` and send a message to the `testtopic/hello` topic 

```shell
mqtt pub -t 'testtopic/hello' -h 'broker.emqx.io' -m 'from MQTT.js'
```

### API introduction

#### mqtt.connect([url], options)

This API connects to the specified MQTT Broker function and always returns a Client object. The first parameter passes in a URL value. The URL can be the following protocols: `mqtt`, `mqtts`, `tcp`, `tls`, `ws`, `wss`. The URL can also be an object returned by URL.parse(). Then, this API passes in an Options object to configure the options of the MQTT connection. Here are some commonly-used attribute values in the Options object:

- Options
  - `keepalive`: The unit is `seconds`, the type is integar, the default is 60 seconds, and it is disabled when it is set to 0
  - `clientId`: The default is `'mqttjs_' + Math.random().toString(16).substr(2, 8)`, and it can support custom modified strings
  - `protocolVersion`: MQTT protocol version number, the default is 4 (v3.1.1) and can be modified to 3 (v3.1) and 5 (v5.0)
  - `clean`: Whether to clear the session, and the default is `true`. When it is set to `true`, the session will be cleared after disconnection, and the subscribed topics will also be invalid. When it is set to `false`, messages with QoS of 1 and 2 can also be received offline
  - `reconnectPeriod`: Reconnect interval time,  the unit is milliseconds, and the default is 1000 milliseconds. **Note:** When it is set to 0, the automatic reconnect will be disabled
  - `connectTimeout`: It is the waiting time before receiving CONNACK, the unit is milliseconds, and the default is 30000 milliseconds
  - `username`: Authentication username. If Broker requires username authentication, please set this value
  - `password`: authentication password. If the Broker requires password authentication, please set this value
  - `will`: Will message, a configurable object value. When the client disconnects abnormally, the Broker will publish a message to the will topic in the format below:
    - `topic`: Topic sent by the will
    - `payload`: the message published by the will
    - `QoS`: QoS value sent by the will
    - `retain`: the retain sign of the message published by the will
  - `properties`: the property values of configurable objects that is new added in [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) . For more details, please refer to: [https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options)
- If you need to configure an SSL/TLS connection, the Option object will be passed to [`tls.connect()`](http://nodejs.org/api/tls.html#tls_tls_connect_options_callback), and you can configure the following properties in option
  - `rejectUnauthorized`: Whether to verify the server certificate chain and address name. When it is set to false, the verification will be skipped and it will be exposed to the attacks of man-in-the-middle. Therefore, this configuration is not recommended in a production environment. When it is set to true, the strong authentication mode will be enabled. If it is a self-signed certificate, please set the Alt name during certificate configuration.
  - `ca`:  The CA file generated in the self-signed certificate. It is necessary only when the server uses a self-signed certificate
  - cert: Client certificate. It is necessary only when the server requires client certificate authentication (two-way authentication),
  - key:  Client key. It is necessary only when the server requires client certificate authentication (two-way authentication)

#### Client Event

When the connection is successful, the returned Client object can listen to multiple events through the on function, and the business logic can be completed in the callback function of the monitor. Here are some common events:

- `connect`

  Triggered when the connection is successful, and the parameter is connack

  ```javascript
  client.on('connect', function (connack) {
    console.log('Connected')
  })
  ```

- `reconnect`

  Triggered when the broker is automatically reconnected after the reconnection interval when it is disconnected

  ```javascript
  client.on('reconnect', function () {
    console.log('Reconnecting...')
  })
  ```

- `close`

  Triggered after disconnection

  ```javascript
  client.on('close', function () {
    console.log('Disconnected')
  })
  ```

- `disconnect`

  Triggered when a disconnected packet sent by Broker is received, and the parameter packet is the packet received when disconnected. It is a new function in MQTT 5.0

  ```javascript
  client.on('disconnect', function (packet) {
    console.log(packet)
  })
  ```

- `offline`

  Triggered when the client goes offline

  ```javascript
  client.on('offline', function () {
    console.log('offline')
  })
  ```

- `error`

  Triggered when the client cannot connect successfully or a parsing error occurs. The parameter error is the error message

  ```javascript
  client.on('error', function (error) {
    console.log(error)
  })
  ```

- `message`

  Triggered when the client receives a published Payload, which contains three parameters, topic, payload and packet. The topic is the topic of the received message, the payload is the content of the received message, and the packet is the MQTT packet which contains QoS, retain and other information

  ```javascript
  client.on('message', function (topic, payload, packet) {
    // Payload is Buffer
    console.log(`Topic: ${topic}, Message: ${payload.toString()}, QoS: ${packet.qos}`)
  })
  ```


#### Client function

In addition to listening to events, Client also has some built-in functions for publishing and subscribing operations. Here are some commonly-used functions.

- `Client.publish(topic, message, [options], [callback])`

  A function to publish a message to a topic, which contains four parameters:

  - topic: the topic to be sent, which is a string
  - message: The message under the topic to be sent, which can be a string or a Buffer
  - options: Optional value.  It refers to the configuration information when publishing a message, and is mainly used to set the QoS and Retain value when publishing a message.
  - callback: callback function after the message is published. The parameter is error. This parameter exists only when publishing fails

  ```javascript
  // Send a test message with QoS of 0 to the testtopic
  client.publish('testtopic', 'Hello, MQTT!', { qos: 0, retain: false }, function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Published')
    }
  })
  ```

- `Client.subscribe(topic/topic array/topic object, [options], [callback])`

  The function of subscribing to one or more topics. When the connection is successful, you need to subscribe to the topic to get the message. This function contains three parameters:

  - topic: It can pass in a string, or an array of strings, or a topic object,`{'test1': {qos: 0}, 'test2': {qos: 1}}`
  - options: Optional value. The configuration information when subscribing to a topic. It is mainly used to fill in the QoS level of the subscribed topic
  - callback: callback function after subscribing to the topic. The parameters are error and granted. The error parameter only exists when the subscription fails. Granted is an array of {topic, QoS}, where the topic is the subscribed topic and QoS is the QoS level granted to the topic

  ```javascript
  // Subscribe to a topic named testtopic with QoS 0
  client.subscribe('testtopic', { qos: 0 }, function (error, granted) {
    if (error) {
      console.log(error)
    } else {
      console.log(`${granted[0].topic} was subscribed`)
    }
  })
  ```

- `Client.unsubscribe(topic/topic array, [options], [callback])`

  Un-subscribe to a single topic or multiple topics. This function contains three parameters:

  - Topic: It can pass in a string or an array of strings
  - Options: Optional value. It refers to configuration information when unsubscribing
  - Callback: the callback function when unsubscribing. The parameter is error. The error parameter exists only when unsubscribing fails

  ```javascript
  // Unsubscribe to a topic named testtopic
  client.unsubscribe('testtopic', function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Unsubscribed')
    }
  })
  ```

- `Client.end([force], [options], [callback])`

  Close the client. This function contains three parameters:

  - force: When it is set to true, the client will be closed immediately without waiting for the disconnected message to be accepted. This parameter is optional and the default is false. **Note**: When it is set to true, the Broker cannot receive the disconnect packet
  - options: Optional value, configuration information when closing the client,
  - Options: optional value. It refers to the configuration information when the client is closed. It is mainly used to configure reasonCode when disconnecting
  - callback: callback function when the client is closed

  ```javascript
  client.end()
  ```

## Summary

So far, this article has briefly introduced the usage functions of some common APIs of MQTT.js. For specific use in actual projects, please refer to the following links:

- [How to use MQTT in Vue](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [How to use MQTT in React](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [How to use MQTT in Electron](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [How to use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [Connect to MQTT server with WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
