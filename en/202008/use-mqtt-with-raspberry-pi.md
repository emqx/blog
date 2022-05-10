[Raspberry Pi](https://www.raspberrypi.org/) is a small single-board computer based on ARM and developed by the Raspberry Pi Foundation in the United Kingdom. This board provides USB interfaces and Ethernet interfaces can connect the keyboard, mouse, and networking cable. This board has the basic functions of PC and Raspberry Pi integrates Wi-Fi, Bluetooth, and a large number of GPIO, and is widely used in teaching, family entertainment, IoT, etc.

[MQTT](https://www.emqx.com/en/mqtt) is a kind of **lightweight IoT messaging protocol** based on the publish/subscribe model, which can provide real-time and reliable messaging service for IoT devices, only using very little code and bandwidth. It is suitable for devices with limited hardware resources and the network environment with limited bandwidth. Therefore, MQTT protocol is widely used in IoT, mobile internet, IoV, electricity power, and other industries.

In this project, we will use Python to write a simple [MQTT client](https://www.emqx.com/en/mqtt-client-sdk) on Raspberry Pi and implement connect, subscribe, unsubscribe, messaging, and other functions between this client and [MQTT broker](https://www.emqx.io).


## Install the dependencies 

### Install Python3

This project use Python3 to develop. Usually, Raspberry Pi has built-in Python3, if you not sure whether the Python3 was installed, you can use the following command to confirm.

```
python3 --version 
```

If it displays Python 3.x.x (x means number), Python 3 was installed. Otherwise, please use the apt command to install (or follow the [Python3 installation guideline](https://wiki.python.org/moin/BeginnersGuide/Download) ).

```
sudo apt install python3 
```

### Install the MQTT client library

We need to install the library `paho-mqtt` for easy to connect the MQTT broker. You can choose one of the following two methods to install.

**Use the source code to install** 

```
git clone https://github.com/eclipse/paho.mqtt.python 
cd paho.mqtt.python 
python3 setup.py install
```

**Use pip3 to install** 

```
pip3 install paho-mqtt 
```



## The use of MQTT

### Connect to the MQTT broker

This article will use [the free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service is based on [MQTT IoT cloud platform](https://www.emqx.com/en/cloud) to create. The accessing information of the broker is as follows:


* Broker: **broker.emqx.io** 
* TCP Port: **1883** 
* Websocket Port: **8083** 

If it is needed, you can use docker to quickly install the EMQX broker locally.

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 18083:18083 emqx/emqx 
```

**The example code of connecting** 

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

 Save the above code as file test_connect.py, and run:

```
python3 test_connect.py 
```

We judge the response code in the function on_connect. If it is 0, then print `Connected success` to represent successfully connected. If it returns other numbers, we need to judge it according to the response code below.

> ```undefined
> 0: connection succeeded
> 1: connection failed - incorrect protocol version
> 2: connection failed - invalid client identifier
> 3: connection failed - the broker is not available
> 4: connection failed - wrong username or password
> 5: connection failed - unauthorized
> 6-255: undefined
> If it is other issues, you can check the network situation, or check whether `paho-mqtt` has been installed.
> ```

In the concept of the MQTT protocol, the message is delivered through the topic. For example, one device sends messages to the topic T, only the devices that subscribed to the topic T can receive the message. Therefore, only accessing the MQTT broker is meaningless. If you want to use the MQTT service completely, we still need to know how to publish and subscribe.

### Subscribe

Open any editor and input the following code, and save it as file subscriber.py.

```python
# subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("raspberry/topic")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
```

Calling the function `subscribe()`, which can enable the Raspberry Pi to subscribe to a topic. In the following code, we use it to subscribe to the topic  `raspberry/topic` and monitor messages.

Besides that, we also use `will_set()` to set the [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message). The will message is a feature of MQTT, when the device is powered off accidentally, it will send messages to a specified topic. We can know whether the Raspberry Pi is powered off, or the network is abnormal.

### Publish messages 

Open any editor and input the following code, and save it as file publisher.py.

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

# send a message to the raspberry/topic every 1 second, 5 times in a row
for i in range(5):
  	# the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_forever()
```

Calling function `publish()` can send messages to a topic. In the above code, we use it to send messages to the topic  `raspberry/topic`. The parameter QoS is another MQTT feature, if you want to know more content of QoS, you can view  [introduction to MQTT QoS (the quality of service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos). Here we temporarily set it to 0.



## Test 

We use [MQTT 5.0 client tool - MQTT X](https://mqttx.app) to do the following tests.

### Test topic subscription 

Run the Python code and actively send messages.

1. Open the terminal, run Python code, monitor messages.

   ```
   python3 subscriber.py
   ```

2. Use MQTT X client to connect to the MQTT broker and send messages to the topic `raspberry/topic`.

   ![MQTT X](https://static.emqx.net/images/cc93d1c6d99f3bfa3a78d8472a6209af.jpg)

3. View the terminal information of Raspberry Pi, and you will see the messages published by MQTT X.


     ![mqtt subscriber](https://static.emqx.net/images/9c4e5b191e9bd00317fed06f94b13850.png)

### Test publish message


1. Subscribe to the topic `raspberry/topic` in the MQTT X client.

2. Run Python code in the terminal.

   ![mqtt publisher](https://static.emqx.net/images/9ea832adda032c9297c84fbf585fb294.png)

3. View the messages published by the Raspberry Pi in the MQTT X client.

    ![MQTT X publish message](https://static.emqx.net/images/07ffb81c764145100b1e21572357c675.jpg)

### Test the will message 

Next, testing whether the will message, is set successfully.


1. Subscribe to `raspberry/status` in the MQTT X client.

   ![subscribe to mqtt topic in the MQTT X](https://static.emqx.net/images/c704c8b0f7117079306d16b5af8c2557.jpg)

2. Interrupt the program or disconnect the network of the Raspberry Pi.

3. View the messages that `raspberry/status` received, in the MQTT X client.  ![receive mqtt message](https://static.emqx.net/images/048da27682c9a86c536f85ffd6417bf2.jpg)



## Summary 

We have finished that use the [Python MQTT client library](https://www.emqx.com/en/blog/python-async-mqtt-client-hbmqtt) `paho-mqtt ` to write and test the client on the Raspberry Pi and implemented the connect, subscribe, unsubscribe, messaging and other functions between the client and the MQTT broker.

So far, you've learned how to simply use the MQTT service, although this is only one part of the MQTT service, it is enough to finish many interesting things. For example:

1. Use a mobile phone to send MQTT messages, remotely control the Raspberry Pi.
2. Send the device information of Raspberry Pi to the MQTT broker regularly and receive messages through mobile phone, then can round-the-clock monitor.
3. You can access the MQTT broker through the Raspberry Pi and use various kinds of sensors and ESP modules to create many interesting IoT applications.

Next, we will publish more articles about IoT development and Raspberry Pi. Stay tuned.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
