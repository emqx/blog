在介绍和使用前，读者可以访问我们 [项目地址](https://github.com/emqx/MQTTX) 或 [官方网站](https://mqttx.app)，了解并获取到最新的版本信息，MQTT X 正在快速开发迭代阶段，使用最新版本有助于提高使用体验。



## 下载

请从 [GitHub Releases](https://github.com/emqx/MQTTX/releases) 下载符合您的版本并安装使用。

如果出现网络原因，导致从 GitHub 下载中出现网速较慢或卡顿的情况时，也可以 [前往 EMQ 官网](https://www.emqx.com/zh/downloads/MQTTX/) ，选择符合您的版本并安装使用。



## MQTT Broker 准备

- 如果您没有本地部署的 MQTT Broker，那么可以使用由 [EMQX Cloud](https://www.emqx.com/en/cloud) 提供的公共 MQTT 服务进行快速测试：

```
Broker 地址: broker.emqx.io
Broker TCP 端口: 1883
Broker SSL 端口: 8883
```

- 如果您打算本地部署 MQTT Broker，推荐您 [下载 EMQX](https://github.com/emqx/emqx/releases) 进行安装使用。EMQX 是一款完全开源，高可用低时延的百万级分布式物联网 MQTT 5.0 消息服务器。

  使用 Docker 快速安装 EMQX：

```shell
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx
```



## 连接配置

在准备好 MQTT Broker 后，进入到主程序页面，可点击左侧菜单栏中的 `+` 号，如果页面没有数据，还可以直接点击右侧的 `新建连接` 按钮，快速配置一个新的客户端连接。

![mqttxcreate.png](https://assets.emqx.com/images/a2e171f179fe4ccd93ea7514ee4d9364.png)

进入到创建页面后，需配置或填写连接客户端的相关信息，读者可以在此处配置定义 Broker 连接的所有设置，例如：`Broker Host`, `Broker Port`, `Client ID ` , `Username`, `Password`, `Clean Session` 等基础配置信息。

![2.png](https://assets.emqx.com/images/ad82e1d8dda141e3921e9b71d3967e44.png)

1. Broker 信息

   配置 `Broker` 信息时，`Client ID`、`Host` 和 `Port` 已经默认填写，您也可根据实际的 `Broker` 信息自行修改。点击 `Client ID` 右侧的刷新按钮，可快速生成新的 `Client ID`。

2. 用户认证信息

   如果您的 Broker 开启了用户认证，配置项中可填写 `Username` 和 `Password` 信息。

3. SSL/TLS

   当需要开启 `SSL/TLS` 认证时，只需要将配置中的 `SSL/TLS` 配置项设置为 `true`，并提供了 `CA signed self` 和 `Self signed` 两种方式。

   如果选择了 `Self signed`，可进行证书配置，点击最右侧的文件夹按钮，选择您已经生成好的各项证书，单向连接只需要选择您的 `CA File` 即可，对于双向认证，还需要选择配置 `Client Certificate File` 和 `Client key file`。

    ![3.png](https://assets.emqx.com/images/f29056efe253cbb3b3b986000615bde5.png)

4. 高级配置

   高级配置中，可以配置 `Connect Timeout`、 `KeepAlive`、`Clean Session`、`Auto Reconnect`、`MQTT Version` 等信息。

5. MQTT v5.0

   在高级配置中，可以选择 MQTT 的协议版本，支持 MQTT v3.1.1 和 MQTT v5.0 版本，默认为 v3.1.1，如果选择了 v5.0 版本后，还可配置 `Session Expiry Interval`、`Receive Maximum`（可选）。

6. 遗嘱消息

   在高级配置下方的配置卡片中，可以配置遗嘱消息，`Last-Will-QoS` 和 `Last-Will-Retain` 的值默认填充为 0 和 `False`，输入 `Last-Will-Topic` 和 `Last-Will-Payload` 的值便可完成对遗嘱消息的配置。



## 发布

连接创建成功后，即可进入到连接的主界面，点击顶部连接名称旁的折叠按钮，可以展开并显示该配置的几个基础信息，快速修改该连接的常用配置，修改时需断开连接，重新点击连接后即可生效。在断开连接的状态下，也可点击右边配置按钮，进行更多的连接配置修改。

连接建立后，可以在连接主页面的下方的输入框内，简单输入 `Topic` 和 `Payload` 后，点击右下角按钮，发送测试消息了。macOS 用户可以使用 `command + enter` 快捷键，其它用户可以使用 `control + enter` 快捷键来快速发送消息。

![fabu.png](https://assets.emqx.com/images/3932f09038e85220800acc665df1dac8.png)



## 订阅

点击左下角的 `New Subscription` 按钮，可以快速订阅一个 Topic，Topic 订阅成功后将立即开始接受消息。

每个 `Topic` 都会随机分配一个色彩标记，你也可以打开颜色选择器自定义标记的颜色。点击页面订阅列表顶部的最右侧的按钮，可以隐藏订阅列表以显示更多的空间。

鼠标悬浮到 `Topic` 列表的卡片上时，点击右上角红色按钮，可以快速取消订阅。

我们再新建一个测试连接用于消息发布测试。在页面右下角填入刚才所订阅的 `Topic` 信息，输入 Payload 的内容后，点击最右侧的发送按钮，就向订阅了该 `Topic` 的连接客户端发送了一条消息。

![一条消息1.png](https://assets.emqx.com/images/4d0d28d4e20bee6e0fc6e9c5c941862c.png)

![一条消息2.png](https://assets.emqx.com/images/8b07a1550c349621fb2ae5676b5fda1c.png)

如果发送消息的连接客户端也订阅了相同的 `topic` ，发送成功后该客户端也将即时接收到刚才所发送的消息。注意，在消息框内，右边栏为发送的消息。左边栏为接收到的消息。



## 其它

1. 设置

   点击左侧菜单栏底部的设置按钮，或使用快捷键，macOS 用户可以使用 `command + ,` 快捷键，其它用户可以使用 `control + ,` 快捷键来跳转到设置页面。目前支持设置语言，是否自动检查更新和选择主题。

2. 消息页面的下拉菜单

![xlcd.png](https://assets.emqx.com/images/37076c58c377111a1c59e0cfa88a97f2.png)

   在消息栏右上角的 `All`，`Received`， `Published` 按钮可以过滤出 全部消息，已接收的消息，和已发布的消息。

   点击顶部的操作栏按钮，选择 `Search by Topic` 项，或使用快捷键，macOS 用户可以使用 `command + f` 快捷键，其它用户可以使用 `control + f` 快捷键，打开按 `Topic` 搜索过滤消息的的功能。

   选择 `Clear Histroy` 项，可以快速清空当前连接中所有发送和接收的消息。

   选择 `Disconnect` 和 `Delete Connection` 项，可以快速断开连接，删除当前连接。

3. 检查更新

   点击左侧底部的 `i` 按钮，可进入到 `About` 页面，了解 **MQTT X** 的版本信息和 [EMQX](https://www.emqx.com/en) 的相关信息。点击 `Check for Updates` 可以检查是否有更新版本。

![mqttxupdate.png](https://assets.emqx.com/images/de17680e289b43e3c555a1a40315ec1c.png)


以上为 MQTT X 使用方法的简单概述。读者可以通过在 GitHub 上的 [使用手册](https://github.com/emqx/MQTTX/blob/main/docs/manual.md) 来完整的使用 MQTT X。

本项目基于 Apache 2.0 开源协议，使用过程中，有任何问题都可以到 [GitHub issues](https://github.com/emqx/MQTTX/issues) 来发表问题，讨论观点或是向我们提交 PR，我们会认真查阅并回复所有问题。
