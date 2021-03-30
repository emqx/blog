EMQ X 节点可以被其他类型的 [MQTT 服务器](https://www.emqx.io/cn/products/broker) 桥接，实现跨平台的消息订阅和发送。本文我们以一个配置实例来说明如何桥接 Mosquitto MQTT  消息至 EMQ X。

Mosquitto 是一个小型轻量的开源 MQTT 服务器，由 C/C++ 语言编写。Mosquitto 采用单核心单线程架构，支持部署在资源有限的嵌入式设备，接入少量 MQTT 设备终端，并实现了 [MQTT 5.0](https://www.emqx.io/cn/mqtt/mqtt5) 和 3.1.1版本协议。

EMQ X 与 Mosquitto 均完整支持了 [MQTT 协议](https://www.emqx.io/cn/mqtt) 特性，但 EMQ X 支持更多通信协议以及私有协议接入。应用层的功能拓展方面，Mosquitto 缺乏开箱即用的如认证鉴权、规则引擎、数据持久化与高性能消息桥接（EMQ X 企业版）等业务相关功能； 监控运维与可视化管理方面， EMQ X 有完整的现有功能和拓展方案支持；基础功能上 Mosquitto 集群功能羸弱，官方和第三方实现的集群方案均难以支撑物联网大规模海量连接的性能需求。

因此 Mosquitto 并不适合用来做规模化服务的 MQTT 服务器，但由于其足够轻量精简，可以运行在任何低功率单片机包括嵌入式传感器、手机设备、嵌入式微处理器上，是物联网边缘消息接入较好的技术选型，结合其桥接功能可以实现消息的本地处理与云端透传。

## 场景描述

假设我们有一个 EMQ X 服务器集群 `emqx1`，和一台 Mosquitto 服务器，我们需要在 Mosquitto 上创建一条桥接，把所有 `传感器(sensor)` 主题消息转发至 `emqx1`  集群，并从 EMQ X 订阅所有`控制(control)`主题。

![Artboard.jpg](https://static.emqx.net/images/f82cb9c8cc1d94b34d5d745ecc259cbd.jpg)

**EMQ X**  

| 集群  | 集群地址      | 监听端口 |
| :---- | :------------ | :------- |
| emqx1 | 192.168.1.100 | 1883     |

**Mosquitto**

| 地址          | 监听端口 |
| :------------ | :------- |
| 192.168.1.101 | 1883     |

## 简单的 Mosquitto MQTT 桥接示例

配置 Mosquitto 的桥接需要在安装后修改 `mosquitto.conf` 文件。对于每一个桥接，需要配置的基本内容有：

- 远端的 EMQ X 服务器的地址和端口；
- MQTT 协议参数，如协议版本，keepalive, clean_session等（如不配置则使用默认值）；
- EMQ X 需要的客户端登录信息；
- 需要桥接的消息的主题；
- 配置桥接主题映射（默认无映射）。

#### 新建 MQTT 桥接

打开 `mosquitto.conf` 文件，增加一个 `connection` 以建立一个新的桥接，`connection` 关键字后的字符串同时也是远端节点上使用的client id：

```
connection emqx1
```

#### 配置桥接远端节点的地址和端口

```
address 192.168.1.100:1883
```

#### 配置 MQTT 协议版本

Mosquitto 桥接使用的 MQTT 协议版本默认为3.1，要使用3.1.1协议需要在配置中指定。

```
bridge_protocol_version mqttv311
```

#### 配置远端节点用户名  

```
remote_username user
```

#### 配置远端节点密码

```
remote_password passwd
```

#### 指定需要桥接的 MQTT 主题

桥接主题的配置格式为 `topic 主题模式 方向 QoS 本地前缀 远端前缀`，它定义了桥接转发和接收的规则。其中：

- 主题模式指定了需要桥接的主题，支持通配符;
- 方向可以是 in, out 或者 both
- QoS 为桥接的QoS级别， 如不指定则使用被转发消息原QoS
- 本地和远程前缀用于主题映射，在转发和接收的消息主题上加上相应前缀，以便应用可以识别消息来源。

以下配置例添加了两条桥接规则：

```
topic sensor/# out 1
topic control/# in 1
```

在配置完成后，需要重新启动 Mosquitto 使 MQTT 桥接配置生效。



## 配置 EMQ X 服务器

在安装 EMQ X 服务器后，为了使 Mosquitto MQTT 消息桥接成功，需要视情况决定是否配置相应的用户认证和鉴权信息。或者在实验阶段为了简化测试，可以使用允许匿名登录和 acl_nomatch 跳过认证和鉴权。

## 测试配置

我们使用 `mosquitto_sub` 和 `mosquitto_pub` 工具来测试 MQTT 桥接的配置是否成功。

### 测试桥接的 out 方向

在'emqx1'上订阅订阅'sensor/#'主题，该主题将接收到 Mosquitto 上报的数据：

```
$ mosquitto_sub -t "sensor/#" -p 1883 -d -q 1 -h 192.168.1.100

Client mosqsub|19324-Zeus- sending CONNECT
Client mosqsub|19324-Zeus- received CONNACK
Client mosqsub|19324-Zeus- sending SUBSCRIBE (Mid: 1, Topic: sensor/#, QoS: 1)
Client mosqsub|19324-Zeus- received SUBACK
Subscribed (mid: 1): 1
```

在Mosquitto上发布消息：

```
mosquitto_pub -t "sensor/1/temperature" -m "37.5" -d -h 192.168.1.101 -q 1
Client mosqpub|19325-Zeus- sending CONNECT
Client mosqpub|19325-Zeus- received CONNACK
Client mosqpub|19325-Zeus- sending PUBLISH (d0, q1, r0, m1, 'sensor/1/temperature', ... (4 bytes))
Client mosqpub|19325-Zeus- received PUBACK (Mid: 1)
Client mosqpub|19325-Zeus- sending DISCONNECT
```

在'emqx1'上应能收到该消息：

```
Client mosqsub|19324-Zeus- received PUBLISH (d0, q1, r0, m1, 'sensor/1/temperature', ... (4 bytes))
Client mosqsub|19324-Zeus- sending PUBACK (Mid: 1)
37.5
```



### 测试桥接的 in 方向

在 Mosquitto上订阅 'control/#' 主题，该主题将接收到 EMQ X 上发布的消息：

```
$ mosquitto_sub -t "control/#" -p 1883 -d -q 1 -h 192.168.1.101
Client mosqsub|19338-Zeus- sending CONNECT
Client mosqsub|19338-Zeus- received CONNACK
Client mosqsub|19338-Zeus- sending SUBSCRIBE (Mid: 1, Topic: control/#, QoS: 1)
Client mosqsub|19338-Zeus- received SUBACK
Subscribed (mid: 1): 1
```

在 'emqx1'上发布消息，消息将在 'emqx1' 集群中传递，同时桥接到 Mosquitto 本地：

```
$ mosquitto_pub -t "control/1" -m "list_all" -d -h 192.168.1.100 -q 1
Client mosqpub|19343-Zeus- sending CONNECT
Client mosqpub|19343-Zeus- received CONNACK
Client mosqpub|19343-Zeus- sending PUBLISH (d0, q1, r0, m1, 'control/1', ... (8 bytes))
Client mosqpub|19343-Zeus- received PUBACK (Mid: 1)
Client mosqpub|19343-Zeus- sending DISCONNECT
```

在 Mosquitto上应能收到该消息：

```
Client mosqsub|19338-Zeus- received PUBLISH (d0, q1, r0, m2, 'control/1', ... (8 bytes))
Client mosqsub|19338-Zeus- sending PUBACK (Mid: 2)
list_all
```