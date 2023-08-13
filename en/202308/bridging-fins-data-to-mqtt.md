## FINS Introduction

Omron FINS (Factory Interface Network Service) is a network communication protocol developed by OMRON for industrial automation control. It enables seamless communication between Ethernet, control network Controller Link, and RS232C/485 serial communication through FINS commands. FINS protocol works on the application layer of the TCP/IP model, which ensures its good expandability, practicality, and real-time performance, thus connecting client applications, including HMI, SCADA, Historian, MES, ERP, and countless custom applications with controllers through Omron FINS Ethernet driver.

The FINS protocol has two variants: the FINS/UDP protocol uses UDP packets for communication, and the FINS/TCP protocol uses TCP connections.

### FINS Session Process

The FINS session process is based on the TCP/IP protocol. The following diagram describes the role of several data frames at the beginning of the FINS session. The session of the FINS protocol has a request frame, and the node parameters of the initiator are attached to the request frame. The Server side(e.g., PLCS) will confirm and return its node parameters to the requester. Only FINS over TCP needs session process.

![FINS Session Process](https://assets.emqx.com/images/0d8af5289a27e88ab5a6f415cb8c3b34.png)

### FINS Frame Structure

The FINS frame structure consists of three parts, namely FIN Header, FINS Command Code, and FINS Command Data.

![FINS Frame Structure](https://assets.emqx.com/images/c7c31b73393dedb48c4cc1be9e0e1464.png)

Both command frames and response frames are comprised of a FINS header for storing transfer control information, a FINS command field for storing a command, and a FINS parameter/data field for storing command parameters and transmission/response data.

![FINS header](https://assets.emqx.com/images/58272c4a564c4b6a36879a61c1270837.png)

The response code (one byte each for MRES and SRES) for the command is added at the beginning of the  FINS parameter/data field in the response frame.

![FINS Response Frame Config](https://assets.emqx.com/images/4ad7fb747e362f0bc2cebf6fcdda12e2.png)

FINS over UDP consists of two parts: FINS Command Code and FINS Command Data.

## FINS Read/Write IO Memory Area

The following table gives the addresses to use when reading or writing PC data.

- The Data area address column gives the normal addresses used in the PC program.

- The Address used in the communications column is the addresses used in CV-mode commands and responses. These addresses are combined with the memory area codes to specify PC memory locations. They are not the same as the actual memory addresses of the data.

- The No. of bytes column specifies the number of bytes to read or write data for that area. The number of bytes varies for the same area depending on the memory area code.

Different PLC CPU models have different memory areas. Take CV500 or CVM1-CPU01-E as an example.

![FINS Read/Write IO Memory Area](https://assets.emqx.com/images/fb21a9091c3f037fb1b3d5d18e65c80e.png)

## FINS Command List

In the illustrations of command and response blocks in this section, each box represents one byte (i.e., two hexadecimal or BCD digits). Be careful when adding the header, where each box represents one digit (i.e., four bits). The following table lists the FINS commands supported by CV-series PCs and the PC operating modes during which they are enabled.

![Command List](https://assets.emqx.com/images/28160d8d452c41d9c73bc7b1a4c411de.png)

**Note** When the PC is in RUN mode, data transfers from files to the program area are not possible, but transfers from the program area to files are possible.

## Why Bridge FINS to MQTT？

With the arrival of the wave of Industry 4.0, there is a growing demand for data intelligence, interconnectivity, and cloud-edge collaboration in the industrial sector. Against this backdrop, the FINS protocol may face some issues.

Firstly, as an intranet application protocol, FINS was not designed with security in mind, and its communication methods are simple, making it vulnerable to hacker attacks and data tampering that could pose a threat to the production environment.

In addition, FINS can only perform one-to-one communication in complex application architectures and cannot effectively support the development of distributed and cloud-native applications.

Compared to FINS, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) has significant advantages. MQTT is a lightweight publish-subscribe message transport protocol commonly used for remote monitoring and communication in IoT applications. It provides a simple and flexible way to transfer messages between devices while effectively handling a large number of concurrent connections. It is currently used in various fields such as IoT, mobile internet, smart hardware, connected vehicles, smart cities, remote medicine, power, oil, and energy.

In the IoT field, MQTT is obviously more suitable for message transmission in distributed systems. Therefore, we can bridge FINS to MQTT to complement each other.

## The Architecture of FINS to MQTT Bridging

In this blog, we use [Neuron](https://www.emqx.com/en/products/neuron) and [EMQX](https://www.emqx.com/en/products/emqx) from EMQ to achieve FINS to MQTT bridging. Neuron can convert the FINS protocol to MQTT, while EMQX acts as an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), handling massive connections and data.

Neuron is a modern industrial IoT connectivity server that can connect various industrial devices that use standard protocols or device-specific protocols, achieving interconnection between industrial IoT platforms and various devices. As a lightweight industrial software, Neuron can run on various IoT edge hardware devices with limited resources. It aims to solve the problem of unified access to data-centric automation devices and provide basic support for intelligent manufacturing.

> Learn more about Neuron: [Neuron: Industrial IoT Connectivity Server](https://www.emqx.com/en/products/neuron)

EMQX is a large-scale and elastic cloud-native distributed IoT MQTT message server. As the most scalable MQTT message server worldwide, EMQX provides efficient and reliable mass connection of IoT devices, capable of high-performance real-time processing of message and event flow data, helping users quickly build critical IoT platforms and applications.

> Learn more about EMQX: [EMQX Enterprise: Enterprise MQTT Platform At Scale](https://www.emqx.com/en/products/emqx)

The following diagram shows how Neuron collects data from the edge and converts it into MQTT for uploading to EMQX.
![diagram](https://assets.emqx.com/images/820e4a0fa4ee05c049c40b83ff97a477.png)

## Bridging FINS to MQTT via Neuron

This section will introduce how to use Neuron to collect data from FINS TCP devices, upload the collected data to EMQX, and view it using [MQTTX](https://mqttx.app/).

### EMQX Quick Start

EMQX provides multiple installation methods, and users can check the detailed installation methods in the [documentation](https://www.emqx.io/docs/en/v5.0/deploy/install.html). This example uses container deployment to quickly experience EMQX.

Run the following command to obtain the Docker image:

```
docker pull emqx/emqx-enterprise:5.1.0
```

Run the following command to start the Docker container:

```
docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.1.0
```

Access the EMQX Dashboard by visiting `http://localhost:18083` (replace “localhost” with your actual IP address) through a web browser. This allows you to manage device connections and monitor related metrics. Keep the Docker container running for this tutorial. If interested, refer to the [documentation](https://www.emqx.io/docs/en/v5.0/) to experience more features in the Dashboard.

Initial username: admin, initial password: public

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

Open a web browser and enter the gateway address and port number to run Neuron. This will take you to the management console page, with the default port number being 7000. You can access it through your browser at [http://localhost:7000/](http://localhost:7000/) (replace "localhost" with your actual IP address).

#### Step 1: Log in

Log in with the initial username and password:

- Username: `admin`

- Password: `0000`

#### Step 2: Add a Southbound Device

In the **configuration** menu, select **South Devices** to enter the South Devices interface. Click **Add Device** to add a new device.

- Name: fill in the name of the device, such as fins-tcp-1";

- Plugin: select the plugin **FINS TCP** from the drop-down box.

#### Step 3: Set Parameters for Southbound Devices

After adding a southbound device, it automatically enters the device configuration interface, where you can fill in the parameters and submit them. The demo equipment uses Omron CP2E.

- Equipment Type: select CP;

- PLC IP Address: input PLC IP;

- PLC Port: default 9600;

#### Step 4: Create a Group in the Device Card

Click on any blank space on the device node card to enter the group list management interface, and click **Create** to bring up the dialog box for creating a group. Fill in the parameters and submit:

- Group Name: Fill in the group name, such as "group-1";

- Interval: 1000.

#### Step 5: Add Tags to the Group

Click on any blank space of the group card, enter the point list management interface, and click **Create** to enter the page for adding data points.

![图片png](https://assets.emqx.com/images/ebcb7ae859c18b0830bda06a7ef30e67.png)

Fill in the parameters of the data point and submit it：

- Name: Fill in the location name, such as tag-1;

- Attribute: Select the location attribute from the dropdown menu, such as Read, Write;

- Type: Select the data type from the dropdown menu, such as INT16;

- Address: Fill in the driver address, for example, CIO1. CIO represents the CIO area of the PLC in and 1 represents the register address of the location.

- Description, Decimal, Precision: not filled.

#### Step 6: View Collected Data in Data Monitoring

Select **Monitoring → Data Monitoring** from the left navigation menu. View the values read by the created data points, as shown in the following figure.

![图片png](https://assets.emqx.com/images/1a2c6e0ab3967449ca72411661e04735.png)

The data monitoring displays values in groups：

- South Device: Select the southbound device you want to view from the drop-down menu, for example, the created fins-tcp-1;

- Group Name: Select the group you want to view under the selected southbound device from the drop-down menu, for example, the created group-1;

- After selecting, the page will display all values of points read in the selected group.

#### Step 7: Add Northbound Plugin Modules to the Application.

By creating a northbound application, Neuron establishes a connection with the northbound application and uploads collected device data to EMQX.

Select the **North Apps** in the **Configuration** menu, click **Add Application**, as shown in the figure below.

![图片png](https://assets.emqx.com/images/f3dc9e4ef83580bd70ea86211a901502.png)

Add an MQTT cloud connection module:

- Name: Fill in the application name, for example, MQTT;

- Plugin: Select the MQTT plugin from the drop-down.

#### Step 8: Configure Northbound Application Parameters

After adding the northbound application, it will automatically enter the application configuration interface to fill in the parameters and submit.

Set up MQTT connection:

- Client ID: Note that this ID should be independent of each other(Duplicate IDs will cause the client to be kicked). For example, set to MQTT-12123;

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

- South device: Select the created southbound device from the dropdown list, for example, fins-tcp-1;

- Group: Select the group to be subscribed to from the dropdown list, for example, group-1；

- Topic: The MQTT topic, which is default set as `/neuron/MQTT/fins-tcp-1/group-1` in this example. Next, subscribe to this topic and receive messages in MQTTX.

#### Step 10: View data in the MQTT Client.

After subscribing, you can use an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) to connect to EMQX and view the reported data. Here we use MQTTX, a powerful cross-platform MQTT client tool, which can be downloaded from the [official website](https://www.emqx.com/en/products/mqttx).

Once MQTTX is launched, click **+ New Connection** on the main page, fill in the configuration parameters, and click **Connect** in the upper right corner.

- Name: Naming messages facilitates viewing. For example, naming them fins-tcp.

- Client ID: Using the default value is ok; ensure that the ID is independent;

- Host: Select **mqtt://** and fill in `localhost`(replace "localhost" with your actual IP address).

- Port: 1883.

Optional parameters can be filled in, and then click the **Connect** button on the upper right corner after completion. After a successful connection, subscribe to the topic.

- Click **Add Subscription**, and the topic should be the same as the one in step 9. For example, fill in `/neuron/MQTT/fins-tcp-1/group-1`;

After a successful subscription, you can see that MQTTX continues to receive data collected and reported by Neuron. As shown in the following figure.

![MQTTX](https://assets.emqx.com/images/a84ca7156be60a96e43c4762b7d4b406.png)

## Summary

With the growing trend towards cloud-edge collaboration in the industrial 4.0 wave, FINS bridging is becoming an increasingly popular choice for a common IoT protocol. By utilizing the solution mentioned in this blog, users can safely and conveniently implement the IIoT platform on demand with enhanced connectivity, resulting in significant improvements in production efficiency, cost savings, and product quality.



<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
