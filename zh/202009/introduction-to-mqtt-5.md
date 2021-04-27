

### MQTT 简介

[MQTT 协议](https://www.emqx.cn/mqtt) 因为其轻量、灵活等特点成为了当今世界上最受欢迎的物联网协议，它已经广泛应用于车联网、智能家居、物流、即时聊天应用和移动消息推送等领域，连接了数以亿计的设备，并且每时每刻都有无数设备开始使用和接入 MQTT 协议。MQTT 协议为这些设备提供了稳定、可靠的通信基础，这些设备庞大的接入数量也向 MQTT 协议规范提出了挑战，[MQTT 5.0](https://www.emqx.cn/mqtt/mqtt5) 的诞生便是为了更好地满足这一需求。



### MQTT 历史

MQTT（消息队列遥测传输）最初由 IBM 于上世纪 90 年代晚期发明。它最初的用途是将石油管道上的传感器与卫星相链接，所以 MQTT 从诞生之初就是专为受限设备和低带宽、高延迟或不可靠的网络而设计，它使用了发布订阅模型，在空间和时间上解耦了消息的发送者与接收者，并且基于 TCP/IP 提供稳定可靠的网络连接，拥有非常轻量的报头以减少传输开销，支持可靠消息传输，可以说天生就满足了物联网场景的各种需求。在 MQTT 3.1.1 发布并成为 OASIS 标准的四年后，MQTT 5.0 正式发布，这是一次重大的改进和升级，它的目的不仅仅是满足现阶段的行业需求，更是为行业未来的发展变化做了充足的准备。2019 年 3 月，MQTT 5.0 成为了新的 OASIS 标准。



### MQTT 5.0 设计目标

面对迅速增长的设备数量和层出不穷的需求，OASIS MQTT 技术委员会需要从繁杂的需求中提取出通用部分，将其纳入标准规范，并且尽可能不增加开销或降低易用性，在不增加不必要的复杂性的前提下提高性能和易用性。

最终，OASIS MQTT 技术委员会为 MQTT 5.0 添加了大量的全新功能与特性，5.0 成为 MQTT 有史以来变化最大的一个版本。在这里，我们将列举一些比较重要的特性：

- 改进的错误报告。现在，所有响应报文都将包含原因码和可选的人类易读的原因字符串。
- 规范通用模式，包括能力发现和请求响应等。
- 对共享订阅的协议支持，此前标准无共享订阅的内容，共享订阅由各个软件厂商自已定义，不具备通用性。
- 新的扩展机制，包括用户属性。
- 引入主题别名等新特性进一步减小传输开销
- 增加了会话过期间隔和消息过期间隔，用以改善老版本中 Clean Session 不够灵活的地方。

完整的新属性列表包含在协议标准的附录C，您可以访问以下网址了解详情：https://docs.oasis-open.org/mqtt/mqtt/v5.0/cs02/mqtt-v5.0-cs02.html#AppendixC。



### 拥抱 MQTT 5.0

随着各 [MQTT 服务器](https://www.emqx.cn/products/broker) 厂商不断加入 MQTT 5.0 的支持阵营（例如 [EMQ](https://www.emqx.cn/) 在 2018 年 9 月就已经完整支持了 MQTT 5.0 协议），整个行业生态逐步迁移至 MQTT 5.0 已经成为大的趋势，MQTT 5.0 也将是未来绝大多数物联网企业的首选。我们也希望用户能够尽早拥抱 MQTT 5.0 并且享受到它带来的便利，这也是这篇文章的目的。如果您已经对 MQTT 5.0 产生了一些兴趣，但还想了解更多，您可以尝试阅读以下文章，我们将以通俗易懂的方式为您介绍 MQTT 5.0 的重要特性：

- [全新开始标识与会话过期间隔](https://www.emqx.cn/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)
- 消息过期间隔
- [原因码与 ACK](https://www.emqx.cn/blog/mqtt5-new-features-reason-code-and-ack)
- [载荷格式和内容类型](https://www.emqx.cn/blog/mqtt5-new-features-payload-format-indicator-and-content-type)
- 请求响应
- [共享订阅](https://www.emqx.cn/blog/introduction-to-mqtt5-protocol-shared-subscription)
- [订阅标识符与订阅选项](https://www.emqx.cn/blog/subscription-identifier-and-subscription-options)
- 主题别名
- [流量控制](https://www.emqx.cn/blog/mqtt5-flow-control)
- 用户属性
- [增强认证](https://www.emqx.cn/blog/mqtt5-enhanced-authentication)



