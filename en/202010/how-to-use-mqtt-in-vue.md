[Vue](https://vuejs.org) is a progressive framework for building user interfaces. Unlike other monolithic frameworks, Vue is designed from the ground up to be incrementally adoptable. The core library is focused on the view layer only, and is easy to pick up and integrate with other libraries or existing projects. On the other hand, Vue is also perfectly capable of powering sophisticated Single-Page Applications when used in combination with modern tooling and supporting libraries.

[MQTT](https://www.emqx.com/en/mqtt) is a kind of **lightweight IoT messaging protocol** based on the publish/subscribe model. This protocol provides one-to-many message distribution and decoupling of applications. It has several advantages which are low transmission consumption and protocol data exchange, minimized network traffic, three different service quality levels of message which can meet different delivery needs. 

This article mainly introduces how to use MQTT in the Vue project, and implement the connection, subscription, messaging, unsubscribing and other functions between the client and MQTT broker.



## Project initialization

### Create project

The reference link is as follows:

- [Use Vue CLI create Vue project](https://cli.vuejs.org/guide/creating-a-project.html#vue-create) 
- [Create Vue project through introduce Vue.js](https://vuejs.org/v2/guide/installation.html)

Examples: 

```shell
vue create vue-mqtt-test
```

### Install MQTT client library

> The following method 2 and 3 are more suitable for the project that directly introduces Vue.js.

1. Installed from the command line, either using npm or yarn (one or the other)

   ```
   npm install mqtt --save
   # or yarn
   yarn add mqtt
   ```

2. Import via CDN

   ```html
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
   ```

3. Download locally, then import using relative paths

   ```html
   <script src="/your/path/to/mqtt.min.js"></script>
   ```



## The use of MQTT

### Connect to the MQTT broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service was created based on the EMQX [MQTT IoT cloud platform](https://www.emqx.com/en/cloud). The information about broker access is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

The key code of connection:

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
        clean: true, // Reserved session
        connectTimeout: 4000, // Time out
        reconnectPeriod: 4000, // Reconnection interval
        // Certification Information
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
    // Create connection
    createConnection() {
      // Connect string, and specify the connection method used through protocol
      // ws unencrypted WebSocket connection
      // wss encrypted WebSocket connection
      // mqtt unencrypted TCP connection
      // mqtts encrypted TCP connection
      // wxs WeChat mini app connection
      // alis Alipay mini app connection
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

### Subscribe topic

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

### Unsubscribe

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

### Publish messages

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

### Disconnect

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



## Test

We use Vue to write the following simple browser application. This application has: create connection, subscribe topic, messaging, unsubscribe, disconnect and other functions.

The complete code for this project: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js)。

![vueui.png](https://assets.emqx.com/images/b6563b0eb66eb51a2a02776889016a18.png)



Use [MQTT 5.0 client tool - MQTT X](https://mqttx.app/) as another client to test messaging.

![vuemqttx.png](https://assets.emqx.com/images/2013cbab1bdffcae69b817bfebb4a33f.png)

If you unsubscribe on the browser-side, before MQTT X sends the second message, the browser will not receive the subsequent messages from MQTT X.



## Summary

In summary, we have implemented the creation of an MQTT connection in a Vue project, simulated subscribing, sending and receiving messages, unsubscribing, and disconnecting between the client and MQTT broker.

As one of the most three popular front-end frames, Vue can be used on the browser-side, and can also be used on the mobile-side. Combining the [MQTT protocol](https://www.emqx.com/en/mqtt) and [MQTT IoT cloud service](https://www.emqx.com/en/cloud), can develop many interesting applications, for example, a customer service chat system or a management system that monitors IoT device information in real-time.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
