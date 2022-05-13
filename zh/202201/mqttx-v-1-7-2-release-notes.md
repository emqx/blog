[MQTT X](https://mqttx.app/zh) 是由全球领先的物联网数据基础设施软件供应商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，支持 macOS、Linux、Windows 系统。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端连接**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的**连接/发布/订阅**功能及其他 [MQTT 协议](https://www.emqx.com/zh/mqtt)特性。

> MQTT X 网站：[https://mqttx.app/zh ](https://mqttx.app/zh)
>
> MQTT X v1.7.1 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.7.2 ](https://github.com/emqx/MQTTX/releases/tag/v1.7.2 )
>
> Mac 用户可在 App Store 中进行下载：[‎](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)
>
> Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![MQTT X 界面](https://assets.emqx.com/images/d88034adb1312466ca146e27c36c4b74.png)

## 新功能预览

### 共享订阅支持 Topic 颜色标记

共享订阅也支持了 Topic 的颜色标记，在使用[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)时，MQTT X 也可以通过自定义颜色标记来区分出当前消息来自于哪个共享订阅。

![MQTT X 共享订阅](https://assets.emqx.com/images/9b686e84a1671c793dbbcb68aea2ec13.png)

### 增加更多的 ARM 包

该版本我们新增了一些可以支持在 ARM64 架构的机器上使用的安装包，对于 macOS 系统和 Linux 系统的用户，无论是什么架构，都可以下载对应的安装包使用。目前使用 ARM64 的包需要到 [Github](https://github.com/emqx/MQTTX/releases/tag/v1.7.2) 或 [官方下载地址](https://www.emqx.com/zh/downloads/MQTTX/v1.7.2) 内找到包含有 `arm64` 的后缀的包来下载和使用。

![MQTT X 下载列表](https://assets.emqx.com/images/e3f5a841c487f56d4cda3d848b6482a1.png)

### 支持设置重连周期

在新建或编辑连接时，该版本对重连部分进行了优化，当设置了连接可以自动重连时，我们还可以配置每次重连时的时间间隔，也就是重连周期，默认是 `4000ms`，注意这里单位是毫秒。

![MQTT X 设置重连周期](https://assets.emqx.com/images/261b7ae46dd61558475fae4b23008d79.png)

 
## 修复及优化

除添加上述新特性外，本次更新还修复了很多已知问题，稳定性得到了进一步提升。

- 修复了订阅新主题时会替换已订阅主题的问题
- 消息框宽度自适应屏幕
- 升级部分依赖提升安全性

## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 更完整的 MQTT 5.0 支持
- 插件系统（例如支持 SparkPlug B）
- MQTT Debug 功能
- 脚本功能优化

## 结语

MQTT X 为连接测试 EMQX 等 [MQTT 消息服务器](https://www.emqx.io/zh)而生，通过一键式的连接方式和简洁的图形界面帮助使用者进行 MQTT 特性探索和功能组件调试。除提供基础 MQTT 测试连接功能，全开源和社区驱动等特性还使其集成了更多丰富、强大、符合用户使用习惯的功能特性。结合 MQTT X 与云原生分布式消息中间件 EMQX，我们相信物联网平台的测试开发工作将变得更加轻松。

MQTT X 项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈，每一个社区用户的使用与肯定，都是我们产品前进的动力。
