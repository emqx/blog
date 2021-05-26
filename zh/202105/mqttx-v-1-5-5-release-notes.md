[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.cn/) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.cn/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.5.5 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.5](https://github.com/emqx/MQTTX/releases/tag/v1.5.5)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://static.emqx.net/images/aa86f5835a6f7a5ce59aecf39990e493.png)

## 新功能概览

### 订阅列表持久化

在该版本中，新增了对 Topic 列表的持久化存储的功能，无论配置 `Clean Session` 为何值，断开客户端连接后，订阅列表都不会被自动删除，方便用户长期查看和管理连接的 Topic。

### 自动恢复订阅

当连接的 Topic 列表支持持久化存储后，如果连接的 `Clean Session` 的值为 `True`，即使重连后，Topic 列表也不可用，此时的订阅已经失效，需要手动再次订阅。此时，在设置页面中提供了一个自动恢复订阅的设置选项。打开该设置后，当连接重连时，如果有存储的 Topic 列表，客户端会自动进行订阅恢复，对于测试时订阅数多或者复杂的场景，避免了每次去手动重新订阅的问题。

![mqttxautoresub.png](https://static.emqx.net/images/dc808e9c451f84885520105cbeb58d6a.png)

### 添加 EMQ X Cloud 链接

对于无法马上连接到本地或已部署好的 MQTT Broker 的做测试和调试的用户，提供了 EMQ X Cloud 的链接，免费体验[云原生的全托管 MQTT 服务](https://cloud.emqx.cn/)。

![mqttxcloud.png](https://static.emqx.net/images/a2fab283b655c58a9600f82f4c6d03ba.png)

## 修复及其优化

- 修复下拉框的宽度被固定的 BUG
- 修复历史记录中的 Payload Type 无法恢复的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！:)
