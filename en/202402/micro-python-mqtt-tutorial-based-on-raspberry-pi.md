## Introduction

[MQTT](https://www.emqx.com/en/mqtt-guide) is a lightweight messaging protocol based on a publish/subscribe model that provides real-time reliable messaging to connected devices with minimal code and bandwidth, making it suitable for devices with limited hardware resources and network environments with limited bandwidth. It is widely used in IoT, Mobile Internet, Smart Hardware, Telematics, Power, Energy and other industries.

MicroPython is a complete software implementation of the Python 3 programming language, written in C and optimized for a full Python compiler and runtime system running on top of MCU (microcontroller unit) hardware, providing the user with an interactive prompt (REPL) to immediately execute the supported commands. In addition to selected core Python libraries, MicroPython includes modules that give programmers access to low-level hardware, and is a streamlined implementation of the Python 3 language that includes a small portion of the Python standard library optimized to run on microcontrollers and in constrained environments.

In this article, we will discuss how to write a simple [MQTT client](https://www.emqx.com/en/mqtt-client-sdk) on Raspberry Pi 4 using MicroPython, and implement the functions of connecting, subscribing, and publishing between the clients and the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

## Prerequisites

Before proceeding, please ensure you have an MQTT broker to communicate and test with. We recommend you use EMQX Cloud.

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service that can connect to a large number of IoT devices and integrate various databases and business systems. With EMQX Cloud, you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simplify the process:

- Server: `broker.emqx.io`
- TCP Port: `1883`
- WebSocket Port: `8083`
- SSL/TLS Port: `8883`
- Secure WebSocket Port: `8084`

## Environment Setup

### Install MicroPython

To install and write code using MicroPython, we need to complete the following installation on the Raspberry Pi 4. The Raspberry Pi operating system used in this article is `Raspberry Pi 4 OS with desktop (Debian version: 10, 64-bit)`.

- When the OS used by the Raspberry Pi 4 is based on `Debian version: 10 (buster)`, you can install MicroPython directly with the following command.

  ```shell
  sudo apt-get update
  sudo apt-get -y install micropython
  ```

  > ***Note***
  >
  > *If you get an* `E: Unable to locate package micropython` error during installation, you can use the `snap` or `build from source code` to install.

- If your Raspberry Pi 4 OS is based on `Debian version: 11 (bullseye)`, you can install MicroPython using snap.

  ```shell
  sudo apt update
  sudo apt install snapd
  sudo reboot
  sudo snap install core
  sudo snap install micropython
  ```

- Install MicroPython from source.

  For more details, please refer to the Raspberry Pi 4 documentation at [Getting Started — MicroPython latest documentation](https://docs.micropython.org/en/latest/develop/gettingstarted.html).

After the installation is complete, execute `micropython` in the terminal, and if MicroPython x.x.x (x means number) is returned, the installation is successful.

![MicroPython](https://assets.emqx.com/images/b9b6de52e3c29063df1f4d906d52e578.png)

### Install the MQTT Client Library

In order to connect to the MQTT server easily, install the `umqtt.simple` library.

```shell
micropython -m upip install umqtt.simple
```

## Connecting to the MQTT Broker

### Connect over TCP Port

This section introduces how to connect MicroPython and MQTT servers through the TCP port on the Raspberry Pi. The complete code example is as follows:

#### Subscribe

Open any editor, type the following code, and save it as a sub.py file:

```python
# sub.py
import time
from umqtt.simple import MQTTClient

SERVER="broker.emqx.io"
ClientID = f'raspberry-sub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

def sub(topic, msg):
    print('received message %s on topic %s' % (msg, topic))

def main(server=SERVER):
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.set_callback(sub)
    client.connect()
    print('Connected to MQTT Broker "%s"' % (server))
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

#### Publish

Open any editor, type the following code, and save it as a pub.py file:

```python
# pub.py
import time
from umqtt.simple import MQTTClient

server="broker.emqx.io"
ClientID = f'raspberry-pub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

def connect():
    print('Connected to MQTT Broker "%s"' % (server))
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.connect()
    return client

def reconnect():
    print('Failed to connect to MQTT broker, Reconnecting...' % (server))
    time.sleep(5)
    client.reconnect()

try:
    client = connect()
except OSError as e:
    reconnect()

while True:
  print('send message %s on topic %s' % (msg, topic))
  client.publish(topic, msg, qos=0)
  time.sleep(1)
```

In the above codes, we call the publish() function to send a message to the topic raspberry/mqtt. The parameter QoS is another MQTT feature. To learn more about QoS, please see the [Introduction to MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos). In this example, we set it to 0.

### Connect over TLS/SSL Port

This section introduces how to connect MicroPython and MQTT servers through the TLS/SSL port on the Raspberry Pi. The TCP port and TLS/SSL port connections differ slightly in the connection setup part, and the publish and subscribe part codes are the same. The complete code example is as follows:

#### Subscribe

Open any editor, type the following code, and save it as a sub-tls.py file:

```python
# sub-tls.py
import time
import ussl
from umqtt.simple import MQTTClient

SERVER="broker.emqx.io"
ClientID = f'raspberry-sub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = b'raspberry/mqtt'
msg = b"hello"

def sub(topic, msg):
    print('received message %s on topic %s' % (msg, topic))

def main(server=SERVER):
    client = MQTTClient(ClientID, server, 8883, user, password, ssl=True, ssl_params={'server_hostname': server})
    client.set_callback(sub)
    client.connect()
    print('Connected to MQTT Broker "%s"' % (server))
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

#### Publish

Open any editor, type the following code, and save it as a pub-tls.py file:

```python
# pub-tls.py
import time
import ussl
from umqtt.simple import MQTTClient

server = "broker.emqx.io"
ClientID = f'raspberry-pub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = b'raspberry/mqtt'
msg = b'{"msg":"hello"}'

def connect():
    print('Connected to MQTT Broker "%s"' % server)
    client = MQTTClient(ClientID, server, 8883, user, password, ssl=True, ssl_params={'server_hostname': server})
    try:
        client.connect()
        return client
    except Exception as e:
        print('Failed to connect to MQTT broker:', e)
        raise

def reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(5)
    client = connect()
    return client

try:
    client = connect()
except Exception:
    client = reconnect()

while True:
    try:
        print('Sending message %s on topic %s' % (msg, topic))
        client.publish(topic, msg, qos=0)
        time.sleep(1)
    except Exception as e:
        print('Failed to publish message:', e)
        client = reconnect()
```

## Testing

We use the [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) to perform the following tests.

### Test subscribe

After successfully connecting to the MQTT server, you can use the Raspberry Pi 4 and MQTTX to test the connection.

1. Open a terminal, run the MicroPython code, and listen for messages.

   ```shell
   micropython sub.py
   ```

   ![micropython sub](https://assets.emqx.com/images/5aceddabb0706609862ba8f6c8436c14.png)

2. Use the MQTTX client to connect with the MQTT server and send messages to the topic `raspberry/mqtt`.

   ![MQTT client tool](https://assets.emqx.com/images/8ebd27d6b93c80dd77a44571557e8bfe.png)

3. Check the Raspberry Pi 4 terminal information and you will see that the MQTTX publish messages have been successfully received.

   ![Receive MQTT messages](https://assets.emqx.com/images/30cf035b0136f7991990705ed76ec24f.png)

### Test publish

1. Subscribe to the `raspberry/mqtt` topic in the MQTTX client.

2. Run the MicroPython code in the terminal and publish the message.

   ```shell
   micropython pub.py
   ```

   ![Publish MQTT messages](https://assets.emqx.com/images/cdd350b4bb8e9506225f922de1e295dd.png)

3. In the MQTTX client, view the messages sent by the Raspberry Pi 4.

   ![MQTTX subscribe](https://assets.emqx.com/images/94abe428d1a1431d288630e90fd17f57.png)

## Summary

This is a brief example of programming with MicroPython on a Raspberry Pi 4. We created a simple test client using MicroPython `umqtt.simple`, and successfully established a connection between the client and the MQTT server for sending and receiving messages. 

The most significant advantage of MQTT is its ability to provide real-time reliable messaging services for connected remote devices with minimal code and limited bandwidth. Additionally, the Raspberry Pi 4 is a small, low-energy, low-heat, and relatively comprehensive hardware module. Combining these two technologies can help you develop more innovative applications, even in microcontrollers or constrained environments.



## Other Articles in This Series

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Using MQTT on ESP8266: A Quick Start Guide](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [How to Deploy an MQTT Broker on Raspberry Pi](https://www.emqx.com/en/blog/how-to-deploy-an-mqtt-broker-on-raspberry-pi)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
