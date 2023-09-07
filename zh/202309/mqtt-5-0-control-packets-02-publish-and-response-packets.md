在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，PUBLISH 报文用于传递应用消息。不管是客户端向服务端发布消息，还是服务端向订阅端转发消息，都需要使用 PUBLISH 报文。决定消息流向的主题、消息的实际内容和 QoS 等级，都包含在 PUBLISH 报文中。

客户端与服务端在消息传递的过程中，除了 PUBLISH 报文，还会用到 PUBACK、PUBREC、PUBREL、PUBCOMP 这四个报文，它们分别用于实现 MQTT 的 QoS 1 和 QoS 2 消息机制。在本文中，我们将深入研究这五个报文的组成。

## PUBLISH 报文结构

### 固定报头

PUBLISH 报文的固定报头中，首字节的高 4 位的值固定为 3，低 4 位则由以下三个字段组成：

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

固定报头中首字节的高 4 位的值固定为 4，表示这是一个 PUBACK 报文，低 4 位是保留位，固定全部为 0。

紧随其后的是剩余长度（Remaining Length）字段，指示了当前报文剩余部分的字节数。

![PUBACK 报文结构](https://assets.emqx.com/images/a11c4f97ac97b147511f43f6496b55e6.png)

### 可变报头

PUBACK 报文的可变报头按顺序包含以下字段：

- **报文标识符**（Packet Identifier）：与 PUBLISH 报文不同，PUBACK 报文中的报文标识符必须存在，它用于向对端指示这是对哪一个 QoS 为 1 的 PUBLISH 报文的响应。
- **原因码**（Reason Code）：这是一个单字节的无符号整数，用于向 PUBLISH 报文的发布端指示发布结果，比如是否因为未授权而被拒绝发布。下表列出了一些在 PUBACK 报文中常见的 Reason Code，完整列表可参阅 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)。

| **Value** | **Reason Code**          | **Description**                                              |
| :-------- | :----------------------- | :----------------------------------------------------------- |
| 0x00      | Success                  | 消息被接受。                                                 |
| 0x10      | No matching subscribers  | 消息被接受，但是当前没有匹配的订阅者。                       |
| 0x87      | Not authorized           | PUBLISH 报文没有通过服务端的权限检查，可能是因为当前客户端不具备向对应主题发布消息的权限。 |
| 0x91      | Packet identifier in use | PUBLISH 报文中的 Packet ID 正在被使用，这通常意味着客户端和服务端的会话状态不匹配，或者有一方的实现不正确。 |

- **属性**（Properties）：下表列出了 PUBACK 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| :------------- | :----------------------------------------------------------- | :----------------- |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |

### 有效载荷

PUBACK 报文不包含有效载荷。

## PUBREC、PUBREL、PUBCOMP 报文结构

PUBREC、PUBREL 和 PUBCOMP 的报文结构与 PUBACK 基本一致，它们的区别主要在于固定报头中报文类型字段的值，以及可以使用的原因码。 

报文类型字段的值为 5，表示这是一个 PUBREC 报文；值为 6，则表示这是一个 PUBREL报文；值为 7，则表示这是一个 PUBCOMP 报文。

## 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)发布三条不同 QoS 等级的消息，并使用 [Wireshark](https://www.wireshark.org/) 工具抓取在客户端与服务器之间往返的 MQTT 报文，Linux 环境可以使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后导入至 Wireshark 分析。

以下是本示例使用的 MQTTX CLI 命令，为了展示 PUBLISH 报文的属性字段，命令中还设置了 Message Expiry Interval 和 Response Topic 属性：

```
mqttx pub --hostname broker.emqx.io --mqtt-version 5 \
  --topic request --qos 0 --message "This is a QoS 0 message" \
  --message-expiry-interval 300 --response-topic response
```

以下是 Wireshark 抓取到的 MQTTX CLI 发出的 QoS 为 0 的 PUBLISH 报文：

![QoS 为 0 的 PUBLISH 报文](https://assets.emqx.com/images/bbeac19654e55b098bf68e7de2b8c49a.png)

```
30 31 00 07 72 65 71 75 65 73 74 10 02 00 00 01 2c 08 00 08
72 65 73 70 6f 6e 73 65 54 68 69 73 20 69 73 20 61 20 51 6f
53 20 30 20 6d 65 73 73 61 67 65
```

第一个字节 0x30 的高 4 位的值为 3，表示这是一个 PUBLISH 报文，因此按照前面介绍的 PUBLISH 报文的结构，我们可以解析得到以下内容：

![报文解析结果](https://assets.emqx.com/images/537a82370c0d6e34ec3e2eb43da06d38.png)

而当我们仅修改 MQTTX CLI 命令中的 QoS 选项，将消息的 QoS 等级设置为 1，我们将看到服务端在收到 PUBLISH 后回复了 PUBACK 报文，他们的报文数据分别为：

```
Client  -- PUBLISH (32 33 00 .. ..)    ->  Server
Client  <- PUBACK  (40 04 64 4a 10 00) --  Server
```

注意此时 PUBLISH 报文中第一个字节的低 4 位的值为 2，所以这是一条 QoS 1 消息。

PUBACK 的报文结构比较简单，可以看到位于第 5 个字节的 Reason Code 值为 `0x10`，表示消息被接收，但是没有匹配的订阅者。由于我们使用的是公共服务器，所以如果有其他人订阅了 `request` 主题，那么 PUBACK 报文中的 Reason Code 就会变成 `0x00`。

![PUBACK 的报文结构](https://assets.emqx.com/images/dd4de263b508fe88663fa04c11a6f95f.png)

继续使用 MQTTX CLI 发布一条 QoS 2 消息，我们将看到客户端和服务端之间发生了两次报文往返，而根据报文首字节的高 4 位我们可以知道，这些报文分别是 PUBLISH、PUBREC、PUBREL 以及 PUBCOMP，并且它们拥有相同的报文标识符 `0x11c2`：

```
Client  -- PUBLISH (34 33 00 .. ..)    ->  Server
Client  <- PUBREC  (50 04 11 c2 10 00) --  Server
Client  -- PUBREL  (62 03 11 c2 00)    ->  Server
Client  <- PUBCOMP (70 04 11 c2 00 00) --  Server
```

以上就是对 MQTT PUBLISH 及其响应报文的介绍，在下一篇文章中，我们将继续研究订阅和取消订阅报文的结构和组成。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
