## What is the Message Expiry Interval？

The Message Expiry Interval is a new feature introduced in MQTT 5.0, which allows the publisher to set an expiry interval for time-sensitive messages. If the message remains on the server beyond this specified interval, the server will no longer distribute it to the subscribers. By default, the message does not include the message expiry interval, which means the message will never expire.

MQTT's persistent sessions can cache unsent messages for offline clients and send them when the client reconnects. However, if the client is offline for a long time, there may be some short-lived messages that are no longer necessary to be sent to the client. Continuing to send these expired messages will only waste network bandwidth and client resources.

Take connected cars as an example, we can send suggested driving speeds to the vehicle so it can pass the intersection during the green light. These messages are usually only valid before the vehicle reaches the next intersection, with a very short life cycle. Messages like front congestion alerts have a longer life cycle, generally valid within half an hour to 1 hour.

If the client sets an expiry interval when publishing a message, the server will also include the expiry interval when forwarding this message, but the value of the expiry interval will be updated to the value received by the server minus the time the message stays on the server.

This can prevent the timeliness of the message from being lost during transmission, especially when bridging to another MQTT server.

![02example.png](https://assets.emqx.com/images/55a8cabcba476a24d6533d2bc3af8651.png)

## When to use the Message Expiry Interval?

The Message Expiry Interval is very suitable for use in the following scenarios:

1. Messages that are strongly bound with time. For instance, a message like 'the discount ends in the next two hours'. If the user receives it after two hours, it would be meaningless.
2. Messages periodically inform the latest status. Continuing with the example of road congestion alerts, we need to periodically send vehicles the expected end time of congestion, which changes with the latest road conditions. So when the latest message arrives, there is no need to continue sending the previous unsent messages. In this case, the message expiry interval is determined by our actual sending cycle.
3. Retained messages. Compared to needing to resend a retained message with an empty Payload to clear the retained message under the corresponding topic, it is obviously more convenient to set an expiration time for it and then have the server automatically delete it, which can also effectively avoid retained messages occupying too much storage resources.

## Demo

1. Access [MQTTX Web](http://www.emqx.io/online-mqtt-client) on a Web browser.

2. Create an MQTT connection named `pub` for publishing messages, and connect it to the [Free Public MQTT Server](http://broker.emqx.io/):

   ![03mqttx.png](https://assets.emqx.com/images/2327dc0ea7bdc040b6b89eac680f4ed0.png)

3. Create a new MQTT connection named `sub` for subscribing, and set the Session Expiry Interval to 300 seconds to indicate that it requires a persistent session:

   ![04mqttx.png](https://assets.emqx.com/images/6ed493df8267f78c5612b83c7a4890ae.png)

4. After successfully connecting, we subscribe to the topic `mqttx_a3c35d15/demo`, using the Client ID as the topic prefix can effectively avoid duplication with the topics used by other users in the public server:

   ![05mqttx.png](https://assets.emqx.com/images/3d913900921b8e366f349e6c37287500.png)

5. After successfully subscribing, we disconnect the `sub` client from the server, then switch to the `pub` client, and publish the following two messages with Message Expiry Intervals of 5 seconds and 60 seconds respectively to the topic `mqttx_a3c35d15/demo`:

   ![06mqttx.png](https://assets.emqx.com/images/b1652e4a3e3656c0ba54c64ba225c40d.png)

   ![07mqttx.png](https://assets.emqx.com/images/c8a4110c0921c4127fed360eab08b6b9.png)

6. After publishing, switch to the `sub` client, set Clean Session to false to indicate the desire to restore the previous session, then wait at least 5 seconds before reconnecting. We will see that `sub` only received the message with an expiry time of 60 seconds because another message has already expired by this time:

   ![08mqttx.png](https://assets.emqx.com/images/d3c2857b87a202746db933bde5d5b1f2.png)

   ![09mqttx.png](https://assets.emqx.com/images/3f8e75a21451f0d8fe6fe1b5dd2a6378.png)

The above is the usage and effect of the Message Expiry Interval. You can also get the Python sample code for Message Expiry Interval [here](https://github.com/emqx/MQTT-Feature-Examples).

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
