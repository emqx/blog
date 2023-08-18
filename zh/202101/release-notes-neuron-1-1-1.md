为解决工业领域数据接入上云过程中所面临的协议繁杂、设备异构化等问题，2020 年 9 月， [物联网边缘工业协议网关软件 EMQX Neuron](https://www.emqx.com/zh/products/neuron) （以下简称 Neuron ）正式发布。

Neuron 提供了通过对各种工业协议转换实现设备端的数据采集、运行业务逻辑服务、警报判定，并将数据及警报上传及存储到云平台。再通过 Web 服务等部署和客户端应用软件，实现设备远程监控、远程维护、设备绩效管理、设备和资产管理等功能。

Neuron 工业网关南向支持接入主流的[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)协议（驱动协议详细列表可参考 EMQ 官网），以及支持自定义协议的扩展。 北向支持通过 [MQTT](https://www.emqx.com/zh/mqtt-guide)、WebSocket 和 HTTP 协议与云平台层进行交互，实现设备上云与云端控制的能力。


## 新功能概览

Neuron V1.1.1 增加了南北协议报文显示，让用户可随时透过 dashboard 观看协议报文，追踪及分析报文内容。

北向 MQTT 协议报文：

![webwxgetmsgimg.jpg](https://assets.emqx.com/images/a0cc294f21ad9e9c678f1818fa0599f2.jpg)

南向 [Modbus](https://www.emqx.com/zh/blog/building-modbus-based-iiot-app-with-neuron) 协议报文：

![webwxgetmsgimg 1.jpg](https://assets.emqx.com/images/5a5d14f99c38bf37b573746faf61ba0b.jpg)

此外，新版本还增加了日志追踪，能让用户了解当前 Neuron 的运行状况。

![webwxgetmsgimg 2.jpg](https://assets.emqx.com/images/4421afbbb936c191e3cb63a2488c81a2.jpg)

## 功能及问题修复

- 修复 TTY 驱动参数配置问题；
- 修复读写驱动设备字节长度不匹配的问题；
- 修复北向协议选择列表，增加 RS232 驱动支持；
- 修改过期时间计算方式；
- 修复内存申请失败的错误；
- 增加支持运行日志等级选择；
- 压缩交互 JSON 数据；
- 删除非必要日志文件；
- 修改 Neuron 脚本引擎支持直接使用对象和属性;


## 联系

如果对 Neuron 有任何问题，请随时通过 [neuron@emqx.io](mailto:neuron@emqx.io) 联系。

作为新基建的重要组成部分，工业互联网已成为一个备受关注的热点领域。为了响应「中国制造 2025」及「工业 4.0」，越来越多的工业企业开始谋求数字化、智能化转型，工业设备上云也因此成为企业转型之路上必须面对的挑战。EMQ 于去年 10 月正式发布的 **云边一体化解决方案**，可以实现异构设备连接及数据汇聚，完成后续边缘或云端计算，以云边协同的方式帮助领域内相关企业快速实现工业互联网架构下边缘层的功能。作为该方案重要组成部分的 Neuron，也将在未来持续为边缘工业互联网提供功能价值。


<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a >
</section>
