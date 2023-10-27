This article will take MQTT.fx as [MQTT client tool](https://www.emqx.com/en/blog/mqtt-client-tools) to connect to [MQTT Cloud Service - EMQX Cloud](https://www.emqx.com/en/cloud). Through this article, you will be able to quickly understand the basic usage of MQTT.fx and the basic concepts and usage of the [MQTT protocol](https://www.emqx.com/en/mqtt-guide).



## Introduction to MQTT.fx 

The major version of MQTT.fx 1.0 is developed by Jens Deters using [JavaFX](https://en.wikipedia.org/wiki/JavaFX) technology, which is a Java virtual machine application. Unfortunately, the maintenance of MQTT.fx has now stopped maintenance and Softblade company has sponsored the development and released its commercial version MQTT.fx® 5.0, which is operated with a fee-based license. MQTT.fx in this article refers to version 1.0 without special instructions.

It contains mainstream MQTT client functions:

- Basic subscribe/publish/connect function
- User Authentication
- SSL/TLS connection support
- Easy to use message editing bar
- Support agent

In addition, MQTT.fx also has other excellent features:

- Support cross-platform
- Support $SYS topic subscription management MQTT Broker
- Complete log console
- Support JavaScript to process messages
- Support predefined templates

But there are also defects:

- [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) protocol is not supported
- Only one connection can be established at a time, which is inconvenient for multi-connection debugging
- The webSocket protocol is not supported and the situation of MQTT over Webscoket cannot be debugged



## Introduction to EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service launched by EMQ that can connect to a large number of IoT devices and integrate various databases and business systems. As the **world's first fully managed** [**MQTT 5.0**](https://www.emqx.com/en/blog/introduction-to-mqtt-5) **public cloud service**, EMQX Cloud provides MQTT message service with one-stop operation and maintenance management and a unique isolation environment.

In the era of the Internet of Everything, EMQX Cloud can help users quickly build industry applications for the IoT area and easily realize the collection, transmission, calculation, and persistence of IoT data.

This article will use [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX Cloud as the MQTT server address for this test. The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

For more details, please visit [EMQX Cloud website](https://www.emqx.com/en/cloud) or check [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/).

 

## MQTT.fx usage

### Preview

The main page is shown in the figure below. The top part is the MQTT Broker connection address bar and its connection configuration. The following function Tabs include Publish column, Subscribe column, Scripts column, Broker Status column, Log column for log information control.

![MQTT.fx Preview](https://assets.emqx.com/images/571a6128a2fd2d71de4c6892997194dd.png)

Each tab supports dragging into a separate window, as shown in the following figure:

![MQTT.fx separate window](https://assets.emqx.com/images/63fafd1866bf97e55a2d87a41cda901e.png)

### Connect

First, the MQTT client and Broker need to establish a connection to communicate. Click the configuration icon on the right side of the input box in the connection address bar to enter the specific connection configuration.

![MQTT.fx Connect](https://assets.emqx.com/images/3203ab53b9ccd95a1fa777cf96a1822a.png)

Select the Profile Type as MQTT Broker. Fill in `broker.emqx.io` for Broker Address and `1883` for Broker Port, as shown in the figure below:

![MQTT.fx Connect Setting](https://assets.emqx.com/images/987021efd99c587008e00061c5abaabf.png)

Click OK to confirm the configuration, return to the main interface, and click Connect. It can be seen that the circle on the right turns to green, indicating that the current connection is successful, as shown in the following figure:

![MQTT.fx Connect Successful](https://assets.emqx.com/images/61c7866eebc762e0fdb7dca8ca669611.png)

### Subscribe/Publish messages

Once the connection is established, you can start subscribing to messages. Because the MQTT protocol adopts the subscribe/publish method, we need to subscribe to the topic after connecting. After a message is generated on the topic, we can receive the messages from EMQX cloud.

![EMQX Platform](https://assets.emqx.com/images/7c3fd862db7bfdc16ef51bbcda0d5b2c.png)

Click to enter the Subscribe Tab to enter `/testTopic/1` in the topic box. Then, click the Subscribe button, and the list of subscribed topics will appear on the left. The current number of subscribed topics is 0, as shown in the following figure:

![MQTT.fx Subscribe](https://assets.emqx.com/images/1e911b2c418c6f072dcb6969f8a95e4c.png)

After that, we will publish the message to the broker. Return to Publish, enter the topic `/testTopic/1`, and enter the message of "hello world" in the message input box, as shown in the following figure:

![MQTT.fx Publish](https://assets.emqx.com/images/fa9bd621a9dee67a07ad481924c2b93c.png)

Click Publish to send the messages and return to the Subscribe Tab. We can find that the subscribed topic `/testTopic/1` has received the message, as shown in the following figure:

![MQTT.fx Receive Messages](https://assets.emqx.com/images/43c8f23108d248f172a978e499b4d446.png)

We use the client MQTT.fx to send the message "hello world" to the topic `/testTopic/1` under EMQX Cloud. All clients that have subscribed to this topic will receive this message, including the sending clients who have just subscribed to this topic.

### Script

You can customize the message publish logic more flexibly by using the script. Click Script Tab and Edit to modify the script content as follows:

```jsx
function execute(action) {
    mqttManager.publish("/testTopic/1", "hello world from script");
    return action;
}
```

Among them, `mqttManager` is the API to open the MQTT.fx script function, mainly including the following:

- publish()，publish messages
- subscribe()，subscribe to topics
- unsubscribe()，unsubscribe to topics
- output，output messages to the console

Click Execute, return to Subscribe column and find that the message is added with the content of "hello world from script". The script sending function is normal, as shown in the figure below:

![MQTT.fx Script](https://assets.emqx.com/images/1504963bd1d751dd481cd995faaccc03.png)

### Log

In the log, we can view the interaction process between MQTT.fx and EMQX Cloud, such as topic subscription, message publish, message reception, etc.:

![MQTT.fx Logs](https://assets.emqx.com/images/cc3b9ee768d37b6cce66316135db261c.png)

### SSL/TLS connection

We take CA self-signed service as an example to show how to enable SSL protocol to connect to EMQX Cloud.

Open the settings, fill in the Broker Address and Broker Port (`broker.emqx.io` and `8883` respectively) like normal connections, select the `SSL/TLS` item, select the TLSv1.2 protocol, check CA signed server certificate , and then select the application, as shown in the figure below:

![MQTT.fx SSL/TLS](https://assets.emqx.com/images/f8f23d25ea6fba54837bea19e1076081.png)

Click Connect, and you can see that the lock icon on the right is closed, indicating that SSL is enabled. Check the log, and you will find the words related to SSL connection port 8883. The connection to SSL/TLS is successful.

![MQTT.fx Connect Logs](https://assets.emqx.com/images/5ea2e8316df5c33d907b6d784309a025.png)

![MQTT.fx SSL/TLS Status](https://assets.emqx.com/images/b3efb08a666b6c3dca2485b5fb5b403a.png)



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
