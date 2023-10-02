In our previous blogs, we discussed the concepts of [ISA95](https://www.emqx.com/en/blog/exploring-isa95-standards-in-manufacturing) and [unified namespaces](https://www.emqx.com/en/blog/the-power-of-unified-namespace-in-modern-manufacturing). In this blog, we will explore the intricacies of implementing a unified namespace with EMQX and Neuron, highlighting the synergy between these platforms and the myriad benefits they bring. From data integration and transformation to multi-site data replication, we will show how this integration best addresses the challenges of data organization, scalability and collaboration in an industrial context. By converging EMQX's MQTT capabilities with Neuron's data transformation capabilities, organizations can realize in a new era of unified data access, streamlined processes, and data-driven decision making.

## Unified Namespace Solution with EMQX and Neuron

The [Unified Namespace (UNS)](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) concept redefines data access, allowing all network participants to interact with information, irrespective of its physical location. [EMQX broker](https://www.emqx.com/en/products/emqx) and [Neuron industrial gateway](https://neugates.io/) is a popular choice for implementing UNS due to its efficiency and scalability.

EMQX plays a pivotal role as the central messaging broker, strategically positioned at its core. Neuron supports the EMQX to access OT sensors and devices with various industrial protocols. As the key components for data communication and message routing, EMQX and Neuron together act as the primary conduit connecting data sources, such as devices, sensors, and machines to data consumers, which includes ERP and MES applications, databases, and analytics platforms. This intermediary role enables seamless data exchange within the manufacturing ecosystem, facilitating the flow of information critical to real-time monitoring, control, and analysis.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/0b88fa3cf1c98545e501e3b8073fdccc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Reference Architecture for IIoT Based on UNS
    </div>
    <div class="mb-32">
      To build an efficient and scalable IIoT infrastructure.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-implementing-unified-namespace-using-emqx-and-neuron" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Design of the Common Naming Convention

Unified Namespace, however, is not solely about technology. It's a strategic design approach that organizes data into a coherent structure, fostering contextual understanding. This design creates common naming conventions for participants to access data, enabling collaboration and efficient decision-making across the network. Common naming conventions refer to the set of rules, guidelines, and patterns that dictate how names should be created and used for various entities, objects, variables, files, or other elements within a system, organization, or domain. 

In EMQX broker, every connected device and application adheres to this standardized [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) hierarchy, rooted in a consistent set of naming conventions and data models. This convention ensures that all devices and applications use a standardized framework for addressing and interacting with each other. By adopting the same MQTT topic hierarchy and data models, devices and applications can effortlessly communicate, regardless of their disparate origins or protocols. This eradicates the barriers that might hinder data exchange in heterogeneous environments.

Naming conventions are particularly important in programming, software development, data management, and various other fields to ensure consistency, clarity, and ease of understanding when referring to different MQTT topic names. Moreover, Incorporating the naming conventions into asset management processes can significantly streamline operations, enhance data-driven decision-making, and contribute to overall business success by maximizing the value and efficiency of assets across their lifecycle.

## Architecture for Implementing Unified Namespace

The Unified Namespace solution emerges as a powerful mechanism to seamlessly integrate devices, applications, and data streams. By using EMQX and Neuron, this solution can be architected into a three-tier structure, ensuring efficient data exchange, organization, and consumption. In the diagram shown, all connected devices and applications are separated into two primary layers. The bottom is the automation layer, while the top is the application layer. The middle layer serves as a conduit through which EMQX and Neuron enable seamless data exchange between automation and application layers.

![Architecture for Implementing Unified Namespace](https://assets.emqx.com/images/d3da26da070ac01ba7d632ef5e7f6f44.png)

### Empowering Analytics and Decision-Making

The Application Layer is where the true value of unified data comes to life. Applications residing within this layer possess the capability to dive into the wealth of contextualized data and perform sophisticated analytics. Utilizing this data, applications can uncover patterns, trends, and anomalies that might go unnoticed with raw data. Predictive maintenance, a prime example, enables the proactive identification of potential equipment failures, preventing costly downtime and production interruptions.

### Real-Time Updates for Swift Responses

The architecture's beauty lies in its real-time responsiveness. Applications in the Application Layer can subscribe to specific data points or device nodes, allowing them to receive instant updates. This feature empowers factories to swiftly respond to changes in the production process, maintaining operational agility and adaptability.

### Elevating AI/ML Capabilities

One of the most remarkable advantages of contextualized data is its impact on AI/ML models. By supplementing raw data with additional context and metadata, AI/ML models can better comprehend and interpret the data they receive. This reduction in interpretation errors leads to enhanced accuracy and more reliable insights.

### Enhanced Predictive Capabilities

Contextualized data significantly amplifies the predictive prowess of AI/ML models. The provision of additional context empowers models to make precise predictions about forthcoming events or outcomes. As a result, factories can foresee potential challenges, optimize processes, and make proactive decisions that drive efficiency and productivity.

### Revolutionizing Data Quality and Interpretation

The Application Layer's access to contextualized data serves as a cornerstone in improving data quality. Through the inclusion of metadata and context, data fed into AI/ML models becomes more reliable, leading to higher-quality predictions and outcomes.

## EMQX Clustering for Multisites Data Replication 

The need for efficient data integration and consistent access across disparate industrial systems has given rise to the Unified Namespace Architecture. This transformative approach overcomes data isolation, promotes collaborative synergy, and optimizes data-driven analytics by creating a harmonized environment for data aggregation. There are two types of deployments of the Unified Namespace Architecture as below.

### Single-Sites Deployment

Within a single-site deployment, the architecture revolves around the careful orchestration of various components to create a unified namespace. On the left side of the diagram are the data sources from the production floor, which is the automation layer of the 3-tier architecture above. The right side is the central control room where all data analysis and storage takes place. In the middle is a unified namespace enabled by EMQX and Neuron.

![Single-site deployment architecture](https://assets.emqx.com/images/fd6fc97dc40438f6c11922394afe171c.png)

1. **EMQX Cluster Management:** The foundation is laid by deploying an EMQX broker cluster under the supervision of the EMQX Edge Cloud Platform (ECP). The inherent scalability of the EMQX ECP allows seamless scaling of EMQX instances to address escalating data demands.
2. **Neuron Gateway Integration:** Neuron gateways, also governed by EMQX ECP, play a key role in bridging the gap between on-premises Operational Technology (OT) devices (e.g., PLCs, CNC machines) and Information Technology (IT) systems. Neuron's data format conversion and intercommunication capabilities are used to ensure seamless data flow.
3. **Enabling eKuiper Rule Engine:** The deployment of eKuiper streaming engines, managed by EMQX ECP, is essential for processing streaming messages emanating from IT systems and Neuron gateways. Configuring eKuiper's data storage or command transmission capabilities enriches the processing cycle.
4. **NanoMQ Facilitation:** NanoMQ is strategically deployed as an agile bridge tailored for edge scenarios housing multiple applications. Its lightweight composition ensures optimal data exchange efficiency, particularly for hardware with constrained resources.
5. **Unified Namespace Enrichment:** The synergy achieved through the collaboration of EMQX cluster, EMQX ECP, Neuron, eKuiper, and NanoMQ culminates in the establishment of a Unified Namespace. This expansive realm embraces data from diverse OT devices, IT systems, application platforms (e.g., Kafka, Redis, PostgreSQL), and cloud analytics systems (e.g., AI/ML).

### Multi-Sites Deployment

In a multi-site deployment, the architecture's scope broadens to encompass diverse production sites. The Unified Namespace spans the entire production process, whether vertical or horizontal, across multiple geographic locations. This includes the central control room where all production information, even down to the sensors, is processed by various applications and AI/ML for better decisions.

![Multi-site deployment architecture](https://assets.emqx.com/images/8a62253d083aca31eab9c463791507ba.png)

1. **Inter-Site Data Replication:** EMQX clusters, meticulously distributed across multiple production sites, enable the seamless replication of data messages. This empowers the realization of cross-site data sharing, fostering a unified data ecosystem.
2. **Contextualized Data Organization:** The essence of the Unified Namespace emerges as all data messages find their place within a contextualized structure. The tenets of ISA-95 guide the structuring, capturing assets, processes, and the intricate tapestry of data relationships.
3. **Holistic Multi-Site Advantages:** This architectural extension enables real-time data sharing and harmonized collaboration across disparate manufacturing sites. Decision-makers gain access to synchronized, up-to-date data, fostering informed decisions across the enterprise.

## Conclusion

The deployment of a Unified Namespace architecture, whether in a single-site or multi-site scenario, signifies a revolutionary step toward optimized industrial data integration. By leveraging the collaborative capabilities of EMQX and Neuron, organizations can break down data barriers, foster collaboration, and make data-driven decisions. This unified approach not only enhances operational efficiency but also propels industries toward a more connected and intelligent future, where data flows seamlessly to enable innovation and excellence.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
