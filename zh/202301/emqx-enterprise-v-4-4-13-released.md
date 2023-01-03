我们很高兴地告诉大家，EMQX Enterprise 4.4.12 以及 4.4.13 版本正式发布！

在本次发布中，我们带来了集群负载重平衡与节点疏散功能为运维人员提供更灵活的集群管理方式，适配了 TDengine 3.0 版本并新增分表批量插入功能，以提供更高的数据集成吞吐。除此之外，我们还修复了多项缺陷。


## 集群负载重平衡与节点疏散

MQTT 作为有状态的长连接接入协议，在生产环境下 EMQX 集群运维不可避免的会遇到一些困难。

一方面，在跨版本升级、垂直或水平扩展时要求关闭 EMQX 节点，这会导致节点上所有连接几乎同时断开并重连，增加了集群过载的风险，与此同时非持久会话也将在节点关闭时丢失。另一方面，长连接一旦建立就不会轻易断开，新加入集群或重新启动的节点会长时间处于负载不足的状态。

为解决以上困难，集群负载重平衡与节点疏散应运而生。

节点疏散功能允许用户在关闭节点之前强制将连接和会话迁移到其他节点，以避免节点关闭带来的会话数据丢失。

启用节点疏散后，当前节点将停止接受 MQTT 新连接，并将所有连接及会话转移到指定节点，在此过程中客户端通过重连或 MQTT 5.0 [Server redirection](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901255) 机制，经历短暂的断开后会迅速连接到新节点。

为确保短时间内的大规模重连导致集群负载过高，EMQX 允许设置疏散速度参数，在可控的范围内平稳地完成这一操作。

集群负载重平衡基于节点疏散，通过手动的方式，控制将部分连接从负载较高的节点疏散到负载较低的节点，从而达成整个集群的负载平衡。

![EMQX 节点疏散流程](https://assets.emqx.com/images/fd6c95358be329cf9bfc2daf2340e74c.png)

<center>节点疏散流程</center>

集群负载重平衡与节点疏散能够确保所有节点以良好的负载工作，并大大降低 EMQX 维护工作对在线客户端以及客户业务的影响，详细的使用方式请参阅 [EMQX 文档](https://docs.emqx.com/zh/enterprise/v4.4/advanced/rebalancing.html)，目前这一功能已经被整合至 [EMQX Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 中以为 EMQX 的 K8s 自动化部署带来更好的使用体验。


## TDengine 3.0 适配以及子表批量插入

TDengine 3.0 带来了大量的架构重构和功能新增，提供了更好的性能和更多灵活易用的功能。在 TDengine 3.0 中，EMQX 依赖的数据写入接口也做了相应的调整导致无法正确写入数据。

本次发布我们对这一变更进行了无缝适配，现有的规则与资源无需修改即可支持 TDengine 3.0 版本。

在版本适配的同时，我们还加入了 [TDengine 子表](https://docs.taosdata.com/concept/#子表subtable) 批量插入能力，通过批量机制提供更高的吞吐性能，性能测试数据表明，预先创建好子表的情况下，单个 EMQX 节点可以支持每秒 10 万 QoS 1、Payload 100B 的消息写入 TDengine。


## BUG 修复

以下是主要 BUG 修复，完整 BUG 修复列表请参考 [EMQX 企业版 4.4.12 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.12)、[EMQX 企业版 4.4.13 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.13)。

- 修复 GCP PubSub 集成测试连接时可能的内存泄露以及 JWT 令牌二次刷新问题。
- 为修复 Kafka 集成的连接问题，为 Kafka 资源 SSL 连接配置增加 `SNI` 字段，能够方便的连接到诸如 Confluent Cloud 等启用了 TLS 且集群部署的 Kafka 资源中。
- 修复备份配置下载时错误，以及导入时不会在集群所有节点上生效的问题。
- 修复 RocketMQ 认证失败问题，该错误导致 EMQX 无法连接到由阿里云提供的 RocketMQ 服务。
- 为 Kafka 与 Pulsar 动作参数添加检查，确保 Segment Bytes 不会超过 Max Bytes。
- 修复 Dashboard 用户验证问题，通过 Dashboard 创建用户时，要求密码格式为字母、数字、中划线与下划线，必须以字母或数字开头(`^[A-Za-z0-9]+[A-Za-z0-9-_]*$`）。
- 持久会话的 MQTT 客户端重新连接 EMQX 之后，未确认的 QoS1/QoS2 消息不再周期性重发，该行为符合协议规范。
  在此之前由 `znone.<zone-name>.retry_interval` 配置指定该消息的重发间隔(默认为 30s)，但当持久会话的 MQTT 客户端重新连接 EMQX 之后，EMQX 只会将队列中缓存的未被确认的消息重发一次而不是按配置的时间间隔重试。
- 修复持久会话的 MQTT 客户端断开连接之后，已经过期的 `awaiting_rel` 队列不会清除问题。
  在这个改动之前，在客户端重连并且发布 QoS2 消息的时候，如果 `awaiting_rel` 队列已满，此客户端会被服务器以 `RC_RECEIVE_MAXIMUM_EXCEEDED(0x93)` 错误码断开连接，即使这时候 `awaiting_rel` 队列里面的报文 ID 已经过期了。





<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
