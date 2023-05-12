## MQTT 持久会话

不稳定的网络及有限的硬件资源是物联网应用需要面对的两大难题，MQTT 客户端与服务器的连接可能随时会因为网络波动及资源限制而异常断开。为了解决网络连接断开对通信造成的影响，MQTT 协议提供了持久会话功能。

MQTT 客户端在发起到服务器的连接时，可以设置是否创建一个持久会话。持久会话会保存一些重要的数据，以使会话能在多个网络连接中继续。持久会话主要有以下三个作用：

- 避免因网络中断导致需要反复订阅带来的额外开销。

- 避免错过离线期间的消息。

- 确保 QoS 1 和 QoS 2 的消息质量保证不被网络中断影响。

 
## 持久会话需要存储哪些数据？

通过上文我们知道持久会话需要存储一些重要的数据，以使会话能被恢复。这些数据有的存储在客户端，有的则存储在服务端。

客户端中存储的会话数据：

- 已发送给服务端，但是还没有完成确认的 QoS 1 与 QoS 2 消息。
- 从服务端收到的，但是还没有完成确认的 QoS 2 消息。

服务端中存储的会话数据：

- 会话是否存在，即使会话状态其余部分为空。
- 已发送给客户端，但是还没有完成确认的 QoS 1 与 QoS 2 消息。
- 等待传输给客户端的 QoS 0 消息（可选），QoS 1 与 QoS 2 消息。
- 从客户端收到的，但是还没有完成确认的 QoS 2 消息，遗嘱消息和遗嘱延时间隔。


## MQTT Clean Session 的使用

Clean Session 是用来控制会话状态生命周期的标志位，为 `true` 时表示创建一个新的会话，在客户端断开连接时，会话将自动销毁。为 `false` 时表示创建一个持久会话，在客户端断开连接后会话仍然保持，直到会话超时注销。

> **注意：** 持久会话能被恢复的前提是客户端使用固定的 Client ID 再次连接，如果 Client ID 是动态的，那么连接成功后将会创建一个新的持久会话。

如下为[开源 MQTT 服务器 EMQX](https://www.emqx.io/zh) 的 Dashboard，可以看到图中的连接虽然是断开状态，但是因为它是持久会话，所以仍然能被查看到，并且可以在 Dashboard 中手动清除该会话。

![MQTT 持久会话](https://assets.emqx.com/images/f5d591b3a7884526efcf595cae23bdbd.png)

同时，EMQX 也支持在 Dashboard 中设置 Session 相关参数。

![EMQX Dashboard](https://assets.emqx.com/images/7bbf34ea3e9cd08b272378be92b9a16c.png)

MQTT 3.1.1 没有规定持久会话应该在什么时候过期，如果仅从协议层面理解的话，这个持久会话应该永久存在。但在实际场景中这并不现实，因为它会非常占用服务端的资源，所以服务端通常不会完全遵循协议来实现，而是向用户提供一个全局配置来限制会话的过期时间。

比如 EMQ 提供的 [免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 设置的会话过期时间为 5 分钟，最大消息数为 1000 条，且不保存 QoS 0 消息。

接下来我们使用开源的跨平台 [MQTT 5.0 桌面客户端工具 - MQTTX](https://mqttx.app/zh) 演示 Clean Session 的使用。

打开 MQTTX 后如下所示，点击 `New Connection` 按钮创建一个 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)。

![MQTT Client](https://assets.emqx.com/images/c3c89247952538c127839de49a398aec.png)

创建一个名为 `MQTT_V3` 的连接，Clean Session 为关闭状态（即为 false），MQTT 版本选择 3.1.1，然后点击右上角的 `Connect` 按钮。

> 连接的服务器默认为 EMQ 提供的 [免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。

![创建 MQTT 连接](https://assets.emqx.com/images/a0c27c205f63c875cc9b1c9dffd07f9f.png)

连接成功后订阅 `clean_session_false` 主题，且 QoS 设置为 1。

![订阅 MQTT 主题](https://assets.emqx.com/images/68921b7dfd81e33f294f3152b2ebe01d.png)

订阅成功后，点击右上角的断开连接按钮。然后，创建一个名为 `MQTT_V3_Publish` 的连接，MQTT 版本同样设置为 3.1.1，连接成功后向 `clean_session_false` 主题发布两条 QoS 1 消息。

![发布 MQTT 消息](https://assets.emqx.com/images/c73cc02fa8e15af71401996c52d28b8c.png)

然后选中 MQTT_V3 连接，点击连接按钮连接至服务器，将会成功接收到两条离线期间的消息。

![接收 MQTT 消息](https://assets.emqx.com/images/67572dcbbd03f2436d883cc7665e6957.png)


## MQTT 5.0 中的会话改进

MQTT 5.0 中将 Clean Session 拆分成了 Clean Start 与 Session Expiry Interval。Clean Start 用于指定连接时是创建一个全新的会话还是尝试复用一个已存在的会话，Session Expiry Interval 用于指定网络连接断开后会话的过期时间。

Clean Start 为 `true` 时表示必须丢弃任何已存在的会话，并创建一个全新的会话；为 `false` 时表示必须使用与 Client ID 关联的会话来恢复与客户端的通信（除非会话不存在）。

Session Expiry Interval 解决了 MQTT 3.1.1 中持久会话永久存在造成的服务器资源浪费问题。设置为 0 或未设置，表示断开连接时会话即到期；设置为大于 0 的数值，则表示会话在网络连接关闭后会保持多少秒；设置为 `0xFFFFFFFF` 表示会话永远不会过期。

更多细节可查看博客：[Clean Start 与 Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。


## 关于 MQTT 会话的 Q&A

### 当会话结束后，保留消息还存在么？

[MQTT 保留消息](https://www.emqx.com/zh/blog/mqtt5-features-retain-message)不是会话状态的一部分，它们不会在会话结束时被删除。

### 客户端如何知道当前会话是被恢复的会话？

MQTT 协议从 v3.1.1 开始，就为 CONNACK 报文设计了 Session Present 字段。当服务器返回的该字段值为 1 时，表示当前连接将会复用服务器保存的会话。客户端可通过该字段值决定在连接成功后是否需要重新订阅。

### 使用持久会话时有哪些建议？

- 不能使用动态 Client ID，需要保证客户端每次连接的 Client ID 都是固定的。
- 根据服务器性能、网络状况、客户端类型等合理评估会话过期时间。设置过长会占用更多的服务端资源，设置过短会导致未重连成功会话就失效。
- 当客户端确定不再需要会话时，可使用 Clean Session 为 true 进行重连，重连成功后再断开连接。如果是 MQTT 5.0 则可在断开连接时直接设置 Session Expiry Interval 为 0，表示连接断开后会话即失效。

## 结语

至此，我们完成了对 MQTT 持久会话的介绍，并通过桌面客户端演示了 Clean Session 的使用。读者可参考本文借助 MQTT 持久会话实现离线消息的接收及降低订阅开销。

接下来，读者可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
