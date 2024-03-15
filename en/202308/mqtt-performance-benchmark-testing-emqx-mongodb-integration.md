>IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
>[EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
>This blog series presents the benchmark test results of the integrations against a single node EMQX server.

In this post, we provide the benchmarking result of [MongoDB integration](https://www.emqx.com/en/blog/mqtt-and-mongodb-crafting-seamless-synergy-for-iot-data-mangement) - a single node EMQX processes and inserts 80,000 QoS1 messages per second to MongoDB.

## Test Scenario

This benchmark testing simulates 80,000 MQTT clients connecting to EMQX, with a connection rate of 4,000 per second. After all connections are established, each client publishes one QoS 1 message with the payload of 100 bytes per second, and all messages, via the rule engine, are written into MongoDB. 

- Concurrent connections: 80,000
- Topics: 80,000
- CPS (new established connections per sec.): 4000
- QoS: 1
- Keep alive: 300s
- Payload: 100 bytes
- Message publish TPS: 80,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service | Deployment  | Version | OS         | CPU  | Memory | Cloud Host model |
| :------ | :---------- | :------ | :--------- | :--- | :----- | :--------------- |
| EMQX    | single node | 5.1.0   | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |
| MongoDB | single      | 5.0.18  | Centos 7.8 | 16C  | 32G    | c6.4xlarge       |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and MongoDB machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and MongoDB in this testing.

![XMeter](https://assets.emqx.com/images/b805a9ab1fa3d6f1bbfc3bb3e181dda3.png)

## Preparation

For the detailed steps of configuring EMQX-MongoDB integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-mongodb.html). The three figures below are MongoDB Bridge settings used in this benchmark testing.

### MongoDB Bridge & Rule Config

![Data Bridge](https://assets.emqx.com/images/d5559be561c5c335fb037ad0441f5711.png)

![Payload template](https://assets.emqx.com/images/3a230a750fc0c3e4803e1e7f7c07b3f6.png)
![Data Bridge 2](https://assets.emqx.com/images/4754bf4dbaffd08381b43ddf0f9e3bcb.png)
![Rules](https://assets.emqx.com/images/c34a7329c8d03a5bd5f64bc71cb3ce8e.png)

After the bridge and rule were created, the data flow in below can be seen from the Dashboard.

![data flow](https://assets.emqx.com/images/57a8138401d6c0a946a3ffb346be30bb.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Observations

- The usage of CPU and memory keeps stable
- The average of CPU user: 76%
- Memory used: Max 14GB, stabilized at around 11G.
- The average of response time of publish: 2.95ms
- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with the number of queries in the corresponding table of the database, it was observed that all messages were written to MongoDB in real-time and successfully.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![EMQX Dashboard](https://assets.emqx.com/images/32d68171e4b1c4c4f62a825607008a27.png)
![Rule Engine](https://assets.emqx.com/images/0df8e30845fccc14575ab26951887cae.png)

The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 80,000+ per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Screenshots 1](https://assets.emqx.com/images/5cd739e318ae527b496e48e28b7f097d.png)
![Screenshots 2](https://assets.emqx.com/images/ffaaa6f1f3a43e08b17495cf59dd8ad1.png)

The above screenshots show that all messages EMQX received were forwarded to MongoDB successfully.

**XMeter report chart**

![XMeter report chart](https://assets.emqx.com/images/c41aa51b1abda57dd22884b4da6bb388.png)

## Wrapping up

MongoDB excels in offering flexibility, scalability, performance, and a robust feature set, making it a popular choice for various applications and use cases. 

This benchmark report demonstrates the powerful performance of integrating EMQX and MongoDB in a single-node deployment. We believe the out-of-the-box solution will bring significant value to IoT customers, delivering exceptional results.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
