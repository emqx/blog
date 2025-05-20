## **About Geely Automobile**

Geely Automobile Group has established design and R&D centers in Shanghai, Ningbo, and internationally, showcasing its strong research and development capabilities.  The company operates world-class manufacturing plants for vehicles and powertrains in China and Malaysia, supported by a network of over 1,400 sales and service outlets worldwide.

Embracing the values of "People-oriented, Innovation, Excellence," Geely’s mission is to "create mobility experiences beyond expectations.” The company is committed to becoming the most competitive and respected Chinese automotive brand.

## **Challenges in Building a Connected Vehicle Platform**

 As automotive intelligence and connectivity continue to grow, user experience has become a core focus for passenger vehicles. Within connected car ecosystems, the infotainment system acts as the primary interface linking drivers, vehicles, and the cloud. By integrating infotainment with a connected platform, automakers can capture real-time vehicle data and user behavior, enabling precise management, predictive maintenance, and personalized services. Mobile app integration further enhances experiences like vehicle tracking and personalized point-of-interest (POI) recommendations. Today, automakers are rapidly transitioning toward data-driven, service-centric platforms – but building these platforms presents several challenges:

- Supporting massive concurrent connections from infotainment systems
- Handling high-throughput, high-concurrency uplink and downlink service data
- Ensuring secure connections and protecting sensitive data
- Maintaining real-time message performance and reliability in complex network environments
- Enabling flexible data routing and storage for diverse business needs
- Guaranteeing message delivery even when vehicles are offline
- Controlling construction costs and reducing long-term maintenance complexity.

## **Geely’s Hybrid Cloud Architecture with EMQX and AutoMQ**

To address these challenges, Geely adopted a hybrid cloud architecture for its connected vehicle platform.

The Telematics Service Provider (TSP) platform operates in a public cloud environment, leveraging EMQX Enterprise—a unified MQTT and AI platform—to deliver high-performance connectivity and real-time data integration for connected vehicles. EMQX’s scalable, reliable, and high-throughput architecture ensures stable transmission and processing of telematics data, freeing Geely’s development teams to focus on upper-layer applications.

Data from TSP applications is transmitted via AutoMQ to the Geely Data Management Platform (GDMP), which provides capabilities such as data ingestion, low-code development, task orchestration, data mapping, quality monitoring, and data services. As Geely’s big data foundation, GDMP supports the full business lifecycle—from R&D and manufacturing to supply, sales, and after-sales service.

With the rise of electrification, intelligence, connectivity, and shared mobility, Geely’s connected vehicle data is growing at a petabyte scale annually, spanning an increasingly wide range of business scenarios. Apache Kafka®, previously a core component, faces new challenges in scalability and elasticity. AutoMQ, a next-generation solution built on Kafka, addresses these challenges by ensuring flexible scaling and stable operation of Geely’s core connected vehicle systems.

## **Solution Workflow**

![image.png](https://assets.emqx.com/images/c182594ebab65147133c0d12974bb065.png)

**Data Reporting:** Vehicles transmit core telemetry via MQTT from their Telematics Control Units (TCUs) to a cloud-based EMQX cluster. The TSP application processes this data, integrating cloud services with in-vehicle systems to support features like emergency assistance, infotainment, autonomous driving support, and FOTA (firmware-over-the-air) updates. An AutoMQ cluster deployed on Geely’s public cloud receives and distributes TSP application data, serving as the core data bus for connected vehicle operations.

**TSP Role:** The TSP acts as a central hub, linking automakers, hardware providers and network operators, and content services. It integrates services like navigation, entertainment, location tracking, security, and remote maintenance, supporting a robust connected vehicle ecosystem.

**Data Flow into GDMP:** Data from the TSP is transmitted through dedicated lines into the GDMP AutoMQ cluster This data includes vehicle connection data from multiple Geely brands – such as Zeekr, Lynk & Co, and Geely Auto – covering information like driving behavior, vehicle health, and compliance with national standards (GB/T32960). Downstream systems like Flink, Spark, and Kafka consume and process this data, which is ultimately stored in a data lake for BI, analytics, and operational reporting.

## **Benefits**

As Geely’s brand portfolio expands, the volume of vehicle connectivity data continues to surge. By adopting the integrated EMQX and AutoMQ solution, Geely has successfully tackled the core technical challenges of building a scalable, future-ready connected vehicle platform

### **EMQX for Data-Driven TSP Development**

1. **Distributed, High Availability Architecture**: 

   Geely’s connected vehicle platforms deploy EMQX clusters in private data centers or public cloud environments, ensuring data protection and compliance. EMQX’s load-balanced distributed architecture supports millions of concurrent infotainment system connections and high-throughput data handling, providing a strong foundation for upper-layer applications.

2. **High-Concurrency, High-Security Vehicle Connections**:

   Vehicles connect over cellular networks using the MQTT protocol.  EMQX’s distributed setup supports millions of connections and enables TLS encryption, one-way or mutual authentication, and PKI/CA integration for robust one-device-one-key security. EMQX also provides real-time connection status monitoring for better operational control.

3. **Reliable High-Throughput Data Transmission:**
   - MQTT’s built-in heartbeat, session persistence, and QoS mechanisms ensure reliable message delivery, even during network interruptions. Lost messages are automatically recovered when vehicles reconnect.
   - With EMQX’s ability to handle millions of TPS (transactions per second), data is routed through logically isolated topics for different upstream and downstream flows supporting both continuous telemetry and targeted messaging (e.g., remote monitoring, POI recommendations, service notifications ).
   - EMQ’s offline messaging ensures that messages destined for temporarily offline vehicles are stored at the access layer and delivered once reconnected. 

4. **Flexible Event Processing and Integration:**

   EMQX's rule engine enables real-time preprocessing and integration of vehicle-reported data into downstream systems like Kafka. Connection and disconnection events, telemetry decoding, and message delivery confirmations can all be seamlessly bridged to backend platforms for analysis and action.

### **AutoMQ for Effortless Scaling and Lower Operational Costs**

1. **Zero-Ops Rapid Scaling:**

   AutoMQ's stream storage architecture leverages cloud storage durability instead of traditional multi-replica models. This allows instant partition reassignment, cost savings, and automatic traffic balancing during scaling, without human intervention.

2. **No Capacity Planning, Reduced Maintenance Overhead:**

   AutoMQ's use of S3-compatible storage eliminates traditional Kafka storage limits and retention concerns. Geely’s infrastructure now automatically handles traffic spikes, freeing the operations team from manual capacity planning and scaling management.

3. **100% Kafka Compatibility:**

   AutoMQ’s full compatibility with Apache Kafka® allowed Geely to adopt the new system without modifying existing applications, tools, or client configurations, preserving prior investments and accelerating migration.

## **Future Outlook**

As Geely advances its "Smart Car AI Everywhere" strategy, the hybrid cloud architecture built on EMQX and AutoMQ will become the core data foundation for its next-generation initiatives. This solution will accelerate Geely’s expansion into smart manufacturing, intelligent driving, and global service networks.

Moreover, this architecture will strengthen Geely's position in electrification and shared mobility, helping set a new benchmark for China's automotive industry transformation – from data-driven to AI-powered intelligence.
