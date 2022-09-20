[树莓派](https://www.raspberrypi.org/) 由英国树莓派基金会开发，是一款基于 ARM 的微型计算机主板。该主板提供 USB 接口和以太网接口，可以连接键盘、鼠标和网线，该主板具备 PC 的基本功能，同时树莓派集成了 Wi-Fi，蓝牙以及大量 GPIO，被广泛运用在教学、家庭娱乐、物联网等。 

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它适用于硬件资源有限的设备及带宽有限的网络环境。因此，MQTT 协议广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。 

在此项目中，我们将在树莓派上使用 Python 编写简单的 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)，并实现该客户端与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、取消订阅、收发消息等功能。 



## 环境搭建 

### 安装 Python3

本项目使用 Python3 进行开发，一般情况下，树莓派系统会内置 Python3，如果不确定系统内是否已经安装，可以使用下面的命令进行确认。

```
python3 --version 
```

如果显示 Python 3.x.x（x 表示数字）则表示已经安装，否则请使用 apt 命令安装（或跟随 [Python3 安装指南](https://wiki.python.org/moin/BeginnersGuide/Download) 操作 ）。

```
sudo apt install python3 
```

### 安装 MQTT 客户端库 

为了方便连接到 MQTT 服务器，我们需要安装 `paho-mqtt` 库。可以选择以下两种方法之一进行安装。

**使用源码安装** 

```
git clone https://github.com/eclipse/paho.mqtt.python 
cd paho.mqtt.python 
python3 setup.py install
```

**使用 pip3 安装** 

```
pip3 install paho-mqtt 
```



## MQTT 的使用 

### 连接 MQTT 服务器 

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下： 


* Broker: **broker.emqx.io** 
* TCP Port: **1883** 
* Websocket Port: **8083** 

如果有需要，您也可以使用 docker 在本地快速安装 EMQX 服务器。 

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 18083:18083 emqx/emqx 
```

**连接示例代码** 

```python
# test_connect.py 
import paho.mqtt.client as mqtt 

# 回调函数。当尝试与 MQTT broker 建立连接时，触发该函数。
# client 是本次连接的客户端实例。
# userdata 是用户的信息，一般为空。但如果有需要，也可以通过 user_data_set 函数设置。
# flags 保存服务器响应标志的字典。
# rc 是响应码。
# 一般情况下，我们只需要关注 rc 响应码是否为 0 就可以了。
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client() 
client.on_connect = on_connect 
client.connect("broker.emqx.io", 1883, 60) 
client.loop_forever() 
```

将上面的代码保存为 test_connect.py 文件，并运行 

```
python3 test_connect.py 
```

我们在 on_connect 函数里对响应码进行了判断，为 0 则输出 `Connected success` 表示连接成功。如果返回的是其它数字，我们就需要对照下面的响应码进行判断。

> ```undefined
> 0: 连接成功
> 1: 连接失败-不正确的协议版本
> 2: 连接失败-无效的客户端标识符
> 3: 连接失败-服务器不可用
> 4: 连接失败-错误的用户名或密码
> 5: 连接失败-未授权
> 6-255: 未定义
> 如果是其它问题，可以检查网络情况，或者确认是否安装了 `paho-mqtt`。 
> ```

在 MQTT 协议的概念中，消息是通过主题传递的，比如设备 A 向主题 T 发送消息，那么只有订阅了主题 T 的设备才能接收到。所以仅仅接入 MQTT 服务器并没有太大意议，要完整地使用 MQTT 服务，我们还需要知道如何订阅和发布消息。

### 订阅消息 

打开任意编辑器，输入下面的代码，并保存为 subscriber.py 文件： 

```python
# subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅，需要放在 on_connect 里
    # 如果与 broker 失去连接后重连，仍然会继续订阅 raspberry/topic 主题
    client.subscribe("raspberry/topic")

# 回调函数，当收到消息时，触发该函数
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 设置遗嘱消息，当树莓派断电，或者网络出现异常中断时，发送遗嘱消息给其他客户端
client.will_set('raspberry/status',  b'{"status": "Off"}')

# 创建连接，三个参数分别为 broker 地址，broker 端口号，保活时间
client.connect("broker.emqx.io", 1883, 60)

# 设置网络循环堵塞，在调用 disconnect() 或程序崩溃前，不会主动结束程序
client.loop_forever()
```

调用 `subscribe()` 函数，可以让树莓派订阅一个主题。在上面的代码中，我们使用它订阅了 `raspberry/topic` 主题，并监听消息。

另外，我们还使用 `will_set()` 设置了遗嘱消息。 遗嘱消息是 MQTT 的一个特性，当设备在意外断开网络连接后，会向某个特定的主题发送消息。通过这个特性，我们可以得知树莓派是否断电，或者出现网络异常。 

### 发布消息 

打开任意编辑器，输入下面的代码，并保存为 publisher.py 文件： 

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

# 每间隔 1 秒钟向 raspberry/topic 发送一个消息，连续发送 5 次
for i in range(5):
  	# 四个参数分别为：主题，发送内容，QoS, 是否保留消息
    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_forever()
```

调用 `publish()` 函数，可以向一个主题发送消息。在上面的代码中，我们使用了它向主题 `raspberry/topic` 发送消息。其中参数 QoS 是另一个 MQTT 特性，如果你想了解更多 QoS 的内容，可以查看 [MQTT QoS（服务质量）介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)，这里我们暂且设为 0。



## 测试 

我们使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 进行以下测试。 

### 测试订阅消息 

运行 Python 代码，并主动发送一个消息。 

1. 打开终端，运行 Python 代码，监听消息 。

   ```
   python3 subscriber.py
   ```

2. 使用 MQTT X 客户端与 MQTT 服务器建立连接，并向主题 `raspberry/topic` 发送消息 。

   ![7B5ORTmqFbJJj6mM__thumbnail.png](https://assets.emqx.com/images/e3ae859641f45129c13bfe3ecc6d83d8.png)

3. 查看树莓派终端信息，将会看到已成功接收到 MQTT X 发布的消息。

   ![ZKNT7l232qHsjQYC__thumbnail.png](https://assets.emqx.com/images/287177254b6de742ebd97e30f55206ab.png)

### 测试发布消息 

1. 在 MQTT X 客户端中订阅 `raspberry/topic` 主题 。

2. 在终端运行 Python 代码。

   ![k19xv59gQdqnpPog__thumbnail.png](https://assets.emqx.com/images/713e54f2afa1bbafafc8237fea0ccb90.png)

3. 在 MQTT X 客户端中，查看树莓派发送的消息。
   
   ![mp39coxpnEprWOE6__thumbnail.png](https://assets.emqx.com/images/a1205fe2264876782a9818f17203f671.png)

### 测试遗嘱消息 

接下来测试一下遗嘱消息是否设置成功。


1. 在 MQTT X 客户端中，订阅 `raspberry/status`。

   ![XKo2GYFsqSLc7nVH__thumbnail.png](https://assets.emqx.com/images/5979c93e7967c7350846b56521b8a27e.png)

2. 中断程序，或者断开树莓派的网络。 

3. 在 MQTT X 客户端中，查看 `raspberry/status` 主题接收到的消息。

   ![RXNIVuQ7HK0z05RV__thumbnail.png](https://assets.emqx.com/images/5d6e7497c02b48f1b1e2923725e015fc.png)



## 总结 

我们完成了在树莓派上使用 [Python MQTT 客户端库](https://www.emqx.com/zh/blog/comparision-of-python-mqtt-client) `paho-mqtt ` 编写测试客户端， 并实现了测试客户端与 MQTT 服务器的连接、订阅、取消订阅、收发消息等功能。

至此，您已经学会了如何简单的使用 MQTT 服务，虽然这只是 MQTT 服务的一小部分，但也足够完成很多有意思的事，比如：

1. 使用手机发送 MQTT 消息，远程控制树莓派。
2. 定时将树莓派的设备信息发送到 MQTT 服务器，通过手机接收消息，可以进行全天候监控。
3. 可以通过将树莓派接入 MQTT 服务器，并配合各类传感器及 ESP 模块创建很多有趣的物联网应用。

接下来我们将会陆续发布更多关于物联网开发及树莓派的相关文章，敬请关注。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
