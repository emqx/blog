As a small and lightweight open-source MQTT broker, Mosquitto is written in C/C++ with a single-core and single-thread architecture, can be deployed on embedded devices with limited resources to access a small number of MQTT device terminals and implements [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) and 3.1.1 protocols. Mosquitto fully supports the MQTT protocol features but is weak in clustering, which makes it difficult for the official and third-party cluster solutions to support the performance requirements of IoT for large-scale mass connectivity.

Therefore, Mosquitto is not suitable for MQTT servers for large-scale services. However, it can run on any low-power microcontroller (including embedded sensors, mobile phone devices, and embedded microprocessors) thanks to its lightweight and simplicity. It is one of the good technology options for IoT edge message access. Combined with its bridging function, Mosquitto can realize local processing and cloud-based passthrough of messages.

As a large-scale distributed MQTT message broker for IoT, EMQX can efficiently and reliably connect to massive IoT devices, and process and distribute messages and event flow data in real-time. EMQX nodes can be bridged by other types of MQTT servers and [MQTT cloud services ](https://www.emqx.com/en/cloud)for cross-platform message subscription & sending. This document will use a configuration example to demonstrate how to bridge Mosquitto MQTT messages to [EMQX](https://www.emqx.com/en/products/emqx).

![Brige Mosquitto MQTT messages](https://assets.emqx.com/images/2caae752676b2cde77bb5d532c250636.jpg)


## Scenario description

Suppose there is an EMQX server cluster `emqx1` and a Mosquitto server. We need to create a bridge on Mosquitto to forward all sensor topic `sensor/#` messages to the `emqx1` cluster and subscribe to all control topics `control/#` from EMQX.

**EMQX**

Thanks to EMQX’s standard MQTT protocol support, Mosquitto can bridge to any version of EMQX. Here, we use the [free public MQTT Broker ](https://www.emqx.com/en/mqtt/public-mqtt5-broker)provided by [EMQX Cloud](https://www.emqx.com/en/cloud) for testing:

| **Cluster** | **Address of Cluster** | **Listening Port** |
| ----------- | ---------------------- | ------------------ |
| emqx1       | `broker.emqx.io`       | 1883               |

**Mosquitto**

We used Mosquitto 2.0.14 in this article. See [Mosquitto Download](https://mosquitto.org/download/) for details on download and installation:

| **Address** | **Listening Port** |
| ----------- | ------------------ |
| 127.0.0.1   | 1883               |


## A simple example of Mosquitto MQTT bridge

To configure the Mosquitto bridge, you need to modify the `mosquitto.conf` file after installation. For each bridge, the basic items to be configured are:

- The address and port of the remote EMQX server.
- Parameters of MQTT protocol, such as protocol version, keepalive, clean session, etc. (if not configured, the default value will be used)
- Client login information required by EMQX.
- Topics of messages to be bridged.
- Configure Bridge Topic Mapping (no mapping by default).

The following is the final configuration file, and the interpretation of each part of the configuration will be explained in detail in the following sections:

```
connection emqx1
address broker.emqx.io:1883
bridge_protocol_version mqttv50
remote_clientid emqx_c
remote_username emqx_u
remote_password public
topic sensor/# out 1
topic control/# in 1
```

#### Create a new MQTT bridge

Open the `mosquitto.conf`, add an MQTT bridge configuration at the end of the configuration file, and use emqx1 as the connection name:

```
connection emqx1
```

#### Configure the address and port of the bridged remote node

```
address broker.emqx.io:1883
```

#### Configure MQTT protocol version

The MQTT protocol version used for Mosquitto bridge is 3.1.1 by default. EMQX fully supports MQTT 5.0 features and MQTT 5.0 is used for bridging here:

```
bridge_protocol_version mqttv50
```

#### Configure client ID for remote node

```
remote_clientid emqx_c
```

#### Configure user name for remote node

```
remote_username emqx_u
```

#### Configure password for remote node

```
remote_password public
```

#### Specify MQTT topics to be bridged

The configuration format of a bridge topic is `topic <topic> [[[out | in | both] qos-level] local-prefix remote-prefix]`, which defines the rules for bridge forwarding and receiving, where:

- `<topic>` specifies the topics to be bridged, and supports wildcards.
- The direction can be “out”, “in” or “both”.
  - out: to send the local topic data to the remote broker.
  - in: to subscribe to the topics of remote Broker and publish data locally.
  - both: to bridge in both directions on the same topic.
- `qos-level` is the QoS level of the bridge. If not specified, the original QoS of the forwarded message will be used.
- `local-prefix` and `remote-prefix` correspond to local and remote prefixes, which will be added to the forwarded and received message topics during topic mapping so that applications can identify the message source.

The following two bridge rules can be added for the scenario in this blog:

```
topic sensor/# out 1
topic control/# in 1
```

Upon completion of the configuration, Mosquitto shall be restarted to make the MQTT bridge configuration take effect.

## Configure EMQX Server

No parameters need to be configured when the public server is used. In practical applications, in order to successfully bridge Mosquitto MQTT messages, it is necessary to decide whether to configure the corresponding client [authentication](https://www.emqx.io/docs/en/v5.0/security/authn/authn.html) and [authorization](https://www.emqx.io/docs/en/v5.0/security/authz/authz.html) information depending on the security configuration of users’ EMQX.

## Test configuration

We can use the [MQTT client tool](https://www.emqx.com/en/blog/mqtt-client-tools) to test whether the configuration of the MQTT bridge is successful. Here [MQTT X CLI](https://mqttx.app/cli) is used, which is a powerful and easy-to-use MQTT 5.0 command line tool developed by EMQ.

### Test the out direction of the bridge

Subscribe to the `sensor/#` topic on the remote EMQX, and wait to receive the data reported by the Mosquitto bridge:

```
mqttx sub -t "sensor/#" -h broker.emqx.io
```

Publish a message on the `sensor/1/temperature` topic of the local Mosquitto. The message will be published in Mosquitto and bridged to the remote EMQX simultaneously:

```
mqttx pub -t "sensor/1/temperature" -m "37.5" -q 1
```

At this time, the remote EMQX should be able to receive the message reported by Mosquitto bridge:

```
payload: 37.5
```

### Test the in direction of the bridge

Subscribe to the `control/#` topic on the local Mosquitto. The topic will receive messages published on the remote EMQX:

```
mqttx sub -t "control/#"
```

Publish a message on the `control/t/1` topic of the remote EMQX. The message will be delivered in the EMQX cluster and bridged to the local Mosquitto at the same time:

```
mqttx pub -t "control/t/1" -m "I'm EMQX" -h broker.emqx.io
```

At this time, the message should be received on Mosquitto:

```
payload: I'm EMQX
```

In addition to Mosquitto, the [NanoMQ, ultra-lightweight MQTT message broker](https://nanomq.io) open-sourced by EMQ is also applicable to the IoT edge access scenario. We will introduce a tutorial on bridging NanoMQ messages to EMQX in follow-up blogs.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
