[Vue](https://cn.vuejs.org) 是一款由尤雨溪及其团队开发的渐进式 Javascript 前端框架。该框架具备数据双向绑定、组件化、响应式和轻量等特点，搭配其脚手架 Vue CLI 使得开发者更加容易上手，大大减少了学习成本。同时其配备一个专用的状态管理模式 Vuex ，在这里可以集中管理所有组件的状态。

[MQTT](https://www.emqx.com/zh/mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议**。该协议提供了一对多的消息分发和应用程序的解耦，具备很小的传输消耗和协议数据交换、最大限度减少网络流量和三种不同消息服务质量等级，满足不同投递需求的优势。

本文主要介绍如何在 Vue 项目中使用 MQTT，实现客户端与 MQTT 服务器的连接、订阅、收发消息、取消订阅等功能。



## 项目初始化

### 新建项目

参考链接如下：  

- [使用 Vue CLI 创建 Vue 项目](https://cli.vuejs.org/zh/guide/creating-a-project.html#vue-create) 
- [通过引用 Vue.js 创建 Vue 项目](https://cn.vuejs.org/v2/guide/installation.html)

示例：

```shell
vue create vue-mqtt-test
```

### 安装 MQTT 客户端库
> 以下 2，3 方法更适用于通过直接引用 Vue.js 创建的 Vue 项目。

1. 通过命令行安装，可以使用 npm 或 yarn 命令（二者选一）
	
	```
  	npm install mqtt --save
  	```

  	```
  	yarn add mqtt
  	```

2. 通过 CDN 引入

   ```html
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
   ```

3. 下载到本地，然后使用相对路径引入

   ```html
   <script src="/your/path/to/mqtt.min.js"></script>
   ```


## MQTT 的使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

连接关键代码：

```vue
<script>
import mqtt from 'mqtt'

export default {
  data() {
    return {
      connection: {
        host: 'broker.emqx.io',
        port: 8083,
        endpoint: '/mqtt',
        clean: true, // 保留会话
        connectTimeout: 4000, // 超时时间
        reconnectPeriod: 4000, // 重连时间间隔
        // 认证信息
        clientId: 'mqttjs_3be2c321',
        username: 'emqx_test',
        password: 'emqx_test',
      },
      subscription: {
        topic: 'topic/mqttx',
        qos: 0,
      },
      publish: {
        topic: 'topic/browser',
        qos: 0,
        payload: '{ "msg": "Hello, I am browser." }',
      },
      receiveNews: '',
      qosList: [
        { label: 0, value: 0 },
        { label: 1, value: 1 },
        { label: 2, value: 2 },
      ],
      client: {
        connected: false,
      },
      subscribeSuccess: false,
    }
  },

  methods: {
    // 创建连接
    createConnection() {
      // 连接字符串, 通过协议指定使用的连接方式
      // ws 未加密 WebSocket 连接
      // wss 加密 WebSocket 连接
      // mqtt 未加密 TCP 连接
      // mqtts 加密 TCP 连接
      // wxs 微信小程序连接
      // alis 支付宝小程序连接
      const { host, port, endpoint, ...options } = this.connection
      const connectUrl = `ws://${host}:${port}${endpoint}`
      try {
        this.client = mqtt.connect(connectUrl, options)
      } catch (error) {
        console.log('mqtt.connect error', error)
      }
      this.client.on('connect', () => {
        console.log('Connection succeeded!')
      })
      this.client.on('error', error => {
        console.log('Connection failed', error)ß
      })
      this.client.on('message', (topic, message) => {
        this.receiveNews = this.receiveNews.concat(message)
        console.log(`Received message ${message} from topic ${topic}`)
      })
    },
  }
}
</script>
```

### 订阅主题

```js
doSubscribe() {
  const { topic, qos } = this.subscription
  this.client.subscribe(topic, { qos }, (error, res) => {
    if (error) {
      console.log('Subscribe to topics error', error)
      return
    }
    this.subscribeSuccess = true
    console.log('Subscribe to topics res', res)
 	})
},
```

### 取消订阅

```js
doUnSubscribe() {
  const { topic } = this.subscription
  this.client.unsubscribe(topic, error => {
    if (error) {
      console.log('Unsubscribe error', error)
    }
  })
}
```

### 消息发布

```js
doPublish() {
  const { topic, qos, payload } = this.publication
  this.client.publish(topic, payload, qos, error => {
    if (error) {
      console.log('Publish error', error)
    }
  })
}
```

### 断开连接

```js
destroyConnection() {
  if (this.client.connected) {
    try {
      this.client.end()
      this.client = {
        connected: false,
      }
      console.log('Successfully disconnected!')
    } catch (error) {
      console.log('Disconnect failed', error.toString())
    }
  }
}
```



## 测试

我们使用 Vue 编写了如下简单的浏览器应用，该应用具备：创建连接、订阅主题、收发消息、取消订阅、断开连接等功能。

项目完整代码请见：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js)。

![vueui.png](https://assets.emqx.com/images/b6563b0eb66eb51a2a02776889016a18.png)



使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh)  作为另一个客户端进行消息收发测试。

![vuemqttx.png](https://assets.emqx.com/images/2013cbab1bdffcae69b817bfebb4a33f.png)

在 MQTT X 发送第二条消息之前，在浏览器端进行取消订阅操作，浏览器端将不会收到 MQTT X 发送的后续消息。



## 总结

综上所述，我们实现了在 Vue 项目中创建 MQTT 连接，模拟了客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。

Vue 作为三大主流的前端框架之一，既能够在浏览器端使用，也能够在移动端使用，结合 MQTT 协议及 [MQTT  物联网云服务](https://www.emqx.com/zh/cloud) 可以开发出很多有趣的应用，比如客服聊天系统或实时监控物联网设备信息的管理系统。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
