> The blog post [Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing) introduced the Open MQTT Benchmark Suite developed by EMQ. We defined MQTT benchmark scenarios, use cases, and observation metrics in [the GitHub project](https://github.com/emqx/mqttbs). Based on the activity and popularity of the community and GitHub project, the top 4 open-source [MQTT brokers in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) – EMQX,  Mosquitto, NanoMQ, and Vernemq, were chosen to perform the benchmark test. 
>
> This blog series presents the benchmark test results and aims to help you choose a suitable MQTT broker based on your needs and use cases.

This blog post will provide the benchmarking results of [EMQX](https://www.emqx.io/) and [Mosquitto](https://github.com/eclipse/mosquitto). Additionally, we compare the features and capabilities of both brokers in detail in another [post.](https://www.emqx.com/en/blog/emqx-vs-mosquitto-2023-mqtt-broker-comparison) 

## MQTT Benchmark Scenarios and Use Cases

[The MQTT Benchmark Suite](https://github.com/emqx/mqttbs) designs two sets of benchmark use cases. One is named Basic Set, which is for small-scale performance verification, and another is called Enterprise Set, which aims for enterprise level verification.

Detailed descriptions of the testing scenarios are already available on the [GitHub project](https://github.com/emqx/mqttbs), for convenience we briefly list them here as well.

All the tests are executed on a single node.

### Use Cases

#### Basic Set

- **Point-to-Point**: p2p-1K-1K-1K-1K
  - 1k publishers, 1k subscribers, 1k topics
  - Each publisher pubs 1 message per second
  - QoS 1, payload 16B
- **Fan-out**: fanout-1-1k-1-1K
  - 1 publisher, 1 topic, 1000 subscribers
  - 1 publisher pubs 1 message per second
  - QoS 1, payload 16B
- **Fan-in:** sharedsub-1K-5-1K-1K
  - 1k publishers, 1k pub topics
  - 5 subscribers consume all messages in a shared subscription way
  - Publish rate: 1k/s (each publisher pubs a message per second)
  - Shared subscription’s topic: $share/perf/test/#
  - Publish topics: test/$clientid
  - QoS 1, payload 16B
- **Concurrent connections**: conn-tcp-10k-100
  - 10k connections
  - Connection rate (cps): 100/s

#### Enterprise Set

- **Point-to-Point**: p2p-50K-50K-50K-50K
  - 50k publishers, 50k subscribers, 50k topics
  - Each publisher pubs 1 message per second
  - QoS 1, payload 16B
- **Fan-out**: fanout-5-1000-5-250K
  - 5 publishers, 5 topics, 1000 subscribers (each sub to all topics)
  - Publish rate: 250/s, so sub rate = 250*1000 = 250k/s
  - QoS 1, payload 16B
- **Fan-in:** sharedsub-50K-500-50K-50K
  - 50k publishers, 50k pub topics
  - Publish rate: 50k/s (each publisher pubs a message per second)
  - Use a shared subscription to consume data (to avoid slow consumption by subscribers affecting broker performance, 500 subscribers are used to share the subscription)
  - Shared subscription’s topic: $share/perf/test/#
  - Publish topics: test/$clientid
  - QoS 1, payload 16B
- **Concurrent connections**: conn-tcp-1M-5K
  - 1M connections
  - Connection rate (cps): 5000/s

### Common MQTT Config

| **Config**                    | **Value**  |
| :---------------------------- | :--------- |
| keep alive                    | 300s       |
| clean session                 | true       |
| authentication enablement     | no         |
| TLS authentication enablement | no         |
| test duration                 | 30 minutes |

## Testbed

The test environment is configured on AWS, and all virtual machines are within a VPC (virtual private cloud) subnet.

### Broker Machine Details

- Public cloud: AWS
- Instance type: c5.4xlarge 16C32G
- OS: Ubuntu 22.04.1 amd64

### Test Tool

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate various business scenarios. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the EMQX/Mosquitto server, enabling a comparison with the information provided by the operating systems.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the MQTT broker server in this testing.

### SW Version

| **Broker**                            | **Version** |
| :------------------------------------ | :---------- |
| EMQX                                  | 4.4.16      |
| Mosquitto (with persistence disabled) | 2.0.15      |
| XMeter                                | 3.2.4       |

## Benchmarking Results

### Basic Set

#### **point-to-point**: 1K:1K

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | 0.27                            | 4%                  | 2%                  | 510M            | 495M            |
| **Mosquitto** | 0.25                            | 0%                  | 0%                  | 278M            | 254M            |

#### Fan-out 1k QoS 1

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | 3                               | 2%                  | 1%                  | 475M            | 460M            |
| **Mosquitto** | 5.73                            | 0%                  | 0%                  | 270M            | 260M            |

#### Fan-in 1k - shared subscription QoS 1

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | 0.19                            | 3%                  | 2%                  | 468M            | 460M            |
| **Mosquitto** | 0.20                            | 0%                  | 0%                  | 281M            | 246M            |

#### 10K connections cps 100

|               | Average latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :------------ | -------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **EMQX**      | 0.74                 | 2%                  | 1%                  | 540M            | 510M                  |
| **Mosquitto** | 0.6                  | 0%                  | 0%                  | 306M            | 264M                  |

### Enterprise Set

#### **point-to-point**: p2p-50K-50K-50K-50K

**Metrics**

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | 50k:50k         | 1.58                            | 88%                 | 80%                 | 5.71G           | 5.02G           |
| **Mosquitto** | 37k:37k         | 353.82                          | 6%                  | 6%                  | 341M            | 318M            |

> In this scenario, Mosquitto cannot reach to the target message rate. It stabilized at 37300/s for both pub and sub. 
>
> EMQX keeps the stable pub & sub rate at 50000/s during the 30-minutes' test.

**pub-to-sub latency percentiles**

![pub-to-sub latency percentiles](https://assets.emqx.com/images/ec5c29b15eaccb355f1cc746580da4ef.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** |
| :--------------- | :------- | :------------ |
| p50              | 1        | 361           |
| p75              | 1        | 367           |
| p90              | 2        | 372           |
| p95              | 4        | 378           |
| p99              | 18       | 417           |

**Result Charts**

- EMQX

  ![EMQX Result Charts](https://assets.emqx.com/images/9d77993ae5813e4358c51f377802bc9a.png)

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/caa81cafeaf2df7685baef65857203e6.png)

#### **Fan-out**: fanout-5-1000-5-250K

**Metrics**

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | 250k            | 1.99                            | 73%                 | 71%                 | 530M            | 483M            |
| **Mosquitto** | 82k             | 12,240.83                       | 7%                  | 6%                  | 355M            | 341M            |

> In this scenario, Mosquitto cannot reach to the target message rate. The throughput has been fluctuating around 80,000/s. 
>
> EMQX keeps the stable rate at 250,000+/s throughout the test.

**pub-to-sub latency percentiles**

![pub-to-sub latency percentiles](https://assets.emqx.com/images/70c66389239808b5a1e22e3dc93b8ba0.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** |
| :--------------- | :------- | :------------ |
| p50              | 2        | 12,378        |
| p75              | 2        | 12,522        |
| p90              | 3        | 12,571        |
| p95              | 3        | 12,596        |
| p99              | 4        | 12,627        |

**Result Charts**

- EMQX

  ![EMQX Result Charts](https://assets.emqx.com/images/5af15d0d153715c2a4daecab78125b2d.png)

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/6b4bf8307ec9d101c7c2c2ab09adfd01.png)

#### **Fan-in:** sharedsub-50K-500-50K-50K

**Metrics**

|               | Actual msg rate      | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | -------------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**      | pub: 50k<br>sub: 50k | 1.47                            | 94%                 | 93%                 | 8.19G           | 6.67G           |
| **Mosquitto** | pub: 50k<br>sub: 40k | 12,723.07                       | 7%                  | 7%                  | 485M            | 456M            |

> In this scenario, the consumption rate of Mosquitto cannot reach to the target rate. It stabilized at 41,000/s. 
>
> EMQX keeps the stable pub & sub rate at 50,000/s throughout the test.

**pub-to-sub latency percentiles**

![pub-to-sub latency percentiles](https://assets.emqx.com/images/ec58d66c7e41afa879642bbdccd353a5.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** |
| :--------------- | :------- | :------------ |
| p50              | 1        | 13,138        |
| p75              | 1        | 13,281        |
| p90              | 2        | 13,423        |
| p95              | 2        | 13,526        |
| p99              | 19       | 13,736        |

**Result Charts**

- EMQX

  ![EMQX Result Charts](https://assets.emqx.com/images/02183e81cfdb5df5f2c1d734b389d048.png)

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/bb36edeff51fba893c2995fc0f2769ce.png)

#### **Concurrent connections**: conn-tcp-1M-5K

**Metrics**

|               | Average latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :------------ | -------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **EMQX**      | 2.4                  | 35%                 | 22%                 | 10.77G          | 8.68G                 |
| **Mosquitto** | 5.74                 | 2%                  | 2%                  | 1G              | 1G                    |

**Latency percentiles**

![Latency percentiles](https://assets.emqx.com/images/13830b642440d532412d6dda02b3f430.png)

| **Latency (ms)** | **ENQX** | **Mosquitto** |
| :--------------- | :------- | :------------ |
| p50              | 2        | 2             |
| p75              | 2        | 2             |
| p90              | 2        | 2             |
| p95              | 2        | 2             |
| p99              | 3        | 9             |

**Result Charts**

- EMQX

  ![EMQX Result Charts](https://assets.emqx.com/images/e0ea4fd7d5f800096d0ae694e93ce0e9.png)

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/f844b52d4c44c8b04fe8d5b1df46cfa7.png) 

## Conclusion

According to the performance benchmarking comparison between EMQX and Mosquitto, EMQX demonstrated superior performance across all scenarios of the enterprise set, with higher throughput and faster response times. In the point-to-point scenario, EMQX achieved a message routing rate of up to 100,000 per second, while Mosquitto was limited to around 40,000. In the fan-out scenario, EMQX demonstrated the ability to handle fan-out throughput up to 500,000 per second, while Mosquitto's maximum was only 80,000.

However, it is worth noting that Mosquitto was observed to perform well and had lower CPU and memory usage when there were smaller loads.

To conclude, the choice between EMQX and Mosquitto depends on the specific use case and requirements. For resource-constrained environments such as embedded hardware and IoT edge deployments, Mosquitto may be a better option. On the other hand, for applications that require high scalability and availability, EMQX is recommended as a cloud-based MQTT messaging service.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
