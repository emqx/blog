> The blog post [Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing) introduced the Open MQTT Benchmark Suite developed by EMQ. We defined MQTT benchmark scenarios, use cases, and observation metrics in [the GitHub project](https://github.com/emqx/mqttbs). Based on the activity and popularity of the community and GitHub project, the top 4 open-source [MQTT brokers in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) – EMQX, Mosquitto, NanoMQ, and Vernemq, were chosen to perform the benchmark test.
>
> This blog series presents the benchmark test results and aims to help you choose a suitable MQTT broker based on your needs and use cases.

## MQTT Benchmark Scenario Sets and Use Cases

[The MQTT Benchmark Suite](https://github.com/emqx/mqttbs) designs two sets of benchmark use cases. One is named Basic Set, which is for small-scale performance verification, and another is called Enterprise Set, which aims for enterprise level verification. 

Detailed descriptions of the testing scenarios are already available on the [GitHub project](https://github.com/emqx/mqttbs), for convenience we briefly list them here as well. All the tests are executed on a single node.

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
  - 5 subscribers consume all messages in a [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) way
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

![XMeter](https://assets.emqx.com/images/2b2a74ce51eb559568b3eb6ed45e2c81.png)

### SW Version

| **Broker**                            | **Version** |
| :------------------------------------ | :---------- |
| EMQX                                  | 4.4.16      |
| Mosquitto (with persistence disabled) | 2.0.15      |
| NanoMQ                                | 0.17.0      |
| VerneMQ                               | 1.12.6.2    |
| XMeter                                | 3.2.4       |

## Benchmarking Results

> CPU and Memory consumption for the message throughput scenarios are counted for the phase of message sending & receiving. For the concurrent connection test, they are counted in the connection phase.

### Basic Set

#### **point-to-point**: 1K:1K

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 0.25                            | 0%                  | 0%                  | 278M            | 254M            |
| **NanoMQ**    | 0.25                            | 1%                  | 0%                  | 271M            | 270M            |
| **EMQX**      | 0.27                            | 4%                  | 2%                  | 510M            | 495M            |
| **VerneMQ**   | 0.4                            | 10%                 | 6%                 | 1.3G              | 1.2G            |

#### Fan-out 1k QoS 1

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 5.73                            | 0%                  | 0%                  | 270M            | 260M            |
| **NanoMQ**    | 13.66                           | 0%                  | 0%                  | 271M            | 263M            |
| **EMQX**      | 3                               | 2%                  | 1%                  | 475M            | 460M            |
| **VerneMQ**   | 21.55                           | 4%                  | 2%                  | 1.2G            | 1.1G            |

#### Fan-in 1k - shared subscription QoS 1

|               | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 0.20                            | 0%                  | 0%                  | 281M            | 246M            |
| **NanoMQ**    | 0.18                            | 0%                  | 0%                  | 294M            | 267M            |
| **EMQX**      | 0.19                            | 3%                  | 2%                  | 468M            | 460M            |
| **VerneMQ**   | 0.34                            | 6%                  | 5%                  | 1.3G            | 1.2G            |

#### 10K connections cps 100

|               | Average  latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :------------ | --------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **Mosquitto** | 0.6                   | 0%                  | 0%                  | 306M            | 264M                  |
| **NanoMQ**    | 0.59                  | 0%                  | 0%                  | 320M            | 320M                  |
| **EMQX**      | 0.74                  | 2%                  | 1%                  | 540M            | 510M                  |
| **VerneMQ**   | 0.89                  | 3%                  | 0%                  | 1.1G            | 1.0G                  |

### Enterprise Set

#### **point-to-point**: 50K:50K QoS1

##### Metrics

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 37k:37k         | 353.82                          | 6%                  | 6%                  | 341M            | 318M            |
| **NanoMQ**    | 50k:50k         | 91                              | 35%                 | 30%                 | 1.33G           | 1.3G            |
| **EMQX**      | 50k:50k         | 1.58                            | 88%                 | 80%                 | 5.71G           | 5.02G           |
| **VerneMQ**   | 50k:50k         | 2136.62                         | 91%                 | 90%                 | 6.30G           | 6.02G           |

> In this scenario, Mosquitto cannot reach to the target message rate. It stabilized at 37300/s for both pub and sub. VerneMQ is able to handle the expected 50k message incoming and outgoing throughput, but the latency was quite high.

##### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/d02666d26d41252ce75cb8c7d27019e0.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :--------------- | :------- | :------------ | :--------- | :---------- |
| p50              | 1        | 361           | 82         | 467         |
| p75              | 1        | 367           | 171        | 2,937       |
| p90              | 2        | 372           | 210        | 6,551       |
| p95              | 4        | 378           | 225        | 9,517       |
| p99              | 18       | 417           | 251        | 16,500      |

#### Fan-out 250k QoS 1

##### Metrics

|               | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | 81k             | 12,240.83                       | 7%                  | 6%                  | 355M            | 341M            |
| **NanoMQ**    | 250k            | 13.91                           | 73%                 | 71%                 | 781M            | 682M            |
| **EMQX**      | 250k            | 1.99                            | 73%                 | 71%                 | 530M            | 483M            |
| **VerneMQ**   | 80k             | 11,802.11                       | 93%                 | 92%                 | 3.01G           | 2.94G           |

> In this scenario, Mosquitto and VerneMQ cannot reach to the target message rate. The throughput of Mosquitto and VerneMQ have been fluctuating around 80,000/s.

##### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/c5cfd5a86a05cb09201d1b6d8adcbbc1.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :--------------- | :------- | :------------ | :--------- | :---------- |
| p50              | 2        | 12,378        | 14         | 11,966      |
| p75              | 2        | 12,522        | 18         | 12,551      |
| p90              | 3        | 12,571        | 21         | 13,060      |
| p95              | 3        | 12,596        | 23         | 13,357      |
| p99              | 4        | 12,627        | 26         | 13,884      |

#### Fan-in 50k - shared subscription QoS 1

##### Metrics

|               | Actual msg rate         | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :------------ | ----------------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **Mosquitto** | pub: 50k<br>sub: 40k    | 12,723.07                       | 7%                  | 7%                  | 485M            | 456M            |
| **NanoMQ**    | pub: 50k<br>sub: 50k    | 2.76                            | 34%                 | 34%                 | 795M            | 783M            |
| **EMQX**       | pub: 50k<br>sub: 50k    | 1.47                            | 94%                 | 93%                 | 8.19G           | 6.67G           |
| **VerneMQ**   | pub: 7.6k<br> sub: 3.5k | 116,888.61                      | 83%                 | 74%                 | 12.16G          | 8.38G           |

##### pub-to-sub latency percentiles

![pub-to-sub latency percentiles](https://assets.emqx.com/images/106b87f857cd196356b9e66f97e892b4.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :--------------- | :------- | :------------ | :--------- | :---------- |
| p50              | 1        | 13,138        | 2          | 128,251     |
| p75              | 1        | 13,281        | 3          | 132,047     |
| p90              | 2        | 13,423        | 4          | 135,239     |
| p95              | 2        | 13,526        | 5          | 137,106     |
| p99              | 19       | 13,736        | 21         | 140,528     |

#### 1M connections cps 5k

##### Metrics

|               | Average  latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :------------ | --------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **Mosquitto** | 5.74                  | 2%                  | 2%                  | 1G              | 1G                    |
| **NanoMQ**    | 3.16                  | 5%                  | 4%                  | 6.9G            | 6.9G                  |
| **EMQX**       | 2.4                   | 35%                 | 22%                 | 10.77G          | 8.68G                 |
| **VerneMQ**   | 2.47                  | 44%                 | 25%                 | 22.4G           | not stable            |

> During a 30-minute’s test of VerneMQ, the memory used keeps increasing. It rose from 18GB when 1 million connections were completed to 22.4GB at the end of the test.

##### latency percentiles

![latency percentiles](https://assets.emqx.com/images/e31e24fcd53347098ecc7c1ff2f34100.png)

| **Latency (ms)** | **EMQX** | **Mosquitto** | **NanoMQ** | **VerneMQ** |
| :--------------- | :------- | :------------ | :--------- | :---------- |
| p50              | 2        | 2             | 2          | 2           |
| p75              | 2        | 2             | 2          | 2           |
| p90              | 2        | 2             | 2          | 2           |
| p95              | 2        | 2             | 2          | 3           |
| p99              | 3        | 9             | 3          | 3           |

## Conclusion

The above benchmark results indicate that there is not much difference in the performance of the four brokers in basic use case set, and except for the fan-out scenario, the latency is within milliseconds. Mosquitto and NanoMQ have the least CPU and memory usage, EMQX is slightly higher, and VerneMQ has the highest usage.

In enterprise level set, EMQX and NanoMQ perform the best in all use cases. Both can support the target throughput and higher, and the latency is reasonable, within milliseconds or tens of milliseconds. In summary, EMQX, Mosquitto, NanoMQ, and VerneMQ are the top four [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) in the open-source community in 2023. You can choose the most suitable one according to your actual needs and usage scenarios.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
