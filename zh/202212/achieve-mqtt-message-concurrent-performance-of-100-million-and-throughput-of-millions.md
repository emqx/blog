随着物联网技术的发展与各行业数字化进程的推进，全球物联网设备连接规模与日俱增。一个可靠高效的物联网系统需要具备高并发、大吞吐、低时延的数据处理能力，支撑海量物联网数据的接入与分析，从而进一步挖掘数据价值。

于今年五月发布的 [EMQX 5.0 版本全球首个实现了单集群 1 亿并发连接支持](https://www.emqx.com/zh/blog/emqx-v-5-0-released)，成为目前世界上最具扩展性的物联网 MQTT 消息服务器。基于 EMQX 这一强大的性能突破，近日，EMQ 与阿里云旗下飞天洛神云网络展开合作，与 NLB 产品合作构建了新一代支持「亿级并发、千万级吞吐」的物联网消息服务系统。

>**飞天洛神云网络打造的 NLB 网络型负载均衡**
>
>NLB 网络型负载均衡是阿里云飞天洛神云网络面向万物互联时代推出的全新一代高性能四层负载均衡，支持超高性能和自动弹性能力，用户无需指定或手动调整 NLB 的实例规格，实例性能会随着业务增减自动弹性伸缩，同时采用多层次容灾架构设计保障实例的可用性，为用户在端连接云时更好地做负载均衡和应用的分发，保障网络的极致弹性，助力用户轻松构建高并发、高安全的物联网平台及应用。
>
>NLB 网络型负载均衡在物联网领域主要应用于车联网、智能家居、智能停车、视频监控等业务场景中，NLB 作为业务入口可以同时处理海量并发连接，同时提供 TCPSSL 卸载、连接限速等能力保障物联网业务安全稳定运行。


## 「1 亿并发、100 Gbps 吞吐」核心性能测试

通过大规模分布式物联网 MQTT 消息服务器 EMQX 的 1 亿连接支持能力，EMQ 助力阿里云验证了飞天洛神云网络 NLB 网络型负载均衡单实例可支持超 1 亿并发连接和超 100 Gbps 吞吐的核心性能指标。

测试详情如下：

### 测试场景

1. 测试 1 亿平稳连接，无订阅发布消息。
2. 测试 QoS 0 下最大的发布接收消息速率。

### 测试准备

本次测试使用 EMQX 开源版 v5.0.8 构建了一个由 3 个 Core 节点和 36 个 Replicant 节点组成的集群，然后将 36 台部署了性能测试工具 `emqtt_bench` 的客户端通过阿里云负载均衡 NLB 接入 EMQX 集群中的 36 个 Replicant 节点进行测试。

![测试架构图](https://assets.emqx.com/images/8fbd62951fde5575fc96fda194dc900d.png)

测试环境为阿里云-德国（法兰克福）区。

机器配置如下：

| **服务**   | **CPU** | **Memory** | **数量** | **备注**     |
| :--------- | :------ | :--------- | :------- | :----------- |
| EMQX 集群  | 32核    | 128G       | 39       | g5ne.x8large |
| 压力机     | 32核    | 128G       | 36       | g5ne.x8large |
| 阿里云 NLB |         |            |          |              |

### 测试结果

1. 下图展示了 EMQX 客户端以 1000*36=36000/s 的速度新增连接，直到客户端数据到达 1 亿左右。

   ![亿级 MQTT 连接](https://assets.emqx.com/images/fd49580cfe570a41c0bccde7408f4f6d.png)

2. 共有 1 亿 80 万连接客户端，其中 5040 万客户端负责订阅，5040 万客户端负责发布。所有发布客户端与订阅客户端均由一个阿里云 NLB 连接到同一个 EMQX 集群。集群中，最大消息并发 1000 万/s，发布的报文大小平均为 400 byte。

   ![千万级 MQTT 消息并发](https://assets.emqx.com/images/49d6bfe8579e0bb832928029233e73ff.png)

   ![MQTT 消息并发测试](https://assets.emqx.com/images/4a4a26dfd2cc24070a5d9311727ea40a.png)

3. 在 EMQX 集群一订阅端和一发布端的测试中，总共约 16000 对测试同时进行，每秒每个客户端发布的包平均为 1M，NLB 总计可稳定支持 160G BPS。

![MQTT 性能测试结果 1](https://assets.emqx.com/images/6029c80d99c14ee797ee630116851f3e.png)

![MQTT 性能测试结果 2](https://assets.emqx.com/images/9e677a12511fd4ee89a90a1875452308.png)

![MQTT 性能测试结果 3](https://assets.emqx.com/images/d77f7eeaa3cc073732ee84b9a03cbfe6.png)

这意味着只需要购买一个 NLB 实例、部署一个 EMQX 集群就可以满足亿级设备并发管理的需求，支撑数据业务的平滑扩张，为后续业务的发展垫定坚实基础。这也为飞天洛神云网络 NLB 在车联网、[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)等高规格物联网应用场景提供了可靠的技术验证。


## 未来展望

未来，EMQ 与阿里云飞天洛神云网络将在物联网领域继续深入合作，为更多物联网场景打造高连接、高吞吐、高并发、低延时的解决方案，让更多的物联网用户不用在并发连接、吞吐上走弯路，实现开箱即用，轻松完成「一亿连接」目标。

EMQ 也在与阿里云相关团队合作探索车联网、工业、能源等重点领域的标准解决方案，并积极推进在国内外相关项目中的落地实践，敬请期待。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
