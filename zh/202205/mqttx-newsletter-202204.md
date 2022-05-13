>MQTT X 是一款由 EMQ 开源的 MQTT 5.0 跨平台桌面客户端。支持快速创建多个同时在线的 MQTT 客户端连接，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能及其他 MQTT 协议特性。
>
>社区站网址：[https://mqttx.app/zh](https://mqttx.app/zh) 
>
>GitHub 仓库：[https://github.com/emqx/MQTTX](https://github.com/emqx/MQTTX) 

在过去的一月中，MQTTX 发布了最新的 v1.7.3 版本（下载地址：[https://github.com/emqx/MQTTX/releases/tag/v1.7.3](https://github.com/emqx/MQTTX/releases/tag/v1.7.3) ），同时优化了在社区站中 MQTTX 安装包的下载方式。

## v1.7.3 版本概览

### 新增 ARM64 和 32bit 安装包

在该版本中我们新增了一些可以支持在 ARM64 架构和 Windows 32bit 的 CPU 机器上使用的安装包，对于 macOS、Linux 和 Windows 系统的用户，无论是哪种芯片或系统架构，都可以下载对应格式的安装包来使用。

### 支持 MQTT 3.1 版本

截止目前，MQTTX 除支持 MQTT 5.0 和 3.1.1 之外，同时也向后兼容并支持了 MQTT 3.1。也就是说， MQTTX 已支持了所有 MQTT 相关协议版本，可支持所有 MQTT 版本的测试连接，为用户提供了更加全面的连接测试能力。

### 为 QoS 添加注解

很多新手用户可能不太了解在发布订阅时如何选择 QoS。为此我们在发布和订阅页面中对 QoS 的每一个值进行了注解，方便刚开始接触 MQTT 的用户了解和使用 QoS。

![为 QoS 添加注解](https://assets.emqx.com/images/a6f8fc9d29b85c5df91ef8cb8c50c58b.png)

### 其他优化

- 优化了新建连接时，开启 TLS / SSL 的选项的样式
- 修复了一些安全性问题

## mqttx.app 社区站优化

### 下载方式优化

由于新版本增加了更多不同系统芯片架构下的安装包，我们对社区站中的下载部分也同步进行了优化。针对下载安装和显示的页面进行了分类，用户可以在选择对应的操作系统后，根据安装包右上角的芯片架构标签，找到符合自己的运行环境的文件，点击下载后即可快速安装和使用。

![下载方式优化](https://assets.emqx.com/images/1c0ad5590aef0499f6bf9bafb557ffc0.png)

### 文档结构优化

我们还对 MQTTX 文档进行了升级和结构调整，优化了之前大篇幅的单文档阅读模式，对文档结构进行了调整和分层。用户可以根据自己的使用需求，在文档页面内快速找到自己想要阅读和了解的内容。

![文档结构优化](https://assets.emqx.com/images/20c20a2505096b29628bd8df69b6767e.png)
