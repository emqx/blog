MQTT is a lightweight messaging protocol widely used to connect devices, applications, and services across the Internet of Things (IoT). 

This guide introduces MQTT fundamentals, explains its architecture and messaging workflow, and walks you through a hands-on tutorial. Whether you are new to MQTT or looking to build a stronger foundation, this guide is your go-to resource for mastering MQTT and elevating your IoT projects.

## What Is MQTT?



MQTT (Message Queuing Telemetry Transport) is a lightweight, client-server messaging protocol that uses a publish/subscribe model. It is designed for efficient communication between devices and applications, particularly in environments with limited bandwidth, constrained resources, or unreliable network connections.

The [OASIS MQTT specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) describes MQTT as a lightweight, open, simple protocol designed to be easy to implement. It is widely used in IoT systems, where sensors, actuators, gateways, and cloud applications need to exchange data efficiently.

## Why Use MQTT for IoT?



MQTT is a popular choice for IoT messaging because it offers several useful characteristics.

- **Lightweight communication.** MQTT has a minimum fixed header of just two bytes. Its compact control packets help reduce protocol overhead, making it suitable for constrained devices and bandwidth-limited networks. Actual bandwidth savings depend on the message payload, connection reuse, protocol configuration, and the alternative being compared.
- **Reliable message delivery.** MQTT provides three QoS levels to accommodate different delivery requirements. It also supports persistent sessions and queued messages for eligible clients, subject to broker configuration, message expiry, storage limits, and session settings.
- **Secure communication.** MQTT can run over TLS to protect data in transit. Brokers can also enforce client [authentication](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication) and topic-level [authorization](https://www.emqx.com/en/blog/authorization-in-mqtt-using-acls-to-control-access-to-mqtt-messaging) through credentials, certificates, and other supported mechanisms.
- **Decoupled, bidirectional communication.** A client can publish messages and subscribe to topics at the same time. Publishers do not need to know which clients will receive their messages, and subscribers do not need to know which clients produce them.
- **Support for intermittent connectivity.** MQTT keep-alive mechanisms help detect unresponsive connections. With an appropriately configured persistent session, a broker can retain subscription state and queue eligible messages while a client is disconnected.
- **Scalable device connectivity.** [MQTT's publish-subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) decouples message producers from consumers, making it easier to add devices and applications without creating direct connections between every participant. A scalable MQTT broker can support large numbers of concurrent client connections and high message throughput.
- **Broad programming-language support.** MQTT client libraries are available for languages including Python, Java, JavaScript, C, C++, Go, and many others. This makes it easier to integrate devices, backend services, and applications built with different technologies. Our [MQTT Client Programming](https://www.emqx.com/en/blog/category/mqtt-programming) blog series shows how to use MQTT in various programming languages.

MQTT is also widely used in [industrial IoT (IIoT)](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges). The [*Eclipse Foundation's 2024 IoT & Embedded Developer Survey*](https://newsroom.eclipse.org/news/announcements/eclipse-foundation-unveils-2024-iot-embedded-developer-survey-results) reported that MQTT was the preferred IIoT communication protocol among surveyed developers, with 56% adoption.

## MQTT Architecture: How Does MQTT Work?



MQTT uses a client-server architecture based on the publish/subscribe messaging pattern. MQTT clients connect to an MQTT broker. Publishers send messages to topics, and the broker routes those messages to clients with matching subscriptions.

### MQTT Client



An MQTT client is any device or application that implements the MQTT protocol and connects to a broker.

Examples include:

- A temperature sensor publishing measurements.
- A mobile application subscribing to device status updates.
- A gateway forwarding industrial telemetry.
- A backend service publishing commands to connected devices.
- An MQTT testing tool used to publish and subscribe to messages.

A client can publish messages, subscribe to topics, or perform both roles.

### MQTT Broker



An MQTT broker is the central component that manages client connections and message delivery. It handles connection requests, subscriptions, unsubscriptions, and message routing.

When a broker receives a published message, it checks the topic against active subscriptions and forwards the message to matching subscribers according to the applicable QoS and session settings.

The broker also manages MQTT features such as retained messages, persistent sessions, and Last Will messages. Its capacity and deployment architecture influence how many client connections and messages an IoT system can support.

For a deeper explanation, see [MQTT Broker: How It Works, Popular Options, and Quickstart](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker).

### MQTT Topics



An MQTT topic is a UTF-8 string used to organize messages and determine which subscribers receive them. Topics are hierarchical and use the forward slash (`/`) as a level separator.

For example:

- `chat/room/1`
- `sensor/10/temperature`
- `factory/line1/machine01/status`

> In the example above, the term preceding the first forward slash represents the first level of the overall topic. While it is technically possible for this (or any other) level to be empty — meaning a topic level with a length of zero — doing so is not recommended. In other words, the use of topic names similar to the following is discouraged:
>
> - `/some/topic/first/level/empty`
> - `//some/topic/second/level/empty`
>
> Doing so can lead to the appearance of unusual or unexpected topic names when utilizing features such as topic mounting or shared subscriptions. In the following example, `name_a` serves as the group name, while the first level of the actual topic is empty.
>
> - `$share/name_a//real/topic`

MQTT supports two wildcard characters for subscriptions:

- `+` matches exactly one topic level. For example, `sensor/+/temperature` matches `sensor/1/temperature` and `sensor/2/temperature`.
- `#` matches multiple topic levels. For example, `sensor/#` matches `sensor/1/temperature` and `sensor/2/humidity`.

Wildcards are used in subscriptions, not when publishing messages.

For scalable IoT deployments, use a consistent topic hierarchy that reflects the structure of your devices and data. For example:

```
telemetry/{tenant_id}/{site_id}/{device_type}/{device_id}/{metric}
```

A well-designed topic structure makes it easier to organize data, manage subscriptions, and apply access control.

For more details, see [MQTT Topics and Wildcards: A Beginner's Guide](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).

### The Publish/Subscribe Pattern



The publish/subscribe pattern separates message producers from message consumers.

For example, a temperature sensor publishes a reading to `sensor/1/temperature`. The MQTT broker checks its subscriptions and forwards the message to connected clients whose topic filters match that topic and whose subscription and delivery conditions allow the message to be delivered.

The sensor does not need to know which applications receive the reading. Likewise, subscribers do not need to establish direct connections to individual sensors.

This decoupling simplifies application integration and allows new publishers and subscribers to be added without redesigning the entire communication system.

![Diagram showing MQTT architecture: A temperature sensor publishing data to an MQTT Broker, which forwards it to a subscriber](https://assets.emqx.com/images/a6baf485733448bc9730f47bf1f41135.png)

A typical MQTT message flow works as follows:

1. **Connect to the broker.** An MQTT client establishes a connection to the broker, typically over TCP/IP. TLS can be used to secure the connection. The client may also provide authentication credentials and specify session settings.
2. **Subscribe to topics.** A client sends a subscription request to receive messages published to one or more topics. The subscription includes a requested QoS level.
3. **Publish messages.** A publisher sends a message to a topic on the broker. The message contains a payload and relevant MQTT properties, such as QoS and the Retain flag.
4. **Route messages.** The broker matches the published topic against subscribers' topic filters and forwards the message to eligible subscribers.
5. **Manage delivery and sessions.** The broker follows the applicable QoS rules and, when a persistent session is configured, can store eligible messages for a disconnected client until it reconnects or the messages expire.

This architecture allows devices and applications to exchange data without maintaining direct connections with one another.

## MQTT Quality of Service (QoS)



MQTT defines three Quality of Service levels that control how message delivery is handled between the sender and receiver in the MQTT protocol exchange.

### QoS 0: At Most Once



The sender transmits the message without waiting for a delivery acknowledgment. The message may be lost if a connection or delivery failure occurs.

QoS 0 is appropriate when low overhead is more important than guaranteed delivery, such as for frequent telemetry updates where the next reading can replace a missed one.

### QoS 1: At Least Once



The sender retransmits the message until it receives the required acknowledgment. This provides at-least-once delivery, meaning the receiver may receive duplicates.

Applications using QoS 1 should account for possible duplicate messages, particularly when processing events or performing operations that must not be applied twice.

### QoS 2: Exactly Once



QoS 2 uses a four-step protocol exchange to provide exactly-once delivery within the relevant MQTT protocol interaction.

It introduces more protocol overhead and state management than QoS 0 or QoS 1. It does not, by itself, guarantee exactly-once execution of an arbitrary downstream business operation or database transaction.

| QoS   | Delivery semantics                      | Relative overhead | Typical use                                        |
| :---- | :-------------------------------------- | :---------------- | :------------------------------------------------- |
| QoS 0 | At most once                            | Lowest            | Frequent telemetry                                 |
| QoS 1 | At least once; duplicates possible      | Moderate          | Important status updates and events                |
| QoS 2 | Exactly once at the MQTT protocol level | Highest           | Applications requiring stronger delivery semantics |

The QoS configured by a publisher is not the only factor affecting delivery. Subscription QoS, broker behavior, connection state, and the protocol exchange determine the effective delivery QoS.

For more details, see [MQTT QoS 0, 1, 2 Explained: A Quickstart Guide](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

## Getting Started with MQTT: A Hands-On Tutorial



This tutorial shows you how to connect MQTT clients, subscribe to topics, publish messages, and explore several core MQTT features.

You'll need an MQTT broker and an MQTT client.

### Step 1: Set up an MQTT Broker



For a quick test, you can use a public MQTT broker. For production applications, use a properly configured broker with appropriate authentication, authorization, TLS, monitoring, and capacity planning.

Here, we offer two options:

**Fully Managed Cloud Service**: **EMQX Serverless**

[EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is a managed MQTT service with usage-based pricing and a monthly free quota. It is suitable for prototyping and applications that benefit from managed infrastructure.

It can start in minutes and runs in 17 regions across AWS, Google Cloud, and Microsoft Azure.

**Free Public MQTT Broker Built on EMQX**

For this tutorial, you can also use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX:

- Broker address: `broker.emqx.io`
- MQTT over TCP: `1883`
- MQTT over WebSocket: `8083`

### Step 2: Prepare an MQTT Client



In this tutorial, we will use [MQTTX Web Client](https://mqttx.app/web-client), which runs directly in a browser. [MQTTX](https://mqttx.app/) is a cross-platform MQTT client tool that also provides [desktop](https://mqttx.app/) and [command-line](https://mqttx.app/cli) versions. It supports MQTT 5.0 and provides an interface for creating connections, managing subscriptions, and publishing messages.

![image.png](https://assets.emqx.com/images/205d84fc148ee248016906422f336b8b.png)

 

### Step 3: Connect to the Broker



1. Open MQTTX Web Client.

2. Create a new connection.

   ![image.png](https://assets.emqx.com/images/72be59bb858c0342708344294d616532.png)

3. Enter a connection name, such as `Simple Demo`.

   ![image.png](https://assets.emqx.com/images/2caefdd431e3f5f6fbaa798b38196e94.png)

4. Set the broker host to `broker.emqx.io`.

5. Set the port to `8083` and select the WebSocket transport.

6. Select a supported MQTT version and configure any required connection parameters.

7. Click **Connect**.

When the connection succeeds, MQTTX will show the connected status.

![image.png](https://assets.emqx.com/images/e41fbff1b1013de778d0fa4c9a22883f.png)

To learn more about MQTT connection parameters, please check out our blog post: [How to Set Parameters When Establishing an MQTT Connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).

### Step 4: Subscribe to a Wildcard Topic



In the `Simple Demo` connection, create a subscription using this topic filter: `sensor/+/temperature`. Set the subscription QoS to 0 for this demonstration.

![image.png](https://assets.emqx.com/images/81a011316cbcd14da56b569dd07615be.png)

The subscription will match topics such as `sensor/1/temperature` and `sensor/2/temperature`.

### Step 5: Publish MQTT Messages



Create two additional MQTTX connections named `Sensor 1` and `Sensor 2`. Connect both to the same broker.

![image.png](https://assets.emqx.com/images/2610e40207f719f25c6632cea8371314.png)

From `Sensor 1`, publish the following message:

**Topic:** `sensor/1/temperature`

**Payload:**

```
{
  "msg": "17.2"
}
```

![image.png](https://assets.emqx.com/images/cc3c98dfa2951f99493972393e4f4baa.png)

From `Sensor 2`, publish:

**Topic:** `sensor/2/temperature`

**Payload:**

```
{
  "msg": "18.2"
}
```

Return to the `Simple Demo` connection. Because its subscription matches both topics, it should receive both messages.

![image.png](https://assets.emqx.com/images/4d87ed815121b19697e9485919f614ef.png)

 

This example demonstrates how MQTT topics and wildcard subscriptions allow multiple devices to publish data that can be consumed by a single application.

### Alternative: Publish an MQTT Message with Python



If you prefer code, you can use the Paho MQTT Python client.

Install the library:

```
pip install paho-mqtt
```

The following example connects to the public broker over TCP and publishes a message:

```python
import paho.mqtt.client as mqtt

# Initialize client and connect
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Python_Client_Demo")
client.connect("broker.emqx.io", 1883, 60)

# Publish a test payload
client.publish("sensor/1/temperature", '{"msg": "17.2"}')
print("Message published successfully!")

```

This is a minimal demonstration, not a production-ready client. It assumes the broker is reachable and does not implement authentication, TLS, application-level validation, or automatic reconnection.

For production applications, configure the appropriate security settings and handle connection and publication failures explicitly. 

For additional examples, explore the [popular MQTT client libraries & SDKs](https://www.emqx.com/en/mqtt-client-sdk).

## Essential MQTT Features in Practice



Beyond basic publishing and subscribing, MQTT offers several features that help applications handle device state, intermittent connectivity, and connection failures.

### Retained Messages



A retained message is a message that the broker stores as the latest retained publication for a topic. When a new subscription matches that topic, the broker can deliver the retained message to the subscriber.

For example, a device can publish its current status to `device/1/status` with the Retain flag enabled. A dashboard subscribing later can receive the latest retained status without waiting for the device to publish again.

To test this in MQTTX:

1. Connect `Sensor 1` to the broker.

2. Publish a message to `retained_message` with the **Retain** option enabled.

3. Publish a second retained message to the same topic.

   ![image.png](https://assets.emqx.com/images/3c30f965b0af343613fb0e649159d57a.png)

4. Subscribe to `retained_message` from `Simple Demo`.

The subscriber should receive the latest retained message for that topic, subject to the broker's retained-message configuration.

![image.png](https://assets.emqx.com/images/0ad3efbf5b901b58875bc8634e147e8d.png)

A retained message stores the latest retained value for a topic, not a complete history of all previous publications. Publishing a zero-byte retained payload removes the retained message for that topic.

Learn more in [The Beginner's Guide to MQTT Retained Messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message).

### Persistent Sessions and Clean Start



MQTT sessions determine whether subscription state and eligible undelivered messages can be retained when a client disconnects.

In MQTT 3.1.1, the Clean Session flag controls whether the client starts a new session or resumes an existing one.

- **Clean Session = 1:** The client requests a new session. Session state is not preserved after disconnection.
- **Clean Session = 0:** The client requests to resume an existing session or establish a session that can be resumed later. The Client ID must be reused, and the broker must support the required session behavior.

In MQTT 5.0, the session model uses two properties:

- **Clean Start:** Determines whether to start a new session or resume an existing one.
- **Session Expiry Interval:** Specifies how long the session should be retained after the network connection ends.

A persistent session does not mean every message published while a client is offline will be delivered. Message delivery depends on subscription QoS, publication QoS, session configuration, message expiry, broker limits, and other conditions.

#### Demonstrating Persistent Sessions



1. Create an MQTT 3.1.1 connection named `MQTT_V311`.

2. Set Clean Session to `false`.

   ![image.png](https://assets.emqx.com/images/6c12c8ebb7ef43ef7b0c9617204e2de9.png)

3. Subscribe to `clean_session_false` at QoS 1.

   ![image.png](https://assets.emqx.com/images/e24334092b2615ac3cb5c312b518f876.png)

4. Disconnect the client.

   ![image.png](https://assets.emqx.com/images/445a16eae79b9f899b9f6c32f5648e10.png)

5. Connect another client, such as `MQTT_V311_Publish`, to the same broker.

6. Publish several QoS 1 messages to `clean_session_false`.

   ![image.png](https://assets.emqx.com/images/7399778ee8aa8f876c4871859702ad2f.png)

7. Reconnect `MQTT_V311` using the same Client ID.

   ![image.png](https://assets.emqx.com/images/9155d8916ae6ea1cf0824ceee185ecb0.png)

If the broker preserves the session and queues the eligible messages, the client should receive the queued messages after reconnecting.

For more information, see [MQTT Persistent Session and Clean Session Explained](https://www.emqx.com/en/blog/mqtt-session).

### Will Message



The Will Message feature allows an MQTT client to specify a message that the broker will publish if the client's network connection is closed unexpectedly.

The client configures the Will Topic, Will Message (payload), Will QoS, and Will Retain settings in the CONNECT packet. Once the broker accepts the connection, it stores the Will Message and publishes it to the specified Topic when the connection is closed under conditions defined by the MQTT protocol.

Will Messages are commonly used to report device availability. For example, a device can configure a Will Message with the payload `offline`, allowing other clients to be notified if the device unexpectedly disconnects.



**Try it in MQTTX:**

1. Create a connection named `Last Will`.

2. Set **Keep Alive** to 5 seconds for this demonstration.

3. Configure the following Will settings:

   - Will Topic: `last_will`

   - Will QoS: `1`

   - Will Retain: enabled

   - Will Payload: `offline`

     ![image.png](https://assets.emqx.com/images/6e741daf0f2bc5a44f13167abfce536d.png)

4. Connect to the broker.

5. Simulate an unexpected disconnection by disabling the network connection or otherwise interrupting the client without sending a normal MQTT DISCONNECT packet.

6. Wait for the broker to detect the disconnection.

7. Connect the `Simple Demo` client and subscribe to `last_will`.

   ![image.png](https://assets.emqx.com/images/0f800e6f6cb99b82d3d88993cfb61444.png)

The subscriber should receive the Will message when the broker publishes it.

A normal MQTT DISCONNECT does not trigger the Will message. The time it takes for the broker to detect an unexpected disconnection depends on the connection state and Keep Alive behavior.

Learn more in [Use of MQTT Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message).

## MQTT vs. HTTP, WebSocket, and CoAP



MQTT is not a universal replacement for other communication protocols. The right choice depends on the application's communication pattern, device constraints, network environment, and integration requirements.

| **Feature**                 | **MQTT**                                                     | **HTTP**                                              | **WebSocket**                                                | **CoAP**                                                |
| :-------------------------- | :----------------------------------------------------------- | :---------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------ |
| **Communication model**     | Publish/subscribe                                            | Request/response                                      | Full-duplex connection                                       | Request/response                                        |
| **Typical transport**       | TCP([QUIC](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov)/UDP via EMQX); TLS optional | TCP; TLS optional                                     | TCP; TLS optional                                            | Commonly UDP; other bindings exist                      |
| **Messaging pattern**       | Broker-mediated distribution                                 | Client-initiated requests and responses               | Bidirectional data exchange                                  | Lightweight REST-like messaging                         |
| **Header Size**             | Min **2 Bytes** (Extremely Lightweight)                      | Hundreds of Bytes                                     | Medium overhead                                              | 4 Bytes (Compact)                                       |
| **Power Usage**             | **Low** (Ideal for battery devices)                          | High                                                  | Medium/High                                                  | **Low**                                                 |
| **Latency**                 | **Low**                                                      | High                                                  | Low                                                          | **Low**                                                 |
| **Typical strengths**       | Telemetry, events, device messaging                          | Web APIs and resource access                          | Browser-based real-time applications                         | Constrained-device and machine-to-machine communication |
| **Important consideration** | Requires a broker for standard broker-based deployments      | Repeated requests may add overhead for some workloads | Does not itself define MQTT-style topic subscriptions or QoS | Different delivery and security mechanisms from MQTT    |

For a detailed comparison of MQTT with these protocols, refer to these blog posts:

- [MQTT vs HTTP](https://www.emqx.com/en/blog/mqtt-vs-http)
- [MQTT vs WebSocket](https://www.emqx.com/en/blog/mqtt-vs-websocket)
- [MQTT vs CoAP](https://www.emqx.com/en/blog/mqtt-vs-coap)
- [MQTT vs AMQP](https://www.emqx.com/en/blog/mqtt-vs-amqp-for-iot-communications)

## MQTT Security Best Practices



MQTT is a messaging protocol, not a complete security solution. Secure deployments require appropriate controls at the transport, authentication, authorization, broker, and infrastructure levels.

### Authentication



Authentication verifies the identity of a connecting client.

Depending on the broker and deployment, options may include:

- [Username and password credentials.](https://docs.emqx.com/en/emqx/latest/guides/access-control/authn/pwoverview.html)
- Client certificates, including mutual TLS (mTLS).
- External authentication systems.
- MQTT 5.0 Enhanced Authentication, which supports challenge-response authentication exchanges and can be used with suitable authentication mechanisms.

Use unique credentials or identities for devices whenever practical. Avoid shared default passwords and rotate credentials according to your security policy.

### Authorization



Authorization determines which topics a client may publish to or subscribe to.

For example, a temperature sensor might be allowed to publish to `telemetry/site1/sensor1/temperature` but not subscribe to command topics or publish data under another device's identity.

Use least-privilege access rules and test both permitted and denied operations.

### TLS Encryption



TLS protects MQTT traffic in transit against eavesdropping and tampering. Use TLS listeners for connections that cross untrusted networks, validate server certificates, and consider mTLS when client certificate authentication is required.

SSL is an obsolete predecessor to TLS. In current documentation, use **TLS** rather than treating SSL and TLS as interchangeable protocol versions.

### Rate Limiting and Abuse Protection



Apply appropriate limits to connections, authentication attempts, message rates, packet sizes, and resource consumption where supported. Monitor unusual connection patterns and repeated authorization failures.

### Infrastructure Security



Also consider:

- Network segmentation and firewall rules.
- Secure management interfaces and API access.
- Timely broker and operating-system updates.
- Logging, monitoring, and incident response.
- Certificate lifecycle management.
- Backup and recovery procedures.

## MQTT Data Storage and Integration



MQTT is designed for message transport. The protocol does not define a general-purpose historical database or analytics engine.

A broker may store retained messages, persistent session state, and queued messages, but these features are different from maintaining a queryable history of all telemetry.

For most production IoT applications, MQTT data must be integrated with a suitable storage or processing system.

Examples include:

- **Time-series databases:** Store sensor readings and measurements for historical analysis.
- **Relational databases:** Store structured business records, device metadata, and application state.
- **Data lakes and analytical platforms:** Support large-scale historical analysis and reporting.
- **Stream-processing systems:** Process events in real time, detect patterns, and trigger downstream actions.
- **Message queues and streaming platforms:** Decouple data producers from downstream consumers and support asynchronous processing.

When selecting a storage architecture, consider data volume, retention requirements, query patterns, consistency needs, operational complexity, and total cost of ownership.

An MQTT platform with built-in data integration can help connect device messages to databases, message queues, and cloud services without requiring every application to implement its own integration logic.

For more guidance, see [Database for MQTT Data Storage: A Selection Guide](https://www.emqx.com/en/blog/mqtt-database).

## Advanced MQTT Concepts and Emerging MQTT Technologies



### **MQTT Sparkplug**



Sparkplug is an open specification that defines how MQTT clients communicate within an industrial MQTT infrastructure. It provides conventions for topic namespaces, payload structures, and device and node state management.

Sparkplug helps standardize data exchange between industrial devices, edge gateways, and applications. It is commonly used in Industrial IoT environments where interoperability between operational technology (OT) systems and information technology (IT) applications is important.

The Eclipse Sparkplug specification describes how Edge of Network (EoN) gateways and native MQTT-enabled devices communicate within an MQTT infrastructure.

Learn more in [**MQTT SparkplugB for Industrial IoT**](https://www.emqx.com/en/solutions/mqtt-sparkplug)**.**

### **MQTT Unified Namespace (UNS)**



A Unified Namespace (UNS) is an architectural approach that organizes operational data in a shared, structured namespace. MQTT is often used as the real-time messaging layer in a UNS architecture.

In industrial environments, devices, gateways, and applications such as SCADA, MES, and ERP systems can exchange data through a central MQTT infrastructure. A well-designed topic hierarchy provides a consistent way to represent assets, locations, and operational information.

A UNS can help connect OT and IT systems and make industrial data more accessible to applications and analytics platforms.

For more details, see: [Unified Namespace (UNS) for Industrial IoT](https://www.emqx.com/en/solutions/unified-namespace) 

### **Geo-Distributed MQTT**



Geo-distributed MQTT architectures connect multiple, independent broker clusters across different regions or cloud environments. By serving devices and applications through nearby clusters, organizations can reduce connection latency while enabling communication across geographic boundaries.

EMQX supports this architecture through Cluster Linking, which connects separate EMQX clusters and enables MQTT clients connected to different clusters to exchange messages. Rather than forwarding all messages between clusters, Cluster Linking uses subscription information to forward only messages relevant to subscribers on the remote cluster.

It is useful for global IoT deployments where devices are distributed across regions and applications need to communicate across locations.

Learn more in [EMQX Cluster Linking | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/develop/cluster-linking/introduction.html) 

### **MQTT over QUIC**



QUIC is a transport protocol built on UDP. It supports features such as connection establishment with reduced latency, stream multiplexing, and connection migration.

Using MQTT over QUIC can be useful in environments where network conditions change frequently or where connection performance is important, such as connected vehicles and mobile IoT deployments.

Learn more in [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic).

### **MQTT Streams**



MQTT Streams refers to broker capabilities for handling and accessing continuous MQTT message streams, including use cases that require historical message retention and replay.

This extends the role of an MQTT platform beyond real-time message delivery. Depending on the implementation, stream capabilities can help applications retrieve earlier messages, support data processing workflows, and reduce the need for separate messaging components.

EMQX introduces MQTT Streams since version 6.1, extending MQTT’s real-time publish/subscribe model with persistent, replayable message streams. It enables Kafka-like streaming capabilities while preserving MQTT semantics.

Learn more in [MQTT Streams | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/develop/mqtt-stream/mqtt-stream-concept.html) 

### **MQTT Multi-Tenancy**



Multi-tenancy allows multiple tenants to share an MQTT broker infrastructure while maintaining separate client identities, resources, and access permissions. It is particularly useful for IoT platforms that serve multiple customers, organizations, or business units.

EMQX provides multi-tenancy capabilities through Namespaces, which allow administrators to organize clients and resources into separate logical scopes within a shared EMQX cluster. Rather than managing an entirely separate broker deployment for every tenant, platform operators can use namespaces to manage tenant-level resources and configurations within a common infrastructure

For more details, see: [Namespace | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/guides/multi-tenancy/namespace-overview.html) 

### MCP over MQTT



The Model Context Protocol (MCP) enables AI applications to interact with external tools and services. MCP over MQTT, supported by EMQX, uses MQTT as the transport layer for remote MCP communication, making it suitable for IoT and edge environments. With broker-based service discovery and MQTT's lightweight messaging, it enables AI agents to discover and access distributed MCP servers without relying on direct connections.

Learn more in [MCP over MQTT | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/develop/emqx-ai/mcp-over-mqtt/overview.html) 

### A2A over MQTT



As AI systems evolve toward multi-agent architectures, agents need to discover one another, delegate tasks, and exchange results. A2A over MQTT provides an MQTT-based transport for the Agent-to-Agent (A2A) protocol, enabling distributed agents to communicate through a broker. EMQX implements this approach with its built-in A2A Registry, which manages agent discovery through Agent Cards and tracks agent availability, while MQTT 5.0 supports request-and-reply interactions between agents.

Learn more in [A2A over MQTT: How AI Agents Find Each Other at Scale](https://www.emqx.com/en/blog/a2a-over-mqtt) 

## MQTT FAQ



### 1. Does MQTT use TCP or UDP?



Traditional MQTT communication runs over TCP/IP. MQTT can also be carried over other transports through specific implementations. For example, MQTT over WebSocket enables browser-based clients to communicate with a broker, while MQTT over QUIC uses QUIC over UDP.

MQTT-SN is a separate protocol designed for sensor networks and can operate over transports such as UDP.

### 2. What is the default port for MQTT?



The commonly used default ports are:

- `1883` for MQTT over TCP without TLS.
- `8883` for MQTT over TLS.
- `80` or `443` may be used for MQTT over WebSocket, depending on the server configuration.
- `8083` and `8084` are commonly used for MQTT over WebSocket and secure WebSocket in some broker configurations.

The actual ports depend on the broker and deployment configuration.

### 3. Is MQTT secure?



MQTT can be deployed securely using TLS encryption, client authentication, and authorization controls. However, security depends on how the broker and clients are configured. Production deployments should use secure transport, strong authentication, appropriate topic permissions, and infrastructure security controls.

### 4. What is the maximum MQTT message size?



The MQTT protocol defines a maximum packet size through its Remaining Length field. The practical message size supported by a deployment may be lower, depending on the MQTT version, broker configuration, client implementation, and network constraints.

For large payloads such as images or firmware files, applications should consider whether transferring the data through MQTT is appropriate. An alternative is to transfer the file through a dedicated storage or file-transfer service and use MQTT to exchange a reference or URL.

### 5. Does MQTT guarantee message delivery?



MQTT provides three QoS levels:

- QoS 0: At most once. Messages may be lost.
- QoS 1: At least once. Messages are acknowledged, but duplicates may occur.
- QoS 2: Exactly once at the MQTT protocol level.

The delivery behavior also depends on session configuration and the QoS settings used by the publisher and subscriber. MQTT delivery guarantees do not automatically guarantee that an application has successfully processed a message.

### 6. When should you not use MQTT?



MQTT is designed for lightweight messaging, telemetry, and device communication. It is generally not the best choice for continuous high-bandwidth media streaming, such as raw video or audio.

For these workloads, protocols and technologies designed for media transport, such as WebRTC or RTSP, may be more appropriate. MQTT can still be used alongside them to exchange control messages, status updates, or stream metadata.

### 7. How many concurrent connections can an MQTT broker handle?



The number of concurrent connections depends on the broker architecture, hardware resources, connection configuration, message workload, and deployment environment.

Distributed MQTT platforms such as EMQX are designed to scale horizontally and support large-scale deployments. Actual capacity should be evaluated through workload-specific benchmarking rather than relying on a single connection limit.

### 8. What is the difference between MQTT 3.1.1 and MQTT 5.0?



MQTT 5.0 introduces several features that provide more control and flexibility than MQTT 3.1.1. Key additions include:

- **Reason Codes:** Provide more detailed feedback about connection and operation outcomes.
- **User Properties:** Allow applications to include custom key-value metadata in MQTT packets.
- **Message Expiry Interval:** Allows a message to expire after a specified period.
- **Session Expiry Interval:** Controls how long a session is retained after a client disconnects.
- **Shared Subscriptions:** Allow multiple subscribers to share message delivery for a subscription group.
- **Enhanced Authentication:** Supports more flexible authentication exchanges.

### 9. What is the MQTT Keep Alive interval?



The Keep Alive interval is a value specified by the client in the MQTT CONNECT packet. It defines the maximum period during which the client can go without sending a control packet to the broker.

If the broker does not receive a control packet from the client within 1.5 times the Keep Alive interval, it must treat the connection as disconnected. If a Will Message was configured, the broker may publish it according to the protocol's disconnection rules.

### 10. Can MQTT be used in a web browser?



Yes. Web browsers cannot establish raw TCP connections to an MQTT broker, but they can use MQTT over WebSocket.

An MQTT broker can expose a WebSocket listener, allowing browser-based applications built with frameworks such as React or Vue to connect and publish or subscribe to MQTT messages.

## Conclusion



MQTT provides a lightweight and flexible foundation for connecting devices, streaming real-time data, and building scalable IoT applications. Understanding its core concepts and capabilities can help you make informed decisions when designing and developing MQTT-based solutions.

Whether you're exploring MQTT for the first time or looking to build production-ready IoT applications, EMQX provides the platform and resources to help you put MQTT into practice.

### Explore More MQTT Resources



Continue learning about MQTT with these resources from EMQ:

- [MQTT Programming Tutorials and Guides](https://www.emqx.com/en/blog/category/mqtt-programming?utm_source=chatgpt.com): Explore practical tutorials and programming guides for building MQTT applications.
- [Comparison of Open Source MQTT Brokers 2026](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023?utm_source=chatgpt.com): Compare popular open-source MQTT brokers and their capabilities.
- [MQTT Client Tools 101: A Beginner's Guide](https://www.emqx.com/en/blog/mqtt-client-tools?utm_source=chatgpt.com): Learn about MQTT client tools for connecting to brokers, publishing messages, and subscribing to topics.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
