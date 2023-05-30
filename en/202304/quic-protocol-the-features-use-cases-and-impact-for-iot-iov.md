## What Is the QUIC Protocol? 

QUIC (Quick UDP Internet Connections) is a protocol Google has developed to improve the speed and reliability of web connections. It is designed to replace the Transmission Control Protocol (TCP) used in the current Internet infrastructure. QUIC is built on top of the User Datagram Protocol (UDP).

QUIC uses a combination of encryption and multiplexing to provide improved security and faster data transfer. It allows multiple streams of data to be sent over a single connection, reducing latency and improving throughput. QUIC also includes features such as congestion control and flow control to manage network congestion and ensure smooth data transmission.

The Internet Engineering Task Force (IETF) is standardizing QUIC, and major web browsers and servers are adopting it. QUIC has been shown to improve web page loading times and reduce the occurrence of disconnections compared to TCP, especially in high-latency and spotty networks such as mobile networks.

## What Are the Basic QUIC Protocol Features? 

Here is an overview of QUIC’s main features.

**Independent logical streams**

Independent logical streams are one of QUIC's core features. This means that multiple streams of data can be sent over a single connection with each stream processed independently. In contrast, TCP uses a single stream of data and requires each packet to be received and acknowledged in sequence. With independent streams, applications can send and receive data and manage resources like network bandwidth more efficiently.

**Consistent security** 

Another important feature of QUIC is that it provides end-to-end security. All data sent over QUIC is encrypted by default, and there is no option for clear text communication. This helps to protect against eavesdropping and other forms of attacks. QUIC uses the Transport Layer Security (TLS) protocol to establish and maintain secure connections and end-to-end encryption.

**Low latency**

The protocol is designed to reduce handshake latency for data to be sent and received between endpoints, which can be especially important in high-latency networks such as mobile networks. QUIC accomplishes this by minimizing the number of round trips required to establish a connection, and by allowing data to be sent in smaller packets. Existing Internet protocols often have a problem with latency, sometimes up to 300 or 400 milliseconds for round-trip time between the US and Europe. 

**Reliability**

QUIC provides reliable transmission capabilities based on UDP, and like TCP, it is a connection-oriented transport protocol. The QUIC protocol has packet loss recovery and retransmission capabilities during data transmission, which can ensure data integrity and accuracy. In addition, QUIC can ensure the order of data packets arriving, avoiding data errors caused by disorder. 

**Avoiding HOL Blocking**

QUIC addresses the issue of head-of-line blocking by allowing for multiple data streams. This enables messages from different applications to be delivered independently, avoiding the potential delay of messages waiting for a blocked application to be processed.

## What Are the 5 Common Use Cases of the QUIC Protocol?

As HTTP/3 and QUIC gain more popularity and are increasingly adopted, a variety of use cases are expected to emerge. These use cases encompass live and video streaming, video on demand, downloads, and web acceleration. Among the most encouraging application scenarios for these technologies are:

1. **Real-time web and mobile applications:** These applications, such as Web and mobile applications with voice and video communication, require low latency and reliable data transmission. QUIC's use of independent streams and congestion control mechanisms make it a good choice for these applications, as it enables data to be sent and received quickly and efficiently. In the multi-stream mode of the QUIC protocol, data transmission between different streams within the same connection is not affected.
2. **Communication with IoT devices:** IoT devices often use protocols such as TCP and MQTT for communication. However, these protocols can be prone to issues such as high latency and packet loss, especially in constrained environments. QUIC can provide a more reliable and efficient alternative, as it is designed to work well in high-latency and lossy networks. Its near-zero Round Trip Time (RTT) is important for improving network performance and ensuring a positive user experience.
3. **Internet of Vehicles and connected cars:** QUIC can greatly benefit the Internet of Vehicles (IoV) ecosystem. These systems rely on real-time data exchange to provide services like traffic management, vehicle tracking, and safety features. QUIC's low latency, multiplexing capabilities, and resilience to packet loss and packet reordering can ensure reliable and efficient communication between vehicles and infrastructure components. Additionally, QUIC's use of TLS encryption provides improved security for sensitive vehicular data.
4. **Cloud computing:** This involves the delivery of computing resources over the Internet. With QUIC, cloud applications can benefit from low latency and end-to-end encryption, which can improve the user experience and security.
5. **Payments and eCommerce applications:** These apps require secure and reliable data transmission. QUIC's use of Transport Layer Security (TLS) encryption and reliable HTTP3 streams make it a good choice for these applications, as it helps to ensure data is transmitted securely and without an interception. From the end-user perspective, the QUIC protocol also improves the user experience by ensuring faster, seamless transactions.

## What Is MQTT and What are the Benefits of Running it Over QUIC?

MQTT is a lightweight messaging protocol specifically designed for situations where low bandwidth, high latency, or unreliable networks are common. It operates at the application layer and is primarily used for machine-to-machine (M2M) communications and Internet of Things (IoT) scenarios. MQTT uses a publish-subscribe model, which allows devices to send messages (publish) to a central broker, and other devices to receive those messages (subscribe) based on specified topics.

While QUIC is focused on improving the performance and security of web-based applications, MQTT is tailored towards providing a lightweight and efficient messaging solution for resource-constrained environments. Running MQTT over QUIC could significantly improve performance and reduce latency, and provide improved performance without the need for the additional overhead of Transport Layer Security (TLS). As the QUIC stack implementations are mostly done in userspace, data transmission of QUIC can be customized to adapt to various network environments based on the specific requirements of the application layer.

## MQTT Over QUIC vs. MQTT Over TCP/TLS 

MQTT over TCP/TLS refers to the use of the MQTT protocol over the Transmission Control Protocol (TCP) as the transport layer. TCP is a reliable, connection-oriented protocol that ensures the proper delivery of data packets between devices. TLS (Transport Layer Security) is a cryptographic protocol that provides secure communication over a network by encrypting the data transmitted between two endpoints. TLS is typically implemented as a layer on top of TCP, which means it uses TCP to establish and maintain a connection between two endpoints before encrypting the data transmitted over that connection. 

![MQTT Over QUIC vs. MQTT Over TCP/TLS ](https://assets.emqx.com/images/ece7636c5d911d7b59761528452dee8d.png)

MQTT over QUIC provides significant advantages compared to MQTT over TCP/TLS: 

**Connection establishment:**

- MQTT over TCP/TLS: MQTT over TCP/TLS applies TLS1.2 spec, which need two handshakes, one handshake is on the TCP layer and another on the TLS layer to complete. That means it requires two to three round trips before the application layer could start to exchange the data.
- MQTT over QUIC: MQTT over QUIC applies TLS1.3 spec, which enables faster connection establishment using a zero or one round-trip time (0-RTT or 1-RTT) handshake, reducing latency during connection setup.

**Latency and performance:**

- MQTT over TCP/TLS: Provides reliable data transfer, but TCP's head-of-line blocking and congestion control mechanisms can lead to increased latency and reduced performance, especially over unreliable networks.
- MQTT over QUIC: Combines the reliability of TCP with the low-latency characteristics of UDP. QUIC's stream multiplexing feature helps minimize head-of-line blocking issues, leading to improved performance over lossy or high-latency networks.

**Security:**

- MQTT over TCP/TLS: To secure MQTT communication, it is often combined with TLS, which adds encryption and authentication. However, this requires additional overhead during connection setup and data transmission.
- MQTT over QUIC: QUIC has built-in encryption using TLS1.3, providing secure communication without the need for additional setup steps or overhead.

**Connection migration for moving clients:**

- MQTT over TCP/TLS: If an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or server changes its IP address or network, the existing TCP connection must be disconnected and reestablished, causing a disruption in communication.
- MQTT over QUIC: Supports connection migration, allowing clients or servers to change IP addresses or networks without disrupting the ongoing communication.

 **Adoption and support:**

- MQTT over TCP/TLS: Widely adopted and supported by various [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), clients, and libraries across different platforms and programming languages.
- MQTT over QUIC: As of now, MQTT over QUIC is not as widely supported or adopted, as QUIC is still an emerging protocol.

***Learn more in our detailed guide to QUIC vs TCP (coming soon)***

## MQTT Over QUIC Use Cases in IoV

MQTT over QUIC can be beneficial in the Internet of Vehicles (IoV) use cases, where low-latency, reliable, and secure communication is essential for various applications. As QUIC combines the best features of TCP and UDP while offering built-in encryption, it can improve the performance and security of MQTT-based IoV applications.

Some use cases for MQTT over QUIC in the Internet of Vehicles include:

- **Vehicle-to-Infrastructure (V2I) communication**: QUIC's low-latency and reliable data transmission can enhance the efficiency of communication between vehicles and infrastructure components, such as traffic signals, toll systems, or smart parking systems.
- **Vehicle-to-Vehicle (V2V) communication:** Fast and secure data exchange is crucial for applications like collision avoidance, cooperative adaptive cruise control, and platooning. MQTT over QUIC can provide the necessary speed and security for these applications.
- **Vehicle-to-Everything (V2X) communication**: Combining vehicles, infrastructure, and other road users, V2X communication aims to increase road safety and traffic efficiency. MQTT over QUIC can provide reliable communication with reduced latency, ensuring timely exchange of critical information.
- **In-vehicle infotainment and telematics**: MQTT over QUIC can improve the performance of infotainment systems, allowing for faster media streaming, navigation updates, and real-time traffic information, while ensuring secure communication.
- **Fleet management and tracking**: Real-time tracking and management of fleets require efficient communication between vehicles and management systems. MQTT over QUIC can provide reliable and secure communication, enabling real-time updates on vehicle location, diagnostics, and driver behavior.
- **Over-the-Air (OTA) updates**: Secure and reliable OTA updates are essential for updating vehicle firmware and software. MQTT over QUIC can provide the necessary security and reliability for delivering these updates without disrupting vehicle operation.
- **Emergency response**: In emergency situations, reliable and fast communication is critical. MQTT over QUIC can ensure timely and secure exchange of information between emergency vehicles, response teams, and control centers.

## EMQX: Leading the Way as the First MQTT Broker to Implement MQTT Over QUIC

[EMQX](https://www.emqx.io/) is a world leading [open-source MQTT broker](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023) with a high-performance real-time message processing engine, powering event streaming for IoT devices at massive scale. Starting from version 5.0, EMQX became the first MQTT broker to support MQTT over QUIC, providing a more efficient and secure way of transmitting MQTT messages over modern complex networks, and improving MQTT's performance in certain scenarios.

The current implementation of EMQX support replaces the transport layer with a QUIC stream where the client initiates the connection and creates a bidirectional stream. EMQX supports two operating modes:

- **Single Stream Mode** is a basic mode that encapsulates MQTT packets in a single bidirectional QUIC stream. It provides a fast handshake, ordered data delivery, connection resumption and 0-RTT, client address migration, and enhanced loss detection and recovery. This mode enables faster and more efficient communication between the client and the broker while maintaining order, resuming connections quickly, and allowing clients to migrate their local addresses without major disturbances.
- **Multi-Stream Mode** leverages the stream multiplexing feature of QUIC, allowing MQTT packets to be transported over multiple streams. This enables a single [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) to carry multiple topic data and provides several improvements, such as decoupling connection control and MQTT data exchange, avoiding head of line blocking, splitting uplink and downlink data, prioritizing different data, improving parallelism, enhancing robustness, allowing flow control data streams, and reducing subscription latency.

![Single Stream Mode and Multi-Stream Mode](https://assets.emqx.com/images/e69cd596d2785e21afc9b4551fed3211.png)

**Using the NanoSDK client to connect with MQTT over QUIC**

[NanoSDK](https://github.com/nanomq/NanoSDK/) is the first SDK for MQTT over QUIC based on C, and it's fully compatible with EMQX 5.0. The key features of the NanoSDK include: the asynchronous I/O, the mapping of the MQTT connection to a QUIC stream, the 0-RTT handshake with low latency, and the parallel processing of multiple cores.

![NanoSDK](https://assets.emqx.com/images/43f6784fc10cf5c756e1f5eb807317a2.png)

EMQX also provides client SDKs to support MQTT over QUIC in multiple programming languages:

- [NanoSDK-Python](https://github.com/wanghaEMQ/pynng-mqtt): The Python binding of NanoSDK.
- [NanoSDK-Java](https://github.com/nanomq/nanosdk-java): The Java JNA binding of NanoSDK.
- [emqtt - Erlang MQTT Client](https://github.com/emqx/emqtt): A MQTT client library, developed in Erlang, supporting QUIC.

**Next steps:**

- [Learn more](https://docs.emqx.com/en/enterprise/v5.0/mqtt-over-quic/introduction.html#mqtt-over-quic) about the EMQX solution for MQTT over QUIC
- [Read our detailed blog post](https://www.emqx.com/en/blog/getting-started-with-mqtt-over-quic-from-scratch) to get started with MQTT over QUIC


### Join Our Webinar on MQTT & QUIC: A New Standard for Connected Vehicles

Connected cars are revolutionizing the automotive industry by providing drivers with advanced features and functions that were not possible before. However, these vehicles face the challenge of transmitting crucial vehicle data in complex network environments. To address this issue, this upcoming webinar presents a cutting-edge solution: MQTT messaging over the QUIC transport protocol and how the combination of these two can improve connectivity and communication for connected vehicles.

[![A New Standard for Connected Vehicles](https://assets.emqx.com/images/4a96d320830d21aa3bb7464005d3f62c.png)](https://www.emqx.com/en/events/mqtt-over-quic-a-new-standard-for-connected-vehicles)


Don’t miss our upcoming webinar on June 21st, where you can gain valuable insights into how MQTT and QUIC are helping build the next generation of connected vehicles.

Register now to [secure your spot](https://www.emqx.com/en/events/mqtt-over-quic-a-new-standard-for-connected-vehicles)!



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
