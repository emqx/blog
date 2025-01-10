## **Introduction**

Siemens PLC, as a key device in industrial automation, plays a vital role in modern manufacturing and production environments. It is not only a core component of industrial automation systems, but also the basis for realizing smart manufacturing, the Internet of Things(IoT) and Industry 4.0.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol designed for unstable or low-bandwidth network environments and has been widely used in IoT communication in modern industrial systems. As an important protocol for IoT communication in modern industrial systems, MQTT provides a flexible, reliable and efficient data transmission solution to help enterprises realize digital transformation and drive the process of smart manufacturing. 

This article will detail the steps to integrate Siemens PLC with MQTT, including the required tools, environment configuration, communication parameter settings, and troubleshooting tips to ensure that readers can realize this integration through this guide. Best practices and real-world application examples are also provided to help readers better understand and apply this integration solution.

## **Overview of Siemens PLCs**

Siemens PLCs connect to industrial networks to gather real-time data from field devices and send control commands to actuators. They are widely used in production control, process automation, and plant management, with the Siemens S7 series being one of the most notable. Here are some key features and functions of the S7 series:

- **High-Speed Processing**: Quickly executes logic operations and handles large volumes of I/O signals for complex manufacturing processes.
- **Modular Design**: Customizable with various modules for easy expansion, upgrades, and cost-effective maintenance.
- **Versatile Communication**: Supports protocols like S7, OPC UA, and Modbus for seamless data exchange with external devices (e.g., HMIs, sensors, robots) and systems (e.g., SCADA, MES).
- **Flexible Programming & Debugging**: Compatible with multiple programming languages and offers powerful debugging tools.
- **Reliable Performance**: Meets industrial certification standards and operates reliably in harsh environments.

## **Practical Use Cases of Siemens and MQTT Integration**

- **Real-Time Monitoring and Control**: Siemens PLCs can use MQTT to send data regarding machine status, sensor readings, and production metrics to a central cloud platform. This allows operators to monitor the status of machinery from anywhere, perform remote diagnostics, and adjust parameters in real-time, improving production efficiency and reducing downtime.
- **Data Analytics and Predictive Maintenance**: By integrating PLCs with MQTT, historical and real-time operational data can be analyzed in cloud-based platforms. This facilitates the implementation of predictive maintenance algorithms that assess the health of machinery and predict failures before they occur, thereby minimizing unplanned downtime and maintenance costs.
- **Interoperability Between Systems**: MQTT enables Siemens PLCs to communicate with other IoT devices, machines, and enterprise systems, regardless of their manufacturer. This interoperability fosters a more cohesive smart factory ecosystem, where various components work together seamlessly, sharing data and insights without compatibility issues.

## **NeuronEX: A Powerful Data Hub for Siemens PLC Connection**

[NeuronEX](https://www.emqx.com/en/products/neuronex) is industrial software designed for device data collection, edge analysis, and IIoT platform integration. It supports industrial protocol data collection, system integration, edge data filtering, AI algorithm deployment, and low-latency data management. NeuronEX helps users gain insights, improve efficiency, and drive sustainability in industrial operations.

With built-in modules for protocols like Siemens, [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol), Ethernet/IP, and [BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained), NeuronEX enables real-time data access from PLCs, CNCs, robots, SCADA systems, and smart meters. It offers robust support for Siemens PLCs through a variety of dedicated plug-ins:

| **Plugin**                    | **Device**                                             | **Description**                                              |
| :---------------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| Siemens S7 ISOTCP             | For Siemens S7-200, S7-200smart, S7-1200, S7-1500 PLCs | Connection via Ethernet                                      |
| Siemens S7 ISOTCP for 300/400 | For Siemens S7-300、S7-400 PLCs                        | Connection via Ethernet                                      |
| Siemens MPI                   | For Siemens S7-300、S7-400 PLCs                        | Connection via adapter 0CA23                                 |
| Siemens S5 Fetch/Write        | For Siemens S7-300、S7-400 PLCs                        | Connection via CP card                                       |
| OPC UA                        | For Siemens S7-1200、S7-1500 PLCs                      | Connection via Ethernet, OPC UA service needs to be turned on in the PLC |

## **Step-by-Step Tutorial: Siemens PLCs to MQTT with NeuronEX**

We will demonstrate how to collect data from a Simens S7-1200 PLC using NeuronEX's Siemens S7 ISOTCP plugin, upload the collected data to a locally-built EMQX MQTT agent (`mqtt://192.168.10.174:1883`), and finally use the MQTT client tool, MQTTX's Subscribe to Topics feature to see how the data has changed.

| **Application** | **IP address** | **Port** |
| :-------------- | :------------- | :------- |
| S7-1200 PLC     | 192.168.10.108 | 102      |
| NeuronEX        | 192.168.10.174 | 8085     |
| EMQX            | 192.168.10.174 | 1883     |
| MQTT X          |                |          |

### **Install and Set Up NeuronEX**  

NeuronEX offers several installation methods, which you can review in detail in the [Installation Guide](https://docs.emqx.com/en/neuronex/latest/installation/docker.html). This example uses a containerized deployment so that you can start experiencing NeuronEX as soon as possible. Execute the following commands to install and run the NeuronEX container.

```shell
## pull NeuronEX
docker pull emqx/neuronex:latest
```

Launch container:

```shell
## run NeuronEX
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:latest
```

Open a web browser and enter the address and port number of the gateway running NeuronEX to access the Management Console page. The default port number is 8085. Access `http://localhost:8085/` through your browser (localhost can be replaced with your actual IP address).

![NeuronEX Console](https://assets.emqx.com/images/d40e6ec336c52363200de1ca3c356204.png)

### **Connect NeuronEX to Siemens PLCs**  

1. Login
   After the page opens, it goes to the login interface, where you can log in with the initial user name and password (initial user name: admin, initial password: 0000).

2. Add Southbound Device
   Select **South Devices** in the **Data Collection** menu to enter the South Devices screen and click **Add Device** to add a new device.

   - Name: fill in the device name, for example, s71200-174;
   - Plugin: drop-down box to select the Siemens S7 ISOTCP.

3. Set the South Device Parameters
   Automatically enter the device configuration interface after adding a southbound device, fill in the parameters and submit. Here we modify the connection parameters according to the actual situation, and then click Add Device to submit the configuration information.

   ![Add Device](https://assets.emqx.com/images/db436f41c78539419802bda20ff88c74.png)

1. Create a Group in the **Group List**
   Click any blank space of the device node card to enter the group list management interface, and click **Create Group** to bring up the dialogue box for creating a group. Fill in the parameters and submit:

   - Group name: Fill in the group name, for example, data;
   - Interval: default 1000.

2. Add Data Point to the Group
   Enter the point list management interface, click Add Tags, fill in the point parameters and submit:

   ![Add tag](https://assets.emqx.com/images/c7354027eb3b8c870f169ca4cc893122.png) 

1. View Collected Data in **Data Monitoring**

   ![Data Monitoring](https://assets.emqx.com/images/bfd299c7531ca1ee5e4a1df244b92b61.png)

### **Configure MQTT in NeuronEX**  

1. Add a North APP Module to the Application
   Select North Apps in the **Data Collection** menu and click **Add Application**.

   - Name: Fill in the application name, for example, mqtt-174;
   - Plugin: drop-down box to select the MQTT plugin.

2. Set the North Application Parameters
   Here we just need to change the Broker Host address to what we need, choose default values for the other parameters, and then click the Add Application button to submit the configuration.

   ![Set the North Application](https://assets.emqx.com/images/dbf905904e2539f92e531f16caa05e04.png)

1. Subscribe to the South Group
   Click on the newly created mqtt-174 node to enter the Group List subscription interface.  Click the **Add Subscription**. Select s7-1200-174/data and **Submit**.

   ![Add Subscription](https://assets.emqx.com/images/02b31ef6d6e0905a4101e81a39db58ed.png)

### **Validate the Data Flow**  

You can go to the [MQTTX official website](https://mqttx.app/) to download and install it. After installation, start MQTTX and add connection, set Host to `mqtt:://192.168.10.174`, Port to `1883`, subscribe to the topic `/neuron/mqtt-174`, and then you can receive the data transferred from S7-1200 PLC.

![MQTTX](https://assets.emqx.com/images/73c77f3248a2101b24cd302d225ea632.png)

## **Conclusion**

In conclusion, NeuronEX provides a powerful and efficient solution for Siemens PLC to MQTT integration, offering simplified connectivity, real-time data transfer, and flexibility in device and protocol support. Its scalability ensures that as your Industrial IoT initiatives grow, NeuronEX can seamlessly expand to meet increasing demands. By streamlining MQTT integration, NeuronEX accelerates your IoT efforts, enabling faster and more reliable data exchange. We encourage you to try NeuronEX with your Siemens devices to experience the ease and efficiency of seamless MQTT integration, and take your industrial IoT projects to the next level.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
