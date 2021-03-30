

[MQTT X](https://mqttx.app) 是由全球领先的开源物联网中间件提供商 [EMQ](https://emqx.io/cn) 开源的一款跨平台 **MQTT 5.0** 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：https://mqttx.app

MQTT X v1.3.0 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.3.0

![mqttxpreview.png](https://static.emqx.net/images/890cee487ea26b7b15b27d4642412e8e.png)

## 新功能概览

- 支持 WebSocket 连接

  该版本中，新增了对 WebSocket 的连接支持，在新建连接的页面中，`Host` 前的下拉框可以选择连接协议，支持 `mqtt://`, `ws://`，如果是 `SSL/TLS` 认证连接的话，需要选择为 `mqtts://`，`wss://`。当协议选项是 `ws` 或 `wss` 时，创建的连接即为 WebSocket 连接。

  **注意**：当协议变化时，需要修改连接的端口。

![mqttxbrokerinfo.png](https://static.emqx.net/images/b84ca95b501fb85155e0bb345db14f88.png)

- 支持对 Payload 的格式转化

  该版本中，对 Payload 的输入框进行了输入编辑时的优化。实现了对 JSON 格式的语法高亮，格式验证等功能，用户可以很方便的在输入框内进行 JSON 内容输入。同时，在 Topic 输入框上方的 Payload 选项中，还可以将当前内容快速转化为其它格式的内容，目前支持转化为 `Base64`，`Hex`, `Plaintext` 和 `JSON`。用户可以根据自己需求进行转化操作。

 ![mqttxmessage.png](https://static.emqx.net/images/1d1322eab2f308af1b3fbf4d9ea4721a.png)

- 可对输入框进行高度的自由调节

  在之前版本中，输入框的高度被固定，用户使用时可看到的 Payload 内容有限，如果发送内容过多，无法很好的在输入框内进行内容输入和编辑。经过优化后，用户可将鼠标放置到输入框顶部，当出现箭头时，拖动鼠标即可对输入框进行高度上的自由调整，以方便更好的对 Payload 内容进行处理。

![mqttxjson.png](https://static.emqx.net/images/720bdc89e8486568b9bac056c9eb1a05.png)

- 支持 Topic 模糊查询

  之前 Topic 只支持精准搜索，只能搜索到同一个 Topic 下的消息，目前支持了模糊查询，可以搜索过滤更为广泛的 Topic 消息。后续将继续优化对于利用 Topic 区分显示消息的功能，敬请期待。

- 在添加 Topic 的弹出框中，可使用 `Enter` 快捷键快速添加订阅

- 设置中添加了 MQTT 最大重连数

- 当连接成功，顶部面板自动折叠后，可在顶部栏点击红色按钮，快速断开连接

- 优化了证书选择，可以支持选择更多的证书格式文件

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。

