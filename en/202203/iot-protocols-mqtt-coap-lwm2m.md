With the development and popularization of IoT (Internet of Things) technology, more and more intelligent devices have the ability of network connection and data transmission. Because of the complexity and diversity of IoT scenarios, hardware conditions of device terminals, network stability, traffic limitation, device power consumption, number of device connections, and other factors can make the messaging of IoT devices very different from that of traditional Internet scenarios, resulting in various IoT communication protocols.

This article will select several popular IoT protocols, and introduce them one by one from their technical features, applicable scenarios, comparative advantages, market conditions, etc. to provide a reference for IoT users and help you choose appropriate IoT protocols in projects.

## Classification of Protocols

Before introduction, we will give a simple classification of IoT Protocols to make it easier for readers to understand their application scenarios.

### **From the Functional Perspective**

From the functional perspective, we can divide them into two categories: Physical **Layer/Data Link Layer Protocol** and **Application Layer Protocol**.

Physical Layer/Data Link Layer Protocol is generally responsible for networking and communication between devices, such as 2G/3G/4G/5G, NB-IoT, WiFi, ZigBee, LoRa, and other long-distance communications. There are also short-distance wireless protocols such as RFID, NFC, and Bluetooth Protocol, and wired protocols such as RS232 and USB.

Application Layer Protocol is mainly the device communication protocol running on the traditional Internet TCP/IP Protocol. This kind of protocol supports the data exchange and communication from the device to the Cloud platform through the Internet, and the common protocols include HTTP, MQTT, CoAP, LwM2M, and XMPP.

### **From the Application Perspective**

From the application perspective of the protocol in the IoT system, we can divide the protocol into Cloud Protocol and Gateway Protocol.

Cloud Protocol is a protocol based on TCP/IP. Data of IoT (such as sensors and control devices) usually need to be transmitted to the Cloud to connect users through the Cloud, and integrate with enterprise systems.

Iot devices that support TCP/IP can access the Cloud through WIFI, cellular network, and Ethernet, using HTTP, MQTT, CoAP, LwM2M, XMPP, and other application layer protocols.

Gateway Protocol is suitable for short-distance communication which cannot be directly put into the Cloud, such as Bluetooth, ZigBee, LoRa, etc. This type of device needs to go to the Cloud through TCP/IP Protocol after gateway conversion.

## ZigBee

ZigBee is a mesh-network wireless protocol designed for building and home automation applications, which is one of the most popular mesh protocols in the IoT environment. At present, it is mainly used for LAN connection, and all kinds of equipment are accessed and controlled as a gateway on the device side.

### Characteristics of the Protocol 

• Low power consumption: The transmitting power is only 1mW. In the standby mode of low power consumption, two No. 5 dry batteries can last for up to 2 years, eliminating the trouble of charging or frequently replacing batteries.

• Low cost: The simple and compact protocol greatly reduces the requirements for communication control, so as to reduce the hardware cost, and at the same time, the protocol patent fee is not charged.

• Low rate: ZigBee works at the speed of 20~250 kbps, providing the raw data throughput rates of 250 kbps (2.4 GHz), 40 kbps (915 MHz), and 20 kbps (868 MHz) respectively, which meets the application demand of low-speed data transmission.

• Short distance: The transmission range of adjacent nodes is 10~100 m, basically covering ordinary home and office environment; After increasing the transmitting power, it can be increased to 1~3 km, and the transmission distance can be longer through the relay between routing and inter-node communication.

• Low delay: The response speed of ZigBee is fast. Generally, it only takes 15 ms to switch from sleep state to working state, and only 30 ms for node connection to enter the network, which saves power. By comparison, Bluetooth takes 3-10 seconds, and WiFi takes 3 seconds.

• High capacity: ZigBee can adopt star, sheet, and mesh network structure. A master node can manage several sub-nodes, and at most one master node can manage 254 sub-nodes; Meanwhile, the master node can also be managed by network nodes of the upper layer, forming a large network of 65,000 nodes at most.

• High security: ZigBee provides CRC packet integrity checking function, supports authentication and identification, and adopts AES-128 encryption algorithm, and each application can flexibly determine its security attribute.

• License-free Frequency Band: Direct Sequence Spread Spectrum for ISM (Industrial Scientific Medicine) bands: 2.4 GHz for global use, 915 MHz for North America, and 868 MHz for Europe.

### Market Conditions

ZigBee technology has such outstanding advantages as low power consumption, large node capacity, short time delay, safety, and reliability, which can meet the application requirements of smart home. It is the core wireless networking connection technology of Smart Home. Thanks to the rapid development of the Smart Home market, the number of Smart Home Devices applying ZigBee technology is constantly increasing. The application and promotion of ZigBee technology is accelerated day by day.

Compared with WiFi and Bluetooth technology, ZigBee technology has outstanding advantages in power consumption, node capacity, self-networking ability, and security, and its application scale is expanding constantly.

## NB-IoT

NB-IoT is a new cellular technology developed by the 3GPP standardization organization and is a type of Low Power Wide Area (LPWA) IoT connectivity, primarily for connecting terminals with limited bandwidth resources, allowing them to collect and exchange data with fewer resources than technologies such as GRPS, 3G, and LTE.

NB-IoT develops rapidly from 2017 to 2018, and many operators around the world have achieved commercial deployment. The low cost, low power consumption, and wide coverage of NB-IoT enable users to implement new scenarios and new applications that traditional cellular networks cannot support.

On July 9, 2020, 3GPP announced the freezing of 5G R16 standard, and NB-IoT was formally incorporated into 5G standard, becoming the core technology of 5G mMTC mass IoT connection scenario.

### Characteristics of the Protocol

• A low-power "sleep" mode (PSM and eDRX) is introduced.

• The communication quality requirement is reduced, and the terminal design is simplified (half duplex mode, protocol stack simplification, etc.).

• Two function optimization modes (CP mode and UP mode) are used to simplify the process and reduce the interaction between the terminal and the network.

• It has ultra-low coverage, covering an enhanced 20dB over GPRS, which is three times the coverage of GPRS. 

### Market Conditions

At present, NB-IoT has entered into the era of hundred-million-level connection, and subsequently, with the full coverage construction of commercial NB-IoT 5G network by global operators, NB-IoT will continue to erupt in smart home, smart agriculture, industrial manufacturing, energy meter, fire smoke sensing, logistics tracking, financial payment, and other fields.

Taking the China Telecom IoT Open Platform as an example, this platform realizes centralized access to NB-IoT and other IoT devices of China Telecom, and provides government and enterprise users with services such as device management, data interface, and application enabling of IoT.

EMQ has participated in the construction of the platform since the beginning, cooperated with CTWing to develop NB-IoT equipment access and message routing capability for the platform, and simultaneously supports the access of Telecom’s TLINK, MQTT, and other protocol equipment. The platform’s overall design access capacity reaches hundred-million levels.

## LoRa

LoRa Protocol(named from the abbreviation of "Long Range".) is a standard protocol for low power, long-range, and wireless WAN (wide area networks).

Compared with other wireless communication protocols (such as ZigBee, Bluetooth, and WIFI), LoRa is characterized by longer propagation distance under the same power consumption, realizing the unification of low power consumption and long distance, and it is 3-5 times larger than traditional radio frequency communication under the same power consumption.

LoRa has a variety of wireless technologies in IoT applications, which can be either LAN or WAN. The LoRa network comprises four parts: terminal (built-in LoRa module), gateway (or base station), server, and Cloud.

The data transmission rate of LoRaWAN ranges from 0.3 kbps to 37.5 kbps. In order to maximize the battery life of the terminal equipment and the whole network capacity, the LoRaWAN network server controls the data transmission rate and the radio frequency output power of each terminal device through an ADR (Adaptive Data Rate) scheme.

### Characteristics of the Protocol

• High coverage: The covering distance of single LoRa gateway is generally in the range of 3-5 km, even over 15 km in wide area.

• Low power consumption: Rechargeable battery power supply system can support for many years or even more than ten years.

• High capacity: Thanks to the characteristics of no-connection of the terminals, it can ensure the access of a large number of terminals.

• Low cost: The cost of communication network is very low. In addition, it is suitable for narrowband transmission data.

• High security: It uses AES128 encryption, which ensures high security.

### Market Conditions

LoRa is extremely flexible for rural or indoor applications in Smart Agriculture, Smart City, Industrial Internet of Things (IIoT), Smart Environment, Smart Home and Buildings, Smart Utilities and Metrology, and Intelligent Supply Chain and Logistics.

LoRa is convenient for networking. By using strong penetrating power, LoRa can be connected to a large range of equipment at low cost. Compared with the access through NB-IoT and SIM card of the operator, LoRa does not need to change the card or pay fees every year, so it has a lower cost for long-term use.

## MQTT

MQTT Protocol is an IoT communication protocol based on publish/subscribe mode, which occupies half of the IoT Protocol because of its simplicity, supporting QoS, and small packet size.

MQTT Protocol is widely used in the fields of IoT, Mobile Internet, Intelligent Hardware, IoV, Energy&Utilities, etc., which can not only be used as a gateway to access communication on the device side, but also as a Device-Cloud Communication Protocol. Most gateway protocols such as ZigBee and LoRa are finally converted into MQTT Protocol to access Cloud.

![MQTT](https://assets.emqx.com/images/cb9f29b8586d68cff9689e7e3b5867d8.png)

### Characteristics of the Protocol

- Light-weight and reliable: The MQTT message is compact, which can realize stable transmission on severely limited hardware equipment and network with low bandwidth and high delay.
- Publish/subscribe mode: Based on the publish/subscribe mode, the advantage of publishing and subscribing mode is that the publisher and subscriber are decoupled: Subscribers and publishers do not need to establish a direct connection or be online at the same time.
- Created for the IoT: It provides comprehensive IoT application features such as heartbeat mechanism, testament message, QoS quality level+offline message, and theme and security management.
- Better ecosystem: It covers all-language platform's clients and SDKs, and it has mature Broker server software, which can support massive Topic and ten-million-level device access and provide rich enterprise integration capabilities.

### Communication Mode

MQTT uses the publish-subscribe mode, which is different from the traditional client-server mode. It separates the client who sends the message (publisher) from the client who receives the message (subscriber), and the publisher does not need to establish direct contact with the subscriber. We can let multiple publishers publish messages to a subscriber, or multiple subscribers can receive a publisher's message at the same time.

### Market Conditions

MQTT is one of the most important standard protocols in the IoT field, which is widely used in industries such as IoV, Industrial Internet of Things (IIoT), Smart Home, Smart City, Electric Petroleum Energy, etc.

MQTT is the standard communication protocol of IoT platform of top Cloud manufacturers such as AWS IoT Core, Azure IoT Hub, and Alibaba Cloud IoT platform, and it is the preferred protocol for Cloud in various industries (such as industrial Internet, car networking, and smart home) and many gateway protocols.

As one of the most popular MQTT brokers in the world, [EMQX](https://www.emqx.com/en/products/emqx) provides the cloud-native distributed IoT messaging platform of "run anywhere, connect once, integrate everything", with an all-in-one [distributed MQTT broker](https://www.emqx.io) and SQL-based IoT rule engine, powering high-performance, reliable data movement, processing, and integration for business-critical IoT solutions.

## CoAP

CoAP is an HTTP-like Protocol in the IoT world, used on resource-constrained IoT devices. Its detailed specification is defined in RFC 7252.

Most IoT devices are resource-constrained, such as CPU, RAM, Flash, network broadband, etc. For this kind of device, it is unrealistic to realize the information exchange directly by using TCP and HTTP of the existing network. CoAP Protocol emerges as the times require, in order to make this part of devices connect to the network smoothly.

### Characteristics of the Protocol

CoAP refers to many design ideas of HTTP, and it also improves many design details and adds many practical functions according to the specific situation of limited resource-limited devices.

- It is based on message model
- Based on UDP Protocol, transport layer supports restricted devices
- It uses request/response model similar to HTTP request, and HTTP is text format, while CoAP is binary format, which is more compact than HTTP
- It supports two-way communication
- It has the characteristics of light-weight and low power consumption
- It supports reliable transmission, data re-transmission, and block transmission to ensure reliable arrival of data
- It supports IP multicast
- It supports observation mode
- It supports asynchronous communication

### Market Conditions

Compared with MQTT, CoAP is lighter with lower overhead, and it is more suitable for certain device and network environments. EMQX and some public cloud IoT platforms provide CoAP access capability. Please refer to: [A「date」between MQTT and CoAP in the EMQX world](https://www.emqx.com/en/blog/url-mqtt-and-coap).

## LwM2M

LwM2M is a lightweight IoT protocol suitable for resource-limited terminal equipment management. LwM2M Protocol was born at the end of 2013, which was proposed and defined by OMA (Open Mobile Alliance). At present, the mature version number is still 1.0, and OMA experts are working on version 1.1.

### Characteristics of the Protocol

**•** The most important entities of LwM2M Protocol include LwM2M Server and LwM2M Client.

**•** As a server, the LwM2M Server is deployed at the M2M service provider or the network service provider.

**•** As a client, the LwM2M Client is deployed on each LwM2M device.

In addition, LwM2M Bootstrap Server or SmartCard can be added as needed to complete the initial boot for the client.

LwM2M Protocol has the following outstanding features:

- The Protocol is based on REST architecture.
- Protocol messaging is achieved through CoAP Protocol.
- The Protocol defines a compact, efficient and scalable data model.

LwM2M Protocol adopts REST to keep pace with the times and realize a simple and easy-to-understand style.

However, because the protocol’s service object is the terminal equipment with limited resources, the traditional HTTP data transmission mode is too cumbersome to support the limited resources, so the REST-style CoAP is chosen to complete the message and data transfer. On the one hand, compared with TCP, CoAP is based on UDP. It is more flexible in environments where network resources are limited and devices cannot be always on-line (for security reasons, UDP-based DTLS secure transport protocol is used). On the other hand, the message structure of CoAP itself is very simple, the message is compressed, and the main part of CoAP can be made very compact without occupying too much resources.

For similar reasons, the protocol’s data structure must be simple enough. The LwM2M Protocol defines a resource-based model, each resource may not only carry a numerical value, but also point to an address to represent each item of information available in the LwM2M client. All resources exist in an object instance, that is, the instantiation of an object. The LwM2M Protocol pre-defines eight types of objects to meet the basic requirements:

For scalability, the Protocol also allows more objects to be customized according to actual needs. In such a data model, resources, object instances, and objects are represented by ID corresponding to numbers to achieve maximum compression, so that any resource can be represented in a concise manner of at most 3 levels, e.g., /1/0/1 represents the server short ID resource in the first instance of the Server Object. At the registration stage, the LwM2M client transmits the object instance carrying the resource information to the LwM2M server, so as to notify the server of the capability of its own device.

[EMQ](https://www.emqx.com/en) also realizes LwM2M access capability on the EMQX server and most functions of the LwM2M Protocol. LwM2M device can register to EMQX-LWM2M to access and manage equipment through EMQX-LWM2M. Device can also report information to EMQX-LWM2M and collect data by using EMQ back-end service.

## XMPP

**XMPP** Extensible Message Processing Protocol (XMPP) is an XML-based instant messaging protocol, which embeds communication context information into XML structured data and enables instant communication among people, among application systems, and between people and application systems.

### Characteristics of the Protocol

• All XMPP information is based on XML, it is the de facto standard of information exchange with high scalability.

• XMPP is a distributed system where each server controls its own resources.

• XMPP Protocol is open source that uses XML to define interactions between clients and servers.

### Market Conditions

XMPP features a mature protocol and extensions, and is designed specifically for instant messaging (IM) scenarios. xMPP is the oldest IM protocol, and lM programs like Google Hangouts, WhatsApp Messenger, and others are based on XMPP.

However, because XMPP relies on XML Protocol, which is too heavy in IoT scenario, it is not suitable for IoT transmission.

## Conclusion

Horizontally, the IoT has a wide range of application scenarios in almost all industries, and each industry has different working conditions and networking modes. Vertically, the IoT system covers the whole software and hardware chain of sensor/control equipment, data access, transmission, route switching components, and data storage & processing, and each link requires reasonable and efficient technical solutions.

At present, the IoT Protocols have diversified development. Different industries and scenarios are applicable to different protocols. In the same scenario, there can be multiple protocols to choose. No protocol can dominate the market, and there is certain complementary effect among various protocol. Therefore, to realize the connectivity of the IoT devices and data, the key point is not the unification with the protocol, but in the connectivity between different protocols and the unification of the upper business application layer protocol.

EMQ addresses data connectivity issues for IoT devices. The flagship product EMQX IoT message broker can connect any device through open standard MQTT, CoAP and LwM2M Protocols. In case of complex and diverse industrial protocols in industrial scenarios, it can also be converted into unified MQTT Protocol through [Neuron](https://www.emqx.com/en/products/neuron), the edge industrial protocol gateway software, to meet the data acquisition requirements of most IoT scenarios and provide an efficient and reliable data access layer for enterprises' IoT business.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
