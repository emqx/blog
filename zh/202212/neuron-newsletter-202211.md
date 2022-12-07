11 月我们发布了 [Neuron](https://neugates.io/zh) 2.2.11 版本，主要优化修复了一系列在 2.2 版本中发现的问题，同时为 2.3 版本的发布做准备：增加 EtherNet/IP 驱动，完善 CNC FOOCAS 驱动，OPC DA 支持远程连接；MQTT 插件依赖库切换为 NanoSDK，极大提高数据收发性能。

## 新增 EtherNet/IP 驱动

EtherNet/IP 是由 ODVA 规范管理并公开的工业通信网络。OVDA 是一家国际标准开发组织，由世界领先的自动化供应商成员组成，EtherNet/IP 正是这个组织的代表作。EtherNet/IP 通过将 CIP 协议、TCP/IP、以太网这三者组合之后得以实现。

Neuron 新增的该协议驱动支持较为完善的数据类型，包括：UINT8/INT8、UINT16/INT16、UINT32/INT32、UINT64/INT64、FLOAT、DOUBLE、STRING、BIT。可用于连接支持 EtherNet/IP 协议的 PLC 设备。

## 完善 CNC FOCAS 驱动

CNC FOOCAS 驱动现支持更多类型的数据采集，包括 CNC 相关数据以及 PMC 区域的数据。

CNC 数据主要有 AXIS 相关数据（位置、速率等），以及 SPINDLE 相关数据。

PMC 数据支持采集的数据区域包括 message demand、counter、data table、extended relay、single to CNC → PMC、single to PMC → CNC、keep relay、input single from other device、output single from other device、internal relay、changeable timer、signal to machine → PMC、single to PMC ->machine；每个区域都支持多种数据类型。

## OPC DA 远程连接

- 添加了局域网跨主机访问的功能；
- 添加了 GUI——可视化设置 DA 和 UA 连接参数，可以直观看到测点数据变化；
- UA 服务器添加了默认加密连接和用户名/密码认证等功能；
- 主程序名称由 opcshift 更改为 neuopc；
- 添加了 DCOM 跨主机访问的设置文档；
- 添加了本机数据源读取的设置文档；

## 其他更新

- WEB 与 API 端口统一为 7000。
- 增加适配 DTU 文档。
- 完善官网文档，适配即将发布的 2.3 版本。

## 问题修复

- 修复 MODBUS 插件处于 server 模式时重连异常的问题。



<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
