We are excited to announce the official release of MQTTX 1.9.4, a powerful MQTT 5.0 client tool. This update brings significant improvements to user experience, including more efficient support for Protobuf message transmission, optimized automatic update functionality, and a range of feature enhancements. 

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads) 

## Testing Message Transmission with Protobuf Format

To meet the testing requirements for large-scale and high-frequency data exchanges, we have incorporated support for Protobuf in MQTTX. This new feature significantly enhances message transmission efficiency, and also further expands MQTTX's testing capabilities.

### Using the Command-Line Client 

In the command-line client, you can directly use the following commands for Protobuf-format message transmission:

```
# Subscription
mqttx sub -t 'testtopic/#' -h broker.emqx.io -Pp ./TestPerson.proto -Pmn Person

# Publish
mqttx pub -t 'testtopic/protobuf' -Pp ./TestPerson.proto -Pmn Person -h broker.emqx.io -m '{"id":0, "name": "test"}'
```

The `-Pp` parameter defines the path to the .proto file for the Protobuf message format, and the `-Pmn` parameter specifies the name of the Protobuf message type (which must exist in the .proto file).

> **Note**: When publishing or subscribing, you need to create a .proto file in any directory and specify the path to the .proto file and the name of the message type during connection.

### Using the Desktop Client

In the desktop client, we have optimized the script section and introduced custom functions and Schema encoding and decoding. In custom functions, the previous scripting capabilities are retained. And you can use custom proto files for Protobuf-format data encoding and decoding. Here's how to operate:

1. Navigate to the script page and select Schema.
2. Create a new proto file or import an existing one.
3. On the connection page, select Run Script, choose the schema you created, and enter a Proto Name, which is the name of the message type.
4. The sent and received messages will be displayed.

Please note that both custom functions and schema encoding/decoding can be used in scripts. The default order of usage is as follows: when sending data, the payload is first processed using custom functions, followed by encoding using the encoding/decoding script; when receiving data, the data is first decoded and then processed using custom functions.

![MQTT Script](https://assets.emqx.com/images/01fbf004ccd70d255d99c62eabe4c871.png)

<center>Scripts</center>

## Optimized Automatic Updates in the Desktop Client

The improved automatic update feature in version 1.9.4 allows users to preview new features. It displays a progress bar during the update process, providing a clearer understanding of the updated content and download progress.

![Update Available](https://assets.emqx.com/images/dd3f581b80fdfafa43dafc63f02e1464.png)

<center>Update Available</center>

<br>

![Download Progress](https://assets.emqx.com/images/1f5f29fe8d12623915c7a52679655a7d.png)

<center>Download Progress</center>

## Enhanced Functionality in the Command-Line Client

We have enhanced the following functionality of the command-line client in version 1.9.4:

### Support for MQTT over WebSocket Connections 

The command-line client now supports MQTT over WebSocket connections, enabling more flexible testing scenarios. You can establish a WebSocket-based connection using the following command:

```
mqttx conn -h broker.emqx.io -p 8083 -l ws
```

Here, the `-l` parameter indicates the connection protocol, with available values including MQTT, MQTTs, Websocket, and WSS. The default value is MQTT.

### Support for Sending Messages in Multiple Formats 

We have added support for specifying the data format when publishing messages. Currently, the CLI supports encoding formats such as Hex, JSON, and Base64. For example, you can send a message in Hex format using the following command:

```
mqttx pub -t testtopic/protobuf -h broker.emqx.io -m '7b0a 2020 2274 656d 7022 3a20 3331 2e35 2c0a 2020 2268 756d 223a 2032 300a 7d' --format hex
```

Here, the `--format` parameter is used to specify the message format, with available values including base64, JSON, and hex.

## Website Upgrade 

This upgrade includes comprehensive optimizations to the official website of [MQTTX.app](https://mqttx.app/), providing a more intuitive display of MQTTX's features and use cases.

![MQTT Client](https://assets.emqx.com/images/ee05da05ecf66c263fae0df84d918a6b.png)

<center>Overview</center>

## Other Enhancements and Bug Fixes 

In addition to the exciting new features, MQTTX 1.9.4 includes various enhancements and bug fixes to ensure a smoother user experience. Here are some of the notable improvements:

- Modifications and optimizations to the scripting functionality;
- Changed the original scripting functionality to custom functions;
- Support for importing local JavaScript files in custom functions;
- Display of which script has been applied to prompt messages;
- Fixed conflicts between the web version's right-click menu and browser default events;
- Fixed connection count statistics error in the bench command to reflect the current connection status accurately;
- Updated the logo of MQTTX Web;
- Fixed the issue of retaining the last selected connection after restarting the client;
- CLI improvements in parameter checking and error handling;
- Fixed version comparison issue during updates;
- Improved user interface by optimizing the display width of message boxes.

## Future Plans 

We have an exciting roadmap ahead as we continue to innovate and improve MQTTX. Here are some of our plans:

- Synchronizing IoT scenario data simulation functionality with the desktop client;
- Enhancing the highlighting of particular data formats (such as JSON) in the message box;
- Support for Avro message format in schema encoding/decoding;
- Support for Sparkplug B;
- Configurable storage ignoring of QoS 0 messages to reduce storage space usage;
- MQTT Debug functionality;
- Automatic chart plotting of received messages;
- Plugin functionality (protocol extensions for CoAP, MQTT-SN, etc.);
- Script testing automation (Flow).


<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
