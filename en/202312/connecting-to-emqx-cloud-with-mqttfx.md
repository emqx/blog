## Introduction to MQTT.fx

The major version of MQTT.fx 1.0 was developed by Jens Deters using [JavaFX](https://en.wikipedia.org/wiki/JavaFX) technology. It was a Java virtual machine application. Unfortunately, MQTT.fx is no longer maintained. However, Softblade company has sponsored the development of a commercial version of MQTT.fx® 5.0, which is available under a fee-based license. This article will refer to MQTT.fx version 1.0 unless stated otherwise.

It contains mainstream MQTT client functions:

- Basic subscribe/publish/connect function.
- User Authentication.
- SSL/TLS connection support.
- Easy-to-use message editing bar.
- Support agent.

In addition, MQTT.fx also has other excellent features:

- Support cross-platform.
- Support $SYS topic subscription management MQTT Broker.
- Complete log console.
- Support JavaScript to process messages.
- Support predefined templates.

But there are also some defects:

- [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) protocol is not supported.
- Only one connection can be established at a time, which is inconvenient for multi-connection debugging.
- The WebSocket protocol is not supported, and the situation of MQTT over Webscoket cannot be debugged.

## MQTT.fx Installation

To install MQTT.fx, visit [Softblade's download page](https://softblade.de/en/download-2/) to access the latest version of MQTT.fx. Choose the appropriate version for your operating system from this page.

## MQTT Basic Features Showcasing with MQTT.fx

### Prepare an MQTT Broker

Before proceeding, please ensure you have an MQTT broker to communicate and test with. 

[**EMQX Cloud Serverless**](https://www.emqx.com/en/cloud/serverless-mqtt) is a fully managed [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) in the cloud that is quick to set up and ideal for small-scale IoT tests. It offers 1 million free monthly session minutes, perfect for maintaining a modest number of devices.

Please follow our guide for newcomers. After registering, you'll receive an instance complete with connection info and a CA certificate, mirroring your deployment's overview.

![EMQX Cloud](https://assets.emqx.com/images/f2bffa3e65bc97ee7511942890987d1a.png)

### Preview of MQTT.fx

The figure below displays the main page of the application. The top section contains the connection address bar for the MQTT Broker and its respective configuration options. The function Tabs, located below the address bar, consist of five columns: Publish, Subscribe, Scripts, Broker Status, and Log—these columns control log information and the application's publishing, subscribing, and scripting functionalities.

![Preview of MQTT.fx](https://assets.emqx.com/images/9258190d7d9a82e4b449fe4a0eb55743.png)

Each tab supports dragging into a separate window, as shown in the following figure:

### MQTT Connection

First, in the MQTT.fx main interface, click the configuration icon next to the connection address bar to access the settings.

1. **Profile Type**: Choose "MQTT Broker" as the profile type.
2. **Server Address and Port**: Enter your Serverless deployment address as the "Broker Address" and use port 8883.
3. **Authentication**: Under the "User Credentials" section, input the username and password you set during your Serverless setup.
4. **Secure Connection Setup**: Navigate to the SSL/TLS tab, tick "Enable SSL/TLS", select the default TLS version, and choose your downloaded CA certificate under "CA Certification File".
5. **Confirm and Connect**: Click `OK` to confirm the configuration, return to the main interface, and click Connect. It can be seen that the circle on the right turns to green, indicating that the current connection is successful, as shown in the following figure:

![MQTT.fx 1](https://assets.emqx.com/images/7b1a70bb095650280f57304b350a5240.png)
![MQTT.fx 2](https://assets.emqx.com/images/534c1f6630701c3b809984c939a0181a.png)
![MQTT.fx 3](https://assets.emqx.com/images/2900c6e62cabe8ee8a7bf70534e3c1e5.png)
![MQTT.fx 4](https://assets.emqx.com/images/7764e6eff98b337471554692da235081.png)

### Messages Subscription/Publishing

Once the connection is established, you can start subscribing to messages. Because the MQTT protocol adopts the subscribe/publish method, we need to subscribe to the topic after connecting. After a message is generated on the topic, we can receive the messages from the EMQX cloud.

Click the Subscribe Tab to enter `/testTopic/1` in the topic box. Then, click the `Subscribe` button, and the list of subscribed topics will appear on the left. The current number of subscribed topics is 0, as shown in the following figure:

![MQTT Messages Subscription/Publishing](https://assets.emqx.com/images/28183b7c7fc665092b7dc22aba3abd24.png)

After that, we will publish the message to the Broker. Return to Publish, enter the topic `/testTopic/1`, and enter the message of "hello world" in the message input box, as shown in the following figure:

![publish](https://assets.emqx.com/images/699b3c242f798b063ac3107dc48a8c3a.png)

Click Publish to send the messages and return to the Subscribe Tab. We can find that the subscribed topic `/testTopic/1` has received the message, as shown in the following figure:

![Click Publish](https://assets.emqx.com/images/411aba4ff248538f42980979c05dba15.png)

We use the client MQTT.fx to send "hello world" to the topic `/testTopic/1` under EMQX Cloud. All clients who subscribe to this topic will receive this message, including the sending clients who have just subscribed to this topic.

### SSL/TLS Connection

We take CA self-signed service as an example of how to enable SSL protocol to connect to EMQX Cloud.

Open the settings, fill in the Broker Address and Broker Port (`broker.emqx.io` and `8883` respectively) like regular connections, select the `SSL/TLS` item, select the TLSv1.2 protocol, check CA-signed server certificate, and then select the application, as shown in the figure below:

![MQTT.fx SSL/TLS Connection](https://assets.emqx.com/images/8e88001fd6ef4d34635a84f7d77da09e.png)

Click Connect, and you can see that the lock icon on the right is closed, indicating that SSL is enabled. Check the log, and you will find the words related to SSL connection port 8883. The connection to SSL/TLS is successful.

![Check the log](https://assets.emqx.com/images/319aa3eff784e30842ba5cab660423f9.png)
![lock icon on the right is closed](https://assets.emqx.com/images/e232c535f668eda621a8fc2a7c8aec7a.png)

## Discover Advanced Features of MQTT.fx 

### Script

You can customize the message publish logic more flexibly by using the script. Click Script Tab and Edit to modify the script content as follows:

```
function execute(action) {
    mqttManager.publish("/testTopic/1", "hello world from script");
    return action;
}
```

Among them, `mqttManager` is the API to open the MQTT.fx script function, mainly including the following:

- `publish()` - publish messages
- `subscribe()` - subscribe to topics
- `unsubscribe()` - unsubscribe to topics
- `output`() - output messages to the console

Click Execute, return to the Subscribe column, and find that the message is added with the content of "hello world from the script". The script-publish function is normal, as shown in the figure below:

![MQTT.fx script](https://assets.emqx.com/images/e5e24b0c4880e6ca0914e72ad4bace83.png)

### Log

In the log, we can view the interaction process between MQTT.fx and EMQX Cloud, such as topic subscription, message publish, message reception, etc.:

![MQTT.fx log](https://assets.emqx.com/images/791436a03039349335541be010f48f3f.png)

### Proxy

In MQTT.fx, when creating or editing a connection, you can use a proxy. Simply select the 'Proxy' option, check the 'Use HTTP Proxy' box, and enter your proxy server information.

Using a proxy is to route your MQTT traffic through a specified server. This is particularly useful for bypassing network restrictions or enhancing communication security.

![MQTT.fx proxy](https://assets.emqx.com/images/dbf1bb5a1478076ae924ed88cb3a634e.png)

## FAQs about MQTT.fx

**Q: Can I establish multiple connections simultaneously in MQTT.fx?**  
**A**: Despite its advanced features, MQTT.fx only allows one MQTT connection at a time, which may limit its use in multi-connection debugging scenarios.

**Q: Is it possible to debug MQTT over WebSocket using MQTT.fx?**  
**A**: MQTT.fx does not support the WebSocket protocol, making it unsuitable for MQTT over WebSocket testing scenarios.

**Q: From which version does MQTT.fx support the MQTT 5.0 protocol?**  
**A**: MQTT.fx started supporting the MQTT 5.0 protocol from version 5.0 onwards. This update brought the software in line with the latest MQTT standards, adding new capabilities and enhancing user experience.

**Q: Is MQTT.fx free to use?**
**A**: MQTT.fx 5.0 offers a 3-month trial license for free. After the trial period, there are various paid licensing options, including a private user license for 49,90 EUR, a single license for 220,00 EUR/year, a team license for 650,00 EUR/year, and an enterprise license for 1.900,00 EUR/year, all prices including VAT for commercial use.

## MQTTX: The Best MQTT.fx Alternative You Should Try In 2024

We recommend using MQTTX, accessed at [mqttx.app](https://mqttx.app/), as an alternative. MQTTX is an All-in-One MQTT client toolbox compatible with macOS, Windows, Linux, and Docker. It offers versions for desktop, CLI, and web. MQTTX fully adheres to MQTT standards 5.0, 3.1.1, and 3.1, enhancing the development and testing of MQTT applications with advanced features such as Scripts, Benchmarks, and IoT Data Simulation.

![MQTTX](https://assets.emqx.com/images/3240de906bd11d729f68863cbf5768aa.png)





<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
