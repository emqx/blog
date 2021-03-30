

React 是一款用于构建用户界面的开源 JavaScript 库。React 视图通常采用包含以自定义 HTML 规定的其他组件的组件渲染。React 为程序员提供了一种子组件不能直接影响外层组件（"data flows down"）的模型，数据改变时对视图进行了有效更新，实现了在现代单页应用中组件之间的干净分离。由于 React 的设计思想极其独特，属于革命性创新，性能出众，代码逻辑却非常简单。所以，越来越多的人开始关注和使用，目前是 Web 开发的主流工具之一。

React 起源于 Facebook 的内部项目，目前由 Facebook 企业和其强大的开源社区进行维护。React 目前正在被 Netflix、Instagram、Imgur、Airbnb 等很多知名网站的主页使用。该框架首先于 2011 年部署于 Facebook 的 newsfeed，随后于 2012 年部署于 Instagram。在2013年5月在 JSConf US 开源。

本文主要介绍如何在 React 项目中使用 [MQTT](https://www.emqx.io/cn/mqtt)，实现客户端与 MQTT 服务器的连接、订阅、收发消息、取消订阅等功能。



## 项目初始化

### 新建项目

参考链接：[https://zh-hans.reactjs.org/docs/getting-started.html](https://zh-hans.reactjs.org/docs/getting-started.html)

- 使用 Create React App 创建新的 React 应用

  ```shell
  npx create-react-app react-mqtt-test
  ```

  如需使用 TypeScript 只需要在命令行后加入 --template typescript 参数即可

  ```shell
  npx create-react-app react-mqtt-test --template typescript
  ```

  然后添加 React 项目中需要的 TypeScript 的类型库

  ```shell
  npm install --save typescript @types/node @types/react @types/react-dom @types/jest
  # or
  yarn add typescript @types/node @types/react @types/react-dom @types/jest
  ```

  使用 TypeScript 将不作为本文示例中的使用重点介绍，如需使用，可参考该创建示例和完整的代码示例后自行添加 TypeScript 特性。

- 使用 CDN 链接引入 React

  ```html
  <script crossorigin src="https://unpkg.com/react@16/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"></script>
  ```

### 安装 MQTT 客户端库

因为 React 是一款 JavaScript 库，因此可以使用 MQTT.js 作为 MQTT 客户端库。

> 以下 2，3 方法更适用于通过 CDN 链接 引用 React 创建的项目。

1. 通过命令行安装，可以使用 npm 或 yarn 命令（二者选一）

   ```shell
   npm install mqtt --save
   # or
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



## MQTT 使用

### 连接 MQTT 服务器

本文将使用 EMQ X 提供的 [免费公共 MQTT 服务器](https://www.emqx.io/cn/mqtt/public-mqtt5-broker)，该服务基于 EMQ X 的 [MQTT 物联网云平台](https://cloud.emqx.io/) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

### 连接代码

```javascript
const [client, setClient] = useState(null);
const mqttConnect = (host, mqttOption) => {
  setConnectStatus('Connecting');
  setClient(mqtt.connect(host, mqttOption));
};
useEffect(() => {
  if (client) {
    console.log(client)
    client.on('connect', () => {
      setConnectStatus('Connected');
    });
    client.on('error', (err) => {
      console.error('Connection error: ', err);
      client.end();
    });
    client.on('reconnect', () => {
      setConnectStatus('Reconnecting');
    });
    client.on('message', (topic, message) => {
      const payload = { topic, message: message.toString() };
      setPayload(payload);
    });
  }
}, [client]);
```

### 订阅主题

```javascript
const mqttSub = (subscription) => {
  if (client) {
    const { topic, qos } = subscription;
    client.subscribe(topic, { qos }, (error) => {
      if (error) {
        console.log('Subscribe to topics error', error)
        return
      }
      setIsSub(true)
    });
  }
};
```

### 取消订阅

```javascript
const mqttUnSub = (subscription) => {
  if (client) {
    const { topic } = subscription;
    client.unsubscribe(topic, error => {
      if (error) {
        console.log('Unsubscribe error', error)
        return
      }
      setIsSub(false);
    });
  }
};
```

### 消息发布

```javascript
const mqttPublish = (context) => {
  if (client) {
    const { topic, qos, payload } = context;
    client.publish(topic, payload, { qos }, error => {
      if (error) {
        console.log('Publish error: ', error);
      }
    });
  }
}
```

### 断开连接

```javascript
const mqttDisconnect = () => {
  if (client) {
    client.end(() => {
      setConnectStatus('Connect');
    });
  }
}
```

## 测试

我们使用 React 编写了如下简单的浏览器应用，该应用具备：创建连接、订阅主题、收发消息、取消订阅、断开连接等功能。

完整项目示例代码：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React)。

![reactmqttpage.png](https://static.emqx.net/images/d1c51195c056f3b4afb267edaeb217f0.png)

使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/cn/) 作为另一个客户端进行消息收发测试。

![reactmqttx.png](https://static.emqx.net/images/621ba9544ea69f9ee7b24203846d0409.png)

可以看到 MQTT X 可以正常接收来自浏览器端发送的消息，同样，使用 MQTT X 向该主题发送一条消息时，也可以看到浏览器端可以正常接收到该消息。

![reactmqtttest.png](https://static.emqx.net/images/da008ae3544a83a3efa78266190ea364.png)



## 总结

综上所述，我们实现了在 React 项目中创建 MQTT 连接，模拟了客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。

本文使用的 React 版本为 v16.13.1，因此将使用 Hook Component 特性来作为示例代码演示，如有需求也可参考完整的示例代码中的 `ClassMqtt` 组件来使用 Class Component 特性来进行项目构建。
