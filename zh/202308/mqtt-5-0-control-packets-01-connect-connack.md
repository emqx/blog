在 [MQTT 5.0 报文介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets) 中，我们介绍了 MQTT 报文由固定报头、可变报头和有效载荷三个部分组成，以及可变字节整数、属性这类 MQTT 报文中的通用概念。现在，我们将按照实际的用途来进一步介绍各个类型的报文的组成。首先，我们将专注于用于建立 MQTT 连接的报文。

如果我们想要使用 MQTT 进行通信，第一步必然是建立一个 MQTT 连接，而建立 MQTT 连接需要用到两个控制报文，它们分别是 CONNECT 报文与 CONNACK 报文。CONNECT 报文是客户端与服务端建立网络连接后，向服务端发送的第一个控制报文，用来发起连接请求。服务端将返回 CONNACK 报文告知客户端连接结果。

## 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](http://broker.emqx.io/) 发起一个连接，在这个连接中，我们将协议版本设置 MQTT 5.0，Clean Start 设置为 1，Session Expiry Interval 设置为 300 秒，Keep Alive 设置为 60，用户名和密码分别设置为 admin 和 public，对应的 MQTTX CLI 命令为：

```
mqttx conn --hostname broker.emqx.io --mqtt-version 5 \  --session-expiry-interval 300 --keepalive 60 --username admin --password public
```

以下是使用 [Wireshark](https://www.wireshark.org/) 工具抓取到的 MQTTX CLI 发出的 CONNECT 报文，Linux 环境可以先使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后再导入至 Wireshark 查看：

```
10 2f 00 04 4d 51 54 54 05 c2 00 3c 05 11 00 00 01 2c 00 0e 6d 71 74 74 78 5f 30 63 36 36 38 64 30 64 00 05 61 64 6d 69 6e 00 06 70 75 62 6c 69 63
```

但这是一串不易理解的十六进制字节，除非它们被转换成以下格式：

![01connectpacket.png](https://assets.emqx.com/images/5bfa9c0f882d9381c5f3d8a0bbb669de.png)

同样我们也抓取到了公共 MQTT 服务器返回的 CONNACK 报文：

```
20 13 00 00 10 27 00 10 00 00 25 01 2a 01 29 01 22 ff ff 28 01
```

在解析这串报文数据之后我们可以看到，CONNACK 报文的 Reason Code 为 0，表示连接成功，后面的多个属性则给出了服务器支持的功能列表，比如支持的最大报文长度，是否支持保留消息等等：

![02connackpacket.png](https://assets.emqx.com/images/6dec28d47b60d2c2bc4d98b7944f78be.png)

当然，Wireshark 其实也已经为我们列出了报文中各个字段的值，通过下文对 CONNECT 和 CONNACK 报文结构的介绍，再结合 Wireshark 的抓包结果按图索骥，你将很快掌握这两个报文：

![03wireshark.png](https://assets.emqx.com/images/22ca21103a6d415bc0c7f2927ea51005.png)

## CONNECT 报文结构

### 固定报头

CONNECT 报文的固定报头中，位于首字节高 4 位的报文类型字段的值必须为 1（0b0001），首字节中低 4 位则固定全为 0。

所以，CONNECT 报文的第一个字节的值必然为 `0x10`，我们可以以此来判断某个报文是否为 CONNECT 报文。

![MQTT CONNECT 固定报头](https://assets.emqx.com/images/f5f7d0b8da9a606ed6de114761bd36aa.png)

### 可变报头

CONNECT 报文的可变报头按顺序包含以下字段：

![MQTT CONNECT 可变报头](https://assets.emqx.com/images/0020fe00d5b190ea80bf6a080e387561.png)

- **Protocol Name**：这是一个 UTF-8 编码的字符串，用来表示协议名称。在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，UTF-8 编码的字符串的前两个字节统一用于指示后面实际的字符数据的长度。MQTT 3.1.1 和 MQTT 5.0 中协议名称固定为 `MQTT`，所以对应的以十六进制字节表示的完整内容就是 `00 04 4d 51 54 54`，其中 `4d 51 54 54` 就是 `MQTT` 这个字符串对应的 ASCII 值。最早的 MQTT 3.1 中的协议名称是 `MQIsdp`，所以它对应的是 `00 06 4d 51 49 73 64 70`。

- **Protocol Version**：这是一个单个字节长度的无符号整数，用来表示协议版本。目前只有三个可取值，3 表示 MQTT 3.1，4 表示 MQTT 3.1.1，5 表示 MQTT 5.0。

- **Connect Flags**：连接标识，它只有一个字节，但包含了多个用于控制连接行为或指示有效载荷中某些字段是否存在的参数。

   ![MQTT Connect Flags](https://assets.emqx.com/images/ed67e14a6cde03513aa3ae9be7e51c96.png)

  - **User Name Flag**：用于指示有效载荷是否包含用户名字段。

  - **Password Flag**：用于指示有效载荷是否包含密码字段。

  - [**Will Retain**](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)：用于指示遗嘱消息是否为保留消息。

  - **Will QoS**：用于指示遗嘱消息的 QoS。

  - **Will Flag**：用于指示有效载荷是否包含了遗嘱消息的相关字段。

  - **Clean Start**：用于指示当前连接是一个新的会话还是一个已存在会话的延续，这决定了服务端将直接新建会话还是尝试复用已存在的会话。

  - **Reserved**：这是一个保留位，它的值必须为 0。

- [**Keep Alive**](https://www.emqx.com/zh/blog/mqtt-keep-alive)：这是一个双字节长度的无符号整数，用来表示客户端发送两个相邻的控制报文的最大时间间隔。

- **Properties**：下表列出了 CONNECT 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| -------------- | ------------------------------------------------------------ | ------------------ |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | 四字节整数         |
| 0x21           | [Receive Maximum](https://www.emqx.com/zh/blog/mqtt5-flow-control) | 双字节整数         |
| 0x27           | Maximum Packet Size                                          | 四字节整数         |
| 0x22           | [Topic Alias Maximum](https://www.emqx.com/zh/blog/mqtt5-topic-alias) | 双字节整数         |
| 0x19           | Request Response Information                                 | 单字节             |
| 0x17           | Request Problem Information                                  | 单字节             |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |
| 0x15           | [Authentication Method](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security) | UTF-8 编码的字符串 |
| 0x16           | [Authentication Data](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security) | 二进制数据         |

### 有效载荷

CONNECT 报文有效载荷中的字段，除了 Client ID 以外，其他字段都是可选的，它们是否存在取决于可变报头的 Connect Flags 中对应标志位的值。但如果这些存在，就必须按照 Client ID、Will Properties、Will Topic、Will Payload、User Name、Password 的顺序出现。

![MQTT 有效载荷](https://assets.emqx.com/images/68a6d281897967d7c89532fbfd6c759e.png)

## CONNACK 报文结构

### 固定报文

固定报头中首字节的高 4 位值为 2（0b0010），表示这是一个 CONNACK 报文。

![MQTT CONNACK 固定报文](https://assets.emqx.com/images/7e64f21fa3f6e1fe20a463b3f451eaf5.png)

### 可变报头

CONNACK 报文的可变报头按顺序包含以下字段：

![MQTT CONNACK 可变报头](https://assets.emqx.com/images/78dd06c5cf2a69493a935e21c1457d2c.png)

- Connect Acknowledge Flags：连接确认标志。

  - Reserved (Bit 7 - 1)：保留位，必须设置为 0.

  - **Session Present (Bit 0)**：用于指示服务端是否正在使用已存在的会话与客户端恢复通信。仅在客户端在 CONNECT 连接中将 Clean Start 设置为 0 时，Session Present 可能为 1。

- **Reason Code**：用于指示连接结果。下表列出了一些在 CONNACK 报文中常见的 Reason Code，完整列表可参阅 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)。

| **Value** | **Reason Code Name**         | **Description**                                              |
| :-------- | :--------------------------- | :----------------------------------------------------------- |
| 0x00      | Success                      | 连接被接受。                                                 |
| 0x81      | Malformed Packet             | 服务端无法按照协议规范正确解析 CONNECT 报文，例如保留位没有按照协议要求设置为 0。 |
| 0x82      | Protocol Error               | CONNECT 报文可以被正确解析，但是内容不符合协议规范，比如 Will Topic 字段的值不是一个合法的 MQTT 主题。 |
| 0x84      | Unsupported Protocol Version | 服务端不支持客户端所请求的 MQTT 协议版本。                   |
| 0x85      | Client Identifier not valid  | 表示 Client ID 是有效的字符串，但是不被服务端接受，比如 Client ID 超出了服务端允许的最大长度。 |
| 0x86      | Bad User Name or Password    | 客户端因为使用了错误的用户名或密码而被拒绝连接。             |
| 0x95      | Packet too large             | CONNECT 报文超过了服务端允许的最大长度，可能是因为携带了较大的遗嘱消息。 |
| 0x8A      | Banned                       | 表示客户端被禁止登录。例如服务端检测到客户端的异常连接行为，所以将这个客户端的 Client ID 或者 IP 地址加入到了黑名单列表中，又或者是后台管理人员手动封禁了这个客户端，当然以上这些通常需要视服务端的具体实现而定。 |

- **Properties**：下表列出了 CONNACK 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| -------------- | ------------------------------------------------------------ | ------------------ |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | 四字节整数         |
| 0x21           | [Receive Maximum](https://www.emqx.com/zh/blog/mqtt5-flow-control) | 双字节整数         |
| 0x24           | Maximum QoS                                                  | 单字节             |
| 0x25           | Retain Available                                             | 单字节             |
| 0x27           | Maximum Packet Size                                          | 四字节整数         |
| 0x12           | Assigned Client Identifier                                   | UTF-8 编码的字符串 |
| 0x22           | [Topic Alias Maximum](https://www.emqx.com/zh/blog/mqtt5-topic-alias) | 双字节整数         |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |
| 0x28           | Wildcard Subscription Available                              | 单字节             |
| 0x29           | Subscription Identifier Available                            | 单字节             |
| 0x2A           | Shared Subscription Available                                | 单字节             |
| 0x13           | Server Keep Alive                                            | 双字节整数         |
| 0x1A           | Response Information                                         | UTF-8 编码的字符串 |
| 0x1C           | Server Reference                                             | UTF-8 编码的字符串 |
| 0x15           | [Authentication Method](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security) | UTF-8 编码的字符串 |
| 0x16           | [Authentication Data](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security) | 二进制数据         |

### 有效载荷

CONNACK 报文不包含有效载荷。

## 总结

CONNECT 是客户端与服务端的网络连接建立后，客户端发送的第一个 MQTT 报文，CONNACK 作为 CONNECT 的响应报文通过原因码来指示连接结果。

客户端和服务端需要借助 CONNECT 和 CONNACK 报文来完成必要信息的交换，例如客户端使用的协议版本、Client ID、用户名、密码，以及服务端是否存在相应的会话、支持的最大报文长度和最大 QoS 等级等等。

以上就是对 MQTT CONNECT 和 CONNACK 报文的介绍，在后续的文章中，我们还会继续研究 PUBLISH、DISCONNECT 这些报文的结构和组成。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
