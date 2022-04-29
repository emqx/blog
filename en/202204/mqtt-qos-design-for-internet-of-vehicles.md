Previously, we have introduced the construction of the IoV MQTT messaging platform and how to design the topic of IoV messaging based on actual business requirements. Next, we need to consider how to transfer message data securely with high quality. In this article, we will introduce the QoS design of MQTT messages in the IoV scenario, which guarantees the quality of data transmission.

## Preface

Massive data will be generated in an IoV scenario, which can be used as the basis for vehicle diagnosis to ensure the safe and stable operation of the vehicle. In addition, the data can also be linked with infrastructures such as mobile phones to provide a better driving experience. Many relevant policy documents put forward higher requirements for data transmission of IoV. The security, stability and reliability of communication has always been a constant topic of IoV, so a set of sound data transmission guarantee scheme is also an important part of IoV business.

## QoS Level of MQTT Protocol

As the first choice of data communication protocol in the IoV industry, the MQTT protocol specifies Quality of Service (QoS) that guarantees the reliability of message transmission in different network environments. This serves as the primary implementation technology for message reliability transmission in IoV scenarios.

The MQTT has three QoS levels:

- **QoS 0**

  A message is delivered at most once and will be lost if the client is unavailable at the time. Once Sender (either Publisher or Broker) sends a message, it no longer cares if it is sent to the other party, nor does it set up any re-transmission mechanism.

  ![MQTT QoS 0](https://static.emqx.net/images/fb046bde08b7cd1e653d3eaacde480fc.png)

- **QoS 1**

  The message is delivered at least once. A simple re-transmission mechanism is included: Sender waits for the receiver's ACK after sending the message, which can be re-transmitted if the ACK is not received. This mode guarantees that the message will arrive at least once, but it does not guarantee that the message will be repeated or not.

  ![MQTT QoS 1](https://static.emqx.net/images/8a707edb6b019f4c62e5e25fa3345030.png)

- **QoS 2**

  The message is delivered only once. The mechanism of re-transmission and repeated message discovery mechanism is designed to ensure that the message reaches the subscriber and only once.

  ![MQTT QoS 2](https://static.emqx.net/images/752c86832c5328c428120a81596ee388.png)

## QoS Design Message in IoV Scenarios

At first, it needs to be understood that the higher the QoS level is, the more complex the message interaction will be, and the greater the system resource consumption will be. In other words, a higher QoS level is not necessarily the best for a given scenario. The application can select the appropriate QoS level according to the required network and service requirements.

According to the attributes and characteristics of data in IoV, we can divide it into six categories: basic attribute data, vehicle industrial control data, environment perception data, vehicle control data, application service data and user personal information. How to choose the most appropriate MQTT QoS level in different IoV scenarios?

- **QoS 0**

  QoS 0 can be chosen in scenarios where occasional message loss is acceptable.  For example, entertainment-related multimedia services such as weather forecasts and other data provided by the IoV.  Some vehicle-related service data, such as the report of vehicle historical driving data and historical driving operation data, could also be appropriate for QoS 0.

- **QoS 1**

  QoS 1 is used in most IoV scenarios.  This balances the optimization of system resource performance, message real-time and reliability.

  QoS 1 is widely used in vehicle control messages, traffic reporting data (including new energy national standard and enterprise standard), traffic safety control data, and early warning data related to traffic safety and road safety.

- **QoS 2**

  QoS 2 can be chosen for scenarios where message loss cannot be tolerated, repeated messages are not expected, and data integrity and timeliness are important.

  There are few applications of QoS 2 in IoV scenarios. Although it can increase message reliability, it also increases resource consumption and message delay significantly. QoS 2 is mainly used in banking, firefighting, aviation and other industries that require high data integrity and timeliness. Certain original equipment manufacturers will choose QoS 2 for traffic warnings and billing messages of vehicle charging piles.



**Special Reminders**

It should be noted that the QoS in the MQTT publishing operation and the subscription operation represent different meanings. The QoS in publication represents the QoS level used for messages sent to the MQTT Broker, and the QoS in subscription represents the maximum QoS level that the MQTT Broker can use when forwarding the message to the subscriber. It is necessary to guarantee that the sending QoS is consistent with that of the subscription, so to ensure that the received message has the intended QoS level, otherwise consumption degradation will occur. For example, if the QoS of the message sent by A is 2 and that of the message subscribed by B is 1, the QoS of the received message will be 1.

## EMQX Message Transmission Guarantee Based on QoS Level

In order to better guarantee the safety and reliability of data transmission between human to vehicle to road to the cloud in IoV, the cloud-native distributed IoT message broker [EMQX](https://www.emqx.com/en/products/emqx) has certain features such as inflight window, message queue, full-link message tracking and offline message storage.  This improves message reliability and also the efficiency of message throughput, which reduces the impact of network fluctuation.

The inflight window may be designed to allow multiple unacknowledged QoS 1 and QoS 2 packets to exist simultaneously on the network.  The message queue may need to store the message further when the message in the message queue exceeds the inflight window.  This can meet the storage requirement of the unreceived message or the unacknowledged data message when the client is offline. The inflight window also has the upgrade_qos parameter to implement features such as mandatory upgrade of QoS according to subscription, achieving consistency of QoS level that helps to ensure that consumption degradation will not occur. In addition, EMQX can also provide the capability of restricting service access by region to realize different QoS levels, data bridging QoS management, and QoS management of MQTT-SN protocol, which provide a strong guarantee for reliable transmission of messages in an IoV scenario.

## Conclusion

In this article, we have shown that the QoS characteristics of MQTT protocol are very important for the secure transmission of message data in an IoV scenario. As a cloud native, distributed message broker that fully supports the MQTT standard protocol, EMQX makes full use of the advantages of the MQTT protocol in product design to provide reliable data connection, movement, processing and integration for IoT platform and applications.


## Other articles in this series

- [IoV beginner to master 01｜MQTT in an IoV scenario](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles)

- [IoV beginner to master 02｜Architecture Design of MQTT Message Platform for Ten-million-level IoV](https://www.emqx.com/en/blog/mqtt-messaging-platform-for-internet-of-vehicles)

- [IoV beginner to master 03｜MQTT topic design in TSP platform scenario](https://www.emqx.com/en/blog/mqtt-topic-design-for-internet-of-vehicles)
