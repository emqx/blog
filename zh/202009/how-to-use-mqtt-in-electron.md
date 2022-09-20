[Electron](https://www.electronjs.org/) 是由 GitHub 开发的一个开源框架。它允许使用 `Node.js`（作为后端）和 [Chromium](https://zh.wikipedia.org/wiki/Chromium)（作为前端）完成桌面 GUI 应用程序的开发。Electron 现已被多个开源 Web 应用程序应用于跨平台的桌面端软件开发，著名项目包括 GitHub 的 Atom，微软的 Visual Studio Code，Slack 的桌面应用等。[^1]

一个基础的 Electron 包含三个文件：`package.json`（元数据）、`main.js`（代码）和 `index.html`（图形用户界面）。框架由 Electron 可执行文件（Windows 中为 electron.exe、macOS 中为 electron.app、Linux 中为 electron）提供。开发者可以自行添加标志、自定义图标、重命名或编辑 Electron 可执行文件。

本文主要介绍如何在 Electron 项目中使用 [MQTT](https://www.emqx.com/zh/mqtt)，完成一个简单的 MQTT 桌面客户端并实现客户端与 [MQTT 服务器](https://www.emqx.com/zh/products/emqx) 的连接、订阅、取消订阅、收发消息等功能。



## 项目初始化

### 新建项目

新建项目的方式有很多种，以下简单列举几种：

- 手动创建，在自建项目目录下执行以下操作

  ```shell
  cd your-project
  
  npm init
  
  npm i -D electron@latest
  ```

  并参考以下文档中的步骤进行项目搭建。

  地址：https://www.electronjs.org/docs/tutorial/first-app

- 通过官方提供的 `electron-quick-start` 模版项目进行快速开发

  地址：https://github.com/electron/electron-quick-start

  ```shell
    # Clone this repository
    git clone https://github.com/electron/electron-quick-start
    # Go into the repository
    cd electron-quick-start
    # Install dependencies
    npm install
    # Run the app
    npm start
  ```

- 通过 `electron-react-bolierplate` 的模板项目进行快速开发构建，该模版可使用 `React.js` 进行开发

  地址：https://github.com/electron-react-boilerplate/electron-react-boilerplate

  ```shell
  git clone --depth 1 --single-branch https://github.com/electron-react-boilerplate/electron-react-boilerplate.git your-project-name
  cd your-project-name
  yarn
  ```

- 通过 `electron-vue` 进行项目的快速开发构建，将配合使用 `vue-cli` 工具进行项目初始化，该方法可使用 `Vue.js` 进行开发

  地址：https://github.com/SimulatedGREG/electron-vue

  ```shell
  # Install vue-cli and scaffold boilerplate
  npm install -g vue-cli
  vue init simulatedgreg/electron-vue my-project
  
  # Install dependencies and run your app
  cd my-project
  yarn # or npm install
  yarn run dev # or npm run dev
  ```

本文为方便快速搭建示例项目，将使用官方提供的 electron quick start 项目模板进行项目初始化构建。

### 安装依赖

通过命令行安装

```shell
npm install mqtt --save
```

安装依赖完成后，如需打开控制台进行调试，需要在 `main.js` 文件中修改代码，将 `win.webContents.openDevTools()` 取消注释。

```javascript
// Open the DevTools.
mainWindow.webContents.openDevTools()
```

如此时未使用前端构建工具对前端页面进行打包构建的话，无法直接在 `renderer.js` 中加载到本地已经安装的 `MQTT.js` 模块。除使用构建工具方法外，还提供另外两种解决方法：

1. 可以在 webPreferences 中设置 nodeIntegration 为 true，当有此属性时, `webview` 中将具有 Node 集成, 并且可以使用像 `require` 和 `process` 这样的 node APIs 去访问低层系统资源。 Node 集成默认是禁用的。

   ```javascript
   const mainWindow = new BrowserWindow({
       width: 800,
       height: 600,
       webPreferences: {
         nodeIntegration: true,
         preload: path.join(__dirname, 'preload.js')
       }
     })
   ```

2. 可以在 `preload.js` 中进行引入 `MQTT.js` 模块操作。当没有 node integration 时，这个脚本仍然有能力去访问所有的 Node APIs, 但是当这个脚本执行执行完成之后，通过 Node 注入的全局对象（global objects）将会被删除。



## MQTT 的使用

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/en/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

为更直观表达，示例的关键连接代码将在 `renderer.js` 文件中编写，并考虑到安全问题，将使用上文中如何引入 `MQTT.js` 里的方法 2，在 `preload.js` 文件中通过 Node.js API 的 `require` 方法加载已安装的 MQTT 模块，并挂载到全局的 `window` 对象中，这样在 `renderer.js` 中，便可以直接访问已加载的模块：

- 引入 MQTT 模块

```javascript
// preload.js
const mqtt = require('mqtt')
window.mqtt = mqtt
```

- 配置测试 MQTT 模块

```javascript
// renderer.js
const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'mqtt://broker.emqx.io:1883'

const options = {
  keepalive: 30,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  },
  rejectUnauthorized: false
}

// 可查看到 mqtt 模块的信息
console.log(mqtt)

console.log('connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})

client.on('reconnect', () => {
  console.log('Reconnecting...')
})

client.on('connect', () => {
  console.log('Client connected:' + clientId)
  client.subscribe('testtopic/electron', {
    qos: 0
  })
  client.publish('testtopic/electron', 'Electron connection demo...!', {
    qos: 0,
    retain: false
  })
})

client.on('message', (topic, message, packet) => {
  console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
})
```

可以看到，在编写完以上代码后并且运行该项目后可以在控制台看到以下内容输出：

![electronconsole.png](https://assets.emqx.com/images/eb708f312630c441bd6f2453af36372e.png)

MQTT 模块运行正常。在设置好模块后，我们就可以编写一个简单的 UI 界面来手动输入 MQTT 连接时所需要的配置等，并在点击连接按钮后可以连接到 MQTT 服务器，此外还可以断开连接，订阅主题，收发消息等。

**应用程序界面**

![electronui.png](https://assets.emqx.com/images/f628816b73b31e6d3c695cd39c439ca6.png)

项目完整代码请见：[https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron)。

### 关键代码

#### 连接

```javascript
  let client = null
  
  const options = {
    keepalive: 30,
    protocolId: 'MQTT',
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 1000,
    connectTimeout: 30 * 1000,
    will: {
      topic: 'WillMsg',
      payload: 'Connection Closed abnormally..!',
      qos: 0,
      retain: false
    },
  }
  
  function onConnect () {
    const { host, port, clientId, username, password } = connection
    const connectUrl = `mqtt://${host.value}:${port.value}`
    options.clientId = clientId.value || `mqttjs_${Math.random().toString(16).substr(2, 8)}`
    options.username = username.value
    options.password = password.value
    console.log('connecting mqtt client')
    client = mqtt.connect(connectUrl, options)
    client.on('error', (err) => {
      console.error('Connection error: ', err)
      client.end()
    })
    client.on('reconnect', () => {
      console.log('Reconnecting...')
    })
    client.on('connect', () => {
      console.log('Client connected:' + options.clientId)
      connectBtn.innerText = 'Connected'
    })
  }
```
#### 订阅主题

```javascript
  function onSub () {
    if (client.connected) {
      const { topic, qos } = subscriber
      client.subscribe(topic.value, { qos: parseInt(qos.value, 10) }, (error, res) => {
         if (error) {
           console.error('Subscribe error: ', error)
         } else {
           console.log('Subscribed: ', res)
         }
      })
    }
  }
```
#### 取消订阅

```javascript
  function onUnsub () {
    if (client.connected) {
      const { topic } = subscriber
      client.unsubscribe(topic.value, error => {
        if (error) {
          console.error('Unsubscribe error: ', error)
        } else {
          console.log('Unsubscribed: ', topic.value)
        }
      })
    }
  }
```
#### 消息发布

```javascript
  function onSend () {
    if (client.connected) {
      const { topic, qos, payload } = publisher
      client.publish(topic.value, payload.value, {
        qos: parseInt(qos.value, 10),
        retain: false
      })
    }
  }
```
#### 接收消息

```javascript
// 在 onConnect 函数中
client.on('message', (topic, message) => {
  const msg = document.createElement('div')
  msg.className = 'message-body'
  msg.setAttribute('class', 'message-body')
  msg.innerText = `${message.toString()}\nOn topic: ${topic}`
  document.getElementById('article').appendChild(msg)
})
```
#### 断开连接

```javascript
  function onDisconnect () {
    if (client.connected) {
      client.end()
      client.on('close', () => {
        connectBtn.innerText = 'Connect'
        console.log(options.clientId + ' disconnected')
      })
    }
  }
```

### 客户端测试

此时我们配合一款同样使用 Electron 编写的 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 进行消息的收发测试。

使用 MQTT X 向客户端发送一条消息时，可以看到能正常接收到消息：

![electronmessage.png](https://assets.emqx.com/images/bfb62b9f23f6836627d8e129d38b9160.png)

使用自己编写的客户端向 MQTT X 发送一条消息，此时可以看到 MQTT X 也能正常接收到消息：

![mqttx.png](https://assets.emqx.com/images/cc97fe533fcce20765530970d7696f58.png)



## 总结

至此， 我们就完成了使用 Electron 创建一个简单的 MQTT 桌面客户端的过程，并模拟了客户端与 MQTT 服务器进行订阅、收发消息、取消订阅以及断开连接的场景。还值得一提的是，因为 Electron 项目同时包含了浏览器环境和 `Node.js` 环境，所以除 MQTT/TCP 连接外，还可以利用浏览器的 WebSocket API，同时实现 MQTT over WebSocket 的连接，只需修改上述代码中的连接协议和端口即可。具体如何使用 WebSocket 连接 MQTT 服务，可参考我们的博客 [使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)。



[^1]: https://zh.wikipedia.org/wiki/Electron


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
