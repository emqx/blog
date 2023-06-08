## What Is an MQTT Broker?

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight protocol that supports the Internet of Things (IoT). This article explains the functionality of its central hub known as the MQTT broker, compares its various implementations, and reviews its use cases, features, and best practices.

An MQTT broker is an intermediary entity that enables [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) to communicate. Specifically, an MQTT broker receives messages published by clients, filters the messages by topic, and distributes them to subscribers.

Using MQTT brokers to enable the publish/subscribe (pub/sub) communication model helps make MQTT a highly efficient and scalable protocol.



## Why Are MQTT Brokers Important?

The MQTT broker plays a crucial role in the MQTT architecture, as it is responsible for facilitating communication between MQTT clients (publishers and subscribers).

Here are some of the main reasons MQTT brokers are important:

- **Message routing**: The MQTT broker receives messages from publishers and routes them to the appropriate subscribers based on their topic subscriptions. This ensures that messages are delivered efficiently and accurately, without the need for clients to establish direct connections with each other.

- **Scalability**: MQTT brokers can handle a large number of simultaneous connections, which is essential for IoT and M2M communication scenarios, where there may be thousands or even millions of connected devices. The broker's ability to manage these connections and messages enables the MQTT protocol to scale effectively.

- **Security**: MQTT brokers can provide security measures like authentication and encryption to ensure that the data transmitted between IoT devices and applications is secure. Learn more: [7 Essential Things to Know about MQTT Security 2023](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security).

- **Integration**: MQTT brokers can integrate with other communication protocols and cloud platforms to provide a complete IoT solution. For example, MQTT brokers can integrate with AWS IoT, Google Cloud IoT, or Microsoft Azure IoT Hub to provide a seamless IoT ecosystem.

- **Session management**: The MQTT broker is responsible for managing client sessions, including maintaining information about the client's subscriptions and handling messages that are retained for delivery to clients when they come online. This session management feature ensures that messages are not lost when clients disconnect and later reconnect to the broker. Learn more: [MQTT Persistent Session and Clean Session Explained](https://www.emqx.com/en/blog/mqtt-session).  


## MQTT Broker Architecture

The MQTT broker architecture is based on the [publish-subscribe messaging pattern](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), which decouples message producers (publishers) from message consumers (subscribers). This architecture includes three primary components: clients, topics, and the broker.

![MQTT Broker Architecture](https://assets.emqx.com/images/cf73c3b847af7b4743993c87f82942e1.png)

- **MQTT Broker Server**

  The MQTT broker is a server that receives messages from publishers and delivers them to subscribers based on their topic subscriptions. It manages client connections, handles subscriptions and unsubscriptions, and ensures message delivery according to the specified [Quality of Service (QoS) levels](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

- **MQTT Clients**

  MQTT clients can be publishers, subscribers, or both. Publishers send messages to the MQTT broker, while subscribers receive messages from the broker. Clients can be any device or application that can establish a connection to the MQTT broker using the MQTT protocol, such as IoT devices, mobile applications, or other servers.

- **Topics**

  Topics are hierarchical strings that define the subject or category of a message. When publishers send messages to the broker, they associate them with a specific topic. Subscribers express their interest in receiving messages by subscribing to one or more [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics). The broker then routes messages to the appropriate subscribers based on their topic subscriptions.

The MQTT broker architecture can be either centralized or distributed. In a centralized architecture, a single broker handles all communication between clients. In a distributed architecture, multiple brokers work together to provide a scalable and fault-tolerant messaging infrastructure. Each broker in a distributed architecture can coordinate with other brokers to manage message routing, ensuring messages are delivered to the intended recipients.

Overall, the MQTT broker architecture provides a flexible and efficient messaging infrastructure that enables devices and applications to communicate securely, efficiently, and at scale.



## Popular Open Source MQTT Brokers

### EMQX

[EMQX](https://www.emqx.io/) is currently the most scalable MQTT broker for IoT applications. It processes millions of MQTT messages in a second with sub-millisecond latency and allows messaging among more than 100 million clients within a single cluster. EMQX is compliant with MQTT 5.0 and 3.x. It’s ideal for distributed IoT networks and can run on the cloud, Microsoft Azure, Amazon Web Services, and Google Cloud. The broker can implement MQTT over TLS/SSL and supports several authentication mechanisms like PSK, JWT, and X.509. Unlike Mosquitto, EMQX supports clustering via CLI, HTTP API, and a Dashboard. 

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

### Mosquitto

[Eclipse Mosquitto](https://github.com/eclipse/mosquitto) is an open-source MQTT broker for MQTT protocol versions 5.0, 3.1.1, and 3.1. Mosquitto is lightweight and can be installed on low-power, single-board computers or enterprise servers. The broker is written in C programming language and can be implemented on MQTT clients with a C library. It can be downloaded for Windows, Mac, Linux, and Raspberry Pi. Ready-to-install binary files are available for all operating systems. The latest version includes an authentication and authorization plugin “mosquitto-go-auth,” a web user interface for managing Mosquitto instances. It also offers a PHP wrapper “Mosquitto-PHP” for creating MQTT clients in PHP.

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

- **[7 Factors to Consider When Choosing MQTT Broker 2023](https://www.emqx.com/en/blog/7-factors-to-consider-when-choosing-mqtt-broker-2023)**

  Looking for the perfect MQTT broker in 2023? Consider these 7 essential factors before making your choice. Read our guide for more.

### MQTT Broker Comparison

- **[A Comprehensive Comparison of Open Source MQTT Brokers in 2023](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)**

  In this post, we’ll explore the top open-source MQTT brokers in 2023 and compare them in-depth to help you choose the best one for your needs.

- **[Top 3 Open Source MQTT Brokers for Industrial IoT in 2023](https://www.emqx.com/en/blog/top-3-open-source-mqtt-brokers-for-industrial-iot-in-2023)**

  This article compares the top 3 MQTT brokers for IIoT in 2023, including each broker's advantages, disadvantages, and use cases.

- **[EMQX vs Mosquitto | 2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-mosquitto-2023-mqtt-broker-comparison)**

  Discover the differences between EMQX and Mosquitto as popular open-source MQTT brokers in 2023 - read our in-depth comparison!

- **[EMQX vs NanoMQ | 2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-nanomq-2023-mqtt-broker-comparison)**

  Compare EMQX and NanoMQ MQTT brokers in 2023 to choose the best fit for your IoT project. Explore their scalability, security, and reliability in our guide.

- **[EMQX vs VerneMQ | 2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison)**

  Read our comprehensive analysis of EMQX and VerneMQ MQTT brokers to make an informed choice for your IoT project.

- **[Mosquitto vs NanoMQ | 2023 MQTT Broker Comparison](https://www.emqx.com/en/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison)**

  This blog post will compare Mosquitto and NanoMQ as MQTT brokers and help readers determine which is better suited for different use cases in 2023.

- **[Evaluation for popular online public MQTT broker](https://www.emqx.com/en/blog/popular-online-public-mqtt-brokers)**

  This article sorts out some popular free online MQTT brokers, which we hope will provide a reference for your choice.

### MQTT Broker Benchmark Testing

- **[Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing)**

  Discover the Open MQTT Benchmark Suite for the unbiased evaluation of MQTT brokers' scalability and performance.

- **[Open MQTT Benchmarking Comparison: MQTT Brokers in 2023](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mqtt-brokers-in-2023)**

  Find your ideal MQTT broker for IoT in 2023 with our open comparison analysis. Get comprehensive benchmarking insights now.

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



## Useful Resources to Help You Get Started with MQTT Brokers

### Getting Started

- **[Get Started with EMQX Cloud: The Easiest Way to Start MQTT Service](https://docs.emqx.com/en/cloud/latest/quick_start/introduction.html)**

  This page will help you start with the fully managed MQTT service - EMQX Cloud- by providing a step-by-step guide on creating an account and exploring its features and characteristics.

- **[How to Install an MQTT Broker on Ubuntu](https://www.emqx.com/en/blog/how-to-install-emqx-mqtt-broker-on-ubuntu)**

  This article will take EMQX as an example to introduce how to build a single-node MQTT broker on Ubuntu.

- **[Enable SSL/TLS for EMQX MQTT broker](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)**

  EMQX MQTT broker supports multiple security authentications, this article will introduce how to enable SSL/TLS for MQTT in EMQX.

### MQTT Broker Integration

- **[Monitoring MQTT broker with Prometheus and Grafana](https://www.emqx.com/en/blog/emqx-prometheus-grafana)**

  In this article, we will introduce how to integrate the monitoring data of EMQX 5.0 into Prometheus, use Grafana to display the monitoring data of EMQX, and finally build a simple MQTT broker monitoring system.

- **[EMQX + ClickHouse implements IoT data collection and analysis](https://www.emqx.com/en/blog/emqx-and-clickhouse-for-iot-data-access-and-analysis)**

  IoT data collection involves mass equipment and data, EMQX + ClickHouse is fully capable of IoT data access, storage, analysis, and processing.

- **[How to access MQTT data with ThingsBoard](https://www.emqx.com/en/blog/how-to-use-thingsboard-to-access-mqtt-data)**

  We will use ThingsBoard Cloud in conjunction with EMQX Cloud to describe how to integrate a third-party MQTT broker into ThingsBoard to access MQTT data.

- **[Process MQTT data with Node-RED](https://www.emqx.com/en/blog/using-node-red-to-process-mqtt-data)**

  This article introduced the operation process for accessing the MQTT broker by using Node-RED and processing the MQTT data before sending it to the broker.



## EMQX: World’s Most Scalable MQTT Broker

[EMQX](https://www.emqx.io/) is one of the most popular MQTT brokers and has 11.5k stars on [GitHub](https://github.com/emqx/emqx). The EMQX project was launched in 2012 and is licensed under Apache version 2.0. EMQX is written in Erlang/OTP, a programming language for building massively scalable soft real-time systems.

EMQX is the world's most scalable MQTT broker that supports advanced features such as MQTT 5.0, MQTT-SN, and [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic). It supports masterless clustering for high availability and horizontal scalability. EMQX 5.0, the latest version, scales to establish 100 million concurrent MQTT connections with a single cluster of 23 nodes.

EMQX offers rich enterprise features, data integration, cloud hosting services, and commercial support from [EMQ Technologies Inc.](https://www.emqx.com/en) Over the years, EMQX has gained popularity among enterprises, startups, and individuals due to its performance, reliability, and scalability. EMQX is widely used for business-critical applications in various industries, such as IoT, [industrial IoT](https://www.emqx.com/en/use-cases/industrial-iot), [connected cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know), [manufacturing](https://www.emqx.com/en/solutions/industries/manufacturing), and telecommunications.

Product page: [https://www.emqx.com/en/products/emqx](https://www.emqx.com/en/products/emqx)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
