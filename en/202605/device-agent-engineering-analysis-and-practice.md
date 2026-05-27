### Introduction

In the IoT industry, hardware sets the boundaries of what a product can do, while software determines how much of that potential is actually realized. Yet whether we're talking about consumer smart hardware or enterprise systems like lighting, HVAC, and access control in office spaces, the software development phase almost always becomes the biggest variable in project delivery, even after the hardware team has completed its prototype or finalized component selection.

From chip adaptation to the end user's app, from single-device control to multi-system coordination, there is a significant amount of underestimated technical complexity and organizational coordination cost embedded in this process.

This article attempts to break down the full chain of IoT device intelligence from an engineering management perspective, analyze the root causes of efficiency bottlenecks, and explore a potential path forward.

### I. The Typical Development Pipeline

From project initiation to mass production, the software development of a smart hardware product typically involves the following stages:

**Chip/Module Selection → Hardware Driver Development → Cloud Service Setup → Agent/AI Capability Development → App/Mini-Program Development**

#### 1.1 Work Involved at Each Stage

Using a moderately complex IoT device (e.g., a smart lamp with voice interaction) as an example:

| Stage                        | Technology Stack                             |
| :--------------------------- | :------------------------------------------- |
| Chip/Module Adaptation       | C embedded, RTOS, communication protocols    |
| Hardware Driver Development  | C low-level drivers, sensor interfaces       |
| Cloud Service Setup          | Go/Java/Node.js, databases, message queues   |
| AI Capability Integration    | Python, LLM APIs, ASR/TTS SDKs               |
| App/Mini-Program Development | React Native / Flutter / WeChat Mini Program |

In summary, the software development cycle for a consumer-grade single product can easily take several months, involving 3–5 teams with different technical backgrounds. Large enterprise deployments can take months to years, involving device manufacturers, system integrators, and enterprise IT departments collaborating across organizational boundaries, and that's before accounting for time spent on cross-team interface alignment, integration testing, and iterative optimization.

#### 1.2 The Hidden Costs of Multi-Stack Collaboration

The stages above are not a simple sequential pipeline; they form a tightly coupled, mesh-like dependency structure:

- The device-side communication protocol must stay consistent with the cloud-side message format
- AI capability outputs need to be consumed by both the device side and the app simultaneously
- App interaction logic must match the device's actual response capabilities
- Any change on one side can trigger cascading modifications across the others

In practice, cross-team interface alignment consumes an enormous amount of time. A typical scenario: the embedded engineer defines a set of MQTT message formats; the backend engineer discovers missing fields during implementation; the app engineer finds that the interaction flow doesn't match expectations during integration testing. This "build and fix as you go" pattern is pervasive in the industry.

### II. Three Root Causes of Efficiency Bottlenecks

#### 2.1 Technology Stack Fragmentation

IoT intelligence spans an extraordinarily wide range of technology stacks:

- **Device side:** C/C++, Linux/RTOS, MQTT, low-power design
- **Cloud side:** microservices, databases, caching, message queues, container orchestration
- **AI layer:** large model APIs, speech recognition, NLP, vector databases
- **Client side:** cross-platform frameworks, native development, UI/UX design

Very few engineers or single teams can be proficient across all of these domains simultaneously. Consumer-grade projects rely on collaboration between embedded, backend, AI, and frontend teams. Enterprise-grade projects further involve device manufacturers, system integrators, and enterprise IT departments. The knowledge silos and communication overhead between teams frequently lead to distorted information transfer and delayed decision-making.

#### 2.2 The High Bar for AI Capability Integration

Voice interaction, natural language understanding, and multimodal perception are increasingly expected in higher-end or AI-oriented smart devices. But integrating these capabilities is far from a simple API call:

- **Speech recognition:** requires handling different accents, noisy environments, and wake-word optimization, involving careful selection and tuning of ASR engines
- **Large model integration:** requires designing prompt engineering, context management, and intent parsing modules to ensure interaction accuracy and response speed
- **Multimodal interaction:** visual understanding, gesture recognition, and similar capabilities require additional model deployment and on-device optimization

For consumer hardware manufacturers, building an AI team with all of these competencies is costly; it requires simultaneously covering algorithm engineering, prompt engineering, ASR tuning, and multimodal fusion, and talent in these areas is in limited supply. This means manufacturers either bear high staffing costs or compromise on AI capabilities by using off-the-shelf generic solutions, making product differentiation difficult.

For enterprise users, AI capability integration faces additional hurdles:

- **Data security and compliance:** enterprise device data often involves trade secrets and cannot simply be uploaded to public cloud LLM services; may require private deployment, local inference, or stricter cloud controls
- **Integration with existing systems:** AI outputs need to be consumed by internal ERP, ticketing, and BI platforms, not just end-user interaction interfaces
- **Permissions and auditing:** enterprise scenarios require AI decisions to be traceable and auditable, requiring additional logging, access control, and multi-tenant isolation

#### 2.3 Limited Scenario Scalability

The current smart device market faces a two-tier "silo" problem.

**The standalone device silo in consumer scenarios:** Most smart hardware products exist as standalone items. After purchase, users can only use the device's built-in functionality, with little ability to collaborate with other devices. This creates problems on multiple levels:

- *User experience:* A user's home may contain smart devices from multiple brands, each with its own app and control scheme, and the experience is fragmented
- *Business value:* The limited use cases of standalone products reduce purchase motivation, lower repurchase rates, and make it hard for brands to build long-term loyalty
- *Technical:* Cross-device collaboration requires a unified communication protocol and task scheduling mechanism, and building this from scratch carries a high technical barrier

**The system silo in enterprise scenarios:** In office spaces or commercial buildings, lighting, HVAC, access control, and security systems typically come from different vendors and run on separate control platforms. For an enterprise to implement cross-system linkages like "lights on when people arrive, AC conserves energy when people leave," it requires substantial engineering effort: connecting to each vendor's proprietary API one by one, writing hardcoded automation rules, and maintaining fragile middleware pipelines. If any vendor upgrades their interface or changes a device model, the entire linkage chain can break. This integration model carries extremely high maintenance costs and scales poorly as business needs evolve.

### III. Engineering Perspectives on Solutions

Facing these bottlenecks, engineering optimizations can be approached at three levels.

#### 3.1 AI-Native Agent Generation

The idea of platformizing general capabilities is not entirely new. Over the past decade, various IoT platforms have done substantial standardization work at the connectivity layer, unifying device onboarding protocols, providing cloud-side message channels, and encapsulating device management APIs. These platforms solved the problem of "getting devices online," but the part about "giving devices intelligent interaction capabilities" has remained the manufacturer's responsibility to build independently.

Specifically, the limitations of traditional IoT platforms include:

- **Device modeling still requires manual effort:** Engineers must manually fill out definition forms for attributes, commands, and events on the platform, a process that is disconnected from the subsequent code development
- **AI capabilities must be self-integrated:** For speech recognition, large model conversation, intent parsing, and similar modules, platforms typically only provide basic SDKs; the specific prompt engineering, context management, and multi-turn dialogue logic must still be implemented by the manufacturer
- **Full validation still depends on hardware:** Without a hardware prototype, much of the interaction flow can be tested earlier through simulators and virtual devices, but final validation still requires physical hardware, which can extend the iteration cycle

The maturity of AI technology now makes platformization possible at a deeper level, evolving from a "connectivity management platform" to an "agent generation platform." In this new model, AI participates in the core development process, significantly reducing the workload at each stage:

- **Device modeling phase:** Manufacturers describe device capabilities in natural language. Consumer scenario: "This is a desk lamp that supports brightness adjustment and color temperature switching, controllable by voice." Enterprise scenario: "This is the lighting system on the 3rd floor of an office building, comprising 50 dimmable fixtures and 10 light sensors that need to automatically adjust brightness based on foot traffic." The system parses this automatically and generates a standardized device specification, with no manual preparation of product specs required.
- **Development phase:** Based on the device specification, the platform automatically generates a complete device-side SDK (including MQTT connection, message sending/receiving, and command parsing). Manufacturers only need to integrate the generated SDK into the target hardware platform and make minor adaptations for the specific MCU to quickly complete device-side development.
- **Debugging phase:** Without waiting for a hardware prototype, an online simulator can virtualize the device's complete behavior from the specification, supporting end-to-end debugging of voice, visual, screen, and other multimodal interactions. Product managers can validate the interaction experience early in the development cycle and front-load feedback.
- **Ecosystem connectivity phase:** Devices are no longer merely managed data nodes; they are intelligent agents with autonomous decision-making capabilities. Via the A2A protocol, devices can automatically discover nearby agents, negotiate task assignments, and autonomously complete cross-device collaboration without manually written automation rules.

The core distinction of this platformized approach: **traditional platforms focused on platformizing infrastructure, while AI-native platforms platformize intelligence itself.** When manufacturers onboard the platform, they receive not just a data channel, but a fully operational device agent capability set.

#### 3.2 A Unified Device Model to Define Agent Capability Boundaries

In traditional development, the device side, cloud side, and client side each maintain their own data structures, kept in sync through documentation or informal agreements. The fragility of this approach is that any change on one side can break the contract. A more robust approach is to introduce a unified device model as the "single source of truth."

In the context of agent generation, the device model is no longer merely a data structure definition; it is a description of the agent's capability boundaries. The device specification defines what the agent can perceive, what it can execute, and what it can report:

- **Properties:** Environmental states the agent perceives, such as brightness, temperature, and battery level
- **Commands:** Operations the agent can execute, such as on/off, adjustment, and restart
- **Events:** State changes or anomaly alerts the agent proactively reports

Based on a unified device specification, the SDK code framework for the device side can be automatically generated (data structures and message handling logic), and manufacturers only need to integrate the generated SDK into the target hardware platform and make minor adaptations for the specific MCU. This **definition-driven development** model bridges device capability description with code generation, eliminates the manual translation step, reduces human error, and makes the agent's capability boundaries clearly verifiable.

#### 3.3 Introducing the A2A-over-MQTT Protocol as Cross-Device Collaboration Infrastructure

The core challenge of cross-device collaboration is: how do device agents from different manufacturers, running on different platforms, understand and cooperate with each other?

One viable solution is the Agent-to-Agent (A2A) protocol. A2A defines standard communication methods between device agents, including:

- **Auto-discovery:** When a new device joins the network, it automatically broadcasts its capabilities to nearby agents
- **Task negotiation:** Multiple agents negotiate task assignments via standardized messages, without requiring a central controller to coordinate
- **Autonomous collaboration:** Agents independently execute their assigned tasks based on negotiation results and feed back execution outcomes to relevant parties

The advantage of this distributed collaboration model is that it does not depend on any centralized platform or vendor; any device that supports the A2A protocol can join the network as an equal participant, enabling true cross-brand interoperability.

A typical consumer scenario is "leaving home mode": after a user issues a command, the security agent automatically activates surveillance, the lighting agent turns off lights in each room in sequence, the HVAC agent switches to energy-saving mode, and the cleaning agent begins its sweep. The entire process is completed through autonomous negotiation among the agents, with no manually preconfigured automation rules and no central controller for unified scheduling.

Enterprise scenarios work the same way. For example, "conference room energy-saving mode": the room booking system sends an idle notification to the conference room agent; the lighting agent automatically dims the lights; the HVAC agent switches to an energy-saving temperature; the blinds agent closes the shades to maintain room temperature. Each agent executes autonomously via the A2A protocol, with no cross-system automation rules to write and no per-room configuration needed.

### IV. Device Agent in Engineering Practice

Device Agent is not a conceptual methodology; it is a complete engineering solution built on the thinking described above. It integrates the AI-native platformization, unified device model, and A2A protocol from Section III into a deployable toolchain, backed by EMQ's long-term foundation in IoT infrastructure to provide a reliable runtime substrate for device agents.

#### 4.1 Implementing the Core Architecture

Device Agent's engineering implementation maps directly to the two core layers described earlier:

- **Agent development layer:** Natural language modeling, device specification generation, automatic SDK generation, and an online simulator are integrated into a unified development environment. Engineers simply describe device capabilities and can generate a compilable, runnable device-side SDK with one click, then validate the interaction experience in the simulator, with no need to switch between multiple tools.
- **Ecosystem connectivity layer (A2A Network):** The A2A protocol is embedded into the device onboarding process. From the moment a device comes online, it has the capability for autonomous discovery, task negotiation, and cross-device collaboration, with no additional development of collaboration logic required.

Infrastructure capabilities, including device onboarding, connection management, and data persistence, are handled automatically by the platform as an underlying layer, so manufacturers don't need to concern themselves with these.

#### 4.2 The Infrastructure Foundation

Device Agent's core advantage lies not only in the completeness of its upper-layer features, but also in the reliability of its underlying infrastructure:

**Carrier-grade messaging engine based on EMQX**

EMQX is a widely deployed MQTT message broker in the industry, capable of supporting concurrent connections from tens of millions of devices. Device Agent uses this as the infrastructure for device connectivity, inheriting its distributed architecture, multi-active high-availability guarantees, and long track record of stable operation in demanding industries (including connected vehicles and power/energy sectors). This means device agents run on a battle-tested, large-scale, validated messaging channel from day one.

**MQTT standard protocol**

Communication between the device side and the cloud uses the MQTT standard protocol, not a proprietary protocol. For manufacturers, this means:

- No vendor lock-in risk; devices can connect to any platform that supports the MQTT standard
- Existing MQTT-based devices can be migrated to Device Agent at a low cost
- A rich open-source ecosystem and mature debugging toolchain can be reused directly

**Private deployment and data sovereignty**

Data security is a core concern for both smart hardware manufacturers and enterprise users. Device Agent supports private deployment, allowing device data to be stored entirely within the manufacturer's own or enterprise-designated infrastructure, meeting requirements for data residency and compliance auditing. For enterprise users, this means device agent inference and collaboration can happen entirely within the local network, with no sensitive business data needing to be uploaded to the public cloud. Private deployment is especially critical for scenarios targeting enterprise clients, government projects, or any use case involving sensitive data.

#### 4.3 The Real Efficiency Gains

Taken together, Device Agent's efficiency improvements operate at two levels:

**Consumer scenarios, reallocation of workload:** What previously required 3–6 months of coordinated work across embedded engineers, backend engineers, AI engineers, and frontend engineers is now handled by the platform through automatic code generation. Manufacturers only need to focus on differentiated functionality (such as drivers for specific sensors or unique business logic). A single hardware-familiar engineer can lead the entire process from device definition to runnable code.

**Enterprise scenarios, reduced integration complexity:** What previously required system integrators to connect to each vendor's proprietary API one by one, write hardcoded automation rules, and maintain middleware pipelines over long project cycles can now be handled through standardized device agent specifications and the A2A protocol. Devices from different vendors collaborate in a plug-and-play fashion. Enterprise IT departments no longer need to deeply engage with the technical details of each device vendor to achieve cross-system intelligent linkage.

**Shorter feedback cycles:** The online simulator turns software and hardware development from sequential into parallel. Product managers can validate interaction experiences before the hardware prototype is ready. This compresses iteration cycles from weeks to days, or even hours.

### V. Conclusion

The efficiency bottleneck in IoT device intelligence is, at its core, the compound result of three factors: technology stack fragmentation, high barriers to AI capability integration, and limited scenario scalability. For both consumer hardware manufacturers and enterprise device integrators, the solution does not lie in hiring more engineers or learning more technologies; it lies in how to effectively leverage AI to rapidly fulfill common industry needs.

Device Agent is built precisely on this philosophy: defining the capability boundaries of device agents through natural language; replacing repetitive coding through automated generation; enabling device agents to autonomously discover, negotiate, and complete cross-device collaboration through the A2A protocol, from single-product intelligence to system-level intelligence, from closed ecosystems to open, interoperable networks.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
