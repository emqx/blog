As we mentioned in the [previous article](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles) of this series, the [MQTT protocol](https://www.emqx.com/en/mqtt) is currently the most suitable communication protocol for building the data platform for IoV. Based on this, this article will continue to discuss the acquisition and transmission of MQTT messages for the IoV and how to build a ten-million-level IoV MQTT message platform, to provide a reference for enterprise users who are engaged in the business of IoV.


## Fundamentals of IoV: Data collection and Transmission 

### **The Significance of the Construction of the Message Platform for IoV** 

With the rapid development of IoV construction today, all original equipment manufacturers have formed a consensus: the purpose of the construction of IoV is not for the Internet, nor for vehicle-mounted entertainment. The purpose of IoV is for data and with IoV there is data. With data, coupled with a complete system of data governance and application, there's everything.

And the target data of the business is not only limited to the relevant data of the vehicle-end. In the V2X framework, it is necessary to solve the interconnection between vehicle and vehicle (V2V), vehicle and road (V2R), vehicle and Internet (V2I), vehicle and cloud (V2C), vehicle and human (V2H), and realize the comprehensive data collection and analysis for vehicles, roads, clouds, Internets and human. The C-V2X protocol and communication mode based on 5G provides a basic capability guarantee for the construction of the whole system.

IoV applications have expanded from traditional OTA application to many new intelligent application scenarios, such as intelligent cockpit, high-precision map adaptation, centimeter-level positioning, vehicle machines' end long connection, mobile-end message acquisition, vehicle-road cloud picture, and vehicle-road coordination. The demand of the IoV business for the messaging platform and data processing system has expanded from the original vehicle cloud to the overall building of the architecture of human-vehicle-road-Internet-cloud, so higher requirements are put forward for the building of the whole message platform.

How to build a message communication and transmission system architecture with mass connection, high concurrent throughput, and low latency to ensure the universality, convenience, high availability, reliability, security and high concurrency of the whole system becomes the key to the building of a new generation of IoV systems based on automatic driving and vehicle-road coordination scenarios.

## Architecture Design of IoV Messaging Platform for Ten-million-level connection

Next, this article will take EMQ's IoV message platform and the total solution for data processing as an example of how to build an IoV message platform for ten-million-level connection.

### Business Challenges

**Secure access of vehicles, road side units and mobile-end systems** 

The vehicle-end needs to cover new IoV business such as vehicle machines' data reporting, POI distribution, file pushing, distribution configuration, message pushing, operation caring, etc. The generated mass message Topic needs more secure and stable access and transmission to realize message subscription and release. The road-end needs to realize the secure access of RSU, message collection and transmission, map data transmission and so on.

**Real-time and reliability of large concurrent message**

Applications such as high-precision map, centimeter-level positioning, and vehicle-road coordination all need to satisfy the millisecond-level low-latency and high-reliability transmission capability requirement of mass vehicle route map messages.  The message processing platform shall be capable of supporting tens of millions of connections and millions of concurrent business scenarios with high performance, low-latency and high reliability.

**Rich integration of application scenarios**

In the IoV system with automatic driving as its core, it is necessary to use a messaging platform to connect various applications related to humans, roads, maps, and clouds. Connecting vehicle-end data with applications such as high-precision map, centimeter-level positioning, vehicle-road coordination and mobile-end connection through the messaging platform, guarantee the coordination of applications through the message platform, and provide a high performance, low-latency and high-reliability data architecture.

**Storage, processing and distribution of mass data**

After the mass IoT data from humans, vehicles, roads, clouds, maps and the Internet is collected, the whole life cycle management shall be carried out.  This includes the access, storage, processing and distribution of large-scale real-time data streams to provide database support for dynamic continuous data streams of the applications.  And it supports applications to use the IoV data to serve consumers and make business decisions.

### Total Solution

In the solution, we mainly use [EMQX](https://www.emqx.com/en/products/emqx), a Cloud-Native IoT Messaging Platform owned by EMQ, to realize the data connection, movement and processing of vehicle-end, human-end and road-end in the IoV system. EMQX’s integrated distributed MQTT message service and powerful IoT rule engine can provide a basic capability base for IoV real-time data movement, processing and integration with high reliability and high performance, helping enterprises to quickly build an IoT platform and applications for key business.

**Message processing for vehicle-end**

EMQX uses the MQTT protocol to access the IoV system. The vehicles are connected with EMQX distributed clusters through load balancing. The horizontal expansion capability of EMQX can realize the data communication capability of ten-million-level vehicle connections and millions of concurrent responses. With the rule engine, the capability of bridging message queues, persistent storage and offline message storage of mass messages can be realized in one-stop. Meanwhile, it provides rich API atomic capability for northbound integration.

In terms of security, EMQX not only supports the TLS/DTLS security protocol to ensure the reliability and stability of the system but also provides multiple guarantee mechanisms such as heartbeat monitoring, last will testament message, QoS level, etc. It can also realize real-time, secure and reliable vehicle machine messaging in complex Internet environments through offline message storage.

**Message processing for human-end and road-end**

EMQX provides a message collection and processing platform for mobile phone APP, RSU and other terminals for human-end and road-end. Based on the capability of 5G network slicing, the traffic information service with ultra-low latency can be realized through the near access of personal terminal and road side unit. Through protocols such as MQTT, information about road conditions perceived by the human-end and road side facilities is pushed to the cloud control platform, and the cloud control platform is integrated with V2X algorithms to achieve intelligent traffic scenarios such as road collaborative perception, security warning and remote collaborative control.

In terms of security, EMQX supports TLS/DTLS encryption of the international standard and guarantees the collaborative security communication of the information system of humans, vehicles and roads by extending the authentication system based on PKI/CA certificates.

### An Architecture Model of Tens of Millions of Connections

For the next generation of IoV, here is the architecture of the overall messaging and data processing platform of EMQ with a ten-million-level of connection scale and million-level of concurrency, for your reference.

- **Business scenario:** The vehicle, mobile APP, RSU and other devices in the IoV system are accessed through MQTT to achieve the concurrent access capability to more than ten-million-level of terminals.
- **System architecture:** The terminal equipment is accessed through MQTT, HTTP and other protocols, and connects to the distributed message platform EMQX through the load balancing component. Through distributed multi-cluster deployment, it can meet the requirement of tens of millions of concurrent connections. According to the million-level of message throughput capacity, the rule engine is connected to the Kafka cluster to realize data forwarding. IoV service platform, high-precision map service, V2X cloud control service, location service and other IoV related applications can be consumed directly by subscribing to Kafka data. Meanwhile, EMQ provides REST, MQTT and MQ message queue three southbound interface services to realize two-way communication of vehicle control (remote control) messages.

With this architecture, EMQ can meet the business requirements of tens of millions of connections and millions of concurrent throughput in the IoV scenario through the Cloud-Native IoT Messaging Platform EMQX.

## Ten-million-level Connection Test 

### Test Environment and Purpose

A vehicle enterprise plans to verify the following capabilities of EMQX cluster based on test environment in the IoV scenario, and make corresponding technical architecture and capability support preparations for subsequent business growth:

- It can support 10 million concurrent connections, and at the same time, it supports QoS0 messages with 100 bytes of payload and 100,000-150,000 per second to be bridged to Kafka through the rule engine;
- It supports the subscription of 10 million concurrent connections and the consumption of OTA broadcast theme;
- The simultaneous connection of 3 million users will not cause a cluster avalanche, and it can test the time required for connection. 

In addition, after all of the above tests have been completed, we will continue to explore the maximum throughput of messaging and bridging and forwarding to Kafka that can be supported with 10 million concurrency in the current configuration (increasing client messaging frequency based on the usage of the EMQX cluster resource), and testing the maximum message throughput with QoS2 and an average response time of 50 milliseconds under 10 million connections.

### Test Preparation

The client connects to load balancing ELB through TLS encryption, then ends the client with TLS on HAProxy, and finally connects to EMQX cluster through TCP. The supporting capability of EMQX cluster can be improved by terminating TLS on HAProxy. In this deployment mode, the processing capability of EMQX is identical to that of client directly connecting through MQTT TCP. In addition, compared with the MQTT TCP connection, the client also needs to consume more resources through TLS connection. However, the scale of this test is ten-million-level, which requires a large number of test machines. In order to reduce the required test resources without affecting the test target of EMQX cluster, the TCP connection will be directly used in this test.

| **Service**                           | **Amount** | **Version** | **OS**    | **CPU** | **RAM** | **Network interface card** | **Port**                  |
| :------------------------------------ | :--------- | :---------- | :-------- | :------ | :------ | :------------------------- | :------------------------ |
| Load balancing cloud service          | 1          |             |           |         |         |                            | 18083/1883/8081           |
| EMQX node                             | 10         | V4.3.4      | Centos7.8 | 64C     | 128G    | 1                          | 18083/1883/8081/8883      |
| Kafka cloud service                   | 4          | 2.3.0       | Centos7.8 | 16      | 32G     | 1                          | 9092                      |
| XMeter pressure test controlling node | 2          | 3.0         | Centos7.8 | 16      | 32G     | 1                          | 443/80/3000/8086port open |
| XMeter pressure test node             | 43         | 3.0         | Centos7.8 | 16      | 32G     | 5                          | port open                 |


### Test Scenarios

| S/N  | Name of Scenarios                                            | Description                                                  | Expected Result                                              |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | Tens of millions of connections + message throughput         | Ten million MQTT TCP concurrent connection with heartbeat interval of 200s. Among them, seven million are background connections (only connecting without sending messages), three million active users, each user reports a QOS0 message every 15s, and the payload is 100B. The message is bridged to Kafka by the rule engine. Test for one hour first, then conduct a 24-hour stability test. | The success rate of intranet test was 100%, and there was no message backlog. During the test, the performance of CPU and internal memory was smooth without significant vibrate. |
| 2    | Message broadcasting                                         | Ten million MQTT TCP concurrent connections, all connections subscribe to the same OTA broadcast theme (QoS0, payload 100B). Simulate an MQTT client to broadcast a message to the topic every 10 minutes, test for 30 minutes. | The success rate of intranet test was 100%, and all subscription clients successfully consumed three messages. |
| 3    | Three million concurrent instant connection                  | Three million MQTT clients simultaneously initiate a connection, and test the time required for the completion of all connections. | With three million clients connected successfully, the cluster would not avalanche. |
| 4    | Exploration of maximum message throughput with ten million connections | Maximum message throughput achievable with existing configuration and ten million connections and bridging kafka (QoS0, payload 100B/1kB). | Test two hours after the maximum message throughput is reached, the success rate of intranet test was 100%, there was no message backlog. During the test, the performance of CPU and internal memory was smooth without significant vibrate. |

### Test Results

The following are the results of this test:

| **S/N** | **Scenarios**                                                | **Average Response Time**             | **EMQX Node CPU Utilization** | **EMQX Node CPU IDLE** | **EMQX Node Internal Memory Usage (G)** | **LB Required Bandwidth (MB)** |
| ------- | ------------------------------------------------------------ | ------------------------------------- | ----------------------------- | ---------------------- | --------------------------------------- | ------------------------------ |
| 1       | Ten million connections+200 thousand message throughput, QoS0, payload 100B | 1.5ms                                 | 31%-48% Average: 47%          | 37%-54% Average: 47%   | Used: 27.7~42 Free: 78.2~92.5           | 45                             |
| 2       | Message broadcasting under ten million connections           | 100ms                                 | Max 21%                       | Min 69%                | Used: Max. 32.3Free:Min. 87.9           | 200                            |
| 3       | Three million client instant connection                      | Connection completed in three minutes | Max 25%                       | Min 63%                | Used: Max 14.7Free: Min 108.2           | 400                            |
| 4       | Explore max throughput: Ten million connections+1.2 million message throughput, QoS0, payload 1kB | 164.3ms                               | 23%-64% Average: 46%          | 20%-64% Average: 43%   | Used: 33~38 Free: 81.3~87.1             | 1350                           |
| 5       | Ten million connection+QoS2 200 thousand message throughput, payload 100B | 51.4ms                                | 3%-51% Average: 41%           | 31%-53% Average: 43%   | Used: 22.2~29 Free: 91~98               | 95                             |

### Summary

As shown above, under the current deployment architecture, it can meet the verification requirements of the vehicle enterprise for tens of millions of concurrent connection+200 thousand message bridging to Kafka, message broadcasting and three million instant concurrent connections. In the exploration test, the maximum 1.2 million message TPS (QoS0, payload 1kB) was tested under 10 million connections, the test lasted for 10 hours, the EMQX cluster was stable, the lowest CPU idle was 20%, and internal memory usage is stable.

It can be seen that EMQX has outstanding performance, stable and reliable architecture for supporting tens of millions of connections in the IoV scenario.


>**Introduction to the Pressure Test Tools**
>
>Due to the large number of testing machines required and complicated management, we use the commercial version of EMQ software XMeter performance test platform and [JMeter-MQTT plug-in](https://github.com/emqx/mqtt-jmeter) for the test.
>
>- XMeter Website: [https://www.xmeter.net/](https://www.xmeter.net/) 
>- JMeter download address: [https://jmeter.apache.org/](https://jmeter.apache.org/) 

## Conclusion

In this article, we introduce the architecture design of the ten-million level of IoV MQTT message platform based on the Cloud-Native IoT Messaging Platform EMQX, and verify the performance of the architecture under the ten-million-level concurrent connection scenario, which provides a possible design reference for the building of the message data platform of the IoV system.

As the world's leading provider of IoT data infrastructure software, EMQ is committed to building products with high performance, low latency, high availability and high reliability thereby providing a total solution for information acquisition, movement, processing and analysis for the new generation of IoV systems. This provides infrastructure service guarantee for automatic driving and intelligent networked automobile business of vehicle manufacturers, T1 suppliers, post-market service providers, travel service companies and government management organizations, and realizes intelligent connection among humans, vehicles, roads and clouds.


## Other articles in this series

- [IoV beginner to master 01｜MQTT in an IoV scenario](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles)

- [IoV beginner to master 03｜MQTT topic design in TSP platform scenario](https://www.emqx.com/en/blog/mqtt-topic-design-for-internet-of-vehicles)

- [IoV beginner to master 04 | MQTT QoS design: quality assurance for the IoV platform messaging](https://www.emqx.com/en/blog/mqtt-qos-design-for-internet-of-vehicles)
