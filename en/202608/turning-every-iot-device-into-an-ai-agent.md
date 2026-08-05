## Meet Device Agent: Reimagining Hardware Intelligence



The hardware industry is undergoing a quiet revolution.

Over the past decade, the core objective was connectivity: getting devices online and sending data to the cloud. Today, the focus has shifted to intelligence: enabling devices to understand intent, make autonomous decisions, and collaborate. 

Yet, turning this vision into reality poses a steep engineering challenge. Bringing natural language AI to a hardware device typically requires months of cross-functional alignment across embedded, backend, AI, and frontend teams, and the resulting intelligence is rarely reusable across different product lines.

That’s why we offered EMQ Device Agent.

Device Agent is an MQTT-driven platform for AI-powered device agents. Simply describe your device's capabilities in plain natural language, and the platform generates a complete, functional agent in minutes, including structured device specifications, edge SDKs, an online web simulator, and multi-channel interaction tools across voice, vision, and instant messaging.

Rather than just another AI chat overlay on top of an IoT connection layer, Device Agent provides a unified toolchain spanning from device modeling to decentralized multi-agent collaboration.

This article provides an overview of Device Agent's design philosophy, core capabilities, and technical architecture, explaining how natural language-driven modeling, multimodal interaction, skill extensions, and decentralized collaboration come together to rapidly turn any physical device into an intelligent AI agent capable of understanding, decision-making, and teamwork.

![image.png](https://assets.emqx.com/images/2971e00365b4c68d5afcf6943bf28af9.png)

## Natural Language Device Modeling



Creating a device agent starts with a simple description, not code. Simply describe what your device is, the commands it accepts, the telemetry it reports, and the events it triggers. The platform automatically generates a structured specification (commands, attributes, and events) complete with field types and validation rules.

If the generated spec needs tweaking, just keep chatting. With interactive side-by-side editing, your descriptions sit on the left while a live preview renders on the right. Describe, preview, revise, and confirm. This continuous loop turns traditional technical documentation into a fluid dialogue between product managers and engineers.

The platform natively supports English, JSON, YAML, and Markdown inputs. You can also specify field naming conventions directly in your prompt, and the model will follow them precisely.

![image.png](https://assets.emqx.com/images/acbfb6d146e5a9efa06f2a104665944b.png)

## Conversational Device Control



Once an agent is created, managing the physical device becomes as simple as having a conversation.

- **Direct Commands:** Say *"Set the target temperature to 24°C and switch to auto mode."* The agent interprets the intent, matches the appropriate command from the device spec, formats the parameters, and sends it directly to the hardware.
- **Telemetry & Event Queries:** Ask *"Check the current status and tell me if any recent events were reported."* The agent reads the real-time telemetry and event logs, returning a clear, natural response.
- **Multi-Device Management:** Targeting specific hardware requires no navigation across different dashboards. Simply type `@thermostat-01` in the prompt, or mention multiple `@` handles simultaneously to compare states or issue batch commands.
- **Automated Rules:** You can set up scheduled tasks conversationally: *"Check the temperature every 5 minutes. If it exceeds 30°C, adjust the target to 24°C."* The agent saves this as a built-in timer, allowing the gateway to execute the task independently. You can inspect active timers at any time with *"What scheduled tasks are currently running?"* and cancel them just as easily.

![image.png](https://assets.emqx.com/images/ce6a5c63a5221104fc88cb018b5e7078.png)

## Multimodal Interaction: Voice and Vision



The end-to-end voice pipeline is completely seamless: audio is captured via microphone, transcribed to text in real time, processed by the agent, and returned as natural speech synthesis.

Out of the box, Device Agent integrates with major global voice providers, including AWS and  ElevenLabs. To bring your device to life, select a provider in the console and enter your API key.

On the device side, integration is equally straightforward: connect to `/ws/voice`, stream 16kHz mono PCM audio frames, and receive TTS audio playback frames. We recommend validating the end-to-end flow in the console prior to deploying code onto real hardware.

If a camera feed is connected, visual frames are automatically appended to voice queries. Asking *"What color is this indicator light?"* prompts the agent to analyze both the speech input and the camera frame to deliver an accurate answer.

![image.png](https://assets.emqx.com/images/701eaacafceefbd01da544366007953a.png)

## Skills & Tools: Extending Capabilities Beyond Hardware



Device commands define basic physical actions: power toggles, temperature adjustments, and mode switches. However, production workflows often require querying external enterprise systems or executing complex business logic. To support this, Device Agent organizes capabilities into three distinct layers:

1. **Device Specifications:** Define core hardware actions and attributes.
2. **Skills:** Define knowledge and standardized procedural templates. Packaged as a `.zip` archive containing a `SKILL.md` description and response templates, imported skills require no manual invocation. When a user states an intent, the agent automatically evaluates whether to load the relevant skill and format its response accordingly.
3. **Tools:** Provide executable TypeScript code with parameter schemas powered by TypeBox. Once saved to the runtime, the agent can autonomously orchestrate complex multi-step workflows (such as reading a device state, executing an external tool calculation, and triggering a device command in response.)

## One-Click SDK Generation & Hardware Simulation



Once your device specification is finalized, connecting physical hardware takes a single click: click "Connect Device", select your target programming language, and download the ready-to-use project bundle.

The platform automatically generates edge SDKs for C, Python, and TypeScript. Every generated project includes production-ready code for MQTT connection management, command handlers, telemetry publishing, event reporting, and voice/vision clients. Developers only need to supply the low-level hardware drivers in `device.*` (e.g., sensor reads and actuator triggers).

If the device-side logic hasn't been written yet, you can describe the operational rules directly in natural language: *"Read telemetry from the DHT22 sensor every 30 seconds and trigger an alert if temperature exceeds 30°C."* The agent will generate a fully runnable codebase built on top of the SDK.

When physical hardware isn't available, the browser-based simulator creates a virtual device from the specification that automatically connects to MQTT, reports state, and responds to commands, allowing product teams to validate user experience long before hardware prototypes arrive.

![image.png](https://assets.emqx.com/images/2363b14005f27e00f3b8da614d37f3e4.png)

## Open Protocols & Decentralized Agent Collaboration



After individual devices become intelligent, the next challenge is enabling cross-device collaboration.

To solve this, we developed A2A (Agent-to-Agent), an inter-agent communication protocol built on EMQX 6.2. Using MQTT v5 as the transport layer and JSON-RPC for invocation formats, A2A eliminates the need for a central orchestrator. Every agent operates as a peer node capable of automatic discovery, task negotiation, and service invocation.

Enabling A2A requires toggling a single switch during agent creation. Every command in the device spec is automatically published as a discoverable skill for other agents. You can also build Composite Applications by selecting multiple device agents and defining high-level collaborative goals for a master orchestration agent to coordinate.

Additionally, Device Agent natively supports major instant messaging platforms like Slack, Discord, and Telegram. Each integration supports user-ID whitelisting to ensure secure control directly from your team’s daily workspace.

![image.png](https://assets.emqx.com/images/a13de00385b61d8b971a386dbdd8fb81.png)

## Model Support & Infrastructure



Device Agent supports over 20 LLM providers, including OpenAI, Anthropic, Google, DeepSeek, Ollama, as well as cloud aggregators like AWS Bedrock and Azure OpenAI. Switch models at any time by entering your key in the console. Vision capabilities can be configured independently or turned off to optimize operational costs.

At the infrastructure level, the platform is powered by the EMQX messaging platform, providing massive scale (tens of millions of concurrent device connections) over standard MQTT protocols. Device Agent supports private on-premises deployment, keeping device data entirely within your own infrastructure.

## Start Today



Software development has entered the agentic era, and hardware development is following suit. From standalone smart devices to interconnected systems, Device Agent bridges the gap between hardware and AI.

Deploy Device Agent locally with a single command to model your first device, generate edge SDKs, launch the simulator, and control hardware using natural language.

**macOS / Linux：**

```shell
curl -fsSL https://emqx.sh/device-agent | sh
```

**Windows PowerShell：**

```shell
powershell irm https://emqx.sh/device-agent.ps1 | iex
```

Learn more about Device Agent: [Device Agent - Turn Any IoT Device into an AI Agent](https://www.emqx.com/en/device-agent)
