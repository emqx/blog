近日，Neuron 2.1.0 正式发布。这是 Neuron 开源后的首个子版本，在 v2.0.0 的基础上对核心代码进行了重构，通过无锁核心提升了产品稳定性。此外 Neuron 2.1.0 还完成了与边缘流式处理引擎 eKuiper 的集成，实现了一站式的边缘数据采集与处理。新增的 Sparkplug B 规范支持和多个驱动插件，也为 Neuron 用户构建符合工业 4.0 时代发展趋势的工业物联网平台提供了更大便利。



> Neuron 的前端代码现已开源，请参考： [https://github.com/emqx/neuron-dashboard](https://github.com/emqx/neuron-dashboard)
>
> Neuron 2.1.0 下载地址：[https://neugates.io/downloads](https://neugates.io/downloads) 



## 全面提升稳定性与易用性

**最新发布的 v2.1.0 核心采用 Actor 模式，** 这一模式下所有 Datatag（数据标签）操作都会转换成相应的消息类型，并通过 NNG 将消息投递到对应的消息处理队列中进行顺序处理，解决了旧版本中因线程间互锁而导致的程序崩溃问题，**提高了设备接入性能，稳定性得到了很大提升。**

此外，Neuron 2.1.0 对所使用的 HASH TABLE、LIST、ARRAY 等数据结构进行了统一，**对项目相关的依赖库与头文件进行了精简，** 用户将可以更容易地参与到 Neuron 项目中，并对其进行二次开发。

同时，之前无法在较低内核版本的 Linux 中使用的问题也得到了改善，Neuron 2.1.0 在更低端的设备中也同样适用。

## 实现一站式工业数据采集与处理

Neuron 2.1.0 实现了与边缘流式处理引擎 eKuiper 的集成。

用户不再需要通过繁琐的配置流程额外手动部署 MQTT Broker 作为数据中转，就可以直接在 Neuron 中接入 eKuiper 对采集到的数据进行实时的流式处理与函数计算，还可以在 eKuiper 中反控 Neuron 所接入的设备。

**两个产品的界面也实现了一体化无缝集成。** Neuron 2.1.0 的安装包默认配置了与 eKuiper 1.5.1 的连接，用户只需在 Neuron 的 Dashboard 找到北向应用管理中默认的 data-stream-processing 应用节点卡片，订阅所需要的 Group，并在数据流处理模块添加需要 eKuiper 处理的规则，即可进行数据处理与清洗。**通过极简的使用流程为云端平台提供高质量的数据源，减轻云端数据处理压力。**

> 具体使用方法可参考[官方文档快速开始](https://neugates.io/docs/zh/latest/quick-start/hardware-specifications.html#run-for-the-first-time)。

![Neuron 北向应用管理](https://assets.emqx.com/images/320870fb329cf08bc433d484af4c5eda.png)

![Neuron 规则管理](https://assets.emqx.com/images/0c9ba2d9d7bef0ce0ae82a2135bee10b.png)


## 支持 Sparkplug B 规范

Sparkplug B 是一种建立在 MQTT 3.1.1 基础之上、依据工业物联网（IIoT）领域应用的特性在信息主题和信息内容格式上所作的规范。Sparkplug B 在保证灵活性和效率的前提下，使 MQTT 网络具备状态感知和互操作性，为设备制造商和软件提供商提供了统一的共享数据结构。

从 2.1.0 版本起，Neuron 正式支持 Sparkplug B 规范，这意味着**不支持 MQTT 的设备也将可以通过 Neuron 间接实现 MQTT 通信。**

此外，网络边缘的设备和传感器还可以通过 Sparkplug B 与 SCADA 系统、Historian 和分析程序等进行通信。

支持 Sparkplug B 的 Neuron 将帮助工业领域用户实现各类工业设备的统一数据接入，打造统一命名空间的工业数据信息平台中心，加速工业 4.0 进程。



## 更完善的工业协议支持

Neuron 2.1.0 还新增了多个驱动插件，另外对部分协议支持进行了优化。

- **ASHRAE BACnet/IP：** 一种用于楼宇自动化和控制网络的通信协议，旨在实现楼宇各控制系统的通信，可用于供暖、通风和空调控制 (HVAC)、照明控制、访问控制和火灾探测系统及其相关设备等应用。

- **KNXnet/IP：** 世界知名的智能楼宇协议，允许通过单一输入进行整体楼宇控制，包括照明、供暖、电机、门禁、安全、能源和音频/视频等。

- **DL/T645 and DL/T645 over tcp：** 多功能电能表通信协议标准，用于统一和规范多功能电能表与数据终端设备进行数据交换时的物理连接和协议。目前主要有 DL/T645-97 和 DL/T645-07 两个版本，Neuron 2.1.0 实现了对 DL/T645-07 的支持。

   >注：另外提供以 TCP 连接方式选项，以便远程利用 DTU 连接。

- **Modbus RTU：** 增加 Modbus RTU 串口支持，用户可使用 DTU 接入设备，通常通过 RS485/232/422 端口连接 Modbus 从机设备，连网方式大多以 TCP 透传为主。

- **Modbus TCP 定制驱动：** Modbus 常规通讯模式的数据包长度描述字段为一个字节，限定 Modbus TCP 数据包长度的最大值是 256B，新增的定制驱动将数据包长度描述字段扩大为两个字节，采集数据包长度最大支持 64KB。

- **IEC 104 新增功能：** 新增支持设备主动上报数据的处理，提高了 IEC104 采集数据点位的效率。

## 未来规划

为了方便用户进行驱动插件的二次开发，我们将在 2.2.0 版本中提供 SDK 开发包。其他产品功能也将进行持续优化。欢迎在 GitHub 提交 issue 或 pr，参与 Neuron 开源项目。

<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
