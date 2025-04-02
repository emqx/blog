## 介绍

[Electron](https://www.electronjs.org/) 是由 GitHub 开发和维护的开源软件框架。它支持开发人员通过结合 Chromium 渲染引擎和 Node.js 创建桌面 GUI 应用程序。Electron 是几个著名项目背后的主要 GUI 框架，包括 Visual Studio Code 和 GitHub Desktop 等开源应用程序，以及 Slack、Discord 和 Microsoft Teams 等商业应用程序。

一个基本的 Electron 包括三个文件：（`package.json`元数据）、`main.js`（代码）和`index.html`（图形用户界面）。框架由 Electron 可执行文件（Windows 上为 electron.exe，macOS 上为 electron.app，Linux 上为 electron）提供。开发人员可以自由添加标志、自定义图标、重命名或编辑 Electron 可执行文件。

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（消息队列遥测传输）是一种轻量级消息传递协议，旨在实现设备之间（尤其是在物联网生态系统中）的快速、高效和可靠通信。通过将 MQTT 集成到 Electron 中，开发人员可以利用其低开销、高性能和易用性，以无缝且响应迅速的方式管理桌面客户端与各种连接设备或服务之间的通信。

本文讲解如何在 Electron 项目中使用 MQTT ，创建一个简单的 MQTT 桌面客户端，实现客户端与 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)之间的连接、订阅、取消订阅、消息发送等功能。

## 项目初始化

### 新建项目

新建项目的方式有很多种，以下简单列举几种：

#### 手动创建

在自建项目目录下执行以下操作

```
cd your-project

npm init

npm i -D electron@lates
```

或者，你可以按照 Electron 官方文档来构建你的项目：https://www.electronjs.org/docs/tutorial/first-app

#### 使用官方模板项目进行快速开发

- `electron-quick-start` ：[https://github.com/electron/electron-quick-start](https://github.com/electron/electron-quick-start) 

  ```
   # Clone this repository
   git clone https://github.com/electron/electron-quick-start
   # Go into the repository
   cd electron-quick-start
   # Install dependencies
   npm install
   # Run the app
   npm start
  ```

- `electron-react-bolierplate`: https://github.com/electron-react-boilerplate/electron-react-boilerplate

  ```
  git clone --depth 1 --single-branch https://github.com/electron-react-boilerplate/electron-react-boilerplate.git your-project-name
  cd your-project-name
  yarn
  
  ```

- `electron-vue` : https://github.com/SimulatedGREG/electron-vue

  ```
  # Install vue-cli and scaffold boilerplate
  npm install -g vue-cli
  vue init simulatedgreg/electron-vue my-project
  
  # Install dependencies and run your app
  cd my-project
  yarn # or npm install
  yarn run dev # or npm run dev
  ```

在本文中，我们将使用官方提供的 electron quick start 模板进行项目初始化构建。

### 在你的 Electron 项目中安装 MQTT

要开始在 Electron 项目中集成 MQTT，你需要安装 [MQTT.js 库](https://github.com/mqttjs/MQTT.js)。

您可以使用 npm 通过命令行轻松完成此操作：

```
npm install mqtt --save
```

安装依赖完成后，如需打开控制台进行调试，需要在 `main.js` 中修改代码，并将 `win.webContents.openDevTools()` 取消注释。

```javascript
// Open the DevTools.
mainWindow.webContents.openDevTools()
```

在这种情况下，如果不使用前端构建工具对页面进行打包构建，就无法直接在 `renderer.js` 中加载到本地已经安装的 `MQTT.js` 模块。除使用构建工具方法外，还有另外两种解决方法：

1、在 webPreferences 中设置 nodeIntegration 为 true，当此属性存在时, `webview` 中将具有 Node 集成, 并且可以使用 `require` 和 `process` 这样的 node APIs 去访问低层系统资源。默认情况下，Node 集成是禁用的。

```javascript
const mainWindow = new BrowserWindow({
  width: 800,
  height: 600,
  webPreferences: {
    nodeIntegration: true,
    preload: path.join(__dirname, 'preload.js'),
  },
})
```

2、可以在 `preload.js` 中引入 `MQTT.js` 模块操作。当没有 node integration 时，这个脚本仍然有能力去访问所有的 Node APIs，但脚本执行执行完成后，通过 Node 注入的全局对象（global objects）将会被删除。

3、可以在 main 主进程中引入 `MQTT.js` 并进行连接操作，使用 Electron 的 IPC 机制来实现不同的进程间相互通信。在 Electron 中，主进程使用 `ipcMain`，渲染进程使用 `ipcRenderer` 模块，二者通过开发人员定义的「通道」进行通信。 这些通道是 **任意** （您可以随意命名它们）和 **双向** （您可以在两个模块中使用相同的通道名称）的。有关用法示例，请查看[进程间通信（IPC）教程](https://www.electronjs.org/zh/docs/latest/tutorial/ipc)。

例如在主进程中，我们可以通过 ipcMain 监听连接操作，当用户点击连接时，render 进程中收集相应的配置信息并通过 ipcRenderer 传递到主进程进行连接：

- 在主进程中接收渲染进程发送过来的连接数据，建立 MQTT 连接：

  ```javascript
  // main.js
  ipcMain.on('onConnect', (event, connectUrl, connectOpt) => {
    client = mqtt.connect(connectUrl, connectOpt)
    client.on('connect', () => {
      console.log('Client connected:' + options.clientId)
    })
    client.on('message', (topic, message) => {
      console.log(`${message.toString()}\nOn topic: ${topic}`)
    })
  })
  
  ```

- 在渲染进程中点击连接，从页面中获取连接数据并发送到主进程：

  ```javascript
  // render.js
  function onConnect() {
    const { host, port, clientId, username, password } = connection
    const connectUrl = `mqtt://${host.value}:${port.value}`
    const options = {
      keepalive: 30,
      protocolId: 'MQTT',
      clean: true,
      reconnectPeriod: 1000,
      connectTimeout: 30 * 1000,
      rejectUnauthorized: false,
      clientId,
      username,
      password,
    }
    console.log('connecting mqtt client')
    window.electronAPI.onConnect(connectUrl, options)
  }
  
  ```

- 在 preload.js 中实现进程间 IPC 通讯的 API 方法，并建立通道：

  ```
  // preload.js
  contextBridge.exposeInMainWorld('electronAPI', {
    onConnect: (data) => ipcRenderer.send('onConnect', data),
  })
  
  ```

## 在 Electron 项目中使用 MQTT

### 连接 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 云服务](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

为更直观表达，示例中的关键连接代码将在 `renderer.js` 文件中编写。出于安全性的考虑，将在 `preload.js` 文件中通过 Node.js API 的 `require` 方法加载已安装的 MQTT 模块，并加载到全局的 `window` 对象中。

> 注意： 自 Electron 12 以来，[上下文隔离（contextIsolation）](https://www.electronjs.org/docs/latest/tutorial/context-isolation)已经默认启用，尽管预加载脚本与其附着的渲染器共享同一个全局的 `window` 对象，但您仍不能从中直接附加任何变量到 `window` 上。

因此，我们需要先在 webPreferences 中设置关闭 `contextIsolation: false` ：

```javascript
const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false; // Version 12.0.0 above are enabled by default
    }
  })

```

这样就可以直接访问已加载的模块 `renderer.js` ：

- 导入 MQTT 模块

  ```javascript
  // preload.js
  const mqtt = require('mqtt')
  window.mqtt = mqtt
  
  ```

- 配置并测试 MQTT 模块

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
      retain: false,
    },
    rejectUnauthorized: false,
  }
  
  // Information about the mqtt module is available
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
      qos: 0,
    })
    client.publish('testtopic/electron', 'Electron connection demo...!', {
      qos: 0,
      retain: false,
    })
  })
  
  client.on('message', (topic, message, packet) => {
    console.log(
      'Received Message: ' + message.toString() + '\nOn topic: ' + topic
    )
  })
  
  ```

编写完以上代码并运行该项目后，我们可以在控制台看到以下内容输出：

![electronconsole.png](https://assets.emqx.com/images/eb708f312630c441bd6f2453af36372e.png)

MQTT 模块运行正常。在设置好模块后，我们就可以编写一个简单的 UI 界面来手动输入 MQTT 连接时所需要的配置，并连接到 MQTT 服务器，此外还可以选择断开连接、订阅主题、收发消息等。

**应用程序界面**

![electronui.png](https://assets.emqx.com/images/f628816b73b31e6d3c695cd39c439ca6.png)

完整代码请见：[MQTT-Client-Examples/mqtt-client-Electron at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron)

### MQTT 集成的关键代码

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
    retain: false,
  },
}

function onConnect() {
  const { host, port, clientId, username, password } = connection
  const connectUrl = `mqtt://${host.value}:${port.value}`
  options.clientId =
    clientId.value || `mqttjs_${Math.random().toString(16).substr(2, 8)}`
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
function onSub() {
  if (client.connected) {
    const { topic, qos } = subscriber
    client.subscribe(
      topic.value,
      { qos: parseInt(qos.value, 10) },
      (error, res) => {
        if (error) {
          console.error('Subscribe error: ', error)
        } else {
          console.log('Subscribed: ', res)
        }
      }
    )
  }
}
```

#### 取消订阅

```javascript
function onUnsub() {
  if (client.connected) {
    const { topic } = subscriber
    client.unsubscribe(topic.value, (error) => {
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
function onSend() {
  if (client.connected) {
    const { topic, qos, payload } = publisher
    client.publish(topic.value, payload.value, {
      qos: parseInt(qos.value, 10),
      retain: false,
    })
  }
}
```

#### 接收消息

```javascript
// In the onConnect function
client.on('message', (topic, message) => {
  const msg = document.createElement('div')
  msg.setAttribute('class', 'message-body')
  msg.innerText = `${message.toString()}\nOn topic: ${topic}`
  document.getElementById('article').appendChild(msg)
})
```

#### 断开连接

```javascript
function onDisconnect() {
  if (client.connected) {
    client.end()
    client.on('close', () => {
      connectBtn.innerText = 'Connect'
      console.log(options.clientId + ' disconnected')
    })
  }
}
```

### 在 Electron 中测试 MQTT 连接

在这个环节中，您可以使用 [MQTT 5.0 客户端工具 - MQTTX](https://mqttx.app/zh) 进行消息的收发测试。

使用 MQTTX 向客户端发送一条消息，可以看到消息被正常接收：

![electronmessage.png](https://assets.emqx.com/images/bfb62b9f23f6836627d8e129d38b9160.png)

使用自己编写的客户端向 MQTTX 发送一条消息，也可以被正常接收：

![mqttx.png](https://assets.emqx.com/images/cc97fe533fcce20765530970d7696f58.png)

## 总结

至此，我们演示了如何使用 Electron 创建 MQTT 桌面客户端，从而实现与 IoT 应用程序 MQTT 代理的无缝通信。按照这些步骤，您可以将 MQTT 集成到自己的基于 Electron 的桌面应用程序中，实现实时消息传递和设备通信。

值得注意的是，由于 Electron 项目包含浏览器环境和 Node.js 环境，因此可以通过修改上述代码中的连接协议和端口，基于浏览器的 WebSocket API 实现 MQTT over WebSocket 连接，参考：[使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)。

## 资源

- [如何在 Vue 中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-vue)
- [如何在 React 中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-react)
- [如何在 Angular 中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-angular)
- [如何在 Node.js 中使用 MQTT](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-nodejs)
- [通过 WebSocket 使用 MQTT 的快速入门指南](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
