七月，我们发布了 Neuron 2.1.1、2.1.2 两个版本，主要修复了 2.1.0 版本中存在的问题。 此外，我们还引入了 SQLite 以存储 Neuron 的配置信息，新增了南向驱动非 A11。同时优化了各插件的错误码，通过错误码可以定位大多数问题。在 CI 中引入了 cppcheck 进行代码的静态检查，在开发阶段就能避免部分问题。

## 非 A11 驱动

非 A11 驱动适用于非 A11 设备，插件支持 CLIENT 和 SERVER 模式对接设备。目前插件支持 UINT16/INT16/UINT32/INT32/FLOAT/STRING 数据类型，支持用户自定义指令读取数据。

## 其他新增功能概览

- 新增 MQTT 周期上报心跳报文，包含 Neuron 下配置各个 Node 的状态信息等。
- 新增驱动插件测试模版，该模版利用自动测试框架 Robot Framework 的 Template 实现，新增南向驱动利用该测试模版可更加便捷地进行功能测试。
- 引入 SQLite 存储 Neuron 各项配置。
- 三菱驱动 QnA 3E 自动根据配置的点位信息进行批量数据采集，提升采集效率。
- 新增适配西门子 S7-300PLC 的驱动插件。
- 插件停止状态下，将断开与设备的连接，并且读写数据时将会报错。

## 问题修复

- 修复 MQTT 插件某些情况下 CPU 跑满的问题。
- 修复 OPC UA 插件崩溃问题。
- 修复 MODBUS 插件状态显示异常问题。
- 修复 S7COMM 插件 License 校验异常问题。

## 文档更新

- 完善了 Neuron 2.1.0 的官网文档，增加了一些设备配置范例以及一些对应 Neuron 版本的修改。

## 即将到来

- OPC DA 南向插件，可用于连接 OPC DA 服务器。
- Beckhoff 南向插件，可用于连接倍福 Beckhoff 设备。
- 点位订阅，点位采集值变化才进行上报。
- C语言实现的 SDK 包，可使用 SDK 包进行插件开发。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
