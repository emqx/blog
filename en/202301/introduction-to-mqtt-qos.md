## What is QoS

In unstable network environments, MQTT devices may struggle to ensure reliable communication using only the TCP transport protocol. To address this issue, MQTT includes a Quality of Service (QoS) mechanism that offers various message interaction options to provide different levels of service, catering to the user's specific requirements for reliable message delivery in different scenarios.

There are 3 QoS levels in MQTT:

- QoS 0, at most once.
- QoS 1, at least once.
- QoS 2, exactly once.

These levels correspond to increasing levels of reliability for message delivery. QoS 0 may lose messages, QoS 1 guarantees the message delivery but potentially exists duplicate messages, and QoS 2 ensures that messages are delivered exactly once without duplication. As the QoS level increases, the reliability of message delivery also increases, but so does the complexity of the transmission process.

In the publisher-to-subscriber delivery process, the publisher specifies the QoS level of a message in the PUBLISH packet. The broker typically forwards the message to the subscriber with the same QoS level. However, in some cases, the subscriber's requirements may necessitate a reduction in the QoS level of the forwarded message.

For example, if a subscriber specifies that they only want to receive messages with a QoS level of 1 or lower, the broker will downgrade any QoS 2 messages to QoS 1 before forwarding them to this subscriber. Messages with QoS 0 and QoS 1 will be transmitted to the subscriber with their original QoS levels unchanged.

![MQTT QoS Downgrade](https://assets.emqx.com/images/6a5e702f5621af6974e0785b1bbbdb43.png)

Let's see how QoS works.

## QoS 0 - At Most Once

QoS 0 is the lowest level of service and is also known as "fire and forget". In this mode, the sender does not wait for acknowledgement or store and retransmit the message, so the receiver does not need to worry about receiving duplicate messages.

![MQTT QoS 0](https://assets.emqx.com/images/2c36da33012fac0e6943c7f6f8b5aa7f.png)

### Why Are QoS 0 Messages Lost?

The reliability of QoS 0 message transmission depends on the stability of the TCP connection. If the connection is stable, TCP can ensure the successful delivery of messages. However, if the connection is closed or reset, there is a risk that messages in transit or messages in the operating system buffer may be lost, resulting in the unsuccessful delivery of QoS 0 messages.

## QoS 1 - At Least Once

To ensure message delivery, QoS 1 introduces an acknowledgement and retransmission mechanism. When the sender receives a PUBACK packet from the receiver, it considers the message delivered successfully. Until then, the sender must store the PUBLISH packet for potential retransmission.

The sender uses the Packet ID in each packet to match the PUBLISH packet with the corresponding PUBACK packet. This allows the sender to identify and delete the correct PUBLISH packet from its cache.

![MQTT QoS 1](https://assets.emqx.com/images/5affbdf88707c5596e0fc5d16045b4ac.png)

### Why Are QoS 1 Messages Duplicated?

There are two cases in which the sender will not receive a PUBACK packet.

1. The PUBLISH packet did not reach the receiver.
2. The PUBLISH packet reached the receiver but the receiver's PUBACK packet has not yet been received by the sender.

In the first case, the sender will retransmit the PUBLISH packet, but the receiver will only receive the message once.

In the second case, the sender will retransmit the PUBLISH packet and the receiver will receive it again, resulting in a duplicate message.

![MQTT QoS 1 duplicated](https://assets.emqx.com/images/9ca3130db4fdcadf1ca2a6fe75240eb0.png)

Even though the DUP flag in the retransmitted PUBLISH packet is set to 1 to indicate that it is a duplicate message, the receiver cannot assume that it has already received the message and must still treat it as a new message.

It is because that there are two possible scenarios when the receiver receives a PUBLISH packet with a DUP flag of 1:

![MQTT QoS 1 DUP](https://assets.emqx.com/images/72015dc94b030ba7f8b9ed6af7300881.png)

In the first case, the sender retransmits the PUBLISH packet because it did not receive a PUBACK packet. The receiver receives two PUBLISH packets with the same Packet ID and the second PUBLISH packet has a DUP flag of 1. The second packet is indeed a duplicate message.

In the second case, the original PUBLISH packet was delivered successfully. Then, this Packet ID is used for a new, unrelated message. But this new message was not successfully delivered to the peer the first time it was sent, so it was retransmitted. Finally, the retransmitted PUBLISH packet will have the same Packet ID and a DUP flag of 1, but it is a new message.

Since it is not possible to distinguish between these two cases, the receiver must treat all PUBLISH packets with a DUP flag of 1 as new messages. This means that it is inevitable for there to be duplicate messages at the protocol level when using QoS 1.

In rare cases, the broker may receive duplicate PUBLISH packets from the publisher and, during the process of forwarding them to the subscriber, retransmit them again. This can result in the subscriber receiving additional duplicate messages.

For example, although the publisher only sends one message, the receiver may eventually receive three identical messages.

![MQTT QoS 1 duplicated](https://assets.emqx.com/images/576568b549516c44969bcb12f442ed19.png)

These are the drawbacks of using QoS 1.

## QoS 2 - Exactly Once

QoS 2 ensures that messages are not lost or duplicated, unlike in QoS 0 and 1. However, it also has the most complex interactions and the highest overhead, as it requires at least two request/response flows between the sender and receiver for each message delivery.

![MQTT QoS 2](https://assets.emqx.com/images/7a29e2c1e65bb68b10f596e10f60be35.png)

1. To initiate a QoS 2 message transmission, the sender first stores and sends a PUBLISH packet with QoS 2 and then waits for a PUBREC response packet from the receiver. This process is similar to QoS 1, with the exception that the response packet is PUBREC instead of PUBACK.
2. Upon receiving a PUBREC packet, the sender can confirm that the PUBLISH packet was received by the receiver and can delete its locally stored copy. It **no longer needs and cannot retransmit** this packet. The sender then sends a PUBREL packet to inform the receiver that it is ready to release the Packet ID. Like the PUBLISH packet, the PUBREL packet needs to be reliably delivered to the receiver, so it is stored for potential retransmission and a response packet is required.
3. When the receiver receives the PUBREL packet, it can confirm that no additional retransmitted PUBLISH packets will be received in this transmission flow. As a result, the receiver responds with a PUBCOMP packet to signal that it is prepared to reuse the current Packet ID for a new message.
4. When the sender receives the PUBCOMP packet, the QoS 2 flow is complete. The sender can then send a new message with the current Packet ID, which the receiver will treat as a new message.

### Why Are QoS 2 Messages Not Duplicated?

The mechanisms used to ensure that QoS 2 messages are not lost are the same as those used for QoS 1, so they will not be discussed again here.

Compared with QoS 1, QoS 2 ensures that messages are not duplicated by adding a new process involving the PUBREL and PUBCOMP packets.

Before we go any further, let's quickly review the reasons why QoS 1 cannot avoid message duplication.

When we use QoS 1, for the receiver, the Packet ID becomes available again after the PUBACK packet is sent, regardless of whether the response has reached the sender. This means that the receiver cannot determine whether the PUBLISH packet it receives later, with the same Packet ID, is a retransmission from the sender due to not receiving the PUBACK response, or if the sender has reused the Packet ID to send a new message after receiving the PUBACK response. This is why QoS 1 cannot avoid message duplication.

![MQTT PUBACK](https://assets.emqx.com/images/fe56d9ac55db01422077f9b311aae302.png)

In QoS 2, the sender and receiver use the PUBREL and PUBCOMP packets to synchronize the release of Packet IDs, ensuring that there is a consensus on whether the sender is retransmitting a message or sending a new one. This is the key to avoiding the issue of duplicate messages that can occur in QoS 1.

![MQTT PUBREL and PUBCOMP](https://assets.emqx.com/images/cc67a5f9b3c583019aecf920e0cfd0ca.png)

In QoS 2, the sender is permitted to retransmit the PUBLISH packet before receiving the PUBREC packet from the receiver. Once the sender receives the PUBREC and sends a PUBREL packet, it enters the Packet ID release process. The sender cannot retransmit the PUBLISH packet or send a new message with the current Packet ID until it receives a PUBCOMP packet from the receiver.

![MQTT PUBREC](https://assets.emqx.com/images/74c4210e7750c0bbda1d771bb2775c32.png)

As a result, the receiver can use the PUBREL packet as a boundary and consider any PUBLISH packet that arrives before it as a duplicate and any PUBLISH packet that arrives after it as new. This allows us to avoid message duplication at the protocol level when using QoS 2.

## Scenarios and Considerations

### QoS 0

The main disadvantage of QoS 0 is that messages may be lost, depending on the network conditions. This means that you may miss messages if you are disconnected. However, the advantage of QoS 0 is that it is more efficient for message delivery.

Therefore, it is often used to send high-frequency, less important data, such as periodic sensor updates, where it is acceptable to miss a few updates.

### QoS 1

QoS 1 ensures that messages are delivered at least once, but it can result in duplicate messages. This makes it suitable for transmitting important data such as critical instructions or real-time updates of important status. However, it is important to consider how to handle or allow for such duplication before deciding to use QoS 1 without de-duplication.

For instance, if the publisher sends messages in the order 1, 2, but the subscriber receives them in the order 1, 2, 1, 2, with 1 representing a command to turn a light on and 2 representing a command to turn it off, it may not be desirable for the light to repeatedly turn on and off due to duplicate messages. 

![MQTT QoS](https://assets.emqx.com/images/3ab6255134132b2edb019056ccb74f00.png)

### QoS 2

QoS 2 ensures that messages are not lost or duplicated. However, it also has the highest overhead. If users are not willing to handle message duplication by themself and can accept the additional overhead of QoS 2, then it is a suitable choice. QoS 2 is often used in industries such as finance and aviation where it is critical to ensure reliable message delivery and avoid duplication.

## Q&A

### How to de-duplicate QoS 1 messages?

As duplication of QoS 1 messages is inherent at the protocol level, so we can only solve this problem at the business level .

One way to de-duplicate QoS 1 messages is to include a timestamp or a monotonically increasing count in the payload of each PUBLISH packet. This allows you to determine whether the current message is new by comparing its timestamp or count with that of the last received message.

### When should QoS 2 messages be forwarded to subscribers?

As we have learned, QoS 2 has a high overhead. To avoid impacting the real-time nature of QoS 2 messages, it is best to initiate the process of forwarding them to subscribers when the QoS 2 PUBLISH packet is received for the first time. However, once this process has been initiated, subsequent PUBLISH packets that arrive before the PUBREL packet should not be forwarded again to prevent message duplication.

### Is there a difference in performance between QoS?

QoS 0 and QoS 1 typically have similar throughput when using EMQX with the same hardware configuration for peer-to-peer communication, but QoS 1 may have higher CPU usage. Additionally, under high load, QoS 1 has longer message latency compared to QoS 0. On the other hand, QoS 2 usually only has about half the throughput of QoS 0 and 1.

## Conclusion

By now, you should have a thorough understanding of MQTT QoS. To continue learning about MQTT, you can check out EMQ's [MQTT Getting Started and Advanced](https://www.emqx.com/en/mqtt-guide) series, which cover topics such as wildcards, retained messages, and will messages. These resources will help you delve deeper into MQTT and develop advanced MQTT applications and services.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
