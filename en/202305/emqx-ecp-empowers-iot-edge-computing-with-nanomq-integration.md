> EMQX Edge Cloud Platform (ECP) is a one-stop management platform for the EMQX product suite. It provides enterprise-level users with solutions for multi-tenant management, multi-project management, multi-cluster management, cloud-edge collaboration, authentication security, and auditing requirements.
>
> EMQX ECP offers full lifecycle management for [EMQX Enterprise](https://www.emqx.com/en/products/emqx), including automatic deployment, deletion, upgrade, elastic scaling, monitoring, and alarm functions. It also provides batch access and batch configuration management for EMQ edge services such as Neuron, eKuiper, and NanoMQ.

## Introduction

In the rapidly evolving landscape of IoT edge computing, efficient and reliable management of edge services is crucial. In the previous release, EMQX Edge to Cloud Platform (EMQX ECP) provides remote management and monitoring capabilities to [Neuron](https://neugates.io/) and [eKuiper](https://ekuiper.org/). With the release of v1.10, the EMQX ECP  takes a significant stride forward by integrating [NanoMQ](https://nanomq.io/) - a lightweight, high-performance MQTT broker designed for efficient message routing in IoT edge computing scenarios. This integration unlocks the capabilities of remote management and monitoring of NanoMQ deployments. 

## NanoMQ Management in EMQX ECP

NanoMQ, as the next generation of lightweight and high-performance MQTT messaging broker, holds immense value in IoT edge message routing and edge computing scenarios. By seamlessly integrating NanoMQ within EMQX ECP, organizations gain a comprehensive edge-to-cloud solution that ensures efficient communication, scalability, and reliability in their IoT deployments.

### Use Case 1: Remote Management of Industry IoT Gateways in Digital Factories

In digitized manufacturing factories, the industrial equipment in workshops generates production data. This data is collected and converted into industrial protocols using small-scale industrial gateway devices and data acquisition software. Once unified under the IoT MQTT protocol, the data is transmitted in real-time to factory or cloud-based data centers for monitoring. It can also be exchanged locally within the factory based on specific business needs. 

NanoMQ, can be deployed in various industrial gateways in the workshop. It aggregates data for centralized transmission and enables local device-to-device data routing through rule engines.

![NanoMQ & ECP](https://assets.emqx.com/images/a6f33862d88b3036763d2c6e54ba4b66.png)

Version 1.10 facilitates remote management and monitoring of NanoMQ devices in factory workshops by deploying EMQX ECP in the data center or cloud.

This proves particularly advantageous when multiple NanoMQ instances are deployed across various workshops, as it significantly reduces local management costs. Furthermore, EMQX ECP's real-time monitoring capabilities for NanoMQ enable system administrators to promptly detect and resolve IoT data link issues, ensuring smooth and efficient data transmission throughout the network.

### Use Case 2:  Empowering Connected Vehicle Data Bridge Management

In the realm of connected vehicles, establishing a robust and efficient data bridge between in-car systems and the cloud is essential to unlocking the full potential of advanced automotive services. As a lightweight MQTT broker, NanoMQ is pivotal in enabling seamless data bridging capabilities, particularly between in-vehicle data buses like DDS, Some/IP, [CAN Bus](https://www.emqx.com/en/blog/can-bus-how-it-works-pros-and-cons), and the cloud using the MQTT protocol.

![Empowering Connected Vehicle Data Bridge Management](https://assets.emqx.com/images/3d82b2e41c8b229ea8d0982e5864cf8f.png)

EMQX ECP complements NanoMQ by providing robust remote management and monitoring capabilities for large-scale connected vehicle data bridges. With EMQX ECP, system administrators gain centralized control over NanoMQ deployments, simplifying management, monitoring, and troubleshooting processes.

## Conclusion

NanoMQ's lightweight MQTT broker capabilities and EMQX ECP's remote management and monitoring features form a powerful solution for all kinds of IoT edge-to-cloud data bridging. They enable seamless and secure communication between edge devices and the Cloud using MQTT, empowering many industries with advanced functionalities and efficient data exchange.
