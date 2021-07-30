## MQTT protocol

MQTT is a standard messaging protocol for the IoT business. It is designed as a very lightweight publish/subscribe messaging protocol, which is very suitable for connecting remote devices with a small code usage and network bandwidth. [MQTT Protocol](https://www.emqx.com/en/mqtt) has the following characteristics:

- **Lightweight and efficient**: [MQTT Client](https://www.emqx.com/en/blog/introduction-to-the-commonly-used-mqtt-client-library) is and requires fewer device resources. The MQTT message header is very small, which can optimize the network bandwidth.
- **Two-way communication**: MQTT allows message delivery both from device to cloud and from cloud to the device.
- **Reliable message delivery**: MQTT has three defined service quality levels: 0-at most once, 1-at least once, 2-exactly once. The reliability of message delivery can be guaranteed according to business scenarios.
- **Support for unreliable networks**: Many IoT devices are connected via unreliable cellular networks. MQTT's support for persistent sessions reduces the time to reconnect the client to the broker.
- **Security**: MQTT allows you to easily use TLS to encrypt messages and use modern authentication protocols (such as OAuth) to authenticate the client.

Today, MQTT is widely used in the industries such as automobiles, manufacturing, telecommunications, petroleum and natural gas.

**This series of articles will explain in detail how MQTT protocol plays a role in practical application scenarios of various industries**.



## IoT business in the petroleum industry

With the rapid development of IoT technology, new information sensing equipment and various wired and wireless network technologies have gradually been widely used in petroleum exploration, production, and storage and transportation environment. Petroleum and petrochemical enterprises hope to use the IoT technology to realize the remote management of oilfield terminal equipment and optimize the efficiency, security and scalability of IoT data storage and management.

In the oil production, transportation and storage scenarios, the traditional industrial bus protocol and PLC protocol are transformed into the IoT [MQTT protocol](https://www.emqx.com/en/mqtt) through the industrial edge gateway, and real-time on-site data is delivered  to the data center to realize remote collection and centralized management of on-site data. This is one of the key directions of production monitoring technology transformation in petroleum and petrochemical enterprises.



## Pain points of traditional petroleum data collection scenarios

Traditional petroleum production plants use on-site dedicated wireless or wired networks to transmit the oil pressure, oil temperature, load, power and other data in the oil well to the RTU or PLC in real-time, and then aggregate them through the local SCADA system and store them in the database in the control room of the production area or combined station. The central computer room of the plant needs to synchronize the data from the database of the station control room regularly to realize the data aggregation of multiple operation areas.

With the increasing demand for real-time data consumption by enterprises, the access frequency of edge database is also increasing, and the following problems have gradually been exposed in the actual operation process:

- The software and hardware of data collection and data storage station are aging, and the update cost is high;
- With the increasing amount of data collected, the overall performance can not meet the ever-increasing data demand;
- Real-time data is not available in the plant area, and the real-time management and monitoring capabilities of the station are insufficient;
- On-site technical maintenance personnel has high work intensity and high labor costs.

## Petroleum data collection solution based on MQTT protocol

Thanks to the popularization of network technology in the petroleum industry, network connectivity has been basically achieved between the oil field operation area and the plant area, which provides basic network conditions for the introduction of IoT technology. All kinds of production data can also be collected, aggregated and further processed through the MQTT protocol to give full play to its value.

Take the EMQ cloud-edge data collection solution as an example:

![EMQ cloud-edge data collection solution](https://static.emqx.net/images/5eeb8696f540a403318ed1291381793c.png)

### Convert various industrial protocols to MQTT to achieve unified access

On the field-station side, by using [Industrial Data Collection Gateway - Neuron](https://www.emqx.com/en/products/neuron), the on-site meter data using Modbus-RTU and Modbus-TCP protocols is converted into highly reliable and lightweight MQTT protocol, and then the real-time data is pushed to the data access platform EMQ X in the plant central computer room through the private network.

### Filter and push the data

Some redundant data or data from other systems can be filtered and processed through the lightweight data processing software [eKuiper](https://github.com/lf-edge/ekuiper) deployed on the field-station side to push meaningful data to the data access platform EMQ X in the central computer room of the plant.

### Move the collected data to the database in real-time for business applications

The data access platform EMQ X in the central computer room of the plant accesses the real-time data uniformly and stores it in the database of the central computer room. Various business applications can dock with the database to pull relevant business data.

### Push alarm information in real-time through MQTT protocol

Data that needs to be processed in real-time, such as production equipment alarms and station access alarms, can be pushed to the alarm processing business system by the data access platform EMQ X through the MQTT protocol to achieve rapid real-time data processing.

### Implement real-time monitoring of equipment through MQTT protocol

The plant data center platform can also realize remote control and management of field devices through MQTT messages.



## What does the MQTT protocol bring?

### Improve real-time performance of the business

MQTT protocol has the characteristics of lightweight and high reliable QoS. It can report a large number of equipment and system data in the production area to the plant data center in real-time, which greatly improves the real-time performance of the business.

### Reduce the cost of hardware and software

The lightweight design of MQTT greatly reduces the hardware requirements from the client to the server. In the EMQ cloud-side data collection solution, the highly available [MQTT broker - EMQ X](https://www.emqx.io) in the central computer room of the plant and the lightweight edge industrial gateway Neuron used in production and business replace the expensive SCADA system and data collection and storage server on the field-station side, which reduces the overall hardware and software costs by more than 50%.

### Save labor cost

Due to the light front-end and heavy back-end architecture, the number and complexity of on-site equipment are greatly reduced, and the on-site operation and maintenance load and personnel cost can be reduced by more than 70%.

Through the data collection architecture based on the MQTT protocol, the plant data center can obtain various on-site real-time data so as to carry out new business applications such as remote equipment operation, wellbore location optimization analysis, monitoring operation environment control emissions, remote auxiliary maintenance through these high-quality business data, which can help achieve cost reduction, efficiency improvement and business innovation for petroleum enterprises.
