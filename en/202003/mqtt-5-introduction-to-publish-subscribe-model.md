

The core of the [MQTT protocol](https://www.emqx.com/en/mqtt) is the publish-subscribe model. In this article, we will introduce this mode in detail.

## Publish-subscribe model

The **publish-subscribe** model is different from the traditional client-server model. It separates the client (publisher) that sends the message from the client (subscriber) that receives the message. The publisher and the subscriber do not need to establish direct contact. We can either let multiple publishers publish messages to one subscriber, or let multiple subscribers receive messages from one publisher at the same time. The essence of it is that an intermediate role called a broker is responsible for all message routing and distribution. The traditional client-server model can achieve similar results, but it cannot be as simple and elegant as the publish-subscribe model.

![User Guide_1备份.jpg](https://static.emqx.net/images/e2954fd3e5922161e347fa5189faac3c.jpg)

The advantage of the publish-subscribe model is the decoupling of publishers and subscribers. This decoupling is manifested in the following two aspects:

- Spatial decoupling. Subscribers and publishers do not need to establish a direct connection, and new subscribers do not need to modify the publisher's behavior when they want to join the network.
- Time decoupling. Subscribers and publishers do not need to be online at the same time. Even if there are no subscribers, it does not affect publishers to publish messages

## Message routing

As the key role of the publish-subscribe model, the broker needs to accurately and efficiently forward the desired messages to the subscribers. Generally speaking, there are two methods:

- Based on the topic. Subscribers subscribe to topics they are interested in from the **MQTT broker**. All messages published by the publisher will include their topics. The broker determines which subscribers need to be forwarded to the message according to the topic of the message.
- Based on message content. The subscriber defines the conditions of the message that they are interested in. Only when the attributes or content of the message meet the conditions defined by the subscriber, the message will be published to the subscriber. Strictly speaking, the topic can also be regarded as a kind of message content.

The loosely-coupled nature of the publish-subscribe model also has some side effects. Since the publisher is not aware of the subscriber's status, the publisher cannot know whether the subscriber has received the message or whether the message has been processed correctly. In such cases, securing delivery often requires a more interactive flow of messages. For example, a subscriber sends a response to a topic after receiving a message, and the publisher is now a subscriber waiting for a response.

## MQTT protocol

The **MQTT protocol** distributes messages based on topics rather than message content. Each message contains a topic, and the broker does not need to parse user data. This provides the possibility to implement a general, business-independent **MQTT broker**. Users can also encrypt their data at will, which is very useful for WAN communication.

**MQTT topics** can have multiple levels, and allow fuzzy matching of one or more levels, enabling clients to subscribe to multiple topics at once. We will introduce the detailed features of the MQTT topic in the following articles.

Compared with message queuing, MQTT does not require the topic to be created explicitly before publishing or subscribing. The only possible adverse effect is that the client may use the wrong topic without knowing it, but the benefit of flexible deployment is higher than that.

Since we have mentioned message queues, it is time to explain the difference between MQTT and message queues. MQTT is not a message queue, although many behaviors and characteristics of the two are very close, such as using a publish-subscribe model. The scenarios they face are significantly different. Message queues are mainly used for message storage and forwarding between server-side applications. In this kind of scenario, the data volume is often large but the access volume is small. MQTT is targeted at the IoT field and the mobile Internet field. The focus of such scenarios is massive device access, management and messaging. In practical scenarios, the two are often used in combination. For example,[MQTT Broker](https://www.emqx.com/en/products/emqx) first receives data uploaded by IoT devices, and then forwards these data to specific applications for processing through message queues.

![User Guide_1备份 2.jpg](https://static.emqx.net/images/876881a17dd8f0b6b82104f301e9a6d1.jpg)

Hopefully, with this short article, you will have an intuitive understanding of the publish-subscribe model. Other features of MQTT will be covered in subsequent articles.