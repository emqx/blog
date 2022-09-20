微信小程序是腾讯推出的一种不需要下载安装即可在微信平台上使用的应用程序。用户扫一扫或者搜一下即可开始使用应用，能够节约大量手机内存和时间成本。

随着微信生态的不断发展，相较于 APP 开发，小程序有着开发难度低、使用便捷、自带微信庞大用户量的优势，因而得到了开发者越来越多的青睐。

微信作为一款 IM 工具，收发消息是最为常用的功能。在物联网业务场景中，若能通过微信小程序与设备端连接，接收、发送消息或是及时收到设备状态异常告警，将会大大提高远程智能操纵的可行性。

本文将以 [MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)测试场景为例，使用 MQTT.js 连接到 MQTT 服务——[EMQX Cloud ](https://www.emqx.com/zh/cloud)部署，在微信小程序中实现一个简单方便的 MQTT 连接测试工具。

> EMQX Cloud 是全托管的云原生 MQTT 消息服务，以自动化、全托管的形式为用户提供可靠、实时的海量物联网设备连接、事件消息处理、IoT 数据桥接等能力，免除基础设施管理维护负担，加速物联网应用开发。
>
> 免费试用：[https://www.emqx.com/zh/cloud](https://www.emqx.com/zh/cloud)


## 项目初始化

### 微信小程序侧相关准备

#### 证书及域名

1. 证书

   由于微信小程序安全要求比较高，在与后台服务器之间的通讯必须使用 https/wss 协议。因此我们需要购买一份证书并进行 TLS/SSL 证书配置。登录前往 [EMQX Cloud 控制台](https://cloud.emqx.com/console/)，进入相应部署的概览页面进行 TLS/SSL 配置。单/双向认证均可，注意**证书链必填**，否则后续真机调试会失败。本文选择的是单向认证。

   - 微信官方文档：[https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html](https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html)
   - EMQX Cloud TLS/SSL 配置帮助文档及证书限制说明：[https://docs.emqx.com/zh/cloud/latest/deployments/tls_ssl.html](https://docs.emqx.com/zh/cloud/latest/deployments/tls_ssl.html)
   - 若选择双向认证，小程序客户端连接代码需携带服务端 CA、客户端证书及客户端私钥，请参考 [https://github.com/mqttjs/MQTT.js/blob/main/examples/tls%20client/mqttclient.js](https://github.com/mqttjs/MQTT.js/blob/main/examples/tls client/mqttclient.js)

      ![小程序双向认证](https://assets.emqx.com/images/0fbe50b26b8abc8ff6d577ef8ca586fd.png)

2. 绑定域名

   EMQX Cloud 专业版部署默认连接地址是 IP，由于小程序只可以跟指定的域名进行网络通信，所以需要 EMQX Cloud 用户将自己经过 [ICP 备案](https://kf.qq.com/faq/180123AZnmEZ180123zIFR3Q.html) 的域名和部署 IP 相绑定，并且前往 [微信公众平台](https://mp.weixin.qq.com/) ->【开发】->【开发管理】->【开发设置】->【服务器域名】中**添加 socket 合法域名**。

   ![小程序绑定域名](https://assets.emqx.com/images/c32606c2715e3d029983ec8620fc97f5.png)


#### 创建项目

[注册](https://mp.weixin.qq.com/wxopen/waregister?action=step1&token=&lang=zh_CN) 微信小程序账号，并下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)。打开微信开发者工具，点击新建一个小程序项目。

![创建小程序](https://assets.emqx.com/images/1eb1c708706f42ce34b10e5fb040b5e5.png)

### MQTT 库安装

推荐使用 [MQTT.js v4.2.1](https://unpkg.com/mqtt@4.2.1/dist/mqtt.min.js)（针对原生的微信小程序），**若调试器可以连接但真机调试仍有问题，建议尝试切换 MQTT.js 版本**。

> 原生微信小程序 MQTT.js 可用版本有 v4.2.1、v4.2.0、v4.1.0 和 v2.18.8
>
> 使用 uniapp 框架搭建微信小程序 MQTT.js 可用版本有 v4.1.0 和 v2.18.8

在项目根目录下新建 utils 文件夹，将下载好的对应版本的 mqtt.min.js 文件放入该文件夹中，在 index.js 中通过如下方式引入 mqtt

```
import mqtt from "../../utils/mqtt.min.js";
```

## MQTT 连接测试工具关键代码

### 建立连接

> 只能使用 wss 协议，但是微信小程序中需要写为 wxs
>
> 端口为 8084（EMQX Cloud 专业版部署），但实际的端口号以 EMQX Cloud 控制台对应部署的概览页面信息为准
>
> 连接地址末尾不要忘了带上路径 /mqtt
>
> EMQX Cloud 部署需要先在部署详情页面的【认证鉴权】->【认证】中添加用户名密码，然后写入 mqttOptions 中

```
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

```
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

```
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

```
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

```
disconnect() {
  this.data.client.end()
  this.data.client = null
  this.setValue('conenctBtnText', '连接')
  wx.showToast({
    title: '成功断开连接'
  })
},
```

项目完整代码请参阅：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-wechat-miniprogram)

## 真机测试验证

本文使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 作为测试的客户端和小程序互相收发消息。

小程序建立连接，并订阅主题 `testtopic/miniprogram`，然后向该主题发送一条消息。与此同时使用 MQTT X 连接相同的地址，订阅主题 `testtopic/#` 。

![MQTT 客户端](https://assets.emqx.com/images/a6bb1493019db39d2e1bded09dadaac8.png)

可以看到 MQTT X 可以正常接收来自小程序发送过来的消息。同样，使用 MQTT X 向主题 `testtopic/miniprogram` 发送一条消息时，也可以看到小程序能正常接收到该消息。

![微信小程序 MQTT](https://assets.emqx.com/images/321f341661bb4c411040b67637ead096.png)


## 结语

通过本文，我们介绍了如何在微信小程序中使用 MQTT.js 实现 MQTT 协议的连接、订阅、取消订阅、收发消息和断开连接这些功能，成功搭建了一个简单的 MQTT 连接测试工具。除了将连接地址暴露出来方便进行修改，其他相关连接参数选项，也可以设置为表单的形式进行配置，会更加灵活高效。在实际生产环境中，可以在此示例的基础上进行优化，实现支持多个连接同时在线，扩展可配置选项参数。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>



相关文档推荐：

- [MQTT 示例](https://github.com/mqttjs/MQTT.js/tree/main/examples)
- [MQTT.js 入门教程](https://www.emqx.com/zh/blog/mqtt-js-tutorial)
- [使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)
- [MQTT 协议 Keep Alive 详解](https://www.emqx.com/zh/blog/mqtt-keep-alive)
