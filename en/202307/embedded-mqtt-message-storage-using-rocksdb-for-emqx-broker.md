[EMQX](https://www.emqx.io/) is an open-source [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) that allows clients to publish and subscribe to data over [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). Basic functions of EMQX router keep messages in RAM, which guarantees low latency and high throughput. However, its message delivery guarantees have some limitations. Specifically, if the broker nodes go offline, the messages kept in memory would be lost. This could potentially cause message loss for clients.

To address this issue and improve reliability, the EMQX team is working on implementing message persistence using an embedded database, RocksDB. This feature will store messages even when broker nodes are offline, thereby ensuring message delivery.

## Challenges and Solutions

Implementing a fast [MQTT session](https://www.emqx.com/en/blog/mqtt-session) and message persistence comes with many challenges. Some key issues include:

1. **Guaranteeing message ordering.** Messages from the same client and topic should be relayed in the right order. EMQX will provide the following guarantees to begin with: messages within data retention window from one subscriber will eventually reach other subscribers, and partial order of the messages will be preserved.
2. **Matching subscriber and publisher throughput.** Using a single subscriber to receive all messages for a topic may overload that connection. EMQX supports group subscriptions, allowing multiple subscribers to share the workload.
3. **Sharding data.** To handle huge volumes of data, EMQX will shard messages by publisher client ID. This distributes load evenly and allows load balancers to direct clients to the right shard. However, replaying sharded data requires coordination across broker nodes.
4. **Designing a database schema.** The schema must enable fast message inserts and replays, work with wildcards, allow restarting replays at any point, minimize space usage, and more. EMQX will use a key format including timestamps, topic indexes, and message IDs to achieve these goals.

Future optimizations could analyze topic patterns to create a more efficient keyspace. By tracking common topic structures, EMQX can derive optimized patterns to store data in a compressed format.

## Implementation Details

The overall design will have multiple layers: a storage layer to store messages on nodes, a replication layer for redundancy, and a logical layer to abstract away implementation details and integrate with the MQTT broker.

![Implementation Details](https://assets.emqx.com/images/5025e78580b151a5dbbac497be04e963.png)

### Storage Layer

This layer will use RocksDB, an embedded database, to store messages on each broker node. RocksDB provides fast inserts and compactions to minimize storage space. It also allows setting TTLs to automatically delete old data based on the EMQX retention policy.

### Replication Layer

To handle node failures, EMQX will replicate message data across nodes. It will map physical broker nodes to virtual nodes or “vnodes.” Each vnode owns a shard of the total data. If a physical node goes down, other nodes can take over its vnodes. This layer handles the redundancy and failover logic.

### Logical Layer

The logical layer will provide a simple API to store and retrieve messages, hiding the complexity of the storage and replication layers. Code interfacing with message persistence storage will call the logical layer API, which will then coordinate across the lower layers as needed. This abstraction makes the feature easy to integrate into the EMQX broker and swap message storage backends if needed. When a client wants to replay messages, the logical layer will retrieve them from the underlying database and forward them to the client.

## Conclusion

This message persistence feature will significantly strengthen EMQX’s reliability and open it up to new markets with strict message delivery requirements. The EMQX team is working hard to bring this capability to users as soon as possible.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
