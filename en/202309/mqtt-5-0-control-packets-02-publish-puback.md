Welcome to the second article of the [MQTT 5.0 Packet Series](https://www.emqx.com/en/blog/Introduction-to-mqtt-control-packets). In the previous article, we introduced the [CONNECT and CONNACK packets](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-01-connect-connack) of MQTT 5.0. Now, we will introduce the PUBLISH packet used to deliver application messages in MQTT, and its response packets.

Whether it's the client publishing messages to the server, or the server forwarding messages to the subscriber, the PUBLISH packet is needed. The topic that determines the direction of the message, the actual content of the message, and the QoS level, are all included in the PUBLISH packet.

In the process of message delivery between the client and server, in addition to the PUBLISH packet, there are also four packets: PUBACK, PUBREC, PUBREL, and PUBCOMP. They are used to implement the QoS 1 and QoS 2 message mechanisms of MQTT.

## Sample Packets

We use [MQTTX CLI](https://mqttx.app/) to publish three messages with different QoS levels to the [Public MQTT Server](http://broker.emqx.io/), and use [Wireshark](https://www.wireshark.org/) to capture the [MQTT packets](https://www.emqx.com/en/blog/Introduction-to-mqtt-control-packets) going back and forth between the client and the server. In Linux, you can use [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) to capture the packets, and then import them into Wireshark for viewing.

The following are the MQTTX CLI commands used in this example. In order to display the Properties of the PUBLISH packet, the commands also set the Message Expiry Interval and Response Topic properties:

```
mqttx pub --hostname broker.emqx.io --mqtt-version 5 \  --topic request --qos 0 --message "This is a QoS 0 message" \  --message-expiry-interval 300 --response-topic response
```

The following is the PUBLISH packet with QoS 0 captured by Wireshark:

```
30 31 00 07 72 65 71 75 65 73 74 10 02 00 00 01 2c 08 00 08
72 65 73 70 6f 6e 73 65 54 68 69 73 20 69 73 20 61 20 51 6f
53 20 30 20 6d 65 73 73 61 67 65
```

This string of hexadecimal bytes corresponds to the following packet content:

![01publishpacket.png](https://assets.emqx.com/images/db09121a673ec2b5b9a71dd0c1ac7a28.png)

When we only modify the QoS option in the MQTTX CLI command and set it to 1, we will see that the server replies with a PUBACK packet after receiving the PUBLISH. Their packet data are as follows.

```
Client  -- PUBLISH (32 33 00 .. ..)    ->  Server
Client  <- PUBACK  (40 04 64 4a 10 00) --  Server
```

At this point, the first byte in the PUBLISH packet has changed from `0x30` to `0x32`, indicating that this is a QoS 1 message.

The PUBACK packet structure is relatively simple, as you can see the Reason Code is 0x10, indicating that the message has been received, but there is no matching subscriber. Once someone subscribes to the topic `request`, then the Reason Code in the PUBACK packet will change to `0x00`, indicating that the message has been received and there are matching subscribers.

![02pubackpacket.png](https://assets.emqx.com/images/206378344c851cad8dfd3dd96aa509d5.png)

Continuing to use MQTTX CLI to publish a QoS 2 message, we will see that there are two rounds of message exchanges between the client and the server. Wireshark will tell us that these packets are PUBLISH, PUBREC, PUBREL, and PUBCOMP respectively, and they all have the same Packet Identifier `0x11c2`:

```
Client  -- PUBLISH (34 33 00 .. ..)    ->  Server
Client  <- PUBREC  (50 04 11 c2 10 00) --  Server
Client  -- PUBREL  (62 03 11 c2 00)    ->  Server
Client  <- PUBCOMP (70 04 11 c2 00 00) --  Server
```

How do we accurately determine from the packet data composed of hexadecimal bytes whether it is a PUBLISH packet, what its QoS level is, and what is the Reason Code in its response packet? The following introduction to these packets will answer these questions.

## PUBLISH Packet Structure

### Fixed Header

In the Fixed Header of the PUBLISH packet, the high 4 bits of the first byte are fixed at 3 (0b0011), and the low 4 bits are composed of the following three fields:

- DUP (Bit 3): When the client or server retransmits the PUBLISH packet, the DUP flag needs to be set to 1, indicating that this is a retransmitted packet. The number and frequency of PUBLISH packets received with DUP set to 1 can reveal the quality of the current communication link.
- QoS (Bit 2 - 1): Used to specify the QoS level of the message.
- Retain (Bit 0): Set to 1, indicating that the current message is a [Retained Message](https://www.emqx.com/en/blog/mqtt5-features-retain-message); if set to 0, it means the current message is a normal message.

Following this is the Remaining Length field, which indicates the number of bytes in the remaining part of the current packet.

![03publishfixedheader.png](https://assets.emqx.com/images/7f2977d080204c7df53f61d244534196.png)

### Variable Header

The Variable Header of the PUBLISH packet contains the following fields in order:

- **Topic Name**: This is a UTF-8 Encoded String, used to indicate which channel the message should be published to.
- **Packet Identifier**: This is a Two Byte Integer, used to uniquely identify the message currently being transmitted. The Packet Identifier only appears in the PUBLISH packet when the QoS level is 1 or 2.
- **Properties**: The table below lists all available Properties of the PUBLISH packet. We will not take extra text here to introduce the purpose of each property. You can click on the property name to view the corresponding blog:

| **Identifier** | **Property Name**                                            | **Type**              |
| :------------- | :----------------------------------------------------------- | :-------------------- |
| 0x01           | [Payload Format Indicator](https://www.emqx.com/en/blog/mqtt5-new-features-payload-format-indicator-and-content-type) | Byte                  |
| 0x02           | Message Expiry Interval                                      | Four Byte Integer     |
| 0x23           | [Topic Alias](https://www.emqx.com/en/blog/mqtt5-topic-alias) | Two Byte Integer      |
| 0x08           | [Response Topic](https://www.emqx.com/en/blog/mqtt5-request-response) | UTF-8 Encoded String  |
| 0x09           | [Correlation Data](https://www.emqx.com/en/blog/mqtt5-request-response) | Binary Data           |
| 0x26           | User Property                                                | UTF-8 String Pair     |
| 0x0B           | [Subscription Identifier](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options) | Variable Byte Integer |
| 0x03           | [Content Type](https://www.emqx.com/en/blog/mqtt5-new-features-payload-format-indicator-and-content-type) | UTF-8 Encoded String  |

### Payload

The content of the application message we send is stored in the Payload of the PUBLISH packet. It can carry application messages in any format, such as JSON, ProtoBuf, and so on.

## PUBACK Packet Structure

### Fixed Header

The high 4 bits of the first byte in the Fixed Header are fixed at 4 (0b0100), indicating that this is a PUBACK packet. The lower 4 bits are reserved and are all set to 0.

Immediately following is the Remaining Length field, which indicates the number of bytes remaining in the current packet.

![04pubackfixedheader.png](https://assets.emqx.com/images/e3a3ff74bd8fc54bc4b6c11b442b02e8.png)

### Variable Header

The Variable Header of the PUBACK packet contains the following fields in order:

- **Packet Identifier**: Unlike the PUBLISH packet, the Packet Identifier in the PUBACK packet must exist. It is used to indicate to the other end which QoS 1 PUBLISH packet this is a response to.
- **Reason Code**: This is a Single-Byte Integer used to indicate the publication result to the publisher, such as whether the publication was rejected due to lack of authorization. The table below lists all available Reason Codes for the PUBACK packet:

| **Value** | **Reason Code**               | **Description**                                              |
| :-------- | :---------------------------- | :----------------------------------------------------------- |
| 0x00      | Success                       | The message is accepted.                                     |
| 0x10      | No matching subscribers       | The message is accepted, but there are currently no matching subscribers. |
| 0x80      | Unspecified error             | Indicates an unspecified error. When one party does not wish to disclose the specific cause of the error to the other party, or no Reason Code can match the current situation in the protocol specification, it can use this Reason Code in the packet. |
| 0x83      | Implementation specific error | The PUBLISH packet is valid, but not accepted by the current receiver's implementation. |
| 0x87      | Not authorized                | The PUBLISH packet did not pass the permission check of the server, probably because the current client does not have permission to publish messages to the corresponding topic. |
| 0x90      | Topic Name invalid            | The topic name is well-formed, but not accepted by the client or server. |
| 0x91      | Packet identifier in use      | The Packet ID in the PUBLISH packet is already in use, which usually means that the session state of the client and server do not match, or that one of them has an incorrect implementation. |
| 0x97      | Quota exceeded                | Used to indicate that a quota limit has been exceeded.The server may limit the sending quota of the publisher, such as allowing a maximum of 1000 messages to be forwarded daily. When the publisher exhausts the quota, the server will use this Reason Code in acknowledgment packets such as PUBACK to remind the publisher. |
| 0x99      | Payload format invalid        | Indicates that the format of the Payload does not match the format indicated by the Payload Format Indicator property. |

- **Properties**: The table below lists all available Properties of the PUBLISH packet. 

| **Identifier** | **Property Name** | **Type**             |
| :------------- | :---------------- | :------------------- |
| 0x1F           | Reason String     | UTF-8 Encoded String |
| 0x26           | User Property     | UTF-8 String Pair    |

### Payload

The PUBACK packet has no Payload.

## PUBREC, PUBREL, PUBCOMP Packet Structure

The packet structure of PUBREC, PUBREL, and PUBCOMP is basically consistent with PUBACK. Their main differences lie in the value of the Packet Type field in the Fixed Header, and the reason codes that can be used.

The value of the Packet Type field is 5, indicating that this is a PUBREC packet; if the value is 6, it indicates that this is a PUBREL packet; if the value is 7, it indicates that this is a PUBCOMP packet.

PUBREC, as the acknowledgment packet for the PUBLISH packet in the QoS 2 message flow, can use the reason codes exactly the same as PUBACK. The reason codes available for PUBREL and PUBCOMP packets are as follows:

| **Identifier** | **Reason Code Name**        | **Description**                                              |
| :------------- | :-------------------------- | :----------------------------------------------------------- |
| 0x00           | Success                     | - When returned in the **PUBREL** packet by the sender of the QoS 2 message, it indicates that the message has been released, and this message will not be retransmitted in the future.<br /><br />- When returned in the **PUBREC** packet by the receiver of the QoS 2 message, it indicates that the Packet Identifier used in the message has been released, and now the sender can use this Packet Identifier to send new messages. |
| 0x92           | Packet Identifier not found | An unknown packet identifier has been received, which usually means that the current session state of the server and client does not match. |

## Conclusion

The **Topic** in the PUBLISH packet determines the direction of the message, and **QoS** determines the reliability of the message. It also determines which packets will be used during transmission. The PUBACK packet is used for QoS 1 messages, and the PUBREC, PUBREC, and PUBCOMP packets are used for QoS 2 messages. When QoS is greater than 0, the packet also needs to contain a Packet Identifier to associate the PUBLISH packet with its response packet.

The **Payload** of the PUBLISH packet does not limit the data type, so we can transmit application messages of any format. In addition, the **Properties** can meet our needs in more scenarios. For example, Topic Alias can reduce the size of each message, and Message Expiry Interval can set expiration times for time-sensitive messages, and so on.

These **response packets** of the PUBLISH packet not only indicate to the sender that the message has been received, but also further indicate the publishing result through the Reason Code. So when the subscriber cannot receive the message, we can also troubleshoot the problem through the reason code in the response packet received by the publisher.

The above is an introduction to MQTT PUBLISH and its response packets. In the next article, we will continue to study the SUBSCRIBE and UNSUBSCRIBE packets.
