## MQTT Protocol Introduction

### Overview

[MQTT](https://mqtt.org/) is a lightweight messaging protocol based on publish/subscribe model, specifically designed for IoT applications in low bandwidth and unstable network environments. It can provide real-time reliable messaging services for network-connected devices with minimal code. MQTT protocol is widely used in IoT, Mobile Internet, Smart Hardware, Internet of Vehicles, Smart Cities, Telemedicine, Power, Oil, Energy, and other fields.

MQTT was created by [Andy Stanford-Clark](http://en.wikipedia.org/wiki/Andy_Stanford-Clark) of IBM, and Arlen Nipper (then of Arcom Systems, later CTO of Eurotech). According to Nipper, MQTT must have the following features:

- Simple and easy to implement
- QoS support (complex device network environment)
- Lightweight and bandwidth-saving (because bandwidth was expensive back then)
- Data irrelevant (Payload data format does not matter)
- Continuous session awareness (always know whether the device is online)

According to Arlen Nipper on [IBM Podcast](https://f.hubspotusercontent00.net/hubfs/6941105/Que%20es%20MQTT%20-%20IBM%20podcast%20-%20Piper,%20Diaz,%20Nipper%20-%2011182011-1.pdf), MQTT was originally named `MQ TT`. Note the space between `MQ` and `TT`. The full name is MQ Telemetry Transport. It is a real-time data transmission protocol that he developed while working on a crude oil pipeline SCADA system for Conoco Phillips in the early 1990s. Its purpose was to allow sensors to communicate with IBM's MQ Integrator via [VSAT](https://en.wikipedia.org/wiki/Very-small-aperture_terminal), which has limited bandwidth. The name `MQ TT` was chosen in accordance with industry practice because Nipper is a remote sensing and data acquisition and monitoring professional.

### Comparison Between MQTT and Other Protocols

**MQTT vs HTTP**

- With a minimum message size of 2 bytes, MQTT takes up less network overhead than HTTP.
- Both MQTT and HTTP can use TCP connections and achieve stable and reliable network connections.
- MQTT is based on a publish-subscribe model and HTTP is based on request-response, so MQTT supports duplex communication.
- MQTT can push messages in real-time, but HTTP needs polling for data updates.
- MQTT is stateful, but HTTP is stateless.
- MQTT can recover connections from abnormal disconnections, which HTTP cannot achieve.

**MQTT vs XMPP**

MQTT protocol is simple and lightweight in design and flexible in routing. It will completely replace the PC-era XMPP protocol in the fields of Mobile Internet and IoT messaging.

- MQTT messages are small and easy to encode and decode, while XMPP is based on heavy XML, and the messages are large and cumbersome to interact with.
- MQTT is based on a publish-subscribe model, which is more flexible than XMPP's JID-based point-to-point message routing.
- MQTT supports different types of messages such as JSON, binary, etc. XMPP uses XML to carry messages, and binary must be Base64 encoded and processed by other methods.
- MQTT guarantees reliable message transmission through QoS; the XMPP protocol does not define a similar mechanism.


## Why is MQTT The Best Protocol for IoT?

According to the latest research report “Status of the IoT Spring 2022” from IoT Analytics, the IoT market is expected to grow 18% and reach 14.4 billion active connections by 2022.

Under such large-scale IoT demand, massive device access and device management pose huge challenges to network bandwidth, communication protocols, and platform service architecture. For **IoT protocols**, several key issues in IoT device communication must be addressed in a targeted manner: complex and unreliable network environment, small memory and flash memory capacity, and limited processor ability.

MQTT protocol was created to address these issues. After many years of development, it has become the preferred protocol for the IoT industry with its advantages of lightweight, efficiency, reliable messaging, massive connection support, secure bidirectional communication, and so on.

![IoT Protocols](https://assets.emqx.com/images/a9926090d622d5f96789b9dc325da7c9.jpg)

### Lightweight and Efficient

MQTT minimizes the extra consumption occupied by the protocol itself, and the minimum message header only needs to occupy 2 bytes. It can run stably in bandwidth-constrained network environments. At the same time, MQTT clients need very small hardware resources and can run on a variety of resource-constrained edge devices.

### Reliable Message Delivery

The MQTT protocol provides 3 levels of Quality of Service for messaging, ensuring reliable messaging in different network environments.

- **QoS 0**: The message is transmitted at most once.

  If the client is not available at that time, the message is lost. After a publisher sends a message, it no longer cares whether it is sent to the other side or not, and no retransmission mechanism is set up.

- **QoS 1**: The message is transmitted at least once.

  It contains a simple retransmission mechanism: the publisher sends a message, then waits for an ACK from the receiver, and resends the message if the ACK is not received. This model guarantees that the message will arrive at least once, but it does not guarantee that the message will be repeated.

- **QoS 2**: The message is transmitted only once.

  A retransmission and duplicate message discovery mechanism is designed to ensure that messages reach the other side and arrive strictly only once.

More about MQTT QoS can be found in the blog: [Introduction to MQTT QoS](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

In addition to QoS, MQTT provides a mechanism of [Clean Session](https://www.emqx.com/en/blog/mqtt-session). For clients that want to receive messages that were missed during the offline period after reconnecting, you can set the Clean Session to `false` at connection time. At this time, the server will store the subscription relationship and offline messages for the client and send them to the client when the client is online again.

### Connect Massive IoT Devices

Since its birth, MQTT protocol has taken into account the growing mass of IoT devices. Thanks to its excellent design, MQTT-based IoT applications and services can easily have the capabilities of high concurrency, high throughput, and high scalability.

The support of [MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) is indispensable to the connection of massive IoT devices. Currently, the MQTT broker that supports the largest number of concurrent connections is EMQX. The recently released [EMQX 5.0](https://www.emqx.com/en/blog/emqx-v-5-0-released) achieved [100 million MQTT connections](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connections) + 1 million per second messages through a 23-node cluster, making itself the most scalable MQTT broker in the world to date.

### Secure Bi-directional Communication

Relying on the publish-subscribe model, MQTT allows bidirectional messaging between devices and the cloud. The advantage of the publish-subscribe model is that publishers and subscribers do not need to establish a direct connection or be online at the same time. Instead, the message server is responsible for routing and distributing all messages.

Security is the cornerstone of all IoT applications. MQTT supports secure bidirectional communication via TLS/SSL, while the client ID, username and password provided in the MQTT protocol allow users to implement authentication and authorization at the application layer.

### Keep Alive and Stateful Sessions

To cope with network instability, MQTT provides a [Keep Alive](https://www.emqx.com/en/blog/mqtt-keep-alive) mechanism. In the event of a long period of no message interaction between the client and the server, Keep Alive keeps the connection from being disconnected. If the connection is disconnected, the client can instantly sense it and reconnect immediately.

At the same time, MQTT is designed with [Last Will](https://www.emqx.com/en/blog/use-of-mqtt-will-message) which allows the server to help the client post a will message to a specified [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) if the client is found to be offline abnormally.

In addition, some MQTT brokers, such as EMQX, also provide online and offline event notifications. When the backend service subscribes to a specific topic, it can receive all the clients' online and offline events, which helps the backend service unify the processing of the client’s online and offline events.


## MQTT 5.0 and MQTT 3.1.1

Four years after MQTT 3.1.1 was released and became an OASIS standard, MQTT 5.0 was released. This is a major improvement and upgrade. It is designed to not only meet the current industry needs, but also to make adequate preparation for the future development of the industry.

Based on the 3.1.1 version, MQTT 5.0 adds the features of session/message delay, reason codes, topic aliases, user properties, shared subscriptions and so on, which better meet the needs of modern IoT applications. It improves the performance, stability, and scalability of large systems. Currently, MQTT 5.0 has become the preferred protocol for most IoT enterprises, and we recommend that developers who are new to MQTT use this version directly.

If you want to learn more about MQTT 5.0, you can try reading our [MQTT 5.0 Explore](https://www.emqx.com/en/mqtt/mqtt5) series of articles, which will introduce you to the important features of MQTT 5.0 in an easy-to-understand way.


## MQTT Broker

The MQTT broker is responsible for receiving client-initiated connections and forwarding messages sent by the client to some other eligible clients. A mature MQTT broker can support massive connections and millions of messages throughput, helping IoT business providers focus on business functionality and quickly create a reliable MQTT application.

[EMQX](https://www.emqx.io/) is a widely-used large-scale distributed MQTT broker for IoT. Since its open-source release on GitHub in 2013, it has been downloaded by more than 10 million times worldwide and the cumulative number of connected IoT key devices exceeds 100 million.

You can install EMQX 5.0 open-source version with the following Docker command to experience it.

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

You can also create fully hosted MQTT services directly on EMQX Cloud.  [Free trial of EMQX Cloud](https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new) is available, with no credit card required.


## MQTT Client

MQTT applications usually need to implement MQTT communication based on MQTT client libraries. At present, basically all programming languages have matured open-source MQTT client libraries. So, you can refer to the [Comprehensive list of MQTT client libraries](https://www.emqx.com/en/mqtt-client-sdk) collated by EMQ to choose a suitable client library to build an MQTT client that meets their business needs. You can also visit the [MQTT Programming](https://www.emqx.com/en/blog/tag/mqtt-client-programming) blog series provided by EMQ to learn how to use MQTT in Java, Python, PHP, Node.js and other programming languages.

MQTT application development is also inseparable from the support of the MQTT testing tool. An easy-to-use and powerful MQTT testing tool can help developers shorten the development cycle and create a stable IoT application.

[MQTTX](https://mqttx.app/) is an open-source cross-platform desktop client. It is easy to use and provides comprehensive MQTT 5.0 functionality, feature testing, and runs on macOS, Linux and Windows. It also provides command line and browser versions to meet MQTT testing needs in different scenarios. You can visit the MQTTX website to download and try it out: https://mqttx.app/.

![MQTT Client](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)


## Quick Start with MQTT

At this point, I believe you have a preliminary understanding of the MQTT protocol. Next, you can visit the blog [The Easiest Guide to Getting Started with MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) to learn how to start using MQTT, or check out [Learn MQTT](https://www.emqx.com/en/mqtt) series of articles to learn about MQTT protocol features, explore more advanced applications of MQTT, and start MQTT application and service development.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
