## 引言：原生 MQTT 会话持久化支持

MQTT 协议标准中规定 Broker 必须存储离线客户端的消息。在之前的版本中，[EMQX 开源版](https://www.emqx.io/zh)采用了基于内存的会话存储，企业版则在此基础上进一步提供了外部数据库存储方案，借此实现数据持久化。

这种基于内存、非持久化的会话存储方式虽然是基于吞吐量和延迟之间相互权衡下的最优解，但在某些场景下仍会给用户使用带来一定的限制。

本着关注社区反馈、不断完善为用户带来更易用产品的理念，我们在 EMQX 5.x 的产品规划中增加了基于 RocksDB 的原生 MQTT 会话持久化支持。目前这一功能已进入正式开发阶段，预计将在 5.1.0 版本中和各位用户见面。

本文是对这一特性的抢鲜技术分享。通过对 [MQTT 会话](https://www.emqx.com/zh/blog/mqtt-session)相关概念以及 EMQX 会话持久化功能设计原理的介绍，帮助读者了解这一更加高可靠、低时延的数据持久化方案。同时，我们还将基于 RocksDB 持久化能力进行更多新功能探索。

## 了解 MQTT 会话

在协议规范中，QoS 1 和 QoS 2 消息首先会在客户端与 Broker 存储起来，在最终确认抵达订阅端后才会被删除，此过程需要 Broker 将状态与客户端相关联，这称为会话状态。除了消息存储外，订阅信息（客户端订阅的主题列表）也是会话状态的一部分。

![QoS 1 消息流程示意图](https://assets.emqx.com/images/461e1595c5025533c1dc068b35827de5.png)

<center>QoS 1 消息流程示意图</center>

![QoS 2 消息流程示意图](https://assets.emqx.com/images/673176007a6f228bcd2bc3142ded28b5.png)

<center>QoS 2 消息流程示意图</center>

> 关于 QoS 的更多信息可参考 [MQTT QoS（服务质量）介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

客户端中的会话状态包括：

- 已发送到服务器，但尚未完全确认的 QoS 1 和 QoS 2 消息
- 已从服务器收到但尚未完全确认的 QoS 2 消息

服务器中的会话状态包括：

- 会话的存在状态，即使会话为空
- 客户订阅信息
- 已发送到客户端，但尚未完全确认的 QoS 1 和 QoS 2 消息
- 等待传输到客户端的 QoS 0（可选）、QoS 1 和 QoS 2 消息
- 已从客户端收到但尚未完全确认的 QoS 2 消息，Will Message（遗嘱消息）和 Will Delay Interval（遗嘱延时间隔）

### 会话生命周期与会话存储

会话是 MQTT 协议通信的关键，MQTT 协议要求网络连接打开时**必须保留**会话状态；当网络连接关闭后，则根据 Clean Session（MQTT 3.1.1）以及 Clean Start + 会话过期间隔（MQTT 5.0）的设置情况控制实际的丢弃时机。


![MQTT Clean Session](https://assets.emqx.com/images/7dfa66174f63a288c45833cc55013440.jpeg)

<center>MQTT 3.1.1 中会话生命周期与 Clean Session 的关系</center>

![MQTT Session Expiry Interval](https://assets.emqx.com/images/45db8d99b5ca71eaa41352ba0925353d.png)

<center>MQTT 5.0 中会话生命周期与 Session Expiry Interval 的关系</center>

本文不再赘述不同机制下会话生命周期差异，相关内容可以参考文章 [Clean Start 与 Session Expiry Interval - MQTT 5.0 新特性](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。

总而言之，当 Broker 中存在会话的时候，消息将持续进入会话，当会话对应的客户端断开连接或不具备消息处理能力时，消息将在会话中堆积。

MQTT 协议并未规定会话持久性上的实现，这意味着客户端和 Broker 可以根据场景需求和自身设计，选择将其存储在内存或磁盘中。

## 过往版本的 EMQX 会话持久化设计

在此前的版本中，EMQX 并未支持 Broker 内部消息持久化，这是吞吐量和延迟之间的权衡以及架构设计选择：

1. EMQX 解决的核心问题是连接与路由，极少情况下需要将消息持久存储，而保留消息作为一种特例是支持存储在磁盘的。
2. EMQX 作为云端服务，这类环境下服务器稳定性足够可靠，即使消息都在内存中也不会有太大的丢失风险。
3. 内置持久化设计需要权衡高吞吐场景下内存与磁盘的使用、多服务器分布集群架构下数据的存储与复制设计，在快速发展的项目中很难确保持久化设计一步到位。

尽管从性能的角度来看将所有消息存储在内存中是有益的，但基于内存的会话存储仍不可避免地会带来一些问题：大量的连接和可能存在的会话消息堆积将带来较高的内存占用，这将限制用户大规模使用持久会话功能（Clean Session = 0）；同时，在对 EMQX 进行重启操作或者 EMQX 意外宕机时也可能会导致会话数据丢失，从而对数据可靠性带来一定影响。

随着服务器市场 SSD 磁盘的大量应用，内存与磁盘两种方案之间的差距其实已经可以做到很小了。另外 LevelDB 和 RocksDB 基础架构的繁荣发展以及在 Erlang 中的成熟使用也为原生会话持久化支持的实现奠定了基础。

EMQX 自 5.0 正式开启了亿级物联网连接时代，无论在功能还是性能方面均以匹配行业最新需求为目标进行了规划设计，一个新的会话持久化能力支持设计方案也因此被提上日程。

## Why RocksDB：全新会话层选型

结合 EMQX 接入的数据特性，对比各种存储引擎后我们最终选择 RocksDB 作为新的持久化层。

### RocksDB 简介

RocksDB 是一个嵌入式、持久化的键值存储引擎。它针对快速、低延迟的存储进行了优化，具有很高的写入吞吐。RocksDB 支持预写日志，范围扫描和前缀搜索，在高并发读写以及大容量存储时能够提供一致性的保证。

### 选型依据

在 [EMQX 会话层设计](https://www.emqx.io/docs/zh/v5.0/design/design.html#会话层设计)中，会话存储于本地节点，我们倾向于在 EMQX 内部存储数据，而不是把 EMQX 作为外部数据库的一个前端，因此选型范围限制在嵌入式数据库中。除了 RocksDB 之外，我们还主要考察了以下数据库：

- **Mnesia：** Mnesia 是 Erlang/OTP 自带的分布式实时数据库系统，在 Mnesia 集群中，所有节点都是平等的。它们中的每一个节点都可以存储一份数据副本，也可以启动事务或执行读写操作。Mnesia 可以凭借复制特性而支持极高的读取吞吐，但这一特性也限制了其写入吞吐，因为这意味着 MQTT 消息基本上是在集群内广播的，广播并不能横向扩展。

   ![Mnesia](https://assets.emqx.com/images/88a29ba400f6cf781089b7b87d72ce0e.png)
 
- **LevelDB：** RocksDB 是 LevelDB 的一个改进分支，从功能上来说它们大多是等同的，但 LevelDB 在 Erlang 中缺少积极维护的驱动（Erlang NIF）因此没有被采用。

相比之下，RocksDB 的优势非常明显：

- 极高的写入吞吐：RocksDB 基于为数据写入而优化的 LSM-Tree 结构，能够支持 EMQX 海量消息吞吐与快速订阅时高频的数据写入
- 迭代器和快速范围查询：RocksDB 支持对排序的键进行迭代，基于此特性 EMQX 可以扩展更多功能
- 支持 Erlang：用于 RocksDB 的 NIF 库已经成熟并得到积极支持

在对 RocksDB 会话持久化方案的初步测试中，RocksDB 的性能优势得到充分发挥，相比内存存储，在其他模块达到瓶颈之前即可达到相同的发布率。

## EMQX 基于 RocksDB 的会话持久化设计

RocksDB 将替换当前 `apps/emqx/src/persistent_session` 目录下的所有模块，以使用 RocksDB 来存储 MQTT 会话数据。

EMQX 允许全部客户端或使用 QoS、主题前缀等过滤器配置需要启用持久化的客户端以及主题。在磁盘性能不足或可以接受消息丢失、需要极端性能的场景中，允许用户关闭持久化功能使用内存存储方案。

### 数据分发

RocksDB 作为嵌入式数据库，不具备集群内数据分发的能力。在需要节点间传递数据的操作中，如会话从一个节点移动至另一个节点，会通过 EMQX 的消息分发机制处理。

我们将 Mnesia 的复制特性与 RocksDB 的持久化特性结合到一起，会话可以存储到 RocksDB，但是使用的是 Mnesia 的 API，RocksDB 只是 Mnesia 的一个后端。

![Mnesia](https://assets.emqx.com/images/ed0da84206577b23a53519e7ef93f335.png)

### 哪些数据可以通过 RocksDB 持久化

1. 以 Clean Start = 0 连接的客户端的会话记录
2. 订阅数据（Subscriptions），在订阅时写入 RocksDB，取消订阅时从 RocksDB 删除
3. 每次客户端发布消息 QoS 1、QoS 2 消息时，数据会写入 RocksDB，保留至确认后删除
4. 作为其他高吞吐低延迟场景的 Storage，如保留消息、数据桥接缓存队列

## 持久化能力扩展

RocksDB 的引入为 EMQX 提供了一个高性能、可靠的持久化层，在此基础上 EMQX 可以扩展更多的功能。

### 消息重放

在某些场景下，发布端不需要关心订阅者是否在线，但又要求消息必须到达订阅端，即使订阅端不在线甚至会话不存在。

通过持久层的支持，EMQX 能够扩展 MQTT 协议实现以支持类似 Kafka 的消息重放功能：消息发布时允许设置特殊的标志位以持久保存在发布目标主题中，订阅者携带非标准的订阅属性时，允许获取主题中指定位置之后的消息。

消息重放能够用于设备初始化、OTA 升级这类不关心指令时效性的场景中，在发布者和订阅者之间更灵活的传输数据。

![消息重放典型流程](https://assets.emqx.com/images/8018540969e6f15c4a7a124f8d86a5a2.png)

消息重放典型流程

1. 发布端发布一条持久性消息
2. EMQX 将消息存储至重放队列中，无需关心订阅者是否在线
3. 订阅端发起订阅
4. EMQX 从指定位置读取消息
5. 重放消息发布到订阅者

### 数据桥接缓存队列

将持久层用于数据桥接的缓存队列，当桥接资源不可用时可以将数据存储至缓存队列，等待资源恢复后再继续传输，避免大量数据在内存中堆积。

## 结语

基于 RocksDB 实现的原生 MQTT 会话持久化是 EMQX 发布以来的一项突破性的重要功能变革，这一能力将为开源用户提供更可靠的业务保证，可以不受限制地充分利用 MQTT 协议特性进行物联网应用开发。使用外部数据存储的企业用户则可以迁移到 RocksDB，从而获得更低时延的数据持久化方案。

同时，结合物联网实际使用场景，EMQX 还将围绕持久化能力扩展更多的功能支持，以满足日益多样化的物联网数据需求。


<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
