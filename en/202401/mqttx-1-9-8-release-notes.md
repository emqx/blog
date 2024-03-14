MQTTX 1.9.8 is now available, introducing a new CLI Debug Mode. This feature greatly enhances developers' troubleshooting and analysis capabilities. Additionally, the update improves the MQTTX Copilot feature, providing users with advanced AI-driven MQTT interaction support.

> *Download the latest version here:* [https://mqttx.app/downloads](https://mqttx.app/downloads)

## MQTTX CLI - Debug Mode

The Debug Mode in MQTTX 1.9.8, powered by MQTT.js, streamlines MQTT debugging. Activated with the `--debug` switch, it provides real-time logs during connection, publishing, and subscribing, detailing client configurations and packet handling. This feature is invaluable for developers to understand and troubleshoot MQTT protocols effectively.

Consider the command `mqttx conn -h broker.emqx.io -p 1883 --debug` as an example of the new Debug Mode. This command initiates a detailed MQTT debug process, revealing logs like:

- Connection initiation to MQTT broker.
- Client settings include protocol version, keepalive, and client ID.
- Stream setup and handling for MQTT communication.
- Packet sending processes like `connect` and `pingreq`.
- Real-time monitoring of MQTT interactions, including packet handling and response checks.

These details aid in understanding the MQTT communication lifecycle, from establishing connections to maintaining them, which is crucial for troubleshooting and advanced MQTT usage.

![MQTT communication lifecycle](https://assets.emqx.com/images/c810a2e4e6a7442e6b51b5d72b14dbae.png)

## MQTTX Copilot Enhancement

MQTTX 1.9.8 introduces substantial improvements to the MQTTX Copilot feature:

- **Stream Response Support**: Enhance the response speed and user experience, making interactions with Copilot more fluid and immediate.

- **One-Click Functionalities**:

  - **EMQX Log Analysis**: Users can now analyze EMQX logs with a single click, simplifying the log review process.

    ![EMQX Log Analysis](https://assets.emqx.com/images/2543f9d9b788f131140b3e9d124276ac.png)

  - **Copy MQTT Client Code**: Enhance the efficiency of generating and using MQTT client code.

    ![Copy MQTT Client Code](https://assets.emqx.com/images/caca6089bb96693d411612b8972c1113.png)

  - **Insert MQTT Test Data**: It's now easy to insert generated MQTT test data into the payload editor.

    ![Insert MQTT Test Data](https://assets.emqx.com/images/6ec2e4ff7f9974a3ef681d987e8707b9.png)

    ![Insert MQTT Test Data](https://assets.emqx.com/images/5457c7f755b79cdf0a6c0605fe21542b.png)

- **Diverse MQTT Test Data Generation**: Automatically create varied MQTT test data.

  ![Diverse MQTT Test Data Generation](https://assets.emqx.com/images/e5b22a0a184443231010126f6e605adf.png)

- **Test Documentation Generation**: Automatically generate test documentation for the current MQTT connection, providing comprehensive documentation for MQTT testing scenarios.

  ![Test Documentation Generation](https://assets.emqx.com/images/8e95de89f6fbe59cd38ea9f22a7bd748.png)

- **User Settings for Copilot**: Reflecting our commitment to user customization and privacy, we've introduced a new setting in Copilot. Users can turn the Copilot feature on or off according to their preference, offering greater control over the tool and ensuring local test data privacy protection.

  ![User Settings for Copilot](https://assets.emqx.com/images/32bb968de9b1c92712d8904cd9458bd0.png)

- **Message Sending Optimization**: Introduce quicker message sending with the Enter key and line breaks with Shift + Enter.

- **Effective Troubleshooting with Connection Info**: Leverage connection data for more efficient problem-solving, streamlining the troubleshooting process within MQTT environments.

- **Enhanced MQTT FAQ Prompts**: Include additional preset MQTT FAQ prompts, offering users better guidance and understanding of MQTTX functionalities.

## Others

- **Connection Management Optimization**:
  - Replace `chart.js` with `echart` to enhance the display of traffic statistics, offering improved visualizations.
  - Address the issue of sending empty authentication information, providing a temporary solution.
    - Known issue: In the MQTT-v5 protocol, the MQTT-packet library incorrectly requires a username when a password is set, contrary to MQTT-v5's allowance for password-only authentication. Thanks to [JimMoen](https://github.com/JimMoen) for the fix: [mqtt-packet PR #148](https://github.com/mqttjs/mqtt-packet/pull/148)
- **OpenAI API**: Adjust the temperature value in the OpenAI API for more accurate Copilot responses.

## Roadmap

In the next development phase following MQTTX 1.9.8, we will focus on boosting visualization capabilities and introducing other key features and improvements.

- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Topic Tree View**: Enhance organization and visualization of topics.
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View:** Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related MQTT topics.

- **IoT Scenario Data Simulation**: Bring this feature to the desktop client to ease IoT scenario testing.
- **Sparkplug B Support**: Extend MQTTX functionalities to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization**: Configurable options to reduce storage space usage.
- **MQTT GUI Debug Functionality**: New features to aid in debugging MQTT communications.
- **Plugin Functionality**: Introduction of a plugin system supporting protocol extensions like CoAP and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **Avro Message Format Support**: Encoding and decoding capabilities for Avro message format.
- **Script Test Automation (Flow)**: Simplify the creation and management of automated testing workflows.



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
