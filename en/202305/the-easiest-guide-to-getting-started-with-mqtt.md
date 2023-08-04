This article will show readers how to get started with the MQTT protocol, with code examples. Beginners of the IoT and MQTT can use this article to understand MQTT-related concepts and quickly start developing MQTT services and applications.



## What Is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe based messaging protocol designed for resource-constrained devices and low-bandwidth, high-latency, or unreliable networks. It is widely used in Internet of Things (IoT) applications, providing efficient communication between sensors, actuators, and other devices.



## Why Is MQTT the Best Protocol for IoT?

MQTT has emerged as one of the best IoT protocols due to its unique features and capabilities tailored to the specific needs of IoT systems. Some of the key reasons include:

- **Lightweight:** IoT devices are often constrained in terms of processing power, memory, and energy consumption. MQTT's minimal overhead and small packet size make it ideal for these devices, as it consumes fewer resources, enabling efficient communication even with limited capabilities.
- **Reliable:** IoT networks can experience high latency or unstable connections. MQTT's support for different QoS levels, session awareness, and persistent connections ensures reliable message delivery even in challenging conditions, making it well-suited for IoT applications.
- **Secure communications:** Security is crucial in IoT networks as they often transmit sensitive data. MQTT supports Transport Layer Security (TLS) and Secure Sockets Layer (SSL) encryption, ensuring data confidentiality during transmission. Additionally, it provides authentication and authorization mechanisms through username/password credentials or client certificates, safeguarding access to the network and its resources.
- **Bi-directionality:** MQTT's publish-subscribe model allows for seamless bi-directional communication between devices. Clients can both publish messages to topics and subscribe to receive messages on specific topics, enabling effective data exchange in diverse IoT ecosystems without direct coupling between devices. This model also simplifies the integration of new devices, ensuring easy scalability.
- **Continuous, stateful sessions:** MQTT allows clients to maintain stateful sessions with the broker, enabling the system to remember subscriptions and undelivered messages even after disconnection. Clients can also specify a keep-alive interval during connection, which prompts the broker to periodically check the connection status. If the connection is lost, the broker stores undelivered messages (depending on the QoS level) and attempts to deliver them when the client reconnects. This feature ensures reliable communication and reduces the risk of data loss due to intermittent connectivity.
- **Large-scale IoT device support:** IoT systems often involve a large number of devices, requiring a protocol that can handle massive-scale deployments. MQTT's lightweight nature, low bandwidth consumption, and efficient use of resources make it well-suited for large-scale IoT applications. The publish-subscribe pattern allows MQTT to scale effectively, as it decouples sender and receiver, reducing network traffic and resource usage. Furthermore, the protocol's support for different QoS levels allows customization of message delivery based on the application's requirements, ensuring optimal performance in various scenarios.
- **Language support:** IoT systems often include devices and applications developed using various programming languages. MQTT's broad language support enables easy integration with multiple platforms and technologies, fostering seamless communication and interoperability in diverse IoT ecosystems.
  You can visit our [MQTT Client Programming](https://www.emqx.com/en/blog/category/mqtt-programming) blog series to learn how to use MQTT in PHP, Node.js, Python, Golang, Node.js, and other programming languages.

**Learn more in our article: [What is MQTT and Why is it the Best Protocol for IoT?](https://www.emqx.com/en/blog/what-is-the-mqtt-protocol)**



## How Does MQTT Work?

To understand how MQTT works, you need to first master the concepts of MQTT Client, MQTT Broker, Publish-Subscribe mode, Topic, and QoS:

**MQTT Client**

Any application or device running the [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk) is an MQTT client. For example, an instant messaging app that uses MQTT is a client, various sensors that use MQTT to report data are a client, and various [MQTT testing tools](https://www.emqx.com/en/blog/mqtt-client-tools) are also a client.

**MQTT Broker**

The MQTT Broker handles client connection, disconnection, subscription, and unsubscription requests, and routing messages. A powerful MQTT broker can support massive connections and million-level message throughput, helping IoT service providers focus on business and quickly create a reliable MQTT application.

For more details on MQTT brokers, please check the blog [The Ultimate Guide to MQTT Broker Comparison in 2023](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

**Publish–subscribe pattern**

The publish-subscribe pattern differs from the client-server pattern in that it separates the client that sends messages (publisher) from the client that receives messages (subscriber). Publishers and subscribers do not need to establish a direct connection, and the MQTT Broker is responsible for routing and distributing all messages.

The following diagram shows the MQTT publish/subscribe process. The temperature sensor connects to the MQTT server as a client and publishes temperature data to a topic (e.g., `Temperature`), and the server receives the message and forwards it to the client subscribed to the `Temperature` topic.

![Publish–subscribe pattern](https://assets.emqx.com/images/a6baf485733448bc9730f47bf1f41135.png)

**Topic**

The MQTT protocol routes messages based on topic. The topic distinguishes the hierarchy by slash `/`, which is similar to URL paths, for example:

```
chat/room/1

sensor/10/temperature

sensor/+/temperature
```

MQTT topic support the following wildcards: `+` and `#`.

- `+`: indicates a single level of wildcards, such as `a/+` matching `a/x` or `a/y`.
- `#`: indicates multiple levels of wildcards, such as `a/#` matching `a/x`, `a/b/c/d`.

For more details on MQTT topics, please check the blog [Understanding MQTT Topics & Wildcards by Case](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).

**Quality of Service (QoS)**

MQTT provides three kinds of Quality of Service and guarantees messaging reliability in different network environments.

- QoS 0: The message is delivered at most once. If the client is not available currently, it will lose this message.
- QoS 1: The message is delivered at least once.
- QoS 2: The message is delivered only once.

For more details on MQTT QoS, please check the blog [Introduction to MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos).



## The MQTT Workflow

Now that we understand the basic components of MQTT, let’s see how the general workflow works:

1. **Clients initiate a connection** to the broker using TCP/IP, with optional TLS/SSL encryption for secure communication. Clients provide authentication credentials and specify a clean or persistent session.
2. **Clients either publish messages to specific topics or subscribe to topics** to receive messages. Publishing clients send messages to the broker, while subscribing clients express interest in receiving messages on particular topics.
3. **The broker receives published messages** and forwards them to all clients subscribed to the relevant topics. It ensures reliable message delivery according to the specified Quality of Service (QoS) level and manages message storage for disconnected clients based on session type.



## Getting Started with MQTT:  Quick Tutorial

Now we will show you how to start using MQTT with a few simple demos. Before we begin, you need to prepare an MQTT Broker and an MQTT Client.

### Prepare an MQTT Broker

You can create an MQTT broker through private deployment or a fully managed cloud service. Or use a free public broker for testing.

- **Private deployment**

  [EMQX](https://www.emqx.io/) is the most scalable open-source MQTT broker for IoT, [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges), and connected vehicles. You can run the following Docker command to install EMQX.

  ```apache
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **Fully managed cloud service**

  The fully managed cloud service is the easiest way to start an MQTT service. As shown below, [EMQX Cloud](https://www.emqx.com/en/cloud) starts in minutes and runs in 17 regions across AWS, Google Cloud, and Microsoft Azure.

  ![MQTT Cloud](https://assets.emqx.com/images/d019e0dbc27f706eca6256e11720eb9b.png?imageMogr2/thumbnail/1520x)

- **Free public MQTT broker**

  In this post, we will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, created based on the fully managed [MQTT cloud service - EMQX Cloud](https://www.emqx.com/en/cloud). The server information is as follows.

  - Broker Address： `broker.emqx.io`
  - TCP Port： `1883`
  - WebSocket Port： `8083`

### Prepare an MQTT Client

In this post, we will use the MQTT client tool provided by [MQTTX](https://mqttx.app/) that supports browser access: [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client). MQTT X also provides a [desktop client](https://mqttx.app/) and a [command line tool](https://mqttx.app/cli).

[MQTTX](https://mqttx.app/) is an elegant cross-platform MQTT 5.0 desktop client that runs on macOS, Linux, and Windows. Its user-friendly chat-style interface enables users to easily create multiple MQTT/MQTTS connections and subscribe/publish MQTT messages.

![MQTTX](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

<center>MQTTX Preview</center>

Currently, there are mature open-source MQTT client libraries for all programming languages. We have selected [popular MQTT client libraries & SDKs](https://www.emqx.com/en/mqtt-client-sdk) in various programming languages and provided code examples to help you quickly understand the use of MQTT clients.


### Create an MQTT Connection

Before using the MQTT protocol to communicate, the client needs to create an MQTT connection to connect to the broker.

Go to [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) with your browser and click on the `New Connection` button in the middle of the page and you will see the following page.

![Create an MQTT connection](https://assets.emqx.com/images/5e110d181ce8489c275d5674910fa16d.png?imageMogr2/thumbnail/1520x)

We enter `Simple Demo` in `Name` and click the `Connect` button in the upper right corner to create an MQTT connection. The following indicates that the connection is established successfully.

![MQTT connection successful](https://assets.emqx.com/images/9583db03a552b24980cf49005e3dc668.png?imageMogr2/thumbnail/1520x)

To learn more about MQTT connection parameters, please check out our blog post: [How to Set Parameters When Establishing an MQTT Connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection).



### Subscribe to The Wildcard Topic

Next, we subscribe to the wildcard topic `sensor/+/temperature` in the Simple Demo connection created earlier, which will receive the temperature data reported by all sensors.

As shown below, click the `New Subscription` button and enter the topic `sensor/+/temperature` in the Topic field in the pop-up box, keeping the default QoS at 0.

![MQTT Subscribe](https://assets.emqx.com/images/79321fd9e22058e27a256152b60908d6.png?imageMogr2/thumbnail/1520x)

Once the subscription is successful, you will see an additional record in the middle of the subscription list.

![MQTT subscription is successful](https://assets.emqx.com/images/3687ba334049a0ca19e3300a2cbc4a98.png?imageMogr2/thumbnail/1520x)

### Publish MQTT Messages

Next, we click the `+` button on the left menu to create two connections, `Sensor 1` and `Sensor 2` respectively, to simulate two temperature sensors.

![Create MQTT connections](https://assets.emqx.com/images/0c96ec70a51ecc605bad4972edd77fb1.png?imageMogr2/thumbnail/1520x)

Once the connection is created, you will see three connections and the online status dots to the left of the connections will all be green.

![MQTT connection created successfully](https://assets.emqx.com/images/70010ba4da8d452ab0f738d36013dd9a.png?imageMogr2/thumbnail/1520x)

Select the `Sensor 1` connection, enter the publish topic `sensor/1/temperature` in the bottom left part of the page, enter the following JSON format message in the message box, and click the publish button at the bottom right to send the message.

```json
{
  "msg": "17.2"
}
```

![Publish MQTT messages](https://assets.emqx.com/images/859966556e5649f1d6ec9bf378162def.png?imageMogr2/thumbnail/1520x)

The message is sent successfully as follows.

![MQTT message is sent successfully](https://assets.emqx.com/images/b1a46d8a415603d87e0c4244ee34bc02.png?imageMogr2/thumbnail/1520x)

Using the same steps, publish the following JSON message to the `sensor/2/temperature` topic in the Sensor 2 connection.

```json
{
  "msg": "18.2"
}
```

You will see two new messages for the Simple Demo connection.

![MQTT notification](https://assets.emqx.com/images/f815767a47f234424ae55ea0fe39eb04.png?imageMogr2/thumbnail/1520x)

Click on the Simple Demo connection and you will see two messages sent by the two sensors.

![MQTT messages](https://assets.emqx.com/images/f88de809773829f6a86dcedc2f612dd5.png?imageMogr2/thumbnail/1520x)



### MQTT Features Demonstration

#### Retained Message

When the MQTT client publishes a message to the server, Retained Message flag can be set. The Retained Message resides on the message server, and subsequent subscribers can still receive the message when they subscribe to the topic.

As shown below, we are sending two messages to the `retained_message` topic in the Sensor 1 connection with the `Retain` option checked.

![MQTT Retained Message](https://assets.emqx.com/images/5c7dcb078d223e0b6d33cb66241caa5d.png?imageMogr2/thumbnail/1520x)

Then, we subscribe to the `retained_message` topic in the Simple Demo connection. After the subscription is successful, the second retained message sent by Sensor 1 will be received, which shows that the server will only keep the last retained message for a topic.

![MQTT Retained Message](https://assets.emqx.com/images/afe8cca62d576404d5f622f362ef3592.png?imageMogr2/thumbnail/1520x)

For more details on Retained Message, please check the blog [The Beginner's Guide to MQTT Retained Messages](https://www.emqx.com/en/blog/mqtt5-features-retain-message).

#### Clean Session

In general, an MQTT client can only receive messages published by other clients when it is online. If the client is offline and then online, it will not receive messages during the offline period.

However, if the client connects with Clean Session set to false and goes online again with the same Client ID, then the message server will keep a certain amount of offline messages for the client and send them to the client when it comes online again.

> The public MQTT server used for this demonstration is set to keep offline messages for 5 minutes and the maximum number of messages is 1000 (no QoS 0 messages).

Next, we create an MQTT 3.1.1 connection and demonstrate the clean session with QoS 1.

> MQTT 5 uses Clean Start and Session Expiry Interval to improve Clean Session. For details, please refer to the blog [Clean Start and Session Expiry Interval](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval).

Create a connection named `MQTT V3`, set Clean Session to false, and choose MQTT version 3.1.1.

![MQTT Clean Session](https://assets.emqx.com/images/1472ce0ea8e728647d973cae56e6b1d5.png?imageMogr2/thumbnail/1520x)

Subscribe to `clean_session_false` topic after successful connection, and set QoS to 1.

![MQTT subscribe](https://assets.emqx.com/images/7a5792040185d956803cb7406b2df3af.png?imageMogr2/thumbnail/1520x)

After the successful subscription, click the Disconnect button in the upper right corner.

![Disconnect MQTT connection](https://assets.emqx.com/images/fd5726bd0e2a5b9d9d73a7095f322ecf.png?imageMogr2/thumbnail/1520x)

Next, create a connection named `MQTT_V3_Publish`, and the MQTT version is also set to 3.1.1. After the successful connection, publish three messages to the `clean_session_false` topic.

![Publish MQTT messages](https://assets.emqx.com/images/0659785e98cb03f9d6e78497e0adb26f.png?imageMogr2/thumbnail/1520x)

Then select the MQTT_V3 connection, click the connect button to connect to the server, and you will receive three offline messages.

![MQTT messages](https://assets.emqx.com/images/106cc289cbb3a07be2ed294dd97fe420.png?imageMogr2/thumbnail/1520x)

For more details on Clean Session, please check the blog [MQTT Persistent Session and Clean Session Explained](https://www.emqx.com/en/blog/mqtt-session).

#### Last Will

When the MQTT client makes a CONNECT request to the server, it can set whether to send the flag of Will Message , as well as the Topic and Payload.

When the MQTT client is abnormally offline (the DISCONNECT message is not sent to the server before the client disconnects), the MQTT server will publish a will message.

As follows, we create a connection named `Last Will`.

- To see the effect quickly, we set Keep Alive to 5 seconds.
- Set Last-Will Topic to `last_will`.
- Set Last-Will QoS to `1`.
- Set Last-Will Retain to `true`.
- Set Last-Will Payload to `offline`.

![MQTT Last Will](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png?imageMogr2/thumbnail/1520x)

After the connection is successful, we disconnect the computer network for more than 5 seconds (simulating an abnormal client disconnection), and then turn on the network again.

Then start the Simple Demo connection, and subscribe to the `last_will` topic. You will receive the will message set by the `Last Will` connection.

![MQTT Last Will](https://assets.emqx.com/images/a216808a1ba964bbddc75708bc55c072.png?imageMogr2/thumbnail/1520x)

For more details on MQTT Will Message, please check the blog [Use of MQTT Will Message](https://www.emqx.com/en/blog/use-of-mqtt-will-message).



## Learn More About MQTT

At this point, we have finished explaining and demonstrating the basic concepts of MQTT and its usage process, so readers can try their hand at using the MQTT protocol based on what they have learned in this article.

Next, you can check out [MQTT Guide 2023: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT Topics, Wildcards, Retained Messages, Last-Will, and other features. Explore more advanced applications of MQTT and get started with MQTT application and service development.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
