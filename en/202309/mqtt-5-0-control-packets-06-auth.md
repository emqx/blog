Welcome to the final article in the [MQTT 5.0 Packet Series](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets). In the previous article, we introduced the [DISCONNECT packet](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-05-disconnect). Now, we will introduce the last control packet in MQTT: AUTH.

MQTT 5.0 introduced the Enhanced Authentication feature, which enables MQTT to support challenge/response style authentication in addition to simple password authentication and token authentication. To achieve this, in addition to the original CONNECT and CONNACK packets, it introduced the AUTH packet to implement any number of authentication data exchanges, to support various types of authentication mechanisms, such as [SCRAM](https://en.wikipedia.org/wiki/Salted_Challenge_Response_Authentication_Mechanism), Kerberos authentication, and so on.

A typical Enhanced Authentication packet interaction process is as follows:

![01enhancedauthenticationflows.png](https://assets.emqx.com/images/3e9d3493b1d75b85af78f1531e864111.png)

For a detailed introduction to Enhanced Authentication, you can refer to [*Leveraging Enhanced Authentication for MQTT Security*](https://www.emqx.com/en/blog/leveraging-enhanced-authentication-for-mqtt-security).

## Sample AUTH Packet

Since there are currently no MQTT clients that support Enhanced Authentication, we will directly illustrate a typical AUTH packet, which includes the two most important Properties in the AUTH packet, namely the Authentication Method and Authentication Data:

![02authpacket.png](https://assets.emqx.com/images/dfb6eee6c1c4ce9013f7beb8fa1f510f.png)

Next, we will introduce the meaning of these fields in turn.

## AUTH Packet Structure

### Fixed Header

In the Fixed Header, the value of the Packet Type field in the first byte's high 4 bits is 15 (0b1111), and the low 4 bits are 0, indicating that this is an AUTH packet.

![03authfixedheader.png](https://assets.emqx.com/images/166e916954e5a35bc295b28dc553a4a5.png)

### Variable Header

The Variable Header of the AUTH packet contains the following fields in order:

- **Reason Code**: A One Byte Unsigned Integer. The AUTH packet only has three available reason codes, all of which are used to control the authentication process:

| **Value** | **Reason Code Name**    | **Sent By**      | **Description**                                              |
| :-------- | :---------------------- | :--------------- | :----------------------------------------------------------- |
| 0x00      | Success                 | Server           | Authentication successful, this will only be returned by the server when re-authentication is successful. When the initial authentication is successful, the server will return the CONNACK packet. |
| 0x18      | Continue authentication | Client or Server | Instruct the peer to continue with the next step of authentication. |
| 0x19      | Re-authenticate         | Client           | The client can re-initiate authentication at any time within a connection. Messages can be sent and received normally during re-authentication. |

- **Properties**: The table below lists all available Properties of the AUTH packet.

| **Identifier** | **Property Name**     | **Type**                                                     | **Description**                                              |
| :------------- | :-------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 0x15           | Authentication Method | UTF-8 Encoded String                                         | Indicates the authentication mechanism used in this authentication. It can be a registered SASL mechanism like SCRAM-SHA-1, or any name negotiated between the client and the server.Once the authentication method is determined in the CONNECT packet, subsequent AUTH, CONNACK packet cannot change it. |
| 0x16           | Authentication Data   | Binary Data (The first two-byte integer indicates the number of subsequent bytes) | Used to carry data required for authentication. The format and content of the data are determined by the authentication method. |
| 0x1F           | Reason String         | UTF-8 Encoded String                                         | Indicates the reason for returning this response. It can be anything, determined by the sender, but preferably human-readable. |
| 0x26           | User Property         | UTF-8 String Pair                                            | Used to append user-defined information to the packet. A packet can contain multiple user properties, even if they have the same name. |

### Payload

The AUTH packet has no Payload.

## Conclusion

The AUTH packet is central to implementing any number of authentication data exchanges, and it also enables MQTT's Enhanced Authentication to support various different authentication mechanisms. Mechanisms like SCRAM authentication, and Kerberos authentication, can provide higher security protection than simple password authentication. Currently, EMQX has already supported [SCRAM authentication](https://www.emqx.io/docs/en/v5.1/access-control/authn/scram.html).

Now, we have introduced all types of control packets in MQTT. As a binary protocol, MQTT allows us to transmit application messages in any format. However, correspondingly, we need to strictly encode and parse MQTT packets according to the protocol specifications, otherwise, it may lead to protocol errors.

When we encounter problems, we can first check the Reason Code in the response packet returned by the other party, which can indicate most of the error causes. When some embedded device end-side SDK implementations are poor and cannot directly provide a Reason Code, we can try packet sniffing to view the Reason Code in the packet. At this time, we can use Wireshark to avoid manual parsing.

[EMQX](https://www.emqx.io/), as a widely used, highly scalable MQTT Broker, also provides a [Log Trace](https://www.emqx.io/docs/en/v5.1/observability/tracer.html) feature that is convenient for users to troubleshoot problems. It can record all relevant logs of specified Client ID, topic, and IP, including packet receiving and sending logs. So we can use it to analyze whether the behavior of the client is abnormal, such as whether it correctly responded to PUBACK, whether it repeatedly sent CONNACK packets, etc.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
