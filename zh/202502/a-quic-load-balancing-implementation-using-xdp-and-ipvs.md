## 引言

互联网的快速发展，需要更高效、更可靠的网络连接。与传统 TCP/IP 相比，QUIC 协议在网络流量方面具有革命性优势。QUIC 具备拥塞控制、降低延迟、提高安全性等核心功能，已成为现代移动应用程序的不二之选。

随着 QUIC 的广泛应用，网络流量快速增长，如何高效管理高并发流量成为关键问题。传统的负载均衡方案主要针对 TCP/IP 设计，难以适配 QUIC 的多项特性，容易出现性能瓶颈，限制 QUIC 的发展潜力。

本文将深入探讨 QUIC 负载均衡的技术，并介绍一种有效的解决方案：通过 XDP（eXpress 数据路径）和 IPVS（IP 虚拟服务器）实现高效的流量分配。我们将详细分析 QUIC 负载均衡的技术难点，阐述 XDP 与 IPVS 的协同工作机制，并探讨这种方案带来的显著优势。此外，我们还将讨论直接路由的概念及其在该框架中的潜在应用价值。

通过阅读本文，您将全面了解如何借助 XDP、IPVS 以及直接路由技术，通过高效的负载均衡方案充分释放QUIC 的全部潜力。现在，让我们共同探索 QUIC 流量管理的未来发展方向。

## QUIC 负载均衡的挑战

传统的负载均衡器在处理基于 UDP 的 QUIC 时经常面临一些障碍：

- **连接 ID 难题：** 

  QUIC 使用连接迁移，客户端和服务器都可以动态更改其连接 ID。这会破坏负载均衡器持续跟踪和管理连接的能力，可能导致连接中断或流量分布不均。

- **NAT 干扰：**

  网络地址转换 (NAT) 会使 QUIC 负载均衡更加复杂。当 NAT 设备后面的客户端建立 QUIC 连接时，源 IP 地址可能会在连接迁移期间发生变化。这会让负载均衡器感到困惑，因为它依赖一致的源 IP 来识别客户端并正确地路由流量。

- **可见性有限：**

  传统负载均衡器通常依靠「四元组」进行流量管理（源 IP、源端口、目标 IP 和目标端口）。由于 QUIC 在 UDP 上运行，因此许多负载均衡器将其视为基本 UDP 流量。这限制了它们对单个 QUIC 连接内多路复用流的可见性。因此，仅靠「四元组」可能不足以基于单个数据流实现最佳流量分配。

## 什么是 QUIC 连接 ID 及其重要性？

与依赖四元组进行识别的传统 TCP 连接不同，QUIC 使用连接 ID (CID) 作为唯一标识符，此 CID 是嵌入在 QUIC 数据包标头中的随机生成的值。与传统的四元组方法相比，CID 有以下几个优点：

- **持久性：保障连接稳定性**

  CID 的一个核心优势是其持久性。与四元组中的源 IP 地址不同，根据QUIC协议，即使 CID 在连接的生命周期中可能被多次动态更新，客户端和服务端仍然对当前使用中的 CID 具有共识。此共识在 QUIC 连接整个生命周期内保持不变。这种特性非常适合移动设备或网络环境不稳定的场景。

- **增强安全性：抵御攻击**

  CID 的随机生成特性使攻击者难以预测或伪造特定 QUIC 连接的数据包。这种设计有效防止了连接劫持和伪造攻击，从而增强了通信的整体安全性。

## 经典问题：NAT 墙和 QUIC 连接中断

由于许多用户通过网络地址转换 (NAT) 网关连接到互联网，此时客户端使用 NAT 分配的公共地址进行通信，其真实 IP 地址具有隐藏性。这种情况对使用仅依赖四元组（源 IP、源端口、目标 IP 和目标端口）的传统方法进行 QUIC 负载平衡提出了挑战。

### **问题分析**

**1、初始握手**

- 位于 NAT 后的客户端与服务器建立 QUIC 连接。
- 由于负载均衡器不具备 QUIC 层解析能力，使用四元组将流量路由到真实服务器（称之为 Server1）。

**2、稳定连接**

四元组保持不变（包括客户端的源端口）且 NAT 绑定未发生变化，来自客户端的后续流量将继续被定向到 Server1。

![Initial Handshake](https://assets.emqx.com/images/9423dc774c20fc9146076178b2354b0f.png)

**3、NAT 绑定中断**

- **非活动流量超时**：

  如果连接在一段时间内没有活动，NAT 可能会重新分配客户端的源端口，导致四元组发生变化。

- **客户端网络变更**：

  如果客户端切换到其他网络（例如从 Wi-Fi 切换到移动网络），它将被分配一个新的公共 IP 地址，从而改变四元组。

![Address Migration LB has no QUlC awareness](https://assets.emqx.com/images/3a3e0b3d6cbb78a47b1bbdbd08de3676.png)


**4、负载均衡器错误定向**

传统的负载均衡器缺乏对 QUIC 协议的支持，可能会将变化后的四元组视为新连接，并将流量错误地路由到其他服务器（例如 Server2）。

**5、连接中断阶段**

尽管 QUIC 支持地址迁移功能，但在这种情况下，由于客户端的源 IP 和最初连接的服务器（Server1）都已发生变化，QUIC 无法保持连接。

### **负面影响**

**1、对客户端的影响**：
客户端可能会遇到连接中断，导致正在进行的通信或数据传输失败，影响用户体验。

**2、对服务器的影响**：
Server1 丢失已建立的连接及其关联的应用程序状态，可能导致数据丢失或服务中断，增加运维复杂性。

## 解决方案：XDP QUIC 转向和 IPVS 直接路由

EMQ 致力于在物联网场景中推动 QUIC 技术的创新。为了解决传统负载均衡在 NAT 环境下的局限性，我们引入了基于 XDP QUIC 转向 和 IPVS 直接路由 的 QUIC 负载均衡解决方案。以下将详细介绍该方案的技术实现。

### **部署概述**

**1、真实服务器（RS）配置**

每个真实服务器 RS 在其本地网络接口（链路本地设备）上配置一个唯一的 VIP（虚拟 IP）地址，该地址作为客户端 QUIC 连接的目标地址。

**2、IPVS 直接路由（DR）模式**

- 标准 IPVS 实例采用直接路由（DR）模式运行。
- IPVS 作为流量导向器，根据预定义规则（如轮询、最少连接）将发往 VIP 地址的传入 QUIC 数据包分发到真实服务器池中。
- IPVS 转发到真实服务器的数据包将保留 VIP 地址作为目标地址。

**3、XDP QUIC 转向模块**

在每个真实服务器的公共网络接口中注入一个定制的 XDP QUIC 转向模块。该模块运行在网络层，提供高性能的数据包处理能力。

### **XDP QUIC 转向的功能**

XDP QUIC 转向模块的核心任务是拦截并处理以真实服务器上配置的 VIP 地址为目标的传入 UDP 数据包。具体步骤如下：

**1、数据包检查**

模块首先检查 UDP 数据包头的内容。

**2、连接 ID 提取**

从 QUIC 数据包头中提取连接 ID（CID）。该 CID 包含标识目标真实服务器的信息。

**3、数据包路由**

- 如果提取的 CID 与本地真实服务器不匹配，XDP 模块将利用其直接操纵数据包的能力，将数据包路由到由 CID 标识的指定真实服务器。
- 该模块不会修改数据包头中的目标地址（仍为 VIP 地址），以确保 IPVS 能够维护其路由表并有效执行健康检查。

### 详细流程

流程 1：握手过程中形成请求和返回路径。

![Initial Handshake](https://assets.emqx.com/images/9423dc774c20fc9146076178b2354b0f.png)

| **步骤** | **行动**                          | **源地址**     | **目标地址**   | **解释**                                                     |
| :------- | :-------------------------------- | :------------- | :------------- | :----------------------------------------------------------- |
| 1        | Client Send QUIC Initial (CRYPTO) | Client Private | VIP            |                                                              |
| 2        | NAT translation                   | NAT GW Public  | VIP            |                                                              |
| 3        | LB select RS                      | NAT GW Public  | VIP            | LB Hashing SRC addr                                          |
| 4        | Server reply QUIC Handshake       | VIP            | NAT GW Public  | Server AssignSCID (Source Connection ID) which contains server id for XDP steering.Server DR (direct route) to the Client. |
| 5        | NAT translation                   | VIP            | Client Private | The request path and return path are now formed.NAT GW remember this Mapping. |
| 6        | Client Send QUIC Handshake (ACK)  | Client Private | VIP            | Reuse 1.                                                     |
| 7        | NAT translation                   | NAT GW Public  | VIP            | Reuse 2. NAT GW find routing in mapping                      |
| 8        | LB forward to RS1                 | NAT GW Public  | VIP            | reuse 3.                                                     |
| 9        | Network path is formed            |                |                | Client and Server will continue communicate with the path: 1 → 2 → 3 → 4 → 5 |

流程 2：地址迁移后的 QUIC 转向。

![QUIC Steering](https://assets.emqx.com/images/94f0fe6eab2124528940e2fb366e4568.png)

前提条件：客户端移动到另一个网络或者发生 NAT 重新绑定，这意味着客户端的公共地址已更改！

| **步骤** | **行动**                   | **源地址**      | **目标地址**    | **解释**                                                     |
| :------- | :------------------------- | :-------------- | :-------------- | :----------------------------------------------------------- |
| 1        | Client send QUIC packet    | Client Private  | VIP             | Client detect network change thus start to probe the new path.ORClient just send regular QUIC packet.Both scenarios will work.The packet contains DCID (Destination Connection ID)which is the SCID in step 4) in above handshake flow. |
| 2        | NAT translation            | NAT GW Public 2 | VIP             | To public, client has a new public address                   |
| 3        | LB select RS 2             | NAT GW Public 2 | VIP             | LB Hashing SRC addr and it select RS 2                       |
| 4        | XDP QUIC steering          | NAT GW Public2  | VIP             | This is where the XDP QUIC steering module kicks in.It finds the DCID is targeting another host (RS 1), thus it reroute the packet to RS1 while keep the SRC and DST Addr unchanged. |
| 5        | RS 1 start probe new path  | VIP             | NAT GW Public 2 | The XDP QUIC steering module on RS 1 detects the UDP packet is for RS1  thus no action on it.QUIC stack on RS 1 detects the client address is changed from “NAT GW Public” to “NAT GW Public2”, thus start to probe new path. |
| 6        | NAT translation            | Client Private  | VIP             | NAT Gateway has the mapping thus does the translation and forward to Client Private |
| 7        | New network path is formed |                 |                 | Client and Server will continue communicate with the path: 1 → 2 → 3 → 4 → 5 → 6 |

## XDP QUIC 转向与 IPVS 直接路由的优势

这种方法与传统 QUIC 流量负载均衡方法相比具有以下优势：

- **适应客户端地址迁移：**与仅依靠客户端源地址的传统 UDP 负载均衡器不同，该解决方案利用 QUIC 连接 ID。即使客户端的 IP 地址因 NAT（网络地址转换）而发生改变，连接 ID 仍可提供目标 RS ID。实际服务器上的 XDP QUIC 转向模块仍可识别并路由属于已建立连接的数据包，确保不间断的应用数据交换，无需重新连接。
- **XDP 的高性能：**通过在 XDP 层处理数据包，这种方法可以受益于 XDP 的效率。XDP 在网络层运行，在传统的操作系统协议介入之前。这最大限度地减少了处理开销，并确保 QUIC 通信的低延迟，这是实时应用的关键因素。
- **IPVS 透明度：**XDP QUIC 转向模块巧妙地修改数据包的内部路由路径，使其根据连接 ID 定向到相应的真实服务器。重要的是，它不会更改 IPVS 可见的目标地址。这可以保持 IPVS 路由表和运行状况检查的完整性，确保其能够继续按预期进行负载均衡。
- **广泛的负载均衡器兼容性：**此方法旨在与大多数支持 DR（直接路由）模式的负载均衡器无缝协作。DR 模式允许负载均衡器根据预先定义的规则将流量直接路由到指定的真实服务器，非常适合 XDP QUIC 转向的特定连接路由。
- **易于扩展：**该解决方案具有高度可扩展性。通过在每个真实服务器上部署 XDP QUIC 转向模块，从池中添加或删除服务器就变得非常简单。这样就可以动态扩展 QUIC 基础设施，以满足波动的流量需求。

总而言之，这种方法结合了 IPVS 在初始流量分配方面的优势和 XDP QUIC 转向在基于连接的路由方面的效率。这使其成为高效可靠的 QUIC 负载均衡的绝佳解决方案。

## **为什么这种方法不适用于 TCP 协议？**

虽然 XDP QUIC 转向与 IPVS 直接路由为 QUIC 负载平衡提供了令人信服的解决方案，但问题随之而来：类似的方法是否能够用于保持 TCP 连接的活跃状态？

答案是否定的。原因如下：

- **TCP 依赖于四元组：**与 QUIC 的连接 ID 不同，TCP 连接依赖于四元组（源IP、源端口、目标 IP 和目标端口）进行识别和路由。XDP QUIC 转向无法有效跟踪和管理 TCP 连接，因为数据包头中缺少关键的连接 ID 元素。
- **TCP 状态管理：**TCP 连接在两端（客户端和服务器）建立和维护状态信息（序列号、确认窗口），以确保可靠的数据传输和有序的数据包接收。XDP QUIC 转向在较低的网络层运行，缺乏管理或操作这种关键的 TCP 连接状态信息的能力。
- **TCP 重新建立（虽然并不理想）：**即使客户端的源 IP 在 TCP 连接期间因 NAT 而发生改变，客户端和服务器都可以尝试通过协商新的四元组来重新建立连接。这种重新建立过程虽然并不理想，但可以恢复 TCP 连接的数据交换。XDP QUIC 转向无法促进 TCP 连接的重新建立。

本质上，XDP QUIC 转向是专门为利用 QUIC 的独特功能而量身定制的，特别是即使在客户端地址发生变化时仍可管理的连接 ID。TCP 连接依赖于不同的识别、状态管理和潜在重建机制，这使得这种方法不适合维持其活动状态。

**关键的一点是，地址迁移是 QUIC 协议提供的独特功能。**该功能与 QUIC 连接 ID 相结合，可通过 XDP QUIC 转向实现高效且灵活的负载均衡。虽然这种方法为 QUIC 提供了显著的优势，但 TCP 协议的局限性使得这种负载均衡方案无法被用于保活客户端连接（当源地址发生变化时）。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
