In [Introduction to MQTT Publish-subscribe Pattern](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), we learned that we need to initiate a subscription with the server to receive corresponding messages from it. The topic filter specified when subscribing determines which topics the server will forward to us, and the subscription options allow us to customize the forwarding behavior of the server further.

In this article, we will focus on exploring the available subscription options in [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) and their usage.

>New to MQTT protocol? Please check out our
>
>[What Is the MQTT Protocol: A Beginner's Guide](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)

## Subscription Options

A subscription in MQTT consists of a topic filter and corresponding subscription options. So, we can set different subscription options for each subscription.

MQTT 5.0 introduces four subscription options: QoS, No Local, Retain As Published, and Retain Handling. On the other hand, MQTT 3.1.1 only provides the QoS subscription option. However, the default behavior of these new subscription options in MQTT 5.0 remains consistent with MQTT 3.1.1. This makes it user-friendly if you plan to upgrade from MQTT 3.1.1 to MQTT 5.0.

Now, let's explore the functions of these subscription options together.

### QoS

QoS is the most commonly used subscription option, which represents the maximum QoS level that the server can use when sending messages to the subscriber.

A client may specify a QoS level below 2 during subscription if its implementation does not support QoS 1 or 2.

Additionally, if the server's maximum supported QoS level is lower than the QoS level requested by the client during the subscription, it becomes apparent that the server cannot meet the client's requirements. In such cases, the server informs the subscriber of the granted maximum QoS level through the subscription response packet (SUBACK). The subscriber can then assess whether to accept the granted QoS level and continue communication.

![image.png](https://assets.emqx.com/images/fa5915cb9df598965881cc08585c1fe7.png)

A simple calculation formula:

```
The maximum QoS granted by the server = min ( The maximum QoS supported by the server, The maximum QoS requested by the client )
```

However, the maximum QoS level requested during subscription does not restrict the QoS level used by the publishing end when sending messages. When the requested maximum QoS level during subscription is lower than the QoS level used for message publishing, the server will not ignore these messages. To maximize message delivery, it will downgrade the QoS level of these messages before forwarding.

![image.png](https://assets.emqx.com/images/b0f2a8b2c655ec59cf5c6338eb1217cc.png)

Similarly, we have a simple calculation formula:

```
QoS in the forwarded message = min ( The original QoS of the message, The maximum QoS granted by the server )
```

### No Local

The No Local option has only two possible values, 0 and 1. A value of 1 indicates that the server must not forward the message to the client that published it, while 0 means the opposite.

This option is commonly used in bridging scenarios. Bridging is essentially two MQTT Servers establishing an [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection), then they subscribe to some topics from each other. The server forwards client messages to another server, which can continue forwarding them to its clients.

![image.png](https://assets.emqx.com/images/84ceaaf5c2e513e6d775d6d3929e672b.png)

Let's consider the most straightforward example where we assume two MQTT servers, Server A and Server B.

They have subscribed to the topic `#` from each other. Now, Server A forwards some messages from the client to Server B, and when Server B looks for a matching subscription, Server A is there too. If Server B forwards the messages to Server A, then Server A will forward them to Server B again after receiving them, thus falling into an endless forwarding storm.

However, if both Server A and Server B set the No Local option to 1 while subscribing to the topic `#`, this problem can be ideally avoided.

### Retain As Published

The Retain As Published option also has two possible values, 0 and 1. Setting it to 1 means the server should preserve the Retain flag unchanged when forwarding application messages to subscribers, and setting it to 0 means that the Retain flag must be cleared.

Like the No Local option, Retain As Published primarily applies in bridge scenarios. 

We know that when the server receives a retained message, in addition to storing it, it will also forward it to existing subscribers like a normal message, and the Retain flag of the message will be cleared when forwarding.

This presents a challenge in bridge scenarios. Continuing with the previous setup, when Server A forwards a retained message to Server B, the Retain flag is cleared, causing Server B not to recognize it as a retained message and not store it. This makes retained messages unusable across bridges.

In MQTT 5.0, we can let the bridged server set the “Retain” publish option to 1 when subscribing to solve this problem.

![image.png](https://assets.emqx.com/images/ef5ed6d09cc7f52e5e4ea7ae123218e2.png)

### Retain Handling

The Retain Handling subscription option indicates to the server whether to send retained messages when a subscription is established.

When a subscription is established, the retained messages matching the subscription in the server will be delivered by default.

However, there are cases where a client may not want to receive retained messages. For example, if a client reuses a session during connection but cannot confirm whether the previous connection successfully created the subscription, it may attempt to subscribe again. If the subscription already exists, the retained messages may have been consumed, or the server may have cached some messages that arrived during the client's offline period. In such cases, the client may not want to receive the retained messages the server publishes.

Additionally, the client may not want to receive the retained message at any time, even during the initial subscription. For example, we send the state of the switch as a retained message, but for a particular subscriber, the switch event will trigger some operations, so it is helpful not to send the retained message in this case.

We can choose among these three different behaviors using Retain Handling:

- Setting Retain Handling to 0 means that retained messages are sent whenever a subscription is established.
- Setting Retain Handling to 1 means retained messages are sent only when establishing a new subscription, not a repeated one.
- Setting Retain Handling to 2 means no retained messages are sent when a subscription is established.

## Demo

### Demo of the QoS Subscription Option

1. Access [MQTTX Web](http://mqtt-client.emqx.com/) on a Web browser.

2. Create an MQTT connection using WebSocket and connect to the [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker):

   ![MQTTX](https://assets.emqx.com/images/1eff007c799cd5e9ed9d65c3a2b1d826.png)

3. After a successful connection, we subscribe to the topic `mqttx_4299c767/demo` with a QoS of 0. Since the public server may be used by many people simultaneously, to avoid topic conflicts with others, we can use the Client ID as a prefix for the topic:

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/7d6598089ff051feadae673734b5be68.png)

4. After a successful subscription, we publish a QoS 1 message to the topic `mqttx_4299c767/demo`. At this point, we will observe that while we have sent a QoS 1 message, we receive a QoS 0 message. This indicates that QoS degradation has occurred:

   ![Publish a QoS 1 message](https://assets.emqx.com/images/4b1a7d69d8344ba6efc2c7fe22370b17.png)

### Demo of the No Local Subscription Option

1. Access [MQTTX Web](http://mqtt-client.emqx.com/) on a Web browser.

2. Create an MQTT connection using WebSocket and connect to the [Free Public MQTT Server](http://broker.emqx.io/).

3. After a successful connection, we subscribe to the topic `mqttx_4299c767/demo` and set the No Local option to true:

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/9255fa97ed59e71be6b7fac0e7d2fed4.png)

4. After a successful subscription, similar to the QoS demonstration mentioned earlier, we still let the subscriber publish the message. However, this time we will notice that the subscriber is unable to receive the message:

   ![Publish MQTT Message](https://assets.emqx.com/images/933d4e0147c2b1720124d8d3e36c55a1.png)

### Demo of the Retain As Published Subscription Option

1. Access [MQTTX Web](http://mqtt-client.emqx.com/) on a Web browser.

2. Create an MQTT connection using WebSocket and connect to the [Free Public MQTT Server](http://broker.emqx.io/).

3. After a successful connection, we subscribe to the topic `mqttx_4299c767/rap0` with Retain As Published set to false. Then, we subscribe to the topic `mqttx_4299c767/rap1` with Retain As Published set to true:

   ![Subscribe to the topic "mqttx_4299c767/rap0"](https://assets.emqx.com/images/3d9cb0512df37e95a1be40ec82384f93.png)

   ![Subscribe to the topic "mqttx_4299c767/rap1"](https://assets.emqx.com/images/627c5a3984d401f7e3cb01a160e593a0.png)

4. After the successful subscription, we publish a retained message to the topics `mqttx_4299c767/rap0` and `mqttx_4299c767/rap1,` respectively. We will see that the Retain flag in the message received by the former is cleared, and the Retain flag in the message received by the latter is retained:

   ![Receive messages](https://assets.emqx.com/images/8e23176543eb78b1f5ee77f6ba98add1.png)

### Demo of the Retain Handling Subscription Option

1. Access [MQTTX Web](http://mqtt-client.emqx.com/) on a Web browser.

2. Create an MQTT connection using WebSocket and connect to the [Free Public MQTT Server](http://broker.emqx.io/).

3. After the successful connection, we publish a retained message to the topic `mqttx_4299c767/rh`. Then, we subscribe to the topic `mqttx_4299c767/rh` and set the Retain Handling option to 0:

   ![Publish a retained message to the topic "mqttx_4299c767/rh"](https://assets.emqx.com/images/9b0a0bfa76836e9e4bfc30d6576b25f6.png)

4. After the successful subscription, we will receive the retained message sent by the server:

   ![Receive the retained message](https://assets.emqx.com/images/1630db5d1e44c7eec81fcd37e7ca0969.png)

5. Unsubscribe and resubscribe with Retain Handling set to 2. After the subscription is successful this time, we will not receive the retained message sent by the server:

   ![Retain Handling set to 2](https://assets.emqx.com/images/2032a4e178b18b0bcfd2866b9f377f75.png)

In MQTTX, we cannot demonstrate the effect of Retain Handling set to 1. You can get a Python sample code for subscription options [here](https://github.com/emqx/MQTT-Feature-Examples).


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
