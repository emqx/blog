## Introduction

We're excited to announce the integration of **Claude 3.7 Sonnet** with **MQTTX Copilot**. This powerful addition brings intelligent code generation to your MQTT testing workflows.

MQTT testing often requires creating realistic data payloads, transforming messages, and implementing processing logic - tasks that can be tedious and time-consuming. Claude 3.7 Sonnet excels at code generation with its advanced understanding of programming patterns. The integration helps you instantly generate custom functions and data schemas within your testing environment, significantly speeding up your IoT development and testing processes.

## Getting Started

To configure Claude 3.7 Sonnet integration, visit the MQTTX settings page and select Claude 3.7 Sonnet as your preferred model under the AI settings section. If you haven't set up MQTTX Copilot yet, you'll need to enter your API key in the settings panel.

![image.png](https://assets.emqx.com/images/cd330887e413bea5fe0447b1bd4c7a4a.png)

Once configured, accessing MQTTX Copilot with Claude 3.7 Sonnet is straightforward. Open MQTTX, navigate to the script page and click the MQTTX Copilot button in the interface. From there, you'll have direct access to the new Claude-powered code generation features for your MQTT testing scenarios.

![image.png](https://assets.emqx.com/images/0f13351028ac9218a4a22c654d39ae90.png)

![image.png](https://assets.emqx.com/images/3561630506622f015bfcec01b5b6fd71.png)

## Core Functionality

### Intelligent Code Generation

MQTTX Copilot offers powerful code generation capabilities to streamline your MQTT testing workflows. The system provides preset templates for immediate use and custom generation options for more specialized requirements.

With preset templates, you can quickly generate code for common testing scenarios without writing a single line of code:

- **Simulate Weather Data**: Generate realistic weather metrics with configurable ranges and random fluctuations for sensor simulation testing. Parameters like temperature and humidity ranges can be easily adjusted to match your testing environment.
- **Dynamic Command Switching**: Create functions that intelligently alternate between command states based on message index or other triggers. This is particularly useful for testing device control sequences or state transitions in your IoT applications.
- **Time Format Processing**: Convert Unix timestamps to human-readable time strings with timezone support, making your test data more intuitive and easier to analyze. The system handles all the complex conversion logic for you.

![image.png](https://assets.emqx.com/images/6404e6b4604893a1431ed64f6c3151f1.png)

Describe your needs in natural language for unique testing requirements, and MQTTX Copilot will generate custom code tailored to your specific scenario. The generated functions follow industry best practices with proper error handling, input validation, and clear comments that explain the processing logic.

### Schema Generation

Efficiently structure your MQTT test messages with automated schema generation for Protobuf and Avro formats. This feature helps standardize message formats across your testing environments, ensures data integrity, and optimizes payload size for more efficient communication.

MQTTX Copilot can generate complete schemas for common IoT scenarios out of the box:

- **Smart Home Device Status Reporting**: Structured formats for device states, sensor readings, and system status reports typical in home automation environments.
- **Industrial Equipment Alarm Messages**: Standardized formats for alert severity, error codes, timestamps, and contextual information needed for industrial monitoring.
- **Connected Vehicle Telemetry Data**: Comprehensive data structures for GPS coordinates, speed, fuel/battery levels, and other vehicle metrics.
- **Smart Meter Real-time Readings**: Precisely formatted schemas for power consumption, voltage readings, and time-series meter data.

![image.png](https://assets.emqx.com/images/48464e7124db19fd6b23c1c10d737bbf.png)

Each generated schema includes comprehensive field definitions, appropriate data types, and required/optional field indicators, and it arrives with corresponding sample data ready for immediate testing. For custom requirements, describe your data structure needs in plain language, and the system will create a tailored schema specification that matches your exact requirements.

![image.png](https://assets.emqx.com/images/bd43a4dd3304437c2091acfd5c847e3d.png)

For any generated code or schema, click the "Insert" button in the top-right corner of the code block to seamlessly add the complete code to your editor, allowing you to begin testing or further customizing the solution immediately.

## End-to-End IoT Device Simulation

Let's walk through a complete example of how MQTTX Copilot streamlines the testing process for IoT applications:

**Smart Thermostat Testing Scenario**

Imagine you're developing a smart home platform that needs to process data from various thermostats. Here's how you can create a comprehensive test environment in minutes:

1. **Generate Data Processing Function:**

   - Select the custom code generation option in MQTTX Copilot.
   - Request: "Create a function that simulates smart thermostat data with temperature readings, target temperature, HVAC mode (heat/cool/off), humidity level, and battery percentage. Include realistic fluctuations and occasional anomalies."
   - Insert the generated JavaScript function into your MQTTX script editor.

   ![image.png](https://assets.emqx.com/images/b1a6064fac2febbf1329b9efdd6ccae9.png)

2. **Create Message Schema:**

   - Use the Schema Generation feature in MQTTX Copilot.
   - Request: "Generate a Protobuf schema for smart thermostat data that includes temperature, target temperature, HVAC mode, humidity percentage, and battery level with appropriate data types and field numbers."
   - Review the generated schema which provides a standardized structure for your thermostat messages.
   - Insert the schema into your project for reference and implementation.

   ![image.png](https://assets.emqx.com/images/d5bb66112faa4aeb13ce73368ca1cc0d.png)

1. **Execute the Test:**

   - Run your script in MQTTX to publish simulated thermostat data.
   - Watch as the function generates realistic data with natural variations.
   - Observe the formatted messages in the MQTTX message view.
   - Analyze how your application processes and responds to the various device states.

   ![image.png](https://assets.emqx.com/images/9c0bd2a16f70d355ad09b81f56129ba6.png)

This integrated approach allows you to create realistic test environments with properly structured data quickly. The generated code handles all the complexities of creating varied, realistic test scenarios while the schema ensures your message format remains consistent.

## Boosting MQTT Testing with AI-Powered Tools—And More to Come!

Integrating Claude 3.7 Sonnet with MQTTX Copilot drastically reduces the time spent on MQTT testing setup. Automating test function creation, data payload generation, and schema development allows developers to focus on validating application behavior rather than crafting test data.

This feature will be officially available in MQTTX version 1.12.0. Beyond Claude 3.7 Sonnet, we've also integrated support for multiple advanced AI models including DeepSeek, Grok, and others, giving you flexibility to choose the model that best fits your specific requirements.

In upcoming releases, we'll introduce advanced AI Agent capabilities and integrate MPC (Model Context Protocol) into MQTTX to support even more sophisticated AI functionalities.

Please get in touch with our team if you're interested in additional AI capabilities for EMQX or have specific AI scenarios you'd like to explore. We're eager to collaborate on new ways to leverage AI in your MQTT development workflows.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
