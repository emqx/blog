建立 MQTT 连接需要用到两个控制报文，分别是 CONNECT 报文与 CONNACK 报文。CONNECT 报文是客户端与服务端建立网络连接后，向服务端发送的第一个控制报文，用来发起连接请求。服务端将返回 CONNACK 报文告知客户端连接结果。在本文中，我们将深入研究这两个报文的结构。

## CONNECT 报文结构

### 固定报头

CONNECT 报文的固定报头中，位于首字节高 4 位的报文类型字段的值必须为 1，首字节中低 4 位则固定全为 0。

所以，CONNECT 报文的第一个字节的值必然为 `0x10`，我们可以以此来判断某个报文是否为 CONNECT 报文。

![MQTT CONNECT 固定报头](https://assets.emqx.com/images/08cdf8ff00ffbb808d3d399be545a245.png)

### 可变报头

CONNECT 报文的可变报头按顺序包含以下字段：

![MQTT CONNECT 可变报头](https://assets.emqx.com/images/67882a45ba2a35b791f59a51bd8d9aae.png)

- **Protocol Name**：这是一个 UTF-8 编码的字符串，用来表示协议名称。在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，UTF-8 编码的字符串的前两个字节统一用于指示后面实际的字符数据的长度。MQTT 3.1.1 和 MQTT 5.0 中协议名称固定为 `MQTT`，所以对应的以十六进制字节表示的完整内容就是 `00 04 4d 51 54 54`，其中 `4d 51 54 54` 就是 `MQTT` 这个字符串对应的 ASCII 值。最早的 MQTT 3.1 中的协议名称是 `MQIsdp`，所以它对应的是 `00 06 4d 51 49 73 64 70`。

- **Protocol Version**：这是一个单个字节长度的无符号整数，用来表示协议版本。目前只有三个可取值，3 表示 MQTT 3.1，4 表示 MQTT 3.1.1，5 表示 MQTT 5.0。

- **Connect Flags**：连接标识，它只有一个字节，但包含了多个用于控制连接行为或指示有效载荷中某些字段是否存在的参数。

   ![MQTT Connect Flags](https://assets.emqx.com/images/1fd83053e697fff76251dca90258cf52.png)

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

![MQTT 有效载荷](https://assets.emqx.com/images/3c0b5c81ff42ca4681e70aef4531a32c.png)

## CONNACK 报文结构

### 固定报文

固定报头中首字节的高 4 位值为 2，表示这是一个 CONNACK 报文。

![MQTT CONNACK 固定报文](https://assets.emqx.com/images/7cd9650b420a7be8028a2f751dd8f762.png)

### 可变报头

CONNACK 报文的可变报头按顺序包含以下字段：

![MQTT CONNACK 可变报头](https://assets.emqx.com/images/006e35f23bd97b41cc8c59dc654cf31c.png)

- Connect Acknowledge Flags：连接确认标志。

  - Reserved (Bit 7 - 1)：保留位，必须设置为 0.

  - **Session Present (Bit 0)**：用于指示服务端是否正在使用已存在的会话与客户端恢复通信。仅在客户端在 CONNECT 连接中将 Clean Start 设置为 0 时，Session Present 可能为 1。

- **Reason Code**：用于指示连接结果。下表列出了一些在 CONNACK 报文中常见的 Reason Code，完整列表可参阅 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)。

| **Value** | **Reason Code Name**      | **Description**                                              |
| --------- | ------------------------- | ------------------------------------------------------------ |
| 0x00      | Success                   | 连接被接受。                                                 |
| 0x81      | Malformed Packet          | 服务端无法按照协议规范正确解析 CONNECT 报文，例如保留位没有按照协议要求设置为 0。 |
| 0x82      | Protocol Error            | CONNECT 报文可以被正确解析，但是内容不符合协议规范，比如 Will Topic 字段的值不是一个合法的 MQTT 主题。 |
| 0x86      | Bad User Name or Password | 客户端因为使用了错误的用户名或密码而被拒绝连接。             |
| 0x95      | Packet too large          | CONNECT 报文超过了服务端允许的最大长度，可能是因为携带了较大的遗嘱消息。 |

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

## 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 发起一个连接，在这个连接中，我们将协议版本设置 MQTT 5.0，Clean Start 设置为 1，Session Expiry Interval 设置为 300 秒，Keep Alive 设置为 60，用户名和密码分别设置为 admin 和 public，对应的 MQTTX CLI 命令为：

```
mqttx conn --hostname broker.emqx.io --mqtt-version 5 \
  --session-expiry-interval 300 --keepalive 60 --username admin --password public
```

以下是使用 Wireshark 工具抓取到的 MQTTX CLI 发出的 CONNECT 报文：

```
10 2f 00 04 4d 51 54 54 05 c2 00 3c 05 11 00 00 01 2c 00 0e 6d
71 74 74 78 5f 30 63 36 36 38 64 30 64 00 05 61 64 6d 69 6e 00
06 70 75 62 6c 69 63
```

但这是一串不易理解的十六进制字节，以下示例可以帮助你更清晰地了解到 CONNECT 报文是如何组织各个字段的：

![CONNECT 报文](https://assets.emqx.com/images/54e526147fa96f407f307c69b047f125.png)

同样我们也抓取到了公共 MQTT 服务器返回的 CONNACK 报文：

```
20 13 00 00 10 27 00 10 00 00 25 01 2a 01 29 01 22 ff ff 28 01
```

在以下示例中可以看到，CONNACK 报文的 Reason Code 为 0，表示本次连接成功，后面的多个属性则给出了服务器支持的功能列表，比如支持的最大报文长度，支持保留消息等等：

![CONNACK 报文的 Reason Code](https://assets.emqx.com/images/32848cc16061f4bddff4e3859bef5791.png)

上面的示例是为了帮助大家更好地理解 MQTT 报文结构，实际应用中，你可以直接在 Wireshark 中查看报文详情，Wireshark 对 MQTT 提供了良好的支持，它直接为我们列出了各个字段的值，不需要我们人工解析：

![Wireshark](https://assets.emqx.com/images/3dfb4359c7c16912652b642577270a98.png)

以上就是对 MQTT CONNECT 和 CONNACK 报文的介绍，在后续的博客中，我们还会继续研究 PUBLISH、DISCONNECT 这些报文的结构和组成。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
