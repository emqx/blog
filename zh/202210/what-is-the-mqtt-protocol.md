## MQTT 协议简介

### 概览

[MQTT](https://mqtt.org/) 是一种基于发布/订阅模式的轻量级消息传输协议，专门针对低带宽和不稳定网络环境的物联网应用而设计，可以用极少的代码为联网设备提供实时可靠的消息服务。MQTT 协议广泛应用于物联网、移动互联网、智能硬件、车联网、智慧城市、远程医疗、电力、石油与能源等领域。

MQTT 协议由 [Andy Stanford-Clark](http://en.wikipedia.org/wiki/Andy_Stanford-Clark) （IBM）和 Arlen Nipper（Arcom，现为 Cirrus Link）于 1999 年发布。 按照 Nipper 的介绍，MQTT 必须具备以下几点：

- 简单容易实现
- 支持 QoS（设备网络环境复杂）
- 轻量且省带宽（因为那时候带宽很贵）
- 数据无关（不关心 Payload 数据格式）
- 有持续地会话感知能力（时刻知道设备是否在线）

据 Arlen Nipper 在 [IBM Podcast 上的自述](https://f.hubspotusercontent00.net/hubfs/6941105/Que%20es%20MQTT%20-%20IBM%20podcast%20-%20Piper,%20Diaz,%20Nipper%20-%2011182011-1.pdf)，MQTT 原名是 `MQ TT`，注意 `MQ` 与 `TT`之间的空格，其全称为: MQ Telemetry Transport，是九十年代早期他在参与 Conoco Phillips 公司的一个原油管道数据采集监控系统（pipeline SCADA system）时开发的一个实时数据传输协议。它的目的在于让传感器通过带宽有限的 [VSAT](https://en.wikipedia.org/wiki/Very-small-aperture_terminal) ，与 IBM 的 MQ Integrator 通信。由于 Nipper 是遥感和数据采集监控专业出身，所以按业内惯例取了 `MQ TT` 这个名字。

### MQTT 与其他协议对比

**MQTT vs HTTP**

- MQTT 的最小报文仅为 2 个字节，比 HTTP 占用更少的网络开销。
- MQTT 与 HTTP 都能使用 TCP 连接，并实现稳定、可靠的网络连接。
- MQTT 基于发布订阅模型，HTTP 基于请求响应，因此 MQTT 支持双工通信。
- MQTT 可实时推送消息，但 HTTP 需要通过轮询获取数据更新。
- MQTT 是有状态的，但是 HTTP 是无状态的。
- MQTT 可从连接异常断开中恢复，HTTP 无法实现此目标。

**MQTT vs XMPP**

MQTT 协议设计简单轻量、路由灵活，将在移动互联网、物联网消息领域，全面取代 PC 时代的 XMPP 协议。

- MQTT 报文体积小且编解码容易，XMPP 基于繁重的 XML，报文体积大且交互繁琐。
- MQTT 基于发布订阅模式，相比 XMPP 基于 JID 的点对点消息路由更为灵活。
- MQTT 支持 JSON、二进制等不同类型报文。XMPP 采用 XML 承载报文，二进制必须 Base64 编码等处理。
- MQTT 通过 QoS 保证消息可靠传输，XMPP 主协议并未定义类似机制。

## 为什么 MQTT 是适用于物联网的最佳协议？

据 IoT Analytics 最新发布的《2022 年春季物联网状况》研究报告显示，到 2022 年，物联网市场预计将增长 18%，达到 144 亿活跃连接。

在如此大规模的物联网需求下，海量的设备接入和设备管理对网络带宽、通信协议以及平台服务架构都带来了巨大的挑战。对于**物联网协议**来说，必须针对性地解决物联网设备通信的几个关键问题：网络环境复杂而不可靠、内存和闪存容量小、处理器能力有限。

MQTT 协议正是为了应对以上问题而创建，经过多年的发展凭借其轻量高效、可靠的消息传递、海量连接支持、安全的双向通信等优点已成为物联网行业的首选协议。

![MQTT 成为物联网首选协议](https://assets.emqx.com/images/a9926090d622d5f96789b9dc325da7c9.jpg)

### 轻量高效，节省带宽

MQTT 将协议本身占用的额外消耗最小化，消息头部最小只需要占用 2 个字节，可稳定运行在带宽受限的网络环境下。同时，MQTT 客户端只需占用非常小的硬件资源，能运行在各种资源受限的边缘端设备上。

### 可靠的消息传递

MQTT 协议提供了 3 种消息服务质量等级（Quality of Service），保证了在不同的网络环境下消息传递的可靠性。

- QoS 0：消息最多传递一次。

  如果当时客户端不可用，则会丢失该消息。发布者发送一条消息之后，就不再关心它有没有发送到对方，也不设置任何重发机制。

- QoS 1：消息传递至少 1 次。

  包含了简单的重发机制，发布者发送消息之后等待接收者的 ACK，如果没收到 ACK 则重新发送消息。这种模式能保证消息至少能到达一次，但无法保证消息重复。

- QoS 2：消息仅传送一次。

  设计了重发和重复消息发现机制，保证消息到达对方并且严格只到达一次。

更多关于 MQTT QoS 的介绍可查看博客：[MQTT QoS 服务质量介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

除了 QoS 之外，MQTT 还提供了[清除会话（Clean Session）](https://www.emqx.com/zh/blog/mqtt-session)机制。对于那些想要在重新连接后，收到离线期间错过的消息的客户端，可在连接时设置关闭清除会话，此时服务端将会为客户端存储订阅关系及离线消息，并在客户端再次上线后发送给客户端。

### 海量连接支持

MQTT 协议从诞生之时便考虑到了日益增长的海量物联网设备，得益于其优秀的设计，基于 MQTT 的物联网应用及服务可轻松具备高并发、高吞吐、高可扩展能力。

连接海量的物联网设备，离不开 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)的支持。目前，MQTT 服务器中支持并发连接数最多的是 EMQX。最近发布的 [EMQX 5.0](https://www.emqx.com/zh/blog/emqx-v-5-0-released) 通过一个 23 节点的集群达成了 [1 亿 MQTT 连接](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)+每秒 100 万消息吞吐，这使得 EMQX 5.0 成为目前为止全球最具扩展性的 MQTT 服务器。

### 安全的双向通信

依赖于发布订阅模式，MQTT 允许在设备和云之间进行双向消息通信。发布订阅模式的优点在于：发布者与订阅者不需要建立直接连接，也不需要同时在线，而是由消息服务器负责所有消息的路由和分发工作。

安全性是所有物联网应用的基石，MQTT 支持通过 TLS/SSL 确保安全的双向通信，同时 MQTT 协议中提供的客户端 ID、用户名和密码允许我们实现应用层的身份验证和授权。

### 在线状态感知

为了应对网络不稳定的情况，MQTT 提供了[心跳保活（Keep Alive）](https://www.emqx.com/zh/blog/mqtt-keep-alive)机制。在客户端与服务端长时间无消息交互的情况下，Keep Alive 保持连接不被断开，若一旦断开，客户端可即时感知并立即重连。

同时，MQTT 设计了[遗愿（Last Will） 消息](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)，让服务端在发现客户端异常下线的情况下，帮助客户端发布一条遗愿消息到指定的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)。

另外，部分 MQTT 服务器如 EMQX 也提供了上下线事件通知功能，当后端服务订阅了特定主题后，即可收到所有客户端的上下线事件，这样有助于后端服务统一处理客户端的上下线事件。

## MQTT 5.0 与 3.1.1

在 MQTT 3.1.1 发布并成为 OASIS 标准的四年后，MQTT 5.0 正式发布。这是一次重大的改进和升级，它的目的不仅仅是满足现阶段的行业需求，更是为行业未来的发展变化做了充足的准备。

MQTT 5.0 在 3.1.1 版本基础上增加了会话/消息延时、原因码、主题别名、用户属性、共享订阅等更加符合现代物联网应用需求的特性，提高了大型系统的性能、稳定性与可扩展性。目前，MQTT 5.0 已成为绝大多数物联网企业的首选协议，我们建议初次接触 MQTT 的开发者直接使用该版本。

如果您已经对 MQTT 5.0 产生了一些兴趣，想了解更多，您可以尝试阅读 [MQTT 5.0 探索](https://www.emqx.com/zh/mqtt/mqtt5)系列文章，该系列文章将以通俗易懂的方式为您介绍 MQTT 5.0 的重要特性。

## MQTT 服务器

MQTT 服务器负责接收客户端发起的连接，并将客户端发送的消息转发到另外一些符合条件的客户端。一个成熟的 MQTT 服务器可支持海量的客户端连接及百万级的消息吞吐，帮助物联网业务提供商专注于业务功能并快速创建一个可靠的 MQTT 应用。

[EMQX](https://www.emqx.io/zh) 是一款应用广泛的大规模分布式物联网 MQTT 服务器。自 2013 年在 GitHub 发布开源版本以来，目前全球下载量已超千万，累计连接物联网关键设备超过 1 亿台。

感兴趣的读者可通过如下 Docker 命令安装 EMQX 5.0 开源版进行体验。

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

也可直接在 EMQX Cloud 上创建完全托管的 MQTT 服务，现在[免费试用 EMQX Cloud](https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new)，无需绑定信用卡。

## MQTT 客户端

MQTT 应用通常需要基于 MQTT 客户端库来实现 MQTT 通信。目前，基本所有的编程语言都有成熟的开源 MQTT 客户端库，读者可参考 EMQ 整理的 [MQTT 客户端库大全](https://www.emqx.com/zh/mqtt-client-sdk)选择一个合适的客户端库来构建满足自身业务需求的 MQTT 客户端。也可直接访问 EMQ 提供的 [MQTT 客户端编程](https://www.emqx.com/zh/blog/tag/mqtt-客户端编程)系列博客，学习如何在 Java、Python、PHP、Node.js 等编程语言中使用 MQTT。

MQTT 应用开发还离不开 MQTT 测试工具的支持，一款易用且功能强大的 MQTT 测试工具可帮助开发者缩短开发周期，创建一个稳定的物联网应用。

[MQTTX](https://mqttx.app/zh) 是一款开源的跨平台桌面客户端，它简单易用且提供全面的 MQTT 5.0 功能、特性测试，可运行在macOS, Linux 和 Windows 上。同时，它还提供了命令行及浏览器版本，满足不同场景下的 MQTT 测试需求。感兴趣的读者可访问 MQTTX 官网进行下载试用：[https://mqttx.app/zh](https://mqttx.app/zh)。

![MQTT 客户端](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif?imageMogr2/thumbnail/1520x) 

 

## 快速体验 MQTT

至此，相信读者已对 MQTT 协议有了初步了解。接下来，读者可访问博客[MQTT 协议快速体验](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)了解如何开始使用 MQTT，或查看 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt)系列文章了解 MQTT 协议相关特性，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
