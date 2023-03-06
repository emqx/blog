过去的 2 月份，EMQX 开源版发布了 v5.0.16、v5.0.17 以及 v5.0.18 三个版本，提供了 MQTT over QUIC 多流（multistream）支持。企业版 v4.3.19 以及 v4.4.15 开发完成，即将发布，数据集成将新增对 HStreamDB 最新版本的适配，并允许设置 RocketMQ 消息生产者投递策略，将相同属性的消息转发到同一 RocketMQ 队列（Queue）中。

正在开发中的功能还有基于 MQTT 的大文件传输，目前已经完成主体开发并在团队内部进行了 PoC Demo。同时，我们对[开源版 5.0 文档](https://www.emqx.io/docs/zh/v5.0)进行了大量重构和内容调整，以帮助用户更快上手使用 EMQX。

## MQTT over QUIC 多流支持

在 5.0.18 版本中，EMQX 利用 QUIC 的多路复用特性，扩展 MQTT over QUIC 实现了多流支持。

启用多流将为消息通信带来以下改善：

1. 解耦连接控制和消息传输；
2. 避免主题之间的队首阻塞，每个主题可以有独立的流以消除其他主题长阻塞带来的影响；
3. 解耦控制平面流量和数据平面流量；
4. 将上行数据（发布）和下行数据（消息接收）拆分为不同通道，更快地响应客户端操作；
5. 为不同主题设置不同流，实现主题优先级控制；
6. 提高客户端/服务器端处理的并行性；
7. 更健壮的 MQTT 数据处理：应用程序导致的单流中止不会导致连接关闭；
8. 更细粒度的收发端协同流量控制：可以对每一个流，同时对整个连接进行流控，实现更细粒度的流量控制；
9. 减少应用层的延迟：客户端在发送订阅或发布数据包之前不需要等待 CONNACK。

## MQTT 文件传输完成 PoC Demo

为满足物联网应用中各类如配置、传感器数据、媒体和 OTA 升级包等文件的传输，EMQX 设计了基于 MQTT 的文件传输功能。

相较于 HTTP/FTP 方案，基于 MQTT 的文件传输与消息传输使用了统一的技术栈，减少了额外的开发、运维和安全审计工作，并且能够实现整体流控，避免文件传输占用大量带宽从而影响业务消息传输。未来 EMQX 还将提供基于 MQTT over QUIC 的大文件传输能力，实现弱网环境下高效可靠文件传输。

本月 MQTT 文件传输已经完成主体开发，实现了大文件分块传输、断点续传、可靠传输等特性并进行了内部 PoC Demo，将在进一步开发和测试后与大家见面。

## 适配 HStreamDB 最新版

EMQX 数据集成支持最新 HStreamDB 0.13.0 版本，相较于此前支持的 0.8 版本，HStreamDB 0.13.0 能够支持更高的数据写入速度并加入了更多功能。

## RocketMQ 数据集成支持设置生产者投递策略

EMQX 支持将客户端消息和事件以生产者的身份投递到 RocketMQ 中，实现与 RocketMQ 的数据集成。

此前版本中 EMQX 采用了 RocketMQ 默认的轮询算法进行消息投递，消息会被投递到不同的队列中。本次发布中 EMQX 新增了生产者投递策略的设置，允许用户将相同客户端 ID、用户名或主题的消息投递到同一 RocketMQ 队列中，满足某些场景下，同一类型的消息投递和消费的顺序性保证。

## 功能增强

- 增加新的通用 TLS 选项 `hibernate_after`，在闲置一段时间后休眠 TLS 进程以减少其内存占用。默认值为 5s。
- 允许在 AuthZ 规则主题中任意位置使用占位符，例如 `{allow, {username, "who"}, publish, ["t/foo${username}boo/${clientid}xxx"]}.`
- 不再提供 Alpine Docker 镜像，Alpine 镜像的优势是体积非常小，但现在 EMQX 的 Alpine Docker 镜像体积已经大于基于 Debian Slim 的常规镜像，失去了存在价值。
- Prometheus 集成添加了 `live_connections.count` 和 `live_connections.max` 两个指标，用于统计活跃客户端的数量。
- HTTP API 支持 Proxy Protocol 协议，能够获取发起 HTTP 请求的客户端真实 IP。

## 问题修复

我们修复了多个已知 BUG，包括排他主题死锁问题、Replicant 节点无法手动加入集群问题。

各版本详细更新日志请查看：

- [EMQX 开源版 5.0.16](https://www.emqx.com/zh/changelogs/broker/5.0.16)
- [EMQX 开源版 5.0.17](https://www.emqx.com/zh/changelogs/broker/5.0.17)
- [EMQX 开源版 5.0.18](https://www.emqx.com/zh/changelogs/broker/5.0.18)

 

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
