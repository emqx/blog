全托管 [MQTT 消息云服务 EMQX Cloud](https://www.emqx.com/zh/cloud) 可以为用户提供可靠、实时的物联网数据移动、处理和集成，助力加速物联网平台与应用开发。

其中，基于原有高性能内置规则引擎优化升级的「数据集成」模块，为用户配置处理及响应消息流与设备事件规则提供了一个清晰灵活的「可配置」架构解决方案，支持包括 Kafka、MySQL、Redis、Webhook 等在内的数十种数据集成资源，是 EMQX Cloud 帮助用户实现数据灵活处理与集成的利器。

在最近的版本更新中，EMQX Cloud 又新增了HStreamDB 和阿里云 Tablestore 两个外部数据库扩展支持。

## 功能详情

借助数据集成功能，用户可以根据自己的需求通过创建资源、创建规则、添加动作、测试运行这 4 个简单的步骤完成配置，实现设备数据的灵活运转。不仅极大简化了开发过程，降低了业务系统和 EMQX Cloud 之间的耦合程度，也为 EMQX Cloud 的私有功能定制提供了一个更优秀的基础架构。

![EMQX Cloud 数据集成步骤](https://assets.emqx.com/images/832567b28e5f94d54fa6344607c3c938.png)

EMQX Cloud 目前支持多种类型的数据队列、数据库及 Web 服务对接。本次新增的是分别由 EMQ 和阿里云开发的两款数据库。

![EMQX Cloud 数据集成](https://assets.emqx.com/images/3d25c7a9c01cbf7a373cd3f91661898a.png)

### HStreamDB

HStreamDB 是 EMQ 开源的一款专为流式数据设计的[流数据库](https://hstream.io/zh)，可针对大规模实时数据流的接入、存储、处理、分发等环节进行全生命周期管理。它使用标准 SQL (及其流式拓展）作为主要接口语言，以实时性作为主要特征，旨在简化数据流的运维管理以及实时应用的开发。与 EMQX Cloud 集成后，用户可以轻松实现设备数据上云、处理与分发。

![EMQX Cloud HStreamDB 配置界面](https://assets.emqx.com/images/9e52cfbbc2d4089731edfa94fcd6bda7.png)

<center>HStreamDB 配置界面</center>

### 阿里云 Tablestore

[阿里云表格存储（Tablestore）](https://help.aliyun.com/document_detail/27280.html)面向海量结构化数据提供 Serverless 表存储服务，同时针对物联网场景深度优化提供一站式的 IoTstore 解决方案。适用于海量账单、IM 消息、物联网、车联网、风控、推荐等场景中的结构化数据存储，提供海量数据低成本存储、毫秒级的在线数据查询和检索以及灵活的数据分析能力。

![EMQX Cloud Tablestore 配置界面](https://assets.emqx.com/images/fd2e30f14bf5058451478ca6d43dae08.png)

<center>Tablestore 配置界面</center>

## 数据集成操作指南

HStreamDB 数据集成参考文档：[https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html](https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html) 

Tablestore 数据集成参考文档：[https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_tablestore.html](https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_tablestore.html) 

> 注：
>
> 1、本次更新资源在基础版不可用
>
> 2、对于专业版部署用户：请先完成 [对等连接的创建](https://docs.emqx.com/zh/cloud/latest/deployments/vpc_peering.html)，本文提到的 IP 均指资源的内网 IP。（专业版部署若开通 [NAT 网关](https://docs.emqx.com/zh/cloud/latest/vas/nat-gateway.html) 也可使用公网 IP 连接资源）


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
