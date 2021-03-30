随着 5G 时代的来临，万物互联的伟大构想正在成为现实。联网的 **物联网设备** 在 2018 年已经达到了 70 亿[^1]，在未来两年，仅智能水电气表就将超过10亿[^2]。

![Numberofglobaldeviceconnections20152025NumberofIoTDevices.png](https://static.emqx.net/images/1abe97466e35ce3fd89417f6ea2fec86.png)

海量的设备接入和设备管理对网络带宽、通信协议以及平台服务架构都带来了很大挑战。对于 **物联网协议** 来说，必须针对性地解决物联网设备通信的几个关键问题：其网络环境复杂而不可靠、其内存和闪存容量小、其处理器能力有限。

[MQTT 协议](https://www.emqx.io/cn/mqtt) 是基于发布/订阅模式的物联网通信协议，凭借简单易实现、支持 QoS、报文小等特点，占据了物联网协议的半壁江山：

![WechatIMG10934.png](https://static.emqx.net/images/c980ab99489d1e771ad7b4dc5ac722b9.png)

## MQTT 协议的诞生

MQTT was created by [Andy Stanford-Clark](http://en.wikipedia.org/wiki/Andy_Stanford-Clark) of IBM, and Arlen Nipper (then of Arcom Systems, later CTO of Eurotech).[^3]

据 Arlen Nipper 在一 [IBM Podcast 上的自述](https://www.ibm.com/podcasts/software/websphere/connectivity/piper_diaz_nipper_mq_tt_11182011.pdf)，MQTT 原名是 `MQ TT`， 注意 `MQ` 与 `TT `之间的空格，其全称为: MQ Telemetry Transport，是九十年代早期，他在参与 Conoco Phillips 公司的一个原油管道数据采集监控系统(pipeline SCADA system)时，开发的一个实时数据传输协议。它的目的在于让传感器通过带宽有限的 [VSAT](https://en.wikipedia.org/wiki/Very-small-aperture_terminal) ，与 IBM 的 MQ Integrator 通信。由于 Nipper 是遥感和数据采集监控专业出身，所以按业内惯例给了个 `MQ TT` 的名字。

## MQTT 协议设计原则

按照 Nipper 的介绍，MQTT 必须简单容易实现，必须支持 QoS(设备网络环境复杂)，必须轻量且省带宽(因为那时候带宽很贵)，必须数据无关(不关心 Payload 数据格式)，必须有持续地会话感知能力(时刻知道设备是否在线)。下面将介绍 MQTT (3.1.1 版本) 的几个核心特色，分别对应了这几个设计原则的实现。

### 灵活的发布订阅和主题设计

发布订阅模式是传统 Client/Server 模式的一种解耦方案。发布者通过 Broker 与消费者之间通信，Broker 的作用是将收到的消息通过某种`过滤规则`，正确地发送给消费者。发布/订阅模式 相对于 客户端/服务器模式 的好处在于：

- 发布者和消费者之间不必预先知道对方的存在，比如不需要预先沟通对方的 IP Address 和 Port
- 发布者和消费者之间不必同时运行。因为 Broker 是一直运行的。

在 MQTT 协议里，上面提到的 `过滤规则` 是 `Topic`。比如：所有发布到 `news` 这个 Topic 的消息，都会被 Broker 转发给已经订阅了 `news` 的订阅者:


![image.png](https://static.emqx.net/images/a97a07cccc199f387b7eb6747eb2223f.png)



上图中订阅者预先订阅了 `news`，然后发布者向 Broker 发布了一条消息 "some msg" 并指定发布到 `news` 主题，Broker 通过 Topic 匹配，决定将这条消息转发给订阅者。

MQTT 的 Topic 有层级结构，并且支持通配符 `+` 和 `#`:

- `+` 是匹配单层的通配符。比如 `news/+` 可以匹配 `news/sports`，`news/+/basketball` 可匹配到 `news/sports/basketball`。
- `#` 是一到多层的通配符。比如 `news/#` 可以匹配 `news`、 `news/sports`、`news/sports/basketball` 以及 `news/sports/basketball/x` 等等。

MQTT 的主题是不要预先创建的，发布者发送消息到某个主题、或者订阅者订阅某个主题的时候，Broker 就会自动创建这个主题。

### 带宽消耗最小化

MQTT 协议将协议本身占用的额外消耗最小化，消息头部最小只需要占用 2 个字节。

MQTT 的消息格式分三部分：

| 固定长度头部，2 个字节，所有消息类型里都有 |
| ------------------------------------------ |
| 可变长度头部，只有某些消息类型里有         |
| Payload，只有某些消息类型里有              |

MQTT 的主要消息类型有：

- CONNECT / CONNACK
- PUBLISH / PUBACK
- SUBSCRIBE / SUBACK
- UNSUBSCRIBE / UNSUBACK
- PINGREQ / PINGRESP
- DISCONNECT

其中 PINGREQ / PINGRESP 和 DISCONNECT 报文是不需要可变头部的，也没有 Payload，也就是说它们的报文大小仅仅消耗 2 个字节。

在 CONNECT 报文的可变长度头部里，有个 Protocol Version 的字段。为了节省空间，只有一个字节。所以版本号不是按照字符串 "3.1.1" 存放的，而是使用数字 4 来表示 3.1.1 版本。

### 三个可选的 QoS 等级

为适应设备不同的网络环境，MQTT 设计了 3 个 QoS 等级，0, 1, 2:

- *At most once* (0)
- *At least once* (1)
- *Exactly once* (2)

QoS 0 是一种 "fire and forget" 的消息发送模式：Sender (可能是 Publisher 或者 Broker) 发送一条消息之后，就不再关心它有没有发送到对方，也不设置任何重发机制。

QoS 1 包含了简单的重发机制，Sender 发送消息之后等待接收者的 ACK，如果没收到 ACK 则重新发送消息。这种模式能保证消息至少能到达一次，但无法保证消息重复。

QoS 2 设计了[略微复杂](https://docs.emqx.io/broker/v3/en/protocol.html#qos2-message-publish-and-subscribe)的重发和重复消息发现机制，保证消息到达对方并且严格只到达一次。

### 会话保持

MQTT 没有假设设备或 Broker 使用了 TCP 的保活机制[^4]，而是设计了协议层的保活机制：在 CONNECT 报文里可设置 Keepalive 字段，来设置保活心跳包 PINGREQ/PINGRESP 的发送时间间隔。当长时间无法收到设备的 PINGREQ 的时候，Broker 就会认为设备已经下线。

总的来说，Keepalive 有两个作用：

- 发现对端死亡或者网络中断
- 在长时间无消息交互的情况下，保持连接不被网络设备断开

对于那些想要在重新上线后，重新收到离线期间错过的消息的设备，MQTT 设计了持久化连接：在 CONNECT 报文里可设置 CleanSession 字段为 False，则 Broker 会为终端存储：

- 设备所有的订阅
- 还未被设备确认的 QoS1 和 QoS 消息
- 设备离线时错过的消息

### 在线状态感知

MQTT 设计了遗愿(Last Will) 消息，让 Broker 在发现设备异常下线的情况下，帮助设备发布一条遗愿消息到指定的主题。

实际上在某些 [MQTT 服务器](https://www.emqx.io/cn/products/broker)的实现里 (比如 EMQ X)，设备上线或下线的时候 Broker 会通过某些系统主题发布设备状态更新，更符合实际应用场景。

## 开源 MQTT 服务器如何选择

到目前为止，比较流行的开源 MQTT 服务器有几个：

1. [Eclipse Mosquitto](https://github.com/eclipse/mosquitto)

   使用 C 语言实现的 MQTT 服务器。Eclipse 组织还还包含了大量的 MQTT 客户端项目：https://www.eclipse.org/paho/#

2. [EMQ X](https://github.com/emqx/emqx)

   使用 Erlang 语言开发的 MQTT 服务器，内置强大的规则引擎，支持许多其他 IoT 协议比如 MQTT-SN、 CoAP、LwM2M 等。

3. [Mosca]( https://github.com/mcollina/mosca)

   使用 Node.JS 开发的 MQTT 服务器，简单易用。

4. [VerneMQ]( https://github.com/vernemq/vernemq)

   同样使用 Erlang 开发的 MQTT 服务器.

从支持 [MQTT 5.0](https://www.emqx.io/cn/mqtt/mqtt5)、稳定性、扩展性、集群能力等方面考虑，[EMQ X](https://www.emqx.io/cn/products/broker) 的表现应该是最好的：

- 使用 Erlang OTP 开发，容错能力好 (电信领域久经考验的语言，曾经做出过 99.9999999% 可用性的交换机设备[^5])
- 官方有大量的扩展插件可供扩展。有很多认证插件，数据存储(backend)插件可供选择。可支持各种关系型数据库，NoSQL 数据库，以及常见消息队列如 Kafka，RabbitMQ，Pulsar 等
- 支持集群，支持节点水平扩展
- 单节点支持 2000K 并发连接
- 支持规则引擎和编解码

## MQTT 协议快速体验

### MQTT 在线服务器

EMQ X [MQTT 物联网云服务](https://cloud.emqx.io/cn/) 提供了一个在线的公共 MQTT 5.0 服务器，不需要任何安装您就可以快速开始 MQTT 协议的学习、测试或原型制作。

该 MQTT 服务器的详细接入信息请见 EMQ 官网页面：[免费的在线 MQTT 服务器](https://www.emqx.io/cn/mqtt/public-mqtt5-broker)。

### MQTT 在线客户端

EMQ 也提供了支持浏览器访问的 [MQTT 在线客户端工具](https://www.emqx.io/cn/mqtt/mqtt-websocket-toolkit)，该工具支持通过普通或者加密的 WebSocket 端口连接至 MQTT 服务器，同时也支持缓存连接方便下次访问使用。



[^1]: The number of connected devices that are in use worldwide now exceeds 17 billion, with the number of IoT devices at 7 billion... https://iot-analytics.com/state-of-the-iot-update-q1-q2-2018-number-of-iot-devices-now-7b/
[^2]: The estimated installed base of smart meters (electricity, gas and water) is expected to surpass the 1 billion mark within the next 2 years. https://iot-analytics.com/smart-meter-market-2019-global-penetration-reached-14-percent/
[^3]: https://github.com/mqtt/mqtt.github.io/wiki/history
[^4]: https://www.cnblogs.com/softidea/p/5764051.html
[^5]: https://pragprog.com/articles/erlang

