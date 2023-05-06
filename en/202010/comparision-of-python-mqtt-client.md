With the rise of artificial intelligence and big data, Python has become one of the most popular computer programming languages because of its elegant language style, rich libraries and easy to start. Also, it is starting to penetrate into various areas like IoT.

There are many excellent MQTT client libraries on Python. These clients allow us to develop an MQTT client application with very little code.

This article collects three common Python MQTT client libraries, and briefly compares them from several perspectives, such as library development and complexity of use, to facilitate the reader to select. At the same time, this article also provides simple Python examples, and you can copy the example code to an editor and run it directly (Python 3.5+ is required, and need to install the corresponding dependency package)



## paho-mqtt

[paho-mqtt](https://github.com/eclipse/paho.mqtt.python) is arguably the best of the Python MQTT open-source client libraries. It was developed under the leadership of the Eclipse Foundation, and besides the Python library, it also supports major programming languages such as C++, Java, JavaScript, Golang, etc. Currently, The Python version has implemented 3.1 and 3.1.1 [MQTT protocol](https://www.emqx.com/en/mqtt), and implemented [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) in the latest development version.

With the support of the foundation, it is updated at a rate of one version per year. The latest version was 1.5.0 (released in August 2019) when this article was published.

On the GitHub home page, it provides detailed explanations from quick implementations for getting started to each function, and covers everything that you need to know for beginners to advanced users. Even if you have an out-of-scope problem, you can use Google to search, and then you will get nearly 200,000 related entries. It is the most popular MQTT client.

It can get so much attention because of its stable code and ease of use. The interface of Paho is very simple and elegant to use, and you only need a small amount of code to implement MQTT subscriptions and messaging.

### Install

```
pip3 install paho-mqtt
```

Or

```
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
python3 setup.py install
```

### Subscriber

```python
import paho.mqtt.client as mqtt

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")
    
# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_forever()
```

### Publisher

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

You can even implement subscription and publish only through a single line of code.

```python
import paho.mqtt.subscribe as subscribe

# When this function is called, the program will block here until a message is sent to the topic paho/test/simple
msg = subscribe.simple("paho/test/simple", hostname="broker.emqx.io")
print(f"{msg.topic} {msg.payload}")
```

```python
import paho.mqtt.publish as publish

# Send a message
publish.single("a/b", "payload", hostname="broker.emqx.io")
# Or send multiple messages at once
msgs = [{'topic':"a/b", 'payload':"multiple 1"}, ("a/b", "multiple 2", 0, False)]
publish.multiple(msgs, hostname="broker.emqx.io")
```



## HBMQTT

[HBMQTT](https://github.com/beerfactory/hbmqtt) is based on Python asyncio to develop, and only supports 3.1.1 MQTT protocol. Because it uses the asyncio library, developers need to use Python 3.4 or higher.

The CPU is much faster than disks, networks, and other IO operations. However, in a thread, no matter how faster the CPU executes, it will stop and wait for reads and writes to complete when it encounters an IO operation, which wastes a lot of time.

To solve this problem, Python added the asynchronous IO feature. In Python 3.4,  asyncio was officially added to the standard library, and in Python 3.5, it added the keyword async/await. Users can easily use the keyword async in front of functions to make them asynchronous.

HBMQTT is built on top of the asyncio standard library. It allows the user to set asynchronous breakpoints explicitly. Through asynchronous IO, the MQTT client pending the current task when receives or sends messages, and continues to process the next task.

However, HBMQTT is much less well known. A Google search on HBMQTT yielded just over 6,000 entries and only 10 questions on Stack Overflow. This means that you need a strong ability for solving problems, if you choose to use HBMQTT.

Interestingly, HBMQTT is also an [MQTT broker](https://www.emqx.com/en/products/emqx). You can enable it with one click through the hbmqtt command.

```python
$ hbmqtt
[2020-08-28 09:35:56,608] :: INFO - Exited state new
[2020-08-28 09:35:56,608] :: INFO - Entered state starting
[2020-08-28 09:35:56,609] :: INFO - Listener 'default' bind to 0.0.0.0:1883 (max_connections=-1)
```

### Install

```
pip3 install hbmqtt
```

Or

```
git clone https://github.com/beerfactory/hbmqtt
cd hbmqtt
python3 setup.py install
```

### Subscriber

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

### Publisher

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

For more details, please refer to the official documentation: https://hbmqtt.readthedocs.io/en/latest/.



## gmqtt

[gmqtt](https://github.com/wialon/gmqtt) is a client library open-sourced by individual developer. MQTT 5.0 protocol is supported by default, but if the connected MQTT agent does not support 5.0 protocol, it will be downgraded to 3.1 and will reconnect.

Compared to the first two, gmqtt is still in the early stages of development, and the version is 0.6.7 when this article was published. However, it is one of the Python libraries which early support MQTT 5.0, so it is well known on the web.

It is also built on the asyncio library, so it requires Python 3.4 or later.

### Install

```
pip3 install gmqtt
```

Or

```
git clone https://github.com/wialon/gmqtt
cd gmqtt
python3 setup.py install
```

### Subscriber

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
    
    # Connectting the MQTT broker
    await client.connect(broker_host)
    
    # Subscribe to topic
    client.subscribe('TEST/#')
    
    # Send the data of test
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

### Publisher

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



## How to Choose

After introducing these three Python MQTT client libraries, let's look at how to choose the proper MQTT client library for yourself. Each of the three clients has its advantages and disadvantages:

The paho-mqtt has the best documentation, and easy-to-understand code style, and strong foundation support, but the current version of the documentation does not support MQTT 5.0.

The implementation of HBMQTT is using the asyncio library, and it can optimize the delay caused by the network I/O. However, the code style is not user-friendly and also does not support MQTT 5.0.

The gmqtt is also implemented by the asyncio library. Compared with HBMQTT, it has a more friendly code style. Most importantly, it supports MQTT 5.0, but the development process is slow and the future is uncertain.

Therefore, you can refer to the following ideas when choosing one:


* If you are a normal developer and want to use it in a production environment, paho-mqtt is undoubtedly the best choice. Its stability and code readability far exceeds that of the other two libraries. When you get some problems, the excellent documentation and a large number of entries on the Internet will also help you to find more solutions.
* For the readers who are familiar with the asyncio library, you can try HBMQTT and gmqtt.
* If you want to learn or participate in an open-source project, or use MQTT 5.0, try gmqtt and try submitting a pull request for it.


## Other Articles in This Series

- [How to Use MQTT in Python (Paho)](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)

- [Python MQTT Asynchronous Framework - HBMQTT](https://www.emqx.com/en/blog/python-async-mqtt-client-hbmqtt)

- [How to Use MQTT in The Django Project](https://www.emqx.com/en/blog/how-to-use-mqtt-in-django)

- [How to use MQTT in Flask](https://www.emqx.com/en/blog/how-to-use-mqtt-in-flask)

- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)




<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
