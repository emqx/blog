## Introduction

Message Queuing Telemetry Transport (MQTT) is the standard messaging protocol for the Internet of Things (IoT). MQTT follows an extremely lightweight publish-subscribe messaging model, connecting IoT devices in a scalable, reliable, and efficient manner.

It's been over 20 years since MQTT was invented in 1999 by IBM and 10 years since we launched one of the most popular open-source [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), [EMQX](https://github.com/emqx/emqx), on GitHub in 2012.

As we move into 2023 and look forward to the years ahead, we can anticipate 7 developing trends in MQTT technology, as the use of [MQTT in IoT](https://www.emqx.com/en/blog/what-is-the-mqtt-protocol) is growing tremendously and diversely, driven by the progress of emerging technologies.

## MQTT over QUIC

[Quick UDP Internet Connections (QUIC)](https://en.wikipedia.org/wiki/QUIC) is a new transport protocol developed by Google that runs over UDP and is designed to reduce the latency associated with establishing new connections, increase data transfer rates, and address the limitations of TCP.

HTTP/3, the latest HTTP protocol version,  uses QUIC as its transport layer.  HTTP/3 has lower latency and a better loading experience on web applications than HTTP/2 due to the adoption of QUIC.

[MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) is the most innovative advancement in the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) since the first release of the MQTT 5.0 specification in 2017.  With multiplexing and faster connection establishment and migration,  it has the potential to become the next generation of the MQTT standard.

The MQTT 5.0 protocol specification defines three types of transport: TCP, TLS, and WebSocket. MQTT over TLS/SSL is widely used in production to secure communications between [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) and brokers, as security is a top priority for IoT applications. However, it is slow and has high latency, requiring 7 handshakes equal to 3.5 RTT, namely, 3 TCP and 4 TLS to establish a new [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).

**MQTT over QUIC**, with 1 RTT connection establishment and 0 RTT reconnection latency, is indeed faster and has lower latency compared to MQTT over TLS. The QUIC stack can be customized for various use cases, such as keeping connections alive in poor networking conditions and for scenarios where there is a need for low client-to-server latency. It will benefit connected cars with unreliable cellular networks and low-latency industrial IoT applications. The adoption of MQTT over QUIC is expected to play a vital role in the future of IoT, Industrial IoT (IIoT), and Internet of Vehicles (IoV).

[EMQX](https://github.com/emqx/emqx), the popular open-source MQTT broker, has introduced [MQTT over QUIC support ](https://www.emqx.com/en/blog/mqtt-over-quic)in its latest version, 5.0. And like HTTP/3, the next version of the MQTT protocol, MQTT 5.1 or 6.0, will use QUIC as its primary transport layer in the near future.

![MQTT over QUIC](https://assets.emqx.com/images/a172e1693e8b7c86ec51e5d69936a802.png)

> Learn more: [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic)

## MQTT Serverless

The serverless trend in cloud computing marks a groundbreaking paradigm shift in how applications are designed, developed, deployed and run. This paradigm enables developers to focus on their application's business logic instead of managing infrastructure, resulting in enhanced agility, scalability, and cost-effectiveness.

Serverless MQTT broker emerges as a cutting-edge architectural innovation for 2023. In contrast to traditional IoT architectures, which require minutes to hours for creating MQTT-hosted services on the cloud or deploying them on-premises, serverless MQTT enables rapid deployment of MQTT services with just a few clicks. Moreover, the true value proposition of serverless MQTT lies not in its deployment speed, but in its unparalleled flexibility.

This flexibility manifests in two key aspects: the seamless scaling of resources in response to user demands and the pay-as-you-go pricing model that aligns with this elastic architecture. As a result, serverless MQTT is poised to drive broader adoption of MQTT, reducing operational costs and spurring innovation and collaboration across diverse industries. We might even see a free serverless MQTT broker for every IoT and Industrial IoT developer.

In March 2023, EMQX Cloud launched the world's first [serverless MQTT service](https://www.emqx.com/en/cloud/serverless-mqtt), offering users not only an incredibly fast deployment time of just 5 seconds, but also the exceptional flexibility that truly sets serverless MQTT apart.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


## MQTT Multi-tenancy

Multi-tenancy architecture is the vital aspect of serverless MQTT broker. IoT devices from different users or tenants can connect to the same large-scale MQTT cluster while keeping their data and business logic isolated from other tenants.

SaaS applications commonly use multi-tenancy architecture, where a single application serves multiple customers or tenants. There are usually two different ways to implement multi-tenancy in SaaS, such as:

- **Tenant Isolation**: A separate application instance is provided to each tenant, running on a server or virtual machine.
- **Database Isolation:** Multiple tenants can share a single application instance, but each tenant has their database schema to ensure data isolation. 

In the multi-tenancy architecture of the MQTT broker, each device and tenant is given a separate and isolated namespace. This namespace includes a unique topic prefix and access control lists (ACLs) that define which topics each user can access, publish to, or subscribe to.

MQTT broker with multi-tenancy support will reduce management overhead and allow greater flexibility for complex scenarios or large-scale IoT applications. For example, departments and applications in a large organization could use the same MQTT cluster as different tenants.

> Learn more: [Multi-Tenancy Architecture in MQTT: Key Points, Benefits, and Challenges](https://www.emqx.com/en/blog/multi-tenancy-architecture-in-mqtt)

## MQTT Sparkplug 3.0

MQTT Sparkplug 3.0 is the latest version of the [MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0), the open standard specification designed by Eclipse Foundation. It defines how to connect industrial devices, including sensors, actuators, Programmable Logic Controllers (PLCs), and gateways using MQTT messaging protocol.

MQTT Sparkplug 3.0 was released in November 2022 with some key new features and improvements:

1. MQTT 5 Support: MQTT Sparkplug 3.0 adds support for the MQTT 5 protocol, which includes several new features such as shared subscriptions, message expiry, and flow control.
2. Optimized Data Transmission: MQTT Sparkplug 3.0 includes several optimizations for data transmission, including the use of more compact data encoding and compression algorithms. 
3. Expanded Data Model: MQTT Sparkplug 3.0 introduces an expanded data model, which allows for more detailed device information to be communicated, as well as additional information such as configuration data and device metadata.
4. Improved Security: MQTT Sparkplug 3.0 includes several improvements to security, including support for mutual TLS authentication and improved access control mechanisms.
5. Simplified Device Management: MQTT Sparkplug 3.0 includes several improvements to device management, including automatic device registration and discovery, simplified device configuration, and improved diagnostics.

MQTT Sparkplug aimed to simplify connecting and communicating with disparate industrial devices and achieve efficient industrial data acquisition, processing, and analysis. As the new version is released, MQTT Sparkplug 3.0 has the potential to be more widely adopted in the Industrial IoT.

> Learn more: [Sparkplug 3.0: Advancements & Formalization in MQTT for IIoT](https://www.emqx.com/en/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot)

## MQTT Unified Namespace

[Unified Namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) is a solution architecture built on the MQTT broker for Industrial IoT and Industry 4.0. It provides a unified namespace for MQTT topics and a centralized repository for messages and structured data. 

Unified Namespace connects industrial devices, sensors, and applications, such as SCADA, MES, and ERP, with star topology using a central MQTT broker. Unified Namespace dramatically simplifies the development of industrial IoT applications with an event-driven architecture.

In traditional IIoT systems, OT and IT systems have generally been separate and operated independently with their data, protocols, and tools. By adopting Unified Namespace, it is possible to allow OT and IT systems to exchange data more efficiently and finally unify the OT and IT in the IoT era.

![MQTT Unified Namespace](https://assets.emqx.com/images/4bd773c5f0197e690c0c819f75940d95.png)

In 2023, with [EMQX](https://www.emqx.io/) or [NanoMQ](https://nanomq.io/) MQTT broker empowered by [Neuron](https://neugates.io/) Gateway, the latest open source IIoT connectivity server, building a UNS architecture empowered by the most advanced technology from the IT world is just within grasp.

>Learn more: [Unified Namespace (UNS): Next-Generation Data Fabric for IIoT](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot)


## MQTT Geo-Distribution

MQTT Geo-Distribution is an innovative architecture that allows MQTT brokers deployed in different regions or clouds to work together as a single cluster. Using Geo-Distribution, MQTT messages can be automatically synchronized and delivered across MQTT brokers in different regions. 

In 2023, we can expect two approaches to implementing MQTT Geo-Distribution:

- Single Cluster, Multi-Region: A single MQTT cluster with brokers running in different regions.
- Multi-Cluster, Multi-Cloud: Multiple MQTT clusters connected with Cluster Linking in different clouds.

We can combine the two approaches to create a reliable IoT messaging infrastructure across geographically distributed MQTT brokers. By adopting the MQTT Geo-Distribution, organizations can build a **Global MQTT Access Network** across multi-cloud, where devices and applications connected locally from the closest network endpoint can communicate with each other regardless of their physical location.

![MQTT Geo-Distribution](https://assets.emqx.com/images/8d37c93155161dc872b657673d028372.png)

## MQTT Streams

MQTT Streams is an expected extension of the MQTT protocol that enables the handling of high-volume, high-frequency data streams in real-time within an MQTT broker. This feature enhances the capabilities of traditional MQTT brokers, which were originally designed for lightweight publish/subscribe messaging. With MQTT Streams, clients can produce and consume MQTT messages as streams, similar to how Apache Kafka works. This allows for historical message replay, which is essential for event-driven processing, ensuring ultimate data consistency, auditing, and compliance.

Stream processing is crucial for extracting real-time business value from the massive amounts of data generated by IoT device sensors. Previously, this required an outdated, complex big data stack involving the integration of an MQTT broker with Kafka, Hadoop, Flink, or Spark for IoT data stream processing.

However, with built-in stream processing, MQTT Streams streamlines the IoT data processing stack, improves data processing efficiency and response time, and provides a unified messaging and streaming platform for IoT. By supporting features such as message deduplication, message replay, and message expiration, MQTT Streams enables high throughput, low latency, and fault tolerance, making it a powerful tool for handling real-time data streams in MQTT-based IoT applications.

## Conclusion

Overall, these 7 trends in MQTT technology reflect the progress of emerging technologies and their role in advancing the IoT. As a standard messaging protocol evolved for over two decades, MQTT’s importance continues to grow. With the increasing use of IoT in various industries, the MQTT protocol is evolving to meet new challenges and demands, such as faster and lower-latency connections, more rapid deployment of MQTT services, greater flexibility for complex scenarios or large-scale IoT applications, and more support on connecting various industrial devices. With these developments, MQTT will become the nerve system of IoT and an even more crucial player in IIoT and IoV in 2023 and beyond.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
