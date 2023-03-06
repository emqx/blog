2 月，Neuron 团队主要侧重于开发新的驱动，新增了南向 IEC61850 驱动、南向 Allen-Bradley DF1 驱动、Profinet 驱动支持以及静态点位等功能，这些新驱动和新功能将在 2.4 版本中正式发布。

## IEC61850 驱动

IEC61850 标准是电力系统自动化领域的通用标准。Neuron IEC61850 驱动实现了该标准中 MMS 协议的连接和读写操作。MMS 中的多种数据类型也已经映射到 Neuron 类型中，现在可以通过指定 IED（智能电子设备）中的 DA（对象属性）地址和类型，完成数据的获取和修改操作。

## Allen-Bradley DF1 驱动

DF1 协议是 AB 公司可编程控制器系统广泛支持的数据链路层通信协议，各系列可编程控制器及装有 RSLinx 通信软件的计算机均支持 DF1 协议。它的物理层建立在 RS232 和 RS485 等电气标准之上，针对不同的设备建立不同的应用层命令。综合物理层、数据链路层和应用层后能够完成基于 DF1 协议的通信。

目前 Neuron 已实现半双工通信方式的部分应用层指令，使用 CRC 校验方式。Neuron 与设备之间通过串口建立连接，并通过站点号与指定的 PLC 模块建立通信。

## Profinet 驱动

Profinet 是一个通过以太网通信的现场总线。Neuron 将作为 Profinet 中的 Controller 与 Profinet IO 设备进行高频率的数据交换，交换频率精度根据设备硬件配置可达到毫秒级别。因 Profinet 循环数据主要在以太网第二层上运行，即不存在 IP 网络层，将不能进行路由间的数据转发，需要保证 Neuron 与 Profinet IO 设备在同一个局域网中。

## 静态点位支持

静态点位主要用于一些静态数据的配置以及上传。静态点位将不会下发到插件层面，完全由 Neuron 核心支持处理，可在任何 Group 中添加静态点位，静态点位可读可写，用户可随时修改静态点位的值；并且通过北向订阅 Group 后进行发送。

## 数据处理相关 UI 升级

目前已发布的 NeuronEX 版本中实现的数据流处理 UI 适配的是 eKuiper 1.6 版本的相关 UI。因此我们将NeuronEX 版本中的数据流处理 UI 进行了升级，适配较新的版本，并增加了 Source 的配置以及上传插件等 UI。

## 问题修复

本月我们对如下问题进行了修复：

- Modbus RTU 配置页面未能根据 schema 正确切换
- 配置多个 OPC UA node 时，SSL 证书导致的连接异常
- ADS 插件多线程数据竞争
- S7Comm 插件某些情况下异常退出
- Docker 镜像中设置 VOLUME 异常



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
