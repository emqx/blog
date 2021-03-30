## Overview

During learning and using [MQTT](https://www.emqx.io/mqtt), a handy client tool can greatly facilitate the user to explore the MQTT features and debug the functional components. Developers from all over the world have developed a number of client test tools for the MQTT protocol around different operating systems.

The type of these MQTT client tools is various, with different features emphasis. Therefore, as for beginners and even MQTT experts, how to choose a suitable MQTT client tool is a problem. 

This article will collect and sort out as much as possible, and make a comprehensive evaluation of various MQTT client tools on the market for readers' reference.

## Features required for MQTT client tools

MQTT client tools are often used to establish connections with the [MQTT broker](https://www.emqx.io/products/broker) for subscribing topics and receiving and publishing messages. The characteristic of functions for an MQTT client tool can be evaluated from the following aspects:

- In each usage phase, the tool needs to provide as much comprehensive parameter configuration capabilities to facilitate to users cope with any using scenarios and simulation tests of using ways. For example, supporting client authentication, configuring certificates and various encryption connections, configuring multiple parameters during the connection, publishing, and subscription process of MQTT, supporting [MQTT 5](https://www.emqx.io/mqtt/mqtt5), etc.
- Enhance user interaction convenience on a full-featured basis and operating interface fluently.
- Provide other extension functions, such as supporting multiple client connections and MQTT protocol debugging at the same time.
- Cross-platform, available under different operating systems.
- Whether supporting multiple languages such as Chinese/English.
- Whether support MQTT payload format converting.

This article will combine the features of each MQTT client tool to introduce evaluations from the above aspects. The participating client tools are as follows:

- MQTT X

- Mosquito CLI

- MQTT.fx

- MQTT Explorer

- MQTT Box

- mqtt-spy

- MQTT Lens

- MQTT WebSocket Toolkit

  


## MQTT X

### Introduction to client 

[MQTT X](https://mqttx.app/) is a cross-platform MQTT 5.0 desktop client tool open-sourced by [EMQ](https://www.emqx.io), supports macOS, Linux, Windows, and is the most beautiful MQTT client tool on the market until now.

MQTT uses Electron cross-platform technology, and can send and receive messages in the form of message chat. It allows establishing and connecting multiple clients at the same time, and freely switch to communicate with each other.  It has better interaction and greatly improves the efficiency of MQTT development test.

MQTT X has relatively comprehensive functions. Users can quickly test the connection/publishing/subscribing function of MQTT/TCP, MQTT/TLS, MQTT/WebSocket and other MQTT protocol features.

### Features of client

- Support MQTT v3.1.1 and MQTT v5.0 protocols
- Support CA, self-signed certificate, and single and two-way SSL /TLS authentication
- Support theme switching between Light, Dark and Night.
- Support MQTT over WebSockets
- Support Hex, Base64, JSON, Plaintext
- Support Simplified Chinese and English
- Support custom color marking when subscribing topics
- Message filter is available after clicking subscribed topic
- Storing MQTT broker information, and can select through drop-down

![1.png](https://mqttx.app/static/img/index/mqttx-usage.png)

### Download client

**Operating system:** Windows，macOS，Linux

**Project address:** [MQTT X](https://mqttx.app/)

**Download link:** [MQTT X GitHub](https://github.com/emqx/MQTTX/releases)



## Mosquito CLI

### Introduction to client

Mosquitto is an open-sourced (EPL/EDL license) message broker. Mosquitto provides two command-line MQTT client tools, [mosquitto_pub](https://mosquitto.org/man/mosquitto_pub-1.html) and [mosquitto_sub](https://mosquitto.org/man/mosquitto_sub-1.html)  by default after installation.

Mosquito CLI has multiple configuration options, supports connections through TLS certificate and a proxy server, supports debug mode, and can get more detailed message information in debug mode.

It is also very easy to use, only needs to provide a few parameters in the default usage environment to use:

```bash
## Enable debug mode to subscribe to testtopic/# topic
wivwiv-mac:workspace emqtt$ mosquitto_sub -t "testtopic/#" -d
Client mosqsub/66418-wivwiv-ma sending CONNECT
Client mosqsub/66418-wivwiv-ma received CONNACK
Client mosqsub/66418-wivwiv-ma sending SUBSCRIBE (Mid: 1, Topic: testtopic/#, QoS: 0)
Client mosqsub/66418-wivwiv-ma received SUBACK
Subscribed (mid: 1): 0
Client mosqsub/66418-wivwiv-ma received PUBLISH (d0, q0, r0, m0, 'testtopic/1', ... (5 bytes))
Hello

## Publish a message to testtopic / 1 topic
mosquitto_pub -t "testtopic/1" -m "Hello"
```

### Features of client

- Thie lightweight command-line tool, support debug mode, easy to install
- Support encrypted and nonencrypted connecting to MQTTQ server
- Easy to test in the remote server

### Download client

**Operating system:** Windows，macOS，Linux

**Project address:** [Github Mosquitto](https://github.com/eclipse/mosquitto)

**Download link:** [Mosquitto website](https://mosquitto.org/) 



## MQTT.fx

### Introduction to client

MQTT.fx is a currently mainstream MQTT client developed by [Jens Deters](http://www.jensd.de/) that can quickly verify whether it can interact with IoT Hub services to publish or subscribe to messages. MQTT.fx is applicable for the Apache License 2.0 protocol but without providing source code.

MQTT.fx is an established MQTT client tool. The related product documentation tutorials of cloud product providers such as Azure IoT Hub, AWS IoT, and Alibaba Cloud IoT are all using MQTT.fx as an example. MQTT.fx use JavaFX technology to develop, and may have a stuck experience on some older machines because of Java virtual machine.

In terms of basic functions, MQTT .fx can save multiple connection configurations, support multiple types of TCL encryption, and specify multiple types of certificates. When creating a connection, you can specify to use an HTTP proxy server. After successfully connecting, the usage of entire publishing and subscription functions are relatively reasonable and smooth. It is a function highlight that the `Topics Collector` function can find the subscribed topics through other methods such as the Broker-side proxy subscribe. Mqtt.fx also supports the connection test of Google Cloud IoT.

Among the advanced features, the biggest highlight of MQTT.fx is to support the JavaScript function scripts. With the JavaScript code written by Nashorn Engine users, users can access Java methods and fields to implement function extension. After familiarizing with the APIs related to MQTT.fx, users can write test scripts that adapt to the business, simulate sensor reporting data, even performance testing tools and other powerful functions.

If you are using Mosquitto broker, MQTT.fx provides a dedicated tab to implement visualize viewing Broker status through subscribing to both **system topics** (topics for publishing Broker run information). That also can get system information about the version and time of Broker, the number of clients and messages, network traffic, load status and other run information.

All in all, MQTT.fx has rich and mature functions, and supports all the configuration items that may encounter in the TCP connection. Except for the slightly poor interaction, interface stuck,  and users can only establish one connection at the same time, which cannot satisfy the demand of using multiple test connections simultaneously. Besides, it does not implement the support for WebSocket, which means that it cannot be used in the test scenario of MQTT over WebSockets.

### Features of client

- Predefine message template
- Get status of the broker through the system topic `$SYS`
- Remember the recently used topics
- Support for JavaScript scripts through Nashorn Engine
- Support log display, display log information in the connection
- Cross-platform desktop with support for Windows, macOS and Linux

![2.png](https://static.emqx.net/images/4f592bb17cbbfe3adf0d13e07277c0dd.png)

### Download client

**Operaring system:** Windows，macOS，Linux

**Download link:** https://mqttfx.jensd.de/index.php/download



## MQTT Explorer

### Introduction to client

MQTT Explorer is a comprehensive MQTT client that provides a structured overview of your MQTT topics and makes working with devices/services on your broker dead-simple. Currently, it based on CC BY-NC-ND 4.0 protocol open source, and users can view and use source code at will.

Visualization and vertical layered display of topics and dynamic preview are the highlights of MQTT-Explorer. Layered view enable this tool to use easily, and has distinguished MQTT Explorer with other outstanding MQTT desktop client. Custom subscribing can limit the number of message which need MQTT Explorer to process, and users can manage subscriptions in advanced connection settings. Users can also display the view of difference of received payload messages. The disadvantages are that users can only create a single client connection, and cannot connect multiple clients and enable them to be online at the same time.

### Features of client

- Visualize topics and dynamic preview of the change of topic
- Delete the reserved topics
- Search/filter topics
- Recursive delete topics
- Difference view of current and previously  received messages
- Publish topics
- Draw digital topics
- Retain the historic record of every topic
- Dark/Light topic

![mqtt-explorer.png](https://static.emqx.net/images/7be0606fdbb16f93359429dba0cc3e6e.png)

### Download client

**Operating system:** Windows，macOS，Linux

**Project address:** [Github MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer)

**Download link:** [https://mqtt-explorer.com/](https://mqtt-explorer.com/)



## MQTT Box

### Introduction to client

MQTT Box is an MQTT client tool developed by Sathya Vikram, originally only used in [Chrome](https://chrome.google.com/webstore/detail/mqtt-client-tcp-and-ws/kaajoficamnjijhkeomgfljpicifbkaf?utm_source=chrome-ntp-launcher) for installation and usage of browser extensions. After rewritten open source, it becomes a desktop-side cross-platform independent software. 

MQTT Box also adopts Electron cross-platform technology. The interface is simple and direct and supports multiple clients to be online at the same time. However, switching and messaging between clients is still inconvenient. MQTT Box is a worthwhile MQTT client tool with the powerful cross-platform features with the help of Chrome and combined with simple load testing.

### Features of client

- Support installation as Chrome plugin
- Support MQTT, MQTT over WebSocket, multiple TCP encryption connections
- Save the sent history
- Copy/paste messages in history
- Save the history of subscription message 
- Simple performance test, testing the load of the broker and viewing the test results through chart visualization

![3.png](https://static.emqx.net/images/4d230117efab9a40e2ff30f7cd82744d.png)

### Download client

**Operating system:** Windows，macOS，Linux, Chrome OS

**Project address:** [GitHub MQTTBox](https://github.com/workswithweb/MQTTBox)

**Download link:** http://workswithweb.com/mqttbox.html



## mqtt-spy

### Introduction to client

Mqtt-spy is part of Eclipse Paho and Eclipse IoT. It runs on top of Java 8 and JavaFX by directly launching JAR files. Mqtt-spy has a good interaction way to display the basic MQTT publish/subscribe mechanism.

Mqtt-spy does not provide a separate installation package, which needs users to install the Java runtime environment before using mqtt-spy. But after launching, mqtt-spy has a friendly hands-on experience, and the guide feature is eye-catching. MQTT newbies can easily connect to the public MQTT broker using mqtt-spy for exploration. The function interface of mqtt-spy is slightly complicated, but after familiar with the function of each component, it will become a development and debugging tool. It is also worth mentioning that the performance and stability of mqtt-spy are poor, maybe is because that the version used by the author is the latest beta. After connecting multiple brokers, there are frequent crashes and suspended animations.

### Features of client

- Support for MQTT and MQTT over WebSocket
- Easy to interact, can publish and subscribe at the same time, connect multiple brokers on different tabs
- Can close different areas of the pub/sub window (publish, new subscriptions, subscriptions and messages) to make room for space currently in use
- The search function allows searching for commonly used MQTT messages, allowing outputting publishing/subscribing messages to standard output or logging to a file for subsequent analysis

![4.png](https://static.emqx.net/images/9836d2b3d18279f9e4d43c5e4c6660f0.png)

![5.png](https://static.emqx.net/images/25b0be7357a3c3cfdc46bae9474c4477.png)

### Download client

**Operating system:** Windows，macOS，Linux

**Project address:** [GitHub mqtt-spy](https://github.com/eclipse/paho.mqtt-spy)

**Download link:** https://github.com/eclipse/paho.mqtt-spy/releases



## MQTT Lens

### Introduction to client

MQTT Lens is a Chrome extension tool that can be installed from the Chrome Web Store. MQTT Lens interface is very concise and provides basic publishing and subscribing function.

Although MQTT Lens is simple enough, provides the fundamental MQTT and MQTT over WebSocket connection function, and can quickly get started, explore and use.

### Features of client

- Accept connections to multiple mqtt brokers at the same time, with different colors to associate
- The interface for subscribing, publishing and viewing all received messages is very simple and easy to master
- Support for MQTT and MQTT over WebSocket

### Download client

**Operating system:** Windows，macOS，Linux, Chrome OS

**Download link:** [Chrome Web Store](https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm)



## MQTT WebSocket Toolkit

### Introduction to client

[MQTT WebSocket Toolkit](https://www.emqx.io/mqtt/mqtt-websocket-toolkit) is a simple and easy-to-use online MQTT client test tool. It based on browser-side to use, only supports MQTT over WebSocket connection, and provides basic MQTT configuring connection settings.

The interface and interaction of MQTT WebSocket Toolkit still use the design and usage style of [MQTT X](https://mqttx.app/). It publishes and receives messages in the form of message chat and allows establishing and connecting multiple clients at the same time and freely switches to communicate with each other,  which improves the efficiency of the MQTT development test. When you need to test MQTT WebSocket connections, users do not need to download and install extra tools, so this tool is quick and available.

### Features of client

- Online quickly access, without installing, and with the concise and easy-to-use interface
- Support  MQTT over WebSockets
- Support for creating multiple clients, and can retain the information of the client until the next access.

![mqtt-websocket-toolkit.png](https://static.emqx.net/images/bb8967f026a3df9fad1ad92ac057caf3.png)

### Download client

**Operating system:** Windows, macOS, Linux, Chrome OS

**Online address:** [MQTT WebSocket Toolkit](http://tools.emqx.io/)

**Project address:** [MQTT WebSocket Toolkit GitHub](https://github.com/emqx/MQTT-Web-Toolkit)

