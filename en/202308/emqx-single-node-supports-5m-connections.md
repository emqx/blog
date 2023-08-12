In this post, we provide the benchmarking result of EMQX connection - a single node EMQX processes 5M concurrent connections.

## Test Scenario

This benchmark testing simulates 5,000,000 MQTT clients connecting to EMQX, with a connection rate of 5,000 per second. 

- Concurrent connections: 5,000,000
- Connection rate: 5000/s
- Authentication: no
- Keep alive: 300s
- Clean session: true

## Testbed

The test environment is configured on Alibaba Cloud, and all virtual machines are within a VPC (virtual private cloud) subnet.

Machine Details:

| Service                      | Deployment  | Version | OS       | CPU  | Memory | Cloud Host model |
| :--------------------------- | :---------- | :------ | :------- | :--- | :----- | :--------------- |
| [EMQX](https://www.emqx.io/) | single node | 5.0.21  | RHEL 8.5 | 64C  | 128G   | hfc6.16xlarge    |

## Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate MQTT clients. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX machines.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the EMQX in this testing.

![MQTT Benchmark Architecture](https://assets.emqx.com/images/01563837a66a84243aea056c6958bb4c.png)

## System Tuning

Please refer to [EMQX Doc](https://www.emqx.io/docs/en/v5.0/performance/tune.html) for the Linux Kernel tuning.

## Benchmark Results

EMQX dashboard illustrates that over 5M concurrent connections are achieved, and the connection is rather stable throughout the 30-minute’s test.

![Benchmark Results](https://assets.emqx.com/images/ab44a93747aad0727714ce6a58897576.png)

![MQTT Connections](https://assets.emqx.com/images/91334a263f3c81d4daa785da742d5878.png)

### Metrics

| Average of connect response time                        | 2.93ms |
| ------------------------------------------------------- | ------ |
| Average of CPU usage                                    | 14%    |
| Max of CPU usage                                        | 40%    |
| Average of memory usage after all clients are connected | 48.7GB |
| Max of memory usage                                     | 51.4GB |

## Wrapping up

This benchmark report demonstrates the robust concurrent connectivity performance of EMQX in a single-node deployment. It shows that EMQX can help users build larger scale IoT applications while using fewer machines, helping to reduce your total cost of ownership.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
