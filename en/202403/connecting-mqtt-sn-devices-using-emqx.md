## Introduction

MQTT-SN (MQTT for Sensor Networks) is an extension of the widely adopted [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), tailored for sensor networks. It addresses the unique requirements of resource-constrained devices, making it a key player in various IoT applications.

This blog aims to demystify MQTT-SN, offering insights into its architecture, comparisons with MQTT, real-world applications, and practical implementation tips.

## Understanding MQTT-SN

MQTT-SN is a Publish/Subscribe message transfer protocol designed for WSN (Wireless Sensor Networks), which is aimed to provide application layer communication standards for non-TCP/IP embedded devices (such as Zigbee and Bluetooth).

### **Advantages of MQTT-SN**

- **Compatible with MQTT protocol:** MQTT-SN communication model completely corresponds to MQTT, such as Publish, Subscribe, Hold a session, [Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message), etc. The unified model helps reduce the end-to-end design complexity.
- **Lightweight:** The protocol design is very lean in order to address the limited transmission bandwidth in the WSN networks. For example, the topic name in the PUBLISH message is replaced with a short, 2-byte Topic ID.
- **Support for sleep:** MQTT-SN protocol adds sleep logic for low power consumption scenarios. For example, after a device enters Sleep mode, all messages sent to it will be cached in the server and delivered to it after its wake-up.

### Differences between MQTT and MQTT-SN

- **Gateway discovery**. For example, an MQTT-SN gateway can periodically broadcast its information to the network, or clients can actively search for the gateway addresses. This feature is commonly used for automatic networking of MQTT-SN clients and gateways within a local area network.
- **Publish with QoS 1**: This feature is designed for basic client implementations that only support sending PUBLISH messages to a known gateway address without any additional setup, registration, or subscription. This is perfect for lightweight and simple terminal devices.
- **Will Message Update:** MQTT-SN allows for updating the topic and content of the Will Message at any time, whereas in the MQTT protocol, the Will Message can only be set during the initial connection establishment.
- **Security challenge**: MQTT-SN lacks username/password-based authentication for connections. When connecting to an MQTT-SN gateway, it only provides the Client ID and does not support username and password. This could pose security risks when deploying MQTT-SN services on public networks. Sometimes people solve this problem by using bidirectional DTLS, but it often adds complexity to design and operation.

## **Common Deployment Architecture of MQTT-SN**

![MQTT-SN Architecture](https://assets.emqx.com/images/d9615f76aa0d90157285634651fc0914.png)

<center>MQTT-SN Architecture</center>

<br>

There are three common architectures in MQTT-SN protocol deployment:

1. Client and Gateway are deployed in a same LAN (such as Zigbee) to communicate via MQTT-SN protocol, and Gateway reports data to the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) in the cloud through Ethernet and MQTT protocol.
2. MQTT Broker and MQTT-SN Gateway are integrated and deployed in the cloud. Client communicates directly with the MQTT-SN Gateway in the cloud through UDP and MQTT-SN.
3. The third deployment mode is similar to the first one with the difference that the MQTT-SN protocol is used for interaction with the MQTT-SN Gateway in the cloud.

In summary:

- The first scheme is the most typical MQTT-SN deployment, which is ideal for scenarios where terminal devices have no public network communication requirements and a gateway needs to be deployed for unified management, such as typical smart home scenario.
- The second scheme is common in scenarios where terminal devices are deployed outdoors and are directly connected to the cloud through mobile networks, such as NB-IoT, and no gateway can be deployed to handle device requests in the middle.
- The third deployment scheme is rare and is only a compromise between Scheme 1 and Scheme 2, which is used only when the server can provide MQTT-SN access services only.

## Real-World Use Cases of MQTT-SN

MQTT-SN is designed to connect sensors and embedded devices with limited network resources to meet the low-power, low-bandwidth, and low-cost requirements of the Internet of Things (IoT). Here are some practical use cases of MQTT-SN:

1. **Agriculture:** Monitoring soil moisture, temperature, and light data for precise irrigation and crop management.
2. **Industrial monitoring:** Real-time monitoring and control of equipment status on production lines to optimize production efficiency and resource utilization.
3. **Smart meters:** Used in energy monitoring systems to real-time monitor the energy consumption of electricity, water meters, gas meters, etc., helping users manage and save energy.

These examples demonstrate how MQTT-SN helps achieve data collection, communication, and intelligent control in various fields, providing a reliable communication framework for a wide range of IoT applications.

## **Accepting MQTT-SN Clients in EMQX**

EMQX MQTT Platform seamlessly supports MQTT protocol. It also efficiently manages all aspects of connection, authentication, and message transmission for non-MQTT protocols via the gateway with a unified user interface for a streamlined experience.

The MQTT-SN gateway for EMQX is implemented on top of [MQTT-SN 1.2](https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf). MQTT-SN gateway is integrated in EMQX as a component and may be deployed on the edge or in the cloud to implement the first and second deployment architectures mentioned above.

### **Enable MQTT-SN Gateway**

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

### **Test with a Client**

Test the Publish/Subscribe with the [MQTT-SN client](https://github.com/njh/mqtt-sn-tools) written in C, for example:

Client ID `mqttsn1` connects and subscribes to the topic `t/a`，

```shell
$ ./mqtt-sn-sub -i mqttsn1 -t t/a -p 1884 -d
```

Log in the MQTT-SN gateway with the Client ID `mqttsn2` , and publish the message `Hi, This is mqttsn2` to the `t/a` topic:

```
$ ./mqtt-sn-pub -i mqttsn2 -p 1884 -t t/a -m 'Hi, This is mqttsn2' -d
```

Finally, the message can be received at the `mqtt-sn-sub` side:

![mqtt-sn sub](https://assets.emqx.com/images/572f95ddaba4e4bef12850c51e8a001d.png)

## **More Advanced Feature Configuration of MQTT-SN**

### **Configure Access Authentication for Clients**

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

In this authentication method, the Client ID is transferred to the HTTP service which determines whether the client has access to the system.

### **Configure Permissions for Publish/Subscribe**

In EMQX 5.0, the Publish/Subscribe permissions for all topics are uniformly configured in **Authorization**. For example, everyone is allowed to publish/subscribe to topics starting with `mqttsn/` :

![Configure permissions for Publish/Subscribe](https://assets.emqx.com/images/ee63792138471dc8a61b198af9bd9b73.png)

<center>Configure Topic Publish/Subscribe permissions in Dashboard</center>

### **Get Connected/Disconnected Events**

The MQTT-SN gateway will publish the Connected/ Disconnected events of all devices to two dedicated topics:

- Connected event topic: `$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/connected`
- Disconnected event topic: `$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/disconnected`

For example, the content of a Connected event message will be:

```json
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

Of course, you may also use the `$event/client_connected` and `$event/client_disconnected` in the rule engine to get the Connected/ Disconnected events of the MQTT-SN gateway. For details, refer to: [Event topic available for FROM clause](https://docs.emqx.com/en/emqx/v5.0/data-integration/rule-sql-events-and-fields.html#mqtt-events)

## Summary

In conclusion, MQTT-SN stands as a powerful solution within the IoT landscape, providing a specialized protocol for sensor networks. 

For an enhanced and seamless experience with MQTT-SN, consider leveraging the capabilities of the EMQX MQTT Platform. With its comprehensive support for MQTT and efficient management of non-MQTT protocols, EMQX opens up a world of possibilities for IoT developers and enthusiasts. We hope you embrace the power of MQTT-SN with EMQX and unlock new dimensions of connectivity in the ever-evolving world of interconnected devices.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
