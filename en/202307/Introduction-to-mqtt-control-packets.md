## What are MQTT Control Packets?

MQTT control packets are the smallest unit of data transfer in [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) and servers exchange control packets for performing their work, such as subscribing to topics and publishing messages.

Currently, MQTT defines 15 types of control packets. If we classify them based on their functionality, we can categorize these packets into three categories: connection, publishing, and subscribing.

![MQTT control packets](https://assets.emqx.com/images/936acfcc4136e28a53732a7751762abb.png)

 Among them, the **CONNECT** packet is used by the client to initiate a connection to the server, and the **CONNACK** packet is sent as a response to indicate the result of the connection. If one wants to terminate the communication or encounters an error that requires terminating the connection, the client and server can send a **DISCONNECT** packet and then close the network connection.

The **AUTH** packet is a new type of packet introduced in MQTT 5.0, and it is used solely for enhanced authentication, providing more secure authentication for clients and servers.

The **PINGREQ** and **PINGRESP** packets are used for connection keep-alive and probing. The client periodically sends a **PINGREQ** packet to the server to indicate that it is still active, then judges whether the server is active according to whether the **PINGRESP** packet is returned in time.

The **PUBLISH** packet is used to publish messages, and the remaining four packets are used to acknowledge QoS 1 and 2 messages.

The **SUBSCRIBE** packet is used by the client to subscribe to topics, while the **UNSUBSCRIBE** packet serves the opposite purpose. The **SUBACK** and **UNSUBACK** packets are used to return the results of subscription and unsubscription, respectively.

## MQTT Packet Format

In MQTT, regardless of the type of control packet, they all consist of three parts: Fixed Header, Variable Header, and Payload.

The Fixed Header always exists in all control packets. The existence and content of the Variable Header and Payload depend on the specific packet type. For example, the **PINGREQ** packet used for keeping alive only includes the Fixed Header, while the **PUBLISH** packet used for transmitting application messages includes all three parts.

![MQTT Packet Format](https://assets.emqx.com/images/1e9c7ce0b37a9605e3fc49100b6f10fe.png)

### Fixed Header

The Fixed Header consists of three fields: MQTT Control Packet Type, Flags, and Remaining Length.

![MQTT Fixed Header](https://assets.emqx.com/images/591a2168c2c192c3b03479e7531c05ea.png)

The MQTT Control Packet Type is located in the high 4 bits of the first byte of the Fixed Header. It is an unsigned integer that represents the type of the current packet. For example, 1 indicates a **CONNECT** packet, 2 indicates a **CONNACK** packet, and so on. The detailed mapping can be found in the [MQTT 5.0 specification - MQTT Control Packet Types](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022). In fact, except for the MQTT Control Packet Type and Remaining Length fields, the content of the remaining part of the MQTT packet depends on the specific packet type. So, this field determines how the receiver should parse the following content of the packet.

The remaining low 4 bits in the first byte of the Fixed Header contain flags determined by the control packet type. However, as of MQTT 5.0, only the four bits in the **PUBLISH** packet have been assigned specific meanings:

- Bit 3：DUP, indicates whether the current **PUBLISH** packet is a retransmitted packet.
- Bit 2,1：QoS, indicates the quality of service level used by the current **PUBLISH** packet.
- Bit 0：Retain, indicates whether the current **PUBLISH** packet is retained.

In all other packet types, these 4 bits remain reserved, meaning they have a fixed value that cannot be arbitrarily changed.

The final Remaining Length field indicates the number of bytes in the remaining part of the control packet, which includes the Variable Header and the Payload. Therefore, an MQTT control packet's total length is equal to the Fixed Header's length plus the Remaining Length.

![Remaining Length](https://assets.emqx.com/images/32dd746e2ead30c8c50bcf2c84296c1e.png)

#### Variable Byte Integer

However, the length of the Fixed Header is not fixed. In order to minimize the packet size as much as possible, MQTT uses the Remaining Length field as a variable byte integer.

In MQTT, there are many fields of variable length. For example, the Payload part in the **PUBLISH** packet is used to carry the actual application message, and the length of the application message is clearly not fixed. So, we need an additional field to indicate the length of these variable-length contents so that the receiving end can parse them correctly.

For a 2 MB application message, which is a total of 2,097,152 bytes, we would need a 4-byte integer to indicate its length. However, not all application messages are that large; in many cases, they are only a few KB or even just a few bytes. Using a 4-byte integer to indicate a message length of only 2 bytes would be excessive.

Therefore, MQTT introduces variable byte integers, which utilize the lower 7 bits of each byte to encode data, while the highest bit indicates whether there are more bytes to follow. This way, when the packet length is less than 128 bytes, the variable byte integer only needs one byte to indicate. The maximum length of a variable byte integer is 4 bytes, allowing it to indicate a length of up to (2^28 - 1) bytes, which is 256 MB of data.

![Variable Byte Integer](https://assets.emqx.com/images/82d598ea1ac6fd2e87f4feb567a70f47.png)

### Variable Header

The contents of the Variable Header in MQTT depend on the specific packet type. For example, the Variable Header of the **CONNECT** packet includes the Protocol Name, Protocol Level, Connect Flags, Keep Alive, and Properties in that order. The Variable Header of a **PUBLISH** packet includes the Topic name, Packet Identifier (if QoS is not 0), and Properties in that order.

![MQTT Variable Header](https://assets.emqx.com/images/34ee456f79d97ae0bc56c4f3dd4a0ddf.png)

The fields in the Variable Header must strictly follow the protocol specification because the receiver will only parse them in the specified order. We cannot omit any field unless the protocol explicitly requires or allows it. For example, in the Variable Header of the **CONNECT** packet, if the Connect Flags are placed directly after the Protocol Name, it would result in a parsing failure. Similarly, in the Variable Header of the **PUBLISH** packet, the packet identifier is only present when QoS is not 0.

#### Properties

Properties are a concept introduced in MQTT 5.0. They are basically the last part of the Variable Header. The properties consist of the Property Length field followed by a set of properties. The Property Length indicates the total length of all the properties that follow.

![Properties](https://assets.emqx.com/images/d412f11e0265a54cb0432408777ce7cf.png) 

All properties are optional, as they usually have a default value. If there is no property, then the value of the Property Length is 0.

Each property consists of an identifier that defines the purpose and data type of the property and a specific value. Different properties may have different data types. For example, one is a two-byte integer, and another is a UTF-8 encoded string, so we need to parse the properties according to the data type declared by their identifiers.

![Property](https://assets.emqx.com/images/b82cfee353efc201214a8aba609b2e58.png)

The order of properties can be arbitrary because we can know which property it is and its length based on the Identifier.

Properties are typically designed for specific purposes. For example, the **CONNECT** packet has a Session Expiry Interval property to set the session's expiration time. However, this property is not needed in a **PUBLISH** packet. Therefore, MQTT strictly defines the usage scope of properties, and a valid MQTT control packet should not contain properties that do not belong to it.

For a comprehensive list of MQTT properties, including their identifiers, property names, data types, and usage scopes, please refer to [MQTT 5.0 Specification - Properties](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901027).

### Payload

Lastly, we have the Payload. The Variable Header of the packet can be seen as its supplementary information, while the Payload is used to achieve the core purpose of the packet.

For example, in the **PUBLISH** packet, the Payload is used to carry the actual application message, which is the primary function of the **PUBLISH** packet. The QoS, Retain, and other fields in the Variable Header of the **PUBLISH** packet provide additional capabilities related to the application message.

The **SUBSCRIBE** packet follows a similar pattern. The Payload contains the topics to subscribe to and their corresponding subscription options, which is the primary task of the **SUBSCRIBE** packet.

 

## MQTT Packets - Advanced

In the upcoming blog series, we will explore the fields in various MQTT packets and their primary purposes. At the end of each blog, we will provide a real-world example of a packet and illustrate the distribution of these fields within the packet. The blogs include:

- Establish a Connection: **CONNECT** & **CONNACK**
- Publish a Message: **PUBLISH**, **PUBACK**, **PUBREC**, **PUBREL** & **PUBCOMP**
- Subscribe to Topics: **SUBSCRIBE** & **SUBACK**
- Unsubscribe from topics: **UNSUBSCRIBE** & **UNSUBACK**
- Keep Alive: **PINGREQ** & **PINGRESP**
- Disconnect notification: **DISCONNECT**
- Enhanced Authentication: **AUTH**





<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
