[MQTT 协议](https://www.emqx.com/zh/mqtt-guide)在物联网，小型设备场景，移动应用等方面已经有了广泛的应用，并逐渐成为了物联网通讯的标准。本文重点介绍了组建 MQTT Broker 集群的挑战及负载均衡在 MQTT 集群中所起的作用。


## MQTT 协议

与大家熟悉的 HTTP 协议类似，MQTT 协议同样基于 TCP/TLS 之上，属于应用层协议（它也可以基于 HTTP 协议之上工作，本文暂不涉及这部分内容）。

MQTT 标准委员会对 MQTT 协议的释义如下：

MQTT 是用于物联网 (IoT) 的 OASIS 标准消息传递协议。它是一种非常轻量级的消息传输协议，采用了发布/订阅的机制，非常适合连接远程设备，无论是代码占用空间还是网络带宽的占用都很小。如今，MQTT 已被广泛用于汽车、工业制造、电信、石油和天然气等各个行业。

[MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)和 HTTP 客户端也很相似。它与服务器端建立一个 TCP 连接，通过该连接传输数据。不同的是，HTTP 采用的是请求/响应模型，而 MQTT 采用的是发布/订阅模型。

举个例子：客厅里安装的温度传感器，会间断性的把室内温度数值上传到 [MQTT 服务器上](https://www.emqx.io/zh)。而另一个智能家居设备订阅了这个温度传感器发布消息的频道，就可以获得室内的温度数据，并根据实际室温采取一些智能应对措施，比如当室内温度超过 32°C 时就打开空调。

## 可拓展性挑战

MQTT 协议听起来似乎离我们很遥远，其实它早已渗透到了我们的日常生活中。一般情况下，单个 MQTT 节点就可以满足单个家庭的智能家居设备连接需求，用户甚至可以在树莓派上运行一个 EMQX Edge （运行在边缘端的 MQTT 服务器）。而运行在云端的一个 EMQX 节点可以支撑高达 200 万的连接数，轻松满足普通智能家居场景需求。

但如果是全国的千百万辆汽车要联网，或者是上百万盏路灯要传递数据之类的场景，那么巨大的设备数（MQTT 客户端）和数据吞吐量，就远远超出了单个 MQTT 节点所能承受的压力，需要组建 MQTT 服务器集群。

在组建集群的同时，也面临着一系列的技术挑战：

1. 提供服务地址：如何让客户端知道该连接哪个地址？

2. 不同节点如何接管 MQTT 订阅者的会话，比如当一个客户端从一台服务器断连后，要如何在另一台服务器恢复连接？

3. 集群中各个节点上的路由表如何保持一致性？

通过在 MQTT 集群前面引入一个负载均衡，可以帮助我们轻松解决问题 1 和 2。


## MQTT 负载均衡

![MQTT 负载均衡](https://assets.emqx.com/images/017284bd21723e22993d75f2305jjsjajs.png)

<p align="center">MQTT 负载均衡</p>


为了应对上述问题，负载均衡需要能够根据配置的均衡策略来帮助客户端决定连接到哪个节点。 MQTT 集群负载均衡的主要功能有：

- 对外提供集群服务地址

  客户端只需要关心负载均衡的地址，而且不需要知道集群内各个节点的地址。这大大提升了服务器迁移和伸缩的灵活性。

- TLS 终结

  许多 MQTT 的用户选择在负载均衡这一层来终结 TLS，这样可以使 MQTT 服务器的资源被充分用于消息的处理。

- 平衡集群中各个节点的负载

  负载均衡服务通常可以配置不同的均衡策略，如：随机分配、轮询（有些轮询策略可以调节节点权重），还有比较有意思的粘性分配。

由于 MQTT 是基于 TCP/IP 之上的协议，因此可以在传输层进行负载均衡。而在传输层负载均衡之外，MQTT 能使用的负载均衡产品 HAProxy 2.4 和 Nginx Plus 还提供了应用层（MQTT 层）的负载均衡解决方案。

Nginx Plus 是在 Nginx（一个开源的 Web 服务器，适用于高流量网站的反向代理）基础上构建的应用程序交付平台。Nginx Plus 的[这篇文章](https://www.nginx.com/blog/nginx-plus-iot-load-balancing-mqtt/)作了较为详细的描述。

同样优秀的，还有 HAProxy。它提供高可用性负载均衡，以及基于 TCP、HTTP 和 MQTT 的应用程序代理。到目前为止（2021 年 8月），HAProxy 2.4 是唯一一款可以提供 MQTT 层负载均衡的免费产品。在他们的 [release note](https://www.haproxy.com/blog/announcing-haproxy-2-4/) 中，对 MQTT 负载均衡的功能作了简单的介绍。

在 “MQTT Broker 集群详解”系列的下一篇文章中，我们将对 HAProxy 2.4 + EMQX 4.3 的集成方案进行详细展开，敬请期待。



## 本系列中的其它文章

- [MQTT Broker 集群详解（二）：粘性会话负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)
- [MQTT Broker 集群详解（三）：有关 EMQX 水平可扩展性的挑战与对策](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
