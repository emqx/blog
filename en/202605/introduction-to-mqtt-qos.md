In a world of unpredictable networks, ensuring reliable data delivery is a major challenge for IoT applications. **MQTT's Quality of Service (QoS)** is a powerful mechanism designed to solve this problem, offering a sliding scale of reliability to match the specific needs of your project.

This guide will break down **MQTT QoS levels 0, 1, and 2**, compare their performance, and provide practical use cases to help you choose the right level for your IoT solution.

## What is QoS in MQTT?

QoS in [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) defines the level of guarantee for a message to be delivered from a publisher to a subscriber. It's not about the network transport itself but a set of rules that sit on top of the TCP connection. There are three primary levels:

- **QoS 0**: **"At most once"**. This is a fire-and-forget approach, where the message is sent but no confirmation is expected.
- **QoS 1**: **"At least once"**. The sender guarantees delivery but acknowledges that duplicate messages might occur.
- **QoS 2**: **"Exactly once"**. This is the highest level of reliability, ensuring no messages are lost or duplicated.

As you move from QoS 0 to QoS 2, the reliability increases, but so does the complexity and overhead of the message exchange.

![MQTT QoS Downgrade](https://assets.emqx.com/images/6a5e702f5621af6974e0785b1bbbdb43.png)

## MQTT QoS Levels Explained

### MQTT QoS 0 - At Most Once

**How it works:** The sender publishes a message and immediately forgets about it. There's no acknowledgment from the receiver, and no retransmission. The reliability of QoS 0 depends entirely on the stability of the underlying TCP connection. If the connection drops, any message in transit or waiting in a buffer will be lost.

**Pros:**

- **Highest performance and lowest overhead:** Requires only a single message transmission.
- **Fastest delivery:** No waiting for acknowledgments.

**Cons:**

- **No guarantee of delivery:** Messages can be lost if the network is unreliable.
- **No deduplication:** The receiver must handle any potential message loss.

**Use cases:** Ideal for high-frequency, non-critical data where losing a message is acceptable. Think of periodic sensor readings like temperature, humidity, or a one-time status update where the next message will quickly replace the lost one.

![MQTT QoS 0](https://assets.emqx.com/images/2c36da33012fac0e6943c7f6f8b5aa7f.png)

### MQTT QoS 1 - At Least Once

**How it works:** This level introduces a handshake to ensure delivery. The sender sends a `PUBLISH` message and stores a copy. It waits for a `PUBACK` packet from the receiver. If the sender doesn't receive the `PUBACK` within a set time, it retransmits the message with the `DUP` flag set. The receiver must acknowledge every message it gets.

**Pros:**

- **Guaranteed delivery:** Messages will eventually reach their destination.
- **Lower overhead than QoS 2:** Simpler handshake process.

**Cons:**

- **Potential for duplicate messages:** This is an inherent risk of the protocol.
- **Higher overhead than QoS 0:** Requires an additional `PUBACK` packet.

**Use cases:** Suitable for important data where some duplication is acceptable. Examples include device control commands (e.g., turning a light on) or financial transaction updates. To handle duplicates at the application level, you can include a unique message ID or a timestamp in the message payload.

![MQTT QoS 1](https://assets.emqx.com/images/5affbdf88707c5596e0fc5d16045b4ac.png)

**Why Does MQTT QoS 1 Cause Duplicate Messages?**

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

### MQTT QoS 2 - Exactly Once

**How it works:** This is a robust, four-step handshake process that guarantees a message is delivered exactly once. The sender and receiver work together to ensure they are on the same page, eliminating the duplication issue seen in QoS 1.

1. **Publish:** Sender sends `PUBLISH` and waits for `PUBREC`.
2. **Received:** Receiver sends `PUBREC` to acknowledge receipt and awaits the next step.
3. **Release:** Sender sends `PUBREL`, signaling it has received the `PUBREC` and is ready to complete the transaction.
4. **Complete:** Receiver sends `PUBCOMP`, confirming the message is fully processed.

**Pros:**

- **Highest reliability:** Guarantees no message loss or duplication.
- **Ideal for mission-critical applications:** Perfect for data where every single message counts.

**Cons:**

- **Highest overhead:** Requires a total of four packets for each message.
- **Slowest delivery:** The complex handshake adds latency.

**Use cases:** This level is reserved for critical, one-time data that must not be lost or duplicated. Examples include financial transactions, medical device readings, or critical security alerts.

![MQTT QoS 2](https://assets.emqx.com/images/7a29e2c1e65bb68b10f596e10f60be35.png)

**Why Are QoS 2 Messages Not Duplicated?**

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

## FAQ & Performance Considerations

### How do you deduplicate MQTT QoS 1 messages?

As duplication is inherent at the protocol level for QoS 1, you must solve this at the application layer. One common method is to include a **timestamp** or a **monotonically increasing count** in the message payload. This allows your application to check if it has already processed a message with the same timestamp or count, effectively discarding any duplicates.

### Is there a performance difference between MQTT QoS levels?

Yes. **QoS 0** and **QoS 1** typically have similar throughput, but QoS 1 requires more CPU and can have slightly higher latency under high load due to the handshake process. On the other hand, **QoS 2** usually has about half the throughput of QoS 0 and 1 because of the additional packets required for each message. **Your choice of QoS is a trade-off between speed and reliability.**

### Can a MQTT broker downgrade a message's QoS?

Yes. When a publisher sends a message with a specific QoS level, the broker typically forwards it to subscribers at that same level. However, a subscriber can specify a maximum QoS level they are willing to receive. If the publisher's QoS is higher than the subscriber's requested level, the broker will **downgrade** the message to match the subscriber's requirement. For example, a QoS 2 message would be downgraded to QoS 1 if the subscriber requested a maximum QoS of 1.

### Is MQTT QoS end-to-end?

Not exactly. MQTT QoS applies to each message delivery hop. A publisher sends a message to the broker with one QoS level, and the broker forwards the message to each subscriber based on the subscriber's requested QoS. This means the effective QoS received by a subscriber may be different from the QoS used by the publisher.

### What is the default QoS in MQTT?

In most MQTT clients and libraries, the default QoS is usually QoS 0 unless another level is explicitly specified. QoS 0 has the lowest overhead, but it does not provide delivery confirmation or retransmission.

### Does MQTT QoS guarantee message ordering?

MQTT QoS controls delivery reliability, not global ordering across all publishers and subscribers. Message ordering depends on factors such as client session, topic, broker behavior, inflight messages, and whether messages come from the same or different publishers. If strict ordering is required, applications should use sequence numbers and carefully design topic and client flows.

### Can I use different QoS levels in the same MQTT application?

Yes. In fact, many production IoT systems use different QoS levels for different message types. For example, a device may publish frequent sensor readings with QoS 0, important status changes with QoS 1, and critical control or billing-related events with QoS 2.

### Is QoS 2 always better than QoS 1?

No. QoS 2 provides a stronger delivery guarantee, but it also requires more packet exchanges and adds more latency. For most IoT applications, QoS 1 is often the better default choice because it ensures delivery while keeping protocol overhead lower than QoS 2.

## Conclusion

Understanding **MQTT QoS** is crucial for building a reliable and efficient IoT system.

- Use **QoS 0** for non-critical, high-frequency data where speed is paramount.
- Choose **QoS 1** for important data that must be delivered, but where the occasional duplicate can be handled at the application level.
- Select **QoS 2** for mission-critical data that cannot be lost or duplicated, and where you can accept the higher overhead.

Choosing the optimal **MQTT QoS level** is a fundamental architectural decision for any enterprise **IoT data infrastructure**. Balancing message delivery guarantees against network overhead ensures your applications remain responsive, scalable, and resilient even under degraded network conditions.

For deeper technical deep-dives into broker implementation, explore the [**EMQ comprehensive MQTT protocol guides**](https://www.emqx.com/en/mqtt-guide), which cover core protocol mechanisms including [MQTT wildcards](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics#mqtt-topic-wildcards), [retained messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message), and session persistence configurations to build enterprise-grade, scalable IoT data infrastructure.
