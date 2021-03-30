

## Overview

When the client disconnects, a will message is sent to the relevant subscriber. Will Messages will be sent when:

- I / O error or network failure occurred on the server;
- The client loses contact during a defined heartbeat period;
- The client closes the network connection before sending offline packets;
- The server closes the network connection before receiving the offline packet.

Will messages are usually specified when the client is connected. As shown below, it is set during the connection by calling the `setWill` method of the` MqttConnectOptions` instance. Any client who subscribes to the topic below will receive the will message.

```
//method1 
MqttConnectOptions.setWill(MqttTopic topic, byte[] payload, int qos, boolean retained)
//method2 
MqttConnectOptions.setWill(java.lang.String topic, byte[] payload, int qos, boolean retained)
```

## Usage scenarios

When client A connects, the will message is set to "offline" and client B subscribes to this will topic. When A disconnects abnormally, client B will receive this will message of "offline"  to know that client A is offline.

### Connect Flag packet field

| Bit    | 7              | 6             | 5           | 4        | 2         | 1           | 0        |
| ------ | -------------- | ------------- | ----------- | -------- | --------- | ----------- | -------- |
|        | User Name Flag | Password Flag | Will Retain | Will QoS | Will Flag | Clean Start | Reserved |
| byte 8 | X              | X             | X           | X        | X         | X           | X        |

The will message is not sent after the client calls the disconnect method normally.

## Will flag function

In short,  it is the last will (also known as the Testament) that the client has defined in advance and left when it is disconnected abnormally. This will is a topic and a corresponding message pre-defined by the client, which is attached to the variable packet header of CONNECT.  In case of abnormal connection of the client, the server actively publishes this message.

When the  bit of Will Flag is 1, Will QoS and Will Retain will be read. At this time, the specific contents of Will Topic and Will Message will appear in the message body, otherwise the Will QoS and Will Retain  will be ignored.

When the Will Flag bit is 0, Will Qos and Will Retain are invalid.

## Command line example

Here is an example of Will Message:

1. Sub side ClientID = sub predefined will message:

   ```
   mosquitto_sub --will-topic test --will-payload die --will-qos 2 -t topic -i sub -h 192.168.1.1
   ```

2. clientid = alive subscribes to the will topic at 192.168.1.1 (EMQ server)

   ```
   mosquitto_sub -t test -i alive -q 2 -h 192.168.1.1
   ```

3. Abnormally disconnect the sub end from the server end (EMQ server), and the pub end receives the will message.

## Advanced usage scenarios

Here's how to use Retained messages with Will messages.

1. The will message of client A is set to "offline", and the topic of the will is set to  `A/status` that is the same as the topic of a normal sending status;
2. When client A is connected, send the "Online" Retained message to the topic `A/status`. When other clients subscribe to the topic` A/status`, they obtain the Retained message as "online";
3. When client A disconnects abnormally, the system automatically sends an "offline" message to the topic `A/status`. Other clients that subscribe to this topic will immediately receive an" offline "message; if the will message is set  Retained, and when a new client subscribing to the `A/status` topic comes online, the message obtained is“ offline ”.




