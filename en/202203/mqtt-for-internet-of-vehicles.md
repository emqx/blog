Internet of Vehicles（IoV）is a typical application of IoT technology in the field of transportation systems. To some extent, the integration layout and collaborative development of relevant technical fields involved in the IoV industry are connected with the IoT. As an open source IoT data infrastructure software supplier, [EMQ](https://www.emqx.com/en) has provided IoT infrastructure software with cloud-edge collaboration for many customers in the field of IoV for many years.  Thus realizing the unified connection of people, vehicles, roads and clouds, and creating intelligent networking, autonomous driving and V2X scenario solutions for vehicle manufacturers, T1 suppliers, aftermarket service providers, travel service companies, etc.

In this series of articles, we will share how to build a reliable, efficient and industry-specific Internet of Vehicles platform based on EMQ's practical experience in the field of Internet of Vehicles, from theoretical knowledge such as protocol selection to practical operations such as platform architecture design.

## Preface

The [MQTT protocol](https://www.emqx.com/en/mqtt) has long been a well-deserved mainstream protocol in the field of IoT. It has been widely used in the building of IoT platforms in many industries by virtue of its characteristics of lightweight, high efficiency, reliability, security and two-way communication. So what about the application of the MQTT protocol in the IoV industry?

Based on EMQ’s use cases in the IoV industry, this article will compare the advantages and disadvantages of different IoT communication protocols in the construction of IoV platforms, and share how enterprises can select appropriate MQTT messaging products and services based on their own conditions, as well as the most popular technical solutions in data transmission security, data integration and so on.

## Is the MQTT protocol suitable for IoV?

The whole business architecture of IoV is complex and involves multiple communication links. In this article, what we focus on is the messaging from device to cloud, which is the main responsibility of the IoV platform.

MQTT is an IoT communication protocol based on the publish or subscribe model. It has the characteristics of simple and easy to implement, QoS support, small message size and so on. It occupies half of the IoT protocols. In the IoV scenario, MQTT is still applicable for flexible, fast and safe access of mass vehicle systems, and ensures the real-time and reliability of messages under complex network environments. Its main advantages of MQTT are:

- It is a fully-open message protocol, simple and easy to implement. There are a large number of mature software libraries and hardware modules in the market, which can effectively reduce the assess difficulty and cost of the vehicles.
- It provides flexible publishing subscription and topic design, which can communicate messages through massive topics to deal with various IoV business cases.
- The Payload format is flexible and the message structure is compact, which can carry various business data and effectively reduce the network traffic of the vehicles.
- It provides three optional QoS levels, which can adapt to different network environments of the vehicles.
- It provides the capability of online state awareness and session management, and is able to manage the online state of the vehicles and keep offline messages.

In summary, if the MQTT protocol is used together with messaging broker products that can handle mass vehicle connections, soft real-time and high concurrent data throughput, and multiple security guarantee capabilities, MQTT protocol will undoubtedly bring convenience to the building an IoV platform.

## Why is MQTT better than other protocols?

So far, most IoV customers have preferred the MQTT protocol. We have also encountered some customers who have chosen other protocols such as private TCP and HTTP, but MQTT is the best choice for IoV use cases.

Before the MQTT protocol was invented, a large-scale original equipment manufacturer in South China adopted the privatized TCP protocol (ACP protocol) to build a service platform for IoV. After a long period of protocol specification design and development, the main features of the IoV platform were basically realized. However, with the increasing demand of the IoV business scenarios and the increasing number of vehicles, the disadvantages of privatized TCP become more and more prominent.  

Some problems with private protocols are: 

- It is difficult to maintain the definition and version of privatized protocols.
- All the functions of the protocol (such as keep alive, reconnecting, offline message, etc.) need to be customized and developed.
- The private protocol leads to the need for customized development of the terminal hardware adaptation.
- High cost, long cycle and slow update iteration are prominent. 

With the continuous improvement of the MQTT protocol and its widespread use in the communication section of the IoV platform, the original equipment manufacturers began to adopt the MQTT protocol in the development of the new generation of IoV platforms. Based on the full support of the MQTT protocol provided by [EMQX](https://www.emqx.com/en/products/emqx) , it not only reduces the development cost, shortens the development cycle, but also allows for more functional scenarios and better operation and maintenance.

A large-scale original equipment manufacturer in East China has more than one million vehicles in stock. The previous IoV platform was built using a private TCP protocol. Because of the large amount of message communication of millions of vehicles, the privatized TCP protocol has high maintenance cost, unsecured message reliability, and a heavy daily system maintenance and functional development workload. With the extensive adoption of the MQTT protocol on the IoV platform within the Group, the original equipment manufacturer also started the transformation and upgrading to the MQTT protocol. At present, some vehicle models have been upgraded by OTA. In the future, they plan to gradually complete the upgrading and transformation of all models in stages.

Another vehicle enterprise customer had contacted us in the early development stage. Because of their relatively simple business case at the early stage, they decided to use a custom in-house HTTP service to access the vehicles.  As the business expanded, traditional request-response mode communication could not meet the new business requirements. At the same time, with the increasing number of functions and terminals, the traffic volume of the whole platform increased exponentially, and the performance bottleneck occurs when HTTP access was used. The customer finally chose MQTT as the access protocol and used the data access solution provided by EMQX to solve their business problems. 

On the whole, private protocols are characterized by closeness and exclusiveness. At the early stage of development, they are designed to solve specific problems, which can lead to a lack of future flexibility. It is often difficult to meet new requirements after business expands and more features are required in the protocols.  Bottlenecks can occur as more connections are required and this causes performance and scalability problem. As a result, the development focuses away from the actual business needs to the development to access layers and middleware.  This increases the overall project cost of the platform. Therefore, MQTT protocol has naturally become the most suitable mainstream protocol in the field of IoV.

## How to select MQTT messaging products or services?

The design of system architecture and the selection of product type is a rigorous process in platform design. In combination with application scenarios, users should first evaluate whether product features meet business requirements, and whether performance and scalability can support both the short-term design capacity of the platform and the possible future growth. Product use cost is also an important criteria. The cost of the product itself, IaaS infrastructure, development integration and maintenance work will affect the customer's total cost of ownership. In addition, it should be evaluated in combination with the globalization capability of the products. For projects with an overseas business, it is important to consider whether the product can support global deployment and meet the compliance of the different regions.  It is also important to avoid cloud computing vendor lock-in.

In the process of selecting models, the IoV customers often compare EMQ with the cloud computing provider's IoT messaging SaaS service. By contrast, the advantages of EMQX are private deployment and standardization capabilities, which support private deployment to any cloud platform without vendor lock-in. And it supports the standard MQTT protocol, which is generally valued by IoV customers.

Avoiding cloud computing supplier lock-in will help enterprise users gain competitive advantage and reduce the impact caused by the termination of partnerships between enterprises and cloud computing suppliers. On the other hand, multi-cloud support can also make full use of the technical and commercial advantages of different cloud computing providers.

In addition, there are a considerable number of customers who benefit from the lower usage cost of EMQX. The basic reason is that due to different billing methods, the larger the business scale, the higher the access service cost of the cloud computing provider.

IoV platform business no longer have to choose between a local installation of EMQX, with management and maintenance, and another cloud provider.  With the launch of [EMQX Cloud](https://www.emqx.com/en/cloud), EMQ's fully-managed MQTT messaging service, users can now eliminate the burden of infrastructure management and maintenance. This allows for clear and controllable cost budgets, cross-cloud and cross-platform consistent with private deployment, and to be able to carry out the construction of IoV platform without worries.

For customers with private deployment needs, EMQX also has its unique advantages. EMQX provides global commercial support. Its high product performance can bring massive connectivity and throughput, and its rule engine and data bridging can provide rapid integration. For the field of IoV, the highly reliable and scalable architecture capability and the V2X information interaction capability of the cloud edge collaboration make EMQX stand out among similar products that support private deployment.

In 2018, when SAIC Volkswagen designed and developed a new generation of IoV system, they took into account the requirements for large concurrency, low delay and high throughput of a new type of IoV system, and the mainstream of a new IoV system architecture.  Finally, they adopted the MQTT protocol to build their new generation of IoV platform.

In this project, the characteristics of MQTT and the capability of EMQX's powerful rule engine data integration, and general bus capability met the customer's requirements for real-time reliability of messages in complex networks and solved the requirement of tight project time, and rapid development.

## What technical solutions are the most commonly used?

As a message broker, EMQX provides rich and flexible integration capabilities, and each feature provides different technical solutions for users to choose. After long-term use, the popular technical solutions are as follows:

### Security assurance

At the transport link layer, we recommend users to enable TLS encrypted transmission, but most cloud computing providers' load balancing products do not support TLS termination. During production deployment, additional components such as HAProxy need to be deployed to terminate TLS certificates.

The most common way to access TBox access is to use certificate authentication. EMQX provides an extensible authentication chain, supports third-party authentication platform extensions (such as PKI system), external data source based on username or password and internal database authentication.

In addition, most users have enabled the EMQX authentication feature, which assigns corresponding publish and subscribe permissions to different TBox terminals to effectively protect data security.

![EMQX Security assurance](https://assets.emqx.com/images/4ff574a38707a1a8160882dca8cd16e7.png)


### Data integration

Customers attach great importance to the ability to connect the massive data of IoV through EMQX with business systems. EMQX has a built-in rule engine and data bridging capability, which can stream MQTT data to Kafka, and various SQL/ NoSQL/ time-series databases.  Most customers in actual projects use Kafka as the back-end stream processing component.

Kafka focuses on data storage and reading, while EMQX focuses on communication between client and server. EMQX is used to quickly receive and process messages from a large number of IoT devices. Kafka can collect and store this data and send it to back-end programs for analysis and processing. This architecture is the most widely used data integration scheme at present.

![EMQX Data integration](https://assets.emqx.com/images/382114e90c6a728659ac9316b73ddd60.png)

## **Conclusion**

At present, the rapid development of automotive electronics promotes the technological upgrading of the industry of IoV. The future market prospect of intelligent transportation and vehicle industry is considerable, and it can be predicted that more consumers and vehicle manufacturers will benefit from it. The full support of MQTT protocol and the powerful product capability of EMQX can help developers to quickly build robust and flexible platforms for IoV. EMQ will also keep pace with the development trend of the industry, promote the development and implementation of technologies related to message transmission and edge computing, and provide faster, better and smarter messaging infrastructure for autonomous driving, vehicle collaboration and IoV users.


## Other articles in this series

- [IoV beginner to master 02｜Architecture Design of MQTT Message Platform for Ten-million-level IoV](https://www.emqx.com/en/blog/mqtt-messaging-platform-for-internet-of-vehicles)

- [IoV beginner to master 03｜MQTT topic design in TSP platform scenario](https://www.emqx.com/en/blog/mqtt-topic-design-for-internet-of-vehicles)

- [IoV beginner to master 04 | MQTT QoS design: quality assurance for the IoV platform messaging](https://www.emqx.com/en/blog/mqtt-qos-design-for-internet-of-vehicles)
