## What Is an MQTT Broker?

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight protocol that supports the Internet of Things (IoT).

An MQTT broker is an intermediary entity that enables [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) to communicate. Functioning as a central hub, an MQTT broker efficiently handles the flow of messages between devices and applications.  Specifically, an MQTT broker receives messages published by clients, filters the messages by topic, and distributes them to subscribers.

Using MQTT brokers to enable the publish/subscribe (pub/sub) communication model helps make MQTT a highly efficient and scalable protocol.

This broker-mediated communication enables a lightweight, scalable, and reliable mechanism for devices to share information in a networked environment, playing a crucial role in the establishment of efficient and responsive IoT ecosystems and other distributed applications.

## Why Are MQTT Brokers Important?

The MQTT broker plays a crucial role in the MQTT architecture, as it is responsible for facilitating communication between MQTT clients (publishers and subscribers).

Here are some of the main reasons MQTT brokers are important:

- **Message routing**: The MQTT broker receives messages from publishers and routes them to the appropriate subscribers based on their topic subscriptions. This ensures that messages are delivered efficiently and accurately, without the need for clients to establish direct connections with each other.

- **Scalability**: MQTT brokers can handle a large number of simultaneous connections, which is essential for IoT and M2M communication scenarios, where there may be thousands or even millions of connected devices. The broker's ability to manage these connections and messages enables the MQTT protocol to scale effectively.

- **Security**: MQTT brokers can provide security measures like authentication and encryption to ensure that the data transmitted between IoT devices and applications is secure. Learn more: [7 Essential Things to Know about MQTT Security 2024](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security).

- **Integration**: MQTT brokers can integrate with other communication protocols and cloud platforms to provide a complete IoT solution. For example, MQTT brokers can integrate with AWS IoT, Google Cloud IoT, or Microsoft Azure IoT Hub to provide a seamless IoT ecosystem.

- **Session management**: The MQTT broker is responsible for managing client sessions, including maintaining information about the client's subscriptions and handling messages that are retained for delivery to clients when they come online. This session management feature ensures that messages are not lost when clients disconnect and later reconnect to the broker. Learn more: [MQTT Persistent Session and Clean Session Explained](https://www.emqx.com/en/blog/mqtt-session).  


## MQTT Broker Architecture

The MQTT broker architecture is based on the [publish-subscribe messaging pattern](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), which decouples message producers (publishers) from message consumers (subscribers). This architecture includes three primary components: clients, topics, and the broker.

![MQTT Broker Architecture](https://assets.emqx.com/images/cf73c3b847af7b4743993c87f82942e1.png)

- **MQTT Broker Server**

  The MQTT broker is a server that receives messages from publishers and delivers them to subscribers based on their topic subscriptions. It manages client connections, handles subscriptions and unsubscriptions, and ensures message delivery according to the specified [Quality of Service (QoS) levels](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

- **MQTT Clients**

  [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) can be publishers, subscribers, or both. Publishers send messages to the MQTT broker, while subscribers receive messages from the broker. Clients can be any device or application that can establish a connection to the MQTT broker using the MQTT protocol, such as IoT devices, mobile applications, or other servers.

- **Topics**

  Topics are hierarchical strings that define the subject or category of a message. When publishers send messages to the broker, they associate them with a specific topic. Subscribers express their interest in receiving messages by subscribing to one or more [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics). The broker then routes messages to the appropriate subscribers based on their topic subscriptions.

The MQTT broker architecture can be either centralized or distributed. In a centralized architecture, a single broker handles all communication between clients. In a distributed architecture, multiple brokers work together to provide a scalable and fault-tolerant messaging infrastructure. Each broker in a distributed architecture can coordinate with other brokers to manage message routing, ensuring messages are delivered to the intended recipients.

Overall, the MQTT broker architecture provides a flexible and efficient messaging infrastructure that enables devices and applications to communicate securely, efficiently, and at scale.



## Popular Open Source MQTT Brokers

### EMQX

[EMQX](https://github.com/emqx/emqx) is currently the most scalable MQTT broker for IoT applications. It processes millions of MQTT messages in a second with sub-millisecond latency and allows messaging among more than 100 million clients within a single cluster. EMQX is compliant with MQTT 5.0 and 3.x. It’s ideal for distributed IoT networks and can run on the cloud, Microsoft Azure, Amazon Web Services, and Google Cloud. The broker can implement MQTT over TLS/SSL and supports several authentication mechanisms like PSK, JWT, and X.509. Unlike Mosquitto, EMQX supports clustering via CLI, HTTP API, and a Dashboard. 

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>



### Mosquitto

[Eclipse Mosquitto](https://github.com/eclipse/mosquitto) is an open-source MQTT broker for MQTT protocol versions 5.0, 3.1.1, and 3.1. Mosquitto is lightweight and can be installed on low-power, single-board computers or enterprise servers. The broker is written in C programming language and can be implemented on MQTT clients with a C library. It can be downloaded for Windows, Mac, Linux, and Raspberry Pi. Ready-to-install binary files are available for all operating systems. The latest version includes an authentication and authorization plugin “mosquitto-go-auth,” a web user interface for managing Mosquitto instances. It also offers a PHP wrapper “Mosquitto-PHP” for creating MQTT clients in PHP.

> Learn more: [Mosquitto MQTT Broker: Pros/Cons, Tutorial, and a Modern Alternative](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives).

### NanoMQ

[NanoMQ](https://nanomq.io/) is a lightweight and fast MQTT broker designed for the IoT edge. NanoMQ is implemented in purely C, based on NNG's asynchronous I/O with a multi-threading [Actor Model](https://en.wikipedia.org/wiki/Actor_model), and fully supports MQTT 3.1.1 and MQTT 5.0 protocol versions. NanoMQ is high-performance in the context of a stand-alone broker. The fascinating advantage is its portability. It can be deployed on any POSIX-compatible platform and runs on different CPU architectures such as x86_64, ARM, MIPS, and RISC-V.

<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>



### VerneMQ

The [VerneMQ](https://github.com/vernemq/vernemq) project was launched in [2014](https://github.com/vernemq/vernemq/tree/3c7703f0d62e758ba22a34ceb756f2ac2a4da44a) and initially developed by [Erlio GmbH](https://vernemq.com/company.html). As the second broker wrote in Erlang/OTP, the project is licensed under Apache Version 2.0 and borrowed [some code](https://github.com/vernemq/vernemq/blob/ff75cc33d8e1a4ccb75de7f268d3ea934c9b23fb/apps/vmq_commons/src/vmq_topic.erl) from the EMQX project. Regarding architectural design, VerneMQ supports MQTT message persistence in LevelDB and uses a clustering architecture based on the [Plumtree](https://github.com/lasp-lang/plumtree) library, which implements [the Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf) algorithm.



## How to Choose an MQTT Broker? Resources to Help Your Evaluation Process

The following articles will help you evaluate and select the best MQTT broker for your organization’s needs.

### Evaluation Criteria

- **[7 Factors to Consider When Choosing MQTT Broker 2024](https://www.emqx.com/en/blog/7-factors-to-consider-when-choosing-mqtt-broker-2023)**

  Looking for the perfect MQTT broker in 2024? Consider these 7 essential factors before making your choice. Read our guide for more.

### MQTT Broker Comparison

- **[A Comprehensive Comparison of Open Source MQTT Brokers in 2024](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)**

  In this post, we’ll explore the top open-source MQTT brokers in 2024 and compare them in-depth to help you choose the best one for your needs.

- **[Top 3 Open Source MQTT Brokers for Industrial IoT in 2024](https://www.emqx.com/en/blog/top-3-open-source-mqtt-brokers-for-industrial-iot-in-2023)**

  This article compares the top 3 MQTT brokers for [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) in 2024, including each broker's advantages, disadvantages, and use cases.

- **[EMQX vs Mosquitto | 2024 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-mosquitto-2023-mqtt-broker-comparison)**

  Discover the differences between EMQX and Mosquitto as popular open-source MQTT brokers in 2024 - read our in-depth comparison!

- **[EMQX vs NanoMQ | 2024 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-nanomq-2023-mqtt-broker-comparison)**

  Compare EMQX and NanoMQ MQTT brokers in 2024 to choose the best fit for your IoT project. Explore their scalability, security, and reliability in our guide.

- **[EMQX vs VerneMQ | 2024 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison)**

  Read our comprehensive analysis of EMQX and VerneMQ MQTT brokers to make an informed choice for your IoT project.

- **[Mosquitto vs NanoMQ | 2024 MQTT Broker Comparison](https://www.emqx.com/en/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison)**

  This blog post will compare Mosquitto and NanoMQ as MQTT brokers and help readers determine which is better suited for different use cases in 2024.

- **[Evaluation for popular online public MQTT broker](https://www.emqx.com/en/blog/popular-online-public-mqtt-brokers)**

  This article sorts out some popular [free public MQTT brokers](https://www.emqx.com/en/mqtt/public-mqtt5-broker), which we hope will provide a reference for your choice.

### MQTT Broker Benchmark Testing

- **[Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing)**

  Discover the Open MQTT Benchmark Suite for the unbiased evaluation of MQTT brokers' scalability and performance.

- **[Open MQTT Benchmarking Comparison: MQTT Brokers in 2024](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mqtt-brokers-in-2023)**

  Find your ideal MQTT broker for IoT in 2024 with our open comparison analysis. Get comprehensive benchmarking insights now.

- **[Open MQTT Benchmarking Comparison: Mosquitto vs NanoMQ](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mosquitto-vs-nanomq)**

  Compare the performance of Mosquitto and NanoMQ with Open MQTT Benchmarking in this comprehensive analysis. Discover the right MQTT broker for your needs.

- **[Open MQTT Benchmarking Comparison: EMQX vs NanoMQ](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-nanomq)**

  Comprehensive benchmarking results of EMQX and NanoMQ on performance with Open MQTT Benchmark Suite, helping you choose a suitable MQTT broker.

- **[Open MQTT Benchmarking Comparison: EMQX vs Mosquitto](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-mosquitto)**

  Compare the performance of EMQX and Mosquitto with Open MQTT Benchmarking in this comprehensive analysis. Discover the right MQTT broker for your needs.

- **[Open MQTT Benchmarking Comparison: EMQX vs VerneMQ](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-vernemq)**

  Compare the performance of EMQX and VerneMQ with Open MQTT Benchmarking in this comprehensive analysis. Discover the right MQTT broker for your needs.

- **[Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)**

  To stress-test the scalability of the MQTT broker EMQX, we established 100M MQTT connections to the clusters of 23 EMQX nodes to see how EMQX performs.



## Get Started with MQTT Brokers

### Getting Started

You can easily get started with a free public MQTT broker or a fully managed MQTT service. 

EMQ provides a [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) built with a global multi-region EMQX Cluster. It is exclusively available for those who wish to learn and test the MQTT protocol. Please note that it’s not recommended to use it in production environments as it may pose security risks and downtime concerns.

The fully managed cloud service is the easiest way to start an MQTT service. With [EMQX Cloud](https://www.emqx.com/en/cloud), you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity. The latest edition, [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), provides a forever free 1M session minutes/month complimentary offering for developers to easily start their MQTT deployment within seconds.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


- **[How to Install an MQTT Broker on Ubuntu](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu)**

  This article will take EMQX as an example to introduce how to build a single-node MQTT broker on Ubuntu.

- **[Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)**

  EMQX MQTT broker supports multiple security authentications, this article will introduce how to enable SSL/TLS for MQTT in EMQX.

- [**Run MQTT Broker on Kubernetes**](https://www.emqx.com/en/blog/running-mqtt-on-kubernetes)

  Kubernetes offers a scalable solution for your MQTT broker, automatically adjusting resources based on usage or custom metrics.

- [**Run MQTT Broker on Docker**](https://www.emqx.com/en/blog/running-mqtt-broker-on-docker)

  This article will show you how to deploy MQTT on Docker with EMQX, a popular, open source MQTT broker.

### MQTT Broker Integration

- [**MQTT with Kafka: Supercharging IoT Data Integration**](https://www.emqx.com/en/blog/mqtt-and-kafka)

  In this blog post, we will explore the seamless integration of MQTT data with Kafka for the IoT Application.

- [**MQTT to MongoDB: A Beginner's Guide for IoT Data Integration**](https://www.emqx.com/en/blog/mqtt-and-mongodb-crafting-seamless-synergy-for-iot-data-mangement)

  This post will elaborate on the benefits and key use cases of MongoDB with MQTT in IoT scenarios. We will also provide a demonstration of integrating MQTT data into a MongoDB database to give readers a better understanding of how to implement this process.

- [**Integrating MQTT Data into InfluxDB for a Time-Series IoT Application**](https://www.emqx.com/en/blog/building-an-iot-time-series-data-application-with-mqtt-and-influxdb)

  This article provides a detailed guide on how to connect energy storage devices with EMQX and integrate it with InfluxDB to ensure reliable data storage and enable real-time analytics.

- [**MQTT with TimescaleDB: An Efficient Solution for IoT Time-Series Data Management**](https://www.emqx.com/en/blog/build-an-iot-time-series-data-application-for-energy-storage-with-mqtt-and-timescale)

  Combining the power of MQTT with TimescaleDB in IoT environments unleashes a formidable synergy that revolutionizes data handling and analytics.

- [**MQTT to MySQL: Powering Real-time Monitoring and Smart Decision-Making**](https://www.emqx.com/en/blog/mqtt-to-mysql)

  Integrate MQTT and MySQL to construct a comprehensive real time data monitoring application.

- [**MQTT and Redis: Creating a Real-Time Data Statistics Application for IoT**](https://www.emqx.com/en/blog/mqtt-and-redis)

  In this blog, we will show you how to use the EMQX MQTT broker to collect data from diverse sensors and device events. We will then integrate this data with the Redis database to achieve real-time statistics and analysis.

- [**MQTT to ClickHouse Integration: Fueling Real-Time IoT Data Analytics**](https://www.emqx.com/en/blog/mqtt-to-clickhouse-integration)

  In this blog post, we will explore how MQTT integration with ClickHouse can unleash the power of data analysis and drive enhanced performance across these diverse industries.

- [**MQTT to Webhook: Extending IoT Applications**](https://www.emqx.com/en/blog/mqtt-to-webhook)

  In this blog, we'll delve into the process of harnessing MQTT to gather various types of device data and seamlessly integrate it with Webhook.

- **[Monitoring MQTT broker with Prometheus and Grafana](https://www.emqx.com/en/blog/emqx-prometheus-grafana)**

  In this article, we will introduce how to integrate the monitoring data of EMQX 5.0 into Prometheus, use Grafana to display the monitoring data of EMQX, and finally build a simple MQTT broker monitoring system.

- **[How to access MQTT data with ThingsBoard](https://www.emqx.com/en/blog/how-to-use-thingsboard-to-access-mqtt-data)**

  We will use ThingsBoard Cloud in conjunction with EMQX Cloud to describe how to integrate a third-party MQTT broker into ThingsBoard to access MQTT data.

- **[Process MQTT data with Node-RED](https://www.emqx.com/en/blog/using-node-red-to-process-mqtt-data)**

  This article introduced the operation process for accessing the MQTT broker by using Node-RED and processing the MQTT data before sending it to the broker.


## Uses of MQTT Brokers Across Various Industries

- [**Real-time Monitoring and Control**](https://www.emqx.com/en/solutions/internet-of-things)**:** MQTT brokers are central to IoT architectures, allowing devices to publish and subscribe to topics. This enables real-time monitoring and control of devices in industries such as manufacturing, smart homes, and healthcare.
- [**Industrial Sensor Networks**](https://www.emqx.com/en/blog/data-infrastructure-for-smart-factory)**:** MQTT brokers play a crucial role in collecting and disseminating data from sensors in industrial environments, supporting applications like predictive maintenance and process optimization.
- [**Telemetry in Transportation**](https://www.emqx.com/en/blog/revolutionizing-tsp-platforms)**:** MQTT brokers enable communication between connected vehicles, supporting telemetry data exchange for applications such as vehicle tracking, performance monitoring, and traffic management.
- [**Energy Management**](https://www.emqx.com/en/blog/emqx-enables-smart-energy-storage)**:** MQTT brokers help coordinate communication between smart meters, grid equipment, and energy management systems, enhancing the efficiency, reliability, and responsiveness of energy systems.
- [**Logistics and Warehousing**](https://www.emqx.com/en/blog/a-data-driven-solution-for-logistics-asset-tracking-and-maintenance)*:* MQTT brokers support real-time tracking and visibility in supply chains by allowing devices to publish and subscribe to location and status updates, enhancing overall supply chain efficiency.

## EMQX: World’s Most Scalable MQTT Broker

EMQX is one of the most popular [open source](https://www.acorn.io/resources/blog/open-source) MQTT brokers and has 12.9k stars on [GitHub](https://github.com/emqx/emqx). The EMQX project was launched in 2012 and is licensed under Apache version 2.0. EMQX is written in Erlang/OTP, a programming language for building massively scalable soft real-time systems.

EMQX is the world's most scalable MQTT broker that supports advanced features such as [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), and [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic). It supports masterless clustering for high availability and horizontal scalability. EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

EMQX offers rich enterprise features, data integration, cloud hosting services, and commercial support from [EMQ Technologies Inc.](https://www.emqx.com/en) Over the years, EMQX has gained popularity among enterprises, startups, and individuals due to its performance, reliability, and scalability. EMQX is widely used for business-critical applications in various industries, such as IoT, [industrial IoT](https://www.emqx.com/en/use-cases/industrial-iot), [connected cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know), [manufacturing](https://www.emqx.com/en/solutions/industries/manufacturing), and telecommunications.

Product page: [https://www.emqx.com/en/products/emqx](https://www.emqx.com/en/products/emqx)


**Related Resources**

- [Free MQTT Broker: Exploring Options and Choosing the Right Solution](https://www.emqx.com/en/blog/free-mqtt-broker)
- [MQTT Platform: Essential Features & Use Cases](https://www.emqx.com/en/blog/mqtt-platform-essential-features-and-use-cases)
- [MQTT Client Tools 101: A Beginner's Guide](https://www.emqx.com/en/resources/mqtt-client-tools-101)
- [Mastering MQTT: Your Ultimate Tutorial for MQTT](https://www.emqx.com/en/resources/your-ultimate-tutorial-for-mqtt)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
