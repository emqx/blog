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

## Bridging OPC UA to MQTT via Neuron

[Neuron](https://www.emqx.com/en/products/neuron) is a modern industrial IoT connectivity server that can connect to a wide range of industrial devices using standard or device-proprietary protocols, enabling the interconnection of industrial IoT platforms with massive devices. As a lightweight industrial protocol gateway software, Neuron is designed to operate on various IoT edge hardware devices with limited resources. Its primary goal is to address the challenge of accessing data from data-centric automation equipment in a unified manner, thus offering essential support for smart manufacturing.

[EMQX](https://www.emqx.io/) is a distributed open-source MQTT broker. As the world's most scalable MQTT messaging server, EMQX provides efficient and reliable connectivity to a massive number of IoT devices, enabling high-performance, real-time movement and processing of messages and event streams, helping users rapidly build business-critical IoT platforms and applications.

OPC UA data sources can be captured and aggregated by Neuron's southbound OPC UA driver, converted to the MQTT protocol, and transmitted to the EMQX MQTT Broker. The latter then distributes them to various distributed applications.

In this blog, we will offer a bridging solution from OPC UA to MQTT with Neuron and EMQX. We will demonstrate using Neuron to collect data from the Prosys OPC UA Simulation Server, upload the collected data to the locally-built EMQX MQTT Broker (mqtt://192.168.10.174:1883), and finally view the changes in the data using the MQTTX subscription topic.

![Bridging OPC UA to MQTT](https://assets.emqx.com/images/0d6aba325262607e1d188703b4e446a3.png)

| **Application**                 | **IP address** | **port** |
| :------------------------------ | :------------- | :------- |
| Prosys OPC UA Simulation Server | 192.168.10.174 | 53530    |
| Neuron                          | 192.168.10.174 | 7000     |
| EMQX                            | 192.168.10.174 | 1883     |
| MQTT X                          |                |          |

### Installing the OPC UA Simulator

The installation package can be downloaded from the [Prosys OPC website](https://www.prosysopc.com/products/opc-ua-simulation-server/). After installation, run Prosys OPC UA Simulation. Make sure that the Neuron is running on the same LAN as the simulator.

Click **Objects->Objects::FolderType->Simulation::FolderType** to view the data and select Counter::BaseDataVariableType.

![Select Counter::BaseDataVariableType](https://assets.emqx.com/images/5a4d4723a45d66d48327d45be58fd1e1.png)

### EMQX Startup

Execute the following commands to install and run the EMQX container. For more information on how to install the EMQX container, you can visit the [Installation Guide](https://www.emqx.io/docs/zh/v5.0/deploy/install.html).

```
docker pull emqx/emqx:5.1.0
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083
```

### Neuron Setting

Neuron offers a variety of installation methods, which you can view in detail in [Installation](https://neugates.io/docs/zh/latest/installation/installation.html). This example uses a containerized deployment so that you can start experiencing Neuron as soon as possible. Execute the following commands to install and run the Neuron container.

```
$ docker pull emqx/neuron:latest
$ docker run -d --name neuron -p 7000:7000 --privileged=true --restart=always emqx/neuron:latest
```

Open a web browser, and enter the address and port number of the gateway where you are running Neuron to get to the management console page. The default port number is 7000. Go to `http://localhost:7000/` (localhost can be replaced with your actual IP address) through your browser.

#### Step 1: Login

After the page opens, it goes to the login interface, where you can log in with the initial user name and password (initial user name: admin, initial password: 0000).

#### Step 2: Add Southbound Device

Select Southbound Devices in the **Configuration** menu to enter the **South Devices** screen and click **Add Device** to add a new device.

- Name: fill in the device name, for example opcua-195-prosys;
- Plug-in: drop-down box to select the OPC UA plug-in.

#### Step 3: Set the Southbound Device Parameters

Automatically enter the device configuration interface after adding a southbound device, fill in the parameters and submit.

- Endpoint URL: Fill in the connection address of OPC UA Simulation Server, such as: opc.tcp://192.168.10.174:53530/OPCUA/SimulationServer;
- Username: default no need to fill in;
- Password: Not required by default;
- Cert: No need to upload by default;
- Key: No need to upload by default.

Ensure that the Prosys OPC UA Simulation Server has been switched to Expert Mode (**Option->Switch to Expert Mode**). Click **Certificates** to set NeuronClient@localhost in the list on the left to Trusted.

![Click **Certificates**](https://assets.emqx.com/images/18303ffbc9c775f0cbcb30243db9a401.png)

#### Step 4: Create a Group in the Device Card

Click any blank space of the device node card to enter the group list management interface, and click Create to bring up the dialogue box for creating a group. Fill in the parameters and submit:

- Group name: Fill in the group name, for example, group-1;
- Interval: default 1000.

#### Step 5: Add Data Point Locations to the Group

Enter the point list management interface, click **Create**, fill in the point parameters and submit:

- Name: Fill in the name of the point, for example, Counter;
- Attribute: Drop down to select point properties, e.g. Read, Write;
- Type: Drop down to select the data type, for example, INT32;
- Address: Fill in the drive address, e.g., 3!1001. 
  - 3 represents the Namespace of the data point in the OPC UA simulator.
  - 1001 represents the Node ID of the data tag;
- Description,  Decimal, and Precision are not filled in.

#### Step 6: View Collected Data in Data Monitoring

Select **Monitoring→Data Monitoring** to enter the Data Monitor interface and view the values read from the created points.

![Neuron Dashboard](https://assets.emqx.com/images/92c58c6e1017480fafc38d54ca254088.png)

#### Step 7: Add a Northbound Plug-in Module to the Application

Select **North Apps** in the Configuration menu and click **Add Application**.

- Name: Fill in the application name, for example, MQTT;
- Plugin: drop-down box to select the MQTT plugin.

#### Step 8: Set the North Application Parameters

- Client ID: Note that this ID should be independent of each other. Duplicate IDs will cause the client to be kicked. For example, set to MQTT1999;
- QoS Level: Default is 0;
- Reporting data format: Default is Values-format;
- Write request subject: Defaults to /neuron/MQTT/write/req;
- Write response subject: Defaults to /neuron/MQTT/write/resp;
- Offline Cache: Off by default;
- Server Address: Fill in the address of the locally installed EMQX MQTT Broker at 192.168.10.174, which is your actual IP address;
- Server Port: Default 1883;
- User name, password: Not filled;
- SSL: Disabled by default.

#### Step 9: Subscribe to the South Tag Group

Go to the list of subscription groups and click **Add Subscription**.

- South Device: Drop-down box to select a created southbound device. For example, opcua-195-prosys;
- Group: Drop-down box to select the group to subscribe to, e.g., group-1;
- Topic: The MQTT topic, which in this case defaults to /neuron/MQTT/group-1. Next, subscribe to this topic in MQTTX and receive messages.

### View the Data Using MQTTX

You can go to the [MQTTX official website](https://mqttx.app/) to download MQTTX and install it. After installation, start MQTTX and add connection, set Host to `mqtt:://192.168.10.174`, Port to `1883`, subscribe to the topic `/neuron/MQTT/group-1`, and then you can receive the data transferred from OPC UA.

![MQTTX](https://assets.emqx.com/images/f72e055d59d5728b079df244ebdb6f0f.png)

## Summary

The OPC UA protocol enables communication and data exchange between devices, while MQTT provides an efficient, flexible and secure messaging mechanism. By leveraging the strengths of both protocols, this integration allows seamless transmission of device data to the cloud, facilitating remote monitoring and control with efficiency and security. The ability to harness real-time insights from equipment and processes empowers businesses to optimize operations, boost productivity, and ensure the highest levels of quality. Embracing this innovative approach not only enhances the overall efficiency of industrial systems but also paves the way for smarter, data-driven decision-making, driving industries towards a more connected and prosperous future.



<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
