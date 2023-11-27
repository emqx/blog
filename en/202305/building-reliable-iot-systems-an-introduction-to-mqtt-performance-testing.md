## Introduction

The Internet of Things (IoT) is experiencing a burst of growth in the recent decade. More complicated applications and services are built on large amounts of IoT devices and data. Not only shall we ensure the correctness of the business functionalities of those IoT systems, but we also need to ensure the system works properly with continuous communications among such a large volume of devices.

That’s why we need performance testing for building reliable IoT systems.

## Why is Performance Testing Important to IoT Systems?

It is already a common practice to take integration testing and end-to-end testing to ensure the functionality of IoT systems.

Performance testing is a way to verify the robustness of a system, which concerns metrics like scalability, availability, reliability and so on. It can help find out how the system behaves under normal usage, as well as under extreme use conditions.

Adopting performance testing in developing IoT systems provides an evaluation based on designed attributes. Comparing the testing result with benchmarks makes it possible to determine if there is degeneration in system performance. 

When introduced into continuous integration, performance testing helps to identify system performance bottlenecks and catch issues before they become costly.

In addition, performance testing provides a reference for capacity planning and helps to take advantage of opportunities.

## What Does Performance Testing Concern in IoT Systems?

To evaluate an IoT system, two primary perspectives are concerned during performance testing. 

- How well the IoT system performs. That means if the system can handle load increases, if the system can handle problems and failures for extreme conditions, if the system's latency is within acceptable range. There are metrics to quantify the above attributes, like response time, throughput, success rate, deviation, etc. 
- How many computing resources are used to meet expected system capacity. There is no doubt that fewer computing resources save money and bring more profit if the same goal can be achieved. Metrics to quantify the computing resources include CPU usage, memory usage, disk I/O rate, packets transfer rate, etc.

## Typical Scenarios in MQTT Performance Testing

Although different scenarios and test cases are used to meet specific requirements for various systems and protocols, there are common types we can refer to when designing a performance test for IoT system:  

- Test how the system performs under stable conditions. The purpose is to verify if the system meets expectations for normal use.
- Test how the system performs under short-term overwhelming load. The purpose is to verify if the system still works or can quickly recover from failure when encountering unexpected stress.
- Test how the system performs for a long time. The purpose is to verify if the system keeps stable if continuously running for a period of time.
- Test how the system performs in an unstable network condition. The purpose is to verify if the system can handle situations of weak networks, which is common for IoT services.

As MQTT is most widely used in IoT industry,  we also list some typical testing scenarios for MQTT protocol based on real customer requirements:

- Connection: Clients connect to the broker within a period of time, and keep the connections with the broker for quite a while.
- Fan-out: Many clients act as subscribers, with only a few or a single publisher.
- Point-to-point: Equal number of clients act as publishers as well as subscribers.
- Fan-in: Many clients act as publishers, with only a few or a single subscriber.

In the context of [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model),  the key point to design testing scenarios for MQTT is considering how to simulate different behaviors of publishers and subscribers.

## Challenges For MQTT Performance Testing

Challenges also come along with performance testing for IoT systems. IoT systems are different from traditional Internet systems in aspects of architecture, network patterns, communication protocols and so on. Therefore traditional performance testing methodology cannot be directly adopted into IoT systems.

First, IoT systems connect to and communicate with many devices and generate massive data. It is essential to simulate the realistic scale in performance testing. It requires a more sophisticated design on the tool that performs load and more effective analysis of testing results.

Second, IoT messaging is distinct from Internet messaging, resulting in various IoT communication protocols. 

As for MQTT protocol, some of its characteristics make it quite different from Internet messaging protocols:

- MQTT is lightweight and designed especially for unstable network connections and bandwidth saving.
- MQTT uses QoS to support for complex device network environments.
- MQTT is data irrelevant.
- MQTT is aware of continuous session.

When performing tests against MQTT protocol, it is also important to meet its unique features.

## EMQ's Performance Testing Solution

Performance testing is critical for IoT systems to minimize risks, improve robustness, and help enterprises to achieve business goals in the rapidly growing IoT industry.

EMQ has proposed the [Open MQTT Benchmark Suite](https://github.com/emqx/mqttbs) to provide a feasible way for MQTT benchmark. It analyzes the key metrics for performance evaluation and presents practical use cases for benchmark testing. Developers can get an impartial comparison reference between different MQTT brokers and make an informed selection.

Read our blog for more information: [Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing).

[XMeter](https://www.emqx.com/en/products/xmeter) is another EMQ product that provides load testing service for MQTT protocol as well as other [IoT protocols](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m). XMeter horizontally scales to simulate millions of [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools), collects and processes data in a stream way, and renders a report containing primary performance metrics. To learn more about the fully managed XMeter Cloud service, please refer to [XMeter: Fully Managed MQTT Load Testing Service](https://www.emqx.com/en/products/xmeter).
