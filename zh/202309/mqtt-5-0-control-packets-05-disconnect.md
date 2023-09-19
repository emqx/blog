欢迎阅读 [MQTT 5.0 报文系列](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets) 的第五篇文章。在上一篇中，我们已经介绍了 [MQTT 5.0 的 PINGREQ 和 PINGRESP 报文](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-04-pingreq-and-pingresp)。现在，我们将介绍下一个控制报文：DISCONNECT。

在 MQTT 中，客户端和服务端可以在断开网络连接前向对端发送一个 DISCONNECT 报文，来指示连接关闭的原因。客户端发送的 DISCONNECT 报文还可以影响服务端在连接断开后的行为，例如是否发送遗嘱消息，是否更新会话过期间隔。

## DISCONNECT 报文示例

我们使用 [MQTTX CLI](https://mqttx.app/zh) 向 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 发起一个指定了 Client ID 的客户端连接，并将 `--reconnect-period` 设置为 0 来禁用自动重连，然后在另一个终端中运行相同的命令创建一个使用相同 Client ID 的连接。

整个过程使用 [Wireshark](https://www.wireshark.org/) 工具来抓取在客户端与服务器之间往返的 MQTT 报文，Linux 环境可以使用 [tcpdump](https://en.wikipedia.org/wiki/Tcpdump) 命令抓取报文，然后导入至 Wireshark 分析。

以下命令将创建一个 Client ID 为 `mqtt-892324` 的客户端连接，为了避免 Client ID 与别人重复，建议将它改为其他随机字符串：

```
mqttx conn --hostname broker.emqx.io --mqtt-version 5 --client-id mqtt-892324 \ --reconnect-period 0
```

在我们发起第二个连接后，Wireshark 将捕获到公共 MQTT 服务器返回给第一个连接的 DISCONNECT 报文：

```
e0 02 8e 00
```

这四个十六进制字节，对应着以下报文内容：

![DISCONNECT Packet.png](https://assets.emqx.com/images/b4639384cab1559bb3e0b95022a9530d.png)

通过下文对 DISCONNECT 报文结构的介绍，你将了解到如何从原始的报文数据中提取你想要的信息。

## DISCONNECT 报文结构

### 固定报头

固定报头首字节的高 4 位，即报文类型字段的值为 14（0b1110），低 4 位全部为 0，表示这是一个 DISCONNECT 报文。

![Fixed Header.png](https://assets.emqx.com/images/c0d352d8aaca25bb63610e7e62df1e31.png)

### 可变报头

DISCONNECT 报文的可变报头按顺序包含以下字段：

![Viriable Header.png](https://assets.emqx.com/images/d87f978e47dad0c2cb22b331ffbe5d99.png)

- **原因码**（Reason Code）：一个单字节的无符号整数，用于向对端指示连接断开的原因。下表列出了在 DISCONNECT 报文中常见的 Reason Code，完整列表可参阅 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)。

| **Value** | **Reason Code Name**         | **Sent By**    | **Description**                                              |
| :-------- | :--------------------------- | :------------- | :----------------------------------------------------------- |
| 0x00      | Normal disconnection         | 客户端、服务端 | 表示连接正常关闭，因此服务端不会发布遗嘱消息。               |
| 0x04      | Disconnect with Will Message | 客户端         | 连接正常关闭，但客户端希望服务端仍然发布遗嘱消息。           |
| 0x81      | Malformed Packet             | 客户端、服务端 | 表示收到了无法按照协议规范正确解析的控制报文，在 MQTT 中我们将这类报文称为畸形报文。 |
| 0x82      | Protocol Error               | 客户端、服务端 | 协议错误通常指控制报文在按照协议规范解析以后才能发现的错误，包括包含协议不允许的数据、行为与协议要求不符等等。比如客户端在一个连接内发送了两个 CONNECT 报文。 |
| 0x8D      | Keep Alive timeout           | 服务端         | 服务端在超过 1.5 倍的 Keep Alive 时间内没有收到任何报文，因此关闭了连接。 |
| 0x8E      | Session taken over           | 服务端         | 另一个更新的使用了且相同的 Client ID 的连接被建立，导致服务端关闭了此连接。 |
| 0x93      | Receive Maximum exceeded     | 客户端、服务端 | 表示对端同时发送的 QoS > 0 的 PUBLISH 报文数量超过了连接时设置的接收最大值。 |
| 0x94      | Topic Alias invalid          | 客户端、服务端 | 表示主题别名不合法。比如 PUBLISH 报文中的主题别名值为 0 或者大于连接时约定的最大主题别名。 |
| 0x95      | Packet too large             | 客户端、服务端 | 表示报文超过了连接时约定的最大允许长度。                     |
| 0x98      | Administrative action        | 客户端、服务端 | 表示连接因为管理操作而被关闭，比如运维人员在服务端后台踢除了客户端连接。 |
| 0x9C      | Use another server           | 服务端         | 表示客户端应该**临时**切换到另一个服务器。如果另一个服务器不是客户端已知的，那么还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。 |
| 0x9D      | Server moved                 | 服务端         | 表示客户端应该**永久**切换到另一个服务器。如果另一个服务器不是客户端已知的，那么还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。 |

- **属性**（Properties）：下表列出了 DISCONNECT 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Sent By**    | **Type**           |
| :------------- | :----------------------------------------------------------- | :------------- | :----------------- |
| 0x11           | [Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) | 客户端         | 四字节整数         |
| 0x1F           | Reason String                                                | 客户端、服务端 | UTF-8 编码的字符串 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | 客户端、服务端 | UTF-8 字符串对     |
| 0x1C           | Server Reference                                             | 服务端         | UTF-8 编码的字符串 |

与之前介绍的其他报文不同，客户端和服务端在 DISCONNECT 报文中可以使用的原因码和属性是不同的，例如 Session Expiry Interval 属性就只能在客户端发送的 DISCONNECT 报文中使用，所以我们在上面的列表中均列出了它们的可用范围。

### 有效载荷

DISCONNECT 报文不包含有效载荷。

## 总结

客户端和服务端都可以发送 DISCONNECT 报文，表示准备断开网络连接，报文中的原因码可以向接收方指示连接关闭的原因。当 MQTT 连接意外断开时，我们可以优先查看是否收到了 DISCONNECT 报文以及报文中原因码的值。

虽然客户端和服务端在 DISCONNECT 报文中可以用的原因码和属性存在差异，但我们并不需要强行去记忆它们。它们通常都和对应的机制与行为相关，例如遗嘱消息只会由服务端发布，所以希望连接正常关闭但对端仍要发布遗嘱消息的原因码 0x04，也会被客户端使用。

以上就是对 DISCONNECT 报文的介绍，在下一篇文章中我们将介绍 MQTT 5.0 增强认证特性所使用的 AUTH 报文，它也是 MQTT 中最后一个报文类型。

 <section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
