[MQTTX](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端，** 方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTTX 网站：https://mqttx.app/zh

MQTTX v1.4.1 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.4.1

Mac 用户可在 App Store 中进行下载：https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12

Linux 用户可在 Snapcraft 中进行下载：https://snapcraft.io/mqttx

![mqttxpreview.png](https://assets.emqx.com/images/39bb4b3ea1775d78971b0f0f958e22aa.png)

## 新功能概览

- 收发流量统计（目前仅支持 EMQX）

  此功能可通过点击右上角的下来菜单，选择流量统计，MQTTX 会自动订阅系统主题，并可以在页面中展示该 Broker 下的简单的流量统计图表，运行版本和运行时间。

  > 注意：使用该功能时，可能会出现订阅系统主题失败的错误，此时可能是因为 EMQX 默认 **只允许** 本机的 MQTT 客户端订阅 $SYS 主题，或请参照 [内置 ACL](https://www.emqx.io/docs/zh/latest/advanced/acl-file.html) 修改发布订阅 ACL 规则。

  ![mqttxbytes.png](https://assets.emqx.com/images/6f10f501a0e5fb530f8bbc9929dd2e03.png)

- 支持定时发送 Payload

  此功能可通过点击右上角的下拉菜单，选择定时消息，这时会打开设置弹窗，用户只需填写发送消息的时间频率，单位为秒。设置成功后填写发送所需要的 Topic 和 Payload 等，手动点击发送一条消息后，即可成功打开定时消息功能，这时消息可按用户设置的时间频率进行定时发送。如需取消定时，可点击顶部栏中，断开连接按钮旁的时钟按钮，即可取消定时。

  ![mqttxtimedmessage.png](https://assets.emqx.com/images/5d968f5e1faa96bbf4845599c05b78cf.png)

- 支持显示当前连接的消息数

  当连接成功后，左上角的连接名称旁，将显示当前连接所有的收发消息数，当鼠标悬浮到该数字上时，还可以看到发送和接收到的消息数分别是多少。

  ![mqttxmessages.png](https://assets.emqx.com/images/d6a43d593c0593ae7663a9c2ac934fe1.png)

- 添加打开新窗口的快捷键

  在之前的版本中，打开连接的新窗口，需要右键点击连接，使用右键菜单功能才能打开新窗口，较为隐蔽且操作繁琐，该版本优化了此功能的交互，在每个连接的顶部栏中，下拉菜单按钮左侧新增了一个新建窗口按钮，当用户需要使用新窗口时，只需要点击该按钮即可。

  ![mqttxnewwindow.png](https://assets.emqx.com/images/a2ff6c71defc26c9106849a9082e2a05.png)

## 修复及其优化

- 修复只能连接到本地 MQTT Broker 的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTTX 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
