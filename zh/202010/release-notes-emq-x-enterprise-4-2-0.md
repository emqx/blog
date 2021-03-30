

EMQ X Enterprise 企业级物联网 MQTT 消息平台，支持百万级物联网设备一站式接入、MQTT&CoAP 多协议处理、低时延实时消息通信。支持基于 SQL 的内置规则引擎，灵活处理/转发消息到后端服务，存储消息数据到各种数据库，或桥接 Kafka、RabbitMQ 等企业中间件。

EMQ X Enterprise 适用于各种物联网应用场景，助企业快速构建物联网应用，并支持公有云、私有云、物理机、容器/K8S 任意部署。

网址：[https://www.emqx.io/cn/products/enterprise](https://www.emqx.io/cn/products/enterprise)

下载：无需提供任何信息， 立即[下载试用](https://www.emqx.io/cn/downloads#enterprise)

![enterprisemqttbroker.png](https://static.emqx.net/images/4b87d5ae6dc17bb84f6414e4d8fc504c.png)



### 概览

EMQ X Enterprise  v4.2.0 版本重点加强了热配置的支持，可以在不重启服务器的情况下通过 Dashboard 实现更多 **配置项** 与 **内置功能模块** 的可视化配置管理。

同时，该版本支持了小版本热升级，使用[版本热升级](https://docs.emqx.cn/cn/enterprise/latest/advanced/relup.html)功能，用户可以快速、安全地升级生产环境的 EMQ X Enterprise，避免因重启服务导致的系统可用性降低。

详细更新日志：https://www.emqx.io/cn/changelogs/enterprise/v4.2.0

### 模块（全新功能）

**模块旨在于替代之前的插件功能，4.2.0 版本之后 EMQ X 插件将置于长期维护状态，不再新增功能。**

同插件一样， **模块** 用于 EMQ X 的功能扩展，其特点是 **「按需添加管理，动态可视化配置」**。

![image20201019175559015.png](https://static.emqx.net/images/903d449fa0730af1efc10bffb0631df6.png)


模块结合 EMQ X 分布式集群特点，解决了插件开发、使用中的各种痛点：

- **插件配置文件难以维护**：插件是基于节点的，EMQ X 集群部署时每个节点本地都有一份插件配置文件，配置文件只能在本地通过文件修改，而在模块中，配置项的变更是集群同步的。
- **插件配置上手难度高**：模块通过 Dashboard 提供了可视化配置，降低上手难度；部分配置项支持热更新，比如用户可以方便地添加 MQTT-SN 监听端口、更改认证 SQL 语句。
- **插件停启操作不方便**：集群中使用 API 与 CLI 停启插件时只能逐个节点进行操作，如果操作有遗漏，极有可能引发生产事故。
- **版本升级困难**：EMQ X 插件数量与配置项比较多，跨版本升级时如果插件配置项有变动，升级会有一定的困难；模块的配置项易于程序读写和人工维护，EMQ X 后续可以提供升级迁移相关的自动化工具，降低版本升级难度。

**模块**将 EMQ X 的易用性提升了一个台阶，通过模块用户能够更快地将业务与物联网设备同 EMQ X 进行集成，缩短研发周期，降低学习、开发与维护难度。

### 规则引擎

[EMQ X 规则引擎](https://docs.emqx.net/enterprise/latest/cn/rule/rule-engine.html)用于配置消息流与设备事件的处理、转发规则， **支持将数据转发到包括 Kafka、Clickhouse 在内的多种数据库、流处理与数据分析系统中，快速构建一站式物联网数据集成，清洗，存储，分析，可视化平台。** 

作为 EMQ X 重磅功能，规则引擎基于 SQL 提供了清晰、灵活的 "配置式" 的业务集成方案，简化了业务开发流程，提升用户易用性并降低业务系统与 EMQ X 的耦合度。

4.2.0 版本中规则引擎新增以下功能：

- **规则引擎 MySQL/MongoDB/Cassandra/Postgresql 资源支持 IPv6 和 SSL 连接**

- **规则引擎 「资源」 支持上传证书**

为了提高安全性，云服务商的部分应用资源默认仅支持 TLS 连接，如华为云 InfluxDB。规则引擎加入 IPv6 与 TLS 连接支持后，EMQ X 可以更好地使用云上资源、与云上应用集成。

EMQ X 支持在 Dashboard 上传 SSL 证书，方便管理相关资源的 SSL 证书。

![image20201019174820927.png](https://static.emqx.net/images/8de954c6c9e5c1ec00aecea5d8826580.png)



**规则引擎「动作」分组**

随着规则引擎的功能增多，创建、管理规则引擎的 **动作** 变得复杂。此版本中 Dashboard 对规则引擎的动作进行了分类，方便用户快速定位所需的功能。

![image20201019175055630.png](https://static.emqx.net/images/269208ac8350a2a6bc739e1f12c6dc53.png)



### 支持更多热配置参数

此前版本中 EMQ X 已经支持绝大部分参数的热配置，本次更新我们新增了监听器以及监控告警阈值相关配置，用户可以在 Dashboard 上动态管理监听端口。

![image20201019175732628.png](https://static.emqx.net/images/4d3e6d3a95bc2e0d9a5d066e42f12605.png)



### 小版本号之间热升级

使用版本热升级功能，用户可以快速、安全地升级生产环境的 EMQ X，并避免了因重启服务导致的系统可用性降低。

目前 EMQ X 仅支持 Patch 版本（Patch 版本是版本号的第三位）的热升级。 即，目前支持 4.2.0 -> 4.2.1，4.2.0 -> 4.2.2 等的热升级，但 4.2.x 暂时无法热升级到 4.3.0 或者 5.0。

热升级步骤说明详见文档[ EMQ X  版本热升级](https://docs.emqx.cn/cn/broker/latest/advanced/relup.html)。



### 功能调整

- 移除 emqx_auth_username 和 emqx_auth_clientid 插件。
- 重构emqx_auth_mnesia,兼容老版本 emqx_auth_username 和 emqx_auth_clientid 的数据导入。
- EMQ X 主配置文件拆分，并且支持 include 配置文件，详细变动见 `etc/emqx.conf` 文件。



### 问题修复

- 修复 InfluxDB 不支持有下划线字符

