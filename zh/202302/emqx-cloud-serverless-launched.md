近日，全球领先的开源物联网数据基础设施软件供应商 EMQ 正式发布了 Serverless MQTT 云服务 —— EMQX Cloud Serverless 的 Beta 版本，开创性地采用弹性多租户技术，用户**无需关心服务器基础设施和服务规格伸缩所需资源**，仅用三秒即可极速创建 MQTT 部署，并根据业务需求进行无感知自动化弹性伸缩、按实际使用量付费，实现全自动化的 MQTT 接入服务，专注物联网业务逻辑和实现。

作为全托管的 MQTT 消息云服务，EMQX Cloud 可以将物联网设备连接到任何云，免除基础设施维护负担，至今已帮助全球各行业的 300 余家企业用户轻松开启 MQTT 服务。EMQX Cloud Serverless 的推出将进一步简化 MQTT 消息服务的使用，更好地满足中小型企业及独立开发者对 MQTT 协议设备的接入需求，推动用户更轻松快捷地实现物联网业务创新。

目前，EMQX Cloud Serverless Beta 版本的免费公测已全面开启，即日起至 2023 年 3 月 31 日止，用户可通过 EMQX Cloud 官方网站免费试用 Serverless 版本。


## 基于多租户架构的 Serverless MQTT 服务

随着云计算的发展，Serverless 这一热点技术趋势逐渐成为云的未来发展方向。作为 Serverless 模式的 MQTT Broker，EMQX Cloud Serverless 为用户提供了完全自动化的 MQTT 接入服务构建、部署与弹性伸缩，用户无需关心底层部署与运维，可以更加专注于业务逻辑的实现。

### 3 秒极速创建部署

不同于专有版单用户独立集群部署，Serverless 模式的 MQTT 云服务采用共享集群多租户架构，在跨多可用区集群的基础上，将服务能力分割给多个租户共享使用。每个租户数据和通讯都是完全隔离的，确保数据安全。同时对配置做了合理规划和限制，确保单一租户高并发下不会影响到其他租户的使用。

得益于多租户架构，用户可即时共享使用事先创建好的集群部署，极大缩短了用户创建部署的时间。只需要简单点击操作，等待约 3 秒，开发者即可拥有一个功能完备、安全可靠的 MQTT Broker。

<video controls width="760px">
    <source src="https://cdn.emqx.com/video/emqx-cloud-serverless-launched.mp4" type="video/mp4">
</video>

### 全自动化弹性伸缩

Serverless 技术对用户强调 No Server，本质上并不是不需要服务器，而是将服务器全权托管给云厂商。用户不用费心管理，只需把业务部署到平台上来，聚焦业务逻辑代码。同时也无需考虑所需资源，即可根据实际请求进行弹性伸缩。

基于这一理念的 EMQX Cloud Serverless 版本帮助开发者实现了更为轻松便捷的自动化 MQTT 接入服务，全托管模式极大降低了用户的部署及运维成本，无感知自动化弹性伸缩能力则帮助用户应对动态变化的业务规模带来的不同需求，有效节省整体使用成本。

## 按量计费，有效控制成本

EMQX Cloud Serverless 版本采用全新的定价模型，以「连接设备数量*设备在线时长」为单位进行计价，并**每月发放 100w 免费连接分钟数**（大约相当于 23 个设备在线 1 个月）。这意味着小微场景下的物联网应用开发几乎不需要付出任何成本。而对于因业务变动带来的设备连接变化、流量不稳定等场景，根据实际用量付费的方式也能帮助用户大幅节约开支。

此外，Serverless 版本在接入规模上提供 **1000 并发接入以内的动态接入规格**，对于设备接入量较小的用户也更加友好。 

### 适应多种场景需求

按量计费、弹性伸缩的 Serverless MQTT 云服务将为处在不同发展阶段的用户带来符合当前业务需求的最优方案：

- 中小规模连接场景。假设 100 台设备连接，每台设备每分钟消息收发 5 条，信息标准大小（300 字节）。一般的 IoT 公有云平台每月成本约为 200~700 元，而使用 Serverless MQTT 云服务的月费用仅为 34 元左右，成本将大幅降低。
- 标准规模连接但消息频率低的场景。假设 1000 台设备连接，每台设备 10 分钟发 1 条消息，信息标准大小（300 字节）。Serverless MQTT 云服务的费用大约为每月 330 元，与 IoT 公有云平台每月约 200～700 元的成本相比，不仅价格更低，还支持停止使用后即刻停止计费，减少用户的非必要支出。
- 研发和测试阶段。假设设备数量只有 20～30 台，在正常的消息频率和大小下，Serverless MQTT 云服务的使用几乎是免费的，为用户节省了很多基础软件成本。而当业务增长，设备连接数上升之后，服务也可以无缝扩展，无需迁移基础设施。

> 更多业务场景使用价格估算请前往[官网价格页面](https://www.emqx.com/zh/pricing)。

### 免费试用计划

为了让大家对 EMQX Cloud Serverless 版本有更加直接的了解和体验，同时收集更多反馈意见不断完善产品，**我们特推出 Serverless Beta 版本，并在 2023 年 3 月 31 日之前提供免费试用**。Beta 版本除了设备接入量限制在 100 以内，与正式版本在功能方面没有任何区别。您可以在 EMQX Cloud 控制台右上角的菜单中提交工单，向我们提交反馈建议，我们将第一时间答复并为优质建议提供者寄送纪念礼品。

## EMQX Cloud Serverless 使用指引

您可以在 EMQX Cloud 官网注册账号后进行使用。登录 EMQX Cloud 控制台，选择 Serverless Beta 版本。

![EMQX Cloud Serverless](https://assets.emqx.com/images/7e001cd9fa3cba0937202a1a24837a6b.png)

> 目前 Serverless 版本仅支持部署在阿里云杭州区域，并且在 Beta 版本最大接入量为 100。

在 2023 年 3 月 31 日之前，Serverless Beta 版本完全免费。之后将按照 8 元/百万连接分钟和 1.5 元/GB 收取连接费和流量费。

![Serverless 费用](https://assets.emqx.com/images/4028ca39f7aff549eaeea195503f414b.png)

点击立即部署，**等待约 3 秒**，Serverless 版本即可部署完成，您将即刻拥有一个功能完备的 MQTT 服务器。

在部署概览页面，您可以看到当前连接数、消息上下行 TPS、已使用的连接分钟数和流量，以及连接地址和连接端口。

![部署概览页面](https://assets.emqx.com/images/db9035d98c92299de82b0f04940611c4.png)

EMQX Cloud 的全部功能和使用指南请参阅产品文档：[EMQX Cloud 帮助中心](https://docs.emqx.com/zh/cloud/latest/)

Serverless 版本与专有版详细功能对比请查看：[https://www.emqx.com/zh/pricing](https://www.emqx.com/zh/pricing) 

## 结语

EMQX Cloud 致力于为不同行业、不同规模的用户提供便捷的物联网 MQTT 云服务。Serverless 版本的推出则让更多用户可以享受到 EMQX Cloud 带来的便利。不论是大型企业还是初创团队，都可以通过 EMQX Cloud 获得稳定可靠数据基础服务，实现物联网业务创新。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
