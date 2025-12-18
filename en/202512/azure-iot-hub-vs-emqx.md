Azure IoT Hub and EMQX are two of the most widely used platforms for connecting large fleets of devices and moving IoT data reliably at scale. Both are proven in production, but they are built on fundamentally different architectures, and those differences shape their limits, performance characteristics, and long-term cost profiles.

This blog provides a detailed, engineering-focused comparison of Azure IoT Hub and EMQX across architecture, protocol support, routing, scalability, storage, device state, file transfer, security, and operational limits. The goal is to help architects and technical decision makers understand where each platform fits, how they differ, and what tradeoffs emerge as deployments grow.

## **1. Architectural Foundations**

In IoT system design, architecture determines everything from throughput ceilings to protocol flexibility. Azure IoT Hub and EMQX take two fundamentally different approaches.

### **1.1 Partitioned Event Architecture vs Distributed Actor Model**

Azure IoT Hub is built on Azure Event Hubs and uses a partitioned log architecture. Incoming telemetry is written to fixed partitions. Each partition can only be read by one consumer at a time. This creates predictable throughput but also introduces structural read bottlenecks, especially when downstream systems need high parallelism. Retention is typically short-term and optimized for hand-off to Azure services.

EMQX is built on the Erlang/OTP actor model. Each connection is handled by a lightweight process, which gives EMQX extremely high concurrency and predictable low latency. EMQX Enterprise 6.0 extends this architecture with a RockDB-based storage engine that supports durable, asynchronous messaging within the same cluster.

### **Architecture Comparison**

| Feature           | Azure IoT Hub                                                | EMQX Enterprise / Cloud                                      |
| :---------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Core Pattern      | Cloud gateway for ingestion and offload                      | Unified broker with pub/sub and durable queuing              |
| Concurrency Model | Connection rate limited per unit (S1: ~12 per sec)           | Hardware-bound, tested up to 100 million connections         |
| Scaling           | Horizontal scaling through capacity units with fixed resource bundles (S1, S2, S3). Throughput, connections, and storage scale together, which can increase cost for unused dimensions. | Horizontal clustering with resource-granular scaling. Sessions, throughput, and storage can be expanded independently depending on the deployment model. |
| Data Path         | Partitioned log with consumer concurrency capped by partition count | Distributed mesh routing without partition limits            |
| Persistence       | Short-term log storage (1 to 7 days)                         | Dual engine (in memory + RocksDB for durability)             |
| Multi-Tenancy     | One tenant per IoT Hub instance                              | Multi-tenant namespaces within one cluster                   |

## **2. Protocol Fidelity and MQTT Standards**

Azure IoT Hub supports [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) 3.1.1 as a compatibility layer, but not as a full-featured broker. Key MQTT capabilities are missing or limited. EMQX implements native MQTT 3.1, 3.1.1, and 5.0, along with protocols like [CoAP](https://www.emqx.com/en/blog/coap-protocol), LwM2M, and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).

### **MQTT and Protocol Support Comparison**

| Feature              | Azure IoT Hub                | EMQX Enterprise / Cloud        | Practical Impact                                             |
| :------------------- | :--------------------------- | :----------------------------- | :----------------------------------------------------------- |
| MQTT Version         | Partial 3.1.1                | Full 3.1, 3.1.1, 5.0           | Azure cannot use MQTT 5 features such as topic aliases or flow control |
| Topic Structure      | Fixed and device-centric     | Fully customizable hierarchies | EMQX supports broader industrial and multi-tenant patterns   |
| QoS 2                | Not supported                | Supported                      | Required for transactional or high-integrity IoT workloads   |
| Retained Messages    | Ignored                      | Fully supported and durable    | Azure users rely on external databases for last-known-state queries |
| Shared Subscriptions | Not supported                | Supported                      | Enables worker pools and horizontal load balancing           |
| MQTT over QUIC       | Not supported                | Supported natively             | Improves performance for unstable or mobile networks         |
| CoAP, LwM2M, MQTT-SN | Requires an external gateway | Native gateway support         | Constrained devices can connect directly to EMQX             |
| Keep Alive           | Max 1,767 seconds            | Up to 65,535 seconds           | Longer intervals reduce battery usage on cellular devices    |

## **3. Routing, Transformation, and Message Durability**

### **3.1 Routing Engines**

Azure IoT Hub provides basic SQL-like filtering on message headers and bodies. It does not support transformation, enrichment, or dynamic reshaping of payloads. For more complex logic, users rely on Azure Functions or Stream Analytics.

EMQX includes a full SQL-style rule engine with native functions for decoding, encoding, reshaping JSON, running regex, performing math, and calling external APIs. EMQX 6.0 also adds a visual flow designer for building pipelines without writing code.

### **3.2 Durable Queuing in EMQX 6.0**

Azure IoT Hub provides limited cloud-to-device queuing and relies on Event Hubs for device-to-cloud buffering. EMQX integrates durable messaging directly into the broker, supporting:

- Offline persistence
- Last Value Queues for high-frequency telemetry
- Pull-based consumption
- Competing consumers

This can reduce the need for a separate Kafka cluster in mid-sized ingestion architectures.

## **4. Scalability and System Limits**

### **4.1 Azure’s Unit-Based Scaling**

| Unit | Daily Message Limit | Approx Connection Rate |
| :--- | :------------------ | :--------------------- |
| S1   | 400,000             | ~12 per second         |
| S2   | 6,000,000           | ~120 per second        |
| S3   | 300,000,000         | ~6,000 per second      |

Because these units combine multiple resource dimensions, customers often pay for unused capacity or hit connection throttles long before reaching message volume ceilings. Partition count, fixed at creation time, also directly limits consumer concurrency.

### **4.2 EMQX Resource-Based Scaling**

EMQX supports extremely high connection density thanks to the Erlang actor model. A single 23-node EMQX 5 cluster supported 100 million concurrent MQTT connections in testing. Processing is hardware-bound. There are no fixed daily message caps, and scaling is linear with added compute resources.

## **5. Device State, File Transfer, and Remote Access**

### **5.1 Device State Models**

Azure offers Device Twins, a managed JSON document with desired and reported properties. It integrates cleanly with Azure services and offers query support.

EMQX uses retained messages and Last Value Queues to maintain device state. This enables immediate reads of the latest values but does not include Azure’s built-in desired versus reported synchronization. Applications that need that pattern typically implement it within backend logic.

### **5.2 File Transfers**

Azure IoT Hub handles file uploads through SAS URLs. Devices must support HTTPS, handle token rotation, and upload directly to Blob Storage.

EMQX allows file transfers over the existing MQTT connection. This avoids adding a second protocol stack to devices, supports resumable uploads, and allows bandwidth shaping to prevent file transfers from impacting telemetry.

### **5.3 Remote Access**

Azure Device Streams offer secure bi-directional TCP tunneling for remote access, though the feature remains in preview. EMQX does not ship a remote-access product but can support custom tunneling approaches using binary payloads and topic routing.

## **6. Security and Multi-Tenancy**

### **6.1 Authentication and Authorization**

Azure IoT Hub integrates with Microsoft Entra ID for management plane access and supports X.509, SAS tokens, and TPM attestation for devices.

EMQX supports authentication with internal databases, JWT, LDAP, and external REST services. Its ACL system offers fine-grained topic-level permissions.

### **6.2 Multi-Tenancy Approaches**

Azure IoT Hub is single tenant per instance. SaaS providers typically deploy separate hubs per customer.

EMQX Enterprise 6.0 supports namespace-based multi-tenancy, allowing multiple customers or business units to share a single cluster while maintaining isolated access control, topics, and data integrations.

## **7. Pricing Models and TCO**

Azure IoT Hub pricing is based on units and message metering. Messages are billed in 4 KB chunks, which often inflates costs for small payloads. Users must provision for peak load and cannot scale to zero.

EMQX pricing varies by deployment model:

- **Serverless**: Pay for session minutes and bandwidth. Ideal for variable or intermittent fleets.
- **Dedicated Flex**: Scale sessions and throughput independently. Useful for high-connection, low-TPS workloads such as smart meters.
- **Self-hosted**: Reduces cost further by managing infrastructure directly.

### **7.1 Example Cost Scenario**

**50,000 devices sending 1 KB every 10 minutes**

- 7.2 million messages per day
- Azure S2 supports 6 million per day
- Requires two S2 units, about 500 dollars per month
- EMQX Dedicated Flex costs about 250 to 350 dollars per month

Higher message rates widen the cost gap because Azure users must upgrade entire units, while EMQX costs scale mainly with bandwidth.

## **8. Operational Limits**

| Metric              | Azure IoT Hub S1         | Azure IoT Hub S3          | EMQX Dedicated Flex          | EMQX Enterprise       |
| :------------------ | :----------------------- | :------------------------ | :--------------------------- | :-------------------- |
| Max Connections     | 1,000,000                | 1,000,000                 | Scales with configuration    | Tested to 100 million |
| Throughput          | 100 or 12 per second     | ~6,000 per second         | ~10,000 per deployment       | Hardware bound        |
| Max Message Size    | 64 KB C2D, 256 KB D2C    | Same                      | 1 MB default, 10 MB optional | 256 MB                |
| File Uploads        | 1.67 per second per unit | 83.33 per second per unit | Included in the message rate | Hardware bound        |
| Retained State Size | 40 KB                    | 40 KB                     | 1 MB                         | 256 MB                |

## **9. When to Choose Each Platform**

Azure IoT Hub is a strong choice for teams that depend heavily on Azure services such as Digital Twins, Functions, or Cosmos DB, and prefer a fully managed device lifecycle. It is suitable for moderate scale, straightforward MQTT usage, and architectures that benefit from Azure’s ecosystem integration.

EMQX is preferred when deployments require high connection density, full MQTT 5.0 support, multi-protocol gateways, multi-tenant architectures, or when cost predictability and multi-cloud routing are priorities. EMQX is also advantageous for organizations that want more control and the ability to run the same data plane across cloud, on-premises, and edge environments.

If you want to explore the practical business and architecture reasons customers decide to switch, you can review [**our page outlining the key reasons teams switch from Azure IoT Hub to EMQX**](https://www.emqx.com/en/switch-from-azure).

*This comparison reflects product features and pricing as of December 2025. Both Azure IoT Hub and EMQX evolve over time, so it is always a good idea to confirm current limits and pricing in the official documentation.*



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
