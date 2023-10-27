[MQTTX](https://mqttx.app/zh) 是由全球领先的物联网数据基础设施软件供应商 [EMQ 映云科技](https://www.emqx.com/zh/about) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 桌面测试客户端，支持 macOS、Linux、Windows 系统。MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端连接**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的**连接/发布/订阅**功能及其他 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)特性。


MQTTX 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTTX v1.7.1 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.7.1](https://github.com/emqx/MQTTX/releases/tag/v1.7.1)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![MQTTX v1.7.1 预览](https://assets.emqx.com/images/43556de4591acb8b2a59e3dfc9b19f6e.png)

<center>v1.7.1 界面一览</center>


## 新功能预览

### 支持 MQTT 5.0 订阅标识符

该版本中，除支持 MQTT 5.0 订阅选项后，我们还新增了对于[MQTT 订阅标识符](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)的支持，允许在订阅报文中指定一个数字订阅标识符，并在消息分发时返回此标识符。客户端可以建立订阅标识符与消息处理程序的映射，以在收到 PUBLISH 报文时直接通过订阅标识符将消息定向至对应的消息处理程序，这会远远快于通过主题匹配来查找消息处理程序的速度。

![MQTTX 支持 MQTT 5.0 订阅标识符](https://assets.emqx.com/images/517ba3105f469e68bde29d500db9b249.png)

### 展示更多 MQTT 5.0 属性

该版本中我们对于 MQTT 5.0 的属性展示做了优化，除展示用户属性外，还支持展示发送和接收时，消息体内包含的内容类型、订阅标识符、主题别名，响应主题，对比数据，同时也优化了对于用户属性的展示。

![MQTTX 支持更多 MQTT 5.0 属性](https://assets.emqx.com/images/1214bdfe30e0f08dd3548e13ce761c1c.png)

### 支持编辑/启用/禁用 Topic

该版本持续对 Topic 的操作进行了优化。在 1.7.1 版本之前，对于 Topic 列表只能进行添加和删除操作，当订阅的 Topic 过长时，需要修改时只能先删除取消订阅，然后再重新订阅，不是很方便，特别只是对于修改个别单词或者分隔符时。

与此同时该版本还支持了禁用/启用 Topic，当订阅的 Topic 过多时，有时候不是所有的 Topic 消息都想要接收到，但是避免再次订阅相同 Topic，该版本提供了禁用功能，需要重新接收该 Topic 的消息，只需再次启用即可。

右键点击已经订阅过的 Topic 列表项，在右键菜单中我们可以快速选择编辑、禁用或启动等操作。

![MQTTX 编辑/启用/禁用 Topic](https://assets.emqx.com/images/b5e6cfb89805c9f2dea19c0e13afc370.png)

### 其它

- 添加同步操作系统主题的开关。当开启该开关后，系统主题颜色将和操作系统主题同步。
- 上架 Linux Flathub，来自社区支持，Linux 用户还可以到：[https://flathub.org/apps/details/com.emqx.MQTTX](https://flathub.org/apps/details/com.emqx.MQTTX) 进行下载和安装。
- 加载页面更新

## 修复及优化

除添加上述新特性外，本次更新还修复了很多已知问题，稳定性得到了进一步提升。

- 修复发送用户属性时的问题
- 修复 Client ID 在数据库中唯一的问题
- 修复设置了 Topic Alias 后无法发送空主题
- 修复重订阅时无法同步 Topic 配置数据的问题
- 修复带有分组的数据无法导入的问题
- 修复重订阅机制
- 修复无法显示离线消息
- 修复新建窗口后的问题

## 未来规划

MQTTX 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 更完整的 MQTT 5.0 支持
- 插件系统（例如支持 SparkPlug B）
- MQTT Debug 功能
- 脚本功能优化

## 结语

MQTTX 为连接测试 EMQX 等 [MQTT 消息服务器](https://www.emqx.io/zh)而生，通过一键式的连接方式和简洁的图形界面帮助使用者进行 MQTT 特性探索和功能组件调试。除提供基础 MQTT 测试连接功能，全开源和社区驱动等特性还使其集成了更多丰富、强大、符合用户使用习惯的功能特性。结合 MQTTX 与云原生分布式消息中间件 EMQX，我们相信物联网平台的测试开发工作将变得更加轻松。

MQTTX 项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTTX 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈，每一个社区用户的使用与肯定，都是我们产品前进的动力。
