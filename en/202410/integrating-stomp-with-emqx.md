## Introduction to STOMP

STOMP (Simple/Streaming Text-Oriented Messaging Protocol) is designed to provide a simple and transparent way for asynchronous message communication across different languages and platforms.

As a text-based protocol, STOMP facilitates interoperable message exchange between clients and servers. It transmits data using frames, each containing a command, an optional header, and an optional body. STOMP defines standard commands like CONNECT, SEND, SUBSCRIBE, and DISCONNECT, which enable structured interaction between clients and servers.

### **How It Works**

The STOMP operates in an intuitive manner. First, a client establishes a connection with a server by sending a CONNECT frame. Once connected, the client can either send messages to a destination using the SEND frame or subscribe to receive messages from a specific destination using the SUBSCRIBE command. The server delivers messages to subscribed clients via a MESSAGE frame. Either party can close the connection by sending a DISCONNECT frame.

### **Features and Benefits**

Key features and benefits of STOMP include:

- **Simplicity**: Its plain-text design is easy to understand and implement.
- **Cross-Language**: Being a text-based protocol, it can be implemented in any programming language, promoting compatibility across environments.
- **Interoperability**: Provides a standardized messaging method that works across different platforms and languages.
- **Flexibility**: Supports customization and extensions through headers, allowing adaptation to various messaging scenarios.

### **Comparison with Other IoT Protocols**

Compared to other popular IoT protocols like [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) and [CoAP](https://www.emqx.com/en/blog/coap-protocol), STOMP offers advantages in simplicity and flexibility. While MQTT excels in bandwidth-constrained environments due to its lightweight publish/subscribe model, its binary message format lacks the cross-language flexibility of STOMP. CoAP, designed for low-power devices, is ideal for constrained environments, whereas STOMP is more suitable for scenarios requiring greater flexibility and simple text messaging.

In summary, the STOMP protocol, with its intuitive design and cross-language compatibility, is a powerful tool for building flexible and scalable IoT applications. When used appropriately, it can significantly enhance the efficiency and interoperability of messaging systems.

## Accessing STOMP Devices with EMQX

EMQX is a powerful, highly scalable distributed MQTT platform designed for IoT and real-time communication applications. In addition to fully supporting the MQTT protocol, EMQX manages connectivity, authentication, and messaging for various non-MQTT protocols, including STOMP, MQTT-SN, CoAP, and LwM2M, through a unified gateway interface for easier use.

The STOMP gateway in EMQX is based on [STOMP v1.2](https://stomp.github.io/stomp-specification-1.2.html) and is compatible with versions v1.0 and v1.1. In the following steps, we’ll use EMQX’s STOMP gateway to connect to STOMP devices.

### Preparation

#### Installing EMQX 5.8.0

EMQX offers download and installation guides for various platforms: [https://docs.emqx.com/en/emqx/latest/deploy/install-enterprise.html](https://docs.emqx.com/en/emqx/latest/deploy/install-enterprise.html).

For this example, we will launch EMQX Enterprise 5.8.0 using Docker:

```shell
docker run -p 18083:18083 -p 1883:1883 -p 61613:61613 emqx/emqx-enterprise:5.8.0
```

#### Configuring the STOMP Gateway

Open the EMQX Dashboard at `http://127.0.0.1:18083` and log in with the default credentials: admin/public. Navigate to Management → Gateways to view the available gateways in the current version.

![EMQX Dashboard](https://assets.emqx.com/images/8d73555d5e00aba577c960f63d8df70a.png)

Click the Configure button for the STOMP gateway to access the configuration page. Use the default settings and click Next several times until the configuration is complete. You will see that the gateway has started successfully.

![Enable STOMP](https://assets.emqx.com/images/057cedcb5f72c2cb1c92039e8edb779b.png)

### Testing Connection

The STOMP protocol is available in various programming languages. Here, we'll use [STOMPjs](https://www.npmjs.com/package/stompjs) in Node.js as an example to connect to the EMQX STOMP gateway.

First, initialize the project and install STOMPjs:

```shell
mkdir STOMP-client-test 
cd STOMP-client-test

npm install STOMPjs
```

Once installed, create a connect.js file:

```javascript
var STOMP = require('STOMPjs');

var client = STOMP.overTCP('localhost', 61613);

client.connect('username', 'password', function() {
    console.log('connected to STOMP gateway');
});
```

Run the connect.js file and check the output:

```shell
node connect.js
```

After a successful connection, open the EMQX Dashboard and navigate to the Client List page of the STOMP gateway to see your client.

![Client List page](https://assets.emqx.com/images/406bd75e8d6b210c6f42015e28427e4a.png)

### Testing Message Communication

In the STOMP protocol, clients receive messages on a topic by subscribing to a specific topic, while publishers send messages by specifying the destination parameter, similar to the MQTT messaging model.

To start a STOMP subscriber client, use the following code:

```javascript
var STOMP = require('STOMPjs');

var client = STOMP.overTCP('localhost', 61613);

client.connect('username', 'password', function() {
    console.log('connected to STOMP gateway');
    console.log('subscribing to /queue/test');
    client.subscribe('/queue/test', function(message) {
        console.log('received message: ' + message.body);
    });
});
```

Then, use MQTTX to publish a message to the topic /queue/test:

```shell
mqttx pub -t /queue/test -m 'Hi, STOMP Client'
```

You should see that the STOMP client successfully connects to EMQX and prints the received message:

```shell
connected to STOMP gateway
subscribing to /queue/test
received message: Hi, STOMP Client
```

Now, the STOMP client is successfully connected to EMQX and can send and receive messages with the MQTT client. You can also manage all STOMP clients through the EMQX Dashboard.

## Advanced STOMP Gateway Applications

### Enabling TLS Listening

The EMQX 5.0 STOMP gateway supports SSL connections. To enable this, open the EMQX Dashboard, navigate to Management → Gateways, select the Settings for the STOMP gateway, go to the Listener sub-page, and click Add.

![Management → Gateways](https://assets.emqx.com/images/c8542ec0b0fccea6641f2f043f7c57d9.png)

### Access Authentication

The STOMP gateway also supports username and password authentication to verify client credentials during the connection process.

To set this up, open the EMQX Dashboard, go to Management → Gateways, select the Settings for the STOMP gateway, then navigate to the Access Authentication sub-page and click Add to create built-in authentication based on username and password.

![Access Authentication](https://assets.emqx.com/images/d03768cdbb9113e47e50054567ce59ff.png)

## Conclusion

This blog outlines the STOMP protocol and demonstrates how to establish STOMP connections through the EMQX Platform's STOMP gateway, enabling message forwarding and interoperability with MQTT messages.

By integrating EMQX with STOMP, users can achieve efficient, unified, and multi-protocol client management and message processing in the same platform, simplifying system complexity.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
