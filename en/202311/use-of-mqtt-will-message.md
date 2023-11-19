Will Message is an important feature in [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), which solves the problem that only the server can know whether clients are offline. It allows us to gracefully take follow-up actions for unexpectedly offline clients.

This article will dive into the MQTT Will Message, including what it is and how it works. Considering that some of the content in this article will involve the concepts of sessions and retained messages, you can read the following two blogs if needed:

1. [Introduction to Clean Start and Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)
2. [The Beginner's Guide to MQTT Retained Messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message)

## What is MQTT Will Message?

In the real world, a person can draw up a will, stating how his assets should be distributed and what actions should be taken after death. When he passes away, the executor of the will makes the will public and carries out the instructions in the will.

In MQTT, the client can register a Will Message on the server when connecting. Similar to normal messages, we can set the Topic, Payload, and other fields of the Will Message. When the client unexpectedly disconnects, the server sends this Will Message to other clients who have subscribed to the corresponding topic. Therefore, these recipients can take actions promptly, such as sending users notifications or switching to backup devices.

Suppose we have a sensor monitoring a value that rarely changes. The typical implementation is regularly publishing the latest value, but a better implementation is sending it only when the value changes in the form of a retained message. This allows any new subscriber to get the current value immediately, without waiting for the sensor to publish again.

However, this also means subscribers cannot judge whether the sensor is offline based on whether they receive messages on time. With the Will Message, we can immediately know when the sensor keeps alive timeout, without always having to get the value published by the sensor.

### Will Message or Last Will and Testament (LWT)?

In some blogs or codes, we might see the name "Last Will and Testament", or its abbreviation: LWT. It refers to the Will Message in MQTT. The reason why these two names coexist might be because the concept of "Last Will and Testament" was mentioned in the summary of the MQTT 3.1 protocol specification.

Although MQTT always clearly used the name "Will Message" in the main body of the protocol, these two names are often used interchangeably among users.

We are not intending to correct either usage. We just hope that different names won't confuse you.

## How MQTT Will Message Works?

### The Client Specifies the Will Message When Connecting

The Will Message is specified when the client initiates a connection, and it is included in the CONNECT packet sent by the client along with fields such as Client ID and Clean Start.

Like normal messages, we can set the Topic (Will Topic), Retain Flag (Will Retain), Properties (Will Properties), QoS (Will QoS), and Payload (Will Payload) for the Will Message.

![mqtt will message fields](https://assets.emqx.com/images/293f990f249a16a5236ed4daaaba5877.jpg)

The usage of these fields is the same as when they are in normal messages. The only difference is that the properties available for Will Messages are slightly different from normal application messages. The following table lists their specific differences:

![mqtt will message](https://assets.emqx.com/images/20a001856d5ca98f6c255cc60bd53d0b.jpg)

The Will Message is always published after the client "dies". In a sense, it is also the last message sent by the client. So, the Topic Alias has no meaning in the Will Message.

In addition, the Will Message has one more exclusive property: **Will Delay Interval**. This is an important improvement introduced by [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) for Will Messages, which we will discuss later.

### The Server Publishes the Will Message When the Connection Unexpectedly Closes

If the client specifies a Will Message when connecting, then the server will store this Will Message in the corresponding session, until any of the following conditions are met to publish it:

- An I/O error or network failure detected by the Server.
- The Client fails to communicate within the Keep Alive time.
- The Client closes the Network Connection without first sending a DISCONNECT packet with a Reason Code of 0x00 (Normal disconnection).
- The Server closes the Network Connection without first receiving a DISCONNECT packet with a Reason Code of 0x00 (Normal disconnection). For example, the server disconnects the client because the message or behavior does not meet the protocol requirements.

For simplicity, we can summarize that as long as the network connection is closed without the server receiving a DISCONNECT packet with a Reason Code of 0x00, the server needs to send the Will Message.

When the client has completed its work and is proactively logging off, it can send a DISCONNECT packet with a Reason Code of 0x00, then close the network connection to prevent the server from publishing the Will Message.

### Will Delay Interval and Delayed Publishing

By default, the server publishes the Will Message immediately when the network connection unexpectedly closes. However, the network connection interruption is usually temporary, and the client can reconnect and continue the previous session. This leads to the Will Message potentially being sent frequently and meaninglessly.

Therefore, MQTT 5.0 specifically added a Will Delay Interval property for the Will Message, which determines how long the server will delay the publication of the Will Message after the network connection closes, measured in seconds.

![mqtt will delay interval](https://assets.emqx.com/images/ab9a228706332d8f391d537c92b1b369.png)

If the Will Delay Interval is not specified or set to 0, the server will immediately publish the Will Message when the network connection closes.

If the Will Delay Interval is set to a value greater than 0, and the client restores the connection before the Will Delay Interval expires, then the Will Message will not be published.

### Will Message and Session

The Will Message is part of the server session state, and when the session ends, the Will Message cannot continue to exist separately.

During the delayed publication of the Will Message, the session might expire, or the server may need to discard the previous session because the client sets Clean Start to 1 in a new connection.

To avoid losing the Will Message, the server must publish the Will Message in this case, even if the Will Delay Interval has not yet expired.

So, when the server finally publishes the Will Message, it depends on whichever of the expiration of the Will Delay Interval and the end of the session occurs first.

### The Will Message in MQTT 3.1.1

In MQTT 3.1.1, as long as the network connection is closed without the server receiving a DISCONNECT packet, the server should publish the Will Message.

Since MQTT 3.1.1 does not have the Will Delay Interval or the Session Expiry Interval, the Will Message is always published immediately when the network connection is closed.

## Why hasn’t the Will Message been published?

The delayed publication and cancellation of the Will Message makes the issue of whether the subscriber will receive the Will Message somewhat complex.

We have sorted out all possible situations to help you better understand:

![when publish will message](https://assets.emqx.com/images/6ebb67496715f5086050d77a2c7924af.jpg)

1. If the connection unexpectedly closes and the Will Delay Interval equals 0, the Will Message will be published immediately when the network connection closes.
2. If the connection unexpectedly closes and the Will Delay Interval is greater than 0, the Will Message will be delayed. The maximum delay time depends on whether the Will Delay Interval or Session Expiry Interval expires first:
   1. If the client fails to restore the connection before the Will Delay Interval or Session Expiry Interval expires, the Will Message will be published.
   2. Before the Will Delay Interval or Session Expiry Interval expires:
      1. The client specifies Clean Start as 0 to restore the connection, the Will Message will not be published.
      2. The client specifies Clean Start as 1 to restore the connection, the Will Message will be immediately published because **the existing session ends**.

If the existing network connection has not been closed, but the client initiates a new connection with the same Client ID, the server will send a DISCONNECT packet with a Reason Code of 0x8E (Session Taken Over) to the existing network connection and then close it. This situation is very likely to occur in poor network conditions, and it is also considered an unexpected connection closure.

Now, consider this question: If the existing network connection's Session Expiry Interval equals 0, and Will Delay Interval is greater than 0, will the server send the Will Message when the client specifies Clean Start as 0 to initiate a new network connection?

The answer is that the Will Message will be published immediately when the existing network connection is disconnected.

When the server closes the existing network connection, the session ends immediately because the Session Expiry Interval is 0. Although Clean Start is set to 0, the server will create a new session for the new network connection. So, the Will Message will be published because the session ends, satisfying scenario 2.1 rather than 2.2.1 as listed above.

## Tips for Using the Will Message

### Using the Retained Message

Once the server publishes the Will Message, it will be removed from the session. If the client who cares about this Will Message is not online, then it will miss this Will Message.

To avoid this situation, we can set the Will Message as a retained message, so that after the Will Message is published, it will still be stored on the server in the form of a retained message, and the client can get this Will Message at any time.

Going further, we can also implement status monitoring for specific clients.

Let the client myclient specifies a Will Message with a topic of myclient/status, a payload of offline, and a Will Retain flag set every time it connects. Whenever the connection is successful, it publishes a retained message with a payload online to the topic myclient/status. Then, we can subscribe to the topic myclient/status at any time to get the latest status of the client myclient.

### Session Expiry Notification

By setting a Will Delay Interval larger than the Session Expiry Interval, the server can send out session expiration notifications as a Will Message. This is more useful for applications that care more about session expiration than network connection interruptions. Even if it is an active offline, the client can send a DISCONNECT packet with a Reason Code of 0x04 to request the server to still send the Will Message.

## Demo

### Using MQTTX

Install and open [MQTTX](https://mqttx.app/), we first initiate a client connection to the [Free Public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker). In this connection, we specified a Will Message with a topic of `mqttx_c7f95fdf/status`, a Payload of offline, and set the Will Delay Interval to 5 seconds, and Session Expiry Interval to 300 seconds. Using the Client ID as a prefix for the topic can effectively avoid duplication with topics used by others on the public server:

![MQTTX](https://assets.emqx.com/images/e9873d7e2e2bbeb2faea074e220cf724.png)

Create a new client connection, connect to the Public MQTT server, and then subscribe to the topic mqttx_c7f95fdf/status to receive the Will Message:

![new mqtt subscription](https://assets.emqx.com/images/56361c0032b7b6ca8f0b6d4ef4b7c15f.png)

Next, we let the first client send a message with an empty topic, but a topic alias set. Since we have not yet established a mapping between the topic and the topic alias, this will cause the server to consider the client's behavior as not conforming to the protocol rules and close the connection, and then send the Will Message:

![send mqtt message](https://assets.emqx.com/images/4d04a2baa33ffbd3f3add8979a020c7a.png)

Since the Will Delay Interval is set, we will see the Will Message arrive on the subscriber 5 seconds after sending the message:

![receive mqtt will message](https://assets.emqx.com/images/2c3dfc1f785dad82dffca014cdcba7ad.png)

### Using MQTTX CLI

In the terminal, we can use the command line tool [MQTTX CLI](https://mqttx.app/cli) to verify the behavior of the Will Message. Next, let's see what happens when the client connection recovers before publishing the Will Message.

First, initiate the connection in the first terminal window and subscribe to the will topic:

```
$ client_id="mqttx_"`date | sha256sum | base64 | head -c 8`
$ echo ${client_id}
mqttx_YzFjZmVj
$ mqttx sub -h broker.emqx.io --topic ${client_id}"/status"
…  Connecting...
✔  Connected
…  Subscribing to mqttx_YzFjZmVj/status...
✔  Subscribed to mqttx_YzFjZmVj/status
```

Then, in the second terminal window, establish a client connection that specifies the Will Message, and set the Will Delay Interval to 10 seconds, and the Session Expiry Interval to 300 seconds.

After the connection is successful, enter Ctrl+C to exit, which will cause the client not to send a DISCONNECT packet and directly disconnect the network connection:

```
$ client_id="mqttx_YzFjZmVj"
$ mqttx conn -h broker.emqx.io --client-id ${client_id} --will-topic ${client_id}"/status" --will-message "offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

Run the following command to reconnect within 10 seconds:

```
$ mqttx conn -h broker.emqx.io --client-id ${client_id} --no-clean --session-expiry-interval 300
```

The subscriber in the first terminal window will not receive the Will Message.

These are two simple examples. You can use MQTTX and Free MQTT public server to verify more characteristics of the Will Message, such as when Will Messages will be published and when they will not be published.

In addition, We provided Python sample code for Will Messages in [emqx/MQTT-Features-Example](https://github.com/emqx/MQTT-Feature-Examples), you can use it as a reference.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
