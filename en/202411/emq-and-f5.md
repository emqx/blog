## Introduction

With the rapid advancement of IoT technology and its widespread adoption across industries, the need for secure, scalable solutions to handle massive device connectivity and rapidly growing data flows has become critical. To meet this demand, EMQ, a global leader in edge-cloud data connectivity and MQTT platform solutions, and F5, a market leader in application delivery and security solutions, have together developed a secure data access solution for emerging IoT scenarios. This solution enables reliable device connectivity and secure data transmission for mission-critical IoT applications, ensuring the efficient operation of enterprise intelligent systems.

## EMQ & F5: Building a Scalable, Secure Data Access Solution

### EMQX Platform: High-Concurrency and Reliable IoT Connectivity

The [EMQX Platform](https://www.emqx.com/en/products/emqx), an enterprise-grade MQTT IoT platform developed by EMQ, is designed for large-scale deployments and high reliability in IoT applications like connected vehicles, industrial IoT, and AIoT. EMQX enhances data access and management through key capabilities:

- **High Reliability and Scalability**: Built on a distributed architecture, EMQX provides high availability and scalability to handle large-scale concurrent message transmission. It supports horizontal scaling to accommodate increasing IoT devices and data traffic, ensuring system stability.
- **Extensive Protocol Support**: Beyond [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), EMQX supports multiple messaging protocols, allowing developers to expand capabilities to various proprietary protocols as needed.
- **Flexible Data Integration**: EMQX seamlessly integrates with diverse data storage services, message queues, cloud platforms, and applications. It enables cloud connectivity for remote data transmission and cloud-based analytics.
- **Security and Authentication**: EMQX offers robust security features like TLS/SSL encryption, client authentication, and access control, supporting authentication methods like username/password, X.509 certificates, and OAuth to ensure secure IoT communications.
- **Rule Engine and Data Processing**: EMQX includes a versatile rule engine for real-time data processing and forwarding based on device data, supporting filtering, transformation, aggregation, and persistence to facilitate analysis and decision-making.
- **Visual Monitoring and Management**: EMQX provides an intuitive interface for real-time monitoring of IoT devices and message transmission, allowing users to track connection status, message flow, and other metrics while managing devices, troubleshooting, and configuring systems.

### NGINX Plus & BIG-IP: Enterprise-Grade Traffic Management and Load Balancing

NGINX Plus is an all-in-one API gateway, content cache, load balancer, and web server launched by F5. As the enterprise version of the high-performance open-source NGINX server, it provides scalable and reliable high availability with monitoring to support debugging and diagnosing complex application architectures, with active health checks and an integrated live activity dashboard.

BIG-IP, F5’s flagship product, provides load balancing, web application firewall capabilities, SSL termination, dynamic load balancing, and global server load balancing. Recognized as the current leader for application security and delivery, BIG-IP TMOS delivers a comprehensive suite of highly programmable and automatable app services for hybrid and multicloud workloads. Building on this strong foundation, BIG-IP Next has been rearchitected and reimagined to meet the demands of the next generation of applications and BIG-IP users.

### Unified Data Access and Load Balancing with EMQX, NGINX Plus, and BIG-IP

![EMQX with NGINX Plus and BIG-IP](https://assets.emqx.com/images/bec5888d8c37a99e213c7ca6fabb2b74.png)

Combining EMQX with NGINX Plus and BIG-IP creates a unified solution integrating load balancing with MQTT message access. This solution offers MQTT load capacity and enhanced MQTT cluster performance via SSL offloading, delivering key benefits like:

- **Flexible Global Sever Load Balancing (GSLB)**: Intelligent monitoring of distributed cluster loads dynamically routes user requests to the optimal node, with automatic failover to ensure service continuity and high reliability.
- **TLS, DTLS, and GMSSL Certification**: Comprehensive security authentication meets diverse regional and industry requirements.
- **Sticky Sessions and TCP Connection Migration**: Minimizes disruptions during system upgrades, scaling, or node failures, improving user experience.
- **Information Security and Session Logging**: Integrates robust logging and analysis for comprehensive system auditing, aiding compliance efforts.
- **MQTT over QUIC Load Balancing**: With the innovative [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), the solution enables reliable, low-latency connections suited to complex network environments and high-demand scenarios like connected vehicles.

This joint solution provides scalable data access, robust traffic management, and secure data delivery, enabling enterprises to build more stable and secure IoT platforms and applications.

## Real-World Applications

### Stable Data Interaction for Connected Vehicles and Smart Factories

In connected vehicles and industrial IoT, devices are widely distributed and require strict real-time data transmission. The joint solution offers Global Server Load Balancing (GSLB) capabilities, monitoring load across distributed clusters and routing traffic to the closest node based on user requests in each region. This setup ensures low-latency data transmission.

For example, in connected vehicles, real-time communication with the nearest server is crucial for functions like navigation, remote diagnostics, and fleet management. If a service node fails, GSLB automatically redirects requests to other nodes, ensuring stable and reliable data transmission. This functionality also supports high-performance, stable connectivity and monitoring in data-intensive scenarios such as smart factories and energy IoT, optimizing business continuity and service quality.

![Stable Data Interaction for Connected Vehicles](https://assets.emqx.com/images/2a4056675e3949391586d4a928a83801.png)

### Seamless Upgrades and Scaling for Critical Business Continuity

In large-scale connected vehicles and smart manufacturing environments, frequent system upgrades and IT resource expansions are common. Traditional solutions often cause brief connection disruptions during these processes, affecting customer experience and critical business continuity.

The solution offers TCP Connection Migration, enabling minimal to zero connection interruptions during system upgrades and scaling. Using BIG-IP's full-proxy architecture, a client-server connection is split into client-to-load-balancer and load-balancer-to-server connections. With its Message Routing Framework (MRF), BIG-IP acts as a message router, identifying and routing messages within the TCP session, handling and forwarding MQTT messages. This capability allows for smooth MQTT server scaling, seamless failover, and service decommissioning, ideal for scenarios demanding high stability and availability.

 ![Seamless Upgrades and Scaling](https://assets.emqx.com/images/5e6f5bc17ea0118ae4482d20c9c1395f.png) 

### Efficient Communication for Connected Vehicles in Complex Networks

In environments with unstable signals, such as highways or remote areas, connected vehicle communication must overcome network fluctuations to maintain fleet management, remote driver assistance, and infotainment continuity. 

EMQ’s pioneering MQTT over QUIC technology provides a low-latency, highly reliable communication protocol for these scenarios, maintaining stable data transmission despite network variability. Combined with F5’s expertise in load balancing, the joint solution not only ensures rapid packet forwarding to the nearest server but also enhances communication continuity during network transitions. This makes it ideal for high-speed vehicles, vehicle-to-road coordination, and remote area communication. Together, they enable large-scale, efficient connected vehicle communication, enhancing safety and efficiency in transportation systems.

![Efficient Communication](https://assets.emqx.com/images/1e31b9a62d86a8d6bf1824c9b2d0abe8.png)

![MQTT over QUIC](https://assets.emqx.com/images/fb809fcd39ef74109e6530fe1a58f4ca.png)

 

## Conclusion

The joint solution from EMQ and F5 combines EMQX Platform's high-concurrency IoT access capabilities with F5’s leading load balancing and security technologies to deliver an integrated, scalable, high-performance data access solution for large-scale smart IoT applications. This solution ensures secure data transmission and system stability, providing reliable support for mission-critical scenarios in connected vehicles, industrial IoT, and AIoT.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
