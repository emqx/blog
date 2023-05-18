随着物联网的飞速发展，保护数据隐私和安全变得愈发重要。构建一个安全、可靠、可扩展的物联网基础设施成为企业的首要任务。

EMQ 近期推出了 [EMQX Cloud BYOC](https://www.emqx.com/zh/cloud/byoc)，采用了以数据隐私为先的架构，为解决这些问题提供了一个理想的方案。用户可以在自己的云环境中部署 MQTT 集群，完全掌控自己的数据隐私和安全。

> 了解更多关于 BYOC 的内容：[提升您的 MQTT 云服务：深入探索 BYOC](https://www.emqx.com/zh/blog/exploring-byoc-taking-your-mqtt-cloud-service-to-the-next-level) 

本文将深入剖析 EMQX Cloud BYOC 的架构，并探讨它如何保障您的物联网基础设施安全。

## EMQX Cloud BYOC 架构概览

EMQX Cloud BYOC 提供了一个灵活可扩展的架构，让客户能够完全掌控访问权限。该架构由两个环境组成：

- EMQX Cloud 云环境：提供多种功能，包括访问控制管理、数据集成、监控、告警等，帮助客户管理他们的 MQTT 集群。
- 客户的云环境：用于托管由 EMQX Cloud 管理的 EMQX MQTT 集群。客户的所有 MQTT 数据都通过这个 MQTT 集群进出。

![EMQX Cloud BYOC 架构图](https://assets.emqx.com/images/caaab8b3bbaefaad3b82d8e1ec7f4909.png)

在客户的云环境中，有一个 EMQX 集群和一个 BYOC Agent 节点，它们位于一个独立的 VPC 内。客户使用云平台提供的负载均衡服务来控制 MQTT 设备的流量，同时通过 VPC 对等连接与其他物联网应用或消息持久化组件进行通信。BYOC Agent 节点负责管理 EMQX 集群、获取监控日志、执行数据备份。

在 EMQX Cloud 云环境中，提供了一个基于 Web 的管理控制台，方便管理和控制客户的 EMQX 集群，并查看集群日志和监控数据。运维服务用于收集监控数据和日志、管理告警规则、自动化自恢复流程。

## BYOC 的核心理念：数据隐私为先

EMQX Cloud BYOC 的架构主要通过两个部分来实现高度数据隐私保障：控制层和数据层。

控制层位于 EMQX Cloud 环境中，担当管理控制台和数据监控的角色。它的主要作用是在系统运行过程中收集监控数据，向客户的集群发送控制指令。它只处理集群控制和监控系统运行情况，不处理任何业务数据的流入或流出。

数据层包括 EMQX 集群和 BYOC Agent 节点，它们均部署在客户的云环境中。客户的所有业务数据都由它们负责处理。

以数据隐私为核心， EMQX Cloud BYOC 为那些希望部署安全可靠的物联网系统的企业提供了对访问权限的完全控制，提高了隐私和安全性。通过 BYOC 架构，客户的业务数据可以安全隔离在自己的云环境中，以满足对数据安全和合规的要求。

## 使用 EMQX Cloud BYOC 的前提条件

在开始使用 EMQX Cloud BYOC 之前，客户需要满足以下一些技术要求：

- 熟悉公有云服务和网络结构的基本概念，如 VPC、子网、ECS 等。
- 拥有一个公有云账号和 EMQX Cloud 账号。
- 准备相关的云资源和账号权限。
- 准备 Ubuntu 20.04 LTS 环境以运行安装脚本。
- 获取 EMQX Cloud BYOC 许可证。
- 准备域名和对应的 SSL 证书。

## 选择 BYOC，从今天开始掌控您的数据

除了通过以数据隐私为先的架构让您在自己的云中实现安全的数据传输和存储，EMQX Cloud BYOC 还提供了企业级的安全功能和定制选项，让您可以灵活地部署和集成。在 EMQ 技术专家的帮助下，您的 MQTT 基础设施管理将变得前所未有的简单。

[访问我们的网站](https://www.emqx.com/zh/cloud/byoc)或[联系我们](https://www.emqx.com/zh/contact?product=cloud&productEdition=BYOC)获取更多信息。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
