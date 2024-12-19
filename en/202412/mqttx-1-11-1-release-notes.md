We are pleased to announce the official release of MQTTX version 1.11.1. This release enhances MQTTX's visualization capabilities with improved Topic Tree features and real-time traffic monitoring. The new traffic rate monitoring feature provides users with real-time packet tracking, and the Topic Tree now supports manual synchronization with connection lists and MQTT properties display. Additionally, we've resolved critical message rendering issues in the Desktop client to ensure a more stable experience.

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads)

## Synchronize Connection Data to Topic Tree

MQTTX now provides bi-directional synchronization between the Topic Tree and connection message list. While new messages are automatically reflected in the Topic Tree, users can manually synchronize historical messages from connections. This can be done in two ways:

![Topic Tree](https://assets.emqx.com/images/fb08422338b9aacfa27f900153a4572c.png)

**From Connection Page**

- Access the dropdown menu in the upper right corner and select "Sync Topic Tree".

- Once confirmed, historical messages from the current connection will be automatically converted into the Topic Tree structure.

  ![image 1](https://assets.emqx.com/images/d29b5b54f25b6b450f43497a2c700f6a.png)

**From Topic Tree View**

- Click "Sync Connection Data" in the upper right corner dropdown menu.

- Select the connection to synchronize.

- The Topic Tree will update to display the synchronized data.

  ![image 2](https://assets.emqx.com/images/fa7dfec0ad8ee8db0e1e7cce8115518f.png)

## Traffic Monitor in Viewer

We've enhanced MQTT traffic monitoring by relocating the bytes statistics function to the Viewer menu as "Traffic Monitor" while adding new rate monitoring capabilities. This feature automatically calculates total traffic volume and rates based on historical messages in connection records, providing deeper insights into your MQTT traffic patterns.

**Quick Access**

- Click the traffic monitor icon in the connection page's upper right corner.
- Navigate through `Viewer` -> `Traffic Monitor` in the left menu bar.

When accessing from the connection page, MQTTX automatically subscribes to the `$SYS/#` system topic. A manual subscription is required for direct menu access.

**Key Features**

- Automatic rate calculation from connection message history.
- Connection selector for monitoring multiple connections.
- Flexible time range selection.
- Comprehensive statistics, including both accumulated values and real-time rates.

**Statistics Display**

- **Accumulated Values**: View total bytes with trend visualization.

  ![Accumulated Values](https://assets.emqx.com/images/4d12ca750d7b45362fcf2ad2ed15e7d0.png)

- **Rate Statistics**: Monitor current send/receive rates with time-based averages and real-time packet synchronization.

  ![Rate Statistics](https://assets.emqx.com/images/dbc6eb6919ad7d5b77fb26d935080eb1.png)

> Note: EMQX by default restricts $SYS topic subscription to localhost clients only. For remote access, ACL rule modifications are required. Please refer to [EMQX documentation](https://docs.emqx.com/en/emqx/latest/access-control/authz/authz.html) for configuration details.

## Connection Selection in Collapsed Mode

We've added a connection selector dropdown in the main view when the left sidebar is collapsed. This enhancement allows users to quickly switch between connections without expanding the connection list, improving workspace efficiency by maintaining easy connection access while maximizing the message viewing area.

![MQTTX](https://assets.emqx.com/images/53a643fc60c5b6a65b86c332f6e2e811.png)

## CLI Line Mode Enhancement

We've streamlined the CLI's multi-line message publishing by introducing `--line-mode` (`-lm`), which simplifies the previously confusing combination of `--stdin` (`-s`) and `--message-by-message` (`-M`) options. While maintaining all existing functionality, this update makes the CLI more intuitive.

**Improvements**

- The new `-line-mode` option replaces the need to combine `s` and `M`.
- Enhanced pipeline support for better integration with Unix-like systems.
- Optimized logging display for multi-line data.
- Fixed display issues when reading files with `s` and `M` options.

**Usage Example**

```shell
# New simplified way
mqttx pub -t "hello" -lm
hello     # Sends immediately
world     # Each line as separate message
<Ctrl+C>  # End input

# Previous method (still supported)
mqttx pub -t 'hello' -s -M
```

You can also leverage the previous `--stdin (-s)` and `--multiline (-M)` options to enable more versatile data input methods:

```shell
# Single message from echo
echo "hello world" | mqttx pub -t "test" -s

# File content as one message
cat message.txt | mqttx pub -t "test" -s

# File content as separate messages (line by line)
cat message.txt | mqttx pub -t "test" -s -M
# Results in:
# Message1: line1
# Message2: line2
# Message3: line3
```

> Note: For users familiar with -s and -M, these options remain fully functional with improved pipeline support. The new --line-mode option simplifies these operations into a single command.

## **Other Improvements**

### Critical Fixes

- Resolved a significant issue where messages were not properly rendered in the display interface, ensuring reliable message visualization and preventing data loss in the UI.

### Desktop Improvements

- Enhanced Topic Tree functionality with MQTT properties display, providing users with comprehensive message context and metadata visualization.
- Implemented rate limiting for the message send button to prevent accidental message flooding and ensure system stability.
- Enhanced visual elements with:
  - Optimized scrollbar style in Topic Tree
  - Improved tooltip display timing
  - Fixed tooltip overflow in tree visualization
  - Resolved unread message count initialization issues

### CLI Enhancements

- Improved benchmark and simulation capabilities with custom client ID support, ensuring unique identifiers for each connection, even in single-connection scenarios.
- Enhanced user experience with clear exit tips for connections, making session management more intuitive.
- Fixed several key issues:
  - Configuration override conflicts that affected command behavior.
  - Binary file type reception problems.
  - Pipeline-related issues affecting multi-line message publishing.

## Roadmap

- **MQTTX 2.0 Refactor** is in progress.
- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View**: Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related MQTT topics.
- **AMQP Support**: Extending protocol support to include AMQP.
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
