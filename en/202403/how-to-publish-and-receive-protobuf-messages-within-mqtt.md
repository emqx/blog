## MQTT and Protobuf

Choosing the correct data serialization format becomes crucial in the increasingly complex data exchange environment. Protobuf has been widely adopted by major internet companies and various microservice projects due to its efficient serialization properties. At the same time, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), a lightweight message transfer protocol based on the publish-subscribe model, evidently enhances the IoT data exchange experience when combined with Protobuf.

Ensuring and testing the correct publishing and receiving of Protobuf messages within MQTT is crucial. [MQTTX](https://mqttx.app/), an open-source, all-in-one [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools), supports multiple formats, from JSON and Base64 to the present-day Protobuf. This article will demonstrate how to define, publish, and receive Protobuf messages with MQTTX.

## Preparation

This tutorial requires some preliminary work to ensure smooth communication with IoT devices. This includes installing an [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and the MQTTX client. An MQTT Broker(we’ll use EMQX here) provides message transmission functionality for IoT devices, while MQTTX allows us to publish and subscribe to messages.

### Install EMQX

EMQX is a high-performance, scalable [MQTT platform](https://www.emqx.com/en/blog/mqtt-platform-essential-features-and-use-cases) suitable for IoT, Industrial IoT, and Vehicular network scenarios. We have chosen the 5.5.1 version of [EMQX Enterprise](https://www.emqx.com/en/products/emqx) edition as its rule engine is capable of encoding and decoding with Protobuf, making it convenient for processing and validating Protobuf data.

- Installation using Docker:

  ```
  docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.5.1
  ```

- For non-Docker users, EMQX offers RPM or DEB packages. The EMQX 5.5.1 Installation Guide provides detailed installation instructions.

### Install MQTTX

MQTTX provides desktop and CLI versions that support Protobuf message transmission. Visit the [MQTTX official website](https://mqttx.app/downloads) to download the appropriate version based on your requirements.

## Use Protobuf Messages with MQTTX Desktop

The MQTTX desktop client offers users a more efficient and personalized experience. We’ve optimized the Schema section in the latest version, especially with the newly added custom functions and Schema scripting capabilities. These enhancements make handling and viewing data in the Protobuf format much more accessible.

1. **Access the Schema Script Page**

   Start the MQTTX client, click the “Scripts” icon in the left menu bar, then select the “Schema” tab. Upon entering this page, there’s a simple default example.

   ![Schema Script Page](https://assets.emqx.com/images/627d34f90a2d1dbdc72f3d5226bcb0ee.png)

   > **Note:** This example serves only as a placeholder. You have to save it before use.

2. **Input or Import a .proto File**

   You can type the content of a proto file in the editor, as shown in the example below. Then click the “Save” button in the top-right corner. This way, you’ve successfully created a new proto Schema in MQTTX. If you already have a prepared .proto file, you can directly click the “Import .proto File” button in the top right to upload it.

   Here’s a commonly used proto format in the IoT:

   ```protobuf
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

   ![Input or Import a .proto File](https://assets.emqx.com/images/28da9a83a48cb8b340ddafebf2b2fc79.png)

3. **Test Input and Output**

   At the bottom of the script editor, you can try entering data to verify whether the proto file you just wrote is correct. First, you can choose a data format, such as JSON, to test with.

   **Example**: Based on the `SensorData` definition, you can input the following JSON data alongside the Proto name for testing:

   ```json
   {
     "deviceId": "123456789",
     "sensorType": "Temperature",
     "value": 24.5,
     "timestamp": 1678339200000
   }
   ```

   Once done, click the “Test” button. If there’s any mismatch between the input data and the proto file definition, the MQTTX client will show relevant error messages or prompts to assist in troubleshooting.

   ![Test Input and Output](https://assets.emqx.com/images/ee171826b8602aeec287f6c3dc125261.png)

4. **Run the Script**

   Once connected to EMQX, you can use the proto file you defined earlier for message encoding and decoding.

   - **Select Run Script**: Click the dropdown in the connection page’s top right corner and choose “Run Script”.

     ![Select Run Script](https://assets.emqx.com/images/4f39d3ab1cbd6d0051b6c8a7f335a32d.png) 

   - **Apply to Publish or Subscribe**: In the pop-up interface, you can decide whether to apply the Schema to message publishing, subscription, or both. For this example, we’ll choose the default “All.”

   - **Select the Schema Script and Set the Proto Name**: In the dropdown, choose the proto file you created or imported. In the “Proto Name” input box, enter the message name you defined in the proto file, such as `IoT.SensorData`. Ensure all settings are correctly configured before confirming.

     ![**Select the Schema Script and Set the Proto Name**:](https://assets.emqx.com/images/6ba83b3845e9693e8b87c633e6ca9481.png)

   **Note:** This tutorial will only focus on using the Schema scripts. While MQTTX does support custom functions, we will not cover that functionality here.

5. **Publish and Receive Messages**

   After configuring the Protobuf Schema feature in the MQTTX client, you can verify its effectiveness by publishing and receiving messages.

   - **Publish a Message**: In the message input box, input the desired JSON data, like:

     ```json
     {
       "deviceId": "Device001",
       "sensorType": "Temperature",
       "value": 23.5,
       "timestamp": 1677328490320
     }
     ```

     Next, subscribe to a topic named `testtopic/protobuf` and publish the above message to that topic.

   - **Receive and View the Message**: Ensure you subscribe to the mentioned topic. You can see the Protobuf message in the reception window when the message arrives. Selecting the JSON format will convert the Protobuf message into JSON for easier viewing.

     ![Receive and View the Message](https://assets.emqx.com/images/d4c9024c9534af0024ff1a59763ac416.png)

   - **Verify Message Processing**: At the top of each message, there’s a tag indicating whether the message underwent Schema. Ensure it means “Used with xx Schema”. If errors arise or the message format doesn’t match the expected proto format, the MQTTX client will provide relevant error prompts.

After completing the above steps, you’ve successfully enabled the Protobuf Schema feature in the MQTTX client. This feature ensures that messages sent or received via MQTT are correctly serialized or deserialized according to the Protobuf format. To turn off this feature, click the “Stop Script” button at the top.

## Use Protobuf Messages with MQTTX CLI

The MQTTX CLI version offers comprehensive support. It utilizes Protobuf for message encoding and decoding within the MQTTX graphical desktop client, providing a more direct and efficient way for those familiar with console operations to operate.

**Introduction to CLI Parameters for Protobuf**

When using the MQTTX CLI client to handle messages in the Protobuf format, you need to be aware of the following essential parameters:

| Parameter | Description                                                  |
| :-------- | :----------------------------------------------------------- |
| Pp        | Specifies the path to the .proto file for the Protobuf message format. |
| Pmn       | Defines the proto name of the Protobuf message. This name must match the definition in your .proto file. |

1. **Prepare the** `.proto` file.

   First, ensure a well-defined `.proto` file describing the Protobuf message format you wish to transmit.

   ```protobuf
   syntax = "proto3";
   
   package IoT;
   
   message SensorData {
   	string deviceId = 1;
   	string sensorType = 2;
   	double value = 3;
   	int64 timestamp = 4;
   }
   ```

2. **Subscribe to Messages Using Commands**

   To receive messages in the Protobuf format, you can subscribe to a specific MQTT topic:

   ```shell
   mqttx sub -t 'testtopic/protobuf' -h 127.0.0.1 -Pp ./SensorData.proto -Pmn IoT.SensorData
   ```

3. **Publish Messages Using Commands**

   Based on the parameters introduced earlier, we can now publish a message in the Protobuf format:

   ```shell
   mqttx pub -t 'testtopic/protobuf' -Pp ./SensorData.proto -Pmn IoT.SensorData -h 127.0.0.1 -m '{"deviceId":"123456", "sensorType": "Temperature", "value": 22.5, "timestamp": 1675873900}'
   ```

4. **View the Received Protobuf Messages**

   After a successful subscription, you will observe the Protobuf-formatted messages received in the command line from the `testtopic/protobuf` topic. This message will be decoded according to the definition in your `.proto` file and displayed in the command line.

   ![View the Received Protobuf Messages](https://assets.emqx.com/images/704c6168020d0faf05ae386ebecdfd01.png)

   If you wish to view the message in JSON format, you can use the `--format` parameter and set it to `JSON`. This will convert the Protobuf message into a more readable JSON format.

## Validate Protobuf Messages Using EMQX

Lastly, to ensure the correctness of your messages, it’s recommended to use the encoding and decoding functionality of EMQX 5.5.1 Enterprise Edition for validation. Through decoding and encoding, the correctness of the messages is verified.

### Decoding

Devices publish messages encoded with Protobuf to the MQTT Broker. The EMQX rule engine captures and decodes this message based on the defined Protobuf Schema and then republishes it to a specified topic.

1. **Create Protobuf Schema**:

   - In the EMQX Dashboard left navigation pane, choose `Integration -> Schema`.

   - Use the following parameters to create a Protobuf Schema:

     - Name: `protobuf_sensor`

     - Type: `protobuf`

     - Schema:

       ```protobuf
       syntax = "proto3";
       package IoT;
       message SensorData {
          string deviceId = 1;
          string sensorType = 2;
          double value = 3;
          int64 timestamp = 4;
       }
       ```

   - Click `Create`.

2. **Set Up Decoding Rule**:

   - Choose `Integration -> Rules` in the left navigation bar.

   - Enter the following in the SQL editor:

     ```sql
     SELECT
       schema_decode('protobuf_sensor', payload, 'SensorData') as sensor_data, payload
     FROM
       "t/#"
     WHERE
       sensor_data.deviceId = 'Device123'
     ```

   - Select `Republish` from the action dropdown menu.

   - Set the target topic as `sensor_data/${sensor_data.deviceId}`.

   - Use `${sensor_data}` as the Payload message template.

     ![Rules Engine](https://assets.emqx.com/images/ccea83c52a1dfa37b08c1dc627bcbe4a.png)

3. **Use MQTTX**:

   - Use MQTTX as the MQTT client to connect to EMQX.

   - Subscribe to the topic `sensor_data/#` in the subscription area

   - Set the Schema script on the publishing side and send a Protobuf encoded `SensorData` message to the `t/1` topic.

   - In the received MQTTX, you should see the decoded message with the topic `sensor_data/Device123`.

     ![MQTTX](https://assets.emqx.com/images/37b9aa3c001ce26b1f69dca42480c064.png)

### Encoding

Devices publish messages in JSON format to the MQTT Broker. The EMQX rule engine encodes it into Protobuf format based on the defined Protobuf Schema and republishes it to another topic.

1. **Use the previously created Schema**.

2. **Set up Encoding Rule**:

   - Choose `Integration -> Rules` in the left navigation bar.

   - Enter the following in the SQL editor:

     ```sql
     SELECT
       schema_encode('protobuf_sensor', json_decode(payload), 'SensorData') as protobuf_sensor
     FROM
       "t/#"
     ```

   - Choose `Republish Message` from the action dropdown menu.

   - Set the target topic as `protobuf_out`.

   - Use `${protobuf_sensor}` as the Payload message template.

     ![Create rule](https://assets.emqx.com/images/cee9344ef1f07996e0f2aae15a48ad90.png)

3. **Using MQTTX to Receive Protobuf Messages**:

   - Connect to EMQX using MQTTX.

   - In the publishing area, input the topic `t/1` and a specific JSON Payload, e.g.

     ```json
     {
       "deviceId": "Device123",
       "sensorType": "Temperature",
       "value": 24.5,
       "timestamp": 1678339200000
     }
     ```

   - Click Publish.

   - Set the Schema script on the receiving end and subscribe to the `protobuf_out` topic.

   - In MQTTX, you should see the encoded Protobuf message.

     ![MQTTX](https://assets.emqx.com/images/775345cea4d97f4b80d7a8b2253d2832.png)

## Conclusion

With the rapid development of the IoT industry, efficient and compact data transmission has become increasingly important. Protobuf, as an efficient data serialization format, can be used in conjunction with MQTT to ensure fast, accurate, and secure data exchange.

Especially in the industrial IoT domain, SparkplugB, a popular data transmission standard, adopts a message format centered around Protobuf. As such, MQTTX can effortlessly support SparkplugB message interactions through Protobuf. To further enhance performance in industrial applications, MQTTX plans to optimize support for SparkplugB in the future.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
