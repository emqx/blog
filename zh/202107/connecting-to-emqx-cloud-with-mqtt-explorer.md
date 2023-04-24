本文将以 [MQTT Explorer](https://mqtt-explorer.com/) 作为 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)测试工具，接入 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)。通过本文，你将能快速了解 MQTT Explorer 的基础用法以及 MQTT 协议的基本概念与使用。



## MQTT Explorer 简介

[MQTT Explorer](https://mqtt-explorer.com/) 是目前较为活跃的 MQTT 客户端桌面应用，一直受到开发者们的喜爱。主要技术是 [Electron](https://github.com/electron/electron)，由 [@thomasnordquist](https://github.com/thomasnordquist) 开发并且开源，遵循 [Creative Commons Public Licenses](https://wiki.creativecommons.org/wiki/Considerations_for_licensors_and_licensees#Considerations_for_licensees) 协议，GitHub 地址为 https://github.com/thomasnordquist/MQTT-Explorer

其包含主要特性有：

- 基本订阅/推送/连接功能
- 用户认证功能
- WebSocket 支持
- 支持 diff 查看和多种类型的 Payload
- 基本的历史信息日志
- 支持 TLS 连接
- 支持黑夜模式

尤其是一些较好的特性有：

- 自动订阅$SYS主题，方便查看 broker 状态信息
- 按照树形结构组织订阅列表，方便用户查看其归属关系
- 有消息可视化功能，直观、可交互的统计图表设计

MQTT Explorer 能够满足大部分开发的需求，但是也有一些缺点：

- 一次只能一个连接存在，不方便多连接调试
- UI 设计上 Publish payload 和 Subscribe Message list 没有分开，并不能很方便地查看收发信息的情况
- 没有完整的操作日志记录，不方便开发者排查与服务器交互的信息



## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为**全球首个全托管的** [**MQTT 5.0**](https://www.emqx.com/zh/mqtt/mqtt5) **公有云服务**，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

本文将使用 EMQX Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker-cn.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQX Cloud 文档](https://docs.emqx.com/zh/cloud/latest/)。 



## MQTT Explorer 使用

### 功能预览

其主页面如下图所示，最上方为主题搜索栏及连接配置。其下左侧是主题的树形结构，右侧是含有 Publish 发布栏、Subscribe 订阅栏、Payload 栏、History 信息控制栏。

![功能预览](https://assets.emqx.com/images/d9bd68b20a3b01843980d8c074a4ca87.png)

### MQTT 连接/订阅

#### 初始化页面

第一次进入 MQTT Explorer 时会弹出配置页面。

![配置页面](https://assets.emqx.com/images/a66c05e560827978c1831596f3391495.png)

#### 创建连接

点击 Connectons 创建新的连接，并填入 Host 为 broker-cn.emqx.io， 端口为 1883，协议为 mqtt 协议。

![创建连接](https://assets.emqx.com/images/94be5666e1715ce0c4ee99134607ba72.png)

#### 订阅主题

之后点击 Advanced。因为 EMQX Cloud 默认禁止了 `$SYS` 主题和 `#` 主题，因此我们将其删去，输入一个测试的订阅主题，我们命名为 `test/1`，结果如下图所示。

![订阅主题](https://assets.emqx.com/images/131357ea19381cf2e9096bdfec8dc656.png)

#### 连接

最后，点击 Back 回到连接配置页面，并点击连接，即可完成 EMQX Cloud 的连接以及主题 `test/1` 的订阅。

连接成功后，将可以看到订阅的树形结构有 `test` 和 `1` 的节点，并且右侧上方状态栏显示已经连接，右侧含有主题 `test/1` 的标题。

![连接](https://assets.emqx.com/images/eadc02d6bb78b25c95f691deb43e4c1c.png)

### MQTT 消息发布

完成连接的建立之后，在页面右下角主题框中输入 `/test/1`，并且输入一些文字，之后点击 Publish 发送消息。

![消息发布](https://assets.emqx.com/images/ff1b9faf9ec30e8510243710449eae38.png)

### 接收订阅消息

发布成功后，右上方的 Value 卡片内将会接收到刚刚发布的消息。

![接收订阅消息](https://assets.emqx.com/images/5f16e17d6deb55e016497abae5a33b3e.png)

### 接收历史记录 

在页面右下角的 History 卡片内，你将能看到相关订阅主题接收到的消息记录。

![接收历史记录](https://assets.emqx.com/images/f3f2581c6cba7f370ec7fd712bb51487.png)

### 统计信息

页面右下角 Stats 将会显示统计信息。

![统计信息](https://assets.emqx.com/images/30eed43a6c0bf4e2e3c3ce5df9bc01ae.png)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
