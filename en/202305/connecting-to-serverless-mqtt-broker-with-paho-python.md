Serverless architecture in cloud computing allows developers to focus on code development and deployment without the hassle of infrastructure management. Serverless MQTT, in particular, provides an MQTT messaging service that scales automatically based on demand, reducing the need for manual intervention.

To learn more about serverless MQTT, read our blog post [Next-Gen Cloud MQTT Service: Meet EMQX Cloud Serverless](https://www.emqx.com/en/blog/next-gen-cloud-mqtt-service-meet-emqx-cloud-serverless). In this blog series, we'll guide you through using various client libraries to set up MQTT connections, subscriptions, messaging, and more with a serverless MQTT broker for your specific project.

## Introduction

[Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) offers a high-level API for integrating MQTT functionality into Python applications. It is an open-source library developed by the Eclipse Foundation.

This blog will use the Paho Python library to connect a serverless MQTT broker. The whole project can be downloaded at [MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Python3).

## Free Serverless MQTT broker

[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is the latest [MQTT broker](https://www.emqx.io/) offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. Additionally, users can get 1 million free session minutes every month, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

If you have not tried serverless deployment yet, please follow [the guide in this blog](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to create one for free. Once you have completed the registration process with the online guide, you will get a running instance with the following similar information from the “Overview” in your deployment. We will use the connection information and CA certificate later.

![EMQX MQTT Cloud](https://assets.emqx.com/images/b7f54f0922422779d30df5ede63e66fb.png)

## Connection Code Demo

### 1. Install Python and Paho MQTT client

If you don't have Python installed, please download it from the [official website](https://www.python.org/downloads/) and follow the installation instructions. Once Python is installed, you can use pip, a package management system for Python, to install paho-mqtt and manage other software packages.

```
pip install paho-mqtt
```

### 2. Import the Paho MQTT client

Next, create a Python file and import the Paho MQTT client by adding the following line at the beginning of your code:

```
from paho.mqtt import client as mqtt_client
```

This line will import the Paho MQTT client, allowing you to use its functionalities in your Python script.

### 3. Connection settings

To configure the connection settings, you need to specify the broker, port, topic, client ID, username, and password.

```
broker = '******.emqxsl.com'
port = 8883
topic = 'python/mqtt'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = '**********'
```

Please replace the connection parameters with your EMQX connection information and login credentials.

- Broker and port: Obtain the connection address and port information from the server deployment overview page.
- Topic: Topics are used to identify and differentiate between different messages, forming the basis of MQTT message routing.
- Client ID: Every [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) must have a unique client ID. You can use the Python function 'random.randint' to generate a random client ID.
- Username and password: To establish a client connection, please make sure that you provide the correct username and password. The following image shows how to configure these credentials under 'Authentication & ACL - Authentication' on the server side.

![Authentication & ACL](https://assets.emqx.com/images/356ec09d07fe9e52960b1c758d0e530e.png)

### 4. Connection Function

Next, write the 'on_connect' callback function. This function will be executed after the client is created. You can check whether the connection is successful by examining the value of 'rc' within this function.

```
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

### 5. Using TLS/SSL

When connecting to EMQX Serverless, it is important to note that it relies on a multi-tenant architecture, which enables multiple users to share a single EMQX cluster. In order to ensure the security and reliability of data transmission within this multi-tenant environment, TLS is required. And if the server is utilizing a self-signed certificate, you must download the corresponding CA file from the deployment overview panel and provide it during the connection setup process.

```
client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
```

The complete code is as below:

```
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

### 6. Publish

Next, you can set the MQTT client's publish function to send messages to the topic 'python/mqtt' every second in the while loop. This allows for continuous message publishing at regular intervals.

```
 def publish(client):
     msg_count = 0
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
```

### 7. Subscribe

Next, write the 'on_message' callback function. This function will be executed when the client receives messages from the MQTT Broker. Within this function, you can print the subscribed topic names and the corresponding received messages. This allows you to view and process the received data as needed.

```
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```

### 8. Unsubscribe

To unsubscribe, call:

```
client.unsubscribe(topic)
```

### 9. Disconnect

To disconnect, call:

```
client.disconnect()
```

## Complete code

Below is the complete code for connecting to the server, subscribing to topics, and publishing and receiving messages. If you want a comprehensive example demonstrating all the functions, please visit our [GitHub repository](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Python3).

```
from paho.mqtt import client as mqtt_client

BROKER = 'qbc11278.ala.us-east-1.emqxsl.com'
PORT = 8883
TOPIC = "python-mqtt/tls"
# generate client ID with pub prefix randomly
CLIENT_ID = f'python-mqtt-tls-pub-sub-{random.randint(0, 1000)}'
USERNAME = 'emqxtest'
PASSWORD = '******'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False

def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')

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
    global FLAG_EXIT
    FLAG_EXIT = True

def on_message(client, userdata, msg):
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=3)
    client.on_disconnect = on_disconnect
    return client

def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        msg_dict = {
            'msg': msg_count
        }
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{TOPIC}`')
        else:
            print(f'Failed to send message to topic {TOPIC}')
        msg_count += 1
        time.sleep(1)

def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()

if __name__ == '__main__':
    run()
```

## Test

Then you can simply run the project using the command `python3`.

```
python3 pub_sub_tls.py
```

Once the project is running, we can see the output information of the console as follows:

![Output information of the console](https://assets.emqx.com/images/f048f2656ef8b6ba9499646e6c93d643.png)

<center>Output information of the console</center>

The client has successfully connected to the MQTT broker, subscribed to the topic, and is publishing and receiving a message every second. 

You can also use [MQTT Client Tool - MQTTX](https://mqttx.app/) as another client for the message publishing and receiving the test. If you subscribe the “`python-mqtt/tls`“ topic in MQTTX, you will receive the message every second.

![Received message displayed on MQTTX](https://assets.emqx.com/images/efeb59eaf22f88d1caacffb76763fc16.png)

<center>Received message displayed on MQTTX</center>

When you publish a message to the topic, the server will receive the message and you can view it both on MQTTX and in the console.

![Received message displayed on MQTTX](https://assets.emqx.com/images/0341f67afa223b1c1b4cf8ce02ec52f9.png)

<center>Received message displayed on MQTTX</center>

![Received message display on the console](https://assets.emqx.com/images/b1858039d04638f2f77fe2c90ab473cd.png)

<center>Received message display on the console</center>

## Summary

This blog provides a step-by-step guide on connecting to a serverless MQTT deployment using Paho Python. By following these instructions, you have successfully created a Python application capable of publishing and subscribing to Serverless MQTT. For further information on connecting to MQTT brokers in Python, please refer to the tutorial blog at [How to Use MQTT in Python with Paho Client](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python).

## Join the EMQX Community

To dive deeper into this topic, explore our [GitHub repository](https://github.com/emqx/emqx) for the source code, join our [Discord](https://discord.com/invite/xYGf3fQnES) for discussions, and watch our [YouTube tutorials](https://www.youtube.com/@emqx) for hands-on learning. We value your feedback and contributions, so feel free to get involved and be a part of our thriving community. Stay connected and keep learning!

 

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
