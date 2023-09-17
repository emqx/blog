In the previous article, we introduced how to design different business scenarios in the IoV TSP platform. Every piece of data reported via the IoV is valuable because there is huge business value behind it when the vehicles continuously generate a large number of messages. Therefore, the vehicle TSP platform we build also needs to have ten-million-level topic and million-level message throughput capability.

Traditional Internet systems cannot support millions of message throughput. In this article, we will focus on how to design a new-generation IoV platform architecture to meet the need for millions of message throughput.

## Related Factors of Message Throughput Design in IoV Scenarios

IoV messages are divided into uplink and downlink. The uplink message is generally an alarm message sent by the sensor and the vehicle, which sends the equipment information to the cloud message platform. The downlink message generally includes remote control instruction set message and message push, which serves as corresponding instructions to vehicles sent by the cloud platform.

In IoV messaging throughput design, we need to concentrate on the following factors:

### Message frequency

During the driving process, GPS and on-board sensors are constantly collecting messages. In order to receive real-time feedback information, they also report and receive messages frequently. The frequency of reporting is generally 100ms-30s, so when the number of vehicles reaches the order of millions, the platform needs to support millions of message throughput per second.

### Message Packet Size

The vehicle collects its own environment and status information through various sensors. The overall message packet size generally varies from 500B to several tens of KB. When a large number of message packets are reported simultaneously, the IoV platform is required to have stronger capability to receive and send large message packets.

### Message Latency

Message data can only be transmitted through a wireless network while the vehicle is being driven. In most IoV scenarios, the delay requirement for the vehicle is ms level. The platform also needs to maintain low latency message transmission even with million-level throughput.

### Number and Level of Topic

When considering million-level message throughput scenarios, we also need to design specifications for the number of message Topics and Topic tree levels.

### Payload Codec

When the message packet is large, the encapsulation of the message body should be considered. Simple JSON encapsulation is not efficient in message parsing, so we should consider using Avro, protobuf and other encoding formats for Payload format encapsulation.

For million-level message throughput scenarios, traditional architectures based on shared subscription messages with MQTT clients or writing to relational databases in real-time via rule engines are obviously unsatisfactory. At present, there are two mainstream architectures: one is message access product/service plus message queue (Kafka, Pulsar, RabbitMQ, RocketMQ, etc.), and the other is message access product/service plus time sequence database (InfluxDB, TDengine, Lindorm, etc.).

We will present the implementation of each of these two architectures, using the cloud-native distributed IoT message broker [EMQX](https://www.emqx.com/en/products/emqx) as the messaging access layer, based on the above correlation factors and best practices from customer cases.

## EMQX+Kafka Building Million-Level Throughput IoV Platform

### Architecture Design

Kafka, as one of the mainstream message queues, has the data persistence capability. It can prevent data loss by persistence data to hard disk and replication. The back-end TSP platform or Big Data platform can subscribe to the desired messages in bulk.

Because Kafka has the capability to subscribe and publish, it can receive from the south, caching the reported messages, or transmit the instructions to be sent to the front end through the interface via the northbound connection.

Taking Kafka as an example to build an EMQX plus Kafka million-level throughput IoV platform:

1. The connection and message of front-end vehicle machines can be used as domain name forwarding through load balancing products provided by public cloud vendors. If TLS/DTLS security authentication is adopted, four HAProxy/Nginx servers can be established on the cloud as certificate unloading and load balancing.
2. Ten EMQX nodes are used to form a large cluster, which divides 1 million message throughput into 100,000 message throughput per node on average, while meeting the requirements of high-availability scenarios.
3. Redis can be used as the storage database if there is a need for offline/message caching.
4. As the overall message queue, EMQX forwards the full message to the back-end Kafka cluster via the rule engine.
5. Applications such as the back-end TSP platform/OTA receive corresponding messages by subscribing to the topic of Kafka. The control instructions and push messages of the service platform can be sent to EMQX by means of Kafka/API.


In this architecture, EMQX, as a message broker, has the following advantages, which can meet the requirements of this scenario:

- It supports ten- million-level vehicle connection and million-level message throughput capability.
- The distributed cluster architecture is stable and reliable, which can support dynamic horizontal expansion.
- Strong rule engine and data bridging, persistence capability, which can support million-level message throughput processing.
- Rich API and certification system, which achieves smooth connection.

### Verification of Million Throughput Scenarios

In order to verify the throughput capability of the above architecture, we can build a million-level message throughput test scenario with the following configuration. Benchmark Tools, JMeter, or XMeter test platforms are available for the load test tool. A total of 1 million devices are simulated, with one topic for each device, which sends messages once per second for 12 hours of pressure testing.

The pressure measurement architecture is as follows:

![pressure measurement architecture](https://assets.emqx.com/images/c4198060ccff1045a641b46cb3628041.png)

Performance Test Section Results: 

![EMQX Cluster Dashboard Statistics](https://assets.emqx.com/images/254ec87ece021f9c52d2e30090808770.jpeg)

<center>EMQX Cluster Dashboard Statistics</center>

![EMQX Rule Engine Statistics](https://assets.emqx.com/images/ce1755bac20462967d0b0a79ef04598d.png)

<center>EMQX Rule Engine Statistics</center>


From the EMQX rule engine, we can see that the processing speed of each node is 100,000/s, and the speed of 10 nodes is 1 million/sec in total.

![Statistics of Kafka management interface](https://assets.emqx.com/images/b428bb875b438630811d8627b2dfd0f8.png) 

<center>Statistics of Kafka management interface</center>

We can see write speeds of 1 million per second in Kafka and these nodes keep storing.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/f933a2361fd2b01d36a7f3667711b2bd.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A 5-Step Demo to Setup MQTT to Kafka
    </div>
    <div class="mb-32">
      Unlock the potential of streaming data with MQTT and Kafka and build a data-driven IoT infrastructure.
    </div>
    <a href="https://www.emqx.com/en/resources/leveraging-streaming-data-with-mqtt-and-kafka?utm_campaign=embedded-leveraging-streaming-data-with-mqtt-and-kafka&from=blog-million-level-message-throughput-architecture-design" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## EMQX+InfluxDB Building Million-Level Throughput IoV Platform

### Architecture Design

With the architecture of EMQX+time series database, we can also build a million-level message throughput platform. We take the InfluxDB as an example.

InfluxDB is a high-performance time series database, which is widely used in certain scenarios such as monitoring data of storage system and real-time data of IoT industry. It records messages from the time dimension, with strong write and storage performance, which is suitable for big data and data analysis. The analyzed data can be provided to the background application system for data support.

In this architecture, the EMQX rule engine is used for message forwarding, and the InfluxDB is used for message storage to interface with the back-end big data and analysis platform, which helps to better serve the timing analysis. 

1. The front-end device messages are used as domain name forwarding and load balancing via cloud vendor's load balancing products.
2. One EMQX node is used for testing this time. If necessary, multi-node mode can be adopted to form a corresponding cluster scheme (10 EMQX nodes can be deployed in the test of 1 million nodes).
3. Redis can be used as the storage database if there is a need for offline/message caching.
4. EMQX forwards total messages through the rule engine to the back-end InfluxDB for data persistence storage.
5. The back-end big data platform receives corresponding messages through InfluxDB, analyzes the big data, and then transmits the desired information to EMQX through APIs.

### Scenario Verification

As shown in the test architecture diagram, the XMeter press simulates 100,000 MQTT clients to initiate connections to EMQX with a new connection rate of 10,000 per second and a client heartbeat interval of 300 seconds. After all connections are successful, each client sends a message with QoS 1 and Payload of 200B per second. All messages are filtered and persistently sent to the InfluxDB database through HTTP InfluxDB rule engine bridge.

The test results are presented as follows:

![EMQX Dashboard Statistics](https://assets.emqx.com/images/99c277d19110f91f5d6cfb6bdf064f7d.png) 

<center>EMQX Dashboard Statistics</center>

![EMQX Rule Engine Statistics](https://assets.emqx.com/images/febac6d2cc240d37bb53ee39040b6a5b.png) 

<center>EMQX Rule Engine Statistics</center>

![Data received in InfluxDB database](https://assets.emqx.com/images/2d4d121ad28c7c83ebe611a0e7314c54.png) 

<center>Data received in InfluxDB database</center>

![Statistics of EMQX Dashboard Messages](https://assets.emqx.com/images/b6704a338fde749a951b289f174c07b8.png) 

<center>Statistics of EMQX Dashboard Messages</center>

A single EMQX server achieves message throughput persistence to InfluxDB capability of 100,000 TPS for a single server. With reference to the test scenario of EMQX plus Kafka architecture, if the EMQX cluster nodes are expanded to 10, it will have the capability to support 1 million TPS message throughput.

## Conclusion

In this article, we introduce the factors that need to be considered in message throughput design of an IoV scenario, and provide two mainstream architecture design schemes of million-level throughput platform. Faced with the increasing amount of data in the IoV scenario, we hope this can help relevant teams and developers with the design and development of IoV platforms.


## Other articles in this series

- [IoV beginner to master 01｜MQTT in an IoV scenario](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles)

- [IoV beginner to master 02｜Architecture Design of MQTT Message Platform for Ten-million-level IoV](https://www.emqx.com/en/blog/mqtt-messaging-platform-for-internet-of-vehicles)

- [IoV beginner to master 03｜MQTT topic design in TSP platform scenario](https://www.emqx.com/en/blog/mqtt-topic-design-for-internet-of-vehicles)

- [IoV beginner to master 04 | MQTT QoS design: quality assurance for the IoV platform messaging](https://www.emqx.com/en/blog/mqtt-qos-design-for-internet-of-vehicles)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
