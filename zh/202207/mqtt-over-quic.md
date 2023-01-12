>**引言：首个将 QUIC 引入 MQTT 的开创性产品**
>
>在最新发布的 [5.0 版本](https://www.emqx.com/zh/blog/emqx-v-5-0-released)中，EMQX 开创性地引入了 QUIC 支持。
>
>QUIC 是下一代互联网协议 HTTP/3 的底层传输协议，与 TCP/TLS 协议相比，它**在减少连接开销与消息延迟的同时，为现代移动互联网提供了有效灵活的传输层。**
>
>基于 QUIC 这些极适用于物联网消息传输场景的优势，EMQX 5.0 引入 QUIC 支持（MQTT over QUIC）并设计了独特的消息传输机制和管理方式。

本文将通过对 MQTT over QUIC 的详细解析，为大家展现这一领先技术实现对于物联网场景的优势与价值，帮助大家更有效地借助 EMQX 5.0 对 QUIC 的支持能力，在各类 MQTT 应用场景中进行更加高效、低成本的物联网数据传输。

## 什么是 QUIC

[QUIC](https://datatracker.ietf.org/doc/html/rfc9000) 是一种建立在 UDP 之上通用的传输层网络协议，最初由 Google 提出，作为 TCP+TLS 的替代方案，旨在改善用户体验。

与现有的 TLS over TCP 方案相比，QUIC 有很多优势：

- 快速建立低延迟连接（1 RTT 或者 0 RTT）
- 端到端加密，握手通过 TLS 1.3 进行身份验证
- 避免队头阻塞的多路复用
- 改进的拥塞控制，可插拔的拥塞控制策略
- 多路径支持，连接平滑迁移
- 无状态负载均衡
- 现有网络无需改造升级即可支持

因其高效的传输效率和多路并发的能力，QUIC 已经成为下一代互联网协议 HTTP/3 的底层传输协议。

> **HTTP/3 协议介绍**
>
> 2018 年 10 月，IETF 的 HTTP 和 QUIC 工作组联合决定将 QUIC 上的 HTTP 映射称为 [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3)，以提前使其成为全球标准。2022 年 6 月 6 日，IETF 将 HTTP/3 标准化为 [RFC](https://en.wikipedia.org/wiki/Request_for_Comments) <sup>[9114](https://datatracker.ietf.org/doc/html/rfc9114)</sup>。
>
> HTTP/3 的目标是通过解决 HTTP/2 的传输相关问题，在所有形式的设备上提供快速、可靠和安全的 Web 连接。HTTP/3 使用与 HTTP/2 版本类似的语义，包括相同的请求方法、状态代码和消息字段，两者根本区别在于，HTTP/2 底层使用的是 TCP/TLS 协议，而 HTTP/3 使用的是 QUIC 协议。
>
> 根据 [W3Techs 统计](https://w3techs.com/technologies/details/ce-http3)，互联网至少 40% 的流量是基于 QUIC 的，前 1000 万个网站中的 25% 已经支持 HTTP/3 协议，包括 Google，Youtube，Facebook 等顶流站点。

## QUIC 在 MQTT 通信场景中的应用前景

MQTT 是基于 TCP 的物联网通信协议，紧凑的报文结构能够在严重受限的硬件设备和低带宽、高延迟的网络上实现稳定传输；心跳机制、遗嘱消息、QoS 质量等级等诸多特性能够应对各种物联网场景。

尽管如此，由于底层 TCP 传输协议限制，某些复杂网络环境下 MQTT 协议存在固有的弊端：

- 网络切换导致经常性连接中断
- 断网后重新建立连接困难：断网后操作系统释放资源较慢，且应用层无法及时感知断开状态，重连时 Server/Client 开销较大
- 弱网环境下数据传输受限于拥塞、丢包侦测和重传机制

例如车联网用户通常会面对类似的问题：车辆可能会运行在山区、矿场、隧道等地方，当进入到信号死角或被动切换基站时会导致连接中断，频繁连接中断与较慢的连接恢复速度会导致用户体验变差。在一些对数据传输实时性和稳定性要求较高的业务，如 L4 级别的无人驾驶中，客户需要花费大量的成本来缓解这一问题。

在上述这类场景中，QUIC 低连接开销和多路径支持的特性就显示出了其优势。经过更深入的探索，我们认为 MQTT Over QUIC 可以非常好地解决这一困境 —— 基于 QUIC 0 RTT/1 RTT 重连/新建能力，能够在弱网与不固定的网络通路中有效提升用户体验。

## EMQX 5.0 的 MQTT over QUIC 实现

EMQX 目前的实现将传输层换成 QUIC Stream，由客户端发起连接和创建 Stream，EMQX 和客户端在一个双向 Stream 上实现交互。

考虑到复杂的网络环境，如果客户端因某种原因未能通过 QUIC 握手，建议客户端自动退回到传统 TCP 上，避免系统无法建立跟服务器的通信。

![MQTT over QUIC](https://assets.emqx.com/images/b93cb1ce646e93b7ce24440b1936ba06.png)

目前 EMQX 5.0 中已经实现了以下特性：

- **更高级的拥塞控制：**有效降低数据丢包率，在测试中在网络波动的情况下仍能持续稳定传输数据
- **运维友好：**减少大规模重连导致的开销（时间开销、客户端/服务器性能开销），减少不必要的应用层状态迁移而引发的系统过载（0 RTT）
- **更灵活的架构创新：**比如 Direct server return (DSR，服务器直接返回模式)，只有入口/请求流量经过 LB，出口和响应流量绕过 LB 直接回到客户端，减少 LB 的瓶颈
- **减少握手延迟 （1 RTT）**
- **多路径支持，连接平滑迁移：**从 4G 切换到 WIFI, 或者因为 NAT Rebinding 导致五元组发生变化，QUIC 依然可以在新的五元组上继续进行连接状态，尤其适用于网络经常性变化的移动设备
- **更敏捷的开发部署：**协议栈的实现在 userspace，能够开发快速迭代
- **端到端加密：**未加密的包头带有极少信息， 减少传输路径中中间节点的影响，带来更好的安全性和更可控的用户体验

同时还有以下更多能力有待进一步探索：

- **不同主题的流：**对于独立主题，每个主题可以有独立的 Streams 以消除其他主题长阻塞带来的影响，比如接收端长阻塞或流量控制，亦可以实现优先级主题功能。
- **不同 QoS 的流：**比如在「流量控制」中，QoS 0 传输应该让位给高 QoS 传输。
- **将控制消息分成不同的流：**MQTT 控制消息可以单向或双向发送。如客⼾端可以通过「控制流」异步发送 UNSUBSCRIBE 请求，以要求服务器端停⽌发送不再感兴趣的数据。
- **更细粒度的收发端协同流量控制：**面对每一个流进行流控且对整个连接进行流控，实现更细粒度的流量控制。

## QUIC vs TCP/TLS 测试对比

我们在实验室环境下，基于 EMQX 5.0 版本对不同的场景下 QUIC 与 TCP/TLS 的性能表现进行了模拟测试。

**测试环境**

- 测试平台：EMQX 5.0 单节点
- 服务器规格：AWS EC2 M4.2xlarge (8 核 32GB)
- 操作系统：Ubuntu 20.04
- 客户端数：5000
- loadgen 并行数：8
- latency 取值：P95

### 客户端连接时延

测试在不同网络时延下握手、建立连接、完成订阅的时延。相较于 TLS，在网络时延较高时 QUIC 有一定的优势。

![1ms 延迟](https://assets.emqx.com/images/587cb62a55c1c8e964772047697c1ee2.png)

<center>1ms 延迟</center>

![10ms 延迟](https://assets.emqx.com/images/0c715dad8849602f7a60a5aaeb073ac0.png)

<center>10ms 延迟</center>

![30ms 延迟](https://assets.emqx.com/images/40507a3f7e0f35b50a5817a4b27eb875.png)

<center>30ms 延迟</center>

### 0 RTT 重连时延

测试断开连接后，重新发起连接并恢复重连所需的时延。

由于 QUIC 在 0 RTT 场景下可以在第一个包上带上应用层的数据包， 应用层相较于 TCP 一个来回握手响应更快。

QUIC 协议支持 0 RTT 握手，当客户端和服务端完成**初次**握手后，服务端可向客户端发送 NST 包。 客户端在连接断开后可用 NST 跳过 1 RTT 中的很多步骤快速重建连接。 

0 RTT 的好处是可有效降低客户端和服务端握手开销和提高性能（握手延迟），EMQX 默认给客户端发送 NST 包， 有效时性为 2 小时。

0 RTT 也支持 early data，相比于 1 RTT 需要握手完成后才可进行应用层传输，0 RTT 的 early data 可以在第一个包上带上应用层数据，用于快速恢复或重启应用层业务。但由于 0 RTT 的 early data 不能防范重放攻击， 因此 QUIC 建议不要在 0 RTT 上携带会改变应用状态的数据。

> EMQX 默认不支持 early data，此测试只用于对比验证。

测试结果表明如果 MQTT 层协议设计得当，在完成首次握手后，QUIC 表现优于纯 TCP。

![MQTT over QUIC](https://assets.emqx.com/images/ee6b0475d2fff3f9902fef578cc76c56.png) 

![MQTT over QUIC](https://assets.emqx.com/images/263e2bfe8e8ba9133e756365365c9c91.png)

### 连接/重连时服务器资源使用

测试新连接与断线重新连接不同过程中服务器 CPU 和内存的占用情况，以对比 TLS，QUIC 1 RTT 和 0 RTT 握手时资源开销。测试结果表明 QUIC 的 CPU 和内存使用均优于 TLS，但是重建连接耗费带宽比 TLS 多。

| **测试项目**             | **QUIC**     | **TLS**   |
| ------------------------ | ------------ | --------- |
| CPU (首次连接)           | ~60%         | ~80%      |
| CPU(重连)                | ~65% ¹       | ~75%      |
| 内存最高使用             | 9 GB         | 12 GB     |
| 网络带宽使用(Trans+Recv) | 峰值 100Mb ² | 峰值 30Mb |

> 注 1：主要为 MQTT 清除会话，踢开旧连接的额外开销
>
> 注 2:：主要为传输路径 MTU 验证导致的大量 QUIC 初始化握手数据包

![MQTT over QUIC 测试](https://assets.emqx.com/images/eb0beee6063dbde95320368c193d946b.png)

### 客户端地址迁移

此测试模拟大规模客户端地址迁移时业务层消息传输的变化。

传统 TCP/TLS 客户端必须在应用层感知到断线才进行重连，此过程响应非常慢并伴有许多不必要的重传。 QUIC 的处理更加平顺，在传输层做到了保持连接不要求重连且让应用层无感（如果有需要应用层也可以订阅地址的变化）。

QUIC 在客户端源 IP 地址/端口变化情况下，消息发送无任何影响。而 TLS 连接在变化后出现消息发送中断现象，即使客户端可以通过重连机制重新连接到 EMQX 上，但中间时间窗口将无法进行任何操作。

这一结果表明 QUIC 非常适合用在网络经常需要切换的环境。

![MQTT over QUIC 测试](https://assets.emqx.com/images/26bca0a052ea8717e9d8f5343b80acd9.png)

### 网络丢包测试

测试在弱网条件下数据传输情况。我们分别做了 3 次测试：EMQX terminated TCP/TLS，QUIC 以及 nginx terminated TCP/TLS。

测试场景：EMQX 以 20K/s 的速率发布 QoS 1 消息，在此过程中注入网络错误：20% 乱序（发送端与接受端包的顺序不一致），10% 丢包，QUIC 测试中还额外增加每 30 秒一次的网络切换干扰。

在此情况下 QUIC 服务端接收的数据稍微有所抖动，但不丢失消息；而 TLS 出现因网络环境差而导致的拥塞、丢包。此项结果表明 QUIC 在弱网环境下可以提供可靠的传输。

![MQTT over QUIC 测试](https://assets.emqx.com/images/dae1f833b20fc71eeccc05dedcb9d5ae.png)

![MQTT over QUIC 测试](https://assets.emqx.com/images/6181a275b718164c16fc961da2488e0a.png)

> 黄圈标记中我们去除了网络错误，可以看到 TLS 的收发恢复正常收发，包数量一致没有堆积，而 QUIC 只是从轻微抖动变得更平滑。

## 更便捷的使用：MQTT over QUIC SDK

[NanoSDK](https://github.com/nanomq/NanoSDK/) 0.6.0 基于 MsQuic 项目率先实现了第一个 C 语言的 MQTT over QUIC SDK。

NanoSDK 通过为 NNG 的传输层增加 QUIC 支持，使 MQTT、nanomsg 等协议能够从 TCP 转为 UDP，从而提供更好的物联网连接体验。其内部将 QUIC Stream 和 MQTT 连接映射绑定，并内置实现了 0 RTT 快速握手重连功能。

> 消息示例代码请参考 [NanoSDK QUIC Demo](https://github.com/nanomq/NanoSDK/blob/main/demo/quic/client.c)。

我们近期也将基于 NanoSDK 进行封装并陆续推出 Python、Go 等语言的 SDK，方便更多用户尽快体验到 MQTT over QUIC 的优势能力。

同时，相关的 SDK 将支持 QUIC fallback，当 QUIC 不可用时，连接层将自动切换为 TCP/TLS 1.2，确保各类网络环境下业务都能正常运行。

![NanoSDK 与 EMQX 之间通过 QUIC 进行消息收发](https://assets.emqx.com/images/113ee2b80e15463b1d45ba952c5f3e83.png)

<center>NanoSDK 与 EMQX 之间通过 QUIC 进行消息收发</center>

 
## 未来的 EMQX QUIC

![未来的 EMQX QUIC](https://assets.emqx.com/images/f01ff156928f2969f197ae0a19f3e93a.png)

结合 QUIC 特性和物联网场景，我们为 MQTT over QUIC 规划了诸多特性，如通过区分控制通道实现主题优先级设置，实现非可靠实时流传输以应对高频数据传输场景，以及灵活的主题和数据通道（Stream）映射以降低主题之间的干扰。未来的版本中将陆续呈现。

EMQ 也正在积极推进 MQTT over QUIC 的标准化落地。继 2018 年成为 OASIS MQTT 技术委员会中目前为止唯一拥有投票权的中国公司并参与 5.0 协议标准制定后，EMQ 目前也已提交了 MQTT over QUIC 的相关草案。相信在不久的将来，MQTT 的底层协议将同时支持 TCP 与 QUIC，使整个物联网行业从中获益。 

## 结语

可以看到，QUIC 非常适用于传统 TCP/IP 网络 UDP MTU 大小能够保证的弱网环境或者网络经常切换的环境。对于设备时刻处在移动中的物联网场景（如车联网、移动采集等），或是需要频繁断连不适合做长连接的场景（如设备需要定期休眠）来说，QUIC 都拥有巨大的潜力，是更为适合的底层协议选择，这也是 EMQX 5.0 引入 QUIC 支持的原因。

MQTT over QUIC 在 EMQX 5.0 中的率先实现，让 EMQ 再次走在全球物联网消息服务器领域的前沿。EMQ 将始终坚持以不断的技术革新驱动产品持续的迭代升级，期待通过领先的产品为物联网领域带来基础设施保障和业务创新动力。

<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>


## 本系列中的其它文章

- [EMQX 5.0 产品解读 01 | Mria + RLOG 新架构下的 EMQX 5.0 如何实现 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)
- [EMQX 5.0 产品解读 03 | 基于 RocksDB 实现高可靠、低时延的 MQTT 数据持久化](https://www.emqx.com/zh/blog/mqtt-persistence-based-on-rocksdb)
- [EMQX 5.0 产品解读 04 | 全新物联网数据集成 ：Flow 可视化编排 & 双向数据桥接](https://www.emqx.com/zh/blog/iot-data-integration)
- [EMQX 5.0 产品解读 05 | 灵活多样认证授权，零开发投入保障 IoT 安全](https://www.emqx.com/zh/blog/securing-the-iot)
