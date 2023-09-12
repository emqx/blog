8 月 31 日，EMQ 举办了 [EMQX Enterprise 5.1 线上发布会](https://www.emqx.com/zh/events/mqtt-made-easy-introducing-emqx-5-1)，介绍了此次新版本的更新与改进，以及 EMQX Enterprise 在石油行业和车联网领域的实际应用。发布会期间，我们收到了许多提问，以下是我们整理的相关 EMQX Enterprise 5.1 发布会期间的问题和相关回答文档，希望对您有所帮助。


## 1. 运营商对 QUIC 的支持如何保证?

A: 目前运营商在公网上对 UDP 确实有一些限制，要解决这个问题，一方面的企业可以和运营商去做这方面的沟通，如果确实要用到 UDP 的话，作为专线的客户来讲运营商是可以提供这方面的一些支撑和服务的；另一方面从技术层面来说，EMQ 提供的 SDK 跟 [NanoMQ](https://nanomq.io/zh) 都提供了回退能力，在 QUIC 受限的时候能够自动切换到 TCP 协议上。


## 2. 没有网络 QUIC 也不断连吗？

A: 并不是不会断连，而是断连之后应用层能够快速感知状态变化，客户端和服务器之间可以在网络恢复后更快地重新建立连接。我们做了一些测试，参考 [QUIC vs TCP/TLS 测试对比](https://www.emqx.com/zh/blog/mqtt-over-quic#quic-vs-tcp-tls-测试对比) ，在网络不稳定、连接多变的物联网场景下，测试数据也表明，基于 QUIC 0 RTT/1 RTT 重连/新建能力，MQTT over QUIC 能够在弱网与不固定的网络通路中有效提升用户体验。


## 3. 怎么做数据重要性的划分呢? 数据重要与否的依据是什么?

A: 这其实是一个业务问题，不同行业比如工业制造或者车联网有不同场景。例如，在工业制造行业，一些信号是持续发送的，可能我们更关注的是信号的变化量。对一些比较重要的业务来说，告警消息是最重要的。工业制造、车联网等行业普遍有告警相关的数据，它的出现会引发很重要的业务流程，需要快速去处理。

MQTT over QUIC 也支持了 multistream 多流能力，可以针对同一个连接不同的业务场景使用不同的 topic 来实现优先级传输。


## 4. 能讲讲共享订阅的均衡策略吗？实测好几种都不是很理想  

A: 这主要取决于你的业务，EMQX 默认的策略是随机，你可以设置为 `round_robin` 循环方式选择订阅者，这两个其实能够适应大部分场景了。如果你需要固定的订阅来自同一个主题或者发布者的消息，可以使用 `hash_topic` 以及 `hash_clientid`。

还有其他策略可以在我们[文档](https://docs.emqx.com/zh/enterprise/v5.1/configuration/configuration-manual.html#mqtt-基本参数:~:text=mqtt.shared_subscription_strategy)跟 Dashboard 配置界面上查看，根据情况灵活选择即可。如果你要解决的是消息量过大共享订阅无法处理的情况，那应该使用 EMQX Enterprise，使用数据集成直接将数据写入到外部的数据系统。

 
## 5. EMQX 在传输文件时，是否可以正常传输其他消息，或者在传输文件期间消息是否会被阻塞？

A: MQTT over TCP 下，一个连接只有一个通道，进行文件传输时会阻塞消息。但 MQTT 文件传输支持断点续传，可以通过本地调度优化：检测到高优先级消息时暂停文件传输，先发送消息，然后继续传输文件。这样可以减少文件传输对消息造成的影响。

 
## 6. QUIC 内置的加密算法是支持多种不同的算法还是固定的某个算法呢?

A: QUIC 协议内置了加密功能，并支持多种不同的加密算法。

 
## 7. 怎么处理上下线不一致的问题？  

A: MQTT 通过心跳机制检测客户端在线状态。服务器端可以配置心跳间隔时间，如果超过此间隔未收到客户端心跳包，则认为客户端已断开连接。客户端断开连接事件可以反馈到 Dashboard 客户端列表，也可以通过数据集成发送到外部服务。缩短心跳间隔可以更快检测到客户端的离线，但会增加一定的网络流量。可以根据实际业务需求选择合理的心跳间隔，以平衡敏感度和流量消耗。


## 8. OTA 升级文件是如何传输的？是用 HTTP 还是 MQTT 文件传输？

A: OTA 升级主要是下行大流量传输，使用最多的还是基于 HTTP 的 CDN 技术，目前 MQTT 文件传输更多场景是客户端到服务器的北向传输。

 
## 9. QUIC 协议部署和兼容性怎么处理?

A: 部署上，一种方式是改造客户端，使用 QUIC 的 SDK 进行开发接入，目前我们提供了 Java, C, Python 的客户端 SDK；另一种方式可以通过 NanoMQ 进行桥接，设备到 NanoMQ 是 MQTT 协议，NanoMQ 到云端的 EMQX 是 QUIC 协议，这种方式是最简单的，也可以作为快速验证的首选。兼容性上，无论是 SDK 跟 NanoMQ，我们都提供了回退能力，支持在 UDP 受限的情况下底层自动切换到 TCP/TLS。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
