[In the last episode of the UNS series](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot), we explained what UNS is and why it is essential for IIoT 4.0. MQTT technology is always a first choice regarding how to build a UNS. Readers unfamiliar with MQTT might be curious why it always appears with UNS in IIoT 4.0 solutions. This episode will walk you through why MQTT is the best partner for building UNS. 

## What is MQTT

Before entering the world of UNS, it is important to have a basic knowledge of MQTT.

MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe-based messaging protocol. It was created in 1991 by Andy Stanford-Clark (IBM) and Arlen Nipper (Eurotech) to connect oil pipelines over unreliable satellite networks. Thus, since day 1, MQTT has been designed to provide efficient connectivity for resource-constrained devices and low-bandwidth, high-latency, or unreliable networks. Now it has become the de-facto standard of the IoT industry.

For more details on MQTT, please refer to [MQTT Protocol: How It Works & Core Concepts Explained](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

## Why Adopt MQTT in UNS

In our last episode, we learned a common tongue of UNS definition: It is about reflecting your business to the digital infrastructure. To create an effective UNS, it is crucial to have a technology stack that can efficiently connect numerous manufacturing devices and unify the whole business from the physical to the digital world.

This is exactly why MQTT plays a pivotal role in UNS. MQTT broker is commonly used as a digital infrastructure for managing fragmented connections and connecting distributed devices in other industries (such as [IoV](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles) ), and so is in [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges). Here are the reasons why you should adopt MQTT in UNS.

### MQTT is Lightweight and Scalable

UNS requires a data hub as a single source of truth to connect all of your manufacturing pieces, including PLC, SCADA, MES, and ERP. The amount of real-time data is huge. Usually, data hub faces thousands or even millions of concurrent connections in large-scale solutions.

MQTT has very low overhead and bandwidth consumption thanks to its binary format. This lightweight design minimizes the size of messages and reduces network traffic. This feature perfectly matches UNS and IIoT.

![MQTT Characteristics](https://assets.emqx.com/images/9526d72e6e7443079eae5989030e2403.png)

![MQTT Packet](https://assets.emqx.com/images/5b297fda9fd32c49b606fbf65f11f540.png)

Business owners need to focus more on the operation, not tangling with the expansion of infrastructure resources to support a fast-growing business. This is why the scalability of UNS matters. In the MQTT architecture, some brokers provide superb scalability that can support millions of messages per second, such as [EMQX](https://www.emqx.com/en/products/emqx).

> Learn more: [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

### MQTT Connects Everything

MQTT may be a newcomer in the world of IIoT, but it has gained immense popularity. This is because MQTT constitutes the greatest common subset of the old IIoT technology, making it an ideal tool for connecting all the components of your existing system without causing any damage.

Because there is no such technology and products that fit all cases, you cannot build a UNS by [OPC UA](https://www.emqx.com/en/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence) alone or depend on one protocol solely, especially when you bring the cloud into consideration. UNS must combine different technologies together, and MQTT is that adapter and coordinator to unify them in one namespace. 

![Adopt MQTT in UNS](https://assets.emqx.com/images/ae8ba11ca3abe2ddbc134ab220585b55.png)

Many data convention tools and protocol proxy software exist in the open-source world, such as [Neuron](https://neugates.io/), ignition and PLC4X. You can connect [OPC UA to MQTT](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot), the same story with Modbus and Ethercat.

<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>

> Read our tutorials on industrial protocol to MQTT bridging:
> 
> - [Bridging OPC UA Data to MQTT for IIoT](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot)
> 
> - [Bridging Modbus Data to MQTT for IIoT](https://www.emqx.com/en/blog/bridging-modbus-data-to-mqtt-for-iiot)

In IIoT 3.0, companies that execute digital transformation must move data through different layers of traditional systems, such as MES, ERP, CRM, and WMS. This results in a complex connectivity problem called “data spaghetti”.

![Unified Namespace](https://assets.emqx.com/images/bf5d1a5ec1731d08ca519aa798be5b6a.png)

With the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) sitting in the middle, facilitating information exchange, UNS moves data in an efficient manner. This is one of the key reasons why we need MQTT to build UNS.

### MQTT is Secure

In the context of UNS, PLCs don't need to report polling requests from unknown sources. It only establishes one long-stand connection to a safe broker, which is known to the whole system and is the only data hub that everything needs to talk to. 

MQTT broker not only decouples the inputs and outputs of IIoT 4.0, but also takes over the responsibility of securing the connectivity of fragmented devices and systems. Thanks to the rich security features of MQTT, it is fully competent to act as an isolation data hub for your manufacturing lines, preventing any malformed data penetrates into fragile PLCs. In this way, UNS shifts the security burden to the broker and manages it in a unified place.

### MQTT Enables Event-Driven Architecture

For IIoT 4.0, data is primarily generated by devices, not people. And most of the time, PLC readings don’t change, it is no point in transmitting redundant data to UNS and overwhelming your network. 

However, once the value of registers changes, it is essential to report it to ERP/MES or cloud immediately to extract the maximum value, since the liquidity and marginal value of information decreases along with time. This is called “report by exception“.

![Event-Driven Architecture](https://assets.emqx.com/images/f32b6b5a3705f2250b52882f1d533909.png)

Therefore, an event-driven technology such as MQTT is important to implement UNS. MQTT brokers are aware of client state changes. This awareness is enabled with SparkPlugB and the MQTT Last Will features. With last will and SparkPlugB, MQTT only communicates changes and ensures stale data is not delivered to subscribing clients.

## MQTT Topic as Metadata of UNS

UNS is the digital reflection of business in the physical world. It is driven by reality, not the other way around. We need the sublime context of generated data to convert it into information, such as the location of site, and which line and cell PLC belongs to. Fortunately, the Pub/Sub messaging model of MQTT provides an easy way of mapping the context of PLC into the digital world. 

UNS with MQTT enables users to browse all the namespaces and features. And the real-time status of every data tag.  

The MQTT topic is well-defined as follows:

**namespace/group_id/message_type/edge_node_id/[device_id]**

![MQTT topic](https://assets.emqx.com/images/402d188d0059c04cfcd6faf4b79ab849.png)

<center>From OSISoft AF</center>

<br>

[MQTT Topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) have a hierarchical organization and could be easily imagined as a folder structure. By adding your namespace of each level as a topic, we can build a tree view on top of MQTT.

When subscribers consume data from the topic “**Enterprise A/Site A/Area A/Process Cell A/Bio Reactor”,** it automatically knows where the data origins and takes necessary action upon it. And they could use wildcards to subscribe to multiple datapoints at the same time. 

![MQTT topics and metadata](https://assets.emqx.com/images/385a249a15ea3470675cf71d71872271.png)

MQTT could help you define metadata that assures consistency and accuracy across different systems in UNS.

## OPC UA: Alternative to MQTT for Building UNS

Precisely speaking, MQTT is the best partner for building UNS. However, it is not compulsory. Therefore, you could build the UNS with other protocols, such as OPC UA and HTTP, or even plain Modbus + TCP/UDP. Among many options, OPC UA remains a popular methodology for IIoT due to the strong commercial backup and the standard's longevity. 

> The detailed comparison between them can be found at:
>
> - [A Comparison of IIoT Protocols: MQTT Sparkplug vs OPC-UA](https://www.emqx.com/en/blog/a-comparison-of-iiot-protocols-mqtt-sparkplug-vs-opc-ua) 
> - [Efficiency Comparison: OPC-UA, Modbus, MQTT, Sparkplug, HTTP](https://www.emqx.com/en/blog/efficiency-comparison-opc-ua-modbus-mqtt-sparkplug-http) 

However, it is not one or the other case; the best approach is to combine the advantages from both sides by [bridging them together](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot), or [using OPC UA via MQTT approach](https://www.emqx.com/en/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence). 

## The General Architecture of Building UNS with MQTT

Theoretically, UNS is a global namespace that unifies all namespaces of your business. Each factory, each site, and each PLC is a stand-alone namespace. 

![Architecture of Building UNS with MQTT](https://assets.emqx.com/images/b9dade93ea0b5ed12476809c1705465a.png)

UNS is to take technology across the business and structure it in a way you can navigate. Thus all other solutions could be built on top of it to their best effort. MQTT is responsible for connecting fragmented technologies from OT, CT and the IT world and seamlessly integrates them together.

## Conclusion

In this blog, we discussed the significance of MQTT within UNS and why MQTT is the data pump of all IT systems. Adopting MQTT in a unified namespace offers a multitude of benefits that can revolutionize how we connect and communicate in the digital world. Organizations can streamline their data flow, create more responsive and connected systems, and unlock new opportunities for innovation and growth. 

In the upcoming episode, we will explore the innovative contributions of EMQ to UNS regarding MQTT.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
