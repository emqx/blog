我们很高兴地宣布：[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.15 和 4.4.16 版本现已正式发布！

本次发布增加了 Apache IoTDB 集成支持以满足工业制造海量数据存储与分析的需求，同时对最新版本的 HStreamDB（v0.14.0）和 MongoDB（v6.0）进行了适配，用户可以根据业务需要轻松与相应的第三方数据库对接，实现物联网数据的持久化与进一步处理。除此之外，我们还修复了多项 BUG。

## 新增 Apache IoTDB 数据集成

[Apache IoTDB](https://iotdb.apache.org/zh/)（物联网数据库）是一体化收集、存储、 管理与分析物联网时序数据的软件系统，具有高吞吐量读写、高效树形元数据结构、丰富查询语义、低硬件成本、灵活部署以及与开源生态系统紧密集成等特点。

EMQX Enterprise 4.4.15 提供了 Apache IoTDB 的支持，包括 0.13.x 以及 1.x 版本。借助 EMQ 提供的边缘工业协议网关软件 Neuron 与 EMQX 的组合，可以实现工业设备的接入，并通过规则引擎将采集到的海量、高频工业实时数据存储到 Apache IoTDB 中，进一步实现海量数据存储、高速数据读取和复杂数据分析需求。详细可参考 [EMQ 工业制造解决方案](https://www.emqx.com/zh/solutions/industries/manufacturing)。

## HStreamDB 最新版适配

本次发布中，EMQX Enterprise 规则引擎适配了 [HStreamDB](https://hstream.io/zh) 最新版本 v0.14.0。

相较于此前支持的 0.8 版本，HStreamDB 后续版本改进了集群架构，新增了 stream 分区、HStream IO 数据集成框架、 端到端压缩等重大特性，提供了 HStream Operator 以简化运维管理，并为 HStream SQL 增加了更多丰富的查询语句，更多内容请参考 [HStreamDB Release Note](https://hstream.io/docs/zh/latest/release_notes/HStreamDB.html)。与最新版本 HStreamDB 的集成，使得用户可以利用 EMQX+HStreamDB 的组合实现海量物联网流数据的存储和实时处理。

有关 EMQX Enterprise 与 HStreamDB 最新版本的集成教程，可参考：[EMQX+HStreamDB 实现物联网流数据高效持久化](https://www.emqx.com/zh/blog/integration-practice-of-emqx-and-hstreamdb) 

此外，该版本中 HStreamDB 数据集成还支持了 SSL/TLS 连接。

## MongoDB 6.0 支持

为认证、发布订阅 ACL、规则引擎等功能适配了 MongoDB 6.0。

MongoDB 6.0 提供了多项适用于物联网的特性，包括增强的时序集合，能够更高效地写入和查询数据；增强的 Change Stream 能够实现物联网数据存储、实时监测传感器数据变化、更新设备状态等；新增的柱状压缩能够减少存储空间的使用，适用于物联网更大规模的数据存储，更多内容请参考 [MongoDB 6.0 Release Note](https://www.mongodb.com/docs/manual/release-notes/6.0/)。

## 数据集成 Kafka 支持 Headers

规则引擎 Kafka 集成支持动态设置 Headers。

Kafka Headers 用于在消息中添加键值对组成的元数据，用来标识消息的类型、来源、目标、时间戳等信息。例如，您可以将客户端属性或 MQTT 5.0 User Property 通过 Headers 透传，并在业务侧进行消息路由、过滤、监控和跟踪等操作，实现更灵活的业务开发。

## 数据集成 RocketMQ 支持设置生产者投递策略

规则引擎 RocketMQ 支持按客户端 ID、用户名或主题将消息投递到同一队列中。

RocketMQ 生产者投递消息时可以设置轮询、哈希、随机或自定义等不同方式的投递策略。此前版本中 EMQX Enterprise 采用了轮询算法进行消息投递，同一来源的消息可能会被投递到不同的队列中导致消费顺序错乱，现在您可以设置投递策略，确保数据消费时的顺序性。

## Prometheus 新增活跃客户端统计指标

在 EMQX Enterprise 中，客户端的总数为仍然保持连接的客户端（即活跃客户端）、已断开连接但保留会话的客户端之和，其状态分别为 “已连接” 和 “已断开”。

在某些情况下，活跃客户端更能准确地反映业务运行情况，因此我们在 Prometheus 集成添加了 `live_connections.count` 和 `live_connections.max` 两个指标，分别表示当前活跃客户端数量和历史最大活跃客户端数量。

## BUG 修复

以下是主要 BUG 修复，完整 BUG 修复列表请参考 [EMQX 企业版 4.4.15 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.15) 与 [EMQX 企业版 4.4.16 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.16)。

- 修复 Redis 离线消息顺序问题，此前该功能会以相反顺序发送离线消息。
- 修复重启之后初始化失败的模块会被禁用的问题。
- 修复热升级后，规则引擎 Oracle 数据库无法自动重连的问题。
- 修复规则引擎无法支持 RocketMQ 集群的问题。
- 修复使用**消息重发布**动作转发带 User-Property 的 MQTT 消息时出错的问题 [#9942](https://github.com/emqx/emqx/pull/9942)。
- 使用 HTTP API 分页请求客户端列表时，当请求发送到不同的 EMQX 节点返回的客户端列表可能不一致的问题 [#9926](https://github.com/emqx/emqx/pull/9926)。
- 修复排他订阅在会话关闭后主题没有被释放的问题 [#9868](https://github.com/emqx/emqx/pull/9868)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
