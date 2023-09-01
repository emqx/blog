> [EMQX](https://www.emqx.io/) *is a popular* [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) *widely used in the Internet of Things(IoT), Industrial IoT (*[IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)*) and Connected Cars. It can connect millions of devices at scale, move and process your IoT data in real-time anywhere with high performance, scalability and reliability.*
>
> In this blog series, we will explore common troubleshooting scenarios when using EMQX and provide practical tips and solutions to overcome them. Readers can optimize your MQTT deployment and ensure smooth communication between your devices following this troubleshooting instruction .

## Introduction

In EMQX, the low-coupling transmission of messages is also carried out in the publish-subscribe mode of the mqtt protocol, which provides a fast and reliable message exchange mechanism for clients and applications. When using EMQX for message publishing and subscribing, there could be issues like message loss, duplication, delay, retained message clearing, etc. In this blog, we will provide some analysis methods to troubleshoot these problems, ensuring the reliability and efficiency of message delivery. 

## Concepts Explained

Firstly, let's walk through several essential concepts involved in EMQX in this chapter:

- **Wildcards**: MQTT topic support the following wildcards: `+` and `#`. 

  - `+`: indicates a single level of wildcards, such as `a/+` matching `a/x` or `a/y`.

  - `#`: indicates multiple levels of wildcards, such as `a/#` matching `a/x`, `a/b/c/d`.

- **Inflight Window**: To improve message throughput efficiency and reduce the impact of network fluctuations, EMQX allows multiple unacknowledged QoS 1 and QoS 2 messages to exist on the network link simultaneously. These sent but unacknowledged messages are stored in the Inflight Window until confirmation is completed.

- **Message Queue**: When the number of messages simultaneously present in the network link exceeds the limit, that is, when the Inflight Window reaches the length limit, EMQX will no longer send subsequent messages but store these messages in the message queue. Once a message in the Inflight Window is confirmed, the messages in the message queue will be sent in a first-in, first-out order and stored in the Inflight Window simultaneously.

- **Shared Subscription**: In an ordinary subscription, all subscribers will receive all messages of the subscribed topic. Clients subscribing to the same topic in shared subscriptions will receive messages under this topic. The same message will not be sent to multiple subscribers, thus achieving load balancing among multiple nodes on the subscriber side.

- **Retained Message**: Retained messages reside on the message server and can still be received by later subscribers when subscribing to the topic.

## Problem Analysis

For each successful client connection, a fixed amount of memory is allocated to store client-related information, flying window, and message queue information. This section provides analysis and solutions for the following commonly occurring problems during publishing and subscription.

### How to solve subscribing  a Large Number of Topics

When the business platform uses the MQTT subscription method to consume a large number of device-side messages, it needs to subscribe to many topics for different devices, and it is uncertain whether all subscriptions are successful for each connection.

For subscriptions to a large number of topics, it is recommended to use wildcard subscriptions to simplify the subscription process, reduce complexity, and improve subscription efficiency. Wildcard subscription refers to subscribing to a group of topics that meet specific rules using wildcards, for example:

- Using the "+" wildcard to match a single-level topic, for example, "a/+/b" can match "a/1/b", "a/2/b", etc.

- Using the "#" wildcard to match a multi-level topic, for example, "a/#" can match "a/b/c", "a/d/e/f", etc.

The advantage of wildcard subscriptions is that a universal subscription rule can be used to subscribe to multiple topics, thereby avoiding the tedious process of subscribing to many topics one by one on the client side. In addition, wildcard subscriptions can also reduce communication volume between the client and the server, improve subscription efficiency, and reduce network bandwidth and server resource consumption.

### Reducing Message Loss

Many reasons can cause message loss. This section analyzes some of the reasons and offers practical solutions.

#### Subscription Failure

Check if the client has subscribed to the topic successfully:

- The subscription relationship may be lost if the client fails to handle the logic of resubscribing to topics after reconnection during the reconnection mechanism.

- After enabling ACL access control, if the client cannot subscribe to some topics, it will cause partial subscription failures. In this case, you need to check whether the ACL configuration is correct and ensure that the client has permission to access these topics.

**Improper Use of Shared Subscriptions**

The following are some possible reasons for message loss in shared subscriptions and their solutions:

- **Too many subscribers**: Shared subscriptions are designed to distribute topic messages among multiple subscribers. When a subscriber's processing capacity falls behind the rate of message generation, messages will accumulate. This affects subsequent transmission and processing of messages.

  **Solution**: While increasing the number of subscribers, ensure that their processing capability can keep up with the speed of message generation. This can be solved by adding more subscribers or optimizing the processing capability of subscribers.

- **Different QoS levels of subscribers**: In shared subscriptions, if different subscribers have different QoS levels, it may cause message loss problems. For example, when a publisher publishes a message with a QoS level of 2, if a subscriber's QoS level is 0, the subscriber will not be able to receive this message.

  **Solution**: When using shared subscriptions, ensure that all subscribers have the same QoS level to transmit messages to all subscribers correctly.

- **Message accumulation during subscriber offline**: In shared subscriptions, if a subscriber is offline for a period of time and other subscribers are online and consuming messages, it may cause message accumulation during the subscriber's offline period, resulting in message loss problems.

  **Solution**: This problem can be solved by setting a reasonable message retention policy. For example, when using the MQTT protocol, you can set the QoS level to 1 or 2, so that messages will be retained by the server during the subscriber's offline period and sent to the subscriber when they reconnect. Additionally, you can also reduce the problem of message accumulation by increasing the processing capability of subscribers.

- **Subscriber disconnection and reconnection issues**: In shared subscriptions, if a subscriber experiences a network failure while processing a message, disconnects, and then reconnects to the server, it may cause message loss problems.

  **Solution**: In the open-source version, you can use webhook to replace shared subscriptions, while in the enterprise version, you can use the bridging message middleware of the rule engine or a persistent database to solve the problem.

**Message Expired**

If the client uses the MQTT 5.0 protocol, check whether the client has set the message expiration time.

**High-Concurrency Consumption**
In high-concurrency scenarios, the client's consumption speed may not keep up with the production speed, which may cause messages to be squeezed into the server's queue and ultimately cause the client to fail to receive messages. If the topic subscribed by the client has a high concurrency of messages, consider the following solutions:

- **Increase the client's consumption capacity**: you can increase the client's consumption capacity by increasing the number of consumers or optimizing consumer code to improve the client's consumption speed.

  1. **Increase the message queue size**: you can increase the message queue size to alleviate message congestion. It should be noted that increasing the message queue size may increase the server's memory usage, so adjustments should be made according to the actual situation.

  2. **Reduce the size of a single message**: if a single message is large, you can consider fragmenting or compressing the message to reduce the size of a single message and improve the efficiency of message transmission.

  3. **Use QoS to ensure message transmission**: you can use QoS to ensure message transmission and ensure that messages are correctly transmitted to clients. If the QoS level is 1 or 2, EMQX will attempt to cache the message in the server's message queue until the client confirms receipt of the message.

### Checking for Duplicate Message Consumption

Duplicate message consumption can be caused by the reasons described below. For each reason, solutions are also provided.

- Duplicate subscription

  When using wildcard subscriptions, there may be subscription conflicts; multiple subscription rules match the same topic. To avoid subscription conflicts, it is recommended to consider the hierarchical structure of the topic when writing subscription rules to avoid unnecessary conflicts.

- Check the QoS quality of messages.

  QoS1: At least send once; there may be duplicate messages sent. For example, the consumer did not respond with a PUBACK message promptly.

- Check if the topic has retained messages, and repeated subscriptions will also consume messages repeatedly.

- Verify whether the client is repeatedly publishing messagesReproduce the messages published by the publisher through the log tracing function to verify if they are the same.

- Check if a group-shared subscription is used with different groups

- Different groups may be due to inconsistent topic settings for shared subscriptions or a combination of normal and shared subscriptions.

- Check if the client offline message function is used together with clean session=falseThe offline message function must not be used together with clean session=false; otherwise, the client may consume duplicate messages when logging in and subscribing again.

## Conclusion

EMQX provides a powerful way to implement MQTT message transmission. By understanding the solutions to these common issues, you can better use EMQX and ensure your application can function reliably.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
