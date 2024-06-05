## Why do we need Subscription Identifiers?

Most implementations of [MQTT clients](https://www.emqx.com/en/mqtt-client-sdk) use a callback mechanism to handle incoming messages.

Within the callback function, we only have access to the topic name of the message. If it is a non-wildcard subscription, the topic filter used during the subscription will be identical to the topic name in the message. Therefore, we can directly establish a mapping between the subscribed topics and callback functions. Then, upon message arrival, we can look up the corresponding callback based on the topic name in the message and execute it.

However, if it’s a wildcard subscription, the topic name in the message will be different from the original topic filter used during the subscription. In this case, we need to match the topic name in the message with the original subscription one by one to determine which callback function should be executed. This obviously affects the processing efficiency of the client.

![MQTT Subscription](https://assets.emqx.com/images/5b3b24a4406e4d342355138f90dd438b.png)

In addition, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) allows a client to establish multiple subscriptions, so a single message can match multiple client subscriptions when using the wildcard subscription.

In such cases, MQTT allows the server to send a separate message for each overlapping subscription or only one message for all the overlapping subscriptions. The former option means that the client will receive multiple duplicate messages.

Regardless of whether it's the former or latter option, the client cannot determine which subscription(s) the message originated from. For example, even if the client finds that a message matches two of its subscriptions, it cannot guarantee that both subscriptions have been successfully created when the server forwards the message to itself. Therefore, the client cannot trigger the correct callback for the message.

![MQTT Subscription](https://assets.emqx.com/images/3a86d62e52c9bfcef85ba590d14c4a19.png)


## How does the Subscription Identifier work?

To address this issue, MQTT 5.0 introduced Subscription Identifiers. Its usage is very simple: clients can specify a Subscription Identifier when subscribing, and the server needs to store the mapping relationship between the subscription and the Subscription Identifier. When a PUBLISH packet matches a subscription and needs to be forwarded to the client, the server will return the subscription identifier associated with the subscription to the client together with the PUBLISH packet.

![Subscription Identifier](https://assets.emqx.com/images/f9f1cf19de90a4e03647dbe52d69f7e7.png)

If the server chooses to send separate messages for overlapping subscriptions, each PUBLISH packet should include the Subscription Identifier that matches the subscription. If the server chooses to send only one message for overlapping subscriptions, the PUBLISH packet will contain multiple Subscription Identifiers.

The client only needs to establish a mapping between Subscription Identifiers and callback functions. By using the Subscription Identifier in the message, the client can determine which subscription the message originated from and which callback function should be executed.

![MQTT Subscription](https://assets.emqx.com/images/7ba966d802c9ee39683870366f5fd7c7.png)

In the client, the Subscription Identifier is not part of the session state, and its association with any content is entirely determined by the client. Therefore, besides callback functions, we can also establish mappings between Subscription Identifiers and subscribed topics, or between Subscription Identifiers and the Client ID. The latter is particularly useful in gateway scenarios where the gateway receives messages from the server and needs to forward them to the appropriate client. With the Subscription Identifier, the gateway can quickly determine which client should receive the message without re-matching and routing the topics.

A SUBSCRIBE packet can only contain one Subscription Identifier. If a SUBSCRIBE packet includes multiple subscriptions, the same Subscription Identifier will be associated with all those subscriptions. So, please ensure that associating multiple subscriptions with the same callback function is intentional.

## Demo

1. Access [MQTTX Web](http://mqtt-client.emqx.com/) on a Web browser.

2.  Create an [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) connection and connect to the [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker):

   ![MQTT over WebSocket](https://assets.emqx.com/images/e1c10cbd018d0742f21f3b371ec89c6a.png)

3. After a successful connection, we subscribe to the topic `mqttx_4299c767/home/+` and specify the Subscription Identifier as 1. Then, we subscribe to the topic `mqttx_4299c767/home/PM2_5` and specify the Subscription Identifier as 2. Since the public server can be used by many people simultaneously, to avoid topic conflicts, we use the Client ID as the topic prefix:

   ![New Subscription 1](https://assets.emqx.com/images/f3c0aed851e02f20aae69cf100b167d6.png)

   ![New Subscription 2](https://assets.emqx.com/images/212728b6ae71b5baf73a860f75d4545a.png)

4. After a successful subscription, we publish a message to the topic `mqttx_4299c767/home/PM2_5`. We will observe that the current client receives two messages, and the Subscription Identifier in the messages is 1 and 2, respectively. This is because EMQX's implementation sends separate messages for overlapping subscriptions:

   ![Receive MQTT Messages](https://assets.emqx.com/images/fd38994dea83422bb31a85b5c14711b1.png)

5. And if we publish a message to the topic `mqttx_4299c767/home/temperature`, we will see that the Subscription Identifier in the received message is 1:

   ![image.png](https://assets.emqx.com/images/f0a2dba909a1efa8fab0b07ea961a959.png)

So far, we have demonstrated how to set a Subscription Identifier for subscription through [MQTTX](https://mqttx.app/). If you are still curious about how to trigger different callbacks based on Subscription Identifier, you can get the Python sample code for Subscription Identifier [here](https://github.com/emqx/MQTT-Feature-Examples).



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
