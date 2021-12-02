### Overview

Shared subscription is a new feature introduced by MQTT 5.0 protocol, which is equivalent to the load balancing function of subscribers.

We know that the general message publishing process for non-shared subscriptions looks like this:

![WechatIMG316.png](https://static.emqx.net/images/47ff10326b8cd86daa0cedd5de5ee9f3.png)

Under this structure, if the subscription node fails, the publisher's messages will be lost (QoS 0) or accumulated in the server (QoS 1, 2). In general, the solution to this problem is to directly increase the number of subscribing nodes, but this generates a large number of duplicate messages, which will wastes performance. In in some business scenarios, subscription nodes also need to be de duplicated by themselves, further increasing the complexity of business.

Secondly, when the publisher's production capacity is strong, there may be situations in which subscribers' consumption power cannot keep up in time. At this time, it can only be solved by the subscriber's own load balancing, which again increases the development cost of users.

### Protocol specification

Now, in the MQTT 5.0 protocol, you can solve the problems mentioned above through the shared subscription feature. When you use a shared subscription, the flow of messages becomes:

![WechatIMG317.png](https://static.emqx.net/images/9aace6468a314ac10cd9badefb79f9d1.png)

Like non-shared subscriptions, shared subscriptions include a topic filter and subscription options. The only difference is that the topic filter format for shared subscriptions must be in the form `$ share / {ShareName} / {filter}`. The meanings of these fields are:

- `$ share` prefix indicates that this will be a shared subscription
- `{ShareName}` is a string without "/", "+" and "#". Subscription sessions share the same subscription by using the same `{ShareName}`, messages matching that subscription will only be published to one of the sessions at a time
  -`(filter)` is the topic filter in non-shared subscriptions

It should be noted that if the server is publishing a QoS 2 message to its selected subscriber and the network is interrupted before the publishing is complete, the server will continue to complete the publishing of the message when the subscriber reconnects. If the subscriber's session is terminated before it reconnects, the server will discard the message without attempting to publish it to other subscribers. If it is a QoS 1 message, the server can continue to complete the publishing after the subscriber reconnects, or it can immediately try to publish the message to other subscribers when the subscriber is disconnected. The MQTT protocol is not mandatory for that, and it depends on the specific implementation of the server. But if its session is terminated while waiting for the subscriber to reconnect, the server will try to publish the message to other subscribers.

### Sharing strategy

Although shared subscriptions allow subscribers to consume messages in a load-balanced manner, the MQTT protocol does not specify what load-balancing strategy the server should use. For reference, EMQ X provides four strategies  for users to choose: random, round_robin, sticky, and hash.

- random: randomly select one in all shared subscription sessions to publish messages 
- round_robin: select in turn according to subscription order
- sticky: use a random strategy to randomly select a subscription session, continue to use the session until the subscription is cancelled or disconnect and repeat the process
- hash: Hash the ClientID of the sender, and select a subscription session based on the hash result

### Effect demonstration

Finally, we use a comprehensive example to demonstrate the effect of shared subscriptions.

The server uses [emqx-v3.2.4](https://github.com/emqx/emqx/tree/v3.2.4) and the client uses [emqtt](https://github.com/emqx/emqtt), and emqx's shared subscription distribution strategy is the default random:

`broker.shared_subscription_strategy = random`

Use `./emqx start` to start emqx, then use emqtt to start three subscription clients, which respectively subscribe to $ share / a / topic`,` $ share / a / topic`, `$ share / b / topic`

![image20191111142037391.png](https://static.emqx.net/images/c3ebf7c105b985765208819e67af4c6d.png)

Start a publishing client to publish messages to the topic.

![image20191111144814890.png](https://static.emqx.net/images/d78a66888dfa5664dc44a819a5b195c6.png)

`$ share / a / topic` and` $ share / b / topic` belong to different session groups. The non-shared subscription  `topic` is load-balanced across all session groups. The client `sub3` receives all messages because there is only one session in the group, and the clients` sub1` and `sub2` receive messages randomly according to the random policy we configured.
