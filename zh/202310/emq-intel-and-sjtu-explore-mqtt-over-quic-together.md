凭借多路复用、更快的连接建立和迁移等优势特性，[MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 已逐渐成为下一代的物联网、车联网协议标准。EMQ 在产品中开创性的采用 MQTT over QUIC 这一协议，为各行业的用户提供更好的性能和更稳定连接，特别适用于解决在不稳定网络环境下出现的各种数据传输挑战。

MQTT over QUIC 将传统 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)中基于 TCP 的传输层协议替换为了 QUIC（Quick UDP Internet Connections）。与 TCP 不同，QUIC 基于 UDP（User Datagram Protocol）构建，更适合在不稳定网络条件下进行通信，带来低延迟、减少握手时间、支持多路复用等诸多优势。

在 2023 年夏季，EMQ 联合 Intel 和上海交通大学推出了一门短期课程，旨在向国内外高校学生深入讲解和实践 MQTT over QUIC 协议的各项性能。在课程中，我们模拟了车联网中常见的不稳定网络环境，为大学提供了机会利用 MQTT over QUIC 协议设计并执行各种实验。课程中使用英特尔开发套件爱克斯开发板 AIxBoard，并运用 EMQ 的各类物联网数据软件完成整个开发项目的实践。

## 大学关于 MQTT over QUIC 的案例分享 

### 1. MQTT over QUIC 在弱网环境下的性能验证

#### 实验一：

来自乌克兰 Kharkiv National University of Radio Electronics 大学 的 Dmytro Fedoryshyn 同学，利用EMQX 5.0 与 emqtt_bench 工具，在 AWS c7g.xlarge (4vCPU/8Gi) 实例上，比较了 MQTT over QUIC 与 MQTT over TCP 两者之间的性能表现。

**实验经过：**Dmytro Fedoryshyn 同学采用随机丢包模拟真实的弱网环境，其结果显示了MQTT over QUIC在网络波动时依然具备很高的稳定性，下图为性能评估结果：

![测试结果](https://assets.emqx.com/images/4cc5115e125c79a4c443269431c00d56.png)

![MQTT over TCP vs MQTT over QUIC](https://assets.emqx.com/images/26e14ffb738c5f934d572f4f2c3b8b28.png)

**实验结论：**“通过进行基准测试，我们探索了 MQTT over QUIC 相对于标准 MQTT over TCP 数据传输协议的关键优势 —— 即使在弱网环境中仍能保持稳定高效运行。这是车联网领域的重要突破，因为许多车辆用户常常面临相似的问题：车辆可能在山区、矿区、隧道等地运行，这可能导致连接中断。频繁的连接中断和缓慢的重连带来糟糕的用户体验，而 MQTT over QUIC 是缓解这个问题的完美方式。”

#### 实验二：

来自加拿大多伦多大学的 Eleonora Scognamiglio 同学和英国华威大学的 Thomas Nguyen 同学，联手设计了一组验证方案，研究不同网络质量下 MQTT over QUIC 与 MQTT over TCP 的性能差异。

**实验经过：**Eleonora Scognamiglio 同学和 Thomas Nguyen 同学，使用不同比例的随机丢包策略，探寻在各种网络状况下 MQTT over QUIC 和 MQTT over TCP 的性能差异，证明在各种弱网状况下，MQTT over QUIC 均有明显的性能优势：

![测试结果](https://assets.emqx.com/images/146d7093fc8fd19b67b7828bd95dce2c.png)

**实验结论：**“上图总结了我们的研究结果，包括两种协议在不同连接条件下达到的最大数据包传输速率。通过上述对四种网络条件（0%、25%、50%、75%）的测试，我们可以看到，在网络条件好的情况下，MQTT over QUIC 和 MQTT over TCP 两种协议表现相似；然而，随着丢包率的增加，MQTT over QUIC 的性能似乎优于其对手。因此，我们可以得出结论，MQTT over QUIC 的速度和稳定性更好，尤其在弱网络条件下表现出色。”

### 2. MQTT over QUIC 桥接方案

在 MQTT over QUIC 桥接技术的专题课程中，来自上海交通大学的 Fengping Sun 同学和加拿大多伦多大学的 Phoebe Chuang 同学，利用 EMQ 的 [NanoMQ](https://nanomq.io/zh) 的桥接功能，在英特尔 AIxBoard 开发板上真实地模拟了物联网和车联网中的场景，成功地通过 MQTT over QUIC 方案，将传感器数据上传到服务器，验证了该技术在实际场景中的可行性。

**实验经过：** 在此专题课程中，Fengping Sun 和 Phoebe Chuang 用英特尔 AIxBoard 开发板模拟车端环境，使用MQTT publisher 通过 MQTT over TCP 协议将模拟数据发送到车端上部署的 NanoMQ。NanoMQ 负责将 MQTT 连接映射到 QUIC 流，将数据上传到云端的 EMQX 集群。这种方法的好处在于，它不需要对客户端进行修改或适配，同时还能够充分利用 MQTT over QUIC 的优势。

![实验截图1](https://assets.emqx.com/images/07bf6c7e7ec70e26d11ba8863755c3c0.png)

![实验截图2](https://assets.emqx.com/images/902714cd001f2b438a38d47d1b1d7930.png)

![实验截图3](https://assets.emqx.com/images/c5d3eb9cf1a66959e1bd903039c360e2.png)

![实验截图4](https://assets.emqx.com/images/de646c18976d2c01a9cd6878bbd323bc.png)

**实验结论：**

“稳定网络条件下，MQTT over QUIC 与 MQTT over TCP 性能相似。在不稳定网络条件下， 相较 MQTT over TCP 的传输率在每秒 3 - 300 数据包间浮动，MQTT over QUIC能够稳定在每秒传输 260 - 280 数据包，有明显的性能提升 ”

## 课程支持

### EMQ

EMQ（杭州映云科技有限公司）是全球领先的开源物联网数据基础设施软件供应商。本次课程中所使用到的核心产品组合包括 EMQX，是世界上最可扩展、可靠的开源 MQTT 消息平台，此平台同时也提供商用版；以及 NanoMQ，一个可以运行在物联网边缘端的超轻量 MQTT 中间件。它们共同提供了一站式的云原生解决方案，让边缘端和云端的物联网数据可以实时连接、传输、处理和分析。EMQ 公司成立于 2017 年，旗舰产品 EMQX 拥有来自 50 多个国家的500 多家企业用户，连接全球超过 2.5 亿台物联网设备。

### Intel

本次课程中学生们使用的英特尔开发者套件 AIxBoard（爱克斯板）开发板是专为支持入门级边缘 AI 应用程序和设备而设计，能够满足人工智能学习、开发、实训等应用场景。该开发板是类树莓派的 x86 主机，可支持 Linux Ubuntu 及完整版 Windows 操作系统。板载一颗英特尔4核处理器，最高运行频率可达2 .9 GHz，且内置核显（iGPU），板载 64GB eMMC 存储及 LPDDR4x 2933MHz（4GB/6GB/8GB），内置蓝牙和 Wi-Fi 模组，支持 USB 3.0、HDMI 视频输出、3.5mm 音频接口、1000Mbps 以太网口。完全可把它作为一台 mini 小电脑来看待，且其可外接 Arduino，STM32 等单片机，扩展更多应用及各种传感器模块。

![AIxBoard（爱克斯板）开发板](https://assets.emqx.com/images/6e7145f9b0656eda9a66616ad1785f27.png)

在过去的50多年里，英特尔对世界产生了深远的影响，通过创造彻底革新我们生活方式的激进创新，推动着商业和社会的发展。如今，英特尔正在运用其影响力、规模和资源，使各类企业更充分地进行数字化转型。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
