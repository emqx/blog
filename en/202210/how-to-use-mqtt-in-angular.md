[Angular](https://angular.io/) is a development platform built on top of TypeScript. It consists of a component-based framework for building scalable Web applications; a set of perfectly integrated libraries covering routing, form management, client-server communication and other functions; and a set of development tools to help users develop, build, test, and update codes.

**MQTT is a lightweight IoT message transfer protocol** based on publish/subscribe mode, providing one-to-many message distribution and application decoupling with small transmission consumption, which can minimize network traffic. At the same time, it can meet various delivery requirements thanks to its three QoS (Quality of Service) levels for messages.

This article will introduce how to use [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) in Angular projects to connect, subscribe, send/receive messages, unsubscribe and perform other functions between clients and [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

## Project Initialization

### Create a new project

The reference is as follows: [Create an Angular project with the Angular CLI](https://angular.io/guide/setup-local#install-the-angular-cli)

Example:

```
ng new my-app
```

### Installation of MQTT client library

The library used in this case is [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/), which isn’t just a wrapper around MQTT.js for angular >= 2. It uses observables and takes care of subscription handling and message routing. [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/) is well suited for applications with many components and many subscribers.

To install [ngx-mqtt](https://sclausen.github.io/ngx-mqtt/) via the command line, you can use the npm or yarn command (either one)

```
npm install ngx-mqtt --save 
yarn add ngx-mqtt 
```

## Use of MQTT

### Connecting to MQTT Broker

We use the [free public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX in this article, which is built on top of the [MQTT cloud service - EMQX Cloud](https://www.emqx.com/en/cloud). EMQX is a large-scale distributed IoT MQTT message broker that can efficiently and reliably connect massive IoT devices, process and distribute messages and event flow data in real-time, and help customers build business-critical IoT platforms and applications.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/b4cff1e553053873a87c4fa8713b99bc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Practical Guide to MQTT Broker Selection
    </div>
    <div class="mb-32">
      Download this practical guide and learn what to consider when choosing an MQTT broker.
    </div>
    <a href="https://www.emqx.com/en/resources/a-practical-guide-to-mqtt-broker-selection?utm_campaign=embedded-a-practical-guide-to-mqtt-broker-selection&from=blog-how-to-use-mqtt-in-angular" class="button is-gradient">Get the eBook →</a>
  </div>
</section>

The server access information is as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- WebSocket Port: **8083**

Key codes for connection:

```
import {
 IMqttMessage,
 IMqttServiceOptions,
 MqttService,
 IPublishOptions,
} from 'ngx-mqtt';
import { IClientSubscribeOptions } from 'mqtt-browser';
import { Subscription } from 'rxjs';

@Component({
 selector: 'app-root',
 templateUrl: './app.component.html',
 styleUrls: ['./app.component.scss'],
})
export class AppComponent {
 constructor(private _mqttService: MqttService) {
   this.client = this._mqttService;
}
 private curSubscription: Subscription | undefined;
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
};
 publish = {
   topic: 'topic/browser',
   qos: 0,
   payload: '{ "msg": "Hello, I am browser." }',
};
 receiveNews = '';
 qosList = [
  { label: 0, value: 0 },
  { label: 1, value: 1 },
  { label: 2, value: 2 },
];
 client: MqttService | undefined;
 isConnection = false;
 subscribeSuccess = false;

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
     console.log('mqtt.connect error', error);
  }
   this.client?.onConnect.subscribe(() => {
     this.isConnection = true
     console.log('Connection succeeded!');
  });
   this.client?.onError.subscribe((error: any) => {
     this.isConnection = false
     console.log('Connection failed', error);
  });
   this.client?.onMessage.subscribe((packet: any) => {
     this.receiveNews = this.receiveNews.concat(packet.payload.toString())
     console.log(`Received message ${packet.payload.toString()} from topic ${packet.topic}`)
  })
}
}
```

### Subscribe to topics

Upon connecting to the MQTT Broker successfully, call the `subscribe` method of the current MQTT instance and pass in the Topic and QoS parameters for the successful subscription.

```
doSubscribe() {
 const { topic, qos } = this.subscription
 this.curSubscription = this.client?.observe(topic, { qos } as IClientSubscribeOptions).subscribe((message: IMqttMessage) => {
   this.subscribeSuccess = true
   console.log('Subscribe to topics res', message.payload.toString())
})
}
```

### Unsubscribe

The `unsubscribe` method can release the resources held by the subscription.

```
doUnSubscribe() {
 this.curSubscription?.unsubscribe()
 this.subscribeSuccess = false
}
```

### Message publishing

The `usafePublish` publishes messages on topics with optional options, such as QoS and Retain, as shown below.

```
doPublish() {
 const { topic, qos, payload } = this.publish
 console.log(this.publish)
 this.client?.unsafePublish(topic, payload, { qos } as IPublishOptions)
}
```

### Disconnect

The `disconnect` will disconnect the MQTT client. The parameter `true` is passed in to force a disconnection from the MQTT client.

```
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

## Test

We create the following simple browser application with Angular, which has the following functions: Establish a connection, Subscribe to topics, Send & receive messages, Unsubscribe, Disconnect, and so on. For the complete code, see: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Angular.js) 

![Angular MQTTT APP](https://assets.emqx.com/images/5fbd7272ef81de85e2cd498762d52b63.png)

Use [MQTT 5.0 client tool - MQTTX](https://mqttx.app/) as another client to test message sending & receiving.

![MQTT Client](https://assets.emqx.com/images/1d5c27483ba0a80800ea3f43bc4e04ed.png)

Before MQTTX sends a second message, unsubscribe at the browser side, and the browser side will not receive subsequent messages sent by MQTTX.

## Summary

We have successfully created an MQTT connection in an Angular project and simulated the scenarios of subscription, message sending and receiving, unsubscription, and disconnection between the client and the MQTT.

As one of the three mainstream front-end frameworks, Angular can be used both on the browser and the mobile side. Various interesting applications can be developed by combining MQTT protocol and [MQTT cloud service](https://www.emqx.com/en/cloud), such as the chat system for customer service or management system for real-time monitoring of IoT device information.

## Resources

- [How to Use MQTT in Vue](https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue)
- [How to Use MQTT in React](https://www.emqx.com/en/blog/how-to-use-mqtt-in-react)
- [How to Use MQTT in Electron](https://www.emqx.com/en/blog/how-to-use-mqtt-in-electron)
- [How to Use MQTT in Node.js](https://www.emqx.com/en/blog/how-to-use-mqtt-in-nodejs)
- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
