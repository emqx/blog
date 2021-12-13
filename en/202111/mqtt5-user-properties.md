MQTT v5 has many new features. We will try to show these features in an easy-to-understand way and discuss the impact of these features on developers. So far, we have discussed these [New Features of MQTT v5](https://www.emqx.com/en/mqtt/mqtt5). Today we will continue to discuss: **User Properties**.

## What are User Properties？

User Properties are the user-defined properties that allow users to add their metadata to MQTT messages and transmit additional user-defined information to expand more application scenarios.

User Properties consist of a user-defined UTF-8 key/value pair array configured in the message property field. As long as the maximum message size is not exceeded, an unlimited number of user properties can be used to add metadata to the MQTT message and transfer information among publishers, MQTT Brokers, and subscribers.

If you are familiar with HTTP protocol, this function is very similar to the concept of HTTP Header. User Properties allow users to extend the [MQTT protocol](https://www.emqx.com/en/mqtt) effectively and can appear in all messages and responses. Because User Properties are defined by the user, they are only meaningful to the user's action.

## Why do we need User Properties？

User Properties are used to solve the poor scalability of MQTT 3. When there is the possibility that any information can be transmitted in the message, it ensures that the user can extend the functionality of the standard protocol to meet his own needs.

For message types with different options or configurations, User Properties can be sent between the client and the MQTT Broker or between the clients. For example, when User Properties are configured in the connected client, they can only be received on the MQTT Broker but not on the client. If User Properties is configured when sending a message, they can be received by other clients. The following two types of User Property configuration are commonly used.

### User Properties of the connected client

When the client initiates a connection with the MQTT Broker, the Broker can predefine some required metadata information that can be used, which is User Properties. When the connection is successful, the MQTT service can get the relevant information sent by the connection for use. Therefore, the User Properties of the connected client depend on the MQTT Broker.

### User Properties during message publishing

User Properties during message publishing may be more commonly used because they can transfer metadata information between the clients. For example, you can add some common information when publishing messages, such as message number, timestamp, file, client information, and routing information.

In addition to the above-mentioned User Properties settings, you can also configure User Properties when subscribing to the Topic, unsubscribing or disconnecting.

## Use of User Properties

### File transfer

User Properties of [MQTT 5](https://www.emqx.com/en/mqtt/mqtt5) can be extended for file transfer instead of putting data in the payload of the message body and using key-value pairs for User Properties in the previous MQTT 3. This also means that the file can be kept as binary because the metadata of the file is in the user properties. For example:

```json
{
  "filename": "test.txt",
  "content": "xxxx"
}
```

### Resource analysis

When the client connects to the MQTT Broker, different clients and platforms or systems from different vendors transmit message data in different ways. There may be structural differences in the message data format, and some clients are distributed in different regions. For example, the message format sent by the device in region A is JSON, and that sent by the device in region B is XML. At this time, the server may need to judge and compare one by one after receiving the message to find an appropriate parser for data analysis.

To improve efficiency and reduce computing load, we can use the User Properties function to add data format information and geographic information. When the server receives the message, it can use the metadata in the User Properties to analyze the data. Moreover, when the client subscription of area A receives the client message from area B, it can also quickly know which area the specific message comes from so that the message is traceable.

```json
{
  "region": "A",
  "type": "JSON"
}
```

![MQTT Resource analysis](https://static.emqx.net/images/c2f4e34d2ff553f12a81826382846366.png)

### Message routing

We can also use User Properties to do application-level routing. As mentioned above, there are different systems and platforms, and there are different devices in each area. Multiple systems may receive messages from the same device. Some systems need to display data in real-time, and another system may store these data in time series. Therefore the MQTT server can determine whether to distribute the message to the system storing the message or to the system presenting the data by the User Properties configured in the reported message.

```json
{
  "type": "real-time",
  "timestamp": 1636620444
}
```

![MQTT Message routing](https://static.emqx.net/images/39dfdc8de0b0251bab3697d72169dfef.png)

## How to configure in MQTT client

Let's take an example of programming with JavaScript, using the [MQTT.js](https://github.com/mqttjs/MQTT.js) client. We can first specify the version of MQTT as MQTT 5.0 when connecting to the client.

### Connect

When connecting, we set the User Properties in the properties options and add the type and region properties. After the connection is successful, the MQTT Broker will receive this user-defined message.

```javascript
// connect options
const OPTIONS = {
  clientId: 'mqtt_test',
  clean: true,
  connectTimeout: 4000,
  username: 'emqx',
  password: 'public',
  reconnectPeriod: 1000,
  protocolVersion: 5,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}
const client = mqtt.connect('mqtt://broker.emqx.io', OPTIONS)
```

### Publish messages

After the connection is successful, we subscribe and choose to publish the message and set the User Properties in the configuration of publishing messages. Then, we monitor the message reception. In the publish function, we configure the User Properties. We print the packet to see the User Properties configured just now in the function that listens to and receives the message.

```javascript
client.publish(topic, 'nodejs mqtt test', {
  qos: 0,
  retain: false,
  properties: {
    userProperties: {
      region: 'A',
      type: 'JSON',
    },
  },
}, (error) => {
  if (error) {
    console.error(error)
  }
})
client.on('message', (topic, payload, packet) => {
  console.log('packet:', packet)
  console.log('Received Message:', topic, payload.toString())
})
```

At this point, we can see that the User Properties configured just before publishing has been printed and output in the console.

 

For other clients, we will first support the user-defined configuration function for User Properties in subsequent versions of the cross-platform [MQTT 5.0 desktop client tool - MQTT X](https://mqttx.app/zh), which facilitates users to quickly test some new features of MQTT 5.0. Please look forward to it!
