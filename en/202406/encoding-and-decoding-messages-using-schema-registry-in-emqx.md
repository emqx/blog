## Introduction

The Schema Registry offers a centralized solution for managing and validating message data for topics, as well as for serializing and deserializing data over the network. [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) publishers and subscribers can utilize the Schema to maintain data consistency and compatibility. As a crucial part of the rule engine, the Schema Registry can be tailored to various device access and rule design scenarios, ensuring data quality, compliance, efficient application development, and optimal system performance.

In the latest version of EMQX Dedicated, users can configure schemas using Avro, Protobuf, and JSON Schema in the EMQX Platform Console. This blog will demonstrate this feature by encoding and decoding Protobuf messages between MQTTX and a Dedicated deployment.

## Step 1: Set up an EMQX Dedicated Deployment

Register for an EMQX account to access a 14-day free trial of an EMQX Dedicated deployment. No credit card is required. 

<section class="promotion">
    <div>
        Try EMQX Dedicated for Free
        <div>No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient">Get Started →</a>
</section>

#### 1. Create a Dedicated Deployment

Log in to the EMQX Platform Console and click the ‘New Deployment’ button. Select the ‘Dedicated’ plan and configure a Dedicated deployment.

![Select the ‘Dedicated’ plan](https://assets.emqx.com/images/2a40c63eb53d7fe0f5943ef902748fb1.png)

For this tutorial, choose the *N.Virginia* region and the 1,000 tier, leave the EMQX version as the default setting (v5) and then click the 'Deploy' button. 

> Schema Registry is available in both v5 and v4 deployments (new created). In v5, you can set schema of Avro, Protobuf, and JSON Schema. In v4, you can set schema of Avro and Protobuf.

![Choose the *N.Virginia* region and the 1,000 tier](https://assets.emqx.com/images/794ff1be14bbbd9d596a3de4e09a2d17.png)

#### 2. Add a Credential for the MQTT Connection

When the deployment is created, navigate to ‘Access Control’ in the deployment console, then click *Authentication* in the submenu. Click the ‘Add’ button on the right and provide a username and password for the MQTT connection. For this example, we will use "emqx" as the username and "public" as the password for the MQTT client connection.

![Add Authentication](https://assets.emqx.com/images/078d3a6a6ab17c1f64dd461d8cf16e38.png)

Your MQTT broker is now operational and ready for use. Let’s now proceed to Step 2.

## Step 2: Use MQTTX to Set up Protobuf Schema

MQTTX provides desktop and CLI that support Protobuf message transmission. Visit the [MQTTX official website](https://mqttx.app/downloads) to download the appropriate version based on your requirements.

### Use Protobuf Messages with MQTTX Desktop

The latest version of the MQTTX desktop client features an optimized Schema section, with new custom functions and Schema scripting capabilities. These improvements significantly enhance the ease of handling and viewing data in the Protobuf format.

#### **1. Navigate to the Schema Script Page**

Start the MQTTX client, click the “Scripts” icon in the left menu bar, then select the “Schema” tab. Upon entering this page, there’s a simple default example.

![Schema Script Page](https://assets.emqx.com/images/42a5794ced5c784e6457e11db3578874.png)

#### 2. Input or Import a .proto File

You can enter the content of a proto file directly in the editor, as demonstrated in the example below. After that, click the "Save" button in the top-right corner to create a new proto Schema in MQTTX. If you have a pre-existing .proto file, you can simply click the "Import .proto File" button in the top right to upload it.

Here’s a commonly used proto format in IoT:

```
syntax = “proto3”;

package IoT;

message SensorData {
  string deviceId = 1;
  string sensorType = 2;
  double value = 3;
  int64 timestamp = 4;
}
```

This proto file defines a `SensorData` message, including device ID, sensor type, sensor value, and timestamp.

![Schema](https://assets.emqx.com/images/af156b57820e799c961a82993808e96e.png)

#### 3. Connect to the Deployment and Run the Script

In MQTTX, click “New Connection” and complete the connection form:

- **Name**: Enter a connection name of your choice.
- **Host**: This is the MQTT broker connection address, available on the EMQX Dedicated overview page.
- **Port**: The MQTT broker connection port, also found on the EMQX Dedicated overview page.
- **Username/Password**: Use the username and password specified in the Authentication settings.

![New Connection](https://assets.emqx.com/images/b07422bb743385ca416692ab5eac02d9.png)

After the connection is established, click the dropdown in the connection page’s top right corner and choose “Run Script”.

 ![Run Script](https://assets.emqx.com/images/c778232820378601eee1788eb46c2f55.png)

- **Apply to Publish or Subscribe**: In the pop-up interface, you can decide whether to apply the Schema to message publishing, subscription, or both. For this example, we’ll choose “Published“ to encode the message.
- **Select the Schema Script and Set the Proto Name**: In the dropdown, choose the proto file you created or imported. In the “Proto Name” input box, enter the message name you defined in the proto file, such as `IoT.SensorData`. Ensure all settings are correctly configured before confirming.

![Script](https://assets.emqx.com/images/32e7071465f68424462c63bfd22f7bf8.png)

#### 3. Publish a Message

After configuring the Protobuf Schema feature in the MQTTX client, you can verify by publishing a message.

- **Publish a Message**: In the message input box, input the desired JSON data, like:

  ```json
  {
    "deviceId": "Device001",
    "sensorType": "Temperature",
    "value": 23.5,
    "timestamp": 1677328490320
  }
  ```

- **View the Message**: In the message dialogue, you can see the published message marked with "Used SensorData.proto Schema," indicating that this message is encoded using the selected schema.

![View the Message](https://assets.emqx.com/images/0816e0bad8d4fd45e42e80a9e3209fb5.png)

With these settings, MQTTX is ready to use.

## Step 3: Set up Data Integration 

In Data Integration, the Rule Engine will process the Protobuf messages and republish them to a new topic to demonstrate the Schema Registry feature.

#### 1. Create a Message Republish

Go to the Data Integrations page and select “Republish” under the “Data Forward” category.

![Create a Message Republish](https://assets.emqx.com/images/3f1a10d1581d5fb796d1c568a85cf5c7.png)

In the SQL Editor, create a new rule to process messages from the topic. Initially, write a rule to receive messages without a schema. This rule will handle messages from the topic `t/#`.

```sql
SELECT
  payload as payload
FROM
  "t/#"
```

![SQL Editor](https://assets.emqx.com/images/4f094adaedff383a0e681c5f581d7664.png)

#### 2. Republish Setting

Click “Next” to add an action to output the messages by republishing the messages to a new MQTT topic.  

- **Topic**: The MQTT topic to forward to. In this tutorial, enter `schema/a`, all the messages will be sent to this topic.
- **QoS**: Message QoS, choose from `0`, `1`, `2`, or `${qos}`, or enter placeholders to set QoS from other fields. Here, choose `${qos}` to follow the QoS of the original message.
- **Retain**: Choose `true`, `false`, or `${flags.retain}`, to confirm whether to publish messages as retain messages. You can also enter placeholders to set retain message flags from other fields.
- **Message Template**: Template for generating the forwarded message payload. Leave blank by default to forward the rule output results. Here, enter `${.}` to forward all fields from the rule.

![New rule](https://assets.emqx.com/images/bf01dbe48ca5d5cbbebac7a19f0e9f66.png)

#### 3. Subscribe to the Messages in MQTTX

In MQTTX, set the subscription to the topic ‘schema/a’, then send a message encoded with Protobuf to the topic 't/a'. In the dialogue, you will receive a message with an unreadable payload.

![Subscribe](https://assets.emqx.com/images/39a6b8eb434bb81ad7e613ceca06de9f.png)

In the next step, we will configure the Schema Registry in Data Integration to verify if we can receive the decoded message.

## Step 4: Schema Registry Configuration in Data Integration

#### 1. Create a Protobuf Schema

On the Data Integration page, you will find the ‘Schema Registry' tab, then click 'New Schema Registry’.

![Protobuf Schema](https://assets.emqx.com/images/2727a358c0df9653315b91bb562b51bb.png)

- **Give the Schema a name**: set the name 'protobuf_test'
- **Choose a type**: Choose 'Protobuf' from the dropdown menu.
- **Schema**: 

```
syntax = "proto3";

message SensorData {
   string deviceId = 1;
   string sensorType = 2;
   double value = 3;
   int64 timestamp = 4;
}
```

![New Schema Registry](https://assets.emqx.com/images/948c50065175fd49c645c5cafcfa76bc.png)

#### 2. Include the Schema in the Rule

- On the Data Integration page, click and edit the rule we created in Step 3.

- Enter the following in the SQL editor:

  ```sql
  SELECT
    schema_decode('protobuf_sensor', payload, 'SensorData') as sensor_data, payload
  FROM
    "t/#"
  ```

- Save the rule.

  ![Save the rule](https://assets.emqx.com/images/7f6e1ddd4945018771b054661dd5b4ab.png)

#### 3. Check the Decoded Messages in MQTTX

In MQTTX, set the subscription to the topic ‘schema/a’, then send a message to the topic ‘t/a' again. In the dialogue, you will receive a message with the decoded field 'sensor_data’, which is readable compared to the original payload.

![Check the Decoded Messages in MQTTX](https://assets.emqx.com/images/785dfce319bffcfee84e367ab036c247.png)

The result verified the Protobuf Schema is successfully set in Data Integration.

## Schema Registry Wrap-Up

Schema Registry allows you to define and register schemas for your MQTT data formats. Once registered, these schemas can be shared and reused across various systems and applications. When a client sends data to a message broker, the schema for the data is included in the message header. The Schema Registry then ensures that the schema is valid and compatible with the expected schema for the topic. Using the Schema Registry in Data Integration, you can effortlessly build business-critical applications with secure data formats in EMQX Dedicated.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
