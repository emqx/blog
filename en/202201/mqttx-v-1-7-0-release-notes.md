Recently, MQTTX v1.7.0 was officially released by EMQ. From this version, MQTTX will further support many new features of [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), which is the most complete desktop test client tool that supports MQTT 5.0 in the world so far.

 
MQTTX website: [https://mqttx.app/](https://mqttx.app/) 

MQTTX v1.7.0 download: [https://github.com/emqx/MQTTX/releases/tag/v1.7.0](https://github.com/emqx/MQTTX/releases/tag/v1.7.0) 

Mac users can download it in the App Store: [https://apps.apple.com/us/app/mqttx/id1514074565?mt=12](https://apps.apple.com/us/app/mqttx/id1514074565?mt=12) 

Linux users can download it in Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![v1.7.0 interface overview](https://assets.emqx.com/images/5c6088dcd04edddd0bcf04895c030282.png)

v1.7.0 interface overview

## More comprehensive support for MQTT 5.0

In 1.7.0, MQTTX adds a lot of support for the property configuration of MQTT 5.0, making it the most complete MQTT desktop client tool among similar tools that supports MQTT 5.0.

To use and test the features of MQTT 5.0, MQTTX v1.7.0 needs to be used with MQTT Broker that supports MQTT 5.0.

Cloud-native distributed [MQTT broker - EMQX](https://www.emqx.io) supports the MQTT 5.0 protocol since version 3.0. It is the first broker in the open-source community to support this protocol specification and is fully compatible with MQTT 3.1 and 3.1.1 protocols. Connecting to EMQX by Using MQTTX, you can quickly use and test the features of MQTT 5.0.

### Support MQTT 5.0 User Properties

In the new version, the configuration of user properties is supported firstly. [User Properties](https://www.emqx.com/en/blog/mqtt5-user-properties) is a handy feature in MQTT 5.0. It is a custom property that allows users to add their metadata to MQTT messages and transfer additional custom information to expand more application scenarios. If you are familiar with the HTTP protocol, this function is very similar to the concept of HTTP Header.

We can configure user properties when creating client connections and publishing messages.

### Extend other properties of MQTT 5.0

In addition to configurable user properties, version 1.7.0 also extends other properties configuration for client connection and message publishing.

When publishing a message, you can configure the Content-Type, specify the Payload Format Indicator to describe the format of the content of the application message, and specify that the message content is a UTF-8 encoded string.

It supports the property configuration of Topic Alias, effectively saving bandwidth and computing resources.

It supports request responses in MQTT 5.0 and provides Response Topic and Correlation Data to control the response message to be routed back to the publisher of the request.

### Support MQTT 5.0 subscription option

Subscription options are supported in this release. The settings of No Local flag, Retain as Published flag, and Retain Handling are also supported. During the test, you can use these subscription options to change the behavior of the server.

In subsequent versions, we will continue to support new features in MQTT 5.0, such as a Subscription identifier.

 

## Smoother using experience

### One-click multi-topic subscription

In the previous release, we can only subscribe to one topic each time when we open the pop-up box for subscribing. For users who want to subscribe to multiple topics, they need to open and close the box multiple times to subscribe to multiple topics, which is not very convenient. Therefore, in the new version, we have optimized it to support subscribing to multiple topics at a time, which reduces users' repeated operations.

### Disable automatic scrolling of messages

The control of automatic scrolling of the message list when receiving and publishing messages were added to the v1.7.0 setting. The auto-scroll function is applicable to help users view the latest messages when the message receiving rate is slow. When the rate of receiving messages is too fast, users can click to turn off this function to view some old messages sent or received.

> Note: When the auto-scroll function is turned off, the performance of sending and receiving messages can be improved.

### Sync with the OS theme(macOS only)

MQTTX currently supports three theme modes of Light, Dark, and Night, which need to be switched manually before. In the new version, this was optimized. When the system theme of the operating system changes, MQTTX can automatically switch the theme. When the macOS system topic is Dark Mode, MQTTX will automatically switch to the Night mode.

### International expansion

With the help of the community, the international expansion of MQTTX has gone further. In addition to supporting simplified Chinese, English, Japanese, and Turkish, we implemented Hungarian language support in version 1.7.0 with the help of a Hungarian contributor.

More community partners are welcome to participate and contribute to building a better MQTTX with us.

## More refined product improving

### Fix and optimization

In addition to the above new features, it also fixes many known issues in this update, and the stability has been further improved.

- Fix the synchronization issue of auto resubscribe
- Fix the issue of importing/exporting data
- Fix the issue that the created connection cannot be edited
- Fixed the issue of certificate expiration error during SSL/TLS connection
- Fix the issue that the history message record cannot be deleted
- Fix the issue of Base64 conversion
- Fix the issue of not being able to create a new window
- Fix the issue of disorder when connecting the connection list

## Product Roadmap

MQTTX is still in the process of continuous enhancement and improvement, to bring more practical and powerful functions to users and facilitate the testing and development of IoT platforms.

Next, we will focus on the following aspects:

- More complete support for MQTT 5.0
- Plug-in system (for example, support SparkPlug B)
- MQTT Debug function
- Script function optimization

## Conclusion

MQTTX is designed to connect to test MQTT Brokers such as EMQX. The one-click connection and a clean graphical interface make it easy to explore and debug MQTT features. MQTTX provides comprehensive testing capabilities for MQTT features. Fully open-source and community-driven makes it integrated with more rich, powerful, user-friendly features. With MQTTX and EMQX - the cloud-native distributed messaging broker, we believe that the test and development of IoT platforms will become easier.

The MQTTX project is completely open-source. You can go to [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) to submit the problems encountered during use, or fork the MQTTX project to submit a revised PR to us. We will review and deal with it in time. We would also like to thank all users in the community for their contributions and feedback. The use and affirmation of each community user is the driving force for the advancement of our products.
