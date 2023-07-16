>IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
>[EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
>This blog series presents the benchmark test results of the integrations against a single node EMQX server.

[HstreamDB](https://hstream.io/) is a streaming database purpose-built to ingest, store, process, and analyze massive data streams. It is a modern data infrastructure that unifies messaging, stream processing, and storage to help get value out of your data in real-time.

This blog will provide the benchmarking results of HStreamDB integration - a single node EMQX processes and inserts 100,000 QoS1 messages per second to HStreamDB.

![MQTT to HStreamDB](https://assets.emqx.com/images/f3f3a2fe922540b75defeabb016a2b12.png)

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message per second, and all messages are transmitted and stored in HStreamDB via the rule engine.

- Concurrent connections: 100,000
- Topics: 100,000
- CPS (new established connections per sec.): 5000
- QoS: 1
- Keep alive: 300s
- Payload: json, 200 bytes
- Message publish TPS: 100,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service   | Deployment                   | Version | OS       | CPU  | Memory | Cloud Host model        |
| :-------- | :--------------------------- | :------ | :------- | :--- | :----- | :---------------------- |
| EMQX      | single node                  | 4.4.15  | RHEL 8.5 | 32C  | 64G    | c7.8xlarge AlibabaCloud |
| HStreamDB | hserver, hstore in 1 machine | 0.14.0  | RHEL 8.5 | 32C  | 64G    | c7.8xlarge AlibabaCloud |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools). XMeter is built on top of [JMeter](https://www.emqx.com/en/blog/introduction-to-the-open-source-testing-tool-jmeter) but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and HStreamDB machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and HStream in this testing.

![Figure 1 Test Topology](https://assets.emqx.com/images/f53a9a0c9c3644ef86920c87f9733b74.png)

<center>Figure 1 Test Topology</center>

## Preparation

### Integration Setup

For detailed steps on how to configure EMQX-HStreamDB integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/rule/backend_hstreamdb.html). Figure 2, 3 and 4 are the rule engine settings used in this benchmark testing.

![*Figure 2 HStreamDB resource*](https://assets.emqx.com/images/9de4f747e6f0ecf6f2783f9bc3a85255.png)

<center>Figure 2 HStreamDB resource</center>

<br>

![*Figrue 3 Rule SQL*](https://assets.emqx.com/images/5a66223e832a5e204ba95e39e362877b.png)

<center>Figrue 3 Rule SQL</center>

<br>

![*Firgure 4 Rule Action*](https://assets.emqx.com/images/6d187cf2188b020be010667f1960dc37.png)

<center>Firgure 4 Rule Action</center>

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel and EMQX tuning.

## Benchmark Results

### Observation Highlights

- CPU and memory stable
- the average of CPU user: 76%
- Memory used: 12GB ~ 16GB
- the average of reponse time of publish: 2.2ms
- After the test was completed, by comparing the data statistics from the EMQX rule engine with the total number of appending in HStreamDB, it was observed that all messages were written to the database in real-time.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![EMQX Dashboard](https://assets.emqx.com/images/e9547d1c1e759367007142527606af5a.png)

![Metrics](https://assets.emqx.com/images/dd9d301e2d7622d76845f5ebddd31352.png)

> The above two figures show that the incoming message rate is around 100,000 per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Metrics](https://assets.emqx.com/images/2d40878a67f8658e4aea616be393225a.png)

![Docker run](https://assets.emqx.com/images/ddff988bc33792cbb61a652cc28ec8e4.png)

> From the above screenshots, it can be seen that the total number of queries in the database after the test is consistent with the message count, rule hit count, and success count as shown on the EMQX dashboard.

**XMeter chart**

![XMeter chart](https://assets.emqx.com/images/be655cf244408215c070387861fabe75.png)

## Wrapping up

The benchmarking test shows that a single node EMQX is able to support 100,000 connections and write 100,000 QoS 1 messages with a payload of 200B to HStreamDB per second, and all messages are written to the database in real time. Within the 30-minute test, the CPU and Memory usage has kept stable. 

Considering both EMQX and HStreamDB are highly scalable, EMQX-HStream integration can be easily scaled to support higher message throughput and larger data streams, for example, one million messages per second, in a cluster. By leveraging the capabilities of HStreamDB in massive data stream ingestion, storage, processing, and analysis, this out-of-the-box solution provides a robust and scalable infrastructure for IoT usage.





<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
