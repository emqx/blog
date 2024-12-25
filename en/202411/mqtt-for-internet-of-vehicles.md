The Internet of Vehicles (IoV) is a broad term encompassing the entire ecosystem of connected vehicles, including communication between cars, infrastructure, and cloud systems. However, Connected Cars, the specific application of IoT technologies within vehicles themselves, is gaining widespread attention due to the growing demand for smarter, more secure transportation solutions.

For many years, EMQ, a global leader in edge-cloud data connectivity and MQTT platform solutions, has been enabling the development of IoT platforms for Connected Cars. By providing cloud-edge collaboration solutions, EMQ has helped vehicle manufacturers, Tier 1 suppliers, service providers, and mobility companies create integrated, intelligent systems that link people, vehicles, roads, and clouds. This integration paves the way for autonomous driving, V2X (Vehicle-to-Everything) communication, and other innovative use cases in the Connected Car ecosystem.

> Related content: [What is a Connected Car? All You Need to Know](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know)

In this series, we will explore how to build a reliable, efficient, and industry-specific IoV platform, drawing from EMQ’s extensive experience in the field. We will cover everything from theoretical aspects like protocol selection to practical operations such as platform architecture design.

## **Introduction to MQTT in Connected Cars**

The [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) has long been the standard for lightweight, efficient, and reliable communication in IoT. With its widespread adoption across various industries, MQTT has proven to be ideal for the real-time messaging needs of Connected Cars. But how does it specifically benefit this sector?

This article compares different IoT communication protocols and explain why MQTT stands out for developing reliable, scalable, and secure platforms for connected vehicles. We’ll also provide insights into selecting the right MQTT products and services, as well as popular technical solutions in the automotive industry.

## Why MQTT is Ideal for Connected Cars

Connected Car systems involve complex business architectures with multiple communication links. Here, we will focus on device-to-cloud messaging, which is the core responsibility of IoV platforms.

MQTT is an IoT protocol based on the publish/subscribe model. Its key advantages include:

- **Open Protocol:** Simple to implement with widespread support through mature software libraries and hardware modules.
- **Flexible Messaging:** Supports large-scale deployments with customizable topics and subscriptions, allowing for diverse IoV use cases.
- **Efficient Payload:** Compact message structure reduces network traffic, which is critical in large-scale IoV systems.
- **Multiple QoS Levels:** Offers three QoS levels to adapt to different vehicle network environments.
- **Session Management:** Provides online state awareness and retains offline messages for enhanced reliability.

In IoV scenarios, MQTT enables flexible, fast, and secure connections for large fleets of vehicles, ensuring real-time messaging reliability even in complex network environments.

If the MQTT protocol is used together with messaging broker products that can handle mass vehicle connections, soft real-time and high concurrent data throughput, and multiple security guarantee capabilities, MQTT protocol will undoubtedly bring convenience to the building an IoV platform.

## Why MQTT Outperforms Other Protocols for Connected Cars 

While other protocols like **private TCP** and **HTTP** have been used in IoV systems, **MQTT** has proven to be the most effective for Connected Cars. Let’s look at a couple of examples to highlight the advantages of switching to MQTT.

**Case 1: Overcoming Limitations of Private TCP**

A large-scale automotive OEM (Original Equipment Manufacturer) in South China initially adopted a privatized TCP protocol for their IoV platform. While this approach met initial needs, it became increasingly difficult to manage as the number of vehicles grew, leading to higher maintenance costs and slower system updates. The private protocol required extensive custom development for each vehicle model, making it unsustainable for a growing business.

**Issues with private protocols include:**

- Difficulties in maintaining and versioning proprietary protocols.
- Custom development for basic features such as connection stability, reconnection, and offline messaging.
- High costs and lengthy development cycles.

Switching to MQTT has enabled the OEM to reduce development costs, improve system scalability, and enhance operational efficiency. Today, they are transitioning all models to MQTT, with many already upgraded via OTA (over-the-air) updates.

**Case 2: Scaling Up with MQTT**

Another vehicle enterprise client initially used an in-house HTTP service for their simpler IoV needs. However, as the business grew and the platform expanded, the traditional HTTP request-response model became a bottleneck. As the traffic volume increased, the system’s performance suffered. Eventually, the company migrated to MQTT to resolve scalability and reliability issues, using EMQX’s data access solutions for seamless integration.

In both examples, the limitations of proprietary protocols and HTTP were overcome by adopting **MQTT**, which naturally scales to meet the growing demands of Connected Car ecosystems.

## Choosing the Right MQTT Product for Connected Cars

Selecting the right MQTT product or service is crucial for developing a Connected Car platform that is secure, scalable, and cost-effective. Key factors to consider include:

- **Performance & Scalability**: Ensure the MQTT solution can handle the massive volume of messages and vehicle connections typical in IoV systems.
- **Cost Efficiency**: Factor in the total cost of ownership, including infrastructure, integration, and maintenance costs.
- **Global Deployment**: For businesses with international operations, choose an MQTT product that supports global scalability and complies with regional regulations.
- **Vendor Lock-in**: A flexible MQTT solution that can be deployed across different cloud platforms without locking you into a single vendor is critical for long-term success.

## EMQX: The Ideal MQTT Platform for Connected Cars

When it comes to building robust, scalable, and secure Connected Car platforms, EMQX stands out as an ideal choice. As an enterprise-grade MQTT platform, EMQX offers powerful features tailored for the automotive industry, providing significant advantages for both OEMs and service providers in the IoV sector:

- **High Scalability:** EMQX is designed to handle massive connections—millions of vehicles can be supported simultaneously without compromising performance. This makes it perfect for Connected Cars, which require high scalability to accommodate the increasing number of connected devices and growing data volume.
- **Reliability & Low Latency**: EMQX’s low-latency messaging ensures real-time communication between vehicles, cloud systems, and infrastructure. This is essential for applications like autonomous driving and V2X communication, where split-second decisions can make a difference.
- **Comprehensive Security**: With built-in TLS encryption, role-based access control, and advanced authentication features, EMQX ensures that data exchanged between vehicles and platforms remains secure from unauthorized access or tampering.
- **Cloud & Edge Collaboration**: EMQX supports cloud-edge collaboration, enabling data processing both in the cloud and at the edge of the network. This is crucial for reducing latency and enhancing the performance of time-sensitive applications, such as vehicle diagnostics or predictive maintenance.
- **Cost-Effective & Flexible Deployment:** EMQX provides flexible deployment options—whether you choose on-premises for full control or cloud service for a fully managed solution. This flexibility helps to manage costs effectively while maintaining control over the platform’s operation.

**Case Study: SAIC Volkswagen Adopts EMQX for IoV Platform**

In 2018, SAIC Volkswagen, one of leading automotive manufacturers, chose EMQX for their new IoV  platform. The company needed a messaging solution capable of handling millions of connected vehicles while ensuring real-time communication and scalability.

By switching to EMQX and adopting the MQTT protocol, SAIC Volkswagen achieved:

- **Scalability**: The platform easily scaled to support millions of connected vehicles.
- **Real-time data transmission**: Ensured low-latency communication for critical IoV applications.
- **Cost savings**: Reduced development costs, thanks to EMQX's powerful data integration capability.

This adoption helped SAIC Volkswagen build a robust IoV platform that can handle future growth and evolving technology needs.

>Learn more: [SAIC Volkswagen and EMQ create a new generation of intelligent Internet of Vehicles systems](https://www.emqx.com/en/customers/saic-volkswagen)

## Key Technical Solutions for Connected Cars

As a powerful MQTT platform, EMQX provides rich and flexible integration capabilities, and each feature provides different technical solutions for users to choose, including:

### Security Assurance

At the transport link layer, we recommend enabling TLS-encrypted transmission. However, many cloud providers' load balancers lack TLS termination support, so additional components like HAProxy are needed for this purpose.

TBox access typically uses certificate authentication, and EMQX provides an extensible authentication chain that supports third-party platforms like PKI systems, as well as username/password and internal database authentication.

Additionally, EMQX authentication allows users to assign specific publish and subscribe permissions to different TBox terminals, enhancing data security.

![EMQX Security assurance](https://assets.emqx.com/images/4ff574a38707a1a8160882dca8cd16e7.png)

### Data Integration

Customers attach great importance to the ability to connect the massive data of IoV through EMQX with business systems. EMQX has a built-in rule engine and data bridging capability, which can [stream MQTT data to Kafka](https://www.emqx.com/en/blog/mqtt-and-kafka), and various SQL/ NoSQL/ time-series databases. Most customers in actual projects use Kafka as the back-end stream processing component.

Kafka focuses on data storage and reading, while EMQX focuses on communication between client and server. EMQX is used to quickly receive and process messages from a large number of IoT devices. Kafka can collect and store this data and send it to back-end programs for analysis and processing. This architecture is the most widely used data integration scheme at present.

![EMQX Data integration](https://assets.emqx.com/images/382114e90c6a728659ac9316b73ddd60.png)

### MQTT over QUIC for Efficient Messaging

EMQX is the first [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to support [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), providing a more efficient and secure way of transmitting MQTT messages over modern complex networks. MQTT over QUIC can be beneficial in the IoV use cases, where low-latency, reliable, and secure communication is essential for various applications. As QUIC combines the best features of TCP and UDP while offering built-in encryption, it can improve the performance and security of MQTT-based IoV applications. Some customers have already tried to use this new feature, and we have received good feedback.

## **Conclusion: MQTT and EMQX Drive the Future of Connected Cars**

As the automotive industry continues to evolve with Connected Cars, the need for reliable, scalable, and secure communication platforms is more critical than ever. MQTT and EMQX are central to enabling the seamless connectivity and data integration required for modern vehicle systems. With the growth of intelligent transportation and the rise of autonomous vehicles, EMQ is committed to providing innovative solutions that power the future of Connected Cars and IoV systems.

By leveraging MQTT's flexibility and the robust capabilities of EMQX, developers can build platforms that not only meet the current needs of the industry but also scale to support the future of connected, intelligent transportation.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
