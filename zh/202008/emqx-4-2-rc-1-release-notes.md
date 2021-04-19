

EMQ X Broker 4.2-rc.1 正式发布，欢迎大家下载试用，下载地址：https://github.com/emqx/emqx/releases/tag/v4.2-rc.1。 如果您想要与我们分享反馈意见，或者遇到任何问题需要帮助，可以通过 https://github.com/emqx/emqx/issues 与我们交流。

> EMQ X Broker 是一款高并发低延迟，支持分布式集群架构的开源 MQTT 消息服务器，支持单机百万连接，更多信息请访问：https://www.emqx.cn/products/broker



![Artboard.png](https://static.emqx.net/images/d2580244a5c143994f4f74a8b48723fb.png)

### 更新说明

- 【新增】支持使用第三方语言编写扩展插件接入其他非 MQTT 协议，目前已支持 Java 和 Python 两种编程语言。访问 https://github.com/emqx/emqx-exproto/blob/master/README.md 获取更多相关信息
- 【新增】支持修订版本间的热更新
- 【新增】新增遥测功能，收集有关 EMQ X Broker 使用情况的信息以帮助我们改进产品，此功能默认开启，支持手动关闭。访问 https://docs.emqx.io/broker/latest/en/advanced/telemetry.html 获取更多遥测相关信息。
- 【新增】规则引擎支持为 MQTT 桥接创建订阅
- 【新增】规则引擎支持功能更加强大的 SQL 语法
- 【新增】MySQL、PostgreSQL 等插件全面支持 IPv6、SSL/TLS
- 【新增】支持消息流控
- 【新增】支持 CentOS 8、Ubuntu 20.04 操作系统和 ARM64 系统架构
- 【新增】Webhook 支持配置自定义的 HTTP 头部
- 【优化】更加友好的告警机制，为开发者提供 HTTP API
- 【优化】优化保留消息性能
- 【调整】后续版本不再支持 Debian 8、Ubuntu 14.04 和 Raspbian 8 操作系统
- 【调整】`emqx-statsd` 插件正式更名为 `emqx-prometheus`
- 【调整】发布与订阅支持独立配置主题重写规则
- 【调整】允许用户配置是否允许 WebSocket 消息包含多个 MQTT 报文，以兼容部分客户端
- 【修复】修复主题指标中存在的问题
- 【修复】修复 LwM2M 插件没有正确获取协议版本的问题



### 5.0 发布计划

EMQ X 开源研发团队已正式进入 5.0 的开发阶段，5.0 版本将作为 5G 大基建超大规模多协议超融合接入平台，拥有更加健壮的全新架构、更加强大的性能以及更加流畅的使用体验，它将为您带来：

- 支持更快的 QUIC 协议
- 领先的 NB-IoT 网络与 LwM2M 支持
- 50+ 节点的大规模集群
- K8S 下集群弹性伸缩
- 极简化的全新配置方式
- 全新的消息路由架构
- 更强的消息路由性能
- 更加强大易用的 API，等等...

欢迎在 https://github.com/emqx/emqx 上关注我们，以随时了解我们的最新研发进度。