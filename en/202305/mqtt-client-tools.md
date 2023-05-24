## Introduction

With the rapid development of the Internet of Things (IoT), the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is being widely used by many companies and developers. In the journey of learning and using MQTT, MQTT client tools are used to connect to [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for publishing, subscribing, and messages sending and receiving. 

A handy client tool can greatly facilitate developers to explore MQTT features and debug IoT applications, shortening the development cycle. Given the variety of MQTT client tools available with different functional focuses, choosing a suitable MQTT client tool is challenging for beginners and even MQTT experts.

We have selected seven of the most useful MQTT client tools in 2023 and listed them by Desktop, Browser, Command Line, and Mobile categories. We hope this article will help you quickly find a suitable one for MQTT development.

## How to Choose an MQTT Client?

A good MQTT client tool should possess the following key features.

- Support for one-way and two-way SSL authentication.
- Support for [MQTT 5](https://www.emqx.com/en/mqtt/mqtt5) features.
- Maintain ease of use on a full-featured basis.
- Support for multiple clients online at the same time.
- Cross-platform, available under different operating systems.
- Support MQTT over WebSocket.
- Advanced features: Customized script, logging, payload format conversion, etc.

## Free Public MQTT Broker

Before diving into the MQTT client desktop tools, we need an [MQTT broker](https://www.emqx.io/) to communicate and test. We choose the free public MQTT broker available on `broker.emqx.io`.

> **MQTT Broker Info**
>
> - Server: broker.emqx.io
> - TCP Port: 1883
> - WebSocket Port: 8083
> - SSL/TLS Port: 8883
> - Secure WebSocket Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

## MQTT Desktop Client Tools

### MQTTX

[MQTTX](https://mqttx.app/) is an elegant cross-platform MQTT 5.0 desktop client that runs on macOS, Linux, and Windows. Its user-friendly chat-style interface enables users to easily create multiple MQTT/MQTTS connections and subscribe/publish MQTT messages.

MQTTX fully supports MQTT versions 5.0 and 3.1.1, MQTT over TLS, MQTT over WebSocket, and one-way and two-way SSL authentication. In addition to these essential features, MQTTX offers advanced functionality, such as customizable scripts for [MQTT Pub/Sub](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) simulation and support for codecs like Hex, Base64, and JSON payloads.

MQTTX is an open-source project developed with [Electron](https://www.electronjs.org/) and maintained by the [EMQX team](https://github.com/emqx). The latest release is version 1.9.2 by the end of April 2023.

GitHub Project: https://github.com/emqx/mqttx

![MQTT X](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

#### Features

- User-friendly and easy-to-use UX design
- Chatbox for sending/receiving MQTT messages
- Fully support for MQTT versions 5.0 and 3.1.1
- Support MQTT over TLS, and [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- Support for one-way and two-way SSL authentication
- Hex, Base64, JSON, and Plaintext payload codec
- Customized colors for different MQTT subscriptions
- Customized script for MQTT Pub/Sub scenario simulation
- Cross-platform, running on Windows, macOS, and Linux

#### Installation

- **Homebrew**

  ```
  brew install --cask mqttx
  ```

- **Download**

  [https://mqttx.app/](https://mqttx.app/)

### MQTT Explorer

MQTT Explorer is an open-source MQTT client tool that provides an easy-to-use graphical user interface (GUI) with a structured topic overview. It adopts a hierarchical main view and supports a visual chart display of received payload messages.

MQTT Explorer supports MQTT 5.0 and 3.1.1 protocols and allows developers to simultaneously create one MQTT/MQTTS connection.

MQTT Explorer is written in Typescript and developed by [Thomas Nordquist](https://github.com/thomasnordquist). It’s cross-platform and can run on Windows, macOS, and Linux. It’s a pity that the project has been out of development since the last release of version 0.4.0-beta1 on April 28, 2020.

GitHub: https://github.com/thomasnordquist/MQTT-Explorer

![MQTT Explorer](https://assets.emqx.com/images/fd34faa00ea66d846bfd0a9d99040359.png)

#### Features

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

#### Download

[https://mqtt-explorer.com/](https://mqtt-explorer.com/)



## MQTT Online Client Tools

### MQTTX Web

[MQTTX Web](https://mqttx.app/web) is a user-friendly, browser-based tool for online debugging, developing, and testing MQTT applications. It connects to an MQTT broker via a WebSocket client and offers an intuitive interface.

Developed by the [EMQX team](https://github.com/emqx), MQTTX Web is an open-source tool that supports MQTT 3.1.1 and MQTT 5.0 protocols and WebSocket transports. It is licensed under Apache Version 2.0.

GitHub Project: https://github.com/emqx/MQTTX/tree/main/web

Try Now: [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client#/recent_connections)

Additionally, MQTTX Web supports private deployment using Docker, which is beneficial when only a browser is available, or for testing in restricted intranet environments. Deploy from Docker Image:

```
docker pull emqx/mqttx-web
docker run -d --name mqttx-web -p 80:80 emqx/mqttx-web
```

![MQTTX Web](https://mqttx-static.emqx.net/img/banner.268d1fa.png)

### MQTT.Cool Test Client

MQTT.Cool Test Client is a very simple and linear GUI (based on the MQTT.Cool API) through which you can test the interaction between the MQTT.Cool server and MQTT brokers. It supports connecting to the broker via MQTT TCP in the browser.

Try Now: [https://testclient-cloud.mqtt.cool/](https://testclient-cloud.mqtt.cool/)

![MQTT.Cool Test Client](https://assets.emqx.com/images/263f0c34a8b93d477acff194ef17d46e.png)


## MQTT CLI Tools

### MQTTX CLI

[MQTTX CLI](https://mqttx.app/cli) is a lightweight and easy-to-use MQTT 5.0 command line tool. With various commands for MQTT publishing, subscribing, benchmarking, and IoT data simulation, it is one of the most powerful tools for MQTT development.

MQTTX CLI is an open-source project written in Node.js and developed by the [EMQX team](https://github.com/emqx). It’s cross-platform and can work on Windows, macOS, and Linux.

GitHub Project: [https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli)

![MQTTX CLI](https://assets.emqx.com/images/21640fc7fa544b56ae41815f390ccee7.png)

#### Features

- Fully support for both MQTT v3.1.1 and MQTT v5.0
- Cross-platform compatibility with Windows, MacOS, and Linux
- Dependency-free setup allowing for quick installation without prerequisites
- Supports CA, self-signed certificates, and one-way and two-way SSL authentication
- Performance testing capabilities for quickly evaluating MQTT service performance.

#### Installation

MQTTX CLI is compatible with Windows, macOS, and Linux. For additional installation options, please consult the [documentation](https://mqttx.app/docs/cli/downloading-and-installation).

- **Docker**

  ```
  docker pull emqx/mqttx-cli
  docker run -it --rm emqx/mqttx-cli
  ```

- **Homebrew**

  ```
  brew install emqx/mqttx/mqttx-cli
  ```

- **Download**

  [https://mqttx.app/cli](https://mqttx.app/cli)

#### Usage Example

- Connect

  Test connecting to an MQTT broker:

  ```
  mqttx conn -h 'broker.emqx.io' -p 1883 -u 'test' -P 'test'
  ```

- **Subscribe**

  Subscribe to an MQTT topic:

  ```
  mqttx sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
  ```

- **Publish**

  Publish a QoS1 message to an MQTT topic:

  ```
  mqttx pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from MQTTX CLI'
  ```

- **Publishing multiple messages**

  The MQTTX CLI also supports publishing multiple messages. Add a -M parameter and a -s parameter to the command in the editor, and newline it after each entry.

  ![MQTTX CLI](https://assets.emqx.com/images/549a31f8b062f099c0eac8c0c6047f35.png)

- **Benchmark**

  For MQTTX CLI, the `bench` command is easy to use and concise in its content output. For a large number of connections, subscriptions, and publications, the display method has been optimized by dynamically updating the real-time numbers to avoid being overwhelmed by a large number of output logs during use.

  ![MQTT Benchmark](https://assets.emqx.com/images/6d942b32742bf859ef66a93abb216860.png)

### Mosquitto CLI

Mosquitto is a widely used open-source MQTT broker with the popular `mosquitto_pub` and `mosquitto_sub` command line clients. These CLI tools offer a wide range of options to connect, subscribe to, and publish messages to an MQTT broker.

The Mosquitto project is written in C/C++ and maintained by the Eclipse Foundation. Mosquitto is highly portable and can be deployed on various platforms, including Linux, Mac, Windows, and Raspberry Pi.

GitHub Project: [https://github.com/eclipse/mosquitto](https://github.com/eclipse/mosquitto)

#### Features

- Lightweight and easy to use
- Support for MQTT v3.1.1 and v5.0 protocols
- Extensive command-line parameters
- Support for SSL/TLS encryption/authentication
- MQTT v5.0 request/response functionality

#### Installation

- Docker

  ```
  docker pull eclipse-mosquitto
  ```

- Homebrew

  ```
  brew install mosquitto
  ```

- Download

  [https://mosquitto.org/download/](https://mosquitto.org/download/)

#### Usage Example

- **Publish**

  Publish a QoS1 message to an MQTT topic:

  ```
  mosquitto_pub -t 'topic' -q 1 -h 'broker.emqx.io' -p 1883 -m 'Hello from Mosquitto CLI'
  ```

- **Subscribe**

  Subscribe to an MQTT topic:

  ```
  mosquitto_sub -t 'topic/#' -h 'broker.emqx.io' -p 1883
  ```

- **Request/Response**

  ```
  mosquitto_rr -t 'req-topic' -e 'rep-topic' -m 'request message' -h 'broker.emqx.io'
  mosquitto_pub -t 'rep-topic' -m 'response message' -h 'broker.emqx.io'
  ```

  

## MQTT Mobile Client Tools

### EasyMQTT

EasyMQTT is an MQTT client for iPhone, iPad, and macOS, allowing you to interact with any MQTT Broker. Use it to manage your own setup at home, control things like Zigbee2MQTT or monitor a remote broker. It features a simple, user friendly interface, supporting both light and dark modes.

<div style="text-align:center;"><img src="https://assets.emqx.com/images/f9118dd8e7c71a668b3667b1c629a1d0.png" width="320px" /></div>


**Download**

[https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone](https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone)



## Conclusion

In conclusion, we have provided a detailed introduction to MQTT client tools in different categories. 

Among these, the MQTTX open-source project stands out as a fast-growing client tool that offers a modern chat-style interface, full MQTT 5.0 support, and a rich set of features that provides a great user experience. With three versions available - Desktop, Command Line, and Browser - MQTTX can fulfill your MQTT testing requirements in diverse scenarios. Undoubtedly, [MQTTX](https://mqttx.app/) is among the top MQTT client tools of 2023.



## References

- [Top 3 MQTT Desktop Client Tools in 2023](https://www.emqx.com/en/blog/top-3-mqtt-desktop-client-tools-in-2023)
- [Top 5 MQTT CLI Tools for IoT Developers in 2023](https://www.emqx.com/en/blog/top-5-mqtt-cli-tools-for-iot-developers-in-2023)
- [Top 3 MQTT WebSocket Clients in 2023](https://www.emqx.com/en/blog/top-3-mqtt-websocket-clients-in-2023)



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
