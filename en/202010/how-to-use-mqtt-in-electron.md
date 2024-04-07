[Electron](https://www.electronjs.org/) is an open-source software framework developed and maintained by GitHub. It allows for the development of desktop GUI applications using web technologies: it combines the Chromium rendering engine and the Node.js runtime. Electron is the main GUI framework behind several notable open-source projects including Atom, GitHub Desktop, Light Table, Visual Studio Code, and WordPress Desktop.[^1]

A basic Electron includes three files: `package.json` (metadata) `main.js` (code) and `index.html` (graphical user interface). The frame is provided by the Electron executable file (electron.exe on Windows, electron.app on macOS, electron on Linux). Developers are free to add flags, customize icons, rename or edit Electron executable files.

This article mainly introduces how to use [MQTT](https://www.emqx.com/en/mqtt-guide) in Electron projects, and complete a simple MQTT desktop client, and implement the connection, subscription, unsubscribe, messaging and other functions between the client and [MQTT broker](https://www.emqx.com/en/products/emqx).

## Project initialization

### New project

There are many ways to build a new project, but here is a brief list of a few:

- To create manually, do the following in the self-built project directory

  ```shell
  cd your-project

  npm init

  npm i -D electron@lates
  ```

  Also, refer to the following documentation for the steps to build the project.

  Address: [https://www.electronjs.org/docs/tutorial/first-app](https://www.electronjs.org/docs/tutorial/first-app)

- Rapid development with the official template projects `electron-qucik-start`.

  Address: [https://github.com/electron/electron-quick-start](https://github.com/electron/electron-quick-start)

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

- Rapid development builds with the template project `electron-react-bolierplate`, which can be developed using `React.js`.

  Address: https://github.com/electron-react-boilerplate/electron-react-boilerplate

  ```shell
  git clone --depth 1 --single-branch https://github.com/electron-react-boilerplate/electron-react-boilerplate.git your-project-name
  cd your-project-name
  yarn
  ```

- The rapid development build of the project via `electron-vue` will be coupled with project initialization using the `vue-cli` tool, which can be developed using `Vue.js`.

  Address: https://github.com/SimulatedGREG/electron-vue

  ```shell
  # Install vue-cli and scaffold boilerplate
  npm install -g vue-cli
  vue init simulatedgreg/electron-vue my-project

  # Install dependencies and run your app
  cd my-project
  yarn # or npm install
  yarn run dev # or npm run dev
  ```

In this article, the official electron quick start project template will be used to initialize the project in order to quickly build the example project.

### Installation dependencies

Installation through the command line

```shell
npm install mqtt --save
```

After the dependencies are installed, if you want to open the console for debugging, you need to modify the code in `main.js` and uncomment `win.webContents.openDevTools()`.

```javascript
// Open the DevTools.
mainWindow.webContents.openDevTools()
```

In this case, the locally installed `MQTT.js` module cannot be loaded directly into `renderer.js` without using the front-end builder to package the front-end page. In addition to using the build tool method, there are two other ways to solve this:

1. `nodeIntegration` can be set to true in `webPreferences`. When this property is present, `webview` will have Node integration in it, and node APIs like `require` and `process` can be used to access low-level system resources. Node integration is disabled by default.

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

2. The [MQTT.js](https://www.emqx.com/en/blog/mqtt-js-tutorial) module can be imported in preload.js. When there is no node integration, this script still can access all Node APIs. However, when this script execution completes, global objects injected via Node will be removed.

3. The [MQTT.js](https://www.emqx.com/en/blog/mqtt-js-tutorial) module can be imported in main process and connected. In Electron, processes communicate by passing messages through developer-defined "channels" with the [`ipcMain`](https://www.electronjs.org/docs/latest/api/ipc-main) and [`ipcRenderer`](https://www.electronjs.org/docs/latest/api/ipc-renderer) modules. These channels are **arbitrary** (you can name them anything you want) and **bidirectional** (you can use the same channel name for both modules). For usage examples, check out the [IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc).

   For example, in the main process, ipcMain listens for connection operations. When the user clicks the connection, the corresponding configuration information collected in the render process is transferred to the main process through ipcRenderer to connect:

   - Receive the connection data sent by the rendering process in the main process and make MQTT connection:

   ```js
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

   - Click to connect in the rendering process, get the connection data from the page and send it to the main process:

   ```js
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

   - In preload.js, the API method for interprocess IPC communication is implemented, and the channel is established:

   ```js
   // preload.js
   contextBridge.exposeInMainWorld('electronAPI', {
     onConnect: (data) => ipcRenderer.send('onConnect', data),
   })
   ```

## The use of MQTT

### Connect to the MQTT broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service was created based on the EMQX [MQTT IoT cloud platform](https://www.emqx.com/en/cloud). The information about broker access is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/b4cff1e553053873a87c4fa8713b99bc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      A Practical Guide to MQTT Broker Selection
    </div>
    <div class="promotion-pdf__desc">
      Download this practical guide and learn what to consider when choosing an MQTT broker.
    </div>
    <a href="https://www.emqx.com/en/resources/a-practical-guide-to-mqtt-broker-selection?utm_campaign=embedded-a-practical-guide-to-mqtt-broker-selection&from=blog-how-to-use-mqtt-in-electron" class="button is-gradient">Get the eBook →</a>
  </div>
</section>

To illustrate more intuitive, the key connection code for the example will be written in the renderer.js file. With the consideration of security, the installed MQTT module will be loaded via the require method of the Node.js API, in the preload.js file (using method 2 above). Also, this method injecting it in the global window object.

> **Note:** [Context isolation (contextIsolation)](https://www.electronjs.org/docs/latest/tutorial/context-isolation) has been enabled by default since Electron 12, Although preload scripts share a `window` global with the renderer they're attached to, you cannot directly attach any variables from the preload script to `window` because of the [`contextIsolation`](https://www.electronjs.org/docs/latest/tutorial/context-isolation) default.

Therefore, we need to set `contextIsolation: false` in webPreferences to close:

```js
const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false; // Version 12.0.0 above are enabled by default
    }
  })
```

So that the loaded module can be accessed directly in `renderer.js`:

- Import MQTT module

```javascript
// preload.js
const mqtt = require('mqtt')
window.mqtt = mqtt
```

- Configure and test MQTT module

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

We can see the following output on the console after writing the above code and running the project:

![electronconsole.png](https://assets.emqx.com/images/eb708f312630c441bd6f2453af36372e.png)

The MQTT module works fine. After setting up the module, we can write a simple UI interface to manually enter the configuration required for the MQTT connection, and click the connect button to connect to the MQTT server, as well as disconnect, subscribe to topics, send and receive messages, and so on.

**Interface of application**

![electronui.png](https://assets.emqx.com/images/f628816b73b31e6d3c695cd39c439ca6.png)

The complete code is available here: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Electron).

### Key code

#### Connect

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

#### Subscribe to the topic

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

#### Unsubscribe

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

#### Publish messages

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

#### Receive messages

```javascript
// In the onConnect function
client.on('message', (topic, message) => {
  const msg = document.createElement('div')
  msg.setAttribute('class', 'message-body')
  msg.innerText = `${message.toString()}\nOn topic: ${topic}`
  document.getElementById('article').appendChild(msg)
})
```

#### Disconnect

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

### Client test

At this point, we test the sending and receiving of messages with a [MQTT 5.0 client tool - MQTTX](https://mqttx.app), also written in Electron.

When using MQTTX to send a message to the client, you can see that the message is received properly:

![electronmessage.png](https://assets.emqx.com/images/bfb62b9f23f6836627d8e129d38b9160.png)

Send a message to MQTTX using the client you wrote yourself, and now you can see that MQTTX is also receiving the message properly:

![mqttx.png](https://assets.emqx.com/images/cc97fe533fcce20765530970d7696f58.png)

## Summary

So far, we have completed that use Electron to create a simple MQTT desktop client, and simulate the connection, messaging, unsubscribe and disconnect scenarios between the client and MQTT broker. It is also worth noting that since the Electron project includes both a browser environment and a Node.js environment, it is possible to use the browser's WebSocket API to implement an MQTT over WebSocket connection by modifying the connection protocol and port number in the above code.

## Resources

- [How to Use MQTT in Vue](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [How to Use MQTT in React](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [How to Use MQTT in Angular](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [How to Use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)


[^1]: https://en.wikipedia.org/wiki/Electron_(software_framework)

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
