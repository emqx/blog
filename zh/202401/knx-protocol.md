## KNX 简介

[KNX](https://www.knx.org/knx-en/for-professionals/What-is-KNX/A-brief-introduction/) 是建筑自动化和家庭控制系统的标准，起源于1990年代初的 EIB (European Installation Bus) 。它是一种开放协议，可以实现建筑物中各种设备和系统之间的通信，如照明、供暖、通风、安全和音视频设备。该技术由 [KNX 协会](https://www.knx.org/knx-en/for-professionals/index.php)管理，该协会负责全球 KNX 产品和解决方案的开发、认证和推广。

KNX 使用各种传输介质，包括双绞线（TP）、电力线通信（PL）、无线电频率（RF）和 IP/Ethernet。这种灵活性使得 KNX 适用于有线和无线安装，既适用于新建筑，也适用于对现有建筑的改造。

## KNX 总线系统

KNX 采用总线通信系统，设备连接到共同的总线上，可以交换信息和指令。由于其分散式结构，KNX 总线系统可以根据需要进行修改和扩展。最小的 KNX 应用是连接两个总线设备的系统：一个传感器和一个执行器。这个基本系统可以后续升级，添加控制任务所需的任意数量的设备。理论上，一个 KNX 系统可以由超过 50,000 个设备组成。在扩展 KNX 系统时，需要遵循特定的拓扑结构。

![KNX Bus System](https://assets.emqx.com/images/c27cefdc4b8b0c6321bcd0c0803046c8.png)

<center>KNX Bus System</center>

## KNX 设备

KNX设备涵盖了广泛的产品，专为家庭和建筑自动化而设计。以下是一些常见类型的 KNX 设备：

- KNX 电源为 KNX 总线提供电力。
- KNX 执行器：执行器用于控制电气负载，如照明、供暖、通风和空调（HVAC）系统。
- KNX 传感器：传感器用于检测和测量环境参数，例如温度传感器、湿度传感器、人体感应传感器、光照传感器和运动检测器。
- KNX 线路耦合器（line coupler）或 KNX 区域耦合器（area coupler）用于连接和桥接多个 KNX 线路或区域。它使得位于不同 KNX 线路上的设备和系统能够交换数据并相互交互。

## KNX 拓扑

拓扑结构指的是 KNX 总线系统的物理布局或排列方式。它描述了设备之间的连接方式和整体安装的结构。

线路（Line）是指 KNX 总线系统的物理段。它代表了一组通过单一总线电缆连接在一起的设备。一条线路包括一个 KNX 电源，通常不超过 64 个其他总线设备。电源和双绞线（总线电缆）具有两个功能：为总线设备提供所需的电力，并允许这些设备之间的信息交换。如果需要超过 64 个设备，可以使用线路中继器（Line Repeater）来扩展线路。

![KNX TP Line](https://assets.emqx.com/images/8e6e4b3665292be06f2afe5f53540232.png)

<center>KNX TP Line</center>

<br>

通过使用线路耦合器来创建新的线路是扩展安装的另一种方式。在主线（main line）上，可以通过线路耦合器操作多达 15 条线路，形成一个区域（area）。在 KNX 中，区域表示 KNX 安装的逻辑分组。它指的是在特定功能区域内相互连接的线路或段的集合。一个区域可以对应建筑物的特定区域，如一个房间或一个部门。

![KNX TP Area](https://assets.emqx.com/images/fbbe49f400dd1a850e1a53a5ab8f190b.png)

<center>KNX TP Area</center>

<br>

通过区域耦合器（area coupler），可以将多达15个区域添加到区域线路上，以形成一个完整的系统。

![image.png](https://assets.emqx.com/images/82413a653c9aaf96a857712c1243f1df.png)

## KNX 地址

在 KNX 系统中，每个连接到总线上的设备都被分配一个唯一的地址，用于标识和与其通信。

#### Individual Address

[Individual address](https://support.knx.org/hc/en-us/articles/115003185789-Individual-Address) 是分配给总线上每个 KNX 设备的唯一地址。它允许 KNX 系统与特定设备之间进行直接通信。Individual address 通常在设备配置或编程过程中设置，并且对于设备来说是固定的。

KNX individual address 是由三部分组成的16位值：区域号（area number）、线路号（line number）和设备地址（device address）。

例如，individual address 为 2.3.20， 表示区域 2 中线路 3 上的编号20的总线设备。

#### Group Address

组地址用于多个 KNX 设备之间的通信。它代表了 KNX 系统中的特定功能或控制点。设备可以被编程以监听和响应特定的组地址，实现基于组的控制和自动化。

组地址由三个主要组成部分组成：主组（main group）、中间组（middle group）和子组（sub group）。

例如，一个组地址为 1/2/3 表示主组1、中间组2和子组3。这些组成部分的具体解释可能会根据应用和配置而有所不同。

## KNXnet/IP

KNXnet/IP 是在 KNX 系统中用于通过 IP 网络传输数据的通信协议。通过 KNXnet/IP，KNX 设备可以通过 IP 网络相互通信，并与外部系统进行通信。它允许从具有网络连接的任何地方远程访问、控制和监控 KNX 安装。该协议利用标准的 IP 网络基础设施和协议为 KNX 提供支持，扩展了系统的功能和覆盖范围。

值得注意的是，KNXnet/IP 只是 KNX 标准中的一种通信选项。传统的 KNX 总线通信方法仍然广泛使用，而 KNXnet/IP 通常与这些方法结合使用，为建筑自动化和控制提供全面灵活的解决方案。

![KNXnet/IP Telegram](https://assets.emqx.com/images/0ab8827a355db6d084745050b44c2697.png)

<center>KNXnet/IP Telegram</center>

## KNX 协议相关工具

### ETS

[ETS (Engineering Tool Software)](https://www.ets6.org/) 是由 KNX 协会开发的一款综合性软件，用于配置、编程和调试基于 KNX 的系统。ETS 提供了一个用户友好的界面，使系统集成商、安装工程师和设计师能够创建、配置和管理 KNX 安装。它可以配置单个 KNX 设备，创建组地址，分配功能和参数，并设置自动化和控制逻辑。

### KNX Virtual

[KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php) 是由 KNX 协会提供的基于 Windows 的应用程序，允许用户模拟 KNX 安装。KNX Virtual 的主要目的是为那些希望在开始他们的第一个真实项目之前获得 KNX 技术实践经验的个人提供一个学习和培训平台。它使用户能够学习 KNX 的基础知识，并在与该系统一起工作方面建立信心。

KNX Virtual 包括 10 多种不同类型的虚拟 KNX 设备，这些设备连接到模拟的 KNX 总线。这些设备代表了各种建筑负载，如灯具、可调光灯、百叶窗、加热和冷却阀。用户还可以尝试更高级的建筑功能，如天气模块、警报、场景和逻辑操作。

## KNX 在物联网中的应用：与 MQTT 集成

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种专为物联网设备和应用程序设计的消息传输协议，采用发布/订阅模型。它具有轻量、高效、可靠的特点，并支持实时通信。MQTT 非常适用于资源受限的环境，需要高效利用能耗和带宽的场景。目前，MQTT 已广泛应用于物联网、移动互联网、智能硬件、连接车辆、智能城市、远程医疗服务、石油和能源等领域。

随着工业 4.0 的到来，制造业对智能化、自动化和数字化的需求不断增加。在这种背景下，MQTT 在设备和平台支持方面拥有广泛的选择，市场上已经有许多可用的物联网设备和系统。相比之下，KNX 的设备生态系统可能更为有限，特别是在涉及专门的物联网设备或附件时。

![Neuron 案例-工业设备连接](https://assets.emqx.com/images/4591cb408b58ee929e32c0add811dc12.png)

### 使用 Neuron 转换 KNX 到 MQTT

[Neuron](https://neugates.io/zh) 是一款强大的工业协议网关软件，可以为实时工业数据采集提供必要的物联网连接能力。Neuron 十分轻量，可以运行在各种资源受限的物联网边缘硬件设备中，并通过标准协议或其自有的专用协议与各种各样的工业设备进行通信，将其连接到工业物联网平台。

从发布之初，Neuron 就支持 MQTT 作为其通信协议之一。Neuron [MQTT 插件](https://neugates.io/docs/en/latest/configuration/north-apps/mqtt/overview.html)允许用户快速构建使用 MQTT 协议的物联网应用程序，实现设备与云之间的通信。

自 Neuron 2.1.0 版本开始，Neuron 提供了 [KNX 插件](https://neugates.io/docs/en/latest/configuration/south-devices/knxnet-ip/knxnet-ip.html)，支持使用 KNXnet/IP 协议通过 UDP 与 KNX IP 耦合器进行通信。

### 使用 EMQX 处理 MQTT 消息

[EMQX](https://www.emqx.com/zh/products/emqx) 是一款大规模可弹性伸缩的云原生分布式物联网 MQTT 消息服务器。作为全球最具扩展性的 MQTT 消息服务器，EMQX 提供了高效可靠海量物联网设备连接，能够高性能实时移动与处理消息和事件流数据，帮助用户快速构建关键业务的物联网平台与应用。

<section class="promotion">
    <div>
        免费试用 EMQX Enterprise
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

EMQX 在桥接架构中的作为 [MQTT broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，而 Neuron 则收集来自 KNX PLC 的数据并通过 MQTT 消息将数据传输到代理。在从 Neuron 接收 MQTT 消息后，EMQX 将转发数据或执行进一步的处理。

EMQX 具有丰富而强大的功能集，例如基于 SQL 的规则引擎，可实时提取、过滤、丰富和转换物联网数据，以及数据集成功能，可将 EMQX 连接到外部数据系统，如数据库。

有关 KNX 协议桥接到 MQTT 的详细教程，请参考：[Bridging KNX Data to MQTT: Introduction and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-knx-data-to-mqtt-introduction-and-hands-on-tutorial)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
