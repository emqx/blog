随着智能化浪潮席卷全球，如今的车辆早已不再是单纯的交通工具，而是一个具备自主推理能力、能和云端交互进行车路协同的移动智能节点。

很多的新型应用场景不但计算量巨大，而且对通信链路有非常强的低时延、低能耗和高可靠要求。传统的通信协议如 HTTP 等并不能同时满足以上要求。而作为目前物联网领域事实上的标准协议，MQTT 提供了 Pub/Sub 的消息模式，具备精简优良的协议设计，可以满足低延时和低功耗的需求，适用于资源有限的车机系统。但不同于智能家居、机器人这类设备固定且网络环境稳定的场景，车联网中快速移动、场景切换快、网络情况复杂多变等特性，对 MQTT 协议在车端和服务端的应用提出了更高的要求。

本文将深入分析车联网移动场景下 MQTT 消息传输面临的问题及产生原因，并利用 MQTT 协议特性对其加以解决和优化，帮助用户构建更稳定的车联网通信架构。

## 当你高速驾驶时，当你穿越隧道时，网络实际发生了什么？

相信大家使用 4G 手机时都有过类似体验：进入地下室时信号强度突然变弱，虽然网络没有显示中断，但是实际使用体验就和断网一样；亦或是在一个很大区域的 WiFi 网络范围内移动，在不同的 AP（无线接入点）覆盖范围之间切换时也会有类似情况。这就是一个典型的移动设备导致的网络迁移问题。而在车联网中，由于车辆是高速移动，特别是在高速公路基站覆盖稀疏或穿过隧道的情况，都会导致这种问题更加频繁地出现，从而引起车机端 MQTT 连接中断重连。

首先我们来看看车联网场景面对的网络现状：根据 2020 年底的数据，我国基站总数为 931 万个，其中 3G/4G 基站总数为 575 万个。但这些基站大多集中在城市区域，而在乡村，高速公路甚至是隧道内的信号覆盖就远没有城市那么全面。目前，针对高速公路和国道省道等区域的网络覆盖方案基本分为公网延伸覆盖和专网覆盖方案。

- 公网延伸覆盖：将路线区域与周边区域统一规划，使用常规基站蜂窝组网方式进行覆盖。由于往往是直接将大网的网络资源延伸到高速公路上，所以也叫大网延伸覆盖。

  ![公网基站覆盖示意图](https://assets.emqx.com/images/df86a9e6a00dd1e1ee79c4ce83ea938d.png)

  <center>公网基站覆盖示意图</center>

- 专网覆盖：针对特殊的点覆盖和线覆盖场景的特殊要求进行优化，配置特殊的频率、信令和功能进行异频组网。由于建设成本高，往往更多用于高速铁路沿线覆盖。专网与公网之间完全隔离，只有在特定出入口例如高速公路收费站才能进入或离开专网。

  ![专网延伸覆盖示意图](https://assets.emqx.com/images/67a2211b9488a73408a245d73b7b0598.png)

  <center>专网延伸覆盖示意图</center>

可以发现，我们使用的网络是依靠通信从业者建设的一个个蜂窝基站提供的。而车辆在快速移动的过程中，位置更新频繁，经常会在多个基站覆盖范围之间切换。这导致其网络信令负荷大，基站切换频繁，最终将导致车载 4G 模块的网络链路中断。虽然专网覆盖可以通过采用 BBU+RRU 小区合并的技术来减少网际切换和同频干扰，进而解决这一问题，但由于专网方案建设成本高昂，所以实际场景里，车联网更多面对的还是第一种公网覆盖方案。

![从运营商提供的管理系统里查看 4G 连接的情况](https://assets.emqx.com/images/7abd9cc35b0adadc674c3722f935c3e3.png)

<center>从运营商提供的管理系统里查看 4G 连接的情况</center>

于是，我们就会发现车机端的 4G 连接出现如上图所示的不断上下线的情况。

**多普勒效应和隧道覆盖**

除了基站覆盖带来的网络问题外，当车辆行驶速度很快的时候，也会由于多普勒效应造成延迟增加和丢包。车速越大，频偏越大，延迟越大，丢包的概率也越大。

![多普勒效应示意图](https://assets.emqx.com/images/ef4a99c52796d76328a36ee920d6cea1.png)

<center>多普勒效应示意图</center>


## MQTT 连接发生了什么？

我们知道了车辆的网络情况，那么这些因素是如何影响车机端 MQTT 连接的呢？

众所周知，MQTT 连接也是基于 TCP/IP 协议栈。看到这里大家可能会有疑问：TCP/IP 协议栈里有连接保活机制，MQTT 协议里也有 Keep Alive 参数供连接重建恢复，哪怕基站切换导致了短暂的通信中断，但是等到进入下一个基站的范围，通信链路也很快就恢复了，那么为什么还会导致车辆设备 MQTT 连接的频繁离线呢？要回答这个疑问，我们需要结合 TCP/IP 和移动网络入网过程一起来分析。

![TCP/IP 协议握手过程](https://assets.emqx.com/images/14c5d70e17b3ef262d78f695c33e57e1.png)

<center>TCP/IP 协议握手过程</center>

TCP/IP 协议诞生之初，主要针对的是稳定的有线网络，作为一个可靠传输协议，其内部有数据 ACK，能够进行数据重传和连接复用。但是，这一切都是基于 IP 地址不变的前提下，而在车联网场景里，基站切换是会导致车机端的 IP 地址变更的。每次车机 4G 模块进入新的基站覆盖范围时都会重新发起一次入网附着请求。

![网络入网过程-UE 初始化附着到 UE-UTRAN 网络的过程](https://assets.emqx.com/images/285419b1e925a9d805488abdb509eaec.png)

<center>网络入网过程-UE 初始化附着到 UE-UTRAN 网络的过程</center>

其中的协议细节这里不进行详细解释。由于目前我们仍然在使用 IPV4 标准，所以车机 4G 模块在重新入网过程中会向新搜寻到的 eNB 基站发送一个关键的信令 PDN（Packet Domain Network）来请求为自己分配一个新的 IP 地址，而这个地址往往都是 NAT 地址，这也是 4G 终端开机即在线的技术的一环。此时还伴随着网络质量检测、APN 匹配等流程来判断终端使用的网络类型和推送网络路由以保证连通性。如果此时的边缘 eNB 基站没有针对车机端的 4G 卡和 PDN 信令进行对应优化，是无法获知其原先使用的 IP 地址的，那么这时候 IP 地址就发生了改变，需要进行 NAT 地址重绑定。而对于 MQTT 和 TCP/IP 这一类长链接协议来说，IP 地址变化后，TCP 服务端无法识别出现在的客户端是否还是原先的客户端，所以 TCP 连接是必须要重新建立的，从而导致 MQTT 连接也必须重建。

![TCP 连接和 MQTT 连接的关系](https://assets.emqx.com/images/69e5ea864e284124c6d421504df48881.png)

<center>TCP 连接和 MQTT 连接的关系</center>

以上是一个正常的快速移动的车辆在蜂窝基站间正常切换会发生的过程。而实际情况中网络更加复杂，公网覆盖方案由于共享基站和接入网资源，若边缘基站负载过高还会发生 eNB 基站对 PDN 请求不响应等情况。网络侧对承载请求不响应，更不用说伪基站。此外地理环境和多普勒效应引起的多径效应和信号衰减都会导致延时增加和连接中断。


## 如何改善移动网络下 MQTT 连接稳定性？

清楚了问题的根源，接下来我们将借助 MQTT 协议的特性来解决上述问题，构建更稳定的车联网通信架构，避免因为连接重连和中断造成的数据丢失。

虽然 TCP/IP 部分无法改变，但 MQTT 协议提供了许多供配置的参数和消息 QoS 等级供我们配置。针对一些关键数据，比如车机端重要的状态变化和用户发出的请求，我们需要保证消息到达，这就需要我们使用QoS 1/2。

### Clean Session

首先，我们要解决 IP 更新导致 TCP 重连后客户端无法识别的问题。我们可以通过 MQTT 会话保持特性来解决。

> 关于 MQTT 会话状态可参考文章：[https://www.emqx.com/zh/blog/mqtt-session](https://www.emqx.com/zh/blog/mqtt-session)。

MQTT 要求客户端与服务端在会话有效期内存储一系列与客户端标识（ClientID）相关联的状态，即会话状态。我们将从客户端向服务端发起 MQTT 连接请求开始，到连接中断直到会话过期为止的消息收发序列称为会话。因此，会话可能仅持续一个网络连接，也可能跨越多个网络连接存在。所以在这种网络切换的过程中，车机端每次连接使用相同的客户端标识，就可以让 MQTT Broker 在 TCP 连接重建的情况下，仍然可以识别到新连接是之前的客户端，从而将缓存的 QoS 消息重发，并应用之前的连接状态。

客户端使用会话保持的方式以 Java 为例：

```
public MQTTPublisher(String address, String clientId, boolean cleanSession, int qos) throws MqttException {
  this.clientId = clientId;
  this.qos = qos;
  this.client = new MqttClient(address, clientId, persistence);
  MqttConnectOptions connOpts = new MqttConnectOptions();
  connOpts.setCleanSession(cleanSession);  //置为 fasle 即为保留会话
  this.client.connect();
}
```

### MQTT 5.0

基于这种网络连接频繁断开重连的情况，为了避免应用层频繁收到上下线事件，影响业务进行。MQTT 5.0 也对协议进行了响应的优化：

Will Delay Interval（延时遗愿消息发布）：我们经常使用遗愿消息对客户端的下线进行追踪和告知。在这种情况下会频繁的收到遗愿消息。所以遗嘱时间间隔的一个重要用途就是避免在频繁的网络连接临时断开时发布遗嘱消息，因为客户端往往会很快重新连上网络并继续之前的会话。

Session Expiry Interval（会话过期间隔）：MQTT 3.1.1 未对会话保持时间做明确规定。如果使用 sesseion 保持功能的客户端大量频繁上下线会造成 Broker 内存使用增加，最终影响服务高可用。所以 MQTT 5.0 也针对这种情况设计了会话过期时间。客户端可以在连接时使用这一特性设置自己的会话保持时间。

### QoS 1/2

设置完会话保留状态，我们就可以使用 QoS 消息来保证消息的到达。

> 关于 QoS 的详解可参考文章：[https://www.emqx.com/zh/blog/introduction-to-mqtt-qos](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

我们建议对于重要数据在车机端使用 QoS 1 进行发送，并且使用带有 QoS 重传功能和内置 QoS 消息窗口（队列）的 MQTT SDK。例如 [NanoSDK](https://github.com/emqx/NanoSDK)，其具有异步确认、内置 QoS 消息队列、自动重发、高吞吐高消费能力等特点。

### Broker QoS MsgQueue

QoS 消息在 Broker 端有内存持久化功能，除了客户端有内置的消息队列，Broker 也有一个 QoS 消息队列。如上文所述，车联网场景经常发生的基站切换导致连接重置，反映到 MQTT 连接就体现为 QoS 消息积压现象。客户端和服务端都会有未确认的消息积压在队列里。所以我们要根据实际情况设置消息队列的长度。

以 EMQX 为例，消息队列设置：

打开 emqx.conf

```
mqtt {
  ## @doc Maximum QoS 2 packets (Client -> Broker) awaiting PUBREL.
  max_awaiting_rel  =  100

  ## @doc The QoS 2 messages (Client -> Broker) will be dropped if awaiting PUBREL timeout.
  await_rel_timeout  =  300s

  ## @doc Maximum queue length. Enqueued messages when persistent client disconnected, or inflight window is full.
  max_mqueue_len  =  1000
}
```

`max_awaiting_rel` 为接受 QoS 2 的消息队列长度。QoS 1 此项无限制。

`await_rel_timeout` 为 QoS 2 消息超时时间。

`max_mqueue_len` 为下发 QoS 1/2 的队列缓存长度

默认的 QoS 2 消息队列长度仅为 100，此处建议根据给客户端发布消息的频率和消费能力适当增加，一般考虑为 publisher 平均每秒产生消息的数量 *2 。此队列提供消费端一定的缓冲时间来完成重连后积压消息的消费。

![MQTT QoS](https://assets.emqx.com/images/5b3b855131e894f56392c146f473788e.png)

## 更优的解决方案：MQTT over QUIC

由于 TCP 采用四元组来判断识别连接的独特性，而 UDP 并没有同样的要求。2022 年 6 月 11 日，IETF 正式颁布了 HTTP/3 RFC 技术标准文档后，基于 UDP 的 QUIC 正式成为了传输层标准之一。而基于 QUIC 的 MQTT 方案也有望成为下一个行业标准。

借助 QUIC 协议的地址迁移、流式多路复用、分路流控、更低的连接建立延迟，我们有望彻底解决车联网移动场景下的连接问题。

![MQTT over QUIC](https://assets.emqx.com/images/55c7f306a21218e2c2476db76c3c7c3b.png)

![0-RTT 示意图](https://assets.emqx.com/images/95da8ddff80f7a9137031046dbaaefe1.png)

<center>0-RTT 示意图</center>

QUIC 能够侦测到地址改变，自动采用 0-RTT 的方式重建连接，从而使得客户端和服务端对于 IP 地址的变动无感知，这样就彻底避免了上文所说的一系列问题。

## 结语

本文分析了车联网移动场景中 MQTT 通信不稳定现象的成因，并通过客户端和服务端对会话保持、QoS、客户端 ID 的配置和内置消息队列缓存等 MQTT 协议特性，在一定程度上解决了高速移动带来的连接不稳定导致的数据丢失问题。

此外，如前文提到，相比之下 MQTT over QUIC 可能是一种更优的解决方案。目前最新发布的 [EMQX 5.0 已支持 MQTT over QUIC ](https://www.emqx.com/zh/blog/mqtt-over-quic)并设计了独特的消息传输机制和管理方式，实现了有效降低数据丢包率，减少握手延迟。车联网用户可以使用 EMQX 5.0 获得更加高效、低延迟的物联网数据传输体验。随着 EMQ 在 MQTT over QUIC 标准化进程的积极推进，相信未来车联网及其他更多物联网行业的弱网与不固定网络通路场景下的消息传输问题都将得到进一步改善。



>**EMQ 车联网行业白皮书现已正式上线！**
>
>汇聚 EMQ 多年服务车联网领域客户的实践经验，从协议选择等理论知识到平台架构设计等实战操作，为车联网从业者搭建可靠、高效、符合行业场景需求的车联网平台提供可操作、可落地的参考指南。
>
>[立即免费下载 ->](https://www.emqx.com/zh/resources/iov-platform-building-from-beginner-to-master)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
