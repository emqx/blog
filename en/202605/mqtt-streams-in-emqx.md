With [EMQX 6.2](https://www.emqx.com/en/blog/emqx-6-2-0-release-notes) now released, we are continuing to expand what MQTT can support across real-time systems, AI workloads, and industrial architectures.

Before looking ahead, it is worth taking a closer look at one of the most important capabilities introduced in [EMQX 6.1](https://www.emqx.com/en/blog/emqx-6-1-0-release-notes): MQTT Streams.

For years, MQTT has been known for real-time data movement, but it has lacked durability and replay, two capabilities that modern systems increasingly expect. MQTT Streams change that.

## **The Limitation of Real-Time Only Messaging**

In a standard MQTT setup, messages are delivered in real time to subscribers and, once consumed, are no longer available.

This works well when systems are always online and continuously processing data. In practice, however, real-world systems are rarely that simple.

Consumers go offline, pipelines fail, and new applications often need access to historical data. Teams also need to replay events to debug issues or rebuild downstream systems. Without replay, gaps inevitably appear.

To address this, many teams introduce a separate streaming system such as Kafka. MQTT handles ingestion, while another system handles durability and replay. While effective, this approach adds complexity, cost, and operational overhead.

## **What Modern IoT Systems Need**

As deployments grow, expectations evolve.

Teams need durable data retention, replayable event streams, and the ability to consume data from specific points in time. They also require reliable pipelines to support analytics and AI workloads.

These are no longer advanced capabilities. They are foundational requirements for modern data architectures. Until recently, MQTT and streaming systems have largely existed in separate domains.

## **MQTT Streams in EMQX 6.1**

MQTT Streams were introduced in EMQX 6.1 to bring durable, replayable data streams directly into MQTT.

Instead of treating MQTT messages as transient events, streams organize them as an ordered, append-only log. This allows data to be retained and consumed independently of when it was originally published.

Subscribers can read from a stream using offsets, similar to modern streaming systems. This makes it possible to replay past messages, recover from failures, and build reliable data pipelines without introducing another system.

At a high level, MQTT Streams introduce three key capabilities. Messages are stored durably, allowing them to persist beyond real-time delivery. Consumers can replay data using offsets to read from any point in the stream. And stream-based consumption operates alongside traditional pub/sub, giving teams flexibility in how data is accessed and processed.

## **How It Works**

MQTT Streams introduce a new way to organize and consume data.

Messages are written into streams and stored as an ordered sequence. Consumers subscribe to that stream and control where they begin reading, either from the latest messages or from an earlier point in time.

Each stream maintains an ordered sequence of messages within its shards, and consumers track their position using offsets. In EMQX, an offset represents a specific point in time within the stream, allowing consumers to replay data or resume processing from where they left off.

This model enables multiple consumers to read the same data independently, each at their own pace, without interfering with one another.

In practice, this supports several important patterns, including reprocessing historical data, backfilling analytics pipelines, recovering from downstream outages, and debugging issues using real event data.

Importantly, this does not replace traditional MQTT pub/sub. Instead, it extends it. Real-time subscribers can continue operating as before, while stream consumers can take advantage of durability and replay when needed.

While the underlying model is similar to modern streaming systems, EMQX makes it straightforward to configure and manage streams directly within the platform.

![image.png](https://assets.emqx.com/images/8f8384423b3e6ceff800e5a95f9d6377.png)

> *Example EMQX Streams configuration, including retention policies, stream key settings, and shard controls for managing durable message storage.*

## **Why This Matters**

MQTT Streams significantly expand what MQTT can be used for.

Instead of acting only as a real-time transport layer, MQTT can now serve as a durable data backbone for IoT and AI systems.

This shift simplifies architecture by removing the need for a separate streaming system. It reduces operational overhead by minimizing the number of components to manage and accelerates development by allowing teams to build replayable pipelines directly on MQTT. It also creates a more consistent data model, with a single system supporting both real-time and historical data access.

For many teams, this eliminates an entire layer of infrastructure.

## **Where MQTT Streams Fit**

MQTT Streams are especially valuable in scenarios where data needs to be both real-time and durable.

- In industrial environments, where systems frequently disconnect or operate intermittently, streams ensure that data is not lost and can be replayed once systems come back online.
- In analytics and AI pipelines, streams make it possible to backfill historical data or reprocess events as models evolve.
- In event-driven architectures, they provide a reliable way to recover from downstream failures without losing critical data.

## **From Messaging to Data Backbone**

MQTT has long been known for efficient real-time communication.

With the introduction of streams in EMQX 6.1, it becomes something more. It becomes a system that not only moves data, but also retains, replays, and supports downstream processing at scale.

MQTT Streams transform MQTT from a transient messaging protocol into a durable data backbone for modern IoT and AI systems.

As EMQX continues to evolve with releases like 6.2, this foundation becomes increasingly important, enabling not just real-time data movement but reliable, replayable, and coordinated systems at scale.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
