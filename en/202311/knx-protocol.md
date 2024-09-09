## What is KNX Protocol

[KNX](https://www.knx.org/knx-en/for-professionals/What-is-KNX/A-brief-introduction/) is a standard for building automation and home control systems that originated as EIB (European Installation Bus) in the early 1990s. It is an open protocol that enables communication between various devices and systems used in buildings, such as lighting, heating, ventilation, security, and audiovisual equipment. The technology is governed by the [KNX Association](https://www.knx.org/knx-en/for-professionals/index.php), which oversees the development, certification, and promotion of KNX products and solutions worldwide.

KNX operates on various transmission media, including twisted pair wiring, powerline communication, radio frequency, and IP/Ethernet. This flexibility allows for both wired and wireless installations, making KNX suitable for new buildings as well as retrofitting existing ones.

## Bus System of KNX Protocol

KNX uses a bus communication system, where devices are connected to a common bus and can exchange information and commands. Due to its decentralized structure, the KNX bus system can be modified and expanded precisely according to requirements. The smallest KNX application is a system that connects two bus devices: a sensor and an actuator. This basic system can later be upgraded to add as many devices as needed to perform the required control tasks. In theory, a KNX system can consist of over 50,000 devices. When expanding a KNX system, specific topological structures need to be followed.

![KNX Bus System](https://assets.emqx.com/images/c27cefdc4b8b0c6321bcd0c0803046c8.png)

<center>KNX Bus System</center>

## KNX Protocol Devices

KNX devices encompass a wide range of products designed for home and building automation. Here are some common types of KNX devices:

- KNX power supply provides electrical power to the KNX bus
- KNX Actuators: Actuators control electrical loads such as lighting, heating, ventilation, and air conditioning (HVAC) systems.
- KNX Sensors: Sensors detect and measure environmental parameters; examples include temperature sensors, humidity sensors, occupancy sensors, light sensors, and motion detectors.
- A KNX line coupler, or KNX area coupler, is a device used in KNX installations to connect and bridge multiple KNX lines or areas together. It facilitates communication between different segments of a KNX installation, allowing devices and systems on separate KNX lines to exchange data and interact with each other.

## KNX Protocol Topology

Topology refers to the physical layout or arrangement of the KNX bus system. It describes how devices are connected and the overall structure of the installation.

A line refers to a physical segment of the KNX bus system. It represents a section of devices that are connected together using a single bus cable. A line includes a KNX power supply, and usually no more than 64 other bus devices. The power supply and twisted pair line (bus cable) perform two functions: they supply the bus devices with the power they need, and permit the exchange of information between those devices. Line Repeaters can be used to extend a line if more than 64 devices are needed.

![KNX TP Line](https://assets.emqx.com/images/8e6e4b3665292be06f2afe5f53540232.png)

<center>KNX TP Line</center>

<br>

Another way of expanding the installation is to create new lines using Line Couplers. Up to 15 lines can be operated via Line Couplers on the main line to form an area. An area in KNX represents a logical grouping or subdivision of a KNX installation. It refers to a collection of lines or segments that are interconnected within a specific area or functional zone. An area can correspond to a specific area of a building, such as a room or a department.

![KNX TP Area](https://assets.emqx.com/images/fbbe49f400dd1a850e1a53a5ab8f190b.png)

<center>KNX TP Area</center>

<br>

Up to 15 areas can be added to an area line via Area Couplers, to form a complete system.

![image.png](https://assets.emqx.com/images/82413a653c9aaf96a857712c1243f1df.png)

## KNX Protocol Address

In KNX, each device on the KNX bus is assigned a unique address to identify and communicate with it.

### Individual Address

The [individual address](https://support.knx.org/hc/en-us/articles/115003185789-Individual-Address) is a unique address assigned to each KNX device on the bus. It allows direct communication between the KNX system and the specific device. The individual address is typically set during the device configuration or programming process and remains fixed for the device.

KNX individual addresses are 16-bit values consisting of three parts: area number, line number and device address.

For example, a group address of 2.3.20 represents bus device 20 in the third line of the second area.

### Group Address

The [group address](https://support.knx.org/hc/en-us/articles/115003188109-Group-Addresses) is used for communication between multiple KNX devices. It represents a specific function or control point within the KNX system. Devices can be programmed to listen to and respond to specific group addresses, enabling group-based control and automation.

A group address consists of three main components: main group, middle group, and sub-group.

For example, a group address of 1/2/3 represents main group 1, middle group 2, and sub-group 3. The specific interpretation of these components may vary depending on the application and configuration.

## KNXnet/IP Protocol

KNXnet/IP is a communication protocol used in the KNX system for transmitting data over IP networks. It enables the integration of KNX devices and systems with IP-based networks, such as Ethernet or the Internet.

With KNXnet/IP, KNX devices can communicate with each other and with external systems through IP networks. It allows for remote access, control, and monitoring of KNX installations from anywhere with network connectivity. This protocol enables the use of standard IP networking infrastructure and protocols for KNX, expanding the capabilities and reach of the system.

It's worth noting that KNXnet/IP is just one of the communication options within the KNX standard. Traditional KNX bus communication methods are still widely used, and KNXnet/IP is often used in combination with these methods to provide a comprehensive and flexible solution for building automation and control.

![KNXnet/IP Telegram](https://assets.emqx.com/images/0ab8827a355db6d084745050b44c2697.png)

<center>KNXnet/IP Telegram</center>

## Tools for KNX Protocol

### ETS

[ETS (Engineering Tool Software)](https://www.ets6.org/) is the official software tool used for the configuration, programming, and commissioning of KNX-based systems. It is a comprehensive software application developed by the KNX Association, the organization responsible for the KNX standard.

ETS provides a user-friendly interface that allows system integrators, installers, and designers to create, configure, and manage KNX installations. It enables the configuration of individual KNX devices, the creation of group addresses, the assignment of functions and parameters, and the setup of automation and control logic.

### KNX Virtual

[KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php) is a Windows-based application provided by KNX Association that allows users to simulate a KNX installation. The main purpose of KNX Virtual is to provide a learning and training platform for individuals who want to gain hands-on experience with KNX technology before starting their first real project. It allows users to learn the basics of KNX and build confidence in working with the system.

KNX Virtual includes over 10 different types of virtual KNX devices that are connected to a simulated KNX bus. These devices represent various building loads such as lamps, dimmable lamps, blinds, heating and cooling valves. Users can also experiment with more advanced building features like weather modules, alarms, scenes, and logic operations.

## Integrating KNX Protocol with MQTT for IoT: Neuron and EMQX

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a messaging protocol designed for IoT devices and applications operating on a publish/subscribe model. It's lightweight, efficient, reliable, and allows for real-time communication. MQTT is well-suited for environments with limited resources, where efficient use of power and bandwidth is necessary. Currently, it has been widely applied in areas such as the Internet of Things (IoT), mobile Internet, smart hardware, connected cars, smart cities, remote healthcare services, oil and energy.

With the advent of Industry 4.0, there is an increasing demand for intelligence, automation and digitization in manufacturing. In this context, MQTT protocol has a wide range of device and platform support, with numerous IoT devices and systems readily available in the market. In comparison, the device ecosystem for KNX may be more limited, especially when it comes to specialized IoT devices or accessories. Combining KNX with MQTT can open up more opportunities for IoT scenarios like smart home and building automation.

### Neuron for Converting KNX into MQTT

[Neuron](https://github.com/emqx/neuron) is an industry IoT gateway software that enables industrial devices with essential IoT connectivity capabilities. With minimal resource utilization, Neuron can communicate with diverse industrial devices through standard or dedicated protocols, realizing the multiple device connections to the [Industrial IoT platform](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions). From the very beginning, Neuron has supported MQTT as one of its communication protocols. The Neuron [MQTT plugin](https://docs.emqx.com/en/neuron/latest/configuration/north-apps/mqtt/overview.html) allows users to quickly build IoT applications that use MQTT communication between devices and the cloud.

Since version 2.1.0, Neuron provides the [KNX plugin](https://docs.emqx.com/en/neuron/latest/configuration/south-devices/knxnet-ip/knxnet-ip.html) which supports communication with KNX IP couplers using the KNXnet/IP protocol over UDP.

### EMQX for Handling MQTT Messages

[EMQX](https://github.com/emqx/emqx) is the world’s leading open-source distributed MQTT broker with high performance and scalability. It provides efficient and reliable connections for massive IoT devices, enabling high-performance real-time movement and processing of the message and event flow data, helping users quickly build IoT platforms and applications for critical business.

EMQX is the broker component in the bridging architecture, while Neuron collects data from KNX devices and transmits the data in MQTT messages to the broker. After receiving the MQTT messages from Neuron, EMQX will then forward the data or perform further processing.

EMQX has a rich and powerful feature set, such as the SQL-based [rules engine](https://www.emqx.com/en/solutions/mqtt-data-processing) to extract, filter, enrich, and transform IoT data in real-time, and data integration to connect EMQX to external data systems like databases.

Learn more about integrating KNX protocol with IoT through this step-by-step tutorial: [Bridging KNX Data to MQTT: Introduction and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-knx-data-to-mqtt-introduction-and-hands-on-tutorial) 



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
