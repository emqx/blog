## Introduction

With the widespread adoption of large language models (LLMs), a key challenge is identifying suitable use cases and building intelligent agents that serve various industries. The community has seen a surge in infrastructure and tools supporting AI agent development, among which Anthropic’s MCP stands out for its ability to connect LLMs with diverse data sources.

This article explores the potential and applications of MCP in driving IoT intelligence through the following questions:

- Can MCP be leveraged to enable intelligence across a vast number of devices?
- Are there any limitations when applying MCP in IoT scenarios?
- How can integration between MQTT and MCP facilitate the seamless connection of both legacy and new devices to AI ecosystems?

## Overview of MCP

MCP (Model Context Protocol) is an open standard protocol introduced by Anthropic in November 2024. It is designed to establish a standardized communication framework between LLMs and external data sources, tools, and services, addressing data silos and enhancing AI applications' interaction efficiency with multi-source information. Its core architecture and key components include:

- **MCP Hosts**: LLM applications that initiate requests (e.g., Claude Desktop, IDE tools).
- **MCP Clients**: Protocol clients running within the host, maintaining a direct one-to-one connection with the server.
- **MCP Servers**: Lightweight programs that provide context, tools, and prompts, supporting both local and remote resource access (e.g., files, databases, APIs).

**Key Advantages and Features of MCP**

- **Simplified Development**: Write once, integrate multiple times—no need to rewrite custom code for each new tool.
- **Dynamic Interaction**: Supports real-time context updates and interactions, improving response efficiency.
- **Secure and Controlled**: Built-in access control ensures LLMs can only perform authorized operations through explicitly defined interfaces.
- **Flexible Expansion**: New features can be added by deploying additional MCP Servers, enabling a modular expansion mechanism similar to plugins.

**AI Application Scenarios of MCP**

- **Intelligent IDEs**: Connects to code repositories and documentation to enable context-aware coding assistance.
- **Data Analytics**: Provides secure access to local databases, allowing SQL queries and automated report generation.
- **Workflow Integration**: Seamlessly connects with enterprise systems (e.g., CRM, ERP) to automate complex tasks.

Since its launch, MCP-related server services have grown rapidly. As of now, [MCP Server Directory](https://mcp.so/servers) lists 4,245 services, covering categories such as databases, cloud platforms, and browser automation. These services enable various MCP Client applications to easily connect with external data sources and tools, leveraging AI’s reasoning capabilities to orchestrate workflows and accelerate the development of intelligent applications.

## **The Potential of MCP in IoT Applications**

IoT devices enable the digital world to perceive the physical environment by reporting data, while also allowing control and operation of physical-world devices through exposed interfaces to meet specific user needs. Currently, most IoT systems rely on the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) for communication. The architectural design of MCP aligns closely with the **"device model"** concept in IoT, making it a promising solution for this domain. MCP not only integrates seamlessly with existing MQTT-based systems but also enhances the connection between devices and AI applications.

**Introduction to the Device Model**

A device model represents the digital twin of physical entities (such as sensors, in-vehicle devices, buildings, and factories) in the cloud. It defines an entity’s characteristics, functions, and externally available information through three key dimensions: **attributes, functions, and events**.

- **Attributes**: Real-time status data of a device. Examples include temperature and humidity readings from an environmental monitoring device or the on/off state of a smart device.
- **Functions**: Actionable commands that a device can execute. Function calls support input parameters (execution conditions) and output parameters (execution results), such as adjusting an air conditioner's temperature or controlling a motor’s start/stop function.
- **Events**: Information actively reported by a device to the cloud, including alerts and fault notifications. These events often contain multiple parameters, such as equipment failure alarms or environmental anomaly warnings.

**Capabilities Offered by MCP**

- **Resources**: Data accessible to clients, such as API responses or file contents.
- **Tools**: Functional modules that LLMs can invoke with user approval.
- **Prompts**: Predefined templates that assist users in performing specific tasks.

**MCP and IoT: A Seamless Integration for AI-driven IoT Systems**

By comparing the device model’s three dimensions with MCP’s capabilities, we can see a clear alignment:

- **Attributes and events in the device model correspond to resources in MCP**, providing LLMs with metadata and real-time status information about physical devices.
- **Functions in the device model align with tools in MCP**, allowing LLMs to access relevant data or trigger device functions upon user authorization.

This strong similarity between the device model and MCP presents a viable approach for building AI-powered IoT systems:

- **Device manufacturers** can offer MCP services for their devices or encapsulate existing device model interfaces (such as HTTP APIs) into MCP services, providing corresponding resources, tools, and prompts.
- **Smartphone apps and other terminal applications** can define or orchestrate workflows based on user needs, automatically invoking MCP services to control devices.

With MCP enabling AI-driven device interaction, end users can seamlessly communicate with IoT devices using natural language. For example, in a smart home scenario, a user could simply say to their smartphone app:

> **“I’ll be home in an hour. Set the living room temperature to 25°C and keep the humidity at 40%.”**

Before MCP, implementing such functionality required developers to manually adapt interfaces for different device models and versions.

With MCP, LLMs like DeepSeek can **intelligently understand** a device’s capabilities based on natural language descriptions, autonomously coordinate relevant MCP services, and manage device control—**without the need for manually written rules or code**. This significantly enhances **device interoperability and AI-driven automation** in IoT ecosystems.

## **Limitations of MCP in IoT Applications**

The MCP protocol currently supports two primary communication methods: **standard input/output (stdio)** and **HTTP + Server-Sent Events (SSE)**. The former is well-suited for local communication between MCP Clients and Servers, while the latter is more appropriate for remote network communication.

In an ideal IoT deployment, an **MCP Server would run on the device**, while a mobile application or other client acts as the **MCP Host**, interacting with the server via an **MCP Client** for intelligent orchestration and execution. However, several challenges arise in real-world implementations:

- **High Resource Requirements**: HTTP and SSE protocols demand significant computational and storage resources, making them unsuitable for resource-constrained IoT devices with limited power and processing capabilities.
- **Unstable Network Environments**: IoT devices are often deployed in mobile, remote, or industrial environments with unreliable connectivity, making it difficult to ensure consistent service availability.
- **MQTT Ecosystem Compatibility**: The IoT industry has already established a robust ecosystem around MQTT. Introducing SSE would require additional access control mechanisms, increasing system complexity.
- **Protocol Support Issues**: Many IoT devices **only support MQTT**. To use MCP, these devices would need additional support for HTTP, complicating implementation.
- **Scalability Challenges**: IoT deployments often involve **tens or even hundreds of thousands of devices**. The current MCP model, which relies on direct client-server connections, lacks the scalability required for managing large-scale device networks.

## **MCP over MQTT: A Proposed Solution**

To address the challenges outlined above, EMQ proposes the **MCP over MQTT** solution, aiming to enhance IoT device intelligence at the protocol level.

This approach offers differentiated support for devices with varying computational capabilities:

- **For resource-constrained devices**, two proxy-based solutions are available:
  - **External Proxy**: Deploy an **MCP Server externally** (outside EMQX) to handle IoT data over MQTT while interacting with MCP Clients via the MCP over MQTT protocol.
  - **Internal Proxy**: Implement an **MCP Server proxy within EMQX**, allowing it to manage device operations on behalf of the devices.
- **For devices with sufficient computing and storage resources**, a **native MCP Server implementation** can be developed using the **MCP over MQTT SDK**.

By replacing **HTTP + SSE** with **MQTT** at the transport layer, MCP over MQTT significantly improves communication reliability in **low-bandwidth and unstable network environments**. Additionally, EMQX, as a **message broker**, enhances scalability by providing:

- **Comprehensive service discovery** for large-scale MCP Server deployments
- **Built-in authentication and access control**, ensuring system security and stability

### **External Proxy Solution**

![image.png](https://assets.emqx.com/images/229c17c2ab27546f059d9c1d6344188c.png)

- **MCP Server (Device Proxy)**
  - Devices upload data to **EMQX** using the **MQTT** protocol. The **MCP Server** subscribes to relevant topics to obtain device information, then exposes the uploaded data using **MCP resources** or **tools**.
  - Device control messages are similarly transmitted through **MQTT** via EMQX, with tools exposed to external systems via the **MCP over MQTT** protocol.
- **App Side**
  - The app communicates with the remote **MCP Server** via **MCP over MQTT** through **EMQX** to retrieve device status and send control commands. It can also interact with other systems by using standard **MCP** protocols to communicate with additional MCP Servers.

The main advantage of this solution is that **existing IoT devices require no modification** to gain AI interaction capabilities. It fully retains the inherent benefits of **MQTT** in **low-power and low-network environments**. Combined with EMQX’s **high concurrency and high availability**, this solution enables rapid deployment of scalable, intelligent IoT applications, solving compatibility and implementation cost challenges for legacy device upgrades.

### **Internal Proxy Solution**

![image.png](https://assets.emqx.com/images/21a0020e1593bbf03ab51d917d2644dc.png)

The **Internal Proxy** solution improves upon the external proxy approach by directly integrating the **MCP Server** into **EMQX**. This integration provides several built-in tools and capabilities that enhance system performance, rather than simply reducing the number of nodes between **EMQX** and the **MCP Server**.

Additionally, since the **MCP Server** operates as an internal component of **EMQX**, it significantly reduces operational complexity, making the development and management of **MCP Server** applications more convenient and efficient.

### Native Solution

![image.png](https://assets.emqx.com/images/06f1c4318b66d1cd41e06e55e39ceccd.png)

The **Native Solution** is designed for high-performance, high-value devices (such as smart cars, 3D printers, etc.) with strong computing and storage capabilities. This approach integrates **MCP** services natively into the device, allowing direct communication with **EMQX** using the **MCP over MQTT** protocol. In this solution, the **MCP Client** interacts directly with the **MCP Server** on the device through the standardized **MCP over MQTT** protocol, enabling end-to-end intelligent control.

For example, consider two 3D printers with the following service names:

- `3D-Printer/ACH301/EECF7892AB1`
- `3D-Printer/ACH301/CAED99C2EE2`

Here, `3D-Printer/ACH301/` is the device type, and `EECF7892AB1` and `CAED99C2EE2` are the device IDs.

The client (mobile app) first checks the current user's permissions, such as determining access only to the `ACH301` model printer. It then subscribes to relevant topics to retrieve the tools (capabilities) available for the `ACH301` printer, allowing the app to intelligently interact with the device.

This new intelligent IoT platform architecture is ideal for **M2M (machine-to-machine)** scenarios. Device manufacturers can embed a fully-featured **MCP Server** (including suggested prompt templates) in the devices. Once a device is procured by the IoT platform, no custom commands need to be written for each device. Instead, unified intelligent access through a client app allows for specialized division of labor:

- Device manufacturers focus on implementing device-side functionality.
- IoT platforms focus on enhancing the user experience of intelligent clients (including voice interactions).

## **MCP over MQTT Protocol at a Glance**

### **Features**

MCP over MQTT enhances the original MCP functionality by adding the following capabilities:

- **Service Discovery**: Using MQTT's retained messages and last-will messages, **MCP Clients** can automatically discover available **MCP Servers**.
- **Linear Scalability of Servers**: Thanks to MQTT's shared subscription feature, **MCP Servers** can scale up or down linearly while maintaining stateful.
- **Centralized Authentication**: By relying on an MQTT Broker as a centralized messaging middleware, mature authentication and authorization solutions are more readily available.

In the future, integrating an **MCP Server** plugin into the MQTT Broker can further simplify **MCP Server** deployment and optimize data transmission efficiency.

### **Limitations**

The **MCP over MQTT** protocol is primarily designed for scenarios where **MCP Servers** are deployed remotely. Its architecture relies on the support of a centralized MQTT Broker. While **MCP Servers** deployed locally can also use **MCP over MQTT**, this may add complexity to the deployment process.

## **Summary and Outlook**

Currently, EMQ has completed the initial validation of the MCP over MQTT solution and built a prototype system for testing. The R&D team is now focusing on standardizing the protocol architecture and engineering implementation, with the next phase dedicated to in-depth validation and performance optimization of key technical components.

Looking ahead, this solution is set to usher in a new Agentic era for IoT. The EMQX MQTT Platform provides protocol adaptation and centralized service management, addressing data silos and fragmentation, while LLMs enable natural language understanding and reasoning to dynamically translate user intents into executable device actions. With this powerful combination, enterprises can seamlessly integrate a vast array of heterogeneous devices into an MCP-based AI ecosystem, significantly reducing the cost of upgrading legacy systems while enabling the rapid development of intelligent applications across different scenarios and systems. Powered by MCP over MQTT, IoT is evolving from simple interconnectivity to intelligent synergy, redefining the path to enterprise digital transformation.

Stay tuned for the latest technological updates and developments as we continue to explore the next generation of intelligent solutions at the intersection of IoT and AI. Contact us if you are interested!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
