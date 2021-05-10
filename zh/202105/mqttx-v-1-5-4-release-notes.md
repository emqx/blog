[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.cn/) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.cn/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.5.4 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.4](https://github.com/emqx/MQTTX/releases/tag/v1.5.4)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)


![mqttxpreview.png](https://static.emqx.net/images/3c7493d6526eb7a02d42c3aa962f48f0.png)

## 新功能概览

- 支持对发送过的 Payload 历史记录进行保存

  当连接的客户端成功发送过一条 Payload 后，将会自动将 Payload 数据保存到历史记录，点击右下方左右按钮可快速切换保存过的历史记录，点击中间按钮可快速切换到最新的一条 Payload 。避免了每次发布消息时，都需要手动编辑的情况。


![mqttxpayload.png](https://static.emqx.net/images/c175486e82496d829b99da0c08f16f4e.png)

- 支持对发送过的 Topic 信息进行历史记录保存

  除自动保存 Payload 消息外，还将会自动保存发送的 Topic 信息，点击 Topic 输入框最右方的下拉按钮，可快速选择历史记录，同样也避免了每次发送前都需要手动输入 Topic 的问题。从而提升测试效率。


![mqttxtopic.png](https://static.emqx.net/images/2befce2f17c088c3afe05cc9df6065a5.png)

## 修复及其优化

- 修复连接列表高亮主题颜色问题
- 修复分组中连接序列显示的问题
- 修复连接高亮显示不正确的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！:)
