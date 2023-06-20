## Why we need Keep Alive

The MQTT protocol is hosted on top of the TCP protocol, which is connection-oriented, and provides a stable and orderly flow of bytes between two connected parties. However, in some cases, TCP can have half-connection problems. A half-connection is a connection that has been disconnected or not established on one side, while the connection on the other side is still maintained. In this case, the half-connected party may continuously send data, which obviously never reaches the other side. To avoid black holes in communication caused by half-connections, the MQTT protocol provides a Keep Alive mechanism that allows the client and MQTT server to determine whether there is a half-connection problem, and close the corresponding connection.

## Mechanism and use of MQTT Keep Alive

### At Connection

When an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) creates a connection to the [MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker), the Keep Alive mechanism can be enabled between the communicating parties by setting the Keep Alive variable header field in the connection request protocol packet to a non-zero value. Keep Alive is an integer from 0 to 65535, representing the maximum time in seconds allowed to elapse between MQTT protocol packets sent by the client.

When the broker receives a connection request from a client, it checks the value of the Keep Alive field in the variable header. When there is a value, the broker will enable the Keep Alive mechanism.

### MQTT 5.0 Server Keep Alive

In the [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) standard, the concept of Server Keep Alive was also introduced, allowing the broker to choose to accept the Keep Alive value carried in the client request, or to override it, depending on its implementation and other factors. If the broker chooses to override this value, it needs to set the new value in the Server Keep Alive field of the Connection Acknowledgement Packet (CONNACK), and the client needs to use this value to override its own previous Keep Alive value when it reads it in the CONNACK.

### The Keep Alive Process

**Client process**

After the connection is established, the client needs to ensure that the interval between any two MQTT protocol packets it sends does not exceed the Keep Alive value. If the client is idle and has no packets to send, it can send PINGREQ protocol packets, instead.

When the client sends a PINGREQ packet, the broker must return a PINGRESP packet. If the client does not receive a PINGRESP packet from the server within a reliable time, it means that there is a half-connection, the broker is offline, or there is a network failure, and the client should close the connection.

**Broker process**

After the connection is established, if the broker does not receive any packets from the client within 1.5 times the Keep Alive time, it will assume that there is a problem with the connection to the client, and the broker will disconnect from the client.

If the broker receives a PINGREQ protocol packet from the client, it needs to reply with a PINGRESP protocol packet for confirmation.

**Client takeover mechanism**

When there is a half-connection within the broker, and when the corresponding client initiates a reconnection or a new connection, the broker will start the client takeover mechanism: it closes the old half-connection and establishes a new connection with the client.

This mechanism ensures that the client will not be prevented from reconnecting due to a half-connection problem.

## Keep Alive & Will Message

Keep Alive is typically used in conjunction with Will Message, which allow the device to promptly notify other clients in the event of an unexpected offline event.

As shown in the figure, when this client connects, Keep Alive is set to 5 seconds and a will message is set. If the server does not receive any packets from the client within 7.5 seconds (1.5 times the Keep Alive), it will send a will message with a payload of 'offline' to the 'last_will' topic.

![MQTT Will Message](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png)

For more details on MQTT Will Message, please check the blog [Use of MQTT Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message).

## How to use Keep Alive in EMQX

In [EMQX](https://www.emqx.com/en/products/emqx), you can customize the behavior of the Server Keep Alive mechanism through the configuration file. The relevant field is as follows:

**zone.external.server_keepalive**

| Type    | Default |
| ------- | ------- |
| integer | -       |

If this value is not set, the Keep Alive time will be determined by the client at the time it creates a connection.

If this value is set, the broker forces the Server Keep Alive mechanism to be enabled for all connections in that zone and will use that value to override the value in the client connection request.

**zone.external.keepalive_backoff**

| Type  | Optional Value | Default |
| ----- | -------------- | ------- |
| float | > 0.5          | 0.75    |


The MQTT protocol requires the broker to assume that the client is disconnected when it does not receive any protocol packets from the client within 1.5 times the Keep Alive time.

In EMQX, we introduced the keepalive backoff factor and exposed this factor through the configuration file in order to allow users to more flexibly control the Keep Alive behavior on the broker side.

After introducing the backoff factor, EMQX calculates the maximum timeout using the following formula:

```
Keepalive * backoff * 2
```

The default value of backoff is 0.75. Therefore, the behavior of EMQX will be fully compliant with the MQTT standard when the user does not modify this configuration.

Refer to the [EMQX configuration documentation](https://www.emqx.io/docs/en/v4.3/configuration/configuration.html) for more information.

> **Note: Setting Keep Alive for WebSocket connections**
>
> EMQX supports client access via WebSockets. When a client initiates a connection using WebSockets, it only needs to set the Keep Alive value in the client connection parameters. Refer to [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket).



## Summary

This article introduces the Keep Alive mechanism in the MQTT protocol and how to use it in EMQX. You can use this feature to ensure the stability of [MQTT connections](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) and build more robust IoT applications.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
