[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.cn/) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.cn/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.6.0 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.6.0](https://github.com/emqx/MQTTX/releases/tag/v1.6.0)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://static.emqx.net/images/cabac14e0c8f75080b659ea72294f97a.png)

## 新功能概览

- 全新的 UI 设计

  在新版本中，我们对 MQTT X 的 UI 进行了升级，提升了界面的软件质感和交互优化。更好的适配了多主题的样式，使用户能在不同的系统主题下使用，避免长时间使用后的视觉和审美疲劳感。

  ![MQTT X dark theme](https://static.emqx.net/images/9241dff3da0149815ee978b06b830509.png)

  ![MQTT X night theme](https://static.emqx.net/images/b864999d4888c7a2c694fa18c6888189.png)

- 支持右键菜单选择美化 JSON 格式数据和接收 JSON 格式数据时的自动美化

  在长时间的使用和观察下发现，JSON 是 MQTT X 用来发送和接收数据最常用数据格式之一，非手动编写的 JSON 数据可能存在格式不美化，难以查看数据的情况。该版本中优化了该问题，可以将复制粘贴到 Payload 编辑器中不美化的 JSON 数据进行格式美化功能，点击右键，选择 `Beautify format` 即可自动美化，或直接使用 `Cmd | Ctrl + B` 来进行快捷美化。

  ![MQTT X JSON 美化 1](https://static.emqx.net/images/65ef92b637e60c15124ee90d69b5eb28.png)

  对于接收到的数据如果是 JSON 格式的，可以在消息框上方选择接收的消息格式为 JSON。此时接收到 JSON 数据会进行自动美化格式，更将方便于用户查看接收数据信息。

  ![MQTT X JSON 美化 2](https://static.emqx.net/images/4db1fc9b22d86a21490108429fa2dd5b.png)

- 新增 `rpm` 和 `deb` 安装包

  之前对于 Linux 系统仅提供了 AppImage 和 snap 格式的安装包，该版本中扩展了其安装包类型，新增了 `deb` 和 `rpm` 格式的安装包。

- 为窗口添加可缩小的最小宽度和最小高度

  添加窗口的可缩小的最小宽度和最小高度可防止在部分情况下，用户无意拖动窗口大小时，造成的页面布局塌陷或不适配的问题，影响使用。

- 适配 macOS 新的图标设计

  在最新版本中，我们适配了 macOS 中的新的图标设计规范，使用了圆角加白色背景的设计风格。

  ![MQTT X 新 logo](https://static.emqx.net/images/503ff92d80f6e6222505a3a0aad29a36.png)

## 修复及其优化

- 修复了历史数据无法回退 Payload 类型的问题
- 修复了无法在历史数据中发送 Hex 和 Base64 格式的数据
- 修复了重连时的 BUG
- 修复了无法正确恢复编辑器宽度的问题
- 修复表单字段名的宽度错位问题
- 修复了使用 ESC 按键退出分组名称的输入时的报错
- 优化了点击新建分组按钮后，自动聚焦到分组名称的输入框
- 优化 Payload 编辑器的输入体验
- 优化自定义系统滚动条的样式

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 [Star](https://github.com/emqx/MQTTX) 进行鼓励！:)
