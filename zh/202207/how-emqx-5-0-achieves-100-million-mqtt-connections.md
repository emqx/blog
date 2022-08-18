## 引言： 单集群 1 亿 MQTT 连接达成

不久前，大规模分布式物联网 MQTT 消息服务器 [EMQX 发布了 5.0 版本](https://www.emqx.com/zh/blog/emqx-v-5-0-released)。这一最新的里程碑版本采用新的后端存储架构 Mria 数据库，并重构了数据复制逻辑，因此 EMQX 5.0 水平扩展能力得到了指数级提升，能够更可靠地承载更大规模的物联网设备连接量。

在 EMQX 5.0 正式发布前的性能测试中，我们通过一个 23 节点的 EMQX 集群，全球首个达成了 1 亿 MQTT 连接+每秒 100 万消息吞吐，这也使得 EMQX 5.0 成为目前为止全球最具扩展性的 MQTT Broker。

本文将对使 EMQX 水平扩展能力得到指数级提升的全新底层架构进行详细解析，帮助大家理解 EMQX 5.0 集群扩展的技术原理，以及在不同的实际应用场景中如何选择合适的部署架构，实现更加可靠的设备接入与消息传输。

![100 millions MQTT connections testing result](https://assets.emqx.com/images/b966f76082acbfbf8b20d1660a1d34fa.png)

<center>100 million MQTT connections testing result</center>

> 测试详情可参考：[https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)


## 4.x 时代：使用 Mnesia 构建 EMQX 集群

### Mnesia 介绍

EMQX 4.x 版本存储采用的是 Erlang/OTP 自带的分布式数据库 [Mnesia](https://www.erlang.org/doc/man/mnesia.html) ，它具备以下优点：

- **Embedded：** 和 MySQL、PostgeresSQL 等数据库不同，Mnesia 和 EMQX 是运行在同一个操作系统进程的（类似于 SQLite）。因此 EMQX 可以以非常快的速度读取路由、会话等相关信息。
- **Transactional：** Mnesia 支持事务且具有 ACID 保证。而且这些保证是针对整个集群所有节点生效的。EMQX 在数据一致性很重要的地方使用 Mnesia 事务，例如更新路由表、创建规则引擎规则等。
- **Distributed：** Mnesia 表会复制到所有 EMQX 节点。这能提高 EMQX  的分布式的容错能力，只要保证一个节点存活数据就是安全的。
- **NoSQL：** 传统的关系型数据库使用SQL与数据库进行交互。而 Mnesia 直接使用 Erlang 表达式和内置的数据类型进行读写，这使得与业务逻辑的整合非常顺利，并消除了数据编解码的开销。

在 Mnesia 集群中，所有节点都是平等的。它们中的每一个节点都可以存储一份数据副本，也可以启动事务或执行读写操作。

Mnesia 集群使用全网状拓扑结构：即每个节点都会与集群中其它所有的节点建立连接，每个事务都被会复制到集群中的所有节点。如下图所示：

![Mnesia 网状拓扑](https://assets.emqx.com/images/4584d7f6b3f31f5c7a2ccfbfbd1dd43c.png)

### Mnesia 的问题

正如我们上面所讨论的，Mnesia 数据库有很多非常显著的优点，EMQX 也从中获得了非常大的收益。但其全连接的特性，**限制了其集群的水平扩展能力，因为节点之间的链接数量随着节点数量的平方而增长，保持所有节点完全同步的成本越来越高，事务执行的性能也会急剧下降**。

这意味着 EMQX 的集群功能有以下限制:

- **水平扩展能力不足。** 在 4.x 我们不建议在集群节点过多，因为网状拓扑中的事务复制的开销会越来越大；我们一般建议是使用节点数保持在 3 ~ 7 个，并尽量提供单节点的性能。
- **节点数增多会增大集群脑裂的可能性**。节点数越多、节点间的链接数也会急剧增多，对节点间的网络稳定性的要求更高。当产生脑裂后，节点自愈会导致节点重启并有数据丢失的风险。

尽管如此，EMQX 凭借独特的架构设计和 Erlang/OTP 强大的功能特性，实现了单个集群 1000 万 MQTT 连接的目标。同时，EMQX 能够以集群桥接的方式，通过多个集群承载更大规模的物联网应用。但随着市场的发展，单个物联网应用需要承载越来越多的设备和用户，EMQX 需要具备更强大的扩展性和接入能力，以支持超大规模物联网应用。

## 5.x 时代：使用 Mria 构建大规模集群

[Mria](https://github.com/emqx/mria) 是 Mnesia 的一个开源扩展，为集群增加了最终的一致性。前文所述的大多数特性仍然适用于它，区别在于数据如何在节点间进行复制。 Mria 从**全网状**拓扑结构转向**网状+星型状**拓扑结构。每个节点承担两个角色中的一个：**核心节点（Core）**或**复制者节点（Replicant）**。

![Mria 核心-复制节点拓扑](https://assets.emqx.com/images/274a84a5be9c44075ae3b467f49beee6.png)

### Core 和 Replicant 节点行为

**Core 节点**的行为与 4.x 中的 Mnesia 节点一致：Core 节点使用全连接的方式组成集群，每个节点都可以发起事务、持有锁等。因此，EMQX 5.0 仍然要求 Core 节点在部署上要尽量的可靠。

**Replicant 节点**不再直接参与事务的处理。但它们会连接到 Core 节点，并被动地复制来自 Core 节点的数据更新。Replicant 节点不允许执行任何的写操作。而是将其转交给 Core 节点代为执行。另外，由于 Replicant 会复制来自 Core 节点的数据，所以它们有一份完整的本地数据副本，以达到最高的读操作的效率，这样有助于降低 EMQX 路由的时延。

我们可以将这种数据复制模型当做**无主复制和主从复制**的一种混合。这种集群拓扑结构解决了两个问题：

- 水平可扩展性（如前文提到，我们已经测试了有 23 个节点的 EMQX 集群）
- 更容易的集群自动扩展，并无数据丢失的风险。

由于 Replicant 节点不参与写操作，当更多的 Replicant 节点加入集群时，写操作的延迟不会受到影响。这允许创建更大的 EMQX 集群。

另外，Replicant 节点被设计成是无状态的。添加或删除它们不会导致集群数据的丢失、也不会影响其他节点的服务状态，所以 Replicant 节点可以被放在一个自动扩展组中，从而实现更好的 DevOps 实践。

出于性能方面的考虑，不相干数据的复制可以被分成独立的数据流，即多个相关的数据表可以被分配到同一个 RLOG Shard（复制日志分片），顺序地把事务从 Core 节点复制到 Replicant 节点。但不同的 RLOG Shard 之间是异步的。

## EMQX 5.0 集群部署实践

### 集群架构选择

在 EMQX 5.0 中，所以如果不做任何调整的话所有节点都默认为 Core 节点，默认行为和 4.x 版本是一致的。

可以通过设置 `emqx.conf` 中的 `node.db_role` 参数或 `EMQX_NODE__DB_ROLE` 环境变量，把节点上设置为 Replicant 节点。

> 请注意，集群中至少要有一个核心节点，我们建议以 3 个 Core + N 个 Replicant 的设置作为开始

Core 节点可以接受 MQTT 的业务流量，也可以纯粹作为集群的数据库来使用。我们建议：

- 在小集群中（3 个节点或更少），没有必要使用 Core + Replicant 复制模式，可以让 Core 节点承担所有的流量，避免增加上手和使用的难度。
- 在超大的集群中（10 个节点或更多），建议把 MQTT 流量从 Core 节点移走，这样更加稳定性和水平扩展性更好。
- 在中型集群中，取决于许多因素，需要根据用户实际的场景测试才能知道哪个更优。

**异常处理**

Core 节点对于 Replicant 节点是无感的，当某一 Core 节点宕机时，Replicant 节点会自动连接到新的 Core 节点，此过程中客户端不会掉线，但可能导致路由更新延迟；当 Replicant 节点宕机时，所有连接到该节点的客户端会被断开，但由于 Replicant 是无状态的，所以不会影响到其他节点的稳定性，此时客户端需要设置重连机制，连接至另一个 Replicant 节点。

### 硬件配置要求

**网络**

Core 节点之间的网络延迟建议 10ms 以下，实测高于 100ms 将不可用，请将 Core 节点部署在同一个私有网络下；Replicant 与 Core 节点之间同样建议部署在同一个私有网络下，但网络质量要求可以比  Core 节点间略低。

**CPU 与内存**

Core 节点需要较大的内存，在不承接连接的情况下，CPU 消耗较低；Replicant 节点硬件配置与 4.x 一致，可按连接和吞吐配置估算其内存要求。

### 监控和调试

对 Mria 的性能监控可以使用 Prometheus 或使用 EMQX 控制台查看。 Replicant 节点在启动过程中会经历以下状态：

- **bootstrap**：当 Replicant 节点启动后，需要从 Core 节点同步最新数据表的过程
- **local_replay**：当节点完成 bootstrap 时，它必须重放这个过程中产生的的写事务
- **normal**：当缓存的事务被完全执行后，节点即进入到正常运行的状态。后续的写事务被实时地应用到当前节点。大多数情况下，Replicant 节点都会保持在这个状态。

#### Prometheus 监控

**Core 节点**

- `emqx_mria_last_intercepted_trans`: 自节点启动以来，分片区收到的交易数量。请注意，这个值在不同的核心节点上可能是不同的。
- `emqx_mria_weight`: 一个用于负载平衡的值。它的变化取决于核心节点的瞬间负载。
- `emqx_mria_replicants`：连接到核心节点的复制器的数量，为给定的分片复制数据。
- `emqx_mria_server_mql`: 未处理的交易数量，等待发送至复制者。越少越好。如果这个指标有增长的趋势，需要更多的核心节点。

**Replicant 节点**

- `emqx_mria_lag`：复制体滞后，表示复制体滞后上游核心节点的程度。越少越好。
- `emqx_mria_bootstrap_time`：复制体启动过程中花费的时间。这个值在复制体的正常运行过程中不会改变。
- `emqx_mria_bootstrap_num_keys`：在引导期间从核心节点复制的数据库记录的数量。这个值在复制体的正常运行中不会改变。
- `emqx_mria_message_queue_len`：复制进程的消息队列长度。应该一直保持在0左右。
- `emqx_mria_replayq_len`: 复制体的内部重放队列的长度。越少越好。

#### 控制台命令

`./bin/emqx eval mria_rlog:status().` 可以获取关于 Mria 数据库运行状态的更多信息。

> 注：它可以显示一些 shard 为 `down` 状态，这表明这些分片没有被任何业务应用使用。

## 结语

全新的底层架构使 EMQX 5.0 具备了更强的水平扩展能力，在构建满足用户业务需求的更大规模集群的同时，可以降低大规模部署下的脑裂风险以及脑裂后的影响，有效减少集群维护开销，为用户提供更加稳定可靠的物联网数据接入服务。


<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>


> **参考资料：**
>
> - [Challenges and Solutions of EMQX horizontal scalability - MQTT broker clustering part 3](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)
>
> - [高度可扩展，EMQX 5.0 达成 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)


## 本系列中的其它文章

- [EMQX 5.0 产品解读 02 | MQTT over QUIC：物联网消息传输还有更多可能](https://www.emqx.com/zh/blog/mqtt-over-quic)
- [EMQX 5.0 产品解读 03 | 基于 RocksDB 实现高可靠、低时延的 MQTT 数据持久化](https://www.emqx.com/zh/blog/mqtt-persistence-based-on-rocksdb)
- [EMQX 5.0 产品解读 04 | 全新物联网数据集成 ：Flow 可视化编排 & 双向数据桥接](https://www.emqx.com/zh/blog/iot-data-integration)
- [EMQX 5.0 产品解读 05 | 灵活多样认证授权，零开发投入保障 IoT 安全](https://www.emqx.com/zh/blog/securing-the-iot)
