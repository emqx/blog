## 前言

很多 MQTT 项目和物联网服务都提供了[在线的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，用户可以直接利用其进行 MQTT 学习、测试、原型制作甚至是小规模使用，而无需再自行部署，方便快捷，节省时间与精力成本。

但因为地理位置、网络环境以及服务器负载不同，每个公共服务器的稳定性以及消息传输时延也不尽相同。尽管几乎所有服务提供方都声明不对其免费服务的稳定性和安全性负责，但用户在使用时却需要考虑这些因素。

为此，本文整理了一些较为热门的免费在线 [MQTT 服务器](https://www.emqx.io/zh)，通过可访问性、网络延时、小规模性能测试以及消息实际传输延时等几个层面进行评估对比，希望可以为您的选择提供参考。


## 热门在线公共 MQTT 服务器

本文选取了以下几个热门的在线公共 MQTT 服务器：

| 名称          | Broker 地址               | TCP  | TLS        | WebSocket |
| :------------ | :------------------------ | :--- | :--------- | :-------- |
| EMQX         | `broker.emqx.io`          | 1883 | 8883       | 8083,8084 |
| EMQX（国内） | `broker-cn.emqx.io`       | 1883 | 8883       | 8083,8084 |
| Eclipse       | `mqtt.eclipseprojects.io` | 1883 | 8883       | 80, 443   |
| Mosquitto     | `test.mosquitto.org`      | 1883 | 8883, 8884 | 80        |
| HiveMQ        | `broker.hivemq.com`       | 1883 | N/A        | 8000      |

### EMQX

免费在线的 MQTT 5 服务器，由 [EMQX Cloud](https://www.emqx.com/zh/cloud) 提供。为优化国内用户访问速度，分别提供了海外跟国内两个接入点，其中 EMQX 部署在 AWS 美国俄勒冈区域，EMQX（国内）部署在腾讯云上海区域，国内访问有稳定的网络通道。

两个接入点均为 2 个节点组成的 [EMQX 集群](https://www.emqx.com/zh/blog/tag/mqtt-broker-集群)，后期根据实际接入量和负载可以自动扩容更多节点。根据后台显示，该服务器基于 [EMQX 企业版](https://www.emqx.com/zh/products/emqx) 4.2.6 版本，当前运行时长为 128 天。

详细介绍请访问 EMQ 官网页面：[免费的在线 MQTT 5 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。

> 注：EMQX 与 EMQX(国内) 两个接入点数据不互通。

### Eclipse

由 Eclipse IoT 提供的免费在线 MQTT 服务器，解析到的 IP 显示其部署在 Azure 美国弗吉尼亚区域。值得一提的是此前该服务器的接入地址一直都是 `mqtt.eclipse.org`，不知因何故更换到现在的接入地址，撰写本文时我使用旧地址接入失败一度以为服务器已经停了，最后通过 HTTP 访问原接入点时才发现已经做了 301 永久重定向。

根据 `$SYS/#` 系统主题查询得出该服务器基于 Mosquitto 2.0.12 版本，当前运行时长为 71227 秒，疑似在一天前重启过服务。

相关介绍：[https://mqtt.eclipseprojects.io/](https://mqtt.eclipseprojects.io/ )

### Mosquitto

由 Mosquitto 社区提供的免费在线 MQTT 服务器，解析到的 IP 显示其部署在 OVH 法国鲁贝区域。在测试中发现正常情况下该接入点网络延时较高，所幸丢包率比较低，某些时段会出现连接失败的情况。

根据 `$SYS/#` 系统主题查询得出该服务器基于 Mosquitto 2.0.12 版本，当前运行时长为 28519 秒，疑似在一天内重启过服务。

相关介绍：[https://test.mosquitto.org/](https://test.mosquitto.org/)

### HiveMQ

由 HiveMQ 提供的免费在线 MQTT 服务器，解析到的 IP 显示其部署在 AWS 德国法兰克福区域。

由于其 `$SYS/#` 系统主题无法订阅，无法获知提供服务的 Broker 类型、具体版本以及当前运行时长。

相关介绍：[http://www.mqtt-dashboard.com/](http://www.mqtt-dashboard.com/)


## 测试环境

- 网络：国内，云南地区电信网络
- 操作系统：macOS 10.15.7

> 注：受限于地理位置不同，不同地方的网络环境会有一定差异，导致本文测试结果可能会有所差异。


## 可访问性测试

### 测试结果

该环节中使用 [MQTT 客户端工具 - MQTTX](https://mqttx.app/zh) 进行可访问性测试，尝试通过 TCP 1883 端口建立连接，经过反复测试只有 Eclipse 提供的免费服务无法访问，总体结果如下：

| 名称          | Broker 地址               | TCP  | 可用 |
| :------------ | :------------------------ | :--- | :--- |
| EMQX         | `broker.emqx.io`          | 1883 | YES  |
| EMQX（国内） | `broker-cn.emqx.io`       | 1883 | YES  |
| Eclipse       | `mqtt.eclipseprojects.io` | 1883 | NO   |
| Mosquitto     | `test.mosquitto.org`      | 1883 | YES  |
| HiveMQ        | `broker.hivemq.com`       | 1883 | YES  |

![在线 mqtt 服务器可访问性测试](https://assets.emqx.com/images/1b5abcf0b2bf6548a62f0ef05a71819e.png)


### 测试配置文件下载

MQTTX 具备连接导入导出功能，以下是本文测试使用的连接数据，可以通过数据恢复的方式导入 MQTTX 中。

- [MQTTX-backup-free-public-mqtt-broker.json](https://github.com/wivwiv/mqtt-explore/blob/master/MQTTX-backup-free-public-mqtt-broker.json)

![MQTTX 配置文件导入](https://assets.emqx.com/images/a7a336d10e7358ee2f8721676a7ba34b.png)


## 国内网络延时测试

通过网络访问检测网络连通情况和网络延时，由于部分服务禁用了 ICMP 协议，同时各个地方的网络情况不一样，此处使用 WebSocket 地址，借助国内热门的测速工具 [站长工具](https://tool.chinaz.com/speedtest/broker.emqx.io:1883) 的 HTTP 测速进行测试：

| 名称        | HTTP 地址(点击进行测试)                                      | WebSocket |
| :---------- | :----------------------------------------------------------- | :-------- |
| EMQX       | [http://broker.emqx.io:8083/mqtt](https://tool.chinaz.com/speedtest/http://broker.emqx.io:8083/mqtt) | 8083      |
| EMQX(国内) | [http://broker-cn.emqx.io:8083/mqtt](https://tool.chinaz.com/speedtest/broker-cn.emqx.io:8083/mqtt) | 8083      |
| Eclipse     | [http://mqtt.eclipseprojects.io/mqtt](https://tool.chinaz.com/speedtest/mqtt.eclipseprojects.io/mqtt) | 80        |
| Mosquitto   | [http://test.mosquitto.org/mqtt](https://tool.chinaz.com/speedtest/test.mosquitto.org/mqtt) | 80        |
| HiveMQ      | [http://broker.hivemq.com:8000/mqtt](https://tool.chinaz.com/speedtest/broker.hivemq.com:8000/mqtt) | 8000      |


![EMQX 国内在线 MQTT 服务器](https://assets.emqx.com/images/1db5ba4457b7470d95335fd4a1a78128.png)

![EMQX 在线 MQTT 服务器](https://assets.emqx.com/images/7ce2e61433a81820e1729aff87b6e39e.png)

![Mosquitto 在线 MQTT 服务器](https://assets.emqx.com/images/8fd2b6f61ea81441d0b683da748bd5df.png)

![HiveMQ 在线 MQTT 服务器](https://assets.emqx.com/images/f1d36385657b4796b753827e67e547a7.png)


## 小规模性能测试

借助开源 [MQTT 性能测试工具 emqtt-bench](https://github.com/emqx/emqtt-bench) 进行测试，测试客户端的 Pub Sub 是否有速率限制。

**出于实用性的考虑**，本轮测试并非是探究每个接入点的速率上限，而是考量每个接入点能够满足常规的使用强度。本轮设计的场景是测试单客户端 Sub/Pub 消息为 1000 msg/s 持续 1 分钟，消息大小为 256 Bytes，记录每个接入点是否达标、是否有限速，下图为测试架构：

![MQTT 服务器测试](https://assets.emqx.com/images/c99599884b7a36bec05977c5429cbe11.png)

准备好 emqtt-bench 之后，以下每组 Sub Pub 命令各自在不同的窗口执行即可：

| 名称          | Broker 地址               | TCP  | Pub 达标                | Sub 达标                   |
| :------------ | :------------------------ | :--- | :---------------------- | :------------------------- |
| EMQX         | `broker.emqx.io`          | 1883 | YES                     | YES                        |
| EMQX（国内） | `broker-cn.emqx.io`       | 1883 | YES                     | YES                        |
| Eclipse       | `mqtt.eclipseprojects.io` | 1883 | YES                     | YES                        |
| Mosquitto     | `test.mosquitto.org`      | 1883 | 速率在 50 msg/s左右波动 | 速率在 0-50 msg/s 之间波动 |
| HiveMQ        | `broker.hivemq.com`       | 1883 | YES                     | 速率稳定在 50 msg/s 左右   |

```shell
# EMQX
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker.emqx.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker.emqx.io -I 1

# EMQX CN
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker-cn.emqx.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker-cn.emqx.io -I 1

# Eclipse
## Sub
./emqtt_bench sub -t t/1 -c 1 -h mqtt.eclipseprojects.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h mqtt.eclipseprojects.io -I 1

# Mosquitto
## Sub
./emqtt_bench sub -t t/1 -c 1 -h test.mosquitto.org
## Pub
./emqtt_bench pub -t t/1 -c 1 -h test.mosquitto.org -I 1

# HiveMQ
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker.hivemq.com
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker.hivemq.com -I 1
```


## 消息实际传输延时测试

目的：考量消息从 Pub 端到 Sub 端所需要的时间，采样分析传输稳定性与平均耗时。

测试步骤：客户端连接到公共服务器，每 5 秒钟发布一条带时间戳的消息，订阅者接收到消息之后去当前时间戳减去消息中的时间戳，计算得出消息时延记录至数据库，统计 30 分钟后进行采样分析。

测试模型如下：

![MQTT 服务器消息传输延时测试模型](https://assets.emqx.com/images/be1b6d5e21db52fb8d2514206905b5de.png)


测试代码：[free-online-public-broker-test.js](https://github.com/wivwiv/mqtt-explore/blob/master/free_online_public_broker_test.js)

### 时延历史

![MQTT 服务器消息传输延时测试](https://assets.emqx.com/images/1a8c044469271d6871cca19321ce3882.png)

### 平均时延

| 名称          | Broker 地址               | TCP  | 平均时延 |
| :------------ | :------------------------ | :--- | :------- |
| EMQX         | `broker.emqx.io`          | 1883 | 212 ms   |
| EMQX（国内） | `broker-cn.emqx.io`       | 1883 | 52.6 ms  |
| Eclipse       | `mqtt.eclipseprojects.io` | 1883 | 261 ms   |
| Mosquitto     | `test.mosquitto.org`      | 1883 | 874 ms   |
| HiveMQ        | `broker.hivemq.com`       | 1883 | 574 ms   |

 

## 总结

在几项测试中各个免费在线 MQTT 服务器整体上均达到了可用的程度，但是细分到具体指标上各个服务器之间还是存在显著的差异。较低的速率限制、不稳定的网络延时，甚至有部分服务器疑似存在定时重启机制，这些稳定性和可用性层面的问题即使在简单测试和原型制作中也会给用户带来不好的体验。

以上内容也从一定程度佐证了物联网平台的相关性能受设备地理位置的影响程度。因此在海外与国内基于优质云服务商网络分别提供就近接入点的 EMQX 免费在线 MQTT 服务相比之下就具有了一定优势，各方面测试数据均较为领先。

我们也很高兴地看到越来越多来自全球各地的物联网设备接入到 EMQX 提供的在线 MQTT 服务器上，平均每秒就有数千条消息传递。`broker.emqx.io:1883` 也出现在 GitHub 的各类开源项目、示例代码（https://github.com/search?q=broker.emqx.io&type=Code ）中。国内的用户则可以选择专为国内优化部署的 `broker-cn.emqx.io` 节点。

EMQX 在线公共服务器在国内和海外的两个接入点服务均由 [EMQX Cloud](https://www.emqx.com/zh/cloud) 提供。EMQX Cloud 是 EMQ 提供的全托管云原生 MQTT 消息服务，支持商业级的可访问性和稳定性保障。对于商业用户来说，使用 EMQX Cloud 可零成本快速启动项目，以简单快速的方式实现 MQTT 设备接入。后期可随业务发展情况按需扩展，同时可在全球范围内就近创建接入点并享受 EMQ 专业团队提供的 7*24 技术支持保障。

无论是个人还是企业项目，EMQ 致力于为各类用户提供最合适的 MQTT 消息服务。在使用 EMQX 的过程中如有任何意见或问题，欢迎随时向我们的团队反馈。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
