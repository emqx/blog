>This is a guest post from Prakhar Dev Gupta, a Backend Engineer at Slice.

# Introduction

As our chatbot requirements grew, we transitioned from a managed chatbot solution to an in-house system. This blog highlights the challenges that led to each migration, the benefits gained, and lessons learned.

# Initial Solution

We initially adopted a well-known managed service for building chatbot and automating customer support experiences across chat and voice for its ease of implementation, chatbot flow management, and live agent support. Key benefits included:

- **No-Code Flow Builder** — Simplified chatbot creation without heavy development effort.
- **Omnichannel Support** — Seamless deployment across web, mobile, and messaging platforms.
- **Integrations & Analytics** — Easy API connections with CRMs and insights into chatbot performance.

> ⚠️ While it provided a solid foundation, we encountered limitations as we scaled.

# Why We Built an In-House MQTT-Based Chatbot Solution

As our chatbot evolved and grew more complex, we started running into major roadblocks with the managed solution we were using. Here’s what pushed us to take things into our own hands:

- **Limited Customization**

  We were constantly hitting walls with UI/UX flexibility. Adding new widgets was slow and painful, and handling conversations the way we wanted just wasn’t possible within the constraints of the vendor’s SDK.

- **Performance Bottlenecks**

  The web SDK had heavy load times — it pulled in a bunch of scripts and assets that slowed things down. On top of that, every message had to go through multiple back-and-forths between the vendor’s servers and our backend, which introduced serious lag.

- **AI Limitations**

  The built-in NLP just didn’t cut it. It struggled with our more advanced language requirements and didn’t offer the flexibility we needed to build meaningful conversations.

- **Slow Support Turnaround**

  Any time we needed something fixed or added — even critical issues — we had to wait. Response times were long, and it felt like we had little control over getting things resolved quickly.

- **Workflow Complexity**

  Building and managing conversation flows with the vendor’s tools was messy. There was no version control, and scaling workflows or making changes safely was a constant challenge.

> 💡 So we made the call — instead of fighting these limitations, we decided to build our own system. Going in-house gave us full control and let us move faster. We chose MQTT over EMQX as our messaging backbone because of its speed, flexibility, and real-time performance, which is exactly what our chat experience needed.

# Why MQTT Was the Right Protocol Choice

> MQTT, a lightweight messaging protocol, was the perfect choice for real-time interactions as it guaranteed efficient message delivery even with low bandwidth consumption.

## Here’s why MQTT made sense:

- **Lightweight & Efficient**

  MQTT is built for *low-bandwidth, high-latency networks* — ideal for delivering snappy chat messages with minimal overhead.

- **Reliable Message Delivery (QoS)**

  We could choose how reliably each message is delivered — at least once, exactly once, or best effort — giving us control over performance and fault tolerance.

- **Retained Messages**

  Bots can pick up the last message or prompt even after a reconnection. It’s super helpful for resuming conversations seamlessly.

- **Presence Detection (LWT)**

  MQTT’s *Last Will and Testament* feature let us detect when a client disconnects unexpectedly — critical for real-time presence awareness.

- **Scalable Architecture**

  Its *pub/sub* model made it easy to grow our system without tight coupling — ideal for scaling across users, bots, and backend services.

> 💬 As our requirements continued to grow, we integrated **EMQX** into our system. EMQX further improved our system by providing better scalability, higher availability, and increased performance, especially in managing a growing number of concurrent connections.

# Choosing MQTT Over Other Alternative Protocols: GRPC or API Polling

Our system required a protocol that could handle high concurrency, low latency, and efficient message delivery. While options like gRPC and polling were on the table, MQTT emerged as the most practical and scalable solution for our needs. Here’s why:

- **Lightweight & Efficient**: MQTT uses a *minimal 2-byte header* and maintains a persistent TCP connection. This makes message delivery fast and bandwidth-efficient — ideal for rapid-fire chat. In contrast, gRPC runs over HTTP/2 with heavier framing and per-call metadata, increasing latency and overhead per message
- **Built-in Presence and Resilience**: MQTT supports persistent sessions and a “*Last Will and Testament*” (***LWT\***). This means it can detect dropped clients and notify others, and resume message delivery after reconnects. gRPC or API Polling lacks built-in presence or offline handling — once a client disconnects, messages are lost unless your app explicitly handles it.
- **Real-time & Event-Driven**: Information is delivered instantly to clients as events happen, rather than requiring clients to constantly ask for updates. This makes it highly efficient for dynamic applications like chat.
- **Publish/Subscribe**: Ideal for immediate, asynchronous message delivery without constant requests.
- **Push-Based**: Reduces latency and server load compared to polling.
- **Scalable & Flexible**: The broker-based architecture means publishers and subscribers are independent. You can add more clients, services, or features without reconfiguring the entire system, making it easy to grow.
- **Decoupled Architecture**: Easier to scale with more users and features.
- **Many-to-Many Communication**: Supports various chatting patterns.
- **Reliable**: MQTT provides three Quality of Service (*QoS*) levels. QoS 1 and 2 ensure messages reach offline clients after they reconnect — crucial for reliable chat delivery. gRPC doesn’t queue or retry messages natively; you need to build that logic yourself.
- **Simple & Easy to Implement**: Simple protocol with readily available libraries and a broker-centric approach.
- **Scalable Pub/Sub Architecture**: MQTT’s broker handles millions of concurrent clients via topic-based *pub/sub*. Chatbots benefit from its decoupled, scalable model. gRPC is point-to-point — scaling group chats or broadcasts requires custom infrastructure.

**Why MQTT is a better choice than:**

- **gRPC:** MQTT has lower overhead, more natural fit for event-driven real-time communication (gRPC is primarily request/response). gRPC real-time requires a more complex streaming setup.
- **API Polling:** MQTT is far more efficient (push vs. constant pull), offers **lower latency**, and scales much better. Polling is inherently poor for real-time experiences.

The above points are better summarized in the tabular form below in the protocol comparison matrix :—

**Protocol Comparison Matrix**

![image.png](https://assets.emqx.com/images/69e9ab386fd6bba8388bcd0a46eebbeb.png)

<center>Comparison of MQTT with other popular protocols</center>

## 🎯 In Summary:

> MQTT’s lightweight, real-time pub/sub architecture is purpose-built for the continuous message flow of chatbots — unlike gRPC’s heavier request-response model or inefficient API polling. With minimal framing, brokered delivery, and built-in session and QoS handling, MQTT aligns naturally with the demands of real-time, large-scale chat systems

# Picking the Right MQTT Broker: Why EMQX Won Us Over

When we set out to choose an MQTT broker to power our chatbot infrastructure, we evaluated a bunch of options. In the end, **EMQX** checked all the right boxes for us. Here’s why:

## Built for Performance and Scale

We needed something that could handle serious traffic — think millions of users — without breaking a sweat. EMQX delivered:

- It supports **5+ million concurrent connections on a single node** and keeps latency under a millisecond.
- It can process **over 2 million messages per second**, and it does this consistently.

**In comparison:**

- **Some other servers** we tried had *single-threaded* architecture and taps out at around 100K connections per node.
- One managed cloud offering looked attractive, yet its usage-based *pricing* made cost forecasting at scale difficult and raised concerns about vendor lock-in. Also the support for QoS 2 was not available.

## Powerful Features Right Out of the Box

Security and flexibility were non-negotiable for us — EMQX came with everything we needed built in:

- **Enterprise-grade security**: TLS/SSL, X.509 certificates, OAuth 2.0, JWT — all supported out of the box.
- **Full MQTT spec support**: Both 3.1.1 and 5.0, including retained messages, QoS levels, and last will messages.
- **Flexible protocol options**: It supports MQTT, WebSocket, and even HTTP APIs for more integration flexibility.

**Compared to:**

- Another broker delivered a comparable feature set, but only behind an expensive enterprise-level licence.

## Excellent Visibility & Monitoring

We really liked how much insight EMQX gives you into what’s going on under the hood:

- A **real-time dashboard** shows active connections, throughput, client behavior, and more.
- **Advanced analytics** help us understand topic usage and message flow patterns.
- **Built-in monitoring** with OpenTelemetry and alerting options meant we didn’t need to bolt on extra tools.

**In contrast:**

- One alternative offered only minimal native monitoring and required substantial manual configuration to gain adequate observability

## A Rule Engine That Actually Helps

One of EMQX’s standout features is its[ ***visual rule engine\***](https://docs.emqx.com/en/emqx/latest/data-integration/rules.html), which lets you route messages to external systems without writing a bunch of custom code.

- Easily connect to ***Kafka, HTTP endpoints, databases\***, and other systems.
- It’s fast enough to ***process millions of messages in real time\*** with minimal overhead.

## Self-Hosted and Vendor-Neutral

We wanted full control over our infrastructure — no lock-in, no surprises.

- EMQX can run **on-premises, in the cloud, or in hybrid environments**.
- It’s **open-source** with optional commercial support — a big win for flexibility.
- Most importantly, **costs are predictable**. No per-connection or per-message pricing gotchas.

## Fast-Moving Project with Strong Community

We didn’t want to bet on a stagnant tool. EMQX is anything but:

- **Frequent releases** bring new features, fixes, and performance boosts.
- Backed by a solid community — **13K+ GitHub stars**, active forums, and great docs.
- For production-grade support, they offer **enterprise plans with SLA guarantees**.

In short: **EMQX gave us the performance, control, and flexibility** we needed — without the trade-offs of vendor lock-in or sky-high pricing. It just made sense.

![image.png](https://assets.emqx.com/images/08632412628c486ae3d89e381bdb205c.png)

<center>Community & Support Metrics — EMQX vs. Alternative MQTT Brokers</center>

## 🎯 Conclusion:

> In the end, EMQX gave us exactly what we were looking for — the speed and scale to support real-time messaging, the flexibility to fit into our evolving architecture, and the control we needed to stay efficient and cost-effective. Its blend of powerful enterprise features and open-source adaptability made it the right fit for our chatbot infrastructure, both now and as we continue to grow.

# HLD for MQTT over EMQX

After choosing EMQX as our MQTT broker, we designed a high-level architecture that plays to its strengths — real-time messaging, reliability, and scalability. To handle large volumes of data and ensure smooth processing, we paired it with Kafka, allowing us to scale effortlessly while keeping message delivery consistent and responsive. We shall discuss the same below:

## Authentication and Authorization:

To ensure secure access to our messaging system, *we rely on EMQX’s built-in support for external authentication*. Every client — whether a user or agent — is authenticated through an HTTP call to our internal auth service. Once verified, they’re authorized to publish or subscribe only to the specific topics returned by our custom API.

To make things clearer, we’ve also included flow and sequence diagrams to illustrate how this process works in practice.

![image.png](https://assets.emqx.com/images/60890d71b0a86e783803fb533a8f02ba.png)

<center>Flow Diagram Representation of Authentication & Authorization via MQTT over EMQX</center>

<br>

![image.png](https://assets.emqx.com/images/c241b6c2ba39fd9e937ef2c230375e83.png)

<center>EMQX Authentication and Authorization Sequence Diagram</center>

The *custom auth API* response looks like this:

```json
HTTP/1.1 200 OK
Headers: Content-Type: application/json
...
Body:
{
    "result": "allow", // "allow" | "deny" | "ignore"
    "is_superuser": false, // options: true | false, default value: false
    "client_attrs": { // optional (since v5.7.0)
        "role": "admin",
        "sn": "10c61f1a1f47"
    }
    "expire_at": 1654254601, // optional (since v5.8.0)
    "acl": // optional (since v5.8.0)
    [
        {
            "permission": "allow",
            "action": "subscribe",
            "topic": "eq t/1/#",
            "qos": [1]
        },
        {
            "permission": "deny",
            "action": "all",
            "topic": "t/3"
        }
    ]
}
```

# Choice of MQTT Topics

Once a user or agent is authenticated and authorized, the next crucial step is determining where they can send and receive messages. To maintain both security and scalability, we’ve implemented a ***structured topic naming\*** convention within our MQTT setup.

**Here’s how we organize it:**

- **User topic:** `user/{uuid}`
  Every user is assigned a unique topic tied to their UUID, allowing for complete message isolation and privacy.
- **Agent topic:** `agent/{emp_id}`
  Similarly, agents communicate through their dedicated topic, mapped to their employee ID.
- **Central publish topic:** `globalmessage`
  Regardless of origin, all messages are funneled here for backend processing and routing.

This design gives us the best of both worlds: users and agents communicate through isolated channels, while our backend retains centralized control for monitoring, analytics, and scaling.

# Events Flow HLD for Current Architecture

![image.png](https://assets.emqx.com/images/06bdebf01160807f0509a0de9e34abff.png)

<center>Event Flow Diagram of EMQX</center>

## Flow Explanation

The following sequence diagram illustrates the complete message flow in our MQTT-based chatbot architecture:

![image.png](https://assets.emqx.com/images/743acc2a4e3a7b3be5c9c1a641cae8ce.png)

<center>Sequence Diagram of Event Flow Between User, Backend and Agent</center>

**Detailed Flow Steps:**

Here’s a breakdown of how messages move through our system, from connection to delivery:

1. **Authentication**

- Users and agents first connect via MQTT.
- EMQX handles authentication using our internal auth service.
- Once authenticated, clients subscribe to their respective topics — based on their *UUID* (for users) or *employee ID* (for agents).

**2. Publishing Messages**

- Users subscribe to: `user/<uuid>`
- Agents subscribe to: `agent/<agent_empid>`
- All messages — regardless of who sends them — are published to a single topic: `globalmessage`. This makes backend processing much simpler.

**3. Routing via Rule Engine**

- EMQX’s *built-in Rule Engine* takes over here.
- It picks up the messages from `globalmessage` and forwards them to *Kafka* — specifically to the topic `globalmessage-prod`.
- We *partition messages by UUID* to maintain **message order** per user.

**4. Backend Event Processing**

- Our backend services *consume Kafka events* and apply business logic (e.g., validation, logging, transformations).
- We use *partition-based consumption*, so each service handles a portion of the load — ensuring the system scales smoothly.

**5. Response Delivery**

- Once processed, responses are sent back through MQTT.
- Depending on who the message is for, it’s routed to either `user/<uuid>` or `agent/<agent_empid>`

# Kafka Integration with EMQX Rule Engine

- The EMQX Rule Engine listens to the `globalmessage` topic.
- Messages are then forwarded to Kafka under `globalmessage-prod`.
- Our backend Kafka consumers pick up the flow from there — handling everything from processing logic to analytics and delivery.

# Why Kafka in the Middle Matters for Our Chatbot

After messages are routed to the `globalmessage` topic, they’re not processed directly. Instead, EMQX forwards them to a Kafka topic (`globalmessage-prod`) using its rule engine.

This extra hop might seem redundant, but it’s essential. Kafka helps us decouple message ingestion from processing, making our system more scalable, fault-tolerant, and easier to manage across distributed backend services. We have listed the advantages of this extra hop:

## 1. Guaranteed Message Ordering

In a chat system, message sequence is crucial. Kafka maintains ordering within a partition, so if messages for a conversation are routed to the same partition, they’re processed in the correct order — unlike MQTT alone, which *doesn’t ensure sequencing* across backend consumers.

## 2. Designed for Distributed Systems

Our backend is deployed as multiple pods. Kafka’s consumer group mechanism allows us to *evenly distribute messages across these pods*. Each pod handles a partition, ensuring scalable and parallel processing without duplication.

## 3. Real-Time Layer Decoupling

EMQX handles fast, lightweight real-time delivery, while Kafka acts as a *durable buffer*:

- If the backend is re-deploying or temporarily down, messages are still sent to Kafka.
- The backend resumes from where it left off, with no data loss.

## 4. Handling Back Pressure Gracefully

MQTT is not designed to handle processing delays or retries. Kafka provides a buffer layer so the backend can consume messages at its own pace, without blocking MQTT publishers or degrading performance.

## 5. Replayability and Auditing

Kafka retains messages for a configurable duration:

- We can replay messages for debugging or analytics.
- Failed messages can be retried without data loss.
- It also gives us a full audit trail of chat activity.

## In Summary

> Putting Kafka between EMQX and the backend gives us the best of both worlds
>
> **🚀 MQTT** for real-time client communication
>
> **Kafka** for durability, scalability, and reliable backend processing
>
> This architecture makes our chatbot system resilient, scalable, and production-ready for modern cloud environments.


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact" class="button is-gradient">Contact Us →</a>
</section>
