In the IoV ecology, TSP (Telematics Service Provider) platform occupies the core position in the industry chain. It connects automobile and vehicle-mounted equipment manufacturers, network operators, and content providers. It is the core data connection platform for vehicles and services of the original equipment manufacturer (OEM). With the development of intelligent automobiles and the increasing demand of vehicle owners for applications, the demand on OEMs for equipment and applications based on the Telematics Service Provider (TSP) platform will continue to increase.

In the previous article, we mentioned that in the choice of data interaction protocol between vehicle-mounted equipment and TSP platform, the MQTT protocol has become the preferred protocol for the next generation TSP platform of all original equipment manufacturers.  This is because of its advantages of being lightweight, scalable, different quality of service (QoS) levels, decoupling the data generation and consumption systems through the publish-subscribe model.

In this article, we will describe how to design the topic of MQTT messages in the process of building the TSP platform of IoV.

## Requirements for Message Channels in TSP Scenarios of IoV

In the TSP scenario of IoV, MQTT protocol, as a business message channel between "vehicle-platform-application", not only ensures that messages between vehicles and applications can be interconnected bidirectional, but also needs to identify and distribute different types of messages through certain rules. The topic of the MQTT protocol is the label of these messages, which can also be regarded as the business channel.

In the IoV scenario, messages can be divided into data uplink channels, which are vehicle-platforms to applications, and data downlink channels, which are applications to vehicle-platforms. As for the TSP platform of IoV, different data directions mean different business types, which shall be clearly distinguished and isolated by the topics of MQTT.

**From the perspective of vehicle-end:**

In the TSP platform, vehicle data reporting is the main business type of uplink data. With the continuous enrichment of IoV business, the computing and communication capabilities of vehicle-mounted systems such as T-box are increasing, and the business scenarios, data volume, and frequency of vehicle data reporting are also increasing. Based on the requirements of business isolation, real-time, and security, one vehicle with one topic in the early stage of IoV has gradually developed into one vehicle with a multi-message channel.

**From the perspective of application side:**

The platform application is not only the receiver and consumer of vehicle data but also the message sender of issuing data and instructions. According to different business requirements, the sending types of messages can also be divided into:

- One-to-one messages: For key business requirements such as vehicle control and those with high-security requirements, a one-to-one message channel shall be provided for each vehicle.
- One-to-many messages: For certain business requirements or a certain type of vehicle, instruction and data can be issued to the vehicle equipment through the same topic channel.
- Broadcast messages: For large-scale message notifications, configuration updates,  large-scale message broadcasts can be sent to the equipment connected to the platform.

## What is the Topic of the MQTT Protocol

### Basic concept 

There are three roles in the communication mechanism of the MQTT protocol: publisher, broker and subscriber. The message is sent from the publisher to the broker and then received by the subscriber, and the topic is the agreed message channel between the publisher and the subscriber.

The publisher sends messages from the specified topic, the subscribers subscribe and receive messages from the specified topic, and the broker acts as an agent to receive and distribute messages in conformity with the topic. In the TSP platform scenario of IoV, vehicle-mounted equipment, mobile terminal, and business application can all be regarded as clients in MQTT. According to different businesses and different data directions, the roles of vehicle-mounted equipment, mobile terminal and business applications will also be switched between publishers and subscribers.

### The definition and specification of the topic

The MQTT protocol specifies that the topic is a UTF-8 encoded string, and the topic shall meet the following rules:

- All topic names and topic filters must contain at least one character.
- Topic names and theme filters are case-sensitive. For example, ACCOUNTS and Accounts are different topic names.
- Topic names and topic filters can contain space characters. For example, “Accounts payable” is a legal topic name.
- Topic names or topic filters are distinguished by leading or trailing slashes `/`. For example, `/finance` and `finance` are different.
- Topic names or topic filters containing only slashes `/` are legal. 
- Topic names and topic filters cannot contain null characters (Unicode U+0000).
- Topic names and topic filters are UTF-8 encoded strings. There are no other restrictions on the number of levels of topic names or topic filters except that they cannot exceed the length limit of UTF-8 encoded strings. 

### Topic level 

MQTT protocol topics can be divided into multiple levels by the slash ("/" U+002F). As a message channel, the client can subdivide the message type by defining the topic level. 

For example, an OEM has multiple models, and there are multiple businesses of IoV under each vehicle model. We can distribute messages to the topic `<Model A>/ <Vehicle Unique ID>/ <Business X>` when defining that the vehicle sends a message to the business system of a certain vehicle model.

In the MQTT world, there can be many levels of the topic, such as: `<Model A>/<Vehicle Unique ID (Frame No.) >/<Business X>/<Sub-business 1>`. There is no limit on the number of levels in the MQTT protocol.

In this way, we can design according to the topic level when we define the level of business channels of IoV.

### Wildcard

Subscribed topic filters can contain special wildcards that allow clients to subscribe to multiple topics at once.

**Multi-level wildcard**

The `#` symbol ("#" U+0023) is a wildcard used to match any level in a topic. A multi-level wildcard represents its parent and any number of child levels. For example, subscribers can subscribe to `<Model A>/#` to receive messages on these types of topics：

`<Model A>`

`<Model A>/<Frame No. 1>`

`<Model A>/<Frame No. 1>/<Business X>`

**Single-level wildcard**

The `+` ("+" U+002B) is a wildcard that can only be used for single topic level matching. For example, subscribers can subscribe to `<Model A>/+/<Business X>` to receive: 

`<Model A>/<Frame No. 1>/<Business X>`

`<Model A>/<Frame No. 2>/<Business X>`

## Best Practice of Topic Design Principles for TSP Platform of IoV

In the IoV scenario, the MQTT topic defines the channel between business and data, and the core of the topic definition is to distinguish the business scenarios. The topic needs to be designed to conform to certain principles. We can design and define the topic in the following dimensions:

### By business data direction

The uplink and downlink directions of data determines who generates the data and who consumes the data. In the scenario of IoV, the data uplink channel from the vehicle-mounted equipment to the platform and the data downlink channel from the platform to the vehicle need to be separated by the topic. By distinguishing the design of uplink and downlink topics, it can help designers, operators and business personnel to quickly locate scenarios, problems and related stakeholders.

Some businesses may use uplink and downlink topics at the same time, such as the platform sending data after the vehicle application data is received, and the vehicle reporting data after the platform requested the vehicle working data. In this case, due to the asynchronous communication mechanism of the MQTT protocol, the uplink and downlink topics of a whole business need to be defined separately.

### By vehicle model

In the IoV scenario, different vehicle models mean that the data generated by vehicles are not identical, the capabilities of vehicles are not identical, and the docking of business applications are also not identical. We can make a topic distinction between differentiated vehicle data and business in conformity with the vehicle model. Of course, different models under the same OEM will also have the same business and data, which can be defined by cross-modal topics.

### By vehicle

In the IoV scenario, business scenarios with high-security levels, such as vehicle control, often require one-to-one topics as data channels. On the one hand, the topic is used to isolate the business information between vehicles. On the other hand, the point-to-point interaction of data can be ensured. In the design of the topic, it is sometimes necessary to take the unique identifier of the vehicle as a part of the topic to realize a one-to-one message channel. A common scheme is to use the vehicle VIN code as part of the topic.

### By user

There can also be a need to realize one-to-one message channel of vehicle and cloud (V2C) based on users (rather than vehicles). Such requirements often occur in user promotion, operation, ToB business and other scenarios. During the design of the topic, there are two common schemes: one is to use user ID as a part of the topic; the other is to transform it into a vehicle-level topic through the human-vehicle relationship. However, due to the timeliness of messages and the login status of users in the vehicle, additional design and processing shall be added to both the production end and the consumption end under this scheme, which is relatively complicated.

### By R&D environment

From the perspective of project implementation, environment variables are generally added in the design of the topic to achieve correctness under different R&D environments configurations.

### By data throughput

Due to different business requirements, the transmission frequency and packet size of the data are different regardless on whether it is uplink data or downlink data. Different data throughput will affect the processing and architecture design of the consumption end. For example, we often need to consider the consumption capacity of the application level when processing the vehicle data reporting business with high frequency. At this time, we may need to use the high throughput message queues such as Kafka to buffer the data, so as to prevent the data backlog and data loss caused by delayed application consumption. Therefore, in the definition of the topic of MQTT, we often need to distinguish the business with different data throughput.

## Application of Topic Design of MQTT Protocol in IoV Scenarios

### The vehicle actively reporting data 

Vehicle-mounted equipment (T-box, vehicle machine, etc.) is the collector of vehicle operation data, which packs the data of various controllers and sensors in the vehicle and sends them to the platform based on a fixed frequency. Generally, this kind of data can be designed in conformity with multiple levels such as vehicle model, frame No. and business data type of the reported data.

For example, with the consent of the user, the vehicle will report the location, speed, electricity and other information to the cloud platform at a fixed frequency in the process of driving. Based on this data, the cloud application provides location search, speeding reminder, electricity warning and geo-fencing service for the end users. 

### The vehicle reporting data after platform issued request 

When the cloud platform needs to obtain the latest status and information of the vehicle, it can actively issue commands to request vehicles to report data. Generally, this kind of scenario can be designed in conformity with frame No., business type and other levels.

For example, in the diagnosis scenario, the platform issues the diagnosis command to the vehicle through MQTT. When the equipment in the vehicle completes the diagnosis operation, the diagnosis data will be packaged and reported to the cloud platform. The vehicle diagnosis engineer will analyze the vehicle condition as a whole and locate the problem based on the collected diagnosis data.

### The platform issuing instructions 

Remote control of vehicle is the most common and typical scenario in the business of IoV. Each OEM provides various remote control functions in the mobile phone App, such as remote starting, remote door opening, remote flashing and honking and so on. In such scenarios, the mobile App sends control commands to the cloud platform. After a series of operations such as authority inspection and safety inspection, the platform application issues the command to the vehicle for execution through MQTT. After successful execution, the vehicle-end will asynchronously inform the platform of the execution result.

Generally, this kind of scenario can be designed in conformity with multiple levels such as uplink and downlink, frame number, business type and operation type.

### The platform issuing data after the request of vehicle client 

In Software Defined Vehicles (SDV), many configurations in the vehicle can be dynamically changed, such as data acquisition rules and security access rules. Therefore, the vehicle will actively request the latest relevant configuration of the platform after starting. If the configurations on both sides are inconsistent, the platform side will issue the latest configuration information to the vehicle and the vehicle side will take effect in real time.

Generally, this kind of scenario can be designed in conformity with multiple levels such as uplink and downlink, frame number and business type.

## Topic Design of TSP Platform of IoV with EMQX

As the world's leading MQTT message broker for IoT, [EMQX](https://www.emqx.com/en/products/emqx) is based on distributed cluster, large-scale concurrent connection, fast and low-latency message routing and other outstanding features, which can effectively process the business requirements of high-efficiency in IoV scenarios, greatly reduce end-to-end latency, and provide standard MQTT services for rapid deployment of large-scale IoV platforms.

### Advantages of EMQX in the IoV scenario 

#### Support of mass topics

With the increasing business in IoV, the number of topics carrying the business channels is also increasing, especially the requirement of one vehicle with one topic and one vehicle with multiple topics for vehicle control.  Because of this, the carrying capacity of the number of topics of MQTT Broker has become an important evaluation index of TSP platform.

EMQ has planned the ability to connect mass equipment and support mass topics from the beginning of the EMQX design. The common 3-node EMQX cluster with 16-core and 32G memory can support the simultaneous running of million-level topic, which provides flexible design space for the topic design of the TSP platform.

#### Powerful rules engine

EMQX provides a built-in [rule engine](https://www.emqx.com/en/solutions/mqtt-data-processing), which can provide data searching, filtering, splitting and rerouting messages for different topics. With the rule engine, we can reprocess the data in the existing topic by creating new routing rules and data pre-processing rules in the scenario where the existing vehicle-mounted equipment and application topics have been established. After the vehicle is launched, the new business application is supported by defining new rules on the platform side.

In EMQX Enterprise, the rule engine provides data persistence docking capability, which can directly dock data in different topics to different persistence schemes through the configuration in the rule engine. For example, for the data with high data throughput, the rules engine can be bridged to the high throughput message queues such as Kafka and Apache Pulsar for data buffering, while the topic data with small throughput and low-latency such as vehicle alarm can be directly connected to the application to realize fast routing consumption of data.

#### Proxy subscription function   

EMQX provides a proxy subscription function. The client does not need to send extra SUBSCRIBE packets when the connection is established, and the subscription relationship preset by the user can be established automatically. In this way, the platform side can directly manage the topic subscription relationship of the vehicle-mounted equipment, which is convenient for the platform side to carry out unified management.

#### Rich topic monitoring and slow subscription statistics

EMQX Enterprise provides running data monitoring with topic as a monitoring dimension. The total number of incoming, outgoing and discarding messages and current rate under the topic can be clearly seen in the EMQX visual Dashboard.

Since version 4.4, EMQX has provided statistics for slow subscriptions. This function tracks the time consumption of the whole message transmission process after the QoS1 and QoS2 messages arrive at EMQX, then uses the exponential moving average algorithm to calculate the average message transmission latency of the subscriber, and then ranks the subscribers in accordance with the latency.

By continuously monitoring the data reception and consumption of various topics during the operation of TSP platform, the platform operator can continuously adjust the platform business design and application design in accordance with the business changes, and realize the continuous optimization and expansion of the platform.

### Tips for using EMQX

When using EMQX as MQTT Broker for TSP platform of IoV, we need to pay attention to the following issues in the process of designing the topic:

- Wildcard usage and topic number level 

  EMQX uses the data structure of the topic tree to filter and match the topic. In the scenario of using wildcards to match multiple topics, if there are many topic levels, it will consume a lot of resources of EMQX. Therefore, in the design of the topic, it is recommended to limit the number of levels, generally no more than 5 levels.

- Consumption of the topic and memory 

  Since the number and length of topics in EMQX are mainly related to memory, we shall focus on monitoring the usage of EMQX cluster memory while carrying a large number of topics.



## Summary

With the popularization of MQTT protocol in IoV business, the topic design of MQTT messages of TSP platform of IoV will be the subject that each OEM and TSP platform scheme supplier must face. This article is the summary of MQTT topic design based on years of experience in the TSP platform.  The goal is to provide some help and inspiration to peers in the early stage of platform design and business expansion.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/a4b8936bb3d27fbccd734eccbe3f821b.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      Rev Up Your Connected Vehicles Future with MQTT
    </div>
    <div class="promotion-pdf__desc">
      The key to building a scalable, secure system for your connected-vehicles business.
    </div>
    <a href="https://www.emqx.com/en/resources/driving-the-future-of-connected-cars-with-mqtt?utm_campaign=embedded-driving-the-future-of-connected-cars-with-mqtt&from=blog-mqtt-topic-design-for-internet-of-vehicles" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>


## Other articles in this series

- [IoV beginner to master 01｜MQTT in an IoV scenario](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles)

- [IoV beginner to master 02｜Architecture Design of MQTT Message Platform for Ten-million-level IoV](https://www.emqx.com/en/blog/mqtt-messaging-platform-for-internet-of-vehicles)

- [IoV beginner to master 04 | MQTT QoS design: quality assurance for the IoV platform messaging](https://www.emqx.com/en/blog/mqtt-qos-design-for-internet-of-vehicles)
