十月，EMQX 在产品质量和用户体验方面进行了进一步提升，同时 QUIC 相关开发工作也在持续进行中。

此外，EMQX Cloud 在订阅渠道、部署地区、操作体验等方面均有更新。


## EMQX

### 产品质量提升

在过去的 10 月，EMQX 团队的工作重点是提升所有支持版本的产品质量。我们解决了共享订阅的问题，以及 HTTP auth 与 Webhook 中 HTTPS 长期连接时可能导致的请求大量超时问题。

### 更好的运维体验

我们在 EMQX 5.0 企业版的规则引擎指标中集成了 [Open telemetry](https://opentelemetry.io/) 框架，它是一个供应商中立的开源可观测性框架，可用于生成、收集、可视化以及导出包括 Trace、指标、日志等遥测数据。

### QUIC 更新

[quicer](https://github.com/emqx/quic) 中多条流（Stream）传输的开发工作已经接近尾声，经过一些调整后我们会将其引入 [EMQX](https://github.com/emqx/emqx) 以及 EMQ 开发的 Erlang 客户端库 [emqtt](https://github.com/emqx/emqtt)。

### 用户体验改进

本月我们改进了用于消息发布的 REST API，使其更成熟稳定。我们已经开始了一个针对 REST API 的专项行动，旨在为用户提供一致的 REST API 体验并解决其中不合理的设计。

macOS 用户的使用体验也得到了进一步改善——当用户运行 EMQX 时，系统不会再发出未签名警告。

此外，我们使用更易扩展的方式来跟踪版本更新日志，每次版本发布将创建 2 个独立的更新日志文件，分别对应英文版和中文版，而不是一个巨大的 CHANGELOG.md 文件。

各版本详细更新日志请查看：

- [EMQX 5.0.9](https://www.emqx.com/zh/changelogs/broker/5.0.9)
- [EMQX 4.4.10](https://www.emqx.com/zh/changelogs/broker/4.4.10)
- [EMQX 4.3.21](https://www.emqx.com/zh/changelogs/broker/4.3.21)


## EMQX Cloud

### EMQX Cloud SaaS 服务上架 AWS Marketplace

针对海外用户，如果需要在 AWS 上统一管理财务和账单，现在可以直接在 AWS Marketplace 中开通 [EMQX Cloud（Pay As You Go）](https://aws.amazon.com/marketplace/pp/prodview-g6zejrbcad6mu)版本。完成注册开通之后，EMQX Cloud 会将账单发送到 AWS 进行记账和扣费。通过 AWS Marketplace 开通的账号依然可以获取 14 天的免费部署试用。

![EMQX Cloud SaaS 服务上架 AWS Marketplace](https://assets.emqx.com/images/6a451dbbd1484ade3bca0880283dbdfa.png) 

### 海外版部署支持更多区域

EMQX Cloud 海外版新增支持 AWS 在东京以及加利福利亚区域的部署。目前专业版的部署区域已经达到了 19 个，满足越来越多用户的使用需求。

### 控制台功能优化

新增在客户端详情中管理订阅的功能。在**监控 -  客户端**，点击客户端名称进入详情，可以在详情下方看到订阅管理显示了当前客户端订阅的主题，可进行添加和删除。

![EMQX Cloud 控制台功能优化1](https://assets.emqx.com/images/24bd7bd85d4650a301e8d89f93e2354e.png)


此外，以前版本中邀请子账号加入到项目时，如果子账号没有及时认证而导致过期，需要删除账号重新创建。现在我们新增支持重新邀请操作，方便账号认证过期再次邀请。

![EMQX Cloud 控制台功能优化2](https://assets.emqx.com/images/9be5024bd2e4b0cbbabeacc343792e9c.png)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
