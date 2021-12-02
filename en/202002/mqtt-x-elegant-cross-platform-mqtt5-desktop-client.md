**MQTT X** is a cross-platform MQTT 5.0 desktop client open sourced by the world's leading open source IoT middleware provider [EMQ](https://github.com/emqx/emqx), which supports macOS, Linux, Windows. The user interface of **MQTT X** simplifies the operation logic of the page with the help of chatting software. The user can quickly create a connection to save and establish multiple connection clients at the same time. It is convenient for the user to quickly test the connection of MQTT/TCP、MQTT/TLS, Publish / Subscribe functions and other features .

Project address: [GitHub](https://github.com/emqx/MQTTX)

Website: [MQTT X Website](https://mqttx.app)
![WX202002101233322x.png](https://static.emqx.net/images/b0cfa74c62c6425e67c1547f4760f1a6.png)

MQTT X is suitable for users who are building their own MQTT message server to test connections, subscribing and publishing messages, etc. When using a client, the user can be either a publisher or a subscriber. It is also applicable to related users who are developing or researching MQTT Broker. In the research and application of MQTT, no matter what stage you are in, you can quickly and deeply understand the relevant characteristics of the MQTT protocol through MQTT X.

This project is completely open source, which uses Vue.js + TypeScript + Electron technology stack for development. You can view and browse the project source code on  [GitHub](https://github.com/emqx/MQTTX). Welcome to discuss and learn Electron project development technology together.

The following is a preview of the features and interface of MQTT X:

- Cross-platform, support Windows, macOS, Linux
- Fully support MQTT v3.1.1 and MQTT v5.0 protocols
- Support CA, self-signed certificate, and single and two-way SSL / TLS authentication
- Multi-theme, theme switching between Light, Dark and Night (Purple).
- Color tags can be customized when subscribing to topics
- Support Simplified Chinese and English
- Supports MQTT / TCP  connections and MQTT / WebSocket connections
- Support auto-subscription of $ SYS topic and can be expanded hierarchically
- Support multiple payload formats of Hex, Base64, JSON, Plaintext
- Simple and clean graphical interface

![mqttxpreview.png](https://static.emqx.net/images/c2ceb11b3c0eae3e421ad63ba721c148.png)

In the main window of MQTT X, the far left is the menu bar, which corresponds to  the connection page, the about page, and the settings page from top to bottom; the middle column is the list of existing connections. After each connection is created, the new connection will appear in the list. User can click on the name in the list (composed of `name @ host: port`) to quickly switch the connection; The rightmost side is the main view interface of the connection, and you can test sending and receiving messages on this page. When the connection is successfully established, the top configuration bar will automatically collapse to show more page space.

- MQTT X is a newly released product that uses Electron cross-platform technology, with beautiful interface and low resource occupation. MQTT X changes the common single client mode in interaction, allowing to save multiple connection information;
- It is easy to use, can quickly create connections, and provides a more comprehensive MQTT parameter configuration, so that users can respond to simulation test of any use scenario and pattern, including support for MQTT v5.0;
- It can send and receive messages in the form of message chat. The interaction process is simple and easy to understand. It allows multiple clients to connect at the same time and freely switch to communicate with each other. It has better interaction and greatly improves the efficiency of interactive debugging;
- It is fully open-source and supports multiple platforms.

![666.png](https://static.emqx.net/images/336b2cd915c0e9ef8ebbe3467270ee76.png)

As of now, MQTT X has released the v1.2.3 version, and more features are still being developed.
