[树莓派](https://www.raspberrypi.org/) 由英国树莓派基金会开发，是一款基于 ARM 的微型计算机主板。该主板提供 USB 接口和以太网接口，可以连接键盘、鼠标和网线，该主板具备 PC 的基本功能，同时树莓派集成了 Wi-Fi、蓝牙以及大量 GPIO，被广泛运用在教学、家庭娱乐、物联网等。

[MicroPython](https://zh.wikipedia.org/wiki/MicroPython) 是 Python 3 编程语言的一个完整软件实现，用 C 语言编写，运行在 MCU（微控制器）硬件之上的完全的 Python 编译器和运行时系统，提供给用户一个交互式提示符（REPL）来立即执行所支持的命令。除了包括选定的核心 Python 库，MicroPython 还包括了给予编程者访问低层硬件的模块，是 Python 3 语言的精简实现 ，包括 Python 标准库的一小部分，经过优化可在微控制器和受限环境中运行。

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的轻量级物联网消息传输协议 ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它适用于硬件资源有限的设备及带宽有限的网络环境。因此，MQTT 协议广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。

本文将介绍如何在树莓派上使用 MicroPython 编写简单的 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)，并实现该客户端与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、发布等功能。



## 环境搭建

1. 安装 MicroPython

   本项目使用 MicroPython 进行开发，可以使用下面的命令进行安装。

   ```
   sudo apt-get update
   # 安装 MicroPython
   sudo apt-get -y install micropython
   ```

   安装完成后，在终端执行 micropython，如果显示 MicroPython x.x.x（x 表示数字）则表示已经安装成功。

   ![MicroPython](https://assets.emqx.com/images/9a4dae4baa22fa6531e09cfa7cb55c84.png)

2. 安装 MQTT 客户端库

   为了方便连接到 MQTT 服务器，我们需要安装 `umqtt.simple` 库。

   ```
   micropython -m upip install umqtt.simple
   ```


## 连接 MQTT 服务器

本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 物联网云平台 - EMQX Cloud](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: `broker.emqx.io`
- TCP Port: `1883`
- Websocket Port: `8083`



## 订阅消息

打开任意编辑器，输入下面的代码，并保存为 sub.py 文件：

```
# sub.py
import time
from umqtt.simple import MQTTClient

# 定义 sub 客户端的连接信息
SERVER="broker.emqx.io"
ClientID = f'raspberry-sub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

def sub(topic, msg):
    # 在回调函数打印主题和消息
    print('received message %s on topic %s' % (msg, topic))

def main(server=SERVER):
    # 创建连接，参数分别为客户端 ID，broker 地址，broker 端口号，认证信息
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.set_callback(sub)
    client.connect()
    print('Connected to MQTT Broker "%s"' % (server))
    # 如果与 broker 失去连接后重连，仍然会继续订阅 raspberry/topic 主题
    client.subscribe(topic)
    while True:
        if True:
            client.wait_msg()
        else:
            client.check_msg()
            time.sleep(1)

if __name__ == "__main__":
    main()
```



## 发布消息

打开任意编辑器，输入下面的代码，并保存为 pub.py 文件：

```
# pub.py
import time
from umqtt.simple import MQTTClient

# 定义 pub 客户端的连接信息
server="broker.emqx.io"
ClientID = f'raspberry-pub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

# 创建连接，参数分别为客户端 ID，broker 地址，broker 端口号，认证信息
def connect():
    print('Connected to MQTT Broker "%s"' % (server))
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.connect()
    return client

def reconnect():
    # 若无法连接到 broker，打印一条消息以通知连接不成功，并且等待 5 秒发起重连
    print('Failed to connect to MQTT broker, Reconnecting...' % (server))
    time.sleep(5)
    client.reconnect()

# 若能连接到 broker，调用 connect()，反之调用 reconnect()
try:
    client = connect()
except OSError as e:
    reconnect()

# 每隔 1 秒给主题 raspberry/mqtt 发送一条消息
while True:
  print('send message %s on topic %s' % (msg, topic))
  client.publish(topic, msg, qos=0)
  time.sleep(1)
```

在上面的代码中，我们调用 publish() 函数向主题 raspberry/mqtt 发送消息。其中参数 QoS 是另一个 MQTT 特性，如果你想了解更多 QoS 的内容，可以查看 [MQTT QoS（服务质量）介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)，本示例中我们设置为 0。



## 测试

我们使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 进行以下测试。

### 测试订阅消息

运行 MicroPython 代码，并主动发送一个消息。

1. 打开终端，运行 MicroPython 代码，监听消息 。

   ```
   micropython sub.py
   ```

   ![运行订阅客户端](https://assets.emqx.com/images/0e20dafbe8acf5be38d66f91f97d9c2a.png)

2. 使用 MQTT X 客户端与 MQTT 服务器建立连接，并向主题 raspberry/mqtt 发送消息 。

   ![MQTT 消息发布](https://assets.emqx.com/images/70f2482e232882d8ced2c526f87a0dc3.png)

3. 查看树莓派终端信息，将会看到已成功接收到 MQTT X 发布的消息。

   ![MQTT 消息接收](https://assets.emqx.com/images/5b973b646249741071e3e1f2560eabd0.png)


### 测试发布消息

1. 在 MQTT X 客户端中订阅 `raspberry/mqtt` 主题 。

2. 在终端运行 MicroPython 代码 ，发布消息。

   ```
   micropython pub.py
   ```

   ![MQTT 消息发布](https://assets.emqx.com/images/558d9410fbff971b58b148bf133ff29f.png)

3. 在 MQTT X 客户端中，查看树莓派发送的消息。

   ![MQTT X 接收消息](https://assets.emqx.com/images/04843f182ab1c26fdd30b2a42b1e1a00.png)


## 结语

以上就是在树莓派上使用 MicroPython 进行编程的简单示例。我们通过 MicroPython umqtt.simple 实现了一个简单的测试客户端，并完成了该客户端与 MQTT 服务器的连接与消息收发。 MQTT 最大优点在于以极少的代码和有限的带宽，为连接远程设备提供实时可靠的消息服务，而树莓派则是一个体积小、发热低、能耗低、相对全面的硬件模块。二者相结合，即使是在微控制器或是受限环境中，也可助您开发出更多创新应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
