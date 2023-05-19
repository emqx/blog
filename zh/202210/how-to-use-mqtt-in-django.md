[MQTT](https://mqtt.org/) 是一种基于发布/订阅模式的轻量级物联网消息传输协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

[Django](https://www.djangoproject.com/) 是一个开源的 Web 框架，是目前较为流行的 Python Web 框架之一。本文主要介绍如何在 Django 项目中实现 [MQTT 客户端](https://www.emqx.io/zh/mqtt-client)与 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)的连接、订阅、取消订阅、收发消息等功能。

本文将使用 [paho-mqtt](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) 客户端库编写一个简单 MQTT 客户端，paho-mqtt 是目前 Python 中使用较为广泛的 MQTT 客户端库，它在 Python 2.7 及 3.x 上为客户端提供了对 MQTT v5.0、v3.1.1 和 v3.1 的支持。


## 项目初始化

本项目使用 Python 3.8 进行开发测试，读者可用如下命令确认 Python 的版本。

```shell
$ python3 --version
Python 3.8.2
```

使用 Pip 安装 Django 和 paho-mqtt。

```shell
pip3 install django
pip3 install paho-mqtt
```

创建 Django 项目。

```shell
django-admin startproject mqtt-test
```

创建完成后目录结构如下。

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


## paho-mqtt 使用

本文将使用 EMQ 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: `broker.emqx.io`
- TCP Port: `1883`
- Websocket Port: `8083`

### 导入 paho-mqtt

```python
import paho.mqtt.client as mqtt
```

### 编写连接回调函数

可以在该回调函数中对 MQTT 连接成功或失败的情况进行处理，本示例将在连接成功后订阅 `django/mqtt` 主题。

```python
def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('django/mqtt')  # 订阅主题
    else:
        print('Bad connection. Code:', rc)
```

### 编写消息回调函数

该函数将打印 `django/mqtt` 主题接收到的消息。

```python
def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
```

### 增加 Django 配置项

在 `settings.py` 中增加 MQTT 服务器的配置项。读者如果对如下配置项及本文中提到的 MQTT 相关概念有疑问，可查看博客 [MQTT 协议快速体验](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)。

> 本示例使用匿名认证，所以用户名与密码设置为空。

```python
MQTT_SERVER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_USER = ''
MQTT_PASSWORD = ''
```

### 配置 MQTT 客户端

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

### 创建发布消息接口

我们创建一个简单的 POST 接口实现 MQTT 消息发布。

> 在实际应用中该接口可能需要进行一些更复杂的业务逻辑处理。

在 `views.py` 中增加如下代码。

```python
import json
from django.http import JsonResponse
from mqtt_test.mqtt import client as mqtt_client


def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})

```

在 `urls.py` 中增加如下代码。

```python
from django.urls import path
from . import views

urlpatterns = [
    path('publish', views.publish_message, name='publish'),
]
```

### 启动 MQTT 客户端

在 `__init__.py` 中增加如下代码。

```python
from . import mqtt
mqtt.client.loop_start()
```

至此我们已完成了所有代码的编写，完整代码请见：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Django](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Django)。

最后，执行如下命令运行 Django 项目。

```bash
python3 manage.py runserver
```

当 Django 应用启动后，MQTT 客户端将会连接到 MQTT 服务器，并且订阅主题 `django/mqtt`。



## 测试

接下来我们使用[开源的跨平台 MQTT 客户端 - MQTTX](https://mqttx.app/zh) 进行连接、订阅、发布测试。

### 测试消息接收

1. 在 MQTTX 中创建 MQTT 连接，输入连接名称，其他参数保持默认，并点击右上角的 `Connect` 按钮连接至服务器。

   ![创建 MQTT 连接](https://assets.emqx.com/images/f9b4449af7ac15183ca9b66ea7210ed1.png)

2. 在 MQTTX 底部的消息发布框里向 `django/mqtt` 主题发布消息 `Hello from MQTTX`。

      ![发布 MQTT 消息](https://assets.emqx.com/images/1d138bc5e7720c3a8c938137e6472ecb.png)

3. 在 Django 运行窗口中将能看到 MQTTX 发送的消息。

      ![Django 接收 MQTT 消息](https://assets.emqx.com/images/ad1a0e19f4bb66c7ebb614eac362a22c.png)


### 测试消息发布接口

1. 在 MQTTX 中订阅 `django/mqtt` 主题。

    ![订阅 MQTT 主题](https://assets.emqx.com/images/fe6d48d40f8411a8921747d02ff8abc6.png)

2. 使用 Postman 调用 `/publish` 接口：发送消息 `Hello from Django` 至 `django/mqtt` 主题。

   ![Postman 调用发布接口](https://assets.emqx.com/images/047e4c70a29041ab23d67379b3114bce.png)

3. 在 MQTTX 中将能看到 Django 发送过来的消息。

   ![接收 MQTT 消息](https://assets.emqx.com/images/9490d8e462c63a461f5540032d03aadc.png)


## 总结

至此，我们使用 paho-mqtt 完成了 MQTT 客户端的开发，实现了在 Django 应用中使用 MQTT 进行通信。在实际应用中，我们可以根据业务需求对 MQTT 客户端进行扩展，实现更复杂的业务逻辑。接下来，读者可查看 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章了解 MQTT 协议特性，探索 MQTT 的更多高级应用，开始 MQTT 应用及服务开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
