## V2X Cloud Control Platform: The Key to Cooperative Vehicle-Infrastructure System

[V2X (vehicle-to-everything)](https://www.emqx.com/en/blog/what-is-v2x-and-the-future-of-vehicle-to-everything-connectivity) is a communication technology that enables vehicles to exchange data with various elements in their environment, including other vehicles (V2V), pedestrians (V2P), infrastructure (V2I), and networks (V2N). CVIS(Cooperative Vehicle-Infrastructure System) is a promising direction of the intelligent transportation system that requires V2X technology integrating with various sensor technologies, cloud computing, edge computing, and traffic control. It can monitor traffic conditions and facilitate vehicle-road-cloud information exchange, thus enhancing traffic safety and efficiency. 

As a crucial component of CVIS, the V2X cloud control platform is required to collect data from various traffic-related sources, including vehicles, roads, and environmental sensors, and integrate this information for analysis. The platform generates standardized V2X messages and delivers them in real-time to support a variety of applications. In the future, it will evolve towards building multi-level cloud control platforms that promote business layer decoupling and cross-domain data and capability sharing.

## Challenges of Building a CVIS Cloud Control Platform

The current CVIS cloud control platform generally includes data modules, V2X message forwarding, cloud control visualization, and operational management. The platform's foundational capabilities encompass resource connectivity, data processing, and data sharing layers.

- The **resource connectivity layer** manages connections with vehicles, roadside computing units, roadside communication units, and external data sources. 
- The **data processing layer** handles data cleaning and storage, associating data with relevant topics. 
- The **data sharing layer** provides various databases for physical data, capability data, and user data. 

The rapid expansion and commercialization of this platform present significant challenges.

### High-Concurrency, High-Reliability, Low-Latency Connections

Future CVIS requires the cloud control platform to connect with various devices, including roadside sensing, computing and communication units. Applications demand low latency (typically 20-100 ms), posing a challenge for high-concurrency message throughput.

### Normalization and Governance of Roadside Sensing Data

The industry lacks a standardized format for data output from roadside computing units, leading to complexity when deploying devices from various manufacturers in different regions, especially concerning data normalization and governance at the access level.

### Computation, Storage, and Distribution of Massive Streaming Data

CVIS involves exchanging data between devices at frequencies ranging from 1 to 10Hz. The cloud control platform needs to process the dynamic data in real-time, provide results to vehicles, distribute them with other cloud applications, and store them for future analysis. However, current solutions involve multiple distributed components, which makes it complex to develop and operate a reliable platform.

### Data Classification Management and Access Control

Efficient data (structured roadside sensing data and V2X application messages ) isolation management and access control are crucial for implementing practical CVIS with multiple intersections, devices, and data types. This helps in flexible data extraction for higher-level applications.

### Efficient Operational Management

The cloud control platform must monitor device status and data flow globally to ensure the stability and continuity of the business. Challenges arise when some roadside devices cannot report their status directly, making real-time monitoring and troubleshooting difficult. The need for negotiations and protocol development between the platform and devices can add to the workload for both parties.

### Ensuring Device Access Security

CVIS handles sensitive road traffic, vehicle data, and control. Security is no doubt paramount. The platform needs to ensure system entry security using device keys, certificates, and identity authentication through a secure channel before device access.

## How EMQ Helps through a Unified MQTT Platform

### MQTT: A Go-To Protocol for Cooperative Vehicle-Infrastructure System

In CVIS, both roadside-uploaded data and V2X messages for vehicle-road-cloud interactions are structured with small but frequent data units. Multiple system applications often need to consume the same device's data based on various dimensions like message type, intersection, device, and manufacturer. Similarly, they may need to distribute different V2X application messages to multiple devices based on intersection dimensions.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), a publish/subscribe IoT communication protocol, facilitates flexible multi-level topic definitions and supports adaptable topic-based subscribe and publish mechanisms. With its compact message structure, versatile payload formats, and provision of three optional QoS levels, MQTT enables online status awareness and session persistence capabilities. These features effectively meet the demands of CVIS, significantly facilitating the implementation of the cloud control platform and its applications. MQTT has become the primary protocol for vehicle-to-cloud and road-to-cloud interactions in numerous CVIS projects.

### EMQ's MQTT-Based Solution for CVIS Cloud Control Platform

EMQ's CVIS solution is centered on MQTT-based data collection and transmission.  It combines the world’s leading MQTT broker, [EMQX](https://www.emqx.com/en/products/emqx), and the streaming data platform, [HStream](https://hstream.io/), to address challenges in data collection, aggregation, transmission, computation, storage, and management.  Users can rapidly build the resource connectivity layer and data processing layer of the cloud control platform using this architecture and seamlessly connect them with the data sharing layer.

![EMQ's MQTT-Based Solution for CVIS Cloud Control Platform](https://assets.emqx.com/images/055d5790553b7ab80fe58bbc53e24931.png)

**Multi-Protocol Access**

EMQX supports various protocols, including MQTT 3.1/3.1.1/5.0, LwM2M, CoAP, MQTT-SN, and private TCP/UDP protocol.

**10M-Level Connections, Million-Level Throughput, Millisecond Message Routing**

EMQX’s high availability, distributed cluster supports million to billion concurrent connections, millisecond message routing, and million TPS data throughput for urban-scale CVIS projects.

**Data Pre-processing with Powerful Rule Engine**

Data from CVIS devices can be efficiently processed and integrated using a low-code SQL-based approach. This allows for real-time data encoding, filtering, aggregation, and template normalization for different data structures, and seamless integration with SQL/NoSQL/time-series databases and message queues to meet diverse application needs.

**Security Guarantee with Multiple Authentication Methods**

EMQX supports TLS/SSL two-way authentication, built-in/external account and password database source authentication, one-device-one-key solution adaptation, and expansion for authentication integration with third-party C-V2X CA certification platforms.

**Flexible Message Distribution and Control**

MQTT's topic-based publish/subscribe model can categorize and route vehicle-to-road data based on factors like type, intersection ownership, and device manufacturer. Access control mechanisms manage permissions for information publishing and subscription by various terminals, simplifying data access and management for upper-level applications.

**Rich APIs for Upper-Level Application Platform Integration**

The V2X message forwarding module, powered by the robust performance of EMQX, achieves high-concurrency V2X message forwarding through interfaces such as message publishing and topic subscription. Data monitoring applications can use APIs to access connection counts, subscription counts, and message traffic monitoring, while operational management can receive real-time device status updates through online and offline message notifications.

**Efficient Data Storage, Management, and Analysis**

HStream is capable of storing and managing large-scale data streams with stable read and write latencies even under high concurrency. It offers a comprehensive event-time-based stateful processing solution, supporting various data operations and special processing for out-of-order and late-arriving messages to ensure accurate results for V2X business. It also allows users to integrate with external data systems for further development.

## What You Can Achieve with EMQ’s Solution

### Facilitating Assisted Driving

The traffic data collected by EMQX can be consumed in HStream to generate real-time downlink messages for businesses. They will then be distributed to the corresponding OBUs or RSUs, which can decode the information and transmit it through in-vehicle human-machine interaction devices to facilitate assisted driving or deliver the information to autonomous driving computing systems for perception assistance.

### Traffic&Vehicle Status Visualization

The abundant data collected by EMQX from the roadside can be utilized to achieve twin representation of traffic elements, cloud-controlled event alerts, and data dashboards. EMQX's extensive APIs enable message throughput statistics for uplink and downlink from different time intervals, as well as operational functions like device status monitoring, roadside device registration management, and vehicle registration management.

### Rapid Setup with Flexible Deployment Solutions

EMQ's solution offers versatile deployment options, including physical servers, containers/K8s, private cloud, hybrid cloud, and public cloud, all while in the same environment as the customer's application systems. Customers can easily establish a feature-rich CVIS cloud control platform with a unified, reliable, efficient data infrastructure.



<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      Ready to Get Started?
    </div>
    <div class="mb-32">
      Talk to our technical sales team to answer your questions.
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
  </div>
</section>
