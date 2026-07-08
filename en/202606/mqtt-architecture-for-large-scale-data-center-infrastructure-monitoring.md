> ***Executive Summary***
>
> *A global digital infrastructure provider managing multiple facilities needed to modernize its [industrial IoT](https://www.emqx.com/en/blog/industrial-iot-systems) infrastructure monitoring. The organization faced the challenge of collecting and processing millions of data points per minute from SCADA systems while maintaining low-latency monitoring for critical infrastructure metrics.*
>
> *They deployed EMQX in a hybrid cloud-on-premises architecture using [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) [Sparkplug B](https://www.emqx.com/en/solutions/mqtt-sparkplug) for industrial data semantics. The platform ingests millions of tags across a multi-tier broker topology, processes data in real time, and integrates with cloud and time-series databases. The initial phase achieved high throughput with no infrastructure bottlenecks, enabling rapid global expansion.*

## Large-Scale Data Centers: Overcoming Legacy SCADA Bottlenecks

Large-scale data center operators manage critical infrastructure: power distribution, cooling systems, security, and compute resources across dozens of facilities. As facility density and monitoring requirements have grown, legacy SCADA architectures struggle with the volume and velocity of sensor data.

Modern data centers require real-time visibility into:

- Power systems (UPS, PDU, generator status)
- Environmental controls (CRAC/CRAH temperature, humidity, airflow)
- Security and facility systems
- Facility operations (fire suppression, water systems, fuel tanks)

Infrastructure monitoring has traditionally relied on isolated SCADA networks or cloud-hosted systems with high latency and integration friction. Organizations investing in [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) modernization need a standards-based, scalable platform that bridges on-premises SCADA systems with cloud data analytics while maintaining real-time responsiveness.

## **The Challenge: Scale, Complexity, and 24/7 Mission-Critical Demands**

### **Volume and Velocity**

This organization maintains millions of tags per facility across multiple data centers. With SCADA transmitting changes at sub-10-second intervals and ambient infrastructure constantly fluctuating, the system generates hundreds of thousands of messages per second during peak operations. Growing facility density and expanded monitoring scope will drive several-fold growth in tag volume in the future.

### **Multi-Tier Data Aggregation**

Data flows across multiple layers: local SCADA systems at each facility → campus-level aggregation → regional hubs → cloud analytics. Each tier must handle sub-second device polling while respecting MQTT transmission constraints and network latency. Traditional single-broker deployments cannot support this topology without bottlenecks.

### **Hybrid Cloud and On-Premises Complexity**

The organization operates both cloud infrastructure and on-premises SCADA systems. A unified MQTT platform must seamlessly bridge on-prem systems with cloud-based event processing and storage without sacrificing latency or reliability.

### **24/7 Infrastructure Uptime Requirement**

Data center operations demand continuous monitoring with zero tolerance for message loss on critical infrastructure events. The platform must guarantee QoS 2 delivery, maintain persistent sessions for offline devices, and provide 24/7 enterprise support.

### **Industrial Data Semantics**

SCADA systems require standardized data models that capture device state, timestamps, and quality metrics. Sparkplug B provides this industrial semantic layer, but not all MQTT platforms native support or scale this protocol at 3+ million tag volumes.

## The EMQX Solution: A Hybrid, Multi-Tier Messaging Backbone

The organization deployed EMQX in a two-pronged architecture:

### Regional BYOC + Campus On-Premises

**North America Region**

- 1 BYOC cluster handling regional aggregation: >1,000 concurrent connections, 20 MBps throughput, 500K msg/sec
- 1 on-premises [EMQX Enterprise](https://www.emqx.com/en/products/emqx) cluster at the primary campus: 600 connections, 5 MBps
- Campus cluster forwards data to regional BYOC via cluster linking

**EMEA Region**

- 1 BYOC cluster: 1,000 connections, 15 MBps, 200K msg/sec
- 1 on-premises campus cluster with similar capacity

### Data Flow Pipeline

1. **SCADA Edge**: SCADA system polls OPC-UA devices every ~1 second
2. **MQTT Sparkplug B Transmission**: The MQTT Transmission Module publishes changes to the local campus broker
3. **Campus Aggregation**: Campus broker buffers and deduplicates, routing to regional BYOC via cluster linking
4. **Regional Processing**: BYOC cluster ingests 500K msg/sec and bridges to two destinations:
   - **Cloud Event Streaming**: JSON-formatted events for real-time analytics dashboards (~15 seconds, 10K tag poll rate)
   - **Time-series Database**: Time-series storage for 5M tags (~10 seconds poll rate) with compression and retention policies
5. **Business Applications**: Event-driven notifications routed via MQTT variable timing

### Key Architectural Decisions

- **BYOC Deployment Model**: Managing EMQX in the customer's own cloud account eliminated infrastructure management overhead while maintaining security and compliance.
- **Hybrid Topology**: On-premises campus brokers absorb local SCADA traffic; regional BYOC handles analytics and cross-facility queries. This reduces WAN congestion and respects facility network boundaries.
- **Sparkplug B Standardization**: All SCADA systems publish Sparkplug B messages, enabling automatic device discovery in downstream applications.
- **Data Bridges**: EMQX rule engine and data bridge connectors eliminated custom code for cloud event streaming service and time-series database integration

## Key EMQX Capabilities Enabling the Solution

### **BYOC (Bring Your Own Cloud)**

EMQX Enterprise managed services on the customer's public cloud subscription provided secure, scalable MQTT infrastructure without requiring dedicated ops teams. Managed upgrades, patching, and monitoring reduced operational burden.

### **Sparkplug B Support**

Native Sparkplug B message handling at the broker level enabled auto-discovery of 5M+ tags and preserved industrial data semantics across tiers. No custom deserialization code was required.

### **Multi-Tier Cluster Linking**

Broker-to-broker cluster linking (campus → regional) created a hierarchical topology matching facility geography, enabling efficient multi-tier aggregation without a single point of failure.

### **Data Integration Bridges**

Pre-built connectors to the cloud event streaming service and time-series database eliminated custom code for analytics pipelines. Rules engine SQL-like syntax filtered and transformed Sparkplug B messages in real time.

### **Massive Scalability**

EMQX handled 500,000 msg/sec with 100M+ concurrent connection capacity, validating the platform for 2–3x future growth.

### **Managed Services with 24/7 Support**

Enterprise support SLAs and automated cluster management provided the 24/7 uptime assurance required for critical infrastructure.

## Results and Value Delivered

### **Rapid, Predictable Rollout**

The multi-tier architecture enabled a highly repeatable deployment model, significantly compressing the time-to-value for new campus onboarding from months to weeks. Campus clusters could be added without regional cluster changes.

### **Sub-15-Second Latency at Scale**

Infrastructure monitoring dashboards received updates within 15 seconds for 10K tag poll rates, meeting operations team response requirements for alerts and anomalies.

### **Unified Data Fabric**

Sparkplug B standardization eliminated data interpretation inconsistencies. Downstream analytics teams could auto-discover device topology and ingest clean, semantically rich data from day one.

### **Cost Efficiency**

BYOC deployment shifted capital and operational expense to the customer's existing cloud commitment. On-premises campus clusters leveraged existing facility infrastructure, avoiding redundant cloud egress charges.

### **Future-Proof Growth**

The architecture accommodated 2–3x tag growth without topology redesign. Regional BYOC scaling and new campus cluster deployments could proceed independently.

## Conclusion

By deploying EMQX in a hybrid, multi-tier topology with Sparkplug B standardization, this global large-scale data center operator unified its infrastructure monitoring across multiple facilities. The combination of BYOC flexibility, industrial protocol support, and massive message throughput enabled rapid time-to-value and positioned the organization for accelerated global rollout. EMQX's data integration capabilities eliminated downstream integration friction, delivering clean infrastructure intelligence to operations and analytics teams in real time.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
