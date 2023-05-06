> The blog post [Open MQTT Benchmark Suite: The Ultimate Guide to MQTT Performance Testing](https://www.emqx.com/en/blog/open-mqtt-benchmark-suite-the-ultimate-guide-to-mqtt-performance-testing) introduced the Open MQTT Benchmark Suite developed by EMQ. We defined MQTT benchmark scenarios, use cases, and observation metrics in [the GitHub project](https://github.com/emqx/mqttbs). Based on the activity and popularity of the community and GitHub project, the top 4 open-source [MQTT brokers in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) – EMQX,  Mosquitto, NanoMQ, and Vernemq, were chosen to perform the benchmark test. 
>
> This blog series presents the benchmark test results and aims to help you choose a suitable MQTT broker based on your needs and use cases.

This is the last post of the blog series, which provides the benchmarking results of EMQX and VerneMQ. Additionally, we compare the features and capabilities of both brokers in detail in another[ post](https://www.emqx.com/en/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison). 

## MQTT Benchmark Scenarios and Use Cases

[The MQTT Benchmark Suite](https://github.com/emqx/mqttbs) designs two sets of benchmark use cases. One is named Basic Set, which is for small-scale performance verification, and another is called Enterprise Set, which aims for enterprise level verification.

Detailed descriptions of the testing scenarios are already available on the [GitHub project](https://github.com/emqx/mqttbs) , for convenience we briefly list them here as well.

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

![XMeter](https://assets.emqx.com/images/fc5defa16b656b6f86f811eb6336288a.png)

### SW Version

| **Broker** | **Version** |
| :--------- | :---------- |
| EMQX       | 4.4.16      |
| VerneMQ    | 1.12.6.2    |
| XMeter     | 3.2.4       |

## Benchmarking Results

### Basic Set

#### **point-to-point**: 1K:1K

|             | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | 0.27                            | 4%                  | 2%                  | 510M            | 495M            |
| **VerneMQ** | 0.33                            | 0.4                 | 10%                 | 6%              | 1.3G            |

#### Fan-out 1k QoS 1

|             | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | 3                               | 2%                  | 1%                  | 475M            | 460M            |
| **VerneMQ** | 21.55                           | 4%                  | 2%                  | 1.2G            | 1.1G            |

#### Fan-in 1k - shared subscription QoS 1

|             | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | 0.19                            | 3%                  | 2%                  | 468M            | 460M            |
| **VerneMQ** | 0.34                            | 6%                  | 5%                  | 1.3G            | 1.2G            |

#### 10K connections cps 100

|             | Average latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :---------- | -------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **EMQX**    | 0.74                 | 2%                  | 1%                  | 540M            | 510M                  |
| **VerneMQ** | 0.89                 | 3%                  | 0%                  | 1.1G            | 1.0G                  |

### Enterprise Set

### **point-to-point**: p2p-50K-50K-50K-50K

**Metrics**

|             | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | 50k:50k         | 1.58                            | 88%                 | 80%                 | 5.71G           | 5.02G           |
| **VerneMQ** | 50k:50k         | 2136.62                         | 91%                 | 90%                 | 6.30G           | 6.02G           |

> EMQX keeps the stable pub & sub rate at 50000/s during the 30-minute's test. VerneMQ is able to handle the target 50k message incoming and outgoing throughput, but the latency was quite high.

**pub-to-sub latency percentiles**

![image.png](https://assets.emqx.com/images/d94211c93890754dd45d113d87104dcc.png)

| **Latency (ms)** | **EMQX** | **VerneMQ** |
| :--------------- | :------- | :---------- |
| p50              | 1        | 467         |
| p75              | 1        | 2,937       |
| p90              | 2        | 6,551       |
| p95              | 4        | 9,517       |
| p99              | 18       | 16,500      |

**Result Charts**

- EMQX

   ![EMQX Result Charts](https://assets.emqx.com/images/f52cb6924abc90ec0a42791696ad65bd.png)

- VerneMQ

   ![VerneMQ Result Charts](https://assets.emqx.com/images/17ccdda6e301e1aabac19244efbbbb8a.png)

#### **Fan-out**: fanout-5-1000-5-250K

**Metrics**

|             | Actual msg rate | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | --------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | 250k            | 1.99                            | 73%                 | 71%                 | 530M            | 483M            |
| **VerneMQ** | 82k             | 11,802.11                       | 93%                 | 92%                 | 3.01G           | 2.94G           |

> In this scenario, Verne cannot reach to the target message rate. The throughput has been fluctuating around 82,000/s. 
>
> EMQX keeps the stable rate at 250,000+/s throughout the test.

**pub-to-sub latency percentiles**

![pub-to-sub latency percentiles](https://assets.emqx.com/images/58f1c28ff3fc629fd54342f84b9132bc.png)

| **Latency (ms)** | **EMQX** | **VerneMQ** |
| :--------------- | :------- | :---------- |
| p50              | 2        | 11,966      |
| p75              | 2        | 12,551      |
| p90              | 3        | 13,060      |
| p95              | 3        | 13,357      |
| p99              | 4        | 13,884      |

**Result Charts**

- EMQX

   ![EMQX Result Charts](https://assets.emqx.com/images/9d448778cfba5e7057ef78d530b3b5db.png)

- VerneMQ

   ![VerneMQ Result Charts](https://assets.emqx.com/images/f0ea6af5a157fa3ade9bcea192616116.png)

#### **Fan-in:** sharedsub-50K-500-50K-50K

**Metrics**

|             | Actual msg rate         | Average pub-to-sub latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Avg memory used |
| :---------- | ----------------------- | ------------------------------- | ------------------- | ------------------- | --------------- | --------------- |
| **EMQX**    | pub: 50k<br>sub: 50k    | 1.47                            | 94%                 | 93%                 | 8.19G           | 6.67G           |
| **VerneMQ** | pub: 7.6k<br> sub: 3.5k | 116,888.61                      | 83%                 | 74%                 | 12.16G          | 8.38G           |

**pub-to-sub latency percentiles**

![pub-to-sub latency percentiles](https://assets.emqx.com/images/5ea05208b58e27e5f7169302012f3661.png)

| **Latency (ms)** | **EMQX** | **VerneMQ** |
| :--------------- | :------- | :---------- |
| p50              | 1        | 128,251     |
| p75              | 1        | 132,047     |
| p90              | 2        | 135,239     |
| p95              | 2        | 137,106     |
| p99              | 19       | 140,528     |

**Result Charts**

- EMQX

   ![EMQX Result Charts](https://assets.emqx.com/images/f384331ef2be2904a4555d8ca98a768f.png)

- VermeMQ

   ![VerneMQ Result Charts](https://assets.emqx.com/images/83796fa0b3605d55f02a2cc08cfcbe41.png)

#### **Concurrent connections**: conn-tcp-1M-5K

**Metrics**

|             | Average latency (ms) | Max CPU user+system | Avg CPU user+system | Max memory used | Memory used Stable at |
| :---------- | -------------------- | ------------------- | ------------------- | --------------- | --------------------- |
| **EMQX**    | 2.4                  | 35%                 | 22%                 | 10.77G          | 8.68G                 |
| **VerneMQ** | 2.47                 | 44%                 | 25%                 | 22.4G           | not stable            |

> During a 30-minute’s test for VerneMQ, the memory used keeps increasing. It rose from 18GB when 1 million connections were completed to 22.4GB at the end of the test.

**Latency percentiles**

![Latency percentiles](https://assets.emqx.com/images/e62ea969bdeb9e438bc8303d26d2548f.png)

| **Latency (ms)** | **ENQX** | **VerneMQ** |
| :--------------- | :------- | :---------- |
| p50              | 2        | 2           |
| p75              | 2        | 2           |
| p90              | 2        | 2           |
| p95              | 2        | 3           |
| p99              | 3        | 3           |

**Result Charts**

- EMQX

   ![EMQX Result Charts](https://assets.emqx.com/images/5722b29a4d555d72d2034d9d102bb24a.png)

- VerneMQ

   ![VerneMQ Result Charts](https://assets.emqx.com/images/3bc56d581615534c12c63fb510c4088e.png)

## Conclusion

EMQX and VerneMQ have similar performance for the basic test cases. In the enterprise level testing,  EMQX outperformed VerneMQ across all scenarios. As stated in another[ post](https://www.emqx.com/en/blog/emqx-vs-vernemq-2023-mqtt-broker-comparison), EMQX is one of the best choices for deploying MQTT brokers in production in 2023.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
