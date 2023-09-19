Welcome to the third article of the [MQTT 5.0 Packet Series](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets). In the previous article, we introduced the [PUBLISH packet and its response packets](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-02-publish-puback) in MQTT 5.0. Now, we will introduce the control packets used for subscription and unsubscription.

In MQTT, the SUBSCRIBE packet is used to initiate a subscription request, while the SUBACK packet is used to return the subscription result. The UNSUBSCRIBE and UNSUBACK packets are used when unsubscribing. Subscribing to topics is more commonly used than unsubscribing. However, in this article, we will still introduce the structure and composition of subscription and unsubscription packets.

## Sample Packets

First, we use [Wireshark](https://www.wireshark.org/) to capture a real MQTT subscription request and response. Here we use the [MQTTX CLI](https://mqttx.app/) to initiate a subscription request to the [Public MQTT Server](http://broker.emqx.io/). The following command will create a subscription with the topic `demo` and maximum QoS set to 2:

```
 mqttx sub --hostname broker.emqx.io --mqtt-version 5 --topic demo --qos 2
```

The following is the SUBSCRIBE and SUBACK packet captured by Wireshark:

```
# SUBSCRIBE 82 0a 05 be 00 00 04 64 65 6d 6f 02 # SUBACK 90 04 05 be 00 02
```

>  In Linux, you can use [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) to capture the packets, and then import them to Wireshark for viewing.

These original and obscure packet data composed of hexadecimal bytes correspond to the following contents:

![01subscribepacket.png](https://assets.emqx.com/images/54667587fb8f421cca9f08a880aca28d.png)

![02subackpacket.png](https://assets.emqx.com/images/fff8f96c91fd20f7671b556d0c5f21cc.png)

Maybe you are starting to wonder how they complete the conversion from simple MQTTX CLI commands to complex packet data, or curious about how you can extract the information you want when you capture an MQTT packet.

In the following introduction to the packet structures of SUBSCRIBE, SUBACK, UNSUBSCRIBE and UNSUBACK, your questions will be answered.

## SUBSCRIBE Packet Structure

### Fixed Header

In the SUBSCRIBE packet, the high 4 bits of the first byte in the fixed header must be set to 8 (0b1000), while the low 4 bits reserved must be set to 2 (0b0010). Following the first byte, there is still the Remaining Length field, which is a variable byte integer.

![03subscriberfixedheader.png](https://assets.emqx.com/images/df010a5d34a47bed6607fb748a3708a2.png)

### Variable Header

The Variable Header of the SUBSCRIBE packet contains the following fields in order:

![04subscribevariableheader.png](https://assets.emqx.com/images/dd3f1c7c0fbb39c1581053fb69dd9450.png)

- **Packet Identifier**: A Two Byte Integer, is used to uniquely identify the subscription request. PUBLISH, SUBSCRIBE, and UNSUBSCRIBE packets use a set of packet identifiers, which means they cannot use the same packet identifier simultaneously.
- **Properties**: The table below lists all available Properties of the SUBSCRIBE packet.

| **Identifier** | **Property Name**                                            | **Type**              |
| :------------- | :----------------------------------------------------------- | :-------------------- |
| 0x0B           | [Subscription Identifier](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options) | Variable Byte Integer |
| 0x26           | User Property                                                | UTF-8 String Pair     |

### Payload

The payload of the SUBSCRIBE packet contains one or more Topic Filter and Subscription Option pairs. The Topic Filter is a UTF-8 Encoded String used to indicate to the server the topic that the client wishes to subscribe to, while the Subscription Option occupies only one byte, currently consisting of the following four options:

- Reserved (Bit 7, 6): Reserved bits, which must currently be set to 0.
- **Retain Handling (Bit 5, 4)**: Used to indicate whether the server needs to send retained messages to this subscription when the subscription is established.
- **Retain As Published (Bit 3)**: Used to indicate whether the server needs to keep the Retain flag in the message when forwarding the application message to this subscription.
- **No Local (Bit 2)**: Used to indicate whether the server can forward the application message to the publisher of the message. No Local and Retain As Published are usually used in bridging scenarios.
- **Maximum QoS (Bit 1, 0)**: This option determines the maximum QoS level that the server can use when forwarding messages to this subscription. If the original QoS of the message exceeds this limit, the server will downgrade the QoS to ensure message delivery.

![05subscribepayload.png](https://assets.emqx.com/images/c63e72b4b587aaa847785619c2b52f4e.png)

## SUBACK Packet Structure

### Fixed Header

For the SUBACK packet, the first byte of the Fixed Header consists of the high 4 bits of the MQTT Control Packet type and the low 4 bits of reserved bits, the former must be 9 (0b1001) and the latter must be 0 (0b0000)

![06subackfixedheader.png](https://assets.emqx.com/images/b6edeabdd7a3a88e4ecd46494e13d6fd.png)

### Variable Header

The Variable Header of the SUBACK packets contains the following fields in order:

![07subackvariableheader.png](https://assets.emqx.com/images/288fc95c8d214629b452e50328e2e179.png)

- **Packet Identifier**: The Packet Identifiers in the SUBACK packet must be consistent with the corresponding SUBSCRIBE packet so that the other party can correctly match the response with the request.
- **Properties**: The following table lists all available properties of the SUBACK packet.

| **Identifier** | **Property Name**                                            | **Type**             |
| :------------- | :----------------------------------------------------------- | :------------------- |
| 0x1F           | Reason String                                                | UTF-8 Encoded String |
| 0x26           | User Property | UTF-8 String Pair    |

### Payload

The Payload of the SUBACK packet contains a Reason Code list, and the Reason Code indicates whether the subscription is successful or the reason for the failure. A Reason Code corresponds to a Topic Filter in the SUBSCRIBE packet, so the order of Reason Codes in the SUBACK packet must be consistent with the order of the Topic Filters in the SUBSCRIBE packet.

![08subackpayload.png](https://assets.emqx.com/images/8b2b7467bbff6485c03f3699f80b1411.png)

The table below lists all available Reason Codes for the SUBACK packet:

| **Value** | **Reason Code Name**                   | **Description**                                              |
| :-------- | :------------------------------------- | :----------------------------------------------------------- |
| 0x00      | Granted QoS 0                          | The subscription is accepted and the maximum QoS level is 0. The QoS level granted by the server may be lower than the QoS level requested by the client, which mainly depends on whether the server supports all QoS or the corresponding permission settings. |
| 0x01      | Granted QoS 1                          | The subscription is accepted and the maximum QoS level is 1. |
| 0x02      | Granted QoS 2                          | The subscription is accepted and the maximum QoS level is 2. |
| 0x80      | Unspecified error                      | Indicates an unspecified error. When one party does not wish to disclose the specific cause of the error to the other party, or no Reason Code can match the current situation in the protocol specification, it can use this Reason Code in the packet. |
| 0x83      | Implementation specific error          | The SUBSCRIBE packet is valid, but not accepted by the current receiver's implementation. |
| 0x87      | Not authorized                         | The Client is not authorized to make this subscription.      |
| 0x8F      | Topic Filter invalid                   | The Topic Filter is in the correct format, but is not accepted by the server. For example, the level of Topic Filters exceeds the maximum number allowed by the server. |
| 0x91      | Packet Identifier in use               | The Packet ID in the received packet is in use.              |
| 0x97      | Quota exceeded                         | Indicates that the quota limit has been exceeded. The server may limit the subscription quota of the subscriber. For example, a client can establish up to 10 subscriptions. |
| 0x9E      | Shared Subscriptions not supported     | The server does not support shared subscriptions.            |
| 0xA1      | Subscription Identifiers not supported | The server does not support subscription identifiers.       |
| 0xA2      | Wildcard Subscriptions not supported   | The server does not support wildcard subscriptions.          |

## UNSUBSCRIBE Packet Structure

### Fixed Header

Same as the SUBSCRIBE packet, the only difference is that the value of the Packet Type field changes from 8 (0b1000) to 10 (0b1010).

![09unsubscribefixedheader.png](https://assets.emqx.com/images/3cbeea749ba7719a755d4d74cd47a5f7.png)

### Variable Header

Same as the SUBSCRIBE packet.

### Payload

The payload of the UNSUBSCRIBE packet contains one or more Topic Filters that the client wishes to unsubscribe from. These Topic Filters are also UTF-8 Encoded Strings, and multiple Topic Filters are closely connected.

![10unsubscribepayload.png](https://assets.emqx.com/images/892f55deca7a9124b5a311a7df35f7a6.png)

## UNSUBACK Packet Structure

### Fixed Header

For the UNSUBACK packet, the first byte of the Fixed Header consists of the high 4 bits of the MQTT Control Packet type and the low 4 bits of reserved bits, the former must be 11 (0b1011) and the latter must be 0 (0b0000)

![11unsubackfixedheader.png](https://assets.emqx.com/images/e028ab1821257fd15eb48e1d306c19be.png)

### Variable Header

The Variable Header of UNSUBACK contains the Packet Identifier and Properties fields in order, and the available properties are the same as those of the SUBACK packet.

### Payload

The Payload of the UNSUBACK packet also contains a Reason Code list. The Reason Code indicates whether the unsubscription was successful or failed. These Reason Codes correspond to the Topic Filters in the UNSUBSCRIBE packet in order.

![12unsubackpayload.png](https://assets.emqx.com/images/58e831469bceeea18e8648c544f33132.png)

The table below lists all available Reason Codes for the UNSUBACK packet:

| **Value** | **Reason Code Name**          | **Description**                                              |
| :-------- | :---------------------------- | :----------------------------------------------------------- |
| 0x00      | Success                       | The Subscription is deleted.                                 |
| 0x11      | No subscription existed       | No matching Topic Filter is being used by the Client.        |
| 0x80      | Unspecified error             | The unsubscribe could not be completed and the Server either does not wish to reveal the reason or none of the other Reason Codes apply. |
| 0x83      | Implementation specific error | The UNSUBSCRIBE is valid but the Server does not accept it.  |
| 0x87      | Not authorized                | The Client is not authorized to unsubscribe.                 |
| 0x8F      | Topic Filter invalid          | The Topic Filter is in the correct format, but is not accepted by the server. For example, the level of Topic Filters exceeds the maximum number allowed by the server. |
| 0x91      | Packet Identifier in use      | The specified Packet Identifier is already in use.           |

## Conclusion

SUBSCRIBE and SUBACK packets are used for subscribing, while UNSUBSCRIBE and UNSUBACK are used for unsubscribing. The list of Topic Filters to subscribe or unsubscribe is located in the Payload of the respective packets. Each Topic Filter in the SUBSCRIBE packet is associated with a set of subscription options.

The Reason Code indicating the request result is located in the Payload of the SUBACK and UNSUBACK packets, and it is a list, corresponding one by one to the Topic Filters in the request packet.

In the next article, we will continue to study the MQTT heartbeat packet.
