## What is CAN Bus?

Control Area Network (CAN) bus is a serial communication protocol that allows devices to exchange data in a reliable and efficient way. It is widely used in vehicles, working like a nervous system to connect ECUs in the vehicle.

CAN bus was originally designed for automotive applications by Bosch in the 1980s. It is a multi-master, multi-slave, half-duplex, and fault-tolerant protocol that fits well with the requirements of automotive applications. It is simple, low-cost, and reliable and can be used in harsh environments. The CAN bus provides one point of entry for all the ECUs in the vehicle, which makes it easy to connect and diagnose.

CAN bus data can provide valuable insights into the performance and status of the connected devices. However, collecting and processing CAN bus data can be challenging due to the high data rate, low bandwidth, and variable network conditions.

One possible solution to overcome these challenges is to use [MQTT](https://www.emqx.com/en/mqtt-guide), enabling timely data transmission from cars to cloud even with weak network conditions. [EMQX is an open-source MQTT broker](https://www.emqx.io/) that can help you build a reliable and scalable MQTT infrastructure for collecting CAN bus data.

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
- Error Frame: An optional part of CAN messaging that allows nodes to signal when they detect an issue with their own transmissions or received messages from other devices on the network.

## Types of CAN

Here are the three main types of CAN:

### Low-Speed CAN

Low-Speed CAN, also known as fault-tolerant or ISO 11898-3, operates at speeds up to 125 kbps. It is designed for less critical systems like body control modules, door locks, window controls, etc., where data transmission speed isn't vital. Its key feature is the ability to continue functioning even when one wire in the bus fails.

### High-Speed CAN

High-Speed CAN, or ISO 11898-2, can reach speeds up to 1 Mbps. This type of network is suitable for more time-sensitive applications such as engine management systems and electronic braking systems due to its faster data transfer rates compared to low-speed counterparts. However, it lacks fault tolerance capabilities found in low-speed networks.

### CAN FD (Flexible Data Rate)

CAN FD, introduced by Bosch in 2012, is an extension of high-speed networks with increased data rates—up to 5 Mbps—while maintaining backward compatibility with existing high-speed devices. The primary advantage of this technology lies in its ability to transmit larger payloads more efficiently than traditional CAN, making it ideal for modern vehicles with increasingly complex electronic systems.

## CAN Bus: Advantages and Challenges

### What are the Main Advantages of CAN Bus?

The CAN bus data can provide valuable insights into the performance, health, and behavior of a vehicle. Collecting CAN bus data to the cloud is a powerful way to leverage the potential of vehicle data through big data analysis. By applying machine learning, artificial intelligence, or other analytical tools to the collected data from a large number of vehicles, vehicle manufacturers can gain valuable insights and leverage them to optimize vehicle performance.

-  Detecting, troubleshooting, and predicting faults: By analyzing the CAN bus data, one can identify any abnormal or erroneous signals from the devices and sensors. This can help diagnose the root cause of a problem and fix it before it leads to more damage or safety issues. Manufacturers can also train machine learning models to predict faults by feeding the collected data to the model.
-  Visualizing vehicle data: With the collected data, users can develop a system to display the aggregated data on a dashboard that allows users to filter, sort, and compare different vehicles and metrics. The dashboard also provides alerts and recommendations based on the data analysis. The system enables users to gain insights into their performance.
-  Vehicle road coordination: The collected data can be calculated together with the road infrastructure data to build a vehicle road coordination system.

In the AI era, data is the most valuable property. By collecting data from cars to the cloud and then distributing it to all kinds of data infrastructure like databases, and data lakes, users can leverage the data for nearly all kinds of applications.

### What are the Challenges of Real-Time Data Collection?

Collecting CAN bus data locally on the vehicle is pretty mature. However, it can be challenging to collect and process the CAN bus data and transfer the insight to the cloud in real-time due to the high data rate, low bandwidth, and variable network conditions. Thus, it is impractical to transfer all the CAN bus data to the cloud for processing. Instead, one can collect and process the CAN bus data locally on the edge side to reduce the data volume, and transfer the insight to the cloud in real-time.

We'll need at least two components to build such a solution:

1. Edge computing engine: An edge computing engine can collect only the needed CAN bus signals, flexibly process them and trigger MQTT transfer actions in real-time. [LF Edge eKuiper](https://ekuiper.org/) is an open-source edge computing engine that can help you process and analyze CAN bus data in real-time.
2. MQTT broker in the cloud: An MQTT broker can help transfer the processed CAN bus data to the cloud in real-time. EMQX is an open-source MQTT broker that can help you build a reliable and scalable MQTT infrastructure for collecting CAN bus data.

> Learn more:
> - [https://ekuiper.org/](https://ekuiper.org/)
> - [https://www.emqx.com/en/products/emqx-ecp](https://www.emqx.com/en/products/emqx-ecp)

Next, we will illustrate the overall solution combining EMQX and eKuiper.

## Addressing the Challenges of CAN Bus Local Processing With eKuiper

eKuiper is an open-source edge computing engine that can help you process and analyze CAN bus data in real-time. eKuiper is designed for stream processing on the edge, suitable for the real-time processing of the typical streaming data generated by the CAN bus. eKuiper can address these challenges:

-  Performant enough to process the high volume and velocity of data generated by the CAN bus in real time. Flexibly filtering, processing and picking interested signals only to reduce the bandwidth to transfer data.
-  Can parse the binary CAN frame to meaningful signals to make it possible for rule processing and trigger actions. It supports dynamic DBC file loading, so that users can flexibly change the DBC file to adapt to different CAN bus devices by themselves without restarting the engine. It also makes the DBC file private and secure, no need to share it with the development team.
-  Can flexibly compose signals from different CAN frames to construct a complete message for applications through rules. Users can agilely change the rule to adapt to different user scenarios or requirement changes with hot reload.

> Notice: Some of the features related to the CAN bus described in this document are not open source. You can experiment with these features by utilizing [ek-can](https://hub.docker.com/r/emqx/ek-can), which extends CAN bus capabilities on top of eKuiper.

## Tutorial: Local Processing for CAN BUS Data with eKuiper

### Step 1: Connect to CAN Bus

eKuiper uses CAN source plugin to connect to CAN bus and receive CAN frames. It supports two modes to connect to CAN bus as shown in the diagram below.

![eKuiper supports two modes to connect to CAN bus](https://assets.emqx.com/images/998a9d2d4c155f86566506b2df4ab368.png)

1. Connect to CAN bus directly by socketCan. SocketCAN uses the Berkeley socket API, the Linux network stack and implements the CAN device drivers as network interfaces. Once the CAN bus is connected to the Linux system, users can get the CAN network interface. In eKuiper, users can create a CAN stream by specifying the **CAN network interface** and **the DBC file path**. Any rules can then be applied to the CAN stream to process the CAN bus data.
2. Connect to CAN bus through a gateway by TCP/UDP. The gateway can be a CAN adapter which combines multiple CAN frames into a packet and sent out in batch by TCP or UDP. Notice that, the packet format sent by the gateway is not standardized. So we may need to modify the plugin to adapt to it. In eKuiper, users can create a CAN stream by specifying the **TCP/UDP address** and **the DBC file path**. Any rules can then be applied to the CAN stream to process the CAN bus data.

### Step 2: Decode CAN Bus Data

CAN bus data is in binary form and organized as a frame. The CAN frame is composed of several fields. Various CAN protocols include CAN 2.0A, CAN2.0B, and CANFD. The CAN frame format is slightly different for different protocols. The CAN frame format for CAN 2.0A is shown in the figure below.

![The CAN frame format for CAN 2.0A](https://assets.emqx.com/images/cbc0baed755040774507737927c30f5a.png)

Among them, two fields are important for us to decode the CAN bus data:

1. The ID field: The ID field is used to identify the CAN frame. It is 11-bit for CAN 2.0A protocol and 29-bit for CAN 2.0B and CANFD.
2. The Data field: The Data field is the payload which is used to carry the actual data. It is 0-8 bytes for CAN 2.0A and CAN 2.0B 0-64 bytes for CANFD.

In the payload, the data is organized as a series of signals. The signal is a named data item with a specific length and a specific position in the payload. DBC file is a text file that contains information for decoding raw CAN bus data to 'physical values'. It defines the signal name, length, position, and the conversion formula to convert the raw data to physical values.

In eKuiper, users can specify the DBC path to use when parsing the CAN bus data. It is pretty flexible and secure to configure the DBC in eKuiper.

-  Multiple DBC files: Users can specify a directory as the DBC path. Inside the directory, multiple DBC files will be loaded in alphabetical order and all will take effect. This can help users to incrementally add or revert signals with separate DBC files.
-  Dynamic DBC file loading: The DBC files are loading in runtime without a need to deploy at development time. This can help users to keep the DBC file private and secure.
-  Hot reload: Users can change the DBC file to adapt to different CAN bus devices by themselves without restarting the engine.

After configuring the eKuiper CAN source, users can create a stream to receive the CAN bus data with physical and meaningful signals. For example, the CAN payload `0x0000000000000000` can be parsed to the following signals:



```
{
  "signal1": 0,
  "signal2": 0,
  "signal3": 0,
  "signal4": 0,
  "signal5": 0,
  "signal6": 0,
  "signal7": 0,
  "signal8": 0
}
```

Next, users can leverage the powerful eKuiper stream processing capabilities to flexibly process the parsed data just like receiving from MQTT.

### Step 3: Process CAN Bus Data

After getting the parsed data, we can do a lot of things with it by eKuiper. In order to reduce the bandwidth to transfer data, we can pick the interested signals only. For example, we can pick the signals `signal1` and `signal2` only.

```
{
  "signal1": 0,
  "signal2": 0
}
```

The eKuiper SQL to do this is simple:

```
SELECT signal1, signal2 FROM canStream
```

Because CAN frame size is limited, there is a good chance that the needed signals spread around multiple CAN frames. In this case, we can flexibly composite the signals from different CAN frames to construct a complete message for applications with various algorithms according to your needs. Check the [data merging](https://ekuiper.org/docs/en/latest/example/data_merge/merge_single_stream.html) example for more details. Here, we use signal1 as the main property to pick the data.

```
SELECT signal1, latest(signal2) as signal2 FROM canStream WHERE isNull(signal1) = false
```

Another example of processing is to collect the data only when some event happens. This can also significantly reduce the bandwidth. For example, we can collect the data only when the signal1 is higher than 100.

```
SELECT signal1, signal2 FROM canStream WHERE signal1 > 100
```

**Moreover, these processing rules are flexible and can be changed on the fly.** Don't worry if you cannot identify the needed signals at the beginning. You can change the rules to adapt to the requirement changes with hot reload.

The most mature usage is to achieve flexible data collection. Besides that, eKuiper can be used in other scenarios like:

1. Real-time, flexible rule engine on the vehicle side that can trigger actions based on specific conditions. For example, automatically closing windows when the vehicle's speed exceeds 70 mph.
2. Agile smart analytics that allows for data and AI model (currently TF Lite) wiring without coding or cloud connection. This feature enables real-time data analysis, such as predicting and suggesting driving modes based on data like speed and tire pressure (even without network connection).
3. Edge computing to reduce transfer bandwidth and reduce cloud-side computing pressure. Parse, reformat and transform the data, such as calculating the average speed for a time window to save.
4. Heterogeneous data aggregation. Parse data from various protocols (TCP, UDP, HTTP, MQTT) and various formats (CAN, JSON, CSV, etc.) and merge them by flexible rules.
5. Message routing. Decide which data to send to the cloud and which to save locally to be leveraged by other vehicle-side apps. For example, based on GDPR or some whitelist to determine the routing.

## Using MQTT to Collect CAN Bus Data

Using an MQTT broker like [EMQX](https://www.emqx.io/) for collecting CAN bus data can offer several benefits, such as:

- Reduced network overhead: MQTT uses a binary format and a minimal header to encode messages, which reduces the network bandwidth consumption and improves the data transmission efficiency.
- Increased scalability: MQTT can support thousands of concurrent connections and millions of messages per second with a single broker. This can enable large-scale data collection from multiple CAN bus devices without compromising performance or reliability.

- Enhanced security: MQTT supports various security mechanisms, such as TLS/SSL encryption, username/password authentication, and access control lists (ACLs), to protect the data from unauthorized access or tampering.
- Improved interoperability: MQTT is based on open standards and widely supported by various platforms and languages. This can facilitate the integration of CAN bus data with other systems or applications.

Besides these benefits, EMQX provides more features and together with eKuiper, it can help users save bandwidth, reduce latency, and improve reliability when transferring CAN bus data.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/a4b8936bb3d27fbccd734eccbe3f821b.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      Rev Up Your Connected Vehicles Future with MQTT
    </div>
    <div class="promotion-pdf__desc">
      The key to building a scalable, secure system for your connected-vehicles business.
    </div>
    <a href="https://www.emqx.com/en/resources/driving-the-future-of-connected-cars-with-mqtt?utm_campaign=embedded-driving-the-future-of-connected-cars-with-mqtt&from=blog-can-bus-how-it-works-pros-and-cons" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

### Save Bandwidth

To transfer CAN bus data over MQTT, we usually need to transfer through weak network conditions with limited bandwidth. In this case, we need to reduce the data size as much as possible.

In eKuiper sink, we can use the `format` option to specify the data format. The default format is `JSON`. We can change it to `protobuf` to serialize the data into binary format to reduce the data size significantly. Additionally, we can use the `compress` option to compress the data by `gzip` or other compression methods. In this way, we can significantly reduce the data size compared to the original JSON data. Especially when sending the data in batch, the data size can be reduced by 90% or more in one of our test cases.

### Real-Time Data

Some of the data is time sensitive for cloud applications. For example, the data to diagnose the vehicle accident is critical. In this case, we need to reduce the latency as much as possible. In eKuiper rule, we can use the MQTT sink to send the data to EMQX.

To save bandwidth in the real-time scenario, we can set the serialization format and compression method as mentioned above in eKuiper MQTT sink. In EMQX side, it provides rule engine which supports decompressing and deserializing the data. Without coding, the data can be consumed by the cloud application in real time.

### Batch Data in File

For data that is not time-sensitive, we can save the data in file or local DB and send it to cloud in batch. It can achieve a higher compression rate to save even more bandwidth. In eKuiper rule, we can use file sink to save and compress data locally. It supports configuring the file rolling policy. For example, we can configure the file rolling policy to roll the file every 10 minutes. In this way, we can save the data in file in batch. EMQX is developing a new feature to support transferring the file. Once completed, the saved file can be transferred by MQTT. Currently, users can use other tools to transfer the file to cloud.

## Conclusion

In this blog, we have introduced how to collect, process and transfer CAN bus data from vehicles to the cloud with eKuiper and EMQX. In the next blog post, we will go into more detail about each step.


**Related resources**
- [Unlocking Efficiency: How EMQX Revolutionizes Logistics Fleet Management](https://www.emqx.com/en/blog/how-emqx-revolutionizes-logistics-fleet-management)
- [What Is V2X and The Future of Vehicle to Everything Connectivity](https://www.emqx.com/en/blog/what-is-v2x-and-the-future-of-vehicle-to-everything-connectivity)
