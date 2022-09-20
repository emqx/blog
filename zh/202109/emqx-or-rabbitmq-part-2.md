在[上篇文章](https://www.emqx.com/zh/blog/emqx-or-rabbitmq-part-1)中，我们采用相同的硬件资源分别对 [MQTT 消息服务器 EMQX](https://www.emqx.io/zh) 和 [RabbitMQ](https://www.rabbitmq.com) 进行了压力测试。结果表明：在「多对一」 场景中，EMQX 和 RabbitMQ 相比并没有太大差别；而在「一对多」场景中，RabbitMQ 则较 EMQX 产生了较为明显的差距。

本期文章中我们将对这一结果进行进一步的解析。

造成差距的原因主要有三个：节点间通讯的方式、消息流架构的方式、队列的使用。



## 节点间的通讯

### RabbitMQ - 委托架构

RabbitMQ 使用了 Erlang 语言的分布式连接，即每个节点之间两两互相连接，每个节点用一个单一的链接连接着另一个节点。在图中的情况下，三个节点依次连接；当节点之间需要通信时，一条消息需要通过这个单一链接从一个节点发送到另一节点。

![RabbitMQ连接.png](https://assets.emqx.com/images/77d2292e39b54f54985bcba287647754.png)

在扇出（fan-out）的例子中，正常来讲你需要将消息推送到所有节点的队列上。RabbitMQ 使用的优化方式则是：你的消息只需要发送一次，之后其内置的代理委托框架会将这一条消息派送并且发到其他节点的队列上。这个过程中，消息是有序发送的，所以保证了消息在不同队列里都是相同的顺序。

![RabbitMQdelegate1.png](https://assets.emqx.com/images/6b7b0e22e32e14c876164a894f9f3505.png)

但是这个方案也不是十全十美的，因为你会将所有的消息只发送一次，在分发工作都依靠同一个委托进程。而且 RabbitMQ 选择这个代理进程的策略是根据发布者的哈希算法。所以，当如果你只有一个发布者，所有的消息都会被一直推送到单个的委托代理进程。

![RabbitMQdelegate2.png](https://assets.emqx.com/images/3701be881446123170efa08751cd5c2f.png)

### EMQX - Gen_RPC

在 EMQX 中有个精妙的设计：其不仅存在着分布式连接，还存在着 Gen_RPC。分布连接和 Gen_RPC 各司其职，前者用于交换 Mnesia 的数据信息，后者则只适用于消息的转发。每当你需要从一个节点向另一个节点发布一个消息的时候，EMQX 不是重新自动生成新的节点间链接（默认 1 个连接），再通过这些新的连接去处理把一个消息从一个节点推送到另一个节点的工作。而是依靠针对此场景特地设计的，专有的 Gen_RPC 连接来处理这个消息推送的工作。所以在扇出（一对多）的例子中，这些链接会被完全有效地利用。

![EMQx连接.png](https://assets.emqx.com/images/85793cea9e516f5981fba9299240fe6f.png)
![EMQxgen_rpc.png](https://assets.emqx.com/images/fee9e2f293c7e5b5ca7fc585ccc433dd.png)

但这种设计在网络分区环境中其性能有可能受到影响，RabbitMQ 节点之间只有一个分布式连接，所以当连接断开造成脑裂时，愈合修复的工作将会更简单。



## 消息流

### MQTT 插件

RabbitMQ 在使用 MQTT 插件后会监听使用 [MQTT 协议](https://www.emqx.com/zh/mqtt)发布的消息。得到消息之后，消息被解析，之后再通过 AMQP 协议进行转化，最后才会被发送到 RabbitMQ 上。

![MQTT插件.png](https://assets.emqx.com/images/1197c10dd374beb30c9c14d8631801b6.png)

如果要发送一条消息，需要经过套接字后进入 mqtt_reader，接下来再进入下图所示的所有过程。然而如果要在同一条通道里同时接收刚刚发送的这条消息，所有上图所示的过程则需要反着重新进行一次，包括 mqtt_reader。其中，mqtt_reader 不仅负责了读，也负责了写。

![RabbitMQ流量控制.png](https://assets.emqx.com/images/f911ce3b56e625fefaf3dcaa9862eaf3.png)

### AMQP

AMQP 场景则不同，每条消息都被一个 reader 读取，一个 writer 写入。这两条通道读写独立，reader 只负责读内容，而 writer 只负责写内容，它们各司其职、相互独立。而唯一的通道 channel 则是一个主 Erlang 进程，其负责着消息的交换。

![AMQP.png](https://assets.emqx.com/images/17717215892fdfd1f1b7a5b47b327d9b.png)

可见 RabbitMQ 在 MQTT 场景中存在的明显的设计问题会导致性能下降，那么如果引入 AMQP 模式的 RabbitMQ 测试用例将会如何呢？将 RabbitMQ 调制成使用 MQTT 插件的和使用单一 AMQP 的模式使用，再对比 EMQX 在压力测试下的情况，可以看出 EMQX 在所有测试中仍是更胜一筹，但总体来说使用 AMQP 模式的 RabbitMQ 要比自己原有的成绩更好。

#### 多对一

![多对一测试结果.png](https://assets.emqx.com/images/4ffa40292efbbe92616e2c78d88547c6.png)

此场景中 RabbitMQ 与 EMQX 已经有了接近的性能表现。

#### 一对多

![一对多测试结果.png](https://assets.emqx.com/images/2e39662f8ccb2cc9dab490197e0a2e22.png)

但如果在 fan-out（一对多)场景里，EMQX 仍然具有显著优势，但 RabbitMQ（AMQP）的差距已经明显缩小。



## 队列

以上的测试均使用了 QoS 1 的消息。当发送 QoS 1 的消息时，这些消息每次都要作为可持久化的备份保存在硬盘上。所以队列空间的使用也尤为重要。

### RabbitMQ

RabbitMQ 成熟地使用了一个默认的队列空间执行方式（可以被替换成其他队列使用）。这个可变队列在消息的持久度和给客户端发送消息的时延里做了均衡。但是在最坏的情况下，一个消息可能会被存入内存。不过这也帮助了 RabbitMQ 在崩溃重启之后可以让服务器再上线，并且所有的客户端还可重连且收到原来持久化的消息。

![RabbitMQQueue.png](https://assets.emqx.com/images/66284df763ff39f0b5fe45b52ba823e2.png)

### EMQX

EMQX 对队列的实现方式非常简单，即在内存中使用了优先队列。如果发来的消息无法推入接收者的队列，则这个消息会被丢掉。在 EMQX 中，只有用一些其他持久化的插件才能使消息持久化保存，这些功能在商业版中提供。

![EMQxQueue.png](https://assets.emqx.com/images/7eda1f96d217ecf4119212cf6bbdea44.png)

EMQX 的设计初衷是将接入层独立，所以将消息持久化的问题留给了后端完成。这一问题在未来具有持久性会话的版本中会解决（persistence session）。



## 节流

### RabbitMQ - 控流

RabbitMQ 采用了一种比较有名的控流机制，它给每一个流程了一个信用值，如下图所示。假设说我们的服务端接收到了一个消息并由 reader 进行了读取后，这条消息被送到 channel。这个过程将会消费掉 reader 和 channel 的相应的信用值。这样一来，就可以通过使两方信用值保持匹配同步的方法实现不超额的发送了。

![RabbitMQ流量控制.png](https://assets.emqx.com/images/372175d7554a2961d4c7d6b6dd1795ef.png)

这其实是一个不错的解决方案。设想我们有许多的用户，即有许多的队列，每发送一条消息就意味着将要将这条消息分发给许多的队列，这会严重影响 RabbitMQ 实例。然而，这一套流程会阻止 RabbitMQ 再继续读区接收缓冲区的消息——因为发送缓冲区已经快满了！

### EMQX - 限流

![EMQxRateLimit.png](https://assets.emqx.com/images/cca55a9d048c822eff3cd9c248990b20.png)

EMQX 的节流主要是靠限制读取一方的流量去实现的。首先，根据预设，将会一次从套接字内读取 200 条消息。当这些消息被完全收到了之后才会逐个将他们处理。一旦套接字报告它已经到达了读取一方的最大限额，它将会检查有发布者的数量和已经被阅读的字节数量，并根据这个数值去休眠一段时间。接收缓冲区最终会被填满，发布者根据 TCP 协议中飞行窗口的要求也将不会再发布任何内容。



## 总结

以上就是这个横向评测的结果和分析。最终的赢家很难断言，但是如果就服务器的性能上来讲，EMQX 肯定是略胜一筹的。不过 RabbitMQ 也有它独特的优势。

### EMQX 的设计原则

EMQX 在设计上，首先分离了前端协议 (FrontEnd) 与后端集成 (Backend)，其次分离了消息路由平面 (Flow Plane) 与监控管理平面 (Monitor/Control Plane)：

![EMQX 的设计原则.png](https://assets.emqx.com/images/81898acde206deb5c88bc237bcac7c7a.png)

1. EMQX 核心解决的问题：处理海量的并发 MQTT 连接与路由消息。
2. 充分利用 Erlang/OTP 平台软实时、低延时、高并发、分布容错的优势。
3. 连接 (Connection)、会话 (Session)、路由 (Router)、集群 (Cluster) 分层。
4. 消息路由平面 (Flow Plane) 与控制管理平面 (Control Plane) 分离。
5. 支持后端数据库或 NoSQL 实现数据持久化、容灾备份与应用集成。

### EMQX 的系统分层

1. 连接层 (Connection Layer)：负责 TCP 连接处理、 MQTT 协议编解码。
2. 会话层 (Session Layer)：处理 MQTT 协议发布订阅消息交互流程。
3. 路由层 (Route Layer)：节点内路由派发 MQTT 消息。
4. 分布层 (Distributed Layer)：分布节点间路由 MQTT 消息。
5. 认证与访问控制 (ACL)：连接层支持可扩展的认证与访问控制模块。
6. 钩子 (Hooks) 与插件 (Plugins)：系统每层提供可扩展的钩子，支持插件方式扩展服务器。

而 RabbitMQ 则更类似于 Kafka 的消息队列缓存设计。建议在 IoT 项目中将两者结合使用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
