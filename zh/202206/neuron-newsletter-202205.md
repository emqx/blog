五月，我们发布了 Neuron 2.0.1，该版本主要修复了一些在 2.0.0 版本中发现的问题。此外，这个月我们主要专注于新驱动的开发，新增了南向 BACnet/IP、KNXnet/IP 驱动，北向 Sparkplug 应用，以及定制扩展了 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication) TCP 协议，极大提高了点位采集效率。

## KNXnet/IP 驱动

KNX 是一种统一且独立于制造商的通讯协定，用于智慧地连接最先进的家居与建筑系统技术，包括家庭住宅和办公综合体的供暖、照明和门禁系统管理对舒适性和多功能性要求高。 KNX 可用于规划和实施高效节能的解决方案，在提供更多功能和便利的同时降低能源成本。

我们实现驱动支持 BIT/BOOL/INT8/UINT8/INT16/UINT16/FLOAT 数据类型，作为 KNXnet/IP Client 进行数据采集和设备控制。KNXnet/IP 驱动支持两种点位地址，一种为 KNX group address，用户只能对其进行写操作，另一种地址格式为 KNX group address 附带一个 KNX individual address，用户只能对其进行读操作。

## BACnet/IP 驱动

BACnet 是用于智慧型建筑的通讯协定，是国际标准化组织（ISO）、美国国家标准协会（ANSI）及美国采暖、制冷与空调工程师学会（ASHRAE）定义的通讯协定。 BACnet 针对智慧型建筑及控制系统的应用所设计的通讯，可用在暖通空调系统（HVAC，包括暖气、通风、空气调节），也可以用在照明控制、门禁系统、火警侦测系统及其相关的装置。

我们实现驱动支持 BIT/FLOAT 数据类型，作为 BACnet/IP Client 进行数据采集和设备反控。BACnet/IP 驱动目前支持的 OBJECT TYPE 主要有 ANALOG INPUT、ANALOG OUTPUT、ANALOG VALUE、BINARY_INPUT、BINARY_OUTPUT、BINARY_VALUE、MULTI_STATE_INPUT、MULTI_STATE_OUTPUT、MULTI_STATE_VALUE。协议层采用了异步收发指令，最大支持 255 条指令并发，提高了采集反控效率。

## Sparkplug 插件

MQTT Sparkplug 是用于智能制造和工业自动化用例的互操作性协议。 Sparkplug 为设备制造商和软件提供商提供了一种一致的方式来共享数据结构，以加速现有工业数字化转型。

北向配置与 MQTT 插件类似，MQTT Topic 组成与 Neuron 的 Group 相匹配，支持按照 Neuron 的 Group 为单位上报订阅数据，并支持在 Sparkplug 的 Application 端对 Neuron 的采集设备进行写入操作。数据类型已经支持 Neuron 南向设备的所有定义类型。

## 客戶定制化的 Modbus TCP 驱动

需要设备侧支持。使用 Modbus TCP MBAP 中 2 字节的长度替代 ADU 中单字节长度来表示帧长，Modbus TCP 帧最大可支持到 65535 字节。扩展后的协议一次采集指令能采集超过三万个数据点位，减少了 Neuron 与设备之间的交互次数，极大提高了采集效率。

## 其他更新

- Neuron 与 eKuiper 的 Dashboard 进行了集成。
- 官网文档进行了大量优化，还在持续改进中。
- 针对 GitHub 社区的一些 issue，对 Neuron 的编译以及交叉编译做了一些优化，降低了搭建入门开发环境的门槛。
- 重构了开源 Modbus TCP 的实现。
- 修复了在 2.0.0 版本中测试发现的问题。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
