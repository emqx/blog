Recently, [the MQTT support in Postman](https://blog.postman.com/postman-supports-mqtt-apis/) has gained significant attention from developers. This is important news for Postman's support of eventing transport layers, and it can also simplify the development process for IoT developers. In this blog post, we will demonstrate how to establish a connection with [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) using Postman.

## Sign Up for Postman

Postman is a popular and versatile API development and testing tool that simplifies the process of working with APIs. With its intuitive interface and extensive feature set, Postman has become a go-to tool for developers across various domains. Now it expanded into the IoT field. If you haven't used Postman before, you can quickly register for a free account [here](https://www.postman.com/).

## Free Serverless MQTT Broker

EMQX Cloud Serverless is the latest [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. **Additionally, users can get 1 million free session minutes every month**, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

If you have not tried serverless deployment yet, please follow [the guide in this blog](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to create one for free. Once you have completed the registration process with the online guide, you will get a running instance with the following similar information from the “Overview” in your deployment. We will use the connection information later.

![EMQX Cloud](https://assets.emqx.com/images/ee156f2d3e8cd3e620e891150728d0bc.png)

Next, you need to configure the Authorization information in advance. The following image demonstrates how to configure these credentials under 'Authentication & ACL - Authentication' on the server side.

![Authentication & ACL - Authentication](https://assets.emqx.com/images/24a419e22962de960e149e00f3287b78.png)

## Creating a new MQTT request

To create a new MQTT request, click on the **New** button in the sidebar. This will open the **Create new** dialog. From the list, select **MQTT** to open a blank MQTT request in a new tab.

![Create a new MQTT request](https://assets.emqx.com/images/3c877775aabccd259cdfbfab617636b4.png)

## Connecting to EMQX Cloud Serverless

Next, you will see an MQTT Request page. Here, you can enter the information of the EMQ Cloud Serverless to establish a connection.

![Connect to EMQX Cloud](https://assets.emqx.com/images/74ac9072a65b33af520b4dcaa82d5745.png)


The URL format is: `wss://[connection address]:[port]/mqtt`. For example, here the address is `wss://*****..emqxsl.com:8084/mqtt`. The * represents the connection address in EMQX Cloud Serverless.

In addition to the address information, you also need to configure Authorization information before creating a Serverless MQTT connection.

![Connected](https://assets.emqx.com/images/53e6e70a006ec004cefa055915591a2c.png)

Click on "Connection", and you will see a message in the response area indicating that you're connected to the broker.

### Subscribing to topics

While connected to the broker, select the **Topics** tab. I will test the connection by transmitting the temperature and humidity data of the room.

1. In the **Topics** column, enter `home/device` as the topic name.
2. Select **Subscribe** to subscribe to the topic.

You will see a message in the response area indicating that you're subscribed to the topic.

![Subscribing to topics on Postman](https://assets.emqx.com/images/46afe41abc131b8b1dad8ef5e4cd6453.png)

### Publishing messages

You can use the **Message** tab to publish messages to the topic.

1. Select the **Message** tab and enter `{"Temperature": 27.5, "Humidity": 65}` as the message.
2. Enter `home/device` as the topic name and `JSON` as the message format.
3. Click on **Send** to publish the message.

You will see an outgoing message in the response area indicating that the message was published. Since you have already subscribed to the topic, `home/device`, you will also see an incoming message with the same body. Go ahead and send a few more messages containing the temperature and humidity of the room.

![Publishing messages on Postman](https://assets.emqx.com/images/399d7a02f414c3523802c14c2e987053.png)

### Using response visualizer

Now that you've subscribed to a topic and published a few messages, you can use the response visualizer to view the messages in a more comprehensible format.

1. Switch to the **Visualization** tab in the response area. You'll see the messages for the `Temperature` field visualized as a line chart.
2. Select **+** to add the `Humidity` field to the chart and view the changes in the values.

The visualization changes in real time as you receive newer messages for the same topic.

![Response visualizer](https://assets.emqx.com/images/1cfd42c449ffc52d912d8db30060f761.png)

## Summary

In this blog, we explored the latest MQTT features of Postman by connecting to the EMQX Cloud Serverless. It is evident that Postman already supports basic MQTT functionalities, such as establishing a connection, subscribing to topics, publishing messages, and receiving real-time messages. Additionally, it also allows for simple real-time response visualization.

Would you use Postman for developing MQTT or IoT applications? Join our [Discord](https://discord.com/invite/xYGf3fQnES) for discussions. Stay connected and keep learning!

## Reference

[Creating your first MQTT request](https://learning.postman.com/docs/sending-requests/mqtt-client/first-mqtt-request/)
