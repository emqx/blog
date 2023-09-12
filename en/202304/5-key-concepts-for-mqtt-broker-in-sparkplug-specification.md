## Introduction

Sparkplug is an industrial IoT communication protocol designed for use in SCADA systems. It provides a standard communication format for industrial devices and applications, making devices from different manufacturers interoperable. The Sparkplug specification was developed by Cirrus Link Solutions and Eclipse Foundation. It is openly available and not proprietary to a single company. So, it has the following benefits for the Sparkplug community:

- Allowing different systems and technologies to work together seamlessly, improving efficiency, reducing costs, and providing more options to consumers.
- Ensuring that products from different vendors can work together without any compatibility issues, and increasing consumer choice, and fostering healthy competition among vendors.
- Encouraging innovation by enabling collaboration and sharing ideas and solutions, thus leading to the development of new products, services, and technologies.
- Promoting transparency, increasing trust, and reducing the risk of vendor lock-in or dependence on a single supplier.
- Ensuring that products and services are accessible to a wide range of users, including those with disabilities.

Sparkplug aims to provide a standardized way to use [MQTT for industrial](https://www.emqx.com/en/use-cases/industrial-iot) applications and promote interoperability between devices and systems from different vendors. As such, the Sparkplug specification has been widely adopted by the industrial IoT community and is supported by many different vendors and organizations.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/0b88fa3cf1c98545e501e3b8073fdccc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Reference Architecture for Modern Manufacturing
    </div>
    <div class="mb-32">
      Amplify the power of MQTT Sparkplug.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-5-key-concepts-for-mqtt-broker-in-sparkplug" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Concept 1 - MQTT Messaging Architecture

The Sparkplug specification is based on the [MQTT protocol](https://www.emqx.com/en/mqtt-guide), a lightweight messaging protocol widely used in IoT applications. It is designed for low-bandwidth, high-latency networks and is adopted in IoT applications due to the following capabilities.

- Lightweight: MQTT is a lightweight protocol requiring minimal network bandwidth and is well-suited for low-bandwidth environments.
- Reliability: MQTT includes support for [Quality of Service (QoS)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos) levels, which ensure that messages are delivered reliably even in the face of network failures or intermittent connectivity.
- Scalability: MQTT is designed to be scalable and can [support millions of devices and clients](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0).
- Flexibility: MQTT can be used for one-to-one and one-to-many communication and supports both [publish/subscribe](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) and [request/response](https://www.emqx.com/en/blog/mqtt5-request-response) messaging patterns.
- Security: MQTT includes support for security features such as [authentication](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication) and encryption, which help to ensure that data is transmitted securely and confidentially.

Overall, using MQTT for implementing the Sparkplug specification provides a range of benefits that make it well-suited for industrial IoT applications. Most importantly, based on MQTT pub-sub messaging architecture, the Sparkplug system supports the decoupling of data producers and consumers. This approach enables a more flexible and scalable data exchange process, as the data producer and consumer can operate independently.

## Concept 2 - Session State Awareness

Decoupling can offer many benefits regarding scalability, flexibility, and resilience. Still, it requires careful attention to session management to ensure that the system maintains a coherent state across multiple requests and components.

Session state awareness is an essential feature of Sparkplug that allows devices to maintain a connection to a broker even when the network connection is interrupted or lost. This is accomplished through the use of session state information that is stored by the broker and used to re-establish communication when the connection is restored.

When a device connects to a Sparkplug broker, it establishes a session with the broker. During this session, the device can publish and subscribe to messages. The broker records the device's session state, including any subscriptions or messages not delivered due to a network interruption.

Session state awareness is a critical feature for mission-critical industrial IoT applications that require high availability and reliable communication. By maintaining session state information, Sparkplug ensures that devices can quickly re-establish communication with the broker after a network interruption, reducing the risk of downtime and data loss.

## Concept 3 - Unified Namespace

The [unified namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) is a concept that refers to the ability of different devices and systems in an industrial setting to share data seamlessly, regardless of their manufacturer or communication protocol. It uses a standard naming convention and data model to ensure interoperability and facilitate data exchange.

On the other hand, Sparkplug is a messaging specification to enable efficient and secure communication between IoT devices and applications. It is based on the MQTT protocol and incorporates the unified namespace concept to provide a standardized way of representing data and metadata across different devices and systems.

In other words, Sparkplug utilizes the unified namespace concept to provide a common language for data exchange between industrial devices and systems. This helps to simplify integration and improve interoperability, making it easier to build and maintain complex IoT applications in industrial environments.

## Concept 4 - Central Data Repository

In the context of the Sparkplug specification, a Central Data Repository (CDR) is a centralized server or platform that acts as a hub for receiving, processing, and distributing data from different industrial devices and applications. The CDR provides a standardized way to manage and store data in a scalable and efficient way and enables interoperability between different devices and connected applications.

The benefits of a CDR include the following:

- Improved data quality: A CDR ensures that all data is standardized and consistent across an organization, improving the accuracy and reliability of the data.
- Simplified data management: With all data stored in one place, it's easier to manage and maintain.
- Faster access to data: A CDR provides a centralized location for data, making it easier and faster to access and analyze.
- Reduced data redundancy: By eliminating redundant data, a CDR reduces storage costs and minimizes the risk of data inconsistencies.

The CDR is responsible for receiving MQTT messages from different devices and applications, parsing and validating the data, and storing it in a format easily accessed and processed by other systems. It also provides a set of APIs and interfaces that enable other systems to access and retrieve the data stored in the CDR, allowing it to send commands or instructions back to the devices and applications connected to it.

## Concept 5 - Single Source of Truth

Single source of truth (SSOT) is a concept commonly used in information management and refers to the idea that there should be one authoritative source of data for a particular piece of information. All data related to a specific topic, such as a customer order, product information, or production details, should be stored in a single location and maintained consistently.

Using an SSOT is also a key aspect of the Sparkplug specification, as it provides a standardized way to manage and store data consistently and reliably. Having a single source of truth makes it easier to ensure that all systems and applications have access to the most up-to-date and accurate information, which is essential for maintaining the integrity and reliability of the system.

In practice, the SSOT is often implemented as part of the CDR, which is responsible for receiving and processing data from different devices and applications. The CDR stores all data in a standardized format that can be easily accessed and processed by other systems and serves as the central point of control for managing and monitoring different devices and systems. By using a centralized SSOT, it is possible to achieve a high degree of interoperability between different devices and systems and to ensure that all systems have access to the same data and information.

## Conclusion

In the Sparkplug specification, an [MQTT broker](https://www.emqx.io/) is an indispensable component to incorporate the above 5 conceptual capabilities. 

First, the MQTT broker offers a pub-sub decoupling messaging architecture for various Sparkplug host systems and devices to operate independently. 

Second, the MQTT broker provides a [Last-Will](https://www.emqx.com/en/blog/use-of-mqtt-will-message) mechanism to support the session state awareness between Sparkplug host systems and devices. 

Third, the Sparkplug specification defines the payload message standard and the topic namespace in the MQTT broker as required by the unified namespace. 

Fourth, the MQTT broker serves as a central data repository that receives messages from devices and forwards them to the host recipients. 

Finally, the MQTT broker stores the most up-to-date and accurate industrial information to maintain a single source of truth for the entire system. That’s why MQTT broker is the right choice for the Sparkplug.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
