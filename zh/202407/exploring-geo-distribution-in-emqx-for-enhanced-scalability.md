## 跨域集群的概念

提到 EMQX，人们通常首先会想到它的可扩展性。尽管 EMQX 能随着硬件数量的增加几乎实现线性扩展，但在单个计算实例上的扩展能力终究有限：资源总会耗尽，升级成本也会急剧上升。这时，*分布式部署*就显得尤为重要。通过在多个计算实例上部署 EMQX 集群节点，可以进一步扩展其能力。得益于 EMQX 强大的集群功能，这项任务变得相对简单。

通过分布式部署，我们不再局限于单一地理位置。我们甚至可以在不同大洲的多个数据中心部署 EMQX 集群，这个过程称为*跨域集群(Geo-Distribution*)。跨域集群的主要优势在于，当客户端分布在世界各地时，可以让它们连接到最近的 EMQX 实例，从而获得更低的延迟和更高的可靠性，提高整体吞吐量。另一个显著的优势是增强了容错性：如果某个数据中心出现故障，影响的只是部分服务，而不是整个系统。

## 挑战

然而，任何分布式部署都会带来成本，跨域集群尤其如此。

1. 实例之间通过网络连接，网络速度相对较慢。

   虽然网络速度并不算非常慢，但比起同一实例上 CPU 核心之间的通信还是要慢得多，后者的延迟以纳秒计，网络引入了*延迟*。实例之间的距离越远，延迟就越高，这是物理定律使然，我们无法改变，因此，需要在某些方面做出妥协。如果我们希望更靠近某些客户端（他们可能在澳大利亚也可能在巴西），那么有些 EMQX 节点之间的距离必然会增加，导致它们之间的通信速度变慢。在这种情况下，延迟可能会达到几十毫秒。

2. 网络不够可靠。

   数据包会丢失，连接会因网络拥塞、硬件故障、配置错误甚至恶意活动而中断。两个 EMQX 节点之间距离越远，中间需要经过的网络设备和传输电缆就越多，出现故障的几率就越大。虽然其中一些问题可以通过网络协议栈处理，只会表现为有较高的延迟，但有些问题会影响到应用层，带来许多不确定性。在出现这种故障时，EMQX 节点无法判断是某个远程节点宕机，还是网络异常。这就是所谓的*部分故障*，可能导致*可用性*降低。

严格来说，当我们谈论延迟时，还需要考虑*吞吐量*。即使高延迟网络也可以具有很高的吞吐量，但网络的不可靠性通常会影响高吞吐量的实现。在 TCP 连接中，即使是单个数据包丢失也会显著降低吞吐量，因为 TCP 协议栈需要重新传输数据包，并大幅缩小传输窗口。而且，通信双方距离越远，这种情况发生的频率就越高。

更糟糕的是，原始网络吞吐量对许多客户端来说并不重要。相反，通过 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)进行的各种*操作*的吞吐量才是最重要的，例如消息发布的吞吐量或 `SUBSCRIBE` 操作的吞吐量。这就是*共享状态*发挥作用的地方，更重要的是，需要*协调*这种状态的更新。

由于 MQTT 协议的异步特性，客户端相对独立，因而共享状态的问题并不明显，但它依然存在。为了更好地理解这个问题，让我们首先从设置一个基本的跨域 EMQX 集群开始。

## 一个跨越 12600 公里的集群

EMQX 5 采用了一种新的部署模型，即集群由两种类型的节点组成：*核心*节点和*复制*节点。这种设计旨在支持更广泛的部署场景（包括跨域集群），但也存在一些隐患，我们稍后将对此进行探讨。在这个模型中，核心节点负责管理共享状态的关键部分，而复制节点则只复制核心节点的状态更改，不参与状态管理。

为了更好地理解新模型的优势，我们首先以传统的方式部署一个集群。这个“传统”集群由分布在三个大洲的三个核心节点组成：

| **位置**                | **节点名称**         |
| :---------------------- | :------------------- |
| 法兰克福 (eu-central-1) | `emqx@euc1.emqx.dev` |
| 香港 (ap-east-1)        | `emqx@ape1.emqx.dev` |
| 开普敦 (af-south-1)     | `emqx@afs1.emqx.dev` |

![EMQX Geo-Distribution 1](https://assets.emqx.com/images/3f0d2c80af41b939f5e2b82050ba9f2d.png)

以下是集群的配置片段，我们可以通过该配置片段更好地理解问题的复杂性，并展示说明我们所做的改进：

```
broker.routing.storage_schema = v1  # 使用 5.4.0 之前的路由表架构
```

首先，集群从启动到开始运行所需的时间就暗示这不是个好的方式。日志显示，某些 `mria` 初始化步骤需要**整秒**才能完成。

```
15:11:42.654445 [notice] msg: Starting mria, mfa: mria_app:start/2
15:11:42.657445 [notice] msg: Starting shards, mfa: mria_app:start/2
15:11:47.253059 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: '$mria_meta_shard', tables: ['$mria_rlog_sync',mria_schema]
15:11:48.714293 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_common_shard, tables: [bpapi,emqx_app,emqx_banned,emqx_trace]
15:11:50.188986 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
15:11:51.662162 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
...
```

为什么会这样？这些节点之间的距离**其实**并不算远。从 ping 时间中可以看出这一点。

```
v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@afs1.emqx.dev']).
{161790,pong}
v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@ape1.emqx.dev']).
{202801,pong}
```

确实，数据包从法兰克福到开普敦再返回需要大约 160 毫秒，到香港再返回需要大约 200 毫秒。这是因为 `mria` 在底层使用 `mnesia`，而 `mnesia` 是一个*分布式数据库*。每个初始化步骤本质上都是一个数据库事务，而每个事务都需要在大多数节点之间进行协调。而每个协调步骤都需要在参与节点之间进行多次往返。在这种情况下，共享状态是数据库模式，这种协调对于确保集群中所有节点的模式*一致性*是必要的。

考虑到这一点，让我们看看这如何影响单个操作的性能：`SUBSCRIBE`。

## 延迟的影响

经过几分钟的等待，集群启动成功并可以正常工作了。我们将利用 [mqttx-cli](https://mqttx.app/zh) 测量连接集群并订阅单个主题所需的时间。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/%i [9:14:29 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/%i ✔  success  [1/1] - Subscribed to t/mqttx/1 [9:14:30 AM] › | Created 1 connections in 0.89s
```

几乎需要一秒的时间，这显然比 160 或 200 毫秒长。要找到原因，我们需要了解 MQTT 客户端和 Broker 如何进行连接和订阅：

1. 客户端与 EMQX 建立连接并发送 `CONNECT` 数据包。

   数据包包含客户端 ID 属性，而规范规定，一个 Broker 在集群中只能有一个具有该 ID 的客户端。这里的关键是“只有一个”。如果多个客户端尝试同时使用相同的客户端 ID 连接到不同的节点，就会产生*冲突*，应该加以解决。Broker 必须对所有连接的客户端有一个[强一致性](https://jepsen.io/consistency/models/strict-serializable)的视图，这意味着所做的任何更改都必须与大多数节点协调。此外，强一致性是通过全局锁来实现的，而全局锁需要获取操作和释放操作。因此，集群节点必须依次与大多数节点进行两轮通信才能完成这些操作。如果运气不好，集群节点需要与最远的节点进行协调，这个操作将花费两次往返该节点的时间。

2. 客户端发送 `SUBSCRIBE` 数据包。

   这个操作相对简单。EMQX 只需要向大多数节点通知该节点上的某人订阅了 `t/mqttx/1`，以便稍后可以将消息路由到正确的位置。这种类型的更改不需要复杂的协调，因为不可能发生冲突。然而，仍然需要与集群其他节点进行一次往返通信。

总体而言，这个操作应该花费大约 600 毫秒，但由于现实世界中的网络并不完美，客户端可能需要等待 1 秒，这对客户端来说并不理想。那么吞吐量怎么样呢？

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/%i
[9:32:19 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/%i
✔  success   [100/100] - Subscribed to t/mqttx/100
[9:32:21 AM] › | Created 100 connections in 1.706s
```

处理 100 倍的客户端花费了 2 倍的时间。这是个好消息。在这种负载下，客户端基本上是相互独立的，因为每个客户端都使用唯一的客户端 ID 连接并订阅唯一的主题。既然没有冲突，那么时间因素应该是 1 倍，但实际情况并非如此，因为为了安全起见 EMQX 默认情况下会人为地限制*并发*，使系统能够更可预测地运行。在内部，EMQX 对每个主题的订阅进行序列化，以避免数据竞争并优化不必要的工作，而且默认情况下，用于序列化的进程数量有限。不过好消息是这个限制[现在是可配置的](https://github.com/emqx/emqx/pull/11390)，可以增加其数量以适应大规模的部署。

## 冲突的巨大影响

让我们来看一下当工作负载稍有变化时会发生什么：每个客户端将订阅一个具有共同前缀的唯一主题过滤器。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[9:48:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[9:48:47 AM] › | Created 1 connections in 2.938s
```

将近 3 秒！罪魁祸首是主题过滤器。EMQX 现在需要在集群中维护一个主题过滤器的*索引*，以便高效地匹配和路由消息。每当客户端订阅或取消订阅主题时，该索引都会更新，并且该更新需要在所有节点上同步，以确保所有节点上的索引相同。这需要事务处理，事务处理需要协调，而协调需要集群节点之间进行多轮通信，这就涉及大量的网络往返。

尽管延迟很高，但吞吐量应该更好，对吧？

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:44:43 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:25 AM] › | Created 100 connections in 101.958s
```

看起来并不怎么样。处理 100 个客户端花费了 102 秒。我们失去了并发带来的所有好处，尽管工作负载看起来差不多：具有唯一客户端 ID 的客户端订阅唯一的主题过滤器。产生问题的原因在于旧版 *v1* 索引的设计。为了快速匹配消息和主题过滤器，索引被组织成一个*字典树*，EMQX 通过使用共同前缀来保持索引简洁。当客户端订阅 `t/mqttx/+/42/sub/+/#` 时，EMQX 需要更新 `t/mqttx/+/42/sub/+` 和 `t/mqttx/+` 的记录。问题是，其他客户端的订阅也会导致 `t/mqttx/+` 记录的更新，这就会导致*冲突*。当冲突发生时，`mnesia` 像传统数据库一样处理它们：锁定记录并进行序列化更新。随着订阅的客户端越来越多，冲突的数量也会增加，解决冲突所需的时间也就越长。

虽然出现连接问题时 TCP 协议栈能够轻而易举地解决。但是如果网络表现出更严重的不稳定性，某些节点将会无法访问，就会导致事务超时。这种性质的事务可能会占用记录上的锁，这些锁将一直被占用到事务超时为止。这将阻塞所有涉及该记录的其他事务，从而使订阅完全停滞。

## 避免冲突

幸运的是，*v1* 架构已经不再是默认选项了。新版 [*v2*](https://github.com/emqx/emqx/pull/11524) 架构非常稳健且性能优越，从 EMQX 5.4.0 开始成为默认架构。这个新架构的主要改进在于它是*无冲突的*：无论您的客户端使用多么复杂的主题过滤器，管理它们都不会涉及写冲突。您再也不用担心订阅中的潜在冲突了。

让我们抛开以前使用的配置，看看 *v2* 与“传统”配置的对比情况如何。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:46:54 PM] › ℹ  Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:55 PM] › ℹ  Created 100 connections in 1.673s
```

100 个客户端所花的时间比之前一个客户端所花的时间还要少。

然而，我们仍然远未达到理论上的 600 毫秒极限。诚然，除非我们的网络完美无缺，否则达到这个极限是不现实的。但仍有改进的空间，让我们探索其他方法来降低延迟。

## 改进手段：复制节点

虽然可以优化工作负载，使其更好地适应我们的部署模型，但无论如何还是需要付出延迟的代价。下面让我们放弃“传统”部署模型，将 EMQX 部署到一个由 3 个共用核心节点和 3 个复制节点组成的集群中，这些节点在地理上分布在相同的三个大洲。

![EMQX Geo-Distribution 2](https://assets.emqx.com/images/460cdbd66a7e51e84f988f1574874025.png)

这样，所有代价高昂的状态变化将仅由延迟较低的核心节点承担，而复制节点只需更新状态变化。与之前一样，客户端将连接到最近的节点，不管它是核心节点还是复制节点。

| **位置**                | **节点名称**                                                 |
| :---------------------- | :----------------------------------------------------------- |
| 孟买 (ap-south-1)       | `emqx@core1.emqx.dev` `emqx@core2.emqx.dev` `emqx@core3.emqx.dev` |
| 法兰克福 (eu-central-1) | `emqx@euc1.emqx.dev`                                         |
| 香港 (ap-east-1)        | `emqx@ape1.emqx.dev`                                         |
| 开普敦 (af-south-1)     | `emqx@afs1.emqx.dev`                                         |

启动并运行！不再需要像以前那样等待几分钟。

我们可以立即看到这种部署模型的好处：不再需要让每个事务等待几次跨越半个地球的往返延时。但延迟仍然存在，因为 EMQX 需要一个接一个地处理 `CONNECT` 和 `SUBSCRIBE` 数据包，但现在已经好多了。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[10:57:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[10:57:45 AM] › | Created 1 connections in 0.696s
```

吞吐量现在也大大提高了，因为事务处理仅在彼此非常接近的核心节点进行。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:04:35 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[11:04:37 AM] › | Created 100 connections in 1.091s
```

这是一个显著的进步。要知道，一开始 100 个客户端做同样的事情要超过 100 秒。

## 隐藏延迟

之前提到过，为避免出现竞争条件，吞吐量可能受到默认序列化进程池数量的限制。我们将负载增加 10 倍，来观察这种限制的影响。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:42:39 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:42:43 PM] › ℹ  Created 1000 connections in 4.329s
```

网络流量增加了 10 倍，这可能主要是网络故障造成的，但总时间仍比原来少了 4 倍。我们能做得更好吗？值得庆幸的是，我们一直在努力进行另一项改进，并已在 [EMQX 5.5.0](https://github.com/emqx/emqx/releases/tag/v5.5.0) 版本中发布：[批量同步](https://github.com/emqx/emqx/pull/12329)路由表更新。其目的是在通信可靠时更好地利用可用的网络吞吐量，并且不会在操作延迟已经很高时再增加延迟。

此功能尚未默认启用，但启用它非常简单。

```
broker.routing.batch_sync.enable_on = replicant
```

这个配置片段仅在复制节点上启用批量同步。将其设置为 `all` 将在所有节点上启用批量同步，一般来说，这对各种工作负载都有好处，因为 Broker 池不再需要进行额外的同步工作。在我们的案例中，效果不会那么明显，也很难演示说明。

默认值是 `none`，这样做的原因是为了安全。我们希望提供平滑的滚动升级体验，在 EMQX 5.7.0 *之前*的版本启用它，例如 5.4.1，可能会导致一些暂时的不可用。如果您从 EMQX 5.5.0 或更高版本升级则无需担心，可立即启用它。

让我们看看现在的情况。

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:46:21 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:46:24 PM] › ℹ  Created 1000 connections in 2.585s
```

这是一个相当显著的改进。现在网络吞吐量得到了更有效的利用，带来了更好的 `SUBSCRIBE` 吞吐量。扩大进程池也能达到大致相同的效果，但代价是更多的信息记录和内存使用，而这个新功能更灵活且更易于使用。

为什么我们仍然远未达到理论上的约 600 毫秒极限？因为要处理偶尔出现的网络故障。网络链路可能会出现短暂的拥塞，导致数据包丢失，TCP 协议栈必须在*重传超时（RTO）*后重新传输它们。这在已建立的连接中通常几乎不可察觉，但如果丢失了初始 SYN 数据包，情况就会大不相同。在这种情况下，TCP 协议栈还没有机会估算出最佳 RTO，因此只能从 *1 秒*的保守默认值开始。回到我们的工作负载，可能大多数客户端都能在几分之一秒内完成连接和订阅，但也有个别客户端因 SYN 数据包丢失而导致总时间增加了一秒。如果我们运气不好的话，可能会增加两秒。

值得一提的是，这种部署模型也需要利弊权衡：集群需要更多的计算资源，并且由于所有核心节点都位于同一个数据中心，对故障的恢复能力会降低。然而，鉴于其带来的好处，这是一个值得做的权衡。此外，由于采用了新的配置选项和新的主题索引设计，我们可以合理地预期，较差的订阅延迟将被吞吐量收益（理论上几乎无限）所抵消。请试用最近发布的 [EMQX 5.7.0](https://github.com/emqx/emqx/releases/tag/v5.7.0)，该版本中所有这些功能均可使用，并且经过了充分的测试。

如果您正在为跨域集群式应用程序部署这种集群，请务必考虑进一步[调整配置](https://docs.emqx.com/en/emqx/v5.7/configuration/configuration.html)。现在有一些额外的配置参数可以提高多区域 EMQX 集群的性能。以下是一个 `emqx.conf` 示例，为简化起见，将适用于核心节点和复制节点的参数合并在一起。

```
# Core nodes node.default_bootstrap_batch_size = 10000 # Replicants node.channel_cleanup_batch_size = 10
```

简要概述这些参数的作用：

- `node.channel_cleanup_batch_size`

  适用于复制节点。如果网络延迟较高，将此值从默认的 10,000 大幅减少可以在大量客户端突然断开连接时提高性能。

- `node.default_bootstrap_batch_size`

  适用于核心节点。默认值为 500，但可以大幅增加，以减少复制节点加入有许多活动订阅的集群所需的时间。

## 替代方案

在某些情况下，如此高的延迟是不可接受的。EMQX 为这些情况提供了一种解决方案：与其建立一个跨域集群式的集群，不如在每个区域部署一个独立的集群，并通过[异步 MQTT 桥接器](https://docs.emqx.com/zh/emqx/v5.7/data-integration/data-bridge-mqtt.html)连接这些集群。这是一种截然不同的部署模型，虽然需要额外的计算资源和运行开销，但它提供了一个明显的优势：不需要在不同大洲之间维护共享状态。每个集群都有自己的状态，任何由订阅引起的变化都将在本地处理，从而降低延迟。

异步模式下的 MQTT 桥接器设计旨在与*外部*资源进行交互，从某种程度上说，位于地球另一端的远程 EMQX 集群可以看作是桥接器。桥接器有由内存或持久存储支持的缓冲区，可以处理在不可靠网络中经常遇到的间歇性连接问题。

如果没有对已连接客户端及其订阅的全局视图，就不可能仅将一部分消息路由到特定区域。每个节点上的每个 MQTT 桥接器都必须将*整个*消息流传输到每个远程位置，从而导致出口带宽达到饱和。这也不可避免地带来信息丢失：桥接后的消息将不再包含原始客户端的信息。此外，要保证相同的桥接信息不会在各大洲之间来回传输，还需要做一些额外的工作。不过，[规则引擎](https://docs.emqx.com/zh/emqx/v5.7/data-integration/rule-sql-syntax.html)应该有足够的能力来处理这个问题。

这些缺点促使我们最近研究了另一种更灵活的解决方案：[集群链接](https://github.com/emqx/emqx/pull/13126)(Cluster Linking)。我们的设计目标是将两者的优点结合起来：既具有与外部资源通信的可靠性和稳健性，又能够仅路由特定区域感兴趣的消息，从而避免不必要的带宽和计算资源浪费。此功能将在即将发布的 EMQX Enterprise 5.8.0 版本中亮相。

## 结语

归根结底，还是要在可接受的权衡中做出选择。我们无法绕过光速的限制，所以必须接受延迟的代价。然而，我们仍然可以通过选择合适的部署模型和优化工作负载来让延迟更容易接受。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
