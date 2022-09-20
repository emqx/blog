上个月，[EMQX 最新的里程碑版本 v5.0.0 正式发布](https://www.emqx.com/zh/blog/emqx-v-5-0-released)。这一版本带来了诸多开创性的更新与改进。目前，EMQX 团队正以每两周一个版本的速度进行后续版本的迭代，以快速修复已知问题和纳入更多功能。此外，本月 EMQX 团队在社区交流和多个新功能上也有比较大的进展。

云服务方面，[EMQX Cloud](https://www.emqx.com/zh/cloud) 新增了两个外部集成数据库支持，用户在进行数据持久化时将有更多选择。[EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 发布了新版本，对 EMQX 5.0 也进行了同步适配支持，此外还实现了 [eKuiper](https://ekuiper.org/)、[Neuron](https://neugates.io/) 等边缘计算产品的部署支持。

## EMQX

### 规则引擎 RocketMQ 支持认证与 ACL

RocketMQ 开启访问权限控制可以提高系统的安全性和保密性，EMQX 团队近期为规则引擎中的 RocketMQ 添加认证与 ACL 能力，以便连接至启用访问权限控制的 RocketMQ 中，此功能将在近期的版本更新中正式上线。

### 支持 Kafka 的 SASL/SCRAM 认证

Kafka 支持 SASL/SCRAM 身份验证，SCRAM（Salted Challenge Response Authentication Mechanism）是 SASL 机制中的一种，通过执行用户名/密码认证（如 PLAIN 和 DIGEST-MD5）的传统机制来解决安全问题。

EMQX 将支持 Kafka 的 SCRAM-SHA-256 和 SCRAM-SHA-512 认证，可与 TLS 一起使用提供更安全的 Kafka 数据集成，此功能同样将在近期的版本更新中正式上线。

### 支持通过 CLI 检查配置文件

我们为 EMQX 增加了配置文件检查能力，在运行时需要重新加载配置的时候，可以通过 CLI 检查所修改的配置文件（包括插件配置）是否有语法错误，此命令非常重要，能够避免 EMQX 重启时因为配置错误无法启动。 

### 4.3 & 4.4 维护版本升级

[EMQX 开源版 v4.3.16 & v4.4.5 以及企业版 v4.3.11 & v4.4.5](https://www.emqx.com/zh/blog/emqx-update-integrated-streaming-database) 已经于上月初正式发布，带来了 EMQX 在 Linux 系统中内存计算不准确等多项已知错误修复以及 HStreamDB 集成、排他订阅等多项功能改进。

更多信息请查看对应版本的 Release Note 以了解更详细的信息：[EMQX v4.4.5](https://www.emqx.com/zh/changelogs/broker/4.4.5)、[EMQX Enterprise v4.4.5](https://www.emqx.com/zh/changelogs/enterprise/4.4.5)。

同时，4.3 & 4.4 下一维护版本的开发目前也已接近尾声，将于近期发布，敬请期待。

### EMQX 5.0 产品解读系列文章与直播

为了方便用户更好地了解 EMQX 5.0 的技术细节和产品价值，EMQX 团队推出了 5.0 版本产品解读系列文章。目前已发布了[《Mria + RLOG 新架构下的 EMQX 5.0 如何实现 1 亿 MQTT 连接》](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)与[《MQTT over QUIC：下一代物联网标准协议为消息传输场景注入新动力》](https://www.emqx.com/zh/blog/mqtt-over-quic)，之后我们还将分享 EMQX 5.0 在数据集成、认证及访问控制、插件扩展等方面的全新进展，敬请关注后续推送。

## EMQX Cloud

### 控制台部署日志监控全新改版

对部署详情中的日志监控进行了改版优化。以前的日志只能进行时间范围和集群节点的搜索和过滤，关键的日志信息需要用户自己去查找，不便于分析。改版后的日志模块重构了对于日志的解析和搜索能力，提供了 EMQX 两个节点 [emqx-node-1] 、[emqx-node-2] 多个级别的日志信息，可从 ClientID、ClientIP、Username、Topic、资源以及规则 ID 多维度进行查找分析，还可以根据不同错误类型进行过滤筛选。错误类型包括：**数据集成**、**客户端、消息**、**模块**、**EMQX 内部错误**等。

详情请查看：[EMQX Cloud 更新：日志分析增加更多参数，监控运维更省心](https://www.emqx.com/zh/blog/emqx-cloud-update-log-analysis-adds-more-parameters) 

![EMQX Cloud](https://assets.emqx.com/images/3627d3c68147c60d1637897871f303f0.png)

### 数据集成支持阿里云表格存储 Tablestore

阿里云表格存储（Tablestore）面向海量结构化数据提供 Serverless 表存储服务，同时针对物联网场景深度优化提供一站式的 IoTstore 解决方案。适用于海量账单、IM 消息、物联网、车联网、风控、推荐等场景中的结构化数据存储，提供海量数据低成本存储、毫秒级的在线数据查询和检索以及灵活的数据分析能力。

EMQX Cloud 已在数据集成中支持将数据持久化到阿里云表格存储（Tablestore），为使用此服务的用户提供了必要的数据持久化的方案。[查看这里](https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_tablestore.html)了解更多。

### 数据集成支持流数据库 HStreamDB

HStreamDB 是 EMQ 开源的一款针对大规模实时数据流的接入、存储、处理、分发等环节进行全生命周期管理的流数据库。它使用标准 SQL (及其流式拓展）作为主要接口语言，以实时性作为主要特征，旨在简化数据流的运维管理以及实时应用的开发。

EMQX Cloud 率先支持将设备端的数据转发、存储到 HStreamDB，为用户提供了新的数据持久化的方案。[查看这里](https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html)了解更多。

## EMQX Kubernetes Operator

### v1.2.3 发布

七月发布的 EMQX Operator 1.2.3 版本中提供了如下新功能：

- 端口调整 pod 不会重启，服务稳定性进一步提升
- 通过 EMQX Dashboard 中调整 listener，无需更改 K8s 相关配置即可自动更新
- 增加 EMQX 集群状态字段，以观察集群是否准备就绪
- 允许用户自定义（Dashboard 和 Management ）账号密码
- 允许用户添加自定义 Container

 同时有如下改进优化：

- 优化了configmap 更新文件延时的问题
- 修复了EMQX 在 K8s 环境中，可能出现脑裂的问题

###  EMQX 5.0 支持

- 实现 EMQX 非 core 节点通过 Deployment 部署（core 仍然采用 sts）
- 支持端口动态伸缩功能

### 完成云环境验证

我们使用 EMQX Operator 在主流云平台中进行了集群搭建测试，目前已完成的有：

- 在 AWS eks 上搭建 EMQX 集群，实现 100 万连接、50 万 TPS 的测试验证
- 在华为 cce 上搭建 EMQX 集群，实现 200 万连接、100 万 TPS 的测试验证
- 在阿里 eks 上搭建 EMQX 集群，实现 100 万连接、50 万 TPS 的测试验证

### 支持边缘计算产品部署

EMQ 旗下边缘计算产品（ 边缘流式处理引擎 eKuiper、边缘工业协议网关软件 Neuron）已支持通过 Helm 方式进行部署，同时高可用性通过 KubeEdge 得到了相关验证。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
