## MQTT Publish-Subscribe Pattern

The Publish-subscribe pattern is a messaging pattern that decouples the clients that send messages (publishers) from the clients that receive messages (subscribers) by allowing them to communicate without having direct connections or knowledge of each other's existence.

The essence of MQTT's Publish-Subscribe pattern is that a middleman role called a Broker is responsible for routing and distributing all messages. Publishers send messages with topics to the Broker, and subscribers subscribe to topics from the Broker to receive messages of interest.

In MQTT, topics and subscriptions cannot be pre-registered or created. As a result, the broker cannot predict how many subscribers will be interested in a particular topic. When a publisher sends a message, the broker will only forward it to the subscribers that are currently subscribed to the topic. **If there are no current subscribers for the topic, the message will be discarded.**

The MQTT Publish-Subscribe pattern has four main components: Publisher, Subscriber, Broker, and Topic.

- **Publisher**

  The publisher is responsible for publishing messages to a topic. It can only send data to one topic at a time and does not need to be concerned about whether the subscribers are online when publishing a message.

- **Subscriber**

  The subscriber receives messages by subscribing to a topic and can subscribe to multiple topics at once. MQTT also supports load-balancing subscriptions among multiple subscribers through [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription).

- **Broker**

  The broker is responsible for receiving messages from publishers and forwarding them to the appropriate subscribers. In addition, the broker also handles requests from clients for connecting, disconnecting, subscribing, and unsubscribing.

- **Topic**

  MQTT routes messages based on topics. A topic is typically leveled and separated with a slash `/` between the levels, this is similar to URL paths. For example, a topic could be `sensor/1/temperature`. Multiple subscribers can subscribe for the same topic, and the broker will forward all messages on that topic to these subscribers. Multiple publishers can also send messages to the same topic, and the broker will route these messages in the order they are received to the subscribed clients.

  In MQTT, subscribers can subscribe to multiple topics simultaneously using topic wildcards. This allows them to receive messages on multiple topics with a single subscription.  Check out the blog [Understanding MQTT Topics & Wildcards by Case](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) for more details.

![MQTT Publish-subscribe Architecture](https://assets.emqx.com/images/b9575ac3d6916dc629c12aa2de5ce5c3.png)

<center>MQTT Publish-subscribe Architecture</center>

## Message Routing in MQTT Publish-Subscribe

In the MQTT publish-subscribe pattern, a client can function as a publisher, a subscriber, or both. When a client publishes a message, it sends it to the broker, which then routes the message to all subscribed clients on that topic. If a client subscribes to a topic, it will receive all the messages that the broker forwards for that topic.

There are generally two common approaches for filtering and routing messages in publish-subscribe systems.

- By topics

  Subscribers can subscribe with the broker for topics that are of interest to them. When a publisher sends a message, it includes the topic to which the message belongs. The broker uses this information to determine which subscribers should receive the message and routes it to the appropriate subscribers.

- By content-based filtering

  Subscribers can specify the conditions that a message must meet to be delivered to them. If the attributes or content of a message matches the conditions defined by the subscriber, the message will be delivered to that subscriber. If the message does not meet the subscriber's conditions, it will not be delivered.

In addition to routing messages based on topics, EMQX provides advanced message routing capabilities through its SQL-based Rule Engine starting with version 3.1. This feature allows for the routing of messages based on the content of the message. For more information about the Rule Engine and how it works, you can refer to the [EMQX documentation](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html).

## MQTT vs HTTP Request and Response

HTTP is a widely-used communication protocol on the World Wide Web due to its simplicity and ease of use. It does not require a specific client and can be used in a variety of industries, including the Internet of Things (IoT) field. In IoT, HTTP can be used to connect IoT devices and web servers, enabling remote monitoring and control of devices.

Although HTTP is simple to use and has a fast development cycle, it has some limitations when used in IoT applications. One disadvantage is that HTTP messages have more network overhead compared to MQTT at the protocol level. Additionally, HTTP is a stateless protocol, meaning that the server does not retain information about the client's state when processing requests and cannot recover from abnormal disconnections. Finally, the request-response model of HTTP requires polling to retrieve updates, while MQTT can provide real-time updates through subscriptions.

The MQTT publish-subscribe pattern has some inherent limitations due to its loosely coupled nature. For example, the publisher has no information about the state of the subscriber and therefore cannot know if the subscriber has received the message or processed it correctly. To address this issue, MQTT 5.0 introduces a [request-response](https://www.emqx.com/en/blog/mqtt5-request-response) feature that allows a subscriber to send a reply to the topic after receiving a message, and for the publisher to follow up after receiving the reply.

## MQTT vs Message Queues

While MQTT and message queues have many similarities, such as the publish-subscribe pattern, they are used for different purposes. Message queues are primarily used to store and transmit messages between server-side applications that typically handle a large amount of data but have a small number of clients. On the other hand, MQTT is a messaging protocol mainly used for communication between IoT devices, which often have a large number of devices that need to be accessed, managed, and communicated with.

In some practical situations, MQTT is often used together with message queues to allow the MQTT server to focus on connecting to devices and routing messages between them. For instance, the MQTT server receives data from IoT devices and then sends it to various business systems for processing via message queues.

Unlike message queues, MQTT topics do not need to be pre-created. We can publish messages to a new topic at any time. Of course, only when someone subscribes, these messages will be consumed instead of being directly discarded by Broker.

## Conclusion

The MQTT publish/subscribe mechanism can easily meet our communication needs of one-to-one, one-to-many, and many-to-one. Its flexibility makes it also well-suited for use in industries besides the IoT field, such as webcasts and mobile push notifications. 

So far, you should have a good understanding of the MQTT publish-subscribe pattern. Next, you can check [the blog](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) to learn how to create an MQTT connection.

You can also visit the [MQTT Getting Started and Advanced](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT topics and related concepts such as wildcards, retained messages, and [will messages](https://www.emqx.com/en/blog/use-of-mqtt-will-message), and to explore more advanced applications of MQTT. These resources will help you get started with MQTT applications and services development.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
