## Modbus Introduction

[Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) is a serial communication protocol used to connect industrial automation devices. Originally developed by Modicon in 1979, it has evolved into one of the universal communication standards widely used in industrial automation scenarios.

Modbus adopts a master-slave mode and supports multiple transmission modes, including serial (RS-232/485) and Ethernet versions (TCP/IP). It is mainly used for monitoring and controlling automation equipment such as sensors, motors, and PLCs. It facilitates data exchange between devices and enables the transmission of control commands, allowing different devices to coordinate with each other.

The Modbus protocol defines four types of storage areas: Coils, Discrete Inputs, Input Registers, and Holding Registers. Different types of storage areas correspond to different read-write operations.

| **Storage Area Name** | **Data Type** | **Access Type** | **PLC Address** | **Register Address** |
| :-------------------- | :------------ | :-------------- | :-------------- | :------------------- |
| Coils                 | Bit           | Read/Write      | 000001-065536   | 0-65535              |
| Discrete Inputs       | Bit           | Read Only       | 100001-165536   | 0-65535              |
| Input Registers       | Word          | Read Only       | 300001-365536   | 0-65535              |
| Holding Registers     | Word          | Read/Write      | 400001-465536   | 0-65535              |

Each storage area has its own address range and read/write operation code. It is important to choose the appropriate storage area for reading and writing operations according to the application scenario.

Taking Modbus TCP as an example, its message structure includes MBAP(Modbus Application Protocol Header)+PDU(Protocol Data Unit).

![MBAP+PDU](https://assets.emqx.com/images/c6c3b139b43fb435e0fdf258f8972073.png)

The Modbus protocol defines multiple function codes for accessing and manipulating memory areas. Below are some commonly used function codes.

| **Function Code** | **Function**             | **Operation Type** | **Number of Operations** |
| :---------------- | :----------------------- | :----------------- | :----------------------- |
| 01                | Read Coil                | Bit Operation      | Single or Multiple       |
| 02                | Read Discrete Inputs     | Bit Operation      | Single or Multiple       |
| 03                | Read Holding Registers   | Word Operation     | Single or Multiple       |
| 04                | Read Input Registers     | Word Operation     | Single or Multiple       |
| 05                | Write Single Coil        | Bit Operation      | Single                   |
| 06                | Write Single Register    | Word Operation     | Single                   |
| 15                | Write Multiple Coils     | Bit Operation      | Multiple                 |
| 16                | Write Multiple Registers | Word Operation     | Multiple                 |

Assuming the slave ID is 01H and the starting address of the holding register to be read is 006BH, and 2 registers are to be read, the instruction is as follows:

| **Slave ID** | **Function Code** | **Starting Address(High Byte)** | **Starting Address(Low Byte)** | **Number of Registers(High Byte)** | **Number of Registers(Low Byte)** |
| :----------- | :---------------- | :------------------------------ | :----------------------------- | :--------------------------------- | :-------------------------------- |
| 01           | 03                | 00                              | 6B                             | 00                                 | 02                                |

Each holding register has a length of 2 bytes. The low-addressed registers are transmitted first, followed by the high-addressed registers. For each register, the high byte is transmitted first, followed by the low byte. The response is as follows:

| **Slave ID** | **Function Code** | **Number of Bytes** | **006BH(High Byte)** | **006BH(Low Byte)** | **006CH(High Byte)** | **006CH(Low Byte)** |
| :----------- | :---------------- | :------------------ | :------------------- | :------------------ | :------------------- | :------------------ |
| 01           | 03                | 04                  | 00                   | 00                  | 00                   | 00                  |

## Why Bridge Modbus to MQTT?

With the advent of Industry 4.0, there is an increasing demand for intelligence, automation and digitization in manufacturing. In this context, the Modbus protocol faces some challenges:

- Firstly, the Modbus protocol has significant security issues. Its straightforward communication method renders it susceptible to security risks, including hacking attacks and data tampering.
- Secondly, when it comes to real-time performance and bandwidth utilization, the Modbus protocol falls short in comparison to modern industrial communication standards. Especially in the case of large-scale device networking, traditional serial communication methods are no longer sufficient to meet requirements.
- In addition, in terms of multi-level architecture and cloud platform applications, the Modbus protocol also has certain limitations. It can only perform point-to-point communication and does not support distributed systems and cloud computing platforms very well.

Compared with Modbus protocol, the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) has obvious advantages. The MQTT  protocol is a lightweight message transmission protocol based on [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) that is built on TCP/IP protocol. It was released by IBM in 1999 and became an officially approved communication standard by OASIS in 2014. Currently it has been widely applied in areas such as Internet of Things (IoT), mobile internet, smart hardware, connected cars, smart cities, remote healthcare services, power industry, oil and energy.

Here are some of the advantages of MQTT.

- **Lightweight**: MQTT is very lightweight and can be used in environments with limited bandwidth and poor network quality.
- **Flexibility**: MQTT supports multiple connection methods and enables flexible message transmission through the subscribe/publish model.
- **Reliability**: MQTT ensures reliable message transmission, even in case of network interruption, by allowing reconnection and communication restoration.
- **Security**: MQTT supports SSL/TLS encryption and authentication mechanisms to ensure data security.

Therefore, in the field of IoT, MQTT is more suitable for message transmission in distributed systems.

## The Architecture of Modbus to MQTT Bridging

The Modbus to MQTT bridging architecture consists of two main components: the Modbus data source and the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). The data source sends Modbus data to the MQTT broker, which then receives and forwards it. To achieve this process, two essential elements are required: an edge device responsible for converting the Modbus protocol into MQTT and transmitting the data to the MQTT broker, and an MQTT broker that handles MQTT messages.

In this article, we use [Neuron](https://neugates.io/) and [EMQX](https://github.com/emqx/emqx) to implement the bridging process.

[Neuron](https://neugates.io/) is a modern [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) connectivity server that can connect various industrial devices using standard or proprietary protocols, achieving interconnectivity between industrial IoT platforms and devices. As a lightweight industrial software, Neuron can run on various IoT edge hardware devices with limited resources. It aims to solve the problem of difficult unified access to automation equipment data centered around data and provide basic support for intelligent manufacturing.

[EMQX](https://github.com/emqx/emqx) is the world’s leading open-source distributed IoT MQTT broker with high performance and scalability. EMQX provides efficient and reliable connections for massive IoT devices, enabling high-performance real-time movement and processing of the message and event flow data, helping users quickly build IoT platforms and applications for critical business.

The following diagram shows how Neuron collects data from the edge and converts it into MQTT for uploading to EMQX.

![Modbus to MQTT Bridging](https://assets.emqx.com/images/a3fd80ef14d7cf067facaf3aceb8aec1.png)

## Bridging Modbus to MQTT via Neuron

This section will introduce how to use Neuron to collect data from Modbus devices, upload the collected data to EMQX, and view it using MQTTX.

### EMQX Quick Start

EMQX provides multiple installation methods, and users can check the detailed installation methods in the [documentation](https://docs.emqx.com/en/emqx/v5.0/deploy/install.html). This example uses container deployment to quickly experience EMQX.

Run the following command to obtain the Docker image: 

```
docker pull emqx/emqx:5.1.0
```

Run the following command to start the Docker container:

```
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

Access the EMQX Dashboard by visiting `http://localhost:18083/` (replace “localhost” with your actual IP address) through a web browser. This allows you to manage device connections and monitor related metrics. Keep the Docker container running for this tutorial. If interested, refer to the [documentation](https://docs.emqx.com/en/emqx/v5.0/) to experience more features in the Dashboard.

Initial username: `admin`, initial password: `public`

### Install Modbus Simulator

Install PeakHMI Slave Simulators. The installation package can be downloaded from the [PeakHMI official website](https://hmisys.com/).

After installation, run Modbus TCP slave EX. Make sure that Neuron and the simulator are running on the same local network.

Click **Windows->Register** data to view data.

Select station number 1.

![Select station number 1](https://assets.emqx.com/images/5813452d2a089039028b6eeeb2ce38da.png)

Select **Holding Registers**. You have successfully launched the simulator, keep the simulator open and proceed to operate Neuron.

![Select Holding Registers](https://assets.emqx.com/images/44edb1ad9b0a52f44891c4262f2a65ad.png)

### Neuron Quick Start

Neuron provides various installation methods, and users can view detailed installation methods in the [documentation](https://neugates.io/docs/en/latest/installation/installation.html). This example uses containerized deployment.

Obtaining Docker images:

```
$ docker pull emqx/neuron:latest
```

Starting the Docker container:

```
$ docker run -d --name neuron -p 7000:7000 --privileged=true --restart=always emqx/neuron:latest
```

Open a web browser and enter the gateway address and port number to run Neuron. This will take you to the management console page, with the default port number being 7000. You can access it through your browser at `http://localhost:7000/` (replace "localhost" with your actual IP address).

#### Step 1: Log in

Log in with the initial username and password:

- Username: `admin`
- Password: `0000`

#### Step 2: Add a Southbound Device

In the **configuration** menu, select **South Devices** to enter the South Devices interface. Click **Add Device** to add a new device.

- Name: fill in the name of the device, such as "modbus-tcp-1";
- Plugin: select the plugin **Modbus TCP** from the drop-down box.

#### Step 3: Set parameters for southbound devices

After adding a southbound device, it automatically enters the device configuration interface, where you can fill in the parameters and submit them.

- Transport Mode: select TCP;
- Connection Mode: select Client;
- Maximum Retry Times: 0;
- Retry Interval: 0;
- Send Interval: 20;
- IP Address: Enter the IP address of the PC where PeakHMI Slave Simulators software is installed;
- Port: 502;
- Connection Timeout: 3000.

#### Step 4: Create a group in the device card

Click on any blank space on the device node card to enter the group list management interface, click **Create** to bring up the dialog box for creating a group. Fill in the parameters and submit:

- Group Name: Fill in the group name, such as "group-1";
- Interval: 1000.

#### Step 5: Add tags to the group.

Click on any blank space of the group card, enter the point list management interface, and click **Create** to enter the page for adding data points.

![Add tags to the group](https://assets.emqx.com/images/85ba37601b0ff0205caa5e8b15022756.png)

Fill in the parameters of the data point and submit it：

- Name: Fill in the location name, such as tag-1;
- Attribute: Select the location attribute from the dropdown menu, such as Read, Write;
- Type: Select the data type from the dropdown menu, such as INT16;
- Address: Fill in the driver address, for example, 1!40001. 1 represents the station number of the location set in Modbus simulator and 40001 represents the register address of the location.
- Description, Decimal, Precision: not filled.

#### Step 6: View collected data in data monitoring.

Select **Monitoring → Data Monitoring** from the left navigation menu. View the values read by the created data points, as shown in the following figure.

![Monitoring → Data Monitoring](https://assets.emqx.com/images/b9a0cbfaf657f2a880797b9575fea77c.png)

> Note: Please confirm that the Modbus simulator has been started.

The data monitoring displays values in groups：

- South Device: Select the southbound device you want to view from the drop-down menu, for example, the created modbus-tcp-1;
- Group Name: Select the group you want to view under the selected southbound device from the drop-down menu, for example, the created group-1;
- After selecting, the page will display all values of points read in the selected group.

#### Step 7: Add northbound plugin modules to the application.

By creating a northbound application, Neuron establishes a connection with the northbound application and uploads collected device data to EMQX.

Select the **North Apps** in the **Configuration** menu, click **Add Application**, as shown in the figure below.

![Add Application](https://assets.emqx.com/images/d91c1d8910617f57ad2f66890028e883.png)

Add an MQTT cloud connection module:

- Name: Fill in the application name, for example, MQTT;
- Plugin: Select the MQTT plugin from the drop-down.

#### Step 8: Configure northbound application parameters.

After adding the northbound application, it will automatically enter the application configuration interface to fill in the parameters and submit.

Set up MQTT connection:

- Client ID: Note that this ID should be independent of each other(Duplicate IDs will cause the client to be kicked). For example, set to MQTT1999;
- QoS Level: Default to 0;
- Upload Format: Default to Values-format;
- Write Request Topic: Default to /neuron/MQTT/write/req;
- Write Response Topic: Default to /neuron/MQTT/write/resp;
- Offline Data Caching: Default to off;
- Broker Host: Fill in the address of the created emqx broker, which is usually localhost, i.e. your actual IP address.
- Broker Port: Default to 1883;
- Username, Password: Not required;
- SSL: Default to off.

#### Step 9: Subscribe to the Southbound Point Group

Click on any blank space of the newly created MQTT application node card to enter the subscription group interface, and click "Add Subscription".

Subscribe to the data group of southbound devices:

- South device: Select the created southbound device from the dropdown list, for example, modbus-tcp-1;
- Group: Select the group to be subscribed to from the dropdown list, for example, group-1；
- Topic: The MQTT topic, which is default set as /neuron/MQTT/group-1 in this example. Next, subscribe to this topic and receive messages in MQTTX.

#### Step 10: View data on MQTT client.

After subscribing, you can use an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) to connect to EMQX and view the reported data. Here we use [MQTTX](https://mqttx.app/), a powerful cross-platform MQTT client tool, which can be downloaded from the [official website](https://mqttx.app/).

Once MQTTX is launched, click **+ New Connection** on the main page, fill in the configuration parameters, and click **Connect** in the upper right corner.

- Name: Naming messages facilitates viewing, for example naming them modbus-tcp.
- Client ID: Using the default value is ok, ensure that the ID is independent;
- Host: Select **ws://** and fill in `emqx@localhost`(replace "localhost" with your actual IP address).
- Port: 8083.

Optional parameters can be filled in, and then click the **Connect** button on the upper right corner after completion. After a successful connection, subscribe to the topic.

- Click **Add Subscription**, and the topic should be the same as the one in step 9. For example, fill in `/neuron/MQTT/group-1`;

After a successful subscription, you can see that MQTTX continues to receive data collected and reported by Neuron. As shown in the following figure.

![MQTTX](https://assets.emqx.com/images/8a2466ce32d54abdbf2275f80496d844.png)

## IIoT Use Cases

### Implementing Oil Production Data Acquisition

As the scale of digital construction in oil production expands, the number of automated equipment is increasing, resulting in the complexity of data acquisition and management. 

By building an open equipment data network, an oil production plant data center can connect directly with different data acquisition devices, such as RTUs, DTUs and PLCs. With industrial protocol gateway software like Neuron, Modbus/TCP and vendor-specific protocols can be converted into MQTT data, a standard IoT protocol that can be collected, processed, and reported in real-time. This facilitates the storage and data consumption of the upper business system.

![Oil Production Data Acquisition](https://assets.emqx.com/images/5c5a23f0474e9305c1f4d0026176f01b.png)

An overall solution combining Neuron and other EMQ products like [EMQX](https://github.com/emqx/emqx), [eKuiper](https://ekuiper.org/) and EMQX ECP can bring the following benefits to oil industry:

- A system architecture that is light on the frontend and heavy on the backend, reducing field equipment and system operation and maintenance costs.
- Improved business system responsiveness through real-time reporting of production data by using the MQTT IoT protocol as the main method of data collection and transmission.
- Aggregation of massive amounts of real-time data from heterogeneous equipment and systems, including storage of various types of production and monitoring equipment.
- The decoupling of data collection and data consumption systems through a unified access middleware platform and rich data interfaces, making application development easier and more efficient.

### Empowering Industrial Networking, Digitization, and Intelligence

An unified one-stop Industrial IoT data platform becomes essential in the context of Industry 4.0.

Neuron supports Modbus, OPC-UA, IEC61850, IEC104, and other complete industrial protocols to realize efficient access to data of heterogeneous industrial equipment. The data collected in real-time is captured, filtered, complemented, and time-windowed calculated at the edge by eKuiper, a lightweight edge streaming processing engine, to provide a high-quality data source for edge AI inference services. 

By enabling real-time data connectivity, movement, storage, processing, and analysis at the cloud side, this facilitates a robust data foundation for big data analysis and artificial intelligence applications, empowering enterprises to rapidly develop upper-layer applications.

![One-stop Industrial IoT data platform](https://assets.emqx.com/images/0f6feb3a273b6adc9dc7e0061e8e0bb1.png)

## Summary

Using the Modbus protocol enables communication and data exchange between devices, while MQTT provides an efficient, flexible, and secure message transmission mechanism. By converting Modbus RTU or TCP to MQTT messages, device data can be easily sent to the cloud for remote control and monitoring when needed. This approach can help industrial enterprises better manage their equipment and production processes, improving productivity and quality.


<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
