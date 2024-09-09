## **Introduction to OPC Protocol**

OPC (Open Platform Communications) protocol is a key technical standard in the field of industrial automation for enabling communication between devices, control systems, and applications. It provides a universal data exchange method for devices and systems from different manufacturers, greatly enhancing the interoperability and efficiency of industrial control systems.

The OPC standard is divided into Classic and Unified Architecture:

- **OPC Classic** specification was born in 1996, based on Microsoft Windows technology, using COM/DCOM (Distributed Component Object Model) to exchange data between software components. It includes sub-specifications such as OPC DA, OPC AE, OPC HAD, and OPC DX, each providing separate definitions for accessing process data, alarms, and historical data.
- **OPC Unified** Architecture (UA), the successor to OPC Classic, was released in 2006. It integrates all the functionalities of various OPC Classic sub-specifications into an extensible framework, independent of the platform and service-oriented. It no longer relies on COM implementation and is stronger in terms of security and scalability.

OPC UA and OPC DA differ significantly in several aspects like interoperability, security, functionality, performance, and compatibility. These variances can impact production and management expenses. This article will provide a comprehensive guide on OPC DA and OPC UA to help readers make wise choices based on specific industrial needs, thus reducing unnecessary costs effectively.

## **Unpacking OPC DA**

### What is OPC DA?

Before OPC technology emerged, there was no unified standard for interconnecting devices in the automation field. Different hardware manufacturers and software manufacturers use their own communication protocols, leading to protocol confusion and increased communication costs.

OPC Classic technology was born to facilitate interoperability between different software and hardware.

OPC DA (Data Access) is a protocol standard introduced earliest by the OPC Foundation, mainly used for accessing and exchanging real-time data. It is built on Microsoft's COM/DCOM technology, providing an industrial automation system with a standardized communication interface.

OPC DA supports reading, writing, subscribing, and unsubscribing real-time data. It adopts a client/server architecture, allowing multiple clients to access data on the server simultaneously.

It is widely used in manufacturing, process control, energy management, and other fields such as oil and gas, chemical, pharmaceutical, and power.

### Pros and Cons of OPC DA

Pros:

- Mature technology
- Wide application
- Ease of implementation and deployment

Cons:

- Dependency on the Windows platform
- Lack of security mechanisms
- Simple data model

## **Introducing OPC UA**

### What is OPC UA?

[OPC UA (Unified Architecture)](https://www.emqx.com/en/blog/opc-ua-protocol) is a new generation protocol standard introduced by the OPC Foundation based on the lessons learned from OPC DA. It adopts a service-oriented architecture (SOA) and provides a platform-independent, secure, and scalable communication mechanism.

Compared to OPC DA, OPC UA introduces a richer data model with support for complex data types and semantic descriptions. It also provides built-in security mechanisms such as authentication, authorization, and encrypted transmission. In addition, OPC UA supports multiple transport protocols such as TCP, HTTPS, WebSocket, etc.

With its outstanding performance and flexibility, OPC UA has been widely used in industrial Internet of Things (IIoT), smart manufacturing, remote equipment monitoring, and other fields. For example, in smart factories, OPC UA can achieve seamless data integration from shop floor equipment to upper-level systems such as MES, ERP, and more.

### Pros and Cons of OPC UA

Pros:

- Platform independence
- Strong security features
- A rich information model

Cons:

- The protocol is relatively complex, leading to higher development and implementation costs.

## **Head-to-Head Comparison**

|                                    | **OPC UA**                                                   | **OPC DA**                                                   |
| :--------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Service Discovery                  | Support finding available OPC UA servers on local PC or network | Only support discovering OPC DA servers in the local network |
| Namespace                          | All data is hierarchically represented (like files and folders), allowing OPC UA clients to discover and utilize simple and complex data structures | Basic support for hierarchical representation                |
| Access Control                     | Read and write data/information based on access permissions  | Supported                                                    |
| Subscription                       | Supported                                                    | Supported                                                    |
| Event                              | Supported                                                    | Supported                                                    |
| Method                             | Support remote method calls                                  | Not supported                                                |
| Cross-Platform                     | Has good cross-platform support, supports mainstream chip architectures, and supports multiple operating systems | Only supports Windows operating system                       |
| Data Transfer                      | Defines many protocols, providing options such as OPC binary transfer or more general SOAP-HTTPS | Forces the use of Windows COM and DCOM transfer, hides all transfer details in the programming interface |
| Session Security                   | Information is securely transmitted at 128-bit or 256-bit encryption levels;<br>The signature when receiving information must be identical to when sending it;<br>Each UA's client and server must be identified by OpenSSL certificates, providing the ability to control how applications and systems connect to each other;<br>Discovered information replay attacks are eliminated through sorting;<br>Applications can request user authentication (login credentials, certificates, etc.), and can further restrict or enhance user access permissions and the ability to view address space;<br>Record user and/or system activities, provide access audit tracking | Uses Windows DCOM session mechanism, security details are hidden |
| Future-Oriented                    | OPC UA's multi-layer architecture allows for the introduction of innovative technologies and methods, such as new transfer protocols, security algorithms, coding standards, and application services, without affecting existing applications | Microsoft has officially announced the end of support for DCOM technology, OPC DA cannot be reliably supported in newer Windows operating systems |
| Comprehensive Information Modeling | New features are constantly being added to the standard      | Not supported                                                |

## **Factors to Consider When Choosing Between OPC UA and OPC DA**

When choosing between OPC UA and OPC DA, you need to consider the following factors:

- System platform and compatibility requirements

  OPC UA is more adaptable to different environments and devices, while OPC DA's server and client can only run on Windows operating systems. If the deployment environment is more complex, OPC DA should be considered as a priority.

- Complexity of data models and functional needs

  OPC UA provides powerful business abstraction capabilities, allowing direct conversion of business logic into actual OPC UA information models that can be easily adjusted; whereas OPC DA only offers a hierarchical structure based on Server/Group/Tag. For complex business logic, OPC UA should be prioritized.

- Security and reliability requirements

  Compared to OPC UA, OPC DA requires a more stable operating environment, typically an intranet environment. If the network environment is complex, such as the need to transmit data over a public network, OPC UA should be prioritized.

- Scalability and future development needs

  OPC UA is significantly more scalable than OPC DA, and Microsoft's decreasing investment in COM technology will inevitably affect the future of OPC DA. The design of OPC DA is based on previous thoughts on middleware technology, which is clearly outdated. For future-oriented applications, OPC UA should be prioritized.

- Project budget and implementation timeline

  Taking into account the advantages of OPC UA mentioned earlier, it seems that OPC UA can effectively reduce deployment and maintenance costs. For budget-sensitive projects, OPC UA and OPC DA can be chosen based on specific circumstances.

- Experience and capabilities of the technical team

  OPC UA requires a greater understanding of concepts for configuration and development compared to OPC DA, especially in terms of session security and comprehensive information modeling. Configuration for OPC DA mainly focuses on settings within the Windows system.

## **FAQs About OPC UA and OPC DA**

### Can OPC UA completely replace OPC DA? 

Although OPC UA is an upgraded version of OPC DA, in certain scenarios, especially for legacy systems, OPC DA still holds its application value. Both can coexist and complement each other.

### Is OPC UA difficult to implement? 

Even though the OPC UA protocol can be complex, there are now many mature development toolkits and frameworks available that significantly reduce implementation difficulty. Additionally, many vendors offer ready-made solutions based on OPC UA.

## **NeuronEX: An Industrial Gateway that Supports OPC Protocols**

[NeuronEX](https://www.emqx.com/en/products/neuronex) is software tailored for the industrial sector, focusing on equipment data collection and edge intelligent analysis. It is primarily deployed in industrial settings, facilitating industrial equipment communication, industrial bus protocol acquisition, industrial system data integration, edge-level data filtering and analysis, AI algorithm integration, and integration with [IIoT platforms](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions). NeuronEX provides multi-protocol access capability, supporting simultaneous access to dozens of industrial protocols such as [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol), Ethernet/IP, [BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained), Siemens, Mitsubishi, and more.

The NeuronEX OPC UA plugin can be used as a client to access OPC UA servers such as KEPServerEX, Industrial Gateway OPC Server, Prosys Simulation Server, and Ignition. It can also directly access the built-in OPC UA server of hardware devices, such as the built-in server of Siemens S7-1200 PLC, Omron NJ series PLC, etc. For more information, you can check [OPC UA | NeuronEX Docs (emqx.com)](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/opc-ua/overview.html) and [Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial | EMQ (emqx.com)](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot).

NeuronEX does not directly support the direct acquisition of OPC DA data. However, it is possible to use NeuOPC to convert OPC DA to OPC UA and then use NeuronEX's OPC UA Plugin for data acquisition. For more information, you can check [OPC DA | Neuron Documentation](https://docs.emqx.com/en/neuron/latest/configuration/south-devices/opc-da/overview.html).

## **Conclusion**

While OPC DA may offer advantages in certain scenarios, OPC UA generally provides a more robust and future-proof solution with enhanced security features and better support for modern industrial applications. Ultimately, the choice between OPC UA and OPC DA will depend on the specific requirements and objectives of each industrial operation, but making an informed decision can significantly impact efficiency, cost-effectiveness, and overall performance in the long run.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
