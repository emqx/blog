## What is OPC UA

OPC UA (OPC Unified Architecture) is a platform-independent, service-oriented, open, and secure communication architecture. It is designed to enable interoperability of industrial automation devices, systems, and software applications from different vendors. The OPC UA information model defines the codes and formats for exchanging data using various transport protocols.

OPC UA and its predecessor, Open Platform Communications (OPC), were developed by the same foundation but significantly different. The foundation continues to develop OPC UA in order to create an architecture that is more desirable than the original OPC communications and more in line with the needs of evolving industrial automation.

The first version of the OPC UA specification was released in 2006, and as of today, the latest version of OPC UA is 1.05. In addition to the Client-Server (Subscriptions) model, OPC UA includes a Pub-Sub mechanism, which allows pushing JSON specifications (also using the standard-defined binary specification - UADP) over the UDP protocol, [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), or [AMQP protocol](https://www.emqx.com/en/blog/mqtt-vs-amqp-for-iot-communications).

Through the fast, secure and reliable transport channel provided by the MQTT protocol, OPC UA can directly use the Internet for data transfer while retaining the key benefits of OPC UA's end-to-end security and standardized data modeling.

![OPC UA](https://assets.emqx.com/images/f4582b4676a6867f6beefa40c055fae2.png)

## Features of OPC UA

- Functional equivalence - All OPC Classic specifications map to the UA, and the OPC UA includes the DA, A&E and HDA functionality found in OPC Classic:

| **Functionality** | **Descriptions**                                             |
| :---------------- | :----------------------------------------------------------- |
| Discovery         | Find available OPC servers on your local PC and/or network   |
| Address space     | All data is represented hierarchically (e.g. files and folders), allowing OPC clients to discover, utilise simple and complex data structures |
| On-demand         | Read and write data/information based on access rights       |
| Subscription      | Monitor data/information and report exceptions when values change beyond the client's settings |
| Event             | Client-based settings notify important information           |
| Method            | Clients can execute programs based on methods defined on the server, etc. |

- Security - Message encryption, authentication and auditing, one of the most important considerations for an organization when choosing a technology standard is security. OPC UA addresses security by providing a set of controls when passing through firewalls:

| **Functionality**        | **Descriptions**                                             |
| :----------------------- | :----------------------------------------------------------- |
| Transport                | A number of protocols are defined, providing options such as ultra-fast OPC binary transfers or the more general SOAP-HTTPS |
| Session encryption       | Information is transmitted securely with 128-bit or 256-bit encryption levels |
| Message Signature        | The signature must be identical when the message is received as when it is sent. |
| Sequencing Data Packages | Identified message replay attacks eliminated through sequencing |
| Authenticate             | Each UA client and server is identified by an OpenSSL certificate, which provides control over how applications and systems connect to each other. |
| User control             | Applications can require user authentication (login credentials, certificates, etc.) and can further restrict or enhance user access to permissions and address space "views". |
| Audits                   | Logging of user and/or system activity to provide an access audit trail |

- Comprehensive Information Modelling: Used to define complex information, the OPC UA Information Modelling Framework converts data into information, allowing even the most complex multi-level structures to be modeled and extended through fully object-oriented functionality, with data types and structures that can be defined in configuration files.

![OPC UA Information Modelling Framework](https://assets.emqx.com/images/1161f4a8f02d771efa813f234c8515a9.png)

## Information Model for OPC UA

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

## Why Bridge OPC UA to MQTT?

MQTT (Message Queuing Telemetry Transport) is a messaging protocol designed for IoT devices and applications that uses a publish-and-subscribe model and has the advantages of being lightweight, efficient, reliable, and supporting real-time communication. MQTT is well suited for resource-constrained environments, especially scenarios requiring efficient power and bandwidth use.

The industry has built an industrial IoT data specification called SparkplugB on top of MQTT 3.1.1, which provides basic data unified modeling capabilities while ensuring flexibility and efficiency. Thanks to the excellent design of the MQTT protocol, SparkPlugB provides good network state awareness and is able to provide strong interoperability for devices and systems.

OPC UA and MQTT have a certain degree of functionality overlap, but their use of scenarios is very different:

- OPC UA is a communication protocol used in industrial scenarios to enable different equipment and systems from various manufacturers to communicate seamlessly using a standardized language.
- MQTT is an IoT protocol designed for Internet-based data transmission of sensors, catering to low bandwidth and unreliable network conditions while efficiently handling continuous real-time data. Its read/publish mechanism offers remarkable flexibility in usage.

In industrial scenarios, MQTT excels at messaging in distributed systems, while OPC UA focuses on providing interoperability. By combining the two, business data can be abstracted and aggregated using OPC UA, and MQTT can enable seamless exchange of this data in a distributed manner, leveraging its strong connectivity capabilities.

## OPC UA over MQTT

The Pub-Sub model proposed by the OPC Foundation in the latest specification of OPC UA allows data changes to be pushed to subscribers using the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

![OPC UA over MQTT](https://assets.emqx.com/images/e3772239f0f42b2f622996c721d7e57f.png)

Pub-Sub security is a bit more complex than that in client/server, and the specification is not as detailed. In an MQTT network, security is based on SSL/TLS, and the broker can define application-level authentication in addition to enabling SSL/TLS for transport. In principle, these security models are either all or nothing for every subscriber and publisher that can join the network. The new OPC UA standardization is still a work in progress, and it is not yet clear how the rich OPC UA information model can best be mapped to MQTT.

## Summary

This article provides essential knowledge about the OPC UA protocol. Additionally, it has been noted that bridging OPC UA data to MQTT can bring more benefits to industrial scenarios and make them more efficient. In our next post "[Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot)", we will provide a detailed guide on how to bridge the two.



<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
