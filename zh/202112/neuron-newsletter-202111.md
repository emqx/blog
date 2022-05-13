本月，Neuron 团队仍专注于 2.0 版本的开发，对部分功能和单元测试进行了完善，增加了整体的功能测试，并解决了测试发现的 Bug。同时，v2.0-alpha 版本发布正在积极筹备中。

## Neuron 2.0 的功能完善

- 完善了 Webserver 部分的 http 请求接口功能。包括用户的登录和注销，节点的设置、启动和停止，datatag 的增加、删除、订阅和读写功能，group config 的配置更新等。
- 完善了 [MQTT](https://www.emqx.com/zh/mqtt) 的部分的接口功能。包括支持 Webserver 部分的功能接口，有支持节点控制，datatag的增加、删除、修改、查找的功能，支持 datatag 的定语，支持 group config 的配置更新，插件的获取更新。
- 完善了 [Modbus](https://www.emqx.com/zh/blog/building-modbus-based-iiot-app-with-neuron) 驱动的功能和稳定性。数据周期读写功能优化，group config 更新后的订阅关系改变。

## Neuron 2.0 的测试

- 完善了通用数据类型的单元测试，对内存泄漏的问题进行了修复，增加了稳定性。
- 使用 robot 自动测试框架来对 Neuron 进行了完整的功能测试。目前已完成节点、分组数据以及插件相关的功能测试。

## Neuron 2.0 Bug 修复

2.0 版本对以下问题进行了修复：

- 节点控制方面的系统 crash，获取节点信息不够完整的问题。
- group config 订阅有时出错的问题。
- 核心层有时消息转发到不匹配节点的问题。
- 数据传输的序列化时有些数据类型会出错的问题。
- 传递数据时的内存泄漏问题。

## Neuron 1.x 当前状态

在 Neuron 2.0 没有正式商业化应用之前，Neuron 1.x 的功能升级及维护尤为重要。近期我们发布了 v1.3.4，新增了以下功能：

- MQTT json 包里时间戳从10个位扩展到13个位。
- OPC 驱动修复了证书连接 Siemens PLC S71200 时出现「0x00AA0000-非关键超时」问题。
- 修改 UI 界面状态栏中的 SEMI，将其改为 EXPIRED。
- Fins on TCP 驱动数据类型问题修复。
- 限制数据 Log file 的增长过大而影响系统运作。


Neuron 1.x 目前已广泛应用或正在测试到不同行业中，包括船运、油田、半导体等等。Neuron 团队也在基于用户反馈和需求持续完善 Neuron 1.x。v1.4.0 将于近期发布，敬请关注。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
