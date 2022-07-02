六月，我们发布了 Neuron 2.1.0 版本，这个版本主要与 eKuiper 进行了深度集成，可一键部署携带数据处理功能的 Neuron。此外，我们主要专注于新驱动的开发，新增南向驱动 DLT645，并对部分功能进行了优化，以更加贴合实际应用场景的使用。Neuron 的 Dashboard 页面进行了开源，用户现在可以对前端界面进行定制化的开发。

## DLT645 驱动

DLT645 驱动适用于 DL/T 645-2007 通信协议，插件支持根据不同的数据标识，自动选择对应的数据格式。目前插件支持 UINT8/UINT64/DOUBLE 数据类型，支持读取 DI3 = 00 , 02 的全部数据标识和 DI3 = 04 的部分数据标识。插件还支持两种连接方式：串口连接和 TCP 连接。

## 新增功能概览

- 新增 IEC104 协议支持设备主动上报数据处理的功能，提高了 IEC104 采集数据点位的效率。
- 新增 Dashboard 数据处理引擎的集成，现在可以直接通过 Neuron 的配置页面，配置北向 eKuiper 插件后（安装包已默认配置），可在数据处理选项中配置数据处理规则，详细使用方式可参考官网文档。
- 新增定制化的 Modbus TCP 模拟器，模拟器支持以标准的 Modbus TCP 协议进行读写数据，并且支持扩展的 Modbus TCP 协议，可以一次读取 65535 字节的数据。
- 重构 Neuron 核心代码的实现，现在 Manager 以及各个 APP 以及 Driver 对应的 Adapter 采用 Actor 模型实现，所以操作都会转换成相应的消息类型，且投递消息到 Manager 或者是 Adapter 对应的消息处理队列，进行顺序处理，解决了很多并发导致的问题；并且现在 Neuron 核心中各个模块采用了无锁的实现，提高了稳定性和对接设备性能。
- 重构了 HTTP API 的参数，使用 PLUGIN/NODE/GROUP/TAG 相应的名字替换 API 中使用的 ID 字段，增强了 HTTP API 的易用性，调用 API 无需再调用其他 API 获取对应的 ID 了。

## 问题修复

- 根据社区反馈较多的一些编译问题，Neuron 删除了一些不必要的依赖库以及删除合并了一些重复的导出头文件，统一 Neuron 中使用的 HASH TABLE、LIST、ARRAY 等数据结构，降低了参与 Neuron 项目开发的门槛；删除了无法在较低内核版本的 Linux 中使用的特性，以使 Neuron 可以在更低端的设备中使用。
- 修复了在之前版本中发现的内存泄漏问题。
- 修复了在之前版本中发现的核心数据异常以及某些驱动对接设备异常的问题。

## 其他更新

- 完善了 Neuron 2.1.0 的官网文档，增加了一些设备配置范例以及一些对应 Neuron 版本的修改。

<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
