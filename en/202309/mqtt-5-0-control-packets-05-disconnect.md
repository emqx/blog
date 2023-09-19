Welcome to the fifth article in the [MQTT 5.0 Packet Series](https://www.emqx.com/en/blog/Introduction-to-mqtt-control-packets). In the previous article, we introduced the [PINGREQ and PINGRESP packets](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-04-pingreq-pingresp) in MQTT 5.0. Now, we will introduce the control packet used when disconnecting: DISCONNECT.

In MQTT, both the client and the server can send a DISCONNECT packet to the other party before disconnecting the network connection, indicating the reason for the connection closure. The DISCONNECT packet sent by the client can also affect the behavior of the server after the connection is disconnected, such as whether to send a will message, or whether to update the Session Expiry Interval.

## Sample DISCONNECT Packet

We use the [MQTTX CLI](https://mqttx.app/) to initiate a client connection with a specified Client ID to the [Public MQTT Server](http://broker.emqx.io), and set `--reconnect-period` to 0 to disable automatic reconnection, and then run the same command in another terminal to create a client connection using the same Client ID.

The entire process uses [Wireshark](https://www.wireshark.org/) to capture the MQTT packets traveling between the client and the server. In Linux, you can use [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) to capture the packets and then import them to Wireshark for viewing.

The following command will create a client connection with the Client ID `mqtt-892324`. In order to avoid repeating the Client ID with others, it is recommended to change it to another random string:

```bash
mqttx conn --hostname broker.emqx.io --mqtt-version 5 --client-id mqtt-892324 \ --reconnect-period 0
```

After we initiate the second connection, Wireshark will capture the DISCONNECT packet returned by the Public MQTT Server to the first connection:

```
e0 02 8e 00
```

These four hexadecimal bytes correspond to the following packet content:

![01disconnectpacket.png](https://assets.emqx.com/images/ed0592c988b7fc7869dae227a431a053.png)

Through the following introduction to the DISCONNECT packet, you will learn how to extract the information you want from the original packet data.

## DISCONNECT Packet Structure

### Fixed Header

The value of the Packet Type field located in the high 4 bits of the first byte of the Fixed Header is 14 (0b1110), and the low 4 bits are all 0, indicating that this is a DISCONNECT packet.

![02disconnectfixedheader.png](https://assets.emqx.com/images/3164fc20dfc619af9be401e63e0459c8.png)

### Variable Header

The Variable Header of the DISCONNECT packet contains the following fields in order:

![03disconnectvariableheader.png](https://assets.emqx.com/images/11124887504b81d0004c4bd90484066c.png)

- Reason Code: A Single-Byte value, is used to indicate the reason for the disconnection to the other end. The table below lists the common Reason Codes in DISCONNECT packets. For a complete list, please refer to the [MQTT 5.0 Reason Code Quick Reference Guide](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack).

| **Value** | **Reason Code Name**         | **Sent By**      | **Description**                                              |
| :-------- | :--------------------------- | :--------------- | :----------------------------------------------------------- |
| 0x00      | Normal disconnection         | Client or Server | The connection was closed normally, so the server will not publish the will message. |
| 0x04      | Disconnect with Will Message | Client           | The connection was closed normally, but the client still expects the server to publish the will message. |
| 0x81      | Malformed Packet             | Client or Server | The received packet cannot be correctly parsed according to the protocol specifications, in MQTT we refer to these types of packets as malformed packets. |
| 0x82      | Protocol Error               | Client or Server | Protocol errors usually refer to errors that can be discovered only after the control packet is parsed according to the protocol specifications, including data that the protocol does not allow, behavior that does not conform to the protocol requirements, and so on. For example, the client sends two CONNECT packets within a single connection. |
| 0x8D      | Keep Alive timeout           | Server           | The server closed the connection because it did not receive any packets within 1.5 times the Keep Alive time. |
| 0x8E      | Session taken over           | Server           | Another more recent connection using the same Client ID was established, causing the server to close this connection. |
| 0x93      | Receive Maximum exceeded     | Client or Server | The number of QoS > 0 PUBLISH messages sent simultaneously by the peer exceeds the maximum receive value set when connecting. |
| 0x94      | Topic Alias invalid          | Client or Server | The Topic Alias is invalid. For example, the value of Topic Alias in the PUBLISH packet is 0 or greater than the maximum Topic Alias agreed upon at the time of connection. |
| 0x95      | Packet too large             | Client or Server | The packet exceeds the maximum allowable size agreed upon at the time of connection. |
| 0x98      | Administrative action        | Client or Server | The connection was closed due to a management operation, such as an administrator kicking out the client connection in the background. |
| 0x9C      | Use another server           | Server           | The client should **temporarily** switch to another server. If another server is not known to the client, it needs to be used together with the Server Reference property to inform the client of the address of the new server. |
| 0x9D      | Server moved                 | Server           | The client should **permanently** switch to another server. If another server is not known to the client, it needs to be used together with the Server Reference property to inform the client of the address of the new server. |

- Properties: The table below lists all available properties of the CONNECT packet.

| **Identifier** | **Property Name**                                            | **Sent By**      | **Type**             |
| :------------- | :----------------------------------------------------------- | :--------------- | :------------------- |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | Client           | Four Byte Integer    |
| 0x1F           | Reason String                                                | Client or Server | UTF-8 Encoded String |
| 0x26           | User Property                                                | Client or Server | UTF-8 String Pair    |
| 0x1C           | Server Reference                                             | Server           | UTF-8 Encoded String |

Different from other packets introduced before, the Reason Codes and Properties that can be used by the client and the server in the DISCONNECT packet are different. For example, the Session Expiry Interval property can only be used in the DISCONNECT packet sent by the client, so we've included their available range in the list above.

### Payload

The DISCONNECT packet has no Payload.

## Conclusion

Both the client and the server can send the DISCONNECT packet to indicate that they are ready to disconnect from the network. The Reason Code in the packet can indicate to the receiver the reason why the connection is closed. When the MQTT connection is disconnected unexpectedly, we can first check whether the DISCONNECT packet is received and the value of the Reason Code in the packet.

Although there are differences in the Reason Codes and Properties that can be used by the client and server in the DISCONNECT packet, we don't need to forcibly remember them. They are usually related to the corresponding mechanisms and behaviors. For example, the Will Message will only be published by the server, so the reason code `0x04`, which is used when there is a wish for normal closure of the connection but the counterpart still needs to publish the Will Message, will only be used by the client.

The above is an introduction to the DISCONNECT packet. In the next article, we will introduce the AUTH packet used by the Enhanced Authentication feature of MQTT 5.0, which is also the last packet type in MQTT.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
