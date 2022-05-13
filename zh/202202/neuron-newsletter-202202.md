本月，我们为即将于三月初发布 Neuron 2.0-beta.1 版本进行了紧张有序的准备工作。beta.1 版本是一个重要版本，该版本中我们增加了商业版 Modbus TCP 和 OPC UA 驱动，有完整的持久化功能，并且具备完善的功能测试和压力测试，是第一个经过稳定测试的具有商用模块的版本，也是后续开发的一个基准版本。

## Neuron 2.0 的功能完善

- 新增商业版的 Modbus TCP 驱动和 Modbus RTU 驱动。商业版的 Modbus TCP 驱动具有更好的性能，支持 bit 类型的数据以及更多的点位数量。Modbus RTU 则在此基础上增加了串口通讯的支持。
- 增加了商业版的 OPC UA 驱动，具有更好的数据读写性能，支持数据订阅和登录功能。
- 完善了压力测试流程，现在可以长时间对 Neuron 2.0 进行压力测试，以测试其稳定性，并输出 CPU 占用和内存占用的图形化报告。目前已经完成了 1K、10K、50K 的点位数量下的压力测试，并输出了测试报告。
- 完善了功能测试，增加了商业版的 Modus TCP 和 Modbus RTU、OPC UA 的功能测试。
- 增加 syslog 的支持。现在用户可以通过 syslog 的工具查看 Neuron 的 log。
- 增加 Neuron 的 SDK 开发包的打包，用户可以用这个 SDK 开发包来开发自己的第三方设备协议驱动和应用。

## Neuron 2.0 的测试

压力测试的流程现已完全可用。用户可以加入到 Neuron2.0 的 weekly build 中使用，也可以在版本发布前进行压力测试。

单元测试和功能测试在持续的维护，添加新模块对应的单元测试和功能测试用例。

## 重要 Bug 修复

- 解决了解析复杂 JSON 字符串时占用 CPU 过多，耗费内存过大的问题。
- 解决了自动代码生成器生成的代码在 encode 字符串数组出错的问题。
- 解决了持久化和 OPC UA 驱动中的一些内存泄漏问题。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
