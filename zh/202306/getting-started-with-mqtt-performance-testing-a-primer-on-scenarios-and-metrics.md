## 引言

在物联网领域，存在大量资源受限的传感器和工业控制设备运行在低带宽且不稳定的网络环境中，这使得 MQTT 成为物联网场景下理想的消息传输协议。因此，MQTT Broker 必须保证优异的性能和高度的可靠性，以满足物联网应用的要求。

在进行系统测试之前，了解基本的测试场景和性能指标至关重要。在本文中，我们将根据 EMQX 团队的测试经验提供一份详尽的说明，它也同样适用于其他 MQTT Broker 测试。

> **名词解释**
>
> MQTT 协议：MQTT（Message Queuing Telemetry Transport）是一种基于发布/订阅模式的轻量级消息传输协议。尽管其名称中包含"消息队列"一词，但它与消息队列并无关联。该协议因其简洁、灵活、易于实现、支持 QoS 以及消息体积小等特点而成为物联网领域的首选协议。更多信息请参考 [MQTT 教程：从入门到精通](https://www.emqx.com/zh/mqtt-guide)。
>
> 性能测试：性能测试是指利用测试工具模拟各种正常、峰值或异常负载条件，以评估被测试系统在各种性能指标上的表现。其目的在于验证系统是否能够满足用户的期望，并发现系统中存在的性能瓶颈和问题。

## 常见的 MQTT 测试场景

MQTT Broker 主要有两种测试场景：

- 并发连接，包括并发连接数和连接速率。
- 消息吞吐，包括消息发送和接收的吞吐量，以及一些影响生产环境系统性能的因素，如 [QoS](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)、有效载荷大小、[主题通配符](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)等。

在设计具体的性能测试场景时，特别是在进行 PoC 或部署前测试时，必须始终注意以下两点：

- 尽量模拟真实生产环境中的使用情况。
- 覆盖可能的峰值负载。

测试场景可以按照连接和消息吞吐量两个基本维度进行划分。

### 并发连接测试

MQTT 连接是一种基于 TCP 的长连接。客户端首先与 MQTT Broker 建立 TCP 连接，然后发送 MQTT 登录请求。连接成功建立后，客户端和 MQTT Broker 通过定期发送心跳包来维持连接状态。所以建立和长期维持一个MQTT连接是需要占用MQTT broker一定资源的，在高并发场景下，这种长连接会消耗 Broker 的大量资源。因此，通过性能测试，我们可以评估 MQTT Broker 在有限资源下能够承受多少并发连接。

另外，连接速率（即每秒新增连接数）越高，需要的计算资源越多，在制定测试场景时需要考虑这个因素，因为在有些场景下大量的设备会同时上线，在测试broker的能力或规划系统容量时需要这个指标。

在并发连接测试中还要考虑是否使用 TLS/SSL 加密传输，因为它会增加压力机和MQTT Broker额外的资源开销。在计划测试时，需要评估它对性能的影响。

综上所述，在 MQTT 并发连接测试中，应该考虑以下三种场景：

1. 在固定的较低连接速率下逐步提高并发连接数，测试系统响应和资源消耗情况。这可以确定系统在给定的硬件和网络资源下能够承受的最大并发数。
2. 在给定的并发连接数下，测试不同连接速率下系统的响应和资源消耗情况。
3. 在设计 1) 和 2) 时，区分普通 TCP 连接和 TLS/SSL 加密连接。

### 消息吞吐量测试

如前文所述，MQTT 是一种基于[发布/订阅模式](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)的消息传输协议，它是一种异步协议，实现了发布-订阅 1对1，1对多，多对1这3种类型，广泛应用于各种物联网场景。因此，消息吞吐量测试应该涵盖以下三种场景：

1. 1 对 1：发布者和订阅者的数量相等。对于每个发布者，有唯一一个订阅者订阅其发布的主题。也就是说，MQTT Broker 的消息流入速率与流出速率相同。
2. 多对1（上报）：一种典型的物联网应用场景，有大量物联网设备作为发布者，但只有少数或单个订阅者，例如大量设备上报其状态或数据。
3. 1对多：即广播模式，少量客户端发布消息，大量设备端订阅消费消息，如控制端指令下发。

另外，在设计消息吞吐量场景时，不要忽略 QoS、消息有效载荷大小、带通配符的订阅主题等因素。不同的 QoS 对负载测试的性能和资源消耗有很大影响。有效载荷大小可以根据实际使用情况确定。

### 其它场景

对于其它 MQTT 功能，如共享订阅、消息转存到数据库或其他消息队列（MQ）、海量主题订阅，以及诸如众多 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)同时连接/断开等极端情况，可以根据实际需求进行设计并加入测试场景中。

## 性能度量指标

在设计好测试场景之后，还要制定度量指标来评估测试的成功与否。

在性能测试中，指标一般可以分为两大类：应用系统指标（比如 MQTT Broker 的指标）和计算资源指标。

- 应用系统指标与用户场景和需求有关，例如响应时间（或延迟）、并发量等。
- 计算资源指标与硬件资源消耗有关。对于我们讨论的 MQTT 测试来说，这些指标与其它软件性能测试的指标相似，例如 CPU、内存、网络、磁盘 I/O。

MQTT 系统指标与测试场景紧密相关，常见的指标如下表所示。

![MQTT 系统指标](https://assets.emqx.com/images/75d57d0f6b8ed1ebc0fc12f69bc85f9a.png)

## 性能测试工具

大规模性能测试需要能够快速、真实、稳定地模拟高并发、高吞吐场景，同时需要管理和维护众多机器和资源，选择合适的测试工具可以起到事半功倍的效果。

EMQX 团队使用的是 emqtt_bench 和 XMeter 这两款性能测试工具。

### emqtt_bench

emqtt_bench 是 EMQX 研发团队基于 Erlang 编写的一款 MQTT 协议性能测试工具。安装完成后，可以通过命令行来使用。

```
用法：emqtt_bench pub | sub | conn
```

与其它工具相比，emqtt_bench 的优点是安装和使用简单，占用的计算资源较少。但它支持的场景比较有限，需要结合其他监控工具测试指标数据

> 具体安装和使用方法请参考 [https://github.com/emqx/emqtt-bench](https://github.com/emqx/emqtt-bench) 

### XMeter

emqtt_bench 适用于开发阶段的快速性能验证。如果要进行大规模测试或正式测试，我们推荐另一款更专业的性能和负载测试工具 - [XMeter](https://www.emqx.com/zh/products/xmeter)。

XMeter 是一款基于 JMeter 的性能测试工具，它对JMeter的架构进行了改造，达到了完全水平扩展的能力。能够轻松处理大量数据并执行高频测试。XMeter不仅继承了 JMeter 的强大功能，还增加了许多新的特性。在测试过程中，提供丰富而实时的测试报告，让测试人员能够随时查看 MQTT 的关键性能指标，如吞吐量、响应时间和成功率等。同时XMeter 内置了监控系统，可以实时监测 MQTT Broker 的资源消耗情况。

此外，XMeter 还提供了自动化和集中化的测试资源管理能力。测试机器（容器）在测试开始时自动创建，在测试结束时自动销毁。

在整个测试阶段，XMeter 将以图形方式实时显示 MQTT 性能指标和计算资源使用情况，如图1～图5所示。

![图1 XMeter报告 - 汇总信息和趋势图](https://assets.emqx.com/images/2f73099734b1d09a90799def40235ee4.png)

<center>图1 XMeter报告 - 汇总信息和趋势图</center>

![XMeter报告-测试数据明细（按页面统计）](https://assets.emqx.com/images/74a149f2e19bbb3706ea220c85245592.png)

<center>图2 XMeter报告-测试数据明细（按页面统计）</center>

![XMeter报告 - 被测监控](https://assets.emqx.com/images/80559bc15d2c725246114df0210c407f.png)

<center>图 3 XMeter报告 - 被测监控</center>

![XMeter报告 - 测试信息](https://assets.emqx.com/images/5a49f0248e2d268226c1ff385e96f755.png)

<center>图 4 XMeter报告 - 测试信息</center>

![XMeter report - Test machine monitoring](https://assets.emqx.com/images/2dd7129ed48bda92ae05c37dde3283d2.png)

<center>图 5 XMeter 报告 - Test machine monitoring</center>

 

**XMeter 使用指南**

XMeter 有两个版本可供选择。

- XMeter 本地私有化部署。适合需要对测试环境进行全面控制，并遵守严格安全和数据隐私规定的企业。使用该版本您需要：

  - 从 [GitHub - emqx/mqtt-jmeter: MQTT JMeter Plugin](https://github.com/emqx/mqtt-jmeter) 下载 XMeter 团队开发并开源的 mqtt-jmeter 插件。

  - 将 jar 文件放入 JMeter 目录中。

  - 根据应用场景，在 JMeter 中编写测试脚本，如图 6 所示。

  - 将脚本上传到 XMeter 并开始对 MQTT 进行性能测试。

    ![图 6 用于 MQTT 测试的 JMeter 测试脚本](https://assets.emqx.com/images/7563e56063d748846bbb7adf580802e0.png)

<center>图 6 用于 MQTT 测试的 JMeter 测试脚本</center>

- [XMeter Cloud](https://xmeter-cloud.emqx.com/)：全托管的MQTT负载测试云服务，简单易用：
  - 一键发起 MQTT 性能测试，无需手动部署测试资源
  - 仅需 3 步完成 MQTT 测试配置，免除编写场景脚本的负担
  - 测试资源云上按需创建，测试环境高度自动化，节省大量时间和人力成本

您只需在我们的[网站](https://xmeter-cloud.emqx.com/)上注册一个免费试用账号，然后按照[此文档](https://docs.emqx.com/en/xmeter-cloud/latest/)的指引，即可开启您的 XMeter 之旅。

## 总结

在本文中，我们讨论了几种常见的测试场景和用来评估 MQTT Broker 性能的关键指标。通过理解和应用这些测试技术和指标，您可以优化 MQTT 系统性能和可靠性，提升物联网和消息传输基础设施的整体水平。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html%23%2Fproducts" class="button is-gradient px-5">开始试用 →</a>
</section>
