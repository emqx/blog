> ***Executive Summary***
>
> *To expand from regional deployments to a global platform, a leading physical security solutions provider delivering cloud-based access control and camera management systems deployed EMQX Enterprise across a multi-region architecture spanning the United States and EMEA. By leveraging Cluster Linking, the solution enables seamless cross-region event routing with sub-500 ms latency and QoS 2 reliability, ensuring every access control event is delivered exactly once.* 
>
> *This unified MQTT backbone eliminates the need for complex custom replication, allowing thousands of customer sites to connect to the nearest data center while maintaining a centralized, audit-grade record of all security events.*

## The Shift to Cloud-Native Physical Security SaaS

Physical security is transitioning from isolated, on-premises systems to cloud-native, multi-tenant SaaS platforms. Organizations operating globally, with offices, warehouses, and facilities across continents, require centralized access control, audit logging, and real-time event notification across all sites.

Modern access control platforms must support:

- **Real-time event delivery**: Door unlock/lock commands, access denials, intrusion alerts
- **Multi-tenant isolation**: Separate customer data and events; enforcing strict access boundaries
- **Global low-latency performance**: Users and cameras anywhere should report events sub-second
- **Audit-grade reliability**: Every access event must be recorded with QoS 2 guarantees (no loss, no duplication)
- **Legacy device integration**: Support for RFID readers and door controllers, and on-premises systems via webhooks and APIs

## The Challenge

A global physical security solutions provider faces a unique challenge: how to build a global infrastructure that feels local. 

**Cross-Region Message Delivery**

Subscribers in one region need to receive events published in another. For example, a security officer logged into the EMEA cluster must be notified when access is denied at a North American facility. Traditional regional MQTT deployments require clients to connect to every region or events to be replicated via external services. Both approaches introduce latency, cost, or operational complexity.

**Latency-Sensitive Security Events**

Access denials and intrusion alerts must propagate globally with minimal latency. Queuing delays or asynchronous replication introduce unacceptable lag in security responses. A client connecting to the nearest datacenter should receive events sub-second, whether or not they originate in that region.

**Guaranteed Delivery at Scale**

Every door unlock, access grant, and alert must be logged without loss or duplication, even if clusters fail or clients disconnect temporarily.

**Multi-Datacenter Operations**

Operating three independent MQTT clusters without a native broker-linking mechanism forces customers to build custom replication logic: SNS/SQS subscriptions, Kafka bridges, or manual topic synchronization. This increases operational burden and introduces consistency risks.

**Cost Efficiency in Multi-Region Deployments**

Cross-region data transfer charges accumulate quickly if events are forwarded via external message queues. A solution that minimizes inter-cluster traffic without sacrificing reliability reduces both cost and operational complexity.

## Why MQTT?

MQTT emerged as the ideal protocol for this use case:

**Real-Time Event Delivery**

MQTT's publish-subscribe pattern decouples event publishers (access control gateways) from subscribers (web dashboards, mobile apps, logging systems). Events propagate instantly without polling or callback overhead.

**Lightweight Protocol**

MQTT's small header overhead (2-4 bytes) and binary payload support minimize bandwidth per event, critical for cost-sensitive multi-region deployments serving thousands of concurrent devices and users.

**QoS 2 Exactly-Once Semantics**

MQTT QoS 2 implements a two-phase commit-like protocol, ensuring no message loss and no duplication even if brokers or clients crash mid-transmission. This satisfies audit and compliance requirements for access control.

**Message Persistence and Durable Sessions**

MQTT brokers can persist offline client subscriptions and buffer messages. When a client reconnects, it automatically receives missed events, critical for mobile apps and offline-capable devices.

**Lightweight Device Support**

Traditional access control hardware (RFID readers, door controllers) can publish events via MQTT with minimal CPU and memory overhead, enabling cost-effective device integration.

## The EMQX Solution: Orchestrating Cross-Region Physical Security

### Multi-Region Cluster Architecture

The organization deployed EMQX Enterprise in three geographically distributed clusters:

| Region         | Datacenter | Connections (Phase 1) | Cluster Linking                                |
| :------------- | :--------- | :-------------------- | :--------------------------------------------- |
| US (Primary)   | US East    | ~5,000                | Linked to both US West & EMEA via cluster link |
| US (Secondary) | US West    | ~5,000                | Linked to both US East & EMEA                  |
| EMEA           | EU Central | ~5,000                | Linked to both US West and East                |

### Latency-Based Client Routing

- **Geographic Load Balancing**: DNS returns the nearest cluster IP based on client geolocation
- **Client Connection**: Devices and applications connect to their local cluster (e.g., European users → EMEA cluster)
- **Cross-Region Event Delivery**: Cluster Linking enables MQTT message routing between clusters; a subscriber in EMEA automatically receives events published in the US

### Event Flow Architecture

![image.png](https://assets.emqx.com/images/e68ecf3e7468cd4c5177efa2b33ddb47.png){.mx-auto .block}

### Key Integration Points

**Real-time Update and Access Control Middleware**

Legacy access control systems publish events via a custom middleware layer to the local MQTT cluster. The middleware handles protocol translation from native access control APIs to MQTT Sparkplug or standard JSON payloads.

**MongoDB Persistence**

All events are persisted to both cloud and local MongoDB instances via EMQX rules engine. This provides long-term audit logs and enables historical queries (e.g., "all access denied events in the last 30 days").

**AWS SNS/SQS Integration**

Customer-facing webhooks and third-party integrations (Slack alerts, security monitoring services, SIEM systems) subscribe to SNS topics published from MQTT events. EMQX rules bridge MQTT → SNS → SQS for reliable async event distribution.

**Legacy Client and Unified Client API Layer**

Legacy cloud application and modern mobile apps interface via the unified client API gateway, which subscribes to MQTT topics and translates to REST/gRPC. This decouples app development from MQTT changes.

### Multi-Tier Non-Production Environments

- **Development Cluster**: Isolated EMQX cluster for feature validation and performance testing
- **Test Cluster**: Replicates production topology (three-region), used for integration testing before deployment

![image.png](https://assets.emqx.com/images/44198e193aa7514daa6392b987da2716.png){.mx-auto .block}

## Key EMQX Capabilities Enabling the Solution

### **Cluster Linking**

EMQX Enterprise's broker-to-broker Cluster Linking feature enables bi-directional message routing between independent clusters. A topic published in one region is automatically replicated to subscribers in all linked regions, eliminating the need for external message queues or custom replication logic. Cluster Linking preserves QoS 2 guarantees across region boundaries.

### **Multi-Region High Availability**

Each region operates an independent cluster with internal replication (HA) and external cluster linking. Failure of one region does not affect the others; subscribers in surviving regions continue receiving events via cluster links.

### **QoS 2 Reliability at Scale**

EMQX's optimized QoS 2 implementation maintains exactly-once delivery semantics across all regional clusters with headroom for 10x growth.

### **Rules Engine and Data Bridges**

Pre-built connectors to MongoDB (event storage) and AWS SNS (webhook distribution) eliminate custom code. EMQX rules filter and route events based on topic patterns (e.g., "route all /access/denied/* events to MongoDB and SNS").

### **Session Persistence**

EMQX stores session state for mobile and web clients, enabling automatic reconnection and missed message replay when clients come online after temporary network loss.

### **Webhook Integration**

Native webhook publishing allows EMQX to send HTTP POST events to third-party systems (Slack, Azure Monitor, customer logging services) without requiring external ETL tools.

### **Enterprise Support and Managed Services**

24/7 support and operational guidance ensure reliable multi-region deployments and SLA compliance.

## Results and Value Delivered

### **Successful POC Validation**

Completed trial POC confirmed latency, load, and publish/subscribe performance met production requirements. No platform changes were needed after POC completion: EMQX was production-ready on day one.

### **Simplified Multi-Region Operations**

Cluster Linking eliminated the need to build custom message replication logic. Operators maintain three independent clusters with automatic cross-region event flow, reducing operational complexity and human error.

### **Sub-Second Latency Globally**

Latency-based routing ensures clients connect to the nearest datacenter; typical latency for access control events is <500 ms globally. Cross-region subscribers receive events via cluster links within seconds, suitable for security officer dashboards and audit systems.

### **Compliance-Grade Audit Logging**

QoS 2 guarantees and MongoDB persistence ensure every access event is recorded exactly once, with full timestamp and metadata. Regulatory audits and incident investigations have a complete, tamper-proof event log.

### **Cost Efficiency**

Cluster Linking reduces inter-region replication costs compared to SNS/SQS-based replication. Event delivery stays within the EMQX cluster network, minimizing AWS egress charges.

### **Vendor Lock-In Avoidance**

Built on open standards (MQTT) allows the organization to migrate clients or integrate new third-party systems with minimal friction. The platform is not dependent on AWS-only services for core functionality.

### **Rapid Rollout to Customers**

The platform launched as a new global offering, supporting immediate scaling to thousands of customer sites. New customers onboard in the nearest region without infrastructure changes.

## Conclusion

By deploying EMQX Enterprise with Cluster Linking, this global physical security provider built a truly global access control platform. Cross-region broker linking enables subscribers anywhere to receive events published anywhere else, with automatic latency-based routing and QoS 2 reliability. The combination of MQTT's real-time semantics and EMQX's multi-region capabilities eliminated the need for complex external replication logic, reducing time-to-market and operational burden. The solution serves as the foundation for a new generation of cloud-native security systems that scale globally without compromise.


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
