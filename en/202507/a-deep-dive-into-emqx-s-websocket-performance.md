## Introduction

In the world of real-time web applications - from live financial dashboards and collaborative whiteboards to interactive gaming and large-scale IoT fleet management - the underlying communication protocol is the engine that drives the experience. While [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is the de facto standard for IoT, **[MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)** has become the go-to solution for bridging the gap between backend services and browser-based clients, offering robust, bidirectional communication that easily traverses corporate firewalls.

But as applications scale, a critical question emerges: how many concurrent WebSocket connections can a broker *truly* handle? At EMQX, we continuously push the boundaries of what's possible. Following our successful test of [100 million MQTT/TCP connections](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0), we turned our attention to WebSockets.

We are thrilled to announce that **a single cluster of EMQX 5.10 has successfully sustained 2 million concurrent MQTT over WebSocket connections**, demonstrating not only massive scalability but also exceptional low latency and resource efficiency.

In this post, we’ll take you on the journey to 2 million connections, detailing our test setup, the results at each stage, and the architectural principles of EMQX that make this remarkable performance possible.

## The Challenge: From 500k to 2M

Our goal was to simulate a real-world, large-scale scenario: a huge number of WebSocket clients subscribing to unique topics and receiving a steady stream of messages. We designed a progressive benchmark, doubling the connection load at each stage to observe how EMQX scaled.

**The Test Scenario:**

- **Connections:** Each client establishes a persistent WebSocket connection.
- **Subscriptions:** Each client subscribes to a unique topic (`t/%i`) with QoS 1.
- **Publishing:** A corresponding number of publisher clients send messages to these unique topics.
- **Message Flow:** 1-to-1 communication, with a message rate of approximately 1 message every 10 seconds per connection.
- **Payload Size:** 256 bytes.

All tests were conducted using our open-source [Performance testing framework based on Terraform](https://github.com/emqx/tf-emqx-performance-test) and the powerful [emqtt-bench](https://github.com/emqx/emqtt-bench) load generation tool.

## Stage 1: Establishing a Baseline at 500,000 Connections

Every journey starts with a single step. For us, that was establishing a solid baseline with 500,000 concurrent WebSocket connections.

**EMQX Cluster Setup:**

- **Nodes:** 2 EMQX core nodes
- **Instance Type:** AWS `c7g.4xlarge` (16 vCPU, 32 GiB RAM)

**Results:**

| Metric                    | Value           |
| :------------------------ | :-------------- |
| Live Connections          | 500,000         |
| Message Rate (in/out)     | ~25,000 msg/s   |
| Avg. CPU Usage (per node) | ~51%            |
| Avg. RAM Usage (per node) | ~60%            |
| Network RX/TX (per node)  | ~50 / 54 Mbit/s |

The cluster handled the 500,000 connections with ease. CPU and memory usage were stable and well within healthy limits, leaving plenty of headroom. This successful first stage confirmed our setup was solid and ready for the next challenge.

![image.png](https://assets.emqx.com/images/9590274e4f044cab5136b401199cf312.png)

<center>EMQX Dashboard showing 500k WebSocket connections</center>

## Stage 2: Doubling Down to 1 Million Connections

With the baseline established, we doubled the stakes. The goal was to reach 1 million connections and see if EMQX would scale linearly. To accommodate the increased load, we vertically scaled our cluster nodes.

**EMQX Cluster Setup:**

- **Nodes:** 2 EMQX core nodes
- **Instance Type:** AWS `c7g.8xlarge` (32 vCPU, 64 GiB RAM)

**Results:**

| Metric                    | Value             |
| :------------------------ | :---------------- |
| Live Connections          | 1,000,000         |
| Message Rate (in/out)     | ~50,000 msg/s     |
| Avg. CPU Usage (per node) | ~46%              |
| Avg. RAM Usage (per node) | ~55%              |
| Network RX/TX (per node)  | ~115 / 119 Mbit/s |

![image.png](https://assets.emqx.com/images/d480a5cc6391bb91daaec63c691fb6dc.png)

<center>EMQX Dashboard showing 1M WebSocket connections</center>

## Stage 3: The Summit - 2 Million Connections

Reaching 1 million connections on just two nodes is impressive, but for the 2 million mark, we adopted the standard EMQX architecture for massive-scale deployments: separating the Core and Replicant nodes.

**Why Core and Replicant Nodes?**
This architecture is a cornerstone of EMQX's scalability.

- **Core Nodes:** Handle cluster management, routing information, and data persistence. They are the "brains" of the cluster.
- **Replicant Nodes:** Are stateless and handle the heavy lifting of client connections and message traffic. They can be added or removed from the cluster seamlessly to scale capacity horizontally.

This separation of concerns prevents management overhead from interfering with connection performance, which is crucial at extreme scales.

**EMQX Cluster Setup:**

- **Core Nodes:** 2 x `c7g.2xlarge` (8 vCPU, 16 GiB RAM)
- **Replicant Nodes:** 4 x `c7g.8xlarge` (32 vCPU, 64 GiB RAM)

**Results:**

| Metric                | Value              |
| :-------------------- | :----------------- |
| Live Connections      | **2,000,000**      |
| Message Rate (in/out) | **~100,000 msg/s** |

The resource usage tells a powerful story:

- **Core Nodes:** CPU usage was negligible (~1%), as they were dedicated to management tasks, not connection handling.
- **Replicant Nodes:** Avg. CPU usage ranged from 56% to 69%, and RAM was stable at ~54%. The four replicant nodes efficiently distributed the 2 million connections, with each handling approximately 500,000 clients.

![image.png](https://assets.emqx.com/images/68b2b2f1ce8ef189813db7b41113af77.png)

<center>EMQX Dashboard showing 2M WebSocket connections</center>

#### The Crown Jewel: End-to-End Latency

Handling a massive number of connections is one thing; doing it with low latency is another. At 2 million connections and nearly 100,000 messages per second, the end-to-end latency was exceptionally low.

| Metric                  | Value       |
| ----------------------- | ----------- |
| **e2e_latency_ms_95th** | **0.96 ms** |
| **e2e_latency_ms_99th** | **4.66 ms** |

A 99th percentile latency of under 5 milliseconds at this scale is a testament to the efficiency of EMQX's internal message passing and the performance of its underlying Erlang/OTP runtime. This level of responsiveness is critical for applications where every millisecond counts.

## Key Technical Insights

1. **Linear Scalability is Key:** The journey from 500k to 1M showed that you can predictably scale EMQX by adding hardware resources. The move to 2M proved that you can scale even further by adding more nodes to the cluster.
2. **Core-Replicant Architecture Shines:** For deployments in the millions, the Core-Replicant model is the proven path. It ensures that the cluster remains stable and manageable while the Replicant nodes focus solely on performance.
3. **Efficiency of the Underlying Stack:** This level of performance wouldn't be possible without a highly optimized tech stack. EMQX benefits from the battle-tested Erlang/OTP environment, designed for building concurrent, fault-tolerant systems, and the high-performance [Cowboy web server](https://www.google.com/url?sa=E&q=https%3A%2F%2Fninenines.eu%2Farticles%2Fcowboy-2.13.0-performance%2F) for handling the WebSocket connections.
4. **A Note on Load Balancers:** For maximum performance and to eliminate variables, these tests were conducted by connecting load generators directly to the EMQX replicant nodes. In a production environment, a high-performance TCP/SSL load balancer would be placed in front of the replicant nodes. The test results show that EMQX itself is not the bottleneck.

## Conclusion

The digital world's demand for real-time interaction over the web is insatiable. This benchmark demonstrates that EMQX is more than ready to meet this demand. By successfully supporting **2 million concurrent MQTT over WebSocket connections** in a single cluster with outstanding low latency, EMQX establishes itself as a leading solution for any large-scale application requiring real-time data movement to and from browser clients.

Whether you are building the next generation of collaborative tools, financial trading platforms, or a massive IoT network with a web-based dashboard, you can build with the confidence that EMQX provides the performance, scalability, and reliability you need.

Ready to see for yourself?

- [Download EMQX](https://www.emqx.com/en/downloads-and-install/enterprise) or deploy [EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) completely for free

- Explore the project on [GitHub](https://github.com/emqx/emqx).

- [Contact our team](https://www.emqx.com/en/contact) to discuss your unique use case.

  

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
