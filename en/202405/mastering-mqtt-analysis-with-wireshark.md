## **Introduction**

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight, publish-subscribe, machine-to-machine network protocol for message queue/message queuing service. It is designed for connections with remote locations that have devices with resource constraints or limited network bandwidth, such as in the Internet of Things (IoT).

As the scale of MQTT deployment and business operations continues to grow, it's becoming more crucial to learn how to analyze MQTT packet captures within the network. This blog will help you master the ins and outs of [MQTT packet](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) analysis using the Wireshark tool, enabling you to diagnose the MQTT exchange process and enhance your understanding of MQTT traffic patterns.

## **Understanding Wireshark**

Wireshark is a popular, open-source network protocol analyzer. It allows users to visualize, search, and analyze network traffic in a human-readable format.

Typically, Wireshark can be utilized to directly capture incoming and outgoing data on our local network card for analysis. Alternatively, we could also employ the tcpdump tool, available in Linux-like systems, to capture specific network traffic, save it as a file, and then open it with Wireshark for more visual analysis. This is usually more useful, especially in the production environment of MQTT, where client devices are often unable to use Wireshark for packet capture directly.

### Install Wireshark

You can visit the [download page](https://www.wireshark.org/download.html) to install Wireshark. In this blog, we used Wireshark 4.2.4 on MacOS M2.

After successful installation, you can see the following page when you open Wireshark:

![Wireshark:](https://assets.emqx.com/images/154b5638bdd0e41164dcb4c08b3d6bb6.png)

We can see the names of each network card of the current machine under Capture. Clicking on any name, Wireshark will start capturing all network traffic on that network card. There may be various different network card names here, due to the different network configurations of each computer.

### Introduction to the Visualization of a Packet

For example, if we click on "Wi-Fi: en0", we can get the following packet capture results (you can stop capturing by clicking the red button in the top left corner):

![Visualization of a Packet](https://assets.emqx.com/images/bcaf4a877ad50e0348dcb153a6c8a888.png)

In the table in the middle of the above picture, each network packet sent and received via Wi-Fi: en0 is arranged in chronological order from top to bottom. Take the marked line as an example:

- The sequence **Number** when this Frame was captured is `111`, this number starts accumulating from 1 at the beginning of the capture.
- The occurrence **Time** is `10:29:35.742488`
- The **Source IP Address is 121.12.119.240,** and the **Destination IP address is 172.31.4.204**. Since the IP address of the Wi-Fi: en0 in my local network is exactly `172.31.4.204`, this proves that this is a datagram sent from the outside to my computer.
- The recognized **Protocol** is `TLSv1.2`, and the **Length** of the entire Frame is 155 bytes.

Furthermore, we can view the details of this Frame through the two marked box areas below, i.e., Source and Destination Port, and each parsed protocol fields.

## Setting up the Testing Environment

### MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

In this guide, we will utilize the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, built on [EMQX](https://www.emqx.com/en/products/emqx) Platform. The server access details are as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**
- WebSocket Port: 8083
- SSL/TLS Port: 8883
- Secure WebSocket Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

### MQTT Client

We recommend using MQTTX as the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) for testing. [**MQTTX**](https://mqttx.app/) is an open-source, cross-platform MQTT 5.0 desktop client initially developed by EMQ, which can run on macOS, Linux, and Windows. Download MQTTX [here](https://mqttx.app/).

After successful installation, open MQTTX and click on the button shown in the following picture. This will allow you to add a new connection and test if the MQTT Client can work with the Broker:

![MQTTX](https://assets.emqx.com/images/461e9c7d64b9bbb81f9fe4800eac6950.png)

Fill in the MQTT Broker information mentioned above as follows (Username and Password are both `wireshark`):

![Fill in the MQTT Broker information](https://assets.emqx.com/images/7c037430e4078408ebf6d123dfb9b0f5.png)

Then click the Connect button in the upper right corner, you will see that MQTTX has successfully connected to the MQTT Broker. This proves that the environment for testing is ready.

## **Analyzing MQTT Traffic with Wireshark**

Once all preparations are complete, we can begin capturing network traffic using Wireshark and analyzing several major MQTT interaction processes.

### Connecting Process

Capture Steps:

- Open MQTTX and Wireshark
- Start capturing packets on the main network card in Wireshark (for me it's Wi-Fi: en0)
- Go back to MQTTX and create a new connection as mentioned in the previous step

After the connection is successfully created, filter in Wireshark by the protocol keyword `mqtt` to get the captured content as shown below:

![Filter MQTT](https://assets.emqx.com/images/a5b0274649ee0231f20d0ad32fcc41ad.png)

Overall, the connecting process will only generate 2 MQTT messages:

1. Connect Command sent from the MQTTX client (182.31.4.204) to the MQTT Broker (54.244.173.190)
2. The MQTT Broker will immediately reply with a Connect Ack to indicate the result of the connecting request.

#### Connect Command

![Connect Command](https://assets.emqx.com/images/886fa9b82986048f20dfa86ae6281138.png)

By selecting the **Connect Command**, you can view the specific values of the connection parameters. For example:

- `Version: MQTT v5.0` shows that the protocol version of the requested connection is MQTT v5.0
- `Keep Alive: 60` communicates that the heartbeat time is 60 seconds
- And the values for `Client ID`, `User Name` and `Password` are also displayed.

For more detailed specifications, you can refer to: [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901035) 

#### Connect Ack

![Connect Ack](https://assets.emqx.com/images/649e64c7b12f0229518ed6c221a2d8bd.png)

By selecting the **Connect Ack**, you can view the specific values of the connection parameters. For example:

- `Reason Code: Success(0)` means the connection is successful
- `Maximum Packet Size: 1048576` indicates the maximum packet size allowed by the server is 1048576 bytes
- `Retain Available` `Shared Subscription Available` `Subscription Identifier Available` indicates that the server supports these features

For more detailed specifications, you can refer to: [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901074) 

### Subscribe Process

Steps:

- Keep Wireshark open for packet capture on the Wi-Fi: en0 network card
- Use MQTTX to create a subscription with the topic `wireshark/testtopic`

After completion, we can see something similar to the following:

![Subscribe](https://assets.emqx.com/images/ae88c2cf4c72fceff2ebdd0d4ec1219f.png)

The figure illustrates that the entire subscription process comprises only two MQTT messages:

- The 'Subscribe Request' represents the subscription request that MQTTX sends to the MQTT Broker.
- The 'Subscribe Ack' signifies the MQTT Broker's response to its subscription result.

#### Subscribe Request

![Subscribe Request](https://assets.emqx.com/images/82db6cfe7690b874e9adf68f541c882c.png)

The message details reveal the following:

- `Message Identifier: 12509` indicates that the ID of this subscription request is 12509, and the subscription result returned by the MQTT Broker should also respond with the same ID.
- `Topic: wireshark/testtopic` shows that the requested subscription topic is `wireshark/testtopic`.
- `Subscription Options` denote the parameters for the requested subscription. The frequently used `QoS` parameter indicates a requested subscription QoS level of 1.

For more detailed specifications, you can refer to: [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901161) 

#### Subscribe Ack

![Subscribe Ack](https://assets.emqx.com/images/3cb228f1530a2dadba0d56ce620d222b.png)

The message details reveal the following:

- `Message Identifier: 12509` indicates which request ID this message corresponds to.
- `Reason Code: 1` indicates that the MQTT Broker successfully granted the QoS level of 1. Its values are
  - `0` `1` `2` represent the QoS levels granted by the Broker
  - Greater than or equal to `128` indicates subscription failure, for example, `135` indicates the Client is not authorized to make this subscription `162` indicates The Server does not support Wildcard Subscriptions

For more detailed specifications, you can refer to: [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901171) 

### Publish to MQTT Broker

Here, we focus on the packet capture analysis of the most complex QoS 2 messages. The logic for QoS 1 and QoS 0 is similar, though their processes are simpler, and thus are not discussed separately.

Steps：

- Keep Wireshark open for packet capture on the Wi-Fi: en0 network card
- Use MQTTX to publish a QoS2 message to the Broker with the topic `wireshark/testtopic`

![Publish to MQTT Broker](https://assets.emqx.com/images/c5f18e7f24633800f939d09fd92f0bf5.png)

After completion, we can see something similar to the following:

![Publish](https://assets.emqx.com/images/4792f45eb64bbbd9ed5fc4f2ebc7643b.png)

QoS 2 is more complex than QoS 0 and QoS 1 as it ensures messages are sent only once. This requires a total of four MQTT messages:

- The `Publish Message` from the client to the Broker carries the message topic, QoS level, payload, and more.
- If the message is QoS 2, the Broker replies with a `Publish Received` of the same ID, indicating successful receipt of the message.
- After receiving the `Publish Received` from the Broker, the client sends a `Publish Release`. This indicates the completion of the first stage of message delivery. If the `Publish Received` is not timely received, the `Publish Message` will be resent.
- After the Broker receives the `Publish Release` from the client, it sends a `Publish Complete` to indicate the completion of the entire sending process.

For a more detailed introduction, you can refer to: [MQTT QoS 0, 1, 2 Explained: A Quickstart Guide](https://www.emqx.com/en/blog/introduction-to-mqtt-qos) 

#### Publish Message

![Publish Message](https://assets.emqx.com/images/1095570f0f7b3f76ddb442ab57dd2305.png)

The message details reveal the following:

- `QoS Level: 2` in `Header Flags` indicates that this is a QoS 2 message
- `Topic: wireshark/testtopic` indicates that the topic of the message is `wireshark/testtopic`
- `Message Identifier: 49457` indicates that the ID of this message is 49457, which matches the subsequent response message.
- `Message` is the content of the message

#### Publish Received, Publish Release and Publish Complete

The remaining three messages are quite similar. They all confirm the previous message using the same message ID `49457`:

![Publish Received](https://assets.emqx.com/images/634c69bfa275f51c3b1540e35a77a17d.png)

## **Conclusion**

Through this guide, we have explored how to effectively use Wireshark to analyze MQTT traffic, which is crucial for network administrators, developers, and IoT enthusiasts alike. With these tools, you can troubleshoot network issues, optimize MQTT traffic, and even uncover potential security vulnerabilities.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
