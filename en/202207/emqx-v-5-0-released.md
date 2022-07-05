EMQ officially announced the latest release of its IoT platform and MQTT broker, EMQX 5.0. 
> View and download EMQX 5.0 at:
> - [https://www.emqx.com/en/try?product=broker](https://www.emqx.com/en/try?product=broker)
> - [https://github.com/emqx/emqx](https://github.com/emqx/emqx)

The latest version has been verified in [test scenarios](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) to scale to 100 million concurrent device connections, which is a critically important milestone for IoT designers. It also comes with plenty of exciting new features and huge performance improvements, including a more powerful rule engine, enhanced security management, Mria database extension, and much more to enhance the scalability of IoT applications.

Feng Lee, Founder and CEO of EMQ, said: “EMQX 5.0 is a huge accomplishment for MQTT technology, as it is the world’s first distributed MQTT broker to support 100M connections in a single cluster! It also introduces the first implementation of MQTT over QUIC. Keeping pace with the frontier of tech advancement is critical, and we’re committed to accelerating our product development cycle to tackle the grand challenges of large-scale IoT deployments.”

During the last several years, EMQX has gained popularity among IoT companies and is used by more than 20,000 global users from over 50 countries, with more than 100 million IoT device connections supported worldwide.


## EMQX 5.0 – Ready to Connect the Next Billion IoT Devices

A recent study by IoT Analytics concluded that “In 2022, the market for the IoT is expected to grow 18% to 14.4 billion active connections.” As the worldwide number of connected devices increases with the growing adoption of IoT in many industries, a huge amount of IoT data is being generated. That is why EMQ is focused on building an IoT platform that can handle billions of always-connected IoT devices.

EMQX was initially released under an open-source license in 2013. Since then, EMQ issued 200+ product releases and delivered more than 100 new features to its users. The updated features and functionality of EMQX 5.0 are designed to ease the IoT development process while enhancing the performance and scalability of its MQTT broker.

**EMQX 5.0 feature highlights:**

**Significant improvements in scalability and reliability**

The latest version adopts a new Mria extension for Erlang’s [Mnesia database](https://github.com/erlang/otp/pull/5926) that increases horizontal scalability by defining two different node types: core nodes and replicant nodes. This new architecture allows EMQX 5.0 to better adapt to increasing demand in IoT networks. The latest performance testing shows it can easily support 100M connections with a single cluster—a 10-fold increase over previous versions—making it the world’s most scalable open-source MQTT broker.

**The world’s first implementation of MQTT over QUIC**

EMQX 5.0 is also the first MQTT broker to introduce support for QUIC, the underlying transfer protocol for the next-generation HTTP/3 protocol used by modern web browsers. QUIC benefits IoT transmission scenarios by reducing connection overhead and latency compared to TCP, increasing overall throughput, and increasing stability for mobile connections. With support for QUIC, EMQ hopes to maintain EMQX’s ability to provide the most advanced and competitive MQTT servers for the next generation of internet connectivity.

**Bidirectional data flow through a more powerful rule engine**

The main improvement of the rule engine in version 5 is the unified interface for managing both northbound and southbound traffic. Users can combine the more powerful rule engine with EMQX’s data bridging functions to deliver southbound messages more efficiently without using external tools.

![IoT rule engine](https://assets.emqx.com/images/bf79ad87b1532f0026c135ea09f8c9fc.png)

<center>Using Apache Kafka to implement message processing and distribution</center>

At the same time, EMQ is also adding visualization capabilities to the rule engine. From the Dashboard, users can clearly see the topology of rule engine data flows, including data bridging from external enterprise data sources.

![IoT rule engine](https://assets.emqx.com/images/0e55fcee0a9a299801cd3e1970a9e870.png)

**Improved security management**

Users will enable authentication and permission control in a simpler way in EMQX 5.0: no need to change the configuration file of each node since controls can be configured for the entire cluster right from the Dashboard. Operation statistics, such as current trigger times and execution speed indicators, ensure that administrators can identify failed requests and abnormal traffic in time. 

**More Intuitive User Experience**

Ease-of-use improvements will be the most obvious change to users of EMQX 5.0. The Dashboard, with its new improved rule engine and action management UI/UX design, makes it easier to access the most frequently used functions according to users' roles. The concise and easy-to-read HOCON configuration file format, the OpenAPI 3.0 compliant REST API documents, more detailed monitoring metrics, log tracking, and slow subscription diagnostic tools will also bring developers a better experience.

**More than an MQTT broker**

EMQX not only fully supports MQTT 3.1, 3.1.1, and 5.0 protocols, but also [CoAP/LwM2M](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m), STOMP, MQTT-SN, and other mainstream IoT protocols. Version 5.0 uses a new gateway architecture to provide independent management interfaces and security authentication capabilities for protocols with different client attributes and life cycles. This improvement enables users to manage multi-protocol IoT networks more easily through a single, native interface.

In addition, version 5.0 allows developers to manage extension plug-ins more easily—compile, distribute, and install them as standalone plugin packages, which can be uploaded via the Dashboard, without needing to reboot the EMQX cluster. The redesigned ExHook also provides a more flexible way for users to extend and customize EMQX in other languages.

**EMQX 5.0 will go beyond the definition of an MQTT broker and become an all-in-one IoT Connectivity Management Platform that can connect any device, and integrate and expand arbitrarily.**


## Choosing the right components for your IoT connections

The technological breakthroughs of EMQX 5.0, in terms of cluster scalability and product stability, will provide critical IoT use cases with more efficient and reliable connections for massive device networks, high-performance messaging, and real-time processing of event streaming data. In addition, with improvements in product operability and usability, EMQX 5.0 will enhance users' experience and boost overall IoT business efficiency. 

As IoT is being implemented in almost all industries, it is hard to meet the increasingly rich, data-driven scenarios and diverse demands with a single technology or product. With EMQX as the core, EMQ delivers unified connection, movement, processing, and analysis of real-time data. In combination with its complete product portfolio from edge to cloud, EMQ can unlock the value of IoT data, and build a solid innovation digital base for the future world.


<section class="promotion">
    <div>
        Get Scalable and Robust IoT Connectivity with EMQX 5.0
    </div>
    <a href="https://www.emqx.com/en/try?product=broker" class="button is-gradient px-5">Get Started →</a>
</section>
