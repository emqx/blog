> IoT scenarios often face challenges like a large number of devices, high data generation rates, and the huge accumulated data volumes. Therefore, how to access, store, and process these massive amounts of data has become a critical issue.
>
> [EMQX](https://www.emqx.com/en/products/emqx), as a highly scalable, powerful and feature-rich MQTT broker for the IoT, can handle billions of concurrent connections and millions of messages per second in a single cluster. Furthermore, its built-in [Data Integration](https://www.emqx.com/en/solutions/mqtt-data-integration) functionality provides an out-of-the-box solution, which enables seamless integrating IoT data with more than 40 cloud services and enterprise systems, including Kafka, SQL, NoSQL, and time-series databases.
>
> This blog series presents the benchmark test results of the integrations against a single node EMQX server.

In this post, we provide the benchmarking result of MySQL integration - a single node EMQX processes and inserts 100,000 QoS1 messages per second to MySQL.

## Test Scenario

This benchmark testing simulates 100,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. After all connections are established, each client publishes one QoS 1 message with a payload of 200 bytes per second, and all messages, via the rule engine, are written into MySQL.

- Concurrent connections: 100,000

- Topics: 100,000

- CPS (newly established connections per sec.): 5000

- QoS: 1

- Keep alive: 300s

- Payload: 200 bytes

- Message publish TPS: 100,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service | Deployment  | Version | OS         | CPU  | Memory | Cloud Host model |
| ------- | ----------- | ------- | ---------- | ---- | ------ | ---------------- |
| EMQX    | single node | 5.1.0   | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |
| MySQL   | standalone  | 8.0.27  | Centos 7.8 | 32C  | 64G    | c6.8xlarge       |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX and MySQL machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX and MySQL in this testing.

![Test Tool](https://assets.emqx.com/images/81af50913b43b568ca45ec3693e02689.png)

## Preparation

For the detailed steps of configuring EMQX-MySQL integration, please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v5.0/data-integration/data-bridge-mysql.html). The three figures below are MySQL Bridge settings used in this benchmark testing.

### MySQL Bridge & Rule Config

![MySQL Bridge](https://assets.emqx.com/images/c61c7c57816a77567f5dda7998b14176.png)

![Rule Config 1](https://assets.emqx.com/images/ad8ed7f4566720b71674a6eec4f3c14f.png)

![Rule Config 2](https://assets.emqx.com/images/43154744fc2d52a82fd8a47f34cea56d.png)

After the bridge and rule were created, the data flow below can be seen from the Dashboard.

![data flow](https://assets.emqx.com/images/1f2102820338d3ef90193d8fa18f24a6.png)

### System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/enterprise/v4.4/tutorial/tune.html) for the Linux Kernel tuning.

### MySQL Tuning

For this test, MySQL config file my.conf was modified as follows:

```
[mysqld]
# The default is 128M, modified to 70% of 64G
# Start at 70% of total RAM for dedicated server
innodb_buffer_pool_size = 48000M

innodb_buffer_pool_instances = 12

max_heap_table_size = 8192M
tmp_table_size = 8192M
```

## Benchmark Results

### Observations

- the usage of CPU and memory keeps stable

- the average of CPU user: 67%

- Memory used: Max 18GB

- the average of response time of publish: 0.72ms

- After the test was completed, by comparing the data statistics from the EMQX Dashboard Data Bridge Statistics with the number of queries in the corresponding table of the database from cli, it was observed that all messages were written to MySQL in real-time and successfully.

### Result Charts

**Screenshots of EMQX Dashboard & Rule Engine during the test**

![Cluster Overview](https://assets.emqx.com/images/51ad5512665ee57db7dc7f2baab81d00.png)

![Data Bridge](https://assets.emqx.com/images/5a607a6fc776643ac478cb1f2f908b6d.png)

The above two screenshots show that both the incoming message rate & processing rate by Data Bridge are 100,000+ per second, and all messages hit by the rule are written to the database in real time.

**Screenshots after the test completed**

![Screenshot 1](https://assets.emqx.com/images/f23d140c899b68ebec004f05fd114cf7.png)

![Screenshot 2](https://assets.emqx.com/images/a02875a2dfef88c12ddd925122bfbb17.png)

The above screenshots show that all messages EMQX received were forwarded to MySQL table successfully.

**XMeter report chart**

![XMeter report chart](https://assets.emqx.com/images/0aa61b01627a8c89eb92d23ee2465b2c.png)

## Wrapping up

This benchmark report has proved the capability of EMQX single-node deployment. With the ability to handle 100,000 QoS 1 messages per second and store the messages in MySQL by one node, the EMQX cluster is a reliable and efficient choice for managing large amounts of IoT data.





<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
