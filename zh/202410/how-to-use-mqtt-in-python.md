## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级的消息传输协议，采用发布/订阅模式，使用最少的代码和带宽提供可靠的实时通信。它特别适用于资源有限和低带宽网络的设备，因此在物联网、移动互联网、车联网和电力行业得到了广泛应用。

Python 因其灵活性、易用性和丰富的库而在物联网中被广泛使用。由于能够处理大量数据，Python 非常适合智能家居自动化、环境监测和工业控制。它与微控制器兼容，使其成为开发物联网设备的重要工具。

本文主要介绍如何在 Python 项目中使用 paho-mqtt 客户端，实施与 MQTT 代理之间的连接、订阅、消息传递等功能。

## 为什么选择 Paho MQTT Python 客户端？

Paho Python 客户端提供了一个支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5)、3.1.1 和 3.1 的客户端，适用于 Python 2.7 或 3.x。它还提供了一些辅助函数，使得向 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)发布单条消息变得非常简单。

作为 Python 社区中最受欢迎的 MQTT 客户端库，Paho MQTT Python 客户端具有以下优点：

- 开源且得到社区支持；
- 简洁易用的 API，便于连接 MQTT 服务器并进行消息的发布/订阅；
- 支持多种安全机制；
- 积极开发和维护，以适应快速发展的物联网环境。

## Python MQTT 项目准备

### Python 版本

该项目在 Python 3.11 中开发和测试。请确认您安装了正确的 Python 版本，可以使用以下命令：

```shell
$ python3 --version             
Python 3.11.8
```

### 安装 Paho MQTT 客户端

paho-mqtt 在 2024 年 2 月发布了 2.0.0 版本，相比 1.X 版本有一些重要更新。本文主要演示 1.X 版本的代码，同时也会提供 2.0.0 版本的相应代码，供读者选择合适的 paho-mqtt 版本。

> 有关 2.0.0 版本的详细变更，请参阅文档：[Migrations — Eclipse paho-mqtt  documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/migrations.html) 

**使用 Pip 安装 paho-mqtt 1.X**

```shell
pip3 install "paho-mqtt<2.0.0"
```

**使用 Pip 安装 paho-mqtt 2.X**

```shell
pip3 install paho-mqtt
```

> 如果您需要安装 Pip 的帮助，请参考官方文档：[Installation - pip documentation v24.2](https://pip.pypa.io/en/stable/installation/) 。该资源提供了在不同操作系统和环境中安装 Pip 的详细说明。

## 准备 MQTT Broker

在开始之前，请确保您有一个 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 用于通信和测试。我们建议使用 EMQX Platform 的 Serverless 版本。

EMQX Platform 是一个全托管的 MQTT 消息云服务，可以无缝连接您的物联网设备到任何云端，无需维护基础设施。EMQX Serverless 在安全、可扩展的集群上提供 MQTT 服务，并采用按量计费的定价模式，是适合快速开启 MQTT 项目的灵活经济的解决方案。

<section class="promotion">
    <div>
        免费试用 EMQX Platform
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient">开始试用 →</a>
</section>

为简化流程，本文将使用[免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

- 服务器：`http://broker.emqx.io`
- TCP 端口：`1883`
- WebSocket 端口：`8083`
- SSL/TLS 端口：`8883`
- 安全 WebSocket 端口：`8084`

## Paho MQTT Python 客户端使用

导入 Paho MQTT 客户端：

```python
from paho.mqtt import client as mqtt_client
```

### 创建 MQTT 连接

#### TCP 连接

我们需要指定 MQTT 连接的代理地址、端口和主题。此外，我们可以使用 Python 的 `random.randint` 函数生成随机的客户端 ID。

```python
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
```

> *了解更多请查看博客:* [*创建 MQTT 连接时如何设置参数*](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)

接下来，我们需要编写 `on_connect` 回调函数，以便连接代理。此函数在客户端成功连接后被调用，我们可以使用 `rc` 参数检查连接状态。通常，我们还会创建一个同时连接到 `broker.emqx.io` 的客户端对象。

```shell
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

#### 自动重连

在 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)中，自动重连功能确保在不稳定的网络条件下，设备与代理之间可靠的通信，无需人工干预。当网络连接中断或代理暂时不可用时，客户端可以恢复发布或订阅主题，这对于汽车系统和医疗设备等高可靠性应用至关重要。

Paho MQTT 客户端的自动重连代码如下：

```python
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
```

然后，将其设置为客户端对象的 `on_disconnect`。

```python
client.on_disconnect = on_disconnect 
```

客户端自动重连的完整代码请见：[GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-Python3/pub_sub_tcp.py).

#### TLS/SSL

在 MQTT 中使用 TLS 可以确保信息的机密性和完整性，防止信息泄露和篡改。TLS 认证可以分为单向认证和双向认证。

#### 单向认证

Paho MQTT 客户端的单向认证代码如下：

```python
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
```

**双向认证**

Paho MQTT 客户端的双向认证代码如下：

```python
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(
        ca_certs='./server-ca.crt',
        certfile='./client.crt',
        keyfile='./client.key'
    )
```

### 发布消息

创建一个 while 循环，每秒向主题 `/python/mqtt` 发送一条消息，并在发送 5 条消息后退出循环。

```python
 def publish(client):
     msg_count = 1
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1
         if msg_count > 5:
             break
```

### 订阅

创建消息回调函数 `on_message`，当客户端收到来自 MQTT Broker 的消息时触发。我们将在此函数中打印订阅主题的名称和收到的消息。

```python
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```

## 完整代码

### MQTT 消息发布代码

```python
# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
```

### MQTT 订阅代码

```python
# python 3.11

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
```

## 测试

#### 订阅

运行 MQTT 订阅脚本 `sub.py`，我们将看到客户端成功连接并开始等待发布者发布消息。

```shell
python3 sub.py 
```

![Subscribe to MQTT Topic](https://assets.emqx.com/images/f6fa795ecafac8e476b12018345ecf60.png)

#### 发布消息

运行 MQTT 消息发布脚本 `pub.py`，我们会看到客户端成功连接并发布了 5 条消息。同时 `sub.py` 也会成功收到 5 条消息。

```shell
python3 pub.py 
```

![Publish MQTT Messages](https://assets.emqx.com/images/cff08d70fe77b9a2391672f3816ba260.png)

## Paho MQTT Python 客户端的常见问题

### 如果不执行 loop_stop() 会发生什么？ 

Loop_stop() 用于停止 MQTT 客户端的消息循环并将其标记为已停止。此过程可确保客户端正常关闭，从而降低消息丢失、连接泄漏和异常程序行为等问题的风险。

例如，在本文提供的 pub.py 示例中，删除 `client.loop_stop()` 方法可能会导致 `sub.py` 脚本接收到的消息少于 5 条。

因此，正确使用 loop_stop() 方法来确保 MQTT 客户端正常关闭并防止由于未关闭连接而可能出现的任何潜在问题至关重要。

### connect_async() 是用来做什么的?

`connect_async()` 在 MQTT 客户端应用程序需要长期 MQTT 连接或需要在后台保持 MQTT 连接处于活动状态而不阻塞主线程的情况下很有用。其主要使用场景有： 

- **长期 MQTT 连接**：`connect_async()` 有助于防止需要长期 MQTT 连接的 MQTT 客户端应用程序停滞或无响应，例如在工业应用程序中。
- **网络连接不稳定**：在网络连接不确定或不稳定的环境中，可以使用 `connect_async()` 通过重试和延迟建立连接来提高应用程序的可靠性。
- **频繁的连接和参数更改**：当连接参数或其他设置频繁更改时，`connect_async()` 有助于提高应用程序响应能力并防止卡顿。
- **后台 MQTT 连接**：`connect_async()` 允许在应用程序运行其他进程时在后台建立 MQTT 连接，从而增强用户体验。

## 结语

本文介绍了如何使用 paho-mqtt 客户端连接到免费的公共 MQTT Broker。我们成功实现了连接过程，使用 `publish()` 方法将消息从测试客户端发送到 Broker，并使用 `subscribe()` 方法从 Broker 订阅消息。

接下来，您可以查看由 EMQ 提供的《[MQTT 教程](https://www.emqx.com/zh/mqtt-guide)》系列，了解 MQTT 协议的特性，探索更多 MQTT 的高级应用，进行 MQTT 应用与服务开发。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
