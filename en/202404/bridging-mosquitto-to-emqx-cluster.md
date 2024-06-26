## Introduction to Mosquitto

[Mosquitto](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives), an open-source MQTT server, is designed to be lightweight and compact, coded in C/C++, featuring a single-core, single-threaded architecture. It caters to deployment in resource-constrained embedded devices and connects to a limited number of MQTT devices. It fully embraces both [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) and version 3.1.1 protocols.

Despite its strengths, Mosquitto lacks robust clustering capabilities. Neither official nor third-party clustering solutions meet the demands of large-scale IoT connectivity. Consequently, it faces limitations:

- **Limited Scalability:** While its lightweight design facilitates easy deployment, it hinders cluster scalability, making horizontal scaling and business expansion challenging.
- **Performance Constraints:** Mosquitto's capacity for simultaneous client connections on a single instance impacts its performance, particularly in large-scale or highly concurrent scenarios.

Hence, Mosquitto isn't suitable for scale-out MQTT services. However, its lightweight nature makes it ideal for edge scenarios where device access is limited, and performance is critical:

- **Effortless Deployment:** Mosquitto's lightweight design simplifies deployment and configuration, enabling quick setup on edge devices.
- **Flexibility:** It can adapt to diverse edge environments such as industrial setups, smart homes, and agricultural IoT, delivering reliable MQTT communication services.
- **Local Control and Decision Making:** For devices requiring low-latency, high-bandwidth real-time control, Mosquitto can operate as an [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), facilitating local decision making and ensuring swift responsiveness.
- **LAN Communication:** In scenarios necessitating LAN communication between edge devices, Mosquitto serves as an MQTT broker, managing device-to-device communication and facilitating data exchange and collaboration. It additionally facilitates essential messaging interactions with the cloud through the Mosquitto Bridge on behalf of the edge devices.

## Introduction to Mosquitto Bridge

Mosquitto offers the **Mosquitto Bridge** feature for MQTT message bridging, facilitating the forwarding of messages between MQTT Brokers. This capability supports cross-network or cross-region messaging, catering to diverse scenarios. Additionally, Mosquitto Bridge addresses challenges in large-scale or highly concurrent environments by transferring only essential messages between Mosquitto Brokers, thereby alleviating performance burdens and simplifying complexities.

- **Inter-Network Communication:** In organizational setups, where multiple MQTT Brokers operate across different network domains, Mosquitto Bridge fosters communication and collaboration by linking these brokers. This allows seamless messaging between departments or businesses, promoting inter-network connectivity.
- **Edge-to-Cloud Integration:** In IoT ecosystems, communication between edge devices and cloud platforms is pivotal. Leveraging Mosquitto Bridge facilitates the connection between edge MQTT Brokers and cloud-based MQTT Brokers, enabling data transfer from edge devices to cloud environments for processing.

This blog elucidates the utilization of Mosquitto Bridge to establish connectivity with a cloud-based MQTT cluster, enabling interaction between edge [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) and the cloud MQTT Broker. EMQX, the most scalable distributed MQTT broker, serves as the designated cloud MQTT Broker. EMQX efficiently handles connections from numerous IoT devices, ensuring real-time processing and distribution of messages and event streams. Moreover, EMQX nodes can be bridged with other MQTT Servers and MQTT Cloud Services, facilitating cross-platform message subscription and delivery.

## An Example Mosquitto Bridge Application Scenario

Imagine a scenario where numerous sensors and actuators are deployed within a large factory, overseeing the production process and equipment operations. These devices must communicate seamlessly in real-time to ensure the efficient functioning of production. Concurrently, plant managers require real-time monitoring of the plant's status and the ability to remotely manage equipment.

In such a scenario, Mosquitto can be deployed as an edge MQTT Broker within the plant's internal LAN. Devices connect to Mosquitto to communicate in real-time via [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), with Mosquitto overseeing message management between devices and interfacing with the cloud. Within the plant, devices can interact swiftly and reliably through Mosquitto, bypassing the cloud, thereby reducing latency and enhancing real-time performance. Simultaneously, managers can monitor equipment status in real-time using Mosquitto's publish-subscribe mechanism and issue commands to control equipment operations.

However, in certain instances, managers may need to access specific data or issue commands from the cloud, such as remotely monitoring plant status or adjusting equipment parameters. In such cases, the Mosquitto Bridge facilitates message bridging from the LAN to the cloud-based MQTT Broker for communication with the cloud.

Consider a setup with a cluster of EMQX servers as the cloud control platform and a Mosquitto server serving as the edge MQTT message broker. Establishing a bridge on Mosquitto enables the transmission of sensor-reported data to EMQX on the cloud and forwards control commands issued by the cloud console to sensor devices at the edge.

- Sensors publish messages in the `sensor/#` topic for data reporting.
- Sensors subscribe to the `control/#` topic to receive control messages.

**Cloud-Side Control Platform - EMQX**

Due to EMQX's comprehensive support for the MQTT protocol, Mosquitto can seamlessly bridge with any version of EMQX. In this instance, we utilize the complimentary [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) offered by EMQX Enterprise for testing purposes.

| Cluster Address  | Listening Port |
| :--------------- | :------------- |
| `broker.emqx.io` | `1883`         |

**Edge-Side MQTT Message Broker - Mosquitto**

Utilize a locally hosted Mosquitto as an edge broker instance. The version is 2.0.18. Refer to [Mosquitto Download](https://mosquitto.org/download/) for comprehensive instructions on downloading and installing the software.

| Address   | Listening Port |
| :-------- | :------------- |
| 127.0.0.1 | 1883           |

## Mosquitto MQTT Bridge Tutorial

### Setting Up Mosquitto

To configure Mosquitto Bridge, you can either modify the mosquitto.conf file post-installation or specify the configuration file path when starting Mosquitto. Detailed information can be found in [mosquitto.conf(5)](https://mosquitto.org/man/mosquitto-conf-5.html).

For Mosquitto Bridge, essential configurations for each bridge include:

- Remote EMQX server's address and port
- MQTT protocol parameters like protocol version, keepalive, clean_session, etc. (defaults are used if not configured)
- Client login credentials required by EMQX
- Topics to be bridged
- Mapping of bridged topics (no mapping by default)

The following are the configuration elements within the bridging section, with detailed explanations for each configuration below.

```
connection emqx1
address broker.emqx.io:1883
bridge_protocol_version mqttv50
remote_clientid emqx_c_5f9072a9
remote_username emqx_u_5f9072a9
remote_password public
topic sensor/# out 1  sen-local/ sen-remote/
topic control/# in 1 cmd-local/ cmd-remote/
```

#### Setting Up a New MQTT Bridge

Begin by opening the mosquitto.conf file and appending an MQTT bridge configuration at the end of the file. Use "emqx1" as the connection identifier:

```
connection emqx1
```

#### Specifying the Address and Port of the Remote Bridge Node

Configure the address of the remote MQTT Broker in the following format: host[:port]. By default, it uses MQTT TCP port 1883 if [:port] is not specified.

```
address broker.emqx.io:1883
```

#### Adjusting the MQTT Protocol Version

The default MQTT protocol version for Mosquitto Bridge is 3.1.1. However, since EMQX fully supports MQTT 5.0 features, we opt to use MQTT 5.0 for bridging in this configuration:

```
bridge_protocol_version mqttv50
```

#### Setting Up the Remote Node Client ID

To prevent duplication with other clients, append a random string as a suffix to the client ID.

```
remote_clientid emqx_c_5f9072a9
```

#### Specifying the Remote Node Username

```
remote_username emqx_u_5f9072a9
```

#### Providing the Remote Node Password

```
remote_password public
```

#### Specifying the Bridged MQTT Topic

The configuration format for a bridged topic follows the pattern:
`topic <topic> [[[out | in | both] qos-level] local-prefix remote-prefix]`, which dictates the bridging rules for forwarding and receiving messages. Here's a breakdown:

- `<topic>` designates the topic to be bridged, supporting wildcards.
- The direction can be `out`, `in`, or `both`:
  - `out`: sends local topic data to the remote Broker.
  - `in`: subscribes to the remote Broker's topic and publishes the data locally.
  - `both`: facilitates two-way bridging on the same topic.
- `qos-level` indicates the QoS level of the bridge. If unspecified, the original QoS of the forwarded message is used.
- `local-prefix` and `remote-prefix` correspond to local and remote prefixes. These are appended to the forwarding and receiving topics, aiding in message source recognition.

For this scenario, two bridging rules are added:

> Note: Utilize local-prefix and remote-prefix to prevent receiving messages from other users on a public server. Additionally, mosquitto uses string splicing to make changes to topics, so it is recommended to use a topic separator in the prefix to differentiate the topic hierarchy.

```
topic sensor/# out 1  sen-local/ sen-remote/
topic control/# in 1 cmd-local/ cmd-remote/
```

Upon completing the configuration, initiate Mosquitto and utilize the -c option alongside a specific configuration file to activate the MQTT bridge configuration.

```shell
$ mosquitto -c mosquitto.conf
1711697768: mosquitto version 2.0.18 starting
1711697768: Config loaded from mosquitto.conf.
1711697768: Starting in local only mode. Connections will only be possible from clients running on this machine.
1711697768: Create a configuration file which defines a listener to allow remote access.
1711697768: For more details see https://mosquitto.org/documentation/authentication-methods/
1711697768: Opening ipv4 listen socket on port 1883.
1711697768: Opening ipv6 listen socket on port 1883.
1711697768: Connecting bridge emqx_brokre (broker.emqx.io:1883)
1711697768: mosquitto version 2.0.18 running
...
```

### Configuring the EMQX Server

No parameters require configuration when utilizing the public server. However, for successful Mosquitto MQTT message bridging, configuring the appropriate client authentication and authorization information is necessary, based on the user's EMQX security settings.

### Testing Configuration

We can employ [MQTT Client Tools](https://www.emqx.com/en/blog/mqtt-client-tools) to assess the success of the MQTT bridge configuration. In this demonstration, we utilize [MQTTX CLI](https://mqttx.app/cli), a robust and user-friendly MQTT command-line tool developed by EMQ.

#### Testing the Outbound Direction of the Bridge

Two MQTT clients are employed — one connected to the local Mosquitto service (`127.0.0.1:1883`) and the other linked to the EMQX cluster in the cloud (`broker.emqx.io:1883`).

The subscribing client subscribes to the `sen-remote/sensor/#` topic on the remote EMQX, awaiting receipt of data relayed by the Mosquitto Bridge:

```shell
$ mqttx-cli sub -u 'suber' -t 'sen-remote/sensor/#' -h broker.emqx.io -p 1883  
[3/29/2024] [5:02:30 PM] › …  Connecting...
[3/29/2024] [5:02:34 PM] › ✔  Connected
[3/29/2024] [5:02:34 PM] › …  Subscribing to sen-remote/sensor/#...
[3/29/2024] [5:02:34 PM] › ✔  Subscribed to sen-remote/sensor/#
...
```

Another client, connected to the local Mosquitto, publishes a message on the
`sen-local/sensor/temperature` topic. This message is then transmitted through Mosquitto and bridged to the remote EMQX:

```shell
$ mqttx-cli pub -t "sen-local/sensor/temperature" -m '{"temperature": 36.8}' -q 1 -h 127.0.0.1 -p 1883
[3/29/2024] [5:03:09 PM] › …  Connecting...
[3/29/2024] [5:03:09 PM] › ✔  Connected
[3/29/2024] [5:03:09 PM] › …  Message publishing...
[3/29/2024] [5:03:09 PM] › ✔  Message published
```

Following these actions, clients connected to the cloud-based EMQX should receive messages relayed by the Mosquitto Bridge:

```shell
...
[3/29/2024] [5:03:09 PM] › payload: {"temperature": 36.8}
```

#### Testing the Inbound Direction of the Bridge

To evaluate the inbound direction of the bridge, subscribe to the `cmd-local/control/#` topic on the local Mosquitto. This subscription will receive messages originating from the remote EMQX:

```shell
$ mqttx-cli sub -u 'suber' -t 'cmd-local/control/#' -h 127.0.0.1 -p 1883
[3/29/2024] [5:03:43 PM] › …  Connecting...
[3/29/2024] [5:03:43 PM] › ✔  Connected
[3/29/2024] [5:03:43 PM] › …  Subscribing to cmd-local/control/#...
[3/29/2024] [5:03:43 PM] › ✔  Subscribed to cmd-local/control/#
...
```

Next, publish a message on the `cmd-remote/control/cmd` topic of the remote EMQX. This message will be delivered to the EMQX cluster and bridged to Mosquitto locally simultaneously:

```shell
$ mqttx-cli pub -t "cmd-remote/control/cmd" -m '{"cmd": "refresh"}' -q 1 -h broker.emqx.io -p 1883
[3/29/2024] [5:03:45 PM] › …  Connecting...
[3/29/2024] [5:03:45 PM] › ✔  Connected
[3/29/2024] [5:03:45 PM] › …  Message publishing...
[3/29/2024] [5:03:46 PM] › ✔  Message published
```

Following this, the client "suber" connected to the local Mosquitto service should receive the message:

```shell
...
[3/29/2024] [5:03:46 PM] › payload: {"cmd": "refresh"}
```

## Conclusion

This blog outlines the utilization of Mosquitto Bridge for bridging MQTT messages from the edge to a cloud-based MQTT cluster. Through the integration of Mosquitto Bridge with EMQX, users can facilitate message communication between edge MQTT servers and the cloud, while also harnessing the capabilities offered by EMQX, such as rule engine, data persistence, large file transfer, [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic), and more. This integration introduces greater convenience and innovation to the development of IoT applications.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
