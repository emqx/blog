欢迎阅读 [MQTT 5.0 报文系列](https://www.emqx.com/zh/blog/Introduction-to-mqtt-control-packets) 的最后一篇文章。在上一篇中，我们已经介绍了 [MQTT 5.0 的 DISCONNECT 报文](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-05-disconnect)。现在，我们将介绍 MQTT 中的最后一个控制报文：AUTH。

MQTT 5.0 引入了增强认证特性，它使 MQTT 除了简单密码认证和 Token 认证以外，还能够支持质询/响应风格的认证。为了实现这一点，它在原先 CONNECT 和 CONNACK 报文的基础上，又引入了 AUTH 报文来实现任意多次的认证数据交换，以支持各种不同类型的认证机制，例如 [SCRAM](https://en.wikipedia.org/wiki/Salted_Challenge_Response_Authentication_Mechanism)、[Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol)) 认证等等。

一次典型的增强认证的报文交互流程如下：

![Enhanced Authentication.png](https://assets.emqx.com/images/a0e0e42c203f113132ab4adabab93461.png)

关于增强认证的详细介绍，可以参考 [《MQTT 5.0 中的安全认证机制：增强认证介绍》](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security)。本文我们将主要介绍在增强认证中至关重要的 AUTH 报文。

## AUTH 报文示例

由于目前没有支持增强认证特性的 MQTT 客户端，所以我们直接以图示的方式来展示一个典型的 AUTH 报文，里面包含了 AUTH 报文中最重要的两个属性，即认证方法（Authentication Method）和认证数据（Authentication Data）：

![AUTH Packet.png](https://assets.emqx.com/images/3b7ac282f542aff5485af51bf2648249.png)

接下来，我们将依次介绍这些字段的含义。

## AUTH 报文结构

### 固定报头

固定报头中首字节高 4 位的报文类型字段的值为 15（0b1111），低 4 位全部为 0，表示这是一个 AUTH 报文。

![Fixed Header.png](https://assets.emqx.com/images/475a63308cf88814f273692e75e8dfd9.png)

### 可变报头

AUTH 报文的可变报头按顺序包含以下字段：

- **原因码**（Reason Code）：一个单字节的无符号整数，AUTH 报文只有 3 个可用的原因码，它们都用于控制认证流程，分别是：

| **Value** | **Reason Code Name**    | **Sent By**    | **Description**                                              |
| :-------- | :---------------------- | :------------- | :----------------------------------------------------------- |
| 0x00      | Success                 | 服务端         | 认证成功，只会在重新认证成功时由服务端返回，如果是连接时的首次认证成功，服务端将返回 CONNACK 报文。 |
| 0x18      | Continue authentication | 客户端、服务端 | 指示对端继续下一步认证。                                     |
| 0x19      | Re-authenticate         | 客户端         | 客户端可以在一个连接内随时发起重新认证，重新认证期间消息可以正常收发。 |

- **属性**（Properties）：下表列出了 AUTH 报文的所有可用属性。

| **Identifier** | **Property Name**                                            | **Type**                                               | **Description**                                              |
| :------------- | :----------------------------------------------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| 0x15           | Authentication Method                                        | UTF-8 编码的字符串                                     | 认证方法是一个 UTF-8 编码的字符串，用于指示本次认证所使用的认证机制，它可以是 SCRAM-SHA-1 这类已注册的 SASL 机制，也可以是客户端和服务端协商好的任意名称。一旦在 CONNECT 报文中确定了认证方法，那么后续的 AUTH、CONNACK 报文都不可以对其进行变更。 |
| 0x16           | Authentication Data                                          | 二进制数据（由最前面的双字节整数来指示后续的字节数量） | 用于承载认证需要的数据，数据的格式与内容由认证方法决定。     |
| 0x1F           | Reason String                                                | UTF-8 编码的字符串                                     | 表示返回此响应的原因，它可以是任意的内容，由发送端决定，但最好是人类易读的。 |
| 0x26           | [User Property](https://www.emqx.com/zh/blog/mqtt5-user-properties) | UTF-8 字符串对                                         | 用于在报文中附加用户自定义的信息。一个报文中可以包含多个用户属性，即使它们的名字相同。 |

### 有效载荷

AUTH 报文不包含有效载荷。

## 总结

AUTH 报文是实现任意次数认证数据交换的核心，也使得 MQTT 的增强认证能够支持各种不同的认证机制。像 SCRAM 认证、Kerberos 认证，都能提供比简单密码认证更高的安全保障，目前 EMQX 已经支持了其中的 [SCRAM 认证](https://www.emqx.io/docs/zh/v5.1/access-control/authn/scram.html)。

现在，我们已经介绍了 MQTT 中的所有控制报文类型，MQTT 作为一个二进制协议，允许我们传输任意格式的应用消息。但相应地，我们也需要严格地按照协议规范来编码和解析 MQTT 报文，否则就可能造成协议错误。

当我们遇到问题时，可以优先查看对端返回的响应报文中的 Reason Code，它可以指明大部分的错误原因。而当一些嵌入式设备上的端侧 SDK 实现不佳无法直接给出 Reason Code 时，我们可以尝试网络抓包来查看报文中的 Reason Code，此时我们可以借助 Wireshark，避免自己人工解析。

[EMQX](https://www.emqx.io/zh) 作为被广泛使用的可扩展、高可用的 MQTT Broker，也提供了一个方便用户排查问题的 [日志追踪](https://www.emqx.io/docs/zh/v5.1/observability/tracer.html#日志追踪介绍) 功能，它可以记录下指定 Client ID、主题、IP 的所有相关日志，包括报文收发日志。所以我们可以用它来分析客户端的行为是否异常，例如是否正确地响应了 PUBACK，是否重复发送了连接报文等等。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
