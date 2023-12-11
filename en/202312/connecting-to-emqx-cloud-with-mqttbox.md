## Introduction to MQTTBox

[MQTTBox](https://github.com/workswithweb/MQTTBox) is an [MQTT client tool](https://www.emqx.com/en/blog/mqtt-client-tools) developed by Sathya Vikram. Initially, it was only used as an extended Chrome installation and was rewritten and open-sourced to become a desktop cross-platform independent software. The interface is simple and supports multiple clients online at the same time. However, client interaction still has some inconveniences, such as switching and sending messages. MQTTBox achieves powerful cross-platform features with Chrome. Combined with simple load-testing functions, it is an MQTT client tool worth trying.

MQTTBox fully supports the following functions:

- Easy to install through Chrome storage that supports Chrome OS, Linux, macOS, and Windows, and supports the independent installation of Linux, macOS, and Windows
- Support [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket), multiple TCP encrypted connections
- Save the history of sent messages
- Copy/paste the messages from the history
- Save subscription message history
- Test broker's load through a simple performance test, and visualize the test results through charts

## MQTTBox Installation

To install MQTTBox, visit the [MQTTBox GitHub page](https://github.com/workswithweb/MQTTBox). You will find the direct download links for various platforms, including Chrome, Linux, macOS, HTML App, and Windows. Choose the version that suits your operating system and follow the installation process of your platform.

## MQTT Basic Features Showcasing with MQTTBox

### Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with. 

[**EMQX Cloud Serverless**](https://www.emqx.com/en/cloud/serverless-mqtt) is a fully managed MQTT broker in the cloud that is quick to set up and ideal for small-scale IoT tests. It offers 1 million free monthly session minutes, perfect for maintaining a modest number of devices.

Please follow [our guide](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) for newcomers. After registering, you'll receive an instance complete with connection info and a CA certificate, mirroring your deployment's overview.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

![EMQX Cloud](https://assets.emqx.com/images/bd088e2e8fb7abea30c017f900d38bec.png)

### MQTT Connection

#### Initialization

After opening the software, enter the main interface of the software, click the `Create MQTT Client` button on the top menu bar, and join the `Create MQTT client page`.

![Create MQTT client page](https://assets.emqx.com/images/5bec8384d7e3328523168bc35596418f.png)

#### Create a Connection

After launching MQTTBox, go to the section for creating a new MQTT client. This demonstration will use WebSocket for the connection. Fill in the MQTT-related configuration details as follows:

- **Host and Protocol**: In the Host field, enter the address of your Serverless deployment. Select 'wss' (WebSocket Secure) as the connection protocol to ensure a secure connection.
- **Port**: Use port 8084 for secure WebSocket (WSS) connections.
- **Authentication**: Provide the username and password established during your Serverless configuration, which is necessary for secure access to the MQTT broker.
- **CA Certificate**: For your Serverless setup, selecting a CA certificate is essential for security. In the MQTTBox settings, choose 'CA Certificate Only' as the SSL Type and select the CA certificate file you downloaded earlier.

This configuration ensures a secure WebSocket connection to your MQTT broker using MQTTBox, leveraging the CA certificate for enhanced security.

> *Note: When filling in the Host, you need to fill in the complete address, including the port number of the connection. If it is a WebSocket connection, you need to add Path. If MQTT Broker enables user name/password authentication, you also need to enter Username/Password in the configuration page.*

![MQTT Client Settings](https://assets.emqx.com/images/1bee598ae336d39757a71dc4b63e38f4.png)

After saving successfully, you will enter a page of client details. If the button in the upper right corner shows `Connected` and its color is green, the MQTT client has been successfully connected. You can disconnect the client by clicking it again.

![Connected](https://assets.emqx.com/images/94db4ddea197401f84e03e00c22251da.png)

### Subscribe to a Topic

Once the connection is established, you can start subscribing to messages. Because the MQTT protocol uses a publish/subscribe model, we need to subscribe to a topic after connecting. Then, there will be messages on the Topic to receive messages from EMQX Cloud Serverless.

There are two input boxes for sending and subscribing by default in the client details page of MQTTBox. You can add multiple boxes if there are numerous subscriptions or different published content. Click the `Add Publisher` and `Add Subscriber` buttons in the top menu bar to add and manage various publishers/subscribers.

We first enter Topic: `testtopic/mqttbox` in the yellow box on the right. After selecting the QoS level, click the `Subscribe` button to subscribe to the related Topic.

### Publish MQTT Message

Then, we enter the Topic to be published in the blue box. Here, we enter the `testtopic/mqttbox` that we just subscribed to and select the QoS level as the default Payload Type that supports `String/JSON/XML/Characters`. After entering a section of JSON in the payload box, click the Publish button.

At this point, we can see the message published in the subscription box on the right. So far, we have created an MQTT client and successfully tested functions such as connection, publishing, and subscription.

![Publish MQTT Message](https://assets.emqx.com/images/5ab7b20942f86bc393c9d0ea8da97b14.png)

### TLS/SSL Connection

In addition to regular connections, MQTTBox also supports TLS/SSL connections.

Using EMQX Cloud, you can refer to this [document](https://docs.emqx.com/en/cloud/latest/deployments/tls_ssl.html) to create a certificate. We can enter the client details page, select the protocol as MQTTS/TLS or WSS, and then select save.

If it is two-way authentication, you can select the CA certificate file, the client certificate, and the client key file on the configuration page, then select the connection. Please confirm the TLS/SSL connection port and modify it before connecting.

![TLS/SSL Connection](https://assets.emqx.com/images/e3dc942066dd8481df7fb369e1e12cda.png)

## Discover Advanced Features of MQTTBox

### MQTT Load Testing

For MQTT load testing in MQTTBox, a simple WebSocket connection is typically employed, as CA certificates are not supported. This approach is suitable for scenarios where advanced encryption and security validation are not required, such as essential performance and functionality testing.

1. **Open MQTTBox** and select or create an MQTT client.
2. **Configure Load Test**:
   - **Load Test Name**: Enter a name like `serverless-test`.
   - **Protocol**: Choose the WebSocket protocol.
   - **Host**: Enter the server address and port, e.g., `broker.emqx.io:8083/mqtt`.
   - **Load Test Type**: Select `Publish`.
   - **# of Messages to Publish**: Set the number of messages, like `20`.
   - **Run Time (seconds)**: Set the test duration, e.g., `5` seconds.
   - **Time Out (seconds)**: Set a timeout period, such as `30` seconds.
   - **# of Instances to Run**: Choose the number of instances, e.g., `2`.
   - **Topic**: Specify the MQTT topic, like `testtopic/load`.
   - **QoS**: Choose the QoS level.
   - **Add Payload**: Input the payload, for instance, `hello`.
3. **Start the Load Test**: Confirm the settings and begin the test.
4. **Monitor the Test**: Observe the message transmission and system response.
5. **Analyze the Results**: Review and analyze the data after the test to understand the performance under the specified load.

![MQTT Load Testing 1](https://assets.emqx.com/images/1fa7db7fd1bc3080e3cfaded455f765c.png)
![MQTT Load Testing 2](https://assets.emqx.com/images/fc0c0ec3973239b42d0b7b8da19e991d.png)
![MQTT Load Testing 3](https://assets.emqx.com/images/7bf162d256db9cec4073ee5ad15afbfa.png)

The MQTT Load Testing feature in MQTTBox is designed to assess the performance and reliability of an MQTT broker or client under varying load conditions. This tool allows users to simulate real-world usage scenarios by sending a specified number of messages over a set period. It helps identify potential bottlenecks, understand capacity limits, and ensure the MQTT implementations' stability and efficiency. It is beneficial in environments where MQTT is used for critical data exchange and where maintaining consistent performance is essential.

## FAQs about MQTTBox

**Q: Does MQTTBox support multiple simultaneous connections?**  
**A**: MQTTBox allows users to create and manage multiple MQTT client connections simultaneously, making it a versatile tool for testing and managing different MQTT environments.

**Q: Can MQTTBox connect using both MQTT and MQTT over WebSocket protocols?**  
**A**: Yes, MQTTBox supports MQTT and MQTT over WebSocket protocols, and it allows connections over standard TCP, TCP/TLS (secure connections), as well as WebSocket Secure (WSS).

**Q: Is MQTTBox compatible with various operating systems?**  
**A**: Yes, MQTTBox is a cross-platform tool compatible with Chrome OS, Linux, macOS, and Windows, making it accessible to a wide range of users.

**Q: Can MQTTBox be used for MQTT load testing?**  
**A**: Yes, MQTTBox includes simple load-testing functionality, enabling users to test the broker's load and visualize the results through charts, which helps evaluate the performance of MQTT brokers.

**Q: Is MQTTBox a free tool?**  
**A**: Yes, MQTTBox is a free tool. Users can download and use it for free to connect, test, and manage MQTT clients.

## Introducing MQTTX: The Next Step in MQTT Tools

Unfortunately, MQTTBox is no longer being maintained. We recommend using MQTTX, accessed at [mqttx.app](https://mqttx.app/), as an alternative. MQTTX is an All-in-One MQTT client toolbox compatible with macOS, Windows, Linux, and Docker. It offers versions for desktop, CLI, and web. MQTTX fully adheres to MQTT standards 5.0, 3.1.1, and 3.1, enhancing the development and testing of MQTT applications with advanced features such as Scripts, Benchmarks, and IoT Data Simulation.

![MQTTX](https://assets.emqx.com/images/3240de906bd11d729f68863cbf5768aa.png)

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
