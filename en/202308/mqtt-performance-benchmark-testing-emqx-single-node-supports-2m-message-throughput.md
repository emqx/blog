## Background

In this post, we provide the benchmarking result of EMQX message throughput - a single node EMQX processes 2M message throughput per second.

## Test Scenario

This benchmark testing simulates 20 publishers and 1000 subscribers connecting to EMQX. After all connections are established, each publisher publishes 100 QoS 0 messages with the payload of 16 bytes per second. Subscribers subscribe to messages from all publishers via topic wildcards.

- Concurrent connections: 20 publishers, 1000 subscribers

- Publish Topics: each publisher has a unique topic with `test/` as the prefix

- Subscribe Topics: all subscribers subscribe to a wildcard topic of the form `test/#`

- QoS: 0

- Payload: 16 bytes

- Message Throughput: 2,000,000/second

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Machine Details

| Service | Deployment  | Version | OS       | CPU  | Memory | Cloud Host model |
| ------- | ----------- | ------- | -------- | ---- | ------ | ---------------- |
| EMQX    | single node | 5.0.21  | RHEL 8.5 | 64C  | 128G   | hfc6.16xlarge    |

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX in this testing.

![Test Architecture Diagram](https://assets.emqx.com/images/76af39a96c5f485a576a6ee2acb6e86d.png)

## System Tuning

Please refer to [EMQX Doc](https://docs.emqx.com/en/emqx/v5.0/performance/tune.html) for the Linux Kernel tuning.

## Benchmark Results

EMQX dashboard illustrates that over 2M outgoing messages per second are achieved, and the rate is rather stable throughout the 30-minute’s test.

![Benchmark Results](https://assets.emqx.com/images/5aa62d0d22035ed2ade692205b8d1154.png)

![图片.png](https://assets.emqx.com/images/aa1d7320da5b6b274651304d23bab88e.png)

### Metrics

| average of pub-to-sub latency              | 2.93ms                                     |
| ------------------------------------------ | ------------------------------------------ |
| CPU usage during the phase of messaging    | the max is 92%, and the average is 88%     |
| Memory usage during the phase of messaging | the max is 1.2GB, and the average is 1.1GB |

## Wrapping up

This benchmark report demonstrates the powerful performance of EMQX message throughput in a single node deployment. EMQX can be used in complex business scenarios while maintaining low message latency even under massive message transmission.





<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
