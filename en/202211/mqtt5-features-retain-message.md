## What is Retained Messages?

If you know MQTT even for just a little bit, you may already know that for each MQTT message, there is a topic name, and there is the payload. If you dig a little deeper, you’ll find that there are also message properties and flags. One of the flags is called `Retain`, which is what this post is about.

Upon receiving a message with the `Retain` flag set, the MQTT broker must store the message for the topic to which the message was published, and it must store only the latest message. So the subscribers which are interested in this topic can go offline, and reconnect at any time to receive the latest message instead of having to wait for the next message from the publisher after the subscription.

As illustrated below, when a client subscribes to a topic, if there is a retained message for this topic, the message is sent to the client immediately.

![MQTT Retained Messages](https://assets.emqx.com/images/f0d556a72ee7d9f1fe609659aa7ed2a9.png)


## When to use MQTT Retained Messages?

While allowing publishers to decouple subscribers, the publish-subscribe pattern also has the disadvantage that subscribers cannot actively fetch messages from publishers. When a subscriber receives a message depends on when the publisher publishes it, which is inconvenient in some scenarios.

New subscribers can get the latest data immediately without waiting for unpredictable times with retained messages. Below are some examples:

- Smart home devices only send state data when the state changes, but the control APP needs to know the device's current state whenever the user opens the APP.
- The interval between sensors reporting data can be very long, but subscribers may need to get the latest data immediately after subscribing.
- Properties such as sensor version and serial number that do not change frequently can be published as a retained message for later subscribers to get the information.


## How to use MQTT Retained Messages?

For MQTT client SDKs, there are typically APIs or parameters to set the `Retain` flag. For example the [paho MQTT Java client library](https://github.com/eclipse/paho.mqtt.java/blob/6f35dcb785597a6fd49091efe2dba47513939420/org.eclipse.paho.mqttv5.client/src/main/java/org/eclipse/paho/mqttv5/common/MqttMessage.java#L88), and the the Erlang MQTT client [emqtt](https://github.com/emqx/emqtt/blob/d5c630bf5c6e0d530be95e7255a089fefa0fe385/src/emqtt.erl#L428-L433).

For MQTT client applications, either with a command line or graphic interface, you should be able to find where to set the `Retain` flag.

In this post, we are not going to dig into the programming SDKs.
We will try to demonstrate MQTT retained messages using the [open-source cross-platform MQTT 5.0 desktop client - MQTT X](https://mqttx.app/).

If you start the MQTT X application for the first time, you will see the main window below. Click the `New Connection` button to create an MQTT connection.

![Create an MQTT connection](https://assets.emqx.com/images/c3c89247952538c127839de49a398aec.png)

We only need to fill in a connection `Name` and leave the other parameters as default. The `Host` will default to the [public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by [EMQX Cloud](https://www.emqx.com/en/cloud). Finally, click the `Connect` button in the upper right corner to create an MQTT connection.

![Create an MQTT connection](https://assets.emqx.com/images/199e08891e0a7ca0ad78efa8f986dc21.png)

After the successful connection, publish a message to the topic `sensor/t1` in the message input box.

![Publish MQTT message](https://assets.emqx.com/images/d66d61a3e507c9371f6665ac1f6be289.png)

Next, we check the Retain flag and publish two retained messages to the topic `sensor/t2`.

![Publish MQTT Retained messages](https://assets.emqx.com/images/2c202c92516bb9d1394b65410b236dde.png)

Then click the `New Subscription` button to create a subscription.

![Create MQTT Subscription](https://assets.emqx.com/images/2e834540fa748f318f7a1f770070db64.png)

We subscribe to the wildcard topic `sensor/+,` which will match the topics `sensor/t1` and `sensor/t2`.

> Check out the blog [Understanding MQTT Topics & Wildcards by Case](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) for more details.

![Subscribe to MQTT Wildcard Topic](https://assets.emqx.com/images/d7da8ae6e8cad9dffa82dee3b3014cc1.png)

Finally, we will see that the subscription successfully receives the second retained message, neither the normal message for `sensor/t1` nor the first retained message for `sensor/t2`. This shows that the MQTT Broker will only store the latest retained message for each topic.

![Receive MQTT Retained Messages](https://assets.emqx.com/images/a1a9d7e1ca32f77a8e54f09dccccee99.png)


## Q & A about MQTT Retained Messages

### How do I know a message is a retained message?

When a message is originated from the `Retain` storage in the broker, the `Retain` flag is set, so the subscriber knows that this is not a new message after its subscription.

That is, if a retained message is published after the subscription, the subscriber will receive it as a regular message (without the `Retain` flag). **After a retained message is delivered, if the subscriber wishes to receive the retained message again, it needs to resubscribe.**

In the example below, we subscribe to the topic `sensor/t2` and then publish a retained message to the topic, the subscriber receives the message immediately, but without the ‘retain’ flag. Then we delete the subscription and re-subscribe to `sensor/t2` to receive the message again with the ‘retain’ flag set.

![MQTT Retained Messages](https://assets.emqx.com/images/06d1e7ec9edfebccf2425c39a73b1e6e.png)

### How long are retained messages stored? How to delete it?

The broker will only store the latest retained message for each topic, and the validity of the retained message is related to the broker's settings. If the broker is set to store retained messages in memory, they are lost when the MQTT Broker is restarted; if they are stored on disk, they remain after the broker is restarted.

Retained messages are not part of session states, meaning retained messages are not deleted when the publishing session terminates. There are several ways to delete retained messages.

- When a client publishes a retained message with an empty payload to a topic, the broker deletes the retained message under that topic.
- Delete on the MQTT Broker, e.g., the EMQX MQTT Broker provides the ability to delete retained messages from management API or from the Dashboard.
- MQTT 5.0 protocol added Message Expiry Interval property, which can be used to set the expiration time of the message when publishing. The message will be automatically deleted after the expiration time, regardless of whether it is a retained message.

## MQTT Retained Messages in EMQX

[EMQX](https://www.emqx.io/) is the most popular MQTT Broker, with over 10 million downloads worldwide. Recently, [EMQX released version 5.0](https://www.emqx.com/en/blog/emqx-v-5-0-released), which achieved [100 million MQTT connections + 1 million message throughput](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connections) per second through a 23-node cluster, making EMQX 5.0 the most scalable MQTT Broker worldwide so far.

EMQX 5.0 supports viewing and setting retained messages in the built-in Dashboard. You may use the following command to install EMQX 5.0 open-source version for trial.

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

After successful installation, use your browser to visit `http://127.0.0.1:18083/` to experience the new EMQX 5.0 Dashboard.

> The default Username is admin, and the Password is public.

After successful login, you can click the `Configuration->MQTT` menu to view the list of retained messages. You can also view the Payload of retained messages or delete a retained message.

![MQTT Retained Messages in EMQX](https://assets.emqx.com/images/125fb714b5ab0eae6689fe305795d0e2.png)

Click on the `Settings` menu under `Retainer`, and you will see that EMQX supports setting the Storage (memory or disk), the Max Retained Messages, the Expire, and other parameters in the Dashboard.

![MQTT Retained Messages Setting](https://assets.emqx.com/images/6b916b14536358e43a58eaac02a816cd.png)
 

## Summary

This article introduces and demonstrates the use of MQTT Retained Messages. Referring to this article, readers can use MQTT Retained Messages to get data immediately after subscription.

In addition, the MQTT protocol has many more valuable features. Check out EMQ's [MQTT Getting Started and Advanced](https://www.emqx.com/en/mqtt) series of articles for a deeper understanding, to explore more advanced applications of MQTT, and to start developing MQTT applications and services.
