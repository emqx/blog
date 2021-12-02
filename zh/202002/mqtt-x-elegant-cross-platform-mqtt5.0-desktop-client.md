**MQTT X** 是由全球领先的开源物联网中间件提供商 [EMQ](https://github.com/emqx/emqx) 开源的一款跨平台 MQTT 5.0 桌面客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建连接保存并同时建立多个连接客户端，方便用户快速测试 MQTT/TCP、MQTT/TLS 的连接、发布/订阅功能及其他特性。

项目地址：[GitHub](https://github.com/emqx/MQTTX)

官方网站：[MQTT X Website](https://mqttx.app/zh)

![WX202002101233322x.png](https://static.emqx.net/images/f5084e406711cb780796e21b42d9c3b4.png)

MQTT X 适用于正在搭建自己的 MQTT 的消息服务器的用户来测试连接，订阅和发布消息等，在使用客户端时，用户既可以是发布者，也可以是订阅者。也适用于正在开发或研究 MQTT Broker 的相关用户。在 MQTT 的研究与应用中，无论你身处什么阶段 都可以通过 MQTT X 快速、深入地理解 MQTT 协议相关特性。

该项目完全开源，项目采用了 Vue.js + TypeScript + Electron 的技术栈进行开发，你可以在 [GitHub](https://github.com/emqx/MQTTX) 上查看和浏览项目源码。欢迎前来一起讨论和学习 Electron 项目开发技术。



以下为 MQTT X 的特性和界面的预览：

- 跨平台，支持 Windows，macOS，Linux

- 完整支持 MQTT v3.1.1 以及 MQTT v5.0 协议

- 支持 CA、自签名证书，以及单、双向 SSL/TLS 认证
- 多界面主题，支持 Light、Dark、Night 三种主题模式切换
- 订阅 Topic 时可自定义颜色标记
- 支持简体中文以及英文
- 支持 MQTT/TCP 连接和 MQTT/WebSocket 连接
- 支持 $SYS 主题自动订阅，并可按层级展开
- 支持多种 Payload 格式 Hex, Base64, JSON, Plaintext
- 简洁的图形化界面
![mqttxpreview.png](https://static.emqx.net/images/9d345953e1186c0b691fd516a84583a5.png)

在 MQTT X 的主窗口中，最左侧为菜单栏，从上往下分别对应为：连接页面，关于页面和设置页面；中间一栏为现有连接列表，每次创建连接后，新的连接就会在列表中出现，点击列表中的名称（`name@host:port` 组成）可快速切换连接；最右侧为连接的主视图界面，可在该页面中进行消息的测试收发等。当连接建立成功后，顶部配置栏会自动折叠，以展示更多的页面空间。



- MQTT X 是新推出的产品，采用了 Electron 跨平台技术，界面美观且资源占用较低，MQTT X 在交互上一改常见的单一客户端模式，允许保存多个连接信息；
- 使用简单，能够快速创建连接，且提供了较为全面的 MQTT 参数配置，以便用户应对任何使用场景、使用方式的模拟测试，包括对于 MQTT v5.0 的支持；
- 以消息聊天的交互形式收发消息，交互流程简单易懂，允许同时建立多个客户端连接并自由切换互相通信，有较好的交互性，大大提高了交互调试的效率；
- 完全开源，支持多平台。

![666.png](https://static.emqx.net/images/4d53d9549016dfc34e4462b154047fb8.png)

截止目前 MQTT X 发布了 v1.2.3 版本，后续更多功能仍在开发中。
