[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：https://mqttx.app/zh

MQTT X v1.3.3 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.3.3

Mac 用户可在 App Store 中进行下载：https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12

Linux 用户可在 Snapcraft 中进行下载：https://snapcraft.io/mqttx

![mqttxpreview.png](https://static.emqx.net/images/26e44fe583be1d22b0fca8da42d381e0.png)

## 新功能概览

- 使用 Toipc 的颜色标记接收消息，展示主题与消息之间的对应关系

  在 MQTT X 中添加订阅 Topic 时，可以选择对应颜色，对 Topic 进行区分。在该版本中还新增了当接收到订阅过的 Topic 消息时，消息框左侧会有和已订阅 Topic 一样的颜色标记，这样可以在接收到很多不同的 Topic 消息时，在视图中清晰明了的分辨出这些消息来源于哪个 Topic。

- 连接客户端列表支持点击右键菜单删除

  在之前版本中，对于删除不需要的连接客户端时，只能通过右上角的下拉菜单，选择删除选项才可以实现该操作，该版本中对此进行了优化，可以实现鼠标右键点击连接客户端的一栏，弹出右键菜单后点击删除即可完成该操作，提升了易用性。

   ![mqttxdelete.png](https://static.emqx.net/images/247b4af27bf276c9f6a5ca5ef2ae08b0.png)

- 支持对接收到的消息进行编码转化

  在之前版本中，MQTT X 支持在发送消息时，将 Payload 转化为 `Base64`，`Hex`, `Plaintext` 和 `JSON` 的编码格式。在该版本中对该功能进行了扩展，同时支持了对接收消息进行编码格式的转化，用户可以根据自己需求实现在发送端和接受端进行不同的消息格式编码转化。

  ![mqttxencode.png](https://static.emqx.net/images/e38e5c8b3b088fe309636f89061ec592.png)

- 支持快速选择已经创建过的 MQTT 连接配置

  对于每次创建新的连接客户端时，很多连接配置都会相同，因此在该版本中对其进行了优化，每当创建不同配置的连接时，都会对其进行存储。当用户下次需要创建相同配置连接时，便可以在连接名称一栏中，快速选择已经创建过的连接配置，从而达到快速创建连接的目的。

  ![mqttxconfig.png](https://static.emqx.net/images/cf2a890c9b9ba3ab1af0a04da93d8543.png)

- 支持在 MQTT 5.0 中配置遗嘱消息的属性

  新版本还对 MQTT 5.0 中的一些功能特性进行了支持。创建连接时，选择 MQTT 的版本为 5.0，便可以对遗嘱消息中的 `willDelayInterval`, `payloadFormatIndicator`, `messageExpiryInterval` 和 `contentType` 属性进行配置。

  ![mqttxwill5.0.png](https://static.emqx.net/images/54c5fa17474b0e3a56911dc6260b8607.png)



## 修复及其优化

- 修复当 `clean session = false` 时，接收到的离线消息会重复的问题
- 修复当发送 `Hex` 和 `Base64` 编码消息时，依然是字符串的问题
- 修复自签名证书认证无法连接的问题
- 修复无法建立 `wss` 连接的问题
- 当发送和接收到错误的 JSON 格式的消息时，给出格式错误提示
- SSL/TLS 连接验证时，当无法读取到证书文件时给出错误提示



该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。
