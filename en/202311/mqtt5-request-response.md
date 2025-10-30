This article will delve into how to implement the **Request / Response** pattern under the asynchronous message delivery framework of [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), with the new features of [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5).

>*New to MQTT 5.0? Please check out our*
>
>[MQTT 5.0: 7 New Features and a Migration Checklist](https://www.emqx.com/en/blog/introduction-to-mqtt-5)


## Request / Response Before MQTT 5.0

The publisher-subscriber mechanism of MQTT completely decouples the sender and receiver of messages, allowing messages to be delivered asynchronously. However, this also brings a problem: even with QoS 1 and 2 messages, the publisher can only ensure that the message reaches the server, but cannot know whether the subscriber has ultimately received the message. When executing some requests or commands, the publisher may want to know the execution result of the other end.

The most direct way is to have the subscriber return a response of the request.

In MQTT, this is not difficult to implement. It only requires the two communicating parties to negotiate the request topic and response topic in advance, and then the subscriber returns a response to the response topic after receiving the request. This is also the method generally adopted by clients before MQTT 5.0.

In this scheme, the response topic must be determined in advance and cannot be flexibly changed. When there are multiple different requesters, since they can only subscribe to the same response topic, all requesters will receive the response, and **they cannot tell whether the response belongs to themselves**:

![request response before mqtt5](https://assets.emqx.com/images/d3f0f0f49cc4e5911f1b8f61580504a5.jpg)

<center>Multiple requesters can easily cause response confusion</center><br>

Although there are many ways to avoid this issue, it also leads to the possibility of completely different implementations among vendors, greatly increasing the difficulty and workload for users when integrating devices from different manufacturers.

To solve these problems, MQTT 5.0 introduced properties such as Response Topic, Correlation Data, and Response Information to standardize the **Request / Response** pattern in MQTT.

## How does MQTT 5.0 Request / Response work?

### Property 1 - Response Topic

In MQTT 5.0, the requester can specify an expected Response Topic in the request message. After taking appropriate action based on the request message, the responder publishes a response message to the Response Topic carried in the request. If the requester has subscribed to that Response Topic, it will receive the response.

![response topic](https://assets.emqx.com/images/92889c77ff810e13135d8be208e79ce5.jpg)

The requester can use its Client ID as part of the Response Topic, effectively avoiding conflicts caused by different requesters inadvertently using the same Response Topic.

### Property 2 - Correlation Data

The requester can also carry Correlation Data in the request, and the responder must return the Correlation Data intact in the response, allowing the requester to identify the original request to which the response belongs.

This can prevent the requester from incorrectly associating the response with the original request when the responder does not return responses in the order of requests, or when a response (QoS 0) is lost due to network disconnection.

On the other hand, the requester may need to interact with multiple responders, such as controlling various smart devices in the home via a mobile phone. The Correlation Data allows the requester to manage responses asynchronously returned from multiple responders by subscribing to a single Response Topic.

![correlation data](https://assets.emqx.com/images/4512c244552569dcaca4880db299a665.png)

In the above **Request / Response** process, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) does not change the Response Topic or Correlation Data, it only serves as a forwarding agent.

### Property 3 - Response Information

For security reasons, the MQTT server usually restricts the topics that clients can publish and subscribe to. The requester can specify a random Response Topic, but cannot guarantee that it has permission to subscribe to that topic, nor can it guarantee that the responder has permission to publish messages to that Response Topic.

Therefore, MQTT 5.0 also introduced the Response Information property. By setting the Request Response Information identifier to 1 in the CONNECT packet, the client can request the server to return Response Information in the CONNACK packet. The client can use the content of the Response Information as a specific part of the Response Topic, to pass the server's permission check.

![response information](https://assets.emqx.com/images/f6962b2403339ec5dbade5b6ca2ffc33.png)

MQTT does not further specify the details of this part, such as the content format of the Response Information and how the client creates the Response Topic based on the Response Information, so different server and client implementations may vary.

For example, the server could use the Response Information “FRONT,mytopic” to indicate both the specific content of a certain part of the Response Topic and its position within the Response Topic. It could also agree with the client on how to use this specific part in advance, then use the Response Information “mytopic” to indicate only the specific content of this part.

Taking a smart home scenario as an example, smart devices will not be used across users. We can let the MQTT server return the ID of the user to whom the device belongs as Response Information, and the client uniformly uses this user ID as the prefix of the Response Topic. The MQTT server only needs to ensure that these clients have the publication and subscription permissions for topics starting with this user ID during the lifecycle of their sessions.

## Suggestions for Using MQTT Request / Response

Here are some suggestions for using **Request / Response** in MQTT, following these will help you implement best practices:

1. QoS 1 and 2 in MQTT can only ensure that messages reach the server. If you want to confirm whether the message has reached the subscriber, you can use the **Request / Response** pattern.
2. Subscribe to the Response Topic before sending the request to avoid missing the response.
3. Ensure that the responder and the requester have the necessary permissions to publish and subscribe to the Response Topic. Response Information can help us build a Response Topic that meets permission requirements.
4. When there are multiple requesters, they need to use different Response Topics to avoid response confusion. Using Client ID as part of the topic is a common practice.
5. When there are multiple responders, it is best for the requester to set Correlation Data in the request to avoid response confusion.
6. We can make the Will Message work with the **Request / Response**. We just need to set the Response Topic for the Will Message when connecting. This can help the client know whether the Will Message has been consumed during its offline period, so it can make appropriate adjustments.

## Demo

Next, we will use [MQTTX](https://mqttx.app) to simulate the scenario of using a mobile phone to remotely control the bedroom light to turn on and receive the response.

Install and open MQTTX, first initiate a client connection to the [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simulate a mobile phone, and subscribe to the response topic `state/light-in-bedroom/power`:

![mqttx 01](https://assets.emqx.com/images/0d09b79ac901828f0737f3f3305c9be4.png)

Create a new client connection to simulate the smart light, and subscribe to the request topic `cmnd/light-in-bedroom/power`:

![mqttx 02](https://assets.emqx.com/images/27a86381a75f1d68b15ab64e2edc485d.png)

Return to the request client, and send a turn-on light command with the Response Topic to the request topic `cmnd/light-in-bedroom/power`:

![mqttx 03](https://assets.emqx.com/images/aaf3322398e3f919d1896bd1726bebeb.png)

In the response client, we can see that the received message carries the Response Topic. So next, we can perform the turn-on light operation according to the command request, and then return the latest status of the light through this Response Topic:

![mqttx 04](https://assets.emqx.com/images/978c9d24fc743c92a1d6cf5a75fff045.png)

Eventually, the request client will receive this response, and according to the content of the response message, we can know that the light has been successfully turned on:

![mqttx 05](https://assets.emqx.com/images/4be557386f9385f719f8145ef42b523c.png)

This is a very simple example, you can also try to increase the number of publishers or responders, to experience how to design the request and response topics in these cases.

In addition, we provide Python sample code for **Request / Response** in [emqx/MQTT-Features-Example](https://github.com/emqx/MQTT-Feature-Examples), you can use it as a reference.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
