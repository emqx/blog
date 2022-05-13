With the advent of the 5G era, the great vision of the IoT is becoming a reality. The number of connected **IoT devices** has reached 7 billion[^1] in 2018. In the next two years, smart water and electricity meters alone will exceed 1 billion[^2].

![Numberofglobaldeviceconnections20152025NumberofIoTDevices.png](https://assets.emqx.com/images/1abe97466e35ce3fd89417f6ea2fec86.png)

Massive device access and device management have brought great challenges to network bandwidth, communication protocols, and platform service architecture. For the **IoT protocol** , several key issues of IoT device communication must be specifically addressed, including that its network environment is complex and unreliable, its memory and flash memory capacity is small, and its processing capacity is limited.

[MQTT protocol](https://www.emqx.com/en/mqtt) is an IoT communication protocol based on the Publish/Subscribe model. With its characteristics of simple and easy implementation, support for QoS, and small size of packet, it occupies half market of the Internet of Things protocol:

![WechatIMG10934.png](https://assets.emqx.com/images/c980ab99489d1e771ad7b4dc5ac722b9.png)

## The birth of MQTT

MQTT was created by [Andy Stanford-Clark](https://en.wikipedia.org/wiki/Andy_Stanford-Clark) of IBM, and Arlen Nipper (then of Arcom Systems, later CTO of Eurotech).[^3]

According to Arlen Nipper's [self introduction on IBM Podcast ](https://www.ibm.com/podcasts/software/websphere/connectivity/piper_diaz_nipper_mq_tt_11182011.pdf), the original name of MQTT was `MQ TT`, note the space between `MQ` and `TT `, and its full name is MQ Telemetry Transport, which is a real-time data transmission protocol developed by him during a crude oil pipeline data acquisition and monitoring system (pipeline SCADA system) in Conoco Phillips. Its purpose is to allow the sensor to communicate with IBM's MQ Integrator via a limited bandwidth [VSAT](https://en.wikipedia.org/wiki/Very-small-aperture_terminal), Since Nipper is a professional in remote sensing and data acquisition and monitoring, he gave the name `MQ TT` according to industry practice.

## MQTT design principles

According to Nipper, MQTT must be simple and easy to implement, and support QoS (the equipment network environment is complex). It must be lightweight and bandwidth-saving (because bandwidth is expensive at that time), and must be data-independent (don't care about the payload data format). It must be continuous session awareness (knowing if the device is online at all times). Several core features of MQTT (version 3.1.1) will be introduced below, which respectively correspond to the implementation of these design principles.

### Flexible topic design for publishing and subscribing

The publish-subscribe model is a decoupling solution of the traditional Client/Server mode. The publisher communicates with the consumer through the Broker. The role of the Broker is to correctly send the received message to the consumer through some sort of `filtering rule`. The benefits of the publish/subscribe model over the client/server model are:

- The publisher and the consumer do not need to know the existence of the other party in advance. For example, they do not need to communicate the other party's IP Address and Port in advance.
- There is no need to run publisher and consumer at the same time, because the broker is always running.

In the MQTT protocol, the `filtering rules` mentioned above are `Topic`. For example: All messages published to the topic `news` will be forwarded by broker to subscribers who have subscribed to `news`:


![image.png](https://assets.emqx.com/images/a97a07cccc199f387b7eb6747eb2223f.png)



In the figure above, the subscribers subscribe to `news`, and then the publisher publishes a message "some msg" to Broker and publishes it to the `news` topic. The broker decides to forward this message to the subscriber by matching the topic.

MQTT topics have a hierarchical structure and support wildcards `+` and `#`:

- `+` is a wildcard that matches a single level. For example, `news/+` can match `news/sports`, and `news/+/basketball` can match `news/sports/basketball`.
- `#` is a wildcard of one to multiple levels. For example, `news/#` matches `news`, `news/sports`, `news/sports/basketball`, and `news/sports/basketball/x`, etc.

MQTT topics are not created in advance. When a publisher sends a message to a topic, or when a subscriber subscribes to a topic, the broker automatically creates the topic.

### Minimize bandwidth consumption

The MQTT protocol minimizes the additional consumption of the protocol itself, and the message header requires only a minimum of 2 bytes.

The message format of MQTT is divided into three parts:

| **Fixed-length header, 2 bytes, available in all types of message** |
| ------------------------------------------------------------ |
| Variable-length header, only in certain types of message     |
| Payload, only in certain types of message                    |

The main message types of MQTT are:

- CONNECT / CONNACK
- PUBLISH / PUBACK
- SUBSCRIBE / SUBACK
- UNSUBSCRIBE / UNSUBACK
- PINGREQ / PINGRESP
- DISCONNECT

Among them, the PINGREQ/PINGRESP and DISCONNECT packets do not require variable headers and there is no Payload, which means that their packet size consumes only 2 bytes.

In the variable-length header of the CONNECT packet, there is a Protocol Version field. To save space, there is only one byte. So the version number is not stored as the string "3.1.1", but the number 4 is used to represent the 3.1.1 version.

### Three optional QoS levels

In order to adapt to different network environments of the equipment, MQTT has designed 3 QoS levels, 0, 1, 2:

- *At most once* (0)
- *At least once* (1)
- *Exactly once* (2)

QoS 0 is a "fire and forget" message sending mode: After a sender (possibly Publisher or Broker) sends a message, it no longer cares whether it is sent to the other party or sets up any resending mechanism.

QoS 1 includes a simple resending mechanism. After the Sender sends a message, it waits for the receiver's ACK. If it does not receive the ACK, it resends the message. This mode can guarantee that the message can arrive at least once, but it cannot guarantee that the message is repeated.

QoS 2 designed a [slightly complicated](https://docs.emqx.io/broker/v3/en/protocol.html#qos2-message-publish-and-subscribe) resending and repeating message discovery mechanism to ensure the message will arrive only once.

### Session Persistence

MQTT does not assume that the device or Broker uses the TCP keepalive mechanism[^4], but designed a keepalive mechanism at the protocol layer: the Keepalive field can be set in the CONNECT packet to set the sending time interval of keepalive heartbeat packet PINGREQ/PINGRESP. When the PINGREQ of the device cannot be received for a long time, the Broker will think that the device is offline.

In general, keepalive has two functions:

- Discover peer death or network outage
- Keep the connection from being disconnected by the network device in the case of no message interaction for a long time

For those devices that want to re-receive the messages that they missed during offline after re-online, MQTT has designed a persistent connection: In the CONNECT packet, you can set the CleanSession field to False, then Broker will store the following for the terminal:

- All subscriptions of the device
- QoS1 and QoS messages that have not been acknowledged by the device
- Messages missed when the device is offline

### Online state awareness

MQTT has designed Last [Will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) to let the broker help the device publish a will message to the specified topic if it finds that the device is offline abnormally.

In fact, in some implementations of [MQTT broker](https://www.emqx.com/en/products/emqx) (such as EMQX), when the device goes online or offline, Broker publishes device status updates through certain system topics, which is more in line with the actual application scenario.

## How to choose the open source MQTT broker

There are several popular MQTT Brokers so far:

1. [Eclipse Mosquitto](https://github.com/eclipse/mosquitto)

   MQTT broker implemented in C. The Eclipse organization also contains a number of MQTT client projects: https://www.eclipse.org/paho/#

2. [EMQX](https://github.com/emqx/emqx)

   MQTT broker developed in Erlang language that supports many other IoT protocols such as CoAP, LwM2M, etc.

3. [Mosca]( https://github.com/mcollina/mosca)

   MQTT broker developed with Node.JS that is easy to use.

4. [VerneMQ]( https://github.com/vernemq/vernemq)

   MQTT broker also developed using Erlang

Considering support for [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5), stability, scalability, cluster capabilities, etc., [EMQX's](https://www.emqx.com/en/products/emqx) performance should be the best:

- Developed with Erlang OTP, good fault tolerance (proven language in telecommunication field that once made 99.9999999% availability of switch equipment[^5])
- There are a lot of official plugins for extension. There are many authentication plugins, and the backend plugin is available. Supports various relational databases, NoSQL databases, and common [message queues](https://www.emqx.com/en/blog/mqtt5-feature-inflight-window-message-queue) such as Kafka, RabbitMQ, Pulsar, etc.
- Support cluster and horizontal expansion of nodes
- Supports 2000K concurrent connections with a single node
- Support rule engine and codec

## Quickly experience the MQTT protocol

### Public MQTT broker

EMQX [MQTT IoT cloud service](https://www.emqx.com/en/cloud) provides an online public MQTT 5.0 broker.  You can quickly start learning, testing MQTT protocol or prototyping.

For the detailed accessing information for this MQTT broker, please visit the EMQ website: [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

### MQTT online client

EMQ also provides the [MQTT online client tool](https://www.emqx.com/en/mqtt/mqtt-websocket-toolkit) that can be accessed through a browser. This tool supports connecting to the MQTT broker through the normal or encrypted WebSocket ports, and cache connections for the next accessing.



[^1]: The number of connected devices that are in use worldwide now exceeds 17 billion, with the number of IoT devices at 7 billion... https://iot-analytics.com/state-of-the-iot-update-q1-q2-2018-number-of-iot-devices-now-7b/
[^2]: The estimated installed base of smart meters (electricity, gas and water) is expected to surpass the 1 billion mark within the next 2 years. https://iot-analytics.com/smart-meter-market-2019-global-penetration-reached-14-percent/
[^3]: https://github.com/mqtt/mqtt.github.io/wiki/history
[^4]: https://www.cnblogs.com/softidea/p/5764051.html
[^5]: https://pragprog.com/articles/erlang


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
