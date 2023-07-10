>IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
>[EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
>This blog series presents the benchmark test results of the integrations against a single node EMQX server.

In this first post, we provide the benchmarking result of Kafka integration - a single node EMQX processes and bridges 100,000 QoS1 messages per second to Kafka.

![MQTT to Kafka](https://assets.emqx.com/images/98455b5297e5ee05947fb5f57c888556.png)

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message with the payload of 1K bytes per second, and all messages, via the rule engine, are forwarded to Kafka.

- Concurrent connections: 100,000
- Topics: 100,000
- CPS (new established connections per sec.): 5000
- QoS: 1
- Keep alive: 300s
- Payload: 1024 bytes
- Message publish TPS: 100,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service | Deployment  | Version    | OS         | CPU  | Memory | Cloud Host model |
| :------ | :---------- | :--------- | :--------- | :--- | :----- | :--------------- |
| EMQX    | single node | 5.1.0      | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |
| Kafka   | standalone  | 2.13-2.6.0 | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools). XMeter is built on top of [JMeter](https://www.emqx.com/en/blog/introduction-to-the-open-source-testing-tool-jmeter) but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and Kafka machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and Kafka in this testing.

![Testing Architecture](https://assets.emqx.com/images/1f2df4ad6d55e0ebd031e4d09d52efc2.png)

## Preparation

For the detailed steps of configuring EMQX-Kafka integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-kafka.html). The three figures below are Kafka Bridge settings used in this benchmark testing.

### Kafka Bridge & Rule Config

![Data Bridge 1](https://assets.emqx.com/images/37034d6ef6f1020060d5130dc0d77d8d.png)

![Data Bridge 2](https://assets.emqx.com/images/d15a5a84fe980cddf4aeffc29a61a46d.png)

![Rules](https://assets.emqx.com/images/6dbe998f05f130388d6068d2dca85d60.png)

After the bridge and rule were created, the data flow below can be seen from the Dashboard.

![Data flow](https://assets.emqx.com/images/66d166fe84b325a4619cc3ddbb8b0f37.png)

### Kafka Topic

The Kafka topic used in this test is 16 partitions and 1 replica since we use standalone.

![Kafka topic](https://assets.emqx.com/images/5a63b7ce888c49a9ebbe68656b84adda.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Observations

- The usage of CPU and memory keeps stable
- The average of CPU user: 76%
- Memory used: ~11GB
- The average of response time of publish: 3.8ms
- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with the total offset number of the Kafka topic from Kafka cli, it was observed that all messages were written to Kafka in real-time.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![Screenshots of EMQX Dashboard](https://assets.emqx.com/images/3710c927d634436336e4b68df31f31f8.png)

![Screenshots of Rule Engine](https://assets.emqx.com/images/526ee6367dc1ee12fb670d67d9646938.png)

> The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 100,000+ per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Screenshots after the test completed 1](https://assets.emqx.com/images/f0350a108ca10590bb2e499dfb147357.png)
![Screenshots after the test completed 2](https://assets.emqx.com/images/21eb9fcdd66ddaca48e7d2c5a60e1e53.png)

> The above screenshots show that all messages EMQX received were forwarded to Kafka successfully.

**XMeter chart**

![XMeter chart](https://assets.emqx.com/images/af49e310e25a642f622095025861cdbf.png)

## Wrapping up

From the EMQX rule engine interface, it is easy to integrate EMQX with Kafka. You only need to:

- Set up the MQTT-to-Kafka topic mapping and the MQTT topic/message filtering; 
- Select synchronous or asynchronous write mode based on actual use cases;
- Determine the caching mode to prevent data loss from network disturbances or service outages.

By leveraging the advantages of Kafka in data storage and stream processing, this out-of-the-box solution provides a robust and scalable infrastructure for IoT scenarios. It enables bi-directional communication between devices and enterprise applications, as well as real-time processing of large-scale data. Organizations can make timely and informed decisions, and maximize the value of their data and drive innovation in the business.

This benchmark report has proved the capability of EMQX single-node deployment. Next, we'll conduct a test against an EMQX cluster to demonstrate its ability to support 1 million QoS 1 messages per second to Kafka. Stay tuned for the report.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
