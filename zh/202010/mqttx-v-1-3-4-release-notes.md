[MQTTX](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTTX 网站：https://mqttx.app/zh

MQTTX v1.3.4 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.3.3

Mac 用户可在 App Store 中进行下载：https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12

Linux 用户可在 Snapcraft 中进行下载：https://snapcraft.io/mqttx

![mqttxpreview.png](https://assets.emqx.com/images/ea395ae029b369e5cd0f046f82be5411.png)

## 新功能概览

- 数据的备份与恢复

  在该版本中新增了数据的备份与恢复功能，用户可选择两种导入导出的方式，通过连接页面中的右上角菜单，和在设置页面中的高级功能栏里。

  点击连接页面中的右上角的菜单可以看到数据导出和数据导入两个选项，点击导出项后会出现弹出框，选择数据格式（目前仅支持 JSON），和设置是否导出全部连接。如果不是全部连接的话，仅导出当前页面中的单个连接数据，如果是的话，将导出软件内所有的连接数据。点击导入项后会出现弹出框，选择导入的数据格式和导入的文件路径，点击确认后即可轻松创建或更新数据。

![mqttxdropdownexport.png](https://assets.emqx.com/images/a1dd6f04c01f361e7cfb390075127375.png)

  在设置页面里可以在最下方的高级功能中，选择点击数据备份和数据恢复两个按钮。选择数据备份时，将导出所有的连接数据，包含所有收发到的消息等。选择数据恢复时，选择完导入文件的路径，确认后即可恢复数据。

  ![mqttxsettingexport.png](https://assets.emqx.com/images/7ccd6f49e35e057f8a881a02fa9039ae.png)

- 消息框支持点击右键菜单复制和删除

  在之前版本中，用户需要使用接收到的消息时，只能手动全选文本后，才能复制消息框内的内容。还有对于存在过多的消息量时，如果需要单独删除时，只能清空所有消息。该版本中对这些进行了优化，实现弹出右键菜单后点击即可复制和删除的操作，提升了易用性。

![mqttxmessagecopy.png](https://assets.emqx.com/images/40a96271bfd2fc857ffa5e6dc14f0163.png)

- 支持 Topic 别名

  在添加 Topic 时，可以给每个 Topic 设置一个别名，该选项为一个可选项，当设置并添加完成订阅后，订阅列表中的 Topic 数据将以别名展示，鼠标悬浮到 Topic 项时，提示框也会同时展示出该 Topic 的原值。这对于需要监控查看的多个 Topic 过长，无法分辩 Topic 的具体含义时，具有较强的帮助性。

  ![mqttxtopicalias.png](https://assets.emqx.com/images/cb1b92c2088a05a19f845eb35041fc13.png)

- 国际化支持，添加日文版本

## 修复及其优化

- 修复了在断开连接时，没有发送 disconnect packet 的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 提交使用过程中遇到的问题，或是 Fork MQTTX 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
