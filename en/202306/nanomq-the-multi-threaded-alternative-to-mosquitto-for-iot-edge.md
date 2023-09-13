## Introduction

This is an era of information explosion. With the advent of IoT and the proliferation of connected devices, processing all the data in the cloud is no longer possible. The edge computing paradigm has been on the rising path. It aims to push the frontier of computing applications, data, and services away from the cloud-centric servers to the network's boundary. 

The benefits of this paradigm shift include the following:

- Lower latency, better reactivity and reliability.
- Reduced data transfer costs toward the cloud services.
- Enhanced confidentiality. 

## The Paradigm Shift of Edge Computing 

Edge computing technology communicates upwards to the cloud and downwards to the end nodes. It acts as a middle ground between cloud computing and embedded systems. With the edge sitting right in the middle, it's necessary to orchestrate both ways. Additionally, for the embedded world, there is a long-existing triangle dilemma: engineers need to find a sweet point among cost (power, maintenance) - size (memory, CPU) - performance (throughput, latency) when developing applications for the edge. Edge computing comes with unique challenges.

The shifting paradigm has a great impact on edge MQTT Messaging Services. While moving computation from the cloud to the edge, close to the source of data, significantly change the way it moves and converges data on the edge. Nowadays, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is the de-facto standard for ingesting IoT data. Hence the MQTT middleware faces the challenges directly, especially for the previously commonly used edge broker such as [Mosquitto](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives). Here are three glaringly apparent challenges:

### Trend #1: From Single-Core to Multi-Core

Due to the increasing number of device connections on edge, one of the biggest conundrums of edge computing is simultaneously achieving high performance for computation and I/O intensive applications (like ML and [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)) while minimizing power consumption. Historically, engineers enjoy the free lunch of the increased clock frequencies to achieve better performance and lower power consumption. But that is no longer the case. We have seen the multi-core trend in the HPC and data center industry. The same story that happens on edge is highly within anticipation. 

![A single thread with single Core CPU](https://assets.emqx.com/images/4e2d47de56a16f4b14980fcb6280cde0.png)

<p style="text-align: center">A single thread with single Core CPU</p>

![Single thread on Modern multi-core CPU](https://assets.emqx.com/images/557a6f8519fe50021c90ca201c1f5057.png)

<p style="text-align: center">Single thread on Modern multi-core CPU</p>

![Slice 121.png](https://assets.emqx.com/images/e3409a3453ed5cb1fba4bdb607ef6f64.png)

<p style="text-align: center">Main thread + Epoll work as a scheduler to dispatch the tasks to Actor threads</p>

<p style="text-align: center">(Image Sourced From the Internet)</p>

### Trend #2: Computation Offloading

Heterogeneous computing is widely adopted for Edge AI applications; It reduces data transmission costs toward cloud servers thanks to enhanced local data processing capabilities. It requires transferring data from sensors to an AI accelerator or DSP enhanced for a typical type of computation. This concept is well known as computation offloading. It is usually achieved via onboard bus I/O when data and destination are on the identical PCB. However, this is not the typical case; where data originated is usually far from where it should be computed. Hence we need a messaging service capable of knowing the context of data and diverting them to a desirable consumer—and keeping the data intact when working in a lossy networking environment. So that it decouples the edge node and diminishes the complexity of the local network topology. Additionally, a messaging broker that supports event-driven architecture would be a plus.

### Trend #3: Interoperability

Interoperability is a characteristic of an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), whose interfaces are completely understood to work with other systems in the edge or cloud, in either ingestion or access, without any restrictions. Under the circumstance of edge computing, it refers to:

- **Edge-cloud Orchestration**

  IoT devices are geographically distributed, and it isn't easy to manage and monitor their lifecycle remotely. Container-based technology is emerging to resolve this problem. The Edge MQTT broker should provide RESTful APIs to integrate cloud-native architecture to achieve edge-cloud orchestration.

- **All-in-one Protocol Support**

  On edge, the IoT ecosystem is fragmented. ZeroMQ and nanomsg/nng are still commonly used in brokerless scenarios. MQTT is a broker-centric protocol that is not suitable for brokerless. Therefore an edge messaging service that can support both broker and brokerless and is flexible in topology when building a bridging network is urgently needed.

## The Comparison Between Mosquitto and NanoMQ

In the last chapter, we have already clarified the challenges ahead. Now it is time to check those previous popular MQTT brokers on edge. We take [Mosquitto](https://mosquitto.org/) as an example to compete with [NanoMQ](https://nanomq.io/) in a fair competition regarding these three challenges.

### The Case of Mosquitto

The [Mosquitto](https://mosquitto.org/) project was initially developed by Roger Light in 2009 and later donated to the Eclipse Foundation. By far, Mosquitto is the most longevity MQTT project and shares a great reputation among users.

Mosquitto's design is straightforward and clean. It runs as a single-threaded daemon process with epoll support. It receives incoming data from one socket and dispatches it to other sockets.

- **Single-threaded**: In the latest 2.0+ version, Mosquitto still runs as a single-threaded application and thus doesn't allow edge applications to take the benefit of multi-core CPUs. Single-threaded design limits the maximum number of publishers on the system, especially for the latency-sensitive application.
- **Computation offloading**: Despite third-party plugins, the Mosquitto project does not support a rule engine or any other method to filter, enrich, or transform MQTT messages. It is challenging to build an event-driven architecture on top of Mosquitto since there is no native event producer. 
- **Interoperability**: Mosquitto provides no RESTful HTTP API (before 2.0.1). It is hard to integrate with external systems such as device management. The most recent 2.0 version focuses on security improvement rather than enhancing integration capabilities.

Apparently, Mosquitto targets traditional embedded scenarios, which means it is more resource-friendly and consumes less memory and CPU. Therefore, Mosquitto is ideal for IoT sensors and devices with low processing power.

### The Silver Bullet from NanoMQ

While Mosquitto is focusing more on cost-efficiency, NanoMQ ([https://github.com/nanomq/nanomq](https://github.com/nanomq/nanomq)) fills the vacancy. In the following chapters, I will walk you through how NanoMQ resolves these challenges and explain why it is the best alternative to Mosquitto in the edge-computing era.

#### Actor on Edge: From 1 to N

Before we dive into the solution, let's glance at the hardware side. Historically, engineers have relied on Moore's law and increased clock frequencies to achieve better performance and lower power—but that is no longer the case. It is simply not efficient to keep cranking up the frequency of a device, especially in an embedded or mobile system, so in the last decade, instead of using the single-core, high-frequency architecture. The industry chose the multi-core and turned the frequency down. But this resulted in significant changes in the programming model. We must spread the computation over multiple courses, especially for I/O intensive middleware like MQTT broker.

Another significant cause of multi-core trending is the semiconductor process hits an invisible wall :

![The single-thread performance is flattening out](https://assets.emqx.com/images/5eea878de15d33a729f85aefeb3faef5.png)

<p style="text-align: center">Plot by Karl Rupp from his <a href="https://github.com/karlrupp/microprocessor-trend-data">microprocessor trend data</a> (CC BY 4.0 license)</p>

As we can see from the chart, the single-thread performance is flattening out. Single-core frequency is struggling over the past two decades. The situation is even worse in edge due to power efficiency and heating problem. But there is only one metric that keeps advancing: the number of cores. 

The idea is that using multiple parallel cores at a lower frequency can achieve the same computational performance as a single core at a higher frequency. The difference, of course, is that multi-core architectures can achieve lower power consumption for the same performance. But the cost of optimism is rising.

#### Parallelism is Salvation

According to [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl's_law), in order to take advantage of a multi-core system, we need to parallelize the code to get the best optimization margin. The serialized code is the part really dragging the software back.  

![Amdahl's law](https://assets.emqx.com/images/25880a7200713d6d00a229c05e3e1132.png)

However, switching to parallel computing needs to solve the following problem:

- Shared state of objects
- Race conditions
- Blocking calls
- Deadlocks
- Memory copy

Unfortunately, in terms of MQTT, there is some tricky logic base on blocking calls that is hard to parallelize, like QoS delivery and topic filtering. Even worse, the fan-out message pattern like broadcasting often leads to a massive memory copy to avoid data racing, which is unacceptable for memory-limited devices. NanoMQ finds a perfect spot to balance the size and performance by implementing a built-in Actor model.

![Actor System](https://assets.emqx.com/images/a261a38d6a36c9391bee1df1686db796.png)

![Actor System](https://assets.emqx.com/images/e2d3ce4eda6bc7a7a86e6013a47af587.png)

The Actor model is a powerful concept of designing software inspired by physics. The internal actor system of NanoMQ is based on the optimized NNG's asynchronous I/O framework toward Linux & MQTT. Abstracting all the computation into several actors, exchange immutable messages among them in an efficient manner. 

NanoMQ elegantly tackles a range of challenges mentioned above with its delicate design:

- Race conditions - Immutable messages
- Blocking calls - Fully asynchronous I/O inside
- Deadlocks - Thread level parallelism
- Memory copy - Zero Copy

Thanks to the innovative actor model on edge, NanoMQ is on multi-threading steroids. It can scale out easily to engage multiple cores with less CPU usage in the modern SMP system. There is no doubt that NanoMQ is more scalable (check [benchmark result](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-mosquitto-vs-nanomq)), while the Zero-Copy feature makes it remains at the same level in terms of memory consumption compared to Mosquitto.

#### Offloading with Rule Engine and WebHook

Computation offloading refers to the transfer of computational tasks to a remote device or cloud platform. In recent years, the industry introduced the concept of [Unified Namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot)(UNS) to make data-stream reusable and reduce network complexity. MQTT broker fits in this place perfectly.

However, the flexibility of offloading strategies requires brokers to provide a context-knowing rule engine to manipulate message sink. Mosquitto and NanoMQ are both MQTT broker that meets the first requirement, but NanoMQ offers awesome features like a built-in rule engine, offline caching, and data persistence, which Mosquitto does not. Data persistence and offline caching are essential when edge applications are running in offline mode and want to keep data safe. NanoMQ is able to resume transmission after the network is restored or persist full-scale data in the backup database. As for Mosquitto, there is no rule engine or protocol proxy, but it also provides data caching feature on SQLite and files. However, this feature is highly limited by the single-threaded design. The broker stops responding to any message when there are too many synchronized disk writing operations.

Furthermore, NanoMQ has a webhook system that is easy to work with old-fashioned HTTP-based applications. It is useful when updating the edge architecture without modifying the existing service to MQTT.

The rule engine of NanoMQ is still in a primitive stage and only supports a minority of SQL. Nonetheless, it is still can make a difference.

#### Interoperability: Broker+Brokerless+HTTP APIs

- **Edge-cloud orchestration**

  NanoMQ provides rich RESTful APIs, including monitoring and remote modification. It allows users to configure broker via environment variables when deploying as docker. Therefore, NanoMQ is more cloud-native friendly compared to Mosquitto.

- **All-in-one protocol support**

  NanoMQ is not only an MQTT broker but also a competent messaging bus on edge. ZeroMQ, DDS and nanomsg/nng are also within the grasp of NanoMQ: it provides a stand-alone proxy plugin to bridge ZeroMQ/DDS/SOME-IP messages with the internal MQTT broker; Even better, NanoMQ can communicate with nanomsg/nng client natively via IPC.

  ![All-in-one protocol support](https://assets.emqx.com/images/95d944d7d884c01a70d894accf40ede5.png)

Interoperability is where these two popular brokers really show different positioning. While Mosquitto is a project with a longevity history of being a lightweight MQTT broker on both cloud and edge, NanoMQ is a newly born project in the modern cloud-native era. Obviously, NanoMQ targets the edge computing field with all-round capabilities, but Mosquitto still remains as the best option for fast deploying as simple MQTT broker.

To align with the newly emerging architecture – UNS, NanoMQ is a good start if you are looking for a tiny but powerful broker that can relieve you from endless protocol conversion.

## The Final Words 

In the end, NanoMQ is in its youth, with less than three years of Open-Source history. There are certain downsides that could be imagined compared to Mosquitto's legacy, lack of well-decorated Docs and tutorials, potential security issues, and a relatively small user base are the main reasons that hinder common users from adapting to new alternatives. Change is always difficult, but always good to be prepared by knowing what could be your backup options. 





<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>
