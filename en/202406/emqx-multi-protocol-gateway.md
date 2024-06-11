## Introduction: A Gateway Framework for IoT Connectivity

The EMQX MQTT platform supports MQTT versions 3.x and 5.0. It also extends its capabilities by embracing a variety of mainstream protocols such as STOMP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), LwM2M/[CoAP](https://www.emqx.com/en/blog/coap-protocol), and JT/T 808, among others. This broad connectivity capability ensures seamless handling of IoT devices across various scenarios while providing a unified access platform and management interface for backend IoT management services, significantly reducing the adaptation costs associated with heterogeneous protocols.

Since version 5.0, EMQX has undergone a transformative upgrade to its multi-protocol access architecture. This upgrade standardizes the configuration and management interfaces, introducing a new framework to support gateway extensions. Concurrently, the standardization of gateway implementations has rendered the functional delineation of each gateway more precise and transparent.

In this blog, we will delve into EMQX's gateway framework and functionalities, offering insights to help readers leverage EMQX's robust multi-protocol access capabilities to connect a wide array of protocol devices and meet diverse IoT data access requirements.

## EMQX Gateway Framework Overview

The diversity of device access protocols, each with its unique connection, login, and messaging definitions, often necessitates the deployment of multiple protocol-specific access services. This can lead to a significant increase in software complexity and maintenance expenses. EMQX has been at the forefront of providing multi-protocol access support since its inception, effectively masking the complexity of various access layer protocols to minimize development and operational costs for users.

Prior to version 5.0, EMQX facilitated multi-protocol support through individual plugins for each protocol. However, this approach suffered from a lack of unified definitions and standards, making it cumbersome for users.

With EMQX 5.0, the multi-protocol access architecture has been restructured to enhance usability and convenience. Non-MQTT protocol accesses are now collectively managed as gateways within a unified framework, streamlining operations such as:

- **Unified User Interface**: The framework introduces a consistent style for configuration files, HTTP APIs, and command-line interfaces. For instance, listener parameter configurations, which varied across protocol plugins in version 4.x, are now standardized in version 5.0.
- **Consolidated Statistics and Monitoring**: The framework provides comprehensive gateway and client-level metrics, including data on bytes transmitted, message counts, and more.
- **Distinct Connection and Session Management**: Each gateway features a dedicated client management interface, with the flexibility for different gateways to share the same Client ID.
- **Separate Client Authentication**: The framework allows for the configuration of distinct authentication mechanisms for each gateway.
- **Extensible and Defined Specifications**: A standardized set of concepts and interfaces simplifies the customization of gateways.

![Unified Gateway Framework](https://assets.emqx.com/images/e40c554e0b37ac7d9659a4b5e0bd348c.png)

<center>Unified Gateway Framework</center>

<br>

The internal components within each gateway have been maintained, with enhancements for better functionality:

- **Listeners**: Gateways can initiate multiple listeners to accommodate network requests, supporting various types such as TCP, SSL, UDP, and DTLS, with each gateway tailored to specific listener types.
- **Packet Parsing**: Dedicated packet parsing modules within each gateway are tasked with handling protocol-specific packets.
- **Connection/Session Management**: These components are responsible for establishing connections and sessions, managing protocol-defined actions like login authentication, and overseeing message exchanges.
- **Messaging Model Adaptation**: This involves adapting messages from other protocols into the MQTT PUB/SUB model, ensuring seamless integration within the EMQX ecosystem, such as converting messages from protocols like LwM2M to EMQX messages with topics and QoS.

![Internal Components within Gateways](https://assets.emqx.com/images/1fd389aa07cdba676e421be433569674.png)

<center>Internal Components within Gateways</center>

## Standardizing Gateway Operations

The EMQX gateway framework not only restructures its architecture but also establishes uniform procedures for **Client Authentication** and **Message Sending and Receiving**.

### Client Authentication: Client Information

The gateway framework employs **Client Information** as the cornerstone for authentication, generated upon a client’s initial access request:

- Irrespective of the gateway type, client information encompasses standard fields like Client ID, Username, Password, etc., with default values assigned where protocol definitions are absent. Additional details such as Peername, ProtoName, and Peercert are also included.
- Unique to each gateway are protocol-specific client details. For instance, the LwM2M gateway includes the Endpoint Name and Life Time.

This approach allows for a comprehensive authentication process, utilizing both generic and protocol-specific client data as inputs for the authenticator.

### Messaging: Adapting to the PUB/SUB Model

To align with MQTT’s PUB/SUB messaging framework, gateways must be compatible with this model to facilitate intercommunication. Gateways using PUB/SUB protocols like MQTT-SN and STOMP, which inherently define topics and message payloads, will:

- Employ the client-specified topic and message directly.
- Assign an appropriate QoS level to the message.

Conversely, for protocols that do not inherently support PUB/SUB concepts such as topics and subscriptions, the following adaptations are necessary:

- A message topic must be designated. For example, LwM2M gateway users can configure message topics for different message types.
- A tailored message format is required. Each gateway type may adopt a unique message format to ensure compatibility with the MQTT model.

## Diving into EMQX Gateway Framework

### Client Authentication

The EMQX gateway framework empowers each gateway type with the flexibility to employ a dedicated authenticator, ensuring tailored security measures:

 ![Customized Client Authentication](https://assets.emqx.com/images/51e1e9564a4aee0af84192c9ec1a168e.png)

<center>Customized Client Authentication</center>

### Messaging Model Adaptation

**For gateways with inherent PUB/SUB capabilities, messaging model transformation is unnecessary**. For instance, the MQTT-SN gateway operates as follows:

- Publishing: Converts a PUBLISH packet from the protocol into a message, retaining the original topic and QoS.
- Subscribing: Processes a SUBSCRIBE packet as a subscription action, retaining the original topic and QoS.
- Unsubscribing: Handles an UNSUBSCRIBE packet as an unsubscription action, retaining the original topic.

**Gateways mirroring the PUB/SUB framework also bypass messaging model conversion**. Taking STOMP as an example, the STOMP gateway functions in this manner:

- Publishing: Translates a SEND packet from the protocol into a publishing message, with the `destination` field serving as the topic, the packet body as the content, and a default QoS of zero.
- Subscribing: Converts a SUBSCRIBE packet into a subscription request, with the `destination` field serving as the topic and a standard QoS of zero, including support for [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) wildcards.
- Unsubscribing: Translates an UNSUBSCRIBE packet into an unsubscription request, with the `destination` field serving as the topic.

**Messaging model conversions are available only for gateways that do not inherently support PUB/SUB models**. For example, the LwM2M protocol requires additional configuration to specify the topic format and rules for organizing message content. Here's an example configuration:

```
gateway.lwm2m {

  mountpoint = "lwm2m/${endpoint_name}/"

  translators {  
    // Downstream command topic.
    // For each new LwM2M client that successfully comes online, the gateway creates a subscription to receive downstream messages and sends them to the client.

    command {
      topic = "dn/#"
      qos = 0
    }                                         

    // Topic used to publish registration events from LwM2M clients
    register {
      topic = "up/register"
      qos = 0
    }
    ...                                   
  }
}
```

For instance, when a client whose `endpoint_name` is `epn1` connects:

- The gateway subscribes to topic `lwm2m/epn1/dn/#` to manage downstream messages for the client.
- The gateway publishes a REGISTER message on topic `lwm2m/epn1/up/register`. The message’s structure follows the LwM2M gateway’s conversion rules, exemplified by the REGISTER message format:

```json
{ "msgType": "register",                                                
  "data": {                                                             
    "ep": "epn1",                                            
    "lt": 6400,                                                
    "sms": "sms_no_example",                                                 
    "lwm2m": "1.2",          
    "objectList": ["1/0", "3/0", "19/0"]                                       
  }                                                                     
}
```

### Publish and Subscribe Authorization

In the EMQX gateway framework, topic authorization is not managed separately within each gateway. Instead, it is centralized within the AuthZ system. Please refer to [Authorization](https://docs.emqx.com/en/emqx/v5.0/access-control/authz/authz.html).

> Note: For gateways that utilize PUB/SUB model conversion, configuring permissions for topics is unnecessary, as the rules governing these topics are inherently mandatory.

### Support for Hooks

EMQX leverages hooks to extend its capabilities, including message tracking for online and offline status, and activating the rule engine. To maintain feature compatibility, gateways are required to publish key events to these hooks.

The essential hooks and their functions are as follows:

| **Hook Name**        | **Description**                                              |
| :------------------- | :----------------------------------------------------------- |
| **Client.\***        |                                                              |
| client.connected     | Notify that a connection has been established                |
| client.disconnected  | Notify that a connection has been disconnected               |
| client.authenticate  | Manage client authentication                                 |
| client.authorize     | Check the PUB/SUB permission                                 |
| **Session.\***       |                                                              |
| session.created      | Notify that a new session has been created                   |
| session.subscribed   | Notify that a new subscription has been established          |
| session.unsubscribed | Notify the cancellation of a subscription                    |
| session.resumed      | Notify that a session has been resumed                       |
| session.discarded    | Notify that the session has been closed (discarded)          |
| session.takeovered   | Notify that the session has been closed (taken over)         |
| session.terminated   | Notify that the session has been closed (terminated)         |
| **Messages.\***      |                                                              |
| message.publish      | Process upstream messages that are about to be published to the Broker |
| message.delivered    | Handle downstream messages to be delivered to the Socket     |
| message.acked        | Confirm receipt of a message                                 |
| message.dropped      | Indicate a message has been dropped                          |

Example:

- The LwM2M gateway’s support for the `client.connected` hook allows the rule engine to detect the online event of LwM2M devices via `$event/client_connected`.
- By supporting the `client.authenticate` hook, the ExHook can manage the authentication of LwM2M clients.

### Customizing Authentication

Similar to the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools), the gateway employs an authentication chain to process requests. This chain continues until an authenticator, plugin, or ExHook grants or denies access:

![EMQX Authentication Chain](https://assets.emqx.com/images/4598b40aa2d7badc60a11d2a00228627.png)

<center>EMQX Authentication Chain</center>

This structure allows for the expansion of authentication support through **customized plugins or ExHooks**. The function of each authenticator can be summarized as follows:

```
fun authenticate(ClientInfo, LastAuthResult)  // The parameters are client information and the result from the previous authenticator.
    -> {stop, NewAuthResult}                  // Option 1: Ends the chain, returning a new authentication outcome.
     | ignore                                 // Option 2: Proceeds without action to the next authenticator.
```

> Note: As all protocols direct authentication requests to this chain, it’s crucial to identify the client’s origin by fields such as protocol and listener_id.

### User Interface for Gateway Management

The EMQX gateway framework offers a consistent user interface across all gateways, accessible through the gateway’s HTTP API. This interface simplifies various operations, including

- Activating or deactivating gateways and modifying their configurations.
- Managing gateway authenticators—enabling, disabling, and updating as needed.
- Handling listeners—adding, removing, or updating to suit different communication needs.
- Overseeing client interactions—from querying to disconnecting or managing subscriptions.

![EMQX Gateway HTTP API Interface Examples](https://assets.emqx.com/images/455f19012d5795713137183e21ed5726.png)

<center>EMQX Gateway HTTP API Interface Examples</center>

This blog only provides some simple examples. For comprehensive guidance, please refer to the official documentation on [Gateway Configuration](https://docs.emqx.com/en/emqx/v5.0/configuration/configuration-manual.html#gateway) and [Gateway HTTP API](https://docs.emqx.com/en/emqx/v5.0/admin/api.html#/gateway).

Example 1: Activating a STOMP gateway using the configuration file:

```
gateway.stomp {

  mountpoint = "stomp/"

  listeners.tcp.default {
    bind = 61613
    acceptors = 16
    max_connections = 1024000
    max_conn_rate = 1000
  }
}
```

Example 2: Enabling an MQTT-SN gateway through the HTTP API:

```shell
curl -X 'POST' 'http://127.0.0.1:18083/api/v5/gateway' \
  -u admin:public \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "mqttsn",
  "enable": true,
  "gateway_id": 1,
  "mountpoint": "mqttsn/",
  "listeners": [
    {
      "type": "udp",
      "bind": "1884",
      "name": "default",
      "max_conn_rate": 1000,
      "max_connections": 1024000
    }
  ]
}'
```

## EMQX Gateway in the Future

EMQX’s gateway architecture already simplifies multi-protocol device access for users. Looking ahead, we aim to further refine this capability in several key areas:

- **Enhanced Observability**: Integrating support for exporting monitoring data to Prometheus and StatsD, providing users with deeper insights into their IoT networks.
- **Protocol Testing**: Establishing a comprehensive suite of standardized tests for each supported protocol to ensure reliability and performance.
- **Interface and Client Management**: Upgrading the management interfaces for a more personalized experience, such as managing resource models for LwM2M devices.
- **NAT Network Support**: Developing a mechanism for UDP-based protocols like LwM2M to maintain session continuity under NAT environments, ensuring seamless device reconnection after dormancy periods.
- **ExProto Optimization**: Streamlining the ExProto design to reduce the complexity of using gRPC, thereby enhancing efficiency and ease of use.

## Conclusion

The innovative gateway framework of EMQX has revolutionized the integration and unified management of diverse protocols, significantly improving user experience. Coupled with powerful data integration, secure and reliable authentication and authorization, and billion-level scalability, EMQX empowers IoT practitioners across industries to seamlessly connect, transfer, and process real-time data for a myriad of applications.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
