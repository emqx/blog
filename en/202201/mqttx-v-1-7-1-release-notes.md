[MQTT X](https://mqttx.app/) is a fully open-source cross-platform MQTT 5.0 desktop client open-sourced by [EMQ](https://www.emqx.com/en), It supports macOS, Linux, and Windows systems. Makes it easy and quick to create multiple simultaneous online MQTT client connections, test the connection, publish, and subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket as well as other [MQTT protocol](https://www.emqx.com/en/mqtt) features.

> MQTT X website: [https://mqttx.app/](https://mqttx.app/)
>
> MQTT X v1.7.1 download: [https://github.com/emqx/MQTTX/releases/tag/v1.7.1 ](https://github.com/emqx/MQTTX/releases/tag/v1.7.1 )
>
> Mac users can download it in the App Store: [https://apps.apple.com/us/app/mqttx/id1514074565?mt=12](https://apps.apple.com/us/app/mqttx/id1514074565?mt=12)
>
> Linux users can download it in Snapcraft: [https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![MQTT X](https://assets.emqx.com/images/ed504e3746e5b9d67360ccd359d463df.png)

## New Features Preview

### Support MQTT 5.0 Subscription Identifier

In this release, in addition, to supporting [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) subscription options, we have added support for [Subscription Identifiers](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options), we can specify a Subscription Identifier when subscribing. The broker will establish and store the mapping relationship between this subscription and the Subscription Identifier when successfully creating or modifying the subscription. The broker will return the Subscription Identifier associated with this PUBLISH packet and the PUBLISH packet to the client when needed to forward PUBLISH packets matching this subscription to this client.

![MQTT 5.0 Subscription Identifier](https://assets.emqx.com/images/d7fe5b3b7611351c1e2b21d42e181108.png)

### Expose more MQTT 5.0 properties on display

In this release, we have optimized the display of properties in MQTT 5.0. In addition to displaying User Properties, we also support displaying the Content Type, Subscription Identifier, Topic Alias, Response Topic, and Correlation Data contained in the message box when sent and received, as well as optimizing the display of User Properties.

![MQTT 5.0 properties](https://assets.emqx.com/images/f06ec9b6d35c81f256913f244cd128f2.png)

### Support Edit/Disable/Enable Topics

This release continues to optimize the operation of the Topic. Before version 1.7.1, the list of topics can only be added and deleted, when the subscribed Topic is too long, when you need to modify it, you can only delete and unsubscribe, and then re-subscribe, which is not very convenient, especially for modifying individual words or separators.

At the same time, this version also supports disable/enable Topic, when subscribed to too many Topic, sometimes not all the Topic messages want to receive, but to avoid subscribing to the same topic again, this version provides a disable function, need to receive the message of the Topic again, just enable again.

Use: Right-click on the subscribed Topic list item, in the context menu we can quickly choose to edit, disable or enable the operation.

![Edit/Disable/Enable MQTT Topics](https://assets.emqx.com/images/f508a287cf7275542e8e64989e017998.png)

### Others

- Add sync the os theme switch button. When this switch is turned on, the system theme colors will be synchronized with the OS theme.
- Linux Flathub deployments from community support. Linux users can also go to [https://flathub.org/apps/details/com.emqx.MQTTX](https://flathub.org/apps/details/com.emqx.MQTTX) for download and installation
- Update loading app page

## More refined product improving

### Fix and optimization

In addition to the above new features, it also fixes many known issues in this update, and the stability has been further improved.

- Fix pass the `__ob__` field to user properties
- Fix client id is unique in the database
- Fix it can not send empty Topic when using Topic Alias
- Fix resub can not sync all subscriptions data
- Fix collection importing issue
- Fix sync auto-resub
- Fix new window issue
- Fix it can not display offline messages

## Product Roadmap

MQTT X is still in the process of continuous enhancement and improvement, to bring more practical and powerful functions to users and facilitate the testing and development of IoT platforms.

Next, we will focus on the following aspects:

- More complete support for MQTT 5.0
- Plug-in system (for example, support SparkPlug B)
- MQTT Debug function
- Script function optimization

## Conclusion

MQTT X is designed to connect to test MQTT Brokers such as EMQX. The one-click connection and a clean graphical interface make it easy to explore and debug MQTT features. MQTT X provides comprehensive testing capabilities for MQTT features. Fully open-source and community-driven makes it integrated with more rich, powerful, user-friendly features. With MQTT X and EMQX - the cloud-native distributed messaging broker, we believe that the test and development of IoT platforms will become easier.

The MQTT X project is completely open-source. You can go to [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) to submit the problems encountered during use, or fork the MQTT X project to submit a revised PR to us. We will review and deal with it in time. We would also like to thank all users in the community for their contributions and feedback. The use and affirmation of each community user is the driving force for the advancement of our products.
