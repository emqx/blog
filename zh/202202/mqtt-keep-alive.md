## 为什么需要 Keep Alive

[MQTT 协议](https://mqtt.org/)是承载于 TCP 协议之上的，而 TCP 协议以连接为导向，在连接双方之间，提供稳定、有序的字节流功能。 但是，在部分情况下，TCP 可能出现半连接问题。所谓半连接，是指某一方的连接已经断开或者没有建立，而另外一方的连接却依然维持着。在这种情况下，半连接的一方可能会持续不断地向对端发送数据，而显然这些数据永远到达不了对端。为了避免半连接导致的通信黑洞，MQTT 协议提供了 **Keep Alive** 机制，使客户端和 MQTT 服务器可以判定当前是否存在半连接问题，从而关闭对应连接。


## MQTT Keep Alive 的机制流程与使用

### 启用 Keep Alive

客户端在创建和 MQTT Broker 的连接时，只要将连接请求协议包内的 *Keep Alive* 可变头部字段设置为非 0 值，就可以在通信双方间启用 **Keep Alive** 机制。 *Keep Alive* 为 0~65535 的一个整数，代表客户端发送两次 MQTT 协议包之间的最大间隔时间。

而 Broker 在收到客户端的连接请求后，会检查可变头部中的 *Keep Alive* 字段的值，如果有值，则 Broker 将会启用 **Keep Alive** 机制。

### MQTT 5.0 Server Keep Alive

在 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 标准中，引入了 *Server Keep Alive* 的概念，允许 Broker 根据自身的实现等因素，选择接受客户端请求中携带的 *Keep Alive* 值，或者是覆盖这个值。如果 Broker 选择覆盖这个值，则需要将新值设置在连接确认包(**CONNACK**) 的 *Server Keep Alive* 字段中，客户端如果在连接确认包中读取到了 *Server Keep Alive*，则需要使用该值，覆盖自己之前的 *Keep Alive* 的值。

### Keep Alive 机制流程

**客户端流程**

在连接建立后，客户端需要确保, 自己任意两次 MQTT 协议包的发送间隔不超过 *Keep Alive* 的值，如果客户端当前处于空闲状态，没有可发送的包，则可以发送 **PINGREQ** 协议包。

当客户端发送 **PINGREQ** 协议包后，Broker 必须返回一个 **PINGRESP** 协议包，如果客户端在一个可靠的时间内，没有收到服务器的 **PINGRESP** 协议包，则说明当前存在半连接、或者 Broker 已经下线、或者出现了网络故障，这个时候，客户端应当关闭当前连接。

**Broker 流程**

在连接建立后，Broker 如果没有在 *Keep Alive* 的 1.5 倍时间内，收到来自客户端的任何包，则会认为和客户端之间的连接出现了问题，此时 Broker 便会断开和客户端的连接。

如果 Broker 收到了来自客户端的 **PINGREQ** 协议包，需要回复一个 **PINGRESP** 协议包进行确认。

**客户端接管机制**

当 Broker 里存在半连接时，如果对应的客户端发起了重连或新的连接，则 Broker 会启动客户端接管机制：关闭旧的半连接，然后与客户端建立新的连接。

这种机制保证了客户端不会因为 Broker 里存在的半连接，导致无法进行重连。


## Keep Alive 与遗嘱消息

Keep Alive 通常还可以与遗嘱消息结合使用，通过遗嘱消息，设备可将自己的意外掉线情况及时通知第三方。

如下图，该客户端连接时设置了 Keep Alive 为 5 秒，并且设置了遗嘱消息。那么当服务器 7.5 秒（1.5 倍 Keep Alive）内未收到该客户端的任何报文时，即会向 `last_will` 主题发送 Payload 为 `offline` 的遗嘱消息。

![MQTT Keep Alive 与遗嘱消息](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png?imageMogr2/thumbnail/1520x)

更多关于遗嘱消息的介绍可查看博客：[MQTT 遗嘱消息（Will Message）的使用](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。



## 如何在 EMQX 中使用 Keep Alive

在 [EMQX](https://www.emqx.com/zh/products/emqx) 中，用户可以通过配置来自定义 **Keep Alive** 机制的行为，主要配置字段有:

```apache
zone.${zoneName}.server_keepalive
server_keepalive 类型 默认值   整型 无
```

如果没有设置这个值，则 EMQX 会按照客户端创建连接时的 *Keep Alive* 的值，来控制 **Keep Alive** 的行为。

如果设置了这个值，则 Broker 会对该 zone 下面所有的连接，强制启用 **Keep Alive** 机制，并且会使用这个值，覆盖客户端连接请求中的值。

```apache
zone.${zoneName}.keepalive_backoff
keepalive_backoff 类型 默认值   浮点数 0.75
```

MQTT 协议中要求 Broker 在 1.5 倍 *Keep Alive* 时间内，如果没有收到客户端的任何协议包，则认定客户端断开了连接。

而在 EMQX 中，我们引入了退让系数(keepalive backoff)，并将这个系数通过配置暴露出来，方便用户更灵活的控制 Broker 端的 **Keep Alive** 行为。

在引入退让系数后，EMQX 通过下面的公式来计算最大超时时间:

```apache
Keepalive * backoff * 2
```

*backoff* 默认值为0.75，因此在用户不修改该配置的情况下，EMQX 的行为完全符合 MQTT 标准。

更多相关内容请参见 [EMQX 配置文档](https://docs.emqx.com/zh/emqx/v4.3/configuration/configuration.html)。

**WebSocket 连接时设置 Keep Alive**

EMQX 支持客户端通过 WebSocket 接入，当客户端使用 WebSocket 发起连接时，只需要在连接参数中设置上 keepalive 的值即可， 具体见[使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)。



## 结语

本文介绍了 MQTT 协议中 Keep Alive 的机制及 EMQX 中 Keep Alive 的使用，开发者可以借助这一特性确保 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)的稳定性，构建更加健壮的上层物联网应用。

接下来可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
