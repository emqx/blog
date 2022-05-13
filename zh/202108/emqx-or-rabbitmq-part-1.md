本文素材来源于 RabbitMQ Summit 2019 会议上 Erlang Solutions 工程师 Grigory Starinkin  的发言内容。原内容主要对 [MQTT 消息服务器 EMQX](https://www.emqx.io/zh) 与 [RabbitMQ](https://www.rabbitmq.com) 进行了介绍及压力测试对比。在此基础上，我们对其进行了补充，深入分析了 EMQX 以及 RabbitMQ  的在核心架构上的侧重，并据此分析了它们为 [MQTT 集群](https://www.emqx.com/zh/blog/tag/mqtt-broker-集群)模式表现带来的不同影响。

## MQTT 协议 - 订阅和发布

[MQTT](https://www.emqx.com/zh/mqtt) 是一个非常轻量级的订阅和发布协议，现在已经是物联网领域最具统治地位和使用最广泛的传输协议。MQTT 协议每个消息最少仅需 2 个字节 （其中报头仅需 1 个字节，其余字节可以全部作为消息载荷）就可以完成通信，专为那些资源和空间有限、功耗敏感的硬件所打造。其主要模式是 Pub/Sub（发布/订阅），客户端可以扮演两个角色，一个角色是发布者，其在连接到服务器之后将针对某个特定主题发送消息给服务器；另一个角色是订阅者，可以订阅感兴趣的主题来接收其中的消息。订阅者也可以使用通配符订阅主题，这样就可以一次订阅多个不同的主题，还可以使用共享订阅进行负载均衡分发。

以下图片揭示了 MQTT 协议是如何运作的：

![MQTT协议运作.png](https://assets.emqx.com/images/0a32545afd5d82cd0988372700ab6bba.png)

目前市场上有很多 MQTT 客户端 SDK，也有很多 [MQTT Broker](https://www.emqx.io/zh)。EMQX 和 RabbitMQ 是 Erlang 家族中具有代表性的两大开源消息服务器，我们接下来将针对 MQTT 场景对其进行深入对比。



## EMQX 与 RabbitMQ

EMQX 是基于高并发的 Erlang/OTP 语言平台开发，支持百万级连接、分布式集群架构、发布订阅模式的开源 MQTT 消息服务器。开源至今，EMQX 在全球物联网市场得到了广泛应用。在开源版基础上，还陆续发展了商业版和提供云版本（cloud-hosting）（[https://www.emqx.com/zh/cloud](https://www.emqx.com/zh/cloud)）。EMQX 支持很多插件，具有强大拓展能力，用户依靠插件可以实现更多的功能。

RabbitMQ 是实现了高级消息队列协议（AMQP）的开源消息代理软件（亦称面向消息的中间件）。RabbitMQ 服务器也是基于 Erlang 语言开发的，现在可以通过插件配置的形式，使其支持 MQTT 协议。

不难发现，他们都选用了 Erlang 作为开发语言，并且他们都使用了 Erlang 语言携带的分布式数据库管理系统 —— Mnesia。Mnesia 适用于交换路由拓扑和在集群之内的节点之间交换信息。



## 压力测试

[MQTT 服务器](https://www.emqx.io/zh)在实际使用中的性能通常被用户作为判断一个服务器好坏的标准，因此本次评测也将重点关注这两个服务器在压力测试下的性能测试结果。

### 测试工具

本次压力测试的工具选用了 MZBench。MZBench（[https://github.com/mzbench/mzbench](https://github.com/mzbench/mzbench)） 是一个使用 Erlang 语言写的测试工具。它具有以下三个类型的节点：

- MZSever：可以用来创建场景（scenarios），例如创建一个发布者和多个订阅者。这些信息会作为服务器传送至 MZBench；
- MZController：从服务器产生的信息会进一步被传送到这里；
- MZNodes：它们会作为 [MQTT 客户端](https://www.emqx.com/zh/blog/category/mqtt-client)来连入你的集群，如下图所示。

![MZBench测试工具.png](https://assets.emqx.com/images/3f2695191e1017c93fe8a2c73f759847.png)

这次评测使用了一个云主机 M5 large 的实例，每个 MQTT 消息服务器集群由 3 个节点组成，每个节点的配置是双核，8GB 内存。需要强调的是，我们对于 EMQX 和 RabbitMQ 的测试使用了完全一致的硬件资源以消除变量。所有这些都配备了 Prometheus 节点导出器用于将指标推送到 Prometheus，并由 Grafana 进行最后的数据收集。

### 测试场景

压力测试将会有两个场景，「多对一」 和 「一对多」。

#### 多对一

许多设备作为发布者，如温度传感器或者是压力传感器，发送数据给一个服务器。服务器再将这些数据发送给一个控制器（即订阅者）处理这些数据。

![测试场景多对一.png](https://assets.emqx.com/images/542b8f4b662e0cd612c4f9aa2187b83f.png)

#### 一对多

一个控制器作为发布者将消息传送给服务器，再由服务器将这些消息传送给多个作为订阅者的设备。

![测试场景一对多.png](https://assets.emqx.com/images/df66fffee3d8775a81191448bbb8d6e1.png)

在每个场景里，「多」的那一方的数量将会从 2000 个逐渐上升到 10000 个。每个场景里，每一秒会发送一条载荷为 256 字节的消息。这样的发布并不会造成过大的吞吐量。仅仅使用 256 字节载荷是为了展示出这两个服务器的工作原理，以及他们的集群模式如何对这些场景作出反应的。

### 测试结果

左侧Y轴是指 CPU 占用，底部X轴是指「多」侧的客户端数量变化。

#### 多对一

从 「多对一」 的结果可以看出，EMQX 和 RabbitMQ 相比并没有太大差别。

![多对一测试结果.png](https://assets.emqx.com/images/aa65dc91c40366b8cf78ee5333d433f6.png)

#### 一对多

但是从「一对多」的结果来看，RabbitMQ 相比于 EMQX 确实有很明显的差距。

![一对多测试结果.png](https://assets.emqx.com/images/f6a014f85691501ce2f5679a7410fc42.png)

造成这种差距的原因是什么？我们将在《[EMQX 与 RabbitMQ 消息服务器 MQTT 性能对比（下）](https://www.emqx.com/zh/blog/emqx-or-rabbitmq-part-2)》中详细解析具体原因。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
