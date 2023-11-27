With the development of IoT, big data, cloud computing and other new-generation information technology, IoT has widely used in various industries and application scenarios, and IoT as a whole shows the trend of device polymorphism, business diversification and application fragmentation. Especially in the [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) scenario, the type of industrial device is various, design bus and protocols are complex and diverse, business applications are flexible, so how to smoothly implement the industrial equipment on the cloud is a problem to be solved.  **EMQX series products provide the ability to decouple industrial equipment and applications, construct the data path from the edge to cloud, establish an intelligent, networked and lightweight digital product and service model, and integrate with 5G to support application innovation in the industrial industry.**



## The era of the Industrial IoT

IIoT is the acronyms of the Industrial Internet of Things, which is the Industrial IoT consisted of hundreds of millions of pieces of the industrial device. Broadly speaking, it refers to the application of instruments, connected sensors, and other equipment to machinery and vehicles in the transportation, energy, and industrial sectors.

With the popularization of [industry 4.0](https://en.wikipedia.org/wiki/Fourth_Industrial_Revolution) concept and the deepening of industrial practice, the traditional centralized control model has transformed into a distributed enhanced control model. At the same time, the advent of the 5G era has accelerated the process of traditional industrial transformation and industrial IoT. To implement the flexible production of personalized and digital products and services, in the process of industrial devices intelligent and networked, the new and old industrial equipment needs to be connected to the internet to implement the business of data collection, remote control and configuration update of industrial equipment. EMQX series products can provide the entire solution from the industrial gateway to the platform and implement data aggregation of the industrial device and sending these data to the cloud, at the edge end of the plant and industrial site. At the same time, its processing ability for edge computing streaming data can provide cloud industrial device data access, data storage and interfacing with cloud-based configuration and applications for the industrial IoT at the platform end. Also, it can facilitate the rapid development of industrial Internet applications.

We will build a simple IIoT application based on [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) through [Neuron](https://www.emqx.com/en/products/neuron) and [EMQX](https://www.emqx.com/en/products/emqx), and use [MQTTX](https://mqttx.app/) to subscribe/display data.



## Introduction to EMQX Neuron

EMQ has recently published [an industrial protocol access software Neuron](https://www.emqx.com/en/products/neuron) deployed on the edge gateway. As a bridge between humans and machines, it can convert and reorganize the 0/1 data of TCP/IP protocol to an easy-to-understand JSON format, and use [MQTT protocol](https://www.emqx.com/en/mqtt-guide) to export the data to the cloud. Therefore, it can better handle the interaction between humans and objects.

EMQX Neuron supports various kinds of industrial protocol, including Modbus, OPC, etc. It can meet most of the industrial access requirements. The detailed protocol list is as follows:

| Protocol Name                                                | **Type** | **Status** |
| ------------------------------------------------------------ | -------- | ---------- |
| **Allen-Bradley DF1 half-duplex for PLC2**                   | Serial   | Avail      |
| **Allen-Bradley DF1 half-duplex for PLC5**                   | Serial   | Avail      |
| **Allen-Bradley DF1 for MicroLogix**                         | Serial   | 2020       |
| **Allen-Bradley Ethernet/IP for MicroLogix**                 | Ethernet | 2020       |
| **Allen-Bradley DF1 for  ControlLogix/CompactLogix/FelxLogix** | Serial   | 2020       |
| **Allen-Bradley Ethernet/IP for ControlLogix/CompactLogix/FelxLogix** | Ethernet | 2020       |
| **Schneider Modbus RTU**                                     | Serial   | Avail      |
| **Schneider Modbus TCP**                                     | Ethernet | Avail      |
| **Schneider Telemecanique UNI-TE**                           | Serial   | Avail      |
| **ABB SattControl Comli**                                    | Serial   | Avail      |
| **Omron Host Link (single)**                                 | Serial   | Avail      |
| **Omron Host Link (multiple)**                               | Serial   | Avail      |
| **Omron   FINS on Host Link**                                | Serial   | 2020       |
| **Omron   FINS on TCP**                                      | Ethernet | 2020       |
| **Omron   FINS on UDP**                                      | Ethernet | 2020       |
| **Omron   Ethernet/IP for CJ/NJ**                            | Ethernet | 2020       |
| **Siemens 3964R/RK512 for S5**                               | Serial   | Avail      |
| **Siemens 3964R/RK512 for S7**                               | Serial   | Avail      |
| **Siemens PPI for S7-200**                                   | Serial   | 2020       |
| **Siemens MPI for S7-300**                                   | Serial   | 2020       |
| **Siemens Fetch Write for S7-300/400 and CP443 module**      | Ethernet | Avail      |
| **Siemens Industrial Ethernet ISO for S7-300/400**           | Ethernet | Avail      |
| **Siemens IE Symbolic Addressing for S7-1200**               | Ethernet | 2020       |
| **Siemens IE Absolute Addressing for S7-1200/1500**          | Ethernet | 2020       |
| **Mitsubishi FX0N/FX0S/FX1N/FX1S/FX2**                       | Serial   | Avail      |
| **Mitsubishi   FX2N/FX3U/FX3G/FX3S**                         | Serial   | Avail      |
| **Mitsubishi   FX3U-ENET-L/FX3U-ENET-ADP**                   | Ethernet | 2020       |
| **Mitsubishi   FX5U**                                        | Serial   | 2020       |
| **Mitsubishi   FX5U Ethernet Module**                        | Ethernet | 2020       |
| **Mitsubishi   FX 232ADP/485BD/232BD Module**                | RS485    | 2020       |
| **Mitsubishi MC Protocol full-duplex for MELSEC-Q and C24   module** | Serial   | 2020       |
| **Mitsubishi MC Protocol for MELSEC-Q and E71 module**       | Ethernet | Avail      |
| **Panasonic MEWTOCOL for FP**                                | Ethernet | 2020       |
| **GE SNP for 90-30**                                         | Serial   | 2020       |
| **GE Ethernet for 90-30**                                    | Ethernet | 2020       |
| **FANUC 0i/30i/31i/32i/35i**                                 | Serial   | 2020       |
| **FANUC 0i/30i/31i/32i/35i Ethernet**                        | Ethernet | 2020       |
| **FANUC T21/D21 for CNC machines**                           | Ethernet | 2020       |
| **Modbus RTU**                                               | RS485    | Avail      |
| **Modbus RTU over TCP**                                      | Ethernet | Avail      |
| **Modbus TCP**                                               | Ethernet | Avail      |
| **OPC UA**                                                   | Ethernet | Avail      |
| **BACnet/MSTP**                                              | RS485    | 2020       |
| **BACnet/IP**                                                | Ethernet | 2020       |
| **IEC 60870-5 (IEC104)**                                     | Ethernet | 2020       |
| **IEC 61850**                                                | Ethernet | 2020       |
| **SNMP**                                                     | Ethernet | 2020       |
| **DNP3**                                                     | Ethernet | 2020       |
| **DLT645-97/07**                                             | Ethernet | 2020       |



## The industrial architecture diagram of EMQX Neuron and EMQX Broker

![Artboard Copy 9备份 4.png](https://assets.emqx.com/images/b922ce2ac26dfac4c6baf23567d3e057.png)


## List of tools used in this simulation

| Tool name               | Version | Description                                 | Operating system    |
| ----------------------- | ------- | ------------------------------------------- | ------------------- |
| PeakHMI Slave Simulator | /       | Modbus simulator                            | Windows Server 2019 |
| EMQX Neuron            | 1.4.6   | Industrial protocol gateway access software | Ubuntu 16.04        |
| EMQX Broker            | 4.0.7   | MQTT Broker                                 | Ubuntu 16.04        |
| MQTTX                  | 1.3.2   | MQTT client tool                            | macOS 10.13.4       |



## Simulation of industrial scenes test

### Deploy/configure EMQX Neuron

- First, unpack and install the EMQX Neuron package.

```
tar -xvlf neuron-1.4.2-x86_64.tar.gz 

sudo ~/bin/installneuron.sh 
```


-  Configure the address which connect to the EMQX Broker in the configuration file, with the username and password as authentication.

```
cd bin/ 

vi neuron.conf  
```

Modify the IP/port, username/password information of the EMQX Broker server in neuron.conf.

```
# MQTT server name or IP address

MQSERVER=127.0.0.1

# Server port no. Note that it will have SSL connection if setting the port no. 

# 8000 or above.

MQPORTNO=1883

# Username and password

MQUSERNAME=emqx123

MQPASSWORD=neuron123
```



- Run EMQX Neuron, the startup is complete when no errors.

```
./neuronsrt  
```



- Log in to the EMQX Neuron Web interface, access IP:7000, the default username password is admin/0000.

![neuron 2.png](https://assets.emqx.com/images/ede993668c0beb95342872a792ca3c06.png)


-  Click Edit Driver, edit the address of Modbus tcp.


![image20200721163444017.png](https://assets.emqx.com/images/a0df7df83a513732bb1b1f777ba10e1d.png)

![image20200721163701173.png](https://assets.emqx.com/images/9026e87281509d5a0c44992a3fdf54aa.png)



- Create Object, define the content within this Object.
![image20200807162508543.png](https://assets.emqx.com/images/65486ad2412b805e897ecf0d22144dec.png)

Create an Attribute in this Object, and then configure the information of Attribute. 

Here simulate an alarm point named Err1@@2D7WS_GAS, the point position is 1!1!07497.

![image20200807162911196.png](https://assets.emqx.com/images/f5471def64343f960b04b266f1c49449.png)

![image20200807163023400.png](https://assets.emqx.com/images/75dc992098e067903bb0e219c847ecac.png)




### Connect the deployed EMQX Broker

The connected EMQX Neuron gateway can be viewed in the EMQX Broker interface, where the Client ID is a string of characters randomly, generated by the EMQX Neuron gateway.

![image20200807163206577.png](https://assets.emqx.com/images/334ea0e8c9b636603d98b21fb9b93a2a.png)


### Configure Modbus simulator

Configure the value of the point 1!1!07497 is 1, and then report the data.

![image20200807164517861.png](https://assets.emqx.com/images/8f1a495e4e983eeaaf37535aa2c49cac.png)



Click the Data Monitoring in the EMQX Neuron interface, the reported value of Attribute “Err1@@2D7WS_GAS” is now 1.


![image20200807164756754.png](https://assets.emqx.com/images/af14d897b8f2d7d876e9611dc91ee1b7.png)


### Use MQTTX subscribe to data for display

Open the connected MQTTX, connect to the EMQX Broker, subscribe to the above topic pubulished by EMQX Neuron, and in MQTTX you will receive the value of 1 for 2D7WS in AlarmObj. After receiving these data, the client can display alarms on the application interface, and can also implement other business transformations through the business logic.

![image20200807165527066.png](https://assets.emqx.com/images/5ef32b447681d675cd1644e8a68315a1.png)



## Summary

The above is a complete simulation test of industrial access using EMQX Neuron, EMQX Broker, MQTTX and other tools to form a clearer and more intuitive understanding of industrial equipment on the cloud. Of course, you can also use the powerful protocol support of EMQX Neuron and the powerful access/forward ability of EMQX Broker to develop your own application demonstration system and build a complete [IIoT platform](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions).

By the end of September 2020, we will implement a complete edge solution for industrial protocol parsing, data aggregation and streaming processing at the edge end through integrating [Neuron](https://www.emqx.com/en/products/neuron), [Edge](https://www.emqx.com/en/products/emqx), [Kuiper](https://github.com/lf-edge/ekuiper) and other software. This solution can implement a complete industrial solution from end to end, and edge to cloud though integrating the cloud series product EMQX Broker / Enterprise.

![Artboard Copy 9备份 4.png](https://assets.emqx.com/images/8c7059339b470666df505bb4e33519f4.png)


<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a >
</section>
