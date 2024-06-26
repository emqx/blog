## Mosquitto 简介

[Mosquitto](https://www.emqx.com/zh/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives) 是一个小型轻量的[开源 MQTT 服务器](https://www.emqx.com/zh/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)，由 C/C++ 语言编写，采用单核心单线程架构，支持部署在资源有限的嵌入式设备，接入少量 MQTT 设备终端。同时，Mosquitto 完整支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 和 3.1.1 版本协议特性。

然而，Mosquitto 集群功能羸弱，官方和第三方实现的集群方案均难以支撑物联网大规模海量连接的性能需求。这导致其具有以下局限性：

- **可扩展性一般**：轻量级的架构带来了易于部署的优点，但同样也限制了其集群扩展性，难以应对业务的横向伸缩和扩张。
- **性能受限：** Mosquitto 在单个实例上连接的最大客户端数量也会影响其性能。在大规模或者高并发的场景下 Mosquitto 表现不佳。

因此 Mosquitto 并不适合用来做规模化服务的 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。但由于其足够轻量精简，可以运行在任何低功率单片机包括嵌入式传感器、手机设备、嵌入式微处理器上，因此在需要接入设备不多、设备性能受限等边缘场景下，Mosquitto 非常适合作为边缘端 MQTT Broker 部署：

- **易部署：**作为一个轻量级 MQTT Broker，Mosquitto 的部署和配置相对简单，可以快速在边缘设备上运行起来。
- **适应性：**Mosquitto 可以灵活适应工业环境、智能家居、农业物联网等各种不同的边缘场景需求，提供可靠的 MQTT 通信服务。
- **本地控制和决策**：某些边缘设备可能需要进行低延迟、高带宽的实时控制和决策，而不能依赖云端的消息反馈。Mosquitto 可以作为边缘设备上的 MQTT Broker ，负责处理本地控制指令和决策，以保证设备的实时响应能力。
- **局域网通信**：在某些场景下，边缘设备之间需要进行局域网通信，但这些数据中的大部分并不需要传输至云端。Mosquitto 可以作为局域网中的 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) ，负责管理设备之间的通信，实现设备之间的数据交换和协作，并通过 Mosquitto Bridge 代替边缘设备与云端进行必要的消息交互。

## Mosquitto Bridge 简介

Mosquitto 提供了 MQTT 消息的桥接功能，称为 **Mosquitto Bridge** 。它允许将一个 MQTT Broker 连接到另一个 MQTT Broker ，从而实现消息的桥接和转发。这样可以实现跨网络或者跨地域的消息传递，满足多种不同场景的需求。此外，Mosquitto Bridge 还能够解决大规模或高并发场景下的困境：在 Mosquitto Broker 之间仅将少量且必要的消息通过 MQTT Bridge 传输，从而降低性能压力，减轻复杂度。

- **跨网络通信：**在企业或者组织内部，可能会部署多个 MQTT Broker ，处于不同的网络环境中。使用 Mosquitto Bridge 可以实现这些代理之间的消息传递和通信，使得各个部门或者业务之间可以进行跨网络的通信和协作。
- **边缘到云端通信：**在物联网领域，通常会涉及到边缘设备与云端之间的通信。使用 Mosquitto Bridge 可以将边缘端的 MQTT Broker 与云端的 MQTT Broker 进行连接，实现边缘设备数据传输到云端进行处理。

本文将介绍如何使用 Mosquitto Bridge 与云端 MQTT 集群连接，实现边缘 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)与云端 MQTT Broker 的交互。我们将采用大规模分布式 MQTT 消息服务器 EMQX 作为云端的 MQTT Broker 。EMQX 可以高效可靠连接海量物联网设备，实时处理分发消息与事件流数据。EMQX 节点可以被其他类型的 MQTT 服务器和 [MQTT 云服务](https://www.emqx.com/zh/cloud)桥接，实现跨平台的消息订阅和发送。

## **Mosquitto Bridge 应用场景示例**

假设一个大型工厂内部部署了大量的传感器和执行器设备，用于监测生产过程、控制设备运行等。这些设备之间需要进行实时通信和协作，以确保生产过程的顺利进行。同时，工厂管理人员希望能够实时监控工厂运行状态，并对设备进行远程控制和管理。

在这种情况下，可以将 Mosquitto 部署在工厂内部的局域网中作为边缘 MQTT Broker 。各个设备可以连接到 Mosquitto，并通过 MQTT 协议进行实时通信。Mosquitto 负责管理设备之间的消息传递，以及与云端的连接。工厂内部设备之间可以通过 Mosquitto 进行快速可靠地消息交互，无需经过云端，从而降低延迟并提高实时性。同时，管理人员也可以通过 Mosquitto 发布订阅机制实时监控设备状态，并通过 Mosquitto 发布指令控制设备运行。

然而，在某些情况下，管理人员可能需要从云端获取特定的数据或者下发特定的指令，例如远程监控工厂运行状态或者调整设备参数。此时可以通过 Mosquitto bridge 将局域网内的消息桥接到云端的 MQTT Broker ，实现与云端的通信。

假设我们有一个 EMQX 服务器集群作为云端控制平台，和一台 Mosquitto 服务器作为边缘 MQTT 消息代理。我们需要在 Mosquitto 上创建一条桥接，将所有传感器上报的数据传输给云端控制平台 EMQX，并将云端控制平台下发的控制指令转发给边缘端的传感器设备。

- 传感器发布 `sensor/#` 主题的消息进行数据上报。
- 传感器订阅 `control/#` 主题以接受控制消息。

![Mosquitto Bridge 应用场景](https://assets.emqx.com/images/4f61e0ec7d88e0b27de29b4290b9af04.png)

**云端控制平台 EMQX**

得益于 EMQX 标准的 MQTT 协议支持，Mosqutto 可以桥接至任意版本的 EMQX，此处使用 EMQX Cloud 提供的 [免费的在线 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 进行测试：

| 集群地址         | 监听端口 |
| :--------------- | :------- |
| `broker.emqx.io` | 1883     |

**边缘 MQTT 消息代理 Mosquitto**

使用本地运行的 Mosquitto 作为边缘 broker 示例。版本为 `2.0.18`
下载安装方式详见 [Mosquitto Download](https://mosquitto.org/download/)：

| 地址      | 监听端口 |
| :-------- | :------- |
| 127.0.0.1 | 1883     |

## Mosquitto MQTT 桥接教程

### 配置 Mosquitto

配置 Mosquitto 的桥接需要在安装后修改 `mosquitto.conf` 文件或在启动 Mosquitto 时通过路径指定配置文件。更多信息请参考 [mosquitto.conf(5)](https://mosquitto.org/man/mosquitto-conf-5.html) 

对于 Mosquitto Bridge 来说，每一个桥接需要配置的基本内容有：

- 远端的 EMQX 服务器的地址和端口
- MQTT 协议参数，如协议版本、keepalive、clean_session 等（如不配置则使用默认值）
- EMQX 需要的客户端登录信息
- 需要桥接的消息的主题
- 配置桥接主题映射（默认无映射）

以下是桥接部分的配置项目，下文会详细讲解每个部分配置的释义：

```
connection emqx1
address broker.emqx.io:1883
bridge_protocol_version mqttv50
remote_clientid emqx_c_5f9072a9
remote_username emqx_u_5f9072a9
remote_password public
topic sensor/# out 1  sen-local/ sen-remote/
topic control/# in 1 cmd-local/ cmd-remote/
```

#### 新建 MQTT 桥接

打开 `mosquitto.conf` 文件，在配置文件末尾增加一个 MQTT 桥接配置，使用 emqx1 作为 connection 名称：

```
connection emqx1
```

#### 配置桥接远端节点的地址和端口

远端 MQTT Broker 的地址配置格式为 `host[:port]`，当 `[:port]` 未指定时默认为 MQTT TCP 1883 端口。

```
address broker.emqx.io:1883
```

#### 配置 MQTT 协议版本

Mosquitto 桥接使用的 MQTT 协议版本默认为 3.1.1，EMQX 完整支持 MQTT 5.0 特性，此处使用 MQTT 5.0 版本进行桥接：

```
bridge_protocol_version mqttv50
```

#### 配置远端节点客户端 ID

此处加入随机字符串作为后缀以避免与其他客户端重复。

```
remote_clientid emqx_c_5f9072a9
```

#### 配置远端节点用户名

```
remote_username emqx_u_5f9072a9
```

#### 配置远端节点密码

```
remote_password public
```

#### 指定需要桥接的 MQTT 主题

桥接主题的配置格式为 `topic <topic> [[[out | in | both] qos-level] local-prefix remote-prefix]`，它定义了桥接转发和接收的规则，其中：

- `<topic>`指定了需要桥接的主题，支持通配符
- 方向可以是 out、in 或者 both
  - out: 将本地主题数据发送到远端 Broker
  - in: 订阅远端 Broker 的主题，将数据发布到本地
  - both: 在同一个主题上进行双向桥接
- `qos-level`为桥接的 QoS 级别，如不指定则使用被转发消息原 QoS
- `local-prefix` 与 `remote-prefix` 对应本地和远程前缀，用于主题映射时在转发和接收的消息主题上加上相应前缀，以便应用可以识别消息来源。

对应本文场景可以添加以下两条桥接规则：

> 注意：使用 local-prefix 及 remote-prefix 以避免接收到公共服务器上的其他用户发布的消息。
> 此外 mosquitto 将会使用字符串拼接的方式对主题进行更改，所以建议对 prefix 加入主题分隔符以区分主题层级。

```
topic sensor/# out 1  sen-local/ sen-remote/
topic control/# in 1 cmd-local/ cmd-remote/
```

在配置完成后，启动 Mosquitto 并使用 `-c` 选项使用特定的配置文件以使 MQTT 桥接配置生效。

```shell
$ mosquitto -c mosquitto.conf
1711697768: mosquitto version 2.0.18 starting
1711697768: Config loaded from mosquitto.conf.
1711697768: Starting in local only mode. Connections will only be possible from clients running on this machine.
1711697768: Create a configuration file which defines a listener to allow remote access.
1711697768: For more details see https://mosquitto.org/documentation/authentication-methods/
1711697768: Opening ipv4 listen socket on port 1883.
1711697768: Opening ipv6 listen socket on port 1883.
1711697768: Connecting bridge emqx_brokre (broker.emqx.io:1883)
1711697768: mosquitto version 2.0.18 running
...
```

### 配置 EMQX 服务器

使用公共服务器时不需要配置任何参数。实际应用中，为了使 Mosquitto MQTT 消息桥接成功，需要视用户 EMQX 的安全配置情况决定是否配置相应的客户端[认证](https://docs.emqx.com/zh/emqx/v5.0/security/authn/authn.html)和[授权](https://docs.emqx.com/zh/emqx/v5.0/security/authz/authz.html)信息。

### 测试配置

我们可以使用 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)来测试 MQTT 桥接的配置是否成功，此处使用的是 [MQTTX CLI](https://mqttx.app/zh/cli)，一款由 EMQ 开发的强大而易用的 MQTT 命令行工具。

#### 测试桥接的 out 方向

两个 MQTT 客户端，分别连接本地(`127.0.0.1:1883`)的 Mosquitto 服务，和云端(`broker.emqx.io:1883`)的 EMQX 集群。

客户端 `suber` 在远程 EMQX 上订阅 `sen-remote/sensor/#`主题，等待接收 Mosquitto 桥接上报的数据：

```shell
$ mqttx-cli sub -u 'suber' -t 'sen-remote/sensor/#' -h broker.emqx.io -p 1883  
[3/29/2024] [5:02:30 PM] › …  Connecting...
[3/29/2024] [5:02:34 PM] › ✔  Connected
[3/29/2024] [5:02:34 PM] › …  Subscribing to sen-remote/sensor/#...
[3/29/2024] [5:02:34 PM] › ✔  Subscribed to sen-remote/sensor/#
...
```

另一个连接至本地 Mosquitto 的客户端在 `sen-local/sensor/temperature` 主题上发布消息，该消息将在 Mosquitto 中发布，同时桥接至远程 EMQX：

```shell
$ mqttx-cli pub -t "sen-local/sensor/temperature" -m '{"temperature": 36.8}' -q 1 -h 127.0.0.1 -p 1883
[3/29/2024] [5:03:09 PM] › …  Connecting...
[3/29/2024] [5:03:09 PM] › ✔  Connected
[3/29/2024] [5:03:09 PM] › …  Message publishing...
[3/29/2024] [5:03:09 PM] › ✔  Message published
```

此时连接至云端 EMQX 的客户端应当能收到 Mosqutto 桥接上报的消息：

```shell
... [3/29/2024] [5:03:09 PM] › payload: {"temperature": 36.8}
```

#### 测试桥接的 in 方向

在本地 Mosquitto上订阅 `cmd-local/control/#` 主题，该主题将接收到远程 EMQX 上发布的消息：

```shell
$ mqttx-cli sub -u 'suber' -t 'cmd-local/control/#' -h 127.0.0.1 -p 1883
[3/29/2024] [5:03:43 PM] › …  Connecting...
[3/29/2024] [5:03:43 PM] › ✔  Connected
[3/29/2024] [5:03:43 PM] › …  Subscribing to cmd-local/control/#...
[3/29/2024] [5:03:43 PM] › ✔  Subscribed to cmd-local/control/#
...
```

在远程 EMQX 的 `cmd-remote/control/cmd` 主题上发布消息，消息将在 EMQX 集群中传递，同时桥接到 Mosquitto 本地：

```shell
$ mqttx-cli pub -t "cmd-remote/control/cmd" -m '{"cmd": "refresh"}' -q 1 -h broker.emqx.io -p 1883
[3/29/2024] [5:03:45 PM] › …  Connecting...
[3/29/2024] [5:03:45 PM] › ✔  Connected
[3/29/2024] [5:03:45 PM] › …  Message publishing...
[3/29/2024] [5:03:46 PM] › ✔  Message published
```

此时连接至本地 Mosquitto 服务的客户端 `suber` 应能收到该消息：

```shell
... [3/29/2024] [5:03:46 PM] › payload: {"cmd": "refresh"}
```

## **结语**

本文介绍了如何使用 Mosquitto Bridge 将边缘端 MQTT 消息桥接至云端的 MQTT Broker 集群。通过将 Mosquitto Bridge 与 EMQX 相结合，用户不仅可以实现边缘 MQTT 服务器与云端的消息通信，还可以获得 EMQX 提供的规则引擎、数据持久化、大文件传输、[MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 等能力，为物联网应用的开发带来更多便利与创新。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
