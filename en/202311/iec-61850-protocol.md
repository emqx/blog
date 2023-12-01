## What is IEC 61850

IEC 61850 is an international communication standard protocol that achieves station-wide communication uniformity through a series of standardizations of device functions. Widely used in the power industry, The IEC 61850 standard puts forward the concept of information layering in the substation, both from the logical and physical levels. The substation automation system is divided three levels: The Station Level, The Bay Level and The Process Level. The ACSI is used to exchange data between the levels.

IEC 61850 summarises the communication services necessary for the transmission of information within a substation, designing an Abstract Communication Service Interface (ACSI) that is independent of network and application layer protocols.

The service implementation of the IEC 61850 standard is divided into three parts: the MMS service, the GOOSE service, and the SV service. 

- The MMS Service is used between the Station Level and the Bay Level of the IEC 61850 standard. It achieves interoperability between different manufacturing devices in a network environment by using an object-oriented modeling approach of the actual devices. 
- The GOOSE (Generic Object Oriented Substation Event) is a fast messaging mechanism in IEC 61850 for transmitting important real-time signals between IEDs in a substation.
- The SV (Simpled Values) is used for Sampled Value Transmission at the Process Level, which is the most commonly used service for real-time measurement data in smart substations. 

![IEC 61850](https://assets.emqx.com/images/984d7d5e42ed71afb6790769d4e2ee43.png)

IEC 61850 effectively solves the problem of poor interoperability between secondary devices in power systems, making it possible to share information in substation automation systems and improving system scalability. 

## The History of IEC 61850

The IEC 61850 standard was originally proposed by the International Electrotechnical Commission (IEC) in 1995 to provide a globally applicable communication standard for power system automation. In March 1999, a committee draft of IEC 61850 was submitted. Subsequently, a ballot draft and a final draft were submitted. In June 2000, IEC TC57 decided to use IEC 61850 as the basis for the development of a standard for a seamless communication system for power systems. Between 2002 and 2005, various sub-sections of the IEC 61850 standard were published as International Standards.

The IEC 61850 standard is divided into several parts, each addressing specific aspects of substation automation.

1. **IEC 61850-1:** This part provides the introduction and overview of the standard. It explains the fundamental principles, the purpose of the standard, and the general architecture of substation automation systems.
2. **IEC 61850-2:** This part covers the data and communication models for substation and device modeling. It defines the abstract data models and communication services for power system devices used in substation automation.
3. **IEC 61850-3:** This part addresses the General Requirements. It outlines the general requirements, specifications, and testing procedures for digital communication and data exchange within substations.
4. **IEC 61850-4:** This part specifies the system and project management aspects. It covers guidelines for the system engineering process, including the system specification, design, implementation, testing, commissioning, and maintenance.
5. **IEC 61850-5:** This part provides communication requirements for functions and device models. It specifies the communication requirements for various functions within the substation and the device models associated with these functions.
6. **IEC 61850-6:** This part deals with configuration language for communication in electrical substations related to IEDs (Intelligent Electronic Devices). It defines the language and rules for configuring IEDs in an IEC 61850-based system.
7. **IEC 61850-7:** This part specifies the Basic Communication Structure. It defines basic communication services and models for the exchange of information in substation automation systems.
8. **IEC 61850-8:** This part defines specific communication service mapping (to MMS and to ISO/IEC 8802-3) for IEC 61850. It defines how the services specified in IEC 61850-7 are mapped to specific protocols for communication.

## Features of IEC 61850

### Logical layering of substation automation systems

![Logical layering of substation automation systems](https://assets.emqx.com/images/9cd8db70361773c326e5670e4c9d85f6.png)

- Station Level: It includes Human Machine Interface (HMI) and gateways to communicate with remote control center and integrate IEDs at the bay level to the substation level. It also performs different process related functions such as implementation of control commands for the process equipment by analyzing data from bay level IEDs.
- Bay Level: The process level equipments are connected to station bus via IEDs at the bay level that implement monitoring, protection, control and recording functions. Here we can find intelligent electronic devices called IEDs. IEC 61850 defines a process bus to allow communications between IEDs and intelligent instruments and switchgears.
- Process level: It includes switchyard equipment, sensors and actuators. The current and potential transformers are located at the process level to collect system data and send them to bay level devices for automatic control & protection operations which are achieved through circuit breakers and remotely operated switches. In this level there are different devices such as switchgears, like circuit breakers, switches, a current transformer and a voltage transformer.

### Information Model and Communication Protocol Independence

The IEC 61850 standard summarises an abstract communication service interface ACSI that meets the needs and requirements of the power production process.

### Data Self-Description

IEC 61850 is a standard for the design of electrical substation automation systems. It's a widely used protocol in the field of power systems and substation automation. In IEC 61850, "Data Self-Description" refers to a fundamental principle of the standard.

In IEC 61850, devices in the substation network describe the data they produce and consume using a standardized data model. This data model includes information such as the type of data, its meaning, the unit of measurement, and other relevant metadata. Devices communicate with each other based on this standardized data description, ensuring interoperability between devices from different manufacturers.

Key aspects of data self-description in IEC 61850 include:

1. **Standardized Data Objects:** IEC 61850 defines a set of standardized data objects and their attributes. These objects cover various aspects of substation automation, such as measurements, control commands, alarms, and settings.
2. **Common Information Models (CIM):** CIM in IEC 61850 defines the logical organization of the information in the substation. It allows different devices to understand the semantics of the data they exchange, ensuring that a device can correctly interpret the data received from another device.
3. **Data Attributes:** Each data object in IEC 61850 has specific attributes that describe the properties of the data, such as its data type, range, and units. This detailed description ensures that devices can interpret and use the data correctly.
4. **Logical Nodes:** IEC 61850 organizes data into logical nodes, each representing a specific function within the substation. Logical nodes encapsulate data objects and provide a standardized interface for accessing the data they contain.
5. **Data Mapping:** Devices in an IEC 61850 network communicate with each other by mapping their internal data structures to the standardized data objects defined in the standard. This mapping allows devices to exchange information seamlessly, regardless of internal data representations.
6. **Dynamic Data Exchange:** IEC 61850 supports dynamic data exchange, allowing devices to report changes in their data in real-time. This self-descriptive nature ensures receiving devices can interpret the incoming data without prior knowledge of the sender's internal data structure.

In summary, data self-description in IEC 61850 ensures that devices in a substation automation system can accurately interpret and use the data they exchange, enabling seamless communication and interoperability between devices from different manufacturers. This standardization simplifies substation automation systems' design, integration, and maintenance, leading to more efficient and reliable power grid operations.

### Unified Object-Oriented Data Modeling

The IEC 61850 standard uses UML modeling techniques to make the information model inheritable and reusable. Each layer of the information model is defined as an abstract class encapsulating the corresponding attributes and services. Attributes describe all the features of the class, and services provide methods to operate on those features.

## Layered Information Model for IEC 61850

### Information Model

The information model contains five levels - Server, Logical Device, Logical Node, Data Object, and Data Attribute.

![information model](https://assets.emqx.com/images/f0699a37469c5add1ff1680ee54ce0e4.png)

- Server: It can be understood as the physical devices in the substation, which are usually IED (Intelligent Electronic Device) or RTU (Remote Terminal Unit). The server is responsible for processing and storing data equipment while providing external access points and Authentication services.
- Logical Device: An abstract concept for a collection of data objects used to describe various devices and functions in a power system.
- Logical Node: A data object in a logical device. It is the smallest unit of the data model. Logical nodes contain data objects, which are sub-elements of logical nodes.
- Data Object: Data is one of the basic objects in IEC 61850 for describing the various elements of a power system, such as switches, transformers, protection devices, etc. The Data object can contain several data attributes.
- Data Attribute: Used to represent a number of characteristics of the data. Each data attribute has a name and a data type. The data type can be a basic type, such as integer, floating point, Boolean, etc., or a composite type, such as a structure, enumeration, etc.

Between logical nodes - data - data attributes is a tree structure that forms a hierarchical data model. The data attributes are the lowest-level components of this tree model. We can get the value of a specified data attribute through the address mapping hierarchy of IEC 61850 in the address format: `Logical Device/Logical Node$FC$Data Object/Data Attribute`*,* where FC is a standard-defined functional constraint code.

### MMS Specification Description

The Manufacture Message Specification (MMS) is located in the application layer and uses a client-server model for communication. It enables interoperability between devices from different manufacturers in a networked environment by means of object-oriented modeling of the actual device. The IEC 61850 standard introduces MMS into the field of power automation by mapping its core ACSI services directly to the MMS specification.

![MMS Specification Description](https://assets.emqx.com/images/85ca7b0d33eb24c1b8afcb12893c5fe2.png)

MMS uses the ASN.1 codec specification to define data transmission specifications.

## Bridging IEC 61850 to MQTT

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a messaging protocol designed for IoT devices and applications using a publish-and-subscribe model that is lightweight, efficient, reliable, and supports real-time communication. MQTT is well suited for resource-constrained environments, especially scenarios requiring efficient power and bandwidth use.

The industry has built an industrial IoT data specification called SparkplugB on top of MQTT 3.1.1, which provides basic data unified modeling capabilities while ensuring flexibility and efficiency. Thanks to the excellent design of the MQTT protocol, SparkPlugB provides good network state awareness and is able to provide strong interoperability for devices and systems.

By bridging IEC 61850 into MQTT, we can easily integrate the power system model into a Sparkplugb-based IoT system for management.

MQTT specializes in sending messages in distributed systems, such as power production workflows, while IEC 61850 can provide interoperability and strong abstraction of substation operations. Combined with the fast, secure, and reliable transmission channel provided by the MQTT protocol, IEC 61850 can directly use the Internet for data transmission, retaining its powerful data modeling capabilities and reliability while expanding its integration capabilities with other third-party applications.

[Neuron](https://neugates.io/) is a modern industrial IoT connectivity server that connects a wide range of industrial devices using standard or device-proprietary protocols, enabling the interconnection of industrial IoT platforms with a huge number of devices. As a lightweight industrial protocol gateway software, Neuron can run on a wide range of resource-limited IoT edge hardware devices, with the primary goal of addressing the challenge of accessing data-centric automation devices in a unified way, thus providing the necessary support for smart manufacturing.

[EMQX](https://www.emqx.com/en/products/emqx) is the world’s most scalable MQTT broker. EMQX provides efficient and reliable connectivity for IoT devices, enabling high-performance real-time movement and processing of messages and event streams, helping users rapidly build business-critical IoT platforms and applications.

Neuron's southbound IEC 61850 driver can capture and aggregate IEC 61850 data sources via the MMS protocol, convert to MQTT, and transmit to EMQX MQTT Broker for distribution to various applications.

You can find a detailed guide on bridging IEC 61850 data to MQTT with Neuron and EMQX in this blog: coming soon.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
