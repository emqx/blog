[MQTT X](https://mqttx.app/zh) 是由 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，支持 macOS、Linux、Windows 系统。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的[MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接/发布/订阅功能及其他 [MQTT 协议特性](https://www.emqx.com/zh/mqtt)。

近日，MQTT X v1.7.0 正式发布。从这一版本起，MQTT X 将进一步支持 MQTT 5.0 的诸多新特性，这也是全球目前为止对 MQTT 5.0 支持最为完整的桌面测试客户端工具。

> MQTT X 网站：[https://mqttx.app/zh](https://mqttx.app/zh)
>
> MQTT X v1.7.0 版本下载：[https://www.emqx.com/zh/try?product=MQTTX](https://www.emqx.com/zh/try?product=MQTTX)
>
> Mac 用户可在 App Store 中进行下载：[‎https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)
>
> Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![MQTT X v1.7.0 界面一览](https://static.emqx.net/images/ba629cd3f538e19317d9a782ea43c0c8.png)

<center>v1.7.0 界面一览</center>

## 更全面的 MQTT 5.0 支持

在 1.7.0 版本中，MQTT X 新增很多关于 MQTT 5.0 的属性配置功能支持，使其成为目前同类工具中支持 MQTT 5.0 最为完整的 MQTT 桌面客户端工具。

>要想对 MQTT 5.0 的特性进行使用和测试，需要 MQTT X v1.7.0 与支持 MQTT 5.0 的 MQTT Broker 配合使用。
>
>[云原生分布式 MQTT 消息服务器 EMQX](https://www.emqx.io/zh) 从 3.0 版本开始支持 MQTT 5.0 协议，是开源社区中第一个支持该协议规范的消息服务器，并且完全兼容 MQTT 3.1 和 3.1.1 协议。使用 MQTT X 连接到 EMQX，就可以快速使用和测试 MQTT 5.0 的功能特性。

### 支持 MQTT 5.0 用户属性配置

新版本中我们首先支持了用户属性的配置。[用户属性](https://www.emqx.com/zh/blog/mqtt5-user-properties)是 MQTT 5.0 中一个非常实用的特性，它是一种自定义属性，允许用户向 MQTT 消息添加自己的元数据，传输额外的自定义信息以扩充更多应用场景。如果你熟悉 HTTP 协议的话，该功能与 HTTP 的 Header 的概念非常类似。

我们可以在创建客户端连接和发布消息时进行用户属性的配置。

### 扩展 MQTT 5.0 其它属性配置

除可配置用户属性外，1.7.0 版本还扩展了客户端连接和消息发布时的其他属性配置。

发送消息时，支持配置 Content Type，指定 Payload Format Indicator，用来描述应用消息的内容的格式，并指定消息内容是 UTF-8 编码的字符串。

支持主题别名的属性配置，可以有效节省带宽资源和计算资源。

支持 MQTT 5.0 中的[请求响应](https://www.emqx.com/zh/blog/mqtt5-request-response)，提供 Response Topic 和 Correlation Data，用以控制响应消息被路由回请求的发布者。

### 支持 MQTT 5.0 订阅选项

该版本中我们还对[订阅选项](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)进行了支持。支持了对 No Local flag、Retain as Published flag 和 Retain Handling 的设置，测试时，你可以使用这些订阅选项来改变服务端的行为。

在后续版本中我们还将继续支持[订阅标识符]( https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)等 MQTT 5.0 中的新特性。

## 更顺畅的使用体验

### 一键多主题订阅

在之前的版本中，我们每次打开订阅主题的弹框只能订阅一个主题，对于想要订阅多个主题的用户来说，每次都需要点击打开和关闭才能订阅多个主题，不是很方便。因此在新版本我们进行了优化，支持一次订阅多个主题，减少用户的重复操作。

### 禁止消息自动滚动

v1.7.0 设置中新增了对接收和发布消息时消息列表自动滚动的控制。自动滚动功能适用于当消息接收速率较慢时，可以帮助用户查看到最新消息。当接收消息的速率过快时，用户可以点击关闭该功能，以查看一些发送或接收到的旧消息。

> 注意：当关闭自动滚动功能后，可以提升部分发送和接收消息时的性能。

### 主题跟随操作系统主题变化（仅支持 macOS）

MQTT X 目前支持 Light、Dark 和 Night 三种主题模式，之前需要手动切换，新版本对此进行了优化。当操作系统的系统主题进行变化时，MQTT X 可以自动切换主题。当 macOS 系统主题是 Dark Mode 时，MQTT X 将自动切换到 Night 主题。

### 国际化扩展

借助来自社区的力量， MQTT X 的国际化扩展更进一步。除支持简体中文、英文、日文和土耳其文外，我们在一位匈牙利贡献者的帮助下，在 1.7.0 版本中实现了匈牙利语支持。

欢迎更多的社区伙伴参与贡献，和我们一起打造更加优秀的 MQTT X。

## 更精细的产品打磨

### 修复及优化

除添加上述新特性外，本次更新还修复了很多已知问题，稳定性得到了进一步提升。

- 修复自动重订阅设置的同步问题
- 修复导入/导出数据的问题
- 修复无法编辑已经创建的连接的问题
- 修复了 SSL/TLS 连接时，出现证书过期错误的问题
- 修复无法删除历史消息记录的问题
- 修复 Base 64 转化的问题
- 修复无法新建窗口的问题
- 修复连接列表连接时，出现乱序的问题

## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 更完整的 MQTT 5.0 支持
- 插件系统（例如支持 SparkPlug B）
- MQTT Debug 功能
- 脚本功能优化

## 结语

MQTT X 为连接测试 EMQX 等 MQTT 消息服务器而生，通过一键式的连接方式和简洁的图形界面帮助使用者进行 MQTT 特性探索和功能组件调试。除提供基础 MQTT 测试连接功能，全开源和社区驱动等特性还使其集成了更多丰富、强大、符合用户使用习惯的功能特性。结合 MQTT X 与云原生分布式消息中间件 [EMQX](https://www.emqx.com/zh/products/emqx)，我们相信物联网平台的测试开发工作将变得更加轻松。

MQTT X 项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈，每一个社区用户的使用与肯定，都是我们产品前进的动力。
