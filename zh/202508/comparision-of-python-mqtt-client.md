## 引言

物联网（IoT）已成为现实，数十亿设备将我们的物理世界与数字世界连接起来。为了实现智能设备之间的有效通信，我们需要一个轻量、可靠的消息传输协议。其中，[MQTT（消息队列遥测传输）](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)作为物联网消息传输的标准协议脱颖而出。

随着物联网应用复杂性的不断增加，**Python** 凭借其简洁优雅、易于阅读的语法、庞大的库生态系统以及快速原型开发的优势，已成为开发物联网解决方案的强大工具。

在开发基于 Python 的物联网应用时，选择合适的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)至关重要。Python 生态系统提供了多样化的选择，既有久经考验的同步库，也有新一代现代化、高性能的异步客户端。面对这些选择，开发者可能会感到困惑：哪个客户端最稳定？哪个能为高流量应用提供最佳性能？哪个能与 FastAPI 等 Web 框架实现最佳集成？

本指南旨在回答这些问题。我们将全面比较 2025 年的五个主流 Python MQTT 客户端：**paho-mqtt**、**gmqtt**、**aiomqtt**、**amqtt** 和 **fastapi-mqtt**。阅读完本文，你将清晰了解它们的优缺点，从而为你的下一个项目做出明智的选择。

## 关键比较标准

为了提供公平而全面的比较，我们将基于一系列统一的标准来评估每个客户端。这些考量因素涵盖了从社区流行度到具体技术特性的多个层面，帮助你在权衡利弊后，找到最符合你需求的客户端。

### **架构：同步 vs. 异步**

这可以说是最关键的决策点，因为它定义了应用程序的基本结构。

- **同步 (Sync)：**这些客户端以阻塞方式执行操作。当调用 `connect()` 或 `publish()` 之类的任务时，程序会等待其完成后再继续执行。这种模型更易于理解，非常适合编写简单的脚本或集成到旧版代码库中。
- **异步 (Async)：**这些客户端基于 Python 的 asyncio 框架构建。它们以非阻塞方式运行，使程序无需使用多线程即可高效处理数千个并发连接和 I/O 操作。这种架构非常适合现代高性能、I/O 密集型应用程序，例如物联网网关或实时数据处理器。

### **MQTT 协议支持（v3.1.1 与 v5.0）**

MQTT 协议本身也在不断完善。虽然 v3.1.1 版本是经过长期验证且获得广泛支持的标准，但 MQTT v5.0 引入了显著的增强功能。我们将检查每个客户端支持的协议版本。v5.0 的主要功能包括所有 ACK 上的原因代码、会话过期、消息过期和用户属性，利用这些功能可以实现更稳健、更复杂的消息传递模式。

### **API 设计和易用性**

我们将介绍每个客户端的常见模式，例如使用回调、async/await 语法或基于类的处理程序。简洁、设计良好的 API 可以显著缩短开发时间，并使代码更易于维护。

### **社区健康与维护**

一个库的可靠性取决于其背后的社区。我们将通过以下几个指标来评估它：

- **GitHub Stars：**流行度和社区信任程度的粗略代表。
- **更新频率：**项目是否积极维护、定期更新和修复错误。最近更新的库是一个可参考的关键数据。
- **文档质量：**文档是否全面、易于浏览且充满有用的示例内容。

### **高级功能和集成**

除了基本的发布/订阅功能外，许多应用程序还需要高级功能。我们将探讨对以下功能的支持：

- **安全性：**是否原生支持 TLS/SSL 加密。
- **WebSockets：**是否支持通过 WebSockets 传输 MQTT 的能力，这对于基于浏览器的客户端至关重要。
- **自动重连：**在网络中断时，客户端是否可以自动重新连接。
- **框架集成：**客户端是通用型设计，还是深度集成于类似 FastAPI 这样的特定框架。

## 为您的 Python 项目准备 MQTT Broker

要使用 Python 实现 MQTT，您需要一个可靠的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 来管理消息路由。EMQX 是一款领先的 MQTT 消息平台，以其卓越的可扩展性和性能而备受信赖。它支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 、3.1.1 和 3.1 版本，可处理数百万个并发连接，并提供基于 SQL 的规则引擎、与 PostgreSQL 和 Kafka 等数据库集成等功能。EMQX 的高可用性和低延迟能力使其成为物联网应用的理想之选。

为了简单起见，我们推荐基于 EMQX Platform [免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

- 服务器：`broker.emqx.io`
- TCP 端口：`1883`
- WebSocket 端口：`8083`
- SSL/TLS 端口：`8883`
- 安全 WebSocket 端口：`8084`

## Python MQTT 客户端深入研究

### paho-mqtt：业界标准

如果说有哪个库堪称 Python 中 MQTT 的基石，那非 paho-mqtt 莫属。作为 Eclipse 基金会的官方项目，paho 提供了无与伦比的稳定性、可靠性和社区支持，是业余爱好者和大型企业部署等无数开发者的首选。

**paho-mqtt 在 2024 年 4 月发布的 2.1.0 版本，相对于旧版 v1.x 系列实现了重大改进。paho-mqtt v2.x 全面支持 MQTT v5.0、v3.1.1 和 v3.1 协议，允许开发者根据自身需求选择合适的版本。**这种灵活性，加上改进的错误处理和现代 Python 的兼容性（需要 Python 3.7 及以上版本），体现了该项目持续的可靠性和与时俱进的承诺。

#### **核心特性**

- **同步与回调机制**：该客户端采用简洁明了的**同步阻塞式网络循环**，并利用回调函数（如 `on_connect`、`on_message`）来处理各种事件。这种模型设计直观，易于理解和调试，适用于多种应用场景。
- **成熟与稳定**：经过多年的发展和广泛应用，该客户端已经过严苛的测试，并被庞大的用户社区公认为生产环境的稳定之选。
- **全面的协议支持**：它能够完全支持 MQTT v5.0、v3.1.1 和 v3.1 协议，您可以根据具体需求灵活选择合适的版本。
- **功能丰富**：该客户端提供一系列强大的功能，包括对 TLS/SSL 安全加密、支持 ALPN 协议、自动重连逻辑、Unix 套接字连接以及用于简化一次性发布/订阅操作的辅助功能。
- **卓越的社区与文档**：得益于完善的官方文档、海量的教程以及庞大的用户群体，您几乎总能通过简单的搜索快速找到问题的解决方案。

#### **安装**

请使用以下命令，直接从 PyPI 安装最新版本。

```shell
pip install paho-mqtt
```

#### **代码示例**

回调驱动的 API 对于设置客户端来说简单而有效。

#### **订阅者示例**

这段代码展示了如何连接到 MQTT 服务器，订阅所有系统主题（`paho/test`），并打印收到的所有消息。`loop_forever()` 调用会阻塞程序，使客户端持续监听消息。

```python
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    if not reason_code.is_failure:
        # Subscribing in on_connect() means that if we lose the
        # connection and reconnect then subscriptions will be renewed.
        client.subscribe("paho/test")
    else:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(f"{message.topic}: {message.payload.decode()}")

# For v2.0+, you must specify the callback API version
# VERSION2 is recommended for new projects
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
```

**发布者示例**

这段代码连接到 MQTT 服务器，并每秒发布一条简单的消息。

```python
import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid, reason_code, properties):
    # Called when message is published successfully
    print(f"Message {mid} published successfully")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_publish = on_publish
client.connect("broker.emqx.io", 1883, 60)

# Start a background thread to handle network traffic
client.loop_start()

# Publish messages
for i in range(5):
    payload = f"Hello from paho-mqtt - Message {i}"
    msg_info = client.publish('paho/test', payload, qos=1)
    msg_info.wait_for_publish()  # Wait for message to be published
    print(f"Sent: {payload}")

# Stop the background thread and disconnect
client.loop_stop()
client.disconnect()
```

#### 优缺点总结

**优点**

- **持续的稳定性**：作为最成熟且久经考验的选择，您完全可以信赖它在生产环境中的表现。
- **社区成熟、文档完善**：在解决问题时，完善的文档和庞大的社区力量是无价之宝。
- **功能全面支持**：对 MQTT v5.0、安全性及其他核心功能提供了出色的支持。
- **模型简单易懂**：同步、基于回调的设计理念对初学者来说非常容易理解和掌握。

**缺点**

- **同步设计是最大局限**：这是它最主要的缺点。对于需要高效处理数千个并发 I/O 操作的高吞吐量现代应用来说，它并非最佳选择。在这种情况下，异步客户端会是更好的方案。
- **回调的复杂性**：尽管对小型脚本来说很简单，但在复杂的应用中，跨多个回调函数管理状态和逻辑可能会变得非常繁琐，俗称“回调地狱”。
- **版本的变更**：从 v1.x 版本迁移需要代码更新，特别是回调 API 版本规范的调整，这可能导致现有应用程序需要进行重构。

### gmqtt：功能丰富的异步客户端

gmqtt 是一个功能强大的异步 MQTT 客户端，由 Wialon（一家专注于 GPS 追踪和物联网解决方案的公司）开发和维护。它于 2018 年 2 月首次发布，现已发展成为一个成熟的异步客户端，在 GitHub 上拥有 422 **个** stars，并保持定期更新，最新版本 v0.7.0 于 2024 年 11 月发布。

它在众多异步客户端中脱颖而出，主要凭借两大优势：对 MQTT v5.0 协议的强大原生支持以及独特而灵活的插件系统，后者可实现广泛的自定义功能。该项目从设计之初就充分利用了 Python 的 asyncio 框架，使其成为需要高性能、非阻塞 I/O 来处理大量并发连接或实时数据流的应用程序的绝佳选择。

#### 核心特性

- **原生支持 Asyncio**：该客户端完全基于 `asyncio` 构建，是现代 I/O 密集型 Python 应用程序的理想之选。
- **优先支持 MQTT v5.0**：它对 MQTT v5.0 及其高级功能提供了卓越的支持，包括 `content_type`、`user_property`、`message_expiry_interval` 和 `topic_alias` 等属性。此外，其设计的一个巧妙之处在于，如果服务器不支持 v5.0 协议，它也能够降级到 v3.1.1，从而确保广泛的兼容性。
- **灵活的插件系统**：这是 `gmqtt` 的关键特性。它允许开发者通过编写自己的插件来扩展客户端功能，实现自定义认证、消息日志记录或专业的订阅管理等任务，而无需修改核心客户端代码。
- **熟悉的 API 风格**：尽管是异步客户端，但它采用基于回调的 API（`on_connect`, `on_message`），这让习惯了 `paho-mqtt` 的开发者能够更顺畅地过渡到异步编程。
- **强大的重连逻辑**：内置自动重连功能，支持配置重试次数和延迟，这对于生产环境中的物联网应用至关重要。
- **商业支持**：由 Wialon 公司维护，这为该项目的长期可行性和持续开发提供了可靠保障，确保了稳定的更新和错误修复。

#### **安装**

请使用以下命令直接从 PyPI 安装该库：

```shell
pip install gmqtt
```

#### 代码示例

以下示例展示了 `gmqtt` 中一种常见的模式：如何设置一个既能发布也能订阅的客户端，并利用 `asyncio.Event` 来实现优雅地关闭程序。

```python
import asyncio
import signal
import time
from gmqtt import Client as MQTTClient

STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('gmqtt/test', qos=0)

def on_message(client, topic, payload, qos, properties):
    print('RECV MSG:', payload.decode(), 'on topic:', topic)

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')

def ask_exit(*args):
    STOP.set()

async def main(broker_host):
    client = MQTTClient("gmqtt-client")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    await client.connect(broker_host)

    # Publish a message with MQTT 5.0 properties
    client.publish('gmqtt/test', str(time.time()), qos=1,
                   content_type='utf-8', user_property=('timestamp', str(time.time())))

    # Wait for a stop signal (e.g., Ctrl+C)
    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    # Add signal handlers for graceful shutdown
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)
    
    host = 'broker.emqx.io'
    loop.run_until_complete(main(host))
```

#### 优缺点总结

**优点**

- **异步高性能**：特别适合需要高效管理大量并发连接的高吞吐量应用。
- **出色的插件架构**：提供了无与伦比的灵活性，可以根据复杂需求自由定制客户端行为。
- **强大的 MQTT v5.0 支持**：如果您需要利用最新的协议特性，它是首选。
- **简洁熟悉的 API**：在 `asyncio` 框架下，其回调系统设计良好，上手相对容易。

**缺点**

- **异步学习曲线**：对于不熟悉异步编程的开发者来说，与 `paho-mqtt` 相比，可能需要更陡峭的学习曲线。
- **社区规模较小**：尽管项目本身很健壮，但其用户基数比 `Paho` 小。这意味着可参考的第三方教程或社区问答可能会比较少。
- **文档有限**：文档主要集中在 GitHub 的 `README` 和代码示例中。虽然这些资料很有用，但可能不如 `Paho` 专门的文档网站那样详尽。

### aiomqtt：最「Pythonic」的异步客户端

aiomqtt 是一个由社区维护的异步 MQTT 客户端，以其简洁和现代化的 API 脱颖而出。该项目最初于 2020 年 4 月创建，名为 asyncio-mqtt，并于 2023 年更名为 aiomqtt，至今已获得 491 个 GitHub stars。其最新版本 v2.4.0 于 2025 年 5 月发布，成为了异步 MQTT 领域「Pythonic」方法的典范。它刻意摒弃了传统的回调函数，转而采用优雅的 `async with` 语句和异步迭代器。

该库的理念是为在 asyncio 生态系统中工作的开发者提供友好直观的体验。它巧妙地利用了 **paho-mqtt** 经过验证的消息解析引擎作为底层支持，**将 paho 的底层稳定性与现代化的异步高级接口完美结合**。因此，对于将代码清晰度、可维护性和易用性作为首要考量的项目来说，aiomqtt 是一个绝佳的选择。

#### 核心特性

**真正的「Pythonic」异步 API**：其最显著的特点是使用 `async with` 管理连接，以及使用 `async for` 循环遍历接收到的消息。这种设计极大地简化了代码，彻底告别了「回调地狱」。

**轻量与极简主义：**aiomqtt 的依赖项极少，专注于提供核心的 MQTT 客户端体验，这使得它快速且易于集成到任何项目中。

**全面的协议支持**：该客户端全面支持现代的 MQTT v5.0 协议和广泛使用的 v3.1.1 协议。

**强大的重连机制：**aiomqtt 能够自动处理网络中断，并采用简单、可配置的指数退避策略进行重连，这对于构建可靠的物联网应用至关重要。

**社区维护**：作为一个活跃的社区驱动项目，它持续获得更新，并拥有不断增长的用户群体。

#### **安装**

请使用以下命令直接从 PyPI 安装该库：

```shell
pip install aiomqtt
```

#### 代码示例

以下示例展示了 aiomqtt 优雅的 `async with` 语法。客户端连接、订阅并发布一条消息，随后使用 `async for` 循环来干净利落地处理所有传入的消息。

```python
import asyncio
import aiomqtt

async def main():
    try:
        # The async with statement handles connection and disconnection automatically
        async with aiomqtt.Client("broker.emqx.io") as client:
            # Subscribe to a topic
            await client.subscribe("aiomqtt/test")
            # Publish a message
            await client.publish("aiomqtt/test", "Hello from aiomqtt!")
            
            # Process incoming messages from the subscribed topic
            async for message in client.messages:
                print(f"[{message.topic}] {message.payload.decode()}")

    except aiomqtt.MqttError as e:
        print(f"MQTT Error: {e}")

if __name__ == "__main__":
    # In a real application, you might want to handle Ctrl+C more gracefully
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
```

#### 优缺点总结

**优点**

- **极易上手**：它采用现代化的 `asyncio` 模式，使 API 高度直观，并显著减少了样板代码。
- **代码简洁且易于维护**：利用 `async for` 循环来处理消息，使得应用程序逻辑清晰流畅，易于追踪。
- **轻量化**：依赖项极少，使其成为多种环境下的理想选择。
- **可靠的底层支持**：它沿用了 Paho 稳定可靠的解析引擎，让您同时拥有优秀的 API 接口和坚实的基础，兼得两者的优势。

**缺点**

- **处理复杂逻辑的灵活性较低**：虽然简洁是优点，但 `async for` 循环这种线性的处理方式，在编排高度复杂、多事件交互的逻辑时，其灵活性可能不如回调函数或插件系统。
- **配置依赖于代码**：它没有类似 `fastapi-mqtt` 那样的专用配置文件系统，所有设置都需要作为参数在代码中进行传递。

### amqtt：多功能 MQTT 客户端和 Broker

amqtt 是 Python 生态系统中一款功能强大、用途广泛的 MQTT 工具。作为备受好评但已停止更新的 HBMQTT 项目的社区维护分支，它于 2021 年 2 月创建，目前在 GitHub 上获得了 162 个星标。其最新版本 v0.11.2 已于 2025 年 7 月发布。amqtt 最显著的特点在于它不仅是一个客户端库，更是一个功能齐全的 MQTT Broker，将两者功能集于一身。

这种双重能力使 amqtt 成为开发者的优选。无论是在本地进行开发、测试，还是构建需要紧密耦合客户端与代理逻辑的专用物联网平台，它都能提供一体化的解决方案。此外，amqtt 基于 asyncio 异步框架从头构建，这确保了其客户端和代理组件都具备出色的性能和可扩展性。

#### **核心特点：**

- **客户端与代理合一：** 这是 amqtt 最核心的特点。通过这一个库，你既可以连接到其他代理，也可以在本地运行自己的代理，用于测试或生产环境。
- **完整的协议支持：** amqtt 提供了稳定且合规的 MQTT v3.1.1 协议实现。需要注意的是，目前它尚不支持 MQTT v5.0。
- **直接的客户端 API：** 其客户端 API 支持直接实例化 `MQTTClient`，并提供 `deliver_message()` 等方法来接收消息。这种设计让开发者能在 asyncio 环境中以简单直接的方式处理 MQTT 操作。
- **命令行工具：** amqtt 自带实用的命令行工具（`amqtt_pub` 和 `amqtt_sub`），无需编写任何 Python 代码，即可快速向任何 MQTT 代理发布、订阅消息或进行测试。
- **WebSocket 支持：** 原生支持通过 WebSocket 传输 MQTT 协议，提供了更灵活的连接选项。

#### **安装**

从 PyPI 安装 amqtt 库及其命令行工具：

```shell
pip install amqtt
```

#### **代码示例**

下面的示例展示了如何使用 amqtt 库，通过直接实例化 `MQTTClient` 并利用 `deliver_message()` 方法来构建客户端并接收消息。

```python
import asyncio
import logging
from amqtt.client import MQTTClient
from amqtt.mqtt.constants import QOS_1

# Configure logging to see amqtt's internal messages
# logging.basicConfig(level=logging.INFO)

async def main():
    client = MQTTClient()
    try:
        # Connect to the broker
        await client.connect("mqtt://broker.emqx.io/")
        
        # Subscribe to a topic
        await client.subscribe([("amqtt/test", QOS_1)])
        
        # Publish a message
        await client.publish("amqtt/test", b"Hello from amqtt!")
        print("Message published")
        
        # Receive messages
        print("Waiting for messages...")
        for i in range(5):  # Listen for a few messages
            message = await client.deliver_message()
            if message:
                print(f"RECV MSG: '{message.data.decode()}' on topic '{message.topic}'")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

#### **优缺点总结**

**优点：**

- **无与伦比的多功能性**：内置的代理功能是 amqtt 的一大亮点，特别适合本地开发和测试，因为它省去了单独安装或运行 Docker 容器的麻烦。
- **API 简单直观**：其客户端 API 采用直接调用的方式，如 `deliver_message()`，为在 asyncio 应用中处理 MQTT 操作提供了一种清晰明了的方法。
- **实用的命令行工具**：附带的命令行工具非常方便，可用于快速调试和交互。
- **活跃的社区维护分支**：作为 HBMQTT 的继承者，amqtt 持续获得更新和社区支持。

**缺点：**

- **可能功能过剩**：如果你的需求只是一个简单的客户端，那么 amqtt 所包含的完整代理功能可能会显得过于复杂。
- **消息处理方式不同**：`deliver_message()` 这种处理消息的方式，与一些其他客户端所使用的回调函数或异步迭代器模式相比，可能没那么直观。

### **fastapi-mqtt：FastAPI 专属的 MQTT 客户端**

fastapi-mqtt 是一个高度专精的 MQTT 客户端，专门为集成 FastAPI 网页框架而设计。该项目创建于 2020 年 11 月，目前已获得 286 个 GitHub 星标，并持续活跃开发，最新版本 2.2.0 已于 2024 年 5 月发布。

它巧妙地将网页服务器的异步世界与 MQTT 的事件驱动特性连接起来，让开发者可以直接在 FastAPI 应用的结构内管理 MQTT 连接和处理消息。

fastapi-mqtt 不以独立脚本的形式运行，而是利用 FastAPI 的 lifespan 上下文管理器来管理 MQTT 客户端的生命周期。它提供了基于简单装饰器的 API 来订阅主题，使其使用体验如同 FastAPI 框架本身的自然延伸。如果你的项目基于 FastAPI 且需要通过 MQTT 进行通信，那么这个库是你的不二之选。

#### **主要功能**

- **与 FastAPI 无缝集成：**专为 FastAPI 设计，可以自动管理 MQTT 连接的整个生命周期，使其与网页服务器同步运行。
- **基于装饰器的 API：** 它使用直观的装饰器（如 `@fast_mqtt.on_connect` 和 `@fast_mqtt.on_message`）来定义事件处理器。这种模式对于任何 FastAPI 或 Flask 开发者来说都非常熟悉。
- **配置简单：** 配置通过 Pydantic 的 `MQTTConfig` 对象来完成，完美契合了 FastAPI 的配置管理模式。
- **基于 gmqtt 构建：** 底层依赖于功能强大且丰富的 `gmqtt` 客户端，因此它也继承了 `gmqtt` 的稳健性，包括对 MQTT v5.0 的支持和自动重连功能。
- **随处发布消息：** 它提供了 `MQTTClient` 实例，可以轻松注入到你的 API 路由中，让你能够直接在处理 HTTP 请求时发布 MQTT 消息。

#### **安装**

从 PyPI 安装 fastapi-mqtt 库：

```shell
pip install fastapi
pip install fastapi-mqtt
```

#### **代码示例**

这个示例展示了一个最简化的 FastAPI 应用，它会在启动时连接到 MQTT broker，订阅一个主题，并提供一个 HTTP 接口用于发布消息。

```python
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from gmqtt import Client as MQTTClient
from fastapi_mqtt import FastMQTT, MQTTConfig

# Configuration for the MQTT client
mqtt_config = MQTTConfig(
    host="broker.emqx.io",
    port=1883,
    keepalive=60
)

fast_mqtt = FastMQTT(config=mqtt_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()

app = FastAPI(lifespan=lifespan)

# Decorator for handling the connect event
@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    # Subscribe to a topic upon connection
    client.subscribe("fastapi-mqtt/test")
    print("Connected: ", client, flags, rc, properties)

# Decorator for handling incoming messages
@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    print("Received message: ", topic, payload.decode(), qos, properties)

# A simple HTTP endpoint to publish a message
@app.post("/publish")
async def publish_message(topic: str, message: str):
    fast_mqtt.publish(topic, message)
    return {"result": "Message published", "topic": topic, "message": message}
```

要运行上面的代码，你需要将其保存为一个 Python 文件（例如 `main.py`），然后使用 ASGI 服务器（如 Uvicorn）来启动它：uvicorn main:app --reload

#### **优缺点总结**

**优点：**

- **专为 FastAPI 用户打造**：fastapi-mqtt 的设计与 FastAPI 框架无缝契合，使用起来感觉就像是框架的内置功能。
- **使用极其简单**：基于装饰器的 API 简化了大量的样板代码，让 MQTT 客户端的管理变得非常轻松。
- **底层强大**：它内部依赖于功能强大且完善的 gmqtt 客户端，因此继承了其稳定性和丰富的功能。
- **应用结构清晰**：能够将你的网页逻辑和 MQTT 逻辑整合在同一个应用上下文中，让代码结构更加清晰有序。

**缺点：**

- **框架限定**：这是它最大的优点，也是最主要的限制。它不是一个通用的 MQTT 客户端，只有在使用 FastAPI 时才有价值。
- **控制力稍弱**：由于它封装了客户端的管理细节，相比于直接使用 gmqtt 或其他通用客户端，你在某些精细化控制上会受到一些限制。

## **概览和对比**

为了帮助你快速了解这些库，下表从关键的定性和定量指标对每个客户端进行了分析。

数据截止到 2025 年 7 月。

| **对比标准**            | **paho-mqtt**                          | **gmqtt**              | **aiomqtt**            | **amqtt**              | **fastapi-mqtt**      |
| ----------------------- | -------------------------------------- | ---------------------- | ---------------------- | ---------------------- | --------------------- |
| **架构**                | 同步                                   | 异步                   | 异步                   | 异步                   | 异步                  |
| **主要 API 风格**       | 基于回调                               | 基于回调 & 插件        | async with / async for | 直接客户端 API         | 基于装饰器 (FastAPI)  |
| **GitHub 项目**         | eclipse/paho.mqtt.python               | wialon/gmqtt           | empicano/aiomqtt       | Yakifo/amqtt           | sabuhish/fastapi-mqtt |
| **项目创建时间**        | 2015 年 12 月                          | 2018 年 2 月           | 2020 年 4 月           | 2021 年 2 月 (分支)    | 2020 年 11 月         |
| **许可证**              | EPL-2.0 & EPL-1.0                      | MIT                    | BSD-3-Clause           | MIT                    | MIT                   |
| **支持的 Python 版本**  | >= 3.7 (已移除对 2.7, 3.5, 3.6 的支持) | >= 3.7                 | >= 3.8                 | >= 3.10 (v0.11.x)      | >= 3.8                |
| **主要依赖**            | 无                                     | 无                     | paho-mqtt              | websockets, passlib    | gmqtt, pydantic       |
| **最新版本**            | v2.1.0 (2024 年 4 月)                  | v0.7.0 (2024 年 11 月) | v2.4.0 (2025 年 5 月)  | v0.11.2 (2025 年 7 月) | v2.2.0 (2024 年 5 月) |
| **GitHub 星标数**       | 2.3k                                   | 422                    | 491                    | 162                    | 286                   |
| **GitHub 版本发布次数** | 10+ (包括预发布版本)                   | 20+                    | 20+                    | 10+                    | 20+                   |
| **GitHub 提交次数**     | 880+                                   | 150+                   | 400+                   | 1300+                  | 200+                  |

## **如何选择合适的 Python MQTT 客户端**

选择最合适的客户端，关键在于它是否与你的项目架构和个人编码风格相契合。没有“一劳永逸”的选择，只有最适合特定任务的工具。

以下指南基于常见场景，为你提供选择建议。

#### **对于初学者、简单脚本或老旧代码库：paho-mqtt**

如果满足以下任一情况，请选择 **paho-mqtt**：

- 你刚接触 MQTT，希望采用最直接、非异步的学习路径。
- 你的应用只是用于发布或订阅少数主题的简单脚本。
- 你正在将 MQTT 集成到现有的同步应用中。

**paho-mqtt** 凭借其同步架构、悠久的历史（2015 年创建）和庞大的社区（拥有 2.3k 星标），是无可争议的标准。其基于回调的 API 易于掌握基本任务，且稳定性经过实战考验。它无需外部依赖，是一个简单可靠的选择。

#### **对于现代化、简洁、通用的异步应用：aiomqtt**

如果满足以下任一情况，请选择 **aiomqtt**：

- 你正在构建新的 **asyncio** 应用。
- 你最看重代码的整洁、可读性和可维护性。
- 你的消息处理逻辑相对简单。

**aiomqtt** 标志性的 `async with` / `async for` API 风格使其成为最“Pythonic”的异步客户端。这种方式避免了回调管理，代码线性且易于理解。其受欢迎程度（491 个星标）和活跃开发状态（400+ 次提交）显示了社区的高度信任。它基于 **paho-mqtt** 构建，将现代 API 与稳固的基础相结合。

#### **对于高性能、复杂、可定制的异步应用：gmqtt**

如果满足以下任一情况，请选择 **gmqtt**：

- 你的应用需要处理大量并发连接和消息。
- 你需要通过自定义逻辑来扩展客户端的核心行为，例如用于身份验证、日志记录或消息路由。
- 你喜欢在 **asyncio** 环境中使用回调风格的 API。

**gmqtt** 的杀手级功能是其**插件系统**。这提供了其他客户端无法比拟的定制能力，使其成为构建复杂企业级物联网平台的理想选择。其坚实的社区地位（422 个星标和 20+ 个版本发布）使其成为要求严苛的项目的可靠选择。

#### **对于需要内置代理或偏好面向对象方法的项目：amqtt**

如果满足以下任一情况，请选择 **amqtt**：

- 你需要一个简单的集成式 MQTT 代理，用于本地开发和测试。
- 你更喜欢通过直接客户端 API 来显式处理消息。
- 你需要一个多功能的命令行工具来快速调试。

作为 HBMQTT 的继承者，**amqtt** 是一个真正的工具包。其直接客户端 API 适合在 **asyncio** 环境中执行直接的 MQTT 操作。其庞大的提交历史（1300+ 次）证明了其深厚的开发积淀。尽管星标数较低（162），但它服务于一个独特而强大的细分市场。

#### **如果你使用 FastAPI 框架：fastapi-mqtt**

如果你的应用基于 **FastAPI** 构建，那么选择很简单：你应该使用 **fastapi-mqtt**。

它专为此目的而设计，其基于装饰器的 API 与 FastAPI 应用的生命周期无缝集成，让你能够非常轻松地在网页应用中管理 MQTT 连接和处理消息。由于它的底层依赖于 gmqtt，你将获得一个功能强大的异步客户端，并将其封装在一个方便的、框架专属的包中。

## **总结**

Python 生态系统为 MQTT 开发提供了极其丰富和成熟的选择。正如我们所见，这些多样的客户端并非混乱的根源，而是社区对不同架构需求和开发者偏好的积极回应。现在，问题的关键不再是你能否用 Python 使用 MQTT，而是你想如何构建你的应用。

**你的决定最终取决于一个关键问题：同步还是异步？**

- **对于同步任务、简单脚本或与传统系统集成**，**paho-mqtt** 依然是无可争议、坚如磐石的标准。其稳定性和庞大的社区支持使其成为安全可靠的选择。
- **对于异步应用**，选择变得有趣起来，这取决于你偏爱的编码风格和项目复杂性。
  - **aiomqtt** 为喜爱现代 `async/await` 语法的开发者提供了最简洁、最“Pythonic”的 API。
  - **gmqtt** 通过其插件系统提供了无与伦比的强大功能和灵活性，非常适合复杂的、高性能的平台。
  - **amqtt** 以其集成的代理功能提供了独特的通用性，是测试和开发的强大工具。
  - **对于 FastAPI 用户**，**fastapi-mqtt** 则提供了无缝且专用的集成，感觉就像是框架的内置部分。

通过本文的深入分析和对比表，你已充分掌握了做出明智决定的信息。选择一个与你的项目架构相符、使用起来最直观的客户端，然后满怀信心地开始构建你的下一个互联应用吧。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
