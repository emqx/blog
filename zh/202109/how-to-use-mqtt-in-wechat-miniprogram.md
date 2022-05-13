微信小程序是腾讯于 2017 年 1 月 9 日推出的一种不需要下载安装即可在微信平台上使用的应用程序，用户扫一扫或者搜一下即可打开应用。也体现了“用完即走”的理念，用户不用关心是否安装太多应用的问题。应用将无处不在，随时可用，但又无需安装卸载。对于开发者而言，小程序开发门槛相对较低，难度不及 APP，能够满足简单的基础应用，对于用户来说，能够节约使用时间成本和手机内存空间，对于开发者来说也能节约开发和推广成本。

本文主要介绍在微信小程序中使用 `MQTT.js` 连接到 [EMQX Cloud](https://www.emqx.com/zh/cloud) 部署，进行订阅、取消订阅、收发消息等功能。

## 前提条件

1. [注册](https://mp.weixin.qq.com/wxopen/waregister?action=step1) 微信小程序账号，并下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 由于微信小程序安全要求比较高，在与后台服务器之间的通讯必须使用 https 或 wss 协议。所以需要登录 [微信公众平台](https://mp.weixin.qq.com/)，在左侧菜单【开发】->【开发管理】->【开发设置】->【服务器域名】中 socket 合法域名添加部署域名。

   - EMQX Cloud 专业版部署默认连接地址是 IP，需要用户自行进行域名绑定，且进行 TLS/SSL 配置（**证书链必填**，否则真机调试会失败）。当 TLS/SSL 的状态为 `运行中` 时，刷新页面，即可在部署概览页面看到连接端口中多了一个 8084 (wss)，请记住这个端口号，后续编写连接代码时，我们需要用到它。
   - 微信小程序仅支持通过 WebSocket 进行即时通信，EMQX Cloud 部署的 MQTT Over WebSocket 能够完全兼容使用在微信小程序上。因此在进行 MQTT 连接时，只能使用 wss 协议（**但是客户端连接代码中需要写成 wxs**）
   - 更多域名相关配置说明，请参阅微信官方文档：<https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html>

   ![设置小程序 socket 域名](https://assets.emqx.com/images/wechat-host.png)

2. 打开已经下载好了的微信开发者工具，在页面点击新建一个小程序项目，如下图所示：

   ![创建微信小程序项目](https://assets.emqx.com/images/wechat-create-program.png)

## 安装依赖

推荐使用 MQTT.js `v4.2.1` <https://unpkg.com/mqtt@4.2.1/dist/mqtt.min.js>（针对原生的微信小程序），**若调试器可以连接但真机调试仍有问题，建议尝试切换 MQTT.js 版本**。

> 原生微信小程序 MQTT.js 可用版本有 `v4.2.1`、`v4.2.0`、`v4.1.0` 和 `v2.18.8`
>
> 使用 uniapp 框架搭建微信小程序 MQTT.js 可用版本有 `v4.1.0` 和 `v2.18.8`

在项目根目录下新建 utils 文件夹，将下载好的对应版本的 mqtt.min.js 文件放入该文件夹中，在 index.js 中通过如下方式引入 mqtt

```javascript
import mqtt from "../../utils/mqtt.min.js";
```

## 连接关键代码

### 建立连接

> 1. 只能使用 wss 协议，但是微信小程序中需要写为 wxs
> 2. 端口为 8084（EMQX Cloud 专业版部署），但实际的端口号以 EMQX Cloud 控制台对应部署的概览页面信息为准。
> 3. 连接地址末尾不要忘了带上路径 /mqtt
> 4. EMQX Cloud 部署需要先在部署详情页面的【认证鉴权】->【认证】中添加用户名密码，然后写入 `mqttOptions` 中

```javascript
Page({
  data: {
    client: null,
    conenctBtnText: "连接",
    host: "wx.emqxcloud.cn",
    subTopic: "testtopic/miniprogram",
    pubTopic: "testtopic/miniprogram",
    pubMsg: "Hello! I am from WeChat miniprogram",
    receivedMsg: "",
    mqttOptions: {
      username: "test",
      password: "test",
      reconnectPeriod: 1000, // 1000毫秒，设置为 0 禁用自动重连，两次重新连接之间的间隔时间
      connectTimeout: 30 * 1000, // 30秒，连接超时时间
      // 更多参数请参阅 MQTT.js 官网文档：https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options
      // 更多 EMQ 相关 MQTT 使用教程可在 EMQ 官方博客中进行搜索：https://www.emqx.com/zh/blog
    },
  },

  setValue(key, value) {
    this.setData({
      [key]: value,
    });
  },

  connect() {
    // MQTT-WebSocket 统一使用 /path 作为连接路径，连接时需指明，但在 EMQX Cloud 部署上使用的路径为 /mqtt
    // 因此不要忘了带上这个 /mqtt !!!
    // 微信小程序中需要将 wss 协议写为 wxs，且由于微信小程序出于安全限制，不支持 ws 协议
    try {
      this.setValue("conenctBtnText", "连接中...");
      const clientId = new Date().getTime();
      this.data.client = mqtt.connect(`wxs://${this.data.host}:8084/mqtt`, {
        ...this.data.mqttOptions,
        clientId,
      });

      this.data.client.on("connect", () => {
        wx.showToast({
          title: "连接成功",
        });
        this.setValue("conenctBtnText", "连接成功");

        this.data.client.on("message", (topic, payload) => {
          wx.showModal({
            content: `收到消息 - Topic: ${topic}，Payload: ${payload}`,
            showCancel: false,
          });
          const currMsg = this.data.receivedMsg ? `<br/>${payload}` : payload;
          this.setValue("receivedMsg", this.data.receivedMsg.concat(currMsg));
        });

        this.data.client.on("error", (error) => {
          this.setValue("conenctBtnText", "连接");
          console.log("onError", error);
        });

        this.data.client.on("reconnect", () => {
          this.setValue("conenctBtnText", "连接");
          console.log("reconnecting...");
        });

        this.data.client.on("offline", () => {
          this.setValue("conenctBtnText", "连接");
          console.log("onOffline");
        });
        // 更多 MQTT.js 相关 API 请参阅 https://github.com/mqttjs/MQTT.js#api
      });
    } catch (error) {
      this.setValue("conenctBtnText", "连接");
      console.log("mqtt.connect error", error);
    }
  },
});
```

### 订阅主题

```javascript
subscribe() {
  if (this.data.client) {
    this.data.client.subscribe(this.data.subTopic)
    wx.showModal({
      content: `成功订阅主题：${this.data.subTopic}`,
      showCancel: false,
    })
    return
  }
  wx.showToast({
    title: '请先点击连接',
    icon: 'error',
  })
},
```

### 取消订阅

```javascript
unsubscribe() {
  if (this.data.client) {
    this.data.client.unsubscribe(this.data.subTopic)
    wx.showModal({
      content: `成功取消订阅主题：${this.data.subTopic}`,
      showCancel: false,
    })
    return
  }
  wx.showToast({
    title: '请先点击连接',
    icon: 'error',
  })
},
```

### 发布消息

```javascript
publish() {
  if (this.data.client) {
    this.data.client.publish(this.data.pubTopic, this.data.pubMsg)
    return
  }
  wx.showToast({
    title: '请先点击连接',
    icon: 'error',
  })
},
```

### 断开连接

```javascript
disconnect() {
  this.data.client.end()
  this.data.client = null
  this.setValue('conenctBtnText', '连接')
  wx.showToast({
    title: '成功断开连接'
  })
},
```

项目完整代码请见：<https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram>。

## 测试验证

我们在小程序中简单编写了如下应用界面，该应用具备：创建连接、订阅主题、收发消息、取消订阅、断开连接等功能。

<img src="https://assets.emqx.com/images/wechat-overview.png"
alt="小程序概览页面" style="zoom:50%;" />

小程序进行连接并订阅主题 testtopic/miniprogram 之后，使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 作为另一个客户端订阅主题 testtopic/# 并发送一条消息到主题 testtopic/miniprogram

![使用 MQTT X 发送消息](https://assets.emqx.com/images/wechat-mqttx.png)

可以看到 MQTT X 可以正常接收来到来自小程序发送过来的消息，同样，使用 MQTT X 向该主题发送一条消息时，也可以看到小程序能正常接收到该消息。

<img src="https://assets.emqx.com/images/wechat-receive-msg.png"
alt="小程序接收消息" style="zoom:50%;" />

## 更多内容

综上所述，我们实现了在微信小程序项目中创建 MQTT 连接，模拟了客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。可以在 [这里](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram) 下载到示例的源码，同时也可以在 [GitHub](https://github.com/emqx/MQTT-Client-Examples) 上找到更多其他语言的 Demo 示例。

本示例只是进行了一个简单的 MQTT 连接演示，更多复杂功能还需开发者深入了解 MQTT 协议，然后进行探索研究实践。

- MQTT 官方示例可参见 <https://github.com/mqttjs/MQTT.js/tree/main/examples>
- EMQ 官方 MQTT.js 入门教程 <https://www.emqx.com/zh/blog/mqtt-js-tutorial>
- 使用 WebSocket 连接 MQTT 服务器 <https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket>
- MQTT 协议 Keep Alive 详解 <https://www.emqx.com/zh/blog/mqtt-keep-alive>
