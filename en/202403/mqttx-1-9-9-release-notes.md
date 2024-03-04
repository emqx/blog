MQTTX 1.9.9 is now available with critical updates: improved connection events, CBOR data format support, customizable log levels for debugging, and enhanced UI flexibility. This release optimizes connection management, data handling, and user experience.

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads)

## Log Level

The latest MQTTX Desktop update introduces log-level customization, including debugging logging, for finer insight into connection statuses. Now accessible from settings or the log page's top-right corner, users can select from levels: DEBUG, INFO, WARN, ERROR. This means choosing DEBUG shows all logs, while ERROR displays only errors, streamlining troubleshooting.

MQTTX Desktop now allows users to customize log levels. The update includes debugging logs for more in-depth insights into connection statuses. Users can select from four levels: DEBUG, INFO, WARN, ERROR from settings or the log page. DEBUG shows all logs, while ERROR displays only errors, streamlining troubleshooting.

![Log Level 1](https://assets.emqx.com/images/ec47c00c6c974ceb5ed60f95f395a1d2.png)

![Log Level 2](https://assets.emqx.com/images/de5c2e47878a1615de037ebcd3fb45d1.png)

This update also improves MQTTX's diagnostic capabilities, making tracking and resolving issues easier.

![Log Level 3](https://assets.emqx.com/images/7a40f6f14b6b12472f60ed8deed224e5.png)

## Connection List Visibility

The latest version allows users to hide the connection list with a simple click, focusing on the current connection's details for a cleaner and more targeted debugging experience. With this adjustment, users can enjoy a neater interface that adapts efficiently to different screen sizes, thus improving the overall usability of the application. This caters to a seamless workflow, enabling users to minimize distractions and better manage screen real estate.

![Connection List Visibility 1](https://assets.emqx.com/images/c0b82f53276b49ad78816efc3d083a06.png)

![Connection List Visibility 2](https://assets.emqx.com/images/0314642b8e8c83fd8875e7c1ea50a617.png)

## CBOR Support

MQTTX now supports CBOR (Concise Binary Object Representation), an efficient data format that surpasses JSON in data optimization. This advancement enables devices to perform better, use less network bandwidth, and conserve battery life. Learn more about CBOR at [cbor.io](https://cbor.io/).

> The Concise Binary Object Representation (CBOR) is a data format whose design goals include the possibility of extremely small code size, fairly small message size, and extensibility without the need for version negotiation.

### Desktop

In MQTTX Desktop, users can now choose CBOR for data transmission:

- To send messages, choose CBOR format and input JSON data.
- When receiving messages, select CBOR format, which automatically decodes the data to JSON.

![CBOR Support](https://assets.emqx.com/images/c2838a6f6c338fd60fdd3c134fe8ed3b.png)

### CLI

With the `--format cbor` option, MQTTX CLI embraces CBOR:

- For subscribing to messages: 

  ```
  mqttx sub -h broker.emqx.io -t 'cbor' --format cbor
  ```

- For publishing messages:

  ```
  mqttx pub -h broker.emqx.io -t 'cbor' -m '{"msg": "hello"}' --format cbor
  ```

![MQTTX CLI CBOR](https://assets.emqx.com/images/97a3bb531c6d1012e1695a2e88ee029c.png)

This update was made possible thanks to the valuable contribution from [@Danfx](https://github.com/Danfx). His dedication and support have been instrumental in furthering MQTTX's capabilities.

## Bench Pub Messages Limit

The `bench pub` command now supports a `--limit` option to specify the number of messages to publish. Use `-L` or `--limit <NUMBER>` to set this, where `0` means unlimited (default is `0`).

For example, to publish 100 messages, you'd use:

```
mqttx bench pub -h broker.emqx.io -t 'testtopic' -m 'hello' -c 10 --limit 100
```

![Bench Pub Messages Limit](https://assets.emqx.com/images/9f21a2d1e7af948705b49e11f9665e4d.png)

This feature allows for controlled publishing, enabling users to limit the data volume for testing or resource management purposes.

## Expanded MQTTX Copilot

The MQTTX Copilot now supports more client code generation options for both software and hardware projects, including UI frameworks like Vue.js and React, hardware platforms such as ESP32, ESP8266, Arduino, Raspberry Pi, and mobile applications for Android, iOS, React Native, and Flutter. This broadens its use for a variety of development projects.

![Expanded MQTTX Copilot](https://assets.emqx.com/images/c2fb344ee8407ce42bf9229d627565bd.png)

## Others

In this release, we've also made several other enhancements and updates to improve your experience:

- **Connection Events**: We've enhanced support for disconnect and offline events across Desktop, Web, and CLI platforms. These improvements ensure better handling and robustness in connection management, including specific behaviors when disconnect packets are received from the broker or when the client goes offline.
- **Connection Issues Fix**: In the desktop version, we've fixed an issue to ensure the reconnect feature operates only within the current connection's page.
- **UI/UX Enhancements**: Desktop and web interfaces have received updates for a more cohesive and user-friendly experience. This includes clearer log messages and updated icons.
- **Documentation and Readme Updates**: We've simplified and updated the CLI readme and badges, making it easier for new users to get started and for existing users to understand the tool's capabilities more clearly.

## Roadmap

In the next development phase following MQTTX 1.9.9, we will focus on boosting visualization capabilities and introducing other key features and improvements.

- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Topic Tree View**: Enhance organization and visualization of topics.
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View:** Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related MQTT topics.
- **Support for Configurable Disconnect Properties (MQTT 5.0)**: Enhance connection management with customizable disconnection settings.
- **IoT Scenario Data Simulation**: Bring this feature to the desktop client to ease IoT scenario testing.
- **Sparkplug B Support**: Extend MQTTX functionalities to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization**: Configurable options to reduce storage space usage.
- **MQTT GUI Debug Functionality**: New features to aid in debugging MQTT communications.
- **Plugin Functionality**: Introduction of a plugin system supporting protocol extensions like CoAP and MQTT-SN.
- **Avro Message Format Support**: Encoding and decoding capabilities for Avro message format.
- **Script Test Automation (Flow)**: Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
