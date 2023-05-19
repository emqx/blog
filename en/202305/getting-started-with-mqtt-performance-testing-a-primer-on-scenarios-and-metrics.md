## Introduction

In the IoT industry, a large number of resource-constrained sensors and industrial control devices rely on unreliable and low-bandwidth networks. This reality has propelled the popularity of MQTT as an ideal IoT message transmission protocol for IoT scenarios. Consequently, it becomes crucial for [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to ensure optimal performance and high reliability to meet the demands of IoT applications.

It's essential to understand the basic testing scenarios and performance metrics before conducting a suitable test for your system. In this blog, we will give a comprehensive explanation based on the testing experience of the EMQX team, which is also applicable to all MQTT brokers testing.

>**Terms Explanation**
>
>- MQTT Protocol: MQTT stands for Message Queuing Telemetry Transport. Despite its name containing "message queuing," it has nothing to do with message queues. Instead, it is a lightweight messaging protocol based on a publish/subscribe model. With its simplicity, flexibility, easy implementation, support for QoS, and small message size, MQTT has become the preferred protocol for the Internet of Things (IoT). For more information, please refer to [MQTT Guide 2023: Beginner to Advanced](https://www.emqx.com/en/mqtt).
>- Performance Testing: Performance testing is a process of using testing tools to simulate various normal, peak, or abnormal load conditions to test various performance indicators of the system under tested. The goal is to verify whether the system can meet the user's expectation, discover performance bottlenecks in the system, and so on.

## Typical MQTT Test Scenarios

There are two main test scenarios for MQTT brokers:

- Concurrent connection, including concurrent connection numbers and connection rates.
- Message throughput, including throughput for message sending and receiving, with some performance-affecting parameters, such as [QoS](https://www.emqx.com/en/blog/introduction-to-mqtt-qos), payload size, [topic wildcard](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), to simulate the production environment requirements.

The following two aspects must always be considered when designing specific performance test scenarios, especially for PoC or pre-deployment test:

- Simulating usage scenarios in the real production environment as much as possible;
- Covering possible peak load.

Test scenarios can be subdivided into the two basic dimensions of connection and message throughput.

### Concurrent Connection Testing

MQTT connections are long (keep-alive) TCP connections. The client initiates a TCP connection with the [MQTT broker](https://www.emqx.io/), sends an MQTT login request, and then uses heartbeat packets to sustain the connection. In high-concurrency scenarios, establishing and maintaining long MQTT connections consumes significant resources for the broker. Through performance testing, we can measure how many concurrent connections the MQTT broker can support under limited resources.

On the other hand, the higher the connection rate (i.e., the new established connections per second), the greater the computing resources required at the same time. It's important to consider this factor during testing, especially in scenarios where numerous devices may come online simultaneously. This value is crucial for evaluating system capacity and planning accordingly.

The third factor to consider in concurrent connection testing is whether to use TLS/SSL encrypted transmission, as it consumes additional resources. It is necessary to evaluate the degree of its impact on performance during testing.

To summarize, in MQTT concurrent connection testing, the following three scenarios should be considered:

1. Gradually increase concurrent connections at a low connection rate to test system response and resource consumption. This can also determine the maximum concurrency the system can support under given hardware and network resources.
2. With a fixed number of concurrent connections, test the system's response and resource consumption at different connection rates.
3. Differentiate between regular TCP connections and TLS/SSL encrypted connections when designing 1) and 2).

### Message Throughput Testing

As mentioned earlier, MQTT is a message transfer protocol based on the [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model). It is an asynchronous protocol that implements 1-to-1, 1-to-many, and many-to-1 types of publishing and subscription, which are widely used in various IoT scenarios. Therefore, message throughput testing should include these three scenarios:

1. 1-to-1 symmetric: The number of publishers and subscribers is the same. For each publisher, there is exactly one subscriber to the published topic. In another word, the incoming messages rate is equal to the outgoing rate for the MQTT broker.
2. Fan-in: A typical IoT applications scenario with many IoT devices acting as publishers, but only a few or a single subscriber, for example, a large number of devices reporting its status or data.
3. Fan-out: A large number of devices subscribing to one or a few publishers.

Besides, when designing message throughput scenarios, do not forget QoS, message payload size, subscription topics with wildcards, and etc. Different QoS significantly impact performance and resource consumption for load tests. The payload size can be determined based on the actual use cases.

### Other Scenarios

For other MQTT functionalities, such as Shared Subscription, messages dumping to databases or MQ, a large number of topic subscriptions, and extreme situations like numerous [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) connecting/disconnecting simultaneously, these can be planned and incorporated into the testing scenarios based on actual requirements.

## Performance Metrics

After designing a proper testing scenario, it is also important to develop performance metrics to measure the success or failure of the test.

In performance testing, the metrics can generally be divided into two categories: application system metrics (here, i.e. MQTT broker metrics) and computing resource metrics.

- Application system metrics are related to user scenarios and requirements, such as response time (or latency) and concurrency. 
- Computing resource metrics are related to hardware resource consumption. For MQTT we’re talking about, the metrics are similar to those of other software performance tests, such as CPU, memory, network, and disk I/O. 

The MQTT system metrics are closely related to the testing scenario, and the common ones are summarized in the table below.

![image.png](https://assets.emqx.com/images/6edc93931b8d86432b64b86413c92b4c.png)

## Performance Testing Tools

Large-scale performance testing demands a tool that can efficiently simulate high-concurrency and high-throughput scenarios, as well as manage numerous machines/resources.

The EMQX team uses emqtt_bench and XMeter as performance testing tools.

### emqtt_bench 

emqtt_bench is a performance testing tool for MQTT protocol developed by the EMQX R&D team written with Erlang. After installation, it can be used via the command line. 

```
Usage: emqtt_bench pub | sub | conn
```

Compared to other tools, the advantage of emqtt_bench is that it is easy to install and use, and requires fewer computing resources. However, it supports limited scenarios and lacks test metric data.

> For installation and usage, please refer to [emqtt-bench: Lightweight MQTT benchmark tool written in Erlang](https://github.com/emqx/emqtt-bench) 

### XMeter

emqtt_bench is suitable for rapid performance verification in the development phase. When it comes to large-scale scenarios or formal testing, we recommend another more professional performance and load test tool - [XMeter](https://www.emqx.com/en/products/xmeter).

XMeter builds upon the foundation of JMeter, enhancing its scalability and expanding its capabilities. This enables XMeter to handle high volumes of data and perform high-frequency testing. It provides comprehensive and real-time test reports during the test, and the reports show the testers real-time MQTT metrics data such as throughput, response time, success rate and etc. And its built-in monitoring system is used to collect the resource usage of the MQTT broker server. 

Besides, XMeter provides the capability of automatic and centralized test resource management. Test machines (containers) are automatically created at the beginning of the test and destroyed at the end. 

Throughout the test phase, XMeter will graphically display MQTT performance metrics and computing resource usage in real-time, as the reports shown in the following figures.

![Summary Information & Trend Charts Over Time](https://assets.emqx.com/images/2f73099734b1d09a90799def40235ee4.png)

<center>Figure 1 XMeter report - Summary Information & Trend Charts Over Time</center>

<br>

![Test data details](https://assets.emqx.com/images/74a149f2e19bbb3706ea220c85245592.png)

<center>Figure 2 XMeter report - Test data details</center>

<br>

![Monitoring](https://assets.emqx.com/images/80559bc15d2c725246114df0210c407f.png)

<center>Figure 3 XMeter report - Monitoring</center>

<br>

![Test info](https://assets.emqx.com/images/5a49f0248e2d268226c1ff385e96f755.png)

<center>Figure 4 XMeter report - Test info</center>

<br>

![Test machine monitoring](https://assets.emqx.com/images/2dd7129ed48bda92ae05c37dde3283d2.png)

<center>Figure 5 XMeter report - Test machine monitoring</center>

<br>

**How to use XMeter**

XMeter offers two versions. 

- XMeter on-premise. It is deal for organizations that require complete control over their testing environment and need to comply with strict security and data privacy regulations. To get started, you need to:

  1. Download mqtt-jmeter plugin developed and open-sourced by the XMeter team from [GitHub - emqx/mqtt-jmeter: MQTT JMeter Plugin](https://github.com/emqx/mqtt-jmeter).

  2. Place the jar file in the JMeter directory.

  3. Write test scripts in JMeter according to test cases, as shown in Figure 6.

  4. Upload the script to XMeter and start testing MQTT performance.

     ![JMeter test script for MQTT test](https://assets.emqx.com/images/7563e56063d748846bbb7adf580802e0.png)

     <center>Figure 6 JMeter test script for MQTT test</center>

- [XMeter Cloud](https://xmeter-cloud.emqx.com/). It is ideal for organizations that want to quickly get started with load testing and performance monitoring without worrying about infrastructure setup and maintenance. To get start, you just need to sign up for a free trial on the [website](https://xmeter-cloud.emqx.com/), then refer to [the document](https://docs.emqx.com/en/xmeter-cloud/latest/) to start your first XMeter run.

## Wrapping up

In this post, we have discussed several typical testing scenarios and important metrics that can be used to evaluate the performance of MQTT brokers. By understanding and applying these testing techniques and metrics, you can optimize the performance and reliability, and improve the overall IoT and messaging system infrastructure.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
