## Introduction to MQTT Sparkplug

[Sparkplug](https://www.emqx.com/en/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot) is an Industrial IoT protocol that provides a standardized way to communicate with industrial devices and applications. An efficient, comprehensive Sparkplug solution can facilitate communication between devices and applications and empower the decision-making of [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) adopters through insights from data.

MQTT Sparkplug is a messaging protocol built on top of [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), a widely used messaging protocol for IoT. It already has all advantages of MQTT protocol. MQTT Sparkplug is designed specifically for the IIoT and includes additional features that make it suitable for industrial applications. It is an open-source protocol that is widely adopted in the industry

This blog will give a practical example of implementing an MQTT Sparkplug solution.

## Essential Components of MQTT Sparkplug Solution

To implement an MQTT Sparkplug solution, we need two components: an MQTT Broker and an edge node.

An [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) is used as the central broker for handling the communication between devices and applications in an IIoT environment. The MQTT broker is responsible for receiving messages from devices, forwarding them to the appropriate subscribers, and storing messages for later retrieval if necessary.

An edge node is a device or gateway that acts as an intermediary between devices and the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). It can handle local data processing and aggregation, as well as buffering and forwarding data to the MQTT broker. Edge nodes are typically used in IIoT environments where numerous devices generate large amounts of data and where network bandwidth is limited.

In the context of MQTT Sparkplug, edge nodes are responsible for implementing the Sparkplug specification, which includes handling the registration of devices, encoding and decoding data using the Sparkplug payload format, and organizing data using the Sparkplug topic namespace format. The edge node communicates with the MQTT broker using the MQTT protocol, and it may also run additional software to perform local analytics or processing on the data.

In this blog, we will demonstrate how to get started with MQTT Sparkplug using EMQX and Neuron.

[EMQX](https://www.emqx.io/) is a popular MQTT broker that supports the Sparkplug protocol, while Neuron is an [industrial IoT platform](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions) that can be used to collect data from industrial devices and generate Sparkplug messages for applications.

[Neuron](https://neugates.io/) can collect the data from the devices and publish Sparkplug messages to the EMQX broker based on the data by reporting changes. EMQX will forward the messages to the application that subscribes to the relevant Sparkplug topic. However, EMQX is able to decode the Sparkplug messages through the rules engine. The messages are then used for data platforms, persistent storage for historical, and so on.

## Install and Configure an MQTT Broker

### Install EMQX

Download and install the EMQX MQTT broker on your server or machine. EMQX provides a community edition that can be downloaded for free from their website. Visit the website [http://www.emqx.io/](https://www.emqx.io/docs/en/latest/deploy/install.html) and follow the documentation.

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

## Install and Configure an Edge Node

Neuron is an industrial IoT platform that can be used to collect, store, and analyze data from industrial devices. You can download and install Neuron from their website. Visit the website [https://www.neugates.io/](https://neugates.io/docs/en/latest/installation/installation.html)  and follow the documentation.

### Configure Devices in Neuron

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

### Connect Neuron to EMQX for MQTT Sparkplug

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
