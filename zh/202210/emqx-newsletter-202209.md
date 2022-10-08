本月，EMQX 5.0 保持稳定更新，目前最新版本已经来到了 5.0.8，在修复目前已知 Bug 的同时，我们也专注于加强性能和改进功能体验。企业版 4.3 & 4.4 发布了最新的维护版本，修复了多项已知问题，稳定性进一步提升。

云服务方面，EMQX Cloud 新增了 1000 连接规格的专业版部署，方便更多用户享受专业版高级功能。

## EMQX

### EMQX 5.0 持续优化

在本月发布的两个版本中，我们改进了节点间共享订阅消息的派发方式，从使用 Erlang distribution 的 RPC 改为独立的 RPC 实现，这将有效减小共享订阅负载较高时 Mnesia 集群事务的执行压力。我们为 ExProto 到 gRPC Server 的发送流增加了对批量操作的支持，使其吞吐性能也得到了一定程度的提升。此外，我们通过简化 TLS 密码套件的配置以及统一 Dashboard 上 TLS 的配置方式，提升了 TLS 的使用体验。

更多功能改动与问题修复的说明，可查看：[https://github.com/emqx/emqx/releases](https://github.com/emqx/emqx/releases)  。

### 4.3 & 4.4 维护版本升级

目前，EMQX 与 EMQX Enterprise 的最新稳定版本已经分别来到了 EMQX 4.3.20 & 4.4.9 以及 EMQX Enterprise 4.3.15 & 4.4.9，这是一次常规升级，以各项问题修复为主，完整修复列表见：[https://www.emqx.com/zh/changelogs/enterprise/4.4.9](https://www.emqx.com/zh/changelogs/enterprise/4.4.9) 。

### 产品解读系列专题完结

为了方便用户更好地了解 EMQX 5.0 的技术细节和产品价值，自 EMQX 5.0 发布，EMQX 团队陆续推出了 5.0 产品解读系列文章与直播。

九月我们发布了文章 [《EMQX 5.0 全新网关框架：轻松实现多协议接入》](https://www.emqx.com/zh/blog/emqx-connects-multiple-iot-protocols)、[《如何保障物联网平台的安全性与健壮性》](https://www.emqx.com/zh/blog/how-to-ensure-the-security-of-the-iot-platform)、[《易操作、可观测、可扩展，EMQX 如何简化物联网应用开发》](https://www.emqx.com/zh/blog/how-emqx-simplifies-iot-development)。至此，EMQX 5.0 产品解读系列暂时告一段落。相应的直播回放可查看：[EMQX 5.0 底层架构解析：如何实现单集群 1 亿 MQTT 连接](https://www.bilibili.com/video/BV1zd4y1S7cE/?spm_id_from=333.788&vd_source=4fd86b93f679c12a9be2003a40a8b1f0) 

## EMQX Cloud

### 新增 1000 连接规格的专业版部署

针对对专业版高级功能有需求但是连接设备数并没有很多的用户，我们上线了 1000 连接的规格，同时 TPS 的限制为 1000，降低了用户使用 EMQX Cloud 专业版的门槛。此外，专业版提供的试用规格也从 5000 连接变为 1000 连接。1000 连接专业版的部署国内价格为 ¥1.28/小时，海外部署价格为 $0.36/小时。

### 小时账单显示优化

现在用户可以在【财务管理】-【概览】-【小时账单】中看到每一种类型的服务所结算的账单，轻松查询服务费用和流量产生的费用。

![MQTT Cloud](https://assets.emqx.com/images/03a46e7d8f5b833f9c0a0e2114181ec7.png)

### 影子服务优化

优化了影子服务数据统计，去除了系统默认调用量的统计和显示，同时也进一步提升了服务调用 QPS（Query Per Second）的上限，以应对更高要求的场景。

关于影子服务的详细内容可查看：[开箱即用的数据缓存服务｜EMQX Cloud 影子服务应用场景解析](https://www.emqx.com/zh/blog/emqx-cloud-shadow-service-application-scenario)

## EMQX Kubernetes Operator

### 高级运维特性预研

本月我们对 EMQX 在生产环境中一些高级运维特性做了相关预研工作，目前已有基本方案。主要包括以下内容:

- 在 Kubernetes 中热更新与 patch
- 在升级过程中减少端重连以及连接可控迁移
- 在 Kubernetes 中的伸缩能力

### Bug 修复优化

- 解决了 loaded_plugins erofs error 的问题
- 解决了 v2.0 中更新字段触发 Webhook update 校验拦截导致更新失败的 Bug
- 解决了升级 EMQX 5.0 的过程中，状态判断的 Bug
- 解决了 v1.1 中可能出现脑裂的 Bug



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
