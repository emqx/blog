## Introduction to MQTT Explorer

[MQTT Explorer](https://mqtt-explorer.com/) is an active MQTT client desktop application popular among developers. It is based on Electron technology and was developed by Thomas Nordquist. The application was open-sourced and follows the  [Creative Commons Public Licenses](https://wiki.creativecommons.org/wiki/Considerations_for_licensors_and_licensees#Considerations_for_licensees) protocol. Its GitHub address is [https://github.com/thomasnordquist/MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer).

Its main features are:

- Essential subscription/push/connection function
- User authentication function
- WebSocket support
- Support diff view and multiple types of Payload
- Basic historical information log
- Support TLS connection
- Support night mode

It's worth highlighting some great features, such as:

- Automatically subscribe to the topic of $SYS to quickly check broker status information.
- Organize the subscription list in a tree structure to facilitate users to view their attribution.
- With message visualization function and intuitive and interactive statistical chart design.

MQTT Explorer can meet most development needs, but it also has some disadvantages:

- Only one connection can exist at a time, which is inconvenient for debugging multiple-connections multiple connections.
- Publish Payload and Subscribe Message lists are not separated in UI design, so checking the status of sending and receiving messages is difficult.
- There is no complete operation log record, which makes it inconvenient for developers to check the information interacting with the server.

## MQTT Explorer Installation

To install MQTT Explorer, download the appropriate installer for your operating system from [mqtt-explorer.com](https://mqtt-explorer.com/) or the GitHub releases page at [thomasnordquist/MQTT-Explorer/releases](https://github.com/thomasnordquist/MQTT-Explorer/releases). The website and GitHub offer downloads for Linux, Windows, and macOS, so choose the file (.exe for Windows, .dmg for macOS) that matches your system.

## MQTT Basic Features Showcasing with MQTT Explorer

### Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with. 

[**EMQX Cloud Serverless**](https://www.emqx.com/en/cloud/serverless-mqtt) is a fully managed MQTT broker in the cloud that is quick to set up and ideal for small-scale IoT tests. It offers 1 million free monthly session minutes, perfect for maintaining a modest number of devices.

For newcomers, please follow our [guide](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to start. After registering, you'll receive an instance complete with connection info and a CA certificate, mirroring your deployment's overview.

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

![EMQX Cloud](https://assets.emqx.com/images/bd088e2e8fb7abea30c017f900d38bec.png)

### Preview of MQTT Explorer

The figure below shows the main page, which consists of the topic search bar and connection configuration at the top. On the lower left side of the page, there is a tree structure that displays the topic, and on the right side, there are columns for Publish, Subscribe, Payload, and History information control.

![Preview of MQTT Explorer](https://assets.emqx.com/images/deeef9426b47286487117c01463863d8.png)

### MQTT Connection and Subscription

#### Initialization page

The configuration page will pop up when you enter MQTT Explorer for the first time.

![MQTT Explorer initialization page](https://assets.emqx.com/images/1a05e11d096b92696cf092e749fd9ffd.png)

#### Create a connection

1. **Initiate a New Connection**: In the MQTT Explorer, click 'Connections' to set up a new connection.
2. **Server Details**: Use the address of your recently created serverless deployment. This can typically be found in your emqx cloud console.
3. **Authentication**: Enter the username and password provided during your serverless setup for secure access.
4. **Secure Connection Setup**: Download the CA certificate from your serverless console. Set the port to either 8883 or 8084 and enable TLS. Then, in the advanced settings of the connection page, select the CA certificate you just downloaded to establish a secure connection.

![Create a connection](https://assets.emqx.com/images/3650f07601ad62ab699b2e31cfe4855c.png)

#### Subscribe to a Topic

Then, click `Advanced`. Because EMQX Cloud prohibits the `$SYS` topic and the `#` topic by default, we delete them and enter a test subscription topic with the name `test/1`, and the result is shown in the figure below.

![Subscribe to a MQTT Topic](https://assets.emqx.com/images/9ac3cc8871b8b2cf403830a3ceb883d0.png)

#### Connect

Finally, click `Back` to return to the connection configuration page, and click `Connect` to complete the connection of EMQX Cloud and the subscription of the topic `test/1`.

Once the connection is established, you can observe that the subscription tree structure has two nodes - `test` and `1`. The status bar at the top right indicates the connection has been successfully established. You will also notice that the topic `test/1` is displayed on the right-hand side.

![MQTT Explorer](https://assets.emqx.com/images/634454ade8036770220af11858ca2fb8.png)

### MQTT Message Publishing

Once the connection is established, type `/test/1` in the topic box at the bottom right corner of the page. Then, please type your message and click on `Publish` to send it.

![MQTT Message Publishing](https://assets.emqx.com/images/bce3d1a202407cfe83576309a94b42a5.png)

### Receiving Subscription Messages

After the publication is successful, the message just published will be received in the Value card at the top right.

![Receiving Subscription Messages](https://assets.emqx.com/images/df6da94ccc9706d236c2ed6f233a99d8.png)

### Receiving History

You can view the message records received by the relevant subscription topic in the "Value" module, which includes a history of these messages.

### Statistical Information

Statistical information will be displayed at the bottom right corner of the page.

## Discover Advanced Features of MQTT Explorer 

### Topic Tree

MQTT Explorer's Topic Tree feature provides a comprehensive and structured overview of [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), greatly simplifying device and service management on your broker. Key functionalities include:

- **Visualizing Topics and Activity**: See all MQTT topics and their activities.
- **Topic Search/Filter**: Powerful tools to quickly locate specific topics or messages.
- **Recursive Topic Deletion**: Manage and maintain the MQTT environment by deleting topics recursively.
- **Diff View**: Track changes in messages with a different view of current versus previous messages.
- **Publishing Topics**: Easily publish new topics directly within MQTT Explorer.
- **Plotting Numeric Topics**: Graphically represent numerical data for analysis and understanding.
- **Retaining Topic History**: Keep a detailed history of each topic for data tracking and analysis.

These features make the Topic Tree an essential tool for effective MQTT topic management and analysis in MQTT Explorer.

![image.png](https://assets.emqx.com/images/f80e3b9b302635714743b2faafafa9c8.png)

## FAQs about MQTT Explorer 

**Q: Can MQTT Explorer support multiple connections simultaneously?**

**A:** No, MQTT Explorer currently supports only one active connection at a time. This can be a limitation for debugging multiple connections.

**Q: How does MQTT Explorer handle different payload formats?**

**A:** MQTT Explorer supports multiple payload formats, including JSON, Hex, and Base64, and provides diff view capabilities to compare current and previous messages.

**Q: How do I manage topic subscriptions in MQTT Explorer?**  
**A**: In MQTT Explorer, manage subscriptions in the "Advanced Configuration" page of the connection settings. This includes adding and deleting subscription topics. Note that dynamic subscription changes are not possible once connected.

**Q: Can I dynamically subscribe and unsubscribe to topics after establishing a connection?**  
**A**: Dynamic subscription changes are impossible in MQTT Explorer after establishing a connection unless subscribed to `#` for all messages, and the broker has no wildcard restrictions. Set all subscriptions in the advanced configuration before connecting.

**Q: Why are** `#` and `$SYS/#` the default subscriptions?  
**A**: `#` is used as a wildcard to match all topics, and `$SYS/#` is for system status information from the MQTT broker. This setup provides immediate, broad topic coverage upon connection.

## MQTTX: The Best MQTT Explorer Alternative You Should Try In 2024

Unfortunately, MQTT Explorer is no longer actively maintained. We recommend using MQTTX, accessed at [mqttx.app](https://mqttx.app/), as an alternative. MQTTX is an All-in-One MQTT client toolbox compatible with macOS, Windows, Linux, and Docker. It offers versions for desktop, CLI, and web. MQTTX fully adheres to MQTT standards 5.0, 3.1.1, and 3.1, enhancing the development and testing of MQTT applications with advanced features such as Scripts, Benchmarks, and IoT Data Simulation.

![MQTTX](https://assets.emqx.com/images/3240de906bd11d729f68863cbf5768aa.png)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
