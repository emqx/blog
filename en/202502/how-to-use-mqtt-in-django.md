## **Introduction**

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight IoT messaging protocol based on a publish/subscribe model, providing real-time, reliable messaging services for connected devices with minimal code and bandwidth. Due to its efficiency, MQTT is widely used in IoT, mobile applications, smart hardware, [Internet of vehicles](https://www.emqx.com/en/blog/category/internet-of-vehicles), and energy sectors.

[Django](https://www.djangoproject.com/) is a popular open-source Python web framework known for its scalability and rapid development capabilities. This guide will walk you through integrating MQTT with Django, covering how to connect, subscribe, unsubscribe, and exchange messages between an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) within a Django project.

## **Setting Up MQTT in Django**

We will use the [paho-mqtt](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) library, a widely used MQTT client library in Python that supports **MQTT 5.0, 3.1.1, and 3.1** on Python 2.7 and 3.x.

This project is tested on **Python 3.12**. You can verify your Python version with:

```shell
$ python3 --version
Python 3.12.2
```

Install Django and `paho-mqtt` using Pip.

```shell
pip3 install django
pip3 install paho-mqtt
```

Create a Django project.

```shell
django-admin startproject django_mqtt
```

The directory structure after creation is as follows.

```
├── django_mqtt
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Using paho-mqtt with Django

This article will use [free public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ. The service is created based on [EMQX ](https://www.emqx.com/en/cloud)Platform. The server access information is as follows:

- Broker: `broker.emqx.io`
- TCP Port: `1883`
- Websocket Port: `8083`

### Importing paho-mqtt

```python
import paho.mqtt.client as mqtt
```

### Writing Connection Callback

Handling **successful or failed** MQTT connections in the callback function. After a successful connection, we subscribe to the `django/mqtt` topic:

```python
def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe('django/mqtt')
   else:
       print('Bad connection. Code:', rc)
```

### Writing Message Callback

This function will print the messages received by the `django/mqtt` topic.

```python
def on_message(mqtt_client, userdata, msg):
   print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
```

## Configuring Django for MQTT

### Adding Django Configuration Items

Add configuration items for the MQTT broker in `settings.py`. For any questions about the following configuration items and MQTT-related concepts mentioned in this article, please check out the blog: [The Easiest Guide to Getting Started with MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

> *This example uses anonymous authentication, so the username and password are set to empty.*

```
MQTT_SERVER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_USER = ''
MQTT_PASSWORD = ''
```

### Configuring the MQTT Client

```python
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
```

## Creating an MQTT Message Publishing API in Django

We create a simple POST API to implement MQTT message publishing.

> *In actual applications, the API code may require more complex business logic processing.*

### **Defining the API in views.py**

Add the following code in `views.py`.

```python
import json
from django.http import JsonResponse
from django_mqtt.mqtt import client as mqtt_client


def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
```

### Mapping the API in urls.py

Add the following code in `urls.py`.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('publish', views.publish_message, name='publish'),
]
```

## Running the Django MQTT Client

Add the following code in `__init__.py`.

```python
from . import mqtt
mqtt.client.loop_start()
```

At this point, we have finished writing all the code, and the full code can be found at [GitHub](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Django).

Finally, execute the following command to run the Django project.

```python
python3 manage.py runserver
```

When the Django application starts, the MQTT client will connect to the MQTT Broker and subscribe to the topic `django/mqtt`.

## Testing MQTT in Django

Next, we will use [MQTT client - MQTTX](https://mqttx.app/) to test connection, subscription, and publishing.

### Test Message Receiving

1. Create an MQTT connection in MQTTX, enter the connection name, leave the other parameters as default, and click the `Connect` button in the upper right corner to connect to the broker.

   ![Receive MQTT messages](https://assets.emqx.com/images/c1f51ce1e983990bb45abd410b190cee.png)

2. Publish the message `Hello from MQTTX` to the `django/mqtt` topic in the message publishing box at the bottom of MQTTX.

   ![Publish MQTT messages](https://assets.emqx.com/images/039bb0a953e8579ccfd89938fcda784b.png)

3. The messages sent by MQTTX will be visible in the Django runtime window.

   ```shell
   $ python3 manage.py runserver
   Performing system checks...
   System check identified no issues (0 silenced).
   
   Django version 5.1.5, using settings 'django_mqtt.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   
   Connected successfully
   Received message on topic: django/mqtt with payload: b'Hello from MQTTX'
   ```

### Test Message Publishing API

1. Subscribe to the `django/mqtt` topic in MQTTX.

   ![Subscribe to MQTT topic](https://assets.emqx.com/images/fe6d48d40f8411a8921747d02ff8abc6.png)

2. Use Postman to call `/publish` API: publish the message `Hello from Django` to the `django/mqtt` topic.

   ![Use Postman to call API](https://assets.emqx.com/images/37a68e55290c1257fbd58aeaf1be7b82.png)

3. You will see the messages sent by Django in MQTTX.

   ![Publish MQTT messages](https://assets.emqx.com/images/5ece1784c6ed0817445b196751456072.png)

## Summary

In this guide, we integrated MQTT with Django using the paho-mqtt library, enabling message publishing and subscription via an MQTT broker. This foundation can be extended to support more advanced use cases, such as real-time IoT applications, device monitoring, or remote control systems.

For further learning, explore our [Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) to dive deeper into MQTT’s advanced features and real-world applications.

 

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
