在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，SUBSCRIBE 报文用于发起订阅请求，SUBACK 报文用于返回订阅结果。而 UNSUBSCRIBE 和 UNSUBACK 报文则在取消订阅时使用。相比于取消订阅，订阅操作更加常用。不过在本文中，我们仍然会一并介绍订阅与取消订阅报文的结构与组成。

## SUBSCRIBE 报文结构

### 固定报头

在 SUBSCRIBE 报文中，固定报头中首字节的高 4 位值必须为 8，而低 4 位保留位必须被设置为 `0x2`。第一个字节之后，仍然是剩余长度（Remaining Length）字段，它是一个可变字节整数。

![SUBSCRIBE 固定报头](https://assets.emqx.com/images/554217bbe3053b74cc91fc545b6dd396.png)

### 可变报头

SUBSCRIBE 报文的可变报头按顺序包含以下字段：

![SUBSCRIBE 可变报头](https://assets.emqx.com/images/8c8af3176fc2ee70c11dd75c80fcf174.png)

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

![SUBSCRIBE 报文的有效载荷](https://assets.emqx.com/images/d514a635aabc2382f15ac7f4dcf6ad69.png)

## UNSUBSCRIBE 报文结构

### 固定报头

与 SUBSCRIBE 报文相同，唯一的区别是报文类型字段的值从 8 变成了 10。

![UNSUBSCRIBE 固定报头](https://assets.emqx.com/images/fd27268bea022ebd77d85b01ea5ac2ce.png)

### 可变报头

与 SUBSCRIBE 报文相同。

### 有效载荷

UNSUBSCRIBE 报文的有效载荷包含一个或多个客户端希望取消订阅的主题过滤器，这些主题过滤器同样是 UTF-8 编码的字符串，并且多个主题过滤器紧密相连。

![UNSUBSCRIBE 有效载荷](https://assets.emqx.com/images/8a484533beb6bb2cacd4b56300fb72ba.png)

## SUBACK、UNSUBACK 报文结构

### 固定报头

SUBACK 报文的首字节高 4 位的值为 9，UNSUBACK 报文的首字节高 4 位的值为 11，它们首字节的低 4 位都必须被设置为 0。

![SUBACK 固定报头](https://assets.emqx.com/images/1ec1afbd6ecbaf11d0882a7df2f1430a.png)

### 可变报头

SUBACK 和 UNSUBACK 报文的可变报头按顺序包含以下字段：

![SUBACK 可变报头](https://assets.emqx.com/images/858271e2149bd7cf44b2fc295235ed53.png)

- **报文标识符**（Packet Identifier）：SUBACK 和 UNSUBACK 报文中的报文标识符必须与对应的订阅或取消订阅报文中一致，以便另一方正确地将响应与请求匹配。
- **属性**（Properties）：下表列出了 SUBACK / UNSUBACK 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**           |
| :------------- | :----------------------------------------------------------- | :----------------- |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对     |

### 有效载荷

SUBACK 和 UNSUBACK 报文的有效载荷包含了一个 Reason Code 列表，Reason Code 指示了订阅/取消订阅是否成功或者失败的原因。一个 Reason Code 对应 SUBSCRIBE 和 UNSUBSCRIBE 报文中的一个主题过滤器，所以响应报文中 Reason Code 的顺序必须与请求报文中主题过滤器的顺序一致。

![SUBACK 和 UNSUBACK 报文的有效载荷](https://assets.emqx.com/images/5c5065343b17604dbf2575df9e10f40c.png)

SUBACK 和 UNSUBACK 报文允许使用的 Reason Code 有所不同，下表列出了在这两个报文中常见的 Reason Code，完整列表可参阅 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)。

| **Value** | **Reason Code Name**    | **Packet** | **Description**                                              |
| :-------- | :---------------------- | :--------- | :----------------------------------------------------------- |
| 0x00      | Granted QoS 0           | SUBACK     | 订阅被接受且最大 QoS 等级为 0。服务端授予的 QoS 等级可能低于客户端请求的 QoS 等级，这主要取决于服务端是否支持所有 QoS 或者是相应的权限设置。 |
| 0x01      | Granted QoS 1           | SUBACK     | 订阅被接受且最大 QoS 等级为 1。                              |
| 0x02      | Granted QoS 2           | SUBACK     | 订阅被接受且最大 QoS 等级为 2。                              |
| 0x87      | Not authorized          | SUBACK     | 客户端无权进行此订阅。                                       |
| 0x00      | Success                 | UNSUBACK   | 订阅已被删除                                                 |
| 0x11      | No subscription existed | UNSUBACK   | 服务端中不存在该订阅。                                       |

## 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 发起订阅和取消订阅请求，并使用 [Wireshark](https://www.wireshark.org/) 工具抓取在客户端与服务器之间往返的 MQTT 报文，Linux 环境可以使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后导入至 Wireshark 分析。

我们使用以下命令来创建一个主题为 `demo`，且最大 QoS 设置为 2 的订阅：

```
 mqttx sub --hostname broker.emqx.io --mqtt-version 5 --topic demo --qos 2
```

以下是从 Wireshark 中截取的 SUBSCRIBE 报文内容：

```
82 0a 05 be 00 00 04 64 65 6d 6f 02
```

第一个字节 0x82 表示这是一个 SUBSCRIBE 报文，后面的字节我们可以依次代入 SUBSCRIBE 报文的各个字段，最终我们将得到：

![SUBSCRIBE报文](https://assets.emqx.com/images/54a03da3d70344decee65a01427b1c95.png)

以下则是对应的 SUBACK 报文内容：

```
90 04 05 be 00 02
```

第一个字节 0x90 表示这是一个 SUBACK 报文，它有着和 SUBSCRIBE 报文相同的报文标识符，而 Reason Code 2 表示订阅被接收，并且服务端授予的最大 QoS 等级为 2：

![SUBACK 报文](https://assets.emqx.com/images/9c35cc90d01dd2dc20d286002b5b354d.png)

UNSUBSCRIBE 和 UNSUBACK 报文的结构与 SUBSCRIBE 和 SUBACK 十分相似，所以这里我们就不再继续展开了。你可以自行发起一个取消订阅的请求并捕获对应的报文，然后按照本文的介绍来解析它们。当然，你需要改为使用 MQTTX 这个桌面端的客户端工具，因为 MQTTX CLI 无法主动取消订阅。

在下一篇文章中，我们将继续研究 MQTT 的心跳报文。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
