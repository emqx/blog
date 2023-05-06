The full name of [MQTT](https://www.emqx.com/en/mqtt) is Message Queuing Telemetry Transport, which is a **lightweight IoT messaging protocol** based on the **publish/subscribe**. [Andy Stanford-Clark](https://en.wikipedia.org/wiki/Andy_Stanford-Clark) ([IBM](https://en.wikipedia.org/wiki/IBM)) and Arlen Nipper (Cirrus Link, then Eurotech) authored the first version of the protocol in 1999.[^1]. After that, the features that easy to implement, support QoS, lightweight and bandwidth saving let the MQTT becoming the standard of IoT communication.



## The basic features of MQTT protocol

- Open message protocol that is easy to implement.

- [Publish-subscribe](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) mode，one-to-many message publishing.

- Based on TCP/IP network connection.

- Message QoS support with a reliable transmission guarantee.

- Very little transmission consumption and protocol data exchange, which can maximum reducing the network flow.

- Provide the mechanism which will notify the related parties when an abnormal disconnection occurs.

  

## Application

[MQTT protocol](https://www.emqx.com/en/mqtt) is widely used in the Internet of Things, Mobile Internet, Intelligent Hardware, Internet of Vehicles, Power Energy and so on.

- M2M Communication and Big Data Acquisition in the Internet of Things.

- Android message push and WEB message push. (Learn more: [How to use MQTT on Android](https://www.emqx.com/en/blog/android-connects-mqtt-using-kotlin).)

- Mobile instant messaging, such as Facebook Messenger.

- Intelligent hardware, smart furniture and appliances.

- Vehicle networking communication, pile collection of electric vehicles.

- Smart City, Telemedicine, Distance Education.

- Electricity, Oil and Energy industry.



## The principle of MQTT protocol

There are three roles in the MQTT protocol which are based on the publish/subscribe model: Publisher, Broker and Subscriber. The publisher publishes messages to the proxy, and the proxy forwards these messages to the subscriber. Usually, the roles of the client are publisher and subscriber and the role of the broker is proxy, while the broker may actively publish or subscribe to topics.

For easy to understand, messages delivered by MQTT can be simplified as two parts, Topic and Payload:

- Topic, the topic of messages. After the subscriber subscribes to the topic, once the proxy received the message of corresponding topics, it will forward this message to the subscriber.
- Payload, message payload, which is the section that the subscriber cares about, usually related to business.



## The basic concept of MQTT protocol

### Client

The program or device that use the MQTT protocol, it can:

- Open the network connection which connects to the server
- Publish the application message to other related clients
- Subscribe for requesting to accept the related application message
- Unsubscribe for removing the request that accepts application message
- Close the network connection which connects to the server

### Server

The program or device that acts as an intermediary, between the client that send messages and the client that has subscribed, it can

- Receive the network connection which is from the client
- Receive the application message published by the client
- Process the request that subscribes and unsubscribe from the client
- Forward the application message to the subscribed client which satisfied conditions
- Close the network connection which is from the client

### Session

After each client establishes a connection with the server, it is a session.  There is a status interaction between the client and the server. The session can exist in a network connection, and can also exist across multiple consecutive network connections.

### Subscription

The subscription includes a Topic Filter and the highest degree of QoS. Subscription associate with a single Session. The session can contain multiple subscriptions. Each subscription of the session has a different topic filter.

### Topic Name

A tag attached to the application message, which is used for matching the existing subscription in the server. The server will send this application message to all client that has matched to the subscription.

### Topic Filter

The topic expression only used in subscribing, which can contain wildcard for matching multiple the name of topics. 

For more features of the MQTT topic, please access our blog: [Advanced features of MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).

### Payload

For the PUBLISH packet, the payload is the information of business, which can be the data with any format(binary, hexadecimal, ordinary string, JSON string and Base64).



## The structure of MQTT packet

The MQTT packet consists of three parts which are fixed header, variable header and payload respectively. The fixed header which contains the type of packet and other fields exists in all MQTT packet. The content of the variable header is different because of the different types of the packet, and the variable header does not even exist in some packet. Usually, the payload is the data related to the business/scenario, for example, for the SUBSCRIBE packet, the payload is the subscription list.



## The advanced MQTT protocol

### Quality of service(QoS) of message

MQTT provides three kinds of quality of service of information which guarantee the messaging reliability in different network environments.

- QoS 0: the message is delivered at most once, if the client is not available currently, will lose this message.
- QoS 1: the message is delivered at least once.
- QoS 2: the message is delivered only once.

For more introduction of QoS, please access our blog: [Introduction to MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

### Clean Session

When the MQTT client initiates a CONNECT request to the server, you can set whether to create a new session through the sign `Clean Session`.

- When `Clean Session` is set as 0 
  - If there is a session that associates with this customer identifier, the server has to recover the communication with the client based on the status of this session.
  - If there is not any session that associates with this customer identifier, the server has to create a new session.
- `Clean Session` is set as 1. The client and server have to discard any existed session and begin a new session.

### Keep Alive

When the MQTT client initiates a CONNECT request to the server, you can set the keep alive period through Keep Alive parameter.

When there is no packet that needs to send, the client sends a 2-byte PINGREQ heartbeat packet regularly according to the Keep Alive period. The server will reply 2-byte PINGRESP packet after receiving the PINGREQ packet.

The server will disconnect the client when it neither receives the packet that the client publishes subscription nor the PINGREQ heartbeat packet within 1.5 heartbeat period.

### Retained Message

When the MQTT client publishes messages to the server, you can set the retained message sign. The retained message will reside in the message server, so the subsequent subscribers can receive the latest retained message when subscribing to the topic.

### Will Message

When the MQTT client sends a CONNECT request to the server, can carry [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message). When the MQTT client goes offline abnormally(the client does not send the DISCONNECT message to the server before disconnecting), the MQTT message server will publish will message.

For more MQTT will message, please access our blog: [Use of MQTT Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message).



## New features of MQTT 5.0 protocol

### Session Expiry

[MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) will divide the Clean Session indicator into the Clean Start indicator (represents that the session should start without using an existed session) and session expired interval attribute(represents the time how long the session will retain after disconnecting ).

### Provide the reason code for all response packet

Modify all response packet for containing the reason code, including CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK, DISCONNECT and AUTH, which for the caller to ensure whether the requested function is successful.

### Request/response

Set the MQTT request/response model and provide the response topic and comparison data attributes for routing the response messages back to the publisher of this request. Besides that, it adds the ability that obtains the configuration information related to building the response topic from the server for the client.

For more MQTT Request/response, please access our blog: [MQTT 5.0 Request Response](https://www.emqx.com/en/blog/mqtt5-request-response).

### Shared subscription

Add the support for the [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), which allows multiple subscribers to load balance.

### Topic alias

Support abbreviating the topic name to integers to reduce the overhead of the MQTT packet. The client and server can specify the number of topic alias that they allowed.

## The next step

After reading this article, if you want to try MQTT, you can access the [Free Public MQTT 5 Broker Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) page on the EMQ website. This page provides an online MQTT 5.0 broker, you can use it for MQTT learning, test and prototype design.

Readers can also access our blog [The comparison of usual MQTT client tools in 2020](https://www.emqx.com/en/blog/mqtt-client-tools) to choose a suitable MQTT client tool for quickly experience the MQTT protocol.



[^1]: [https://en.wikipedia.org/wiki/MQTT#History](https://en.wikipedia.org/wiki/MQTT#History)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
