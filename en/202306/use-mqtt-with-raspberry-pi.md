[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol for IoT in [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), offering reliable real-time communication with minimal code and bandwidth. It is especially beneficial for devices with limited resources and low-bandwidth networks, making it widely adopted in IoT, mobile internet, IoV, and power industries.

[Raspberry Pi](https://www.raspberrypi.org/) is a small single-board computer based on ARM and developed by the Raspberry Pi Foundation in the United Kingdom. This board provides USB interfaces and Ethernet interfaces can connect the keyboard, mouse, and networking cable. This board has the basic functions of PC and Raspberry Pi integrates Wi-Fi, Bluetooth, and a large number of GPIO, and is widely used in teaching, family entertainment, IoT, etc.

In this project, we will use Python to write a simple [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) on Raspberry Pi and implement connection, subscription, messaging, and other functions between this client and [MQTT broker](https://www.emqx.io/).

## Raspberry Pi MQTT Project Preparation

### Install the Operating System

Raspberry Pi is a versatile mini-computer that can run different operating systems, including Raspberry Pi OS, Ubuntu, and Kodi. Each operating system has its own unique set of features, advantages, and recommended applications.

Raspberry Pi OS in particular, is highly recommended for beginners due to its compatibility with Raspberry Pi hardware and the pre-installed optimized software and tools. It is based on Debian Linux and customized specifically for Raspberry Pi, providing a user-friendly platform for programming, multimedia, and electronics projects.

To install Raspberry Pi OS, we advise following the [official documentation's installation guide](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system). This article uses a Raspberry Pi 4 with the **Raspberry Pi OS with desktop (Debian version: 11)** installed.

### Install Python3

We will use Python as the development language for MQTT on the Raspberry Pi. With an easy-to-learn syntax and a vast range of libraries and tutorials available online, Python is an excellent choice for working with MQTT.

This project is developed using Python 3.6. Typically, Raspberry Pi already comes with Python 3 pre-installed. However, if you are unsure whether Python 3 is installed, you can verify it by using the following command:

```vim
$ python3 --version             
Python 3.6.7
```

If the command line returns "Python 3.x.x" (where "x" indicates the version number), it means that Python 3 is already installed on your Raspberry Pi. In case it is not installed, you can use the "apt" command to install it, or you can follow the [Python3 installation guidelines](https://wiki.python.org/moin/BeginnersGuide/Download).

```cmake
sudo apt install python3
```

### Install the Paho MQTT Client

We will use the [Paho Python Client](https://github.com/eclipse/paho.mqtt.python) library, which offers a client class that supports MQTT v5.0, v3.1.1, and v3.1 in Python 2.7 and 3.x. In addition, it includes convenient helper functions that make publishing one-off messages to an MQTT server very simple.

**Use the source code to install**

```vim
git clone https://github.com/eclipse/paho.mqtt.python 
cd paho.mqtt.python 
python3 setup.py install
```

**Use pip3 to install**

```cmake
pip3 install paho-mqtt
```

## Prepare an MQTT Broker

Before proceeding, please ensure you have an MQTT broker to communicate and test with. There are several options for obtaining an MQTT broker:

- **Private deployment**

  [EMQX](https://www.emqx.io/) is the most scalable open-source MQTT broker for IoT, [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges), and connected vehicles. You can run the following Docker command to install EMQX.

  ```apache
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **Fully managed cloud service**

  The fully managed cloud service is the easiest way to start an MQTT service. With [EMQX Cloud](https://www.emqx.com/en/cloud), you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity.

  The latest edition, [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), provides a forever free 1M session minutes/month complimentary offering for developers to easily start their MQTT deployment within seconds.

- **Free public MQTT broker**

  The Free public MQTT broker is exclusively available for those who wish to learn and test the MQTT protocol. It is important to avoid using it in production environments as it may pose security risks and downtime concerns.

For this blog post, we will use the free public MQTT broker at `broker.emqx.io`.

> **MQTT Broker Info**
>
> Server: `broker.emqx.io`
>
> TCP Port: `1883`
>
> WebSocket Port: `8083`
>
> SSL/TLS Port: `8883`
>
> Secure WebSocket Port: `8084`

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/b4cff1e553053873a87c4fa8713b99bc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Practical Guide to MQTT Broker Selection
    </div>
    <div class="mb-32">
      Download this practical guide and learn what to consider when choosing an MQTT broker.
    </div>
    <a href="https://www.emqx.com/en/resources/a-practical-guide-to-mqtt-broker-selection?utm_campaign=embedded-a-practical-guide-to-mqtt-broker-selection&from=blog-use-mqtt-with-raspberry-pi" class="button is-gradient">Get the eBook →</a>
  </div>
</section>

## Quick Usage of MQTT

### Create an MQTT Connection

**Connection code**

```python
# test_connect.py 
import paho.mqtt.client as mqtt 

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
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

You can save the code above as a file named "test_connect.py". To run the file, open a terminal on your Raspberry Pi and navigate to the directory where the file is located. Then enter the command below to execute the script. This will start the MQTT client and connect to the MQTT broker.

```vim
python3 test_connect.py
```

In the `on_connect` function, we check the response code returned by the MQTT broker. If the response code is `0`, we print "Connected success" to indicate the successful connection. However, if the response code is `not 0`, we need to check its meaning based on the following response code table.

```
0: connection succeeded
1: connection failed - incorrect protocol version
2: connection failed - invalid client identifier
3: connection failed - the broker is not available
4: connection failed - wrong username or password
5: connection failed - unauthorized
6-255: undefined
If it is other issues, you can check the network situation, or check whether `paho-mqtt` has been installed.
```

### Subscribe

The MQTT protocol routes messages based on topics. Subscribers can subscribe to the topics they are interested in with the broker. When a publisher sends a message to a specific topic, the broker forwards that message to all subscribers who have subscribed to that topic.

Open any text editor and input the following code. Save the file as "subscriber.py".

```python
# subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe, which need to put into on_connect
    # If reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("raspberry/topic")

# The callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# Create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# Set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
```

The `subscribe()` function enables Raspberry Pi to subscribe to a particular topic. In the code above, we use this function to subscribe to the topic `raspberry/topic` and monitor any incoming messages.

Additionally, we utilize the `will_set()` function to set up a [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message). This feature of MQTT allows the device to send messages to a specified topic in case it is unintentionally powered off. Using this feature, we can determine whether the Raspberry Pi has been powered off or has network connectivity problems.

### Publish Messages

Open any text editor and input the following code. Save the file as "publisher.py".

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Send a message to the raspberry/topic every 1 second, 5 times in a row
    for i in range(5):
        # The four parameters are topic, sending content, QoS and whether retaining the message respectively
        client.publish('raspberry/topic', payload=i, qos=0, retain=False)
        print(f"send {i} to raspberry/topic")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

client.loop_forever()
```

The `publish()` function allows for sending messages to a specific topic. In the code example above, we use this function to send messages to the topic `raspberry/topic`. The QoS parameter is another feature of MQTT that defines the quality of service level for message delivery. To learn more about the QoS level, please refer to [Introduction to MQTT QoS 0, 1, 2](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

> For more information about using Paho Client, please check out the blog [How to Use MQTT in Python with Paho Client](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python).

## Test

For conducting the following tests, we will use MQTTX. [MQTTX](https://mqttx.app/) is an elegant cross-platform MQTT 5.0 desktop client that runs on macOS, Linux, and Windows. Its user-friendly chat-style interface enables users to easily create multiple MQTT/MQTTS connections and subscribe/publish MQTT messages.

### Subscribe

1. Running the MQTT subscription script `subscriber.py`, we will see the client successfully connected and started waiting for the publisher to publish messages.

   ```vim
   python3 subscriber.py
   ```

   ![python3 subscriber.py](https://assets.emqx.com/images/39d734d2935a8ea39980c386064c6189.png)

2. Publish a message to the "raspberry/topic" using MQTTX as the publisher.

   ![MQTTX](https://assets.emqx.com/images/cc93d1c6d99f3bfa3a78d8472a6209af.jpg?imageMogr2/thumbnail/1520x)

3. You will see the messages published by MQTTX.

   ![Messages published by MQTTX](https://assets.emqx.com/images/2b4b3eb61401434ff02d35ef94c5acc9.png)

### Publish Messages

1. Subscribe to the `raspberry/topic` within the MQTTX client.

2. Run `publish.py` in the terminal.

   ![python3 publish.py](https://assets.emqx.com/images/8efd674aff8e58b465bed00bbade388c.png)

3. In the MQTTX client, you can view the messages that have been published by the Raspberry Pi.

   ![MQTTX publish message](https://assets.emqx.com/images/07ffb81c764145100b1e21572357c675.jpg?imageMogr2/thumbnail/1520x)

### Test the Will Message

Next, we will test whether the will message has been set successfully.

1. Subscribe to `raspberry/status` in the MQTTX client.

   ![subscribe to mqtt topic in the MQTTX](https://assets.emqx.com/images/c704c8b0f7117079306d16b5af8c2557.jpg?imageMogr2/thumbnail/1520x)

2. Interrupt the program or disconnect the network of the Raspberry Pi.

3. View the messages that `raspberry/status` received, in the MQTTX client. 

   ![receive mqtt message](https://assets.emqx.com/images/048da27682c9a86c536f85ffd6417bf2.jpg?imageMogr2/thumbnail/1520x)

## Raspberry Pi MQTT Advanced

### Reading Raspberry Pi Serial Data

The provided code establishes a serial connection with a Raspberry Pi, reads data from the serial port, and publishes it to an MQTT broker. It uses the `serial` library to configure the serial port settings and read data, while the `paho.mqtt.client` library is used to connect to the MQTT broker and publish the data. The code reads serial data in a loop, publishes it to the specified MQTT topic, and repeats this process for a defined number of iterations. Finally, it disconnects from the MQTT broker and closes the serial connection.

```python
import time

import paho.mqtt.client as mqtt
import serial


# Establishing the connection with the serial port
ser = serial.Serial(
    # Serial Port to read the data from
    port='/dev/ttyAMA0', # Use `dmesg | grep tty` to find the port
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

broker_address = "broker.emqx.io"
broker_port = 1883
topic = "emqx/serial/read"

client = mqtt.Client()
client.connect(broker_address, broker_port)

# Read data from serial port and publish it to MQTT broker
for i in range(10):
    data = ser.readline().decode()
    client.publish(topic, data)
    print("Read data {data} from serial port and publish it to MQTT broker".format(data=data))
    time.sleep(1)


client.disconnect()

ser.close()
```

### Writing Raspberry Pi Serial Data

The provided code establishes a serial connection with a Raspberry Pi and listens for MQTT messages. When a message is received, it is written to the serial port. The code uses the `serial` library to configure the serial port settings and write data, while the `paho.mqtt.client` library is used to connect to the MQTT broker, handle MQTT message reception, and publish data to the serial port. The MQTT client is set up with the necessary callbacks, including `on_connect` to subscribe to a specific MQTT topic and `on_message` to handle incoming messages. Once connected, the code enters an infinite loop to continuously listen for MQTT messages and write them to the serial port.

```python
import paho.mqtt.client as mqtt
import serial


# Establishing the connection with the serial port
ser = serial.Serial(
    # Serial Port to read the data from
    port='/dev/ttyAMA0', # Use `dmesg | grep tty` to find the port
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

broker_address = "broker.emqx.io"
broker_port = 1883
topic = "emqx/serial/write"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Received message: {payload} on topic {topic}".format(payload=payload, topic=msg.topic))
    # Write data to serial port
    ser.write(payload.encode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port)
client.loop_forever()
```

## Summary

In this blog, we use the Python MQTT client library `paho-mqtt` to write and test the client on the Raspberry Pi. We have implemented the connection, subscription, messaging, and other functions between the client and the MQTT broker.

Great progress so far! You have learned the basics of building many exciting applications with the MQTT. For example:

1. You can remotely control the Raspberry Pi from your mobile phone using MQTT messages.
2. By regularly sending device data from the Raspberry Pi to the MQTT broker, you can continuously monitor and receive messages on your mobile phone.
3. With Raspberry Pi accessing the MQTT broker and employing various sensors and ESP modules, you can create numerous interesting IoT applications.

Next, you can check out the [MQTT Guide: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


## Resources

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [ESP8266 Connects to MQTT Broker with Arduino](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [Upload Sensor Data to MQTT Cloud Service via NodeMCU (ESP8266)](https://www.emqx.com/en/blog/upload-sensor-data-to-mqtt-cloud-service-via-nodemcu-esp8266)




<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
