>IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
>[EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
>This blog series presents the benchmark test results of the integrations against a single node EMQX server.

In this post, we provide the benchmarking result of InfluxDB integration - a single node EMQX processes and inserts 100,000 QoS1 messages per second to InfluxDB.

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message with the payload of 200 bytes per second, and all messages, via the rule engine, are written into InfluxDB. EMQX supports both V1 and V2 of Influx version. We used V2 for this test.

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

| Service  | Deployment  | Version | OS         | CPU  | Memory | Cloud Host model |
| :------- | :---------- | :------ | :--------- | :--- | :----- | :--------------- |
| EMQX     | single node | 5.1.0   | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |
| InfluxDB | standalone  | 2.6.1   | Centos 7.8 | 16C  | 32G    | c6.4xlarge       |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and InfluxDB machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and InfluxDB in this testing.

![XMeter](https://assets.emqx.com/images/42a27aac21592e97ef5e77654436c163.png)

## Preparation

For the detailed steps of configuring EMQX-InfluxDB integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-influxdb.html). The three figures below are InfluxDB Bridge settings used in this benchmark testing.

### InfluxDB Bridge & Rule Config

![Data bridge 1](https://assets.emqx.com/images/9b533129732a83cd8ae5e23480f87ccf.png)
![Data bridge 2](https://assets.emqx.com/images/778698d2de36d25bdc685a89d5cdbfb6.png)
![Rules 1](https://assets.emqx.com/images/b2452203dadfad1abe13dce7ca3a12a1.png)

After the bridge and rule were created, the data flow in below can be seen from the Dashboard.

![Rules 2](https://assets.emqx.com/images/bc20bd66e017e464516440f87c61bcca.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Observations

- the usage of CPU and memory keeps stable
- the average of CPU user: 77%
- Memory used: Max 14GB 
- the average of response time of publish: 0.85ms
- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with  the number of queries in the corresponding measurement from Influx UI, it was observed that all messages were written to InfluxDB in real-time and successfully.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![EMQX Dashboard](https://assets.emqx.com/images/fe84fb71d3d32c5f48fe756c4ed0637d.png)
![Rule Engine](https://assets.emqx.com/images/a07e30eab8404292469b87293f9d5a10.png)

The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 100,000+ per second, and all messages hit by the rule are written to the database in real time.

#### Screenshots after the test completed

![Data bridge 3](https://assets.emqx.com/images/b93665f74bca2c7766779f8eabe7cda0.png)
![Data explprer](https://assets.emqx.com/images/cc5c5e3f65807c57bced26a82646e220.png)

The above screenshots show that all messages EMQX received were forwarded to Influx Measurement M1 successfully.

**XMeter Report Chart**

![XMeter Report Chart](https://assets.emqx.com/images/9fd8ae69a78d05043c34bf0d95303f04.png)

## Wrapping up

InfluxDB is a database for storing and analyzing time series data. This benchmark report has shown the great performance of EMQX-InfluxDB integration on single-node deployment. 

Combining EMQX's outstanding scalability and performance with InfluxDB's powerful data throughput capability and stable performance, the out-of-the-box integration solution is highly suitable for the field of IoT.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
