[MQTT protocol](https://www.emqx.com/en/mqtt) specifies the quality of service, which guarantees the reliability of message delivery under different network environments. The design of QoS is the focus of the MQTT protocol. As a protocol specifically designed for IoT scenarios, MQTT's operating scenarios are not only for PC, but also in a wider range of narrow-bandwidth networks and low-power devices. If the problem of transmission quality can be solved at the protocol layer, it will provide a great convenience for the development of the Internet of things applications.


## MQTT QoS levels

MQTT has designed 3 QoS levels.

- *At most once* (0)
- *At least once* (1)
- *Exactly once* (2)

QoS 0 is a "fire and forget" message sending mode: After a sender (possibly Publisher or Broker) sends a message, it no longer cares whether it is sent to the other party or sets up any resending mechanism.

QoS 1 includes a simple resending mechanism. After the Sender sends a message, it waits for the receiver's ACK. If it does not receive the ACK, it resends the message. This mode can guarantee that the message can arrive at least once, but it cannot guarantee that the message is repeated.

QoS 2 designed a resending and repeating message discovery mechanism to ensure the message will arrive only once.


## Working principle

#### QoS 0 - Publish once at most

When QoS is 0, the publish of messages depends on the capabilities of the underlying network. The publisher will publish the message only once,  the receiver will not answer the message, and the publisher will not save and resend the message. Messages have the highest transmission efficiency at this level, but may not be delivered once. 

![MQTT_1.png](https://assets.emqx.com/images/8c6e4c6b37e76e23b84d3341a2ff9b33.png)

#### Qos 1 - Publish once at least

When the QoS is 1, the message can be guaranteed to be published at least once. MQTT guarantees QoS 1 through a simple ACK mechanism. The publisher will publish the message and wait for the response of the receiver's PUBACK packet. If the PUBACK response is not received within the specified time, the publisher will set the message's DUP to 1 and resend the message. The receiver should respond to the PUBACK message when receiving a message with QoS 1. The receiver may accept the same message multiple times. Regardless of the DUP flag, the receiver will treat the received message as a new message and send a PUBACK packet as a response.

![MQTT_2.png](https://assets.emqx.com/images/6777e0797f80ddaa1d623b173890f63c.png)

#### QoS 2 - Publish only once

When the QoS is 2, publishers and subscribers ensure that messages are published only once through two sessions. This is the highest level of service quality, and message loss and duplication are unacceptable. There is an additional cost to using this quality of service level.

After the publisher publishes a message with a QoS of 2, it will store the published message and wait for the receiver to reply with the PUBREC message. After the publisher receives the PUBREC message, it can safely discard the previously published message because it already knows the receiver successfully received the message. The publisher saves the PUBREC message and responds with a PUBREL, waiting for the receiver to reply with the PUBCOMP message. When the sender receives the PUBCOMP message, it will clear the previously saved state.

When the receiver receives a PUBLISH message with a QoS of 2, it processes the message and returns a PUBREC in response. When the receiver receives the PUBREL message, it discards all saved states and responds with PUBCOMP.

Whenever packet loss occurs during transmission, the sender is responsible for resending the previous message. This is true regardless of whether the sender is Publisher or Broker. Therefore, the receiver also needs to respond to each command message.

![MQTT_3.png](https://assets.emqx.com/images/9d1234bb84dc9a3e3c178c55732f8444.png)


## The difference of QoS in publishing and subscribing

QoS of MQTT publishing messages is not end-to-end, but between the client and the server. The QoS level at which subscribers receive MQTT messages ultimately depends on the QoS of the published message and the QoS of the topic subscription.

- When the QoS used by client A publish is greater than the QoS used by client B's subscription, the QoS of server forwarding messages to client B is the QoS used by client B's subscription.
- When the QoS used by client A publish is less than the QoS used by client B's subscription, the QoS of server forwarding messages to client B is the QoS used by client A's publishing.

You can refer the following table for the message QoS that the client received in different situations:

| QoS of publish | QoS of subscribe | QoS of received message |
| -------------- | ---------------- | ----------------------- |
| 0              | 0                | 0                       |
| 0              | 1                | 0                       |
| 0              | 2                | 0                       |
| 1              | 0                | 0                       |
| 1              | 1                | 1                       |
| 1              | 2                | 1                       |
| 2              | 0                | 0                       |
| 2              | 1                | 1                       |
| 2              | 2                | 2                       |


## How to choose QoS

The higher QoS level corresponds to more complicated processes and the greater the consumption of system resources. The application can choose the appropriate QoS level according to their network scenarios and business requirements.

#### QoS 0 can be chosen in the following cases

- It is accepted that messages are occasionally lost.
- In the scenario that the message interaction between the internal services in the same subnet, or the network of other client and server is very stable.

#### QoS 1 can be chosen in the following cases

- Focus on the consumption of system resources and wish optimized performance.
- Can not lose any message, but can accept and process duplicate messages.

#### QoS 2 can be chosen in the following cases

- It is unacceptable that lost message(the loss of message may result in loss of life or property), and do not want to receive duplicate messages.
- For some industries such as a bank, firefight, aviation, etc that require high completeness of data and timeliness.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
