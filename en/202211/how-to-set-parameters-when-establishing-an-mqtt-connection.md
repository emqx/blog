Establishing an MQTT connection is the first step in communicating using the MQTT protocol. The MQTT protocol provides rich connection parameters to enable developers to create IoT applications that meet different business needs.

This article introduces the role of each connection parameter in MQTT and helps developers take their first steps in using MQTT.

 

## Introduction to MQTT Connection

MQTT connections are initiated from the client to the broker. Any application or device running the MQTT client library is an [MQTT client](http://mqttx.app/). The [MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) handles client connection, disconnection, subscribe (or unsubscribe) requests, and routes messages up on receiving publish requests.

After establishing a network connection with the broker, the very first message the client must send is a `CONNECT` packet. The broker must reply with a `CONNACK` to the client as a response, and the MQTT connection is established successfully after the client receives the `CONNACK` packet. If the client does not receive a `CONNACK` packet from the broker in time (usually a configurable timeout from the client side), it may actively close the network connection.

MQTT protocol specification does not limit which transport to use, the mostly commonly adopted transport protocol for MQTT is TCP/TLS and Websocket. EMQ has also implemented [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic).

### MQTT over TCP/TLS

TCP/TLS is widely used and is a connection-oriented, reliable, byte-stream-based transport layer communication protocol. It ensures that the bytes received are the same as those sent through the acknowledgment and retransmission mechanism.

MQTT is usually based on TCP/TLS, which inherits many of the advantages of TCP/TLS and can run stably in low bandwidth, high latency, and resource-constrained environments.

### MQTT over WebSocket

With the rapid development of the Web technology, more and more applications can be implemented in the web browser taking advantage of the powerful rendering engine for UI. WebSocket, the native communication method for Web applications, is also widely used.

Many IoT web-based applications such as device monitoring systems need to display device data in real-time in a browser. However, browsers transmit data based on the HTTP protocol and cannot use MQTT over TCP.

The founder of the MQTT protocol foresees the importance of Web applications, so the MQTT protocol supports communication through MQTT over WebSocket since its creation. Check out [the blog](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) for more information on how to use MQTT over WebSocket.

### MQTT over QUIC

QUIC (RFC 9000) is the underlying transport protocol of the next-generation Internet protocol HTTP/3, which provides connectivity for the modern mobile Internet with less connection overhead and message latency compared to TCP/TLS protocols.

Based on the advantages of QUIC, which make it highly suitable for IoT messaging scenarios, EMQX 5.0 introduces MQTT over QUIC. Check out [the blog](https://www.emqx.com/en/blog/mqtt-over-quic) for more information.


## Use of MQTT Connection Parameters

### Connection Address

The connection address of MQTT usually includes the broker IP (or domain name), broker port, and protocol. In case of clustered MQTT brokers, there is typically a load-balancer put in front, so the IP or domain name might actually be the load-balancer.

**TCP-based MQTT connections**

For example, `mqtt://broker.emqx.io:1883` is a TCP-based MQTT connection address, and `mqtts://broker.emqx.io:1883` is a TLS/SSL based MQTT secure connection address.

> In some client libraries, TCP-based connection is `tcp://ip:1883`

**WebSocket-based connection**

The connection address also needs to contain the Path when using a WebSocket connection. The default Path configured for [EMQX](http://www.emqx.io/) is `/mqtt`.

For example, `ws://broker.emqx.io:8083/mqtt` is a WebSocket-based MQTT connection address, and `wss://broker.emqx.io:8083/mqtt` is a WebSocket-based MQTT secure connection address.

### Client ID

The MQTT Broker uses Client ID to identify clients, and each client connecting to the broker must have a unique Client ID. Client ID is a UTF-8 encoded string. If the client connects with a zero-length string, the broker should assign a unique one for it.

Depending on the MQTT protocol version and implementation details of the broker, the valid set of characters accepted by the broker varies. The most conservative scheme is to use characters `[0-9a-zA-Z]` and limit the length to 23 bytes.

**Due to the uniqueness nature of the Client ID,  if two clients connect to the same broker with the same Client ID, the client connects later will force the one connected earlier to go offline.**

### Username & Password

The MQTT protocol supports username-password authentication, but if the underlying transport layer is not encrypted, the username and password will be transmitted in plaintext, hence for the best security,`mqtts` or `wss` protocol is recommended.

Most MQTT brokers default to allow anonymous login, meaning there is no need to provide username or password (or set empty strings).

### Connect Timeout

The waiting time before receiving the broker `CONNACK` packet, if the `CONNACK` is not received within this time, the connection is closed.

### Keep Alive

Keep Alive is an interval in seconds. When there is no message to send, the client will periodically send a heartbeat message to the broker according to the value of Keep Alive to ensure that the broker will not disconnect the connection.

After the connection is established successfully, if the broker does not receive any packets from the client within 1.5 times of Keep Alive, it will consider that there is a problem with the connection with the client, and the broker will disconnect from the client.

Check out [the blog](https://www.emqx.com/en/blog/mqtt-keep-alive) for more details on Keep Alive.

### Clean Session

Set to `false` means to create a persistent session. When the client disconnects, the session remains and saves offline messages until the session expires. Set to `true` to create a new temporary session that is automatically destroyed when the client disconnects.

The persistent session makes it possible for the subscribe client to receive messages while it has gone offline. This feature is very useful in IoT scenarios where the network is unstable.

The number of messages the broker keeps for persistent sessions depends on the broker's settings. For example, [the public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ is set to keep offline messages for 5 minutes, and the maximum number of messages is 1000 (for QoS 1 and QoS 2 messages).

> **Note:** The premise of persistent session recovery is that the client reconnects with a fixed Client ID. If the Client ID is dynamic, then a new persistent session will be created.

Check out [the blog](https://www.emqx.com/en/blog/mqtt-session) for more details on Clean Session.

### Last Will

When an MQTT client that has set a Will Message goes offline abnormally, the MQTT broker publishes the Will Message set by that client.

> **Unexpected offline includes**: the connection is closed by the server due to network failure; the device is suddenly powered off; the device attempts to perform an unallowable operation and the connection is closed by the server, etc.

The Will Message can be seen as a simplified MQTT message that also contains Topic, Payload, QoS, Retain, etc.

- When the device goes offline unexpectedly, the will message will be sent to the `Will Topic`.

- The `Will Payload` is the content of the message to be sent.

- The `Will QoS` is the same as the QoS of standard MQTT messages. Check out [the blog](https://www.emqx.com/en/blog/introduction-to-mqtt-qos) to learn more about MQTT QoS.

- The `Will Retain` set to `true` means the will message is a retained message. Upon receiving a message with the `retain` flag set, the MQTT broker must store the message for the topic to which the message was published, and it must store only the latest message. So the subscribers which are interested in this topic can go offline, and reconnect at any time to receive the latest message instead of having to wait for the next message from the publisher after the subscription.

  Check out [the blog](https://www.emqx.com/en/blog/mqtt5-features-retain-message) to learn more about MQTT Retained.

### Protocol

The most used versions of the MQTT protocol are MQTT v3.1, MQTT v3.1.1, and MQTT v5.0. Currently, MQTT 5.0 has become the protocol of choice for most IoT enterprises, and we recommend that first-time MQTT developers use this version directly.

Check out the [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) blog series provided by EMQ to learn about using the new features of MQTT 5.0.

### New Connection Parameters in MQTT v5.0

**Clean Start & Session Expiry Interval**

Clean Session was removed in MQTT 5.0, but Clean Start and Session Expiry Interval were added.

When Clean Start is `true` it discards any existing session and creates a new session. A `false` value means that the server must use the session associated with the Client ID to resume communication with the client (unless the session does not exist).

If Session Expiry Interval is set to 0 or is absent, the session ends when the network connection is closed. If it is `0xFFFFFFFF` (UINT_MAX), the session does not expire. If it is greater than 0, the number of seconds the session will remain after the network connection is closed.

Check out [the blog](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) to learn more about Clean Start & Session Expiry Interval.

**Connect Properties**

MQTT 5.0 also adds new connection properties to enhance the extensibility of the protocol. Check out [the blog](https://www.emqx.com/en/blog/mqtt5-connect-properties) to learn more about Connect Properties.

## How to establish a secure MQTT connection?

Although the MQTT protocol provides authentication mechanisms such as username-password, Client ID, etc., this is not enough for IoT security. With TCP-based plaintext transmission communication, it is difficult to guarantee data security.

TLS (Transport Layer Security), or in some context, the new-deprecated name SSL, aims primarily to provide privacy and data integrity between two or more communicating computer applications. Running on top of TLS, MQTT can take full advantage of its security features to secure data integrity and client trustworthy.

The steps to enable SSL/TLS vary from MQTT broker to MQTT broker. EMQX has built-in support for TLS/SSL, including support for one-way/two-way authentication, X.509 certificates, load-balanced SSL, and many other security certifications.

One-way authentication is a way to establish secure communication only by verifying the server certificate. It ensures the communication is encrypted but cannot verify the client's authenticity. It usually needs to be combined with authentication mechanisms such as username-password and client ID. Check out [the blog](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) to learn how to establish a secure One-way authenticated MQTT connection.

Two-way authentication means that both the server and the client must provide certificates when authenticating communications, and both parties need to authenticate to ensure that the other is trusted. Some application scenarios with high-security requirements require Two-way authentication to be enabled. Check out [the blog](https://www.emqx.com/en/blog/enable-two-way-ssl-for-emqx) to learn how to establish a secure Two-way authenticated MQTT connection.

> **Note:** If you use MQTT over WebSocket on the browser, Two-way authentication communication is not yet supported.
>
> [How to use TLS/SSL two-way authentication connections in browser? · Issue #1515 · mqttjs/MQTT.js](https://github.com/mqttjs/MQTT.js/issues/1515) 


## Summary

At this point, you should have a good understanding of how MQTT connections are established and the role of each connection parameter.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt) series of articles provided by EMQ to learn about MQTT Topics, Wildcards, Retained Messages, Last-Will, and other features. Explore more advanced applications of MQTT and get started with MQTT application and service development.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
