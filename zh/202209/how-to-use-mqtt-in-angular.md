## 前言

[Angular](https://angular.io) 是一个基于 TypeScript 构建的开发平台。它包括一个基于组件的框架，用于构建可伸缩的 Web 应用；一组完美集成的库，涵盖路由、表单管理、客户端-服务器通信等各种功能；一套开发工具，可帮助用户开发、构建、测试和更新代码。

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种基于发布/订阅模式的**轻量级物联网消息传输协议**。该协议提供了一对多的消息分发和应用程序的解耦，传输消耗小，可最大限度减少网络流量，同时具有三种不同消息服务质量等级，满足不同投递需求的优势。

本文将介绍如何在 Angular 项目中使用 MQTT 协议，实现客户端与 MQTT 服务器的连接、订阅、收发消息、取消订阅等功能。

## 项目初始化

### 新建项目

参考链接如下：[使用 Angular CLI 创建 Angular 项目](https://angular.cn/guide/setup-local#install-the-angular-cli)

示例：

```
ng new my-app
```

### 安装 MQTT 客户端库

本次使用的是库为 [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/)，这个库不仅仅是 MQTT.js 的包装器，用于 angular >= 2。它使用 observables 并负责订阅处理和消息路由， [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/) 非常适合具有许多组件和许多订阅者的应用程序。

通过命令行安装 [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/)，可以使用 npm 或 yarn 命令（二者选一）

```
 npm install ngx-mqtt --save
 yarn add ngx-mqtt
```

## MQTT 的使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 云服务器 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建。EMQX 是一款大规模分布式物联网 MQTT 消息服务器，可高效可靠连接海量物联网设备，实时处理分发消息与事件流数据，助力构建关键业务的物联网平台与应用。

服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- WebSocket Port: **8083**

连接关键代码：

```
import {
  IMqttMessage,
  IMqttServiceOptions,
  MqttService,
  IPublishOptions,
} from 'ngx-mqtt';
import { IClientSubscribeOptions } from 'mqtt-browser';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  constructor(private _mqttService: MqttService) {
    this.client = this._mqttService;
  }
  private curSubscription: Subscription | undefined;
  connection = {
    hostname: 'broker.emqx.io',
    port: 8083,
    path: '/mqtt',
    clean: true, // 保留会话
    connectTimeout: 4000, // 超时时间
    reconnectPeriod: 4000, // 重连时间间隔
    // 认证信息
    clientId: 'mqttx_597046f4',
    username: 'emqx_test',
    password: 'emqx_test',
    protocol: 'ws',
    }
  subscription = {
    topic: 'topic/mqttx',
    qos: 0,
  };
  publish = {
    topic: 'topic/browser',
    qos: 0,
    payload: '{ "msg": "Hello, I am browser." }',
  };
  receiveNews = '';
  qosList = [
    { label: 0, value: 0 },
    { label: 1, value: 1 },
    { label: 2, value: 2 },
  ];
  client: MqttService | undefined;
  isConnection = false;
  subscribeSuccess = false;

  // 创建连接
  createConnection() {
    // 连接字符串, 通过协议指定使用的连接方式
    // ws 未加密 WebSocket 连接
    // wss 加密 WebSocket 连接
    // mqtt 未加密 TCP 连接
    // mqtts 加密 TCP 连接
    try {
      this.client?.connect(this.connection as IMqttServiceOptions)
    } catch (error) {
      console.log('mqtt.connect error', error);
    }
    this.client?.onConnect.subscribe(() => {
      this.isConnection = true
      console.log('Connection succeeded!');
    });
    this.client?.onError.subscribe((error: any) => {
      this.isConnection = false
      console.log('Connection failed', error);
    });
    this.client?.onMessage.subscribe((packet: any) => {
      this.receiveNews = this.receiveNews.concat(packet.payload.toString())
      console.log(`Received message ${packet.payload.toString()} from topic ${packet.topic}`)
    })
  }
}
```

### 订阅主题

连接 MQTT 服务器成功之后，调用当前 MQTT 实例的 subscribe 方法，传入 Topic 和 QoS 参数，即可订阅成功。

```
doSubscribe() {
  const { topic, qos } = this.subscription
  this.curSubscription = this.client?.observe(topic, { qos } as IClientSubscribeOptions).subscribe((message: IMqttMessage) => {
    this.subscribeSuccess = true
    console.log('Subscribe to topics res', message.payload.toString())
  })
}
```

### 取消订阅

unsubscribe 方法可以释放订阅持有的资源。

```
doUnSubscribe() {
  this.curSubscription?.unsubscribe()
  this.subscribeSuccess = false
}
```

### 消息发布

unsafePublish发布带有可选选项的主题的消息，如 QoS、Retain 等选项，如下所示。

```
doPublish() {
  const { topic, qos, payload } = this.publish
  console.log(this.publish)
  this.client?.unsafePublish(topic, payload, { qos } as IPublishOptions)
}
```

### 断开连接

disconnect 断开与 MQTT 客户端的连接，传入参数 True 表示强制断开与 MQTT 客户端的连接。

```
destroyConnection() {
  try {
    this.client?.disconnect(true)
    this.isConnection = false
    console.log('Successfully disconnected!')
  } catch (error: any) {
    console.log('Disconnect failed', error.toString())
  }
}
```

## 测试

我们使用 Angular 编写了如下简单的浏览器应用，该应用具备：创建连接、订阅主题、收发消息、取消订阅、断开连接等功能。完整代码请见：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js)。

![Angular MQTT Demo](https://assets.emqx.com/images/60a0b5943d2c96c1d66a96a68e671d22.png)

使用 [MQTT 5.0 客户端工具 - MQTTX](https://mqttx.app/zh) 作为另一个客户端进行消息收发测试。

![MQTT 5.0 客户端工具](https://assets.emqx.com/images/409493dd7b27f7744a805e286a337329.png)

在 MQTTX 发送第二条消息之前，在浏览器端进行取消订阅操作，浏览器端将不会收到 MQTTX 发送的后续消息。

## 总结

综上所述，我们实现了在 Angular 项目中创建 MQTT 连接，模拟了客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。

Angular 作为三大主流的前端框架之一，既能够在浏览器端使用，也能够在移动端使用，结合 MQTT 协议及 [MQTT 物联网云服务](https://www.emqx.com/zh/cloud) 可以开发出很多有趣的应用，比如客服聊天系统或实时监控物联网设备信息的管理系统等。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
