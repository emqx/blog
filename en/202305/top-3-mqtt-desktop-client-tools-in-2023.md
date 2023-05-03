## Introduction

With the rise of MQTT as a standard messaging protocol for the Internet of Things (IoT), the MQTT desktop client is becoming an essential tool for developers to debug, test and develop IoT applications.

This blog post will explore the top 3 MQTT desktop clients in 2023 based on their features, project activity, and user experience.

- MQTTX
- MQTT Explorer
- MQTT.fx

## Comparison At a Glance

First, we compare the 3 top MQTT desktop clients in the following chart.

|                                      | **MQTTX**                                                    | **MQTT Explorer**                                            | **MQTT.fx**                 |
| :----------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :-------------------------- |
| **License Mode**                     | Open Source (Apache License 2.0)                              | Open Source (CC BY-ND 4.0)                                   | Commercial                  |
| **GitHub Project**                   | [MQTTX GitHub](https://github.com/emqx/mqttx)                | [MQTT-Explorer GitHub](https://github.com/thomasnordquist/MQTT-Explorer) | N/A                         |
| **GitHub Stars**                     | 2.6k                                                         | 2.3k                                                         | N/A                         |
| **Latest Release**                   | [v1.9.2](https://github.com/emqx/MQTTX/releases/tag/v1.9.2) (Apr 29, 2023) | [0.4.0-beta1](https://github.com/thomasnordquist/MQTT-Explorer/releases/tag/0.0.0-0.4.0-beta1) (Apr 28, 2020) | N/A                         |
| **MQTT 5.0 Support**                 | Yes                                                          | Yes                                                          | Yes                         |
| **MQTT Connectivity**                | Excellent                                                    | Good                                                         | Moderate                    |
| **MQTT over TCP**                    | Yes                                                          | Yes                                                          | Yes                         |
| **MQTT over TLS/SSL**                | Yes                                                          | Yes                                                          | Yes                         |
| **MQTT over WebSocket (WS)**         | Yes                                                          | Yes                                                          | No                          |
| **MQTT over Secure WebSocket (WSS)** | Yes                                                          | Yes                                                          | No                          |
| **Multiple Connections**             | Yes                                                          | No                                                           | No                          |
| **Authentication (SSL)**              | Excellent                                                    | Good                                                         | Good                        |
| **Payload Format/Codec**             | Hex, Base64 and JSON                                         | JSON                                                         | N/A                         |
| **User Interface**                   | Excellent (chat style)                                       | Good (topic tree)                                            | Moderate                    |
| **Ease of Use**                      | Excellent                                                    | Good                                                         | Good                        |
| **Compatibility**                    | Good                                                         | Good                                                         | Good                        |
| **Community Support**                | Excellent                                                    | Moderate                                                     | Moderate                    |
| **Pricing**                          | Free                                                         | Free                                                         | Start from € 49,90 inc. VAT |

## Free Public MQTT Broker

Before diving into the MQTT client desktop tools, we need an [MQTT broker](https://www.emqx.io/) to communicate and test. We choose the free public MQTT broker available on `broker.emqx.io`.

>**MQTT Broker Info**
>
>- Server: broker.emqx.io
>- TCP Port: 1883
>- WebSocket Port: 8083
>- SSL/TLS Port: 8883
>- Secure WebSocket  Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

<section class="promotion">
    <div>
        Try Serverless MQTT Broker
        <div class="is-size-14 is-text-normal has-text-weight-normal">Get forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Start Free →</a>
</section>

## 1. MQTTX

[MQTTX](https://mqttx.app/) is an elegant cross-platform MQTT 5.0 desktop client that runs on macOS, Linux, and Windows. Its user-friendly chat-style interface enables users to easily create multiple MQTT/MQTTS connections and subscribe/publish MQTT messages.

MQTTX fully supports MQTT versions 5.0 and 3.1.1, MQTT over TLS, MQTT over WebSocket, and one-way and two-way SSL authentication. In addition to these essential features, MQTTX offers advanced functionality, such as customizable scripts for [MQTT Pub/Sub](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) simulation and support for codecs like Hex, Base64, and JSON payloads.

MQTTX is an open-source project developed with [Electron](https://www.electronjs.org/) and maintained by the [EMQX team](https://github.com/emqx). The latest release is version 1.9.2 by the end of April 2023.

Official Website: [https://mqttx.app/](https://mqttx.app/) 

GitHub Project: [https://github.com/emqx/mqttx](https://github.com/emqx/mqttx) 

![MQTT Desktop Client - MQTTX](https://assets.emqx.com/images/95bfe7f0779416da02c27e9ba7a0a09c.png)

### Features

- User-friendly and easy-to-use UX design
- Chatbox for sending/receiving MQTT messages
- Fully support for MQTT versions 5.0 and 3.1.1
- Support MQTT over TLS, and [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- Support for one-way and two-way SSL authentication
- Hex, Base64, JSON, and Plaintext payload codec
- Customized colors for different MQTT subscriptions
- Customized script for MQTT Pub/Sub scenario simulation
- Cross-platform, running on Windows, macOS, and Linux

### **Homebrew**

```
brew install --cask mqttx
```

### **Download**

- [https://mqttx.app/](https://mqttx.app/) 
- [https://github.com/emqx/MQTTX/releases](https://github.com/emqx/MQTTX/releases) 

### User Experience

MQTTX offers a great user experience with a clean, intuitive chat-style interface and support for advanced features.

## 2. MQTT Explorer

MQTT Explorer is an open-source MQTT client tool that provides an easy-to-use graphical user interface (GUI) with a structured topic overview. It adopts a hierarchical main view and supports a visual chart display of received payload messages. 

MQTT Explorer supports MQTT 5.0 and 3.1.1 protocols and allows developers to simultaneously create one MQTT/MQTTS connection.

MQTT Explorer is written in Typescript and developed by [Thomas Nordquist](https://github.com/thomasnordquist). It’s cross-platform and can run on Windows, macOS, and Linux. It’s a pity that the project has been out of development since the last release of version 0.4.0-beta1 on April 28, 2020.

Official Website: [https://mqtt-explorer.com/](https://mqtt-explorer.com/) 

GitHub: [https://github.com/thomasnordquist/MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer) 

![MQTT Explorer](https://assets.emqx.com/images/fd34faa00ea66d846bfd0a9d99040359.png)

### Features

> Quote from [MQTT Explorer](http://mqtt-explorer.com/) 

- Visualize topics and a dynamic preview of the change of topic
- Delete the retained topics
- Search/filter topics
- Recursive delete topics
- Difference view of current and previously received messages
- Publish topics
- Draw digital topics
- Retain the historic record of every topic
- Dark/Light topic

### Download

- [https://mqtt-explorer.com/](https://mqtt-explorer.com/) 
- [https://github.com/thomasnordquist/MQTT-Explorer/releases](https://github.com/thomasnordquist/MQTT-Explorer/releases) 

### User Experience

MQTT Explorer offers an impressive experience with a user-friendly GUI, structured topic tree, and payload data visualization.

## 3. MQTT.fx

Developed by Softblade GmbH, MQTT.fx is a commercial client tool commonly used to test IoT routes during development. It supports MQTT versions 3.1.1 and 5.0 and provides advanced features such as TLS/SSL encryption and extensive configuration options for [MQTT connections](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).

However, while MQTT.fx has many powerful features, and it has some limitations to consider. For example, it only allows users to establish one MQTT connection at a time and lacks support for MQTT over WebSocket.

MQTT.fx is written in JavaFX and provides native installation packages for platforms including Windows, MacOS, and Linux. The price of MQTT.fx starts from **€ 49,90 inc. VAT**, with a 3-month free trial period.

**Official Website:**

[https://softblade.de/en/welcome/](https://softblade.de/en/welcome/) 

![MQTT.fx](https://assets.emqx.com/images/1a8b56d846e551d216844a79dea219ca.png)

### Features

- Predefined message template
- Easy monitoring of broker status through system topic `$SYS`
- Support for JavaScript scripts through Nashorn Engine
- Support log display, display log information in the connection
- Cross-platform desktop with support for Windows, macOS, and Linux

### Download

- [https://softblade.de/en/download-2/](https://softblade.de/en/download-2/) 

### User Experience

MQTT.fx provides a good user experience with an intuitive GUI with rich features. You can download the trial version and try it out for yourself.

## Conclusion

In summary, a desktop client is critical for troubleshooting and developing MQTT. However, while MQTT Explorer is no longer maintained and MQTT.fx is a commercial and expensive option, other alternatives are available.

Among these, the [MQTTX](https://mqttx.app/) open-source project stands out as a fast-growing client tool that offers a modern chat-style interface, full MQTT 5.0 support, and a rich set of features that provides a great user experience. As a result, MQTTX is a top pick for the best MQTT desktop client in 2023.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
