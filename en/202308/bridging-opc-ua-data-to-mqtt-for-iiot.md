## Introduction

In this blog, we will offer a bridging solution from [OPC UA]() to MQTT with Neuron and EMQX.

[Neuron](https://neugates.io/) is a modern industrial IoT connectivity server that can connect to a wide range of industrial devices using standard or device-proprietary protocols, enabling the interconnection of industrial IoT platforms with massive devices. As a lightweight industrial protocol gateway software, Neuron is designed to operate on various IoT edge hardware devices with limited resources. Its primary goal is to address the challenge of accessing data from data-centric automation equipment in a unified manner, thus offering essential support for smart manufacturing.

[EMQX](https://www.emqx.io/) is a distributed open-source [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). As the world's most scalable MQTT messaging server, EMQX provides efficient and reliable connectivity to a massive number of IoT devices, enabling high-performance, real-time movement and processing of messages and event streams, helping users rapidly build business-critical IoT platforms and applications.

OPC UA data sources can be captured and aggregated by Neuron's southbound OPC UA driver, converted to the MQTT protocol, and transmitted to the EMQX MQTT Broker. The latter then distributes them to various distributed applications.

We will demonstrate using Neuron to collect data from the Prosys OPC UA Simulation Server, upload the collected data to the locally-built EMQX MQTT Broker (`mqtt://192.168.10.174:1883`), and finally view the changes in the data using the MQTTX subscription topic.

| **Application**                 | **IP address** | **port** |
| :------------------------------ | :------------- | :------- |
| Prosys OPC UA Simulation Server | 192.168.10.174 | 53530    |
| Neuron                          | 192.168.10.174 | 7000     |
| EMQX                            | 192.168.10.174 | 1883     |
| MQTT X                          |                |          |

## Installing the OPC UA Simulator

The installation package can be downloaded from the [Prosys OPC website](https://www.prosysopc.com/products/opc-ua-simulation-server/). After installation, run Prosys OPC UA Simulation. Make sure that the Neuron is running on the same LAN as the simulator.

Click **Objects->Objects::FolderType->Simulation::FolderType** to view the data and select Counter::BaseDataVariableType.

![Select Counter::BaseDataVariableType](https://assets.emqx.com/images/5a4d4723a45d66d48327d45be58fd1e1.png)

## EMQX Startup

Execute the following commands to install and run the EMQX container. For more information on how to install the EMQX container, you can visit the [Installation Guide](https://www.emqx.io/docs/zh/v5.0/deploy/install.html).

```
docker pull emqx/emqx:5.1.0
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083
```

## Neuron Setting

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

## View the Data Using MQTTX

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
