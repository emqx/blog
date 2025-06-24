The Internet of Things (IoT) is all about data. But as the volume of data from connected devices explodes, the challenge shifts from simply collecting it to understanding and acting on it in real-time. What if you could ask your data stream questions in plain English? What if you could automatically summarize complex sensor readings into simple, actionable alerts?

The convergence of real-time data streaming and artificial intelligence has reached a new milestone. With the release of EMQX Enterprise 5.10.0, we're excited to introduce LLM integration capabilities directly within our Flow Designer, bringing the power of OpenAI GPT, Anthropic Claude, and any OpenAI-compatible LLM providers to your MQTT data streams.

![image.png](https://assets.emqx.com/images/74b33dc1243c013e4f5bdfb4e9f8192e.png)

<center>EMQX - Bridges the physical world and AI</center>

## Why Combine IoT Data Streams and AI?

Traditionally, applying AI to IoT data required complex and costly engineering. You’d have to move data from your MQTT broker to a separate platform for processing, introducing unacceptable latency for time-sensitive applications.

EMQX now bridges this gap. By embedding AI processing directly into the data flow, you can build intelligent workflows that analyze, enrich, and transform MQTT messages on the fly. This enables a new class of applications that can perceive, reason, and act on live data instantly. The initial release includes seamless integration with models from OpenAI and Anthropic.

![image.png](https://assets.emqx.com/images/81d2d733ddaa09390cac364bf813b705.png)

<center>Embedding AI processing into the MQTT data flow</center>

## Unlock New Possibilities: Key Application Scenarios

Integrating LLMs into your data flows opens up powerful new use cases that were previously difficult to implement.

- **Intelligent Anomaly Detection:** Go beyond simple threshold-based alerts. An LLM can analyze the relationship between multiple fields to identify complex conditions. For example, a payload like `{'vibration': 9.5, 'temp': 85, 'pressure': 1.2}` can be analyzed holistically. The LLM can be prompted to reason that high vibration combined with high temperature in the same reading indicates a more severe issue than either reading alone, generating a nuanced alert like, *"CRITICAL ALERT: Machine XYZ shows simultaneous high vibration and temperature, suggesting potential bearing stress."*
- **Real-time Data Summarization:** Transform raw, complex JSON payloads from sensors into concise, understandable summaries for dashboards or mobile notifications. For example, a raw message like `{"device_id": "device123", "temperature": 38.2, "humidity": 75}` can be automatically converted to *"Device device123 reported a high temperature of 38.2°C and 75% humidity."*
- **Natural Language Data Transformation:** Use plain English prompts to perform complex data manipulations. For instance, you can instruct an LLM to process a JSON payload containing multiple power readings and return only the sum, simplifying data preparation for downstream analytics.
- **Semantic Data Classification:** Automatically classify and route messages based on their content. An LLM can read a device log, determine if it's an "INFO," "WARNING," or "CRITICAL_ERROR" event, and tag the message for appropriate routing to different systems.

## Quick Start: Create Your First AI-Powered Flow in 5 Minutes

Let's see how easy it is to build a flow that reads sensor data and uses OpenAI to generate a human-readable summary. All of this is done in the visual Flow Designer without writing a single line of code.

**Prerequisite:** You'll need a valid OpenAI API Key.

**Step 1: Set Up Your Data Source**

In the EMQX Flow Designer, drag a **Messages** node onto the canvas. Configure it to subscribe to the MQTT topic where your devices publish data, for example, `sensors/temp_humid`.

![image.png](https://assets.emqx.com/images/2ab172c30aa252392e603022092bd410.png)

**Step 2: Add the AI Magic**

Drag an **OpenAI** node from the processing panel and connect it to your source node. In the configuration panel:

- **Input:** Select `payload` to pass the entire MQTT message payload to the model.
- **System Message:** Enter your instruction in plain English. For example: *"Generate a short summary of the device's sensor readings in human-readable format."*
- **Model:** Choose an OpenAI model, such as `gpt-4o`.
- **API Key:** Securely enter your OpenAI API Key.
- **Output Result Alias:** Give the AI's output a name, like `summary`.

![image.png](https://assets.emqx.com/images/52fdacbeb490c779938f842144b9d7a5.png)

**Step 3: Republish the Insight**

Drag a **Republish** node from the sink panel and connect it to the OpenAI node. Configure it to publish the result to a new topic, like `ai/summary`, using the alias you just created in the payload field: `${summary}`.

![image.png](https://assets.emqx.com/images/5451e1e49d3eebddfaf9d202ec51fdb8.png)

**Step 4: Deploy and Test**

Connect all the nodes and save the flow. 

![image.png](https://assets.emqx.com/images/2cae54cca2e4e192f5612922b404efd8.png)

Now, when you publish a JSON message to the `sensors/temp_humid` topic, you will see a natural language summary appear on the `ai/summary` topic in real time!

Example:

Publish a test message like:

```json
{
  "device_id": "device123",
  "temperature": 38.2,
  "humidity": 75,
  "timestamp": 1717568000000
}
```

And receive an intelligent summary:

> "On June 5, 2024, the device with ID ‘device123’ recorded a temperature of 38.2°C and a humidity level of 75%."

![image.png](https://assets.emqx.com/images/a5c545fad2e17ff7fed1d99b815c66fe.png)

For a complete demo, please watch this video:

<video src="https://assets.emqx.com/data/video/EMQX_LLM_DEMO.mp4" controls style="max-width: 100%;">
  Your browser does not support the video tag.
</video>

## Beyond Basic Processing: Advanced AI Capabilities

The LLM integration in EMQX 5.10 goes beyond simple data summarization. You can:

- **Classify and categorize** incoming data streams
- **Generate alerts** based on complex pattern recognition
- **Extract structured information** from unstructured sensor logs
- **Provide contextual recommendations** based on historical patterns
- **Translate technical data** into business-friendly insights

## Performance Considerations

Invoking an LLM and processing data takes time. The entire process may take several seconds to over ten seconds, depending on the response speed of the model. Therefore, LLM processing nodes are not suitable for scenarios with high message throughput (TPS).

For optimal performance:

- Apply LLM processing selectively to high-value data
- Use data filtering to process only relevant messages
- Consider aggregating multiple data points or messages at the edge before sending them as a single MQTT message to the broker
- Monitor processing times and adjust accordingly

## What's Next?

The LLM integration in EMQX 5.10 represents just the beginning of our AI journey. We're already working on additional AI capabilities, including:

- Support for more LLM providers
- Vector embedding generation for semantic search
- Integration with popular AI frameworks
- Enhanced prompt templates and optimization tools

## The Future with EMQX is Intelligent and Real-Time

The integration of LLMs into EMQX is more than just a new feature; it's a paradigm shift for IoT application development. By empowering developers to leverage generative AI within their data pipelines using a simple, low-code interface, we are making it easier than ever to build truly smart, responsive, and autonomous systems.

**Ready to activate your IoT data with AI?**

- [**Download EMQX Enterprise 5.10.0**](https://www.emqx.com/en/downloads-and-install/enterprise) to get started.
- Dive deeper with our technical documentation on [**LLM-Based Data Processing**](https://docs.emqx.com/en/emqx/latest/flow-designer/llm-based-data-processing.html).
- Follow our step-by-step tutorials for [**OpenAI**](https://docs.emqx.com/en/emqx/latest/flow-designer/openai-node-quick-start.html) and [**Anthropic**](https://docs.emqx.com/en/emqx/latest/flow-designer/anthropic-node-quick-start.html).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
