## Understanding DDS

### Introduction to DDS

DDS (Data Distribution Service) is a data-centric middleware protocol and API standard published by the OMG organization. It integrates system components to provide low-latency data connectivity, high reliability, and a highly scalable architecture, making it suitable for various commercial-grade IoT applications.

 ![DDS](https://assets.emqx.com/images/4fe1d6ec1d35cf82bdf769f461d1e514.png)

DDS operates as a publish-subscribe messaging protocol, enabling real-time, reliable, and scalable data distribution. Initially, DDS was employed in industrial automation, where large volumes of data needed to be captured and transmitted in real-time for high-performance and reliable control. Due to its real-time performance, reliability, and scalability, DDS quickly became the standard protocol for industrial automation. Over the years, DDS has also found applications in aerospace, automotive, medical, and other fields.

![DDS Communicate](https://assets.emqx.com/images/0cb794d5e2c7daf813c0472ac6ff98f3.png)

 

### Features of DDS

The core of DDS revolves around data, encompassing functions such as transmission, storage, and processing. These functions can be summarized into the following features:

- **Data Centricity**: DDS inherently understands what data is stored and manages how it is shared. Unlike traditional message-centric middleware, where programmers must write code to specify data sharing, DDS handles this internally, eliminating the need for such code management.
- **Global Data Space**: This feature allows all DDS nodes to access the same data sources as if they were in a unified space. In practice, DDS nodes share data by sending messages to update remote nodes, ensuring that all nodes in the network have consistent and up-to-date data.
- **Quality of Service (QoS)**: DDS filters data through various QoS parameters, including reliability, system performance, and security. Not every node requires all data from the data center; DDS nodes share only the necessary information filtered by QoS. DDS ensures data reaches its intended destination reliably, dynamically adjusts data transmission based on system changes, and uses multicast messages for quick updates. For security-critical applications, DDS controls access, enforces data flow, and encrypts data in real-time.
- **Dynamic Discovery**: DDS supports dynamic discovery of publishers and subscribers, allowing nodes to find each other at runtime without pre-configured communication ports. This enables “plug and play” functionality for DDS applications.
- **Scalable Architecture**: DDS can scale horizontally across multiple nodes and different control domains.
- **Security**: DDS provides robust security mechanisms, including authentication, access control, confidentiality, and data integrity.

 ![DDS Scale](https://assets.emqx.com/images/c944a141da983a66f8283a0ce2177e9f.png) 

## DDS in Industry

### DDS and Industrial Automation

DDS’s scalability and quality of service are tailored to meet the demands of industrial automation, focusing on reliability, scale, and customization. It addresses the following key areas:

- **Data Acquisition and Transmission**: DDS enables real-time data acquisition and transmission from industrial equipment and sensors. For instance, in a robot control system, DDS can gather data from robot sensors using Pub-Sub, filter it through Quality of Service (QoS) parameters like position, velocity, and angle, and transmit this data to the controller to manage the robot’s movements.
- **Control and Coordination**: DDS is used to control industrial equipment and systems, facilitating coordination between different systems. In industrial production control systems, DDS sends control commands via Pub-Sub communications to manage production equipment. Through horizontal and vertical scaling, it ensures coordination between various production units and regions, enhancing production efficiency.
- **Monitoring and Diagnostics**: DDS monitors the status of industrial equipment and systems and diagnoses malfunctions. In industrial safety systems, DDS leverages its global data space feature to easily access the status of all monitored equipment and issue warnings when abnormalities are detected.

### DDS and the Automobile

In the automotive industry, real-time and reliable data transmission is crucial. DDS ensures real-time data transmission and employs various QoS mechanisms to guarantee data reliability within vehicles. The primary applications of DDS in the automotive sector include:

- **Vehicle Sensing**: DDS collects data from various vehicle sensors, such as radar, cameras, and LIDAR, and transmits this data to vehicle safety controllers for collision detection and prevention.
- **Vehicle Control**: In autonomous driving systems, DDS gathers data from vehicle sensors and transmits it to an autonomous driving controller. This controller processes the data to determine actions like steering, braking, and acceleration, thereby controlling the vehicle’s movement.
- **Vehicle Communication**: DDS facilitates vehicle-to-vehicle (V2V) and vehicle-to-infrastructure (V2I) communications within a vehicle network, enabling cooperative driving.
- **Vehicle Diagnostics**: In vehicle maintenance systems, DDS collects data from vehicle sensors and transmits it to diagnostic systems for fault detection and analysis.

## Benefits of DDS

### Industry Standards

DDS serves as the foundation for various industry protocols and system framework standards, including OpenFMB, Adaptive AUTOSAR, MD PnP, GVA, NGVA, and ROS2.

### Rich QoS Policies

DDS offers a comprehensive set of QoS policies to manage the quality of data transmission and communication, addressing aspects such as timeliness, traffic prioritization, reliability, and resource constraints. These QoS policies are broadly categorized as follows:

- **Reliability**: Ensures reliable data transmission.
- **Durability**: Manages data storage and recovery after system restarts.
- **Deadline**: Specifies the expiration date of data.
- **Lifespan**: Defines the lifespan of data.
- **Ownership**: Controls the transfer of data ownership.
- **Time-Based Filter**: Filters data based on time conditions.
- **Resource Limits**: Limits the resources (e.g., memory, bandwidth, processors) used for data processing.

These QoS parameters can be configured to meet specific application requirements for data transfer and communication.

### Security, Extensibility, and Autodiscovery

DDS provides robust security features, including standardized authentication, encryption, access control, and logging, ensuring secure end-to-end data connections in IoT systems. In terms of scalability, DDS can expand both horizontally and vertically to support a large number of devices. It can achieve point-to-point latency as low as 30μs and handle millions of messages per second. For large systems, DDS offers auto-discovery and plug-and-play capabilities, simplifying system deployment.

## Limitations of the Current DDS

### Compatibility of Different DDS Middlewares

DDS middleware abstracts applications from the specifics of the operating system, network transport, and low-level data formats. It provides consistent concepts and APIs across various programming languages, enabling applications to exchange information across different operating systems, languages, and processor architectures. Middleware manages underlying details such as data formats, discovery, connectivity, reliability, protocols, transportation, QoS, and security.

Although the DDS protocol is designed to be universal, compatibility between different DDS middleware implementations can be inconsistent, particularly in the following areas:

- **Version Incompatibility**: The DDS standard evolves over time, leading to potential incompatibilities between different versions or implementations. If two implementations use different DDS versions, communication protocols, APIs, or functionalities may not be compatible.
- **QoS Parameter Incompatibility**: While the DDS specification defines a set of QoS parameters, different implementations may support varying QoS parameters or values, potentially hindering interaction between different DDS implementations.
- **Data Type Incompatibility**: DDS supports user-defined data types, which may be defined and interpreted differently by various implementations. Inconsistent data types across implementations can result in incorrect data parsing or transmission.
- **Transport Protocol Incompatibility**: DDS can use different transport protocols for data transfer, such as TCP/IP, UDP, or shared memory. Different implementations may use different transport protocols, preventing direct data exchange.
- **Serialization Format Incompatibility**: DDS implementations may use different serialization formats for encoding and decoding data. If serialization formats differ, data may not be correctly parsed or transmitted.
- **Security Mechanism Incompatibility**: DDS supports security mechanisms like encryption and authentication for data transmission. Different implementations may use varying security mechanisms or specifications, complicating secure data exchange.

### Cross-Domain

DDS is designed to support cross-domain operations, but several common issues arise in practice:

- Limited Cross-Domain Performance: DDS performs well within the same domain but is less efficient across domains compared to protocols like HTTP and MQTT.
- Different Cross-Domain Approaches: Various DDS implementations have different cross-domain strategies. For example, FastDDS often uses a multi-domain configuration, while CycloneDDS tends to implement from Zenoh.
- Different versions of the same DDS implementation have different ways of crossing domains.

### Lack of MCU Support

Current DDS implementations, such as FastDDS, CycloneDDS, and RTI Connext DDS, do not run on MCUs (non-Linux). The prevalence of MCU devices in industrial automation and automotive sectors limits the ability to leverage DDS for large-scale device support. Although DDS-XRCE, a simplified version of DDS, can support MCUs, it remains immature and faces similar compatibility issues.

## Addressing DDS Challenges with MQTT

### Introduction to MQTT

[**MQTT**](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol based on the publish/subscribe model, specifically designed for IoT applications in low-bandwidth and unstable network environments. It provides real-time and reliable messaging services for connected devices with minimal code. MQTT is characterized by low bandwidth consumption, asynchronous communication, and scalability, making it suitable for large-scale device connectivity and the publish/subscribe messaging model. The MQTT protocol is widely used in IoT, mobile Internet, smart hardware, IoV, smart cities, telemedicine, power, oil, and energy sectors.

Key features of the MQTT protocol include:

- Lightweight: Uses a binary data format with smaller packet sizes and lower bandwidth consumption.
- Asynchronous Communication: Clients can subscribe to topics to receive messages without actively requesting them.
- Scalability: Supports multiple QoS levels, retained messages, last will messages, and other features that can be configured as needed.
- Data-Agnostic: Does not concern itself with the payload data format.
- Persistent Session Awareness: Always knows if a device is online.

### Good Compatibility Between Different Versions of MQTT

The major versions of MQTT are MQTT 3.1, MQTT 3.1.1, and [MQTT 5](https://www.emqx.com/en/blog/introduction-to-mqtt-5). The main difference between these versions is that MQTT 5 introduces new features compared to MQTT 3.1.1, which are disabled when forwarding MQTT 5 messages to MQTT 3.1.1 nodes, but this does not affect communication. MQTT 3.1.1 only changes the version number of MQTT 3.1, without affecting the communication itself.

All major [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) are compatible with all three MQTT versions, ensuring seamless interaction between all MQTT clients.

### Solving Cross-Domain Problems with MQTT

MQTT and DDS differ in several ways, including their communication models and decentralization. The main differences for cross-domain communication are summarized below:

|      | Transport Layer | Communication Modes | Overhead of Parsing Protocols | Bandwidth Consumption | Intra-Domain Delay | Cross-Domain Delay |
| :--- | :-------------- | :------------------ | :---------------------------- | :-------------------- | :----------------- | :----------------- |
| MQTT | TCP, QUIC       | PUB-SUB             | Low                           | Low                   | Low                | Low                |
| DDS  | TCP, UDP        | PUB-SUB, REQ-REP    | High                          | High                  | Low                | High               |

As shown in the table, DDS excels in intra-domain communication, while MQTT is advantageous for cross-domain communication due to its lightweight nature, resulting in lower bandwidth usage and latency.

DDS can leverage MQTT for cross-domain communication in the following ways:

 ![How DDS Proxy Wroks](https://assets.emqx.com/images/7cb29e3bc7c5a5d3eadb474649ccceab.png)

By introducing an MQTT-DDS Proxy, which acts as both a DDS node and an MQTT node. The required data from the DDS domain is sent to the MQTT Broker through the MQTT-DDS Proxy and then forwarded to the corresponding DDS domain, enabling DDS cross-domain communication. There are two key considerations in this process:

1. The complexity of converting DDS messages to MQTT messages and vice versa.
2. The potential performance loss introduced by the additional MQTT-DDS Proxy.

For the first issue, the conversion process only adds a serialization overhead, which is generally negligible. For the second issue, introducing a single node in a DDS network does not significantly impact performance. Instead, due to the design of the DDS global data space, the MQTT-DDS Proxy only transfers the necessary data to another domain, which is less costly compared to directly combining the data of nodes in two DDS domains to manage the global data together.

### MCU Supports for all MQTT Features

The MQTT protocol is lighter than DDS and is more widely used in the IoT space. Many implementations support running on MCUs, including poho-c, Adafruit MQTT, and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).

Besides these open-source libraries, most embedded systems or frameworks come with their own MQTT SDK implementations, which typically fully implement all features in MQTT 3.1 and MQTT 3.1.1.

Therefore, data from MCUs can be integrated into the DDS network via MQTT to achieve better compatibility.

![MQTT to DDS](https://assets.emqx.com/images/f5594fc47818fe7a7f2cb10513b9d7db.png)

Deploying the MQTT Broker in the LAN and sending data to the MQTT-DDS Proxy via the [MQTT Client](https://www.emqx.com/en/blog/mqtt-client-tools) on the MCU can reduce the number of DDS nodes, shrink the DDS network size, and improve performance. Rules can also be set in the MQTT-DDS Proxy to pass only the required data into the DDS domain.

## NanoMQ DDSProxy: Easily Sharing Data Between MQTT and DDS

The [NanoMQ DDSProxy](https://github.com/emqx/nanomq/blob/master/docs/en_US/gateway/dds.md) is an MQTT-DDS Proxy that functions as both a DDS node and an MQTT node. NanoMQ DDSProxy can share data between MQTT and DDS networks by filtering data by topic. Its main features include:

- Support for MQTT 3.1, MQTT 3.1.1, and MQTT 5.
- Support for parsing [most IDL syntax](https://github.com/nanomq/idl-serial).
- Support forwarding rules from DDS to MQTT and MQTT to DDS in both directions.
- Support for [sharing DDS data via shared memory](https://cyclonedds.io/docs/cyclonedds/0.8.2/shared_memory.html).
- Support for TCP, TLS, and QUIC to MQTT networks.
- REST API support.

NanoMQ DDSProxy operates as follows:

![DDSProxy](https://assets.emqx.com/images/13891a44394b3e2d29164d4e879497d3.png)

Since DDS handles the serialization and deserialization of messages internally, and deserialized structures are only available to upper-layer applications, the DDS Proxy needs the IDL file to generate the corresponding serialization and deserialization code to transform DDS structures into MQTT messages. NanoMQ DDSProxy integrates both MQTT and DDS nodes, which need to be initialized separately. After initialization, the nodes receive messages from both the DDS and MQTT networks. When a message is received from either network, it is serialized or deserialized and then forwarded as specified in the configuration file, enabling data sharing between the MQTT and DDS networks.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
