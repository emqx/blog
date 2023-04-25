## Introduction

We are thrilled to announce that the [Open MQTT Benchmark Suite](https://github.com/emqx/mqttbs) presented by EMQ is now available! With typical and practical use cases, primary metrics for measuring broker performance, and a tool to simulate loads and collect benchmark results, our Open MQTT Benchmark Suite can help you evaluate the scalability and performance of MQTT brokers to make an informed selection.

![MQTT Performance Testing](https://assets.emqx.com/images/88392ce7081424a43dffcdecbfe2b61b.png)

## Born for Impartial MQTT Load Testing

The MQTT broker is central in connecting devices and transferring IoT data in the [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) context. With IoT proliferating, the challenging problem of handling massive devices and high data throughput makes an MQTT broker's scalability and performance crucial for any IoT solution.

The Open MQTT Benchmark Suite is designed to provide an impartial and practical way to test MQTT brokers. It will simplify MQTT broker load testing with the following main advantages:

**Offering an open and practical evaluation base**

Despite numerous research papers and technical writeups evaluating and comparing MQTT brokers, the current benchmarks typically measure only specific factors and do not reflect the real-world scenarios of large-scale IoT applications. Our Open MQTT Benchmark Suite thoroughly examines the key factors for evaluation from various aspects and designs scenarios that are impartial towards any brokers, with the goal of establishing an unbiased testing base.

**Based on real use cases and feasible metrics for measurement**

We have analyzed and addressed a significant number of actual testing requirements from our customers, and based on that, we have developed this Open MQTT Benchmark Suite. We are confident that this benchmark suite can fulfill the majority of testing requirements.

**Open to the community for a comprehensive benchmark**

We are committed to building an open and collaborative community around our MQTT benchmark suite. By including diverse use cases contributed by the community, our suite will accurately reflect the needs and requirements of the industry. Join us in building a comprehensive benchmark suite for the MQTT protocol and help us empower users to be well-informed about their MQTT broker choices.

## What’s Inside the Open MQTT Benchmark Suite

The Open MQTT Benchmark Suite's first edition introduces the key factors affecting MQTT broker performance and defines metrics for measuring scalability, availability, latency, and computing resource cost.

Next, the benchmark suite categorizes typical usage scenarios into connection, fan-out, point-to-point, and fan-in and includes practical use cases based on real-world customer requirements.

To illustrate how these use cases are applied in benchmarking, we provide several examples with detailed benchmark results.

## An Example Benchmark Result

To demonstrate a practical example, we present below the detail of a fan-out use case and benchmarking result using [NanoMQ](https://nanomq.io) as the MQTT broker.

In this fan-out use case, connections for 5 publishers and 1,000 subscribers are established (i.e., more subscribers than publishers for “fan-out" purposes), and 5 topics are used for Publish/Subscribe. Once a subscriber is connected, it immediately subscribes to all 5 topics. Later on, each publisher sends a 16-byte message to an exclusive topic. Both publishers and subscribers use QoS 1. The publish rate for each publisher is 50 messages per second, and consequently, the total expected subscription rate is 250K messages per second. 

To perform benchmarking, NanoMQ is deployed on a single node. The configuration details are:

| **Deployment** | **Version**   | **OS**               | **CPU** | **Memory** | **Cloud host model** |
| :------------- | :------------ | :------------------- | :------ | :--------- | :------------------- |
| single-node    | NanoMQ 0.17.0 | Ubuntu 22.04.1 amd64 | 16vCPUs | 32 GiB     | c5.4xlarge (AWS)     |

[XMeter](https://www.emqx.com/en/products/xmeter) is used as the tool to perform benchmarking. It simulates all clients and messages throughput, analyzing data and rendering metrics reports. The highlighted metrics are:

|        | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :----- | :-------------- | :------------------------------ | :------------------ | :------------------ | :-------------- | :-------------- |
| NanoMQ | 250k            | 14.07                           | 72%                 | 70%                 | 824M            | 685M            |

The detailed charts are also appended:

![MQTT Benchmark Result](https://assets.emqx.com/images/273d64560e44b09646ab78d349cdc8c3.png)

## Future Works

We use NanoMQ as an example, but the benchmark suite targets all brokers implementing the MQTT protocol and will continuously iterate and evolve. We are also going to propose a tool for the MQTT benchmarking.

If you are interested in this MQTT benchmark suite, we highly recommend you check out the [GitHub](https://github.com/emqx/mqttbs) and get more information. And any contributions to make the benchmark suite better are welcome!


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
