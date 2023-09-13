EMQX 5.0.16, 5.0.17, and 5.0.18 have recently been released, introducing multistream support for [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic). Along with this, EMQX Enterprise 4.3.19 and 4.4.15 are now complete and will be launched soon. These enterprise versions include adaptations to the latest version of HStreamDB and allow messages with the same properties to be forwarded to the same RocketMQ queue through the setting of the RocketMQ message producer delivery policy.

The team is currently working on developing a feature for large file transfers based on MQTT, and the primary development has been completed, with a PoC Demo conducted within the team. To help users start with EMQX more efficiently, the [EMQX 5.0 Document](https://www.emqx.io/docs/en/v5.0) has undergone review and refactoring.

## Introduce Multistream Support for MQTT over QUIC

EMQX utilizes the multiplexing feature of [QUIC](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) in v5.0.18 to enable multistream support for MQTT over QUIC.

Enabling multistream provides several improvements to message communication, including:

1. Separating connection control from message transmission.
2. Preventing queue blocking between topics by allowing each topic to have an independent stream.
3. Decoupling control plane stream and data plane stream.
4. Distributing uplink data (publishing messages) and downlink data (receiving messages) to different channels, improving responsiveness.
5. Setting different streams for topics enables priority control of topics.
6. Improving client/server processing parallelism.
7. Enhancing robustness for MQTT data processing. Specifically, if an application terminates a single stream, it will no longer result in the closure of the entire connection.
8. Facilitating more fine-grained cooperative stream control at the receiving and sending sides, enabling more precise control of each stream and the entire connection.
9. Reducing application layer latency by allowing clients to send subscriptions and publish data packets without waiting for CONNACK.

## MQTT-based File Transmission Function Completed PoC Demo

EMQX has developed a file transmission function based on MQTT to enable the transmission of various files in IoT applications such as configuration, sensor data, media, and OTA upgrade packages.

Compared to HTTP/FTP, MQTT-based file transmission and message transmission use a unified technology stack, reducing development, maintenance, and security audit efforts. Overall stream control is achieved to avoid file transmission occupying a large amount of bandwidth, which could impact the transmission of business messages. In the future, EMQX will provide large file transfer capability based on MQTT over QUIC to ensure efficient and reliable file transfer in a weak network environment.

The MQTT-based file transmission function has completed its main development this month and includes features such as large file transfers in chunks, resumable transfer, and reliable transfer. An internal PoC Demo has been conducted, and further development and testing will be conducted before release.

## Adapt to the Latest Version of HStreamDB

EMQX's data integration feature now supports the latest version of HStreamDB, v0.13.0, which offers improved data write speeds and additional functions compared to the previous version (v0.8).

## Support Setting Producer Delivery Policy

To achieve data integration with RocketMQ, EMQX has the capability to act as a producer, delivering client messages and events to RocketMQ.

In previous versions of EMQX, RocketMQ's default polling algorithm was used for message delivery, which meant that messages were delivered to different queues. In the latest release, EMQX has added the ability to configure the producer delivery policy. This enables users to deliver messages with the same client ID, username, or topic to the same RocketMQ queue, which is particularly useful in scenarios that require sequential delivery and consumption of the same message type.

## Enhance Functionality

- A new generic TLS option, `hibernate_ After`, allows the TLS process to sleep after being idle for a specified period, reducing its memory usage. The default value for this option is 5 seconds.
- AuthZ rule topic now allows placeholders anywhere. For example, `{allow, {username, "who"}, publish, ["t/foo${username}boo/${clientid}xxx"]}`.
- The Alpine Docker image is no longer available. Although the Alpine image was previously used due to its small size, the current size of the Alpine Docker image for EMQX is larger than that of the conventional image based on Debian Slim, rendering it less useful.
- Prometheus now includes two new indicators, `live_Connections.count` and `live_Connections.max`, to count the number of active clients.
- The HTTP API now supports the Proxy Protocol and can obtain the real IP address of the client that initiated the HTTP request.

## Bug Fixes

We have addressed several known bugs, including the issue of exclusive topic deadlock and the problem of the Replican nodes not being able to manually join the cluster.

For a comprehensive list of updates and changes in each version, please refer to the update logs available at:

- [EMQX 5.0.16](https://www.emqx.com/en/changelogs/broker/5.0.16)
- [EMQX 5.0.17](https://www.emqx.com/en/changelogs/broker/5.0.17)
- [EMQX 5.0.18](https://www.emqx.com/en/changelogs/broker/5.0.18)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
