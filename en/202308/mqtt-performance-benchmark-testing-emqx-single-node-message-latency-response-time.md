## Background

In this blog, we provide the benchmarking result of EMQX message latency and response time.

## Test Scenario

This benchmark testing simulates 1000 publishers and 1000 subscribers connecting to EMQX. After all connections are established, each publisher publishes 1 message with the payload of 50 bytes per second, execute 30 mins to get the average value.

- Concurrent connections: 1000 publishers, 1000 subscribers

- QoS: Tests messages at the QoS 0, QoS 1, and QoS 2 levels

- Payload: 50 bytes

- Message Throughput: 1000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service | Deployment  | Version | OS       | CPU  | Memory | Cloud Host model |
| ------- | ----------- | ------- | -------- | ---- | ------ | ---------------- |
| EMQX    | single node | 5.0.6   | RHEL 8.5 | 2C   | 4G     | c6.large         |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX in this testing.

![Test Architecture Diagram](https://assets.emqx.com/images/76af39a96c5f485a576a6ee2acb6e86d.png)

## System Tuning

Please refer to [EMQX Doc](https://www.emqx.io/docs/en/v5.0/performance/tune.html) for the Linux Kernel tuning.

## Benchmark Results

### Define

- Latency: the time taken by a broker to transmit a message from a publisher to a subscriber.

- Response time: the time difference between msg received and msg sent.

### Metrics

|                    | **QoS 0** | **QoS 1** | **QoS 2** |
| ------------------ | --------- | --------- | --------- |
| Latency (ms)       | 0.048     | 0.065     | 0.07      |
| response time (ms) | 1.7       | 1.7       | 1.7       |

### XMeter Report Chart

#### QoS 0

![XMeter Report Chart QoS 0](https://assets.emqx.com/images/bca9b0aac84df53ace517f33e62da1c8.png)

#### QoS 1

![XMeter Report Chart QoS 1](https://assets.emqx.com/images/23eb172c8443ec0652ed9830f4db24e4.png)

#### QoS 2

![XMeter Report Chart QoS 2](https://assets.emqx.com/images/000570cf3d4a2c19a44feadc47531df5.png)

## Wrapping up

This is a low load test and the results show that EMQX has very low message latency. In fact, EMQX is able to maintain its low latency even with a large number of messages. These results indicate that EMQX can be a valuable tool in IoT applications that require a high level of real-time responsiveness.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
