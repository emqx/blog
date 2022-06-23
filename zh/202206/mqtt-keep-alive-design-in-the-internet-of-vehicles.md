随着车联网的快速发展，其应用场景也越来越丰富。除了在车辆行驶中进行相关数据传输上报，在车辆熄火状态下也可实现远程控车（远程启动、开启空调与开后备箱等）、OTA 升级等场景需求。为了给车主提供低时延、高成功率的使用体验，需要通过车联网平台与车机的心跳保活机制，保持长连接状态，并在车辆熄火的情况下快速远程唤醒车机，实现远程控车。

本篇文章将介绍车联网平台中 [MQTT](https://www.emqx.com/zh/mqtt) 的心跳保活和远程唤醒设计。

## MQTT 车联网通信消息保活

构建大型车联网平台时，为了实现车机与平台的高效实时通信，我们通常采用长连接方式通信（如 MQTT、HTTP、私有化 TCP 长连接等），本文主要围绕 MQTT 协议长连接通信与远程车控唤醒场景进行详细介绍。

### 业务场景

MQTT 本身也是采用 TCP 长连接的方式进行通信保活，TCP 长连接是指通过传输层三层握手建立的连接并长期保持，这样在应用层做消息传递请求的时候免去了 DNS 解析、连接建议等时间，大大加快了请求的速率，有利于消息的实时性。但同时我们需要端对端连接的维护和连接的保活。

![车联网 MQTT keep alive](https://assets.emqx.com/images/4dcd10cfba5d2663faecc3eda85c0185.png)
 

MQTT 是标准的 RFC 协议，相比私有协议更加标准。同时 MQTT 协议面向物联网场景设计，具有如下功能优势：

- 完善的心跳机制
- 支持遗嘱消息
- QoS 质量等级+离线消息
- 基于订阅发布的异步机制
- 低功耗，可以实现长连接低功耗保活和远程快速唤醒
- 采用 Topic 主题、支持安全扩展

使用 MQTT 协议建立车机与 TSP 等平台的长连接通信，可以有效解决对象唯一性与实时性等问题。其所具备的完善功能特性支持，适用于快速构建车联网业务，因此广泛应用于车联网 TSP 平台车控数据上报、远程控车、道路救援、高精地图、ADAS 和 C-V2X 等场景。

## MQTT 消息心跳保活

### MQTT Keep Alive 心跳机制

MQTT 协议设计了一套 Keep Alive 心跳机制。车机在与 Broker 建立连接的时候，我们可以传递一个 Keep Alive 参数，它的单位为秒。MQTT 协议中约定：在 1.5 倍 Keep Alive 的时间间隔内，如果 Broker 没有收到来自车机端的任何数据包，那么 Broker 认为它和车机端之间的连接已经断开；同样地，如果车机端没有收到来自 Broker 的任何数据包，那么车机端认为它和 Broker 之间的连接已经断开。

MQTT 还有一对 PINGREQ/PINGRESP 数据包，当 Broker 和车机端之间没有任何数据包传输的时候，可以通过 PINGREQ/PINGRESP 来满足 Keep Alive 心跳通信和连接状态检测。

- PINGREQ

  PINGREQ 数据包没有可变头（Variable header）和消息体（Payload），当 Client（车机端）在一个 Keep Alive 时间间隔内没有向 Broker 发送任何数据包，比如 Publish 和 Subscribe 的时候，它应该向 Broker 发送 PINGREQ 数据包。

- PINGRESP

  PINGRESP 数据包没有可变头（Variable header）和消息体（Payload），当 Broker 收到来自 Client 的 PINGREQ 数据包，它应该回复 Client 一个 PINGRESP 数据包。

对于 MQTT Keep Alive 机制，我们还需要注意以下几点：

- 如果在一个 Keep Alive 时间间隔内，车机端和 Broker 有过数据包传输，比如 Publish，车机端就没有必要再使用 PINGREQ 了，在网络资源比较紧张的情况下这点很重要；
- Keep Alive 值是由 Client 指定的，不同的 Client 可以指定不同的值，我们可以根据车机硬件和业务特性使用不同的 Keep Alive 值；
- Keep Alive 的最大值为 18 小时 12 分 15 秒（65535 秒），默认一般为 60s，我们可以根据车机的性能选择 10s、30s、60s 等值；
- Keep Alive 如果设为 0，则代表不使用 Keep Alive 机制。

### MQTT 心跳保活车联网场景设计

#### 通信保活

例如，假设我们选择了 30s 作为 Keep Alive 的心跳周期，我们在车机端建立与 Broker 连接的时候发送 Keep Alive 值为 30s。

- Broker 判断车机离线：

  在 1.5 倍 Keep Alive 的时间间隔即 45s 内，如果 Broker 没有收到来自车机端的任何数据包（包括PINGREQ），那么 Broker 认为它和车机端之间的连接已经断开，这个时候 Broker 就会把车机端状态离线，如果客户端有遗嘱消息，Broker 就向某个主题 Publish 这个遗嘱消息。

- 车机判断与 Broker 断开连接：

  同理，在 Keep Alive 周期内，如果车机端没有收到来自 Broker 的任何数据包（包括 PINGRESP），那么车机端认为它和 Broker 之间的连接已经断开，这个时候车机端可以设置重连机制，重新连接上 Broker。

当车辆熄火后，在一定周期内为了实现快速的远程控车响应，车机端的 T-Box 会自动进入低功耗的休眠模式，这时 T-Box 主控模块关闭，只保留通信模块工作（低功耗模式，一般在微安级），采用定时唤醒的方式给 Broker 发送心跳报文以保持长连接 Socket 通道。

#### 远程唤醒

之前为了实现车辆离线状态下远程控车场景，平台通常采用短信或电话振铃的方式对车机端 T-Box 进行远程唤醒。这种传统方式存在以下弊端：

1. 时延大且成功率不高：通过短信方式往往会有运营商短信延时，T-Box 唤醒后往往需要一定的时间启动，这个时候远程控车的消息有可能因为 T-box 未启动完成导致执行失败。
2. 运营成本较高：假如业务场景 1sms/车/天，100 万车机的系统短信产生的费用成本将会很高。

所以现在主机厂大多结合越来越成熟的 T-Box 终端采用 4G/5G 网络通信（MQTT消息）唤醒方式，通过低功耗的保活消息实现车机长连接（有些主机厂部分车型还采用双连接），当平台有车控消息下发时，车机端 T-Box 收到消息后迅速唤醒对应的 ECU 执行对应的车控指令，有效缩短了远程控车的消息时延，提升车主的使用感知，同时大大降低主机厂的运营成本。

## 基于 EMQX 的心跳保活系统架构

### 系统架构


![车联网架构](https://assets.emqx.com/images/2c2d7706e47457aaea2cdcff8fc8095f.png)
 

我们已在本系列之前的文章中介绍了[如何基于 EMQX 构建千万级的车联网平台架构](https://www.emqx.com/zh/blog/mqtt-messaging-platform-for-internet-of-vehicles)。[EMQX](https://www.emqx.com/zh/products/emqx) 支持 MQTT 3.1、3.1.1、5.0 全协议栈，基于 EMQX 构建的消息 Broker 集群可以完美实现 Keep Alive 心跳、遗嘱消息、保留消息等 MQTT 协议特性，支撑车联网平台的长连接保活和远程唤醒场景。

### EMQX 能力扩展

除了基本的心跳保活和远程唤醒场景支持外，根据车联网场景下的实际业务需求，EMQX 还增加了如下扩展功能，帮助车联网用户构建更加适应各类场景的平台应用。

- 增加心跳超时确认机制

  考虑到车联网场景车辆经常处于地下车库、隧道等网络不稳定的环境中，EMQX 增加了心跳超时确认机制，（可配置启用）在标准的 1.5 倍的 Keep Alive 周期之上再增加 1 倍的心跳时间，即在 2.5 个 Keep Alive 周期没收到心跳报文才会认为车机端因网络中断断开连接，可以优化在弱网场景客户端频繁上下线的问题。

- 心跳周期 Keep Alive 值支持 API 远程设置

  例如在某知名主机厂的车联网场景中，为了更好地控制电瓶馈电情况，当车主在熄火后，平台可以通过 EMQX 的离线消息功能感知车辆离线，这时 T-Box 自动进入休眠模式，并且 Keep Alive 时间间隔从 30s 自动设置为 300s。但由于 Broker 与车机建立连接时 Keep Alive 设置的是 30s，所以需要平台通知 Broker 同步将 Keep Alive 值修改为 300s。

EMQX 通过定制化能力扩展方式，提供标准化的 REST API 原子能力，TSP 在获取车机熄火的事件后第一时间调用 EMQX 提供的原子能力，将 Broker 与该车机的 Keep Alive 心跳周期设置为 300s，确保车机端 T-Box 进行低功耗休眠场景依然能够实现长连接保活。

## 结语

基于 MQTT 协议完善的长连接保活通信机制和 EMQX 强大的产品能力，车联网平台开发者可以快速构建高可用、低时延的车联网应用平台。随着 T-Box 的不断完善，通过双 APN 通信链路、提前唤醒（车主 APP 进入控车模式时提前唤醒 T-Box）或基于车机控车行为大数据分析更高效的馈电控制等方式，车企可以为广大车主提供更加优质的车联网业务体验。

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## 本系列中的其它文章

- [车联网平台搭建从入门到精通 01 | 车联网场景中的 MQTT 协议](https://www.emqx.com/zh/blog/mqtt-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 02 | 千万级车联网 MQTT 消息平台架构设计](https://www.emqx.com/zh/blog/mqtt-messaging-platform-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 03 | 车联网 TSP 平台场景中的 MQTT 主题设计](https://www.emqx.com/zh/blog/mqtt-topic-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 04 | MQTT QoS 设计：车联网平台消息传输质量保障](https://www.emqx.com/zh/blog/mqtt-qos-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 05 | 车联网平台百万级消息吞吐架构设计](https://www.emqx.com/zh/blog/million-level-message-throughput-architecture-design-for-internet-of-vehicles)
- [车联网平台搭建从入门到精通 06 | 车联网通信安全之 SSL/TLS 协议](https://www.emqx.com/zh/blog/ssl-tls-for-internet-of-vehicles-communication-security)
