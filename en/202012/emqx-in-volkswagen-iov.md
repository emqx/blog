
IoV establishes the connection between cars and cars, cars and people, cars and roads through 「Cloud, Channel & Device」technology, and implement in-car information services, vehicle control automation, and intelligent transportation. Data interaction with T-Box and vehicle and machine systems through the IoV platform is also one of the main forms of intelligent interaction in IoV today. 

The Volkswagen Group has been focusing on vehicle and machine systems for a long time. The first generation of MIB was launched in 2013, and in terms of networking the first generation of MIB was the first to show the beginnings of IoV. From the first to the third generation, the MIB was rapidly iterated to reach the leading level at that time. **But the key difference between a smart vehicle and machine and a traditional vehicle and machine is its expandability. The ability to connect to the cloud and infinitely extend functions via download APP is the most essential feature of a smart car and machine, and it is also the trend in the development of the car and machine.**

In response to the trend of the times, SAIC Volkswagen is launching a new smart IoV system in 2020, in conjunction with the new MOS vehicle and machine system, first on the latest Passat models, a rare exploration of the Volkswagen brand's focus on the IoV field in the last two years.

From 2018, when SAIC Volkswagen designed and developed the new generation IoV system, the SC department took into account the needs of the new IoV scenario of large concurrency, low latency, and high throughput, referred to the mainstream new IoV system architecture at home and abroad, and adopted the MQTT protocol to establish the new generation IoV platform. The new IoV platform needs to be able to support SAIC Volkswagen's IoV development in the next few years, **which requires the [MQTT Broker](https://www.emqx.com/en/products/emqx)  in the platform to have the ability to support connectivity and data delivery from millions to tens of millions of IoV vehicle and machine,** covering IoV business support such as IoV data reporting, POI sending, pushing files, sending configuration, pushing messages, operation care, etc.

![1.jpeg](https://static.emqx.net/images/74feb63cc8309809382e65a841d9e8f5.jpeg)

In selecting the MQTT message broker for building the new platform, the SC department mainly considered the following functional and performance requirements:

### Functionality

Full support for the MQTT v3.1.1 protocol is required, and full support for the [MQTT v5.0](https://www.emqx.com/en/mqtt/mqtt5) protocol will be available at a later stage. For SAIC Volkswagen's scenarios in IoV applications, the following features also need to be supported:

1. Support the persistence of the data reported by the vehicle and machine on the platform side to ensure that the data is not lost.
1. In the scenario of POI sending, support to be informed at the platform side whether the feedback information of the message is received at the vehicle and machine side; the platform-side provides caching the data POI send and can set the caching time of POI to ensure that the sending message is not lost when the vehicle and machine are offline, and the message is automatically sent after going online.
1. Support the platform to push files to the vehicle and machine, configure push, support broadcast-type push.
1. In terms of security, the device supports security authentication through certificates, and the device connection supports TLS1.2; for illegal connections to the platform, the client can carry out client authentication control, and the platform side can also close illegal connections through the API.

### Performance

The following capabilities are required:

1. With the ability to support distributed architecture and horizontal expansion, support for cluster deployment; cluster with high availability, support for automatic node discovery, automatic clustering, automatic deletion of downtime node capability.
1. Performance indicators: on a 16-core, 32G memory Linux operating system, the number of connections to a single node is not less than 500,000; the total number of connections to a single cluster is not less than 10 million.
1. Considering the actual scenario where each vehicle will have one to multiple unique topics, it needs to be able to support 10 million topics.

### Deployment

The ability to deploy in SAIC Volkswagen's private cloud environment and support docker container deployment is required to facilitate the subsequent unified deployment and maintenance of microservice nodes with the overall system.

### Operations and maintenance

A comprehensive monitoring system is required, and the export and integration of monitoring data are also required. The monitoring indicators need to include the overall business indicators of the cluster, including the number of connections, messages, topics, message throughput, etc. The node system monitoring information includes the CPU of node, memory, network, disk I/O, virtual machine internal indicators, etc.

With these requirements in mind, **SAIC Volkswagen chose EMQ X Enterprise as the IoT MQTT messaging broker for its next-generation IoV access platform** after more than a year of comparative analysis and functional performance testing of different products.

![2.png](https://static.emqx.net/images/f4a466363c48f0018aecc91d6564f123.png)

EMQ X, a well-known open-source MQTT messaging broker project, provides secure and stable access and low latency data processing capabilities for T-box and mobile devices in the millions to tens of millions range. The EMQ X Enterprise based IoV access layer solution provides features such as **data persistence, southbound message caching, secure connectivity, and secure authentication** to meet SAIC Volkswagen's needs in the next generation establishment of IoV.

![3.png](https://static.emqx.net/images/131d31c9c2cdafeea323a8254bd29fd3.png)SAIC Volkswagen IoV Access Platform Operation and Maintenance Dashboard

This year, SAIC Volkswagen's new-generation IoV platform was on-line, and more new models have been connected one after another. The total number of vehicles connected to the platform has now reached hundreds of thousands and is still growing, while the platform has always maintained a stable operation. So far, with EMQ X, the business needs of SAIC Volkswagen's new IoV and new vehicle and machine system in the access layer have been met. On this basis, SAIC Volkswagen is also actively investigating the implementation of more business rule filtering and distribution in the messaging middleware layer based on the built-in rule engine and codec capabilities provided in the new version of EMQ X, to provide a more convenient data interface for the development of upper-layer applications.

In the future, SAIC Volkswagen's new-generation IoV platform will continue to connect to more new models of the brand's other petrol cars and new energy vehicles, providing SAIC Volkswagen customers with a more intelligent and convenient human-vehicle interaction experience and creating a new generation of the human-vehicle social platform.