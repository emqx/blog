## Introduction to OCPP

The **Open Charge Point Protocol (OCPP)** is an application protocol designed for communication between electric vehicle (EV) charging stations and a central management system. It facilitates the exchange of information related to charging sessions, status updates, and other operational data, enabling effective management for charging business.

The adoption of the OCPP has seen significant growth in the EV charging industry as the de facto standard for communication between EV charging stations and central management systems. Many countries and companies are incorporating OCPP into their infrastructure to ensure a seamless and scalable EV charging network.

The OCPP protocol standardizes the exchange of information. For example, it supports various operations:

1. **Boot Notification**: When a Charge Point connects to the Central System, it sends a boot notification to register itself and provide initial status information.
2. **Heartbeat**: The Charge Point periodically sends heartbeat messages to the Central System to indicate that it is still connected and operational.
3. **Authorize**: Before a charging session begins, the Charge Point sends an authorization request to the Central System to verify the identity of the user or vehicle.
4. **Start and Stop Transaction**: The Charge Point communicates the start and stop of charging sessions, providing data such as meter readings, session duration, and energy consumption.
5. **Status Notification**: The Charge Point sends status updates to inform the Central System of its current state, such as available, occupied, or faulted.
6. **Firmware Management**: The Central System can manage the firmware of Charge Points by sending update commands.
7. **Data Transfer**: The protocol allows for the transfer of various operational data between the Charge Point and the Central System for monitoring and analysis.

These operations ensure that the Central System can effectively monitor, control, and manage the network of EV charging stations.

The OCPP protocol has the following two specifications for transmitting messages over the network:

- **OCPP-J:** OCPP communication over WebSockets using JSON. Specific OCPP versions should be indicated with the J extension. OCPP1.6J means we are talking about a JSON/WebSockets implementation of 1.6.
- **OCPP-S:** OCPP communication over SOAP and HTTP(s). As of version 1.6, this should be explicitly mentioned. Older versions are assumed to be S unless clearly specified otherwise, e.g. OCPP 1.5 is the same as OCPP1.5S

For example, a `BootNotification.req` message format in the OCPP-J specification is:

```json
[
  // MessageTypeId, 2 indicates that this is a Client to Server request message
  2,
  // UniqueId, a unique Id for the message to identify it
  "19223201",
  // Action, indicates the type of message being transmitted
  "BootNotification",
  // Payload, the body of the message
  {"chargePointVendor": "VendorX", "chargePointModel": "SingleSocketCharger"}
]

```

## OCPP Gateway in EMQX 5

EMQX is a scalable, distributed MQTT platform that supports unlimited connections, offers seamless integration, and can be deployed anywhere. It provides a Multi-Protocol Gateway to handle all non-MQTT protocol connections, authentication, and message sending and receiving. 

> For more information about EMQX Multi-Protocol Gateway, please refer to: [EMQX Multi-Protocol Gateway: Streamlining IoT Communication](https://www.emqx.com/en/blog/emqx-multi-protocol-gateway) 

In EMQX 5, there is an OCPP Gateway that works with the OCPP-J 1.6 protocol:

![OCPP Gateway](https://assets.emqx.com/images/7790d3b6c47ad74915eb48cfe311f5f7.png)

This means:

- The OCPP Gateway starts a WebSocket server port to handle connections, message reception, and message delivery from all Charge Point devices.
- **Third Services** refers to the user-implemented backend service that processes OCPP requests based on the MQTT messaging pattern.
- The OCPP Gateway converts all upstream messages from devices into corresponding [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) and payloads and sends them to third-party services. It also receives MQTT control messages from third-party services, converts them into OCPP format messages, and sends them to the appropriate Charge Point.

This Blog will introduce how to use the OCPP Gateway in EMQX 5.0 to integrate OCPP devices, thus enabling interoperability across different manufacturers and service providers.

## Configuring OCPP Gateway

First, we should install the latest enterprise edition of EMQX. Please refer to [Get Started with EMQX Enterprise | EMQX Enterprise Docs](https://docs.emqx.com/en/enterprise/latest/getting-started/getting-started.html#install-emqx) .

Or directly use the following command to start the latest version of the EMQX container using Docker:

```shell
docker run -p 18083:18083 -p 1883:1883 -p 33033:33033 emqx/emqx-enterprise:latest
```

On the EMQX Dashboard, click **Management** -> **Gateways** on the left navigation menu. On the **Gateway** page, all supported gateways are listed. Locate **OCPP** and click **Setup** in the **Actions** column. Then, you will be directed to the **Initialize OCPP** page.

![Gateways 1](https://assets.emqx.com/images/947c00eda0813396bf3af55c3b23ccf3.png)

To simplify the configuration process, EMQX offers default values for all required fields on the **Gateways** page. We just need:

1. Change the `Message Format Checking` to `Disable` .
2. Click **Next** in the **Basic Configuration** tab to accept all the default settings.
3. Then, you will be directed to the Listeners tab, where EMQX has pre-configured a WebSocket listener on port 33033. Click **Next** again to confirm the setting.
4. Then click the **Enable** button to activate the OCPP Gateway.

Upon completing the gateway activation process, you can return to the **Gateways** page and see that the OCPP Gateway now displays an **Enabled** status.

![Gateways 2](https://assets.emqx.com/images/c9b357ae40c5180d5e1167623d9fde8d.png)

## Working with OCPP Clients

Once the OCPP gateway is operational, you can use OCPP client tools to test connections and verify that the setup functions correctly.

Take [**ocpp-go**](https://github.com/lorenzodonini/ocpp-go) as a practical example. This section demonstrates how to connect it to the OCPP Gateway in EMQX.

Begin by preparing an MQTT client to interface with the OCPP Gateway. For instance, using [**MQTTX**](https://mqttx.app/downloads), configure it to connect to EMQX and subscribe to the topic `ocpp/#`.

![MQTTX](https://assets.emqx.com/images/c79d8703c14ebfb02765860b71974093.png)

Execute the ocpp-go client and establish a connection with the OCPP Gateway.

**Note**: Replace `<host>` in the command below with the address of your EMQX server.

```shell
docker run -e CLIENT_ID=chargePointSim -e CENTRAL_SYSTEM_URL=ws://<host>:33033/ocpp -it --rm --name charge-point ldonini/ocpp1.6-charge-point:latest
```

A successful connection will output logs similar to:

```shell
INFO[2023-12-01T03:08:39Z] connecting to server logger=websocketINFO[2023-12-01T03:08:39Z] connected to server as chargePointSim logger=websocketINFO[2023-12-01T03:08:39Z] connected to central system at ws://172.31.1.103:33033/ocppINFO[2023-12-01T03:08:39Z] dispatched request 1200012677 to server logger=ocppj
```

Monitor MQTTX for an incoming message formatted as:

```
Topic: ocpp/cp/chargePointSim
Payload
{
  "UniqueId": "1200012677",
  "Payload": {
    "chargePointVendor": "vendor1",
    "chargePointModel": "model1"
  },
  "Action": "BootNotification"
}
```

This message signifies that the ocpp-go client has connected to the OCPP Gateway and initiated a `BootNotification` request.

In MQTTX, compose a message to the topic `ocpp/cs/chargePointSim` with the following content and send it.

**Note**: Ensure to replace `UniqueId` with the one received in the previous message.

```json
{
  "MessageTypeId": 3,
  "UniqueId": "***",
  "Payload": {
    "currentTime": "2023-12-01T14:20:39+00:00",
    "interval": 300,
    "status": "Accepted"
  },
  "Action": "BootNotification"
}
```

Subsequently, MQTTX will receive a `StatusNotification` status report. This indicates that the OCPP client has successfully established a connection with the OCPP Gateway.

```
Topic: ocpp/cp/chargePointSim

Payload:
{
  "UniqueId": "3062609974",
  "Payload": {
    "status": "Available",
    "errorCode": "NoError",
    "connectorId": 0
  },
  "MessageTypeId": 2,
  "Action": "StatusNotification"
}
```

Now, the OCPP client has connected to EMQX's OCPP Gateway and communicated with third-party services.

## Conclusion

In conclusion, the integration of OCPP devices with EMQX 5.0 through the OCPP Gateway is a powerful solution for managing and monitoring EV charging stations. It offers scalability, flexibility, real-time monitoring, enhanced security, improved data management, simplified configuration, and cost-effectiveness. By adopting this solution, businesses can ensure efficient and effective management of their EV charging infrastructure, paving the way for a more sustainable and connected future.

Learn more about EMQ’s contribution to the EV industry:

- [Empowering EV Infrastructure Management: EMQX MQTT Platform for Smart Charging](https://www.emqx.com/en/blog/electric-vehicle-charging-stations-management) 
- [Empowering Electric Mobility: EV Power's Journey in Pioneering Community Charging with the Unified MQTT Platform](https://www.emqx.com/en/customers/ev-power) 



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
