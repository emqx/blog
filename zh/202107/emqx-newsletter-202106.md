近几周以来，我们一直在努力对 EMQX 5.0 版本规划加以明确。本月里我们完成了确定范围和优先级并开始投入开发这一具有挑战性的任务。目前来看，这一版本中将要实现和交付的功能变得愈发明朗。


## v5.0-alpha.1 发布


我们已经发布了第一个 alpha 版本，希望可以更早地从社区获得反馈。以下是一些突出的新功能：

### HOCON config + HOCON schema

一直关注我们每月项目 Newsletter 和 Demo Day 的朋友应该对 HOCON 已不再陌生。HOCON 或 Human-Optimized Config Object Notation 是一种更友好的配置文件格式，是 JSON 的超集。EMQX v5.0 将使用 HOCON  格式进行配置。HOCON schema 是 EMQX 团队开发的一个库/框架，用于提供类型安全的配置验证。此外，它还会用于 HTTP API  JSON 数据验证。我们相信通过统一两个管理接口（配置和 HTTP API）对用户和开发人员都有好处。

### EMQX 资源的基础设施代码

在 EMQX v5.0 中，认证数据库连接、规则引擎资源/操作等资源将可以从配置文件中部署。即便在运行时修改，例如来自 Web UI 或  HTTP API 的更新，也将保留在配置文件中。和以前将资源存储在 Mnesia 中的方式相比，这将使基础设施的部署变得更加容易。

### 可组合身份验证步骤

为了简化用户界面和实现，身份验证插件被合并到一个 Erlang 应用程序（AuthN 应用程序）中，这使得身份验证步骤可以组合为 HOCON 配置中的「链」。同步支持 EMQX v4.x  支持的所有后端仍然是一项持续的任务。目前完成的有：Mnesia、MySQL、PostgreSQL 和 JWT。

### 可组合授权步骤

为了支持可组合步骤的访问控制，ACL 或访问控制列表将包含在更通用的应用程序（AuthZ 应用程序）中。新界面（也是 HOCON 格式）类似于旧的 acl.conf，但可以扩展各种数据库后端以支持更具体的访问控制。

### MQTT-over-QUIC

自三月份以来，[QUIC](https://github.com/emqx/quic) 项目一直处在与 EMQX 主项目分离的开发中。现在它终于与 [emqx.git](https://github.com/emqx/emqx) 进行了集成。**MQTT-over-QUIC** 将作为实验性功能在 v5.0 中发布。接下来我们还将迎接很多挑战，欢迎与我们一同努力，去探索物联网 QUIC 协议的更多精彩之处。

### RLOG

[RLOG](https://github.com/emqx/eip/blob/main/implemented/0004-async-mnesia-change-log-replication.md)，或 Replicated (mnesia transaction) Logs，是一个旨在使 Erlang 的内置数据库 “Mnesia” 可扩展的项目。该项目的主要工作是三月起在 [ekka](https://github.com/emqx/ekka) 应用程序中开发的，目前也完成了与 [emqx.git](https://github.com/emqx/emqx) 的集成。

这一特性可以使一个 EMQX 集群得以配置两种类型的节点角色：core 和 replicant。core 节点形成传统的 Mnesia 集群，而 replicant 节点则是无状态的，并且可以轻松地扩展和缩减。

## 4.3 改进

在投入精力进行 v5.0 开发的同时，我们也仍然在积极维护 v4.3。在六月，我们发布了 v4.3.5，修复了一些插件问题。更多详细信息，可以参阅发行说明：[https://github.com/emqx/emqx/releases](https://github.com/emqx/emqx/releases)。
