## Introduction

[Sparkplug](https://www.emqx.com/en/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot) is an Industrial IoT protocol that provides a standardized way to communicate with industrial devices and applications. An efficient, comprehensive Sparkplug solution can facilitate communication between devices and applications and empower the decision-making of IIoT adopters through insights from data.

This blog will give a practical example of implementing an [MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) solution using EMQX and Neuron.

## Essential Components: EMQX and Neuron

[EMQX](https://www.emqx.io/) is a popular [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) that supports the Sparkplug protocol, while Neuron is an industrial IoT platform that can be used to collect data from industrial devices and generate Sparkplug messages for applications.

[Neuron](https://neugates.io/) can collect the data from the devices and publish Sparkplug messages to the EMQX broker based on the data by reporting changes. EMQX will forward the messages to the application that subscribes to the relevant Sparkplug topic. However, EMQX is able to decode the Sparkplug messages through the rules engine. The messages are then used for data platforms, persistent storage for historical, and so on.

> Read our post to learn more about the architecture of Sparkplug solution: [MQTT Sparkplug Solution for Industrial IoT Using EMQX & Neuron](https://www.emqx.com/en/blog/mqtt-sparkplug-solution-for-industrial-iot-using-emqx-and-neuron) 

![MQTT Sparkplug solution](https://assets.emqx.com/images/eca65d9a9ab24cb2bc02ce929162d1b5.png)

In this blog, we will demonstrate how to get started with MQTT Sparkplug using EMQX and Neuron following these steps:

1. Install EMQX
2. Configure EMQX
3. Install Neuron
4. Configure devices in Neuron
5. Connect Neuron to EMQX
6. Check the result in MQTT X

Let’s start!

## Install EMQX

Download and install the EMQX MQTT broker on your server or machine. EMQX provides a community edition that can be downloaded for free from their website. Visit the website [http://www.emqx.io/](http://www.emqx.io/) and follow the documentation.

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>


## Configure EMQX

Once EMQX is installed, you need to configure it to support the Sparkplug protocol.

### Create Schema Registry in EMQX

Click the Create button in Schema Registry.

![Schema Registry](https://assets.emqx.com/images/414d1d19937f7b127bf078022516db5b.png)

Select the protobuf for **Parse Type** and fill in the schema with Sparkplug schema.

![Select the protobuf for **Parse Type**](https://assets.emqx.com/images/92713344955371feef0f189c2714564e.png)

### Create Rules in EMQX

The SQL statement used for decoding.

```
SELECT
 schema_decode('neuron', payload, 'Payload') as SparkPlugB
FROM
 "spBv1.0/group1/DDATA/node1/modbus"
```

The key point here is schema_decode('neuron', payload, 'Payload') :

- `schema_decode()` decodes the content of the payload field according to the Schema 'protobuf_person'.
- `as SparkPlugB` stores the decoded value in the variable "SparkPlugB".
- The last parameter `Payload` indicates that the message type in the payload is the 'Payload' type defined in the protobuf schema.

![Edit rules](https://assets.emqx.com/images/c86eaf113839e16ac2ef47fe65866ee2.png)

Then add the action with the following parameters:

- Action Type: Message Repost
- Purpose topic: SparkPlugB/test

This action sends the decoded "Payload" to the SparkPlugB/test topic in JSON format.

![Edit action](https://assets.emqx.com/images/a11c438376914cc10bda248d9dbace96.png)

## Install Neuron

Neuron is an industrial IoT platform that can be used to collect, store, and analyze data from industrial devices. You can download and install Neuron from their website. Visit the website [https://www.neugates.io/](https://www.neugates.io/)  and follow the documentation.

## Configure Devices in Neuron

Sparkplug devices are configured with a set of data points that define their capabilities and properties. You can configure Sparkplug devices using the Neuron platform by defining the data points and assigning them to specific devices.

Select the driver plugin module for devices.

![Select the driver plugin module for devices](https://assets.emqx.com/images/dee478a56cabf28982d95bc30d15c440.png)

Set up the driver parameters for device communication.

![Set up the driver parameters](https://assets.emqx.com/images/95ddaf88bdb5cc305bf8110b9f1ca87c.png)

![Device config](https://assets.emqx.com/images/2da88ff4dddec3ae4ffaca60fa384170.png)

Create Group and set up polling interval.

![Create group](https://assets.emqx.com/images/aa91471395538ceb7a7edb054f4bff59.png)

Add Tags to the Group and set up an address for each Tag.

![Add tags](https://assets.emqx.com/images/fb215e69ffcbe4e8ec6d52ac23351935.png)

## Connect Neuron to EMQX

Once Neuron is installed, you need to connect it to the EMQX broker. You can do this by configuring the MQTT connection settings in Neuron to point to the EMQX broker.

Select the Northbound communication driver (SparkplugB).

![Add app](https://assets.emqx.com/images/8a9ee5ab1a09cb5d70a62999e745722c.png)

Set up the driver parameters for EMQX connection.

![Set up the driver parameters](https://assets.emqx.com/images/c629e130b36ac53f66a21d9adfd8689a.png)

![App config](https://assets.emqx.com/images/64cbe0d49c98ab3dc482b6686f337223.png)

Subscribe to the Group you interested in.

![Add subscription](https://assets.emqx.com/images/a0f825a4446a6ab52153ec0a5da06efd.png)

## Check up on the Result in MQTTX

With EMQX and Neuron configured and connected, you can now publish and subscribe to Sparkplug data. You can use the Neuron platform to publish data to Sparkplug devices and subscribe to data from those devices.

[MQTTX](https://mqttx.app/) tool is used to subscribe to the data decoded by the codec function of the EMQX rule engine, as shown in the following:

![MQTTX SparkplugB](https://assets.emqx.com/images/38691752e5463c39951eddec129f91be.png)

## Conclusion

By following these steps, you can get started with MQTT Sparkplug using EMQX and Neuron. Keep in mind that this is just a basic overview, and there are many more advanced features and configurations that you can explore to customize your setup. We highly recommend you explore the powerful features of EMQX and Neuron to accelerate your IIoT development.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
