工业协议网关软件 Neuron 2.5.1 版本现已正式发布！

最新版本带来了基于南向设备的模版、[Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) UDP 传输支持、Modbus 读重试支持、IEC104 高可用主备访问模式等新功能。同时新增了 Profinet IO、Mitsubishi FX、Omron FINS UDP、Panasonic Mewtocol 和 DLT645-1997 五种南向驱动。

此外，从该版本开始，我们对产品进行了如下调整： 

- 为英语用户提供了[国际版](https://www.emqx.com/en/try?product=neuron)。 
- 取消与 eKuiper 集成的 NeuronEX 版本。 
- 取消 Modbus TCP community 插件，Modbus TCP 和 Modbus RTU 插件由闭源转为开源。此外，用户可以免费体验 30 个数据标签或节点内的所有协议驱动。了解详情：[Neuron 提供免费无限时试用：完整体验数十种工业协议连接](https://www.emqx.com/zh/blog/experience-neuron-industrial-iot-gateway-software-for-free-with-time-unlimited-trial-license) 

## 新功能概览

### 基于南向设备的模版功能

该功能适用于实际使用中需要配置大量相同型号的设备点位的场景。例如，配置三台点位相同但配置不一致的设备时，可借助模版功能在添加设备时快捷创建三个带相同点位的设备节点。

![模板管理](https://assets.emqx.com/images/b5774a91a4d3f0e08115dfbb59965a69.png)

<center>模版</center>

<br>

![新增设备](https://assets.emqx.com/images/69ce43be0e0555f2f3a15ee1358d7865.png)

<center>基于模版创建设备节点</center>

<br>

同时具有模版导入/导出功能。[模版使用说明文档](https://neugates.io/docs/zh/latest/configuration/templates/templates.html)

### Modbus 支持 UDP 传输

UDP 是一种传输层协议，Modbus TCP 插件支持基于 Modbus TCP 协议的 UDP 传输。

![Modbus 支持 UDP 传输](https://assets.emqx.com/images/61c26fa40e364ee2cdd1719b078e7655.png)

<center>Modbus UDP 配置界面</center>

### Modbus 插件支持读重试

Modbus 插件在设备连接异常等情况下支持读重试，用户可通过配置页面设置重试的次数以及重发读指令的时间间隔。

### IEC104 支持高可用的主备访问模式

在 IEC 104 协议中，主备访问是一种实现高可用性的机制，以确保在主设备故障或不可用的情况下，备用设备可以接管并继续提供服务。

IEC 104 协议的主备访问机制可以实现系统在主设备故障或不可用时的无间断运行。这对于需要高可用性和可靠性的远程监控和控制应用非常重要，特别是在电力系统等关键领域中。

![IEC60870-5-104 配置界面](https://assets.emqx.com/images/5f7cc28ade50dc27c5bc87d475a8eb0c.png)

<center>IEC60870-5-104 配置界面</center>

## 新增驱动介绍

### Profinet IO

Profinet IO（Industrial Ethernet Input/Output）是一种用于工业自动化领域的实时以太网通信协议。它基于以太网技术，旨在提供高性能、可靠的数据交换和实时控制，适用于工厂自动化、过程控制和机械设备等领域。

Profinet IO 是 Profinet 协议家族中的一个成员，它专门用于实现输入/输出（I/O）设备与控制系统之间的通信。它允许实时传输数字和模拟信号，以及控制和监视设备的状态。

![Profinet IO](https://assets.emqx.com/images/49612671fc569880b1283242b9218ea9.png)

[Profinet IO 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/profinet/profinet.html)

### Mitsubishi FX

Mitsubishi FX 系列 PLC 是三菱电机推出的一款经济实用的 PLC 产品系列。它以其简单易用、可靠稳定和灵活性等特点而受到广泛欢迎。FX 系列 PLC 适用于各种规模和复杂度的应用，从小型机械设备到大型生产线都可以使用。

Neuron 中 Mitsubishi FX 插件可用于通过 FX 编程口访问三菱的 FX0、FX2、FX3 等系列 PLC。

![Mitsubishi FX](https://assets.emqx.com/images/5d3aaddd4038bd657034f7055a876108.png)

[Mitsubishi FX 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/mitsubishi-fx/overview.html)

### Omron FINS UDP

Omron FINS 是一种用于工业自动化领域的通信协议。FINS 协议用于实现欧姆龙设备之间的数据交换和通信，包括 PLC（可编程逻辑控制器）、传感器、伺服驱动器等。

在 FINS 协议中，UDP（User Datagram Protocol）是一种传输层协议，用于在网络上传输 FINS 协议的数据包。UDP 是一种无连接的协议，它提供了一种简单的、不可靠的数据传输机制，适用于需要高效性和实时性的应用场景。

Neuron 对 FINS UDP 协议的支持，使欧姆龙设备可以通过以太网进行快速、实时的数据交换。UDP 通信相比于其他协议（如TCP）具有更低的通信延迟，但它不提供可靠性和数据完整性检查。因此，在使用 FINS UDP 进行通信时，需要确保网络稳定，并使用适当的机制来处理数据丢失和错误。

![Omron FINS UDP](https://assets.emqx.com/images/682b0087802fe53099d8732299a60985.png)

[Omron FINS UDP 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/omron-fins/omron-fins-udp.html)

### Panasonic Mewtocol

Panasonic Mewtocol 是一种用于工业自动化领域的通信协议。它是用于实现松下设备之间的数据交换和通信的协议，包括可编程逻辑控制器（PLC）、人机界面（HMI）、伺服系统和其他工业设备。

Neuron 中的 Panasonic Mewtocol 插件用于通过以太网访问松下的 FP-XH、FP0H 系列 PLC。

![Panasonic Mewtocol](https://assets.emqx.com/images/35fb115aa058ee3bf47f1b55753e7dde.png)

[Panasonic Mewtocol 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/panasonic-mewtocol/overview.html)

### DLT645-1997

DL/T645-1997 是中国用于电子能量计量器的技术标准。该标准规定了电子能量计量器与数据采集系统之间进行信息交换的通信协议和数据格式。

DL/T645-1997 定义了数据帧的结构、数据字段的内容以及传输能耗和其他相关信息的通信方法。它涵盖了诸多方面，如抄表、负荷控制、事件记录和参数设置等。

该标准为能量计量器与供电公司或其他参与能源监测和管理的实体之间的通信提供了共同的框架。它实现了对能量使用情况进行准确高效的数据采集、计费和分析。

DL/T645-1997 插件支持串口连接和透传的 TCP 连接。

![DLT645-1997](https://assets.emqx.com/images/886a6548dfb439dde55e42e41b5370f4.png)

[DLT645-1997 驱动使用说明文档](https://neugates.io/docs/zh/latest/configuration/south-devices/dlt645-1997/dlt645-1997.html)

## 未来规划

- MQTT 功能升级

   上报离线缓存数据计划添加频率控制，用户可自行设置上报数据的频率。同时，MQTT 上报离线缓存数据支持单独定义 Topic，可由用户自行定义。

- 驱动升级

   未来版本中将会对 IEC60870-5-104、BACnet/IP 等驱动进行持续升级完善。同时，SECS/GEM 等驱动协议也在计划支持中。

- 功能优化

   下载日志及 DEBUG 日志的功能会不断优化，便于用户使用及问题的排查。同时，支持配置文档的功能也在优化中。

 

<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
