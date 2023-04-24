随着人工智能、大数据兴起的，Python 凭借着优雅的语言风格，丰富的库，以及平缓的入门曲线，搭上了时代的顺风车，成为了最热门的计算机编程语言之一，开始深入到物联网等各个领域中。

Python 上有许多优秀的 MQTT 客户端库，借助它们，我们可以以极少量的代码开发一个 MQTT 客户端应用。

本文收集了三个常见的 [Python MQTT 客户端库](https://www.emqx.com/zh/blog/comparision-of-python-mqtt-client)，并从库的开发、使用复杂度等几个角度进行简单的对比以方便读者进行选择。同时，文章里也提供了简单的 Python 示例，您可以将示例代码复制到编缉器中直接运行（需要 Python 3.5+，并安装对应的依赖包）。



## paho-mqtt

[paho-mqtt](https://github.com/eclipse/paho.mqtt.python) 可以说是 Python MQTT 开源客户端库中的佼佼者。它由 Eclipse 基金会主导开发，除了 Python 库以外，同样支持各大主流的编程语言，比如 C++、Java、JavaScript、Golang 等。目前 Python 版本已经实现了 3.1 和 3.1.1 [MQTT 协议](https://www.emqx.com/zh/mqtt)，在最新开发版中实现了 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5)。

在基金会的支持下，以每年一个版本的速度更新，本文发布时的最新版本为 1.5.0（于 2019 年 8 月发布）。

在 GitHub 主页上，它提供了从入门的快速实现到每一个函数的详细解读，涵盖了从初学者到高级使用者需要了解的各个部分。即使遇到超出范围的问题，在 Google 上搜索，可以得到近 20 万个相关词条，是目前最为流行的 MQTT 客户端。

得到如此多的关注度，除了稳定的代码外，还有其易用性。Paho 的接口使用非常简单优雅，您只需要少量的代码就能实现 MQTT 的订阅及消息发布。

### 安装

```
pip3 install paho-mqtt
```

或者

```
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
python3 setup.py install
```

### 订阅者

```python
import paho.mqtt.client as mqtt

# 连接的回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")
    
# 收到消息的回调函数
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_forever()
```

### 发布者

```python
import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)
for i in range(3):
    client.publish('a/b', payload=i, qos=0, retain=False)
    print(f"send {i} to a/b")
    time.sleep(1)

client.loop_forever()
```

甚至，你可以通过一行代码，实现订阅、发布。

```python
import paho.mqtt.subscribe as subscribe

# 当调用这个函数时，程序会堵塞在这里，直到有一条消息发送到 paho/test/simple 主题
msg = subscribe.simple("paho/test/simple", hostname="broker.emqx.io")
print(f"{msg.topic} {msg.payload}")
```

```python
import paho.mqtt.publish as publish

# 发送一条消息
publish.single("a/b", "payload", hostname="broker.emqx.io")
# 或者一次发送多个消息
msgs = [{'topic':"a/b", 'payload':"multiple 1"}, ("a/b", "multiple 2", 0, False)]
publish.multiple(msgs, hostname="broker.emqx.io")
```


## HBMQTT

[HBMQTT](https://github.com/beerfactory/hbmqtt) 基于 Python asyncio 开发，仅支持 3.1.1 的 MQTT 协议。由于使用 asyncio 库，开发者需要使用 3.4 以上的 Python 版本。

CPU 的速度远远快于磁盘、网络等 IO 操作，而在一个线程中，无论 CPU 执行得再快，遇到 IO 操作时，都得停下来等待读写完成，这无疑浪费了许多时间。

为了解决这个问题，Python 加入了异步 IO 的特性。在 Python 3.4 中，正式将 asyncio 纳入标准库中，并在 Python 3.5 中，加入了 async/await 关键字。用户可以很轻松的使用在函数前加入 async 关键字，使函数变成异步函数。

HBMQTT 便是建立在 asyncio 标准库之上。它允许用户显示的设置异步断点，通过异步 IO，MQTT 客户端在收取消息或发送消息时，挂起当前的任务，继续处理下一个。

不过 HBMQTT 的知名度却小得多。在 Google 上搜索，关于 HBMQTT 仅有 6000 多个词条，在 Stack Overflow  上只有 10 个提问数。这就意味着，如果选择 HBMQTT 的话你需要很强的解决问题的能力。

有意思的是，HBMQTT 本身也是一个 [MQTT 服务器](https://www.emqx.com/zh/products/emqx)。你可以通过 hbmqtt 命令一键开启。

```python
$ hbmqtt
[2020-08-28 09:35:56,608] :: INFO - Exited state new
[2020-08-28 09:35:56,608] :: INFO - Entered state starting
[2020-08-28 09:35:56,609] :: INFO - Listener 'default' bind to 0.0.0.0:1883 (max_connections=-1)
```

### 安装

```
pip3 install hbmqtt
```

或者

```
git clone https://github.com/beerfactory/hbmqtt
cd hbmqtt
python3 setup.py install
```

### 订阅者

```python
import logging
import asyncio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

async def uptime_coro():
    C = MQTTClient()
    await C.connect('mqtt://broker.emqx.io/')
    await C.subscribe([
            ('$SYS/broker/uptime', QOS_1),
            ('$SYS/broker/load/#', QOS_2),
         ])
    try:
        for i in range(1, 100):
            message = await C.deliver_message()
            packet = message.publish_packet
            print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")
        await C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        await C.disconnect()
    except ClientException as ce:
        logging.error("Client exception: %s" % ce)
        
if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
```

### 发布者

```python
import logging
import asyncio
import time
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

async def test_coro():
    C = MQTTClient()
    await  C.connect('mqtt://broker.emqx.io/')
    tasks = [
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),
    ]
    await asyncio.wait(tasks)
    logging.info("messages published")
    await C.disconnect()
    
if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
```

更多使用细节情参考官方文档：https://hbmqtt.readthedocs.io/en/latest/



## gmqtt

[gmqtt](https://github.com/wialon/gmqtt) 是由个人开发者开源的客户端库。默认支持 MQTT 5.0 协议，如果连接的 MQTT 代理不支持 5.0 协议，则会降级到 3.1 并重新进行连接。

相较于前两者，gmqtt 还属于初级开发阶段，本文发布时的版本号是 0.6.7。但它是早期支持 MQTT 5.0 的 Python 库之一，因此在网络上知名度尚可。

同样，它建立在 asyncio 库上，因此需要使用 Python 3.4 以上的版本。

### 安装

```
pip3 install gmqtt
```

或者

```
git clone https://github.com/wialon/gmqtt
cd gmqtt
python3 setup.py install
```

### 订阅者

```python
import asyncio
import os
import signal
import time
from gmqtt import Client as MQTTClient

STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected')
    
def on_message(client, topic, payload, qos, properties):
    print(f'RECV MSG: {topic} {payload}')
    
def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')
    
def on_disconnect(client, packet, exc=None):
    print('Disconnected')
    
def ask_exit(*args):
    STOP.set()

async def main(broker_host):
    client = MQTTClient("client-id")
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    
    # 连接 MQTT 代理
    await client.connect(broker_host)
    
    # 订阅主题
    client.subscribe('TEST/#')
    
    # 发送测试数据
    client.publish("TEST/A", 'AAA')
    client.publish("TEST/B", 'BBB')
    
    await STOP.wait()
    await client.disconnect()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    host = 'broker.emqx.io'
    loop.run_until_complete(main(host))
```

### 发布者

```python
import asyncio
import os
import signal
import time
from gmqtt import Client as MQTTClient

STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('TEST/#', qos=0)
    
def on_message(client, topic, payload, qos, properties):
    print(f'RECV MSG: {topic}, {payload}')
    
def on_disconnect(client, packet, exc=None):
    print('Disconnected')
    
def ask_exit(*args):
    STOP.set()
    
async def main(broker_host):
    client = MQTTClient("client-id")
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    await client.connect(broker_host)
    
    client.publish('TEST/TIME', str(time.time()), qos=1)
    
    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)
    
    host = 'broker.emqx.io'  
    loop.run_until_complete(main(host))
```



## 如何选择

在介绍完这三款 Python MQTT 客户端库之后，我们再来看看如何为自己选择合适的 MQTT 客户端库。这三个客户端各有自己的优缺点：

paho-mqtt 有着最优秀的文档，代码风格易于理解，同时有着强大的基金会支持，但目前文档的版本还不支持 MQTT 5.0。

HBMQTT 使用 asyncio 库实现，可以优化网络 I/O 带来的延迟。但是代码风格不友好，同样不支持 MQTT 5.0。

gmqtt 同样通过 asyncio 库实现，相比 HBMQTT ，代码风格友好，最重要的是，它支持 MQTT 5.0。但开发进程慢，未来前景不明。

因此，在选择时，您可以参考一下的思路：


* 如果您是正常开发，想要将其运用在生产环境中，paho-mqtt 无疑是最好的选择，其稳定性和代码易读性远远超过其它两个库。在遇到问题时，优秀的文档和互联网上大量的词条，也能帮您找到更多的解决方案。

* 对于熟练使用 asyncio 库的读者，不妨尝试一下 HBMQTT 和 gmqtt。

* 如果您想要学习、参与开源项目或者使用 MQTT 5.0， 则不妨试用一下 gmqtt，并尝试为其贡献一份代码吧。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
