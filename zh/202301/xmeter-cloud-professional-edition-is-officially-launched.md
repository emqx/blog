去年 8 月，EMQ 正式在全球市场推出了最简单、快速的 MQTT 负载和场景测试云服务——XMeter Cloud，用户无需部署即可进行 MQTT 测试，以更低的测试成本轻松打造具有竞争力的可靠物联网平台与应用。经过近半年的打磨，**近日，更强大的 XMeter Cloud 专业版正式上线**。专业版对性能和功能进行了全面升级，支持私有网络测试以及更高连接数和消息吞吐量，非常适合企业级大规模物联网测试场景。

## 升级特性应对物联网测试挑战

随着物联网场景的全面普及落地，很多物联网应用上线前都需要进行全面的性能测试验证，全面评估系统的负载能力，验证系统的稳定性和可靠性，以便上线后灵活应对不同负载下的场景，保障用户体验。

作为全球首个物联网 MQTT 负载测试云服务，XMeter Cloud 支持千万量级 MQTT 模拟连接与消息吞吐性能测试，并可为 IoT 应用扩展更丰富的测试场景与协议支持。最新发布的专业版则在此基础上进行了进一步特性升级，帮助企业客户应对物联网测试中所面临的挑战。

### 支持私网测试，保障数据安全

物联网是以数据为中心的，所有连接设备/系统都基于可用的数据进行交互。数据在设备间进行交互的过程中存在被非法第三方获取的风险，因此我们需要确保数据受到加密或保护。

XMeter Cloud 专业版支持基于 VPC 对等连接的私有网络测试。完成与 XMeter Cloud 的 VPC 对等连接设置后，用户即可使用该对等连接来使用内网地址进行测试，不仅可以降低网络时延、减轻带宽费用负担，同时因为不必将测试环境暴露在公网环境下，可以有效保障测试数据的安全性。

### 海量连接和吞吐支持企业级大规模场景

无论什么系统，都需要确保其具有足够的可伸缩性，因此性能测试就变得十分必要。而大规模接入及大量消息吞吐场景，对测试工具的性能支持无疑是一个巨大的挑战。

XMeter Cloud 专业版目前可轻松支持 50w 测试连接量和 50w 消息吞吐量无限制，并严格保证测试质量，帮助用户轻松应对企业级规模的性能测试。

> 如有更高测试量需求，可通过 [xmeter@emqx.io](mailto:xmeter@emqx.io) 与我们联系。

## 多规格云服务，轻松按需测试

除了上述专业版的独有升级特性，XMeter Cloud 还提供以下优势能力，帮助用户应对不同测试场景需求。

### 全托管免除运维负担

XMeter Cloud 提供全托管的测试服务，一键提交测试，无需繁琐的手动部署即可自动在云上按需创建测试资源。同时可根据测试周期自动管理与释放资源，免除运维负担，极大节省时间和人力成本。

### 继承 JMeter 优势特性

XMeter Cloud 基于 Apache JMeter 开源项目，完全兼容 JMeter 测试脚本，在充分继承 JMeter 高度可扩展、多种应用及协议支持、跨平台等优势特性的基础上，进一步改善了 JMeter 在测试规模方面的瓶颈，帮助用户根据需求创建更加灵活复杂的测试场景。

### 多协议兼容

XMeter Cloud 专为物联网应用设计开发，100% 支持 MQTT 协议，同时支持 CoAP、LwM2M 等多种物联网协议以及自定义扩展协议的测试，架构复杂的物联网系统也能轻松完成测试。

![XMeter Cloud 基础版与专业版对比](https://assets.emqx.com/images/9bdf542cc0b294a63dc37dc4b1b8338b.png)

<center>XMeter Cloud 基础版与专业版对比</center>

## XMeter Cloud 专业版使用指引

您可以通过以下方式联系我们开通专业版服务，我们会在第一时间处理您的申请。

- 400 电话：400-696-5502
- 邮箱：xmeter@emqx.io

![XMeter Cloud 专业版](https://assets.emqx.com/images/2622238b8400e8889a8d798c362afbe4.png)

开通完成后，在正式开始测试之前您需要根据您的测试需求购买资源包。

测试规模不同，测试所使用的测试机资源也不同。专业版使用 VUM（ VU * M，VU 表示连接数，M 表示测试实际运行时间，单位为分钟）作为衡量测试资源消耗的单位，并根据 VUM 计算测试费用。

> 更多关于测试包的相关事项可参考：[https://docs.emqx.com/zh/xmeter-cloud/latest/features/test_packs.html](https://docs.emqx.com/zh/xmeter-cloud/latest/features/test_packs.html) 
>
> 测试包仅用于涵盖测试相关的基础资源费用，不包括公网测试产生的流量部分。如果您通过公网进行测试，需要购买流量包抵用或使用余额抵扣流量消费。关于流量包的购买事项可参考：[https://docs.emqx.com/zh/xmeter-cloud/latest/features/traffic_packs.html](https://docs.emqx.com/zh/xmeter-cloud/latest/features/traffic_packs.html) 

之后完成测试基础设置及场景设置，即可提交测试。测试完成后，您可以通过测试报告查看关键指标，快速分析系统性能状况。

> 有关测试配置的详细操作请参考：[https://docs.emqx.com/zh/xmeter-cloud/latest/quick_start/mqtt_test.html](https://docs.emqx.com/zh/xmeter-cloud/latest/quick_start/mqtt_test.html) 
>
> 请注意专业版测试中基础配置项包含发压区域，发压区域是指，若您创建了 VPC 对等连接，您的 VPC 所属区域将会显示在这里供选择，以便您进行私网测试。

XMeter Cloud 基础版支持升级专业版。若您正在使用基础版，可以联系我们进行规格升级，升级后我们将赠送您 1 G 免费流量包用于测试。

若您有其他定制化测试需求，欢迎[联系我们](https://www.emqx.com/zh/contact?product=xmeter)，我们会有专业的技术人员帮助您进行测试场景搭建。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>
