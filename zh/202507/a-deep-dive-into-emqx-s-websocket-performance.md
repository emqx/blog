## 引言

在实时 Web 应用领域，从实时金融仪表盘和协作白板，到交互式游戏和大规模物联网设备群管理，底层通信协议是影响体验的关键。MQTT 是物联网的事实标准，[MQTT over WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket) 已成为连接后端服务和浏览器客户端的首选解决方案，提供了强大、双向的通信能力，同时也能轻松适配企业网络环境，实现稳定连接。

随着应用程序规模的扩大，一个关键问题开始浮现：一个 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 服务能承载多少 WebSocket 并发连接？在 EMQX，我们不断突破技术极限。在成功完成[ 1 亿次 MQTT/TCP 连接测试](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)后，我们将目光转向了 WebSocket 协议。

**本文中，我们基于 EMQX 5.10 进行了一次性能测试，证明 EMQX 集群可以轻松应对 200 万 MQTT over WebSocket 的并发连接以及 100K TPS 的消息速率，并展现了卓越的低延迟特性。**

接下来，我们将带您深入探索 200 万连接背后的技术征程，详细解读测试环境设置、各阶段结果以及实现这一卓越性能的 EMQX 架构原理。

## 挑战：从 50 万到 200 万连接

我们的目标是模拟现实世界的大规模应用场景：海量 WebSocket 客户端各自订阅独立主题，并持续接收消息流。为此，我们设计了渐进式的基准测试，通过逐阶段倍增连接负载，精准观测 EMQX 的扩展能力。

**测试场景：**

- **连接：**每个客户端建立一个持久的 WebSocket 连接。
- **订阅：**每个客户端订阅一个唯一的主题（`t/%i`，%i 表示客户端 ID 的占位符），QoS 为 1。
- **发布：**同等数量的发布者客户端向这些唯一主题发送消息。
- **消息流：**一对一通信，每个连接大约每 10 秒发送 1 条消息。
- **消息大小：** 256 字节。

所有测试均使用我们[基于 Terraform 的开源性能测试框架](https://github.com/emqx/tf-emqx-performance-test)和强大的 [emqtt-bench](https://github.com/emqx/emqtt-bench) 负载生成工具进行。

## 第一阶段：建立 50 万连接为基础

千里之行，始于足下。首先，我们需要做一个 50 万并发连接的基准测试。

**EMQX 集群设置：**

- **节点：** 2 个 EMQX Core 节点
- **实例类型：** AWS `c7g.4xlarge`（16 vCPU，32 GiB RAM）

**结果：**

| **指标**                    | **数值**            |
| :-------------------------- | :------------------ |
| 网络 RX/TX（每个节点）      | 约 50 / 54 Mb/s     |
| 消息速率（输入/输出）       | 约 25,000 条消息/秒 |
| 并发活跃连接                | 50 万               |
| 平均 RAM 使用量（每个节点） | 约 60%              |
| 平均 CPU 使用率（每个节点） | 约 51%              |

可以看到，该集群轻松承载了 50 万个并发连接，CPU 与内存占用率始终维持在健康阈值内，且仍保留充足性能空间。第一阶段的成功证明了测试环境的可靠性，为后续更高强度的挑战奠定了坚实基础。

![image.png](https://assets.emqx.com/images/9590274e4f044cab5136b401199cf312.png)

<center>EMQX 仪表板显示 500k WebSocket 连接</center>

## 第二阶段：突破 100 万连接大关

在确定基准性能后，我们将连接规模倍增至 100 万，并验证 EMQX 是否具备线性扩展能力。为了应对激增的负载压力，我们对集群节点进行了纵向扩容。

**EMQX 集群设置：**

- **节点：** 2 个 EMQX Core 节点
- **实例类型：** AWS `c7g.8xlarge`（32 vCPU，64 GiB RAM）

**结果：**

| **指标**                    | **数值**            |
| :-------------------------- | :------------------ |
| 并发活跃连接                | 1,000,000           |
| 消息速率（输入/输出）       | 约 50,000 条消息/秒 |
| 平均 CPU 使用率（每个节点） | 约 46%              |
| 平均 RAM 使用量（每个节点） | 约 55%              |
| 网络 RX/TX（每个节点）      | 约 115 / 119 Mb/s   |

![image.png](https://assets.emqx.com/images/d480a5cc6391bb91daaec63c691fb6dc.png)

<center>EMQX 仪表板显示 1M WebSocket 连接</center>

## 第三阶段：实现 200 万连接

在仅使用两个节点的情况下实现 100 万连接测试看起来还不错。但为了突破 200 万连接，我们采用了标准 EMQX 架构进行大规模部署：将 Core 节点和 Replicant 节点分离。

**为什么要使用 Core 节点和 Replicant 节点：这种架构是 EMQX 可扩展性的基石。**

- **Core 节点：**负责集群管理、路由信息和数据持久化。它们是集群的「大脑」。
- **Replicant 节点：**采用无状态设计，负责处理繁重的客户端连接和消息流量。它们可以无缝地在集群中添加或移除，从而实现容量的水平扩展。

通过这种分离部署架构，可以有效分离集群管理的算力与 MQTT 连接**、**消息的处理算力，这在超大规模场景中至关重要。

**EMQX 集群设置：**

- **Core 节点：** 2 x `c7g.2xlarge`（8 vCPU，16 GiB RAM）
- **Replicant 节点：** 4 x `c7g.8xlarge`（32 vCPU，64 GiB RAM）

**结果：**

| **指标**              | **数值**             |
| :-------------------- | :------------------- |
| 并发活跃连接          | 2,000,000            |
| 消息速率（输入/输出） | 约 100,000 条消息/秒 |

资源使用情况清晰展现了架构优势：

- **Core 节点：**CPU 占用率极低（约 1%），因为它们专用于集群管理任务，而不是连接处理。
- **Replicant 节点：**平均 CPU 使用率在 56% - 69% 之间，RAM 占用维持在 54% 左右。四个Replicant 节点高效协同，将 200 万连接均衡分配，每个节点处理约 50 万客户端。

![image.png](https://assets.emqx.com/images/68b2b2f1ce8ef189813db7b41113af77.png)

<center>EMQX 仪表板显示 2M WebSocket 连接</center>

### 核心指标：端到端延迟表现

在接入并保持海量并发连接的基础上，消息投递能够保持低延迟是 EMQX 的一大优势。在 200 万个连接和每秒近 10 万条消息的吞吐量下，系统的端到端延迟极低。

| **指标**            | **数值** |
| ------------------- | -------- |
| e2e_latency_ms_95th | 0.96 ms  |
| e2e_latency_ms_99th | 4.66 ms  |

在此规模下，99% 的延迟低于 5 毫秒，这充分证明了 EMQX 内部消息传递的效率以及其底层 Erlang/OTP 运行时的性能。对于毫秒必争的应用来说，这种级别的响应速度至关重要。

## 关键技术解析

**线性扩展能力是关键：**

从 50 万到 100 万连接的测试证明，可以通过增加硬件资源来可预测地扩展 EMQX。而 200 万连接的突破则进一步验证，可以通过扩展集群 Replicant 节点规模来进一步提升系统容量。

**Core-Replicant 架构优势：**

对于百万级连接的部署场景，Core-Replicant 架构模型是行之有效的方案。该架构在确保集群保持稳定且易于管理的同时，让 Replicant 节点能够专注于性能提升。

**底层技术栈的高效：**

如果没有高度优化的技术堆栈，这种性能水平是不可能实现的。EMQX 受益于久经考验的 Erlang/OTP 环境（专为构建并发、容错系统而设计），以及用于处理 WebSocket 连接的高性能 [Cowboy Web 服务器](https://ninenines.eu/articles/cowboy-2.13.0-performance/)。

**关于负载均衡器的说明：**

为确保最佳性能并排除干扰因素，本次测试中没有使用负载均衡器，而是将客户端直接连接到 EMQX 节点上。在生产环境中，建议在 Replicant 节点前端部署高性能 TCP/SSL 负载均衡器。在我们其他的使用负载均衡器的大规模测试中发现，EMQX 节点通常不是整个网络中的瓶颈。

## 结论

数字世界对网络实时交互的需求永无止境。本次基准测试表明，EMQX 已完全具备满足这一需求的能力。通过在集群中轻松支持 200 万个 MQTT over WebSocket 并发连接，并保持卓越的低延迟表现，EMQX 已经成为与浏览器客户端实时传输数据的大规模应用的首选方案。

无论您正在构建下一代协作工具、金融交易平台，还是基于 Web 仪表盘的大规模物联网网络，EMQX 都能提供您所需的性能、可扩展性和可靠性，让您没有后顾之忧地开展业务部署。

欢迎感兴趣的用户亲身体验！

- 免费[下载 EMQX ](https://www.emqx.com/zh/downloads-and-install/enterprise)或部署 [EMQX Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt)。
- [在 GitHub](https://github.com/emqx/emqx) 上探索该项目。
- [联系我们的团队](https://www.emqx.com/zh/contact)讨论您的独特用例。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
