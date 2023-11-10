## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol for IoT in [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), offering reliable real-time communication with minimal code and bandwidth. It is especially beneficial for devices with limited resources and low-bandwidth networks, making it widely adopted in IoT, mobile internet, IoV, and power industries.

Python is widely used in IoT for its versatility, ease of use and vast libraries. It's ideal for smart home automation, environmental monitoring and industrial control due to its ability to handle large amounts of data. Python is also compatible with microcontrollers, making it a valuable tool for developing IoT devices.

This article mainly introduces how to use the **paho-mqtt** client and implement connection, subscribe, messaging, and other functions between the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), in the Python project.



## Why Choose Paho MQTT Python Client?

The [Paho Python Client](https://github.com/eclipse/paho.mqtt.python) provides a client class with support for MQTT v5.0, MQTT v3.1.1, and v3.1 on Python 2.7 or 3.x. It also provides some helper functions to make publishing one off messages to an MQTT server very straightforward.

As the most popular MQTT client library in the Python community, Paho MQTT Python Client has the following advantages:

1. Open-source and community-supported.
2. Easy-to-use API for connecting to MQTT servers and publishing/subscribing to MQTT messages.
3. Supports various security mechanisms.
4. Actively developed and maintained to stay relevant in the rapidly evolving IoT landscape.

Want to explore more Python MQTT client libraries? Check out this [comparison blog post on Python MQTT clients](https://www.emqx.com/en/blog/comparision-of-python-mqtt-client).



## Python MQTT Project Preparation

### Python Version

This project has been developed and tested using Python 3.6. To confirm that you have the correct Python version installed, you can use the following command.

```vim
$ python3 --version             
Python 3.6.7
```

### Install The Paho MQTT Client

Install the paho-mqtt library using Pip.

```cmake
pip3 install paho-mqtt
```

>If you need help installing Pip, please refer to the official documentation at [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/). This resource provides detailed instructions for installing Pip on different operating systems and environments.



## Prepare an MQTT Broker

Before proceeding, please ensure you have an MQTT broker to communicate and test with. We recommend you use EMQX Cloud.

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service that can connect to a large number of IoT devices and integrate various databases and business systems. With EMQX Cloud, you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simplify the process:

- Server: `broker.emqx.io`

- TCP Port: `1883`

- WebSocket Port: `8083`

- SSL/TLS Port: `8883`

- Secure WebSocket Port: `8084`


## Paho MQTT Python Client Usage

### Import the Paho MQTT client

```axapta
from paho.mqtt import client as mqtt_client
```

### Create an MQTT Connection

#### TCP Connection

We need to specify the broker address, port, and topic for the MQTT connection. Additionally, we can generate a random client id for the connection using the Python random.randint function.

```ini
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
```

> To learn more, please check out the blog [How to Set Parameters When Establishing an MQTT Connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).

Next, we need to write the `on_connect` callback function for connecting the broker. This function is called after the client has successfully connected, and we can check the connection status using the `rc` parameter. Typically, we'll also create a client object that connects to `broker.emqx.io` at the same time.

```reasonml
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

#### Auto Reconnet

Automatic reconnection in [MQTT client libraries](https://www.emqx.com/en/mqtt-client-sdk) ensures reliable communication between devices and brokers in unstable network conditions without human intervention. It allows clients to resume publishing or subscribing to topics when the network connection is interrupted, or the broker is temporarily unavailable, making it crucial for high-reliability applications such as automotive systems and medical equipment.

The auto reconnect code for the Paho MQTT client is as follows:

```
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

Then, set it as the `on_disconnect` of the client object.

```
client.on_disconnect = on_disconnect
```

The full code for client auto reconnect can be found at [GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-Python3/pub_sub_tcp.py).

#### TLS/SSL

Using TLS in MQTT can ensure the confidentiality and integrity of information, preventing information leakage and tampering. TLS authentication can be classified into one-way authentication and two-way authentication.

**One-way authentication**

The one-way authentication code for the Paho MQTT client is as follows:

```
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
```

**Two-way authentication**

The two-way authentication code for the Paho MQTT client is as follows:

```
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(
        ca_certs='./server-ca.crt',
        certfile='./client.crt',
        keyfile='./client.key'
    )
```

### Publish Messages

Create a while loop that sends a message every second to the topic `/python/mqtt`, and exits the loop after sending five messages.

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

### Subscribe

Create the message callback function `on_message`, triggered once the client receives messages from the MQTT Broker. We will print the subscribed topic's name and the received messages within this function.

```python
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```



## Full Python MQTT Code Example

### The Code for Publishing MQTT Messages

```python
# python 3.6

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

### The Code for MQTT Subscription

```routeros
# python3.6

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

## Test

#### Subscribe

Running the MQTT subscription script `sub.py`, we will see the client successfully connected and started waiting for the publisher to publish messages.

```vim
python3 sub.py
```

![Subscribe to MQTT Topic](https://assets.emqx.com/images/f6fa795ecafac8e476b12018345ecf60.png)

#### Publish Messages

Running the MQTT message publishing script `pub.py`, we will see the client successfully connected and publish five messages. At the same time, sub.py will also successfully receive five messages.

```vim
python3 pub.py
```

![Publish MQTT Messages](https://assets.emqx.com/images/cff08d70fe77b9a2391672f3816ba260.png)

#### 

## Q&A About Paho MQTT Python Client

### What happens if loop_stop() is not executed?

The `loop_stop()` method is used to halt the MQTT client's message loop and to mark it as stopped. This process ensures a graceful shutdown of the client, reducing the risk of issues such as message loss, connection leaks, and abnormal program behavior.

For instance, in the pub.py example provided in this article, deleting the `client.loop_stop()` method may result in the `sub.py` script receiving fewer than five messages.

Therefore, it is crucial to properly use the loop_stop() method to ensure the MQTT client's graceful shutdown and prevent any potential problems that may occur due to unclosed connections.

### What is connect_async() used for?

`connect_async()` is helpful in scenarios where an MQTT client application requires long-term MQTT connections or needs to keep the MQTT connection alive in the background without blocking the main thread. Its primary use cases are:

1. **Long-term MQTT connections**: `connect_async()` helps prevent stalling or unresponsiveness of an MQTT client application that requires long-term MQTT connections, such as in industrial applications.

2. **Unstable Network Connectivity**: Using `connect_async()` in environments with uncertain or unstable network connectivity improves the application's reliability by establishing connections with retries and delays.

3. **Frequent Connections and Parameter Changes**: When connection parameters or other settings change frequently, `connect_async()` helps improve application responsiveness and prevents stutters.

4. **Background MQTT connections**: `connect_async()` allows establishing MQTT connections in the background while the application runs other processes, enhancing the user experience.

## Summary

So far, we have explained how to use the **paho-mqtt** client to connect to the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker). We have successfully implemented the connection process, sent messages from the test client to the broker using the `publish()` method, and subscribed to messages from the broker using the `subscribe()` method.

Next, you can check out the [MQTT Guide: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.

**Related resources:**

- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
