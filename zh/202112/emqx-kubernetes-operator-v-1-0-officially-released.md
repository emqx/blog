EMQX 始终致力于为全球客户提供高可靠、高性能的实时数据移动、处理能力。通过 EMQX，无论是公有云还是私有云环境，用户都可以快速构建关键 IoT 应用。

作为 EMQX 全面拥抱云原生的一项重要进展，EMQX Kubernetes Operator v1.0 于近日正式发布，将帮助广大用户更方便、快捷、安全地基于 Kubernetes 平台对 EMQX 集群进行生命周期管理。

项目地址：[https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator) 

## 什么是 EMQX Kubernetes Operator?

EMQX Kubernetes Operator 是一种封装、部署和管理 EMQX 的方法，也是一个特定的应用控制器，允许 DevOps 人员在 Kubernetes 上编排 EMQX 集群，管理他们的生命周期。

![EMQX Kubernetes Operator](https://assets.emqx.com/images/33ce831314e38062f253b83b766b5c80.png)

## 为什么需要 EMQX Kubernetes Operator？

EMQX Kubernetes Operator 可以帮助用户在 Kubernetes 的环境上快速创建和管理 EMQX 集群，不仅极大简化部署和管理流程，也降低了管理和配置的专业技能要求。EMQX Kubernetes Operator 将使部署和管理工作变成一种低成本、标准化、可重复性的能力，高效实现集群扩容、无缝升级、故障处理和统一监控。

### 快捷部署

通过 Helm 或者 Manifest 文件，无需考虑底层存储和 LB，使用默认配置就可以在 Kubernetes 上快速部署一个 EMQX 集群，轻松体验 MQTT 服务。

同时提供可配置的 EMQX Custom Resource，供您定制满足业务需求和适配您的 Kubernetes 平台的 EMQX 集群。

目前 EMQX Kubernetes Operator 已经完成对阿里云 ACK、AWS EKS 的优化，可实现无缝对接上述 Kubernetes 平台的网络和共享存储资源。其他平台优化也在持续进行中。

### 高效运维

使用 EMQX Kubernetes Operator，您可以在不中断业务的情况下实现 EMQX 集群扩展、安全升级、配置更新，承载更多设备和更复杂的业务，而现有业务本身不会受到任何影响。

> Kubernetes 版本需为 1.20.0 或以上

### 统一监控

EMQX Kubernetes Operator 会采集 EMQX 集群运行的关键指标，对集群运行状态进行实时监控。同时支持与 Prometheus 的无缝对接，可将指标数据导出到 Prometheus 中，与您自己的监控系统集成。EMQX 集群运行状态尽在掌握。

 
作为一款[云原生的分布式 MQTT 消息服务器](https://www.emqx.io/zh)，EMQX 产品的部署和运维体验是 EMQ 团队持续关注和优化的重点之一。EMQX Kubernetes Operator 的正式发布，标志着 EMQX 的产品设计又向云原生理念进一步深入，帮助用户充分享受云计算带来的优势。

点击项目地址：[https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator) ，访问 GitHub 主页下载试用 EMQX Kubernetes Operator。如果您有任何建议、疑问或反馈，欢迎在 GitHub 上提交 issue。我们期待您与我们一起，成就一个更好的开源产品。
