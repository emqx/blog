MQTT v5 brings lots of new features, and we will try our best to present these features in an easy-to-understand way and discuss the impact of these features on developers. So far, we have discussed these [new features of MQTT v5](https://www.emqx.com/en/mqtt/mqtt5). Today, we will continue to discuss: **Request Response**.

### Request Response

In the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools), we know that we can either publish messages to a specified topic or subscribe to a specified topic for receiving messages of interest. In the case of ensuring some people subscribed, a QoS which is greater than 0 can ensure messages are delivered to the subscriber [^1]. However, if we combine some business scenarios where not only need to deliver messages to the subscriber, and may need the subscriber to trigger some actions and return results, or need to request some information from the subscriber, the implementation under the publish-subscribe model is slightly cumbersome, and the two communication parties need to negotiate a request topic and a response topic in advance.

If the same request topic has lots of requestors, we need multiple different response topics for correctly return the response to the requestor. The most common method is inserting the field Client ID which can uniquely identify the requesting client at the head of Payload or elsewhere. The responder extracts these fields and the real Payload according to the pre-agreed rules and uses these fields for constructing a response topic.

![image20200901155125123.png](https://assets.emqx.com/images/b6f86c4ee3f7140bde66235cf65eb36a.png)

However, this is not a good implementation. We expect that the request recipient only needs to pay attention to how to process requests, without spending extra energy considering how to correctly return the response to the requestor. Therefore, MQTT 5.0 adds the new attribute **Response Topic**, and define the following request-response interaction process:

1. [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) (requestor) publish the request message including **Response Topic** to the request topic.
2. If there are other MQTT clients (responder) subscribe to the topic filter which matches the topic name used when request publishing messages, then the request message will be received.
3. The responder takes appropriate action according to the request message, then publish the response messages to the topic specified by this attribute **Response Topic**.

![image20200901155200573.png](https://assets.emqx.com/images/b1d14036452acced378d1e0c1d66188b.png)

#### Correlation data

Different from the HTTP request-response model, [MQTT](https://www.emqx.com/en/mqtt-guide) request-response is asynchronous, which brings a problem, that is how to associate the response message with the request message. The most commonly used method is to carry one characteristic field in the request message. The responder will intact return the received fields when they receive the response message. Obviously, MQTT also considers this, so we add a new attribute **Correlation Data** for the PUBLISH packet.

![image20200901154600805.png](https://assets.emqx.com/images/d624fb3a3061f043f32ae02338f635a0.png)

#### Response message

We have already mentioned above that there may be cases that multiple requestors initiate requests at the same time. To avoid the conflicts between different requestors, the response topic that the requestor client used should be unique to this client. Because the requestor and responder usually need to authorize these topics, use a randomized topic name will cause a challenge to authorize.

To solve this problem, MQTT 5.0 defines a new attribute called response message in the CONNACK packet. The server can use this attribute to guide the client on how to choose the response topic to use. This mechanism is optional for the server and client. When connecting, the client will request the server to send response messages through setting the request-response information attribute in the CONNECT packet. This will cause the server to insert the response information attribute in the CONNACK packet, and the requestor can use response information to construct the response topic.

![image20200901161153410.png](https://assets.emqx.com/images/e47ab01f85fa153f4ad57b49dd1d91ec.png)

### Recommendation for use

- Due to some limitations of the publish-subscribe model, using a QoS greater than 0 only can ensure that the message will reach the opposite end instead of the subscriber. If the subscription is not completed when publishing messages, the message will be lost, but the publisher is unaware of it. Therefore, for some messages with more strict delivery requirements, you can confirm whether the message reached the subscriber through requesting response.

- For some data reporting type of applications, when you feel like the reporting interval is set too long or too short to be appropriate, you can try setting it to actively request data through requesting response. However, it should be noted that if too many requesters cause the actual frequency of data reporting is highly greater than the original, the losses outweigh the gains, so you need to consider the actual scenario.

- If you have used the **Correlation Data** attribute correctly, you can use [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) for responders with confidence.
- Pay particular attention to cases that multiple responders subscribe to the same request topic and multiple requesters subscribe to the same response topic.

[^1]: When QoS is greater than 0, the publisher can ensure that messages are delivered to the server and the server retained message will be delivered to the subscriber.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT 5.0 service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
