本月 [EMQX 开源版](https://github.com/emqx/emqx)和企业版对稳定性和部分功能进行了优化提升，同时提供了 TDengine 的新版本适配，帮助用户基于 EMQX 拓展更多可能。

云服务方面，EMQX Cloud 数据集成新增支持 Google Pub/Sub，为使用 GCP 其他数据服务的用户提供了便利。此外，EMQX Operator 2.1 即将发布，通过 EMQX 节点疏散能力在 Kubernetes 上实现了可控、平滑的优雅升级。


## EMQX

12 月 EMQX 开源版发布了 [v5.0.12](https://github.com/emqx/emqx/releases/tag/v5.0.12)，更新了 Dashboard [1.1.3](https://github.com/emqx/emqx-dashboard-web-new/releases/tag/v1.1.3) 版本，[v4.4.12](https://github.com/emqx/emqx/releases/tag/v4.4.12) 即将发布。企业版即将发布 v4.3.18 以及 v4.4.12，提供集群负载重平衡与节点疏散、TDengine 3.0 适配、字表批量插入等多个新功能。

同时，我们在 v4.4 以及 v5.0 中提供了适用于 Apple M1/M2（macOS-12）以及 Amazon Linux 2 的软件包。

### 集群负载重平衡与节点疏散

集群负载重平衡与节点疏散包含在企业版 v4.4.12 中，它允许用户在集群负载不平衡时重新分配每个节点的连接，亦或是因维护关闭节点之前强制将连接和会话迁移到其他节点，以避免因此带来的会话数据丢失。

启用节点疏散后，当前节点将停止接受 MQTT 新连接，并将所有连接及会话转移到指定节点，在此过程中客户端通过重连机制，经历短暂的断开后会迅速连接到新节点，绝大多数 MQTT 客户端库都实现了这一机制。

节点重平衡可以看做是不完全的节点疏散，它允许将部分连接从负载较高的节点迁移到负载较低的节点时间集群负载均衡。

为避免短时间内的大规模重连导致 EMQX 负载过高，EMQX 支持参数化地设置疏散速度，以确保这一过程平稳地进行。

集群负载重平衡与节点疏散提供了灵活可控的运维实践，能够大大降低 EMQX 负载状态不均衡以及维护工作对业务的影响，详细的使用方式请参阅 [EMQX 文档](https://docs.emqx.com/zh/enterprise/v4.4/advanced/rebalancing.html)，目前这一功能已经被整合至 [EMQX Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 中以为 EMQX 的 K8s 自动化部署带来更好的使用体验。

### TDengine 3.0 适配以及子表批量插入

TDengine 3.0 进行了大量的架构重构和功能新增，提供了更好的性能和更多灵活易用的功能。在该版本中，EMQX 依赖的数据写入接口发生了一些不兼容的变化导致 EMQX 无法继续正确写入数据。

本次发布我们对这一变更进行了无缝适配，您无需修改规则引擎即可升级到 TDengine 3.0 版本。

在版本适配的同时，我们还加入了 [TDengine 子表](https://docs.taosdata.com/concept/#子表subtable)批量插入能力，您可以借助批量机制实现更高的吞吐性能，经测试 EMQX 单节点上可以达到每秒 10 万的插入速度。

### 功能增强

- 提高了 EMQX 5.0 中保留消息写入性能。
- 在 EMQX 5.0 中增加禁用全局 GC 的配置项 `node.global_gc_interval = disabled`，禁用后可以提高消息吞吐，避免海量连接下因全局 GC 对业务产生波动，但相应地内存占用会更高。
- 在 EMQX 5.0 中删除非标准共享订阅主题前缀 `$queue` 的支持，共享订阅现在是 MQTT 规范的一部分。改用 `$share` 前缀。
- 重构了 MQTT 5.0 数据集成 MQTT Bridge，现在您可以在一个 MQTT Bridge 中实现消息的流入（ingress）和流出（egress）桥接。
- 为主题重写模块增加主题合法性检查，带有通配符的目标主题不允许被创建。
- 在 EMQX 4.3 中增加对 Kafka 资源配置字段的合法性检查，避免创建时传入错误的字符串导致运行时出现错误。

### 问题修复

我们修复了多个已知 BUG，包括潜在的 MQTT 数据包解析错误、RocketMQ 集成认证功能无法正常工作、已过期 `awaiting_rel` 队列不会清除以及备份数据无法正确导入导出的问题。


## EMQX Cloud

### 数据集成支持 Google Pub/Sub

[Google Cloud Pub/Sub](https://cloud.google.com/pubsub) 是一种异步消息传递服务，旨在实现极高的可靠性和可扩缩性。

现在，您可以通过 EMQX Cloud 规则引擎的 GCP Pub/Sub 集成能力，快速建立与该服务的连接，基于 GCP 构建物联网应用：

- **使用 Google 的流式分析处理物联网数据**：以 Pub/Sub 以及 Dataflow 和 BigQuery 为基础而构建整体解决方案，实时提取、处理和分析源源不断的 MQTT 数据，基于物联网数据发掘更多业务价值。
- **异步微服务集成：**将 Pub/Sub 作为消息传递中间件，通过 pull 的方式与后台业务集成；也可以推送订阅到 Google Cloud 各类服务如 Cloud Functions、App Engine、Cloud Run 或者 Kubernetes Engine 或 Compute Engine 上的自定义环境中。

在数据集成页面中选择 GCP PubSub 即可打通 EMQX Cloud 连接到 GCP 的通道。

![EMQX Cloud 数据集成支持 Google Pub/Sub](https://assets.emqx.com/images/cdf63d1dcd3acbb135aea14428094573.png)


## EMQX Kubernetes Operator

### EMQX Operator 2.1 即将发布

该版本适配了 EMQX 4.4.12 中的节点疏散功能，借助该能力，EMQX Operator 在 Kubernetes 上实现了优雅升级，为用户带来如下便利：

- 在新的升级方案里，升级过程中客户端仅需断连一次（在之前的方案中连接可能会中断多次）。
- 借助 EMQX 的节点疏散能力，在升级过程中实现连接可控迁移（控制连接断开速率与迁移速率）。
- 通过减少连接中断次数与可控连接速率迁移，能够有效防保障服务端在整个升级过程中的平滑、稳定运行，防止过载。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
