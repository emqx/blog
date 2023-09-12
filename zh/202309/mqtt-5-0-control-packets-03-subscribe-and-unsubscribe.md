在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，SUBSCRIBE 报文用于发起订阅请求，SUBACK 报文用于返回订阅结果。而 UNSUBSCRIBE 和 UNSUBACK 报文则在取消订阅时使用。相比于取消订阅，订阅操作更加常用。不过在本文中，我们仍然会一并介绍订阅与取消订阅报文的结构与组成。

## 报文示例

首先我们借助 [Wireshark](https://www.wireshark.org/) 来捕获一次真实的 MQTT 订阅请求与响应，这里我们使用 MQTTX CLI 向 公共 MQTT 服务器 发起订阅请求。以下命令将创建一个主题为 demo，且最大 QoS 设置为 2 的订阅：

```
mqttx sub --hostname broker.emqx.io --mqtt-version 5 --topic demo --qos 2
```

以下是 Wireshark 捕获到的 SUBSCRIBE 和 SUBACK 报文数据：

```
# SUBSCRIBE
82 0a 05 be 00 00 04 64 65 6d 6f 02

# SUBACK
90 04 05 be 00 02
```

> Linux 环境可以先使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后导入至 Wireshark 分析。

这些由十六进制字节组成的原始且晦涩的报文数据，它们分别对应着以下报文内容：

![SUBSCRIBE 报文.png](https://assets.emqx.com/images/db8a7ad5d48659c96b6367295a168c34.png)

![SUBACK 报文.png](https://assets.emqx.com/images/4a30f4624f78b6b86cd48d33d8e92361.png)

也许你开始好奇它们是如何完成从简单的 MQTTX CLI 命令到复杂的报文数据的转换，或者好奇当你捕获到一个 MQTT 报文，你应该如何从中提取你想要的信息。

那么在接下来的 SUBSCRIBE、SUBACK、UNSUBSCRIBE 以及 UNSUBACK 的报文结构的介绍中，你的疑问将得到解答。

## SUBSCRIBE 报文结构

### 固定报头

在 SUBSCRIBE 报文中，固定报头中首字节的高 4 位值必须为 8（0b1000），而低 4 位保留位必须被设置为 2（0b0010）。第一个字节之后，仍然是剩余长度（Remaining Length）字段，它是一个可变字节整数。

![SUBSCRIBE 固定报头](https://assets.emqx.com/images/172bbaaa09a23bea723f205260766c78.png)

### 可变报头

SUBSCRIBE 报文的可变报头按顺序包含以下字段：

![SUBSCRIBE 可变报头](https://assets.emqx.com/images/b33033a485a500528d9c917bd7a184d9.png)

- **报文标识符**（Packet Identifier）：一个两个字节长度的无符号整数，用来唯一地标识订阅请求。PUBLISH、SUBSCRIBE、UNSUBSCRIBE 报文使用一组报文标识符，这表示它们不能同时使用同一个报文标识符。
- **属性**（Properties）：下表列出了 SUBSCRIBE 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**       |
| :------------- | :----------------------------------------------------------- | :------------- |
| 0x0B           | [Subscription Identifier](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options) | 变长字节整数   |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对 |

### 有效载荷

SUBSCRIBE 报文的有效载荷包含一个或多个主题过滤器/订阅选项对。主题过滤器是一个 UTF-8 编码的字符串，用于向服务端指明客户端希望订阅的主题，订阅选项则仅占用一个字节，目前由以下四个选项组成：

- Reserved (Bit 7, 6)：保留位，目前必须设置为 0。
- **Retain Handling (Bit 5, 4)**：用于指示当订阅建立时，服务端是否需要向此订阅发送保留消息。
- **Retain As Published (Bit 3)**：用于指示服务端在向此订阅转发应用消息时是否需要保持消息中的 Retain 标志。
- **No Local (Bit 2)**：用于指示服务端是否可以将应用消息转发给该消息的发布者。No Local 和 Retain As Published 通常用于桥接场景。
- **Maximum QoS (Bit 1, 0)**：这个选项决定了服务端向此订阅转发消息时可以使用的最大 QoS 等级。如果消息的原始 QoS 超过了这个限制，那么服务端就会对 QoS 进行降级以保证消息的传递。

![SUBSCRIBE 报文的有效载荷](https://assets.emqx.com/images/4374c15b38cc5f7f98d310f926843d3b.png)

## SUBACK 报文结构

### 固定报头

SUBACK 报文的首字节高 4 位的值为 9，低 4 位都必须全部被设置为 0。

![SUBACK 固定报头](https://assets.emqx.com/images/b1bb02d581f04b546973c073da736b7f.png)

### 可变报头

SUBACK 的可变报头按顺序包含以下字段：

![SUBACK 可变报头](https://assets.emqx.com/images/08d231823e2b37e7573ebc4a97286c2a.png)

- **报文标识符**（Packet Identifier）：SUBACK 报文中的报文标识符必须与对应的 SUBSCRIBE 报文一致，以便另一方正确地将响应与请求匹配。
- **属性**（Properties）：下表列出了 SUBACK 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| :------------- | :----------------------------------------------------------- | :----------------- |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |

### 有效载荷

SUBACK 报文的有效载荷包含了一个 Reason Code 列表，Reason Code 指示了订阅是否成功或者失败的原因。一个 Reason Code 对应 SUBSCRIBE 报文的一个主题过滤器，所以 SUBACK 报文中 Reason Code 的顺序必须与 SUBSCRIBE 报文中主题过滤器的顺序一致。

![SUBACK 有效载荷](https://assets.emqx.com/images/eee7bf2f4c5a9ea01ddef84f831c831f.png)

下表列出了 SUBACK 报文可用的所有 Reason Code：

| **Value** | **Reason Code Name**                   | **Description**                                              |
| --------- | -------------------------------------- | ------------------------------------------------------------ |
| 0x00      | Granted QoS 0                          | 订阅被接受且最大 QoS 等级为 0。服务端授予的 QoS 等级可能低于客户端请求的 QoS 等级，这主要取决于服务端是否支持所有 QoS 或者是相应的权限设置。 |
| 0x01      | Granted QoS 1                          | 订阅被接受且最大 QoS 等级为 1。                              |
| 0x02      | Granted QoS 2                          | 订阅被接受且最大 QoS 等级为 2。                              |
| 0x80      | Unspecified error                      | 表示未指明的错误。当一方不希望向另一方透露错误的具体原因，或者协议规范中没有能够匹配当前情况的 Reason Code 时，那么它会在报文中使用这个 Reason Code。 |
| 0x83      | Implementation specific error          | SUBSCRIBE 报文有效，但是不被当前服务端的实现所接受。         |
| 0x87      | Not authorized                         | 客户端无权进行此订阅。                                       |
| 0x8F      | Topic Filter invalid                   | 主题过滤器的格式正确，但是不被服务端接受。比如主题过滤器的层级超过了服务端允许的最大数量限制。 |
| 0x91      | Packet Identifier in use               | 收到报文中的 Packet ID 正在被使用。                          |
| 0x97      | Quota exceeded                         | 表示超出了配额限制。服务端可能会对订阅端的订阅配额进行限制，比如一个客户端最多建立 10 个订阅。 |
| 0x9E      | Shared Subscriptions not supported     | 服务端不支持共享订阅。                                       |
| 0xA1      | Subscription Identifiers not supported | 服务端不支持订阅标识符。                                     |
| 0xA2      | Wildcard Subscriptions not supported   | 服务端不支持通配符订阅。                                     |

## UNSUBSCRIBE 报文结构

### 固定报头

与 SUBSCRIBE 报文相同，唯一的区别是报文类型字段的值从 8 变成了 10。

![UNSUBSCRIBE 固定报头](https://assets.emqx.com/images/c1d2d3bf49f7cc46dcb510647c7ab0f1.png)

### 可变报头

与 SUBSCRIBE 报文相同。

### 有效载荷

UNSUBSCRIBE 报文的有效载荷包含一个或多个客户端希望取消订阅的主题过滤器，这些主题过滤器同样是 UTF-8 编码的字符串，并且多个主题过滤器紧密相连。

![UNSUBSCRIBE 有效载荷](https://assets.emqx.com/images/0ab75a33265b33bdb35229874122809e.png)

## UNSUBACK 报文结构

### 固定报头

UNSUBACK 报文的首字节高 4 位的值为 11，低 4 位都必须全部被设置为 0。

![UNSUBACK 固定报头](https://assets.emqx.com/images/1eae85d3d63835f9312ce950a1cb16c7.png)

### 可变报头

UNSUBACK 的可变报头按顺序包含报文标识符和属性字段，可用的属性与 SUBACK 报文相同。

### 有效载荷

UNSUBACK 报文的有效载荷同样包含了一个 Reason Code 列表，Reason Code 指示了取消订阅是否成功或者失败的原因。这些 Reason Code 按顺序对应 UNSUBSCRIBE 报文的主题过滤器。

![UNSUBACK 有效载荷](https://assets.emqx.com/images/b9ea7577d509711c3391d044e1e5894d.png)

下表列出了 UNSUBACK 报文可用的所有 Reason Code：

| **Value** | **Reason Code Name**          | **Description**                                              |
| --------- | ----------------------------- | ------------------------------------------------------------ |
| 0x00      | Success                       | 订阅已被删除                                                 |
| 0x11      | No subscription existed       | 服务端中不存在该订阅。                                       |
| 0x80      | Unspecified error             | 表示未指明的错误。                                           |
| 0x83      | Implementation specific error | UNSUBSCRIBE 报文有效，但是不被当前服务端的实现所接受。       |
| 0x87      | Not authorized                | 客户端无权取消此订阅。                                       |
| 0x8F      | Topic Filter invalid          | 主题过滤器的格式正确，但是不被服务端接受。比如主题过滤器的层级超过了服务端允许的最大数量限制。 |
| 0x91      | Packet Identifier in use      | 收到报文中的 Packet ID 正在被使用。                          |

## 总结

SUBSCRIBE 和 SUBACK 报文用于订阅，UNSUBSCRIBE 和 UNSUBACK 用于取消订阅，想要订阅或者取消订阅的主题过滤器列表，都在对应报文的有效载荷中，SUBSCRIBE 报文中的每个主题主题过滤器，都与一组订阅选项相关联。

指示请求结果的 Reason Code 位于 SUBACK 和 UNSUBACK 报文的有效载荷部分，并且它是一个列表，一一对应请求报文中的主题过滤器。

在下一篇文章中，我们将继续研究 MQTT 的心跳报文。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
