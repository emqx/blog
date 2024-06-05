由 EMQ 开源的 MQTTX 是一款 MQTT 5.0 跨平台桌面客户端。MQTTX 为连接测试各类 MQTT 消息服务器而生，支持快速创建多个同时在线的 MQTT 客户端连接，采用一键式的连接方式和简洁的图形界面，帮助使用者便捷地测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能，探索更多 [MQTT 协议特性](https://www.emqx.com/zh/mqtt-guide)。

在近期发布的 v1.8.0 中，除了通过新增的快速复制连接功能优化使用体验之外，还扩展了两个新的使用场景，即增加了 CLI（命令行） 和 Web 端（浏览器网页）这两种新的交互方式 。这使得 MQTTX 1.8.0 成为支持使用场景最完整的 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)。用户可以根据使用需求，自行选择下载桌面客户端、使用终端命令行或是在桌面浏览器上快速完成对 MQTT 的连接测试。

## MQTTX Web 介绍

对于一些初次体验 MQTT 协议的新用户来说，快速理解并上手使用 MQTT 协议是首要需求。[MQTTX Web](https://mqttx.app/zh/web) 则为其提供了一种更为便捷的方式：**无需繁杂的下载安装步骤，只需在浏览器内打开页面，即可快速连接和测试 MQTT 服务与应用**，了解和探索 MQTT 协议。

MQTTX Web 是一款在线 MQTT 5.0 客户端工具，即运行在浏览器上的 MQTT 5.0 WebSocket 客户端工具。其具有以下功能特性：

- 支持通过普通或者加密的 WebSocket 端口连接至 MQTT 服务；
- 连接的新建、编辑、删除以及缓存连接，方便下次访问使用；
- 不同连接的订阅列表管理；
- 消息发布、接收、以及接收到新消息时提示，同时也支持按照消息类型过滤消息列表。

> MQTTX Web 网站：[https://mqttx.app/zh/web](https://mqttx.app/zh/web) 
>
> MQTTX Web 在线使用地址：[http://mqtt-client.emqx.com/](http://mqtt-client.emqx.com/) 
>
> MQTTX Web GitHub 仓库：[https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web) 

![MQTTX Web](https://assets.emqx.com/images/6514d8f357b84bf708589f13b2dc0d1f.png)

### MQTT over WebSocket

近年来随着 Web 前端的快速发展，浏览器新特性层出不穷，越来越多的应用可以在浏览器端通过浏览器渲染引擎实现，Web 应用的即时通信方式 WebSocket 也因此得到了广泛的应用。

MQTTX Web 核心就是使用 WebSocket 连接到 MQTT 服务，因此从功能性来说，MQTTX Web 不仅使用方便，还能提供 MQTT over WebSocket 的连接测试功能。当您需要在 Web 应用场景中使用 MQTT 时，就可以通过 WebSocket 来连接和使用，使用 MQTTX Web 来调试您的 MQTT 服务与应用，加快您的应用生产并提高稳定性。

### 基于现代浏览器

MQTTX Web 基于现代浏览器技术开发，将应用部署到网页上。用户无需下载和安装 MQTTX 软件包，打开浏览器即可使用。同时还可将新建的连接和消息信息等持久化存储到浏览器内，方便下次访问使用。

### 开放源码

MQTTX Web 代码与 [MQTTX 桌面应用](https://github.com/emqx/MQTTX)和 [MQTTX CLI ](https://github.com/emqx/MQTTX/tree/main/cli)保持一致，基于 Apache License 2.0 协议开放源码，高级用户可以直接到代码仓库内修改和使用 MQTTX Web，并将其部署到任意您的使用环境中。

## 使用 MQTTX Web 开发和调试 MQTT 服务与应用

MQTTX Web 同样使用了图形化页面，采用聊天界面形式来帮助您快速测试 MQTT 服务，使用方式与 MQTTX 桌面应用基本一致。

打开浏览器后输入 [http://mqtt-client.emqx.com/](http://mqtt-client.emqx.com/) 就可以访问到 MQTTX Web。

> 更多详细的使用介绍可以参考 MQTTX 的使用文档：[https://mqttx.app/zh/docs/get-started](https://mqttx.app/zh/docs/get-started)。

为测试 MQTTX Web 的使用，我们需要准备一个 MQTT 服务，本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 物联网云平台 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建，服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- WebSocket Port: **8083**

### 创建连接

点击页面中的的 **New Connection** 按钮，在页面里输入连接信息，点击右上角即可快速创建并连接到 MQTT 服务。

![MQTTX Web 创建连接](https://assets.emqx.com/images/14e2b3c420562d0075007ca874400fe1.png)

### 订阅管理

创建并成功连接后，点击订阅列表中的 **New Subscription** 按钮弹出订阅列表框，在该页面可进行新建/取消订阅操作。

![MQTTX Web 订阅](https://assets.emqx.com/images/6994bd38ecef44968de3ce49d38f9508.png)

### 消息发布/接收

点击页面右侧底部的输入框，可弹出消息发布框，填写好 **Topic** 及 **Payload** 字段后点击右下角的发布图标可发布消息，发布成功后的消息将会显示在消息列表的右侧。

![MQTTX Web 消息收发](https://assets.emqx.com/images/ee91effb4314a56906e888519c256c96.png)

订阅主题所收到的消息将会显示在消息列表的左侧，可点击右上角的消息类型切换按钮只显示已接收或是已发送的消息。

最后，我们再通过使用 MQTTX 的桌面客户端来和 MQTTX Web 连接到同一个 MQTT 服务，以测试和验证 MQTTX Web 的功能。首先使用 MQTTX Web 发布一条消息，通过 MQTTX 桌面客户端来接收，再反向使用 MQTTX 桌面客户端发送一条消息到 MQTTX Web。此时，我们可以看到两边都收到了各自收发的消息。

![MQTTX Web 消息收发](https://assets.emqx.com/images/57c69f0233d017a8cb2e82194f94116c.png)

至此，我们就完成了使用 MQTTX Web 对 MQTT 消息发布订阅功能的测试和验证。在接下来的 1.8.1 版本中，我们还将继续优化页面样式，完善测试功能，支持更多的 MQTT 5.0 属性设置等。

## 结语

MQTTX Web 的发布，为物联网开发者进行 MQTT 连接测试提供了一种新的选择。而对命令行调用、桌面客户端下载和在线浏览器这几种交互形式的完整支持，使得 MQTTX 1.8.0 可帮助不同使用场景需求的用户完成对 MQTT 服务或应用的开发与调试，从而提高用户自身相关业务能力与稳定性。简单易用的测试客户端工具 MQTTX 结合高效可靠的[物联网消息服务器 EMQX](https://www.emqx.com/zh/products/emqx)，将帮助物联网开发者构建具有竞争力的物联网平台与应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
