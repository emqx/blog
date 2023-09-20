Serverless architecture in cloud computing allows developers to focus on code development and deployment without the hassle of infrastructure management. Serverless MQTT, in particular, provides an MQTT messaging service that scales automatically based on demand, reducing the need for manual intervention.

To learn more about serverless MQTT, read our blog post [Next-Gen Cloud MQTT Service: Meet EMQX Cloud Serverless](https://www.emqx.com/en/blog/next-gen-cloud-mqtt-service-meet-emqx-cloud-serverless). In this blog series, we'll guide you through using various client libraries to set up MQTT connections, subscriptions, messaging, and more with a serverless [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for your specific project.

## Introduction

As the Internet of Things (IoT) continues to grow, more and more developers are turning to React to build applications that can interact with IoT devices. React is a popular framework for building web applications, and it's increasingly being used in IoT projects. Some of the application scenarios for React in IoT include:

- Building dashboards to monitor and control IoT devices
- Creating interfaces for IoT devices
- Developing web-based tools for managing IoT devices

This blog will provide a step-by-step guide on how to connect a serverless MQTT broker in React using the [MQTT.js library](https://github.com/mqttjs/MQTT.js). You can download the project from the Github repo [MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React).

## Prerequisites

### Free Serverless MQTT Broker

EMQX Cloud Serverless is the latest MQTT broker offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. Additionally, users can get 1 million free session minutes every month, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

If you have not tried serverless deployment yet, please follow [the guide in this blog](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to create one for free. Once you have completed the registration process with the online guide, you will get a running instance with the following similar information from the “Overview” in your deployment. We will use the connection information and CA certificate later.

![EMQX Cloud](https://assets.emqx.com/images/507b25002396a7098fd34be45e61cb6c.png)

### Install Node.js and MQTT.js library

To develop React applications locally, you will need to install [Node.js](https://nodejs.org/en/). Official installers for all major platforms are available for download at [Download | Node.js](https://nodejs.org/en/download).

React is a JavaScript library, so you can use [MQTT.js](https://www.emqx.com/en/blog/mqtt-js-tutorial) as the MQTT client library. MQTT.js is a client library for the MQTT protocol written in JavaScript and is currently the most widely used [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk) in the JavaScript ecosystem. You can install MQTT.js using NPM.



```
npm install mqtt --save
```

## Connection Code Demo

This blog uses the [mqtt-client-React Example](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React) to illustrate the process of connecting to a serverless MQTT broker. The example application provides a webpage that demonstrates how to subscribe, publish, and receive messages from an MQTT broker. As a React application, it offers two types of implementation: class and Hook. We will use the Hook implementation as an example to demonstrate how this application works.

### Import MQTT.js

To get started, import the MQTT.js client library.


```
import mqtt from 'mqtt/dist/mqtt'
```

### Initial the connection

To establish an MQTT connection, you need to set the connection address, port, and client ID. In this example, we use public MQTT broker information as the default connection information. When the application runs, you can enter the information of the Serverless MQTT broker in the input box.



```javascript
const Connection = ({ connect, disconnect, connectBtn }) => {
  const [form] = Form.useForm()
  const initialConnectionOptions = {
    // ws or wss
    protocol: 'ws',
    host: 'broker.emqx.io',
    clientId: 'emqx_react_' + Math.random().toString(16).substring(2, 8),
    // ws -> 8083; wss -> 8084
    port: 8083,
    username: 'emqx_test',
    password: 'emqx_test',
  }

  const handleProtocolChange = (value) => {
    form.setFieldsValue({
      port: value === 'wss' ? 8084 : 8083,
    })
  }

  const onFinish = (values) => {
    const { protocol, host, clientId, port, username, password } = values
    const url = `${protocol}://${host}:${port}/mqtt`
    const options = {
      clientId,
      username,
      password,
      clean: true,
      reconnectPeriod: 1000, // ms
      connectTimeout: 30 * 1000, // ms
    }
    connect(url, options)
  }
  }
```

- Broker and port: Obtain the connection address and port information from the server deployment overview page.
- Client ID: Every MQTT client must have a unique client ID. You can call the PHP `rand` function to generate the MQTT client id randomly.
- Username and password: To establish a client connection, please make sure that you provide the correct username and password. The following image shows how to configure these credentials under 'Authentication & ACL - Authentication' on the server side.

### Connect to the broker

Once you have created the MQTT client and set up the connection options, you can connect to the broker by using the `connect` method of the MQTT client. This will establish a connection, allowing you to start sending and receiving messages.



```js
const HookMqtt = () => {
  const [client, setClient] = useState(null)
  const [isSubed, setIsSub] = useState(false)
  const [payload, setPayload] = useState({})
  const [connectStatus, setConnectStatus] = useState('Connect')

  const mqttConnect = (host, mqttOption) => {
    setConnectStatus('Connecting')
    /**
     * For more details about "mqtt.connect" method & options,
     * please refer to https://github.com/mqttjs/MQTT.js#mqttconnecturl-options
     */
    setClient(mqtt.connect(host, mqttOption))
  }

  useEffect(() => {
    if (client) {
      // https://github.com/mqttjs/MQTT.js#event-connect
      client.on('connect', () => {
        setConnectStatus('Connected')
        console.log('connection successful')
      })

      // https://github.com/mqttjs/MQTT.js#event-error
      client.on('error', (err) => {
        console.error('Connection error: ', err)
        client.end()
      })

      // https://github.com/mqttjs/MQTT.js#event-reconnect
      client.on('reconnect', () => {
        setConnectStatus('Reconnecting')
      })
    }
  }, [client])
  }
```

### Subscribe to an MQTT topic

Next, use the `subscribe` function of the returned `Client` instance to monitor the connection status. Once the connection succeeds, you can subscribe to the specified topic in the callback function.


```javascript
const mqttSub = (subscription) => {
    if (client) {
      // topic & QoS for MQTT subscribing
      const { topic, qos } = subscription
      // subscribe topic
      // https://github.com/mqttjs/MQTT.js#mqttclientsubscribetopictopic-arraytopic-object-options-callback
      client.subscribe(topic, { qos }, (error) => {
        if (error) {
          console.log('Subscribe to topics error', error)
          return
        }
        console.log(`Subscribe to topics: ${topic}`)
        setIsSub(true)
      })
    }
  }

```

Once you have subscribed to a topic, you can monitor incoming messages using the `on` function. When a new message arrives, you can obtain the corresponding topic and message within the callback function. This allows you to handle the received message and respond effectively.


```javascript
      client.on('message', (topic, message) => {
        const payload = { topic, message: message.toString() }
        setPayload(payload)
        console.log(`received message: ${message} from topic: ${topic}`)
      }
```

### Publish MQTT messages

After completing the tasks of subscribing to the topic and monitoring messages, we can proceed to write a function for publishing messages.

> Note: The message should only be published after a successful MQTT connection has been established. Therefore, we should write the function in the callback function that executes once the connection has been established.


```javascript
const mqttPublish = (context) => {
    if (client) {
      // topic, QoS & payload for publishing message
      const { topic, qos, payload } = context
      client.publish(topic, payload, { qos }, (error) => {
        if (error) {
          console.log('Publish error: ', error)
        }
      })
    }
  }
```

## Test

To run the project, use the following command.



```
npm start
```

After that, open your web browser and type `http://localhost:3000`. You will see an MQTT Server connection page, which includes the Connection module, Subscriber module, Publisher module, and Receiver module.

![reactapp.png](https://assets.emqx.com/images/706542f249c40877db5edff182d0d525.png)

Change the Protocol to "wss", then type in your Serverless MQTT broker address and login information, and click on “Connect”. It will show that you have successfully connected to the Serverless MQTT broker.

![connection.png](https://assets.emqx.com/images/7110c13815cae3cdde0280625ae9dc55.png)

Next, subscribe to the "testtopic/react" topic in the Subscriber module.

![subscriber.png](https://assets.emqx.com/images/61d508924574e8c47dcc661780e7f25d.png)

Then, publish a test message to this topic and you can see that the test message is received in the Receiver module.

![publish.png](https://assets.emqx.com/images/8e5fee2f7d45c9ffc3cc9edaf8276a0b.png)

## Summary

This blog provides a step-by-step guide on connecting to a serverless MQTT deployment in React. With these steps, we can connect to the EMQX Cloud Serverless broker in a React application using MQTT.js. For a complete code of all functions, see the project's [GitHub repository](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React).

## Join the EMQ Community

To dive deeper into EMQ, explore our[ GitHub repository](https://github.com/emqx/emqx) for the source code, join our [Discord](https://discord.com/invite/xYGf3fQnES) for discussions, and watch our [YouTube tutorials](https://www.youtube.com/@emqx) for hands-on learning. We value your feedback and contributions, so feel free to get involved and be a part of our thriving community. Stay connected and keep learning!
