[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端，** 方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTT X v1.5.3 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.3](https://github.com/emqx/MQTTX/releases/tag/v1.5.3)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![collection_group.png](https://assets.emqx.com/images/3fecd14eb079273cc5e027c5a78eb4f1.png)

## 新功能概览

- 加入了文件夹功能，以达到分组管理连接的功能

  - 基本功能：支持文件夹和连接的 **拖拽移动、** 展开和折叠，支持文件夹嵌套；
  - 支持在顶层新建文件夹，点击连接管理栏目右上角的图标即可在顶层新建文件夹；
  - 支持右键点击文件夹打开当前文件夹下的菜单，包含有：
    - 新建子文件夹
    - 删除当前文件夹
    - 重命名当前文件夹
  - **最佳实践：** 根据不同的服务器类型创建分组，拖拽连接到文件夹下，完成分类；

- 支持拖拽连接到窗口外以创建新的窗口

  拖拽一个连接并拉到窗口范围外，松手之后即可新建一个连接窗口

![new_collection.png](https://assets.emqx.com/images/41f9e89534c1d1e3d61e77f5b786aea7.png)

## 修复及其优化

- 修复了 SYS 主题拒绝提示非预期的错误
- 修复了复制主题提示信息消失问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。

如果您觉得该项目对您还有帮助，请在 GitHub 上给我们一个 Star 进行鼓励！:)
