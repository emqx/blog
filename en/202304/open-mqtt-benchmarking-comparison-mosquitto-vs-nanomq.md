> The blog post [Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing) introduced the Open MQTT Benchmark Suite developed by EMQ. We defined MQTT benchmark scenarios, use cases, and observation metrics in [the GitHub project](https://github.com/emqx/mqttbs). Based on the activity and popularity of the community and GitHub project, the top 4 open-source [MQTT brokers in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) – EMQX,  Mosquitto, NanoMQ, and Vernemq, were chosen to perform the benchmark test. 
>
> This blog series presents the benchmark test results and aims to help you choose a suitable MQTT broker based on your needs and use cases.

In this first post, we provide the benchmarking results of NanoMQ and Mosquitto brokers. Additionally, we compare the features and capabilities of both brokers in detail in another [post.](https://www.emqx.com/en/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison) 


## MQTT Benchmark Scenarios and Use Cases

Detailed descriptions of the testing scenarios are already available on the [GitHub project](https://github.com/emqx/mqttbs), but for convenience, we briefly list them here as well.

All the tests are executed on a single node.

### Use Cases

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

[XMeter](https://www.emqx.com/en/products/xmeter) is used in this benchmark test to simulate various business scenarios. XMeter is built on top of JMeter but with enhanced scalability and more capabilities. It provides comprehensive and real-time test reports during the test. Additionally, its built-in monitoring tools are used to track the resource usage of the Mosquitto/NanoMQ server, enabling a comparison with the information provided by the operating systems.

XMeter provides a private deployment version (on-premise) and a public cloud SaaS version. A private XMeter is deployed in the same VPC as the MQTT broker server in this testing.

![XMeter Architecture](https://assets.emqx.com/images/2fa0a7d8348ec532b386d5723fc32419.png)

### SW Version

| **Broker**                            | **Version** |
| :------------------------------------ | :---------- |
| Mosquitto (with persistence disabled) | 2.0.15      |
| NanoMQ                                | 0.17.0      |
| XMeter                                | 3.2.4       |

## Benchmarking Results

### **point-to-point**: p2p-50K-50K-50K-50K

#### Metrics

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 37k:37k         | 353.82                          | 6%                  | 6%                  | 341M            | 318M            |
| **NanoMQ**    | 50k:50k         | 91                              | 35%                 | 30%                 | 1.33G           | 1.3G            |

> In this scenario, Mosquitto cannot reach to the expected message rate. It stabilized at 37300/s for both pub and sub. 
>
> NanoMQ keeps the stable pub & sub rate at 50000/s during the 30-minutes' test.

#### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/dff9e6e24c0cbbbdb2fbacb2fe40abdf.png)

| **Latency (ms)** | **Mosquitto** | **NanoMQ** |
| :--------------- | :------------ | :--------- |
| p50              | 361           | 82         |
| p75              | 367           | 171        |
| p90              | 372           | 210        |
| p95              | 378           | 225        |
| p99              | 417           | 251        |

#### Result Charts

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/be85ec742b1d733ec9ac3ada28a654e2.png)

- NanoMQ

  ![NanoMQ Result Charts](https://assets.emqx.com/images/8313fed21a7d383cb7179e9e72423ac7.png)

### **Fan-out**: fanout-5-1000-5-250K

#### Metrics

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 82k             | 12,240.83                       | 7%                  | 6%                  | 355M            | 341M            |
| **NanoMQ**    | 255k            | 13.91                           | 73%                 | 71%                 | 781M            | 682M            |

> In this scenario, Mosquitto cannot reach to the expected message rate. The throughput has been fluctuating around 80,000/s. 
>
> NanoMQ keeps the stable rate at 250,000+/s throughout the test.

#### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/728c1e8db438652164b79a1d39de40f4.png)

| **Latency (ms)** | **Mosquitto** | **NanoMQ** |
| :--------------- | :------------ | :--------- |
| p50              | 12,378        | 14         |
| p75              | 12,522        | 18         |
| p90              | 12,571        | 21         |
| p95              | 12,596        | 23         |
| p99              | 12,627        | 26         |

#### Result Charts

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/a6cb91309ef95e61c42bbe3510a625c6.png)

- NanoMQ

  ![NanoMQ Result Charts](https://assets.emqx.com/images/1570427cf926486387e66be698b24704.png)

### **Fan-in:** sharedsub-50K-500-50K-50K

#### Metrics

|               | Actual msg rate  | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ---------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | pub: 50ksub: 40k | 12,723.07                       | 7%                  | 7%                  | 485M            | 456M            |
| **NanoMQ**    | pub: 50ksub: 50k | 2.76                            | 34%                 | 34%                 | 795M            | 783M            |

> In this scenario, the consumption rate of Mosquitto cannot reach to the expected rate. It stabilized at 41,000/s. 
>
> NanoMQ keeps the stable pub & sub rate at 50,000/s throughout the test.

#### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/37c8a28c3c68e86cae6e0102695eb08d.png)

| **Latency (ms)** | **Mosquitto** | **NanoMQ** |
| :--------------- | :------------ | :--------- |
| p50              | 13,138        | 2          |
| p75              | 13,281        | 3          |
| p90              | 13,423        | 4          |
| p95              | 13,526        | 5          |
| p99              | 13,736        | 21         |

#### Result Charts

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/31a1a62938e40893782fd7cb891f5531.png)

- NanoMQ

  ![NanoMQ Result Charts](https://assets.emqx.com/images/2275dba61116d31a256f2e33d7839f7b.png)

### **Concurrent Connection**: conn-tcp-1M-5K

#### Metrics

|               | Average latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :------------ | -------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **Mosquitto** | 5.74                 | 2%                  | 2%                  | 1G              | 1G                    |
| **NanoMQ**    | 3.16                 | 5%                  | 4%                  | 6.9G            | 6.9G                  |

#### Latency percentiles

![Latency percentiles](https://assets.emqx.com/images/4f1c661a88962a1b89ce929634affddb.png)

| **Latency (ms)** | **Mosquitto** | **NanoMQ** |
| :--------------- | :------------ | :--------- |
| p50              | 2             | 2          |
| p75              | 2             | 2          |
| p90              | 2             | 2          |
| p95              | 2             | 2          |
| p99              | 9             | 3          |

#### Result Charts

- Mosquitto

  ![Mosquitto Result Charts](https://assets.emqx.com/images/8aa85e4d28f187dad1412164a3899097.png)

- NanoMQ

  ![NanoMQ Result Charts](https://assets.emqx.com/images/244b7bbcb7e0696553fc3e686fc494dd.png)

## Conclusion

As mentioned in the [blog post](https://www.emqx.com/en/blog/mosquitto-vs-nanomq-2023-mqtt-broker-comparison), Mosquitto is a single-threaded design, while NanoMQ is built on NNG's asynchronous I/O with a built-in actor multi-threading model. The above test results have proven that NanoMQ fully utilizes the multi-core and multi-threading capabilities to support higher and more stable message throughput. 

For example, in the fan-out scenario, Mosquitto can only support an outgoing message rate of around 82k per second, while NanoMQ can keep a stable rate of 250k. Even NanoMQ can stably handle message throughput of up to 500k on this c5.4xlarge virtual machine. 

While Mosquitto struggles to contain the workload, NanoMQ can easily fit into the boots. However, it doesn't mean NanoMQ beats Mosquitto, and only they are designed for different targets: single-core vs. multi-cores. It is becoming common for embedded designs to incorporate more than one CPU on an SMP platform. That said, NanoMQ is the best fit if you work with a multi-core platform and want to achieve the best throughput. On the other hand, Mosquitto can help you limit CPU and memory usage while performance is not a priority.

 

<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>
