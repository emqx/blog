The [MQTT 5.0 client tool MQTTX](https://mqttx.app/) has recently rolled out its version 1.9.7. A significant highlight of this release is the introduction of **MQTTX Copilot**, our innovative MQTT AI assistant, specially designed to offer crucial convenience to users. This feature improves user interaction by providing intuitive assistance for better understanding and utilization of MQTT and EMQX. The update also addresses several bug fixes, leading to a notable improvement in the overall user experience.

> *Download the latest version here:* [*https://mqttx.app/downloads*](https://mqttx.app/downloads)

## MQTTX Copilot

MQTTX Copilot is an AI assistant designed to help with MQTT-related queries, provide solutions for common issues, and offer insights on best practices.

Using MQTTX and [EMQX](https://www.emqx.com/en/products/emqx) can be easier than ever with this tool. It simplifies testing MQTT connections, publishing and subscribing to topics, debugging, and developing MQTT applications and brokers, enriching your MQTT experience.

![MQTTX Copilot Preview](https://assets.emqx.com/images/d072d9c582feed8f2c50159f232020b5.png)

<center>MQTTX Copilot Preview</center>

### Preparation Before Getting Started

MQTTX Copilot is powered by OpenAI's GPT models. To use it, you need to configure your OpenAI API key on the MQTTX settings page located at the bottom. You can find detailed steps and information for getting your API key on the [OpenAI API Keys page](https://platform.openai.com/api-keys).

Also, remember to choose a language model version(e.g. GPT-3.5 or GPT-4) that aligns with your specific needs and OpenAI API Key requirements.

![Copilot Settings](https://assets.emqx.com/images/8f4232445a2e76400032a806597ca96a.png)

<center>Copilot Settings</center>

### Error Analysis with One Click

When encountering errors during connection or subscription, you can swiftly click the “Ask Copilot” button within the error prompt. Upon activation, MQTTX Copilot will assist you in analyzing potential causes for the issue, enabling you to methodically check and troubleshoot each possibility to identify and resolve the error.

![Error Analysis with One Click 1](https://assets.emqx.com/images/f3d2cc09ab5c29190b8dd935f40fa7cd.png)
![Error Analysis with One Click 2](https://assets.emqx.com/images/8b22f4a77ce42a821dbcab57615706a9.png)

### AI-Powered Code Generation

MQTTX Copilot now offers a one-click solution for generating MQTT client codes tailored to your current test connections. This feature greatly simplifies setting up MQTT clients in various programming languages. Currently, MQTTX Copilot supports code generation for several languages, including:

- JavaScript
- Python
- Java
- Golang
- ...

This functionality ensures a more streamlined and efficient development process, making it easier for users to integrate MQTT into their projects.

![AI-Powered Code Generation](https://assets.emqx.com/images/5bc0faa7671f0f6cc7f7af29b59ab063.png)

### MQTT FAQs and EMQX Tutorials

MQTTX Copilot offers tutorials on EMQX installation and usage, along with MQTT FAQs guidance, to enhance users' proficiency in MQTT and EMQX.

![MQTT FAQs and EMQX Tutorials](https://assets.emqx.com/images/a2ed4853459addf386cd01b4932aef09.png)

### Automated Test Data Generation

MQTTX Copilot simplifies test payload generation, allowing users to analyze and optimize MQTT data implementations quickly.

![Automated Test Data Generation](https://assets.emqx.com/images/a86a250549e6c173fa34a91402ede53c.png)

### Current Connection Information

With just one click, MQTTX Copilot offers valuable insights into MQTT connections by analyzing and interpreting connection information. This feature empowers users to effectively manage and optimize their MQTT connections.

![Current Connection Information](https://assets.emqx.com/images/e747eba5a7f50c3258d4d6e0f3c46a0a.png)

Besides, MQTTX Copilot allows users to edit prompt messages and quickly access relevant information using the `@connection` keyword. This enables customization and other upcoming features like topic management, automatic payload filling, and EMQX log analysis to enhance the MQTTX Copilot experience.

## Fixes and Improvements

In addition to the launch of MQTTX Copilot, MQTTX 1.9.7 includes a variety of optimizations and fixes:

### JSON Data Precision (Desktop, CLI, Web)

The issue of data precision loss in JSON messages has been solved, ensuring an accurate representation of long-type numerical data. (BigInt Support)

![JSON Data Precision (Desktop, CLI, Web)](https://assets.emqx.com/images/836037793c9f5bf1ffe7b532b97041ce.png)

### SSL Option Clarified (Desktop)

It enhanced the SSL option to include `CA Signed server certificates` and `CA or Self-Signed certificates` for improved clarity.

![SSL Option Clarified (Desktop)](https://assets.emqx.com/images/5dc5f442c89b17c5e105e9578b235ebf.png)

### Topic-Alias Issue Fix (Web, CLI):

The topic-alias maximum error in web and CLI connections has been resolved. This fixes the issue of MQTTX CLI not receiving messages with topic aliases properly, and also addresses the problem of not being able to set a maximum topic alias.

### Others

- **Reconnection Issue Fixed (Desktop)**: Addressed issues with reconnection after disconnection.
- **Unused Placeholders Removed (Desktop)**: Cleaned up unused placeholders in code.
- **Translation Updates (Desktop, Web)**: Improved translations for specific languages.
- **Typo Corrections (Desktop)**: Corrected typographical errors in documentation or code.
- **Web README Update**: Improved the README documentation for MQTTX Web.

## Special Thanks

Huge thanks to [@ni00](https://github.com/ni00) for resolving critical issues like JSON precision and topic alias, and to [@Rotzbua](https://github.com/Rotzbua) for documentation and engineering fixes in MQTTX.

## Roadmap

- **MQTTX Copilot Enhancements:** Upgrades to include stream output, payload autofill, payload analysis, and automatic creation of connections and subscriptions to topics.

- **IoT Scenario Data Simulation:** Sync this feature to the desktop client to simplify the testing of IoT scenarios.
- **Sparkplug B Support:** Extend the functionalities of MQTTX to include support for Sparkplug B.
- **QoS 0 Message Storage Optimization:** Reduce storage space usage through configurable options.
- **MQTT Debug Functionality:** Introduce features to assist users in debugging MQTT communications.
- **Automatic Chart Drawing:** Automatically transform received messages into charts for more straightforward analysis.
- **Plugin Functionality:** Launch a plugin system that supports protocol extensions such as [CoAP](https://www.emqx.com/en/blog/coap-protocol) and [MQTT-SN](https://www.emqx.com/en/blog/connecting-mqtt-sn-devices-using-emqx).
- **Avro Message Format Support:** Introduce encoding and decoding functionalities for Avro message format.
- **Script Test Automation (Flow):** Simplify the creation and management of automated testing workflows.

 

<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
