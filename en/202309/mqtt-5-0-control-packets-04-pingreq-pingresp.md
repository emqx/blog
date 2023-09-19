Welcome to the fourth article of the [MQTT 5.0 Packet Series](https://www.emqx.com/en/blog/Introduction-to-mqtt-control-packets). In the previous article, we introduced the [SUBSCRIBE and UNSUBSCRIBE packets](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-03-subscribe-unsubscribe) in MQTT 5.0. Now, we will introduce the control packets used to maintain the connection: PINGREQ and PINGRESP.

In addition to the control packets used for connecting, publishing, and subscribing, MQTT also has a type of packet used to simulate heartbeats between the client and server to maintain the connection. They are PINGREQ and PINGRESP packets, which we often call heartbeat packets.

The client periodically sends PINGREQ packets to the server, which lets the server know that the connection is good and the client is still active. For each PINGREQ packet received, the server will reply with a PINGRESP packet, so the client can also know that the connection is good and the server is still active.

## Sample Packets

We use [MQTTX CLI](https://mqttx.app/) to initiate a client connection to the [Public MQTT Server](http://broker.emqx.io/). We do not publish messages or subscribe to topics, but we can still see MQTT packets periodically appearing between the client and server in [Wireshark](https://www.wireshark.org/). These packets are the PINGREQ and PINGRESP.

The following command will create a client connection with a Keep Alive of 5 seconds, which allows us to see the client sending the PINGREQ message as soon as possible.

```
 mqttx conn --hostname broker.emqx.io --mqtt-version 5 --keepalive 5
```

We will find that PINGREQ and PINGRESP packets are always only 2 bytes in size, and their contents seem to never change:

```
# PINGREQ c0 00 # PINGRESP d0 00
```

This is because these two packets have a very simple structure.

## PINGREQ & PINGRESP Packet Structure

The only difference between PINGREQ and PINGRESP packets is the Packet Type field in the Fixed Header. The Packet Type for PINGREQ is 12 (0x0C), while for PINGRESP it is 13 (0x0D).

The value of the Remaining Length field that follows is always 0 because neither PINGREQ nor PINGRESP packets contain the **Variable Header** or **Payload**.

![01pingreqandpingresp.png](https://assets.emqx.com/images/74dec0938b2cef37c488d4003c9a3027.png)

This structure minimizes the size of PINGREQ and PINGRESP packets, so sending them does not take up much bandwidth.

## Conclusion

PINGREQ and PINGRESP are the simplest packets in MQTT, and their contents are fixed. The only thing we can change is to affect the frequency of the client sending PINGREQ packets through the **Keep Alive** option during connection.

If the server does not receive any control packet from the client within 1.5 times the Keep Alive time, it will consider that the client is inactive or the network is abnormal and disconnected. In the packet example in this article, we set Keep Alive to 5 seconds when connecting, so the timeout for the server is 7.5 seconds.

For the client, if it does not receive the PINRESP packet returned by the server within a period after sending the PINGREQ packet, it should disconnect. The length of this time mainly depends on the client's expectation of network delay and the specific implementation of each client SDK.

We have learned more about MQTT packets. In the upcoming article, we will introduce the DISCONNECT packet used when disconnecting.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
