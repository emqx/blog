## Introduction to KNX

[KNX](https://www.knx.org/knx-en/for-professionals/What-is-KNX/A-brief-introduction/) is a standard for building automation and home control systems that originated as EIB (European Installation Bus) in the early 1990s. It is an open protocol that enables communication between various devices and systems used in buildings, such as lighting, heating, ventilation, security, and audiovisual equipment. The technology is governed by the [KNX Association](https://www.knx.org/knx-en/for-professionals/index.php), which oversees the development, certification, and promotion of KNX products and solutions worldwide.

KNX operates on various transmission media, including twisted pair wiring, powerline communication, radio frequency, and IP/Ethernet. This flexibility allows for both wired and wireless installations, making KNX suitable for new buildings as well as retrofitting existing ones.

### KNX Bus System

KNX uses a bus communication system, where devices are connected to a common bus and can exchange information and commands. Due to its decentralized structure, the KNX bus system can be modified and expanded precisely according to requirements. The smallest KNX application is a system that connects two bus devices: a sensor and an actuator. This basic system can later be upgraded to add as many devices as needed to perform the required control tasks. In theory, a KNX system can consist of over 50,000 devices. When expanding a KNX system, specific topological structures need to be followed.

![KNX Bus System](https://assets.emqx.com/images/c27cefdc4b8b0c6321bcd0c0803046c8.png)

<center>KNX Bus System</center>

### KNX Devices

KNX devices encompass a wide range of products designed for home and building automation. Here are some common types of KNX devices:

- KNX power supply provides electrical power to the KNX bus
- KNX Actuators: Actuators control electrical loads such as lighting, heating, ventilation, and air conditioning (HVAC) systems. 
- KNX Sensors: Sensors detect and measure environmental parameters; examples include temperature sensors, humidity sensors, occupancy sensors, light sensors, and motion detectors.
- A KNX line coupler, or KNX area coupler, is a device used in KNX installations to connect and bridge multiple KNX lines or areas together. It facilitates communication between different segments of a KNX installation, allowing devices and systems on separate KNX lines to exchange data and interact with each other.

### KNX Topology

Topology refers to the physical layout or arrangement of the KNX bus system. It describes how devices are connected and the overall structure of the installation.

A line refers to a physical segment of the KNX bus system. It represents a section of devices that are connected together using a single bus cable. A line includes a KNX power supply, and usually no more than 64 other bus devices. The power supply and twisted pair line (bus cable) perform two functions: they supply the bus devices with the power they need, and permit the exchange of information between those devices. Line Repeaters can be used to extend a line if more than 64 devices are needed.

![KNX TP Line](https://assets.emqx.com/images/8e6e4b3665292be06f2afe5f53540232.png)

<center>KNX TP Line</center>

Another way of expanding the installation is to create new lines using Line Couplers. Up to 15 lines can be operated via Line Couplers on the main line to form an area. An area in KNX represents a logical grouping or subdivision of a KNX installation. It refers to a collection of lines or segments that are interconnected within a specific area or functional zone. An area can correspond to a specific area of a building, such as a room or a department.

![KNX TP Area](https://assets.emqx.com/images/fbbe49f400dd1a850e1a53a5ab8f190b.png)

<center>KNX TP Area</center>

Up to 15 areas can be added to an area line via Area Couplers, to form a complete system.

![image.png](https://assets.emqx.com/images/82413a653c9aaf96a857712c1243f1df.png)

### KNX Address

In KNX, each device on the KNX bus is assigned a unique address to identify and communicate with it. 

#### Individual Address

The [individual address](https://support.knx.org/hc/en-us/articles/115003185789-Individual-Address) is a unique address assigned to each KNX device on the bus. It allows direct communication between the KNX system and the specific device. The individual address is typically set during the device configuration or programming process and remains fixed for the device.

KNX individual addresses are 16-bit values consisting of three parts: area number, line number and device address.

For example, a group address of 2.3.20 represents bus device 20 in the third line of the second area.

#### Group Address

The [group address](https://support.knx.org/hc/en-us/articles/115003188109-Group-Addresses) is used for communication between multiple KNX devices. It represents a specific function or control point within the KNX system. Devices can be programmed to listen to and respond to specific group addresses, enabling group-based control and automation. 

A group address consists of three main components: main group, middle group, and sub-group.

For example, a group address of 1/2/3 represents main group 1, middle group 2, and sub-group 3. The specific interpretation of these components may vary depending on the application and configuration.

### KNXnet/IP

KNXnet/IP is a communication protocol used in the KNX system for transmitting data over IP networks. It enables the integration of KNX devices and systems with IP-based networks, such as Ethernet or the Internet.

With KNXnet/IP, KNX devices can communicate with each other and with external systems through IP networks. It allows for remote access, control, and monitoring of KNX installations from anywhere with network connectivity. This protocol enables the use of standard IP networking infrastructure and protocols for KNX, expanding the capabilities and reach of the system.

It's worth noting that KNXnet/IP is just one of the communication options within the KNX standard. Traditional KNX bus communication methods are still widely used, and KNXnet/IP is often used in combination with these methods to provide a comprehensive and flexible solution for building automation and control.

![KNXnet/IP Telegram](https://assets.emqx.com/images/0ab8827a355db6d084745050b44c2697.png)

<center>KNXnet/IP Telegram</center>

### ETS

[ETS (Engineering Tool Software)](https://www.ets6.org/) is the official software tool used for the configuration, programming, and commissioning of KNX-based systems. It is a comprehensive software application developed by the KNX Association, the organization responsible for the KNX standard.

ETS provides a user-friendly interface that allows system integrators, installers, and designers to create, configure, and manage KNX installations. It enables the configuration of individual KNX devices, the creation of group addresses, the assignment of functions and parameters, and the setup of automation and control logic.

### KNX Virtual

[KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php) is a Windows-based application provided by KNX Association that allows users to simulate a KNX installation. The main purpose of KNX Virtual is to provide a learning and training platform for individuals who want to gain hands-on experience with KNX technology before starting their first real project. It allows users to learn the basics of KNX and build confidence in working with the system.

KNX Virtual includes over 10 different types of virtual KNX devices that are connected to a simulated KNX bus. These devices represent various building loads such as lamps, dimmable lamps, blinds, heating and cooling valves. Users can also experiment with more advanced building features like weather modules, alarms, scenes, and logic operations.

## Why Bridge KNX to MQTT

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a messaging protocol designed for IoT devices and applications operating on a publish/subscribe model. It's lightweight, efficient, reliable, and allows for real-time communication. MQTT is well-suited for environments with limited resources, where efficient use of power and bandwidth is necessary. Currently, it has been widely applied in areas such as the Internet of Things (IoT), mobile Internet, smart hardware, connected cars, smart cities, remote healthcare services, oil and energy.

With the advent of Industry 4.0, there is an increasing demand for intelligence, automation and digitization in manufacturing. In this context, MQTT has a wide range of device and platform support, with numerous IoT devices and systems readily available in the market. In comparison, the device ecosystem for KNX may be more limited, especially when it comes to specialized IoT devices or accessories.

## The Architecture of KNX to MQTT Bridging

![The Architecture of KNX to MQTT Bridging](https://assets.emqx.com/images/94d52d2aba496120411cc0d02bde8ad7.png)

### Neuron for Converting KNX into MQTT

[Neuron](https://neugates.io/) is an industry IoT gateway software that enables industrial devices with essential IoT connectivity capabilities. With minimal resource utilization, Neuron can communicate with diverse industrial devices through standard or dedicated protocols, realizing the multiple device connections to the Industrial IoT platform.

From the very beginning, Neuron has supported MQTT as one of its communication protocols. The Neuron [MQTT plugin](https://neugates.io/docs/en/latest/configuration/north-apps/mqtt/overview.html) allows users to quickly build IoT applications that use MQTT communication between devices and the cloud. 

Since version 2.1.0, Neuron provides the [KNX plugin](https://neugates.io/docs/en/latest/configuration/south-devices/knxnet-ip/knxnet-ip.html) which supports communication with KNX IP couplers using the KNXnet/IP protocol over UDP. 

### EMQX for Handling MQTT Messages

[EMQX](https://www.emqx.io/) is the world’s leading open-source distributed IoT MQTT broker with high performance and scalability. It provides efficient and reliable connections for massive IoT devices, enabling high-performance real-time movement and processing of the message and event flow data, helping users quickly build IoT platforms and applications for critical business.

EMQX is the broker component in the bridging architecture, while Neuron collects data from KNX devices and transmits the data in MQTT messages to the broker. After receiving the MQTT messages from Neuron, EMQX will then forward the data or perform further processing.

EMQX has a rich and powerful feature set, such as the SQL-based [rules engine](https://www.emqx.com/en/solutions/mqtt-data-processing) to extract, filter, enrich, and transform IoT data in real-time, and data integration to connect EMQX to external data systems like databases.

## Bridging KNX to MQTT via Neuron

This section will introduce how to use Neuron to collect data from KNX devices, upload the collected data to EMQX, and view it using MQTTX.

We will use a Linux machine for installing EMQX, MQTTX, and Neuron. As ETS and KNX Virtual only support Windows, we run a Windows VM to simulate KNX installation. 

### EMQX Quick Start

EMQX provides multiple installation methods, and users can check the detailed installation methods in the [documentation](https://www.emqx.io/docs/en/v5.0/deploy/install.html). This example uses container deployment to quickly experience EMQX.

Run the following command to obtain the Docker image:

```
docker pull emqx/emqx:5.1.0
```

Run the following command to start the Docker container:

```
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

Access the EMQX Dashboard by visiting [http://localhost:8083/](http://localhost:18083/) (replace “localhost” with your actual IP address) through a web browser. This allows you to manage device connections and monitor related metrics. Keep the Docker container running for this tutorial. You can refer to the [documentation](https://www.emqx.io/docs/en/v5.0/) to experience more features in the Dashboard.

Initial username: `admin`, initial password: `public`

### Setup KNX Virtual Using ETS

We need to [download and install KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php). There is a [blog tutorial](https://www.ets6.org/ets6-and-knx-virtual/) on how to simulate KNX installation using ETS and KNX Virtual, or if you prefer, a video tutorial [KNX Virtual Basics](https://www.youtube.com/watch?v=01MO_zmtGv4).

To keep things simple, we will simulate a KLiX (D0), a dimming actuator (D0), a blinds/shutter actuator (D2) and a switch actuator (D7) in KNX Virtual. The association between addresses and group objects is shown in the following image.

![KNX Virtual](https://assets.emqx.com/images/6d36e1efa508eca48c39832c7954f57c.png)

### Neuron Quick Start

Consult the [installation instruction](https://neugates.io/docs/en/latest/installation/installation.html) on how to install Neuron. After Neuron is installed, you can access the dashboard through your browser at [http://localhost:7000](http://localhost:7000/) (replace "localhost" with your actual IP address).

#### Step 1. Login

Log in with the initial username and password:

- Username: `admin`
- Password: `0000`

#### Step 2. Add a south device

In the Neuron dashboard, click **Configuration ->  South Devices -> Add Device** to add an *knx* node.

![Add a south device](https://assets.emqx.com/images/769435a4caf26298e8e0cb924de59a20.png)

#### Step 3. Configure the *knx* node

Configure the newly created *knx* node as the following image shows.

![Configure the *knx* node](https://assets.emqx.com/images/8b93dfd897e88acba6d51f129f0426d5.png)


#### Step 4. Create a group in the *knx* node

Click the *knx* node to enter the **Group List** page, and click **Create** to bring up the **Create Group** dialog. Fill in the parameters and submit:

- Group Name: grp.
- Interval: 1000.

![Create a group in the *knx* node](https://assets.emqx.com/images/b3ce997da0687c578dfc8ed850744627.png)

#### Step 5. Add tags to the group

Add four tags corresponding to the dimming actuator, shutter actuator and switch actuator in the KNX Virtual configuration.

![Add tags to the group](https://assets.emqx.com/images/17ecb2eba0fbbe000112872f8833e374.png)

#### Step 6. Data monitoring

In the Neuron dashboard, click **Monitoring -> Data Monitoring**, and see that tag values are read correctly.

![Data monitoring 1](https://assets.emqx.com/images/8f5dd1e3c15a5c4a2f515e6e8c5b2e4f.png)

![Data monitoring 2](https://assets.emqx.com/images/2b09ae4a02367b3c2b8c3221902b6b06.png)

#### Step 7. Add an MQTT North app

In the Neuron dashboard, click **Configuration ->  North Apps -> Add App** to add an *mqtt* node.

![Add an MQTT North app](https://assets.emqx.com/images/6dc854ceedafc6615e71b5fa275c1699.png)

#### Step 8: Configure the *mqtt* node

Configure the *mqtt* node to connect to the EMQX broker set up earlier.

![Configure the *mqtt* node](https://assets.emqx.com/images/c6725171f15e8529492588ae3693af98.png) 

#### Step 9. Subscribe the *mqtt* node to the *knx* node

Click the newly created *mqtt* node to enter the **Group List** page, and click **Add subscription**. After a successful subscription, Neuron will publish data to the topic `/neuron/mqtt/knx/grp`.

![Subscribe the *mqtt* node to the *knx* node](https://assets.emqx.com/images/b673b0c1b5b23f682065d2beab900d6d.png)

### View Data Using MQTTX

Now, you can use an MQTT client to connect to EMQX and view the reported data. Here, we use [MQTTX, a powerful cross-platform MQTT client tool](https://mqttx.app/), which can be downloaded from the [official website](https://www.emqx.com/en/products/mqttx).

Launch MQTTX, and add a new connection to the EMQX broker set up earlier, then add a subscription to the topic  `/neuron/mqtt/knx/grp`. After a successful subscription, you can see that MQTTX continues to receive data collected and reported by Neuron. As shown in the following figure.

![MQTTX](https://assets.emqx.com/images/9beb4e4d3514aff1b659067c42be9084.png)

## Conclusion

In this blog, we introduced the KNX protocol and demonstrated the overall process of bridging KNX data to MQTT using Neuron.

KNX provides a robust and flexible platform for home and building automation. Neuron, with its powerful connectivity for Industrial IoT, facilitates the data collection from KNX devices and seamless transmission of the acquired data to the cloud for convenient remote control and monitoring whenever necessary. 

Neuron also supports other industrial protocols like [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), OPC UA, SIEMENS, and more. For more bridging tutorials, read our post: 

- [Bridging Modbus Data to MQTT for IIoT:  A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-modbus-data-to-mqtt-for-iiot#the-architecture-of-modbus-to-mqtt-bridging) 
- [Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-opc-ua-data-to-mqtt-for-iiot) 
- [Bridging TwinCAT Data to MQTT: Introduction and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-twincat-data-to-mqtt) 
- [Bridging FINS Data to MQTT: Protocol Explained and Hands-on Tutorial](https://www.emqx.com/en/blog/bridging-fins-data-to-mqtt) 



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
