React (also known as React.js or ReactJS) is an open-source, front end, JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies. React can be used as a base in the development of single-page or mobile applications. However, React is only concerned with rendering data to the DOM, and so creating React applications usually requires the use of additional libraries for state management and routing. Redux and React Router are respective examples of such libraries.[^1]

This article mainly introduces how to use [MQTT](https://mqtt.org/) in the React project for implementing connect, subscribe, messaging and unsubscribe, etc., between the client and MQTT broker.



## Project initialisation

### New project

Reference link: [https://legacy.reactjs.org/docs/getting-started.html](https://legacy.reactjs.org/docs/getting-started.html)

- Creating new React applications with `Create React App`

  ```shell
  npx create-react-app react-mqtt-test
  ```

  If you need to use TypeScript, simply add the --template typescript parameter at the end of the command line

  ```shell
  npx create-react-app react-mqtt-test --template typescript
  ```

  Then add the TypeScript type library required in the React project

  ```shell
  npm install --save typescript @types/node @types/react @types/react-dom @types/jest
  # or
  yarn add typescript @types/node @types/react @types/react-dom @types/jest
  ```

  The use of TypeScript will not be the focus of the examples in this article, but if you wish to use it, you can add TypeScript features after referring to the creation example and the full code examples.

- Import via CDN

  ```html
  <script crossorigin src="https://unpkg.com/react@16/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"></script>
  ```

### Install the MQTT client library

As React is a JavaScript library, it is possible to use [MQTT.js](https://www.emqx.com/en/blog/mqtt-js-tutorial) as the MQTT client library.

> The following methods 2, 3 are more suitable for referencing projects created by React via CDN links.

1. Installation via the command line, either using the npm or yarn command (one or the other)

   ```shell
   npm install mqtt --save
   # or
   yarn add mqtt
   ```

2. Import via CDN

   ```html
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
   ```

3. Download to the local and then import using the relative path

   ```html
   <script src="/your/path/to/mqtt.min.js"></script>
   ```



## The use of MQTT

### Connect the MQTT broker

This article will use [the free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) which is provided by EMQX. This service is based on EMQX's [MQTT IoT cloud platform](https://www.emqx.com/en/cloud) to create. The server access information is as follows.

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

### Connect

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

### Subscribe

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

### Unsubscribe

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

### Publish

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

### Disconnect

```javascript
const mqttDisconnect = () => {
  if (client) {
    client.end(() => {
      setConnectStatus('Connect');
    });
  }
}
```

## Test

We have written the following simple browser application using React with the ability to create connections, subscribe to topics, send and receive messages, unsubscribe, and disconnect.

The complete project example code: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React)。

![reactmqttpage.png](https://assets.emqx.com/images/d1c51195c056f3b4afb267edaeb217f0.png)

Use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) as another client to test sending and receiving messages.

![reactmqttx.png](https://assets.emqx.com/images/621ba9544ea69f9ee7b24203846d0409.png)

You can see that MQTTX can receive messages from the browser side normally, as can be seen when sending a message to the topic using MQTTX.

![reactmqtttest.png](https://assets.emqx.com/images/da008ae3544a83a3efa78266190ea364.png)



## Summary

In summary, we have implemented the creation of an MQTT connection in the React project, and simulated subscribing, sending and receiving messages, unsubscribing and disconnecting between the client and MQTT broker.

In this article, we use React v16.13.1, so the Hook Component feature will be used as example code to demonstrate, or if required, you can refer to the ClassMqtt component in the full example code to use the Class Component feature for project building.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


[^1]: https://en.wikipedia.org/wiki/React_(web_framework)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
