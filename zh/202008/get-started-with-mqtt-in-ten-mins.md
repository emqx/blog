[MQTT](https://www.emqx.com/zh/mqtt) 全称为 Message Queuing Telemetry Transport（消息队列遥测传输），是一种基于 **发布/订阅** 模式的 **轻量级物联网消息传输协议**。[IBM](https://zh.wikipedia.org/wiki/IBM) 公司的安迪·斯坦福-克拉克及 Arcom 公司的阿兰·尼普于 1999 年撰写了该协议的第一个版本[^1]，之后 MQTT 便以简单易实现、支持 QoS、轻量且省带宽等众多特性逐渐成为了 IoT 通讯的标准。


## MQTT 协议基本特点

- 使用发布/订阅消息模式，提供了一对多的消息分发和应用程序的解耦。
- 不关心负载内容的消息传输。
- 提供 3 种消息服务质量等级，满足不同投递需求。
- 很小的传输消耗和协议数据交换，最大限度减少网络流量。
- 提供连接异常断开时通知相关各方的机制。


## MQTT 应用行业

MQTT 作为一种低开销，低带宽占用的即时通讯协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它适用于硬件资源有限的设备及带宽有限的网络环境。因此，MQTT 协议广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。

- 物联网 M2M 通信，物联网大数据采集。
- 移动即时消息，及消息推送。
- 智能硬件、智能家居、智能电器。
- 车联网通信，电动车站桩采集。
- 智慧城市、远程医疗、远程教育。
- 电力、石油与能源等行业市场。



## MQTT 协议原理

基于发布/订阅模式的 MQTT 协议中有三种角色：发布者（Publisher）、代理（Broker）、订阅者（Subscriber）。发布者向代理发布消息，代理向订阅者转发这些消息。通常情况下，客户端的角色是发布者和订阅者，服务器的角色是代理，但实际上，服务器也可能主动发布消息或者订阅主题，客串一下客户端的角色。

为了方便理解，MQTT 传输的消息可以简化为：主题（Topic）和载荷（Payload）两部分：

- Topic，消息主题，订阅者向代理订阅主题后，一旦代理收到相应主题的消息，就会向订阅者转发该消息。
- Payload，消息载荷，订阅者在消息中真正关心的部分，通常是业务相关的。



## MQTT 协议基础概念

### 客户端 （Client）

使用 MQTT 协议的程序或设备。它可以

- 打开连接到服务端的网络连接
- 发布应用消息给其它相关的客户端
- 订阅以请求接受相关的应用消息
- 取消订阅以移除接受应用消息的请求
- 关闭连接到服务端的网络连接

### 服务器（Server）

在发送消息的客户端与已订阅的客户端之间充当中介角色的程序或设备，它可以

- 接受来自客户端的网络连接
- 接受客户端发布的应用消息
- 处理客户端的订阅和取消订阅请求
- 转发应用消息给符合条件的已订阅客户端
- 关闭来自客户端的网络连接

### 会话（Session）

每个客户端与服务器建立连接后就是一个会话，客户端和服务器之间有状态交互。会话可以存在于一个网络连接之间，也可以跨越多个连续的网络连接存在。

### 订阅（Subscription）

订阅包含一个主题过滤器（Topic Filter）和一个最大的服务质量（QoS）等级。订阅与单个会话（Session）关联。会话可以包含多于一个的订阅。会话的每个订阅都有一个不同的主题过滤器。

### 主题名（Topic Name）

附加在应用消息上的一个标签，被用于匹配服务端已存在的订阅。服务端会向所有匹配订阅的客户端发送此应用消息。

### 主题过滤器（Topic Filter）

仅在订阅时使用的主题表达式，可以包含通配符，以匹配多个主题名。

MQTT 主题的更多特性请访问我们的博文：[MQTT 主题的高级特性](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)。

### 载荷（Payload）

对于 PUBLISH 报文来说载荷就是业务消息，它可以是任意格式（二进制、十六进制、普通字符串、JSON 字符串、Base64）的数据。



## MQTT 报文结构

MQTT 报文由三部分组成，分别为：固定报头（Fixed header）、可变报头（Variable header）以及有效载荷（Payload）。包含报文类型等字段的固定包头存在于所有 MQTT 报文中。可变报头的内容根据报文类型的不同而不同，一些报文中甚至不存在可变报头。有效载荷通常是与业务/场景相关的数据，例如对 PUBLISH 报文来说有效载荷就是应用消息，对 SUBSCRIBE 报文来说有效载荷就是订阅列表。



## MQTT 协议进阶

### 消息服务质量（QoS）

MQTT 协议提供了 3 种消息服务质量等级（Quality of Service），它保证了在不同的网络环境下消息传递的可靠性。

- QoS 0：消息最多传递一次，如果当时客户端不可用，则会丢失该消息。
- QoS 1：消息传递至少 1 次。
- QoS 2：消息仅传送一次。

QoS 更多介绍请访问我们的博文：[MQTT QoS 服务质量介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

### 清除会话（Clean Session）

MQTT 客户端向服务器发起 CONNECT 请求时，可以通过 `Clean Session` 标志设置是否创建全新的会话。

- `Clean Session` 设置为 0 时
  - 如果存在一个关联此客户标识符的会话，服务端必须基于此会话的状态恢复与客户端的通信。
  - 如果不存在任何关联此客户标识符的会话，服务端必须创建一个新的会话 
- `Clean Session` 设置为 1，客户端和服务端必须丢弃任何已存在的会话，并开始一个新的会话。

### 保活心跳（Keep Alive）

MQTT 客户端向服务器发起 CONNECT 请求时，通过 Keep Alive 参数设置保活周期。

客户端在无报文发送时，按 Keep Alive 周期定时发送 2 字节的 PINGREQ 心跳报文，服务端收到 PINGREQ 报文后，回复 2 字节的 PINGRESP 报文。

服务端在 1.5 个心跳周期内，既没有收到客户端发布订阅报文，也没有收到 PINGREQ 心跳报文时，将断开客户端连接。

### 保留消息（Retained Message）

MQTT 客户端向服务器发布（PUBLISH）消息时，可以设置保留消息（Retained Message）标志。保留消息会驻留在消息服务器，后来的订阅者订阅主题时可以接收到最新一条保留消息。

### 遗嘱消息（Will Message）

MQTT 客户端向服务端发送 CONNECT 请求时，可以携带遗嘱消息。MQTT 客户端异常下线时（客户端断开前未向服务器发送 DISCONNECT 消息)，MQTT 消息服务器会发布遗嘱消息。

MQTT 遗嘱消息的更多请访问我们的博文：[MQTT 遗嘱消息的使用](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。



## MQTT 5.0 协议新增特性

### 会话过期
[MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 把 Clean Session 标识拆分成 Clean Start 标识（指示会话应该在不使用现有会话的情况下开始）和会话过期间隔属性（指示连接断开之后会话保留的时间）。会话过期间隔可以在断开连接时修改。把 Clean Start 标识设置为 1 且会话过期间隔设置为 0，等同于在 MQTT v3.1.1中把 CleanSession 设置为 1。

### 为所有响应报文提供原因码

更改所有响应报文以包含原因码，包括 CONNACK，PUBACK，PUBREC，PUBREL，PUBCOMP，SUBACK，UNSUBACK，DISCONNECT 和 AUTH，以使得调用方确定请求的函数是否成功。

### 请求/响应
规定 MQTT 请求/响应模式，提供响应主题和对比数据属性，以使得响应消息被路由回请求的发布者。此外，为客户端添加从服务端获取关于构造响应主题的配置信息的能力。

### 共享订阅
添加对[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)的支持，允许多个订阅消费者进行[负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)。

### 主题别名
支持将主题名缩写为整数来减小 MQTT 报文的开销。客户端和服务端可以分别指定它们允许的主题别名的数量。



## 下一步

读完本文之后，读者若是想试用一下 MQTT ，可访问 EMQ 官网 [免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 页面，该页面提供了一个在线的 MQTT 5.0 服务器，您可以将它用于 MQTT 的学习、测试或原型设计。

读者也可访问我们的博文 [2020 年常见 MQTT 客户端工具比较](https://www.emqx.com/zh/blog/mqtt-client-tools)，选择一款适合自己的 MQTT 客户端工具快速体验 MQTT 协议。


[^1]: [https://zh.wikipedia.org/wiki/MQTT#%E5%8E%86%E5%8F%B2](https://zh.wikipedia.org/wiki/MQTT#历史)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
