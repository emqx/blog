[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.51 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.1](https://github.com/emqx/MQTTX/releases/tag/v1.5.1)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://static.emqx.net/images/fbd24ad549dd807461a4f77eb4b1d871.png)
**注意：** 该版本包含介绍了 1.5.0 版本的更新，1.5.1 提升了更多的稳定性，对于使用 1.5.0 版本的用户推荐更新到 1.5.1 版本。

## 新功能概览

- 日志系统

  在 v1.5.0 版本后，MQTT X 引入了日志记录功能，方便用户调试连接、报告错误。生产环境下，日志系统显示 3 个级别的信息：

  - `INFO` 用于提示用户操作信息
  - `WARN` 产生不安全/潜在风险的警告
  - `ERROR` 产生失败的错误

  默认情况下，日志会被写入 log 文件：

  - Linux: `~/.config/MQTTX/logs/log`
  - macOS: `~/Library/Application Support/MQTTX/logs/log`
  - Windows: `%USERPROFILE%\AppData\Roaming\MQTTX\logs\log`

  在每次关闭 MQTT X 时，当前的日志文件会被重命名为 timestamp `[YY]-[MM]-[DD]T[hh]:[mm].log` 格式。

  ![mqttxlog.png](https://static.emqx.net/images/6a1acc82b2a554aa2b360b28750676ec.png)

## 修复及其优化

- 修复无法编辑 `Payload` 的问题
- 修复使用快捷键 `cmdOrCtrl + enter` 发送消息时，出现重复的问题
- 修复无法读取日志文件的问题
- 修复 `Client ID` 无法自动刷新的问题
- 修复从编辑连接页面跳转到创建页面时，无法初始化数据的问题
- 加入正在连接状态当面板处于折叠状态时
- 优化部分弹出框样式
- 修改 EMQ X Logo
- 加入 GitHub 的 issue 模版，包含： **Bug_Report**, **Feature_Want**, **Help_Wanted**

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！: )
