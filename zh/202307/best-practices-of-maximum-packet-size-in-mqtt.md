## 什么是 Maximum Packet Size

[MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)的理论最大长度为 268435456 字节，也就是 256 MB。但显然，不仅仅是资源受限的客户端，一些作为边缘网关运行的 MQTT 服务端，可能也无法处理这一长度的报文。

考虑到不同客户端对报文的处理能力可能有着较大差异，发送过大的报文不仅可能影响对端的正常业务处理，甚至可能直接压垮对端。所以，我们需要使用 Maximum Packet Size 属性来协商客户端和服务端各自能够处理的最大报文长度。

客户端首先在 CONNECT 报文中通过 Maximum Packet Size 来指定允许服务端给自己发送的报文的最大长度，而服务端则会在 CONNACK 报文中同样通过 Maximum Packet Size 来指定允许客户端给自己发送的报文的最大长度。

![MQTT CONNECT packet](https://assets.emqx.com/images/1f64b4c59e8da8d446d823d6b8f20535.png)

一旦连接建立，双方就必须遵循这一约定来发送消息。任何一方都不允许发送超过约定长度限制的报文，否则接收方就会返回 Reason Code 为 0x95 的 DISCONNECT 报文然后关闭网络连接。

但需要注意，如果客户端在 CONNECT 报文中设置了遗嘱消息，这可能在其不自知的情况下使得 CONNECT 报文超过了服务端允许的最大报文长度。这时服务端将返回 Reason Code 为 0x95 的 CONNACK 报文然后关闭网络连接。

## 发送方如何在 Maximum Packet Size 限制下工作

对客户端来说，不管是发布还是订阅，作为主动发送的一方，它都可以将一个报文拆分多个发送来避免超过长度限制。

但对服务端来说，它只负责转发消息，并不能决定消息的大小。所以如果它发现准备转发的消息的大小超过了客户端能够接受的最大值，那么它只能丢弃这个消息。如果当前是共享订阅，那么服务端除了丢弃以外，还可以选择把消息发送给组内其他能够接收此消息的客户端。

除了上面提到的两种策略，不管是客户端还是服务端，他们都可以在一定程度上裁剪报文的内容来减少长度。我们知道响应方可以在 CONNACK、PUBACK 这些响应报文中包含 User Property 和 Reason String 这两个属性来向对端传递更多信息。

但响应报文超过最大长度限制的可能性也正是由这两个属性带来的。显然，传输它们的优先级低于确保协议流程正常进行，所以响应方可以在报文长度超出限制时，从报文中移除这两个属性来尽可能保证响应报文被正常发送。

需要注意的是，这里仅仅指响应报文，PUBLISH 报文不在此列。对于 PUBLISH 报文来说，User Property 属于消息的一部分，服务端不能为了确保消息投递而尝试将它从报文中移除。

## 使用示例

1. 打开已经安装在本地的 [MQTTX](https://mqttx.app/)

2. 创建一个 MQTT 连接，设置 Maximum Packet Size 为 100，然后连接至免费的 [公共 MQTT 服务器](https://www.emqx.com/en/mqtt/public-mqtt5-broker)：

   ![Create an MQTT connection](https://assets.emqx.com/images/784f1078a559f75b0c9ed10f30a5a218.png)

3. 连接成功后我们可以通过 Wireshark 抓包工具看到，服务端返回的 CONNACK 报文中 Maximum Packet Size 属性的值为 1048576，也就是说客户端每次只能向公共 MQTT 服务器发送最多 1 MB 的报文：

   ![Wireshark packet capture tool](https://assets.emqx.com/images/0d6c9d52f8dbb2c052119386f0bb10b3.png)

4. 回到 MQTTX 中，我们订阅 `mqttx_0c668d0d/demo` 主题：

   ![Subscribe to the topic "mqttx_0c668d0d/demo"](https://assets.emqx.com/images/8653151cecd5a961b77ba24a40373a4a.png)

5. 然后向 `mqttx_0c668d0d/demo` 主题分别发布长度为 5 字节和 172 字节的两条消息，我们将看到最终只会收到长度为 5 字节的消息，另一条超过 100 字节长度限制的消息没有被服务端转发：

   ![Publish two messages to the topic "mqttx_0c668d0d/demo"](https://assets.emqx.com/images/833e937b1195e1ca9e11f719e350053d.png)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
