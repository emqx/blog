## What is CAN Bus?

Control Area Network (CAN) bus is a serial communication protocol that allows devices to exchange data in a reliable and efficient way. It is widely used in vehicles, working like a nervous system to connect ECUs in the vehicle.

CAN bus was originally designed for automotive applications by Bosch in the 1980s. It is a multi-master, multi-slave, half-duplex, and fault-tolerant protocol that fits well with the requirements of automotive applications. It is simple, low-cost, and reliable and can be used in harsh environments. The CAN bus provides one point of entry for all the ECUs in the vehicle, which makes it easy to connect and diagnose.

CAN bus data can provide valuable insights into the performance and status of the connected devices. However, collecting and processing CAN bus data can be challenging due to the high data rate, low bandwidth, and variable network conditions.

One possible solution to overcome these challenges is to use [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), enabling timely data transmission from cars to cloud even with weak network conditions. EMQX is an open-source [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) that can help you build a reliable and scalable MQTT infrastructure for collecting CAN bus data.

![Collecting CAN bus data](https://assets.emqx.com/images/e8c8c72601898e841855a8efa306d63e.png)

## A Brief History of CAN Bus

The Controller Area Network (CAN) bus, developed by Bosch, a German multinational engineering and technology company, originated in the early 1980s. Its primary purpose was to establish an effective communication system for automotive applications, specifically to decrease the complexity of wiring harnesses in vehicles.

In 1986, Bosch introduced their initial CAN protocol, which quickly gained momentum among auto makers due to its reliability and robustness. By 1993, it became an international standard under ISO-11898. To summarize the evolution of the protocol:

- 1991: Mercedes-Benz becomes one of the first automobile manufacturers to implement CAN bus in their W140 S-Class model.
- 2004: The introduction of CAN FD (Flexible Data Rate), providing higher data rates and larger payloads than traditional CAN networks.
- 2015: Adoption of ISO-16845:2015 as a conformance test plan for devices implementing both classic CAN and CAN FD protocols.

Apart from automotive applications, other industries have embraced this versatile network protocol over time. Today, it is used in industrial automation systems (CANopen) and marine electronics (NMEA 2000). Its widespread adoption is mainly attributed to its ability to operate reliably even under harsh conditions while maintaining low-cost implementation requirements.

## How Does a CAN Bus Work?

The CAN bus is a decentralized communication protocol. Its decentralized approach makes it ideal for applications in automotive and industrial systems where reliability and real-time performance are essential.

In a CAN network, all nodes are connected via twisted-pair wiring or optical fiber cables. Each node has its own microcontroller responsible for processing incoming messages and sending outgoing ones. Data is broadcasted by a node on the shared bus, allowing all other nodes to receive it. The primary stages of the communication process are:

1. Arbitration: To prevent collisions when multiple nodes attempt to transmit simultaneously, CAN uses an arbitration process based on message priority. The lower the identifier value of a message, the higher its priority.
2. Error detection: Built-in error detection mechanisms ensure data integrity within CAN networks. These include cyclic redundancy checks (CRC), frame check sequences (FCS), and acknowledgment bits from receiving nodes.
3. Fault confinement: If any node detects an error or malfunctions during transmission, it will enter an "error passive" state until proper operation resumes. This prevents faulty transmissions from affecting overall system functionality.

This combination of features allows CAN buses to maintain high levels of efficiency while ensuring reliable communication between different components in complex systems like vehicles or factory automation equipment.

## Message Structure in the CAN Protocol

The message structure in a CAN bus system is crucial for efficient communication between devices. The protocol uses a data frame format that consists of several fields, including an identifier, control field, data field, and error detection mechanism.

- Identifier: This unique value determines the priority of each message on the network. In standard 11-bit identifiers (CAN 2.0A), there are up to 2048 different priorities available. Extended 29-bit identifiers (CAN 2.0B) provide even more options with over half a billion distinct values.
- Data Length Code (DLC): Located within the control field, this code specifies how many bytes are present in the data field - ranging from zero to eight bytes.
- Data Field: Contains actual information being transmitted across nodes in byte-sized segments.
- Cyclic Redundancy Check (CRC): A built-in error detection mechanism that ensures reliable communication by detecting transmission errors and requesting retransmission if necessary.
- Acknowledgment Slot: A single bit used by receiving nodes to acknowledge successful receipt of messages or indicate errors requiring retransmission.
- Error Frame: An optional part of CAN messaging that allows nodes to signal when they detect an issue with their own transmissions or receive messages from other devices on the network.

## Types of CAN

Here are the three main types of CAN:

### Low-Speed CAN

Low-Speed CAN, also known as fault-tolerant or ISO 11898-3, operates at speeds up to 125 kbps. It is designed for less critical systems like body control modules, door locks, window controls, etc., where data transmission speed isn't vital. Its key feature is the ability to continue functioning even when one wire in the bus fails.

### High-Speed CAN

High-Speed CAN, or ISO 11898-2, can reach speeds up to 1 Mbps. This type of network is suitable for more time-sensitive applications such as engine management systems and electronic braking systems due to its faster data transfer rates compared to low-speed counterparts. However, it lacks fault tolerance capabilities found in low-speed networks.

### CAN FD (Flexible Data Rate)

CAN FD, introduced by Bosch in 2012, is an extension of high-speed networks with increased data rates—up to 5 Mbps—while maintaining backward compatibility with existing high-speed devices. The primary advantage of this technology lies in its ability to transmit larger payloads more efficiently than traditional CAN, making it ideal for modern vehicles with increasingly complex electronic systems.

## Main Advantages of CAN Bus

The CAN bus data can provide valuable insights into the performance, health, and behavior of a vehicle. Collecting CAN bus data to the cloud is a powerful way to leverage the potential of vehicle data through big data analysis. By applying machine learning, artificial intelligence, or other analytical tools to the collected data from a large number of vehicles, vehicle manufacturers can gain valuable insights and leverage them to optimize vehicle performance.

- Detecting, troubleshooting, and predicting faults: By analyzing the CAN bus data, one can identify any abnormal or erroneous signals from the devices and sensors. This can help diagnose the root cause of a problem and fix it before it leads to more damage or safety issues. Manufacturers can also train machine learning models to predict faults by feeding the collected data to the model.
- Visualizing vehicle data: With the collected data, users can develop a system to display the aggregated data on a dashboard that allows users to filter, sort, and compare different vehicles and metrics. The dashboard also provides alerts and recommendations based on the data analysis. The system enables users to gain insights into their performance.
- Vehicle road coordination: The collected data can be calculated together with the road infrastructure data to build a vehicle road coordination system.

In the AI era, data is the most valuable property. By collecting data from cars to the cloud and then distributing it to all kinds of data infrastructure like databases, and data lakes, users can leverage the data for nearly all kinds of applications.

## Addressing Challenges of Real-Time CAN Bus Data Collection

Collecting CAN bus data locally on the vehicle is pretty mature. However, it can be challenging to collect and process the CAN bus data and transfer the insight to the cloud in real-time due to the high data rate, low bandwidth, and variable network conditions. Thus, it is impractical to transfer all the CAN bus data to the cloud for processing. Instead, one can collect and process the CAN bus data locally on the edge side to reduce the data volume, and transfer the insight to the cloud in real-time.

We'll need at least two components to build such a solution:

1. Edge computing engine: An edge computing engine can collect only the needed CAN bus signals, flexibly process them and trigger MQTT transfer actions in real-time.
2. MQTT broker in the cloud: An MQTT broker can help transfer the processed CAN bus data to the cloud in real-time.

### CAN Bus Local Processing with eKuiper

eKuiper is an open-source edge computing engine that can help you process and analyze CAN bus data in real-time. eKuiper is designed for stream processing on the edge, suitable for the real-time processing of the typical streaming data generated by the CAN bus. eKuiper can address these challenges:

- Performant enough to process the high volume and velocity of data generated by the CAN bus in real time. Flexibly filtering, processing and picking interested signals only to reduce the bandwidth to transfer data.
- Can parse the binary CAN frame to meaningful signals to make it possible for rule processing and trigger actions. It supports dynamic DBC file loading, so that users can flexibly change the DBC file to adapt to different CAN bus devices by themselves without restarting the engine. It also makes the DBC file private and secure, no need to share it with the development team.
- Can flexibly compose signals from different CAN frames to construct a complete message for applications through rules. Users can agilely change the rule to adapt to different user scenarios or requirement changes with hot reload.

> *Notice: Some of the features related to the CAN bus described in this document are not open source. You can experiment with these features by utilizing* [*ek-can*](https://hub.docker.com/r/emqx/ek-can)*, which extends CAN bus capabilities on top of eKuiper.*

### Using MQTT to Collect CAN Bus Data

Using an MQTT broker like [EMQX](https://www.emqx.com/en/products/emqx) for collecting CAN bus data can offer several benefits, such as:

- Reduced network overhead: MQTT uses a binary format and a minimal header to encode messages, which reduces the network bandwidth consumption and improves the data transmission efficiency.
- Increased scalability: MQTT can support thousands of concurrent connections and millions of messages per second with a single broker. This can enable large-scale data collection from multiple CAN bus devices without compromising performance or reliability.
- Enhanced security: MQTT supports various security mechanisms, such as TLS/SSL encryption, username/password authentication, and access control lists (ACLs), to protect the data from unauthorized access or tampering.
- Improved interoperability: MQTT is based on open standards and widely supported by various platforms and languages. This can facilitate the integration of CAN bus data with other systems or applications.

## Tutorial: Transferring Processed CAN Bus Data to the Cloud with EMQX

In this section, we will offer a simple demonstration of transferring processed CAN bus data to the cloud for further insights using EMQX.

### Receiving and Parsing Raw Vehicle Data

We will use eKuiper to process and convert raw CAN data from the vehicle. The raw data message we receive is as follows:

```json
{
  "frames": [
    {"id":100,"data":"608474d818f34000","bus":4,"d":0,"t":0},
    {"id":485,"data":"2d38562000000000","bus":4,"d":0,"t":0},
    {"id":555,"data":"00000d0028209e00","bus":4,"d":0,"t":0},
    {"id":423,"data":"0077600000000000","bus":4,"d":0,"t":0},
    {"id":312,"data":"ffc00747800093d6","bus":4,"d":0,"t":0}
  ]
}
```

With eKuiper, we can parse these raw messages based on the DBC file, obtaining signal values in JSON format. For example:

```json
{
  "DASHBOARD": {
    "FuelConsumptionRate": 10.23,
    "FuelUsed": 3727,
    "Odometer": 37846,
    "bus": 4,
    "d": 0,
    "id": 312,
    "t": 0
  },
  "DRIVE": {
    "Acceleration": 0.4,
    "Angle": 43,
    "Speed": 21.71,
    "bus": 4,
    "d": 0,
    "id": 485,
    "t": 0
  },
  "ENGINE": {
    "RPM": 1308,
    "Temperature": 83,
    "Torque": 53,
    "bus": 4,
    "d": 0,
    "id": 555,
    "t": 0
  },
  "GPS": {
    "Altitude": 20.13,
    "Latitude": 33.54,
    "Longitude": 119.12,
    "bus": 4,
    "d": 0,
    "id": 100,
    "t": 0
  },
  "PEDAL": {
    "AcceleratorOpeningAngle": 49.6,
    "BrakePosition": 0,
    "bus": 4,
    "d": 0,
    "id": 423,
    "t": 0
  },
  "raw": {
    "DASHBOARD": "0 4 138 Rx d 8 ff c0 07 47 80 00 93 d6",
    "DRIVE": "0 4 1E5 Rx d 8 2b 21 ee 30 00 00 00 00",
    "ENGINE": "0 4 22B Rx d 8 00 00 0c e0 28 e0 6a 00",
    "GPS": "0 4 64 Rx d 8 60 84 74 d8 18 e7 d0 00",
    "PEDAL": "0 4 1A7 Rx d 8 00 4d 80 00 00 00 00 00"
  },
  "ts": 0
}
```

### Data Collection Rules and Processing

Different collection rules can be applied to further process the parsed data.

In a periodic collection scenario, we can set a rule to collect engine speed, temperature, and torque signals every 10 seconds and report an MQTT message. First, create a data stream and configure it as `interval=10s` to downsample the data. Then, set up a rule with the SQL statement: `SELECT RPM as RPM_10s, Temperature as Temperature_10s, Torque as Torque_10s FROM Stream10s`. After running the rule, you will receive output in the following format:

```json
{
  "RPM_10s": 1214,
  "Temperature_10s": 90,
  "Torque_10s": 56
}
```

In an event collection scenario, we can monitor the brake signal BrakePosition. When its value exceeds the threshold of 10, an event is triggered, and the related signal data from the 10 seconds prior to the trigger is reported. The SQL statement is: `SELECT Acceleration, Angle, BrakePosition, Speed, event_time() FROM stream GROUP BY SlidingWindow(ss, 10) OVER (WHEN BrakePosition > 10)`.

```json
{ 
  {
    "Acceleration": -0.12,
    "Angle": 108,
    "BrakePosition": 0,
    "Speed": 42.15,
    "event_time": 1733826299265
  },
  {
    "Acceleration": 0,
    "Angle": 108,
    "BrakePosition": 0,
    "Speed": 42.18,
    "event_time": 1733826299364
  }
}
```

### Receiving Reported Messages via EMQX

In EMQX, we need to create a rule to process the messages reported by eKuiper. You can also use EMQX's built-in SQL functions to further process the reported messages:

```sql
SELECT
  *
FROM
  "vehicle_events/#"
```

After processing the data with the rule, EMQX will use rule actions to write the vehicle data from the message payload to Kafka and a specific TimescaleDB table.

### **Storing Data to Kafka**

With EMQX's data integration feature, MQTT messages can be forwarded in bulk to Kafka, allowing backend systems to consume Kafka messages and enabling high-throughput, reliable delivery of device messages to business systems.

First, create a topic in Kafka:

```shell
bin/kafka-topics.sh --create --topic vehicle_events --bootstrap-server localhost:9092
```

Following the "[Stream MQTT Data into Apache Kafka](https://docs.emqx.com/en/emqx/latest/data-integration/data-bridge-kafka.html)" guide, add a Kafka action in the EMQX rule engine. Key parameters are as follows:

- **Kafka Topic Name**: Enter `vehicle_events`.
- **Kafka Headers**: Enter metadata or context information related to Kafka messages (optional).
- **Message Key**: Kafka message key. Enter `${clientid}` to use the client ID as the message key.
- **Message Value**: Kafka message value. Enter `${payload}` to include the MQTT payload in the Kafka message payload.

After configuring, submit the action and add it to the rule.

### **Storing Data to TimescaleDB**

You can easily insert or update specific field data into the corresponding tables and columns in a database like TimescaleDB using SQL templates with EMQX's data integration feature, enabling flexible data storage and management.

Next, create a data table in TimescaleDB:

```sql
CREATE TABLE vehicle_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    acceleration NUMERIC,
    angle NUMERIC,
    brake_position NUMERIC,
    speed NUMERIC,
    event_time BIGINT
);
```

In the EMQX rule engine, add a TimescaleDB action and configure the database settings. The key SQL parameters for data insertion are as follows:

```sql
INSERT INTO vehicle_events (acceleration, angle, brake_position, speed, event_time)
VALUES (${payload.Acceleration}, ${payload.Angle}, ${payload.BrakePosition}, ${payload.Speed}, ${payload.event_time});
```

Submit the action to the rule and then finalize the rule creation. This completes the entire process from receiving CAN data, reporting it via MQTT to EMQX, and then forwarding it to Kafka and TimescaleDB. The upper-layer application can flexibly choose to consume the entire message or query specific signal data from the database based on the business requirements.

## Conclusion

The CAN bus is a robust communication protocol that has become integral to modern automotive and industrial systems, providing efficient and reliable data transmission. In this blog, we introduced how to collect, process, and transfer real-time CAN bus data from vehicles to the cloud with eKuiper and EMQX. Organizations can harness the power of real-time data collection and processing, enabling smarter decision-making and more efficient operations in industries ranging from automotive to IoT.


**Related resources**

- [Unlocking Efficiency: How EMQX Revolutionizes Logistics Fleet Management](https://www.emqx.com/en/blog/how-emqx-revolutionizes-logistics-fleet-management)
- [What Is V2X and The Future of Vehicle to Everything Connectivity](https://www.emqx.com/en/blog/what-is-v2x-and-the-future-of-vehicle-to-everything-connectivity)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
