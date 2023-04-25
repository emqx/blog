The [MQTT Broker](https://www.emqx.io/) plays a crucial role in facilitating messaging between IoT devices, making it a key component in IoT applications. As such, selecting the appropriate MQTT Broker serves as the initial and most critical step in building IoT applications. This article outlines general selection considerations and potential concerns based on typical IoT project requirements and scenarios. By delving into these factors, readers will understand how to choose an MQTT Broker that aligns with their unique needs and requirements.

## Identify the Requirements of Your Project

The market offers a variety of [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), from private deployment options to cloud-based services that enable MQTT connectivity.

Having a lot of choices gives you more options, but it also makes it more difficult to decide because of the increased complexity.

There is no universal formula for making the best decision. However, the following questions may guide you in the selection process:

1. What is the expected scale of devices in the long run?
2. What are the necessary performance metrics? How essential are message latency and reliability for your project?
3. Where will the MQTT Broker be located? How will you leverage the data?
4. Where your users and IoT devices are geographically located?
5. What are the characteristics of your data? Is message size and frequency a necessary consideration?
6. How do you process IoT data in your application, including the preferred programming language and the data storage and analysis components?
7. Is there a widely used MQTT Broker in the relevant industry?
8. Do you have a budget for paid services?
9. …

These questions will help you identify the features and functionalities that you need from the MQTT Broker. The following section will discuss MQTT Broker features in more detail to help you choose the most suitable MQTT Broker for your project.

## How the MQTT Broker Works

First, let's comprehend how the MQTT Broker operates.

The MQTT Broker uses the **publish-subscribe** messaging model, which means that a message publisher client sends a message to a specific topic, and a message subscriber client receives the message by subscribing to the same topic. The message is delivered to all subscribers who have subscribed to the topic.

The diagram below shows how the **publish-subscribe** model enables message distribution among multiple subscribers, which can be devices or applications.

> Learn [MQTT Publish-subscribe Pattern](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model).

![MQTT publish-subscribe model](https://assets.emqx.com/images/b9575ac3d6916dc629c12aa2de5ce5c3.png)

These are the steps that the client and MQTT Broker take when messaging:

1. Establish a connection: Both the publisher and subscriber clients initiate a connection request to establish a connection with the MQTT Broker.
2. Subscribe to topics: The subscriber client subscribes to one or more topics.
3. Message publishing: The publisher client specifies the topic and payload to publish the message.
4. Message routing: When the Broker receives a message, it checks the list of subscribers and routes the message to all clients that have subscribed to the topic.
5. Disconnect: The client initiates a request to disconnect. The MQTT Broker can also disconnect from the client after a network exception or heartbeat expiration.

Most MQTT Brokers implement the fundamental features specified in the MQTT protocol to support basic messaging functionality, such as QoS levels, client authentication, retained messages, shared subscriptions, and more. These features facilitate the rapid implementation of specific use cases.

However, there is more to it than that. If the MQTT Broker is like a port, message delivery is only the transportation of goods. In fact, to ensure the transportation of goods, a complete logistics system and storage facilities are required to provide essential support. To send goods from various places to different destinations, it is necessary to unpack and repack the goods and use different logistics methods to deliver them. In the off-season and peak season of logistics, it is necessary to adjust the scale of port facilities and personnel dynamically and flexibly to meet demand while maximizing efficiency.

In the context of MQTT Broker, these requirements correspond to security, fault handling, and metrics monitoring for basic operation, data processing and integration capabilities for MQTT messaging, and scalability for the entire service. These features are essential for building enterprise-class IoT applications that cater to diverse needs.

## Security

Security is a key factor to consider when choosing an MQTT Broker, and the following aspects are important to keep in mind.

### Client Authentication

![Client Authentication](https://assets.emqx.com/images/5401567bf5cb065fe376afee0b2b4f5c.png)

The MQTT client authentication requires clients to provide specific credentials to confirm their identity when connecting to the MQTT Broker. Here are the commonly used authentication methods and their requirements for the MQTT Broker:

| **Authentication Method** | **Description**                                              | **Functional Requirement**                                   |
| :------------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Username/Password         | When the client connects, it provides a specific username and password. After receiving it, the server will verify and decide whether to allow the connection. | Compatible with multiple databases and existing data. Support custom authentication and integration with existing enterprise authentication services. |
| JWT Authentication        | The server does not store client authentication or session information. The client provides a signed token for authentication. | Support JWKs and a complete set of encryption algorithms.    |
| X.509 Certificate         | The client and server use the TLS/SSL protocol for secure communication to avoid eavesdropping and data loss, while using X.509 client certificates for authentication. | Provide secure communication with SSL/TLS protocols. Offer low-cost certificate checking with OCSP Stapling/CRL validation. |

### Authorization for Publishing and Subscribing

![Authorization for Publishing and Subscribing](https://assets.emqx.com/images/54531dbe656b0d85d4657db65f3ab665.png)

Authorization is the process of verifying the operational privileges of clients for a specific topic before they can publish or subscribe. Permission lists are usually stored in databases, either internal or external, and need to be updated in real time to reflect business changes.

The following are some typical requirements for the authorization function:

| **Functional Requirement**                               | **Description**                                              |
| :------------------------------------------------------- | :----------------------------------------------------------- |
| Fine-grained access control                              | Able to meet the access control needs of various levels.     |
| Support caching                                          | As publishing and subscribing are high-frequency operations, a caching mechanism can effectively alleviate pressure during peak hours. |
| Support integration with multiple databases              | Users can flexibly choose their own familiar technology stack. |
| Compatible with the data present in the current database | Consider this when migrating from an old system.             |

### Software Vulnerabilities and Enterprise IT Security

The software industry has gained valuable insights from past experiences, recognizing that security vulnerabilities in software can substantially affect an enterprise's operations.

If you plan to use an MQTT Broker in a production environment, it is vital to conduct a rigorous security evaluation using the widely accepted security validation methods to ensure its compliance with security standards:

- Open source validation: check the Broker's code openness and the level of its validation by the open source community;
- Security integration: check the sufficiency of security testing and protection, and the adoption of professional security solutions.

Enterprise IT security is essential to safeguard enterprise data from various security threats such as data leakage, destruction, theft, and abuse. To ensure optimal security, password policies, security audits, data encryption, and other relevant security features must be offered by MQTT Brokers.

> Discover more about MQTT security by reading our blog series [7 Essential Things to Know about MQTT Security 2023](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security).

## Clustering and Auto-Scaling

An MQTT Broker cluster is a system that distributes the workload of connecting and messaging among multiple MQTT Brokers (also known as nodes).

Clients can interact with the cluster as a unified entity, without being aware of the internal workings or any changes in the number of nodes. The cluster handles connections and also publishes and subscribes messages just like a single node.

![MQTT load balance](https://assets.emqx.com/images/adde22edec17a94cc8f8ec96d82e79d0.png)

### Why Do We Need MQTT Broker Cluster?

#### Ensure Larger Connections and Higher Scalability

Imagine that you have a car equipped with IoT capabilities. As it floods the market, with monthly sales reaching thousands to tens of thousands of units, your MQTT Broker needs to prepare for a potential surge in connections, ranging from tens of thousands to millions, in the coming years. With the OTA upgrades of the vehicle system, more data is expected to be transmitted to the cloud, causing a significant increase in message throughput for your MQTT Broker.

With a cluster-supported MQTT Broker, you have the ability to add nodes to the cluster at runtime, enabling easy horizontal scaling to accommodate an increasing number of MQTT messages and client connections.

#### **Guarantee high availability of services**

Not every application is required to handle the demands of business expansion. For instance, if your business is solely focused on environmental monitoring in a particular school or manufacturing facility, the volume of clients and messages can be anticipated to remain consistent for several years, even without any alterations.

You might have noticed that a solitary MQTT broker has the capacity to accommodate tens of thousands of clients, which is adequate for the majority of IoT applications. In light of this, is it essential to implement clustering?

Indeed, it is. An MQTT Broker cluster can persist in functioning even when certain node failures, guaranteeing that there is no single point of failure and that the service remains accessible at all times.

Therefore, if you need your application to be reliable, you should select an MQTT Broker that supports clustering.

### Only a Few MQTT Brokers Support Clustering

An MQTT Broker cluster's main responsibility is to synchronize and replicate MQTT session state, such as subscribed messages and pending message transfers, among cluster nodes in an efficient and reliable way. It also aims to balance the load of connections, manage devices centrally, and ensure the scalability and high availability of the whole cluster.

Implementing all these features is a complex undertaking, which is why the deployment of most MQTT Brokers is restricted to a single node. However, recognizing the significance of scalability and high availability, some of these Brokers offer specialized implementation solutions.

**Use MQTT Bridging Feature to Link Multiple Brokers**

Using MQTT message publishing and subscribing to exchange messages among multiple Brokers provides some level of scalability, allowing more clients to connect and interact with each other. However, this mode of communication is known to be highly inefficient and does not ensure high availability.

**Synchronize Full Session State Between Multiple Nodes**

One way to achieve high availability of MQTT Brokers is to run multiple instances simultaneously and perform full synchronization of session state among nodes. If a node fails, load balancing can quickly switch to another node, providing single-machine hot backups and avoiding any disruption to IoT applications. However, it is important to note that this method may not be the best choice for scaling and can lead to increased costs.

Although the above solutions are functional, it does not provide both scalability and high availability at the same time, and can also complicate the deployment process. To simplify the creation of reliable IoT services that can scale as needed, it is recommended to choose MQTT Brokers that support clustering themselves.

>Find out how EMQX achieved 100M connections with a single cluster using efficient clustering.
>
>[Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)



## Data Integration and Rule Engine

When developing IoT applications, it's often essential to enable data exchange among multiple systems, not only between devices.

For instance, data collected from sensors on a factory line can be sent to accompanying MES and ERP systems via an MQTT Broker. To establish a reliable connection between the two systems, a database or an event-driven message queue like Apache Kafka can serve as a bridge.

Similarly, weather sensor data scattered across a city can be gathered and stored in a time-series database like InfluxDB for thorough analysis, enabling the data's full potential to be realized.

A simple way to do this is to create an application that subscribes to messages from an [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) and sends them to the relevant data integration. Some MQTT Brokers offer this functionality as plugins or extensions, since this is a common requirement.

You may also need to filter, encode, or otherwise process the data before saving it to meet the actual business needs.

Some MQTT Brokers offer a built-in rule engine that facilitates data processing by enabling users to create data-driven rules on the Broker and send results to data integration. Typically, this functionality can be configured using low-code tools such as SQL or form.

The entire process is shown in the following diagram:

![Entire process](https://assets.emqx.com/images/b8b1b2be373f56476be6e1269bb76d47.png)

For IoT applications that require integration with external data systems, having a built-in data integration and rule engine can be a major advantage of MQTT Brokers. This feature reduces the need for additional development work and can speed up business delivery, while also enabling auto-scaling within the cluster for high availability.

## Performance

MQTT Broker is used to connect a large number of clients and enable massive messaging, where the following performance metrics need to be considered:

1. Maximum number of connections: which refers to the maximum number of client connections that the MQTT Broker can support.
2. Message transmission latency: the time it takes for a message to be sent from the sender to the receiver, and is primarily dependent on the performance of the MQTT Broker, assuming a consistent network environment.
3. Message send/receive rate: the number of messages that can be sent or received per second by the MQTT Broker.
4. Message storage performance: this metric is relevant for MQTT Brokers that support message persistence with external data integration, as it measures the performance of the message storage functionality.

While performance is essential, it's not the only thing to look for in an MQTT Broker. A high-performing broker usually excels in other areas too, but don't rely solely on performance metrics to evaluate it, unless it's significantly underperforming.

Besides, it is important to note that the performance metrics reported by an MQTT Broker are based on a specific scenario, and various factors such as message rate, topic level, message QoS, message payload size, and the status of the rule engine can influence the outcomes.

Moreover, any Broker can claim a performance metric that is hard to replicate and irrelevant to the users. If you have high performance demands, please carefully examine whether its technology can deliver the expected results and whether its test results can be reproduced. Real knowledge comes from practice, so it is best to conduct a stress test based on your own application scenarios.

## Cloud Native

Cloud-Native is a modern software architecture and delivery approach specifically designed to facilitate the efficient and reliable creation and deployment of cloud-based applications.

By leveraging Cloud-Native technology, MQTT Broker and infrastructure can be seamlessly integrated to enable efficient, flexible, and reliable deployment through the use of containers, microservices, and automated operations and maintenance.

Additionally, Cloud-Native technology offers management capabilities such as configuration management, cluster scaling, seamless upgrades, fault handling, and unified monitoring to enhance the development and operation of large-scale IoT applications.

To achieve these goals, it is crucial for the scalability and management functionalities of the MQTT Broker to be tightly integrated with the underlying capabilities of the cloud infrastructure. However, in reality, the level of Cloud-Native implementation varies among different Brokers.

>Automate the creation, configuration, and management of your MQTT cluster with [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator).

## Support Extensions

A single software solution cannot fulfill the requirements of all users. To accommodate specific requirements, such as support for multiple message transfer protocols, custom authentication and authorization, specialized data encryption methods, and monitoring and alert capabilities, it may be necessary to extend the functionality of the MQTT Broker.

To facilitate this, the MQTT Broker must provide an appropriate extension mechanism, such as a plugin architecture, to enable customization when needed. Additionally, it should support mainstream programming languages for extension development.

> Learn [best practice of MQTT in various clients](https://www.emqx.com/en/blog/category/mqtt-client).

## Cost

Cost is a multifaceted consideration that must be evaluated in relation to your budget.

Depending on your needs, you may opt for enterprise services or an open-source MQTT Broker. There are many open-source MQTT Brokers available, which can typically be deployed without incurring any licensing fees if the open-source license allows it. However, installation, maintenance, and extension development may require additional resources.

When deploying MQTT Brokers for large-scale applications, it's essential to assess their performance and consider the costs associated with them. High-performance MQTT Brokers can significantly reduce the overheads associated with hardware, network, and maintenance, resulting in lower overall costs.

When choosing a managed [MQTT cloud service](https://www.emqx.com/en/cloud), it is essential to understand how billing works, as it usually depends on the number of connections and the amount of traffic. You should review the details of each billing option carefully and select the most cost-effective option for your specific use case.

## Additional Considerations

In addition to the MQTT Broker itself, there are several other factors to consider:

- **Provide Enhanced and Localized Services**

  Choose MQTT Broker providers who deliver regional or global services, as they help enterprises to get quicker technical support, accelerate delivery and cut costs substantially.

- **Avoid Building Systems From Scratch**

  To minimize investment risks and costs when selecting MQTT Brokers or technologies for IoT projects, it is advisable to opt for established solutions with a proven track record in the industry. Developing systems from scratch should be avoided as it can be time-consuming, costly, and potentially risky.

- **Support Seamless Integration of Edge and Cloud**

  When deploying at the edge, it is important to select an MQTT Broker that has low resource consumption, is optimized for edge environments, or has a proven cloud-edge solution.

- **Conclusion**

  In this article, we have outlined the key criteria that developers should consider when selecting an MQTT Broker for their projects. By carefully evaluating each criterion based on their specific requirements, readers can make an informed decision and choose the MQTT Broker that best fits their needs.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
