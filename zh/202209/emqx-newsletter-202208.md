本月，[EMQX](https://www.emqx.com/zh/products/emqx) 发布了 v5.0.5 和 v5.0.6 两个版本，引入配置文件检查支持，提供了能够减少 35% TLS 连接内存占用的配置选项，同时修复了目前已知 Bug。此外，企业版 5.0 的开发工作也在快速推进，将为数据集成带来质的变化，异步、批量、磁盘缓存，这些大家期待已久的功能都会随着企业版 5.0 的正式发布上线。

云服务方面，[EMQX Cloud](https://www.emqx.com/zh/cloud) 本月对认证鉴权搜索及海外站账单页面进行了优化。[EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 也随着 EMQX 5.0 的发布一并进行了相关能力的更新升级，以更好地支持 EMQX 的云原生特性。

## EMQX 

### 企业版 5.0：异步、批量和磁盘缓存

此前的版本中，如果外部资源持续不可用，写入失败的消息将被直接丢弃。为了进一步提升稳定性，在 EMQX Enterprise 5.0 中，我们增加了磁盘缓存机制，一旦外部资源不可用，便会将消息写入缓存，直到资源恢复后重试。而如果缓存的消息量超过了预设的值，便会按照 FIFO 的规则丢弃消息。

在引入对异步的支持后，外部资源的状态将不会再影响 EMQX 的稳定性，也不会再影响正常消息的吞吐流转。当一条消息被多个规则处理时，其中一个规则执行异常、长耗时、抖动，都不会再对其他规则产生影响，最大程度上保证了业务的稳定性。在框架层面实现了对批量的支持，降低了批量的支持难度，提升了支持效率。

目前，EMQX Enterprise 5.0 已经内部迭代了两个 beta 版本，以上功能也基本开发完成，进入了测试阶段。

### 节点疏散和节点重平衡

节点疏散功能允许用户在因维护底层软件或硬件而需要关闭节点之前强制将连接和会话迁移到其他节点，以减少因此带来的会话数据丢失。

而节点重平衡功能则允许连接地从负载较高的节点迁移到负载较低的节点，以降低使集群负载均衡的运维难度。

以上两个功能都将可以通过 HTTP API 来启停以及设置疏散和重平衡的速率。

目前功能代码已经开发完成，我们将在测试完成后于下个月的维护版本中正式上线。

### 4.3 & 4.4 维护版本升级

EMQX 开源版 v4.3.18 & v4.4.7 以及企业版 v4.3.13 & v4.4.7 已经于本月中旬正式发布，除了提供能够减少 35% TLS 连接内存占用的配置选项和允许通过日志查看详细的握手过程来帮助 Debug 等提升 TLS 使用体验的改动以外，主要为 4.3 版本带来了 OTP 版本的升级，以解决 OTP Bug 导致的低概率的随机进程无响应的问题，在这一版本上我们仍然保留了对热升级的支持以便广大用户更好地完成升级。

EMQX 开源版 v4.3.19 & v4.4.8 以及企业版 v4.3.14 & v4.4.8 也将于本月发布，本次版本升级主要聚焦于各项问题修复和一些使用体验上的改进。

更新详情请查看：[《EMQX 4.x 版本更新：Kafka 与 RocketMQ 集成安全增强》](https://www.emqx.com/zh/blog/emqx-v-4-x-released)

### 5.0 产品解读文章与直播

为了方便用户更好地了解 EMQX 5.0 的技术细节和产品价值，EMQX 团队近期陆续推出了 5.0 产品解读系列文章与直播。

八月发布了文章[《基于 RocksDB 实现高可靠、低时延的 MQTT 数据持久化》](https://www.emqx.com/zh/blog/mqtt-persistence-based-on-rocksdb)、[《全新物联网数据集成：Flow 可视化编排 & 双向数据桥接》](https://www.emqx.com/zh/blog/iot-data-integration)、[《灵活多样认证授权，零开发投入保障 IoT 安全》](https://www.emqx.com/zh/blog/securing-the-iot)、[《全新 EMQX Dashborad：易操作、可观测，集群数据尽在掌握》](https://www.emqx.com/zh/blog/an-easy-to-use-and-observable-mqtt-dashboard)。之后我们还将分享 EMQX 5.0 在多协议网关、插件扩展等方面的全新进展，敬请关注后续推送。


## EMQX Cloud

### 认证鉴权搜索优化

对于最新版本创建的部署，控制台中认证以及访问控制部分添加了搜索功能。用户可以根据用户名、客户端 ID、主题在认证和权限控制已经收录的条目中进行搜索，方便精确控制以及管理。

### 海外站账单页面优化

对于海外站的用户，控制台使用了更符合用户习惯的出帐方式，可以更方便地查看到当月的预估账单以及历史已出的账单，并且可以按照账单的维度对未支付账单进行支付。海外用户除了使用信用卡的方式支付进行支付，也支持预付费（充值）的方式，余额将显示为 Available Credits。

![EMQX Cloud 账单](https://assets.emqx.com/images/d7a35fd486ef7a9ae1e17f06c6216700.png)

## EMQX Kubernetes Operator

### EMQX Kubernetes Operator 1.2.4 & 1.2.5 

新增功能如下：

- 支持向 pod 添加额外的容器，用户可以添加 sidecar container 来进行自己的业务处理。
- 支持在 EMQX 自定义资源的 `.spec.emqxTemplate` 中增加 Dashboard 的用户名和密码，用户可以方便设置用户名和密码。
- 如果用户没有在 `.spec.emqxTemplate`中设置 acl，ConfigMap 将不会被创建。对于 EMQX Enterprise，如果用户没有在 `.spec.emqxTemplate`中设置 `modules`，ConfigMap 将不会被创建。方便用户自主选择是否创建 ConfigMap。
- EMQX 自定义资源新增 `.status` 字段，根据这个字段来观察EMQX集群的运行状态。
- 默认不再为 EMQX 日志创建 volume 和 volumeMount，EMQX 日志将默认输出到容器 stdout，如需要写到相应的日志文件可自行配置。
- 为 Headless Service 增加 publishNotReadyAddresses: true，以解决 EMQX 集群可能存在的脑裂问题。

### EMQX Kubernetes Operator 2.0

即将发布的 EMQX Kubernetes Operator 2.0 支持 EMQX 5.0 在 Kubernetes 上部署，相关能力如下 :

- 全新的集群策略

  EMQX Kubernetes Operator 2.0 利用了 Deployment 资源来部署 EMQX Replicant 节点。相比于 Core 节点，Replicant 节点彼此独立，只向 Core 节点发起请求并组成集群，Replicant 节点没有绑定任何持久化的资源，这意味着他们可以随时被销毁和重建。

- 全新的配置格式

  用 EMQX 全新的 HOCON 配置和 Dashboard 的热配置功能，允许用户将原生的 EMQX 配置写入 EMQX 自定义资源中。这些配置都会在整个集群中生效，并且会在新的节点加入集群时将配置同步过去，保证所有节点的一致性。

- 全新的升级管理

  2.0 版本提供了升级管理的能力，当用户想升级 / 降级 EMQX 时，只需要直接修改 EMQX 自定义资源中的 Image，EMQX Kubernetes Operator 就会自动完成所有的工作。

详情可查看：[《EMQX Kubernetes Operator：快速体验 EMQX 5.0 云原生特性》](https://mp.weixin.qq.com/s?__biz=Mzg3NjAyMjM0NQ==&mid=2247490324&idx=1&sn=d1d16d700dac3012a17a6602b93c535e&chksm=cf39c432f84e4d2436f83e2c60340b916ac13a15b20779b969b138cef478046d1fcc453bd5ae#rd)

### 各大云平台**部署指南**

用户在各主流云平台进行 EMQX 集群部署时可参考以下文档：

- [阿里云 ACK 部署文档](https://github.com/emqx/emqx-operator/blob/main/docs/zh_CN/deployment/aliyun-ack-deployment.md)
- [AWS EKS 部署文档](https://github.com/emqx/emqx-operator/blob/main/docs/zh_CN/deployment/aws-eks-deployment.md)
- [Azure AKS 部署文档](https://github.com/emqx/emqx-operator/blob/main/docs/zh_CN/deployment/azure-deployment.md)
- [华为云 CCE 部署文档](https://github.com/emqx/emqx-operator/blob/main/docs/zh_CN/deployment/cce-deployment.md)
- [腾讯云TKE 部署文档](https://github.com/emqx/emqx-operator/blob/main/docs/zh_CN/deployment/tencent-tke-deployment.md)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
