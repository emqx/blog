本文将以 [MQTTBox](https://github.com/workswithweb/MQTTBox) 作为 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)测试工具，接入 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)。通过本文，你将能快速了解 MQTTBox 的基础用法以及 MQTT 协议的基本概念与使用。

## MQTTBox 简介

[MQTTBox](https://github.com/workswithweb/MQTTBox) 是 Sathya Vikram 个人开发的 MQTT 客户端工具，最初仅在 Chrome 上作为拓展安装使用， 后经重写开源成为桌面端跨平台独立软件。界面简单直接，支持多个客户端同时在线，但客户端之间的切换、互发消息等交互还是有一些不便。MQTTBox 借助 Chrome 实现强大的跨平台特性，结合简单的负载测试功能，是一款值得尝试的 MQTT 客户端工具。

MQTTBox 完整的支持了以下功能：

- 通过支持 Chrome OS，Linux，macOS，Windows 的 Chrome 存储易于安装，支持 Linux、macOS、Windows 独立安装
- 支持 MQTT、MQTT over WebSocket，多种 TCP 加密方式的连接
- 保存发送的消息历史记录
- 复制/粘贴历史记录中的消息
- 保存订阅消息历史记录
- 简单的性能测试，对 Broker 的负载做出测试并通过图表可视化查看测试结果



## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为**全球首个全托管的** [**MQTT 5.0**](https://www.emqx.com/zh/mqtt/mqtt5) **公有云服务**，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

本文将使用 EMQX Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQX Cloud 文档](https://docs.emqx.cn/cloud/latest/)。 



## MQTTBox 使用

### MQTT 连接

#### 初始化页面

打开软件后，进入到软件主界面，点击顶部菜单栏的 `Create MQTT Clinet` 按钮，进入到创建 MQTT 客户端页。

![MQTTBox 界面](https://static.emqx.net/images/75d7f67d4c584a017f0f50ffd8a4f87e.png)

#### 创建连接

进入到创建 MQTT 客户端页面后，填写 Host、选择连接协议等 MQTT 相关配置信息后，点击底部的 `Save` 按钮即可立即创建一个连接客户端。

> 注意：填写 Host 时，需填入完整的地址，包含连接的端口号。如果是 WebSocket 连接，还需加上 Path。如果 MQTT Broker 开启用户名/密码认证的，还需要在配置页面内输入 Username / Password

![MQTTBox 创建连接](https://static.emqx.net/images/a83d9f97fbfea900e3105ed2618744b0.png)

此时保存成功后，会进入到一个客户端详情页面，如果右上角的按钮显示 `Connected` 并且为绿色，即表示该 MQTT 客户端已经成功连接，再次点击后可以断开客户端连接。

### 订阅主题

完成连接的建立之后，即可开始订阅消息。因为 MQTT 协议采用的是发布/订阅的模型，所以我们需要在连接之后订阅主题，之后主题上有消息产生即可收到来自 EMQX Cloud 推送。

在 MQTTBox 的客户端详情页面中默认有两个发送和订阅的输入框。如果有多个订阅或者不同的发布内容，可以添加多个，点击顶部菜单栏中的 `Add publisher` 和 `Add subscriber` 按钮可以添加和管理多个发布订阅。

我们先在右侧的黄色框内输入 Topic：`testtopic/mqttbox`，选择 QoS 等级后，点击 `Subscribe` 按钮即可订阅相关 Topic。

### MQTT 消息发布

然后我们在蓝色的框内输入要发布的 Topic，这里输入刚才订阅过的 `testtopic/mqttbox`，选择 QoS 级别，选择默认的 Payload Type，支持 `String / JSON / XML / Characters`，我们 Payload 的框内输入一段 JSON 后，点击 Publish 按钮。

此时我们可以看到右边的订阅框内，出现了刚才发布的消息。至此，我们已经创建了一个 MQTT 客户端并成功测试了连接、发布、订阅等功能。

![MQTTBox 消息发布](https://static.emqx.net/images/638cea055bb29c8b6265ac6df0496413.png)

### TLS/SSL 连接

除普通连接外，MQTTBox 还支持 TLS/SSL 连接。

如使用 EMQX Cloud 的话，可以参考该[文档](https://docs.emqx.cn/cloud/latest/deployments/tls_ssl.html#%E8%AF%81%E4%B9%A6%E9%99%90%E5%88%B6)来创建证书。我们可以进入到客户端详情页中，选择协议为 mqtts/tls 或者 wss，然后选择保存。

如果是双向认证的话，可以在配置页面中选择 CA 证书文件，客户端证书和客户端 Key 文件，再选择连接。连接前请确定 TLS/SSL 连接的端口并做修改。

![MQTTBox TLS/SSL 连接](https://static.emqx.net/images/485b86efcafdce32c30bc74199472285.png)
