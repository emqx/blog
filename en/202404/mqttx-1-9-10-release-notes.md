MQTTX 1.9.10 is now available. This release features crucial Faker.js updates, better diagnostic insights for disconnections and subscription issues, and new CLI and UI enhancements. It aims to simplify user workflows and enhance troubleshooting.

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads)

## Faker.js Upgrade in CLI

MQTTX 1.9.10 introduces a crucial update: upgrading Faker.js to v8, bringing breaking changes. This impacts users with custom `simulate` scripts, requiring modifications for compatibility.

The update simplifies locale management but removes the ability to change locales on existing instances. For detailed adaptation instructions, refer to the [Faker.js Upgrade Guide](https://fakerjs.dev/guide/upgrading.html). This enhancement aims to improve simulation precision and efficiency within MQTTX.

For script upgrade guidance, see this PR example: [Adjustments for Faker.js v8](https://github.com/emqx/MQTTX/pull/1585). It showcases adjustments made to align with the new Faker.js version, serving as a valuable guide for your script modifications.

## Enhanced Simulate Command with Message Limit

The `simulate` command now supports a `--limit` parameter, mirroring the functionality found in the `bench` command. This enhancement allows users to set a precise number of messages to be published, offering greater control over simulation activities.

**Usage Example:**

Simulate to publish a total of 100 messages across 10 connections:

```shell
mqttx simulate -sc tesla -c 10 -h broker.emqx.io -t 'testtopic/simulate' -u 'admin' -P 'public' --limit 100
[4/10/2024] [11:13:42 AM] › ℹ  Start simulation publishing, scenario: tesla, connections: 10, req interval: 10ms, message interval: 1000ms
✔  success   [10/10] - Connected
[4/10/2024] [11:13:44 AM] › ℹ  Created 10 connections in 2.111s
[4/10/2024] [11:13:55 AM] › ℹ  Published total: 100, message rate: 0/s
```

**Parameter:**

- `-L, --limit <NUMBER>`: Sets the total number of messages to publish. Setting this to 0 allows for unlimited messages (default: 0).

## Diagnostic Insights for Connection & Subscription

MQTTX 1.9.10 enriches feedback mechanisms with MQTT 5.0's reason codes, detailing why connections are terminated or subscriptions fail. This feature aids in pinpointing issues, specifically highlighting scenarios like ACL rejections for subscriptions and server-initiated disconnections.

- **Subscription Failures**: Displays a "Not authorized" reason, clarifying access control restrictions.

  ![Subscription Failures](https://assets.emqx.com/images/fa75247eb5d66237be72d9d00f8f50b0.png)

- **Disconnections**: Indicates "Administrative action" reason, shedding light on server-side actions.

  ![Disconnections](https://assets.emqx.com/images/ba4bb89e5306d1a15059539f1395cce3.png)

This concise, actionable information, reserved for [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) users, streamlines troubleshooting and enhances operational transparency. For deeper insights into MQTT 5.0's reason codes, see [MQTT Reason Code Introduction and Quick Reference](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack).

## New Save Feature Enhances Connection Management

MQTTX 1.9.10 introduces a much-requested save button for new and edited connections, streamlining connection management. This feature, a direct response to community feedback, allows for temporary saving of connection details, providing flexibility for users to complete configurations at their convenience.

**How to Use:**

Simply select "Save Only" from the dropdown menu next to the top-right connection button when editing or creating a connection. This updates the information without connecting, facilitating easy later adjustments.

![Save Only](https://assets.emqx.com/images/97e04431f8e3fb32bd0664f7ef3fc7b5.png)

## Others

In this update, we've included several enhancements to improve the user experience:

- **Subscription Validation for Multiple Topics**: Fixed an issue with validation when subscribing to multiple topics, ensuring accurate subscriptions.
- **Record Encode/Decode Type**: MQTTX now remembers the selected encode/decode type, preventing reset upon restart or switching, which could lead to message garbling.
- **Enhanced** `sub` **Command Display**: Improved the display of information in the CLI for the `sub` command, including clearer representation of topics and QoS.

These adjustments are designed to streamline operations, enhance application usability, and increase stability.

## Roadmap

In the next development phase following MQTTX 1.9.10, we will focus on boosting visualization capabilities and introducing other key features and improvements.

- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Topic Tree View**: Enhance organization and visualization of topics.
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View:** Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics).
- **Support for Configurable Disconnect Properties (MQTT 5.0)**: Enhance connection management with customizable disconnection settings.
- **IoT Scenario Data Simulation**: Bring this feature to the desktop client to ease IoT scenario testing.
- **Sparkplug B Support**: Extend MQTTX functionalities to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization**: Configurable options to reduce storage space usage.
- **MQTT GUI Debug Functionality**: New features to aid in debugging MQTT communications.
- **Plugin Functionality**: Introduction of a plugin system supporting protocol extensions like [CoAP](https://www.emqx.com/en/blog/coap-protocol) and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **Avro Message Format Support**: Encoding and decoding capabilities for Avro message format.
- **Script Test Automation (Flow)**: Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://mqttx.app/downloads" class="button is-gradient">Get Started →</a>
</section>
