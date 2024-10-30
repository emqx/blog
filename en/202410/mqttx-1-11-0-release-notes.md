We’re thrilled to announce that MQTTX 1.11.0 is now available!

This release introduces Topic Tree visualization, a powerful new way to organize and monitor [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) hierarchically. We've also added support for Avro Schema and Message Pack formats in both Desktop and CLI clients, expanding MQTTX's data format handling capabilities. These updates provide users with enhanced tools for understanding their MQTT message flows and managing complex data structures.

> ***Download the latest version here:*** [***https://mqttx.app/downloads***](https://mqttx.app/downloads**)

## Topic Tree

Starting from v1.11.0, MQTTX Desktop introduces the **Viewer** feature, providing MQTT data visualization capabilities to help users better understand and monitor message flows.

The **Topic Tree**, currently in `Beta` version, is a powerful visualization tool that transforms MQTT topics and messages into an intuitive hierarchical structure. It displays your MQTT topic relationships and message flows in a tree-like format, making it easier to understand and manage your MQTT data.

Located in the **Viewer** menu, the **Topic Tree** automatically updates as your subscribed topics receive messages. The interface features a search box for quick topic filtering, operation buttons for tree manipulation, and a detailed information panel that provides message-specific data.

The Topic Tree organizes nodes into three levels:

- Root nodes show client connection details, including client ID and host information.
- Intermediate nodes represent topic hierarchies with their subtopics.
- Leaf nodes contain message details, including reception time, Retain flag, and QoS value.

![MQTT Topic Tree](https://assets.emqx.com/images/c6712e791d2df6025b60a1059d110986.png)

Users can switch to the visual tree diagram mode for a different perspective. This mode offers a more graphical representation of the topic structure, providing adjustable expansion levels (default is 4 layers) and interactive features. Users can hover over nodes to display topic paths, message counts, sub-topic counts, and message content.

![Visualize Topic Tree](https://assets.emqx.com/images/21f0b0ce3a37e7686c3f72f745cde078.png)

> Note: The Topic Tree feature is currently in Beta and may have incomplete functionality. We welcome your feedback and suggestions. If you encounter any issues or have ideas for improvement, please visit https://github.com/emqx/MQTTX/issues to share your thoughts.

## Avro Schema Support

> This feature is made possible thanks to a community contribution from [**@LAST7**](https://github.com/LAST7)

MQTTX 1.11.0 introduces Avro Schema support, expanding its message format testing capabilities. This enhancement enables developers to thoroughly test their MQTT applications that use Avro for data serialization, ensuring messages are correctly encoded and decoded in their communication flows.

Before publishing messages to your production environment, you can now validate that your JSON data is properly converted to Avro format and verify that subscribers can successfully decode Avro messages back to JSON. This testing capability helps identify potential serialization issues early in your development cycle, saving time and reducing debugging efforts in production.

### Desktop

The Desktop client provides an intuitive interface for Avro schema testing in the `Script` → `Schema` page. Here you can:

- Define your Avro schema using the standard `.avsc` format.
- Test JSON to Avro encoding before publishing.
- Validate Avro to JSON decoding for subscribed messages.
- Immediately see conversion results in the testing panel.

Example schema:

```json
{
  "type": "record",
  "name": "Person",
  "fields": [
    { "name": "id", "type": "int" },
    { "name": "name", "type": "string" }
  ]
}
```

![`Script` → `Schema` page](https://assets.emqx.com/images/aef3b5b57c6b2b509814289767d6928b.png)

### CLI

For automated testing scenarios or command-line operations, MQTTX CLI integrates Avro support through the `-Ap` or `--avsc-path` option:

| -Ap, --avsc-path <PATH> | the path to the .avsc file that defines the avro schema for AVRO encoding |
| :---------------------- | :----------------------------------------------------------- |
|                         |                                                              |

```
# Publish: Test your JSON to Avro encoding
mqttx pub -t 'msg/avro' -m '{"id": 1, "name": "hello"}' -Ap ./Person.avsc

# Subscribe: Verify Avro to JSON decoding
mqttx sub -t 'msg/avro' -Ap ./Person.avsc
```

This feature enhances MQTTX's capability for testing structured data communication. It's ideal for IoT device development and data pipeline construction, ensuring accurate Avro Schema message handling in MQTT applications.

## Message Pack Format Support

> This feature is made possible thanks to a community contribution from [**@lantica**](https://github.com/lantica)

MQTTX 1.11.0 now supports Message Pack, a highly efficient binary serialization format. This addition enables you to work with MQTT applications that demand more efficient data transmission while preserving structured data formats. By supporting Message Pack alongside JSON, Base64, and CBOR, MQTTX broadens its capacity to handle diverse MQTT messaging scenarios.

### Desktop

The Desktop client fully integrates Message Pack format into both publishing and subscribing interfaces:

- Publishing: Send MQTT messages in Message Pack format, automatically converting your JSON data into a compact binary format.
- Subscribing: Receive Message Pack formatted MQTT messages and view them as readable JSON, simplifying message inspection and comprehension.

![Message Pack](https://assets.emqx.com/images/e876bab4b35b1c0a9c1448801000ea07.png)

### CLI

The CLI supports Message Pack format through the `-f` or `--format` option:

```shell
# Send messages in Message Pack format
mqttx pub -t 'msg/msgpack' -m '{"value": 123}' -f msgpack

# Receive Message Pack formatted messages
mqttx sub -t 'msg/msgpack' -f msgpack
```

This enhancement boosts MQTTX's versatility as a testing tool, particularly for IoT scenarios where message size efficiency is crucial. Whether you're testing systems that already use Message Pack or exploring more efficient message formats for your MQTT communications, MQTTX now offers the capability to work with this compact binary format.

## WebSocket Headers Support in CLI

MQTTX 1.11.0 introduces custom WebSocket headers support for the CLI client—a feature highly requested by the community. This enhancement allows users to add custom headers when establishing WebSocket connections, which is particularly useful for scenarios requiring special authentication or custom data transmission.

Use the `-wh` or `--ws-header` option to specify custom WebSocket headers:

```shell
mqttx sub -t test -wh "Authorization: Bearer token123" -wh "Custom-Header: value" -l ws -p 8083
```

> Note: This feature is only available in the CLI client running in a Node.js environment. Due to browser security restrictions, the Desktop and Web versions cannot modify WebSocket headers—a known limitation in browser WebSocket implementations.

This feature addresses a common need in WebSocket MQTT connections, particularly in scenarios such as:

- Adding authentication tokens
- Including custom identification headers
- Setting up special connection parameters

This addition makes MQTTX CLI a more flexible tool for testing MQTT over WebSocket connections, especially in enterprise environments where custom headers are required for security or routing purposes.

## Configurable QoS 0 Message Storage

MQTTX 1.11.0 introduces an option to ignore QoS 0 messages, optimizing performance for high-volume message flows. QoS 0 messages—the most basic form of message delivery without guaranteed delivery—can now be configured to display without local storage.

In the Settings page under the Advanced section, you'll find the "Ignore QoS 0 Message" option, disabled by default. When enabled:

- QoS 0 messages are displayed but not stored locally.
- Storage overhead is reduced in high-frequency messaging scenarios.
- Previously saved QoS 0 messages remain intact.

This feature is especially useful when testing MQTT applications that generate large volumes of QoS 0 messages. It allows you to focus on messages requiring delivery guarantees while maintaining optimal performance and reducing storage space usage.

![Ignore QoS 0 messages](https://assets.emqx.com/images/9a65db1c7939f1049c1f104bbd26f745.png)

## Other Improvements

### Enhanced Client Configuration

- **Empty Client ID Support**: Introduced support for empty client IDs in MQTT 5.0, enabling brokers to automatically allocate client IDs. This enhancement allows for a more accurate simulation of MQTT 5.0 scenarios.
- **Default Session Expiry**: Adjusted the default session expiry interval to 7200 seconds (2 hours) for MQTT 5.0 connections with clean start set to false. This change aligns with EMQX's default configuration and optimizes server-side resource management.

### Improved MQTT Operations

- **Wildcard Topic Matching**: Resolved an issue where wildcard topic matching with '#' incorrectly matched unintended topics (e.g., 'foo/#' matching 'foobar/#').
- **Version Notation**: Updated MQTT version notation from '5' to '5.0' in CLI, enhancing clarity and consistency.

### AI Copilot Enhancements

- **Default Model Update**: Switched the default model to GPT-4o, delivering improved performance and capabilities.
- **New Model Support**: Expanded support to include additional GPT models, such as GPT-4o-mini and o1-preview.
- **DeepSeek Integration**: Incorporated DeepSeek model support for users in China, offering a cost-effective language model alternative.

### General Fixes

- Resolved connection name style issues.
- Improved benchmark subscription topics logging.
- Corrected some typos throughout the Desktop client.

## Roadmap

- **Topic Tree Milestone-2**: Enhance organization and visualization of topics.
- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View:** Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).
- **Support for Configurable Disconnect Properties (MQTT 5.0)**: Enhance connection management with customizable disconnection settings.
- **IoT Scenario Data Simulation**: Bring this feature to the desktop client to ease IoT scenario testing.
- **Sparkplug B Support**: Extend MQTTX functionalities to include support for Sparkplug B.
- **MQTT GUI Debug Functionality**: New features to aid in debugging MQTT communications.
- **Plugin Functionality**: Introduction of a plugin system supporting protocol extensions like [CoAP](https://www.emqx.com/en/blog/coap-protocol) and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **JSON Schema**: Encoding and decoding capabilities for JSON Schema.
- **Script Test Automation (Flow)**: Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://mqttx.app/downloads" class="button is-gradient">Get Started →</a>
</section>
