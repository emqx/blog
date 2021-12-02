[MQTT Web Toolkit ](http://tools.emqx.io)是 EMQ 最近开源的一款 MQTT (WebSocket) 测试工具，支持线上 ([tools.emqx.io](http://tools.emqx.io)) 访问使用。该工具采用了聊天界面形式，简化了页面操作逻辑，方便用户快速测试验证MQTT应用场景。


### 功能简介

1. 支持通过普通或者加密的 WebSocket 端口连接至 MQTT 消息服务器；
2. 链接的新建、编辑、删除以及缓存链接方便下次访问使用；
3. 不同链接的订阅列表管理；
4. 消息发布、接收、以及接收到新消息时提示，同时也支持按照消息类型过滤消息列表。

### 使用指南

#### 创建/删除链接

使用浏览器打开地址 [tools.emqx.io](http://tools.emqx.io)，点击左下角的 **New Connection** 按钮，在弹出框里输入链接信息创建链接。

鼠标 **Hover** 到左侧链接列表里的某一项时，会显示删除图标，点击该图标可删除该链接。

![1.png](https://static.emqx.net/images/eb40a2eb67bcd01557b2eeb0982e8bd9.png)

#### 订阅管理

链接创建成功后，点击右上角的 **Connect** 按钮连接至 MQTT 服务器。连接成功后点击左上角的 **New Sub** 按钮弹出订阅列表框，在该页面可进行新建/取消订阅操作。

![2.png](https://static.emqx.net/images/b9e415ec480b4a0b3dc4f2954af39b30.png)

#### 消息发布/接收

点击页面右侧底部的输入框，可弹出消息发布框，填写好 **Topic** 及 **Payload** 字段后点击右下角的发布图标可发布消息，发布成功后的消息将会显示在消息列表的右侧。

订阅主题所收到的消息将会显示在消息列表的左侧，可点击右上角的消息类型切换按钮只显示已接收或是已发送的消息（默认显示所有消息）。
![3.png](https://static.emqx.net/images/bb2e8a7832420da8f0008b4508c8202a.png)



欢迎访问 [tools.emqx.io](http://tools.emqx.io) 在线试用。

------


![二维码](https://static.emqx.net/images/b99a97727d6f86a9912846e145b8b124.jpg)
