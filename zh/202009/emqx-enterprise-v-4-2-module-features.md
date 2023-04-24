**在即将到来的 v4.2 版本中，EMQX 企业版**提供了 **模块** 功能，用于替代之前的 **插件** 。该版本之后插件将置于长期维护状态，不再新增功能。
![1.png](https://assets.emqx.com/images/d3056829973a659d92fb3b8c5edfe459.png)




## 为什么采用新的模块功能

同插件一样， **模块** 用于 EMQX 的功能扩展，与插件不同的是，模块结合 EMQX 分布式集群特点，解决了插件开发、使用中的各种痛点：

- **插件配置文件难以维护**：插件是基于节点的，EMQX 集群部署时每个节点本地都有一份插件配置文件，配置文件只能在本地通过文件修改，而在模块中，配置项的变更是集群同步的。
- **插件配置上手难度高**：模块通过 Dashboard 提供了可视化配置，降低上手难度；部分配置项支持热更新，比如用户可以方便地添加 MQTT-SN 监听端口、更改认证 SQL 语句。
- **插件停启操作不方便**：集群中使用 API 与 CLI 停启插件时只能逐个节点进行操作，如果操作有遗漏，极有可能引发生产事故。
- **版本升级困难**：EMQX 插件数量与配置项比较多，跨版本升级时如果插件配置项有变动，升级会有一定的困难；模块的配置项易于程序读写和人工维护，EMQX  后续可以提供升级迁移相关的自动化工具，降低版本升级难度。

**模块**将 EMQX 的易用性提升了一个台阶，通过模块用户能够更快地将业务与物联网设备同 EMQX 进行集成，缩短研发周期，降低学习、开发与维护难度。



## 模块概览

EMQX 模块按照功能组织，分为以下几类：

### 认证鉴权

客户端连接到 EMQX、发布/订阅主题的时候可以使用认证鉴权模块进行身份与权限验证。

认证鉴权模块支持文件、内置数据库、JWT、外部主流数据库和自定义 HTTP API 等数据源，支持动态更改认证逻辑（如查询 SQL），动态添加、删除认证链。
![认证鉴权.png](https://assets.emqx.com/images/73679e9f0b6019b7faba35b21630c861.png)



### 协议接入

除了标准 MQTT 协议（完整 QoS 与 MQTT 5.0 支持），EMQX 还扩展了一系列的物联网协议，支持的协议包括MQTT-SN、CoAP/LwM2M、HTTP、WebSocket、STOMP、私有 TCP、JT/T808 行业协议等。

在协议接入相关模块中，用户能够快速启用需要的扩展协议，动态增改协议的监听端口，以及协议与 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)的挂载关系。

![协议接入.png](https://assets.emqx.com/images/98273b92dcb3459e4e7bf40de2145109.png)



### 消息下发

服务端下发指令到设备是物联网应用中常用的场景，EMQX 提供多种消息下发方式，针对下行流量较大的项目，用户可以使用消息下发模块配置消费 Kafka 或 Pulsar 进行消息下发，模块能够方便地配置数据源以及 Kafka-MQTT、Pulsar-MQTT 的主题映射关系，实现高吞吐、事务级的服务端消息下发。

![消息下发.png](https://assets.emqx.com/images/98ab2bd2917fc74ff9017c8e43731bd7.png)



### 多语言扩展

包含 Python 与 Java 的扩展支持，开发者可以使用 Python 或者 Java 快速开发自己的插件，在官方功能的基础上进行扩展，满足自己的业务场景。

多语言扩展中包含两个模块， **exproto** 模块用于协议扩展，可以使用 Java/Python 驱动实现特定的协议支持， **exhook** 模块基于 EMQX 钩子，用户可使用 Python 和 Java 直接处理 EMQX 各类事件，实现设备上下线、认证、ACL 规则控制，消息桥接和持久化等功能。



### 运维监控

EMQX 提供 Prometheus Agent 模块，用于将 EMQX 运行指标及 Erlang 虚拟机状态数据输出到第三方的监控如 Prometheus 中。通过 Prometheus 自带的 node-exporter 还可以采集 Linux 服务器相关指标，实现服务器 + EMQX 整体运维监控。

此外，运维监控还包含代码热加载、性能调试模块，借助两个模块可以很方便地进行测试调优，服务器调整。



### 内部模块

现版本有6 个内部模块，主要围绕 MQTT 协议使用进行功能拓展：

#### MQTT 增强认证

基于更强的安全性考虑，MQTT v5 增加了新特性 **增强认证**，[增强认证](https://www.emqx.com/zh/blog/mqtt5-enhanced-authentication)包含质询/响应风格的认证，可以实现对客户端和服务器的双向认证，服务器可以验证连接的客户端是否是真正的客户端，客户端也可以验证连接的服务器是否是真正的服务器，从而提供了更高的安全性。

增强认证依赖于认证方法和认证数据来完成整个认证过程，在增强认证中，认证方法通常为 [SASL（ Simple Authentication and Security Layer )](https://zh.wikipedia.org/zh-hans/简单认证与安全层) 机制，使用一个注册过的名称便于信息交换。但是，认证方法不限于使用已注册的 SASL 机制，服务器和客户端可以约定使用任何质询 / 响应风格的认证。

#### 上下线通知

启用该模块后，客户端上下线时将在[系统主题](https://www.emqx.io/docs/zh/latest/advanced/system-topic.html)上发布一条通知消息，订阅相应的主题即可获取上下线客户端事件与客户端信息。

> Webhook 插件、规则引擎同样支持设备上下线事件处理，用户可以根据自己的需要选择不同的方式进行业务开发集成。

#### MQTT 代理订阅

该模块可以配置代理订阅信息，模块启用后，EMQX 将在客户端连接成功时自动订阅模块配置的主题，无需客户端主动发起订阅。

#### 主题重写

该模块可以配置重写规则，在客户端发布/订阅主题时将目标主题按照规则重写为新的主题。

EMQX 的 [保留消息](https://docs.emqx.com/zh/enterprise/latest/modules/retainer.html) 和 [延迟发布](https://www.emqx.io/docs/zh/latest/advanced/delay-publish.html) 可以与[主题重写](https://www.emqx.com/zh/blog/rewriting-emqx-mqtt5-topic)配合使用，例如，当用户想使用延迟发布功能，但不方便修改客户端发布的主题时，可以使用主题重写将相关主题重写为延迟发布的主题格式。

#### MQTT 保留消息

用于 EMQX 中 MQTT 保留消息的管理，可以配置存储位置、有效期、消息大小等参数。禁用此模块且没有启用其他保留消息功能，EMQX 将不支持保留消息。

![MQTT 保留消息.png](https://assets.emqx.com/images/6cff9581c968d03e83e29d68b5601ff7.png)



#### 延迟发布

EMQX 的延迟发布功能可以实现按照用户配置的时间间隔延迟发布 PUBLISH 报文的功能。当客户端使用特殊主题前缀 `$delayed/{DelayInteval}` 发布消息到 EMQX 时，将触发延迟发布功能。



该版本将于近期发布，敬请期待。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a >
</section>
