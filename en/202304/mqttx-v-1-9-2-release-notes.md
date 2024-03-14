At the end of April 2023, the MQTTX team released a brand new version, 1.9.2, which supports the output mode of the command-line tool, allowing users to customize data pipelines according to their needs and thus more conveniently and efficiently process output data. This update also introduces importing and exporting YAML format data to the desktop client, further enhancing the flexibility and richness of data processing. At the same time, we continue to optimize the user experience of the desktop client, providing developers of MQTT services and applications with the best toolbox in the world!

## Download

<section class="promotion">
    <div>
        Download The Latest MQTTX Now!
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Download →</a>
</section>

## MQTTX CLI Enhancements

In earlier versions of the MQTTX CLI, the command-line client's output was inflexible and had a fixed structure, which restricted users from utilizing output data directly in specific scenarios. To resolve this problem, the MQTTX v1.9.2 emphasizes bolstering the output mode support for the command-line client's `sub` command. It allows users to easily tailor data pipelines according to their requirements and handle diverse output demands.
The new clean mode allows users to output complete data packets, making it easier to manage output data with tools such as `jq`. For example, users can subscribe to a topic and output data in clean mode using the following command:

```
mqttx sub -t topic --output-mode clean | jq '.payload'
```

In the clean output mode, we can obtain a complete MQTT client-receivable data packet, and then filter the data using the `jq` tool to output simple payload content:

```
"Hello from MQTTX CLI"
```

Users can also reorganize the received data using more complex filtering conditions.

```
mqttx sub -t topic --output-mode clean | jq '{topic, payload, retain: .packet.retain, userProperties: .packet.properties.userProperties}'
```

Now, we can obtain a data structure customized to our needs:

```
{
  "topic": "topic",
  "payload": "Hello From MQTTX CLI",
  "retain": true,
  "userProperties": {
    "name": "mqttx"
  }
}
```

By strengthening the output mode, users can easily customize data pipelines to write more convenient and efficient test scripts, thereby expediting the development and data integration of various MQTT services and applications. 

![MQTTX CLI](https://assets.emqx.com/images/9f3f4a1a27abd60f7b8d180ee74fdd6e.png)

## Desktop Client Enhancements

We continue to focus on improving the user experience of our desktop client in version 1.9.2 with several key optimizations, including:

1. Support for YAML format data: The desktop client now supports importing and exporting data in YAML format, further enhancing the flexibility and richness of data processing.
2. Added loading animation for exporting data: To improve user experience, we added a loading animation for the data export process, allowing users to have a clearer understanding of the current progress while waiting for data export.
3. Optimized the update of links on the About MQTT page: To enable users to find the desired help content more accurately, we updated the links on the About MQTT page so that users can conveniently access detailed information and usage guides on MQTT.
4. Fixed compatibility issues with user property data: We resolved issues related to the inability to delete user properties and the need to click twice to update property configurations, thereby improving stability and compatibility when configuring properties.
5. Fixed compatibility issues with username and password for MQTT 3.1.1 and 5.0 versions: We fixed the issue where the default username was not passed when an anonymous connection was made and added support for validating the need to fill in the username when using passwords in MQTT 3.1.1 connections, enhancing compatibility across different MQTT versions.
6. Fixed the order of selected connections: We ensured that when leaving a page and returning to the previously selected connection, users can quickly return to the last operated connection after switching between different pages, improving work efficiency.
7. Added default values for [subscription options](https://www.emqx.com/en/blog/an-introduction-to-subscription-options-in-mqtt) when using MQTT 5.0 connections, simplifying MQTT 5.0 subscription operations and enhancing user experience.
8. Optimized the display title of the history topic: We fixed the display issue of topic messages in the selection box when the message was too long.
9. Fixed the display issue of message line breaks, improving message readability.
10. Optimized the translation of various prompt messages, improving the accuracy of multilingual support.
11. Upgraded dependencies to improve security and stability continuously.

![MQTT Client - MQTTX](https://assets.emqx.com/images/45c8239d2de33ef4ea195672086ebf3b.png)

## Future Plans

MQTTX is still continuously improving and enhancing, aiming to bring more practical and powerful features to users and provide convenience for IoT application and service testing and development. Next, we will focus on the following aspects, stay tuned:

- Support for Protobuf message format
- Support for SparkplugB
- IoT scenario data simulation (IoT Data Simulator)
- Switching options for QoS 0 message storage 
- MQTT Debug function
- Automatic chart drawing of received messages
- Plugin function (protocol extension CoAP, [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx), etc.)
- Script testing automation (Flow)


<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Download Now →</a>
</section>
