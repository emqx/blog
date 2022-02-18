开源物联网 MQTT 服务器 [EMQX Broker](https://www.emqx.com/zh/products/emqx) 是基于高并发的 Erlang/OTP 语言平台开发，支持百万级连接和分布式集群架构。EMQX Broker 已经在全球物联网市场广泛应用，无论是产品原型设计、物联网创业公司、还是大规模的商业部署，都支持免费使用。

现在，EMQX Broker 已发布至 v4.1-beta.1 版本，此版本重点增加了对 Python 与 Java 的扩展支持。EMQX Broker 支持通过插件来扩展功能，但在此之前，仅支持由 Erlang 编写的插件，对开发者而言使用门槛较高。即使官方提供了 Lua 脚本扩展支持，但也仅支持简单场景。现在，开发者可以使用 Python 或者 Java 快速开发自己的插件，在官方功能的基础上进行扩展，满足自己的业务场景。

EMQX Broker 的多语言扩展通过 `emqx-extension-hook` 插件中的驱动（Driver）实现，不同的编程语言由不同类型的驱动提供支持。目前的 Python 和 Java 驱动基于 `Erlang/OTP - Port`（https://erlang.org/doc/tutorial/c_port.html） 进程间通信实现，所以驱动本身具有非常高的吞吐性能。

![361588066850_.pic.jpg](https://static.emqx.net/images/21ff6cd7a9d18d2926c662fe4dde8fe1.jpg)

除此之外，v4.1-beta.1 还增加了规则引擎的暂停与编辑等功能，欢迎大家[下载 EMQX](https://www.emqx.com/zh/downloads?product=broker) 使用。

### v4.1-beta.1 改进详情

#### 功能增强

- 支持多语言插件扩展

  用户可使用 Python 和 Java 直接处理 EMQX Broker 的各类事件，包含上下线、认证、ACL 规则控制，消息桥接和持久等功能。

- 支持客户端与订阅的模糊查询与多条件查询

  支持以 Client ID、Username 模糊查找客户端，或按协议类型，连接时间段等筛选客户端。支持按 Client ID、 QoS、主题等筛选订阅。

- 规则引擎支持暂停和编辑

  提高规则引擎的使用友好性，用户可以随时启停指定规则，需要修改规则时可以直接编辑，不再需要先删除再创建。

- 支持服务端到客户端的主题别名

  现在，不仅仅是客户端发布消息到服务端时可以使用主题别名，服务端转发消息到客户端时，也可以使用主题别名，最大程度地减少流量消耗。

- 支持跨版本数据迁移

  提供命令行接口，支持迁移的数据包括：规则引擎已创建的资源和规则信息、黑名单信息和存储在 Mnesia 数据库的认证信息等。

- 支持基于主题的指标统计

  支持指定主题的消息收发数量与速率的统计。

- Dashboard 提供内置模块管理页面

  目前存在延迟发布、内置 ACL、上下线通知、[主题重写](https://www.emqx.com/zh/blog/rewriting-emqx-mqtt5-topic)、代理订阅与主题指标共六个内置模块，都支持通过 Dashboard 或 HTTP API 动态加载和卸载。

- 支持 MQTT [增强认证](https://www.emqx.com/zh/blog/mqtt5-enhanced-authentication)，已支持的认证算法包括：SCRAM-SHA-1

  现在可以使用 TLS/SSL 或增强认证来进行双向认证。

- 增加基于 Mnesia 内置数据库的认证插件

  支持 Client ID 与 Username 认证（注意 `emqx-auth-clientid` 与 `emqx-auth-username` 插件即将废弃）

- 为 CoAP、LwM2M 协议设备接入增加 IPv6 支持



### 错误修复

- 修复异常客户端检测功能没有删除过期数据导致特定场景下内存持续增长的问题
- 修复规则引擎的一些问题
- 修复 MQTT Bridge 默认情况下不会发送 PINREQ 报文的问题
- 修复内置 ACL 模块重新加载时没有清除 ACL 缓存的问题
- 修复 `emqx-statsd` 没有获取 EMQX Broker 指标的问题
- 修复使用 WebSocket 连接时 Proxy Protocol 不可用的问题
