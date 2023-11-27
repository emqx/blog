The convergence of Information Technology (IT) and Operational Technology (OT) involves integrating traditionally separate enterprise networks and computing systems with industrial control systems and devices to create a unified and interconnected ecosystem. Selecting the best protocol for IT and OT convergence depends on various factors, including the specific industry, existing infrastructure, security considerations, and scalability requirements.

[OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol) and [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) are the protocols that are commonly used in this scenario. As these two technologies continue to evolve, a new protocol has emerged which is a powerful combination of both, providing even greater benefits for the industry. It is called OPC UA over MQTT. In this article, we will dive into OPC UA over MQTT and explore its potential to empower the convergence of IT and OT.

## How Does OPC UA over MQTT Come?

**OPC UA** is a popular protocol for bridging the gap between IT and OT environments. It provides secure and reliable communication with standardized data models, making it suitable for real-time data exchange and complex information sharing. OPC UA offers built-in security features and supports various platforms and devices.

**[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)** is a lightweight publish-subscribe messaging protocol designed for efficient data transmission in resource-constrained environments. It's well-suited for IoT and OT integration scenarios where bandwidth and power considerations are important. [MQTT's publish-subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) enables efficient data distribution to multiple subscribers.

**OPC UA over MQTT** is a protocol that combines MQTT and OPC UA to leverage the advantages of both protocols. Both OPC UA and MQTT have their own benefits for using them in an IT and OT convergence scenario. MQTT is used as a transport to carry the rich data context of OPC UA. This approach benefits you from MQTT's lightweight publish-subscribe messaging model and OPC UA's standardized data modeling, security features, and broader capabilities for complex information exchange.

## Benefiting From MQTT Pub-Sub Pattern

### Flexible and Scalable IT and OT Infrastructure

MQTT (Message Queuing Telemetry Transport) is primarily a message-driven protocol. It follows a pub-sub messaging pattern, where publishers send messages to a central message broker, and subscribers receive those messages from the broker. The [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) acts as an intermediary between publishers and subscribers. It receives messages published by publishers and forwards them to subscribers who have expressed interest in receiving messages on specific topics.

![Flexible and Scalable IT and OT Infrastructure](https://assets.emqx.com/images/04fad3e33add07f5623fb11655bde6de.png)

Pub-sub messaging systems are inherently more scalable than client-server systems. In a client-server model, each client must establish and maintain a connection with the server, which can lead to performance bottlenecks as the number of clients increases. In a pub-sub model, the publisher sends messages to a centralized broker, which then disseminates messages to interested subscribers. This architecture scales more effectively as the number of publishers and subscribers grows.

### Network Bandwidth Utilization

In client-server systems, each client's request generates traffic on the network and the server by using the polling mechanism. As a result, it generates unnecessary large amount of network traffic even if there are no updates in the target values. In pub-sub, subscribers receive updates only when there's new data available, reducing unnecessary network load. This is important in applications such as IoT, where sensor data or status updates need to be delivered promptly.

### Event-Driven Architecture

Pub-Sub aligns well with event-driven architectures, where components react to events or changes in data. This is especially useful in scenarios where actions need to be triggered based on specific conditions or events. This benefits from the decoupling of the sender (publisher) and receiver (subscriber). Publishers don't need to know who their subscribers are, and subscribers don't need to know who their publishers are. This separation allows for flexibility in executing components without affecting each other, leading to more efficient resource utilization and responsiveness.

![Publish-subscribe model](https://assets.emqx.com/images/c1ab4dba0def1c22c94be5f471ea5cff.png)

Therefore, publishers and subscribers don't need to be aware of each other's existence or specific implementation details, making it easier to replace or upgrade individual components without disrupting the entire system.

## Rich Data Context Powered by OPC UA

Apart from the advantages brought by the MQTT Pub-Sub mechanism, OPC UA gives out another level of importance to ensure seamless communication between diverse devices and applications. OPC UA is designed with a strong focus on interoperability and standardization across different systems, vendors, and industries. It excels in handling complex data structures, hierarchical data models, metadata, and robust security features, fitting the application with intricate data relationships. This makes the protocol well-suited for complex industrial environments, regardless of the underlying technologies or vendors in different industrial domains.

OPC UA is widely used in industries such as manufacturing, process automation, energy, automotive, and more. Its adoption is seen across diverse sectors that rely on robust and standardized communication for their operations. Some application scenarios such as power plants, chemical processing, and aerospace, are highly critical, where reliability and safety are paramount.

## Operational Model of Building OPC UA over MQTT Messages

The provided diagram showcases the internal steps within a Publisher for generating and dispatching messages, along with the necessary parameters for this process. It also illustrates the process within a Subscriber for receiving, decoding, and comprehending messages, along with the parameter model essential to achieving these actions.

![Diagram](https://assets.emqx.com/images/a43616ab5a8ac59a146fbfbac290a262.png)

### Publisher Processing

**Step 1 - Data Collection**

In the initial stage, data (DataSet) is gathered to prepare for publication. This process involves configuring the collection using a structure called PublishedDataSet. Within the PublishedDataSet, essential details about the data, known as DataSetMetaData, are defined. The result of this data collection process is the creation of values for the individual fields within the DataSet.

**Step 2 - DataSetWriter and DataSetMessage Creation**

Subsequently, a component known as a DataSetWriter is employed to create what is called a DataSetMessage. Multiple DataSetMessages generated by different DataSetWriters within a WriterGroup can be grouped into a unified NetworkMessage.

**Step 3 - NetworkMessage Creation**

The creation of a NetworkMessage follows, utilizing the information acquired in the previous step along with the PublisherId specified in the PubSubConnection. The structure of this NetworkMessage conforms to the specific communication protocol in use.

**Step 4 - NetworkMessage Delivery**

The final step involves transmitting the fully-formed NetworkMessage to the designated Message Oriented Middleware. This is accomplished by leveraging the predefined Address specified for this purpose.

### Subscriber Processing

**Step 1 - Initiating Connection and Subscription:**

The Subscriber chooses the appropriate Message Oriented Middleware and establishes a connection via the provided Address, using multicast for OPC UA UDP or connecting to a Broker for MQTT. The Subscriber begins listening for incoming messages. Filters such as PublisherId, DataSetWriterId, or DataSetClassId are configured to screen out messages that don't match the specified criteria.

**Step 2 - Processing Incoming NetworkMessages**

When a NetworkMessage arrives, it is subjected to decryption and decoding using the security parameters employed by the Publisher.

**Step 3 - Decoding and Application-Specific Handling**

Relevant DataSetMessages are directed to the corresponding DataSetReaders. The content of DataSetMessages is decoded utilizing DataSetMetaData, which contains comprehensive field syntax, version information, and relevant properties. Application-specific processing follows, which could involve tasks such as mapping received values to Nodes within the Subscriber's OPC UA AddressSpace.

**Step 4 - Configuration and Management of SubscribedDataSet**

The Subscriber configures the SubscribedDataSet for data dispatching.

Two distinct choices exist:

- TargetVariables configuration dispatches DataSetMessage fields to pre-existing Variables within the Subscriber's OPC UA AddressSpace.

- SubscribedDataSetMirror configuration is utilized when received DataSet fields should be transformed into Variables within the Subscriber's OPC UA AddressSpace. If these Variables don't exist, they are created as part of the Subscriber's configuration.

### Configuration Tools

The setup and customization of both Publishers and Subscribers are commonly facilitated through dedicated configuration tools. This configuration process can occur through two primary avenues:

1. Utilize a generic OPC UA PubSub configuration tool that adheres to the PubSub configuration Information Model.

   ![OPC UA PubSub configuration tool](https://assets.emqx.com/images/3a778dee963d7d49584be505613cc445.png)

   > Note: To align with the PubSub configuration Information Model, both Publishers and Subscribers are required to function as OPC UA Servers themselves.

2. Employ vendor-specific configuration tools that cater to the specific characteristics of the application.

   ![vendor-specific configuration tools](https://assets.emqx.com/images/a469e1b8753a2e096dc71e99b6d6eabc.png)

The configuration procedure encompasses the arrangement of DataSets and determining how data is sourced for eventual publishing. This configuration can be accomplished using the PubSub configuration model, which outlines a standardized framework, or it can be tailored using configuration tools designed by individual vendors to suit their specific offerings.

While an OPC UA Application can be pre-configured to operate as a Publisher, often, additional configuration is needed to specify the content to be included in messages and the frequency at which these messages are transmitted. This enables precise tailoring of the message content and transmission intervals according to the application's needs, ensuring effective communication between Publishers and Subscribers in the OPC UA network.

## Proven Protocol for IT and OT Organization

OPC UA over MQTT is indeed a proven protocol that has gained widespread adoption and recognition in various industries. It's used in supervisory control and data acquisition (SCADA) systems, manufacturing execution systems (MES), [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) solutions, and more. Many industrial automation vendors such as Siemens, Beckhoff, and KUKA provide OPC UA over MQTT support in their products, ranging from PLCs and sensors to software platforms. This wide support signifies the maturity of the protocol.

OPC UA over MQTT's suitability for IoT deployments extends to cloud-based applications. Many cloud providers such as AWS, Azure and GCP offer the protocol support, allowing seamless integration of IoT data into cloud services for storage, analysis, and visualization. By running OPC UA over MQTT, OPC UA's capabilities can be extended from cloud to edge devices and enable seamless integration into industrial IoT ecosystems.

![Proven Protocol for IT and OT Organization](https://assets.emqx.com/images/f76c2d7f2c580da82d9c0c5b89d7be3e.png)

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
      An Innovative Architecture for IIoT System
    </div>
    <div class="mb-32">
      Harnessing the true potential of industrial connectivity and real-time data.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-opc-ua-over-mqtt-the-future-of-it-and-ot" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Security and Authentication

OPC UA over MQTT offers comprehensive security mechanisms, including authentication, authorization, encryption, and data integrity. It addresses the security challenges inherent in industrial environments, helping to protect sensitive data and prevent unauthorized access.

## Conclusion

In conclusion, OPC UA over MQTT brings together the best of both worlds by combining the strengths of OPC UA and MQTT protocols. This integration offers efficient communication, standardized data modeling, and interoperability, making it an appealing choice for industrial and IoT applications. By leveraging MQTT's lightweight nature and publish-subscribe architecture while retaining OPC UA's robust data representation and standardized services, OPC UA over MQTT provides a positive and versatile solution for modern communication needs.

[EMQX](https://www.emqx.com/en/products/emqx) MQTT broker and [Neuron](https://www.emqx.com/en/products/neuron) gateway can perfectly enable OPC UA over MQTT. EMQX's proven track record as an MQTT broker ensures reliable message delivery and efficient data distribution, while Neuron's specialization in bridging OPC UA to MQTT allows you to leverage the strengths of both protocols.





<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
