
## Overview

The MQTT 5.0 protocol has made some upgrades for part of QoS packet, and the processes of dealing with packets, this article below display some simple introduction about the content of upgrades. 

## The packet format and process of processing of QoS

In the MQTT 5.0 protocol, the message will be divided into three levels (QoS0, QoS1, QoS2) respectively. The values of these three different QoS represent different levels of service quality.

0：The message will be sent once only. If the level of messages is QoS 0, the publisher only sends messages once when publishing the message. 
Regardless of  whether the message was sent successfully or not ;

1：The message will be sent once at least. If the level of messages is QoS 1, the publisher will send the message repeatedly when publishing the message to ensure that the message has been sent successfully;

2：The message will be sent once only and confirmed that message sending successfully. If the level of messages is QoS 2, when publishing the message, the publisher will ensure that the receiver only receives one message, and will not send the message repeatedly.

QoS 0 saves the most computer resource among three QoS message levels, while QoS 1 still needs to receive one sending successful packet after sending messages, to stop sending repeated packets. The transmission of the QoS 2 message needs more steps, which needs sending the packet four times to ensure the message is sent in a single pass, and consumes the most computer resource and bandwidth.

The following flow charts are about the process of three different values of QoS ：

In the MQTT 3.0, the process of publishing the QoS 0 message is :

- **QoS 0 message** 

  | sender                   | the flow direction of controlling packet | recipient                                         |
  | ------------------------ | ----------------------------------------------- | ------------------------------------------------- |
  | PUBLISH QoS = 0, DUP = 0 |                                                 |                                                   |
  |                          | —>                                              |                                                   |
  |                          |                                                 | receive messages(may not be received) and process |

  


- **QoS 1 message**  

  | sender                                    | the flow direction of controlling packet | recipient                                       |
  | ----------------------------------------- | ---------------------------------------- | ----------------------------------------------- |
  | store messages                            |                                          |                                                 |
  | send PUBLISH QoS1, DUP = 0, with Packetld | —>                                       |                                                 |
  |                                           |                                          | receive message and process                     |
  |                                           |                                          | send confirmed message with Packetld and PUBACK |
  | discard messages                          |                                          |                                                 |

  If the recipient does not receive the QoS 1 message or receive the wrong QoS 1 message, the recipient does not reply PUBACK packet to the sender. Therefore, the sender will send the QoS 1 message again rather than discard, and the QoS 1 message may be published repeatedly. 



- **QoS 2 message**

  | sender                                                       | the flow direction of controlling packet | recipient                                                |
  | ------------------------------------------------------------ | ---------------------------------------- | -------------------------------------------------------- |
  | store messages                                               |                                          |                                                          |
  | send PUBLISH QoS1, DUP = 0, with Packetld                    |                                          |                                                          |
  |                                                              | —>                                       |                                                          |
  |                                                              |                                          | store Packet ID and prepare sending application messages |
  |                                                              |                                          | publish PUBREC packet with Packetld and Reason Code      |
  |                                                              | <---                                     |                                                          |
  | discard stored messages, store received PUBREC packet with the same packet ID |                                          |                                                          |
  | send PUBREC packet                                           | —>                                       | discard Packetld                                         |
  |                                                              |                                          | send PUBCOMP PACKET with Packetld                        |
  |                                                              | <---                                     |                                                          |
  | discard stored status                                        |                                          |                                                          |

To ensure the message being sent successfully in a single pass. At first, the publisher needs to publish a PUBLISH packet, the recipient will store received messages after receiving the PUBLISH packet, and then will return the PUBREC packet to the sender. The sender will replace the stored PUBLISH packet into received the PUBREC packet after receiving a PUBREC packet, and then send the PUBREL packet to the recipient. The recipient will discard the previous stored status after receiving PUBREL message. At this time the recipient already received the message, and can ensure that the message reached once only.

The MQTT protocol faced with embedded devices with low ability of computing. Although the MQTT 5.0 protocol has made some slight upgrades in the process of messages, using the QoS 2 message to communicate still consumes a lot of resources. Therefore, if the client's demand for the information transmission priority is not extremely high, please not trying to transmit the QoS 2 message.

## MQTT 5.0 update

The update of QoS in the MQTT 5.0 mainly reflected in when QoS 2 recipients processing messages.

* In the MQTT 5.0 protocol, the process of processing of publishing the QoS 2 message is slightly different from the MQTT3.0 protocol. In the MQTT3.0 protocol, the recipient can store information and Packet Id after receiving the QoS 2 message, while the protocol implementer only can store Packet Id in the 5.0 protocol. This behavior is to force MQTT protocol developers to reduce the consumption of QoS 2 message bandwidth.

- In the QoS 2 receiver, it will return the previous Packet Id and the PUBERC message with the tag Reason Code. 

The [EMQ X MQTT broker](https://www.emqx.com/en/products/emqx) v3.0 already includes support for the MQTT 5.0 protocol, welcome to use.

