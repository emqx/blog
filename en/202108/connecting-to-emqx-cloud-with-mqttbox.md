This article will take [MQTTBox](https://github.com/workswithweb/MQTTBox) as [MQTT client](https://www.emqx.com/en/blog/introduction-to-the-commonly-used-mqtt-client-library) test tool to connect to [MQTT Cloud Service-EMQX Cloud](https://www.emqx.com/en/cloud). Through this article, you will be able to quickly understand the basic usage of MQTTBox and the basic concepts and usage of the [MQTT protocol](https://www.emqx.com/en/mqtt).



## Introduction to MQTTBox

[MQTTBox](https://github.com/workswithweb/MQTTBox) is an MQTT client tool developed by Sathya Vikram. Initially, it was only used as an extended installation on Chrome, and was later rewritten and open sourced to become a desktop cross-platform independent software. The interface is simple and straightforward, and supports multiple clients online at the same time. However, there are still some inconveniences in the interaction between clients, such as switching and sending messages. MQTTBox achieves powerful cross-platform features with Chrome. Combined with simple load testing functions, it is an MQTT client tool worth trying.

MQTTBox fully supports the following functions:

- Easy to install through Chrome storage that supports Chrome OS, Linux, macOS, and Windows, and support the independent installation of Linux, macOS, and Windows
- Support MQTT, MQTT over WebSocket, multiple TCP encrypted connections
- Save history of sent messages
- Copy/paste the messages from history
- Save subscription message history
- test Broker's load through a simple performance test,  and visualize the test results through charts



## Introduction to EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service launched by [EMQ](https://www.emqx.com/en) company that can connect to a large number of IoT devices and integrate various databases and business systems. As the **world's first fully managed** [**MQTT 5.0**](https://www.emqx.com/en/mqtt/mqtt5) **public cloud service**, EMQX Cloud provides MQTT message service with one-stop operation and maintenance management and a unique isolation environment.

In the era of the Internet of Everything, EMQX Cloud can help users quickly build industry applications for the IoT area and easily realize the collection, transmission, calculation, and persistence of IoT data.

This article will use [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX Cloud as the MQTT server address for this test. The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

For more details, please visit [EMQX Cloud website](https://www.emqx.com/en/cloud) or check [EMQX Cloud documentation](https://docs.emqx.io/en/cloud/latest/).



## MQTTBox usage

### MQTT connection

#### Initialization page

After opening the software, enter the main interface of the software, click the `Create MQTT Client` button on the top menu bar, and enter the page of `create MQTT client`.

![MQTTBox Initialization page](https://assets.emqx.com/images/75d7f67d4c584a017f0f50ffd8a4f87e.png)

#### Create a connection

After entering the page for creating an MQTT client, fill in the MQTT-related configuration information such as Host, connection protocol, and click the `Save` button at the bottom to immediately create a connection client.

> Note: When filling in the Host, you need to fill in the complete address, including the port number of the connection. If it is a WebSocket connection, you need to add Path. If MQTT Broker enables user name/password authentication, you also need to enter Username/Password in the configuration page.

![MQTTBox Create a connection](https://assets.emqx.com/images/f371711eda1ffc0ebd6a12976e88cfbd.png)

After saving successfully, you will enter a page of client details. If the button in the upper right corner shows `Connected` and its color is green, it means that the MQTT client has been successfully connected. You can disconnect the client by clicking it again.

### Subscribe to a topic

Once the connection is established, you can start subscribing to messages. Because the MQTT protocol uses a publish/subscribe model, we need to subscribe to a topic after connecting, and then there will be messages on the topic to receive messages from EMQX Cloud.

There are two input boxes for sending and subscribing by default in the client details page of MQTTBox. If there are multiple subscriptions or different published content, you can add multiple boxes. Click the `Add publisher` and `Add subscriber` buttons in the top menu bar to add and manage multiple publishers/subscribers.

We first enter Topic: `testtopic/mqttbox` in the yellow box on the right. After selecting the QoS level, click the `Subscribe` button to subscribe to the related topic.

### MQTT message publishing

Then we enter the topic to be published in the blue box. Here, we enter the `testtopic/mqttbox` that we just subscribed to, and select the QoS level as the default Payload Type that supports `String/JSON/XML/Characters`. After entering a section of JSON in the payload box, click the Publish button.

At this point, we can see the message just published in the subscription box on the right. So far, we have created an MQTT client and successfully tested functions such as connection, publishing, and subscription.

![MQTTBox publish message](https://assets.emqx.com/images/638cea055bb29c8b6265ac6df0496413.png)

### TLS/SSL connection

In addition to normal connections, MQTTBox also supports TLS/SSL connections.

If you use EMQX Cloud, you can refer to this [document](https://docs.emqx.io/en/cloud/latest/deployments/tls_ssl.html) to create a certificate. We can enter the client details page, select the protocol as mqtts/tls or wss, and then select save.

If it is two-way authentication, you can select the CA certificate file, the client certificate, and the client key file on the configuration page, and then select connection. Please confirm the TLS/SSL connection port and modify it before connecting.

![MQTTBox TLS/SSL connection](https://assets.emqx.com/images/6d53d3f95ac3b4bef0cfcdd2bc51a11f.jpg)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
