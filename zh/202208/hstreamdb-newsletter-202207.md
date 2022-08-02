本月，HStreamDB 团队主要在进行 v0.9 的最后开发和发布准备工作，对 v0.9 即将带来的 stream 分区模型改进、新集群机制、HStream IO 等新特性进行了进一步的完善和测试，同时也将主要的客户端升级到适配 v0.9。

## Stream 分区模型改进

在之前版本中，HStreamDB 采用透明分区模型，每个 stream 内的分区数是根据写入负载的情况动态调整的，且 stream 内部的分区对用户不可见。这种模型的优势在于保持用户概念简单性的同时也保留了实现的灵活性，能够做到随负载动态伸缩分区数量，且在伸缩过程中保持需要的数据顺序性。

当前这一模型的主要缺点在于用户无法直接进行分区级的操作和精细化控制，比如无法直接从任意位置读取某个分区的数据。为此，我们决定将开放分区的操作和控制能力给到用户，使用户可以：

- 通过 `partitionKey` 控制数据在分区之间的路由
- 直接从指定位置读取任意 shard 的数据
- 手动控制 stream 内分区的动态伸缩

在实现上，HStreamDB 采用的是 key-range-based 分区机制， stream 下的所有 shard 共同划分整个 key space，每个 shard 归属一段连续的子空间（key range），shard 的扩展与收缩对应子空间的分裂与合并。同时分区的伸缩不会造成老数据的复制和迁移，而是引起父分区的封闭，新数据会自动进入子分区，但与此同时父分区的数据依然是可读的。基于这种设计， 分区的动态伸缩将会更加可控、快速， 而且不会带来由于老数据的重分布引起的低效和影响数据顺序等问题，这实际也是透明分区的内部工作机制。

上述的分区模型改进将包含在即将发布的 v0.9 中（暂不包含控制分区分裂和合并的能力）。

## HStream IO 更新

HStream IO 是 HStreamDB v0.9 即将发布一个内部数据集成框架，包含 source connectors、sink connectors、IO runtime 等组件，它能够实现 HStreamDB 和多种外部系统的互联互通，从而助力促进数据在整个企业数据栈内的高效流转以及实时价值释放。

继上月我们新增了对多个数据库的 cdc source 支持后， 本月我们新增了对 MySQL 和 PostgreSQL 的 sink connector 支持，另外也对 embbed IO runtime 在 connector 参数检查、 配置文档生成以及任务安全退出等方面进行了改进和增强，同时也提供了 SQL commands 方便用户通过 CLI 创建和管理 IO task，示例如下：

```
create source connector source01 from mysql with ("host" = "127.0.0.1", "port" = 3306, "user" = "root", "password" = "password", "database" = "d1", "table" = "t1", "stream" = "stream01");

create sink connector sink01 to postgresql with ("host" = "127.0.0.1", "port" = 5432, "user" = "postgres", "password" = "postgres", "database" = "d1", "table" = "t1", "stream" = "stream01");

show connectors;

pause connector source01;

resume connecctor source01;

drop connector source01;
```

## HStream MetaStore

目前 HStreamDB 使用 Zookeeper 存储系统内的元数据，比如 shard 的复制属性和集群节点的任务分配和调度信息等，这给 HStreamDB 的部署和运维带来了一些额外的复杂性，如部署需要依赖 JVM，要单独管理 Zookeeper 集群等。

为此，我们计划移除 HStreamDB 对 Zookeeper 的直接依赖，并引入专门的 HStream MetaStore 组件（简称 HMeta）。HMeta 将提供一组抽象的元数据存储接口，理论上可基于多种存储系统来实现。目前我们正在开发提基于 rqlite [[https://github.com/rqlite/rqlite](https://github.com/rqlite/rqlite) ]的默认实现。rqlite 基于 SQLite 和 raft，采用 Golang 编写，非常轻量，易于部署和管理。

HMeta 的开发工作还在持续进行中，如我们之前 newsletter 中提到的， HServer 的新集群机制已经不再依赖 Zookeeper ， 本月我们也已经实现了将 HStore 的 EpochStore 迁移到 HMeta。这项特性将不会纳入即将发布的 v0.9 中，它还需要更多的测试，我们计划在 v0.10 中正式发布它。

## 客户端更新

本月客户端也在适配 HStreamDB v0.9 方面带来了多项升级，以 hstreamdb-java 为例，主要包含以下改动：

- `createStream` 可指定初始分区数
- 增加 `listShards` 方法
- `producer` 和 `bufferedProducer` 适配新的分区模型
- 增加 `Reader` 类，可用来读取任意分区

其它语言的客户端（Golang、Python）也将包含对 v0.9 的支持。

## 其它

本月完成的其它一些值得关注的特性包括：

- HServer 新增 `advertised-listeners`配置，该配置用于解决 HStreamDB 部署在复杂网络环境下时外部 client 访问 HStreamDB 的问题。

- 改进了 HServer 集群启动时的 bootstrap 流程。
