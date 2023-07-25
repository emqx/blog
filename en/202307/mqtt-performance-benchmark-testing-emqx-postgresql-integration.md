>IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
>[EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
>This blog series presents the benchmark test results of the integrations against a single node EMQX server.

In this post, we provide the benchmarking result of PostgreSQL integration - a single node EMQX processes and inserts 100,000 QoS1 messages per second to PostgreSQL.

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message with the payload of 200 bytes per second, and all messages, via the rule engine, are written into PostgreSQL. 

- Concurrent connections: 100,000
- Topics: 100,000
- CPS (new established connections per sec.): 5000
- QoS: 1
- Keep alive: 300s
- Payload: 200 bytes
- Message publish TPS: 100,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service    | Deployment  | Version | OS         | CPU  | Memory | Cloud Host model |
| :--------- | :---------- | :------ | :--------- | :--- | :----- | :--------------- |
| EMQX       | single node | 5.1.0   | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |
| PostgreSQL | standalone  | 13.5    | Centos 7.8 | 16C  | 64G    | c6.4xlarge       |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and PostgreSQL machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and PostgreSQL in this testing.

![MQTT to PostgreSQL](https://assets.emqx.com/images/60ba9b8364809e2bfe270bedb0bcabb6.png)

## Preparation

For the detailed steps of configuring EMQX-PostgreSQL integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-pgsql.html). The 3 figures below are PostgreSQL Bridge settings used in this benchmark testing.

### PostgreSQL Bridge & Rule Config

![PostgreSQL Bridge 1](https://assets.emqx.com/images/ab5b1652a4c93ee5698e08088ee20a7d.png)

![PostgreSQL Bridge 2](https://assets.emqx.com/images/78b403b1684e5d762aca51c87aedc2fb.png)

![Rules 1](https://assets.emqx.com/images/f394c6dd32c5098b71d7030631098e29.png)

![Rules 1](https://assets.emqx.com/images/5a1a3da1bf0f56cd588ba620c96236e3.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Observations

- the usage of CPU and memory keeps stable
- the average of CPU user: 76%
- Memory used: Max 14GB, stabilized at around 11G.
- the average of response time of publish: 2.95ms
- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with  the number of queries in the corresponding table of the database, it was observed that all messages were written to PostgreSQL in real-time and successfully.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![Screenshots of EMQX Dashboard](https://assets.emqx.com/images/d3e9295b54aa8ad6a089e33fbc665164.png)
![Rule Engine](https://assets.emqx.com/images/26a68cf148b59e2641ea8324a61b96f6.png)

> The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 100,000+ per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Screenshots after the test completed 1](https://assets.emqx.com/images/e5b041163bb495b7e6665fee543a7f62.png)
![Screenshots after the test completed 2](https://assets.emqx.com/images/d67eb38e0d988a21d2452cf298f350a4.png)

> The above screenshots show that all messages EMQX received were forwarded to PostgreSQL successfully.

**XMeter report chart**

![XMeter report chart](https://assets.emqx.com/images/9e6559bfaa5b36eae00d146af8e02f9d.png)

## Wrapping up

PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. This benchmark report has showed the great performance of EMQX-PostgreSQL integration on single node deployment. 

By easily configuring EMQX and PostgreSQL through a user-friendly interface, a robust and out-of-the-box IoT solution is ready for you.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
