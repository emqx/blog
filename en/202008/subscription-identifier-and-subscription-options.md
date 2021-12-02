MQTT v5 brings many new features, we will show these features in an easy-to-understand way and discuss the impact of these features on the developer. So far, we have discussed these [new features of MQTT v5](https://www.emqx.com/en/mqtt/mqtt5). Today, we will continue discussing: **subscription identifier** and **subscription options**.



## Subscription identifier

The client can specify a subscription identifier when subscribing. The broker will establish and store the mapping relationship between this subscription and subscription identifier when successfully create or modify subscription. The broker will return the subscription identifier associated with this PUBLISH packet and the PUBLISH packet to the client when need to forward PUBLISH packets matching this subscription to this client.

Therefore, the client can establish the mapping between the subscription identifier and message processing program for directly orientating messages to the corresponding message processing program through the subscription identifier when receiving a PUBLISH packet. It is much faster than finding the message processing program through topic matching.

![image20200723152010505.png](https://static.emqx.net/images/14752d1986cadf5bd7b6c96a3f4229f7.png)

Because the SUBSCRIBE packet supports containing many subscriptions, multiple subscriptions may associate with one subscription identifier. Even if subscribing separately, this situation may happen. Users need to realize the result might cause when using it in this way, although this situation is allowed to happen. According to the actual subscription situation of the client, the PUBLISH packet that the client finally received may contain multiple subscription identifiers, and these subscription identifiers may be completely different or the same. The following are several common situations:

1. The client subscribes to the topic `a` and specifies the subscription identifier as 1, subscribes to the topic `b` and specifies the subscription identifier as 2. Because of using different subscription identifiers, the messages of the topic `a` and `b` will be directed to different message processing programs.
2. The client subscribes to the topic `a` and specifies the subscription identifier as 1, subscribes to the topic `b` and specifies the subscription identifier as 1. Because of using the same subscription identifier, the messages of the topic `a` and `b` will be directed to the same message processing program.
3. The client subscribes to the topic `a/+` and specifies the subscription identifier as 1, subscribes to the topic `a/b` and specifies the subscription identifier as 1. The PUBLISH packet of topic `a/b` will carry two identical subscription identifiers, the corresponding message processing program will be triggered twice.
4. The client subscribes to the topic `a/+` and specifies the subscription identifier as 1, subscribes to the topic `a/b` and specifies the subscription identifier as 2. The PUBLISH packet of topic `a/b` will carry two different subscription identifiers, a message will trigger two different message processing program.

![image20200723152040226.png](https://static.emqx.net/images/fd6fb5f61d116aa66d837711e337a30f.png)

The situation that PUBLISH packet carries multiple subscription identifiers is ok when the message rate is low, but it may cause some performance issues when the message rate is high. Therefore, we suggested that you try to ensure that this happens intentionally.



## Subscription options

In the MQTT v5, you can use more subscription options to change the server behavior.

![image20200723161859058.png](https://static.emqx.net/images/0a255be6657118484a6ca663c9755c6b.png)

### QoS

Please refer to [MQTT Quality of Service](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

### No Local

In the MQTT v3.1.1, if you subscribe to the topic published by yourself, you will receive all messages that you published.

However, in the MQTT v5, if you set this option as 1 when subscribing, the server will not forward the message you published to you.


### Retain As Publish

This option is used to specify whether the server retains the RETAIN mark when forwarding messages to the client, and this option does not affect the RETAIN mark in the retained message. Therefore, when the option Retain As Publish is set to 0, the client will directly distinguish whether this is a normal forwarded message or a retained message according to the RETAIN mark in the message, instead of judging whether this message is the first received after subscribing(the forwarded message may be sent before the retained message, which depends on the specific implementation of different brokers).


### Retain Handling

This option is used to specify whether the server forwards the retained message to the client when establishing a subscription.

- **Retain Handling is equal to 0**, as long as the client successfully subscribes, the server will send the retained message. 
- **Retain Handling is equal to 1**, if the client successfully subscribes and this subscription does not exist previously, the server sends the retained message. After all, sometimes the client re-initiate the subscription just to change the QoS, but it does not mean that it wants to receive the reserved messages again. 
- **Retain Handling is equal to 2**, even if the client successfully subscribes, the server does not send the retained message.
