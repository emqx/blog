本月，EMQX 团队为大家带来了期待已久的 5.0.0-rc.1 版本，它是 5.0 版本的一个阶段性成果，包含了 v5.0 开发至今我们致力于为大家带来的各项重大改进。同时，4.x 维护版本的迭代升级也在进行中。

云服务方面，[EMQX Cloud](https://www.emqx.com/zh/cloud) 本月发布了全新改版的规则引擎模块，同时支持了阿里云新版云企业网。此外，Cloud Native 团队也发布了集群部署管理工具 [EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 的新版本。

## EMQX

### 5.0 新进展：5.0.0-rc.1 正式发布

本月 EMQX 团队陆续发布了 5.0.0-beta.4 和 [5.0.0-rc.1](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.1) 版本。目前，5.0 版本的功能已基本完备，欢迎大家下载试用。在后续的版本迭代中，EMQX 团队将专注在 5.0 版本的稳定性提升和 Dashboard 交互优化上。

相较于 beta.3 版本，rc.1 主要带来了以下改进：

- 为热配置功能提供 UI 界面，支持分层配置，并且为每个配置项提供详细的配置说明
- 上线全新的插件功能，支持上传、安装和管理插件
- 部分消息收发指标支持速率统计
- 改进了速率限制功能
- 为基于内置数据库的 AuthN 与 AuthZ 添加搜索支持
- 为 MQTT-SN 设备添加睡眠模式支持
- 各项问题修复与使用体验改进

### 维护版本升级

我们即将为社区和企业用户发布 4.3 和 4.4 的最新维护版本，除了进一步提升稳定性，我们还在这些版本中带来了一些增强性的改进，主要包括：

- 在严格模式下为 MQTT 报文增加对 UTF-8 字符串的检查
- 增加对 Dashboard User 与 AppID 的格式检查
- 提高规则引擎浮点型数据的写入精度
- 为 Kafka 生产者增加 OOM 保护（仅企业版）
- 修复资源不可用时查看详情请求超时的问题
- 修复 MongoDB 相关功能在配置不正确时输出过量错误日志的问题
- 修复 server_keepalive 配置项的值会被错误应用于 MQTT v3.1.1 客户端的问题
- 修复 EMQX 启动时系统内存告警误激活的问题
- 修复通过多语言协议扩展功能接入的连接进程异常退出时未释放相关资源导致连接计数不更新的问题

### 即将登场

在未来几个月内，EMQX 将推出一些功能改进，在此为大家剧透如下：

- 规则引擎编解码支持 gRPC 以获取更好的性能
- 规则引擎将支持更多函数，包括时间格式转换函数、压缩/解压缩等
- 规则引擎将支持更多事件，例如连接失败等
- 规则引擎将支持重置指定规则的统计指标
- 即将支持使用消息队列大小对客户端进行范围查找
- 即将支持运行时调整钩子调用顺序

我们的团队将持续努力，为您带来更佳的 EMQX 使用体验。

## EMQX Cloud

### 规则引擎改版为「数据集成」

EMQX Cloud 的规则引擎功能模块现已正式更名为「数据集成」，同时进行了更易于用户理解、操作、管理的 UI 改版升级。对比之前版本的规则引擎模块，新版本「数据集成」通过导航的方式一步步帮助用户快速熟悉资源与规则的创建。用户只需按照创建资源-创建规则-添加动作-测试运行的流程进行操作，便可以完成对规则的配置，进一步实现对设备数据的处理转存。

> 更多详情请查看： [https://mp.weixin.qq.com/s/Vvg0joa4IW7AjebXDQKmwA](https://mp.weixin.qq.com/s/Vvg0joa4IW7AjebXDQKmwA) 

![EMQX Cloud 数据集成](https://assets.emqx.com/images/633495d451db95a655412868be321e12.png)

### 阿里云新版云企业网支持

该功能对于选择阿里云作为云服务商创建部署的用户很有帮助。由于阿里云计划停售云企业网基础版转发路由器并升级成企业版转发路由器，云企业网配置方式和收费也有所变动。

> 详情可查看：[https://help.aliyun.com/document_detail/353235.html](https://help.aliyun.com/document_detail/353235.html) 

对于需要配置 VPC 对等连接的 EMQX Cloud 用户，流程上会相比原来的方式简化很多。详细步骤和说明请查看帮助文档： [https://docs.emqx.com/zh/cloud/latest/deployments/vpc_peering.html](https://docs.emqx.com/zh/cloud/latest/deployments/vpc_peering.html)

## EMQX Kubernetes Operator

EMQX Kubernetes Operator 是一个用来帮助用户在 Kubernetes 的环境上快速创建和管理 EMQX 集群的工具。 它可以大大简化部署和管理 EMQX 集群的流程，将其变成一种低成本的、标准化的、可重复性的能力。

### 功能更新

本月 EMQX Kubernetes Operator 先后发布了 1.1.4 和 1.1.5 两个版本，新版本增加了对 DNS Server 自动发现集群的支持，现在使用 EMQX 4.4 版本进行部署时，将默认使用 DNS Server 自动发现集群，相比于之前通过 k8s APIServer 进行自动发现，DNS Server 无需配置额外的 serviceAccount，提高了安全性。

EMQX Kubernetes Operator 支持将 Telegraf 容器以 SideCar 模式部署在 EMQX Pod 中，可以通过 Telegraf 和 `emqx_prometheus` 插件采集并发送 EMQX 的数据。

### 重大变更

在 1.1.4 版本中，我们将 v1beta1 APIVersion 设置为 unserved version，这意味着将无法新建 v1beta1 APIVersion 的任何资源。无需担心的是，现有的 v1beta1 APIVersion 的资源将会无感知的转换为 v1beta2 APIVersion，而且不会导致业务中断。我们计划在 1.2 版本中彻底删除对 v1beta1 APIVersion 的支持。

### 即将到来

EMQX Kubernetes Operator v1.2 和 v1beta3 APIVersion 正在开发中，v1beta3 APIVersion 将带来更合理的 `.spec`结构。敬请期待。

 

为了完成「通过世界级开源软件产品服务人类未来产业与社会」的使命，敬请期待一个更优秀的 EMQX。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
