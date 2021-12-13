### What is the session?

The messaging series which start from initiating an MQTT connection request to the server from the client, until the connection is interrupted and the session expires is called a session. Therefore, the session may only last for one network connection, or if the client can re-establish the connection before the session expires, the session may exist across multiple network connections.

> In the MQTT v5, the session expiration time depends on the Session Expiry Interval filed. The previous version of the protocol did not limit the session expiration time, but is usually determined by the MQTT server.

### What is session state?

[MQTT](https://www.emqx.com/en/mqtt) requires the client and server to store a series of states related to the client identifier during the valid period of the session, which is called session state.

The client needs to store the following session state:

- The QoS 1 and QoS 2 message that has been sent to the server, but have not yet completed the confirmation.
- The QoS 2 message that has been received from the server, but has not yet completed the confirmation.

The server needs to store the following session state:

- Whether the session is existed, even if the rest of the session state is empty.
- The client subscribes to messages, including any [subscription identifier](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options).
- The QoS 1 and QoS 2 message that has been sent to the client, but have not yet completed the confirmation.
- The QoS 0 (optional), QoS 1 and QoS 2 message that waiting to be delivered.
- The QoS 2 message, [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) and will delay interval that has been received from the client, but has not yet completed the confirmation.
- The session expiration time.

### The use of session state

If the client causes the connection briefly interrupted because of the network fluctuation or other reasons and re-establish the connection with the server before the session is expired, the client can continue to use the subscription relationship established by the last connection. In the low bandwidth and unstable network scenario, the network interruption may happen frequently. The way that saves the session state can avoid re-subscription every time you connect, and can reduce the resource consumption of the client and the server when reconnecting. The server will retain the messages that have not been completed the confirmation and the follow-up messages for the client during the client offline. The server will forward these messages when the client reconnects, which can avoid losing messages and can also reduce the user's perception of network changes in some scenarios.

### Start and end of the session

[MQTT v5.0](https://www.emqx.com/en/mqtt/mqtt5) and v3.1.1 have significant changes in the session. MQTT v3.1.1 only has one field Clean Session which is specified by the client when connecting. When the field is 1, it means that the client and the broker have to discard any previous session and create a new session, and the life cycle of the session is consistent with the network connection. When the field is 0, it means that the server has to use the session that associated with Client ID to recover the communication with the client (unless the session does not exist). The client and the server have to store the session state after disconnecting.

MQTT v3.1.1does not stipulate when the persistent session should be expired. If only understood from the protocol level, this persistent session should exist forever. However, in the actual scenario, this is not realistic, because it will highly occupy the resource of the server. Therefore, the server usually does not follow the protocol to implementation, but provides a global configuration for limiting the session expiration time.

In the MQTT 5.0, this problem has been properly resolved. The field Clean Session is divided into field [Clean Start](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval) and Session Expiry Interval. The field Clean Start specifies whether need a new session, field Session Expiry Interval specifies the session expiration time. They will be specified when connecting, but the field Session Expiry Interval can be updated when the client disconnected. Therefore, we can easily implement retaining the session when the client disconnected because of an abnormal network connection. Also, we can easily implement terminating the session by closing the connection when the client offline normally.

### How does the client know that this is a resumed session?

It is obvious that when the client initiates a connection in expecting from a previously established session resume state way, it needs to know whether there is a corresponding session existing in the server, and then it can determine whether the need to re-subscribe after establishing the connection. For this point, from v3.1.1, [MQTT protocol](https://www.emqx.com/en/mqtt) has designed the field Session Present for CONNACK packet. This field is used to represent whether the session currently used is new, and the client can judge according to the value of this field.

### Recommendation for use

The developer needs to pay special attention to the connection between Client ID and session. If the same ClientID is used by different applications or users multiple times in some scenarios, that is each connection will have completely different behavior, you need to ensure that you request a new session whenever you connect. Evaluate reasonably whether the persistent session is needed, if it is unnecessary, you can set the session as immediately expired for reducing the occupancy of resources by the server. Set appropriate session expiration time.  If the time is set too short, may lose the meaning of storing the session state. If the time is set too long, may occupy excessive server resources.
