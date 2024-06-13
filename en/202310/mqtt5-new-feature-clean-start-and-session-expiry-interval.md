In this article, we will introduce the session mechanism of [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), as well as **Clean Start** and **Session Expiry Interval**, two connection parameters used to manage the session lifecycle.

>New to MQTT 5.0? Please check out our
>
>[MQTT 5.0: 7 New Features and a Migration Checklist](https://www.emqx.com/en/blog/introduction-to-mqtt-5)


## Why does MQTT support the session mechanism?

In IoT scenarios, devices may frequently disconnect due to network or power issues. If the client and server always establish connections in a new context, it will bring the following problems:

1. The client must resubscribe all the relevant topics after reconnecting to continue receiving messages, which will bring additional overhead to the server.
2. The client will miss messages during offline periods.
3. The service quality of QoS 1 and QoS 2 will not be guaranteed.

To avoid these problems, the MQTT protocol designed a session mechanism, which also forms the basis of MQTT communication.

## What is an MQTT Session?

An [MQTT session](https://www.emqx.com/en/blog/mqtt-session) is essentially a set of contextual data that requires additional storage by the server and client. Some Sessions can only last while the network connection is established, others can exist across multiple consecutive network connections. When the client and server resume communication with the help of this session data, the network interruption will be as if it never happened.

Taking the server as an example, it needs to store the client's subscription list. Regardless of whether the client is currently connected or not, as long as the session has not expired, the server can know which messages are subscribed by the client and cache these messages for it. In addition, the client does not need to re-initiate the subscription when connecting again, which also reduces the performance overhead of the server.

MQTT defines the session state that needs to be stored for the server level and the client respectively. For the **server**, it needs to store the following:

1. The existence of the session.
2. The client's subscriptions.
3. QoS 1 and QoS 2 messages which have been sent to the client but have not been completely acknowledged.
4. QoS 1 and QoS 2 messages pending transmission to the client, and optionally QoS 0 messages pending transmission to the client.
5. QoS 2 messages which have been received from the client but have not been completely acknowledged.
6. The [Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) and the Will Delay Interval.
7. If the session is currently not connected, the time at which the session will end and the session state will be discarded.

For the **client**, it needs to store the following:

1. QoS 1 and QoS 2 messages which have been sent to the server but have not been completely acknowledged.
2. QoS 2 messages which have been received from the server but have not been completely acknowledged.

It is obvious that asking the server and client to permanently store these session data will not only bring a lot of additional storage costs but is also unnecessary in many scenarios. For example, if we just want to avoid message loss caused by a brief interruption of the network connection, we generally set the session data to be retained for a few minutes after the connection is disconnected.

In addition, when the client and server session state is inconsistent, for example, the client device loses session data due to restart, then it needs to inform the server to discard the original session and create a new session when connecting.

For these two points, [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) provides two connection fields, **Clean Start** and **Session Expiry Interval**, to control the lifecycle of the session.

## Introduction to Clean Start

**Clean Start** is located in the [Variable Header](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) of the CONNECT packet. The client specifies whether to reuse the existing session through this field when connecting. It has only two values: 0 and 1.

**When Clean Start is set to 0**, if the server has a session associated with the Client ID specified when the client is connected, it must use this session to resume communication.

If no session exists associated with this Client ID, the server must create a completely new session. In this case, the client is using an old session, and the server is using a brand-new session. The session states on both sides are inconsistent. Therefore, the server must set the Session Present flag in the CONNACK packet to 0 to let the client know that the session it expects does not exist. If the client wants to continue this network connection, it must discard its saved session state.

**When Clean Start is set to 1**, the client and server must discard any existing sessions and start a new one. Correspondingly, the server will also set the Session Present flag in the CONNACK packet to 0.

![MQTT Clean Start](https://assets.emqx.com/images/5aa78a5c038aacafdbd314930e060c67.jpg)

## Introduction to Session Expiry Interval

**Session Expiry Interval** is also located in the Variable Header of the CONNECT packet, but it is an optional [Property](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets). It is used to specify the maximum time that a session can be retained on the server after the network is disconnected. If the expiration time is reached but the network connection has not been restored, the server will discard the corresponding session state. It has three typical values:

1. **If this property is not specified or is set to 0**, the session will end immediately when the network connection is lost.
2. **Set to a value greater than 0**, indicating the number of seconds a session can last after a network connection is disconnected before it expires.
3. **When set to 0xFFFFFFFF**, which is the maximum value that the **Session Expiry Interval** property can be set to, it means that the session will never expire.

Each [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) can independently set its own **Session Expiry Interval**. We can flexibly set the expiration time according to actual needs. For example, some clients do not need a persistent session, and some clients only need to keep the session for a few minutes to avoid the impact of network fluctuations, while other clients may need to keep the session for a longer period of time.

MQTT also allows the client to update the **Session Expiry Interval** when disconnecting, which mainly relies on the property with the same name in the DISCONNECT packet. A common application scenario is that the client sets the **Session Expiry Interval** to a value greater than 0 when it goes online to avoid network interruptions that affect normal business. Then, when the client completes all business and actively logs off, the **Session Expiry Interval** is updated to 0, so that the server can release the session in time.

![MQTT Session Expiry Interval](https://assets.emqx.com/images/da0627af8aaeb1bd7ea152f0b0eeee39.jpg)

## Session and Client ID

The server uses the Client ID to uniquely identify each session. If the client wants to reuse the previous session when connecting, it must use the same Client ID as before. So when we use the function of automatically assigning Client ID at the server, the client must save the Assigned Client Identifier returned in the CONNACK packet for next use.

Note that protocol versions prior to MQTT 5.0 do not support the server returning an automatically assigned Client ID, so we have to choose between having the Client ID automatically assigned by the server and using persistent sessions

## Clean Session in MQTT 3.1.1

The session mechanism in MQTT 3.1.1 is far less flexible than 5.0. Because 3.1.1 has only one **Clean Session** field, and it has only two values, 0 and 1.

Setting **Clean Session** to 0 in MQTT 3.1.1 is equivalent to setting **Clean Start** to 0 in MQTT 5.0, and setting **Session Expiry Interval** to 0xFFFFFFFF, that is, the session will never expire.

Setting **Clean Session** to 1 in MQTT 3.1.1 is equivalent to setting **Clean Start** to 1 in MQTT 5.0, and setting **Session Expiry Interval** to 0, that is, the lifecycle of the session is consistent with the network connection.

![MQTT Clean Session](https://assets.emqx.com/images/4c5f9c5d6c0693d468441f1d2f81d6b0.jpg)

As we can see, in MQTT 3.1.1, there are only two options for the lifecycle of a session: never expire or be consistent with the network connection.

However, permanently storing sessions for all clients undoubtedly wastes resources on the server. This seems to be an omission in the protocol design of MQTT 3.1.1. Therefore, EMQX provided the `mqtt.session_expiry_interval` configuration item, which allows us to set a global session expiry interval for the MQTT 3.1.1 client so that we can control the resource consumption of the server within an acceptable range.

In addition, whether to create a new session is also forcibly bound to the lifecycle of the session. In MQTT 3.1.1, we must specify **Clean Session** 1 and 0 to connect once each to make the server create a brand-new, persistent session.

So compared to MQTT 3.1.1, MQTT 5.0 has huge improvements in sessions.

## Some practical suggestions for MQTT persistent session

In MQTT, we usually refer to sessions whose lifecycle is longer than the network connection as persistent sessions. However, there are some things we need to pay attention to when using persistent sessions.

For example, we need to correctly evaluate the impact of persistent sessions on server resources. The longer the session expires, the more storage resources the server may need to spend. Although the server usually does not cache messages for clients without limit. Taking [EMQX](https://github.com/emqx/emqx) as an example, the maximum number of messages that can be cached in each client session is 1000 by default, but considering the number of clients, this may still be an objective storage cost. If your server has limited resources, then you may need to be more careful with setting the session expiration time and the maximum cache of sessions.

In addition, we also need to evaluate whether it is necessary for the client to continue processing messages arriving during these offline periods after being offline for a long time. Of course, setting a larger cache to save as many messages as possible, or setting a smaller cache to allow the client to only process messages that have arrived recently, mainly depends on your actual scenario.

## Demo

1. Install and open [MQTTX](https://mqttx.app). In order to better demonstrate the session mechanism of MQTT, first we go to the settings page of MQTTX and turn off the `Auto resubscribe` function:

   ![MQTTX](https://assets.emqx.com/images/3c9de957f47a29255265e3c194f5c050.png)

2. Create a Client connection named `sub`, set MQTT Version to 5.0, enable **Clean Start**, set **Session Expiry Interval** to 300 seconds, then connect to the [Free Public MQTT server](https://www.emqx.com/en/mqtt/public-mqtt5-broker), and subscribe to the topic `mqttx_290c747e/test`:

   ![MQTTX New Connection](https://assets.emqx.com/images/2e21f2a679152c5a59d21ed8b5c26777.png)

3. Create a client connection named `pub` to publish messages to the topic `mqttx_290c747e/test`. The message content can be set arbitrarily. We will see that the client `sub` receives these messages. Then, we disconnect the client `sub` and continue to publish messages through the client `pub`:

   ![MQTTX publish messages](https://assets.emqx.com/images/46210f16fd8327e7ba968bb0cb2b18c0.png)

4. Next, we will disable the **Clean Start** option of the client `sub`, keep the **Session Expiry Interval** at 300 seconds, and then connect again. We will see the client `sub` receiving messages we published during its offline period:

   ![disable the Clean Star](https://assets.emqx.com/images/2b2aa5ec17a6ea935ebbc3d36fc0d7c2.png)

   ![connect again](https://assets.emqx.com/images/40129a8bb1eb363b7a6d8076f2673d4e.png)

The above is the ability of MQTT sessions to cache messages for offline clients. In the terminal interface, we can also use the command line tool [MQTTX CLI](https://mqttx.app/cli) to complete the above operations. We first use the following command to subscribe to the topic. After the subscription is successful, enter `Ctrl+C` in the terminal to disconnect the client:

```
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting...
✔  Connected
…  Subscribing to mqttx_290c747e/test...
✔  Subscribed to mqttx_290c747e/test
^C
```

Then publish a message to the topic `mqttx_290c747e/test` using the following command:

```
mqttx pub -h 'broker.emqx.io' --topic mqttx_290c747e/test --message "hello world"
```

After the publication is successful, restore the connection to the subscriber. Note that we keep the Client ID the same as before in the following command, and set the `--no-clean` option. We will see that the subscriber immediately receives the message we published before the connection:

```
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--no-clean --session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting...
✔  Connected
…  Subscribing to mqttx_290c747e/test...
payload: hello world 

✔  Subscribed to mqttx_290c747e/test
```

Whether [MQTTX](https://mqttx.app) or [MQTTX CLI](https://mqttx.app/cli) , as MQTT Client tools, their main purpose is to help everyone quickly get started with MQTT, so they do not provide some unnecessary features, such as viewing the Session Present returned by the server, and updating the **Session Expiry Interval** when disconnecting. So if you are interested in this part, you can get the corresponding Python sample code [here](https://github.com/emqx/MQTT-Feature-Examples) to learn more.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
