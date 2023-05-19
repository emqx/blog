12月，我们发布了 Neuron2.0-alpha.1 版本。这是第一个具备基本完整功能的内部版本，目前已经提供给内测用户使用。从这个版本我们可以看到 Neuron 2.0 具有非常低的内存消耗和 CPU 占用率。

### Neuron 2.0-alpha.1 版本功能

- 具有完整的 Web UI 界面。用户可以通过 Web UI 来控制和配置 Neuron、设置点位、读写 Neuron 连接设备的数据。
- 支持 [MQTT](https://www.emqx.com/zh/mqtt-guide) 连接。用户可以远程通过 MQTT 来控制和配置 Neuron、设置点位，读写neuron连接的设备的数据。
- 支持同时连接多个相同或不同的工业设备。目前已支持 Modbus TCP 和 OPC UA 协议设备。
- 插件化的应用和驱动支持，可以在运行时独立控制驱动的启动和停止，也可以动态增加应用和驱动，在Neuron 运行时更改配置。
- 使用 Haskell 语言写的代码生成器来生成 json 解析的C代码及序列化成 json 的 C 代码。极大减少了手写的代码数量，以及手写解析代码和序列化代码带来的错误，增强了程序的稳定性。

### Neuron 2.0 的测试

Neuron 2.0 已经有了完整的单元测试，每个独立的模块都有对应的单元测试，可以及时发现模块修改后产生的 Bug。

我们使用了 robot 自动测试框架来对 Neuron 进行完整的功能测试。目前已经完成了 Web API 接口、MQTT 接口节点、分组数据、插件、设备连接状态、group config、数据读写等相关的功能测试。

### Neuron 2.0 Bug 修复

本月我们修复了 Neuron 2.0 中的以下问题：

- Modbus 循环读有时出现崩溃的问题。
- 删除 node 时偶尔崩溃的问题。
- 重启 adapter 系统假死的问题。
- 关闭 Neuron 时引用释放的 group config 导致崩溃的问题。
- MQTT 订阅 node 新建的 group config 不成功的问题。

### Neuron 1.x 版本情况

基于 1.3.x 版经验以及客户对 Neuron 的建议，我们对 Neuron 进行了架构调整并于本月初发布了 Neuron 1.3.5 。主要更新包括：

- 在 MQTT JSON 结构中添加 uuid 项。
- 在 MQTT 参数列表中为 Heartbeat 消息添加自定义主题设置。
- 为每个标签添加中文描述字段。

同时，本月我们开始对 1.4.0 进行规划，计划在明年一月发布，主要在以下方面进行更新：

- 添加三菱 FX5U 驱动

- 为以下 PLC 添加 STRING 数据类型处理，可读写 PLC 字符串

| Modbus TCP/RTU/RTU on TCP |
| ------------------------- |
| OPC UA                    |
| 西门子 ISOTCP             |
| 欧姆龙 FINS on TCP        |
| 三菱 Q 系列和 L 系列      |
| 三菱FX5U                  |

敬请关注 Neuron 的后续进展。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
