MQTTX 1.10.1 is now available!

This release focuses on enhancing the user experience with several key updates. The highlight is the one-click installation for MQTTX CLI via the Desktop application. Additionally, we've added support for custom AI Copilot API, built-in Moonshot LLM API support for Chinese users, and migrated the web client to a new address. These updates aim to make MQTTX more functional and user-friendly for everyone.

> *Download the latest version here:* [https://mqttx.app/downloads](https://mqttx.app/downloads)

## One-Click MQTTX CLI Installation

Starting from v1.10.1, the MQTTX desktop client supports one-click installation for the MQTTX CLI tool. Users can automate the setup process through a user-friendly graphical interface, avoiding manual downloads and configurations. This feature ensures that the latest version of the MQTTX CLI is easily accessible.

**Installation Steps:**

1. Navigate to the settings page, find the MQTTX CLI section, and click the install button.
2. Select the 'Install MQTTX CLI' option from the top menu.
3. The client will automatically download and install the required package for your system. You might need to enter a password to grant installation permissions.
4. After installation, the `mqttx` command will be ready from any terminal.

> **Note:** After clicking install, Windows users need to manually download the MQTTX CLI executable file and use it in the corresponding directory.

![One-Click MQTTX CLI Installation 1](https://assets.emqx.com/images/b003645e647f1d5460e65071ee8cb2bc.png)

![One-Click MQTTX CLI Installation 2](https://assets.emqx.com/images/f66d1b109f8ca613b9ce905b92701130.png)

![MQTTX CLI](https://assets.emqx.com/images/edf91b1652ec6b21c847e17ea8bb2caf.png)

## Support for Custom AI Copilot API

In previous versions, MQTTX Copilot was limited to using the built-in OpenAI API. 

Starting from v1.10.1, we have updated this strategy to allow users to customize the AI service API endpoint and models. As long as the API follows the OpenAI format, MQTTX Copilot can support various generative AI LLMs. This flexibility enables users to input their API key, host API, and supported models, integrating various AI services and providing enhanced, personalized AI capabilities within MQTTX. Users can easily switch between AI providers and models, tailoring the Copilot to their needs and preferences.

![Support for Custom AI Copilot API](https://assets.emqx.com/images/9d92f405ec524c750ae56888a26894ea.png)

This feature is made possible thanks to a community contribution from [@ni00](https://github.com/ni00).

## Migration of MQTTX Web Address

We have once again migrated the MQTTX Web online address to [https://mqttx.app/web-client](https://mqttx.app/web-client) to enhance security and compliance. 

**Impact:**

- WebSocket connections must now use Secure WebSocket (wss://) instead of ws://.
- Users need to update their WebSocket connection configurations.

**Solution:**

- Download the MQTTX Desktop or CLI version.
- Consider private deployment of the web client.

For detailed information, please refer to our [migration announcement](https://www.emqx.com/en/blog/mqttx-web-migration-announcement#why-migrate).

Additionally, we have added a data collection policy. If you have any concerns about data collection, please view the details on the About page.

![data collection policy](https://assets.emqx.com/images/e95a222e79d0a415200221845136920e.png)

## Specify the Default Protocol in Config Files

MQTTX now allows users to set default protocols in the configuration files. Users can choose protocols like WebSocket (ws, wss) or MQTT over SSL (mqtts) as defaults, eliminating the need to specify them for each connection.

To configure, use the `mqttx init` command and select your preferred default protocol.

This feature is made possible thanks to a community contribution from [@rpendleton](https://github.com/rpendleton).

![Specify the Default Protocol in Config Files 1](https://assets.emqx.com/images/b382f8b3e7c30c33f28bad8670e894b9.png)
![Specify the Default Protocol in Config Files 2](https://assets.emqx.com/images/cb90e68abd49dd909e33ca1a174626e1.png)

## Others

**New Features and Improvements**

- **Improved Desktop Backup Import Progress**: Supports importing large backup files and displays a progress bar.
- **Show Load Data Errors on Desktop**: The Desktop application now clearly displays any errors encountered during data loading, helping users quickly identify and resolve issues.
- **Support Rebuilding Database on Load Connection Error**: Provides an option to rebuild the database when a loading connection error occurs.
- **Highlight Subscription Info on Sub Output in CLI**: The CLI has been enhanced to highlight subscription information in the output, making it easier to manage and track subscriptions.

**Bug Fixes**

- **Fix Issue with Resubscribing on Desktop**: Resolved an issue that caused problems with resubscribing, improving the reliability of the Desktop application.
- **Correct Data Conversion for Publishing Messages with Format in CLI**: Fixed a bug in the CLI that caused incorrect data conversion when publishing messages with specific formats.

These updates focus on improving user experience, enhancing functionality, and fixing critical bugs to ensure a smoother and more reliable operation of MQTTX.

## Roadmap

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
