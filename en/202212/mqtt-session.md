## MQTT Persistent Session

Unstable networks and limited hardware resources are the two major problems that IoT applications need to face. The connection between MQTT clients and brokers can be abnormally disconnected at any time due to network fluctuations and resource constraints. To address the impact of network disconnection on communication, the MQTT protocol provides Persistent Session.

[MQTT client](https://www.emqx.io/mqtt-client) can set whether to use a Persistent Session when initiating a connection to the server. A Persistent Session will hold some important data to allow the session to continue over multiple network connections. Persistent Session has three main functions as follows:

- Avoid the additional overhead of need to subscribe repeatedly due to network outages.
- Avoid missing messages during offline periods.
- Ensuring that QoS 1 and QoS 2 messages are not affected by network outages.


## What Data Need to Store for a Persistent Session?

We know from the above that Persistent Session needs to store some important data in order for the session to be recovered. Some of this data is stored on the client side and some on the server side.

Session data stored in the client:

- QoS 1 and QoS 2 messages have been sent to the server but have not yet completed acknowledgment.
- QoS 2 messages that were received from the server but have not yet completed acknowledgment.

Session data stored in the server:

- Whether the session exists, even if the rest of the session status is empty.
- QoS 1 and QoS 2 messages that have been sent to the client but have not yet completed acknowledgment.
- QoS 0 messages (optional), QoS 1 and QoS 2 messages that are waiting to be transmitted to the client.
- QoS 2 messages that are received from the client but have not yet completed acknowledgment, Will Messages, and Will Delay Intervals.

## Using MQTT Clean Session

Clean Session is a flag bit used to control the life cycle of the session state. A value of 1 means that a brand new session will be created on connection, and the session will be automatically destroyed when the client disconnects. If it is 0, it means that it will try to reuse the previous session when connecting. If there is no corresponding session, a new session will be created, which will always exist after the client disconnects.

> **Note:** A Persistent Session can be resumed only if the client connects again using a fixed Client ID. If the Client ID is dynamic, a new Persistent Session will be created after a successful connection.

The following is the Dashboard of the [open-source MQTT broker EMQX](https://www.emqx.io/). You can see that the connection in the diagram is disconnected, but because it is a Persistent Session, it can still be viewed in the Dashboard.

![MQTT Connections](https://assets.emqx.com/images/f66ac8daa11ef2ff5df6b466cd81b510.png)

EMQX also supports setting session-related parameters in the Dashboard.

![MQTT Session](https://assets.emqx.com/images/b1a0e23bf46e46762ce8dd9fc4a38bef.png)

MQTT 3.1.1 does not specify when a Persistent Session will expire; if understood at the protocol level alone, this Persistent Session should be permanent. However, this is not practical in a real-world scenario because it takes up a lot of resources on the server side. So, the server usually does not follow the protocol exactly, but provides a global configuration to the user to limit the session expiration time.

For example, the[ Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ sets a session expiration time of 5 minutes, a maximum number of 1000 messages, and does not save QoS 0 messages.

Next, we will demonstrate the use of Clean Session with the open-source cross-platform [MQTT 5.0 desktop client tool - MQTTX](https://mqttx.app/).

After opening MQTTX, click `New Connection` button to create an [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) as shown below.

![Click New Connection](https://assets.emqx.com/images/905a669d634a4438a7bdcc6cad90b975.png)

Create a connection named `MQTT_V3` with Clean Session off (i.e., false), and select MQTT version 3.1.1, then click `Connect` button in the upper right corner.

> The default server connected to is the [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ.

![Create a connection](https://assets.emqx.com/images/fb8b1986a743b061cab5028c353016c9.png)

Subscribe to `clean_session_false` topic after a successful connection and QoS is set to 1.

![Subscribe to clean_session_false topic](https://assets.emqx.com/images/5fa0b38984c1f199bbd6f875a6a65bd4.png)

After a successful subscription, click `Disconnect` button in the upper right corner. Then, create a connection named `MQTT_V3_Publish` , again with the MQTT version set to 3.1.1, and publish two QoS 1 messages to `clean_session_false` topic after a successful connection.

![Publish MQTT Messages](https://assets.emqx.com/images/1590dd170d31a0576110dd2790a8eabd.png)

Then, select the MQTT_V3 connection and click `Connect` button to connect to the server. You will successfully receive two messages that were published during the offline period.

![Receive MQTT Messages](https://assets.emqx.com/images/3797fb43e05558eca50e41596e307fde.png)


## Session Improvements in MQTT 5.0

In MQTT 5.0, Clean Session is split into Clean Start and Session Expiry Interval. Clean Start specifies whether to create a new session or try to reuse an existing session when connecting. Session Expiry Interval is used to specify how long the session will expire after the network connection is disconnected.

Clean Start of `true` means that any existing session must be discarded, and a completely new session is created; `false` indicates that the session associated with the Client ID must be used to resume communication with the client (unless the session does not exist).

Session Expiry Interval solves the server resource waste problem caused by the permanent existing of Persistent Sessions in MQTT 3.1.1. A setting of 0 or none indicates that the session expires when disconnected. A value greater than 0 indicates how many seconds the session will remain after the network connection is closed. A setting of `0xFFFFFFFF` means that the session will never expire.

More details are available in the blog: [Clean Start and Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval).


## Q&A About MQTT Session

### When the session ends, do the Retained Messages still exist?

[MQTT Retained Messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message) are not part of the session state and will not be deleted at the end of the session.

### How does the client know that the current session is the resumed session?

The MQTT protocol has designed a Session Present field for CONNACK message since v3.1.1. When the server returns a value of 1 for this field, it means that the current connection will reuse the session saved by the server. The client can use this field value to decide whether to re-subscribe after a successful connection.

### Best practices of using Persistent Session

- You cannot use dynamic Client ID. You need to ensure that the Client ID is fixed for each client connection.
- Properly evaluate the session expiration time based on server performance, network conditions, and client type. Setting it too long will take up more server-side resources. And setting it too short will cause the session to expire before reconnecting successfully.
- When the client determines that the session is no longer needed, you can reconnect using Clean Session as true, and then disconnect after a successful reconnection. In the case of MQTT 5.0, you can set the Session Expiry Interval as 0 directly when disconnecting, indicating that the session will expire when the connection is disconnected.

## Summary

At this point, we have completed our introduction to MQTT Persistent Session and demonstrated the use of Clean Session through the desktop client. You can refer to this article to receive offline messages and reduce subscription overhead by using MQTT Persistent Session.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT Topics, Wildcards, Retained Messages, Will Messages, and other features. Explore more advanced applications of MQTT and get started with MQTT application and service development.




<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
