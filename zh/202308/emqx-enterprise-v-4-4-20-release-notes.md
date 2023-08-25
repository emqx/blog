我们很高兴地宣布：[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.20 版本现已正式发布！

本次发布我们改进了 Kafka 和 HStreamDB 数据集成的性能，为 GCP PubSub 数据集成添加了属性和排序键的支持。除此之外还修复了多项 BUG。

## 提升 Kafka 和 HStreamDB 数据集成的性能

EMQX 通过集成 Kafka 和 HStreamDB，可以实现物联网消息事件流的一站式采集、存储、处理和分发，这为各种实时物联网应用场景提供了强大支持。

此前版本中，EMQX 已经实现了异步、批处理机制，可满足大规模海量数据集成场景下的高性能需求。在 EMQX Enterprise 4.4.20 中，改进后的 Kafka 与 HStreamDB 驱动为 Erlang 进程通信增加了一个消息缓冲区，利用批处理机制提升内部的消息传递速度，进而提升整体的吞吐性能，以满足更极端的性能需求。

此功能默认关闭，用户可以通过 Kafka 和 HStreamDB 动作中的**最大 Erlang 消息累积数**与**最大 Erlang 消息累积间隔**配置开启。

内部测试表明，启用此新特性后，不同场景下数据集成吞吐量可提升 10%-40%。该优化特性也将同步到 EMQX 企业版 5.0 后续的版本中。

## GCP PubSub 集成添加属性和排序键的支持

GCP PubSub 作为一个全托管的事件流和订阅服务，广泛用于构建可靠的实时流式处理管道。EMQX 规则引擎支持将数据经过处理后发布到 GCP PubSub，实现与 GCP 服务的无缝集成。

EMQX Enterprise 4.4.20 为 GCP PubSub 动作新增了属性(Attributes)和排序键(Ordering Keys)的支持，可以为数据集成提供更丰富的上下文信息和顺序保证，实现灵活的物联网数据处理。

## 其他新增特性

- 为 SQL Server 数据集成增加 `auto_reconnect` 选项，能够在 EMQX 与 SQL Server 之间的连接断开后自动重新建立连接，保证数据写入的连续性。

- 为 RabbitMQ 数据集成添加了 TLS 连接支持，提高传输数据的安全性和完整性。

## BUG 修复

- 修复了无法在 Dashboard 上测试规则引擎的 `mongo_date()` 函数的问题。

- 修复了热升级到 4.4.19 之后，规则引擎通过 RabbitMQ 动作发送消息失败的问题。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
