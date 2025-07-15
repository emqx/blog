在当今高度互联的数字化世界中，实时数据流的复杂性日益增长，尤其是在物联网（IoT）和微服务架构领域。企业和开发者面临着一个普遍的挑战：各种数据协议和系统往往各自为政，形成难以逾越的“数据孤岛”。这种碎片化的局面不仅增加了开发和维护的巨大开销，还阻碍了对数据潜力的全面发掘和利用，导致关键业务洞察和实时决策的缺失。

作为服务于物联网实时智能的统一 MQ + AI 平台，EMQX 致力于提供高效可靠的物联网连接。自 5.0 版本起，EMQX 便引入了强大的协议网关特性，旨在打破传统 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)的边界，使其能够接收来自其他非 MQTT 协议的客户端连接。这一创新为 EMQX 赋予了卓越的多协议接入能力，使其成为一个真正意义上的统一消息平台，能够无缝集成各种异构系统和设备 。  

![image.png](https://assets.emqx.com/images/fe9cc883cb77c71da319e2da399ec636.png)

随着最新版本 EMQX 5.10.0 的发布，EMQX 协议网关家族又迎来了一位新成员：**EMQX NATS Gateway**。这项新功能进一步扩展了 EMQX 的连接边界，实现了 MQTT 与 NATS 协议之间的原生、双向互通，为构建更灵活、更强大的实时数据基础设施提供了前所未有的可能性 。  

## 什么是 NATS 协议

[NATS（Neural Autonomic Transport System）](https://nats.io/)是一个高性能、轻量级、云原生的消息系统，专为现代分布式应用设计。它以其简洁、高效的特点而闻名，支持发布-订阅（Publish-Subscribe）、请求-响应（Request-Reply）等多种消息模式，并提供了丰富的客户端库，覆盖多种编程语言 。  

**NATS 的核心特点包括：**

- **高性能与低延迟：** NATS 采用轻量级协议和优化的路由机制，确保消息以极高的吞吐量和低延迟进行传输。Core NATS 提供“至多一次”（At-most-once）的消息传递语义，适用于对速度和可用性要求极高的场景 。  
- **云原生设计：** NATS 从设计之初就考虑了云环境的特性，易于部署在裸机、虚拟机、容器或 Kubernetes 等任何环境中，并支持集群化部署以实现高可用性和可扩展性 。  
- **简洁性：** NATS 协议简单，客户端库易于使用，降低了开发和运维的复杂性 。  
- **主题寻址：** NATS 基于主题（Subject）进行消息路由，并支持单层和多层的主题通配符，这使得 M:N（多对多）通信变得轻松。

|                | **MQTT**                                                     | **NATS**                                                     |
| :------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **传输层**     | TCP/TLSWebsocket/Websocket over SSL                          | TCP/TLSWebsocket/Websocket over SSL                          |
| **报文格式**   | 二进制形式，报文紧凑且字段丰富                               | 使用 PlainText，但语义非常精简                               |
| **客户端连接** | 支持持久会话 (Clean Session)，可断线重连保持会话状态和未送达消息 | 无持久化 Session 概念                                        |
| **消息模式**   | 发布/订阅 (Publish/Subscribe)                                | 发布/订阅 (Publish/Subscribe)<br>请求/回复 (Request/Reply)<br>队列 (Queueing) |
| **主题**       | **分层主题 (Topic)**，使用 `/` 进行层级划分，支持通配符 (`+`, `#`) | **扁平化 Subject**，使用 `.` 进行分隔，同样支持通配符 (`*`, `>`) |
| **消息质量**   | **内置 QoS Quality of Service 级别：**<br>QoS0: 最多一次<br> QoS1: 至少一次<br>QoS2: 恰好一次 | 通过确认机制控制：<br>最多一次 (不开启确认机制)<br>至少一次 (开启确认机制) |
| **消息持久化** | **内置持久会话和保留消息，**依赖 Broker 实现 QoS 1/2 消息的持久存储 | **核心 NATS 无持久化**（JetStream 扩展提供强大、可配置的消息持久化 ） |
| **适用场景**   | 物联网设备、传感器网络、移动应用、智能家居、工业自动化等资源受限或网络不稳定的环境。 | 微服务通信、实时数据流处理、命令与控制系统、金融服务、事件驱动架构、云原生应用。 |
| **生态系统**   | 广泛应用于 IoT 领域，拥有丰富的客户端库、开源和商业 Broker 实现。 | CNCF (云原生计算基金会) 项目，在云原生、微服务和实时通信领域快速发展。 |

尽管 NATS 和 MQTT 在各自领域都表现出色，但它们之间存在协议差异，传统上需要复杂的定制桥接才能实现互通。EMQX NATS Gateway 的出现，正是为了弥合这一鸿沟。它打通了 NATS 和 MQTT 协议，使得 IoT 设备（通常使用 MQTT）能够与后端微服务（通常使用 NATS）无缝共享数据，从而打破数据孤岛，为构建更全面、更具洞察力的应用提供了无限可能。这种集成不仅简化了系统架构，还为企业带来了前所未有的灵活性，使其能够根据具体需求选择最适合的协议，同时确保所有组件之间的无缝通信 。  

## EMQX NATS Gateway 的快速配置与启动

本节将为您提供一个快速指南，介绍如何安装最新版本的 EMQX 5.10.0，以及如何配置和使用 EMQX NATS Gateway。

### 安装 EMQX 5.10.0

首先，您需要安装 EMQX 5.10.0。您可以从 [EMQX 官方下载页面](https://www.emqx.com/en/downloads-and-install/enterprise) 获取适用于您操作系统的安装包（例如 Debian 或 macOS 等）。

此处，以 Docker 为例：

```shell
docker run --name emqx \
 -p 18083:18083 -p 1883:1883 -p 20243:20243 \
 -d emqx/emqx-enterprise:5.10.0
```

启动成功后，您可以通过访问 [http://localhost:18083/ ](http://localhost:18083/)进入 EMQX Dashboard，默认用户名密码为 `admin`/`public` 。  

### 开启和配置 NATS Gateway

EMQX NATS Gateway 的配置非常灵活，可以通过 Dashboard 或配置文件进行：

1. 登录 EMQX Dashboard。

2. 在左侧导航栏中，点击 **“管理” -> “网关”**。

3. 找到 **NATS** 网关，点击 **“配置”** 。  

   ![image.png](https://assets.emqx.com/images/0a2b925d6143a1ccefead552aa29dcf0.png)

4. 进入**基础参数**配置，保持默认即可

   ![image.png](https://assets.emqx.com/images/9ab6901d9a9bd85070ab159ff6addff5.png)其中：

   - **挂载点：**为所有 NATS 客户端发布/订阅的主题设置一个固定前缀。此处为空，表示不设置任何前缀
   - **默认心跳间隔：**配置 NATS 网关向客户端发送心跳的间隔时间
   - **心跳超时阈值：**即网关等待心跳的最大超时时间。此处为 5 秒，即 5 秒后未收到客户端的心跳应答，即认为客户端已断线。

5. 点击**下一步**，进入到监听器配置页面，点击**添加监听器**。配置监听器名称为 `default` 监听地址为 `20243` 端口，点击 **添加** 完成监听器配置。

   ![image.png](https://assets.emqx.com/images/1cf2a6e9f93afd66f516197f055e2990.png)

6. 设置完成后，点击启用即完成 NATS 网关的配置和启动。

   ![image.png](https://assets.emqx.com/images/e961a1032921d228f77ee2cae4f3eb2c.png)

## 使用演示：通过 Python 客户端代码实现 NATS 与 MQTT 消息互通

本节将通过 Python 客户端代码示例，演示如何连接 NATS Gateway，实现 NATS 客户端与 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)之间的双向消息互通。

首先，确保您已安装 Python 环境，并安装了 NATS 和 Paho MQTT 客户端库：

```shell
pip install nats-py paho-mqtt
```

我们将演示以下两种情况：

1. NATS 客户端发布消息，MQTT 客户端订阅并接收。
2. MQTT 客户端发布消息，NATS 客户端订阅并接收。

### **NATS 客户端发布，MQTT 客户端接收**

`nats_publisher.py` **：**此脚本连接到 EMQX NATS Gateway，并向 `iot.sensor.data.temperature` Subject 发布消息：

```python
import asyncio
import nats

async def run():
    nc = await nats.connect(servers=["nats://localhost:20243"])
    print("NATS Publisher connected to EMQX NATS Gateway.")

    subject = "sensor.data.temperature"
    message = b'{"device_id": "sensor_001", "temp": 25.5}'

    await nc.publish(subject, message)
    print(f"Published NATS message to subject '{subject}': {message.decode()}")

    await nc.drain()
    print("NATS Publisher disconnected.")

if __name__ == '__main__':
    asyncio.run(run())
```

`mqtt_subscriber.py`**：**此脚本连接到 EMQX MQTT 监听器，并订阅映射后的 MQTT 主题 `sensor/data/temperature`。

```python
import paho.mqtt.client as paho
from paho import mqtt
import time

# MQTT 消息回调函数
def on_message(client, userdata, msg):
    print(f"Received MQTT message on topic '{msg.topic}': {msg.payload.decode()}")

def run():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_message = on_message

    # 连接到 EMQX MQTT 监听器 (默认端口 1883)
    client.connect("localhost", 1883, 60)
    print("MQTT Subscriber connected to EMQX.")

    # 订阅映射后的 MQTT 主题
    # 根据 NATS Gateway 的 topic_mapping 规则，iot.sensor.data.temperature 映射到 sensor/data/temperature
    client.subscribe("sensor/data/temperature", qos=1)
    print("MQTT Subscriber subscribed to 'sensor/data/temperature'.")

    client.loop_forever()

if __name__ == '__main__':
    run()
```

**运行步骤：**

1. 首先运行 `mqtt_subscriber.py`。
2. 然后运行 `nats_publisher.py`。 您将看到 `mqtt_subscriber.py` 接收到 NATS 客户端发布的消息。

### **MQTT 客户端发布，NATS 客户端接收**

`mqtt_publisher.py` ：此脚本连接到 EMQX MQTT 监听器，并向 `command/device/light_001` 主题发布消息。

```python
import paho.mqtt.client as paho
from paho import mqtt
import time

def run():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

    # 连接到 EMQX MQTT 监听器 (默认端口 1883)
    client.connect("localhost", 1883, 60)
    print("MQTT Publisher connected to EMQX.")

    topic = "command/device/light_001"
    message = '{"action": "turn_on", "brightness": 80}'

    client.publish(topic, message, qos=1)
    print(f"Published MQTT message to topic '{topic}': {message}")

    client.disconnect()
    print("MQTT Publisher disconnected.")

if __name__ == '__main__':
    run()
```

`nats_subscriber.py`**：**此脚本连接到 EMQX NATS Gateway，并订阅映射后的 NATS Subject `command.device.light_001`。

```python
import asyncio
import nats

async def message_handler(msg):
    print(f"Received NATS message on subject '{msg.subject}': {msg.data.decode()}")

async def run():
    # 连接到 EMQX NATS Gateway
    nc = await nats.connect(servers=["nats://localhost:20243"])
    print("NATS Subscriber connected to EMQX NATS Gateway.")

    # 订阅映射后的 NATS Subject
    # command/device/light_001 映射到 command.device.light_001
    await nc.subscribe("command.device.light_001", cb=message_handler)
    print("NATS Subscriber subscribed to 'device.command.light_001'.")

    # 保持连接，等待消息
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()
        print("NATS Subscriber disconnected.")

if __name__ == '__main__':
    asyncio.run(run())
```

**运行步骤：**

1. 首先运行 `nats_subscriber.py`。
2. 然后运行 `mqtt_publisher.py`。 您将看到 `nats_subscriber.py` 接收到 MQTT 客户端发布的消息。

通过这些简单的示例，您可以看到 EMQX NATS Gateway 无缝地在 MQTT 和 NATS 协议之间转换和转发消息，极大简化了异构系统间的集成工作。

## 总结

EMQX 5.10.0 NATS Gateway 的发布，是 EMQX 在构建统一、灵活的实时数据基础设施方面迈出的又一重要步伐。它通过提供 MQTT 和 NATS 协议之间的原生、双向互通能力，有效地打破了实时通信领域长期存在的协议壁垒，为构建更加互联互通、灵活高效的分布式系统奠定了坚实基础。

这项创新不仅显著简化了复杂的集成挑战，消除了对定制桥接或独立消息中间件的需求，从而降低了开发和运营成本，更开启了物联网、微服务和实时控制等领域应用的新篇章。无论是智能工厂中的传感器数据流向云端微服务进行实时分析，还是后端控制系统向边缘设备发送指令，EMQX NATS Gateway 都能够确保数据在不同协议生态系统之间自由、高效地流动。  



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
