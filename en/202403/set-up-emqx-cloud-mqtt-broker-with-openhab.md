## **Introduction**

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol designed for IoT and M2M communication. It operates on a publish-subscribe model, facilitating efficient message exchange between devices and a central broker. MQTT is known for its simplicity, low bandwidth usage, support for various Quality of Service levels, asynchronous communication, and robust security features, making it a popular choice for IoT applications requiring reliable messaging over constrained networks.

OpenHAB is an open-source home automation platform designed to integrate and control diverse smart home devices and technologies. It offers unified control through a central hub, supports various protocols for device integration, enables advanced automation, provides flexibility for customization, and benefits from a thriving community of users and developers. 

In this article, we will use an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to connect to openHAB, greatly leveraging openHAB's extension capabilities. Once we associate MQTT devices with openHAB, we can link these devices with other smart home devices to complete smart home management and coordination.

## Why Use MQTT in openHAB?

1. **Interoperability**: MQTT is widely supported, enabling seamless integration of various smart home devices within openHAB.
2. **Flexibility**: MQTT's lightweight design allows for adaptable communication between devices, enabling custom automation rules.
3. **Scalability**: MQTT scales well for both small and large smart home setups, ensuring efficient communication and control.
4. **Reliability**: MQTT's Quality of Service levels guarantee message delivery, maintaining system stability even in challenging network conditions.
5. **Community Support**: Both MQTT and openHAB have active communities, providing resources and assistance for setting up and customizing smart home automation.

## **A Step-by-Step Guide on Integrating MQTT with openHAB**

### Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

We will use EMQX Serverless in this article. EMQX Serverless is an MQTT broker offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. Additionally, users can get 1 million free session minutes every month, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

### Set up an EMQX Serverless Deployment

Register for an account to access EMQX Console. 

<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


#### 1. Create a Serverless Deployment

Log in to the Console and click the “New Deployment” button to begin creating a new deployment. Select the “Serverless” plan to deploy in the region close to your service.

![EMQX Serverless](https://assets.emqx.com/images/b808a557efcc18a007da93b43c6ddd64.png)

Set the Spend Limit to 0, which means we can have a MQTT Serverless deployment for free. Then, click “Deploy” to initiate the serverless deployment.

![Set the Spend Limit to 0](https://assets.emqx.com/images/06bd6058fb5a8a1939307e4539cedbc1.png)

#### 2. Add a Credential for the MQTT Connection

In the Console, navigate to “Authentication & ACL” from the left menu, and then click “Authentication” in the submenu. Click the “Add” button on the right and provide a username and password for the MQTT connection. For this example, we will use `emqx` as the username and `public` as the password for the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) connection.

![Add Authentication](https://assets.emqx.com/images/03d84484e5bafbb107b2bb7051a10b84.png)

With these steps, your MQTT Serverless is now operational and ready for use.

![Deployment status](https://assets.emqx.com/images/97ab561e5f132c2ab4c9d222f96e233a.png)

### Download and Install OpenHAB

Download OpenHAB ([Download page](https://www.openhab.org/download/)) and install it. Once openHAB is installed and started, launch the user interface by navigating to `http://localhost:8080` (if not running locally, replace localhost with the server's address or hostname accordingly).

### Install MQTT Binding

Navigate to Add-on Store, find MQTT Binding in openHAB Distribution. Click “INSTALL” button to install.

![openHAB Install MQTT Binding](https://assets.emqx.com/images/a05e3c09fcc723e424447829e56f3801.png)

### Add Things from MQTT Binding

In openHAB, "Things" are the physical or virtual devices integrated into the home automation system, such as lights, sensors, or switches. They serve as the interface between openHAB and these devices, enabling users to monitor and control them within the openHAB environment.

Navigate to Settings - Things page, click “+” to create a Thing from MQTT Binding we installed in the last step.

![Add Things from MQTT Binding](https://assets.emqx.com/images/acefb0640cb8de82a675eff922631039.png)

On the next page, we add a MQTT Broker.

![Add a MQTT Broker to openHAB](https://assets.emqx.com/images/719d856ccaae59c9cfc9587c969970a2.png)

In the configuration, enter the Broker host and port which can be found on EMQX Serverless deployment overview page. Enable **Secure Connection** and Select **TCP** as protocol.

![Enable **Secure Connection** and Select **TCP** as protocol.](https://assets.emqx.com/images/b40ccbb84d1bbaa52cc21ace183deb30.png)

MQTT 3 is the established version of the protocol, featuring QoS levels, retained messages, and clean sessions. [MQTT 5](https://www.emqx.com/en/blog/introduction-to-mqtt-5), the latest version, introduces advanced features like user properties, shared subscriptions, message expiry, topic aliases, and response codes, enhancing flexibility and scalability.

MQTT offers three levels of Quality of Service (QoS):

1. QoS 0: "At most once" - Messages are delivered without acknowledgment.
2. QoS 1: "At least once" - Messages are guaranteed to be delivered, possibly resulting in duplicates.
3. QoS 2: "Exactly once" - Ensures each message is delivered exactly once, with the highest reliability.

![QoS](https://assets.emqx.com/images/dc1ffba946bda466dd586b508983100d.png)

Input Username and Password, which can be found on the EMQX Serverless Authentication page. 

![Input Username and Password](https://assets.emqx.com/images/b0e99c9be95537e221cd80d7b34aa867.png)

Following the setup, we'll have an operational MQTT Broker successfully linked with openHAB.

![MQTT Broker successfully linked with openHAB](https://assets.emqx.com/images/bde976210369c0f0599a97a65f5fd61a.png)
![EMQX Console](https://assets.emqx.com/images/40473d55538197ff6fbe28bd5ae1414a.png)

### Add Channel for MQTT Device

In openHAB, "Channels" act as communication links between Things and Items, representing specific functionalities or data points of a Thing. They enable users to control or monitor the capabilities of Things by sending commands or receiving updates.

![Add Channel for MQTT Device](https://assets.emqx.com/images/c206957c727bad99390568933d16f468.png)

For MQTT Broker, there is one channel type: Publish trigger. This channel is triggered when a value is published to the configured [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) on this broker connection. Then we need to define an MQTT Topic. Any message sent to this topic will trigger the the channel event.

![Add emqx_channel](https://assets.emqx.com/images/4b0a45a9cdff8e3ad3216d29249adf61.png)

Assign an item to the channel. Here, we can specify its type and category.

![Add a new Item](https://assets.emqx.com/images/7f26d47c8c8d3a27c48c3903ca960540.png)

This completes the connection of a simple smart home device. When a device connects to EMQX Serverless and sends a message to the `t/emqx` topic, it triggers the Channel and sends instructions to the corresponding device.

## **Conclusion**

The usage of MQTT in openHAB facilitates seamless communication and control among smart home devices within the openHAB ecosystem. It enables device integration, message passing, topic-based communication, event triggering, and remote access/control. MQTT's role in openHAB enhances interoperability and flexibility, empowering users to create sophisticated smart home automation solutions.

EMQX Serverless simplifies the deployment and management of MQTT messaging infrastructure, offering powerful capabilities. By leveraging EMQX Serverless, you can streamline development processes and seamlessly integrate with openHAB to build comprehensive solutions.



**Related Resources**

- [Home Assistant and MQTT: 4 Things You Could Build](https://www.emqx.com/en/blog/home-assistant-and-mqtt-4-things-you-could-build)
- [MQTT with Zigbee: A Practical Guide](https://www.emqx.com/en/blog/mqtt-with-zigbee-a-practical-guide)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
