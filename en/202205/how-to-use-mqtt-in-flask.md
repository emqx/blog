[Flask](https://flask.palletsprojects.com/en/2.1.x/) is a lightweight Web application framework written with Python, which is called "micro-framework" because it uses a simple core for extension of other features, such as: ORM, form validation tools, file upload, various open authentication techniques, etc.  

[MQTT](https://mqtt.org/) is a lightweight Internet of Things (IoT) message transmission protocol based on publish/subscribe mode. It can provide a real-time and reliable message service for networked devices with very less code and smaller bandwidth. It is widely used in IoT, mobile Internet, intelligent hardware, IoV, power and energy industries, etc.

This article mainly introduces how to use MQTT in the Flask project, and implement the connection, subscription, messaging, unsubscribing and other functions between the  [MQTT client](https://www.emqx.com/en/blog/introduction-to-the-commonly-used-mqtt-client-library) and [MQTT broker](https://www.emqx.io/).

We will use the [Flask-MQTT](https://flask-mqtt.readthedocs.io/en/latest/index.html) client library, which is a Flask extension and can be regarded as a decorator of [paho-mqtt](https://www.eclipse.org/paho/clients/python/) to simplify the MQTT integration in Flask applications.

## Project Initialization

This project is developed and tested with Python 3.8, and users may use the following commands to verify the version of Python.

```
$ python3 --version
Python 3.8.2
```

Use Pip to install the Flask-MQTT library.

```
pip3 install flask-mqtt
```

## Use Flask-MQTT

We will adopt the [Free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, which is created on the basis of [MQTT cloud service - EMQX Cloud](https://www.emqx.com/en/cloud). The following is the server access information:

- Broker: `broker.emqx.io`
- TCP Port: 1883
- Websocket Port: 8083

### Import Flask-MQTT

Import the Flask library and Flask-MQTT extension, and create the Flask application.

```
from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)
```

### Configure Flask-MQTT extension

```
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)
```

For complete configuration items, please refer to [Flask-MQTT configuration document](https://flask-mqtt.readthedocs.io/en/latest/configuration.html).

### Write connect callback function

We can handle successful or failed MQTT connections in this callback function, and this example will subscribe to the `/flask/mqtt` topic after a successful connection.

```
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)
```

### Write message callback function

This function will print the messages received by the `/flask/mqtt` topic.

```
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
```

### Create message publish API

We create a simple POST API to publish the MQTT messages.

> In practical case, the API may need some more complicated business logic processing.

```
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})
```

### **Run Flask application**

When the Flask application is started, the MQTT client will connect to the server and subscribe to the topic `/flask/mqtt`.

```
if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
```

## Test

Now, we use the [MQTT client - MQTTX](https://mqttx.app) to connect, subscribe, and publish tests.

### Receive message

1. Create a connection in MQTTX and connect to the MQTT server.

   ![MQTTX new connection](https://assets.emqx.com/images/0813905d4d732565476cdbf5275a65e2.png)

2. Publish `Hello from MQTTX` to the `/flask/mqtt` topic in MQTTX.

   ![MQTTX publish MQTT message](https://assets.emqx.com/images/b4b533b9113da3735304c7b38397aa12.png)

3. We will see the message sent by MQTTX in the Flask running window.

   ![Flask receive MQTT message](https://assets.emqx.com/images/ce56d6aa495c5193f0fe8fd63c911c40.png)


### Publish message

1. Subscribe to the `/flask/mqtt` topic in MQTTX.

   ![MQTTX subscribe](https://assets.emqx.com/images/b2d98f1d30a9158444c2894294014dcf.png)

2. Use Postman to call the `/publish` API: Send the message `Hello from Flask` to the `/flask/mqtt` topic.

   ![Postman test](https://assets.emqx.com/images/901ac5434b526edd82c413c26cf21c72.png)

3. We can see the message sent from Flask in MQTTX.

   ![Flask publish MQTT message](https://assets.emqx.com/images/3bcb310ab66fdb20b2f3d169673dd4b7.png)


### Complete code

```
from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
```

## Limitations

**Flask-MQTT is currently not suitable for the use with multiple worker instances.** So if you use a WSGI server like *gevent* or *gunicorn* make sure you only have one worker instance.

## Summary

So far, we have completed a simple MQTT client using Flask-MQTT and can subscribe and publish messages in the Flask application.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


## Other Articles in This Series

- [How to Use MQTT in Python (Paho)](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)

- [Python MQTT Asynchronous Framework - HBMQTT](https://www.emqx.com/en/blog/python-async-mqtt-client-hbmqtt)

- [Comparison of Python MQTT clients](https://www.emqx.com/en/blog/comparision-of-python-mqtt-client)

- [How to Use MQTT in The Django Project](https://www.emqx.com/en/blog/how-to-use-mqtt-in-django)

- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)




<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
