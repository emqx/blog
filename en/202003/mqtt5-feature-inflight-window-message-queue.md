###  Introduction to Inflight Window and Message Queue 

In order to improve message throughput efficiency and reduce the impact of network fluctuations, multiple unacknowledged QoS 1 and QoS 2 packets are allowed to exist on the network link at the same time by EMQ X broker. These packets that has been sent but unconfirmed will be stored in the inflight Window until the confirmation is completed.

When the simultaneously existing packets in the network link exceeds the limit, that is, the  Inflight Window reaches its length limit of the (see `max_inflight`), the EMQ X broker will no longer send subsequent packets, but will store these packets in the Message Queue. Once a packet is confirmed in the Inflight Window, the packets in the Message Queue will be sent in first-in, first-out order and stored in the Inflight Window.

When the client is offline, Message Queue is also used to store QoS 0 messages, which will be sent the next time the client is online. This feature is enabled by default, and you can also disable it manually, which can be seen in  `mqueue_store_qos0`.

It should be noted that if the Message Queue also reaches the length limit, subsequent packets will still be buffered to the Message Queue, but the first buffered message in the corresponding Message Queue will be discarded. If there are QoS 0 messages in the queue, the QoS 0 messages are discarded first. Therefore, it is very important to configure a suitable message queue length limit (see `max_mqueue_len`) according to your actual situation.

### Inflight Window and Receive Maximum

The CONNECT packet is added with a `Receive Maximum` attribute by the MQTT v5.0 protocol. The official interpretation of it is that *the client uses this value to limit the maximum quantity of published messages with QoS of 1 and QoS of 2 that the client is willing to process simultaneously. There is no mechanism to limit the published messages with a QoS of 0 that the server is trying to send.* That is to say, the server can send subsequent PUBLISH packets to the client with different packet identifiers while waiting for confirmation, until the number of unconfirmed packets reaches the `Receive Maximum` limit.

It is not difficult to see that `Receive Maximum` is actually the same as the Inflight Window mechanism in the EMQ X broker. However, before the MQTT v5.0 protocol was released, the EMQ X already provided this feature to the accessed MQTT client. Now, the clients with the MQTT v5.0 protocol will set the maximum length of the Inflight Window according to the specification of the Receive Maximum, while clients with earlier versions of the [MQTT protocol](https://www.emqx.com/en/mqtt) will still set it according to the configuration.



### Configuration Item

| Configuration Item | Type    | Optional          | Default                                    | Description                                                  |
| ------------------ | ------- | ----------------- | ------------------------------------------ | ------------------------------------------------------------ |
| max_inflight       | integer | >= 0              | 32 *(external)*,<br /> 128 *(internal)*    | Inflight Window length limit, 0 means no limit               |
| max_mqueue_len     | integer | >= 0              | 1000 *(external)*,<br />10000 *(internal)* | Message Queue length limit, 0 means no limit                 |
| mqueue_store_qos0  | enum    | true,<br /> false | true                                       | Whether EMQ X store QoS 0 messages to Message Queue when the client is offline |
