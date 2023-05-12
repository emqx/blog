[MQTTX](https://mqttx.app/) is a fully open-source cross-platform [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) desktop client open-sourced by [EMQ](https://www.emqx.com/en), It supports macOS, Linux, and Windows systems. Makes it easy and quick to create multiple simultaneous online MQTT client connections, test the connection, publish, and subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket as well as other MQTT protocol features.

> MQTTX website: [https://mqttx.app/](https://mqttx.app/)
>
> MQTTX v1.7.2 download: [https://github.com/emqx/MQTTX/releases/tag/v1.7.2](https://github.com/emqx/MQTTX/releases/tag/v1.7.2)
>
> Mac users can download it in the App Store: [https://apps.apple.com/us/app/mqttx/id1514074565?mt=12 ](https://apps.apple.com/us/app/mqttx/id1514074565?mt=12)
>
> Linux users can download it in Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![MQTTX](https://assets.emqx.com/images/cf2e677ede2b5fd5eb7aece9c88c68d0.png)

## New Features Preview

### Shared subscriptions support topic color markers

Shared Subscriptions also support color markers, and when using [Shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), MQTTX can also distinguish which shared subscription the current message comes from by customizing the topic color.

![Shared subscriptions](https://assets.emqx.com/images/1624a13546e46f143d02d2ebe608c580.png)

### Add more ARM builds

In this release, we have added some new builds that can be used on ARM64 architectures. For macOS and Linux users, you can download the corresponding builds for any architecture. To use ARM64 builds, you need to go to [GitHub](https://github.com/emqx/MQTTX/releases/tag/v1.7.2) or [Official Downloads](https://www.emqx.com/en/downloads/MQTTX/v1.7.2) to find a package with the arm64 suffix to download and use.

![MQTTX add more ARM builds](https://assets.emqx.com/images/769872da8aba8f6d15f8a4204c38b98f.png)


### Support set reconnect period

When creating or editing a connection, this release optimizes the reconnection section. When setting a connection to be automatically reconnected, we can also configure the time interval between each reconnection, that is, the reconnection period, which is 4000ms by default, note that the unit here is milliseconds.

![Support set reconnect period](https://assets.emqx.com/images/877a23bc42e70c28cd932e04fecbf4d4.png)
 

## Fix and optimization

In addition to the above new features, it also fixes many known issues in this update, and the stability has been further improved.

- Fix new topic instead of the subscribed topic
- Message box width adaption
- Enhanced security

## Product Roadmap

MQTTX is still in the process of continuous enhancement and improvement, to bring more practical and powerful functions to users and facilitate the testing and development of IoT platforms.

Next, we will focus on the following aspects:

- More complete support for MQTT 5.0
- Plug-in system (for example, support SparkPlug B)
- MQTT Debug function
- Script function optimization

## Conclusion

MQTTX is designed to connect to test MQTT Brokers such as [EMQX](https://www.emqx.io). The one-click connection and a clean graphical interface make it easy to explore and debug MQTT features. MQTTX provides comprehensive testing capabilities for MQTT features. Fully open-source and community-driven makes it integrated with more rich, powerful, user-friendly features. With MQTTX and EMQX - the cloud-native distributed messaging broker, we believe that the test and development of IoT platforms will become easier.

The MQTTX project is completely open-source. You can go to [Github](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) to submit the problems encountered during use, or fork the MQTTX project to submit a revised PR to us. We will review and deal with it in time. We would also like to thank all users in the community for their contributions and feedback. The use and affirmation of each community user is the driving force for the advancement of our products.
