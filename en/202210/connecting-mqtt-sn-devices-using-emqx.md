MQTT-SN (**MQTT for Sensor Networks**) is a Publish/Subscribe message transfer protocol designed for WSN (Wireless Sensor Networks), which is aimed to provide application layer communication standards for non-TCP/IP embedded devices (such as Zigbee and Bluetooth).

The large-scale distributed IoT [MQTT message broker EMQX](https://www.emqx.io) can fully support the MQTT protocol and handle all non-MQTT protocol connection, authentication and message sending & receiving for all non-MQTT protocols through the gateway, and provide a unified user layer interface for them. This article will introduce how to access MQTT-SN protocol devices to EMQX, and secure the device access through authentication and authorization.

## **What are the advantages of MQTT-SN?**

- **Compatible with MQTT protocol:** MQTT-SN communication model completely corresponds to MQTT, such as Publish, Subscribe, Hold a session, [Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message), etc. The unified model helps reduce the end-to-end design complexity.
- **Lightweight:** The protocol design is very lean in order to address the limited transmission bandwidth in the WSN networks. For example, the topic name in the PUBLISH message is replaced with a short, 2-byte Topic ID.
- **Support for sleep:** MQTT-SN protocol adds sleep logic for low power consumption scenarios. For example, after a device enters Sleep mode, all messages sent to it will be cached in the server and delivered to it after its wake-up.

## **Common deployment architecture of MQTT-SN**

![img](https://assets.emqx.com/images/b65bb745702ab0c90fe34bb522a50a00.png)

<center>MQTT-SN Architecture</center>

1. Client and Gateway are deployed in a same LAN (such as Zigbee) to communicate via MQTT-SN protocol, and Gateway reports data to the MQTT broker in the cloud through Ethernet and MQTT protocol.
2. MQTT Broker and MQTT-SN Gateway are integrated and deployed in the cloud. Client communicates directly with the MQTT-SN Gateway in the cloud through UDP and MQTT-SN.
3. The third deployment mode is similar to the first one with the difference that the MQTT-SN protocol is used for interaction with the MQTT-SN Gateway in the cloud.

In comparison:

- The first scheme is the most typical MQTT-SN deployment, which is ideal for scenarios where terminal devices have no public network communication requirements and a gateway needs to be deployed for unified management, such as typical smart home scenario.
- The second scheme is common in scenarios where terminal devices are deployed outdoors and are directly connected to the cloud through mobile networks, such as NB-IoT, and no gateway can be deployed to handle device requests in the middle.
- The third deployment scheme is rare and is only a compromise between Scheme 1 and Scheme 2, which is used only when the server can provide MQTT-SN access services only.

Therefore, MQTT-SN is mainly used in application scenarios with short distance, limited bandwidth, low power consumption, such as smart cities, smart furniture, water, electricity and gas meters, etc.

## **Access to MQTT-SN protocol with EMQX**

The MQTT-SN gateway for EMQX is implemented on top of [MQTT-SN 1.2](https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf). MQTT-SN gateway is integrated in EMQX as a component and may be deployed on the edge or in the cloud to implement the first and second deployment architectures mentioned above.

### **Enable MQTT-SN gateway**

In EMQX 5.0, the MQTT-SN gateway can be enabled through Dashboard, HTTP-API, or configuration files.

For example, enable and configure the MQTT-SN gateway listening on UDP port 1884:

```
gateway.mqttsn {

mountpoint = "mqttsn/"

listeners.udp.default {
  bind = 1884
  max_connections = 10240000
  max_conn_rate = 1000
}
}
```

### **Test with a client**

Test the Publish/Subscribe with the [MQTT-SN client](https://github.com/njh/mqtt-sn-tools) written in C, for example:

Client ID `mqttsn1` connects and subscribes to the topic `t/a`，

```
$ ./mqtt-sn-sub -i mqttsn1 -t t/a -p 1884 -d
```

Log in the MQTT-SN gateway with the Client ID `mqttsn2` , and publish the message `Hi, This is mqttsn2` to the `t/a` topic:

```
$ ./mqtt-sn-pub -i mqttsn2 -p 1884 -t t/a -m 'Hi, This is mqttsn2' -d
```

Finally, the message can be received at the `mqtt-sn-sub` side:

![mqtt-sn sub](https://assets.emqx.com/images/572f95ddaba4e4bef12850c51e8a001d.png)

## **More advanced features configuration**

### **Configure access authentication for clients**

As the Connect message of MQTT-SN v1.2 protocol only defines the Client ID, with no Username and Password, MQTT-SN gateway currently supports HTTP Server-based authentication only.

For example, add an HTTP authentication for the MQTT-SN gateway through the configuration file:

```
gateway.mqttsn {
authentication {
  enable = true
  backend = "http"
  mechanism = "password_based"
  method = "post"
  connect_timeout = "5s"
  enable_pipelining = 100
  url = "<http://127.0.0.1:8080">
  headers {
    "content-type" = "application/json"
  }
  body {
    clientid = "${clientid}"
  }
  pool_size = 8
  request_timeout = "5s"
  ssl.enable = false
}
}
```

In this authentication method, the Client ID is transferred to the HTTP service which determines whether the client has access right to the system.

### **Configure permissions for Publish/Subscribe**

In EMQX 5.0, the Publish/Subscribe permissions for all topics are uniformly configured in **Authorization**. For example, everyone is allowed to publish/subscribe to topics starting with `mqttsn/` :

![Configure permissions for Publish/Subscribe](https://assets.emqx.com/images/ee63792138471dc8a61b198af9bd9b73.png)

Configure Topic Publish/Subscribe permissions in Dashboard

### **Get Connected/Disconnected events**

The MQTT-SN gateway will publish the Connected/ Disconnected events of all devices to two dedicated topics:

- Connected event topic: `$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/connected`
- Disconnected event topic: `$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/disconnected`

For example, the content of a Connected event message will be:

```
{
 "clientid": "abc",
 "username": "undefined",
 "ts": 1660285421750,
 "sockport": 1884,
 "protocol": "mqtt-sn",
 "proto_ver": "1.2",
 "proto_name": "MQTT-SN",
 "keepalive": 10,
 "ipaddress": "127.0.0.1",
 "expiry_interval": 7200000,
 "connected_at": 1660285421750,
 "clean_start": false
}
```

Of course, you may also use the `$event/client_connected` and `$event/client_disconnected` in the rule engine to get the Connected/ Disconnected events of the MQTT-SN gateway. For details, refer to: [Event topic available for FROM clause](https://www.emqx.io/docs/en/v5.0/data-integration/rule-sql-events-and-fields.html#mqtt-events)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
