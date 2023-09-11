Establishing an MQTT connection requires two control packets, namely the CONNECT packet and the CONNACK packet. The CONNECT packet is the first control packet sent by the client to the server after establishing a network connection, and is used to initiate a connection request. The server will return a CONNACK packet to inform the client of the connection result. In this article, we will delve into the structure of these two packets.

## CONNECT Packet Structure

### Fixed Header

In the Fixed Header of the CONNECT packet, the Packet Type field located in the high 4 bits of the first byte must be 1, and the low 4 bits in the first byte must all be 0.

Therefore, the value of the first byte of the CONNECT packet must be `0x10`. We can use this to determine whether a packet is a CONNECT packet.

![MQTT CONNECT Fixed Header](https://assets.emqx.com/images/08cdf8ff00ffbb808d3d399be545a245.png)

### Variable Header

The Variable Header of the CONNECT packet contains the following fields in order:

![MQTT CONNECT Variable Header](https://assets.emqx.com/images/67882a45ba2a35b791f59a51bd8d9aae.png)

- **Protocol Name**: This is a UTF-8 encoded string used to indicate the protocol name. In [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), the first two bytes of the UTF-8 encoded string are uniformly used to indicate the length of the actual character data that follows. The protocol name is fixed as `MQTT` in MQTT 3.1.1 and MQTT 5.0, so the corresponding complete content in hexadecimal bytes is `00 04 4d 51 54 54`, where `4d 51 54 54` is the ASCII value of the string `MQTT`. The protocol name in the earliest MQTT 3.1 is `MQIsdp`, so it corresponds to `00 06 4d 51 49 73 64 70`.

- **Protocol Version**: This is a single-byte length unsigned integer used to indicate the protocol version. Currently, there are only three possible values, 3 represents MQTT 3.1, 4 represents MQTT 3.1.1, and 5 represents MQTT 5.0.

- **Connect Flags**: Connection flags, it has a length of only one byte, but contains several flags used to indicate connection behavior or whether certain fields exist in the Payload.

  ![MQTT Connect Flags](https://assets.emqx.com/images/1fd83053e697fff76251dca90258cf52.png)

  - **User Name Flag**: Used to indicate whether the Payload contains the Username.
  - **Password Flag**: Used to indicate whether the Payload contains the Password.
  - [**Will Retain**](https://www.emqx.com/en/blog/use-of-mqtt-will-message): Used to indicate whether the will message is a retained message.
  - **Will QoS**: Used to indicate the QoS of the will message.
  - **Will Flag**: Used to indicate whether the Payload contains relevant fields of the will message.
  - **Clean Start**: Used to indicate whether the current connection is a new session or a continuation of an existing session, which determines whether the server will directly create a new session or attempt to reuse an existing session.
  - **Reserved**: This is a reserved bit, its value must be 0.

- [**Keep Alive**](https://www.emqx.com/en/blog/mqtt-keep-alive): This is a double-byte length unsigned integer used to indicate the maximum time interval between two adjacent control packets sent by the client.

- **Properties**: The table below lists all available properties of the CONNECT packet.

| **Identifier** | **Property Name**                                            | **Type**             |
| :------------- | :----------------------------------------------------------- | :------------------- |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | Four Byte Integer    |
| 0x21           | [Receive Maximum](https://www.emqx.com/en/blog/mqtt5-flow-control) | Two Byte Integer     |
| 0x27           | Maximum Packet Size                                          | Four Byte Integer    |
| 0x22           | [Topic Alias Maximum](https://www.emqx.com/en/blog/mqtt5-topic-alias) | Two Byte Integer     |
| 0x19           | Request Response Information                                 | Byte                 |
| 0x17           | Request Problem Information                                  | Byte                 |
| 0x26           | [User Property](https://www.emqx.com/en/blog/mqtt5-user-properties) | UTF-8 String Pair    |
| 0x15           | [Authentication Method](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | UTF-8 Encoded String |
| 0x16           | [Authentication Data](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | Binary Data          |

### Payload

In the Payload of the CONNECT packet, aside from the Client ID, all other fields are optional. Their existence depends on the value of the corresponding flag in the Connect Flags of the variable header. However, if these exist, they must appear in the order of Client ID, Will Properties, Will Topic, Will Payload, User Name, and Password.

![MQTT CONNECT Payload](https://assets.emqx.com/images/3c0b5c81ff42ca4681e70aef4531a32c.png)

## CONNACK Packet Structure

### Fixed Header

The value of the high 4 bits in the first byte of the Fixed Header is 2, indicating that this is a CONNACK packet.

![MQTT CONNACK Fixed Header](https://assets.emqx.com/images/7cd9650b420a7be8028a2f751dd8f762.png)

### Variable Header

The Variable Header of the CONNACK packet contains the following fields in order:

![MQTT CONNACK Variable Header](https://assets.emqx.com/images/006e35f23bd97b41cc8c59dc654cf31c.png)

- Connect Acknowledge Flags: Connection confirmation flag.
  - **Reserved (Bit 7 - 1)**: Reserved bits, must be set to 0.
  - **Session Present (Bit 0)**: Used to indicate whether the server is using an existing session to resume communication with the client. Session Present may be 1 only when the client has set Clean Start to 0 in the CONNECT connection.
- **Reason Code**: Used to indicate the result of the connection. The table below lists some common Reason Codes in the CONNACK packet, for a complete list, please refer to the [MQTT 5.0 Reason Code Quick Reference Guide](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack).

| **Value** | **Reason Code Name**      | **Description**                                              |
| :-------- | :------------------------ | :----------------------------------------------------------- |
| 0x00      | Success                   | The connection is accepted.                                  |
| 0x81      | Malformed Packet          | The server cannot correctly parse the CONNECT packet according to the protocol specification, for example, the reserved bit is not set to 0 according to the protocol requirements. |
| 0x82      | Protocol Error            | The CONNECT packet can be parsed correctly, but the content does not conform to the protocol specification, for example, the value of the Will Topic field is not a valid MQTT topic. |
| 0x86      | Bad User Name or Password | The client was refused a connection because it used an incorrect username or password. |
| 0x95      | Packet too large          | The CONNECT packet exceeds the maximum size allowed by the server, probably because it carries a large will message. |

- **Properties**: The table below lists all available properties for the CONNACK packet.

| **Identifier** | **Property Name**                                            | **Type**             |
| :------------- | :----------------------------------------------------------- | :------------------- |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | Four Byte Integer    |
| 0x21           | [Receive Maximum](https://www.emqx.com/en/blog/mqtt5-flow-control) | Two Byte Integer     |
| 0x24           | Maximum QoS                                                  | Byte                 |
| 0x25           | Retain Available                                             | Bytes                |
| 0x27           | Maximum Packet Size                                          | Four Byte Integer    |
| 0x12           | Assigned Client Identifier                                   | UTF-8 Encoded String |
| 0x22           | [Topic Alias Maximum](https://www.emqx.com/en/blog/mqtt5-topic-alias) | Two Byte Integer     |
| 0x1F           | Reason String                                                | UTF-8 Encoded String |
| 0x26           | [User Property](https://www.emqx.com/en/blog/mqtt5-user-properties) | UTF-8 String Pair    |
| 0x28           | Wildcard Subscription Available                              | Byte                 |
| 0x29           | Subscription Identifier Available                            | Bytes                |
| 0x2A           | Shared Subscription Available                                | Byte                 |
| 0x13           | Server Keep Alive                                            | Two Byte Integer     |
| 0x1A           | Response Information                                         | UTF-8 Encoded String |
| 0x1C           | Server Reference                                             | UTF-8 Encoded String |
| 0x15           | [Authentication Method](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | UTF-8 Encoded String |
| 0x16           | [Authentication Data](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | Binary Data          |

### Payload

The CONNACK packet has no Payload.

## Examples

We use [MQTTX CLI](https://mqttx.app/) to initiate a connection to a [Public MQTT server](http://broker.emqx.io/). In this connection, we set the protocol version to MQTT 5.0, Clean Start to 1, Session Expiry Interval to 300 seconds, Keep Alive to 60, and the username and password to admin and public respectively. The corresponding MQTTX CLI command is:

```
mqttx conn --hostname broker.emqx.io --mqtt-version 5 \
  --session-expiry-interval 300 --keepalive 60 --username admin --password public
```

Below is the CONNECT packet sent out by MQTTX CLI captured using the Wireshark tool:

```
10 2f 00 04 4d 51 54 54 05 c2 00 3c 05 11 00 00 01 2c 00 0e 6d 71 74 74 78 5f 30 63 36 36 38 64 30 64 00 05 61 64 6d 69 6e 00 06 70 75 62 6c 69 63
```

But this is a set of hexadecimal bytes that is not easy to understand. The following example can help you better understand how the CONNECT packet organizes various fields:

![MQTT CONNECT packet](https://assets.emqx.com/images/54e526147fa96f407f307c69b047f125.png)

Similarly, we also captured the CONNACK packet returned by the public MQTT server:

```
20 13 00 00 10 27 00 10 00 00 25 01 2a 01 29 01 22 ff ff 28 01
```

In the following example, you can see that the Reason Code of the CONNACK packet is 0, which means that the connection was successful. The multiple properties that follow provide a list of features supported by the server, such as the maximum packet size supported, whether to support retained messages, etc.:

![MQTT CONNACK packet](https://assets.emqx.com/images/32848cc16061f4bddff4e3859bef5791.png)

The above examples are to help everyone better understand the structure of MQTT Packets. In actual applications, you can directly view the packet details in Wireshark. Wireshark provides excellent support for MQTT. It directly lists the values of each field for us, without the need for us to analyze ourselves:

![Wireshark](https://assets.emqx.com/images/3dfb4359c7c16912652b642577270a98.png)

The above is an introduction to the MQTT CONNECT and CONNACK packet. In subsequent blogs, we will continue to study the structure and composition of PUBLISH, DISCONNECT, and other packets.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
