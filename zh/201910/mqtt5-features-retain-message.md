### 前言

发布订阅模式虽然让消息的发布者与订阅者充分解耦，但也出现了一个隐含的问题，即订阅者无法主动向发布者请求消息，订阅者何时收到消息完全依赖于发布者何时发布消息，这在某些场景中就产生了不便。例如，某设备定期发布自身 GPS 坐标，但对于订阅者而言，从它发起订阅到第一次收到数据可能需要几秒钟，也可能需要十几分钟甚至更多，这样并不友好。因此 [MQTT](https://www.emqx.com/zh/mqtt) 引入了[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)。

### 保留消息

![image20191014152158994.png](https://assets.emqx.com/images/211d363915c98f86e3f55ff2e5b20326.png)

当服务端收到 Retain 标志为 1 的 PUBLISH 报文时，它将进行以下操作：

1. 如果存在匹配此主题名的订阅者，则按正常逻辑进行转发，并在转发前清除 Retain 标志。MQTT v3.1.1 协议中 Retain 标志必须被清除，而 MQTT v5.0 协议则在[订阅选项](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)中新增了一个 Retain As Publish 字段，由客户端自行指示服务端在转发前是否需要清除 Retain 标志。
2. 如果 Payload 非空，存储此应用消息，如果此主题名下已经存在保留消息则进行替换。如果 Payload 为空，服务端不会存储此应用消息，同时清除此主题名下已经存在的保留消息。

而每当有订阅者建立订阅时，服务端就会查找是否存在匹配该订阅的保留消息，如果保留消息存在，就会立即转发给订阅者。当保留消息在这种情况下被转发给订阅者时，它的 Retain 标志必须保持为 1。相比 MQTT v3.1.1，MQTT v5.0 对于订阅建立时是否发送保留消息做了更细致的划分，并在订阅选项中提供了 Retain Handling 字段。例如某些客户端可能仅希望在首次订阅时接收保留消息，又或者不希望在订阅建立时接收保留消息，都可以通过 Retain Handling 选项调整。

保留消息虽然存储在服务端中，但它并不属于会话的一部分。也就是说，即便发布这个保留消息的会话终结，保留消息也不会被删除。删除保留消息只有两种方式：

1. 前文已经提到过的，客户端往某个主题发送一个 Payload 为空的保留消息，服务端就会删除这个主题下的保留消息。
2. 消息过期间隔属性在保留消息中同样适用，如果客户端设置了这一属性，那么保留消息在服务端存储超过过期时间后就会被删除。

借助保留消息，新的订阅者能够立即获取最近的状态，而不需要等待无法预期的时间，这在很多场景下很非常重要的。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
