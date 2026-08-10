With the rise and widespread use of IoT (Internet of Things) technology, a growing number of smart devices can now connect to networks and transmit data. However, due to the complexity and diversity of IoT scenarios, messaging between IoT devices can be very different from traditional Internet scenarios. Factors such as hardware conditions of device terminals, network stability, traffic limitations, device power consumption, and the number of device connections result in a variety of IoT communication protocols and standards.

This article will introduce 8 popular IoT protocols, discussing their technical features and advantages, to help you choose the appropriate one for your projects.

## Classification of IoT Protocols

In the IoT ecosystem, there exist various protocols, each with its unique features and capabilities that cater to different situations. To comprehend the commonly used IoT protocols, we can classify them from two perspectives, which will be discussed in detail in this blog.

### **By Function**

From the functional perspective, we can divide them into two categories: **Physical** **Layer/Data Link Layer Protocol** and **Application Layer Protocol**.

Physical Layer/Data Link Layer Protocols are generally responsible for facilitating networking and communication between devices. Examples of these protocols include 2G/3G/4G/5G, NB-IoT, WiFi, ZigBee, LoRa, and other long-distance communication protocols. Additionally, there are short-distance wireless protocols like RFID, NFC, and Bluetooth, as well as wired protocols like RS232 and USB.

Application Layer Protocols are mainly the device communication protocol running on the traditional Internet TCP/IP Protocol. They enable devices to exchange data and communicate with the Cloud platform through the Internet. Commonly used protocols include HTTP, MQTT, CoAP, LwM2M, and XMPP.

### **By Application**

From an IoT system architecture perspective, communication can be divided into direct device-to-cloud communication and gateway-assisted communication.

Devices that support TCP/IP can connect directly to cloud platforms using application-layer protocols such as HTTP, MQTT, CoAP, LwM2M, and XMPP over networks such as Wi-Fi, cellular, and Ethernet.

Devices using short-range or non-IP connectivity technologies such as Bluetooth, Zigbee, and LoRa may connect to a gateway first. The gateway can then forward or convert the device data using IP-based protocols for transmission to the cloud.

## 1. ZigBee

ZigBee is a mesh-network wireless protocol designed for building and home automation applications, which is one of the most popular mesh protocols in the IoT environment. At present, it is mainly used for LAN connection, and all kinds of equipment are accessed and controlled as a gateway on the device side.

- **Low Power Consumption**: The transmitting power is only 1 mW. In the standby mode of low power consumption, two No.5 dry batteries can last for up to 2 years, eliminating the trouble of charging or frequently replacing batteries.
- **Low Cost**: The protocol is simple and compact, reducing communication control requirements and hardware costs. Additionally, there are no protocol patent fees.
- **Low Rate**: ZigBee works at the speed of 20~250 kbps, providing raw data throughput rates of 250 kbps (2.4 GHz), 40 kbps (915 MHz), and 20 kbps (868 MHz) respectively, which meets the application demand of low-speed data transmission.
- **Short Distance**: The range of communication between adjacent nodes is typically 10 to 100 meters, which is suitable for home and office environments. By increasing the transmitting power, the range can be extended up to 1 to 3 kilometers. Additionally, the transmission distance can be further increased by utilizing relay communication between routing and inter-node communication.
- **Low Latency**: Zigbee supports fast device wake-up and communication, making it suitable for many low-power IoT applications that require responsive device interactions.
- **High Capacity**: ZigBee offers three networks: star, tree, and mesh. A master node can control up to 254 sub-nodes, and can be managed by upper layer nodes, creating a network of up to 65,000 nodes.
- **High Security**: ZigBee provides a CRC packet integrity checking function, supports authentication and identification, and adopts the AES-128 encryption algorithm, and each application can flexibly determine its security attribute.
- **License-free Frequency Band**: Direct Sequence Spread Spectrum for ISM (Industrial Scientific Medicine) bands: 2.4 GHz for global use, 915 MHz for North America, and 868 MHz for Europe.

ZigBee’s outstanding advantages make it the core wireless networking connection technology of Smart Home. With the rapid development of the Smart Home market, the application and promotion of ZigBee technology is accelerated day by day.

> Explore the integration of Zigbee and MQTT in this practical guide: [MQTT with Zigbee: A Practical Guide](https://www.emqx.com/en/blog/mqtt-with-zigbee-a-practical-guide).

## 2. Matter

[Matter](https://csa-iot.org/all-solutions/matter/) is an open, IP-based smart home connectivity standard developed by the Connectivity Standards Alliance (CSA), with support from companies including Amazon, Apple, Google, and many other smart home ecosystem participants. It aims to develop and promote a new connectivity protocol that exempts patent fees, simplifying the development costs for smart home device manufacturers.

Matter is an IP-based application-layer standard that operates over networking technologies such as Ethernet, Wi-Fi, and Thread. It enables local interoperability and internet connectivity, facilitating communication between devices, applications, and cloud services.

- **Lower Latency and Higher Reliability**: Compared to cloud-to-cloud connections, Matter offers lower latency and higher reliability because it is a locally connected IP-based protocol.
- **Lower Development Costs**: Building once for all Matter-certified ecosystems significantly improves compatibility among different manufacturers' smart home products, reducing development costs.
- **Interoperability and Standardization**: Devices adopting the Matter standard can seamlessly work together, allowing users to easily build and expand their smart home systems with consistent settings across all Matter-supported devices.
- **Security**: Matter adopts modern security standards and encryption technologies to ensure secure communication and data transmission between devices. It also requires device manufacturers to follow security best practices, such as using strong passwords and regularly updating device software, for enhanced security assurance.
- **Scalability and Flexibility**: The Matter protocol supports a wide range of device types and functions, including lighting, security systems, temperature control, and power management. It can adapt to various scales and needs, from small residences to large commercial buildings. Additionally, Matter provides flexible configuration and customization options for personalized settings based on users' preferences and requirements.

## 3. NB-IoT

NB-IoT is a Low Power Wide Area (LPWA) cellular technology standardized by 3GPP, primarily designed for connecting devices with limited bandwidth and power resources. This technology enables these terminals to collect and exchange data with fewer resources than other technologies, such as GPRS, 3G, and LTE.

NB-IoT developed rapidly from 2017 to 2018, and many operators around the world have achieved commercial deployment. The low cost, low power consumption, and wide coverage of NB-IoT enable users to implement new scenarios and new applications that traditional cellular networks cannot support.

NB-IoT was introduced in 3GPP Release 13 and has continued to evolve as part of the 3GPP standards ecosystem for massive IoT connectivity.

- A low-power "sleep" mode (PSM and eDRX) is introduced.
- The communication quality requirement is reduced, and the terminal design is simplified (half duplex mode, protocol stack simplification, etc.).
- Two function optimization modes (CP mode and UP mode) are used to simplify the process and reduce the interaction between the terminal and the network.
- It provides enhanced coverage compared with traditional cellular technologies, helping devices maintain connectivity in indoor and hard-to-reach environments.

Currently, NB-IoT has reached a milestone of connecting hundreds of millions of devices. With the global operators constructing commercial NB-IoT 5G network and providing full coverage, NB-IoT is expected to expand further in various fields such as smart homes, smart agriculture, industrial manufacturing, energy meter, fire and smoke sensing, logistics tracking, financial payment, and many others.

## 4. LoRa

LoRa, short for "Long Range," is a low-power, long-range wireless modulation technology, while LoRaWAN is a networking protocol built on top of LoRa.

Compared with short-range wireless technologies such as Zigbee and Bluetooth, LoRa is designed to provide long-range communication while maintaining low power consumption, making it well suited to battery-powered IoT devices deployed over large areas.

LoRa and LoRaWAN are widely used in low-power wide-area IoT applications. A typical LoRaWAN network consists of four main components: end devices, gateways, a network server, and application services.

The data transmission rate of LoRaWAN ranges from 0.3 kbps to 37.5 kbps. In order to maximize the battery life of the terminal equipment and the whole network capacity, the LoRaWAN network server controls the data transmission rate and the radio frequency output power of each terminal device through an ADR (Adaptive Data Rate) scheme.

- **High Coverage**: A single LoRa gateway typically covers a range of 3-5km, extending up to 15km in open areas.
- **Low Power Consumption**: Battery-powered systems can support several years to over a decade of operation. 
- **High capacity**: Due to the nature of unconnected terminals, it ensures the connection of a large number of terminals. 
- **Low Cost**: The communication network costs are extremely low, and it is suitable for transmitting narrowband data. 
- **Security**: It uses AES128 encryption to ensure a high level of security.

LoRa offers high flexibility for applications in smart agriculture, smart cities, [Industrial Internet of Things](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) (IIoT), smart environments, smart homes and buildings, smart utilities and metering, as well as smart supply chains and logistics, particularly in rural or indoor settings.

LoRa's easy network setup and strong penetration capabilities enable low-cost connectivity for devices over large areas. Compared with operator-managed cellular connectivity, private LoRaWAN networks can avoid recurring per-device SIM subscription fees, potentially reducing long-term connectivity costs.

## 5. MQTT

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is an OASIS standard messaging protocol for the Internet of Things (IoT). It is designed with an extremely lightweight publish/subscribe messaging model, making it ideal for connecting IoT devices with a small code footprint and minimal network bandwidth and exchanging data in real-time between connected devices and cloud services.

MQTT can be used for both device-to-cloud communication and communication between gateways, applications, and backend services. Data collected through connectivity technologies such as Zigbee and LoRaWAN can be forwarded or converted to MQTT for transmission to cloud platforms.

![MQTT](https://assets.emqx.com/images/cb9f29b8586d68cff9689e7e3b5867d8.png)

- **Lightweight and Reliable**: MQTT messages are compact, enabling stable transmission on severely constrained hardware devices and networks with low bandwidth and high latency.
- **Publish/Subscribe Model**: Based on the publish/subscribe model, its advantage lies in decoupling publishers and subscribers - they don't need to establish a direct connection or be online simultaneously.
- **Designed for IoT**: Provides comprehensive IoT application features such as [keep alive](https://www.emqx.com/en/blog/mqtt-keep-alive) mechanism, [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message), [QoS](https://www.emqx.com/en/blog/introduction-to-mqtt-qos), [topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), and security management.
- **More Complete Ecosystem**: It covers client and SDK platforms in all languages, and has mature Broker server software, supporting a vast number of topics, millions of device connections, and rich enterprise integration capabilities.

MQTT is a messaging protocol that uses a publish-subscribe model, which is different from the traditional client-server model. It separates the message sender (publisher) from the receiver (subscriber), making it an efficient way to send and receive messages in a distributed network. Multiple publishers can send messages to a subscriber, and multiple subscribers can receive messages from a publisher simultaneously.

MQTT today is widely used in the IoT, [Industrial IoT](https://www.emqx.com/en/blog/industrial-iot-systems) (IIoT), Internet of Vehicles (IoV), and [Connected Cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know), as well as in a wide variety of industries such as automotive, manufacturing, telecommunications, transportation & logistics, and oil & gas, etc.

MQTT is the standard communication protocol of the IoT platform of top Cloud providers such as [AWS IoT Core](https://www.emqx.com/en/blog/understanding-aws-iot-core), [Azure IoT Hub](https://www.emqx.com/en/blog/azure-iot-hub-4-key-features-use-cases-and-how-to-get-started), and Alibaba Cloud IoT platform. It is also the preferred protocol for gateways and Cloud in various industries.

> Learn more about MQTT protocol: [MQTT Guide 2026](https://www.emqx.com/en/mqtt-guide).

## 6. CoAP

CoAP is an HTTP-like Protocol in the IoT world, used on resource-constrained IoT devices. Its detailed specification is defined in RFC 7252.

IoT devices have limited resources like CPU, RAM, Flash, and network bandwidth. Direct data exchange using TCP and HTTP is unrealistic. CoAP protocol emerged to solve this problem and enable these devices to connect to the network smoothly.

CoAP incorporates HTTP design ideas and develops practical functions specific to resource-limited devices.

- Based on the message model.
- Its transport layer is based on UDP Protocol and supports restricted devices.
- Uses [request/response](https://www.emqx.com/en/blog/mqtt5-request-response) model similar to HTTP and binary format which is more compact than the text format of HTTP.
- Supports two-way communication.
- Lightweight and low power consumption.
- Supports reliable transmission, data re-transmission, and block transmission to ensure reliable arrival of data.
- Supports IP multicast.
- Supports observation mode.
- Supports asynchronous communication.

Compared with MQTT, CoAP is lighter with lower overhead, and it is more suitable for certain device and network environments.

>**More resources about CoAP protocol:**
>
>[CoAP Protocol: Key Features, Use Cases, and Pros/Cons](https://www.emqx.com/en/blog/coap-protocol)
>
>[Connecting CoAP Devices to EMQX](https://www.emqx.com/en/blog/connecting-coap-devices-to-emqx)

## 7. LwM2M

LwM2M is a lightweight IoT protocol suitable for resource-limited terminal equipment management. LwM2M Protocol was proposed and defined by OMA (Open Mobile Alliance) in 2013. 

The most important entities of LwM2M Protocol include LwM2M Server and LwM2M Client.

- As a server, the LwM2M Server is deployed at the M2M service provider or the network service provider.
- As a client, the LwM2M Client is deployed on each LwM2M device.

In addition, LwM2M Bootstrap Server or SmartCard can be added as needed to complete the initial boot for the client.

LwM2M Protocol has the following features:

- The Protocol is based on REST architecture.
- Protocol messaging is achieved through CoAP Protocol.
- The Protocol defines a compact, efficient, and scalable data model.

The LwM2M protocol uses REST to achieve a clear and understandable style. However, traditional HTTP data transfer method is too cumbersome and challenging to support constrained resources of resource-limited terminal devices. Therefore, the protocol uses CoAP with RESTful style for message and data delivery.

On one hand, CoAP, based on UDP, is more adept in environments with limited network resources and devices not always online compared to TCP (DTLS secure transport protocol based on UDP was chosen for security reasons). On the other hand, CoAP's message structure is very simple, with compressed messages that can be extremely compact, requiring minimal resources.

For similar reasons, the protocol's data structure must be sufficiently simple. The LwM2M protocol defines a model based on resources, where each resource can carry a value, point to an address, representing every available piece of information in an LwM2M client. Resources are contained within object instances, i.e., the instantiation of an object.

The LwM2M Protocol pre-defines eight types of objects to meet the basic requirements:

| Object                  | Object ID |
| :---------------------- | :-------- |
| Security                | 0         |
| Server                  | 1         |
| Access Control          | 2         |
| Device                  | 3         |
| Connectivity Monitoring | 4         |
| Firmware                | 5         |
| Location                | 6         |
| Connectivity Statistics | 7         |

For scalability, the protocol also allows customization of additional objects based on specific needs. In this data model, resources, object instances, and objects are represented by numerical IDs to achieve maximum compression. Therefore, any resource can be represented in a concise manner with up to 3 levels, such as /1/0/1 representing the short ID resource of the first instance of the Server Object. During the registration phase, the LwM2M client transmits object instances carrying resource information to the LwM2M server, informing the server of the capabilities of the device itself.

[EMQX](https://www.emqx.com/en/products/emqx) provides an [LwM2M gateway](https://docs.emqx.com/en/enterprise/latest/gateway/lwm2m.html) that enables device onboarding, security management, seamless conversion of LwM2M-MQTT messages, and integration of LwM2M data with over 40 external data systems.

## 8. XMPP

**XMPP** (Extensible Messaging and Presence Protocol) is an XML-based instant messaging protocol that embeds communication context information into structured XML data, enabling real-time communication between individuals, application systems, and individuals with application systems.

- All XMPP information is based on XML. It is the de facto standard of information exchange with high scalability.
- XMPP is a distributed system where each server controls its own resources.
- XMPP Protocol is open source and uses XML to define interactions between clients and servers.

XMPP is a mature and feature-rich protocol designed specifically for instant messaging (IM) scenarios. It is the backbone of popular IM applications like Google Hangouts and WhatsApp Messenger.

However, due to its reliance on the XML protocol, XMPP is too heavy for IoT applications and is not suitable for IoT data transmission.

## EMQX: The World’s Leading Broker that Supports Multiple IoT Protocols

EMQX is a large-scale distributed MQTT messaging platform that offers "unlimited connections, seamless integration, and anywhere deployment."

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


As a high-performance, scalable [MQTT message broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), EMQX provides reliable real-time message transmission and device connectivity solutions for IoT applications. With its robust built-in rule engine and data integration capabilities, EMQX can perform real-time data processing, transformation, and routing for massive IoT data. It seamlessly integrates IoT data with various backend databases and analytics tools, enabling enterprises to build IoT platforms and applications with leading competitiveness rapidly.

EMQX not only fully supports MQTT 3.1, 3.1.1, and 5.0 but also supports various mainstream protocols such as STOMP, OCPP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), LwM2M/CoAP for connectivity. It provides extensive connection capabilities to handle IoT devices for various scenarios and serves as a unified access platform and management interface for backend IoT management services, reducing the adaptation costs between heterogeneous protocols.

## Frequently Asked Questions About IoT Protocols

### What is the most commonly used IoT protocol?

There is no single protocol that fits every IoT scenario. MQTT is widely used for device-to-cloud messaging because of its lightweight publish/subscribe model, while protocols and technologies such as CoAP, Zigbee, Matter, LoRaWAN, and NB-IoT are suited to different connectivity, device management, and networking requirements.

### What is the difference between MQTT and CoAP?

MQTT uses a publish/subscribe messaging model and typically relies on a broker to route messages between clients. CoAP primarily follows a RESTful request/response model similar to HTTP and is designed for constrained devices and networks. MQTT is often used for scalable device-to-cloud messaging, while CoAP is suitable for lightweight, resource-oriented communication.

### What is the difference between LoRa and LoRaWAN?

LoRa is a low-power, long-range wireless modulation technology, while LoRaWAN is a networking protocol built on top of LoRa that defines how devices communicate with gateways and network servers.

### Is Matter replacing Zigbee?

Not necessarily. Matter is an IP-based smart home standard that can operate over technologies such as Wi-Fi, Ethernet, and Thread, while Zigbee is a separate low-power wireless networking technology. Existing Zigbee devices can also be integrated with Matter ecosystems through compatible bridges.

### How do I choose the right IoT protocol?

The best choice depends on factors such as communication range, bandwidth, power consumption, latency, device constraints, network topology, security requirements, and whether devices require direct cloud connectivity. In many IoT systems, multiple protocols are used together.

## Conclusion

IoT has applications in various industries, each with different conditions and modes. The IoT system covers hardware and software chains requiring efficient technical solutions. Multiple protocols can be suitable for the same scenario, and there is a complementary effect among them. To achieve IoT device and data connectivity, the key is to establish connectivity between different protocols and unify the upper business application layer protocol.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
