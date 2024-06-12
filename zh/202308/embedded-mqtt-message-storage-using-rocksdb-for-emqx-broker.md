[EMQX](https://github.com/emqx/emqx) 是一个开源的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，它允许客户端通过 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)进行数据的发布和订阅。EMQX 的消息路由主要是将消息存储在内存中，以实现低延迟和高吞吐量。然而，这种存储方式也存在一些限制，例如当 Broker 节点掉线时，内存中的消息将会丢失，可能导致客户端无法接收到消息。

为了解决这一问题并提高可靠性，EMQX 团队正在采用嵌入式数据库 RocksDB 来实现消息的持久化。通过这个功能，在 Broker 节点失去连接时，消息仍然会被保存下来，从而确保消息的可靠传递。

## 挑战与解决方案

实现快速的 [MQTT 会话](https://www.emqx.com/zh/blog/mqtt-session)和消息持久化有很多挑战，主要包括：

1. **保证消息顺序。**来自同一个客户端和主题的消息应该按照正确的顺序进行转发。EMQX 会让客户端在数据保留期间发送的消息都能够传递给其他订阅者，并且保证消息的相对顺序不变。
2. **匹配订阅者和发布者的吞吐量。**单个订阅者接收一个主题的所有消息可能会导致连接过载。EMQX 支持分组订阅，使用分组订阅可以让多个订阅者分担工作负载。
3. **分片数据。**为了处理大量数据，EMQX 会根据发布者的客户端 ID 将消息进行分片。这样可以实现负载均衡，确保负载均匀分配，并且负载均衡器能够将客户端正确引导到相应的分片。但是，要想回放分片的数据，就需要 Broker 节点之间相互协作。
4. **设计数据库模式。**为了实现消息插入和回放的高效性，与通配符的兼容性，以及在任意时刻的回放能力，同时最小化空间使用等等，EMQX 设计了高效的数据库键，其中包括时间戳、主题索引和消息 ID。

在未来的优化过程中，EMQX 将对主题模式进行分析，并建立一个更有效的键空间。还会通过监测常见的主题结构，得出优化的模式，并用紧凑的格式来保存数据。

## 实现细节

整体设计由三个层次组成：存储层、复制层和逻辑层。存储层负责在节点上保存消息数据。复制层负责提供冗余。逻辑层负责封装底层的实现细节，并提供与 MQTT Broker 的集成。

![Implementation Details](https://assets.emqx.com/images/5025e78580b151a5dbbac497be04e963.png)

### 存储层

EMQX 使用嵌入式数据库 RocksDB 在 Broker 节点存储消息。RocksDB 提供快速的插入和压缩功能，以最小化存储空间的使用。此外，它还允许根据 EMQX 的保留策略设置 TTL，以自动删除旧数据。

### 复制层

为了应对节点故障，EMQX 会在不同的节点上备份消息数据。它将物理代理节点映射到虚拟节点，每个虚拟节点负责一部分数据。如果某个物理节点出现故障，其他节点可以接管它的虚拟节点。这一层负责实现冗余和故障转移。

### 逻辑层

逻辑层提供了简洁的 API，用于存取消息，同时隐藏了存储层和复制层的复杂性。与消息持久化相关的代码会调用逻辑层的 API，由它来根据实际情况协调底层的操作。这样的抽象设计使得这个功能可以轻松地集成到 EMQX Broker 中，并且可以在必要时更换消息存储的后端。当客户端需要回放消息时，逻辑层会从底层的数据库中取出消息，并转发给客户端。

## 结语

这个消息持久化解决方案能够大幅增强 EMQX 的可靠性，并让它拓展到对消息传送有严苛要求的新领域。EMQX 的团队正全力以赴，争取早日将这项功能推出给用户。

关于该功能的更多设计细节，欢迎阅读： [https://github.com/emqx/eip/blob/main/active/0023-rocksdb-message-persistence.md](https://github.com/emqx/eip/blob/main/active/0023-rocksdb-message-persistence.md)





<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
