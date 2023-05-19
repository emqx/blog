[Flask](https://flask.palletsprojects.com/en/2.1.x/) 是一个使用 Python 编写的轻量级 Web 应用框架，其被称为 “微框架”，因为它使用简单的核心，用扩展增加其他功能，例如：ORM、窗体验证工具、文件上传、各种开放式身份验证技术等。

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种基于发布/订阅模式的 轻量级物联网消息传输协议 ，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、[车联网](https://www.emqx.com/zh/blog/category/internet-of-vehicles)、电力能源等行业。

本文主要介绍如何在 Flask 项目中实现 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)与 [MQTT 服务器](https://www.emqx.io/zh)的连接、订阅、取消订阅、收发消息等功能。

我们将使用到 [Flask-MQTT](https://flask-mqtt.readthedocs.io/en/latest/index.html) 客户端库 ，它是一个 Flask 扩展，可以看作一个 [paho-mqtt](https://www.eclipse.org/paho/clients/python/) 的装饰器，用于简化 Flask 应用程序中的 MQTT 集成。

## 项目初始化

本项目使用 Python 3.8 进行开发测试，读者可用如下命令确认 Python 的版本。

```
$ python3 --version
Python 3.8.2
```

使用 Pip 安装 Flask-MQTT 库

```
pip3 install flask-mqtt
```

## Flask-MQTT 使用

本文将使用 EMQ 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: `broker.emqx.io`
- TCP Port: `1883`
- Websocket Port: `8083`

### 导入 Flask-MQTT

导入 Flask 库以及 Flask-MQTT 扩展，并创建 Flask 应用

```
from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)
```

### 配置 Flask-MQTT 扩展

```
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # 当你需要验证用户名和密码时，请设置该项
app.config['MQTT_PASSWORD'] = ''  # 当你需要验证用户名和密码时，请设置该项
app.config['MQTT_KEEPALIVE'] = 5  # 设置心跳时间，单位为秒
app.config['MQTT_TLS_ENABLED'] = False  # 如果你的服务器支持 TLS，请设置为 True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)
```

完整的配置项可以参考 [Flask-MQTT 配置文档](https://flask-mqtt.readthedocs.io/en/latest/configuration.html)。

### 编写连接回调函数

可以在该回调函数中对 MQTT 连接成功或失败的情况进行处理，本示例将在连接成功后订阅 `/flask/mqtt` 主题。

```
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # 订阅主题
   else:
       print('Bad connection. Code:', rc)
```

### 编写消息回调函数

该函数将打印 `/flask/mqtt` 主题接收到的消息。

```
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
```

### 创建发布消息接口

我们创建一个简单的 POST 接口实现 MQTT 消息发布。

> 在实际应用中该接口可能需要进行一些更复杂的业务逻辑处理。

```
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})
```

### 运行 Flask 应用

```
if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
```

当 Flask 应用启动后，MQTT 客户端将会连接到服务器，并且订阅主题 `/flask/mqtt`。

## 测试

接下来我们使用 [MQTT 客户端 - MQTTX](https://mqttx.app/zh) 进行连接、订阅、发布测试。

### 测试消息接收

1. 在 MQTTX 中创建链接并连接到服务器。

   ![MQTTX 中创建链接](https://assets.emqx.com/images/0813905d4d732565476cdbf5275a65e2.png)

2. 在 MQTTX 中向 `/flask/mqtt` 主题发布消息 `Hello from MQTTX`。

   ![MQTTX 消息发布](https://assets.emqx.com/images/b4b533b9113da3735304c7b38397aa12.png)

3. 在 Flask 运行窗口中将能看到 MQTTX 发送的消息。

   ![Flask 接收 MQTT 消息](https://assets.emqx.com/images/ce56d6aa495c5193f0fe8fd63c911c40.png)


### 测试消息发布接口

1. 在 MQTTX 中订阅 `/flask/mqtt` 主题。

   ![MQTTX 订阅主题](https://assets.emqx.com/images/b2d98f1d30a9158444c2894294014dcf.png)

2. 使用 Postman 调用 `/publish` 接口：发送消息 `Hello from Flask` 至 `/flask/mqtt` 主题。

   ![Postman 调用发布接口](https://assets.emqx.com/images/901ac5434b526edd82c413c26cf21c72.png)

3. 在 MQTTX 中将能看到 Flask 发送过来的消息。

   ![Flask 发布 MQTT 消息](https://assets.emqx.com/images/3bcb310ab66fdb20b2f3d169673dd4b7.png)


### 完整代码

```
from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # 当你需要验证用户名和密码时，请设置该项
app.config['MQTT_PASSWORD'] = ''  # 当你需要验证用户名和密码时，请设置该项
app.config['MQTT_KEEPALIVE'] = 5  # 设置心跳时间，单位为秒
app.config['MQTT_TLS_ENABLED'] = False  # 如果你的服务器支持 TLS，请设置为 True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic)
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

## 注意事项

Flask-MQTT 目前不适合使用多个工作实例，如果您需要使用 *gevent* 或 *gunicorn* 这样的 WSGI 服务器，请确保只有一个工作实例。

## 总结

至此，我们使用 Flask-MQTT 完成了简单的 MQTT 客户端，并且可以在 Flask 应用中订阅、发布消息。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
