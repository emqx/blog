## Introduction

[Angular](https://angular.io/) is a development platform built on TypeScript. It features a component-based framework designed for creating scalable web applications, along with a comprehensive set of integrated libraries that cover routing, form management, client-server communication, and other essential functions. Additionally, Angular provides development tools to assist users in developing, building, testing, and updating code.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight message transfer protocol for the Internet of Things (IoT), based on a publish/subscribe model. It enables one-to-many message distribution and application decoupling while minimizing transmission costs, thereby reducing network traffic. MQTT also accommodates various delivery requirements through its three Quality of Service (QoS) levels for messages.

This article will explain how to implement the MQTT protocol in Angular projects, covering how to connect, subscribe, send and receive messages, unsubscribe, and perform other functions between clients and the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

## Setting Up Your Angular Project with MQTT

### Create a New Project

You can refer to two different documentation sources:

1. [Create an Angular project with the Angular CLI](https://v17.angular.io/guide/setup-local#install-the-angular-cli) - This is the **archived documentation for Angular v17**
2. [angular.dev](https://angular.dev/tools/cli/setup-local#before-you-start) - This is the **current version** of Angular documentation

Install the Angular CLI:

```shell
npm install -g @angular/cli
```

Create a new workspace and initial application:

```shell
ng new my-app
```

Navigate to the project directory:

```shell
cd my-app
```

Now you're ready to start development!

### Install the MQTT Client Library

The library used in this case is [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/), which isn’t just a wrapper around MQTT.js for angular >= 2. It uses observables for efficient subscription handling and message routing, making it ideal for Angular applications.

Install it using npm or yarn command:

```shell
npm install ngx-mqtt --save 
yarn add ngx-mqtt
```

## Implementing MQTT in Angular

### Connecting to an MQTT Broker

We use the [free public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX in this article, which is built on the EMQX MQTT Platform. EMQX is a large-scale distributed IoT MQTT message broker that can efficiently and reliably connect massive IoT devices, process and distribute messages and event flow data in real-time, and help customers build business-critical IoT platforms and applications.

The server access information is as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- WebSocket Port: **8083**

Key codes for connection:

```javascript
import type { IMqttServiceOptions, MqttService } from 'ngx-mqtt'
import type { Subscription } from 'rxjs'
import { IClientSubscribeOptions } from 'mqtt-browser'
import { IMqttMessage, IPublishOptions } from 'ngx-mqtt'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  constructor(private _mqttService: MqttService) {
    this.client = this._mqttService
  }

  private curSubscription: Subscription | undefined
  connection = {
    hostname: 'broker.emqx.io',
    port: 8083,
    path: '/mqtt',
    clean: true, // Retain session
    connectTimeout: 4000, // Timeout period
    reconnectPeriod: 4000, // Reconnect period
    // Authentication information
    clientId: 'mqttx_597046f4',
    username: 'emqx_test',
    password: 'emqx_test',
    protocol: 'ws',
  }

  subscription = {
    topic: 'topic/mqttx',
    qos: 0,
  }

  publish = {
    topic: 'topic/browser',
    qos: 0,
    payload: '{ "msg": "Hello, I am browser." }',
  }

  receiveNews = ''
  qosList = [
    { label: 0, value: 0 },
    { label: 1, value: 1 },
    { label: 2, value: 2 },
  ]

  client: MqttService | undefined
  isConnection = false
  subscribeSuccess = false

  // Create a connection
  createConnection() {
    // Connection string, which allows the protocol to specify the connection method to be used
    // ws Unencrypted WebSocket connection
    // wss Encrypted WebSocket connection
    // mqtt Unencrypted TCP connection
    // mqtts Encrypted TCP connection
    try {
      this.client?.connect(this.connection as IMqttServiceOptions)
    } catch (error) {
      console.log('mqtt.connect error', error)
    }
    this.client?.onConnect.subscribe(() => {
      this.isConnection = true
      console.log('Connection succeeded!')
    })
    this.client?.onError.subscribe((error: any) => {
      this.isConnection = false
      console.log('Connection failed', error)
    })
    this.client?.onMessage.subscribe((packet: any) => {
      this.receiveNews = this.receiveNews.concat(packet.payload.toString())
      console.log(`Received message ${packet.payload.toString()} from topic ${packet.topic}`)
    })
  }
}
```

### Subscribing to Topics

Upon connecting to the MQTT Broker successfully, call the `subscribe` method of the current MQTT instance and pass in the Topic and QoS parameters for the successful subscription.

```javascript
doSubscribe() {
  const { topic, qos } = this.subscription
  this.curSubscription = this.client?.observe(topic, { qos } as IClientSubscribeOptions).subscribe((message: IMqttMessage) => {
    this.subscribeSuccess = true
    console.log('Subscribe to topics res', message.payload.toString())
  })
}
```

### Unsubscribing from Topics

The `unsubscribe` method can release the resources held by the subscription.

```javascript
doUnSubscribe() {
 this.curSubscription?.unsubscribe()
 this.subscribeSuccess = false
}
```

### Publishing Messages 

The `usafePublish` publishes messages on topics with optional options, such as QoS and Retain, as shown below.

```javascript
doPublish() {
 const { topic, qos, payload } = this.publish
 console.log(this.publish)
 this.client?.unsafePublish(topic, payload, { qos } as IPublishOptions)
}
```

### Disconnecting from MQTT Broker

The `disconnect` will disconnect the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools). The parameter `true` is passed in to force a disconnection from the MQTT client.

```javascript
destroyConnection() {
  try {
    this.client?.disconnect(true)
    this.isConnection = false
    console.log('Successfully disconnected!')
  } catch (error: any) {
    console.log('Disconnect failed', error.toString())
  }
}
```

## Testing the Angular MQTT Application

We create the following simple browser application with Angular, which has the following functions: Establish a connection, Subscribe to topics, Send & receive messages, Unsubscribe, Disconnect, and so on.

### Code Examples Reference

For Angular v17 and above code example, see: [Angular v17 MQTT Example](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js/Angular17)

For previous Angular versions code example, see: [Angular MQTT Example](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js)

![Angular MQTTT APP](https://assets.emqx.com/images/5fbd7272ef81de85e2cd498762d52b63.png)

Use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) as another client to test message sending & receiving.

![MQTT Client](https://assets.emqx.com/images/1d5c27483ba0a80800ea3f43bc4e04ed.png)

Before MQTTX sends a second message, unsubscribe at the browser side, and the browser side will not receive subsequent messages sent by MQTTX.

## Summary

This guide illustrated how to integrate MQTT into an Angular application, enabling functions like connecting to an MQTT Broker, subscribing to topics, and publishing messages. Combining Angular with MQTT opens up exciting possibilities, such as developing real-time monitoring systems for IoT devices or chat systems for customer service.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
