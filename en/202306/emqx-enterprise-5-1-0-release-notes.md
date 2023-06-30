## Introduction

We are excited to announce our latest release of the [EMQX Enterprise 5.1 MQTT platform](https://site-ip.mqttce.com/en/products/emqx). This latest version provides an even more powerful and flexible IoT data solution, empowering you to build your digital businesses easily and efficiently, streamlining your IoT data flow from edge to cloud.

Some of the new features from our new EMQX Enterprise MQTT platform include:

- Distributed architecture to scale up to 100 million MQTT connections. 
- Option to enable [MQTT over QUIC](https://site-ip.mqttce.com/en/blog/mqtt-over-quic), the next generation of IoT messaging.
- MQTT-based large file transfer capability to seamlessly unify IoT data channels.
- Visualization of bi-directional data integrations.

We invite you to explore these new features and take your IoT solutions to the next level. Upgrade to EMQX Enterprise 5.1 today and unlock the full potential of your IoT data management.

<section class="promotion">
    <div>
        Try EMQX Enterprise 5.1 Now
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>


## New Architecture for Improved Reliability and Scalability

EMQX Enterprise 5.1 introduces a revolutionary architecture powered by the Mria cluster architecture. Our new groundbreaking architecture enables EMQX to handle billions of concurrent IoT connections. In our latest version, a single cluster will scale up to 23 nodes, supporting over 100 million MQTT connections. This represents a tenfold increase in access capacity, marking a significant improvement from the previous 4.x version.

Our enhanced architecture brings robust horizontal scalability and also ensures higher reliability. The unique core-replicant node pattern allows you to add or remove nodes without disrupting operations.  This ability to hot-swap nodes provides the flexibility to scale the number of nodes without interrupting business operations, improving scale and reducing operational costs. At the same time, the risks of node split-brain in large-scale deployments, where nodes are out of sync or processing conflicting data, are significantly reduced. 

![Mria Cluster Architecture Diagram](https://assets.emqx.com/images/206cf3dca10ecb1e8690612f13ec052c.png)

<center>Mria Cluster Architecture Diagram</center>

<br>

The benefits of this architecture are leveraged in [EMQX Cloud](https://site-ip.mqttce.com/en/cloud), our fully managed MQTT Cloud service. Our EMQX Kubernetes Operator implements this new architecture for improved automated deployment and scalability. 

For more information about the brand-new architecture, please refer to [Architecture](https://docs.emqx.com/en/enterprise/v5.0/deploy/cluster/mria-introduction.html) 

## MQTT over QUIC: The Next Generation of IoT Messaging

The [MQTT protocol](https://site-ip.mqttce.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is commonly used for messaging services in the IoT and Internet of Vehicles (IoV) applications. It is designed to work on top of a transport protocol that provides a reliable, ordered, and lossless stream of bytes in both directions. This reliable transport protocol guarantees that messages are delivered accurately and in the order they were sent. Traditionally, IoT applications apply MQTT over TCP-based protocols, such as raw TCP, TCP/TLS (for security), and WebSocket (for web browser adaption). However, there are limitations in scenarios where wireless networks do not provide consistent coverage, causing high latency and packet loss. MQTT over QUIC provides reliable messaging over wireless networks with poor connectivity or low bandwidth.

### What is QUIC

QUIC, initially developed by Google, was later adopted as a worldwide standard by the Internet Engineering Task Force (IETF). QUIC is the underlying transport protocol of the next-generation internet protocol HTTP/3. QUIC communicates over the UDP instead of the TCP protocol. Compared to TCP/TLS protocols, QUIC provides efficient and flexible transport layer capabilities while reducing connection overhead and message latency, it is well-suited for modern mobile internet like IoT and IoV.

### Why MQTT over QUIC

EMQX Enterprise is the first product that combines QUIC with the MQTT protocol. Through extensive customer service and technological exploration, we have observed that the features of QUIC perfectly address challenges common in IoT environments, such as weak network conditions and unstable network paths. As a result, we integrated QUIC into the transport layer of MQTT and designed unique message transmission mechanisms and management methods. This diagram shows the Application, Transport, and Network layers of the IP protocol stack when using MQTT over QUIC. Note that MQTT over QUIC uses UDP instead of TCP.

![MQTT over QUIC Protocol Layers](https://assets.emqx.com/images/60fc64f70bd64b983ca438a33beede2d.png)

<center>MQTT over QUIC Protocol Layers</center>

<br>

EMQX Enterprise 5.1 introduces MQTT over QUIC, a breakthrough solution that outperforms TCP/TLS in multiple comparative tests. This powerful combination addresses the challenges faced by IoT workflows that demand constant mobility, such as connected vehicles or devices with periodic sleep requirements.

MQTT over QUIC has undergone extensive testing and integration within the EMQX Enterprise user base, receiving positive feedback. As a member of OASIS, EMQ is also actively promoting the standardization of MQTT over QUIC. Customers in the connected vehicle and mobile data collection can leverage the latest developments and standardized protocols.

To learn more about MQTT over QUIC, please refer to: [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) 

## Transfer Large Files with MQTT

In IoT applications, alongside real-time data transmissions, there is often a need for offline bulk data transfer, such as audio, video, and images. To fulfill this need without using different protocols, EMQX Enterprise 5.1 introduces a dedicated extension feature for MQTT-based transfer of large files.

### Key Features

- Utilize the same MQTT connection as other business purposes, fully leveraging the existing client management system.
- Enable lightweight clients to handle large files by chunked transfer and surpass the MQTT protocol size limit (256MB).
- Allow clients to pause file transfers for higher-priority data transfers or resume transfers after network interruptions.
- Employ QoS, verification mechanisms, and retransmission protocols to guarantee the integrity of file transfers.
- Choose to save uploaded files to a designated local directory or compatible object storage, such as S3, for future use and easy retrieval.

### Use Cases

- **Connected Vehicles:** Bulk Upload of Vehicle Telemetry Data

  Enable bulk upload of vehicle telemetry data, addressing network issues that hinder immediate transmission and facilitating data batch uploads to cloud platforms or data centers.

- **Industrial Internet of Things (IIoT):** Unified Reporting of Unstructured Production Data

  Facilitate the unified reporting of unstructured production data, including text, images, and videos, from industrial environments to servers or cloud platforms.

- **Smart Cities and CCTV:** Transmission of Surveillance Images and Facial Recognition Files

  Efficiently transmit surveillance images and facial recognition files from devices to central servers for storage, analysis, and integration with higher-level services.

EMQX's MQTT-based file transfer functionality is designed for seamless integration without modifying existing clients and applications. Compared to HTTP/FTP protocols, MQTT has the advantage of low bandwidth consumption and minimal resource usage, enabling fast and efficient file transfers. The unified IoT data channel simplifies system architecture, reducing application complexity and maintenance costs.

## Accelerate Business Innovation with Bi-directional Data Integration and Rules Processing

EMQX incorporates advanced data integration capabilities through its rule engine and data bridging functionality. This allows real-time processing of IoT data and seamless integration with third-party data systems, including Kafka, AWS RDS, MongoDB, Oracle, and popular time series databases like TimescaleDB and InfluxDB.

In EMQX Enterprise 5.1, we have further improved these capabilities by visualizing data integration workflows. With easy-to-understand visualizations of your data integrations in our dashboard, you can achieve effortless application integration and drive business innovation.

### Visualizing Data Integration

In previous versions, configuring data integration involved working with SQL and rule actions, which required familiarity with SQL syntax. Managing and maintaining data processing and integration flows without visibility became challenging when dealing with numerous rules. This increased the development cost and configuration complexity. 

EMQX Enterprise 5.1 addresses these challenges by introducing a visual Flows page, where users can easily view the data processing rules and the integration with third-party data systems for each topic in our dashboard. 

Use our dashboard to monitor the status of each step of your data flow in real-time.

![Data Flow View](https://assets.emqx.com/images/62ec79a60cbb850b41e2d8c1aa4a12fd.png)

<center>Data Flow View</center>

<br>

### Efficient Data Processing with Custom Rules Engine

EMQX Enterprise 5.1 extends bi-directional data bridging capabilities. Devices can bridge data to external systems, while data from external sources like MQTT services or Kafka, can also be bridged to EMQX. After undergoing rule processing, the data is then sent to designated devices. What does this mean?  More efficient use of the network! Our EMQX rules engine will filter incoming messages and only publish the messages that you choose to deliver to clients. This unique rules engine can greatly reduce the amount of unnecessary data sent over the network.

This is perfect for cloud-to-device scenarios, enabling real-time processing of IoT data using a unified language while supporting continuous large-scale message delivery. The EMQX rules engine opens up new possibilities for IoT business development.

![Data Bridge and Rule Engine](https://assets.emqx.com/images/e410f207f9765a9323bc02ba0f6a70c4.png)

<center>Data Bridge and Rule Engine</center>

<br>


## Comprehensive Security for IoT Messages

With IoT in critical industries like transportation, power, oil, and industrial manufacturing, the need for enhanced data security has become paramount. The underlying infrastructure services must demonstrate exceptional stability and reliability. 

EMQX provides a comprehensive solution for IoT messaging security. In addition to using SSL/TLS for communication security and X.509 device authentication, EMQX Enterprise 5.1 includes CRL and OCSP Stapling authentication mechanisms to enhance the security and flexibility of authentication at the transport layer.

EMQX Enterprise 5.1 provides built-in client authentication, authorization, blacklisting, and connection jitter protection at the application layer. These features ensure the system only communicates with legitimate clients while mitigating potential security risks and abnormal connection behaviors.

All these security options can be easily configured through the Dashboard, eliminating the need for code development, ensuring higher development efficiency and stronger security.

Furthermore, the hot updates and patching capabilities of EMQX Enterprise 5.1 allow real-time fault repairs without disrupting business operations. This mechanism allows you to continuously reinforce security defenses while maintaining business availability, laying a solid foundation for a reliable, trusted, secure, and robust IoT system.

## Realtime Monitoring and Diagnostics

With a completely redesigned UI/UX, EMQX Enterprise 5.1 introduces a revamped Dashboard that enhances the visual experience and optimizes menu structures for different user roles. The new Dashboard seamlessly integrates real-time cluster status monitoring, streamlined functionality configuration, and advanced troubleshooting and diagnostics, providing a superior experience and enabling you to rapidly build IoT solutions tailored to your needs.

![Real-Time MQTT Cluster Overview](https://assets.emqx.com/images/cc6419f3a395a5910529b729d87a6234.png)

<center>Real-Time MQTT Cluster Overview</center>

## Conclusion

With unique capabilities including MQTT messaging over the QUIC protocol, a customizable rules engine, and real-time monitoring dashboard, EMQX Enterprise is the most innovative MQTT platform available.  

Ready to take your IoT solutions to the next level? Upgrade to EMQX Enterprise 5.1 today and unlock the full potential of your IoT data management.

<section class="promotion">
    <div>
        Try EMQX Enterprise 5.1 Now
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
