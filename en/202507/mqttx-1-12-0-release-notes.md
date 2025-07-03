MQTTX 1.12.0 lands with **Copilot 2.0** (Gemini 2.5 Pro, Claude-4, GPT-4.1, o3/o4-mini, Azure OpenAI), **native MCP integration** for instant AI workflows, a snappier **Electron 33 + Node 18** desktop, and a CLI capable of firing off exactly-sized payloads for stress tests—delivering a serious intelligence upgrade to the MQTT toolkit.

> Download the latest version here: [https://mqttx.app/downloads](https://mqttx.app/downloads)

## Copilot 2.0: Multi-Model Intelligence

Copilot 2.0 now lets you pick from the latest leading LLMs—**Gemini 2.5 (Pro)**, **Claude-4**, **GPT-4.1**, **o3/o4-mini**, and **Azure OpenAI**—directly inside MQTTX. Choose the model that best fits your workflow and switch at any time within the same session.

![image.png](https://assets.emqx.com/images/1cbf2c66d9e6632fca45e916ac2a6056.png)

### Quick Code & Schema Generation

Need a Protobuf or Avro schema for a new device class, or a JavaScript helper to randomize telemetry? Just describe the idea in plain English—Copilot replies with production-ready code blocks, complete with validation, error handling, inline comments, and sample payloads you can drop straight into the Script page.

### Intelligent Payload Simulation

Copilot understands typical IoT patterns—sensor drift, duty cycles, anomaly spikes—and can synthesize realistic, parameterized data streams that exercise your backend like the real thing. Tweak ranges, frequencies, or outlier ratios in natural language; Copilot regenerates the generator on the spot.

### Typical 5-Minute Workflow

1. **Choose a model** (e.g., Claude-4 for longer reasoning).
2. **Ask:** “Create a JS function that simulates an industrial pump with pressure, temperature, and random fault codes.”
3. **Copy** to drop the generated function into the script panel.
4. **Ask:** “Now give me an Avro schema that matches this payload.”
5. **Publish** to your broker and watch live messages flow, complete with realistic anomalies.

Copilot 2.0 turns hours of manual scripting into minutes of conversational prompting—so you can focus on validating business logic rather than wrangling test data.

![image.png](https://assets.emqx.com/images/eaf9543fd4d855d2410fa576262bf489.png)

## MCP Integration

MQTTX 1.12.0 adds first-class support for the **Model Context Protocol (MCP)**, letting Copilot call external tools and data sources through a single, vendor-agnostic interface.

### What MCP Brings

- **Standard “USB-C” port for AI** – Copilot can reach local or remote resources without exposing raw credentials.
- **Two server types** – connect to MCP servers over **stdio** (run as a local process) or **SSE** (HTTP endpoint).
- **Model-agnostic** – works with every LLM available in Copilot 2.0.

### Quick Setup

1. Open **Settings → Copilot → MCP**.

2. Paste a JSON block that defines one or more servers, e.g.:

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/Users/you/Desktop",
           "/Users/you/Downloads"
         ]
       },
       "mqttx-sse": {
         "url": "http://localhost:4000/mqttx/sse"
       }
     }
   }
   ```

1. Save. Available servers appear in a list; flip the toggle to enable or disable each one.

### Example Workflows

| **Scenario**                                                 | **Prompt to Copilot**                                        | **Result**                                                   |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Generate code to disk** (filesystem server)                | “Create a JS script that connects to @connection and publishes a random temperature every second. Save it as /Users/you/Downloads/mqtt-demo.js.” | Copilot calls the filesystem server and writes the file with the correct connection string. |
| **Publish via AI** ([MQTTX HTTP SSE server](https://github.com/ysfscream/mqttx-mcp-sse-server)) | “Connect to mqtt://broker.emqx.io:1883 and publish ‘hello MCP’ to testtopic/mcp.” | The message appears instantly on any client subscribed to testtopic/mcp. |

### Status & Feedback

MCP support is marked **Beta**. We’re already experimenting with “MCP-over-MQTT” for native discovery and pub-sub tool calls. Try it out and let us know what workflows you want next!

![image.png](https://assets.emqx.com/images/1da3b52a34d32fa14f6c92ae4798f3de.png)

## Desktop Enhancements

MQTTX 1.12.0 now runs on **Electron 33** with **Node 18**, cutting startup time, lowering memory use, and bringing the latest security patches along for the ride.

Your workspace stays just the way you like it—**window size & position are saved on exit and restored on launch**, so you always reopen exactly where you left off.

Search is clearer, too. As you type, keywords are highlighted live in both topic names and payload content, making matches pop instantly—**huge thanks to community contributor** [**@muzaffarmhd**](https://github.com/muzaffarmhd) for the patch that made this possible.

![image.png](https://assets.emqx.com/images/44186a60b1243dbf83969f55caa56ed7.png)

Developer Tools can be opened in production builds for on-site debugging—press **Ctrl + Shift + I** on Windows/Linux, **Cmd + Opt + I** on macOS, or choose **View → Toggle Developer Tools**. Once the panel is up, switch to the **Console** tab, reproduce the issue, and copy any red error or warning messages in full. This on-demand console is invaluable for diagnosing white screens, rendering glitches, or other UI surprises, and it also lets you inspect network traffic and profile performance directly in production-like environments.

![image.png](https://assets.emqx.com/images/3296038ddd4101fc764305531ac7a0c1.png)

## Precise Payload Generation in CLI

The 1.12.0 CLI lets you work with **exact-sized messages**: every incoming payload is reported with its length, and outgoing messages can be generated at a size you specify—ideal for repeatable load tests, bandwidth planning, or broker tuning.

**Parameter**

-S, `--payload-size` <SIZE> — creates a random payload of the requested size.

- Accepted units: B, KB, MB, GB (up to MQTT’s 256 MB ceiling).
- Ignored if you also provide -m, -s, -M, or --file-read, so hand-written payloads aren’t overwritten.

**Examples**

```shell
# Display payload size while subscribing
mqttx sub -t demo
> topic: demo | qos: 0 | size: 12 B
> Hello World!

# Publish a single 1 KB random payload
mqttx pub -t demo --payload-size 1KB

# Generate 512 bytes or 2.5 MB, same flag
mqttx pub -t demo --payload-size 512B
mqttx pub -t demo --payload-size 2.5MB

# Stress-test: 100 publishers, each sending 1 KB
mqttx bench pub -c 100 -t demo --payload-size 1KB
```

## Fixes & Polishing

A final sweep of UX tweaks and under-the-hood fixes rounds out 1.12.0:

- **Copilot Chat UI Preset prompts via “/” shortcut** – Press / in any Copilot chat to pop up a menu of built-in commands. A standout is **Generate Client Code**, which instantly scaffolds MQTT boilerplate for JavaScript, Python, Java, Go, etc, and you can ask for other languages on demand.
- **Paste restored in Monaco editor** – copy-and-paste works again for scripts and payloads.
- **Native scrollbar styling refined (Windows)** – scrollbars now match the OS theme.
- **Search filters persist & apply live** – set a filter once; it sticks and updates with new traffic.
- **Copilot UI glitches fixed** – focus jumps, flicker, and preset-prompt hiccups are gone, and dead code has been trimmed.

## Note for Windows arm64 Desktop users

A dedicated arm64 installer isn’t available in 1.12.0. Please download the **Universal** package from the downloads page— it runs on both x64 and arm64 systems.

## Roadmap

- **MQTTX 2.0 Refactor** is in progress.
- **MCP over MQTT** support.
- **AI Agent Mode** for Desktop and CLI.
- **Payload Chart Visualization Enhancement - MQTTX Viewer**:
  - **Diff View**: Compare different messages or payloads easily.
  - **Dashboard View**: Offer a customizable overview of MQTT activities for personalized insights.
  - **JSON View**: Improve handling and display of JSON formatted data.
  - **System Topic View**: Specialized view for system-related MQTT topics.
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
