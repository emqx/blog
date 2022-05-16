>EMQX 是一款云原生分布式物联网接入平台，通过一体化的分布式 MQTT 消息服务和强大的 IoT 规则引擎，为高可靠、高性能的物联网实时数据移动、处理和集成提供动力，「随处运行，无限连接，任意集成」，助力企业快速构建关键业务的 IoT 平台与应用。
>
>官网地址：[https://www.emqx.com/zh/products/emqx](https://www.emqx.com/zh/products/emqx) 
>
>EMQX Cloud 是全托管的云原生 MQTT 消息服务，以自动化、全托管的形式为用户提供可靠、实时的海量物联网设备连接、事件消息处理、IoT 数据桥接等能力，免除基础设施管理维护负担，加速物联网应用开发。
>
>免费试用：[https://www.emqx.com/zh/try?product=cloud](https://www.emqx.com/zh/try?product=cloud) 



本月，EMQX 团队发布了多个 4.x 的维护版本，在进一步提升稳定性的基础上还为大家带来了多项新功能，包括强化对 Pulsar 的支持、支持使用 gRPC 服务解码数据、多项针对规则引擎的使用体验改进等。此外，5.0.0-rc.2 也即将发布。

云服务方面，EMQX Cloud 上线了流量包与自定义函数两个增值服务，带来了简化用户采购流程的功能更新，同时支持了阿里云部署私网连接。此外，Cloud Native 团队也带来了好消息：EMQX 现已加入 Docker 官方镜像。

## EMQX

### 5.0 新进展：5.0.0-rc.2 即将发布

本月 EMQX 团队对 5.0 Dashboard UI 风格与交互样式进行了诸多改进，也对各项功能进行了细节上的打磨和完善。目前 5.0.0-rc.2 还在进行最后的测试，相信几天之后就能与大家见面，届时也欢迎广大用户朋友下载试用。


![EMQX 5.0 Dashboard 1](https://assets.emqx.com/images/d21c69265ffe6bc5d52bd56cc8bf2a49.png)

![EMQX 5.0 Dashboard 2](https://assets.emqx.com/images/a73d10ee1d0cd9c5988c1538bafabc52.png)

### 维护版本快速迭代

本月 EMQX 团队先后发布了社区版 v4.3.13、v4.3.14、v4.4.2、v4.4.3 与企业版 v4.3.8、v4.3.9、v4.4.2、v4.4.3 共计 8 个版本，总共带来四十余项问题修复，修复详情可以访问[官网](https://www.emqx.io/)下载页面右侧的 Release Notes。

> 如果您遇到的问题未包含在以上修复内容中，可以通过我们的 [Github 社区](https://github.com/emqx/emqx/issues) 或者 [EMQ 问答社区](https://askemq.com/) 反馈，我们将积极帮助您解决。

![维护版本快速迭代](https://assets.emqx.com/images/8d831b2164c7d01e7129a915dc48b25b.jpeg)

除了提升使用稳定性，以上新版本也为大家带来了多项功能改进：包括规则引擎支持重置指定规则的统计指标、新增连接确认和鉴权完成事件、支持 zip 与 gzip 等压缩函数、强化对 Pulsar 的支持、编解码功能支持使用 gRPC 服务等。

详情请查看：[https://www.emqx.com/zh/blog/emqx-multi-release-rules-engine-supports-reset-run-data](https://www.emqx.com/zh/blog/emqx-multi-release-rules-engine-supports-reset-run-data) 

## EMQX Cloud

### 流量包增值服务

[本月 EMQX Cloud 增值服务上线了流量包](https://www.emqx.com/zh/blog/emqx-cloud-cost-savings)，经常超出免费流量的用户可以以一个更加优惠的价格购买流量包，预计可节约 20%+ 的成本。

购买流量包后，运行中的部署每个月将优先消耗免费流量，在免费流量耗尽之后会消耗流量包的流量。流量包的使用时间为购买之后的 6 个月以内。流量包可以为一个根账号下的所有部署提供超额之后的流量。

用户在增值服务模块中即可自行开通流量包服务。目前流量包仅支持国内部署。

![EMQX Cloud 流量包](https://assets.emqx.com/images/7ecfa36b8b23bad99cae45cb830f2731.png)

### 自定义函数

自定义函数是新开发上线的增值服务，使用自定义函数为 Topic 绑定脚本。目前支持 ECMAScript5.1/JavaScript，可实现对 Payload 内容的编解码或预处理，解决了在工业设备连接等场景下设备上报的数据和应用端数据转化的问题。例如设备上报的是二进制的编码数据，可以转化成 JSON 格式的数据上报到服务端进行处理。Topic 中的数据在经过自定义函数处理之后，可以使用数据集成功能分发到云资源中去，也可以直接被订阅消费，十分灵活。

![自定义函数](https://assets.emqx.com/images/a364e3fc0cced9500e22e541e15790f0.png)

当前自定义函数服务处于内测阶段中，用户可通过工单申请获得 14 天的免费试用。更多请查看[帮助文档](https://docs.emqx.com/zh/cloud/latest/vas/codec.html)。

### 连续包年和订单体系

国内站新增了连续包年部署，用户（包含新购部署、计时部署转包年部署、续费购买包年部署）可以选择直接购买 1 - 3 年时长的连续包年部署。同时增加了订单体系，提交订单后，用户可以在控制台查询订单，也可以下载 PDF 格式订单作为企业内部提交付款申请的依据，方便用户企业内部的财务审批流程。详情请查看：[https://www.emqx.com/zh/blog/emqx-cloud-order-system-optimization](https://www.emqx.com/zh/blog/emqx-cloud-order-system-optimization) 

![连续包年](https://assets.emqx.com/images/a8b1ffff9ed1cd28d9dfdd957ee650ad.png)

![查询订单](https://assets.emqx.com/images/8755e0e701970a77309afc6ae9f57266.png)

### 阿里云部署支持私网连接（Private Link）

私网连接（PrivateLink）能够实现 EMQX Cloud 部署所在的专有网络 VPC 与公有云上的服务建立安全稳定的私有连接，简化网络架构，实现私网访问服务，避免通过公网访问服务带来的潜在安全风险。

如果用户 EMQX Cloud 的部署云服务选择的是阿里云，并且自己的云资源也在阿里云 VPC 内，即可创建私网连接。开通了私网连接之后，EMQX Cloud 部署和阿里云上的自己的资源打通，相比与云企业网，私网连接的服务之间的通讯更加安全可控，可以通过端口对服务做更精细的管理。

私网连接（Private Link）可以在部署概览 - 私网连接中进行配置及创建。更多关于私网连接请[查看文档](https://docs.emqx.com/zh/cloud/latest/deployments/privatelink.html#阿里云平台私网连接-privatelink)。

### 外部认证及访问控制

外部认证与访问控制帮助用户使用自己服务进行认证鉴权。目前在支持 HTTP 认证的基础上，新增了 MySQL、PostgreSQL 作为数据源的认证鉴权。外部认证及访问控制的原理为当客户端需要进行认证时， EMQX Cloud 将使用当前客户端的信息填充到设置的查询语句当中，并且执行用户配置的认证。通过返回来判断是否通过验证。这样使用用户自己数据库中的数据进行认证，更加安全可靠并且灵活。

在部署详情页面中，点击左侧菜单【认证鉴权】- 【外部认证鉴权】选择相应的认证方式进行配置。

![外部认证及访问控制](https://assets.emqx.com/images/ef5328f4a9148c065041d1c616abb66c.png)

## EMQX Kubernetes Operator

### 功能更新

本月发布的 EMQX Operator 1.1.6 版本中提供了如下新功能：

1. `SecurityContext` 自定义配置，用户可根据自己需求进行安全上下文的配置
2. 提供了关于`EMQX Operator Metrics` 的采集的默认配置。

### 完善优化

1. 修复了基于 EKS、ACK 等云厂家提供的 Kubernetes 集群服务上部署的权限问题
2. 修复了重启 Node 出现的 Operator Manager 节点选举失败的问题
3. 移除了关于 EMQX 集群节点数`>=3` 的限制
4. 移除了 `emqx_prometheus` 插件的默认配置，用户可根据具体需求自行决定是否配置
5. 基于性能压测结果，完善 `EMQX Operator Manager` 的资源配置参数

### 即将到来

EMQX Operator v1.2 和 v1beta3 APIVersion 正在开发中，v1beta3 APIVersion 将带来更合理的 `.spec`结构，

1.2 版本将引入更完善的事件日志以及集群状态描述。

### Docker 镜像

EMQX 现已加入 Docker 官方镜像：[https://hub.docker.com/_/emqx](https://hub.docker.com/_/emqx)

用户现在可以通过 `docker pull emqx `直接获取 EMQX 镜像。

![EMQX Docker 镜像](https://assets.emqx.com/images/0b24b183a5581754b39742d9c65cbd0c.png)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
