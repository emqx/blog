## Introduction: Streamlining IoT Telemetry with Built-in Durable Streams

You are collecting data from a fleet of devices, and live pub/sub is no longer enough. You need to keep that data and read it back later: a service you deploy next month should be able to replay what the sensors reported today, and after a bad deploy you should be able to reprocess from a point in time. **That is a durable stream.** 

The classic way to get one in an MQTT shop has been to run Kafka behind the broker and bridge messages into it. NATS folds that capability into the server as JetStream; EMQX folds it into the broker as MQTT Streams, so when Kafka was in the path only to retain and replay the data, you can now keep that in the broker.

![image.png](https://assets.emqx.com/images/fa038a3fbb89bcd45a74e3755773a156.png)

The streaming layers look alike. What differs is the system each one lives in. 

- EMQX is a full [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), and a device fleet leans on MQTT guarantees that sit around the stream: a last-will message when a device drops off, a retained message so a reconnecting client gets current state at once, a durable per-client session, and QoS 2 for the messages that must not be lost or doubled. 
- NATS is a cloud-native messaging system, strong at streaming and request-reply, but it was built for services talking to services, and most of those device guarantees are not part of it.

This post builds the same durable-telemetry scenario on both, each fed by its native clients, and maps where they match and where they diverge, on the stream itself and on the device features around it. 

The code is public and available for you to explore at: [github.com/emqx/emqx-streams-demo](https://github.com/emqx/emqx-streams-demo).

## What JetStream is

[JetStream](https://docs.nats.io/nats-concepts/jetstream) is the persistence layer built into the NATS server. Enable it and the same server that does pub/sub also gives you durable streams bound to subjects, consumers that track their own position and redeliver on missed acknowledgments, a key-value store, an object store, and work-queue retention where a message is removed once a consumer acknowledges it. Publisher deduplication is built in: stamp a `Nats-Msg-Id` header and the server drops duplicates inside a configurable window.

![image.png](https://assets.emqx.com/images/e8c92429beaedc65649dd4a041f78a97.png)

That is a lot of capability with no external dependencies, and it is why teams building cloud-native backbones reach for NATS. JetStream consumes and produces through NATS clients speaking the NATS protocol.

## What MQTT Streams is

[MQTT Streams](https://docs.emqx.com/en/emqx/latest/mqtt-stream/mqtt-stream-concept.html) arrived in [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 6.1. A stream is a named, durable store that captures every MQTT message matching a topic filter. Two types exist: append-only streams for history and replay, and last-value streams that keep the newest message per key, which is how a dashboard gets current state.

Producers are untouched. Any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) publishing to a matching topic feeds the stream, and the device fleet does not know streams exist. Consumers subscribe with [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) to `$stream/<name>` and pick the start position with a `stream-offset` subscription property: `earliest`, `latest`, or a timestamp. History arrives first, then the subscription keeps tailing. Replay is an MQTT subscription, nothing else.

![image.png](https://assets.emqx.com/images/a7c12599aa50271bf4a33b21ecd328c1.png)

Work queues are a separate EMQX feature, [Message Queues](https://www.emqx.com/en/blog/real-time-mqtt-pub-sub-and-durable-queues-natively-in-emqx), consumed via `$queue/<name>`: the broker delivers each message to exactly one of the subscribed workers.

## The Same Scenario, Built Twice

The demo runs both builds from one compose file. Each fleet speaks its broker's native protocol: MQTT sensors publish to EMQX, and a separate fleet publishes to NATS over the NATS protocol. The stacks are symmetric, one broker plus a sensor fleet plus four consumers on each side, with no gateway in either. That keeps the comparison about features and fit rather than plumbing.

![image.png](https://assets.emqx.com/images/0b5873bef4fc970e93f9f2532ce063f3.png)

Four consumers exercise the durable-streaming need on both sides: a live tail, a late joiner that replays the full history in order, a dashboard that reads current state on a cold start, and a pool of two workers that split dispatched tasks one-to-one. Both systems do all four. The differences are elsewhere.

## What Actually Differs

On the core job, the two are close. Each replays history in order, load-balances a work queue, and serves the latest value per sensor:

- **[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)** achieves this through retained messages and last-value streams.
- **NATS** achieves this through a KV bucket (written by the producer) or a last-per-subject stream.

Where they diverge, however, comes down to five key architectural areas:

### 1. Durable Consumers

- **NATS JetStream:** Keeps a named consumer's position on the server. If a consumer crashes, it simply reattaches and resumes exactly where it stopped. For a long-lived pipeline that must never miss or reprocess data, JetStream's model requires less operational effort to get right.
- **EMQX Streams:** The stream consumer picks a start point and tracks its own position to resume from.

### 2. Device-Centric Features around the Stream

An IoT fleet needs more than just a log of readings. MQTT natively includes three core features designed for device management, whereas native NATS does not support them at the protocol level:

| **Feature**            | **EMQX (Native MQTT Broker)**                                | **Native NATS (Alternative Approach)**           |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| **Last-Will Message**  | Automatically announces a device's sudden loss, **eliminating the need for custom timeout detection**. | Handled via **Connection Events**.               |
| **Retained Message**   | Gives a dashboard or replacement unit the device's current state **the instant it subscribes**, without waiting for the next publish. | Handled via a **manually maintained KV bucket**. |
| **Per-Client Session** | Acts as a **durable mailbox per device**, ensuring commands sent while a device is offline arrive immediately upon reconnection. |                                                  |

You can build each of these features in the application layer with NATS, but that is your code to write and run.

NATS does match MQTT on the basics (wildcards, load-balanced subscriptions, headers, and per-message TTL since v2.11), and its request-reply pattern is more first-class; the gap is specifically these device-centric features.

### 3. Endpoint Protocols

This is usually the ultimate deciding factor in technical selection:

- **MQTT Dominance:** The device and OT installed base is overwhelmingly MQTT, much of it consisting of third-party or fixed-firmware hardware whose protocol you cannot change. If your endpoints *must* use MQTT, EMQX puts **durable streams natively right where the devices already are**.
- **NATS Ecosystem:** When you fully control the endpoints and they can run a NATS client, the MQTT ecosystem advantage falls away. The choice then comes down to pure features, where NATS's breadth is a real draw.

### 4. Open Standard vs. Single Implementation

- **MQTT (EMQX):** An OASIS and ISO/IEC 20922 standard with many interoperable brokers (EMQX, HiveMQ, Mosquitto, cloud IoT services) and clients. The practical effect is at the device layer: because devices speak a standard protocol rather than a vendor-locked one, **you can change brokers without re-touching the fleet**.
- **NATS:** Has a **single implementation**, the CNCF `nats-server`. It is Apache-2.0 licensed, so you have access to the source code, but there is no alternative server to migrate to, and the protocol tracks one project's roadmap.

In fairness, the streaming feature is proprietary on both sides, MQTT Streams to EMQX and JetStream to NATS; the portability MQTT buys you is at the protocol and device layer, not the stream.

### 5. Licensing

- **NATS:** Fully open-source under **Apache-2.0**.
- **EMQX:** Features a single edition since v5.9 that is **free for single-node and non-commercial use**, but requires a license for clustering or commercial production.

If an OSS-only stack is a hard constraint for your architecture, this settles the choice early.

### Beyond Streaming: Platform Capabilities

Beyond data streaming, each technology functions as a much broader platform. Your choice here depends heavily on your extended architecture:

- **NATS adds:** A key-value store, an object store, and first-class request-reply.
- **EMQX adds:** A SQL rule engine and data bridges directly to Kafka and various databases.

Data ordering is **per key on both sides** as configured here (per sensor), and the replay consumers in both repositories verify this behavior.

## How to Choose

- **Choose NATS JetStream** when your producers and consumers speak NATS, or you build them to, or when you want an Apache-2.0 system that is also a key-value, object, and request-reply platform. That is what JetStream is built for, and a fleet of NATS-native services is a fine architecture.
- **Choose EMQX MQTT Streams** when your fleet is MQTT, as most IoT and OT fleets are or must be, and the job is replay, current state, or work distribution on that data. The stream then lives in the same system as the device connections and the rule processing, with nothing to translate.

## The Wider Pattern

Messaging systems have been growing each other's primitives for years: Kafka added queue-style consumption with share groups, RabbitMQ added replayable streams, and MQTT brokers are now adding durable logs and queues of their own. The protocol label on the box says less and less about what the system can do; what still differs is which clients connect natively and where the data enters. For device fleets, that entry point is usually MQTT, and that is the strongest reason to want the stream where the devices already are.

Run both builds yourself: [github.com/emqx/emqx-streams-demo](https://github.com/emqx/emqx-streams-demo). Fifteen minutes, Docker only, and the README walks through replay, current state, work queues, and a broker restart.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
