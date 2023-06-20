[MQTTX](https://mqttx.app) is a cross-platform MQTT 5.0 desktop test client provided by the world's leading open source IoT middleware provider  [EMQ](https://www.emqx.com/en) , which supports macOS, Linux, Windows. The user interface of **MQTTX** simplifies the operation logic of the page with the pattern of chatting software. Users can quickly create multiple simultaneous-online **MQTT clients** to test the connection/publish/subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket and other **MQTT protocol** features.

MQTTX website: https://mqttx.app

MQTTX v1.3.0 download link: https://github.com/emqx/MQTTX/releases/tag/v1.3.0

![mqttxpreview.png](https://assets.emqx.com/images/d796340f0486ecccdada4a8e1962635b.png)

## Overview of the new features

- Support [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)

  In this version, WebSocket connection support function is added. In the new connection page, the drop-down box in front of  `Host`  can be used to select the connection protocol, which supports ` mqtt:// `,` ws:// `, if  ` SSL/TLS` authentication connection is used, you need to select `mqtts://`, `wss://`. When the protocol option is `ws` or ` wss`, the connection created is a WebSocket connection.

   **Note:** When the protocol changes, you need to modify the connection port.

   ![2.png](https://assets.emqx.com/images/ac6eefd1e7f676bad67de6aab72d5c83.png)

- The format conversion of Payload is supported

  In this version, the input box of Payload has been optimized during input editing. The functions of syntax highlighting and format verification for the JSON format are realized so that users can easily input JSON content in the input box. At the same time, in the Payload option above the Topic input box, you can also quickly convert the format of current content to other formats. Currently it supports conversion format of `Base64`,` Hex`, `Plaintext`, and ` JSON`. Users can perform conversion operations according to their needs.

![3.png](https://assets.emqx.com/images/a0844e5ee2c2a170072f9f55f1414b67.png)

- The height of the input box can be adjusted freely

  In the previous version, the height of the input box was fixed, and the Payload content that the user could see when using it was limited. If too much content was sent, the operation of input and editing in the input box could not be performed well. After optimization, users can place the mouse on the top of the input box, and when the arrow appears, drag the mouse to freely adjust the height of the input box to facilitate better processing of the Payload content.

![4.png](https://assets.emqx.com/images/3953f2e1128eaa408db27a0a71c60cce.png)

- Fuzzy query for the Topic is supported

  In the previous version, only precise search for the Topic is supported, and only messages under the same Topic were searched. Currently, fuzzy query is supported, which can search and filter a wider range of Topic messages. We will continue to optimize the function of distinguishing and displaying messages by Topic, and it is coming soon.

- In the pop-up box for adding Topic, the Enter key can be used as a shortcut to quickly add subscriptions.

- MQTT maximum reconnection is added in settings

- When the connection is successful and the top panel is automatically folded, you can click the red button on the top bar to quickly disconnect

- Certificate selection is optimized , which supports to select more certificate format files.

This project is completely open sourced. If you have any questions during use, you can go to [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) to submit your questions and opinions, or Fork our MQTTX project, and submit the revised PR to us. We will carefully review and respond shortly.
