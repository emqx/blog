本文将以 [MQTT.fx](http://www.mqttfx.jensd.de/) 作为 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)测试工具，接入 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)。通过本文，你将能快速了解 MQTT.fx 的基础用法以及 MQTT 协议的基本概念与使用。



## MQTT.fx 简介

[MQTT.fx](http://www.mqttfx.jensd.de/) 是目前最为流行的 MQTT 桌面客户端工具，[MQTT.fx](http://www.mqttfx.jensd.de/) 1.0 Major 版本由 [Jens Deters](https://www.jensd.de/wordpress/) 使用[JavaFX](https://en.wikipedia.org/wiki/JavaFX) 技术开发，即为 Java 虚拟机应用。遗憾的是 [MQTT.fx](http://www.mqttfx.jensd.de/) 目前已经停止维护，并转为由 Softblade 公司资助开发另发行了其商业版本 [MQTT.fx® 5.0](https://softblade.de/en/mqtt-fx/)，采用收费许可证方式经营该软件。本文中的 [MQTT.fx](http://www.mqttfx.jensd.de/) 不经特殊说明即特指 1.0 版本。

它包含主流的 MQTT 客户端功能：

- 基本订阅/推送/连接功能
- 用户认证
- SSL/TLS连接支持
- [易用的消息编辑栏](https://github.com/Jerady/mqttfx-payload-decoders)
- 支持代理

此外 [MQTT.fx](http://www.mqttfx.jensd.de/) 也有其他优秀特性:

- 软件自由，其开源协议为 [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0)
- 支持跨平台
- 支持 $SYS 主题订阅管理 MQTT Broker
- 完整的日志控制台
- 支持 JavaScript 脚本处理消息
- 支持预定义模版

但同时也有缺陷：

- 不支持 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 协议
- 一次只能建立一个连接，不方便多连接调试
- 不支持 WebSocket 协议，无法调试 MQTT over Webscoket 的情况



## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为**全球首个全托管的** [**MQTT 5.0**](https://www.emqx.com/zh/mqtt/mqtt5) **公有云服务**，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

本文将使用 EMQX Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQX Cloud 文档](https://docs.emqx.cn/cloud/latest/)。 



## MQTT.fx 使用

### 预览

其主页面如下图所示，最上方为 MQTT Broker 连接地址栏，及其连接配置。其下方功能 Tabs 含有 Publish 发布栏、Subscribe 订阅栏、Scripts 脚本栏、Broker Status 状态消息栏、Log 日志信息控制栏。

![MQTT.fx 预览](https://static.emqx.net/images/571a6128a2fd2d71de4c6892997194dd.png)

其中每一个 Tab 均支持拖拽成为单独窗口，如下图所示：

![MQTT.fx 独立窗口](https://static.emqx.net/images/63fafd1866bf97e55a2d87a41cda901e.png)

### 连接

首先 MQTT client 与 Broker 通讯需要建立连接。点击连接地址栏中输入框右边的配置图标，进入具体的连接配置。

![MQTT.fx 连接按钮](https://static.emqx.net/images/3203ab53b9ccd95a1fa777cf96a1822a.png)

选择 Profile Type 为 MQTT Broker。Broker Address 填入 `broker-cn.emqx.io`，Broker Port 填入 `1883`，如下图所示：

> broker-cn.emqx.io 为国内服务器，broker.emqx.io 为国外服务器，读者可自行选择一个进行连接。

![MQTT.fx 连接配置](https://static.emqx.net/images/987021efd99c587008e00061c5abaabf.png)


点击OK，确认配置，回到主界面，点击 Connect ，可见右边的圆圈变为绿色，表示当前连接连通，如下图所示：

![MQTT.fx 连接成功](https://static.emqx.net/images/61c7866eebc762e0fdb7dca8ca669611.png)

### 订阅/发送消息

完成连接的建立之后，即可开始订阅消息。因为 MQTT 协议采用的是订阅/推送的方式，所以我们需要在连接之后订阅主题，之后主题上有消息产生即可收到来自 EMQX Cloud 推送。

![EMQX Platform](https://static.emqx.net/images/7c3fd862db7bfdc16ef51bbcda0d5b2c.png)

点击进入 Subscribe Tab 下，在主题框中输入 `/testTopic/1`，点击 Subscribe 订阅按钮，在左侧出现订阅的主题列表，订阅的主题目前消息数量为0，如下图所示:

![MQTT.fx 主题订阅](https://static.emqx.net/images/1e911b2c418c6f072dcb6969f8a95e4c.png)

之后，我们将把消息推送到 Broker，回到 Publish 下，并且输入主题 `/testTopic/1`，并在消息输入框中输入"hello world"等消息，如下图所示：

![MQTT.fx 消息发布](https://static.emqx.net/images/fa9bd621a9dee67a07ad481924c2b93c.png)

点击 Publish 发送，回到 Subscribe Tab，发现订阅的主题`/testTopic/1`收到消息，如下图所示：

![MQTT.fx 消息接收](https://static.emqx.net/images/43c8f23108d248f172a978e499b4d446.png)

我们使用 MQTT.fx 这一客户端向 EMQX Cloud 下的 `/testTopic/1` 主题发送了消息"hello wolrd"，订阅了这个主题的所有客户端都会收到这个消息，包括刚刚订阅了该主题的发送客户端。

### 脚本

使用脚本可以更加灵活地自定义消息推送逻辑，点击 Script Tab，点击 Edit 对脚本内容进行修改，修改为以下内容：

```jsx
function execute(action) {
    mqttManager.publish("/testTopic/1", "hello world from script");
    return action;
}
```

其中 `mqttManager` 是 MQTT.fx 脚本功能开放的 API，主要有：

- publish()，推送消息
- subscribe()，订阅主题
- unsubscribe()，取消主题订阅
- output，输出消息到控制台

点击 Execute 执行，之后回到 Subscribe 下发现消息增加，其内容为 “hello world from script”。脚本发送功能正常，如下图所示：

![MQTT.fx 脚本](https://static.emqx.net/images/1504963bd1d751dd481cd995faaccc03.png)

### 日志

在日志内，我们可以查看 MQTT.fx 与 EMQX Cloud 交互过程，例如主题订阅，消息推送，消息接收等：

![MQTT.fx 日志](https://static.emqx.net/images/cc3b9ee768d37b6cce66316135db261c.png)

### SSL/TLS连接

以 CA 自签名服务为例子，展示如何启用 SSL 协议连接到 EMQX Cloud。

打开设置，和普通连接一样填写好 Broker Address 和 Broker Port（分别为 `broker.emqx.io` 和 `8883`），选择 `SSL/TLS` 项，选择 TLSv1.2 协议，勾选 CA signed server certficate，之后选择应用，如下图所示：

![MQTT.fx SSL/TLS](https://static.emqx.net/images/f8f23d25ea6fba54837bea19e1076081.png)

点击连接，可以看到右边的锁图标是关闭的，表示启用了 SSL，查看日志，发现 SSL 连接相关端口 8883 相关字样，连接 SSL/TLS 成功。

![MQTT.fx 连接日志](https://static.emqx.net/images/5ea2e8316df5c33d907b6d784309a025.png)

![MQTT.fx SSL/TLS 状态](https://static.emqx.net/images/b3efb08a666b6c3dca2485b5fb5b403a.png)

以上就是使用 MQTT.fx 接入 EMQX Cloud 的简单示例，更多详情可访问 [EMQX Cloud](https://www.emqx.com/zh/cloud)。
