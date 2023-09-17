Unity is a popular game engine that is used to create a wide range of games and simulations. [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol based on publish/subscribe model, specifically designed for IoT applications in low bandwidth and unstable network environments.

MQTT can be used in Unity for a variety of purposes, including AR (Augmented Reality) games, IoT-enabled games that utilize sensors and other devices, and remote control of games and simulations. For example, in AR games, MQTT can be used to receive information about the world from the user's device, such as the locations of planar surfaces, the detection of objects, people, faces, and so on.

This blog provides a simple [Unity3d](http://unity3d.com/) project for using [M2MQTT](https://github.com/eclipse/paho.mqtt.m2mqtt) with Unity. The project includes an example scene with a user interface for managing the connection to the broker and testing messaging.

# Prerequisites

## Install Unity

Download the installers for all major platforms from the Unity website: [https://unity.com/download](https://unity.com/download).

## Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

In this blog post, we will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) at `broker.emqx.io`.

```
Server: broker.emqx.io
TCP Port: 1883
WebSocket Port: 8083
SSL/TLS Port: 8883
Secure WebSocket Port: 8084
```

The free public MQTT broker is exclusively available for those who wish to learn and test the MQTT protocol. It is important to avoid using it in production environments as it may pose security risks and downtime concerns.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/b4cff1e553053873a87c4fa8713b99bc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Practical Guide to MQTT Broker Selection
    </div>
    <div class="mb-32">
      Download this practical guide and learn what to consider when choosing an MQTT broker.
    </div>
    <a href="https://www.emqx.com/en/resources/a-practical-guide-to-mqtt-broker-selection?utm_campaign=embedded-a-practical-guide-to-mqtt-broker-selection&from=blog-using-mqtt-in-unity-with-m2mqttunity-library" class="button is-gradient">Get the eBook →</a>
  </div>
</section>

## M2MQTT for Unity

[M2MQTT library](https://github.com/CE-SDV-Unity/M2MqttUnity) is a simple [Unity3d](http://unity3d.com/) project for using [M2MQTT](https://github.com/eclipse/paho.mqtt.m2mqtt) with Unity. It includes an example scene with a UI for controlling the connection to the broker and for testing messaging. In this blog post, we will use the example scene to illustrate how to use MQTT to create an application that communicates with an MQTT broker.

To begin, download the repository from GitHub.

```
Git clone https://github.com/CE-SDV-Unity/M2MqttUnity.git
```

# **Import the Example Scenes**

Next, create a new Unity project in UnityHub.

![New Unity project in UnityHub](https://assets.emqx.com/images/df5df7aeb67cba3b8e326afa811f0ace.png)

Then, copy the `M2Mqtt` and `M2MqttUnity` folders from the downloaded M2MQTT repository to the `Assets` folder of the new Unity project.

![Copy the `M2Mqtt` and `M2MqttUnity`](https://assets.emqx.com/images/38244fa7514bf682f547c0168fdf18f4.png)

The library provides a test scene called `M2MqttUnity_Test`, located in the `M2MqttUnity/Examples/Scenes` folder. By inspecting the scene, we can see that the only script used to setup the MQTT Client is `M2MqttUnityTest.cs`, which is attached to the M2MQTT GameObject in the scene. However, this script is linked with other classes of the main folder `M2Mqtt`.

# Connect and Subscribe

Press `Play` to run the application. In the `Game` tab, you will see a default broker which is already offline in the Broker Address input box. You should replace it with the public MQTT broker (`broker.emqx.io`) we have prepared beforehand.

![Press `Play` to run the application](https://assets.emqx.com/images/ed8a1df0d2f4a6623c1be3a0de599554.png)

After replacing the address, click on "Connect" to establish a connection to the public MQTT broker.

![Click on "Connect"](https://assets.emqx.com/images/fc291b03470defbc144797ad20b7758d.png)

The corresponding code is very simple. It creates a connection to `broker.emqx.io`, and then subscribes to the topic "M2MQTT_Unity/test".

```
public void SetBrokerAddress(string brokerAddress)
        {
            if (addressInputField && !updateUI)
            {
                this.brokerAddress = brokerAddress;
            }
        }

        public void SetBrokerPort(string brokerPort)
        {
            if (portInputField && !updateUI)
            {
                int.TryParse(brokerPort, out this.brokerPort);
            }
        }

        public void SetEncrypted(bool isEncrypted)
        {
            this.isEncrypted = isEncrypted;
        }

        public void SetUiMessage(string msg)
        {
            if (consoleInputField != null)
            {
                consoleInputField.text = msg;
                updateUI = true;
            }
        }

        public void AddUiMessage(string msg)
        {
            if (consoleInputField != null)
            {
                consoleInputField.text += msg + "\\n";
                updateUI = true;
            }
        }

        protected override void OnConnecting()
        {
            base.OnConnecting();
            SetUiMessage("Connecting to broker on " + brokerAddress + ":" + brokerPort.ToString() + "...\\n");
        }

        protected override void OnConnected()
        {
            base.OnConnected();
            SetUiMessage("Connected to broker on " + brokerAddress + "\\n");

            if (autoTest)
            {
                TestPublish();
            }
        }

        protected override void SubscribeTopics()
        {
            client.Subscribe(new string[] { "M2MQTT_Unity/test" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }
```

# Publish MQTT Messages

We will use [**MQTT Client Tool - MQTTX**](https://mqttx.app/) as another client to test the message publishing and receiving.

![MQTTX Client Tool - MQTTX](https://assets.emqx.com/images/e4c4c7b8881eb127ff0555e9eb68084d.png)

After connecting, click on `Test Publish`. You will see that the "Test message" has been received by both the game client and MQTTX.

![Click on `Test Publish`](https://assets.emqx.com/images/ca89bd7e9468bea94c68d0346345d8f5.png)

!["Test message" has been received](https://assets.emqx.com/images/6d31b73d694b2e02f31c0e4fd439bba8.png)

The corresponding code is to use publish() function to publish a message “Test message” to topic "M2MQTT_Unity/test".

```
public void TestPublish()
        {
            client.Publish("M2MQTT_Unity/test", System.Text.Encoding.UTF8.GetBytes("Test message"), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
            Debug.Log("Test message published");
            AddUiMessage("Test message published.");
        }
```

# Receive Messages

![Receive Messages](https://assets.emqx.com/images/d186935dd01c49f768d42e703a8c81a3.png)

When using MQTTX to send another test message, the client will receive it and we can see it in the Game tab.

![Send another test message](https://assets.emqx.com/images/13304957c825cd5b9a1233aa9ebb4b84.png)

The corresponding code is to decode, process and display the message on the Game tab.

```
protected override void DecodeMessage(string topic, byte[] message)
        {
            string msg = System.Text.Encoding.UTF8.GetString(message);
            Debug.Log("Received: " + msg);
            StoreMessage(msg);
            if (topic == "M2MQTT_Unity/test")
            {
                if (autoTest)
                {
                    autoTest = false;
                    Disconnect();
                }
            }
        }

        private void StoreMessage(string eventMsg)
        {
            eventMessages.Add(eventMsg);
        }

        private void ProcessMessage(string msg)
        {
            AddUiMessage("Received: " + msg);
        }

        protected override void Update()
        {
            base.Update(); // call ProcessMqttEvents()

            if (eventMessages.Count > 0)
            {
                foreach (string msg in eventMessages)
                {
                    ProcessMessage(msg);
                }
                eventMessages.Clear();
            }
            if (updateUI)
            {
                UpdateUI();
            }
        }
```

# Summary

This blog post provides a guide to creating an application that communicates with an MQTT broker using Unity. By following this guide, you will learn how to establish a connection, subscribe to topics, publish messages, and receive real-time messages using the [M2MQTT library](https://github.com/CE-SDV-Unity/M2MqttUnity).

# Join the EMQ Community

To dive deeper into MQTT, explore our [**GitHub repository**](https://github.com/emqx/emqx) for the source code, join our [**Discord**](https://discord.com/invite/xYGf3fQnES) for discussions, and watch our [**YouTube tutorials**](https://www.youtube.com/@emqx) for hands-on learning. We value your feedback and contributions, so feel free to get involved and be a part of our thriving community. Stay connected and keep learning!



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
