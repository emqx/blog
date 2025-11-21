In Internet of Things (IoT) systems, data immediacy and service availability are paramount to business success. Downtime in any software or server can lead to massive device disconnections, critical data loss, and halted operations. Consequently, a robust IoT infrastructure necessitates an industrial-grade reliable MQTT platform.

A recent case study highlights EMQX's exceptional resilience: An enterprise's dual-node EMQX cluster achieved an astonishing **1770 days of continuous operation** since 2020. The only cause of a final node shutdown was **physical hardware failure** (a motherboard fault), not a software defect.

Significantly, during the failure, load balancing mechanisms enabled clients to perform a **sub-second, zero-downtime failover**, ensuring uninterrupted data flow. Once the hardware was replaced and the node was restored, the system service automatically self-healed.

This incident begs a key technical question: **How does the system guarantee business continuity and achieve such seamless recovery when faced with underlying hardware faults?**

This article explores the technical foundations of EMQX's stability, focusing on the **fault-tolerant design of Erlang/OTP** and the **EMQX clustering architecture**.

## EMQX’s Technical Foundation: Erlang/OTP’s Fault-Tolerant Philosophy

EMQX is built on Erlang/OTP, a platform that fundamentally guarantees its industrial stability and high availability. Erlang/OTP is specifically engineered for high-concurrency, fault-tolerant distributed systems, providing a robust architectural core for EMQX.

In EMQX, essential functions—including client connections, session management, and message routing—are encapsulated in separate, lightweight Erlang processes. This Shared-Nothing architecture eliminates memory-sharing conflicts, ensuring precise fault isolation.

This design underpins Erlang’s distinctive "*Let It Crash*" philosophy. This is not error tolerance, but a proactive recovery strategy. Developers avoid writing exhaustive defensive code; instead, when a process crashes, a dedicated **Supervisor** immediately intervenes. It restarts the failed process based on a preset policy, automatically restoring stability.

EMQX is structured as a sophisticated **Supervision Tree**. If an isolated client session process fails, its Supervisor instantly restarts only that process according to the policy. This guarantees zero disruption to other clients on the same node. This granular fault management is key to EMQX’s sustained reliability.

## EMQX Cluster Architecture: High Availability Against Hardware Failure

While Erlang/OTP lays the groundwork for EMQX stability, the EMQX cluster architecture extends this advantage system-wide, allowing it to easily handle hardware failures at the physical machine level.

### Mnesia Full-Mesh Cluster: Ensuring Data Consistency

The EMQX cluster is built around Mnesia, the Erlang distributed database, utilizing a **Full-Mesh topology**. This structure ensures all nodes are peers, interconnected for real-time data synchronization. Every node maintains a complete replica of all sessions and subscriptions within the cluster.

In the dual-node scenario of this case study, this design was crucial for achieving **"zero-downtime failover."** When a client reconnects to a healthy node after an outage, that node must instantly possess the client’s full session and subscription details.

The Mnesia Full-Mesh perfectly addresses this: as the failed EMQX node exited the cluster, the healthy node had already received the client's latest state via real-time synchronization. Upon reconnecting, the client finds a **"twin" service** fully aware of its session, enabling seamless business takeover.

### Synergy with Load Balancers: Non-Disruptive Client Failover

In production, EMQX clusters are typically deployed behind a Load Balancer (e.g., HAProxy) for High Availability and load distribution. When an EMQX node fails due to hardware issues, the Load Balancer instantly detects the change and automatically routes new client connection requests to the cluster's healthy nodes.

This mechanism is the key to **sub-second, zero-downtime client failover**. Though clients on the downed node are instantly disconnected, the Load Balancer ensures that their reconnection attempts are automatically directed to available nodes, enabling rapid business recovery with minimal impact.

### Session Persistence and Offline Messages: Safeguarding Continuity

Beyond cluster-level data synchronization, the MQTT protocol’s session persistence mechanism provides a core guarantee for continuity. Using `Clean Session=false (Persistent Session)`, the EMQX cluster fully retains the client’s session state and subscriptions even if the client disconnects due to network instability or server failure.

When a client requests a persistent session with setting `Clean Session=false`, EMQX creates a session object, which Mnesia synchronizes across all nodes, ensuring cluster-wide session protection. If the client disconnects abnormally, all messages published to its subscribed topics are automatically cached.

### From Repair to Regeneration: Smooth Service Recovery

In this hardware failure event, once the physical motherboard was replaced and restarted, the EMQX service on the recovered node executed an automatic, defined process: it first cleans up any potentially incomplete local data, then synchronizes complete session and routing information from healthy nodes, quickly returning to a cluster-consistent state.

This **"rejoin"** process is fully automated, requiring no manual intervention, demonstrating Erlang/OTP’s self-healing capabilities and the EMQX architecture’s robustness. Concurrently, the Load Balancer’s health checks immediately readmit the node back into service.

The entire procedure results in virtually zero business impact: clients maintain normal communication via other healthy nodes during the entire outage and recovery, achieving uninterrupted business continuity.

## Summary

The impressive **1770 days of continuous stable operation** perfectly validates the **"Let It Crash" philosophy** and the robust EMQX architecture.

This case study demonstrates that for reliability-critical fields like IoT, a truly resilient system must incorporate **fault consideration and tolerance design at every layer**. Based on this principle, EMQX has built a reliable fault-tolerant system from the ground up. By collaborating effectively with external components, EMQX ensures business continuity even when facing extreme hardware failures, fully showcasing its exceptional reliability as an enterprise-grade IoT messaging platform.

In crucial sectors such as **Industrial IoT, Internet of Vehicles (IoV), financial payments, and energy**, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) often carries core business data streams. Even a single minute of downtime can disconnect tens of thousands of devices or lead to severe safety incidents. Stability is, therefore, the lifeline.

EMQX's achievement of 1770 days of uninterrupted operation confirms its architecture meets the high availability requirements of carrier-grade systems. It successfully delivers a **"24/7" sustained service capability** and provides customers with an SLA approaching 100%. This success is no accident; it is the inevitable result of a combination of advanced system architecture, high-quality code implementation, and a comprehensive operations and maintenance framework.

## Outlook: Advancing Resilience and Scale

While this case highlights EMQX's excellent performance during unexpected failures, EMQX 5.0 and subsequent versions build on this core HA capability by further enhancing system operability and resilience, achieving breakthroughs in **planned maintenance** and **ultra-large-scale deployment**.

### Node Evacuation and Cluster Rebalancing

The **Node Evacuation and Cluster Rebalancing** feature in EMQX 5.0 is designed specifically for planned maintenance scenarios. Before version upgrades or hardware expansion, operations staff can safely and controllably migrate connections and sessions from one node to others in the cluster. This mechanism effectively prevents the **"reconnection storm"** caused by mass restarts during large-scale cluster maintenance, ensuring a smooth and orderly process.

### Innovative Architecture: Core and Replicant Nodes

To support greater scale and enhanced horizontal scalability, EMQX 5.0 restructured the cluster architecture, evolving from a Full-Mesh Mnesia topology to a **hybrid Core-Replicant architecture**:

- **Core Nodes:** Responsible for core transaction processing and data synchronization, forming a fully interconnected cluster.
- **Replicant Nodes:** Act as stateless nodes that passively replicate data from Core Nodes, without participating in transaction processing.

This new architecture significantly boosts cluster scalability and simplifies the management of massive deployments.

### Cross-Cloud Connectivity: Multi-Cloud HA Architecture

Responding to the trend of IoT globalization and multi-cloud deployment, EMQX uses the **Cluster Linking** feature to connect multiple independent EMQX clusters into a unified, highly available messaging platform. This feature provides:

- **Unified Messaging:** Seamless communication between clients connected to EMQX clusters across different cloud platforms.
- **Cluster Disaster Recovery:** Automatic business takeover by interconnected clusters if a single cloud region fails, ensuring service continuity.
- **Simplified Cross-Cloud Communication:** Built-in optimization ensures reliable message routing between cross-cloud clusters.
- **Multi-Cloud Strategy Support:** Enables enterprises to build infrastructure not reliant on a single cloud vendor.

Through various network interconnection solutions like NAT gateways and VPNs, EMQX supports seamless cross-cloud cluster communication, delivering higher bandwidth, lower latency, and more reliable performance for critical IoT applications.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
