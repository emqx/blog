[MQTTX](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTTX 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTTX v1.6.1 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.6.1](https://github.com/emqx/MQTTX/releases/tag/v1.6.1)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttx-preview](https://assets.emqx.com/images/9c1ad0d3e678954b67dce923087c7a7a.png)

> **注意：** 该版本包含破坏性改动！我们重构了底层数据存储结构，升级后将没有原来的数据，请提前备份好重要数据。（可以在设置页面中导出需要数据，在新版本中进行导入）。这是一个重构版本，没有更多的新功能，有问题可以到 [issue](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 区进行讨论。感谢你的帮助和支持。


## 新功能概览

- 支持在消息框内显示[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)的标识

## 修复及其优化

- 优化连接页面的加载样式
- 提高消息列表的显示性能（~10倍）
- 重构数据存储结构
- 修复数据库崩溃问题，在之前的版本中经常数据写入错误后，数据库崩溃导致无法打开软件的问题
- 修复历史消息记录问题
- 修复重新打开客户端时的数据格式转换错误

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTTX 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！:)
