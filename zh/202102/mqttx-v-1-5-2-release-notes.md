
[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.cn/) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.cn/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.5.2 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.2](https://github.com/emqx/MQTTX/releases/tag/v1.5.2)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://static.emqx.net/images/fdeeaa3093e114157fdbf46fd18bcd32.png)

## 新功能概览

- 优化订阅的 Topic 项的样式和点击 Topic 项过滤消息时的效果
- 支持快捷连接，当连接的信息面板折叠起来的时候
- 查看日志信息时，自动滚动页面到日志详情的底部
- 添加 Code of Conduct，[贡献者行为准则](https://github.com/emqx/MQTTX/blob/master/.github/CODE_OF_CONDUCT_CN.md)

## 修复及其优化

- 修复了出现 JavaScript Uncaught Exception 的错误提示框，当在 Windows 系统中关闭 MQTTX 1.5 或 1.5.1时
- 修复了路由从其他页面跳转到创建和连接时的编辑器错误
- 修复无法记录错误的连接失败日志
- 修复了当发送其他主题过滤器时无法记录日志消息的问题
- 修复了由于连接名称过长，引起的布局错乱的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！: )