As the most popular communication protocol in the Internet of Things (IoT) field, the latest version of MQTT has already reached 5.0 in 2019. Compared with previous versions, 5.0 has added features more in line with modern IoT application requirements, such as session expiry, reason codes, shared subscriptions, request-response, etc., making it the preferred version for the majority of IoT companies.

To give you a more comprehensive understanding of MQTT 5.0, this article will introduce each new feature introduced in 5.0 in turn, and use the [MQTTX CLI](https://mqttx.app/) tool to demonstrate how we can use these features in [EMQX](https://www.emqx.io/). You can easily run the examples in this article by copying and pasting commands.

Before we start, we need to complete the following preparations:

1. Use Docker to deploy a basic EMQX instance, you can run the following command:

   ```
   docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx:5.1.3
   ```

2. Download and install [MQTTX CLI](https://mqttx.app/downloads) 1.9.4. It is an open-source MQTT 5.0 command-line client tool, and we will use it to complete all the examples in this article.

3. Install [Wireshark](https://www.wireshark.org/). In some examples, we will use it to capture and analyze some [MQTT packets](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets), which can help us better understand what exactly happened. 

## Feature 1: Session Expiry

In MQTT 5.0, the client can use Session Expiry Interval in the CONNECT packet to indicate the session expiration interval (in seconds) it expects after the network connection is disconnected. If the server does not accept this expiration interval, it can also indicate a new expiration interval in the CONNACK packet, and the client should comply with the server's requirements.

Before the session expires, both the client and the server need to store the corresponding session status. Taking the server as an example, the session status it needs to store includes messages that have been sent but not yet confirmed, messages that have not been sent, and the client's subscription list, etc.

As long as the connection between the client and the server is restored before the session expires, they can continue their previous communication, as if the connection had never been interrupted.

### Example 1

The client sub1 subscribes to the topic t1 and sets the Session Expiry Interval to 60 seconds. After the subscription is successful, disconnect the client by typing Ctrl+C in the terminal.

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
^C
```

Publish a message to the topic t1 within 60 seconds:

```
mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

Reconnect the client sub1, note that the --no-clean option is specified here, indicating the desire to reuse the previous session. We will see that this client received the message that we published before it connected: 

```
mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
payload: Hello World
✔  Subscribed to t1
```

### Example 2

The maximum session expiration interval allowed by EMQX by default is 2 hours. We can access the EMQX Dashboard (by typing http://localhost:18083 in the browser), and modify it through the Session Expiry Interval configuration item on the Management -> MQTT Settings -> Session page.

In this example, we set it to 0 seconds, which means the session will expire immediately when the network connection is disconnected:

![MQTT Session Expiry Interval](https://assets.emqx.com/images/84a3d445ad64b2bb5c0ac0d7575637cf.png)

Next, repeat the steps in example 1. This time, the client sub1 will not receive the message after reconnecting:

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
^C

mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published

mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
```

## Feature 2: Message Expiry

In MQTT 5.0, we can set an expiration interval (in seconds) for each message. If the message remains on the server beyond this period, it will no longer be distributed to the client.

This feature becomes extremely useful when we wish to retain sessions for a lengthy duration while also dispatching some time-sensitive messages.

Furthermore, if the client sets an expiration interval while publishing a message, the server will also include the expiration interval when forwarding this message. However, the value of the expiration interval will be updated to the value received by the server minus the time that the message stayed on the server.

In this way, the receiver can know that this message is time-sensitive and when it will expire.

### Example 1

The client sub2 subscribes to the topic t2 and sets the Session Expiry Interval to 300 seconds. After the subscription is completed, type Ctrl+C in the terminal to disconnect the client:

```
mqttx sub --client-id sub2 --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
^C
```

Publish a message to the same topic and set the Message Expiry Interval to 5 seconds:

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 5
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

Wait for 10 seconds before reconnecting the client sub2, it will not receive the message we just published:

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
```

### Example 2

Continue to publish messages to topic t2 and set the Message Expiry Interval to 60 seconds:

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 60
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

Wait for 10 seconds before reconnecting the client sub2, it will receive the message we just published, with a Message Expiry Interval of 50 seconds:

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 0 --topic t2 --output-mode clean
{
  "topic": "t2",
  "payload": "Hello World",
  "packet": {
  	...
    "properties": {
      "messageExpiryInterval": 50
    }
  }
}
```

## Feature 3：All response packets support reason codes

MQTT 5.0 not only adds a reason code field to all response packets, but also expands the available reason codes. Now both the server and client can clearly indicate the cause of an error to each other. 

For example, when a message arrives but there is no matching subscription, the server will discard this message. But in order to let the sender know what happened, the server will set the reason code in the response packet to 0x10 (only for QoS 1 and QoS 2 messages), indicating that there is no matching subscriber.

> You can learn more about reason codes through [MQTT Reason Code Introduction and Quick Reference](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack).

### Example

In this example, we will use Wireshark. After launching Wireshark, select the correct network interface first. If your EMQX and MQTTX CLI are running on the same machine, then you should select the loopback interface as in this example, and then enter the following filter statement to capture packets:

```
tcp.port == 1883
```

Publish a QoS 1 message to the topic t3:

```
mqttx pub --topic t3 --message "Hello World" --qos 1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

In the Wireshark, we will see that the Reason Code in the PUBACK packet returned by EMQX is set to 0x10:

![Wireshark](https://assets.emqx.com/images/dc6b0ade500c1df276114bd14d4792fe.png)

## Feature 4: Server Disconnect

MQTT 5.0 allows the server to send a DISCONNECT packet before disconnecting, to indicate to the client the reason for the disconnection.

### Example

Type the following filter statement in Wireshark to capture packets:

```
tcp.port == 1883
```

Establish an MQTT connection:

```
mqttx conn --client-id conn4
…  Connecting...
✔  Connected
```

In another terminal window, use the CLI command provided by EMQX to manually kick the client:

```
docker exec emqx emqx ctl clients kick conn4
ok
```

We will see the connection disconnected in the first terminal window:

```
✖  Connection closed
```

The Reason Code in the DISCONNECT packet sent by EMQX is set to 0x98, indicating that the connection is closed due to management operations:

![Wireshark](https://assets.emqx.com/images/05744c8ecd86b07215cff789c10425cb.png)

## Feature 5: Payload Format and Content Type

In MQTT 5.0, the publisher can use the Payload Format Indicator to indicate whether the content of the message is UTF-8 encoded character data or binary data in an unspecified format.

Content Type can further indicate the specific format of the message content, so that the receiver can more easily know how to parse the message. A common practice is to set it to a MIME content type such as application/json. Of course, this is not mandatory, we can also use any UTF-8 string to indicate our custom message type.

### Example

Subscribe to topic t6:

```
mqttx sub --topic t6 --output-mode clean
```

Publish a message in another terminal window, set Payload Format Indicator to indicate that the content of this message is UTF-8 encoded character data, set Content Type to application/json to indicate that this is a message in JSON format:

```
mqttx pub --topic t6 --message "{\"content\": \"Hello World\"}" --payload-format-indicator --content-type application/json 
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

The first terminal window will print the content of the received message, we can see that the Content Type and Payload Format Indicator are included in the message:

```
{
  "topic": "t6",
  "payload": "{\"content\": \"Hello World\"}",
  "packet": {
		...
    "properties": {
      "contentType": "application/json",
      "payloadFormatIndicator": true
    }
  }
}
```

 

 

## Feature 6: Request-Response

MQTT 5.0 greatly improves support for the request-response pattern. The requester can specify a response topic (Response Topic) in the request message, and the responder needs to publish a response message to the response topic.

This is very useful when there are multiple requesters at the same time, and the responder needs to correctly reply the response to one of the requesters. Different requesters only need to specify different response topics. A simple way to do this is to include your own Client ID in the response subject.

MQTT cannot guarantee that the request of the requester will be received by the responder, and vice versa. Therefore, the requester also needs to be able to correctly associate the request it sends with the response it receives. In MQTT 5.0, we can set Correlation Data in the request, and the responder will return the Correlation Data in the response intact, so that the requester can know which request this is in response to.

### Example

In the first terminal window, the responder subscribes to the topic of the request:

```
mqttx sub --client-id responder --topic request --session-expiry-interval 300 --output-mode clean
```

In the second terminal window, the requester publishes a request message and sets the response topic to response/requester1:

```
mqttx pub --client-id requester1 --session-expiry-interval 300 --topic request --message "This is a reuqest" --response-topic response/requester1 --correlation-data request-1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

In the first terminal window, the responder receives the request message, which contains the Response Topic and Correlation Data:

```
{
  "topic": "request",
  "payload": "This is a reuqest",
  "packet": {
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      },
      "responseTopic": "response/requester1"
    }
  }
}
```

Back to the second terminal window, the requester subscribes to the Response Topic (in practical applications, the requester needs to subscribe to the Response Topic before publishing the request to avoid missing the response message):

```
mqttx sub --client-id requester1 --no-clean --session-expiry-interval 300 --topic response/requester1 --output-mode clean
```

In the first terminal window, the responder publishes a response to the Response Topic in the received request, and carries Correlation Data:

```
mqttx pub --client-id responder --topic response/requester1 --message "This is a response" --correlation-data request-1
```

In the second terminal window, the requester receives the response message:

```
{
  "topic": "response",
  "payload": "This is a response",
  "packet": {
  	...
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      }
    }
  }
}
```

 

## Feature 7：Shared Subscriptions

MQTT 5.0 adds support for [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), enabling subscribers to consume messages in a load-balanced manner.

It allows us to divide subscribing clients into multiple subscribing groups, and messages will still be forwarded to all subscribing groups, but clients in a subscribing group will alternately receive messages with strategies such as random and round-robin. These policies are completely implemented by the server, and the client does not need to make any modifications. The only thing that needs to be done is to initiate a shared subscription through $share/{ShareGroup}/{Topic}.

 

### Example

In the first terminal window, subscribe to the topic $share/g1/t7:

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

In the second terminal window, subscribe to the same topic:

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

In the third terminal window, subscribe to the topic $share/g2/t7:

```
mqttx sub --topic '$share/g2/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g2/t7...
✔  Subscribed to $share/g2/t7
```

In the fourth terminal window, publish a message to the topic t7, here we use the --multiline option to send multiple messages by pressing Enter each time:

```
mqttx pub --topic t7 -s --stdin --multiline
…  Connecting...
✔  Connected, press Enter to publish, press Ctrl+C to exit
Message 1
Message 2
Message 3
Message 4
Message 5
Message 6
^C
```

EMQX's default shared subscription strategy is round_robin, which means that messages will be distributed to subscribers in the same subscription group in turn. So we will see that the subscribers in the first and second terminal windows will alternately receive our published messages:

```
payload: Message 1

payload: Message 3

payload: Message 5
payload: Message 2

payload: Message 4

payload: Message 6
```

There is only one subscriber in the shared subscription group g2 , so we will see all messages received by the subscriber in the third terminal window:

```
payload: Message 1

payload: Message 2

payload: Message 3

payload: Message 4

payload: Message 5

payload: Message 6
```

## Feature 8: Subscription Identifier

MQTT 5.0 allows the client to set a Subscription Identifier when subscribing, and the server will bind the identifier to the subscription. When the server forwards a message to the subscription, it will attach the corresponding identifier to the message. The client can use the subscription identifier in the message to decide which callback to trigger or to perform other operations.

### Example

The same client subscribes to topics t8/1 and t8/#, and sets different Subscription Identifiers:

```
mqttx sub --client-id sub8 --session-expiry-interval 300 --topic t8/1 --subscription-identifier 1
…  Connecting...
✔  Connected
…  Subscribing to t8/1...
✔  Subscribed to t8/1
^C
mqttx sub --client-id sub8 --no-clean --session-expiry-interval 300 --topic t8/# --subscription-identifier 2 --output-mode clean 
```

In the second terminal window, publish a message to topic t8/1:

```
mqttx pub --topic t8/1 --message "Hello World"
```

The subscriber in the first terminal window will receive two messages. According to the Subscription Identifier in the message, we can know that the first message comes from the subscribed topic t8/#, and the second message comes from the subscribed topic t8/1:

```
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
		...
    "properties": {
      "subscriptionIdentifier": 2
    }
  }
}
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
		...
    "properties": {
      "subscriptionIdentifier": 1
    }
  }
}
```

> When a message matches multiple subscriptions of the same client, the MQTT server can send a message to each of these overlapping subscriptions, or send only one message to these overlapping subscriptions. EMQX belongs to the former.

 

## Feature 9: Topic Alias

MQTT 5.0 allows us to replace the topic name with a two-byte integer-type Topic Alias when publishing a message, which can effectively reduce the size of the PUBLISH packet when the topic name is long.

When using a topic alias, we need to send a message containing both the topic name and the Topic Alias first, let the peer establish a mapping relationship, and then send a message containing only the Topic Alias.

The Topic Aliase mapping is not part of the session state, so even if the session is restored when the client reconnects, it needs to re-establish the mapping of topic aliases with the server.

The Topic Alias mappings used by the client and server are independent of each other. Therefore, the message with the Topic Alias value 1 sent from the client to the server and the message with the Topic Alias value 1 sent from the server to the client will be mapped to different topics.

The client and server can also agree on the maximum value of Topic Alias that can be sent to each other when connecting. The maximum value of Topic Alias allowed by EMQX by default is 65535. We access open the EMQX Dashboard (type `http://localhost:18083` in the browser), and configure it through the Max Topic Alias on the Management -> MQTT Settings -> General page item to modify it.

![MQTT 主题别名](https://assets.emqx.com/images/c853659e22cf620edc4eadb562cf7633.png)

## Feature 10: Flow Control

In MQTT 5.0, the client and the server can use Receive Maximum to indicate the maximum number of unconfirmed QoS 1 and QoS 2 messages that they are willing to process at the same time.

When the number of messages that have been sent but not fully acknowledged reaches the maximum limit, the sender cannot continue to send messages to the receiver (QoS 0 messages are not subject to this limit). This can effectively prevent the sender from sending too fast and exceeding the processing capacity of the receiver.

## Feature 11: User Properties

Most packets in MQTT 5.0 can contain User Properties. The User Property is a name-value pair composed of UTF-8 encoded strings. The specific content of the name and value can be defined by the implementation of the client and server. We can specify any number of User Properties without exceeding the maximum size of the packet.

The User Properties in packets such as CONNECT and SUBSCRIBE usually depend on the implementation of the specific MQTT server.

The User Properties in the PUBLISH packet will be directly forwarded by the server to the subscriber without modification, so as long as the publisher and the subscriber agree on the content of the User Properties. For example, attach the client ID of the publisher to the User Property of the application message, so that the subscriber can know where the message comes from.

### Example

Subscribe to the topic t11:

```
mqttx sub --topic t11 --output-mode clean
```

In another terminal window, publish a message to topic t11 and set two User Properties, one indicating the source of the message and one indicating when it was published:

```
mqttx pub --client-id pub11 --topic t11 --message "Hello World" --user-properties "from: pub11" --user-properties "timestamp: 1691046633"
```

Back in the first terminal window, the message received by the subscriber contains the User Properties we set:

```
{
  "topic": "t11",
  "payload": "Hello World",
  "packet": {
		...
    "properties": {
      "userProperties": {
        "from": "pub11",
        "timestamp": "1691046633"
      }
    }
  }
}
```

## Feature 12: Maximum Packet Size

MQTT 5.0 allows the client and the server to agree on the maximum packet size that they can handle through the Maximum Packet Size property when connecting. After that, neither party can send a packet that exceeds the agreed size limit, otherwise it will cause a protocol error and the connection will be closed.

Therefore, when the PUBLISH packet is too large to be forwarded, the server will discard the PUBLISH packet.

### Example 1

In the first terminal window, declare to the server that the Maximum Packet Size it can accept is 128 bytes, and subscribe to topic t12:

```
mqttx sub --maximum-packet-size 128 --topic t12
…  Connecting...
✔  Connected
…  Subscribing to t12...
✔  Subscribed to t12
```

In a second terminal window, publish a message that is less than 128 bytes long:

```
payload=$(head -c 10 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "$payload"
```

In the first terminal window, the subscriber will receive the following message:

```
payload: 0000000000
```

Publish a message longer than 128 bytes in a second terminal window:

```
payload=$(head -c 128 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "${payload}"
```

This time the subscriber in the first terminal window will not receive the message, we can type Ctrl+C to disconnect the subscriber, and then run the following command to view the EMQX log:

```
docker logs emqx
```

We will see the log that the message was dropped due to frame_is_too_large:

```
2023-08-03T06:17:52.538541+00:00 [warning] msg: packet_is_discarded, mfa: emqx_connection:serialize_and_inc_stats_fun/1, line: 872, peername: 172.17.0.1:39164, clientid: mqttx_f0a3847c, packet: PUBLISH(Q0, R0, D0, Topic=t12, PacketId=undefined, Payload=******), reason: frame_is_too_large
```

 

### Example 2

The Maximum Packet Size allowed by EMQX is 1MB by default. We can access the EMQX Dashboard (type http://localhost:18083 in the browser), and modify the Max Packet Size configuration item on the Management -> MQTT Settings -> General page.

Note that the maximum size limit is for all packets, so if the Maximum Packet Size is too small, the connection may not be established. This is what we should pay attention to avoid.

In this example, we modify it to 1024 bytes:

![图片.png](https://assets.emqx.com/images/512963490e383148c2288bf5255f8751.png)

Then type the following filter statement in Wireshark to capture packets:

```
tcp.port == 1883
```

Publish a message longer than 1024 bytes in a terminal window:

```
payload=$(head -c 1024 < /dev/zero | tr '\0' 0)
mqttx pub --client-id pub12 --topic t12 -m "${payload}"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

In Wireshark, we will see that EMQX returns a DISCONNECT packet, and sets the Reason Code to 0x95, indicating that the connection has been closed due to receiving an oversized message:

![Wireshark](https://assets.emqx.com/images/3ac6a07014588cc82ea14365795e8843.png)

## Feature 13: Optional Server Feature Availability

MQTT allows the server to not fully support the functions and features declared by the protocol, but the server needs to inform the client of the unsupported features in the CONNACK packet to prevent the client from using these unavailable functions. Optional server-side features include:

- Maximum QoS level supported
- Retained Message
- Wildcard Subscription
- Subscription Identifier
- Shared Subscription

If the client still uses the feature that the server has notified as unavailable, it will cause a protocol error and the server will close the connection.

### Example

EMQX supports all MQTT features by default, but we can manually disable some features, such as wildcard subscription, shared subscription, retained messages, etc. In this example, we disable the retained message feature:

![Disable the retained message feature](https://assets.emqx.com/images/16873e4be8c387d5766c68b69d2a51f1.png)

Type the following filter statement in Wireshark to capture packets:

```
tcp.port == 1883
```

Publish a retained message in the terminal window:

```
mqttx pub --topic t13 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

In the Wireshark, we will see that EMQX returns the availability of each feature in the CONNACK packet, and the retained message is declared as unavailable:

![Wireshark](https://assets.emqx.com/images/542a90a629c938de745d7abb7016ca1e.png)

After the client publishes the retained message, EMQX returns a DISCONNECT packet and sets the Reason Code to 0x9A, indicating that the server does not support retained messages:

![Wireshark](https://assets.emqx.com/images/e79cda1541771f559068a4813d1d3ded.png)

After completing this example, please enable the retained message feature of EMQX again, so as not to affect the subsequent examples.

## Feature 14: Subscription Options

MQTT 5.0 provides three new subscription options other than QoS, namely:

1. No Local, used to indicate whether the message can be forwarded to the client that published this message.
2. Retain As Published, used to indicate whether the server needs to keep the Retain flag when forwarding the message to this subscription.
3. Retain Handling, used to indicate whether the server needs to send retained messages to the subscription when the subscription is established. This option has three possible values:
   1. Set to 0, send retained messages whenever the subscription is established.
   2. Set to 1, send retained messages only if the subscription does not exist when the subscription is established.
   3. Set to 2, no retained messages will be sent when the subscription is established.

You can read more about subscription options in [An Introduction to Subscription Options in MQTT](https://www.emqx.com/en/blog/an-introduction-to-subscription-options-in-mqtt).

### Example 1 - No Local

Clients sub14 and pub14 publish a message to topic t14 respectively. Here we use EMQX's [Delayed Publish](https://www.emqx.io/docs/en/v5.1/messaging/mqtt-delayed-publish.html) feature to delay publishing messages by 10 seconds:

```
mqttx pub --client-id sub14 --topic '$delayed/10/t14' --message "You will not receive this message"
mqttx pub --client-id pub14 --topic '$delayed/10/t14' --message "You will receive this message"
```

Let the client sub14 subscribe to the topic t14, and set the No Local option, it will receive the messages published by the client pub14, but will not receive the messages published by itself:

```
mqttx sub --client-id sub14 --topic t14 --no_local
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: You will receive this message 
```

### Example 2 - Retain As Published

In the first terminal window, subscribe to topic t14 and set the Retain As Published option:

```
mqttx sub --topic t14 --retain-as-published --output-mode clean
```

In the second terminal window, publish a retained message to topic t14:

```
mqttx pub --topic t14 --message "Hello World" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

In the first terminal window, the subscriber will receive the message with the Retain flag set:

```
{
  "topic": "t14",
  "payload": "Hello World",
  "packet": {
  	...
    "retain": true,
		...
  }
}
```

Clear retained messages:

```
mqttx pub --topic t14 --message '' --retain
```

### Example 3 - Retain Handling

Publish a retained message to topic t14:

```
mqttx pub --topic t14 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

Subscribing to the same topic and setting Retain Handling to 0, we will receive retained messages:

```
mqttx sub --client-id sub14 --session-expiry-interval 300 --topic t14 --retain-handling 0
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: This is a retained message
retain: true
^C
```

Type Ctrl+C in the terminal to disconnect the client.

Reconnect and resume the session, subscribe to the same topic, but set Retain Handling to 1, this time we will not receive the retained message, because the subscription already exists on the server side:

```
mqttx sub --client-id sub14 --no-clean --session-expiry-interval 300 --topic t14 --retain-handling 1
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
^C
```

Type Ctrl+C in the terminal to disconnect the client.

Reconnecting but creating a new session, subscribing to the same topic, setting Retain Handling to 2, this time we still won't receive the retained message:

```
mqttx sub --client-id sub14 --topic t14 --retain-handling 2
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
```

Clear retained messages:

```
mqttx pub --topic t14 --message '' --retain
```

## Feature 15: Will Delay

In MQTT 5.0, the client can set a delay interval for the [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) instead of letting it be published immediately when the network connection is closed. If the client connection can be restored in time before the Will Delay Interval expires, the will message will not be published. This effectively prevents will messages from being published just because of a brief interruption of the client's connection.

If the Will Delay Interval is greater than the Session Expiry Interval, then the will message will be sent immediately when the session expires, so we can also use the will message for session expiration notification.

### Example 1

Subscribe to topic t15 in the first terminal window:

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
```

Establish an MQTT connection with a will message in the second terminal window, and set the Will Delay Interval to 10 seconds. After the connection is successful, type Ctrl+C to disconnect the client:

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

Subscribers in the first terminal window will receive the will message after 10 seconds:

```
payload: I'm offline 
```

### Example 2

Establish an MQTT connection with a will message in the second terminal window again, and set the Will Delay Interval to 10 seconds. After the connection is successful, type Ctrl+C to disconnect the client:

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

Reconnect within 10 seconds:

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --no-clean --session-expiry-interval 300
```

This time the subscriber in the first terminal window will not receive the will message.

### Example 3

We can also set the Will Retain flag for the will message to make it a retained message, so as to prevent the subscriber from missing the will message because it is not online.

Go ahead and make an MQTT connection with a will message in the second terminal window, this time we set the Will Delay Interval to 0 seconds, so the will messages will be published as soon as the connection is closed. After the connection is successful, type Ctrl+C to disconnect the client:

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 0 --will-retain --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

Subscribing to topic t15 in the first terminal window, we will receive will messages published before this:

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
payload: I'm offline
retain: true
```

 

## Feature 16: Server Keep Alive

The Keep Alive value determines the maximum idle time for the client to send two adjacent control packets, and the server can judge whether it is still active according to whether it receives the client's packet within the expected time.

In MQTT 5.0, the server can not accept the Keep Alive value specified by the client, and returns a Server Keep Alive in the CONNACK packet. The client must use this Keep Alive time to maintain communication.

### Example

By default, EMQX allows the client to specify the Keep Alive. We can access the EMQX Dashboard (type http://localhost:18083 in the browser), and modify it through the Server Keep Alive configuration item on the Management -> MQTT Settings -> General page.

In this example, we set it to 10 seconds.

![MQTT Keep Alive](https://assets.emqx.com/images/db10dece7733daaa0bde63bdda8e314e.png)

Then type the following filter statement in Wireshark to capture packets:

```
tcp.port == 1883
```

Back to the terminal window, initiate an MQTT connection with Keep Alive set to 30 seconds:

```
mqttx conn --keepalive 30
…  Connecting...
✔  Connected
```

We will see in Wireshark that EMQX sets the Server Keep Alive property in the returned CONNACK packet with a value of 10. After the connection is established, the client also sends heartbeat packets at intervals of 10 seconds instead of 30 seconds:

![Wireshark](https://assets.emqx.com/images/2285d82210f5ba969519114020937ef1.png)

## Feature 17: Return the Client ID assigned by the server

When the client uses a Client ID with a length of 0 to initiate a connection, the server will assign a unique Client ID to the client. In MQTT 5.0, the assigned Client ID can be included in the CONNACK packet and returned to the client. This prevents the client from being unable to resume the session on the next connection because it does not know the Client ID.

### Example

Type the following filter statement in Wireshark to capture packets:

```
tcp.port == 1883
```

Back to the terminal window, initiate an MQTT connection and set the Client ID to a zero-length string:

```
mqttx conn --client-id ''
```

We will see in Wireshark that the CONNACK packet returned by EMQX contains an Assigned Client Identifier property, and its value is the Client ID assigned by EMQX to the client:

 ![Wireshark](https://assets.emqx.com/images/ed6e0702da12fdf44e13504af7162759.png)

## Conclusion

The above is the basic introduction and demonstration of all the features of MQTT 5.0. You can try to convert the steps in the demonstration into code and reproduce it in your client. If you want to learn more about these new features of MQTT 5.0, you can visit our [MQTT Guide](https://www.emqx.com/en/mqtt-guide), which aggregates all the knowledge you need to know about MQTT.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
