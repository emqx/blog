本文将以 [MQTTLens](https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm/related?hl=zh_cn) 作为 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)测试工具，接入 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)。通过本文，你将能快速了解 MQTTLens 的基础用法以及 MQTT 协议的基本概念与使用。



## MQTTLens 简介

[MQTTLens](https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm/related?hl=zh_cn) 是有一个 Chrome 拓展工具，可以通过 Chrome 网上应用商店安装。MQTTLens 界面非常简洁，提供基础的发布订阅功能。

MQTTLens 足够简单，借助 Chrome 有很强大的跨平台特性提供了基础的 [MQTT](https://www.emqx.com/zh/mqtt) 和 MQTT over WebSocket 连接功能，可以快速满足入门探索使用。

MQTTLens 完整的支持了以下功能：

- 能同时与多个 MQTT 服务器建立连接，并采用不同颜色区别
- 订阅、发布和查消息的界面非常简单且易于掌握
- 支持 MQTT 和 MQTT over WebSocket



## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为**全球首个全托管的** [**MQTT 5.0**](https://www.emqx.com/zh/mqtt/mqtt5) **公有云服务**，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

本文将使用 EMQX Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQX Cloud 文档](https://docs.emqx.com/zh/cloud/latest/)。



## MQTTLens 使用

### MQTT 连接

#### 初始化页面

我们进入到 Chrome 网上应用商店，点击安装后即可在 Chrome 中打开该应用。

进入到应用的主界面后，我们点击右边的 `Connections` 按钮可创建一个新的连接客户端。

![MQTTLens 界面](https://assets.emqx.com/images/017284bd21723e22993d75f23050348d.png)

#### 创建连接

点击创建按钮后，此时会出现一个 MQTT 相关配置填写的弹出框，填写 `Connection name`，`Hostname`、`Port`，选择连接协议等 MQTT 相关必要配置信息后，点击底部的 `CREATE CONNECTION` 按钮即可立即创建一个连接客户端。

MQTTLens 还支持对遗嘱消息的配置，在创建弹出框底部，点击 `Last-Will` 即可配置相关配置。

> 注意：如果 MQTT Broker 已开启用户名/密码认证的话，还需要在配置页面内输入 Username / Password

![创建连接](https://assets.emqx.com/images/314c56bdde5cbfc64d48813a52851929.png)

创建成功后，应用会进入到连接客户端的操作页面，如果右边的连接列表中的按钮变为绿色，即表示该 MQTT 客户端已经成功创建并连接成功。再次点击绿色按钮变为红色后，即可断开连接。点击右边的设置按钮可重新编辑客户端配置，点击删除按钮后可快速删除该连接。

### 订阅主题

完成连接的建立之后，即可开始订阅消息。因为 MQTT 协议采用的是发布/订阅的模型，所以我们需要在连接之后订阅主题，订阅成功后即可收到该主题的消息。

在 MQTTLens 的客户端的操作页面中，右边视图内分别有三个模块，分别是 `Subscrible`、`Publish` 和 `Subscriptions`。`Subscrible` 配置订阅主题，`Publish` 可以配置发送相关的数据和配置信息，当接收到消息时会在 `Subscriptions` 下面显示消息列表。

我们先在顶部的的 `Subscrible` 内输入 Topic：`testtopic/mqttlens`，选择 QoS 等级后，点击 `Subscribe` 按钮即可订阅相关 Topic。

### MQTT 消息发布

在 `Publish` 模块内输入要发布的 Topic，这里输入刚才订阅过的 `testtopic/mqttlens`，选择 QoS 级别，如果是 Retain 消息，需要勾选 Retained 选项。我们 Payload 的框内输入一段字符信息后，点击 Publish 按钮。

![MQTTLens 发布消息](https://assets.emqx.com/images/1022237564e692fa597e9236ecd81640.png)

此时我们可以看到底部的 `Subscriptions` 框内，出现了刚才发布的消息。至此，我们已经创建了一个 MQTT 客户端并成功测试了连接、发布、订阅等功能。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
