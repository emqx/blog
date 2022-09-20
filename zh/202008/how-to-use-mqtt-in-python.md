[Python](https://www.python.org/) 是一种广泛使用的解释型、高级编程、通用型编程语言。Python 的设计哲学强调代码的可读性和简洁的语法（尤其是使用空格缩进划分代码块，而非使用大括号或者关键词）。Python 让开发者能够用更少的代码表达想法，不管是小型还是大型程序，该语言都试图让程序的结构清晰明了。[^1]

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

本文主要介绍如何在 Python 项目中使用 **paho-mqtt** 客户端库 ，实现客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。



## 项目初始化

本项目使用 Python 3.6 进行开发测试，读者可用如下命令确认 Python 的版本。

```
➜  ~ python3 --version             
Python 3.6.7
```

#### 选择 MQTT 客户端库

[paho-mqtt](https://www.eclipse.org/paho/clients/python/) 是目前 Python 中使用较多的 MQTT 客户端库，它在 Python 2.7 或 3.x 上为客户端类提供了对 MQTT v3.1 和 v3.1.1 的支持。它还提供了一些帮助程序功能，使将消息发布到 MQTT 服务器变得非常简单。

#### Pip 安装 Paho MQTT 客户端

Pip 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。

```bash
pip3 install -i https://pypi.doubanio.com/simple paho-mqtt
```



## Python MQTT 使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

#### 导入 Paho MQTT客户端

```python
from paho.mqtt import client as mqtt_client
```

#### 设置 MQTT Broker 连接参数

设置 MQTT Broker 连接地址，端口以及 topic，同时我们调用 Python  `random.randint` 函数随机生成 MQTT 客户端 id。

```python
broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
```

#### 编写 MQTT 连接函数

编写连接回调函数 `on_connect`，该函数将在客户端连接后被调用，在该函数中可以依据 `rc` 来判断客户端是否连接成功。通常同时我们将创建一个 MQTT 客户端，该客户端将连接到 `broker.emqx.io`。

```python
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

### 发布消息

首先定义一个 while 循环语句，在循环中我们将设置每秒调用 MQTT 客户端 `publish` 函数向 `/python/mqtt` 主题发送消息。

```python
 def publish(client):
     msg_count = 0
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
```

### 订阅消息

编写消息回调函数 `on_message`，该函数将在客户端从 MQTT Broker 收到消息后被调用，在该函数中我们将打印出订阅的 topic 名称以及接收到的消息内容。

```python
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```

### 完整代码

**消息发布代码**

```python
# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
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


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

```

**消息订阅代码**

```python
# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
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

#### 消息发布

运行 MQTT 消息发布代码，我们将看到客户端连接成功，并且成功将消息发布。

```bash
python3 pub.py
```

![pub.png](https://assets.emqx.com/images/e4b472134f5c648220a04d29472bfecb.png)

#### 消息订阅

运行 MQTT 消息订阅代码，我们将看到客户端连接成功，并且成功接收到发布的消息。

```bash
python3 sub.py
```

![sub.png](https://assets.emqx.com/images/770ba0ce419f2430db94d9e90cb30250.png)



## 总结

至此，我们完成了使用 **paho-mqtt** 客户端连接到 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。

与 C ++ 或 Java 之类的高级语言不同，Python 比较适合设备侧的业务逻辑实现，使用 Python 您可以减少代码上的逻辑复杂度，降低与设备的交互成本。我们相信在物联网领域 Python  将会有更广泛的应用。

接下来我们将会陆续发布更多关于物联网开发及 Python 的相关文章，敬请关注。



[^1]: https://zh.wikipedia.org/wiki/Python



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
