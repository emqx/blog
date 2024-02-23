## Introduction

React (also known as React.js or ReactJS) is an open-source, front end, JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies. React can be used as a base in the development of single-page or mobile applications. However, React is only concerned with rendering data to the DOM, and so creating React applications usually requires the use of additional libraries for state management and routing. Redux and React Router are respective examples of such libraries.[^1]

This article mainly introduces how to use [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) in the React project for implementing connect, subscribe, messaging and unsubscribe, etc., between the client and [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

## Project initialisation

Starting a new React project involves selecting the appropriate tools and frameworks. While Create React App (CRA) was popularly used for bootstrapping new React applications, the ecosystem has evolved. The official React documentation now suggests using more modern frameworks like Next.js or Remix.

In future updates, we'll guide you on using frameworks such as Next.js and Remix.js for building [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools). However, this blog will focus on guiding users through using SPA (Single Page Application) web apps.

### Creating a New React Application with Vite

For developers seeking a faster development experience, Vite offers a modern and efficient setup. Here's how to start a new project with Vite:

- For a basic React project:

  ```shell
  npm create vite@latest react-mqtt-test --template react
  # Or using Yarn
  yarn create vite react-mqtt-test --template react
  ```

- If using TypeScript:

  ```shell
  npm create vite@latest react-mqtt-test --template react-ts
  # Add necessary TypeScript libraries
  npm install --save typescript @types/node @types/react @types/react-dom @types/jest
  ```

### Traditional Method: Using Create React App

Create React App remains an option for creating single-page applications:

```shell
npx create-react-app react-mqtt-test
# For TypeScript
npx create-react-app react-mqtt-test --template typescript
```

### Install the MQTT client library

To incorporate MQTT in a React application directly, installing the [MQTT.js](https://www.emqx.com/en/blog/mqtt-js-tutorial) library is recommended:

```shell
npm install mqtt --save
# Or
yarn add mqtt
```

This method allows for flexibility in integrating MQTT into your React project, whether via CDN for quick prototypes or through npm/yarn for more stable, production-ready applications.

**Via CDN**

For projects that prefer to integrate React and MQTT.js via CDN, the following script tags can be included in your HTML:

```html
<script src="<https://unpkg.com/mqtt/dist/mqtt.min.js>"></script>
```

## Prepare an MQTT Broker

Before proceeding, please ensure you have an MQTT broker to communicate and test with. We recommend you use EMQX Cloud.

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service that can connect to a large number of IoT devices and integrate various databases and business systems. With EMQX Cloud, you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simplify the process:

- Server: `broker.emqx.io`
- TCP Port: `1883`
- WebSocket Port: `8083`
- SSL/TLS Port: `8883`
- Secure WebSocket Port: `8084`

## The use of MQTT

### Connecting to an MQTT Broker

Firstly, we define a `client` state to store the MQTT client instance, managed by the `useState` hook. The `mqttConnect` function establishes this connection and sets the connection status accordingly.

```javascript
const [client, setClient] = useState(null);
const mqttConnect = (host, mqttOption) => {
  setConnectStatus('Connecting');
  setClient(mqtt.connect(host, mqttOption));
};

useEffect(() => {
  if (client) {
    console.log(client);
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

### Subscribing to Topics

The `mqttSub` function allows the client to subscribe to one or more topics. The client can receive messages for these topics with the provided topic and Quality of Service (QoS) parameters.

```javascript
const mqttSub = (subscription) => {
  if (client) {
    const { topic, qos } = subscription;
    client.subscribe(topic, { qos }, (error) => {
      if (error) {
        console.log('Subscribe to topics error', error);
        return;
      }
      setIsSub(true);
    });
  }
};
```

### Unsubscribing

The `mqttUnSub` function is for unsubscribing from previously subscribed topics. Upon successful unsubscription, the client will no longer receive messages for that topic.

```javascript
const mqttUnSub = (subscription) => {
  if (client) {
    const { topic } = subscription;
    client.unsubscribe(topic, error => {
      if (error) {
        console.log('Unsubscribe error', error);
        return;
      }
      setIsSub(false);
    });
  }
};
```

### Publishing Messages

The `mqttPublish` function enables the client to publish messages to a specified topic. The message's Quality of Service (QoS) and retain flag can be set.

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
};
```

### Disconnecting

Finally, the `mqttDisconnect` function disconnects the client from the MQTT broker. Upon successful disconnection, related resources can be cleaned up.

```javascript
const mqttDisconnect = () => {
  if (client) {
    client.end(() => {
      setConnectStatus('Disconnected');
    });
  }
};
```

## Test

We have written the following simple browser application using React with the ability to create connections, subscribe to topics, send and receive messages, unsubscribe, and disconnect.

The complete project example code: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-React)。

![reactmqttpage.png](https://assets.emqx.com/images/d1c51195c056f3b4afb267edaeb217f0.png)

Use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) as another client to test sending and receiving messages.

![reactmqttx.png](https://assets.emqx.com/images/621ba9544ea69f9ee7b24203846d0409.png)

You can see that MQTTX can receive messages from the browser side normally, as can be seen when sending a message to the topic using MQTTX.

![reactmqtttest.png](https://assets.emqx.com/images/da008ae3544a83a3efa78266190ea364.png)

## Q&A

### Can MQTT be used in React Native mobile app development?

Yes, MQTT can be integrated with React Native for real-time communication. For detailed instructions, visit [How to Use MQTT in React Native](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react-native).

### Can MQTT only be connected through WebSocket when using React?

Yes, MQTT connections are made through WebSocket for React applications running in web browsers. This is due to browser restrictions that prevent direct TCP connections. WebSocket is a compatible solution for real-time communication, adhering to these constraints. Ensuring the broker is configured to accept WebSocket connections is essential, often requiring a specific `path` in the host URL.

### Is it possible to use MQTT hooks in React for better state management?

Yes, although there are no official MQTT hooks in React, you can develop custom hooks to encapsulate the MQTT client's logic, including connection, subscription, publication, and message handling. This method streamlines component logic, enhancing readability and reusability throughout your application.

### How to resolve "Module not found: Can't resolve 'mqtt'" in React?

Ensure MQTT.js is installed (`npm install mqtt` or `yarn add mqtt`). Verify import statements for correctness and restart your development server.

### Fixing **the** "WebSocket connection failed" error with MQTT.js in React?

Ensure the broker's URL is correct (`ws://` for unsecured, `wss://` for secured) and the port is open. For self-hosted brokers, confirm WebSocket support is enabled and accessible, considering any firewall or network restrictions.

### Can MQTT.js support mutual (two-way) SSL/TLS authentication in browser-based React applications?

No, MQTT.js cannot support mutual SSL/TLS authentication in browsers because JavaScript cannot specify client certificates for connection, and the browser controls CA configuration.

Reference: [Issue #1515 on MQTT.js GitHub](https://github.com/mqttjs/MQTT.js/issues/1515)

## React MQTT Advanced

### Advanced MQTT in React with Custom Hooks

To enhance the integration of MQTT in React applications and facilitate clean, reusable code, custom hooks can be leveraged for MQTT operations like subscribing to topics and publishing messages. Here's a concise guide on creating and using these hooks.

**Custom Hook: `useMQTTSubscribe`**

This hook abstracts the subscription logic, allowing components to subscribe to [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) effortlessly and handle incoming messages.

```javascript
function useMQTTSubscribe(client, topic, onMessage) {
  useEffect(() => {
    if (!client || !client.connected) return;
    const handleMsg = (receivedTopic, message) => {
      if (receivedTopic === topic) {
        onMessage(message.toString());
      }
    };
    client.subscribe(topic);
    client.on('message', handleMsg);
    return () => {
      client.unsubscribe(topic);
      client.off('message', handleMsg);
    };
  }, [client, topic, onMessage]);
}
```

**Custom Hook: `useMQTTPublish`**

This hook simplifies the message publishing process, ensuring messages are sent when the client is connected.

```javascript
function useMQTTPublish(client) {
  const publish = (topic, message, options = {}) => {
    if (client && client.connected) {
      client.publish(topic, message, options);
    }
  };
  return publish;
}
```

### Example Usage

#### Subscribing to a Topic

A component to display messages from a specific topic:

```javascript
const MessageDisplay = ({ client }) => {
  const [message, setMessage] = useState("");
  useMQTTSubscribe(client, "example/topic", setMessage);

  return <div>Latest message: {message}</div>;
};
```

#### Publishing to a Topic

A component that publishes user input to a topic:

```javascript
const MessageSender = ({ client }) => {
  const [input, setInput] = useState("");
  const publish = useMQTTPublish(client);

  const sendMessage = () => {
    publish("example/topic", input);
    setInput(""); // Clear input after sending
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};
```

### Integration Tips

- **Client Initialization**: Ensure the MQTT client is initialized outside the components to avoid reconnections on every render.
- **Connection State**: Manage and monitor the MQTT client's connection state to enable or disable UI elements accordingly.
- **Error Handling**: To enhance application reliability, implement error handling for publish and subscribe operations.

React applications can efficiently manage MQTT connections, subscriptions, and messages using custom hooks for MQTT operations, leading to cleaner code and improved user experiences.

## Summary

In summary, we have implemented the creation of an MQTT connection in the React project, and simulated subscribing, sending and receiving messages, unsubscribing and disconnecting between the client and MQTT broker.

In this article, we use React v16.13.1, so the Hook Component feature will be used as example code to demonstrate, or if required, you can refer to the ClassMqtt component in the full example code to use the Class Component feature for project building.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


## Resources

- [How to Use MQTT in Vue](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [How to Use MQTT in Angular](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [How to Use MQTT in Electron](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [How to Use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)




[^1]: https://en.wikipedia.org/wiki/React_(web_framework)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
