## Overview

**MQTT** is an application layer protocol based on the TCP protocol and work in TCP/IP protocol cluster, and designed and developed by IBM in 1998. MQTT uses a lightweight publish/subscribe pattern for message transmission. It is designed to provide reliable network services for IoT devices in low-bandwidth and unstable network environments. Devices need to connect to the **MQTT broker** for messaging communication.

Among many **IoT protocols**, MQTT is accepted by more and more enterprises due to its openness, lightweight, energy-saving, universality, etc. It has become the fact standard of IoT communication protocols. However, due to the particularity of the industry or other reasons, there are a large number of communication protocols that are based on TCP/IP in the IoT industry: the scaled standard industry protocol(such as power, road traffic, industrial control), and the private protocol developed by companies, projects, and even individuals. Both new and old projects may encounter the dilemma of not being able to use the **MQTT protocol**.



## Problems in the traditional private TCP protocol of the IoT industry

TCP protocol communication involves network programming. Both the client and the server software needs to deal with complex network environments, business logic, and component architecture issues. In actual development, each component needs to balance performance and stability, and also needs to take security and usability into account, which has brought great difficulty to development.

Besides, the private TCP protocol has fewer users due to its relative niche or strong industry specificity, it often lacks an excellent client and server software. With the development of the business, the number of devices increases, the communication traffic exceeds expectations and the functional requirements increase and change, the potential problems in the entire business will be amplified:

- The performance of the single server is poor, the horizontal expansion is relatively difficult, and the service capacity limits the business growth;
- It is difficult to add or modify functions on the server/client, which restricts the development of application layer functional requirements;
- The lack of reliable operation and maintenance system, results in inaccurate and untimely problems for operation and maintenance management.

As an excellent [open source MQTT broker](https://www.emqx.com/en/products/emqx), based on supporting high-performance, large-scale standard [MQTT protocol](https://www.emqx.com/en/mqtt) access to millions of devices, and supporting cluster level expansion, [EMQX](https://www.emqx.com/en) expanded private TCP protocol access and integrated a large number of out-of-the-box functions: multiple ways of authentication, publish/subscribe ACL control, rule engine message processing, message storage and bridge, complete monitoring operation and maintenance system and external REST API control call, etc.

On the basis of high performance and high scalability, [EMQX](https://www.emqx.com/en) opens up the upper-layer application to control the entire life cycle of device connection/communication and data interaction channels, allowing users to quickly complete the development of **loT applications**.

At present, EMQX provides a complete private TCP access solution through server adaptation/device-side adaptation:

- **Server adaptation:** For the existing private TCP protocol, adjust the server function without changing the old network device to add the right adapter plug. After the adaptation, the device can be seamlessly migrated and connected to EMQX MQTT broker;
- **Device-side adaptation:** For new devices, development and adjustment on the device side was done according to **the EMQ private TCP protocol specification** provided by EMQ and accessed SDKs After the adaptation, the device can be seamlessly migrated and connected to EMQX.

## Private TCP protocol device access example

The connection of the EMQX TCP private protocol eliminates the difference with the MQTT connection at the application layer. Taking the **emqx-tcp** plug as an example, some configuration items are as follows:

```bash
## Upsream topic
##
## Placeholder:
##   - %c: ClientId of access client
##   - %u: Username of access client
tcp.proto.up_topic = tcp/%c/up

## Downstream topic. After the client access is successful, emqx-tcp will ## subscribe to this topic, to receive the message sent by the EMQ system ## to this type of client
##
## Placeholder:(Same as above)
tcp.proto.dn_topic = tcp/%c/dn
```

From the configuration items, we can see the communication mode of private TCP protocol access:

- The upstream message of the client will be published to the topic `tcp/%c/up`, and other EMQX clients including applications can subscribe to this topic to receive private TCP protocol device information;
- Messages can reach the client if they are been sent to `tcp/%c/dn` through the built-in REST API of EMQX or any client.

Therefore, we have established two-way communication with the client that has established the private TCP protocol. At the same time, the client can use the built-in authentication components for authentication before accessing. When the message arrives, it can also use the publish/subscribe ACL components for accessing control. In the whole link, the rule engine, message bridge, and persistence components can also process this part of data after configuring relevant rules.



## Server adaptation

The service that EMQ provides customers with private payment development and customization, also includes private TCP protocol access adaptation projects.

The server adaptation aims to the existing private TCP protocol and adjusts the server function without changing the old network device. After the adaptation, the device can seamlessly migrate and connect to EMQX. In the EMQX system layer, the **connection layer** is responsible for processing the server Socket connection and MQTT protocol codec, and its functions are as follows:

1. Asynchronous TCP server based on [eSockd](https://github.com/emqx/esockd) framework
2. TCP Acceptor pool and asynchronous TCP Accept
3. TCP/SSL, WebSocket/SSL connection support
4. The limitation of maximum number of concurrent connections
5. Access control based on IP address (CIDR)
6. Flow control based on **Leaky Bucket**
7. MQTT protocol codec
8. MQTT protocol heartbeat detection
9. MQTT protocol packet processing


![image20191112155608683.png](https://static.emqx.net/images/b64b6dce3d716e39d4f6e0c27e7dfef3.png)

<center>Figure 1 EMQX functional architecture diagram, and the red box in the figure is the private TCP/UDP protocol layer</center>

In the current architecture design, to adapt to a specific private TCP protocol, only need to extend the corresponding protocol codec and message processing functions at the connection layer. After the user extends the EMQX protocol adapter with plugins, the private protocol TCP device can directly access the EMQX without going through the gateway/proxy server, allowing project development and use to fully enjoy the convenience brought by EMQX.



## Device side adaptation: EMQ private TCP protocol specification

For the new device, development and adjustment on the device side was done according to the **EMQ private TCP protocol specification** provided by EMQ and accessed SDK. After adaptation, the device can seamlessly migrate and connect to [EMQX](https://www.emqx.com/en). 

Based on the experience of developing and customizing the private TCP protocol in several mature projects, EMQ has launched a universal access specification based on the TCP private protocol, **EMQ private TCP protocol specification**. It is more lightweight than the MQTT protocol and provides a complete solution for private TCP Access.

EMQX TCP includes a private TCP protocol standard and corresponding access plug **emqx-tcp**. The design principles of the entire specification are as follows:

1. **Lightweight:** Minimize the byte size of the header and control fields;
2. **Simple:** Private TCP protocol, whose main function is to transparently transmit the upper-layer applications/protocols data packets. Therefore, the function should be concise and focus on transparent transmission;
3. **Reliable:** Ensure the orderly reachability of messages.

As an access module close to the end in the specification, **emqx-tcp** can divide the entire message exchange process into three parts: the client side, broker side and another side, according to its functional logic and the relationship of the entire system.

```
|<-- Terminal -->|<--------- Broker Side --------->|<---  Others  --->|
|<-    Side    ->|                                 |<--    Side    -->|

+---+                                                PUB  +-----------+
| D |  INCOMING  +----------+    PUB     +---------+   -->| subscriber|
| E |----------->|          |----------->|         |--/   +-----------+
| V |            | emqx-tcp |            |  EMQX  |
| I |<-----------|          |<-----------|         |<--   +-----------+
| C |  OUTGOING  +----------+    PUB     +---------+   \--| publisher |
| E |                                                PUB  +-----------+
+---+
```

1. On the client side, access can be implemented through the TCP private protocol defined by EMQX TCP, and then implement data reporting or receive downstream messages.
2. On the platform side, the main body is the emqx-tcp access plug and EMQX system. emqx-tcp is responsible for the encoding and decoding of packets, and proxy subscribes to the downstream topics. It can implement the conversion of upstream messages into **MQTT messages** in the EMQX system and PUBLISH them into the entire system; It also converts the downstream MQTT messages into TCP private protocol packet structures and deliver them to the terminal.
3. On the other side, you can subscribe to the topic of the upstream **PUBLISH message** that appears in the previous item to receive the upstream message, or to publish messages to specific downstream topics to send data to the terminal side.



## Comparison of two adaptation methods

Currently **EMQX TCP protocol specification** and **emqx-tcp** plugins are distributed with [EMQX Enterprise](https://www.emqx.com/en/products/emqx). The users of EMQX Enterprise can freely use this part of the function to driver device-side and develop communication, according to EMQ private TCP protocol specification, and private TCP protocol access can be adapted from the device side.

However, there are many kinds of the device side protocols in actual IoT projects. When the old projects or industry-related projects use other private TCP protocol specifications, the **emqx-tcp** plug is not directly applicable. At this time, it needs to adapt from the server.

The more value of **EMQX TCP protocol specification** and **emqx-tcp** plugs is built on the experience of many projects, providing a mature solution for enterprise private TCP protocol customization.

Only EMQX Enterprise Edition supports the private TCP protocol access adaptation. After the adaptation, EMQX Enterprise and corresponding function plugins are delivered. Open source users with Erlang development experience can also develop and implement it by themselves.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a >
</section>
