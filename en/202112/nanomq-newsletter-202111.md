In November, the NanoMQ team focused on adding MQTT support to NNG, and also fixing issues for  NanoMQ.

## NanoMQ updates

1. The log print output of the configuration file was optimized. It will automatically determine whether to output alarm information according to the condition whether the configuration file path is specified.
2. Bugfix: when the client subscribes to multiple topics in batch, NanoMQ cannot forward the message with the correct subscription QoS level.

## NNG now supports MQTT

NanoMQ is an open-source project jointly developed by EMQ and NNG. There is a sub-module of NNG in the GitHub repository of NanoMQ, which is maintained independently as the NNG version of NanoMQ ([https://github.com/nanomq/nng/tree/master](https://github.com/nanomq/nng/tree/master)). At present, its master branch is a special version developed and optimized for NanoMQ Broker and maintained independently, from which we have submitted several valuable PRs and Issues for NNG. However, it is not compatible with the SP protocol of nanomsg for now.

Therefore, to make NanoMQ compatible with NNG's SP protocol, we are committed to adding MQTT 3.1.1 protocol support for NNG this month. So that the two kinds of protocols(MQTT and SP) can be used together with NNG in the future. This is also in accordance with the RoadMap direction previously formulated by NanoMQ team.

According to the technical goals previously formulated with the NNG project maintainer - Garrett at the jointly open-source cooperation meeting, NNG will support ZeroMQ and MQTT 3.1.1/5.0 in the future. After a month of hard work, we have completed the development of support for MQTT 3.1.1 protocol for NNG and named it NanoSDK. The internal design of NanoSDK honors the programming style of the NNG framework and is compatible with the original SP protocol of NNG. At the same time, it does not affect the other features like HTTP/Websocket/TLS.

Compared with other popular MQTT 3.1.1 SDK, NanoSDK has the following advantages:

**1. Fully asynchronous I/O and good SMP support**

NanoSDK based on NNG's asynchronous I/O, we implement the Actor-like programming model in C language. And managing to distribute the computation load among multiple CPU cores averagely.

**2. High compatibility and portability**

Inheriting the compatibility and easy portability of NNG, NanoSDK only relies on the native POSIX standard API and is friendly to various distributions of Linux. It can be migrated to any hardware and operating system platform easily.

**3. Support multiple API styles**

The programming style of the NNG framework comes with a high learning cost, and users need to have a deep understanding of the concept of AIO and Context. Therefore, we also prepared a traditional callback registration mechanism for users who are accustomed to using Paho and Mosquitto SDK. This not only reduces the programming difficulty but also reserves the advantages of NNG.

**4. High throughput** **&** **Low latency**

In NanoMQ's test report, its performance advantages of powerful high throughput and low latency have been reflected, and the direct successor of NanoMQ -  the SDK also has excellent performance. It is cost-effective in terms of resources consumption. Unlike the traditional MQTT SDK which has only 1-2 threads, NanoSDK can make full use of system hardware resources to provide higher consumption throughput.

In most IoT solutions based on EMQX, the backend service’s insufficient consuming capability always results in message congestion, which has always been a problem for open source developers. Especially for QoS 1/2 messages, most SDKs reply Ack for QoS 1/2 messages synchronously. NanoSDK provides asynchronous Ack capability under the premise of ensuring the QoS message sequence and message retransmission mechanism, which greatly improves the throughput and consumption capacity of QoS 1/2.

## Attachment: performance test comparison report between NanoSDK and Paho C MQTT SDK

We selected the most widely used Paho C MQTT SDK and NanoSDK for performance comparison tests.

### Test environment

- Quad-Core model: 11th Gen Intel Core i7-1165G7
- 16G memory
- 500K PUBLISH message with 2 bytes payload

### Test scenario logic

The scenario is to establish a client to connect to the EMQX broker and complete the sending and receiving of 50,000 QoS 0/1/2 messages (both only count the total time spent on reading sockets to calculate the message rate). In order to get close to most real business scenarios, we use the Emqtt_bench tool to send a 2-byte message to this client. Each time the client receives a message, it will reply with a 14-byte Publish message. The client sends and receives a message each time. The two testing results are consistent except for the used SDK.

### Test result

The specific time may be slightly different for each test.

| Qos  | NanoSDK（NNG） | Paho C MQTT |
| :--- | :------------- | :---------- |
| 0    | 2946 msg/s     | 2944 msg/s  |
| 1    | 2944 msg/s     | 610 msg/s   |
| 2    | 2919 msg/s     | 585 msg/s   |

It can be seen that in the case of a single client in a multi-core platform, NanoSDK has a huge advantage in QoS 1/2 scenario. At the same time, since NanoSDK implements the Actor-like programming model of MQTT in C language based on NNG, the implementation of fully asynchronous I/O can well distribute the computation load to multiple CPU cores. Developers can start multiple MQTT connections according to our Context routine configuration to achieve a higher consumption capacity of QoS 0, instead of worrying about multi-threaded concurrent development.

 
In December, the NanoMQ team plans to hold an open-source development meeting with Garrett, the maintainer of the NNG project, discussing how to merge the projects of both parties. Everyone is welcome to try [nng-mqtt](https://github.com/nanomq/nng/tree/nng-mqtt) forked by NanoMQ in the NNG repository.
