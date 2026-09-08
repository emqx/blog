> ***Executive Summary***
>
> *A global telecommunications technology provider needed to modernize its broadband device management platform to support tens of millions of always-online customer premises equipment (CPE) devices across multiple deployments. The platform had to deliver massive concurrent connectivity, support both managed SaaS and customer-dedicated environments, minimize per-device infrastructure costs, and provide seamless integration with downstream data platforms.*
>
> *By adopting EMQX Enterprise, the company built a highly scalable MQTT infrastructure featuring multi-tenant deployment, cross-region resilience, and native Kafka integration for real-time device telemetry.*

## The Challenge: Scaling Broadband Device Management Cost-Effectively



Telecommunications service providers depend on sophisticated device management platforms to remotely configure, monitor, and troubleshoot billions of broadband customer devices globally. 

Managing large fleets of broadband devices presents several unique challenges:

- **Massive persistent connections** with relatively low message volume per device.
- **Multi-tenant deployments** supporting both internal platforms and customer-dedicated environments.
- **Low infrastructure cost per device**, where operational efficiency directly impacts profitability.
- **Real-time remote management** for configuration, diagnostics, and firmware operations.
- **High availability and disaster recovery** across regions.
- **Reliable integration** with downstream analytics and operational systems.

Traditional public cloud IoT services often become increasingly expensive as connection counts grow, making specialized MQTT infrastructure a more sustainable option for large-scale deployments.

## Why MQTT for Telecom CPE Management



Unlike high-throughput IoT workloads, broadband CPE devices maintain long-lived connections while exchanging relatively small amounts of data.

MQTT's design fundamentally aligns with CPE device control architecture:

- **Persistent connections minimize reconnection overhead**: CPE devices can maintain single long-lived MQTT connections, avoiding the connection storms and latency spikes that plague REST-based polling.
- **Publish-subscribe enables efficient command distribution**: Technician-initiated commands (reboot, configuration push, diagnostic request) can target specific devices via topic subscriptions without server-initiated connections or push notification complexity.
- **QoS 1 supports reliable command delivery**: CPE configuration commands must arrive in order and at-least-once; MQTT QoS 1 provides these guarantees natively.
- **Session persistence handles temporary disconnections**: Cellular handoff or temporary WAN failure causes brief disconnection; persistent sessions allow devices to resume without losing command queue context.
- **Lightweight protocol reduces device resource usage**: Embedded CPE devices have modest CPU and memory; MQTT's low bandwidth footprint (vs. REST+JSON) conserves resources for critical device functions.

## The EMQX Solution: A Multi-Region MQTT Backbone



The telecommunications provider deployed EMQX Enterprise as their multi-tenant CPE management backbone:

**Multi-Cluster Deployment**

- Primary SaaS platform: EMQX cluster in primary region
- Dedicated customer environments: Individual EMQX deployments in customer-preferred regions
- Shared multi-tenant environments: Shared multi-tenant EMQX instances with topic-level ACL isolation
- Disaster recovery: A warm standby cluster in a secondary region, with device-side endpoint failover and Cluster Linking bridging the two clusters so northbound applications remain reachable across regions.

**Device Connection Model**: 

CPE firmware initiates persistent MQTT 5.0 connections over TLS 1.3+ to the EMQX cluster. Connections remain open indefinitely (24-hour always-on), with device heartbeat messages every 5-15 minutes.

**Message Pipeline**:

![image.png](https://assets.emqx.com/images/3152f8db2c592470bf45bb2c595195c0.png)

**Authentication & Isolation**:

- Server certificate: TLS 1.3+ with certificate pinning on devices
- Client authentication: Device certificates (X.509) or mTLS, enabling revocation and per-device security
- Topic ACL: Fine-grained access control ensures Tier 1 devices cannot accidentally subscribe to other customers' topics

**Cross-Region Disaster Recovery**: 

A warm standby cluster in a second region absorbs the fleet when the primary is unreachable. Devices fail over at the connection layer via short-TTL DNS and fallback endpoints, reconnecting with randomized backoff to avoid a cutover storm. Sessions are not replicated across clusters, so the platform re-issues unacknowledged commands under idempotent IDs; Cluster Linking keeps command paths reachable while the fleet is split.

## Key EMQX Capabilities Deployed



The deployment leverages several core EMQX Enterprise capabilities:

- **Massive connection scalability** optimized for millions of always-on devices
- **Native Kafka integration** for reliable telemetry delivery
- **Multi-tenant topic ACLs** for secure customer isolation
- **Cluster Linking** for cross-region message routing between primary and standby clusters
- **TLS and mTLS security** for device authentication
- **MQTT 5.0 persistent sessions** for seamless reconnection and state recovery

## Results & Value Delivered



- **Economic Efficiency**: Per-device infrastructure cost for millions of connections is substantially lower than cloud IoT service pricing, directly improving customer pricing competitiveness and SaaS margins.
- **Scalable Multi-tenant Architecture**: Single EMQX deployment pattern replicated for SaaS, Tier 1, and Tier 2 customers eliminates custom integration work for each new customer.
- **Disaster Recovery Confidence**: A warm standby cluster in a second region gives the platform a regularly exercised regional failover path. Because recovery relies on device-side endpoint failover and application-level command re-issue rather than broker state replication, the failure modes are few and well understood — an operational property the provider values more than a lower theoretical RTO.
- **Operational Simplicity**: Kafka integration eliminates custom webhook infrastructure and provides single source-of-truth for device telemetry across analytics, billing, and customer dashboards.
- **Connection Resilience**: Devices reconnecting from varied networks (cellular, cable, fiber, satellite) experience transparent session recovery without application-level complexity.
- **Competitive Advantage**: Infrastructure optimized for massive, low-throughput connections enables aggressive customer pricing while maintaining healthy infrastructure costs, providing a competitive advantage over cloud IoT competitors.

## Conclusion



Managing millions of broadband devices requires infrastructure optimized for persistent connectivity rather than high message throughput.

With EMQX Enterprise, the provider built a scalable MQTT platform that combines high connection density, secure multi-tenancy, disaster recovery, and real-time data integration. The result is a cost-efficient foundation capable of supporting large-scale broadband device management while maintaining high reliability, operational simplicity, and room for future growth.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
