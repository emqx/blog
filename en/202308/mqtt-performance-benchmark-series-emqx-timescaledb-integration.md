> In IoT scenarios, there are often challenges such as a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
> 
> EMQX, as a highly scalable, powerful and feature-rich MQTT broker for the Internet of Things, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
> 
> This blog series presents the benchmark test results of the integrations against a single node EMQX server.
> 
> In this post, we provide the benchmarking result of TimescaleDB integration - a single node EMQX processes and inserts 100,000 QoS1 messages per second to TimescaleDB.

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message with the payload of 200 bytes per second, and all messages, via the rule engine, are written into TimeScaleDB.

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

| Service | Deployment | Version | OS  | CPU | Memory | Cloud Host model |
| --- | --- | --- | --- | --- | --- | --- |
| EMQX | single node | 5.1.0 | Centos 7.8 | 32C | 64G | c6.8xlarge |
| PostgreSQL/TimescaleDB | standalone | 13.5 | Centos 7.8 | 16C | 64G | c6.4xlarge |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and TimescaleDB machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and TimescaleDB in this testing.

## Preparation

For the detailed steps of configuring EMQX-TimescaleDB integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-pgsql.html). The 3 figures below are TimescaleDB Bridge settings used in this benchmark testing.

### TimescaleDB Bridge & Rule Config

![TimescaleDB Bridge 1](https://assets.emqx.com/images/b93ee201a6ec334adab2b91b27fbf2db.png)

![TimescaleDB Bridge 2](https://assets.emqx.com/images/f94005a571fc3c226f3729764d6b03ba.png)

![Rule Config](https://assets.emqx.com/images/d9bbcc86a38ed5210ca4a5262f812f5f.png)

After the bridge and rule were created, the data flow in below can be seen from the Dashboard.

![data flow](https://assets.emqx.com/images/1f0e3e51b581c7b5ed22c3dbeac8e600.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Observations

- the usage of CPU and memory keeps stable
  
- the average of CPU user: 77%
  
- Memory used: Max 13GB
  
- the average of response time of publish: 2.39ms
  
- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with the number of queries in the corresponding table of the database, it was observed that all messages were written to TimescaleDB in real-time and successfully.
  

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![EMQX Dashboard](https://assets.emqx.com/images/f1cdf8038de2f9e974bd132d4edf8153.png)

![Rule Engine](https://assets.emqx.com/images/c2f61266a4c8171166aaa810f2c4e823.png)

> The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 100,000+ per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Screenshots 1](https://assets.emqx.com/images/5789ed6721ba567796501bd39b27ff87.png)

![Screenshots 2](https://assets.emqx.com/images/d896c7b04f38863995687b96c2b58783.png)

> The above screenshots show that all messages EMQX received were forwarded to TimeScaleDB successfully.

**XMeter report chart**

![XMeter report chart](https://assets.emqx.com/images/acb5ca296cd4c995916b9c791a440e59.png)

## Wrapping up

TimescaleDB has been recognized for its easy use, fast query speed, and cost-efficiency in time-series database area. The integration between EMQX and TimescaleDB brings together the strengths of both, providing a comprehensive solution for for IoT applications.

In addition, both EMQX and Timescale provide cloud service. Harnessing the capabilities of Cloud in one-stop operations and maintenance, horizontal scalability, and more, you can effortlessly deploy and integrate EMQX Cloud and Timescale Cloud services, and connect to your existing cloud-native infrastructure. Please refer to our [blog](https://www.emqx.com/en/blog/seamlessly-integrating-emqx-cloud-with-the-new-timescale-service) for more information.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
