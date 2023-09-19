欢迎阅读 [MQTT 5.0 报文系列](https://www.emqx.com/zh/blog/Introduction-to-mqtt-control-packets) 的第二篇文章。在上一篇中，我们已经介绍了 [MQTT 5.0 的 CONNECT 和 CONNACK 报文](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-01-connect-connack)。现在，我们将介绍在 MQTT 中用于传递应用消息的 PUBLISH 报文以及它的响应报文。

不管是客户端向服务端发布消息，还是服务端向订阅端转发消息，都需要使用 PUBLISH 报文。决定消息流向的主题、消息的实际内容和 QoS 等级，都包含在 PUBLISH 报文中。

客户端与服务端在消息传递的过程中，除了 PUBLISH 报文，还会用到 PUBACK、PUBREC、PUBREL、PUBCOMP 这四个报文，它们分别用于实现 MQTT 的 QoS 1 和 QoS 2 消息机制。在本文中，我们将深入研究这五个报文的组成。

## 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](http://broker.emqx.io/) 发布三条不同 QoS 等级的消息，并使用 [Wireshark](https://www.wireshark.org/) 工具抓取在客户端与服务器之间往返的 MQTT 报文，Linux 环境可以使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后导入至 Wireshark 分析。

以下是本示例使用的 MQTTX CLI 命令，为了展示 PUBLISH 报文的属性字段，命令中还设置了 Message Expiry Interval 和 Response Topic 属性：

```
mqttx pub --hostname broker.emqx.io --mqtt-version 5 \  --topic request --qos 0 --message "This is a QoS 0 message" \  --message-expiry-interval 300 --response-topic response
```

以下是 Wireshark 抓取到的 MQTTX CLI 发出的 QoS 为 0 的 PUBLISH 报文：

```
30 31 00 07 72 65 71 75 65 73 74 10 02 00 00 01 2c 08 00 08 72 65 73 70 6f 6e 73 65 54 68 69 73 20 69 73 20 61 20 51 6f 53 20 30 20 6d 65 73 73 61 67 65
```

这串十六进制字节，对应以下报文内容：

![01publishpacket.png](https://assets.emqx.com/images/6c9b3ed2947093241f0864ee408431c6.png)

而当我们仅修改 MQTTX CLI 命令中的 QoS 选项，将消息的 QoS 等级设置为 1，我们将看到服务端在收到 PUBLISH 后回复了 PUBACK 报文，他们的报文数据分别为：

```
Client  -- PUBLISH (32 33 00 .. ..)    ->  Server
Client  <- PUBACK  (40 04 64 4a 10 00) --  Server
```

此时 PUBLISH 报文中第一个字节从 0x30 变成了 0x32，表示这是一条 QoS 1 消息。

PUBACK 的报文结构比较简单，可以看到 Reason Code 为 `0x10`，表示消息被接收，但是没有匹配的订阅者。一旦有人订阅了 `request` 主题，那么 PUBACK 报文中的 Reason Code 就会变成 `0x00`，即消息被接收，且存在匹配的订阅者。

![02pubackpacket.png](https://assets.emqx.com/images/b29eb054e5351e9bc5c66a78818ea052.png)

继续使用 MQTTX CLI 发布一条 QoS 2 消息，我们将看到客户端和服务端之间发生了两次报文往返，Wireshark 会告诉我们，这些报文分别是 PUBLISH、PUBREC、PUBREL 以及 PUBCOMP，并且它们拥有相同的报文标识符 `0x11c2`：

```
Client  -- PUBLISH (34 33 00 .. ..)    ->  Server
Client  <- PUBREC  (50 04 11 c2 10 00) --  Server
Client  -- PUBREL  (62 03 11 c2 00)    ->  Server
Client  <- PUBCOMP (70 04 11 c2 00 00) --  Server
```

如何从由十六进制字节组成的报文数据中准确地知道这是否是一个 PUBLISH 报文，它的 QoS 是多少，它的响应报文中的原因码又是多少，接下来对这些报文的介绍将会回答这些问题。

## PUBLISH 报文结构

### 固定报头

PUBLISH 报文的固定报头中，首字节的高 4 位的值固定为 3（0b0011），低 4 位则由以下三个字段组成：

- DUP（Bit 3）：客户端或服务端在重传 PUBLISH 报文时，需要将 DUP 标志设置为 1，表示这是一个重传的报文。收到 DUP 为 1 的 PUBLISH 报文的数量和频率可以为我们揭示当前通信链路的质量。
- QoS（Bit 2 - 1）：用于指定消息的 QoS 等级。
- Retain（Bit 0）：设置为 1，表示当前消息是 [保留消息](https://www.emqx.com/zh/blog/mqtt5-features-retain-message)；设置为 0，则表示当前消息是普通的消息。

紧随其后的是剩余长度（Remaining Length）字段，指示了当前报文剩余部分的字节数。

![PUBLISH 报文结构](https://assets.emqx.com/images/69b9d59e40ce662856b5e4ac7e40e8c0.png)

### 可变报头

PUBLISH 报文的可变报头按顺序包含以下字段：

- **主题名**（Topic Name）：这是一个 UTF-8 编码的字符串，用来指示消息应该被发布到哪一个信息通道。
- **报文标识符**（Packet Identifier）：这是一个两个字节长度的无符号整数，用来唯一地标识当前正在传输的消息，只有在 QoS 等级为 1 或 2 时，报文标识符才会出现在 PUBLISH 报文中。
- **属性**（Properties）：下表列出了 PUBLISH 报文的所有可用属性，这里我们不再额外花费篇幅具体介绍每个属性的用途，你可以点击属性名以查看对应的博客：

| **Identifier** | **Property Name**                                            | **Type**           |
| :------------- | :----------------------------------------------------------- | :----------------- |
| 0x01           | [Payload Format Indicator](https://www.emqx.com/zh/blog/mqtt5-new-features-payload-format-indicator-and-content-type) | 单字节             |
| 0x02           | [Message Expiry Interval](https://www.emqx.com/zh/blog/mqtt-message-expiry-interval) | 四字节整数         |
| 0x23           | [Topic Alias](https://www.emqx.com/zh/blog/mqtt5-topic-alias) | 双字节整数         |
| 0x08           | [Response Topic](https://www.emqx.com/zh/blog/mqtt5-request-response) | UTF-8 编码的字符串 |
| 0x09           | [Correlation Data](https://www.emqx.com/zh/blog/mqtt5-request-response) | 二进制数据         |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |
| 0x0B           | [Subscription Identifier](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options) | 变长字节整数       |
| 0x03           | [Content Type](https://www.emqx.com/zh/blog/mqtt5-new-features-payload-format-indicator-and-content-type) | UTF-8 编码的字符串 |

### 有效载荷

我们发送的应用消息的实际内容，就存放在 PUBLISH 报文的有效载荷中，它可以承载任意格式的应用消息，比如 JSON、ProtoBuf 等等。

## PUBACK 报文结构

### 固定报头

固定报头中首字节的高 4 位的值固定为 4（0b0100），表示这是一个 PUBACK 报文，低 4 位是保留位，固定全部为 0。

紧随其后的是剩余长度（Remaining Length）字段，指示了当前报文剩余部分的字节数。

![PUBACK 报文结构](https://assets.emqx.com/images/a11c4f97ac97b147511f43f6496b55e6.png)

### 可变报头

PUBACK 报文的可变报头按顺序包含以下字段：

- **报文标识符**（Packet Identifier）：与 PUBLISH 报文不同，PUBACK 报文中的报文标识符必须存在，它用于向对端指示这是对哪一个 QoS 为 1 的 PUBLISH 报文的响应。
- **原因码**（Reason Code）：这是一个单字节的无符号整数，用于向 PUBLISH 报文的发布端指示发布结果，比如是否因为未授权而被拒绝发布。下表列出了PUBACK 报文所有可用的 Reason Code：

| **Value** | **Reason Code Name**          | **Description**                                              |
| :-------- | :---------------------------- | :----------------------------------------------------------- |
| 0x00      | Success                       | 消息被接受。                                                 |
| 0x10      | No matching subscribers       | 消息被接受，但是当前没有匹配的订阅者。                       |
| 0x80      | Unspecified error             | 表示未指明的错误。当一方不希望向另一方透露错误的具体原因，或者协议规范中没有能够匹配当前情况的 Reason Code 时，那么它将在报文中使用这个 Reason Code。 |
| 0x83      | Implementation specific error | PUBLISH 报文有效，但是不被当前接收方的实现所接受。           |
| 0x87      | Not authorized                | PUBLISH 报文没有通过服务端的权限检查，可能是因为当前客户端不具备向对应主题发布消息的权限。 |
| 0x90      | Topic Name invalid            | 主题名的格式正确，但是不被接收端接受。                       |
| 0x91      | Packet identifier in use      | PUBLISH 报文中的 Packet ID 正在被使用，这通常意味着客户端和服务端的会话状态不匹配，或者有一方的实现不正确。 |
| 0x97      | Quota exceeded                | 表示超出了配额限制。服务端可能会对发布端的发送配额进行限制，比如每天最多为其转发 1000 条消息。当发布端的配额耗尽，服务端就会在 PUBACK 等确认报文中使用这个 Reason Code 提醒对方。 |
| 0x99      | Payload format invalid        | 表示有效载荷的格式与 Payload Format Indicator 属性所指示的格式不匹配。 |

- **属性**（Properties）：下表列出了 PUBACK 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| :------------- | :----------------------------------------------------------- | :----------------- |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |

### 有效载荷

PUBACK 报文不包含有效载荷。

## PUBREC、PUBREL、PUBCOMP 报文结构

PUBREC、PUBREL 和 PUBCOMP 的报文结构与 PUBACK 基本一致，它们的区别主要在于固定报头中报文类型字段的值，以及可以使用的原因码。 

报文类型字段的值为 5（0b0101），表示这是一个 PUBREC 报文；值为 6（0b0110），则表示这是一个 PUBREL报文；值为 7（0b0111），则表示这是一个 PUBCOMP 报文。

PUBREC 作为 QoS 2 消息流程中对 PUBLISH 报文的确认报文，它可以使用的原因码与 PUBACK 完全一致。PUBREL 和 PUBCOMP 报文可用的原因码如下：

| **Identifier** | **Reason Code Name**        | **Description**                                              |
| :------------- | :-------------------------- | :----------------------------------------------------------- |
| 0x00           | Success                     | 由 QoS 2 消息的发送端在 PUBREL 报文中返回时，表示消息已经被释放，即之后将不会再重传该消息。由 QoS 2 消息的接收端在 PUBREC 报文中返回时，表示消息中使用的**报文标识符**已经释放，现在发送端可以使用该报文标识符发送新的消息。 |
| 0x92           | Packet Identifier not found | 表示收到了未知的报文标识符，这通常意味着当前服务端和客户端的会话状态不匹配。 |

## 总结

PUBLISH 报文中的**主题**决定了消息的流向，**QoS** 则决定了消息的可靠性，同时也决定了传输时将用到哪些报文，PUBACK 报文用于 QoS 1 消息，PUBREC、PUBREC 和 PUBCOMP 报文用于 QoS 2 消息。QoS 大于 0 时报文中还需要包含报文标识符来关联 PUBLISH 报文和它的响应报文。

PUBLISH 报文的**有效载荷**不限制数据类型，所以我们可以传输任意格式的应用消息。另外，**属性**可以满足我们在更多场景下的需要，比如主题别名可以减少每个消息的大小，消息过期间隔可以为有时效性的消息设置过期时间等等。

PUBLISH 报文的**响应报文**除了向发送端指示消息被接收以外，还能通过 Reason Code 进一步指示发布结果。所以当订阅端迟迟无法收到消息，我们还可以通过发布端收到的响应报文中的原因码来排查问题。

以上就是对 MQTT PUBLISH 及其响应报文的介绍，在下一篇文章中，我们将继续研究订阅和取消订阅报文的结构和组成。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
