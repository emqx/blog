## LwM2M 协议介绍

LwM2M 是一种轻量级的物联网设备管理协议，由 OMA（Open Mobile Alliance）组织制定。它基于 CoAP （Constrained Application Protocol）协议，专门针对资源受限的物联网设备设计，例如传感器、智能表计等，它们通常由电池供电，并且 CPU、内存、网络链接资源有限。

### 协议栈结构

![协议栈结构](https://assets.emqx.com/images/808ffadc53b4ca2ba0af54b39868a61a.png)

LwM2M 协议栈有以下几个特点：

- 应用层除了协议本身定义了一套标准的对象资源模型外，也允许用户进行自定义对象模型。
- 传输层上一般是常用的 CoAP/UDP，使其在兼顾轻量的前提下，也提供了一定程度的可靠性保证。
- 传输安全上采用 DTLS 协议，支持 Pre-Shared Key、Raw Public Key、X.509 证书等多种安全模式。
- 网络层一般以 UDP + IPv4/6 和 SMS 为主，同时也支持将其部署在 NB-IoT、TCP、LoRAWAN 等网络上。

### 资源模型

资源模型是 LwM2M 协议的核心，它定义了客户端与服务器之间的通信规范。客户端按该定义的数据格式向服务器上报数据，服务器通过资源模型向客户端对应的资源发送读、写、执行等控制命令。

下图展示了客户端（LwM2M Client)、对象（Objects）和资源（Resources）之间的关系，客户端可能有多个类型的资源，每个资源都隶属于某个对象：

![资源模型](https://assets.emqx.com/images/c06be1948effd185f49ea74ef7044edc.png)

所有标准的对象和资源都存在一个固定的编号，他们由 [OMA LwM2M Registry](https://www.openmobilealliance.org/lwm2m/resources/registry) 进行统一维护。

例如，用于温度传感器类设备的对象 Id 为 3303，它定义了：

- **Resource 5700**: Sensor Value (current temperature reading) 

  资源 5700：传感器值（当前温度读数）

- **Resource 5701**: Sensor Units (units of the temperature reading, e.g., Celsius or Fahrenheit)

  资源 5701：单位（例如，摄氏度或华氏度）

- **Resource 5601**: Min Measured Value (minimum recorded temperature)

  资源 5601：最小测量值

- **Resource 5602**: Max Measured Value (maximum recorded temperature)

  资源 5602：最大测量值

LwM2M 协议支持在对象和资源上定义允许的操作，例如：

- **Read**: 获取资源的当前值
- **Write**: 设置新值
- **Execute**: 调用定义在资源上的函数
- **Observe/Notify**: 订阅该资源值的变化，并实时进行通知

### 优势和主要应用场景

综上可见，LwM2M 协议的主要优势有：

- **轻量级：**基于 CoAP 和 UDP 协议，网络开销小，适合资源受限设备。
- **远程管理：**定义了多种标准化的资源，支持设备升级、资源状态查询、监控等操作。
- **灵活的资源模型：**LwM2M 的资源模型允许灵活地表示设备能力，可根据具体应用定义自定义资源。
- **安全性：**支持 DTLS 安全传输，确保设备数据的安全性。

主要适用的场景有：

- **智慧城市：**管理路灯、交通传感器和环境监测设备。
- **交通运输：**跟踪和管理车队车辆，优化物流，监控车辆健康状况。
- **工业物联网：**在工厂环境中监控和管理机器、传感器和执行器。
- **智慧农业：**远程管理土壤传感器、气象站和灌溉系统。
- **智能制造：**监控和管理机器、传感器和生产线，以提高效率和实现预测性维护。
- **医疗保健：**管理可穿戴健康监测设备和医疗设备。

## 使用 EMQX 接入 LwM2M 协议

EMQX 是一款大规模分布式 MQTT 消息服务器，功能丰富，专为物联网和实时通信应用而设计。EMQX 除了完整支持 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)之外，还可通过网关有效地管理 STOMP、MQTT-SN、CoAP、LwM2M 等非 MQTT 协议的连接、身份验证和消息传输等，并提供统一的用户界面以简化使用。

EMQX 提供了强大的内置 LwM2M 网关功能，能够高效地接入各类 LwM2M 设备。它支持基于 UDP 或 DTLS 的设备连接方式，确保了设备通信的安全性和稳定性。通过 EMQX Dashboard，用户可以轻松地进行设备管理。此外，LwM2M 网关还具备强大的消息转换能力，能够将 LwM2M 消息与 JSON 格式的 MQTT 消息进行相互转换。这一功能不仅实现了设备上行消息的结构化解析，方便用户对设备数据进行进一步的处理和分析，还支持通过 JSON 格式的消息下行操作，实现对设备的灵活控制。这种双向转换机制，使得 EMQX 在物联网设备管理和数据交互方面表现得更加出色，为复杂的物联网应用场景提供了强大的支持。

### 启用 LwM2M 网关

EMQX 5 及其以上的版本支持通过 EMQX Dashboard 在网页上进行启动 LwM2M 网关。

首先，使用以下命令启动 EMQX 5.8.4，并将端口 1883、18083、5684 映射到宿主机上：

```shell
sudo docker run -d --name emqx584 \
     -p 18083:18083 \
     -p 1883:1883 \
     -p 5783:5783/udp emqx/emqx:5.8.4
```

然后打开 EMQX Dashboard，通过 “Managment“ → “Gateway“  进入到网关管理页面，选中 ”LwM2M“ 开始配置：

![Management → Gateway](https://assets.emqx.com/images/81660ca53c39e3bb508b1bdd72739fcc.png)

所有页面都保持默认配置即可，配置完成后显示以下提示，即表示成功开启 LwM2M 网关：

![Gateways](https://assets.emqx.com/images/33f93da2301d601aa344ce93486684c1.png)

### 启用 LwM2M 客户端和消息收发

在本示例中，你可以选择手动编译安装 [wakaama](https://github.com/eclipse/wakaama) 以提供 LwM2M 客户端的支持，或使用已经预编译好的 Docker 镜像进行测试。以 Docker 为例：

1. 先通过 Docker 启动 MQTTX-CLI，用于观察 LwM2M 上线过程：

   ```shell
   sudo docker run -it --rm --network host emqx/mqttx-cli
   ```

1. 订阅 `up/#` 主题以接收 LwM2M 客户端产生的消息：

   ```shell
   mqttx sub --topic up/#
   ```

1. 使用 Docker 启动 wakaama 命令行容器：

   ```shell
   sudo docker run --rm -it --network host heeejianbo/my-wakaama:1.0
   ```

1. 在容器中，使用以下命令建立一个 LwM2M 客户端连接：

   ```shell
   lwm2mclient -l 57830 -p 5783 -h 127.0.0.1 -4 -n testlwm2mclient
   ```

1. 在 mqttx 客户端观察到以下消息，则表示 LwM2M 客户端成功登录到 EMQX 中：

   ```shell
   topic: up/register, qos: 0
   {"msgType":"register","data":{"objectList":["/1","/1/0","/2/0","/3/0","/4/0","/5/0","/6/0","/7/0","/31024","/31024/10","/31024/11","/31024/12"],"lwm2m":"1.1","lt":300,"ep":"testlwm2mclient","b":"U","alternatePath":"/"}}
   topic: up/resp, qos: 0
   {"msgType":"observe","is_auto_observe":true,"data":{"reqPath":"/3/0","content":[{"path":"/3/0","value":"W3siYm4iOiIvMy8wLyIsIm4iOiIwIiwidnMiOiJPcGVuIE1vYmlsZSBBbGxpYW5jZSJ9LHsibiI6IjEiLCJ2cyI6IkxpZ2h0d2VpZ2h0IE0yTSBDbGllbnQifSx7Im4iOiIyIiwidnMiOiIzNDUwMDAxMjMifSx7Im4iOiIzIiwidnMiOiIxLjAifSx7Im4iOiI2LzAiLCJ2IjoxfSx7Im4iOiI2LzEiLCJ2Ijo1fSx7Im4iOiI3LzAiLCJ2IjozODAwfSx7Im4iOiI3LzEiLCJ2Ijo1MDAwfSx7Im4iOiI4LzAiLCJ2IjoxMjV9LHsibiI6IjgvMSIsInYiOjkwMH0seyJuIjoiOSIsInYiOjEwMH0seyJuIjoiMTAiLCJ2IjoxNX0seyJuIjoiMTEvMCIsInYiOjB9LHsibiI6IjEzIiwidiI6MzEwNDg1ODkwM30seyJuIjoiMTQiLCJ2cyI6IiswMTowMCJ9LHsibiI6IjE1IiwidnMiOiJFdXJvcGUvQmVybGluIn0seyJuIjoiMTYiLCJ2cyI6IlUifV0="}],"codeMsg":"content","code":"2.05"}}
   ```

1. 再连接一个 MQTTX-CLI 的客户端，用于与 LwM2M 设备交互：

   ```shell
   sudo docker run -it --rm --network host emqx/mqttx-cli
   ```

1. 向步骤 3 中创建的 `testlwm2mclient` 客户端发送一条读指令，读取其设备的固件版本：

   ```shell
   mqttx pub --topic dn/testlwm2mclient -m '{"msgType": "read", "data": {"path": "/3/0/3"}}'
   ```

8. 可以观察到步骤1中创建的订阅端接收到了读指令的数据返回，其固件版本为 `1.0`：

   ```shell
   topic: up/resp, qos: 0
   {"msgType":"read","data":{"reqPath":"/3/0/3","content":[{"value":"1.0","path":"/3/0/3"}],"codeMsg":"content","code":"2.05"}}
   ```

 至此，一个简单的 LwM2M 连接和指令收发的示例便完成了。

### 管理 LwM2M 客户端

在 EMQX 中可以通过 Dashboard 对这三类设备进行管理。例如针对 MQTT，可以在对应网关的 **Clients** 页面进行查看：

![LwM2M Clients](https://assets.emqx.com/images/405528527fb19cba25f50e5c527d2a92.png)

<center>LwM2M Clients</center>

<br>

点击该客户端 ID 时，也可查看其详细的信息：

![LwM2M Client Info](https://assets.emqx.com/images/7c5b24affde8fa1b637a7b13c585c60e.png)

<center>LwM2M Client Info</center>

## 总结

LwM2M 协议在资源受限设备的场景中有着广泛的应用，它不仅提供了丰富的互操作语来实现设备之间的互联互通，还提供了丰富的安全机制以确保设备数据的安全性。EMQX 的 LwM2M 网关提供了简单的用户层接口，实现 LwM2M 协议的接入和设备管理。用户可以方便地将 LwM2M 设备接入到 EMQX 中，实现与 MQTT 协议的互通，进行更完整的设备数据采集、处理和分析。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
