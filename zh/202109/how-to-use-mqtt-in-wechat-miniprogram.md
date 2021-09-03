微信小程序是腾讯于 2017 年 1 月 9 日推出的一种不需要下载安装即可在微信平台上使用的应用程序，用户扫一扫或者搜一下即可打开应用。也体现了“用完即走”的理念，用户不用关心是否安装太多应用的问题。应用将无处不在，随时可用，但又无需安装卸载。对于开发者而言，小程序开发门槛相对较低，难度不及 APP，能够满足简单的基础应用，对于用户来说，能够节约使用时间成本和手机内存空间，对于开发者来说也能节约开发和推广成本。

本文主要介绍如何在**微信小程序**项目中使用 [MQTT](https://www.emqx.com/zh/mqtt)，实现小程序客户端与 [MQTT 云服务](https://www.emqx.com/zh/cloud)的连接、订阅、收发消息、取消订阅等功能。

> MQTT 是一种基于发布/订阅模式的轻量级物联网消息传输协议，可以用极少的代码和带宽为联网设备提供实时可靠的消息服务，它广泛应用于物联网、移动互联网、智能硬件、车联网、电力能源等行业。



## 项目初始化

### 前期准备

注册微信小程序帐号，并下载[微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)。由于微信小程序安全要求比较高，在与后台服务器之间的通讯必须使用 https 或 wss 协议，因此要在微信小程序后台设置域名服务器。

微信小程序仅支持通过 WebSocket 进行即时通信，EMQ X 的 MQTT Over WebSocket 能够完全兼容使用在微信小程序上。但由于微信小程序的规范限制，EMQ X 使用微信小程序接入时需要注意以下几点：

- 使用已经通过[域名备案](https://baike.baidu.com/item/域名备案)的**域名**接入

- 域名需要[微信公众平台](https://mp.weixin.qq.com/)登录后在主页面的服务器域名下添加配置服务器域名地址
- 仅支持 WebSocket/TLS 协议，需要为域名分配受信任 CA 颁发的证书
- **由于微信小程序 BUG，安卓真机必须使用 TLS/443 端口，否则会连接失败（即连接地址不能带端口）**

添加服务器域名，这里我们将 `broker.emqx.io` 为例添加到服务器域名中，我们进入到页面中选择开始配置按钮，在 socket 合法域名列下输入 `wss://broker.emqx.io`，**注意**：必须以 wss 协议开头，如下图：

![微信小程序添加 MQTT 服务器域名](https://static.emqx.net/images/580dae268a35678e6d8fe14f90dabf45.png)

添加完成后，在微信小程序开发时才允许我们于该域名地址下的服务器进行通信与交互。

### 新建项目

准备完成前期网络通讯相关工作后，我们打开已经下载好了的微信开发者工具，打开后在页面点击新建一个小程序项目，如下图所示：

![新建小程序项目](https://static.emqx.net/images/70e3a461651c46a33f16c9624b32e9e6.png)

点击确认后，微信开发者工具就自动初始化好了项目，我们就可以开始开发了。

### 安装 MQTT 客户端库

因为小程序是通过 JavaScript 开发的，因此可以使用 MQTT.js 作为 [MQTT 客户端库](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)。

从小程序基础库版本 [2.2.1](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 或以上、及[开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 1.02.1808300 或以上开始，小程序支持使用 npm 安装第三方包。如感兴趣的读者可自行查看小程序 [npm 支持的](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html)官方文档来操作使用，本文为简化操作过程，将不使用 npm 的方式安装。我们将在 utils 文件夹下新建一个 mqtt.js 文件，我们直接获取在 MQTT.js CDN 上的打包构建后的源码复制 mqtt.js 文件中。

MQTT.js CDN 地址：[https://unpkg.com/mqtt@4.0.1/dist/mqtt.min.js](https://unpkg.com/mqtt@4.0.1/dist/mqtt.min.js) 可通过浏览器打开查看。

> **注意**：截止目前最新的 mqtt.js v4.2.8 版本，在小程序中使用会报 net.createConnection 未定义的错误，需要回退和使用 4.0.1 版本。

完成后我们，在 index.js 主页面中直接 import 即可：

```javascript
import mqtt from '../../utils/mqtt'
```



## MQTT 使用

本文将使用 EMQ X Cloud 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 作为本次测试的 MQTT 服务器地址，服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

更多详情请访问 [EMQ X Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQ X Cloud 文档](https://docs.emqx.cn/cloud/latest/)。

### 连接代码

微信小程序使用 WebSocket 的方式连接到 [MQTT 服务器](https://www.emqx.io/zh)，但连接的 URL 地址中请使用 `wxs` 协议名称，连接及初始化数据的关键代码：

```javascript
Page({
  data: {
    client: null,
    host: 'broker.emqx.io:8084',
    topic: 'testtopic/miniprogram',
    msg: 'Hello! I am from WeChat miniprogram',
    mqttOptions: {
      protocolVersion: 4, //MQTT连接协议版本
      clientId: 'emqx_cloud_miniprogram',
      clean: true,
      password: '',
      username: '',
      reconnectPeriod: 1000, // 1000毫秒，两次重新连接之间的间隔
      connectTimeout: 30 * 1000, // 1000毫秒，两次重新连接之间的间隔
      resubscribe: true // 如果连接断开并重新连接，则会再次自动订阅已订阅的主题（默认true）
    },
  },
  connect() {
    this.data.client = mqtt.connect(`wxs://${this.data.host}/mqtt`, this.data.mqttOptions)
    this.data.client.on('connect', () => {
      wx.showToast({
        title: '连接成功'
      })
    })
  },
})

```

### 订阅主题

```javascript
subscribe() {
  this.data.client.subscribe(this.data.topic)
  wx.showToast({
    title: '主题订阅成功'
  })
},
```

### 取消订阅

```javascript
unsubscribe() {
  this.data.client.unsubscribe(this.data.topic)
  wx.showToast({
    title: '取消订阅成功'
  })
},
```

### 消息发布

```javascript
publish() {
  this.data.client.publish(this.data.topic, this.data.msg)
},
```

### 断开连接

```javascript
disconnect() {
  this.data.client.end()
  wx.showToast({
    title: '断开连接成功'
  })
},
```



## 测试

我们在小程序中简单编写了如下应用界面，该应用具备：创建连接、订阅主题、收发消息、取消订阅、断开连接等功能。

完整的项目示例代码：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram)

<img src="https://static.emqx.net/images/8f0d503051f21fd9ba36ace426c8ff64.png" alt="小程序示例应用" style="zoom:50%;" />

使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 作为另一个客户端进行消息收发测试。

![MQTT 5.0 客户端工具 - MQTT X](https://static.emqx.net/images/435e50c6d4616269fb952fb47a559892.png)

可以看到 MQTT X 可以正常接收来到来自小程序发送过来的消息，同样，使用 MQTT X 向该主题发送一条消息时，也可以看到小程序能正常接收到该消息。

<img src="https://static.emqx.net/images/1158fb3ea9e5056ed66074771c45e8b6.png" alt="微信小程序接收 MQTT 消息" style="zoom:50%;" />

## 总结

综上所述，我们实现了在小程序项目中创建 MQTT 连接，模拟了小程序客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。
