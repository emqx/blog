Today, [OASIS Open](https://www.oasis-open.org) and EMQ jointly announced that [EMQ](https://www.emqx.com/en) is now the newest Foundational Member of OASIS that helps fulfill its mission at the highest level, to advance the development and adoption of open standards together.

OASIS Open is one of the most respected, nonprofit international open source and standards consortiums. EMQ, as the leading provider of open-source IoT data infrastructure, joined OASIS in 2020 to help advance the OASIS standard for the MQTT Protocol, the most commonly used messaging protocol for IoT.

“Since joined OASIS, EMQ has been leading the cutting edge research using MQTT over QUIC and aiming to standardize it with the MQTT Technical Committee. All these years we saw how they devoted into and contributed to open-source and the IoT industry, as well as their commitment to MQTT and advancing open standards,” said **OASIS Open Executive Director Guy Martin**.

## Pioneering Participant in MQTT and the IoT Messaging

EMQ has been working on [EMQX](https://www.emqx.io/), the open source distributed MQTT broker which is fully compatible with MQTT 3.1 and 3.1.1 specifications since 2013. Then when MQTT became an OASIS open standard in 2016, we actively engaged in the development and discussion of the MQTT 5.0 specification. It’s EMQX that innovatively introduced the [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) features back when the specification was still in draft form.

One of the most game-changing releases so far came in 2020 when EMQ introduced EMQX 4.0, the world's first cloud-native MQTT 5.0 Server with the full latest specification support. Now EMQX has become the world's most popular cloud-native distributed MQTT broker with a high-performance real-time message processing engine, connecting more than 100 million IoT devices worldwide for IoT data movement, processing and analytics.

Meanwhile, edge computing is now seeing explosive growth, yet due to the highly constrained embedded hardware resources and the fragmented edge bus protocols ecosystem, it is challenging to implement the essential high-performance message bus at the edge. In 2021, EMQ created [NanoMQ](https://nanomq.io), a lightweight MQTT messaging engine and multi-protocol message bus. It’s designed to tackle the challenge of edge data convergence, collaboration, bridging, and re-distribution in a portable, scalable and time-space efficient manner.

EMQ is also actively contributing to the open-source IoT world by introducing several popular MQTT SDKs:

- [CocoaMQTT](https://github.com/emqx/CocoaMQTT), an MQTT 5.0 and 3.1.1 client SDK for iOS/OS X/tvOS written in Swift 5, the world’s first iOS MQTT 5.0 client for the Apple developer ecosystem
- [emqtt](https://github.com/emqx/emqtt), an MQTT client library and command-line tools written in Erlang that supports MQTT 5.0, 3.1.1 and 3.1
- [NanoSDK](https://github.com/nanomq/NanoSDK), a high-performance, non-blocking MQTT 3.1.1 C SDK with full asynchronous I/O under the hood. It has a significant throughput advantage on QoS 1/2 message
- [qmqtt](https://github.com/emqx/qmqtt), an MQTT 3.1.1 C++ SDK, which is easy to use with the QT framework

## Relentless in Contributing to MQTT in the Future

In the past ten years, EMQ has witnessed and participated in the development of the IoT industry worldwide. In the coming years, EMQ will continue to firmly commit to open source, MQTT and IoT industry by relentlessly contributing to MQTT specifications and MQTT server development.

### MQTT over QUIC

At EMQ, we believe QUIC as the future transport protocol will be a huge value add if combined with MQTT. Since early 2021, EMQX team have been experimenting with MQTT over QUIC as a single stream connection (like a TCP connection). Believing in the benefits that some of the great features of QUIC will bring to MQTT, together with OASIS MQTT-TC, EMQX team will keep devoting into the state-of-the-art work of MQTT over QUIC and bring some of our ideas to the MQTT standards.

### Standardize Shared Subscription Dispatch Strategy

EMQX has a pretty unique configuration-based implementation of shared subscription dispatch strategy. The supported policies are random, round-robin, hash, and sticky. We believe this can be standardized in MQTT specification, so the clients can choose in which ways they will receive the messages instead of relying on the broker’s implementation or configuration.

### MQTT Streams

So far, MQTT is a message broking protocol, once a message is delivered, it‘s deleted from the server. To meet the replay (time-travel) requirements, people usually turn to other streaming platforms such as Apache Kafka and Apache Pulsar. It will be a great advantage if the MQTT clients are able to request messages from any specific point in a stream to replay messages (time-travel).

Although MQTT 5.0’s user-properties can be used to implement your sub-protocols between a broker vendor and client implementations, it would be great if it's standardized in the MQTT specification, and that’s what EMQ will work on in 2022.

### MQTT Server Development

In 2022, EMQ will continue to drive forward in MQTT server development, including:

- Keeping working on the most highly scalable MQTT-based IoT messaging platform EMQX. It has now reached stunning 100 million unique subscribers in a 22-nodes EMQX cluster, and we’ll go further beyond
- Supporting highly available persistent sessions
- Delivering advanced NanoMQ, it will provide more abundant messaging patterns and other powerful features such as message persistence and rule-engine, and will facilitate MQTT application at the edge
- Making the [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) gateway software Neuron open source.

 

"We are excited to be a foundational member of OASIS and to participate in the MQTT TC. We hope that the innovations EMQ has made to the MQTT server, including MQTT over QUIC, and MQTT Streaming, will become part of the MQTT open standards in the future,” said **Feng Lee, CEO at EMQ**. “We look forward to working closely with OASIS to further drive the application of MQTT in the IoT industry and scenarios, to power the future-proof IoT solutions and enterprise digital transformation."
