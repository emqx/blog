## What is asynchronous

The speed of the CPU is much faster than the disk, network, and other IO operations. However, in a thread, no matter how fast the CPU is executing, when it encounters an IO operation, it has to stop and wait for the read/write to complete, which undoubtedly wastes a lot of time.

To solve this problem, Python added the feature of asynchronous IO. In Python 3.4, asyncio was formally included in the standard library, and in Python 3.5, the async/await keyword was added. Users can easily make functions becoming asynchronous functions by adding the async keyword to the front of the function.

In the MQTT client libraries for Python, [HBMQTT](https://github.com/beerfactory/hbmqtt) was the first Python MQTT library supporting asynchronous IO.



## HBMQTT Library

HBMQTT is an open source library written on Python that implements the MQTT 3.1.1 protocol. Features are as follows:

* Support for QoS 0, QoS 1, and QoS 2 messages
* The client will automatically reconnect
*  Support for TCP and WebSocket
*  Support for SSL
* Support for plugin systems

We will demonstrate how to use the Python MQTT asynchronous framework - HBMQTT to easily implement an asynchronous demo with MQTT publish and subscribe features.



## Project Initialisation

### Determining Python versions

This project was developed and tested using Python 3.6. Users can use the following command to confirm the version of Python.  

> You need to make sure that the version of Python is not lower than Python 3.5 because you need to use the async keyword.

```shell
➜  ~ python3 --version
Python 3.6.7
```

### Using Pip to install the HBMQTT library

Pip is the management tool for Python packages. This tool provides functions for finding, downloading, installing, and uninstalling Python packages.

```plain
pip3 install -i https://pypi.doubanio.com/simple hbmqtt
```



## Connect to the MQTT broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service is created based on the [IoT cloud platform](https://www.emqx.com/en/cloud) of EMQX. The information of broker access is as follows:

* Broker: broker.emqx.io
* TCP Port: 1883
* Websocket Port: 8083

First, import the MQTT client library.

```python
from hbmqtt.client import MQTTClient

client = MQTTClient()
# Connect to the broker
client.connect('mqtt://broker.emqx.io/')
# Disconnect
client.disconnect()
```

The asynchronous function is written as follows:

```python
async def test_pub():
    client = MQTTClient()
    await client.connect('mqtt://broker.emqx.io/')
    await client.disconnect()
```



## Publish Messages

The publish function is the publish function of the MQTTClient class.

```python
client = MQTTClient()
# The three parameters of the function are the topic, the message content, and the QoS
client.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)
```

The asynchronous function is written as follows:

```
async def test_pub():
    client = MQTTClient()
    await Client.connect('mqtt://broker.emqx.io/')
    await asyncio.gather(
        client.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1),
        client.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
    )
    logging.info("messages published")
    await Client.disconnect()
```

In this code, we put these three sending message functions into the task list of asyncio, and they will be executed in turn. When all tasks have been completed, the connection is disconnected.



## Subscribe

The subscribe function is the subscribe function in the MQTTClient class.

```python
client = MQTTClient()
# Subscribe
client.subscribe([
  ('topic/0', QOS_0),
  ('topic/1', QOS_1),  
])
# Unsubscribe
client.unsubscribe([
  ('topic/0', QOS_0),
]
```

The asynchronous function is written as follows:

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
        print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")
    await client.disconnect()
```

In this code, we set await when receiving messages, so when the code gets to the following position, the CPU will perform other tasks first until the message is delivered and then print it. 

```python
message = await client.deliver_message()
```

Finally, the program will wait 10 times for receiving messages and then closes the connection.



## Complete Code

### Code for subscribing to messages

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


### Code for publishing messages

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



## Tests

### Publish messages

Execute the MQTT message publishing code and we will see that the client connected successfully and published the message successfully.

![hbmqtt_pub.png](https://assets.emqx.com/images/afb947f2a8af5b2b3485d43ad1bfd739.png)


The following is that the [MQTT X](https://mqttx.app/) client successfully received the messages published by the HBMQTT client.

![mqttx_sub.png](https://assets.emqx.com/images/b16f8c811d7528ed80d98ef3ffb6ccf1.png)

### Subscribe

Executing the MQTT message subscription code, we will see that the client is successfully connected and is waiting for the message to come in.

![running_sub_py.png](https://assets.emqx.com/images/48740199e70903cc21f24360d5101a6a.png)

Use the MQTT X client to connect to broker.emqx.io and then send a message 10 times to topic a/b.

![pub_from_mqttx.png](https://assets.emqx.com/images/2d3c9a2fc3fb320b643b47f119141ec0.png)

Back in the terminal, we see that the client receives and prints messages. Also, it will actively exits the program after receiving 10 messages.

![finished_sub_py.png](https://assets.emqx.com/images/d7a097b207a30a45a6d7374ca13022c9.png)



## Summary

So far, we have completed connecting the HBMQTT library to the [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) and implemented the connection, message publishing, and subscription between the test client and the MQTT broker. We can implement a more effective MQTT client by using Python asynchronous IO to perform the sending and receiving of messages. 

We will continue to publish more articles on IoT development and Python, so stay tuned for more.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
