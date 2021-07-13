

## 什么是异步

CPU 的速度远远快于磁盘、网络等 IO 操作，而在一个线程中，无论 CPU 执行得再快，遇到 IO 操作时，都得停下来等待读写完成，这无疑浪费了许多时间。

为了解决这个问题，Python 加入了异步 IO 的特性。在 Python 3.4 中，正式将 asyncio 纳入标准库中，并在 Python 3.5 中，加入了 async/await 关键字。用户可以很轻松的使用在函数前加入 async 关键字，使函数变成异步函数。

在 Python 的 MQTT 客户端库中，[HBMQTT](https://github.com/beerfactory/hbmqtt) 是最早支持异步 IO 的 Python MQTT 库。



## HBMQTT 库

HBMQTT 是基于 Python 编写的开源库，实现了 MQTT 3.1.1 协议，特性如下：

* 支持 QoS 0, QoS 1 以及 QoS 2 消息
* 客户端自动重连
* 支持 TCP 和 WebSocket
* 支持 SSL
* 支持插件系统

下面我们将演示如何使用 Python MQTT 异步框架 - HBMQTT，轻松实现一个具备 MQTT 发布、订阅功能的异步 Demo。



## 项目初始化

### 确定 Python 版本

本项目使用 Python 3.6 进行开发测试，读者可用如下命令确认 Python 的版本。

> 因为需要使用 async 关键字，需要确保 Python 版本不低于 Python 3.5

```shell
➜  ~ python3 --version
Python 3.6.7
```

### 使用 Pip 安装 HBMQTT 库

Pip 是 Python 的包管理工具，该工具提供了对 Python 包的查找、下载、安装和卸载功能。

```plain
pip3 install -i https://pypi.doubanio.com/simple hbmqtt
```



## 连接 MQTT 服务器

本文将使用 EMQ X 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQ X 的[MQTT 物联网云平台](https://cloud.emqx.cn/)创建。服务器接入信息如下：

* Broker: broker.emqx.io
* TCP Port: 1883
* Websocket Port: 8083

首先，导入 MQTT 客户端库。

```python
from hbmqtt.client import MQTTClient

client = MQTTClient()
# 连接服务器
client.connect('mqtt://broker.emqx.io/')
# 断开连接
client.disconnect()
```

异步写法如下：

```python
async def test_pub():
    client = MQTTClient()
    await client.connect('mqtt://broker.emqx.io/')
    await client.disconnect()
```



## 发布消息

发布消息函数为 MQTTClient 类的 publish 函数。

```python
client = MQTTClient()
# 函数的三个参数分别为主题、消息内容、QoS
client.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)
```

异步写法如下：

```
async def test_pub():
    client = MQTTClient()
    await Client.connect('mqtt://broker.emqx.io/')
    await asyncio.gather(
        client.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
    )
    logging.info("messages published")
    await Client.disconnect()
```

在这段代码中，我们将三个发送消息函数放进 asyncio 的任务列表里，它们将会依次被运行。当所有任务都完成后，断开连接。



## 订阅消息

定阅消息函数为 MQTTClient 类中的 subscribe 函数。

```python
client = MQTTClient()
# 订阅
client.subscribe([
  ('topic/0', QOS_0),
  ('topic/1', QOS_1),  
])
# 取消订阅
client.unsubscribe([
  ('topic/0', QOS_0),
]
```

异步写法如下：

```python
async def test_sub():
    client = MQTTClient()
    await client.connect('mqtt://broker.emqx.io/')
    await client.subscribe([
            ('a/b', QOS_1),
         ])
    for i in range(0, 10):
        message = await client.deliver_message()
        packet = message.publish_packet
        print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")
    await client.disconnect()
```

在这段代码中，我们在接收消息时设置了 await 等待，当代码执行到如下位置时，CPU 会先去执行其它任务，直到有消息传达，再将其打印。

```python
message = await client.deliver_message()
```

最终，程序会等待 10 次消息接收，然后关闭连接。



## 完整代码

### 消息订阅代码

```python
# sub.py
# python 3.6+

import asyncio
import logging

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


async def test_sub():
    client = MQTTClient()
    await client.connect('mqtt://broker.emqx.io/')
    await client.subscribe([
        ('a/b', QOS_1),
    ])
    for i in range(0, 10):
        message = await client.deliver_message()
        packet = message.publish_packet
        print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")
    await client.disconnect()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.run(test_sub())

```


### 消息发布代码

```python
# pub.py
# python 3.6+

import asyncio
import logging

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2


async def test_pub():
    client = MQTTClient()

    await client.connect('mqtt://broker.emqx.io/')
    await asyncio.gather(
        client.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
    )
    logging.info("messages published")
    await client.disconnect()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.run(test_pub())

```



## 测试

### 消息发布

运行 MQTT 消息发布代码，我们将看到客户端连接成功，并且成功发布消息。

![hbmqtt_pub.png](https://static.emqx.net/images/afb947f2a8af5b2b3485d43ad1bfd739.png)


如下为 MQTT X 客户端成功接收到 HBMQTT 客户端发布的消息：

![mqttx_sub.png](https://static.emqx.net/images/b16f8c811d7528ed80d98ef3ffb6ccf1.png)

### 消息订阅

运行 MQTT 消息订阅代码，我们将看到客户端连接成功，此时客户端正在等待消息进入

![running_sub_py.png](https://static.emqx.net/images/48740199e70903cc21f24360d5101a6a.png)

使用 MQTT X 客户端连接 broker.emqx.io，然后向主题 a/b 发送 10 次消息

![pub_from_mqttx.png](https://static.emqx.net/images/2d3c9a2fc3fb320b643b47f119141ec0.png)

回到终端，我们看到客户端接收并打印消息，并且在收到 10 条消息后，主动退出了程序。

![finished_sub_py.png](https://static.emqx.net/images/d7a097b207a30a45a6d7374ca13022c9.png)



## 总结

至此，我们完成了 HBMQTT 库连接到[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。通过使用 Python 异步 IO 执行消息的发送接收，可以帮助我们实现更加高效的 MQTT 客户端。

接下来我们将会陆续发布更多关于物联网开发及 Python 的相关文章，敬请关注。

