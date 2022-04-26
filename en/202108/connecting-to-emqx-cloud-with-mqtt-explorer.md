This article will take [MQTT Explorer](https://mqtt-explorer.com/) as [MQTT client](https://www.emqx.com/en/blog/introduction-to-the-commonly-used-mqtt-client-library) test tool to connect to [MQTT Cloud Service - EMQX Cloud](https://www.emqx.com/en/cloud). Through this article, you will be able to quickly understand the basic usage of MQTT Explorer and the basic concepts and usage of the [MQTT protocol](https://www.emqx.com/en/mqtt).



## Introduction to MQTT Explorer

[MQTT Explorer](https://mqtt-explorer.com/) is currently a relatively active MQTT client desktop application, which has always been liked by developers. Its main technology is [Electron](https://github.com/electron/electron), which is developed by [@thomasnordquist](https://github.com/thomasnordquist) and open-sourced, and follows [Creative Commons Public Licenses](https://wiki.creativecommons.org/wiki/Considerations_for_licensors_and_licensees#Considerations_for_licensees) protocol. GitHub address is [https://github.com/thomasnordquist/MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer).

Its main features are:

- Basic subscription/push/connection function
- User authentication function
- WebSocket support
- Support diff view and multiple types of Payload
- Basic historical information log
- Support TLS connection
- Support night mode

In particular, some good features are:

- Automatically subscribe to the topic of $SYS for easy check of broker status information
- Organize the subscription list in a tree structure to facilitate users to view their attribution
- With message visualization function and intuitive and interactive statistical chart design

MQTT Explorer can meet most development needs, but it also has some disadvantages:

- Only one connection can exist at a time, which is not convenient for multiple-connections debugging
- Publish payload and Subscribe Message list are not separated in UI design so that it is not easy to check the status of sending and receiving messages
- There is no complete operation log record, which makes it inconvenient for developers to check the information interacting with the server



## Introduction to EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service launched by [EMQ](https://www.emqx.com/en) company that can connect to a large number of IoT devices and integrate various databases and business systems. As the **world's first fully managed** [**MQTT 5.0**](https://www.emqx.com/en/mqtt/mqtt5) **public cloud service**, EMQX Cloud provides MQTT message service with one-stop operation and maintenance management and a unique isolation environment.

In the era of the Internet of Everything, EMQX Cloud can help users quickly build industry applications for the IoT area and easily realize the collection, transmission, calculation, and persistence of IoT data.

This article will use [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX Cloud as the MQTT server address for this test. The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

For more details, please visit [EMQX Cloud website](https://www.emqx.com/en/cloud) or check [EMQX Cloud documentation](https://docs.emqx.io/cloud/latest/).



## MQTT Explorer usage

### Function preview

The main page is shown in the figure below, with the topic search bar and connection configuration at the top. On the lower left of the page, it is the tree structure of the topic, and on the right, it is the Publish column, Subscribe column, Payload column, and History information control column.

![MQTT Explorer preview](https://static.emqx.net/images/2d409b0d702597f30f5cd53a7940ab68.png)

### MQTT connection/subscription

#### Initialization page

The configuration page will pop up when you enter MQTT Explorer for the first time.

![MQTT Explorer Initialization page](https://static.emqx.net/images/a66c05e560827978c1831596f3391495.png)

#### Create a connection

Click Connections to create a new connection, and fill in the Host as broker-cn.emqx.io, the port as 1883, and the protocol as MQTT protocol.

![MQTT Explorer Create connection](https://static.emqx.net/images/640f91f59964d64d587856c8992158b0.png)

#### Subscribe to a topic

Then, click Advanced. Because EMQX Cloud prohibits the `$SYS` topic and the `#` topic by default, we delete them and enter a test subscription topic with the name `test/1`, and the result is shown in the figure below.

![MQTT Explorer Subscribe to a topic](https://static.emqx.net/images/7718a737bc39114356ea10cd97bbe89c.png)

#### Connect

Finally, click Back to return to the connection configuration page, and click Connect to complete the connection of EMQX Cloud and the subscription of the topic `test/1`.

After the connection is successful, you can see that the subscription tree structure has `test` and `1` nodes, and the status bar at the top right shows that it has been connected, and the title of the topic `test/1` is contained on the right.

![MQTT Explorer Connect](https://static.emqx.net/images/5425f6c546aa033e9b07d44eed16ce71.png)

### MQTT message publishing

After the connection is established, enter `/test/1` in the topic box at the bottom right corner of the page, and enter some text, and then click Publish to send the message.

![MQTT Explorer MQTT message publishing](https://static.emqx.net/images/ff1b9faf9ec30e8510243710449eae38.png)

### Receive subscription messages

After the publish is successful, the message just published will be received in the Value card at the top right.

![MQTT Explorer Receive subscription messages](https://static.emqx.net/images/e14ee78f54a3a8e50354282eeb545397.png)

### Receiving history

In the History card at the bottom right corner of the page, you can see the message records received by the relevant subscription topic.

![MQTT Explorer Receiving history](https://static.emqx.net/images/f3f2581c6cba7f370ec7fd712bb51487.png)

### Statistical information

Statistical information will be displayed at the bottom right corner of the page.

![MQTT Explorer Statistical information](https://static.emqx.net/images/30eed43a6c0bf4e2e3c3ce5df9bc01ae.png)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
