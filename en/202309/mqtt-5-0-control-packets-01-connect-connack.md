In [*Introduction to MQTT 5.0 Packet*](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets), we introduced that MQTT packets are composed of three parts: Fixed Header, Variable Header, and Payload, as well as common concepts in MQTT packets such as Variable Byte Integer and Property. Now, we will further introduce the composition of each type of packet according to its actual use. First, we will focus on the packets used to establish an MQTT connection.

If we want to use MQTT for communication, the first step must be to establish an MQTT connection. Establishing an MQTT connection requires the use of two control packets, which are the CONNECT packet and the CONNACK packet. The CONNECT packet is the first control packet sent by the client to the server after establishing a network connection and is used to initiate a connection request. The server will return a CONNACK packet to inform the client of the connection result.

## Sample Packets

We use [MQTTX CLI](https://mqttx.app/) to initiate a connection to a [Public MQTT server](http://broker.emqx.io/). In this connection, we set the protocol version to MQTT 5.0, Clean Start to 1, Session Expiry Interval to 300 seconds, Keep Alive to 60, and the username and password to admin and public respectively. The corresponding MQTTX CLI command is:

```
mqttx conn --hostname broker.emqx.io --mqtt-version 5 \
  --session-expiry-interval 300 --keepalive 60 --username admin --password public
```

Below is the CONNECT packet sent out by MQTTX CLI captured using the Wireshark tool:

The following is the CONNECT packet sent by MQTTX CLI captured using [Wireshark](https://www.wireshark.org/). In Linux, you can use [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) to capture the packet first, and then import it to Wireshark for viewing:

```
10 2f 00 04 4d 51 54 54 05 c2 00 3c 05 11 00 00 01 2c 00 0e 6d
71 74 74 78 5f 30 63 36 36 38 64 30 64 00 05 61 64 6d 69 6e 00
06 70 75 62 6c 69 63
```

But this is a string of hexadecimal bytes that is not easy to understand unless they are converted into the following format:

![01connectpacket.png](https://assets.emqx.com/images/de934ddfbedc2922a19c2bb88ea3b26a.png)

Similarly, we also captured the CONNACK packet returned by the public MQTT server:

```
20 13 00 00 10 27 00 10 00 00 25 01 2a 01 29 01 22 ff ff 28 01
```

After parsing this string of packet data, we can see that the Reason Code of the CONNACK packet is 0, which means that the connection was successful. The multiple properties that follow provide a list of features supported by the server, such as the maximum packet size supported, whether to support retained messages, etc:

![02connackpacket.png](https://assets.emqx.com/images/0d48fa57b6590900bf66e2b67df32464.png)

The above examples are to help everyone better understand the structure of MQTT Packets. In actual applications, you can directly view the packet details in Wireshark. Wireshark provides excellent support for MQTT. It directly lists the values of each field for us, without the need for us to analyze ourselves:

Of course, Wireshark has actually listed the values of each field in the packet for us. Through the following introduction to the structure of the CONNECT and CONNACK packets, combined with the packet capture results of Wireshark, you will quickly master these two packets:

![03wireshark.png](https://assets.emqx.com/images/9be85c6a5a68cccafdd32dd93d810ce1.png)

## CONNECT Packet Structure

### Fixed Header

In the Fixed Header of the CONNECT packet, the Packet Type field located in the high 4 bits of the first byte must be 1 (0b0001), and the low 4 bits in the first byte must all be 0.

Therefore, the value of the first byte of the CONNECT packet must be `0x10`. We can use this to determine whether a packet is a CONNECT packet.

![04connectfixedheader.png](https://assets.emqx.com/images/e34ffd1888f42d4ffd28966e63533547.png)

### Variable Header

The Variable Header of the CONNECT packet contains the following fields in order:

![05connectvariableheader.png](https://assets.emqx.com/images/710ded5e349b0fc2300f82972a7c49a2.png)

- **Protocol Name**: This is a UTF-8 encoded string used to indicate the protocol name. In MQTT, the first two bytes of the UTF-8 encoded string are uniformly used to indicate the length of the actual character data that follows. The protocol name is fixed as `MQTT` in MQTT 3.1.1 and MQTT 5.0, so the corresponding complete content in hexadecimal bytes is `00 04 4d 51 54 54`, where `4d 51 54 54` is the ASCII value of the string `MQTT`. The protocol name in the earliest MQTT 3.1 is `MQIsdp`, so it corresponds to `00 06 4d 51 49 73 64 70`.

- **Protocol Version**: This is a single-byte length unsigned integer used to indicate the protocol version. Currently, there are only three possible values, 3 represents MQTT 3.1, 4 represents MQTT 3.1.1, and 5 represents MQTT 5.0.

- **Connect Flags**: Connection flags, have a length of only one byte, but contain several flags used to indicate connection behavior or whether certain fields exist in the Payload.

  ![06connectflags.png](https://assets.emqx.com/images/ca561dee1f5e9fd4a304b16c0472a911.png)

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

![07connectpayload.png](https://assets.emqx.com/images/0272022bd2f54c09eeac3b6dbd60c40a.png)

## CONNACK Packet Structure

### Fixed Header

The value of the high 4 bits in the first byte of the Fixed Header is 2 (0b0010), indicating that this is a CONNACK packet.

![08connackfixedheader.png](https://assets.emqx.com/images/63ab41f7efdbecb40eab76caf52e1e70.png)

### Variable Header

The Variable Header of the CONNACK packet contains the following fields in order:

![09connackvariableheader.png](https://assets.emqx.com/images/797c0f4df6c91c530a8f09b2d91029d5.png)

- Connect Acknowledge Flags: Connection confirmation flag.

  - Reserved (Bit 7 - 1): Reserved bits, must be set to 0.
  - **Session Present (Bit 0)**: Used to indicate whether the server is using an existing session to resume communication with the client. Session Present may be 1 only when the client has set Clean Start to 0 in the CONNECT connection.

- **Reason Code**: Used to indicate the result of the connection. The table below lists some common Reason Codes in the CONNACK packet, for a complete list, please refer to the [MQTT 5.0 Reason Code Quick Reference Guide](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack).

| **Value** | **Reason Code Name**         | **Description**                                              |
| :-------- | :--------------------------- | :----------------------------------------------------------- |
| 0x00      | Success                      | The connection is accepted.                                  |
| 0x81      | Malformed Packet             | The server cannot correctly parse the CONNECT packet according to the protocol specification, for example, the reserved bit is not set to 0 according to the protocol requirements. |
| 0x82      | Protocol Error               | The CONNECT packet can be parsed correctly, but the content does not conform to the protocol specification, for example, the value of the Will Topic field is not a valid MQTT topic. |
| 0x84      | Unsupported Protocol Version | The server does not support the MQTT protocol version requested by the client. |
| 0x85      | Client Identifier not valid  | Client ID is valid, but is not accepted by the server. For example, the Client ID exceeds the maximum length allowed by the server. |
| 0x86      | Bad User Name or Password    | The client was refused a connection because it used an incorrect username or password. |
| 0x95      | Packet too large             | The CONNECT packet exceeds the maximum size allowed by the server, probably because it carries a large will message. |
| 0x8A      | Banned                       | Indicating that the client is prohibited from logging in. For example, the server detects the abnormal connection behavior of the client, so the Client ID or IP address of the client is added to the blacklist, or the background administrator manually blocks the client. Of course, the above usually depends on the specific server implementation. |

- **Properties**: The table below lists all available properties for the CONNACK packet.

| **Identifier** | **Property Name**                                            | **Type**             |
| :------------- | :----------------------------------------------------------- | :------------------- |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | Four Byte Integer    |
| 0x21           | [Receive Maximum](https://www.emqx.com/en/blog/mqtt5-flow-control) | Two Byte Integer     |
| 0x24           | Maximum QoS                                                  | Byte                 |
| 0x25           | Retain Available                                             | Bytes                |
| 0x27           | [Maximum Packet Size](https://www.emqx.com/en/blog/best-practices-of-maximum-packet-size-in-mqtt)                                          | Four Byte Integer    |
| 0x12           | Assigned Client Identifier                                   | UTF-8 Encoded String |
| 0x22           | [Topic Alias Maximum](https://www.emqx.com/en/blog/mqtt5-topic-alias) | Two Byte Integer     |
| 0x1F           | Reason String                                                | UTF-8 Encoded String |
| 0x26           | [User Property](https://www.emqx.com/en/blog/mqtt5-user-properties) | UTF-8 String Pair    |
| 0x28           | Wildcard Subscription Available                              | Byte                 |
| 0x29           | [Subscription Identifier](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options) Available                            | Bytes                |
| 0x2A           | [Shared Subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) Available                                | Byte                 |
| 0x13           | Server Keep Alive                                            | Two Byte Integer     |
| 0x1A           | Response Information                                         | UTF-8 Encoded String |
| 0x1C           | Server Reference                                             | UTF-8 Encoded String |
| 0x15           | [Authentication Method](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | UTF-8 Encoded String |
| 0x16           | [Authentication Data](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security) | Binary Data          |

### Payload

The CONNACK packet has no Payload.

## Conclusion

CONNECT is the first MQTT packet sent by the client after the network connection between the client and the server is established. CONNACK, as the response packet of CONNECT, indicates the connection result through the reason code.

The client and server need to use CONNECT and CONNACK packets to complete the exchange of necessary information, such as the protocol version, Client ID, user name, password used by the client, and the maximum packet size and QoS supported by the server, and whether there is a corresponding session.

The above is an introduction to the MQTT CONNECT and CONNACK packets. In subsequent articles, we will continue to study the structure and composition of packets like PUBLISH, and DISCONNECT.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
