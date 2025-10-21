In today's complex industrial and commercial landscapes, managing data from a single site can be challenging. Now, imagine capturing and making sense of **500,000 data points** from operations spanning across multiple buildings and even continents. This was the reality for a recent customer, a global enterprise grappling with a tangled web of disconnected systems, fragmented data, and limited visibility for their ESG (Environmental, Social, and Governance) and carbon footprint reporting. They shifted to UNS with [EMQX](https://www.emqx.com/en/products/emqx) and [NeuronEX](https://www.emqx.com/en/products/neuronex) to achieve this.

## Why Get Rid of Traditional ESG Reporting?

Instead of relying on aggregated electricity bills for ESG reporting, this enterprise chose to gather data directly from its equipment and power meters. This is because electricity bills just provide a single, aggregated number for energy consumption, which is often a monthly or quarterly total. This data is sufficient for a basic, “location-based" calculation, but lacks the detail needed for a truly accurate and effective carbon footprint analysis. 

By monitoring equipment directly, they can:

- **Pinpoint the Hotspots**: Identify which specific machines or processes are the highest energy consumers. This level of detail is crucial for prioritizing decarbonization efforts. For example, they might find that a single, older machine is responsible for a disproportionate amount of their factory's electricity use.
- **Identify Inefficiencies**: Real-time or granular equipment data can reveal energy spikes or waste during specific times, such as when a machine is idle or running at a low load. This allows the company to implement operational changes to improve energy efficiency and reduce emissions.
- **Improve Verification**: Using detailed, equipment-level data provides a more robust and verifiable basis for carbon accounting. It adds a layer of credibility that a simple utility bill cannot, which is important for stakeholders and for complying with stringent reporting standards.

## Overcoming the Challenges of Communication and Interoperability

With their ESG accounting platform ready in a private cloud data center, the next step was to ingest energy consumption details from everywhere. However, they quickly encountered a major difficulty, a complex mix of legacy communication standards and maintenance factors that created significant interoperability challenges. 

To overcome this, they deployed **NeuronEX** as a critical edge-to-cloud data gateway. NeuronEX addresses the issue of interoperability by supporting over 70 industrial protocols, from [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) TCP to Siemens S7 and [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol), enabling it to collect data from a vast range of heterogeneous devices.

It then seamlessly translates this diverse data into a unified protocol, such as **[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)** or its industrial variant **Sparkplug**. As a key protocol in the **Industrial Internet of Things (IIoT)**, MQTT is far more suitable than legacy industrial protocols like **OPC UA** for remote transmission. Its lightweight, publish-subscribe architecture minimizes network traffic by only sending data when a change occurs, which is a sharp contrast to the client-server model of OPC UA. This design is specifically tailored for the low-bandwidth and unreliable connections, which are common in remote locations, over WANs and the Internet.

## UNS: A Scalable and Self-Sustaining Solution

Once the data is standardized, it is published to a central **EMQX** broker in the private data center. EMQX is built to handle a high volume of data ingestion from millions of concurrent connections, ensuring it can receive and process energy consumption data from all locations without performance bottlenecks. This data is then organized into a logical, hierarchical tree structure, a key feature of the **[Unified Namespace (UNS)](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot)** architecture that provides a single source of truth for all operational data. EMQX's extensive library of built-in data connectors allows the ESG accounting platform to easily subscribe to the energy consumption data it needs, integrating with systems like databases, data lakes, and business intelligence tools. This entire system is a perfect example of the convergence of **Information Technology (IT)** and **Operational Technology (OT)**, leveraging IT infrastructure to manage and analyze data from physical OT assets.

![image.png](https://assets.emqx.com/images/59166de61a63a2ec0e7bce4cad1b5a6a.png)

A major benefit of this system is its efficiency, thanks to NeuronEX's support for **report by exception**. Instead of constantly sending data at fixed intervals, NeuronEX only transmits information when a pre-defined change or "exception" occurs. For example, a sensor might only publish a new reading to the central broker if the value has changed by a certain percentage or exceeded a specific threshold. This approach drastically reduces the amount of data sent over the network, lowering operational costs and increasing the reliability of communication, especially in environments with unstable or limited bandwidth. By focusing on transmitting only the most critical and relevant updates, NeuronEX ensures that the ESG accounting platform receives timely and actionable data without the unnecessary overhead of constant, redundant reporting.

## AI-Powered Troubleshooting for Scalable ESG Reporting

The combination of EMQX and NeuronEX together provides a powerful and scalable solution for managing a large number of connected devices, which is critical as a business grows and its ESG reporting requirements expand. This is facilitated by a centralized management console that offers a comprehensive configuration table for all connected data points and their link statuses. This allows in-house engineers to easily monitor the health of the entire system at a glance.

When an issue arises, the platform provides a specific **error code** next to the troubled connection point, which an engineer can use to quickly diagnose the problem. This process is further enhanced by a linked **knowledge base** powered by a large language model (LLM). This AI-driven knowledge base acts as an intelligent assistant, providing conversational guidance to explain what the error code means and offering step-by-step instructions on how to resolve it. This feature significantly reduces troubleshooting time and the need for external support.

It is like a **Manufacturing Floor Assistant.** For example, an operator on the factory floor encounters an error code on a machine, like "Error 3008: Modbus timeout." With LLM, the machine can send not just the error code, but also contextual data like its current operational state, recent sensor readings, and even its last maintenance date. The LLM receives this rich context and can provide a precise diagnosis, such as, "Error 3008 is likely caused by a loose wire on terminal block X. Check the connection and restart the Modbus communication driver." Without the context, the LLM might only be able to provide a generic definition of the error.

Furthermore, as the business scales and more equipment needs to be integrated for ESG monitoring, the **Unified Namespace (UNS)** architecture makes it very easy to scale out the system by adding new devices and data points. With the help of the conversational guidance from the LLM, a company's own engineers can now independently insert new monitoring points and maintain the entire UNS with minimal effort. This empowers them to manage the growing demands of ESG reporting efficiently and autonomously, ensuring the system can evolve with the business.

## Future-Proofing ESG Reporting with a Unified Architecture

For any enterprise looking to manage a large number of data points for ESG reporting, the combination of **NeuronEX** and **EMQX** provides a robust and proven solution. NeuronEX serves as the critical edge component, addressing the fundamental challenge of **OT/IT interoperability** by seamlessly connecting to a vast array of industrial equipment and standardizing diverse communication protocols. It then transmits this data to EMQX, a centralized message broker that can handle massive data ingestion from countless remote locations. This partnership not only solves the technical complexities of data collection but also provides a superior experience for **Unified Namespace (UNS) maintenance**, ensuring that the entire system is easy to manage and can scale effortlessly with the company's growth.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
