The MQTT protocol communicates by exchanging predefined MQTT control packets. We will take  **[MQTTX](https://github.com/emqx/MQTTX)**  as an example to show how to implement the publish and subscribe function through MQTT packets.

## Connect 

MQTT protocol is based on the TCP / IP protocol. Both the MQTT Broker and the Client need a TCP / IP address.

### Broker

![1.png](https://assets.emqx.com/images/5002d126f2768ed89f0186d35cb5f3d7.png)

If you don't have an available MQTT broker for the time being, **[EMQX](https://github.com/emqx/emqx)** provides a public broker address for testing: `broker.emqx.io:1883` .

### Client

![WX201911281139012x.png](https://assets.emqx.com/images/824bc7779391f86ec9cf02bd73378f42.png)

The configuration of the Client in the MQTTX tool is actually the configuration of the Connect packets in the [MQTT protocol](https://www.emqx.com/en/mqtt). The following explains the related configuration items:

#### Client ID

The server uses the ClientId to identify the client. Each client that connects to the server has a unique ClientId. Both the client and server must use the ClientId to identify the status related to the [MQTT session](https://www.emqx.com/en/blog/mqtt-session) between them.

The ClientId must exist, but the server can allow the client to provide a zero-byte ClientId. If this is done, the server must treat this as a special case and assign a unique ClientId to that client. Then, it can process this CONNECT packet normally.

#### Username/Password

MQTT can implement related authentication and authorization by sending the username and password. However, if this information is not encrypted, the username and password are sent in clear text. EMQX not only supports SSL / TLS encryption, but also provides **[emqx-auth-username](https://github.com/emqx/emqx-auth-username)** plugin to encrypt passwords.

#### Keep Alive

Keep Alive is a time interval in seconds. It refers to the maximum time interval allowed between the time when the client transmits a control packet to the time when the next message is sent. The client is responsible for ensuring that the interval of sending control packets does not exceed the value of the keep-alive. If no other control packet can be sent, the client must send a PINGREQ packet.

If the value of Keep Alive is non-zero, and the server does not receive the control packet from the client within 1.5 times of the Keep Alive time, it must disconnect the client's network connection and consider the network connection to be disconnected.

#### Clean Session

The client and server can save session state to support reliable message transmission across network connections. This flag tells the server whether this connection is a brand new connection.

The session state of the client includes:

- QoS 1 and QoS 2 level messages that have been sent to the server but have not yet been confirmed
- QoS 2 level messages that have been received from the server but have not yet been confirmed

The session state of the server includes:

-  Whether the session exists, even if the rest of the session state is empty.
-  Client's subscription information.
-  QoS 1 and QoS 2 level messages that have been sent to the client but have not yet been confirmed
-  QoS 1 and QoS 2 level messages to be transferred to the client.
-  QoS 2 level messages that have been received from the client but have not yet been confirmed
-  Optional, QoS 0 level message to be sent to the client.

If the CleanSession flag is set to 1, the client and server must discard any previous sessions and start a new session. The session only lasts as long as the network connection.

If the CleanSession flag is set to 0, the server must resume communication with the client based on the state of the current session (identified by ClientId). If there is no session associated with this client identifier, the server must create a new session. When the connection is disconnected, the client and server must save the session information.

## Connack confirms connection request

When the client sends a Connect packet to request a connection to the server, the server must send a Connack packet as a response to the Connect packet  from the client. If the client does not receive the CONNACK packet from the server within a reasonable time, the client should close the network connection. The reasonable time depends on the type of application and the communication infrastructure. In  **[MQTTX](https://github.com/emqx/MQTTX)**, you can set a reasonable timeout time through Connection Timeout.

![Connect.png](https://assets.emqx.com/images/cc1c9341a7e7471f0528e884788ab82e.png)

Connack messages contain two important signs of Session Present and Connect Return code.

#### Session Present

Session Present flag indicates whether the current session is a new session. If the server receives a connection with a CleanSession flag of 1, the SessionPresent flag in the Connack packet is 0. If the server receives a connection with CleanSession 0, the value of the SessionPresent flag depends on whether the server has saved the session state of the client corresponding to ClientId. If the server has saved the session state, the SessionPresent flag in the Connack packet is 1. If the server has no saved session state, the SessionPresent flag in the Connack packet is 0.

#### Connect Return code 

Connect Return code represents the server's response to this Connect, and 0 indicates that the connection has been accepted by the server. If the server receives a valid CONNECT packet but cannot process it for some reason, the server should try to send a CONNACK packet with a non-zero return code (one in the following table). If the server sends a CONNACK packet with a non-zero return code, it must close the network connection.

| **Value** | Return Code Response                                   | Description                                                  |
| --------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| 0         | 0x00 connection accepted                               | The connection has been accepted by the server               |
| 1         | 0x01 connection refused, unsupported protocol version  | The server does not support the MQTT protocol level requested by the client |
| 2         | 0x02 connection refused, unqualified client identifier | The client identifier is correctly UTF-8 encoded, but  is not allowed by the server |
| 3         | 0x03 Connection refused, server is unavailable         | Network connection has been established, but MQTT service is unavailable |
| 4         | 0x04 connection refused, invalid username or password  | Data format for username or password is invalid              |
| 5         | 0x05 connection refused, unauthorized                  | Client is not authorized to connect to this server           |
| 6-255     |                                                        | retained                                                     |

If all connection return codes in the above table are considered inappropriate, the server must close the network connection without sending a CONNACK packet.

## Subscribe to topics

The client sends a Subscribe packet to the server to create one or more subscriptions. Each registered client cares about one or more topics. In order to forward application messages to topics that match those subscriptions, the server sends Publish packet to the client. The Subscribe packet specifies the maximum QoS level for each subscription, and the server sends an application message to the client based on it.

![WX201911281425432x.png](https://assets.emqx.com/images/0e75ee848d01e883623bc925a898285e.png)

The payload of a Subscribe packet must contain at least one pair of topic filter and QoS level fields combination. A Subscribe packet without a payload is a violation of the protocol.

Use **[MQTTX](https://github.com/emqx/MQTTX)** to connect the Broker of  `broker.emqx.io:1883`and create a subscription with the topic of `testtopic/#` and Qos equal to 2.

![WX201911281439252x.png](https://assets.emqx.com/images/3eaa7a9170d37596496eb9d1fa187f4d.png)

## Suback subscription confirmation

The server sends a Suback packet to the client to confirm that it has received Subscribe packet and is processing it .

![Subscribe.png](https://assets.emqx.com/images/5dbc2a5fcbd65cfb8283d61bdc94c748.png)

The Suback packet contains a list of reason codes, which is used to specify the maximum QoS level or an error that occurs for each subscription requested by the Subscribe packet. Each reason code corresponds to a topic filter in the Subscribe packet. The reason code sequence in the Suback packet must match the order of the topic filters in the Subscribe packet.

Allowed values of return code:

- 0x00 - maximum QoS 0
- 0x01 - success – maximum QoS 1
- 0x02 - success – maximum QoS 2
- 0x80 - Failure  



## Publish messages

Publish packet refers to an application message transmitted from the client to the server or from the server to the client. After receiving the Publish packet, the server forwards the message to other clients according to the topic filter.

![Publish.png](https://assets.emqx.com/images/94513f3dab1454b41d9c66992d149a82.png)

Try using **[MQTTX](https://github.com/emqx/MQTTX)** to publish a message with the topic `testtopic/mytopic` and the content` {"msg":"hello world"} `. Because  the topic `testtopic/#`  has been subscribed before, the message forwarded by Broker is received immediately.

![WX201911281441422x.png](https://assets.emqx.com/images/45e8021cf9012bd49a561f9e6a201740.png)

#### Topic

The topic name is used to identify which session the message should be published. The topic name of the Publish packet sent by the server to the subscribing client must match the topic filter of the subscription.

#### QoS

QoS refers the quality level of service for application message distribution

| QoS value | **Bit 2** | **Bit 1** | Description              |
| ----------- | --------- | --------- | ------------------------ |
| 0           | 0         | 0         | Distribute at most once  |
| 1           | 0         | 1         | Distribute at least once |
| 2           | 1         | 0         | Distribute only once     |
| -           | 1         | 1         | Retained                 |

Publish packet cannot set all QoS bits to 1. If the server or client receives a Publish packet with all QoS bits set to 1, it must close the network connection.

For the working principle of different levels of QoS, please refer to [MQTT 5.0 Protocol Introduction-QoS Quality of Service](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).

#### Retain

If the RETAIN flag of the Publish packet sent by the client to the server is set to 1, the server must store this application message and its quality of service level (QoS) so that it can be distributed to future subscriber with the matching topic names . When a new subscription is created, for each matching topic name, if there is a recently retained message, it must be sent to this subscriber. If the server receives a Q message with a RETAIN flag of 1, it must discard any messages previously retaind for that topic and treat this new message as a new retained message for that topic.

Publish packet with a retain flag of 1 and a payload of zero bytes will be treated as a normal message by the server, and it will be sent to the client that matches the topic of the subscription. In addition, any existing retained messages under the same topic must be removed, so any subscribers following this topic will not receive a retained message

When the server sends a Publish packet to the client, if the message is sent as a result of a new subscription by the client, it must set the retain flag of the packet to 1. When a Publish packet is sent to the client because it matches an established subscription, the server must set the retain flag to 0, regardless of the value of the retain flag in the message it receives.

If the retain flag of the Publish packet sent by the client to the server is 0, the server cannot store the message and cannot remove or replace any existing retained message.

#### Payload

The payload contains application messages to be published. The content and format of the data is specific to the application and images, any encoded text, encrypted data, and almost all binary data can be sent.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
