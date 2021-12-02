Before introduction and use, readers can visit our [GitHub](https://github.com/emqx/MQTTX) or [website](https://mqttx.app) to understand and get the information of latest version.  MQTT X is undergoing rapid development and iterations, and the latest version will help improve the using experience.

## Download

Please download the right version from [GitHub Releases](https://github.com/emqx/MQTTX/releases)  and install it for use.

If there is a network problem resulting in a slow network speed or a jam in the GitHub download process, you can also  [go to the EMQ website](https://www.emqx.com/en/downloads/MQTTX/) to select the right version that matches your requirement and install it for use.



## MQTT Broker Preparation

- If you don't have an MQTT broker deployed locally, you can use the public MQTT service provided by [EMQ X Cloud](https://www.emqx.com/en/cloud)  for quick testing:

```
Broker Address: broker.emqx.io
Broker TCP Port: 1883
Broker SSL Port: 8883
```

- If you plan to deploy MQTT Broker locally, we recommend that you  [download  EMQ X](https://github.com/emqx/emqx/releases) for installation and use. EMQ X is a fully open source, highly available, low latency, million-level distributed IoT MQTT 5.0 message server.

  Quickly install EMQ X by using Docker:

```shell
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx
```



## Connection Profiles

After MQTT Broker is ready, enter the main program page and click the "+"  in the menu bar on the left. If there is no data on the page, you can also click the `New Connection` button on the right to quickly configure a new client connection.

![mqttxcreate.png](https://static.emqx.net/images/c0bee729cd26e338535ae234d7212384.png)

After entering the  `New Connection`  page, you need to configure or fill in the relevant information relevant to the client connection. The reader can configure all settings that define the Broker connection here, such as `Broker Host`,` Broker Port`, `Client ID`,` Username`, `Password`,` Clean Session`, .etc.

![2.png](https://static.emqx.net/images/cd943b647eb222d35c5dd1acdd7df9df.png)

1. Broker information

   When configuring the `Broker` information,` Client ID`, `Host`, and` Port` are already filled in by default. You can also modify it yourself based on the actual `Broker` information. Click the refresh button on the right of Client ID to quickly generate a new `Client ID`.

2. User authentication information

   If your broker has enabled user authentication, you can fill in the information of `username` and `password` in the configuration item.

3. SSL/TLS

   When you need to enable SSL / TLS authentication, you only need to set the SSL / TLS  in the configuration to `true`, and provide two methods of `CA signed` `self` and `Self signed`.

   If you select `Self signed`, you can configure the certificate. Click the folder button on the far right and select the certificates that has been generated. For one-way connection,you  just need to select your ` CA File`. For two-way authentication, you also need to choose to configure `Client Certificate File`  and ` Client key file`.

![3.png](https://static.emqx.net/images/48fbcdc6d3f29704ac1b7fa6154a4fe4.png)

4. Advanced configuration

   In advanced configuration, you can configure `Connect Timeout`,` KeepAlive`, `Clean Session`,` Auto Reconnect`, `MQTT Version` and other information.

5. MQTT v5.0

   In advanced configuration, you can select the protocol version of MQTT. Both MQTT v3.1.1 and MQTT v5.0 are supported and the default is v3.1.1. If you choose v5.0, you can also configure `Session Expiry Interval`,` Receive Maximum` (optional).

6. Will message

   In the configuration card under the advanced configuration, you can configure the will message. The values of `Last-Will-QoS` and` Last-Will-Retain` are filled with 0 and `False` by default. You only need to fill the value of  `Last-Will-Topic` and `Last-Will-Payload` to complete the configuration of the will message.



## Publish

After the connection is successfully created, you can enter the main interface of the connection. Click the fold button next to the connection name at the top to expand and display several basic information about the configuration and Quickly modify the common configuration of the connection. When modifying, you need to disconnect. After clicking the connection again, the modification will take effect. In the disconnected state, you can also click the configuration button on the right to modify more connection configurations.

After the connection is established, you can simply enter `Topic` and` Payload` in the input boxes at the bottom of the connection main page, and then click the button in the lower right corner to send a test message. macOS users can use the `command + enter`  shortcut to quickly send messages, and other users can use the`control + enter`  shortcut for that.

![fabu.png](https://static.emqx.net/images/59dffcc0988d9815714359a83333b873.png)

## Subscribe

Click the `New Subscription` button in the lower left corner to quickly subscribe to a topic. After the topic is successfully subscribed, it will start accepting messages immediately.

Each `Topic` is assigned a color mark at random. You can also open the color picker to customize the color of the mark. You can hide the subscription list to show more space by clicking the rightmost button at the top of the subscription list.

When hovering over a card in the `Topic` list, click the red button in the upper right corner to quickly unsubscribe.

Let's create a new test connection for the message publishing test. Fill in the `Topic` information you just subscribed to in the lower right corner of the page, input the content of the Payload, and click the send button on the far right to send a message to the connected client that subscribed to the  `Topic` .

![一条消息1.png](https://static.emqx.net/images/9c4de8dc1c3e978c5e6b2befe9f4011a.png)

![一条消息2.png](https://static.emqx.net/images/c157de49efe9bf8714dc7c0d7bc3b8d4.png)

If the sending client also subscribes to the same `topic`, the client will immediately receive the message after sending successfully. Note that in the message box, the right column is the sent message, and the left column is the received message.


## Others

1. Setting

   You need to click the settings button at the bottom of the left menu bar, or use shortcut keys to jump to the settings page. MacOS users can use `command +,` shortcut keys. Other users can use `control +,` shortcut keys. The  current supported setting includes language, whether to automatically check for updates and topic selection .

2. Drop-down menu on the message page

![xlcd.png](https://static.emqx.net/images/08707251ab7113cfd713ba8972cf9d60.png)

   Through the button of `All`,` Received`, `Published` in the upper right corner of the message bar, it can filter out all messages, received messages, and published messages.

   Click the action bar button at the top and select the `Search by Topic` item to open the function of searching and filtering  messages by  `Topic`. Shortcut key can be used for that. MacOS users can use the command + f shortcut key. Other users can use the control + f shortcut key. 

   Select the `Clear Histroy` item to quickly clear all sent and received messages in the current connection.

   Select the `Disconnect` and ` Delete Connection` items to quickly disconnect and delete the current connection.

3. Check for updates

   Click the `i` button on the left bottom to display the ` About` page to learn about the version of **MQTT X**  and related information of [EMQ X](https://www.emqx.com/en) . Click `Check for Updates` to check if there are newer versions.

![mqttxupdate.png](https://static.emqx.net/images/889ae0041b88ba2ac8f6fefc44a92fde.png)



The above is a brief overview of how to use MQTT X. Readers can use MQTT X entirety through the  [manual](https://github.com/emqx/MQTTX/blob/master/docs/manual.md) on GitHub.

This project is based on the Apache 2.0 open source protocol. In the process of using, you can go to [GitHub issues](https://github.com/emqx/MQTTX/issues) to submit issues, discuss opinions or submit PR to us. We will carefully review and respond to all questions.
