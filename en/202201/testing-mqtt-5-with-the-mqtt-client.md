Recently, the cross-platform MQTT 5.0 desktop test client MQTT X, which is open-sourced by EMQ, [released the latest version of v1.7.0](https://github.com/emqx/MQTTX/releases/tag/v1.7.0). MQTT X supports the rapid creation of multiple simultaneous online MQTT client connections, tests the connection, publish, and subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket as well as other MQTT protocol features.

The newly released v1.7.0 provides more comprehensive support for MQTT 5.0 and is the desktop test client tool that supports MQTT 5.0 most worldwide so far. At the same time, many new features have been added to optimize the user experience.

In this article, we will introduce in detail the specific use of the new features of MQTT X v1.7.0, especially how to use MQTT X to test features of MQTT 5.0, so that readers can apply MQTT 5.0 in projects better.

## Get MQTT Broker Ready

Before using MQTT X v1.7.0 to test the features of MQTT 5.0, we first need to get an MQTT Broker that supports MQTT 5.0.

This article will use the public MQTT 5.0 Broker provided by [EMQX Cloud](https://www.emqx.com/en/cloud) with the MQTT X client for testing. As a fully managed cloud-native MQTT 5.0 message service, EMQX Cloud can quickly create an MQTT Broker instantly in minutes and fully supports MQTT 5.0. It is also the world's first fully managed MQTT 5.0 public cloud service.

Start a 30-day free trial: [fully managed cloud-native MQTT message service](https://www.emqx.com/en/cloud)

Before the test, the access information of the public MQTT 5.0 broker is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

## MQTT 5.0 test

### User properties

In v1.7.0, we first support the User Properties. [User Properties](https://www.emqx.com/en/blog/mqtt5-user-properties) is a very useful feature in MQTT 5.0. It is a custom property that allows users to add their metadata to MQTT messages and transfer additional custom information to expand more application scenarios, such as message distribution, file transfer, language distinction, etc. This feature is very similar to the concept of HTTP Header. We can configure user properties when creating client connections and publishing messages.

**Client Connection**

Click the New button to go to the new client page. First, we need to select the version of MQTT as 5.0, so that we can see that a card for configuring user properties below. Inside the card, there is an input box that can configure key-value pairs. You can click the Add button in the upper right corner can add user property configuration. Click the Delete button at the end of each line to delete the configuration. Finally, enter the name and content of the property that needs to be configured. After the connection is successful, the MQTT broker can obtain the user properties of the client.

![MQTT Client Connection](https://static.emqx.net/images/891bb0a76b6c2ecf76690266d45bd51c.png)

**Publish messages**

In addition to the configuration of user properties when the client is connected, this version also supports the configuration of user properties when publishing messages. When the new connection is a client of MQTT 5.0, we can see that a `Meta` button appears in the area where the message is published in the lower right corner. Click this button to display a card that configures the properties at the time of publishing. We can see the user property configuration at the top of the card.

![mqtt user property](https://static.emqx.net/images/04b0f36baa9063f008f5285f5af5274f.png)

After configuring the user properties, click the Save button. At this time, we enter Topic and Payload and click Send. Then, we can see that the sent message box contains the user properties contained in the current message. If the message we received also contains the user properties, We can also see the user property configuration sent by the client in the received message box.

![message box contains the user properties](https://static.emqx.net/images/d047089b3a9c14b49bc50e03a360a5cc.png)

With MQTT X's support for user properties, it can help developers quickly verify and test the function of the MQTT 5.0 user properties, thereby improving the efficiency of development and use.

### Request Response

In v1.7.0, the [Request Response](https://www.emqx.com/en/blog/mqtt5-request-response) in MQTT 5.0 is supported, and the configuration of Response Topic and Correlation Data is provided, The response message is routed back to the publisher of the request.

Because the MQTT protocol is based on the Pub/Sub model, which is different from the request/response model like the HTTP protocol, it is difficult for us to receive some response messages. For example, when we want to test a control command, it is difficult for us to obtain the response after the command is issued. Although it can be implemented, it is too complicated. The requested topic in MQTT 5.0 can realize this capability faster and more effectively.

We will show how to use the Response Topic by issuing a command to switch the light and respond to the command. We click the Meta button, enter a Response Topic in the input box: /ack/1, enter a Correlation Data: light, and subscribe to a /ack/1 in the currently connected client.

> Note: MQTT's request/response is asynchronous, and the comparison data can associate the response message with the request message.

![MQTT Response Topic](https://static.emqx.net/images/3943405f5ac48f376d239c7194bf8328.png)

We use MQTT.js to implement another client to simulate a light device that receives control commands. After receiving the command to turn on the light, send a response message of successful turning-on to the response topic. The key code is implemented below:

```
client.on('message', (topic, payload, packet) => {
  console.log('Received Message:', topic, payload.toString())
  if (packet.properties && packet.properties.responseTopic) {
    client.publish(packet.properties.responseTopic, 'Success!', {
      qos: 0,
      retain: false,
    })
  }
})
```

Click Send button, and we can receive the response message from the light device after successfully receiving the switch command.

![MQTT Response Topic](https://static.emqx.net/images/1e7ecbb59602251011fdd7bdf19f2f62.png)

Currently, for the Request Response feature, MQTT X only supports configuring the Response Topic and Correlation Data when sending. In the future, we will continue to optimize the configuration of the response part to bring users a more complete capability to test Request Response.

### **Content type and Payload Format Indicator**

In v1.7.0, the specified configuration of the [Payload Format Indicator and Content Type](https://www.emqx.com/en/blog/mqtt5-new-features-payload-format-indicator-and-content-type) is supported. It is allowed to specify the payload format (binary, text) and MIME style content type when the message is published. We just need to click the Meta button before publishing the message, enter the Content Type in the input box, click to set the value of Payload Format Indicator, and publish the message.

![MQTT Payload Format Indicator](https://static.emqx.net/images/bb8b44bcc722fe53c73d4c9c52c0510c.png)

A typical application of content type is to store MIME types. For example, text/plain means text files, audio/aac means audio files, and application/json means application messages in JSON format.

When the payload indicator property is set to false, the byte of the message is undetermined. When the property is set to true, it means that the payload in the message body is UTF-8 encoded character data.

This will help the MQTT client or MQTT Broker to parse the content of the message more effectively without deliberately judging the format or type of the payload.

### Subscription options

In v1.7.0, [Subscription Options](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options) in MQTT 5.0 are also supported. After creating a new MQTT 5.0 connection, we open the pop-up box of the subscription topic, and the configuration options including No Local, Retain as Published, and Retain Handling appear below. Users can use these subscription options to change the behavior of the broker.

![MQTT Subscription options](https://static.emqx.net/images/e998eb7259b46c683c037d915d65e7f4.png)

If the No Local flag is set to true, the broker will not forward self-published messages to you. Otherwise, if you subscribe to the topic of self-published messages, then you will receive all the messages published by yourself.

If Retain as Published flag is set to true, you can specify whether the broker should retain the Retain identifier when forwarding the message to the client, instead of relying on the retain identifier in the message to distinguish whether this is a normal forwarding message or a retained message.

Retain Handling is used to specify whether the broker sends a retained message to the client when the subscription is established. If it is set to 0, as long as the client subscribes successfully, the broker will send a retained message; If it is set to 1, only when the client subscribes successfully and the subscription does not exist before, the broker sends a retained message; If it is set to 2, even if the customer subscribes successfully, the broker will not send a retained message.

In subsequent versions, we will continue to support new features in MQTT 5.0, such as Subscription Identifier.

## Use of other new features

### One-click multi-topic subscription

In the previous version, we can only subscribe to one topic each time we open the pop-up box for subscribing. For users who want to subscribe to multiple topics, they need to click open and close multiple times to subscribe to multiple topics, which is not very convenient. Therefore, in this version, we have made optimizations to support subscribing to multiple topics at one time.

After we open the pop-up box for subscribing to topics, enter multiple topics and split them with commas (,) in the Topic input box. After clicking to confirm the successful subscription, we can see that multiple topics are included in the subscription list. For using the alias function of the client layer, you can also set multiple topics at the same time. Similarly, use a comma (,) to separate them.

> Note: The content in the alias input box needs to correspond to the Topic in the Topic input box one by one.

![MQTT multi-topic subscription](https://static.emqx.net/images/ce7690743443fcce274cfb4d7ef912f2.png)

### Disable automatic scrolling of messages

The control of automatic scrolling of the message list when receiving and publishing messages were added to the v1.7.0 setting. The auto-scroll function can be enabled in the setting page, which is applicable to help users view the latest messages when the message receiving rate is slow. When the rate of receiving messages is too fast, users can click to turn off this function to view some old messages sent or received.

> Note: When the auto-scroll function is turned off, the performance of sending and receiving messages can be improved.

![MQTT X automatic scrolling](https://static.emqx.net/images/944659abebc73c140c86f53b8dfa3371.png)

## Conclusion

Through this article, we believe that you have a better understanding of the functions of MQTT X v1.7.0. The combination of MQTT X and EMQX can help you fully grasp the MQTT 5.0 protocol and better apply its features in projects.

In the future, we will also improve the ability of MQTT X to support configurations such as Topic Alias, Request Responses, and Subscription Identifier, please stay tuned.
