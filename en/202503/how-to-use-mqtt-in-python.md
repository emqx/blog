## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a lightweight messaging protocol designed for IoT (Internet of Things) applications using a publish/subscribe model. It ensures reliable, real-time communication with minimal code and bandwidth, making it ideal for resource-constrained devices and low-bandwidth networks. Industries like IoT, mobile internet, Internet of Vehicles (IoV), and power systems widely adopt MQTT for its efficiency.

Python, a versatile and easy-to-use programming language, is a top choice for IoT development thanks to its extensive libraries and ability to process large datasets. From smart home automation to environmental monitoring and industrial control, Python shines in IoT projects. Its compatibility with microcontrollers further enhances its value for building IoT solutions.

In this guide, we’ll explore how to use the **Paho MQTT Python client** to connect an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) to an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), subscribe to topics, publish messages, and more in a Python project. Whether you're new to **Python MQTT** or looking to refine your skills, this tutorial has you covered.

## Why Choose Paho MQTT Python Client?

The Paho MQTT Python Client supports [MQTT versions 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), 3.1.1, and 3.1, running on Python 2.7 or 3.x. It offers a simple client class and helper functions to easily publish one-off messages to an MQTT server.

Here’s why it’s the top MQTT client library for Python users:  

- Open-source and backed by a strong community.  
- Simple API for connecting, publishing, and subscribing to MQTT messages.  
- Supports multiple security options.  
- Regularly updated to keep pace with IoT advancements.

Interested in other Python MQTT libraries? See our [comparison blog post](https://www.emqx.com/en/blog/comparision-of-python-mqtt-client) for details.

## Real-World Python MQTT Examples

Python MQTT powers many IoT solutions. For instance, you can use it to:  

- Monitor temperature in a smart home and send alerts via MQTT.  
- Control industrial machines remotely with real-time data.  
- Track vehicle locations in an IoV system using a Python MQTT client.  

These examples show how lightweight and versatile MQTT can be with Python.

## Python MQTT Project Preparation

### Python Version

This project uses Python 3.11 and was tested with version 3.11.8. To check your Python version, run this command:  

```shell
$ python3 --version             
Python 3.11.8
```

### Install The Paho MQTT Client

`paho-mqtt` released version 2.0.0 in February 2024, which includes some significant updates compared to version 1.X. This article will primarily demonstrate code for version 1.X, but will also provide corresponding code for version 2.0.0, allowing readers to choose the appropriate version of `paho-mqtt`.

> For detailed changes in version 2.0.0, please refer to the documentation: [https://eclipse.dev/paho/files/paho.mqtt.python/html/migrations.html](https://eclipse.dev/paho/files/paho.mqtt.python/html/migrations.html)

Install the `paho-mqtt` 1.X using Pip.

```shell
pip3 install "paho-mqtt<2.0.0"
```

Install the `paho-mqtt` 2.X using Pip.

```shell
pip3 install paho-mqtt
```

>If you need help installing Pip, please refer to the official documentation at [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/). This resource provides detailed instructions for installing Pip on different operating systems and environments.

## Set Up an MQTT Broker for Python MQTT

You'll need an MQTT broker to communicate and test your code. We suggest EMQX Serverless, a fully managed MQTT service. It connects millions of IoT devices, integrates with databases and systems, and deploys in minutes across 20+ regions on AWS, Google Cloud, or Azure for fast, global access.  

<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

For simplicity, this guide uses a [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker):  

- Server: `broker.emqx.io`

- TCP Port: `1883`

- WebSocket Port: `8083`

- SSL/TLS Port: `8883`

- Secure WebSocket Port: `8084`


## Paho MQTT Python Client Usage

### Import the Paho MQTT client

```python
from paho.mqtt import client as mqtt_client
```

### Create an MQTT Connection

#### TCP Connection

To set up an MQTT connection, define the broker address, port, and topic. You can also create a random client ID using Python’s `random.randint` function:

```python
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
```

> To learn more, please check out the blog [How to Set Parameters When Establishing an MQTT Connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).

Next, we need to write the `on_connect` callback function for connecting the broker. This function is called after the client has successfully connected, and we can check the connection status using the `rc` parameter. Typically, we'll also create a client object that connects to `broker.emqx.io` at the same time.

```python
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

#### Auto Reconnect

Automatic reconnection in [MQTT client libraries](https://www.emqx.com/en/mqtt-client-sdk) ensures reliable communication between devices and brokers in unstable network conditions without human intervention. It allows clients to resume publishing or subscribing to topics when the network connection is interrupted, or the broker is temporarily unavailable, making it crucial for high-reliability applications such as automotive systems and medical equipment.

The auto reconnect code for the Paho MQTT client is as follows:

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

Then, set it as the `on_disconnect` of the client object.

```python
client.on_disconnect = on_disconnect
```

The full code for client auto reconnect can be found at [GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-Python3/pub_sub_tcp.py).

#### TLS/SSL

Using TLS in MQTT can ensure the confidentiality and integrity of information, preventing information leakage and tampering. TLS authentication can be classified into one-way authentication and two-way authentication.

**One-way authentication**

The one-way authentication code for the Paho MQTT client is as follows:

```python
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
```

**Two-way authentication**

The two-way authentication code for the Paho MQTT client is as follows:

```python
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

## Complete Python MQTT Code Examples

### Publishing MQTT Messages

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

### MQTT Subscription

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

## Testing Your Python MQTT Demo

#### Subscribe

Running the MQTT subscription script `sub.py`, we will see the client successfully connected and started waiting for the publisher to publish messages.

```shell
python3 sub.py
```

![Subscribe to MQTT Topic](https://assets.emqx.com/images/f6fa795ecafac8e476b12018345ecf60.png)

#### Publish Messages

Running the MQTT message publishing script `pub.py`, we will see the client successfully connected and publish five messages. At the same time, sub.py will also successfully receive five messages.

```shell
python3 pub.py
```

![Publish MQTT Messages](https://assets.emqx.com/images/cff08d70fe77b9a2391672f3816ba260.png)

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

This guide walked you through using the Paho MQTT client to connect to a free public MQTT broker. You’ve set up a connection, sent messages with `publish()`, and received them with `subscribe()`.  

You can check out the [MQTT Guide: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.

**Related resources:**

- [MQTT Broker: How It Works, Popular Options, and Quickstart](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)
- [Free MQTT Broker: Exploring Options and Choosing the Right Solution](https://www.emqx.com/en/blog/free-mqtt-broker)
- [MQTT Client Tools 101: A Beginner's Guide](https://www.emqx.com/en/resources/mqtt-client-tools-101)
- [Mastering MQTT: Your Ultimate Tutorial for MQTT](https://www.emqx.com/en/resources/your-ultimate-tutorial-for-mqtt)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
