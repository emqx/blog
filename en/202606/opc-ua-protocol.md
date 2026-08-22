## What is OPC UA Protocol

**OPC UA (Open Platform Communications Unified Architecture)** is a platform-independent, service-oriented, open, and secure communication architecture. It is designed to enable interoperability of industrial automation devices, systems, and software applications from different vendors. The OPC UA information model defines the codes and formats for exchanging data using various transport protocols.

OPC UA and its predecessor, Open Platform Communications (OPC), were developed by the same foundation but significantly different. The foundation continues to develop OPC UA in order to create an architecture that is more desirable than the original OPC communications and more in line with the needs of evolving industrial automation.

## The History of OPC UA Protocol

![OPC UA](https://assets.emqx.com/images/f4582b4676a6867f6beefa40c055fae2.png)

Prior to the release of the OPC UA specification, industry vendors, end-users, and software developers had worked together to develop a set of specifications for defining industrial process data, alarms, and historical data. This set of specifications is known as OPC Classic and was first released in 1995, based on the COM/DCOM technology stack for Microsoft Windows. It includes the following three parts:

1. OPC Data Access is best known as [OPC DA](https://www.emqx.com/en/blog/opc-ua-vs-opc-da). The OPC DA specification defines the exchange of data, including value, time and quality information.
2. OPC Alarms & Events, or OPC A&E, the OPC A&E specification defines the exchange of alarm and event type message information, as well as variable status and state management.
3. OPC Historical Data Access (OPC HDA): The OPC HDA specification defines standardized methods for querying, retrieving, and analyzing time-series historical process data.

OPC Classic is known for its excellent performance in process control. However, due to the advancements in technology and changes in external factors, it is no longer able to fully meet the needs of people. To address this issue, the OPC Foundation introduced OPC UA in 2006. This new technology provides cross-platform data transfer, improved data security, and better handling of large data volumes. OPC UA integrates all of the functionality of the existing OPC Classic specification while addressing the problems that existed with OPC Classic.

With the release of the **OPC UA 1.05 specification series and subsequent maintenance updates such as 1.05.06**, OPC UA has continued to evolve its communication capabilities. In addition to the traditional Client-Server model, OPC UA supports a **Publish/Subscribe (PubSub)** mechanism for scalable one-to-many data distribution. PubSub supports message mappings such as JSON and the standard-defined UADP binary format over transports and messaging protocols including UDP, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), and [AMQP](https://www.emqx.com/en/blog/mqtt-vs-amqp-for-iot-communications), making it well suited for industrial edge and cloud integration.

## Features of OPC UA Protocol

**Functional equivalence:** All OPC Classic specifications map to the UA, and the OPC UA includes the DA, A&E and HDA functionality found in OPC Classic:

| **Functionality** | **Descriptions**                                             |
| :---------------- | :----------------------------------------------------------- |
| Discovery         | Find available OPC servers on your local PC and/or network   |
| Address space     | All data is represented hierarchically (e.g. files and folders), allowing OPC clients to discover, utilise simple and complex data structures |
| On-demand         | Read and write data/information based on access rights       |
| Subscription      | Monitor data/information and report exceptions when values change beyond the client's settings |
| Event             | Client-based settings notify important information           |
| Method            | Clients can execute programs based on methods defined on the server, etc. |

**Platform Independence:** From embedded microcontrollers to cloud-based infrastructure, OPC UA is not dependent on the Windows platform and can be deployed for use on any platform.

**Security:** Message encryption, authentication and auditing, one of the most important considerations for an organization when choosing a technology standard is security. OPC UA addresses security by providing a set of controls when passing through firewalls:

| **Functionality**        | **Descriptions**                                             |
| :----------------------- | :----------------------------------------------------------- |
| Transport                | A number of protocols are defined, providing options such as ultra-fast OPC binary transfers or the more general SOAP-HTTPS |
| Session encryption       | Information is transmitted securely with 128-bit or 256-bit encryption levels |
| Message Signature        | The signature must be identical when the message is received as when it is sent. |
| Sequencing Data Packages | Identified message replay attacks eliminated through sequencing |
| Authenticate             | Each UA client and server is identified by an OpenSSL certificate, which provides control over how applications and systems connect to each other. |
| User control             | Applications can require user authentication (login credentials, certificates, etc.) and can further restrict or enhance user access to permissions and address space "views". |
| Audits                   | Logging of user and/or system activity to provide an access audit trail |

**Extensibility:** OPC UA's multi-tier architecture allows for the incorporation of innovative technologies and approaches, such as new transport protocols, security algorithms, coding standards, and application services, without affecting existing applications. This ability to add new functionalities makes OPC UA a "future-proof" framework. In the meantime, OPC UA maintains compatibility with existing products. This means that today's UA products can interoperate with future UA products.

**Comprehensive Information Modelling:** Used to define complex information, the OPC UA Information Modelling Framework converts data into information, allowing even the most complex multi-level structures to be modeled and extended through fully object-oriented functionality, with data types and structures that can be defined in configuration files.

![OPC UA Information Modelling Framework](https://assets.emqx.com/images/1161f4a8f02d771efa813f234c8515a9.png)

## Uses of OPC UA Protocol

OPC UA has a wide range of applications in industrial automation and IoT, bringing many benefits to different industries, including data collection, device integration, remote monitoring, historical data access, and more. 

### Manufacturing

- Data collection and monitoring: Equipment and production lines in the manufacturing industry can easily collect data through OPC UA to monitor the production process in real time and optimize productivity.
- Device Integration and Interoperability: Devices produced by different manufacturers can be seamlessly integrated, from sensors to robots, enabling data exchange between devices.

### Building Automation

- Intelligent Building Management: OPC UA is used to connect building automation systems, including lighting, air conditioning, and security systems, to achieve intelligent energy management and equipment control.
- Equipment Monitoring and Maintenance: Condition monitoring and maintenance of building equipment can be realized through OPC UA to improve equipment reliability and efficiency.

### Oil and Gas

- Remote Monitoring and Control: Equipment in oilfields, pipelines and refineries can be remotely monitored and controlled via OPC UA, reducing manual intervention.
- Data History: OPC UA's historical data access feature is used to record equipment operating data for easy analysis and optimization.

### Renewable Energy

- Wind and Solar Farms: OPC UA is used to monitor the operating status of wind and solar farms for remote control and troubleshooting.
- Grid Management: Renewable energy access and grid management require real-time data exchange, and OPC UA provides a reliable communication mechanism.

### Utilities

- Water Treatment and Water Supply System: OPC UA is used to monitor water treatment equipment, pumping stations and water supply systems to ensure stable water quality and supply.
- Power systems: Monitoring, fault detection and remote operation of power equipment can be realized with OPC UA.

## Information Model for OPC UA Protocol

The OPC UA information model is a network of nodes, or structured graph, consisting of nodes and references, which is called the OPC UA address space. The address space represents objects in a standard form - model elements in the address space are called nodes, and objects and their components are represented in the address space as a collection of nodes, which are described by attributes and connected by references. OPC UA modeling is all about creating nodes and references between nodes.

### Object Model

OPC UA uses objects as the basis for representing data and activities in the process system. Objects contain variables, events and methods that are interconnected by reference.

![OPC UA Object Model](https://assets.emqx.com/images/313bb04eebc2beaacc6c359eba0e17d8.png)

### Node Model

![OPC UA Node Model](https://assets.emqx.com/images/185c6a8d55d470c5e558bd3afd76a0ca.png)

- Attributes are used to describe nodes, and different node classes have different attributes (sets of attributes). The definition of a node class includes the definition of attributes, so attributes are not included in the address space.
- A Reference represents a relationship between nodes. A reference is defined as an instance of a node of the reference type that exists in the address space.
- Generic properties of the node model

![Generic properties of the node model](https://assets.emqx.com/images/21e683edc5e34b7e2da17b662b99a421.png)

### Reference Model

The node containing the reference is the source node and the referenced node is called the target node. The referenced target node can be in the same address space as the source node, or in the address space of another OPC server, or even the target node can be non-existent.

![OPC UA Reference Model](https://assets.emqx.com/images/3b484967bea36515325de244dda332bd.png)

### Node Types

The most important node categories in OPC UA are objects, variables and methods.

- Object nodes: Object nodes are used to form address spaces and do not contain data. They use variables to expose values for objects. Object nodes can be used to group management objects, variables or methods (variables and methods always belong to an object).
- Variable node: Variable node represents a value. The data type of the value depends on the variable. The client can read, write and subscribe to the value.
- Method node: The method node represents a method in the server that is called by the client and returns the result. The input parameters and the output result are in the form of variables as part of the method node. The client specifies the input parameters and gets the output result after the call.

## How the OPC UA Protocol Works

Hardware providers support OPC UA in two ways: by embedding an OPC UA server in the device or offering software on a PC that obtains data through a private protocol and exposes it to other platforms via OPC UA. In some mid-range and high-end PLCs, there are OPC UA server integrations such as Siemens S71200/1500, while Siemens also provides software like WINCC to indirectly provide data from other devices to third parties through OPC/OPC UA.

![opc ua client and server](https://assets.emqx.com/images/e9398279706d0e493388a5c60fede41f.png)

After the data is exposed through the OPC UA Server, it can be accessed using the two access modes specified by the OPC UA protocol: the Request/Response mode and the Publish/Subscribe mode. To begin, the client must establish a connection to the server, which will create a session channel between the client and server.

In request/response mode, the client application can request some standard services from the server through the session channel, such as: reading raw data from the node, writing data to the node, invoking remote methods, and so on.

![request/response mode](https://assets.emqx.com/images/f7c47ebeb1f5da8bc6290b6b014b106e.png)

In publish/subscribe mode, each client can create any number of server subscriptions, and when the server's node data changes, notification messages are instantly pushed to the client.

![publish/subscribe mode](https://assets.emqx.com/images/16eedf2be88eb090746d9a7de6ad40e5.png)

Generally, end users don't have to worry about the processes mentioned above. Their main concerns are the OPC UA server address, user login policy, communication security policy, and the address where they can access the data.

### OPC UA Server Endpoint

| **Protocol**      | **Url**                                |
| :---------------- | :------------------------------------- |
| OPC UA TCP        | `opc.tcp://localhost:4840/UADiscovery` |
| OPC UA Websockets | `opc.wss://localhost:443/UADiscovery`  |
| OPC UA HTTPS      | `https://localhost:443/UADiscovery`    |

### User Authentication Method

1. Anonymous
2. Username & Password
3. Certificate

### Security Modes

1. None
2. Sign
3. Sign & Encrypt

### Security Policies

1. Basic128Rsa15
2. Basic256
3. Basic256Sha256
4. Aes128Sha256RsaOaep
5. Aes256Sha256RsaPass

### Node Address

| **Address type** | **Address**          |
| :--------------- | :------------------- |
| Byte string      | ns=x;b=<byte string> |
| GUID             | ns=x;g=<GUID>        |
| Int              | ns=x;i=x             |
| String           | ns=x;s=<string>      |

## Leveraging OPC UA Protocol with MQTT

MQTT (Message Queuing Telemetry Transport) is a messaging protocol designed for IoT devices and applications that uses a publish-and-subscribe model and has the advantages of being lightweight, efficient, reliable, and supporting real-time communication. MQTT is well suited for resource-constrained environments, especially scenarios requiring efficient power and bandwidth use.

The industry has built an [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) data specification called SparkplugB on top of MQTT 3.1.1, which provides basic data unified modeling capabilities while ensuring flexibility and efficiency. Thanks to the excellent design of the MQTT protocol, SparkPlugB provides good network state awareness and is able to provide strong interoperability for devices and systems.

OPC UA and MQTT have a certain degree of functionality overlap, but their use of scenarios is very different:

- OPC UA is a communication protocol used in industrial scenarios to enable different equipment and systems from various manufacturers to communicate seamlessly using a standardized language.
- MQTT is an [IoT protocol](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m) designed for Internet-based data transmission of sensors, catering to low bandwidth and unreliable network conditions while efficiently handling continuous real-time data. Its read/publish mechanism offers remarkable flexibility in usage.

In industrial scenarios, MQTT excels at messaging in distributed systems, while OPC UA focuses on providing interoperability. By combining the two, business data can be abstracted and aggregated using OPC UA, and MQTT can enable seamless exchange of this data in a distributed manner, leveraging its strong connectivity capabilities.

## OPC UA over MQTT

The Pub-Sub model proposed by the OPC Foundation in the latest specification of OPC UA allows data changes to be pushed to subscribers using the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

![OPC UA over MQTT](https://assets.emqx.com/images/e3772239f0f42b2f622996c721d7e57f.png)

OPC UA PubSub defines standardized mappings for MQTT, including both JSON and UADP message encodings. When MQTT is used as the transport, the MQTT broker provides scalable message distribution, while OPC UA PubSub defines the structure and semantics of the exchanged industrial data.

## How to Bridge OPC UA to MQTT with EMQX Neuron and EMQX

**[EMQX Neuron](https://www.emqx.com/en/products/emqx-neuron)** is a lightweight industrial connectivity gateway designed for real-time equipment data acquisition, edge processing, and OT/IT integration. It supports more than 100 industrial protocols, including OPC UA, Modbus, Siemens S7, EtherNet/IP, BACnet, Mitsubishi, and others, allowing data from heterogeneous industrial devices and systems to be collected through a unified interface.

For OPC UA scenarios, EMQX Neuron can connect to OPC UA servers on PLCs, controllers, gateways, and other industrial systems, collect selected data points, and process the data locally at the edge. It can then convert and publish the collected OPC UA data to MQTT, making industrial data easier to distribute to IIoT platforms, cloud services, MES, SCADA, databases, and other applications.

When used together with **[EMQX](https://www.emqx.com/en/products/emqx)**, Neuron provides a straightforward OPC UA-to-MQTT data pipeline:

**OPC UA devices and servers → EMQX Neuron → MQTT → EMQX → IIoT and enterprise applications**

In this architecture, EMQX Neuron handles southbound industrial connectivity and protocol conversion. It collects OPC UA data, performs edge-side filtering, transformation, aggregation, and other processing when required, and publishes the resulting data through MQTT. EMQX acts as the MQTT messaging layer, efficiently distributing the data to downstream consumers and applications.

This combination helps bridge the gap between Operational Technology (OT) and Information Technology (IT). OPC UA provides standardized access to structured industrial data, while MQTT provides lightweight and scalable data distribution across edge, data center, and cloud environments.

By combining OPC UA, EMQX Neuron, and EMQX, industrial organizations can build a scalable data architecture for scenarios such as real-time equipment monitoring, predictive maintenance, production analytics, industrial data integration, Unified Namespace (UNS), and edge-to-cloud data pipelines.

To learn how to implement the integration in practice, see our step-by-step guide: [Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot).

## OPC UA FAQ

### 1. What is OPC UA used for?

OPC UA is used for secure and standardized data exchange in industrial automation and Industrial IoT (IIoT). It enables PLCs, sensors, machines, control systems, software applications, and cloud platforms from different vendors to communicate and share structured data. Common use cases include equipment monitoring, production data collection, remote control, predictive maintenance, historical data access, and OT/IT integration.

### 2. What is the difference between OPC UA and OPC Classic?

OPC Classic is based mainly on Microsoft COM/DCOM technologies and is closely tied to Windows environments. OPC UA is platform-independent and provides built-in security, richer information modeling, and support for modern industrial and IIoT architectures. OPC UA also combines capabilities such as data access, alarms and events, and historical data access within a unified architecture.

### 3. How does OPC UA work?

In a typical Client-Server architecture, an OPC UA Server exposes industrial data through an Address Space made up of Nodes and References. OPC UA Clients connect to the server to browse, read, write, call methods, or subscribe to data changes. OPC UA also supports Publish/Subscribe (PubSub) communication for scalable one-to-many data distribution.

### 4. Is OPC UA secure?

Yes. OPC UA includes built-in security mechanisms for application authentication, user authentication, message signing, encryption, authorization, and auditing. OPC UA applications can use certificates to establish trust between clients and servers, while security policies and modes determine how communication is authenticated and protected.

### 5. What is the difference between OPC UA and MQTT?

OPC UA and MQTT serve different but complementary purposes. OPC UA focuses on industrial interoperability, structured information modeling, and standardized access to machine data. MQTT is a lightweight publish/subscribe messaging protocol designed for efficient and scalable data distribution. In Industrial IoT architectures, OPC UA is often used to collect and model OT data, while MQTT distributes that data to edge, cloud, and enterprise applications.

### 6. How can OPC UA data be sent to MQTT?

OPC UA data can be bridged to MQTT using an industrial gateway such as EMQX Neuron. Neuron connects to OPC UA servers, collects selected data points, performs edge-side processing when needed, and publishes the resulting data through MQTT. An MQTT broker such as EMQX can then distribute the data to IIoT platforms, cloud services, databases, MES, SCADA, and other applications.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
