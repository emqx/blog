[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端** ，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：https://mqttx.app/zh

MQTT X v1.4.0 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.4.0

Mac 用户可在 App Store 中进行下载：https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12

Linux 用户可在 Snapcraft 中进行下载：https://snapcraft.io/mqttx

![mqttxpreview.png](https://assets.emqx.com/images/8e995e772783202b5c5b50dc4799f800.png)

## 新功能概览

- 支持多窗口

  在该版本中，用户连接后需要监控消息收发时，不再只是通过单项视图去查看某一连接，可以在连接列表中，右键点击，选择新建窗口，为该连接创建新窗口。在新窗口中，同样可以进行连接，订阅主题，发布和接受消息等。如果当创建的多个连接之间存在某种联系时，或需要查看同时接受到的消息，可以新建多个视图窗口，同时进行查看。

![mqttxnewwindow.png](https://assets.emqx.com/images/c584749b8daf7c25d864740532ea4eaa.png)

![mqttxmutiwindow.png](https://assets.emqx.com/images/35209fb06c4bff335e6c49faaec14094.png)

- 新增导入导出数据格式

  在之前版本中，新增了数据的导入导出，但仅支持 `JSON` 格式的数据。该版本中对此进行了扩展，除 `JSON` 格式外，还支持了 `XML`，`CSV` 和 `Excel`。用户可以快速导出以上格式的数据，根据需求进行处理，也可以使用以上任意一种的数据格式，快速导入自定义数据，例如使用 Excel 快速生成测试用例，导入后进行快速测试。

  ![mqttxmoreformat.png](https://assets.emqx.com/images/ec94622bdd335b84041eaebcbf578657.png)

- 支持消息搜索

  在之前版本中，仅支持按 `Topic` 搜索来过滤消息内容，此版本中加入了消息搜索，打开搜索框后，右边多了一个消息输入框，可输入关键信息，消息框内会根据搜索内容进行过滤，也可以和 `Topic` 搜索一起进行联合查询。

![mqttxmessagesearch.png](https://assets.emqx.com/images/8b0c9c5625481449bc7ee4477e2a740f.png)

- 首屏加入加载动画

  首次打开程序时，加入了页面初始化时的加载动画

## 修复及其优化

- 优化页面消息动画显示
- 修复接受到消息无法自动滚动的问题
- 修复了页面切换时出现的错误

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
