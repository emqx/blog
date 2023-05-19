React Native 是 Facebook 推出并开源的跨平台移动应用开发框架，是 React 在原生移动应用平台的衍生产物，支持 iOS 和安卓两大平台。React Native 使用 Javascript 语言，类似于 HTML 的 JSX，以及 CSS 来开发移动应用，因此熟悉 Web 前端开发的技术人员只需很少的学习就可以进入移动应用开发领域，同时 React Native 也提供了接近原生应用的性能和体验。

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议** ，可在严重受限的硬件设备和低带宽、高延迟的网络上实现稳定传输。它凭借简单易实现、支持 QoS、报文小等特点，占据了物联网协议的半壁江山。

本文主要介绍如何在 React Native 项目中使用 MQTT，实现客户端与服务器的连接、订阅、取消订阅、收发消息等功能。

### 新建 React Native 项目

这里以创建一个名为 `RNMQTTDemo` 的项目为例，开发环境为 macOS，应用平台为 iOS，具体过程参考 [Setting up the development environment](https://reactnative.dev/docs/environment-setup)。

项目创建完成后，在项目根目录环境下，执行以下命令安装所需依赖：

```
npm install @react-native-async-storage/async-storage @rneui/base @rneui/themed
```

### 安装 MQTT 客户端模块

```
npm install react_native_mqtt
```

react_native_mqtt 是一个在 React Native 项目中使用的 MQTT 客户端模块，支持 iOS 和 Android。

### MQTT 客户端模块使用

#### 连接 MQTT 服务器

这里使用 EMQ 提供的免费公共 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQ 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

#### 创建客户端实例

```
init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  sync : {}
});
const options = {
  host: 'broker.emqx.io',
  port: 8083,
  path: '/testTopic',
  id: 'id_' + parseInt(Math.random()*100000)
};
client = new Paho.MQTT.Client(options.host, options.port, options.path);
```

#### 连接 MQTT 服务器

```
  connect = () => {
    this.setState(
      { status: 'isFetching' },
      () => {
        client.connect({
          onSuccess: this.onConnect,
          useSSL: false,
          timeout: 3,
          onFailure: this.onFailure
        });
      }
    );
  }
```

#### 主题订阅

```
  subscribeTopic = () => {
    this.setState(
      { subscribedTopic: this.state.topic },
      () => {
        client.subscribe(this.state.subscribedTopic, { qos: 0 });
      }
    );
  }
```

#### 消息发布

```
  sendMessage = () =>{
    var message = new Paho.MQTT.Message(options.id + ':' + this.state.message);
    message.destinationName = this.state.subscribedTopic;
    client.send(message);
  }
```

#### 取消订阅

```
  unSubscribeTopic = () => {
    client.unsubscribe(this.state.subscribedTopic);
    this.setState({ subscribedTopic: '' });
  }
```

### 运行项目

完整的 RNMQTTDemo 项目地址：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React-Native](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React-Native) 。

在项目根目录环境下，新建两个终端窗口，分别执行以下命令：

```
npx react-native start
npx react-native run-ios
```

执行完后将看到应用运行在 iOS 的模拟器中，其中顶部显示的是当前客户端的 id，如下图：

![MQTT React Native iOS](https://assets.emqx.com/images/180f325e5b2ff3d34be952a9df99aff2.png)

### MQTT 连接测试

这里使用 [MQTT 5.0 客户端工具 - MQTTX](https://mqttx.app/zh) 进行相关测试，创建一个名为 react-native-demo 的连接，所有配置项均使用默认值，点击连接按钮，连接成功后添加一个主题名称为 testTopic 的订阅，显示如下：

![MQTT 5.0 客户端工具 - MQTTX](https://assets.emqx.com/images/f4b8a59a025f95cf712c26e9482419d3.png)

#### 连接

点击 APP 中的 CONNECT 按钮，连接成功后的界面显示如下，其中顶部 ClientID 一行的内容变成绿色，表示已成功连接到 MQTT 服务器。

![连接 MQTT 服务器](https://assets.emqx.com/images/2191362e7bf727560de823815ad9bce5.png)

#### 主题订阅

输入需要订阅的主题，这里以 `testTopic` 为例，然后点击 SUBSCRIBE 按钮，订阅后的界面显示如下：

![订阅 MQTT 主题](https://assets.emqx.com/images/563ad2c30b75d75a1b9b30442d53edd6.png)

#### 消息发布

输入需要发布的消息内容，输入完成后点击 PUBLISH 按钮，最下方会列出当前订阅主题下接收到的消息，其中黑色背景的消息是当前客户端发出去的，id_67485 就是当前客户端的 id，界面显示如下：

![MQTT 消息发布](https://assets.emqx.com/images/b6cc5c392784791198c10660380dd39c.png)

同时在 MQTTX 的 react-native-demo 连接下，也往 `testTopic` 主题发布一些消息，同时也能看到客户端 id 为 id_67458 往该主题发布的消息，显示如下：

![MQTT 消息发布](https://assets.emqx.com/images/2aec69acb78aeddc53cc11531298e697.png)

#### 取消订阅

在 APP 中点击 UNSCRIBE 按钮，然后在 MQTTX 上继续往 testTopic 主题发布一条内容为 `{ "msg": "hello test" }` 的消息，显示如下：

![MQTT 消息发布](https://assets.emqx.com/images/c9c7b3cb40785fbf111b6c6487774fa0.png)

取消订阅 testTopic 主题后，未收到 MQTTX 往该主题发布的消息 `{ "msg": "hello test" }`

![MQTT 取消订阅](https://assets.emqx.com/images/27caa87029972c19f711ba986b3638e8.png)


### 总结

至此，我们完成了在 iOS 平台上利用 React Native 构建一个 MQTT 应用，实现了客户端与 MQTT 服务器的连接、主题订阅、收发消息、取消订阅等功能。

通过 React Native，开发者可以使用标准的 iOS 平台组件，开发出的应用几乎与原生应用的性能相似；无缝的跨平台可以让团队更快地工作，同时开发过程中只需将改动保存，即可在 iOS 模拟器中查看实际效果。高效、接近原生的性能、热重载和广泛的社区支持，使得 React Native 成为很多移动应用开发者的最佳选择，而结合 React Native、MQTT 协议以及 [MQTT 云服务](https://www.emqx.com/zh/cloud)，我们也可以开发出很多有趣的创新应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
