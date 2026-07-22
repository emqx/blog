> ***Executive Summary***
>
> *A large water and wastewater utility managing critical water and wastewater systems across a massive geographic footprint, faced a fragmented technology landscape spanning SCADA systems, IoT sensors, pressure sensors, hydrometers, and programmable logic controllers (PLCs) from different vendors. Evaluating a centralized MQTT infrastructure to unify these diverse systems, the organization deployed EMQX Enterprise combined with EMQX Neuron industrial protocol gateway to handle large-scale endpoint data ingestion while converting legacy protocols (OPC-UA, Modbus, Ethernet/IP) into standard MQTT messages. The result: unified endpoint management across critical water infrastructure with seamless integration into existing historian systems.*

## Smart Water Infrastructure: The Race to Modernize Critical Utilities

Water utilities face unprecedented pressure to modernize aging infrastructure while maintaining service reliability for millions of customers. Digital transformation in the water sector requires:

- **Real-time sensor visibility** across vast geographic territories (hydrometers, pressure sensors, level sensors, flow meters)
- **Legacy infrastructure integration** unifying decades-old SCADA systems with modern IoT deployments
- **Multi-protocol translation** converting industrial communication standards (OPC-UA, Modbus, Ethernet/IP) into unified message streams
- **Massive connection scaling** as utilities expand sensor coverage and remote operation capabilities
- **Reliable data flow** to historian systems for compliance reporting and operational analysis
- **High availability** because service interruptions directly impact customer safety and municipal services

Utilities historically operated isolated protocol islands: SCADA networks disconnected from IoT systems, which operated separately from cloud monitoring platforms. Modern operations require unified visibility without sacrificing the reliability and security of critical infrastructure.

## The Challenge: Fragmentation, Massive Scale, and Zero-Downtime Mandates

- **Massive Endpoint Proliferation:** The utility needed to scale from isolated, facility-level open source MQTT broker instances to a single enterprise-wide system capable of anchoring one million concurrent endpoints.
- **Protocol Heterogeneity:** Operational data was trapped in vendor-specific silos, including SCADA networks running OPC-UA, legacy PLCs running Modbus, and newer IoT sensors using Ethernet/IP.
- **Rigid Historian Dependencies:** The existing data historian represents the single source of truth for compliance. The new IoT architecture had to integrate natively without disrupting or replacing this core system.
- **Multi-Environment Lifecycles:** The team required multiple isolated environments to validate configurations without risking public water safety.
- **Mission-Critical Delivery Safeguards:** Water management leaves no room for data loss; missing or dropped messages could lead to catastrophic service disruptions.

## The EMQX Solution: A Unified, Protocol-Agnostic Data Backbone

The organization deployed EMQX Enterprise paired with EMQX Neuron industrial gateway to create a unified, protocol-agnostic infrastructure:

![image.png](https://assets.emqx.com/images/ba7e459da01d8c093f27cf19ae0c3005.png)

- **Multi-Protocol Edge Translation:** EMQX Neuron instances deploy at regional facilities to ingest large volumes of industrial tags without requiring hardware modifications.
- **Centralized MQTT Aggregation:** Translated edge data is published as a unified MQTT stream to a cloud-hosted EMQX Enterprise cluster scaled for one million active connections.
- **Environment-Specific Guardrails:** Independent broker instances separate development and testing from production, backed by automated active-passive failover for disaster recovery.
- **Direct Historian Streaming:** Data flows from EMQX to the enterprise historian via low-latency data bridges, utilizing topic mapping that mirrors the utility's operational hierarchy.

## Key EMQX Capabilities Enabling This Solution

- **Massive Connection Headroom:** EMQX Enterprise provides the structural capacity to maintain 1M+ concurrent connections with low resource overhead, avoiding cost-prohibitive cloud vendor lock-in.
- **Native Industrial Gateway Integration:** EMQX Neuron converts industrial protocols (OPC-UA, Modbus, Ethernet/IP) to MQTT natively at the edge, bridging decades of installed equipment with modern infrastructure.
- **QoS 2 Exactly-Once Delivery:** Enforces strict execution of operational commands and compliance tracking, eliminating the risks of duplicated or ambiguous message states.
- **Out-of-the-Box Data Bridges:** Pre-built connectors pipe high-velocity data directly into enterprise historian systems without custom wrapper code or intermediate ETL databases.
- **Unified Role-Based Security:** Features central multi-protocol authentication, topic-level access control lists (ACLs), and automated audit logging to trace every command back to its source.

## Results and Business Value

- **Unified Operational Visibility:** Replaced fragmented, facility-level views with a single, real-time dashboard monitoring one million endpoints across treatment plants and distribution networks.
- **Massive Capital Expense Savings:** Prolonged the lifecycle of functional, legacy industrial equipment by using software-based protocol translation instead of tearing out and replacing field hardware.
- **Elimination of Integration Middleware:** Simplified the technical stack and lowered total cost of ownership (TCO) by removing expensive, standalone translation middleware in favor of native EMQX-to-historian data bridges.
- **Audit-Ready Regulatory Compliance:** Achieved flawless compliance reporting with guaranteed QoS 2 data delivery and complete audit trails for water safety regulators.
- **Future-Proof Scalability:** Established an elastic, cloud-native foundation ready to scale from one million to multiple millions of endpoints as smart city and IoT infrastructure expands.

## Conclusion

By deploying EMQX Enterprise alongside EMQX Neuron, this water utility successfully transformed a fragmented network of legacy equipment into a unified, high-performance digital fabric. The solution proves that public infrastructure can modernize rapidly without abandoning existing capital investments. By securing massive connections, providing native protocol conversion, and guaranteeing absolute data integrity to the core historian, EMQX has delivered a secure, scalable blueprint for next-generation municipal utility management.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
