[MQTT](https://mqtt.org/) is a lightweight IoT messaging protocol based on publish/subscribe model, which can provide real-time reliable messaging services for connected devices with very little code and bandwidth. It is widely used in industries such as IoT, mobile Internet, smart hardware, [Internet of vehicles](https://www.emqx.com/en/blog/category/internet-of-vehicles), and power and energy.

[Django](https://www.djangoproject.com/) is an open-source Web framework and one of the more popular Python Web frameworks. This article mainly introduces how to connect, subscribe, unsubscribe, and send and receive messages between [MQTT client](https://www.emqx.io/en/mqtt-client) and [MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) in the Django project.

We will write a simple MQTT client using [paho-mqtt](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) client library. `paho-mqtt` is a widely used MQTT client library in Python that provides client support for MQTT 5.0, 3.1.1, and 3.1 on Python 2.7 and 3.x.


## Project initialization

This project uses Python 3.8 for development testing, and the reader can confirm the version of Python with the following command.

```
$ python3 --version
Python 3.8.2
```

Install Django and `paho-mqtt` using Pip.

```
pip3 install django
pip3 install paho-mqtt
```

Create a Django project.

```
django-admin startproject mqtt-test
```

The directory structure after creation is as follows.

```
├── manage.py
└── mqtt_test
  ├── __init__.py
  ├── asgi.py
  ├── settings.py
  ├── urls.py
  ├── views.py
  └── wsgi.py
```

## Using paho-mqtt

This article will use [free public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ. The service is created based on [MQTT Cloud service - EMQX Cloud](https://www.emqx.com/en/cloud). The server access information is as follows:

- Broker: `broker.emqx.io`
- TCP Port: `1883`
- Websocket Port: `8083`

### Import paho-mqtt

```
import paho.mqtt.client as mqtt
```

### Writing connection callback

Successful or failed MQTT connections can be handled in this callback function, and this example will subscribe to the `django/mqtt` topic after a successful connection.

```
def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe('django/mqtt')
   else:
       print('Bad connection. Code:', rc)
```

### Writing message callback

This function will print the messages received by the `django/mqtt` topic.

```
def on_message(mqtt_client, userdata, msg):
   print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
```

### Adding Django configuration items

Add configuration items for the MQTT broker in `settings.py`. Readers who have questions about the following configuration items and MQTT-related concepts mentioned in this article can check out the blog [The Easiest Guide to Getting Started with MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

> This example uses anonymous authentication, so the username and password are set to empty.

```
MQTT_SERVER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_USER = ''
MQTT_PASSWORD = ''
```

### Configuring the MQTT client

```
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

### Creating a message publishing API

We create a simple POST API to implement MQTT message publishing.

> In actual applications, the API code may require more complex business logic processing.

Add the following code in `views.py`.

```
import json
from django.http import JsonResponse
from mqtt_test.mqtt import client as mqtt_client


def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
```

Add the following code in `urls.py`.

```
from django.urls import path
from . import views

urlpatterns = [
    path('publish', views.publish_message, name='publish'),
]
```

### Start the MQTT client

Add the following code in `__init__.py`.

```
from . import mqtt
mqtt.client.loop_start()
```

At this point, we have finished writing all the code, and the full code can be found at [GitHub](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Django).

Finally, execute the following command to run the Django project.

```
python3 manage.py runserver
```

When the Django application starts, the MQTT client will connect to the MQTT Broker and subscribe to the topic `django/mqtt`.

## Testing

Next, we will use [open-source cross-platform MQTT client - MQTT X](https://mqttx.app/) to test connection, subscription, and publishing.

### Test message receiving

1. Create an MQTT connection in MQTT X, enter the connection name, leave the other parameters as default, and click the `Connect` button in the upper right corner to connect to the broker.

   ![Receive MQTT messages](https://assets.emqx.com/images/f9b4449af7ac15183ca9b66ea7210ed1.png)

2. Publish the message `Hello from MQTT X` to the `django/mqtt` topic in the message publishing box at the bottom of MQTT X.

   ![Publish MQTT messages](https://assets.emqx.com/images/1d138bc5e7720c3a8c938137e6472ecb.png)

3. The messages sent by MQTT X will be visible in the Django runtime window.

   ![Run Django MQTT APP](https://assets.emqx.com/images/ad1a0e19f4bb66c7ebb614eac362a22c.png)

### Test message publishing API

1. Subscribe to the `django/mqtt` topic in MQTT X.

   ![Subscribe to MQTT topic](https://assets.emqx.com/images/fe6d48d40f8411a8921747d02ff8abc6.png)

2. Use Postman to call `/publish` API: publish the message `Hello from Django` to the `django/mqtt` topic.

   ![Use Postman to call API](https://assets.emqx.com/images/047e4c70a29041ab23d67379b3114bce.png)

3. You will see the messages sent by Django in MQTT X.

   ![Receive MQTT messages](https://assets.emqx.com/images/9490d8e462c63a461f5540032d03aadc.png)

## Summary

At this point, we have completed the development of the MQTT client using `paho-mqtt`, enabling communication using MQTT in Django applications. In practice, we can extend the MQTT client to achieve more complex business logic based on business requirements.

Next, readers can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
