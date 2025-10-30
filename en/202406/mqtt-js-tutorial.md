## Introduction

In the rapidly evolving world of Internet of Things (IoT) and real-time communication, MQTT (Message Queuing Telemetry Transport) has emerged as a crucial protocol. For JavaScript developers looking to harness the power of MQTT in their applications, [**MQTT.js**](https://github.com/mqttjs/MQTT.js) stands out as an essential tool.

**MQTT.js** is a robust client library for the [**MQTT protocol**](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), meticulously crafted in JavaScript to cater to both Node.js and browser environments. Its versatility and efficiency have made it the most widely adopted [**MQTT client library**](https://www.emqx.com/en/mqtt-client-sdk) within the JavaScript ecosystem, empowering developers to create sophisticated IoT and messaging applications with ease.

Key features of MQTT.js include:

- Asynchronous Operation: Leveraging JavaScript's single-threaded nature, MQTT.js operates as a fully asynchronous MQTT client, ensuring optimal performance and responsiveness in your applications.

- Broad Protocol Support: The library seamlessly supports MQTT/TCP, MQTT/TLS, and MQTT/WebSocket, providing flexibility for various network configurations and security requirements.

- Cross-Platform Compatibility: MQTT.js offers tailored support for different operating environments:

  - Browser: Enables [**MQTT over WebSocket**](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket), allowing real-time communication in web applications.

  - Node.js: Supports both MQTT and MQTT over WebSocket, catering to server-side applications and IoT devices.

This guide aims to introduce beginners to the world of MQTT.js, exploring its setup, basic usage, and practical applications. We'll cover topics such as:

- Setting up MQTT.js in your project
- Connecting to an MQTT broker
- Publishing and subscribing to topics
- Handling messages and events
- Best practices for error handling and security

## Installation

### Install MQTT.js Using NPM or Yarn

To install MQTT.js using NPM or Yarn, run the following command:

```bash
npm install mqtt --save

# Alternatively, use yarn
yarn add mqtt
```

> Note: MQTT.js v5.0.0 (07/2023) introduces major changes including TypeScript rewrite, Node.js v18/v20 support, while v4.0.0 (04/2020) supports Node.js v12/v14.

### Install MQTT.js Using CDN

In the **browser**, you can also use a CDN to import MQTT.js. The bundle package of MQTT.js is managed by [http://unpkg.com](http://unpkg.com/), and you can directly add [unpkg.com/mqtt/dist/mqtt.min.js](https://unpkg.com/mqtt/dist/mqtt.min.js) to use it.

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<script>
  // An mqtt variable will be initialized globally
  console.log(mqtt)
</script>
```

### Global Installation

In addition to the above installation methods, MQTT.js also provides a global installation method that uses command-line tools to complete MQTT connection, publishing, and subscription. We will describe in detail how to use the command-line tool of MQTT.js in some tutorials below.

To install MQTT.js globally using NPM, run the following command:

```bash
npm install mqtt -g
```

## Preparing an MQTT Broker

Before proceeding, ensure that you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with. There are several options for obtaining an MQTT broker:

- **Private deployment**

  [EMQX](https://github.com/emqx/emqx) is the most scalable open-source MQTT broker for IoT, [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges), and connected vehicles. To install EMQX, run the following Docker command:

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  
  ```

- **Fully managed cloud service**

  The fully managed cloud service is the easiest way to start an MQTT service. With [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity. It provides a complimentary offering of 1M session minutes/month for developers to easily start their MQTT deployment within seconds.

- **Free public MQTT broker**

  The Free public MQTT broker is exclusively available for those who wish to learn and test the MQTT protocol. It is important to avoid using it in production environments as it may pose security risks and downtime concerns.

For this blog post, we will use the free public MQTT broker at `broker.emqx.io`.

> MQTT Broker Info
>
>
> Server: `broker.emqx.io`
>
> TCP Port: `1883`
>
> WebSocket Port: `8083`
>
> SSL/TLS Port: `8883`
>
> Secure WebSocket Port: `8084`

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/b4cff1e553053873a87c4fa8713b99bc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      A Practical Guide to MQTT Broker Selection
    </div>
    <div class="promotion-pdf__desc">
      Download this practical guide and learn what to consider when choosing an MQTT broker.
    </div>
    <a href="https://www.emqx.com/en/resources/a-practical-guide-to-mqtt-broker-selection?utm_campaign=embedded-a-practical-guide-to-mqtt-broker-selection&from=blog-mqtt-js-tutorial" class="button is-gradient">Get the eBook →</a>
  </div>
</section>

## Simple MQTT.js Example

We will provide an example of how to connect to EMQX Cloud, subscribe to topics, and send and receive messages using MQTT.js.

> Note: WebSocket connections are supported only in browsers. As a result, we will be using different connection parameters for the browser and Node.js environments. However, all other parameters are the same, except for the connection URL. Readers can use the parameters that best suit their needs.

```jsx
const mqtt = require('mqtt')

/***
 * Browser
 * This document explains how to use MQTT over WebSocket with the ws and wss protocols.
 * EMQX's default port for ws connection is 8083 and for wss connection is 8084.
 * Note that you need to add a path after the connection address, such as /mqtt.
 */
const url = 'ws://broker.emqx.io:8083/mqtt'
/***
 * Node.js
 * This document explains how to use MQTT over TCP with both mqtt and mqtts protocols.
 * EMQX's default port for mqtt connections is 1883, while for mqtts it is 8883.
 */
// const url = 'mqtt://broker.emqx.io:1883'

// Create an MQTT client instance
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Authentication
  clientId: 'emqx_test',
  username: 'emqx_test',
  password: 'emqx_test',
}
const client  = mqtt.connect(url, options)
client.on('connect', function () {
  console.log('Connected')
  // Subscribe to a topic
  client.subscribe('test', function (err) {
    if (!err) {
      // Publish a message to a topic
      client.publish('test', 'Hello mqtt')
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

## MQTT.js Command Line

After installing MQTT.js globally, we can use the command-line tool to subscribe to topics and send and receive messages.

Example: connect to `broker.emqx.io` and subscribe to the `testtopic/#` topic:

```bash
mqtt sub -t 'testtopic/#' -h 'broker.emqx.io' -v
```

Example: connect to `broker.emqx.io` and send a message to the `testtopic/hello` topic

```bash
mqtt pub -t 'testtopic/hello' -h 'broker.emqx.io' -m 'from MQTT.js'
```

If you require a more comprehensive MQTT command-line tool, you can refer to [MQTTX CLI](https://mqttx.app/cli).

## MQTT.js API Introduction

### mqtt.connect([url], options)

This API connects to the specified MQTT Broker function and always returns a `Client` object. The first parameter passes in a URL value, which can use the following protocols: `mqtt`, `mqtts`, `tcp`, `tls`, `ws`, `wss`. Alternatively, the URL can be an object returned by `URL.parse()`.

Next, this API passes in an `Options` object to configure the options of the MQTT connection. If using a WebSocket connection, you must consider whether to add a path after the address, such as `/mqtt`.

Here are some commonly-used attribute values in the Options object:

- Options

  - `keepalive`: The unit is `seconds`, the type is integar, the default is 60 seconds, and it is disabled when it is set to 0

  - `clientId`: The default is `'mqttjs_' + Math.random().toString(16).substr(2, 8)`, and it can support custom modified strings

  - `protocolVersion`: MQTT protocol version number, the default is 4 (v3.1.1) and can be modified to 3 (v3.1) and 5 (v5.0)

  - `clean`: Whether to clear the session, and the default is `true`. When it is set to `true`, the session will be cleared after disconnection, and the subscribed topics will also be invalid. When it is set to `false`, messages with QoS of 1 and 2 can also be received offline

  - `reconnectPeriod`: Reconnect interval time, the unit is milliseconds, and the default is 1000 milliseconds. **Note:** When it is set to 0, the automatic reconnect will be disabled

  - `connectTimeout`: It is the waiting time before receiving CONNACK, the unit is milliseconds, and the default is 30000 milliseconds

  - `username`: Authentication username. If broker requires username authentication, please set this value

  - `password`: authentication password. If the broker requires password authentication, please set this value

  - `will`

    : [Will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message), a configurable object value. When the client disconnects abnormally, the broker will publish a message to the will topic in the format below:

    - `topic`: Topic sent by the will
    - `payload`: the message published by the will
    - `QoS`: QoS value sent by the will
    - `retain`: the retain sign of the message published by the will

  - `properties`: the property values of configurable objects that is new added in [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) . For more details, please refer to: [https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options)

- If you need to configure an SSL/TLS connection, the Option object will be passed to `tls.connect()`, and you can configure the following properties in option

  - `rejectUnauthorized`: Whether to verify the server certificate chain and address name. When it is set to false, the verification will be skipped and it will be exposed to the attacks of man-in-the-middle. Therefore, this configuration is not recommended in a production environment. When it is set to true, the strong authentication mode will be enabled. If it is a self-signed certificate, please set the Alt name during certificate configuration.
  - `ca`: The CA file generated in the self-signed certificate. It is necessary only when the server uses a self-signed certificate
  - `cert`: Client certificate. It is necessary only when the server requires client certificate authentication (two-way authentication),
  - `key`: Client key. It is necessary only when the server requires client certificate authentication (two-way authentication)

### Client Event

Once the connection is successful, the returned Client object can listen to multiple events using the on function. The business logic can be completed within the callback function of the monitor. Here are some common events:

- `connect`

  Triggered when the connection is successful, and the parameter is connack

  ```jsx
  client.on('connect', function (connack) {
    console.log('Connected')
  })
  ```

- `reconnect`

  Triggered when the broker is automatically reconnected after the reconnection interval when it is disconnected

  ```jsx
  client.on('reconnect', function () {
    console.log('Reconnecting...')
  })
  ```

- `close`

  Triggered after disconnection

  ```jsx
  client.on('close', function () {
    console.log('Disconnected')
  })
  
  ```

- `disconnect`

  Triggered when a disconnected packet sent by broker is received, and the parameter packet is the packet received when disconnected. It is a new function in MQTT 5.0

  ```jsx
  client.on('disconnect', function (packet) {
    console.log(packet)
  })
  ```

- `offline`

  Triggered when the client goes offline

  ```jsx
  client.on('offline', function () {
    console.log('offline')
  })
  ```

- `error`

  Triggered when the client cannot connect successfully or a parsing error occurs. The parameter error is the error message

  ```jsx
  client.on('error', function (error) {
    console.log(error)
  })
  ```

- `message`

  This event is triggered when the client receives a published payload, which contains three parameters: topic, payload, and packet. The topic refers to the topic of the received message, the payload is the content of the received message, and the packet is the [MQTT packet](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) containing QoS, retain, and other information.

  > Note: The received payload is a value of Buffer type. You can use JSON.parse, JSON.stringify or toString() method as needed to display the final format.

  ```jsx
  client.on('message', function (topic, payload, packet) {
    // Payload is Buffer
    console.log(`Topic: ${topic}, Message: ${payload.toString()}, QoS: ${packet.qos}`)
  })
  ```

### Client Function

In addition to listening to events, the Client also has some built-in functions for publishing and subscribing. Here are some commonly used functions.

- `Client.publish(topic, message, [options], [callback])`

  A function to publish a message to a topic, which contains four parameters:

  - topic: the topic to be sent, which is a string
  - message: The message under the topic to be sent, which can be a string or a Buffer
  - options: Optional value. It refers to the configuration information when publishing a message, and is mainly used to set the QoS and Retain value when publishing a message.
  - callback: callback function after the message is published. The parameter is error. This parameter exists only when publishing fails

  ```jsx
  // Send a test message with QoS of 0 to the testtopic
  client.publish('testtopic', 'Hello, MQTT!', { qos: 0, retain: false }, function (error) {
    if (error) {
      console.log(error)
    } else {
      console.log('Published')
    }
  }
  ```

- `Client.subscribe(topic/topic array/topic object, [options], [callback])`

  The function of subscribing to one or more topics. When the connection is successful, you need to subscribe to the topic to get the message. This function contains three parameters:

  - topic: It can pass in a string, or an array of strings, or a topic object,`{'test1': {qos: 0}, 'test2': {qos: 1}}`
  - options: Optional value. The configuration information when subscribing to a topic. It is mainly used to fill in the QoS level of the subscribed topic
  - callback: callback function after subscribing to the topic. The parameters are error and granted. The error parameter only exists when the subscription fails. Granted is an array of {topic, QoS}, where the topic is the subscribed topic and QoS is the QoS level granted to the topic

  ```jsx
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

  ```jsx
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

  ```jsx
  client.end()
  ```

To view a complete example of using MQTT.js in JavaScript, please see: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-JavaScript](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-JavaScript)

### MQTT 5.0

MQTT.js fully supports the MQTT 5.0 protocol, offering numerous new features and improvements. This section demonstrates how to use key MQTT 5.0 features in MQTT.js.

- Session Expiry Interval: Allows clients to specify how long a session should be maintained.

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      protocolVersion: 5,
      clean: true,
      properties: {
        sessionExpiryInterval: 300 // 300 seconds
      }
    })
    ```

- Topic Alias: Reduces network traffic by using short integer aliases instead of long topic strings.

    ```javascript
    client.publish('long/topic/name', 'message', {
      properties: {
        topicAlias: 1
      }
    })

    // Subsequent publishes can use just the alias
    client.publish('', 'another message', {
      properties: {
        topicAlias: 1
      }
    })
    ```

- User Properties: Allows adding custom key-value pairs to messages.

    ```javascript
    client.publish('topic', 'message', {
      properties: {
        userProperties: {
          'custom-key': 'custom-value'
        }
      }
    })
    ```

- Subscription Identifier: Used to identify specific subscriptions.

    ```javascript
    client.subscribe('topic', {
      properties: {
        subscriptionIdentifier: 123
      }
    })

    client.on('message', (topic, message, packet) => {
      if (packet.properties.subscriptionIdentifier === 123) {
        console.log('Message from subscription 123')
      }
    })
    ```

- Request Response Information: Implements a request-response pattern.

    ```javascript
    client.publish('request/topic', 'request', {
      properties: {
        responseTopic: 'response/topic',
        correlationData: Buffer.from('request-1')
      }
    })

    client.subscribe('response/topic')
    client.on('message', (topic, message, packet) => {
      if (packet.properties.correlationData) {
        console.log('Response received for', packet.properties.correlationData.toString())
      }
    })
    ```

- Message Expiry Interval: Sets a lifetime for messages.

    ```javascript
    client.publish('topic', 'message', {
      properties: {
        messageExpiryInterval: 60 // 60 seconds
      }
    })
    ```

- Will Delay Interval: Delays sending the will message.

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      will: {
        topic: 'will/topic',
        payload: 'client gone offline',
        properties: {
          willDelayInterval: 30 // 30 seconds
        }
      }
    })
    ```

- Receive Maximum: Controls the maximum number of unacknowledged PUBLISH packets.

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      properties: {
        receiveMaximum: 100
      }
    })
    ```

- Maximum Packet Size: Specifies the maximum packet size the client is willing to accept.

    ```javascript
    const client = mqtt.connect('mqtt://broker.emqx.io', {
      properties: {
        maximumPacketSize: 100 * 1024 // 100 KB
      }
    })
    ```

These examples showcase some key MQTT 5.0 features in MQTT.js. Using these can enhance your application's flexibility and efficiency. Ensure your MQTT broker supports MQTT 5.0 when using these features.

For full MQTT.js API documentation, including all MQTT 5.0 properties, see the [MQTT.js GitHub repository](https://github.com/mqttjs/MQTT.js).

## MQTT.js Q&A

### Can I implement two-way authentication connections in the browser?

No, it is not possible to specify a client certificate using JavaScript code when establishing a connection in a browser, even if client certificates are set up in your OS certificate store or potentially some type of smart card. This means that MQTT.js cannot do so. Additionally, you cannot specify a Certificate Authority (CA) either, as it is controlled by the browser.

Reference: [https://github.com/mqttjs/MQTT.js/issues/1515](https://github.com/mqttjs/MQTT.js/issues/1515)

### Can I use MQTT.js with TypeScript?

Yes, MQTT.js can be used with TypeScript. It has TypeScript type definitions included in the library.

The type files can be found here: [https://github.com/mqttjs/MQTT.js/tree/main/types](https://github.com/mqttjs/MQTT.js/tree/main/types)

Here is an example code when using TypeScript:

```tsx
import * as mqtt from "mqtt"
const client: mqtt.MqttClient = mqtt.connect('mqtt://broker.emqx.io:1883')
```

### Can I connect to multiple brokers with a single MQTT.js client?

No, each MQTT.js client can only connect to one broker at a time. If you want to connect to multiple brokers, you need to create multiple MQTT.js client instances.

### **Can I use MQTT.js in a Vue, React or Angular application?**

Yes, MQTT.js is a library that can be integrated into any JavaScript-based application, including those using Vue, React or Angular frameworks.

### WebSocket connection cannot be established?

When connecting to WebSocket, if the protocol, port, and Host are all correct, make sure to add the path.

## MQTT.js Advanced

### How to Debug MQTT.js Applications

Debugging MQTT.js applications is an essential part of the development process. This guide explains how to enable MQTT.js debug logs in Node.js and browser environments, and when to use network protocol analyzers like Wireshark for deeper troubleshooting.

**Debugging MQTT.js in Node.js**

In a Node.js environment, you can enable MQTT.js debugging logs by using the `DEBUG` environment variable:

```bash
DEBUG=mqttjs* node your-app.js
```

You will see debugging information printed out, which you can use to compare each step and see what happened to the MQTT message during transmission.

```bash
DEBUG=mqttjs* node index.js
mqttjs connecting to an MQTT broker... +0ms
mqttjs:client MqttClient :: options.protocol mqtt +0ms
mqttjs:client MqttClient :: options.protocolVersion 4 +0ms
mqttjs:client MqttClient :: options.username emqx_test +1ms
mqttjs:client MqttClient :: options.keepalive 60 +0ms
mqttjs:client MqttClient :: options.reconnectPeriod 1000 +0ms
mqttjs:client MqttClient :: options.rejectUnauthorized undefined +0ms
mqttjs:client MqttClient :: options.topicAliasMaximum undefined +0ms
mqttjs:client MqttClient :: clientId emqx_nodejs_986165 +0ms
mqttjs:client MqttClient :: setting up stream +0ms
mqttjs:client _setupStream :: calling method to clear reconnect +1ms
mqttjs:client _clearReconnect : clearing reconnect timer +0ms
mqttjs:client _setupStream :: using streamBuilder provided to client to create stream +0ms
mqttjs calling streambuilder for mqtt +3ms
mqttjs:tcp port 1883 and host broker.emqx.io +0ms
mqttjs:client _setupStream :: pipe stream to writable stream +3ms
mqttjs:client _setupStream: sending packet `connect` +2ms
mqttjs:client sendPacket :: packet: { cmd: 'connect' } +0ms
mqttjs:client sendPacket :: emitting `packetsend` +1ms
mqttjs:client sendPacket :: writing to stream +0ms
mqttjs:client sendPacket :: writeToStream result true +11ms
...
```

Executing this command will generate debugging logs in the console, providing detailed information about the operations of your [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) such as connections, message publishing and subscription, and potential errors.

**Debugging MQTT.js in the Browser**

For debugging in browser environments, you need to set a specific value in the localStorage object in your JavaScript code:

```bash
localStorage.debug = 'mqttjs*'
```

After refreshing your browser with this setting, MQTT.js will start logging detailed debug information to your **browser's Console**, which is especially useful for debugging MQTT over WebSocket connections.

If you're unable to fix your issues using MQTT.js debug logs, try using a network protocol analyzer like Wireshark. It can capture and interpret network traffic between your MQTT.js application and MQTT broker, showing the specifics of MQTT communication, IP addresses, port numbers, and TCP handshakes. By starting with MQTT.js debug logs and switching to Wireshark when needed, you can comprehensively troubleshoot your MQTT.js applications.

### Optimizing Message Processing in MQTT.js Using RxJS

> RxJS is a reactive programming library for JavaScript that follows the observer pattern and functional programming principles. It simplifies handling asynchronous data streams and event streams for developers and offers various operators, including map, filter, and reduce, for transforming and combining these streams.

In practical development, MQTT servers send various types of messages to clients, which need to be processed. For example, we may need to save messages to a database or render them on the UI after processing. However, with MQTT.js, we have to rely on callbacks to handle these messages, and each message received triggers the callback function. This could lead to performance issues with frequent callback invocation, particularly when dealing with high-frequency messages.

By leveraging the powerful functionalities of RxJS, we can handle MQTT.js messages more conveniently and efficiently. RxJS can convert the subscription of MQTT.js messages into observables, which makes it easier for us to handle asynchronous data streams and event streams. Additionally, RxJS provides a range of operators that allow us to transform and filter messages, enabling us to handle them more efficiently. RxJS can also assist us in implementing advanced features such as merging or partitioning multiple streams. Furthermore, RxJS can provide message caching and processing delay functionalities to enable more convenient and flexible handling of complex data streams.

Here, we will demonstrate how to optimize message processing in MQTT.js using RxJS, through a simple example.

```javascript
import { fromEvent } from 'rxjs'
import { bufferTime, map, takeUntil } from 'rxjs/operators'

// Convert the connection close event to an Observable
const unsubscribe$ = fromEvent(client, 'close')

// Convert message subscription to Observable, continue receiving and processing messages until the connection is closed
const message$ = fromEvent(client, 'message').pipe(takeUntil(unsubscribe$)).pipe(
  map(([topic, payload, packet]: [string, Buffer, IPublishPacket]) => {
    return processMessage(topic, payload, packet)
  }),
)

// Use filter to filter out system messages
const nonSYSMessage$ = message$.pipe(filter((message: MessageModel) => !message.topic.includes('$SYS')))

// Use bufferTime to cache messages, and save them to the database in batches at a frequency of once per second.
nonSYSMessage$.pipe(bufferTime(1000)).subscribe((messages: MessageModel[]) => {
  messages.length && saveMessage(id, messages)
})

// Use bufferTime to cache messages and render them on the UI at a rate of twice per second.
nonSYSMessage$.pipe(bufferTime(500)).subscribe((messages: MessageModel[]) => {
  messages.length && renderMessage(messages)
})
```

## Summary

This article has briefly introduced the usage functions of some common APIs of MQTT.js. To learn about [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), wildcards, retained messages, last-will, and other features, check out the [MQTT Guide 2024: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ. Explore more advanced applications of MQTT and get started with MQTT application and service development.

For specific use in actual projects, please refer to the following links.

- [How to Use MQTT in Vue](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [How to Use MQTT in React](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [How to Use MQTT in Angular](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [How to Use MQTT in Electron](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [How to Use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- [MQTT vs WebSocket: Key Differences & Applications](https://www.emqx.com/en/blog/mqtt-vs-websocket)

<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
