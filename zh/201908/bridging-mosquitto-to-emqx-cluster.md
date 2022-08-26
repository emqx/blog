EMQX 可以被其他类型的 [MQTT 服务器](https://www.emqx.com/zh/products/emqx) 和 [MQTT 云服务](https://www.emqx.com/zh/cloud)桥接，实现跨平台的消息订阅和发送。本文我们以一个配置实例来说明如何桥接 Mosquitto MQTT 消息至 EMQX。

Mosquitto 是一个小型轻量的开源 MQTT 服务器，由 C/C++ 语言编写。Mosquitto 采用单核心单线程架构，支持部署在资源有限的嵌入式设备，接入少量 MQTT 设备终端，并实现了 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 和 3.1.1版本协议。

EMQX 与 Mosquitto 均完整支持了 [MQTT 协议](https://www.emqx.com/zh/mqtt) 特性，但 EMQX 支持更多通信协议以及私有协议接入。应用层的功能拓展方面，Mosquitto 缺乏开箱即用的如认证鉴权、规则引擎、数据持久化与高性能消息桥接（EMQX 企业版）等业务相关功能； 监控运维与可视化管理方面， EMQX 有完整的现有功能和拓展方案支持；基础功能上 Mosquitto 集群功能羸弱，官方和第三方实现的集群方案均难以支撑物联网大规模海量连接的性能需求。

因此 Mosquitto 并不适合用来做规模化服务的 MQTT 服务器，但由于其足够轻量精简，可以运行在任何低功率单片机包括嵌入式传感器、手机设备、嵌入式微处理器上，是物联网边缘消息接入较好的技术选型之一，结合其桥接功能可以实现消息的本地处理与云端透传。

除了 Mosquitto 外，另外一个开源产品一款超轻量级 MQTT 消息服务器 [NanoMQ](https://nanomq.io/zh) 同样适用于物联网边缘接入场景，我们将在后续的文章中带来 NanoMQ 桥接消息至 EMQX 的教程。

## 场景描述

假设我们有一个 EMQX 服务器集群 `emqx1`，和一台 Mosquitto 服务器，我们需要在 Mosquitto 上创建一条桥接，把所有传感器主题 `sensor/#` 消息转发至 `emqx1`  集群，并从 EMQX 订阅所有控制主题 `control/#`。

![Artboard.jpg](https://assets.emqx.com/images/f82cb9c8cc1d94b34d5d745ecc259cbd.jpg)

**EMQX**  

得益于 EMQX 标准的 MQTT 协议支持，Mosqutto 可以桥接至任意版本的 EMQX，此处使用 EMQX Cloud 提供的 [免费的在线 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 进行测试：

| 集群  | 集群地址       | 监听端口 |
| :---- | :------------- | :------- |
| emqx1 | broker.emqx.io | 1883     |

**Mosquitto**

本文使用的 Mosquitto 版本为 2.0.14，下载安装方式详见 [Mosquitto Download](https://mosquitto.org/download/)：

| 地址      | 监听端口 |
| :-------- | :------- |
| 127.0.0.1 | 1883     |

## 简单的 Mosquitto MQTT 桥接示例

配置 Mosquitto 的桥接需要在安装后修改 `mosquitto.conf` 文件，对于每一个桥接，需要配置的基本内容有：

- 远端的 EMQX 服务器的地址和端口
- MQTT 协议参数，如协议版本，keepalive, clean_session等（如不配置则使用默认值）
- EMQX 需要的客户端登录信息
- 需要桥接的消息的主题
- 配置桥接主题映射（默认无映射）

以下是最终的配置文件，下文会详细讲解每个部分配置的释义：

```
connection emqx1
address broker.emqx.io:1883
bridge_protocol_version mqttv50
remote_clientid emqx_c
remote_username emqx_u
remote_password public
topic sensor/# out 1
topic control/# in 1
```

#### 新建 MQTT 桥接

打开 `mosquitto.conf` 文件，在配置文件末尾增加一个 MQTT 桥接配置，使用 emqx1 作为 connection 名称：

```
connection emqx1
```

#### 配置桥接远端节点的地址和端口

```
address broker.emqx.io:1883
```

#### 配置 MQTT 协议版本

Mosquitto 桥接使用的 MQTT 协议版本默认为 3.1.1，EMQX 完整支持 MQTT 5.0 特性，此处使用 MQTT 5.0 版本进行桥接：

```
bridge_protocol_version mqttv50
```

#### 配置远端节点客户端 ID

```
remote_clientid emqx_c
```

#### 配置远端节点用户名  

```
remote_username emqx_u
```

#### 配置远端节点密码

```
remote_password public
```

#### 指定需要桥接的 MQTT 主题

桥接主题的配置格式为 `topic <topic> [[[out | in | both] qos-level] local-prefix remote-prefix]`，它定义了桥接转发和接收的规则，其中：

- `<topic>`指定了需要桥接的主题，支持通配符
- 方向可以是 out, in 或者 both
  - out: 将本地主题数据发送到远端 Broker
  - in: 订阅远端 Broker 的主题，将数据发布到本地
  - both: 在同一个主题上进行双向桥接

- `qos-level `为桥接的 QoS 级别， 如不指定则使用被转发消息原 QoS
- `local-prefix`  与 `remote-prefix` 对应本地和远程前缀，用于主题映射时在转发和接收的消息主题上加上相应前缀，以便应用可以识别消息来源。

对应本文场景可以添加以下两条桥接规则：

```
topic sensor/# out 1
topic control/# in 1
```

在配置完成后，需要重新启动 Mosquitto 使 MQTT 桥接配置生效。



## 配置 EMQX 服务器

使用公共服务器时不需要配置任何参数。实际应用中，为了使 Mosquitto MQTT 消息桥接成功，需要视用户 EMQX 的安全配置情况决定是否配置相应的客户端[认证](https://www.emqx.io/docs/zh/v5.0/security/authn/authn.html)和[授权](https://www.emqx.io/docs/zh/v5.0/security/authz/authz.html)信息。

## 测试配置

我们可以使用 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)来测试 MQTT 桥接的配置是否成功，此处使用的是 [MQTT X CLI](https://mqttx.app/cli)，一款由 EMQ 开发的强大而易用的 MQTT 5.0 命令行工具。

### 测试桥接的 out 方向

在远程 EMQX 上订阅 `sensor/#`主题，等待接收 Mosquitto 桥接上报的数据：

```
mqttx sub -t "sensor/#" -h broker.emqx.io
```

在本地 Mosquitto 的 `sensor/1/temperature` 主题上发布消息，该消息将在 Mosquitto 中发布，同时桥接至远程 EMQX：

```
mqttx pub -t "sensor/1/temperature" -m "37.5" -q 1
```

此时人称 EMQX 应当能收到 Mosqutto 桥接上报的消息：

```
payload:  37.5
```

### 测试桥接的 in 方向

在本地 Mosquitto上订阅 `control/#` 主题，该主题将接收到远程 EMQX 上发布的消息：

```
mqttx sub -t "control/#"
```

在远程 EMQX 的 `control/t/1` 主题上发布消息，消息将在 EMQX 集群中传递，同时桥接到 Mosquitto 本地：

```
mqttx pub -t "control/t/1" -m "I'm EMQX" -h broker.emqx.io
```

此时在 Mosquitto上应能收到该消息：

```
payload:  I'm EMQX
```

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
