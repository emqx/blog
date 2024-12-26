[Vue](https://vuejs.org/), one of the most popular frameworks for building user interfaces, is highly flexible and ideal for incremental adoption. With its focus on the view layer, Vue is easy to integrate into existing projects or use with complementary libraries. When paired with modern tooling, Vue excels at creating advanced Single-Page Applications (SPAs).

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a lightweight messaging protocol tailored for IoT applications. Using the publish/subscribe model, MQTT efficiently enables one-to-many communication and decouples application logic. Its key advantages include low transmission overhead, minimal network traffic, and support for three Quality of Service (QoS) levels to cater to diverse message delivery needs. 

In this tutorial, we’ll demonstrate how to integrate MQTT into your Vue project to quickly build MQTT Web application and enable seamless real-time IoT communication, covering essential operations like establishing a connection, subscribing to topics, publishing messages, and managing disconnections.

> To create an MQTT connection in Vue 3 application using MQTT.js, please refer to [MQTT-Client-Examples/mqtt-client-Vue3.js at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue3.js) 

## Setting Up Your Vue Project with MQTT

### Initialize Your Vue Project

To create a Vue application, you can refer to the [Creating a Vue Application](https://vuejs.org/guide/quick-start.html#creating-a-vue-application) section in the Vue documentation.

Examples:

```shell
npm create vue@latest
```

### Install the MQTT Client Library

To use MQTT in your Vue project, you'll need to install the [MQTT.js library](https://github.com/mqttjs/MQTT.js). There are several ways to do this:

1. Installed from the command line, either using npm or yarn (one or the other)

   ```shell
   npm install mqtt --save
   # or yarn
   yarn add mqtt
   # or pnpm
   pnpm add mqtt
   ```

2. Import via CDN

   ```html
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
   ```

3. Download locally, then import using relative paths

   ```html
   <script src="/your/path/to/mqtt.min.js"></script>
   ```

> *The method 2 and 3 are more suitable for the project that directly introduces Vue.js.*

## Implementing MQTT in Your Vue Project

### Connect to an MQTT Broker

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX. This service was created based on the EMQX [MQTT platform](https://www.emqx.com/en/cloud). The information about broker access is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- WebSocket Port: **8083**
- WebSocket Secure Port: **8084**

Here's the code to establish a connection:

#### Connect over WebSocket Port

You can set a client ID, username, and password with the following code. The client ID should be unique.

```javascript
const connection = reactive({
  clientId: "emqx_vue3_" + Math.random().toString(16).substring(2, 8),
  username: "emqx_test",
  password: "emqx_test",
  // ...other connection options
});
const { ...options } = connection
```

You can establish a connection between the client and the MQTT broker using the following code:

```javascript
const client = mqtt.connect("ws://broker.emqx.io:8083/mqtt", options);
```

#### Connect over WebSocket Secure Port

If TLS/SSL encryption is enabled, the connection [parameter options](https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options) are the same as for establishing a connection via the WebSocket port, you just need to be careful to change the protocol to `wss` and match the correct port number.

You can establish a connection between the client and the MQTT broker using the following code:

```javascript
const client = mqtt.connect("wss://broker.emqx.io:8084/mqtt", options);
```

### Subscribe to Topics

Specify a topic and the corresponding [QoS level](https://www.emqx.com/en/blog/introduction-to-mqtt-qos) to be subscribed.

```javascript
// Topic & QoS
const subscription = ref({
  topic: "topic/mqttx",
  qos: 0 as mqtt.QoS,
});

const doSubscribe = () => {
  const { topic, qos } = subscription.value;
  client.subscribe(
    topic,
    { qos },
    (error: Error, granted: mqtt.ISubscriptionGrant[]) => {
      if (error) {
        console.log("subscribe error:", error);
        return;
      }
      console.log("subscribe successfully:", granted);
    }
  );
};
```

### Unsubscribe

You can unsubscribe using the following code, specifying the topic and corresponding QoS level to be unsubscribed.

```javascript
const doUnSubscribe = () => {
  const { topic, qos } = subscription.value;
  client.unsubscribe(topic, { qos }, (error) => {
    if (error) {
      console.log("unsubscribe error:", error);
      return;
    }
    console.log(`unsubscribed topic: ${topic}`);
  });
};
```

### Publish Messages

When publishing a message, the MQTT broker must be provided with information about the target topic and message content.

```javascript
const publish = ref({
  topic: "topic/browser",
  payload: '{ "msg": "Hello, I am browser." }',
  qos: 0 as mqtt.QoS,
});

const doPublish = () => {
  const { topic, qos, payload } = publish.value;
  client.publish(topic, payload, { qos }, (error) => {
    if (error) {
      console.log("publish error:", error);
      return;
    }
    console.log(`published message: ${payload}`);
  });
};
```

### Disconnect from the Broker

To disconnect the client from the broker, use the following code:

```javascript
const destroyConnection = () => {
  if (client.connected) {
    try {
      client.end(false, () => {
        console.log("disconnected successfully");
      });
    } catch (error) {
      console.log("disconnect error:", error);
    }
  }
};
```

## Testing the MQTT Connection in Vue

We use Vue to write the following simple browser application. This application has: create connections, subscribe topics, messaging, unsubscribe, disconnect and other functions.

The complete code for this project: [MQTT-Client-Examples/mqtt-client-Vue.js at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Vue.js).

![vueui.png](https://assets.emqx.com/images/b6563b0eb66eb51a2a02776889016a18.png)

Use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) as another client to test messaging.

![vuemqttx.png](https://assets.emqx.com/images/2013cbab1bdffcae69b817bfebb4a33f.png)

If you unsubscribe on the browser side, the browser will not receive the subsequent messages from MQTTX before MQTTX sends the second message.

## Summary

In this guide, we demonstrated how to integrate MQTT with Vue to create a real-time IoT Web Web application. From establishing a connection to managing subscriptions and messages, the combination of Vue and MQTT opens up endless possibilities for developing robust IoT solutions.

Want to dive deeper into MQTT? Check out EMQ's [Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) for more insights and advanced use cases.

## Resources

- [How to Use MQTT in React Projects](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [How to Use MQTT in Angular Projects](https://www.emqx.com/en/blog/how-to-use-mqtt-in-angular)
- [How to Use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [How to Integrate MQTT in Your Electron Project](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
