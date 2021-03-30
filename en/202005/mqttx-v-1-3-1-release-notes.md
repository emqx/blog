[MQTT X](https://mqttx.app/) is a cross-platform **MQTT 5.0** client tool open-sourced by [EMQ](https://emqx.io/ ), supports macOS, Linux, Windows. The user interface of MQTT X simplifies the operating logic with the help of the chat software format. Users can quickly create multiple simultaneous online **MQTT client** to facilitate testing the connection/publishing/subscribing of MQTT / TCP, MQTT / TLS, MQTT / WebSocket, and other **MQTT protocol** features.

MQTT X website: [https://mqttx.app](https://mqttx.app/)

Download MQTT X v1.3.1: [https://github.com/emqx/MQTTX/releases/tag/v1.3.1](https://github.com/emqx/MQTTX/releases/tag/v1.3.1)



## Preview the new features

- Support for more attributes of MQTT 5.0 

  This version adds the configuration for `Topic Alias Maximu ` MQTT 5.0 attribute. It is the maximum value of the topic alias, which means that the client sent by the server will be accepted as the maximum value of the topic alias. Users select the version of MQTT protocol as 5.0 when establishing a connection and then they can configure this item. 

	![mqttxtopicaliasmax.png](https://static.emqx.net/images/23cc2d0d8c7130f32f5fbbd38781db62.png)

- Implement filtering messages through click the already subscribed topic projects

  For the previous versions, all subscribed messages will be displayed in the same view. If users subscribed to multiple message topics, it will be very inconvenient to view. In the latest version, users can click the subscribed items in the subscription list on the left to implement filtering messages. After clicking, the message view will only display the message content of subscribing the current topic. Click again to cancel filtering.

	![mqttx-topic-messages.png](https://static.emqx.net/images/d8dd29376bdbeb320597694c4c22576a.png)

- Support for quickly copy topic information after clicking the topic name

  After successfully adding a topic, users can click the topic name in the subscribed list to quickly copy the information of the current topic. When the user needs to send messages to this topic, just quickly paste it into the topic input box in the message bar for modifying, then you can quickly finish this operation.

	![mqttx-topic-copy.png](https://static.emqx.net/images/8e09355380e767a1b7cdfe419dd876a8.png)

- Add an enable item of strict validate certificate 

  When creating a TLS/SSL secure link, the select certificate card has added the option enable `strict validate certificate `. When enabling this option,  a more complete certificate validation link will be enabled. It is recommended that enable this option when users need to test the formal environment.

	![mqttx-tls.png](https://static.emqx.net/images/325142f5c6400918525bf2071e29921c.png)



## Optimize and repair

- Allow directly sending messages in the message box
- Fixed the issue that the client received repeated messages 
- Fixed the issue of verification certificate failure



This project is completely open source, you can submit the problems you met when using it to [MQTT X GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc), or submit the modified PR to the project Fork MQTT X. We will view and deal with it in time.

