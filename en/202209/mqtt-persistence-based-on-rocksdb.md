## Introduction: Native MQTT session persistence support

The MQTT protocol standard states that the broker must store messages from offline clients. In previous versions, [the open-source version of EMQX ](https://www.emqx.io/)used memory-based session storage, while the enterprise version further provides an external database storage solution for data persistence.

This memory-based, non-persistent session storage is the optimal solution based on a trade-off between throughput and latency, but it still imposes limitations on users in certain scenarios.

In line with our philosophy of paying attention to community feedback and continuously improving the product to bring users more ease of use, we have added native MQTT session persistence support based on RocksDB to the EMQX 5.x product plan. This feature is now in the formal development stage and is expected to be available to all users in version 5.1.0.

This article is a technical preview of this feature. Through the introduction of MQTT session related concepts and the design principle of EMQX session persistence feature, we will help readers understand this more reliable and low-latency data persistence solution. Also, we will explore more new features based on RocksDB persistence capabilities.

## Understanding MQTT sessions

In the protocol specification, QoS 1 and QoS 2 messages are first stored on the client side and the broker. The messages are not deleted until the final confirmation arrives on the subscriber. This process requires the Broker to associate the state with the client, which is called session state. In addition to the message store, subscription information (the list of topics to which the client subscribes) is also part of the session state.

![QoS 1 message flow diagram](https://assets.emqx.com/images/40d8b6f9e36eee75116d65c2d6c70217.png)

<center>QoS 1 message flow diagram</center>


![QoS 2 message flow diagram](https://assets.emqx.com/images/aeb83145c8a0cbcb5c589e56d111bae8.png)

<center>QoS 2 message flow diagram</center>

> For more information about QoS, see [MQTT QoS (Quality of Service) Introduction](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)

The session state in the client includes:

- QoS 1 and QoS 2 messages that have been sent to the server but not yet fully acknowledged
- QoS 2 messages that have been received from the server but not yet fully acknowledged

The session state in the server includes:

- The existence status of the session, even if the session is empty
- Client subscription messages
- QoS 1 and QoS 2 messages that have been sent to the client but have not been fully acknowledged
- Waiting for QoS 0 (optional), QoS 1, and QoS 2 messages to be transmitted to the client
- QoS 2 messages, [Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) and Will Delay Interval that have been received from the client but not yet fully acknowledged

### Session life cycle and session storage

Sessions are the key to MQTT protocol communication, and the MQTT protocol **requires** that the session state be **preserved** when a network connection is opened. When the network connection is closed, the actual timing of the discard is controlled based on the Clean Session (MQTT 3.1.1) and Clean Start + session expiration interval (MQTT 5.0) settings.

![Relationship between Session lifecycle and Clean Session in MQTT 3.1.1](https://assets.emqx.com/images/90fe98166e240d594231c75c6ad557ee.png)

<center>Relationship between Session lifecycle and Clean Session in MQTT 3.1.1</center>

![The Relationship Between Session lifecycle and Session Expiry Interval in MQTT 5.0](https://assets.emqx.com/images/21c9a3b9d8fe5e67ca3ef2b2864e075b.png)

<center>The Relationship Between Session lifecycle and Session Expiry Interval in MQTT 5.0</center>

This article will not go into the differences between the Session Lifecycles of the different mechanisms. For relevant information, see [Clean Start and Session Expiry Interval - New Features in MQTT 5.0](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval).

In summary, messages will continue to enter a session while there is a session in the Broker and will accumulate in the session when the client corresponding to the session disconnects or does not have message handling capabilities.

The MQTT protocol does not specify the implementation of session persistence, which means that clients and the Broker can choose to store them in memory or on disk, depending on the needs of the scenario and their design.

## Session persistence design in previous versions of EMQX

In previous versions, EMQX did not support internal disk message persistence out of a trade-off between throughput and latency and an architectural design.

1. EMQX solves the core problem of connectivity and routing. In rare cases, messages need to be stored persistently, and reserved messages as a special case are supported to be stored on disk.
2. EMQX is a cloud service, and the server stability is reliable enough in this kind of environment. Even if the messages are in the memory, there is not much risk of loss.
3. The built-in persistence design requires a trade-off between memory and disk usage in high-throughput scenarios, and data storage and replication design in a multi-server distributed cluster architecture, which makes it difficult to ensure the persistence design is in place in a single step in a fast-growing project.

Although storing all messages in memory is beneficial from the performance point of view, memory-based session storage inevitably poses some problems: a large number of connections and possible session message buildup will result in a higher memory footprint, which will limit the large-scale use of persistent session functionality (Clean Session = 0). In addition, session data loss may occur during EMQX restart operations or unexpected EMQX downtime, which can have an impact on data reliability.

With the massive adoption of SSD disks in the server market, the gap between memory and disk solutions is actually quite small. In addition, the prosperous development of LevelDB and RocksDB infrastructure and the mature use in Erlang also laid the foundation for the implementation of native session persistence support.

EMQX 5.0 officially started an era of 100 million level IoT connections. Both features and performance are planned and designed to match the latest industry requirements. Therefore, a new design solution for session persistence support is on the agenda.

## Why RocksDB: A New Session Layer Selection

After comparing various storage engines with the data characteristics of EMQX access, we finally chose RocksDB as the new persistence layer.

### RocksDB Introduction

RocksDB is an embedded, persistent key-value storage engine. It optimizes fast and low-latency storage with high write throughput. RocksDB supports pre-written logging, range scans, and prefix searches, providing consistency guarantees during high concurrency reads and writes as well as high volume storage.

### Selection basis

In the [EMQX session layer design](https://www.emqx.io/docs/en/v5.0/design/design.html#session-layer-design), sessions are stored in local nodes, and we prefer to store data inside EMQX rather than using EMQX as a front-end to an external database. So, the selection is limited to embedded databases. In addition to RocksDB, we looked primarily at the following databases.

- **Mnesia:** Mnesia is a distributed real-time database system built in Erlang/OTP. All the nodes of the Mnesia cluster are equal. Each of these nodes can store a copy of the data and can also start a transaction or perform a read or write operation. Mnesia can support extremely high read due to its replication feature, but this also limits its write throughput as it means MQTT messages are largely broadcast within the cluster and the broadcast cannot scale out.
- **LevelDB:** RocksDB is an improved branch of LevelDB, and they are mostly functionally equivalent, but LevelDB lacks an actively maintained driver in Erlang (Erlang NIF). So, it has not been adopted.

![Mnesia mesh topology](https://assets.emqx.com/images/f315719ace6ed72fa8c6b8bdd711086b.png)

<center>Mnesia mesh topology</center>

In contrast, RocksDB has some obvious advantages:

- Extremely high write throughput: RocksDB is based on an LSM-Tree structure optimized for data writes, capable of supporting EMQX massive message throughput and high frequency data writes during fast subscriptions
- Iterators and fast range queries: RocksDB supports iteration over sorted keys. Based on this feature, EMQX can be extended with more features
- Support for Erlang: The NIF library for RocksDB is mature and actively supported

In preliminary testing of the RocksDB session persistence solution, the performance advantage of RocksDB was maximized, which allows to achieve the same release rate before other modules reached their bottlenecks compared to memory storage.

## EMQX session persistence design based on RocksDB

RocksDB will replace all modules in the current `apps/emqx/src/persistent_session` directory to use RocksDB to store MQTT session data.

EMQX allows all clients or the clients and topics that need persistence enabled due to configuration using filters such as QoS and topic prefixes. In scenarios where extreme performance is required and disk performance is insufficient or message loss is acceptable, users are allowed to turn off persistence and use the memory storage solution.

### What data can be persisted with RocksDB

When the client allows persistence to be enabled：

1. Session records for clients connected with Clean Start = 0
2. Subscriptions are written to RocksDB when Subscriptions are made and deleted from RocksDB when Subscriptions are cancelled
3. Every time the client publishes a message QoS 1, QoS 2 message, the data will be written to RocksDB and reserved until it is confirmed and then deleted
4. Serves as a Storage for other scenarios with high throughput and low latency, such as message retention and data bridging cache queues

## **Extension of persistence capability**

The introduction of RocksDB provides EMQX with a high-performance and reliable persistence layer on which EMQX can be extended with more features.

### Message Replay

In some scenarios, the publisher does not need to care whether the subscriber is online or not, but requires that the messages reach the subscriber, even if the subscriber is not online or even if the session does not exist.

With persistence layer support, EMQX can extend the MQTT protocol implementation to support Kafka-like message replay functionality: allowing special flag bits to be set when a message is published to persist in the publish target topic; allowing subscribers to fetch messages after a specified location in the topic when they carry non-standard subscription attributes.

Message replay can be used for more flexible transfer of data between publishers and subscribers in scenarios such as device initialization and OTA upgrades that are not concerned with the timeliness of instructions.

![Message Replay](https://assets.emqx.com/images/f3540777cd2803f9dffd419d645c3e58.png)

Typical flow of message replay:

1. The publisher publishes a persistent message
2. EMQX stores the message in the replay queue, without caring whether the subscriber is online or not
3. The subscriber initiates a subscription
4. EMQX reads the message from the specified location
5. The replay message is published to the subscriber

### Data bridging cache queue

Use the persistence layer as a cache queue for data bridging, so that data can be stored to the cache queue when the bridging resource is unavailable and the transmission can be continued after the resource is recovered, avoiding massive data accumulation in the memory.

## Epilogue

Native MQTT session persistence based on RocksDB is a groundbreaking and important feature change since the release of EMQX. This capability will provide open-source users with more reliable business assurance, and they can make full use of MQTT protocol features for IoT application development without restriction. Enterprise users who use external data storage can migrate to RocksDB for a lower latency data persistence solution.

At the same time, combined with the actual use scenarios of IoT, EMQX will also expand more functional support around persistence capability to meet the increasingly diverse IoT data demands.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
