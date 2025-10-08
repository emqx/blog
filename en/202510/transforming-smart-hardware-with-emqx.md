## Introduction: A New Era for Smart Hardware Interaction

As AI advances, smart hardware is no longer just a tool. It's becoming an intelligent agent that can **perceive, understand, interact, and act,** fundamentally changing several industries.

- **Emotional companionship:** Toys are now intelligent partners with emotional recognition and personalized interaction.
- **Smart homes:** Individual smart devices are evolving into integrated home ecosystems that respond to natural language.
- **Robotics:** Embodied intelligent robots, including service and industrial robots, can now perceive their surroundings and respond to human intent.
- **Automotive:** Smart cars are mobile intelligent spaces, with AI assistants providing safe, convenient voice control for complex driving scenarios.

By becoming more personalized and integrated, smart hardware is creating a more natural and intelligent way for us to interact with technology.

## Challenges: The Core Difficulties in Building Smart Hardware

However, building truly intelligent hardware devices faces numerous technical challenges:

- **Real-time Performance:** High response latency directly impacts the user experience. Delays in audio, video, or sensor data can disrupt the natural flow of interaction, making the device seem slow and affecting the user's perception of its intelligence.
- **Semantic Understanding:** Devices need to accurately understand the user's natural language and maintain contextual memory. A lack of effective semantic understanding leads to misinterpreting user intent, severely impacting the user experience.
- **System Integration:** Coordinating the complex interactions between hardware, middleware, and AI models requires handling various protocol conversions, data format unification, and system compatibility issues, which greatly increases development difficulty.
- **Reliability:** Device control failures can quickly erode user trust. Establishing reliable control channels and secure execution mechanisms is essential to ensure accurate and prompt command execution.
- **Scalability:** As the device ecosystem expands, it needs to support large-scale concurrent connections while maintaining low latency and high availability.

In the following sections, we will delve into how the EMQX technology stack addresses these core challenges and build a smart hardware system with the ability to perceive, understand, interact, and act.

## The Six Pillars of Building Smart Hardware

As shown in the figure below, we define the necessary components for building qualified smart hardware from six perspectives, divided into input and output capabilities.

**Input Capabilities:**

- **Perceptible:** Perceive the physical world through environment, location, motion sensors, and beyond. 
- **Audible:** Hear and understand natural language with noise suppression and multi-language recognition. 
- **Visible:** See and recognize environments through image detection, facial recognition, and gesture recognition. 

**Output Capabilities:**

- **Understandable:** Integrate LLM/VLM models to achieve semantic understanding and emotional recognition. 
- **Speakable:** Output high-quality speech through speakers, supporting multi-timbre synthesis and emotional expression. 
- **Actionable:** Control device functions through MCP, executing user semantic commands and taking corresponding actions. 

![image.png](https://assets.emqx.com/images/3d9a8eedd9fe13dc1507984b10cf17e5.png)

### Perceptible: Sensor Data Processing

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol that has become the standard for IoT communication, especially for transmitting real-time sensor data. Its advantages over traditional HTTP make it the ideal choice for resource-constrained devices.

- **Efficient Connectivity:** MQTT's persistent connections allow devices to communicate continuously with a server, saving power and ensuring data is reported in real-time. It also automatically reconnects, making the connection more reliable.
- **High Performance:** MQTT supports millisecond-level message delivery and offers different Quality of Service (QoS) levels to prioritize data. Its low-power design is perfect for battery-powered sensors, while its built-in heartbeat mechanism maintains connections with minimal energy use.
- **Scalability:** [EMQX MQTT platform](https://www.emqx.com/en/platform) can handle millions of simultaneous connections, which allows it to support large-scale IoT deployments.

Acting as the "nerve endings" for smart hardware, sensors use MQTT to transmit crucial information like environmental data(temperature, humidity, light, sound, etc.), user interactions(touch, gestures, location, etc.), device status(battery level, operating conditions, fault information), and security alerts(intrusion detection, abnormal behavior recognition). This real-time, accurate data is the foundation for intelligent systems to make correct decisions and responses, and MQTT ensures it gets to the right place quickly and efficiently.

### Audible, Visible, Speakable: Audio and Video Stream Data Processing

**WebRTC Protocol: The Standard for Real-Time Audio and Video Communication**

WebRTC (Web Real-Time Communication) is an open standard protocol for real-time audio and video, now a core technology for multimedia applications. Its benefits in low latency and cross-platform compatibility make it ideal for the multimodal interaction needs of smart hardware.

Our media server, powered by EMQX, supports flexible audio and video streaming. It provides simple configuration interfaces for ASR (Automatic Speech Recognition) and TTS (Text-to-Speech) and standard APIs for interaction. This allows developers to quickly add voice and video capabilities. The solution also supports integrating third-party WebRTC services, giving users the flexibility to choose and customize based on their business needs. 

**Audio and Video Stream Processing Based on WebRTC** 

In intelligent interaction, voice and visual input and output form the core of the system's ability to communicate with users:

- **"Audible" - Voice Input:** High-quality microphones capture sound with support for multiple sampling rates and bit depths, while intelligent noise reduction keeps voices clear, even in noisy environments. Real-time ASR quickly converts speech to text, supporting multiple languages like Chinese and English, so the device can instantly understand commands. 
- **"Visible" - Visual Input:** The camera provides high-definition video stream capture, supporting various resolutions and frame rates to ensure detailed image presentation. Using image recognition and object detection, the system can identify objects and track specific targets. Gesture recognition also allows for non-contact interaction through natural movements, making it more flexible and convenient. 
- **"Speakable" - Voice Output:** TTS technology synthesizes high-quality, natural-sounding speech. It can adjust tone and emotion based on context, making the voice more lifelike. The system also intelligently adjusts speech rate and pauses, creating a more realistic and engaging conversation. 

By combining these three abilities, smart hardware can truly understand and interact with users, creating an immersive, multimodal experience. For implementation, you can use cloud-based ASR and TTS services provided by public cloud vendors or a private, open-source setup. Remember, the quality of voice capture also depends on the device's hardware.

**The Value of WebRTC** 

Audio and video stream data are the key media for smart hardware to achieve natural interaction. Using WebRTC, devices can communicate with you in the most human-like way possible.

With voice tone and facial expressions, they can understand your emotions. Through visual data, they can recognize your surroundings and behaviors. Your unique voice and facial features can even be used to create personalized experiences.

This real-time, high-quality data is the key to truly intelligent interaction, and the WebRTC protocol ensures it is transmitted and processed with minimal delay and maximum quality.

### Understandable: Accessing LLM / VLM

**LLM/VLM Technology: The "Brain" of Smart Hardware** 

LLM (Large Language Model) and VLM (Vision Language Model) are the brains of smart hardware, responsible for understanding user intent, processing multimodal information, and generating intelligent responses. Compared to traditional rule-based engines, LLM/VLM possess powerful semantic understanding capabilities and contextual memory functions, enabling truly intelligent human-computer interaction.

**Intelligent Understanding Based on LLM/VLM** 

In the cognition and interaction of an intelligent agent, LLM/VLM play a key role.

- **LLMs for "Thinking":** LLMs allow a system to understand language, manage multi-turn conversations, and even adopt a specific persona with emotional awareness. By combining short- and long-term memory, LLMs can maintain context, accurately understand complex commands, and follow long conversations.
- **VLMs for "Seeing and Understanding":** VLMs expand a device's perception by processing images, videos, and text simultaneously. This gives the system the ability to "see and understand." They can recognize objects, scenes, and actions, analyze emotions from facial expressions and body language, and provide smart, context-aware responses.

When it comes to implementation, you have a few options for accessing these models:

- **Public Cloud APIs:** These are great for fast integration. You don't need to manage infrastructure and can simply pay to use top models like Alibaba's Qwen, DeepSeek, and GPT.
- **Private Deployment:** This is the best choice for high data security. It ensures privacy and allows you to customize and fine-tune models to fit your specific needs.
- **Hybrid Approach:** This method balances cost, latency, and privacy. You can process sensitive data locally while offloading general tasks to the cloud, using flexible policies and load balancing to maintain efficiency and security.

**The Value of Intelligent Understanding**

Combining LLMs and VLMs allows smart devices to understand and respond like humans. They go beyond simple function by deeply comprehending both language and visual cues.

With semantic understanding and multimodal processing, smart hardware can provide personalized, context-aware interactions. This helps them build long-term emotional connections, transforming them from basic tools into true intelligent companions. 

### Actionable: MCP Device Control

**MCP Protocol: The Bridge Between AI and Devices** 

MCP (Model Context Protocol) is a standard protocol that connects AI models with external tools and services, providing a unified device control interface for smart hardware. Compared to traditional hard-coded control methods, MCP allows AI to dynamically discover and invoke device functions, achieving truly intelligent control.

**Device Control Based on MCP** 

Core Components:

- **MCP Server:** A lightweight program that provides context, tools, and prompt information, supporting access to local and remote resources (such as files, databases, APIs).
- **MCP Client:** A protocol client that runs within the host and maintains a 1:1 connection with the server.
- **MCP Hosts:** The LLM application that initiates requests, responsible for parsing user intent and invoking the corresponding tools.

Correspondence in a Smart Hardware Scenario:

- **MCP Server:** Deployed on the smart hardware device (e.g., ESP32, Raspberry Pi), responsible for registering device functions (like volume control, camera activation, expression switching), acting as a representative of the device's capabilities.
- **MCP Client:** Runs in the cloud or on an edge computing node, communicating with the MCP Server on the device via the MQTT protocol, responsible for forwarding AI commands to the specific device.
- **MCP Hosts:** Integrated into the cloud AI application or edge AI service. When a user says "turn down the volume," the LLM initiates a tool call through the MCP Hosts, which ultimately controls the device to perform the corresponding action.

![image.png](https://assets.emqx.com/images/9ccf4506e2771acacb79103d877eb81b.png)

By using EMQX's implementation of the MCP, device control becomes faster and more secure. The unified MQTT protocol ensures low latency and high reliability. Devices can automatically register their functions when they connect, allowing the AI system to dynamically discover and use them. Additionally, permission control and execution validation mechanisms prevent unauthorized or incorrect actions. The system's millisecond-level response time provides robust support for real-time interaction, ensuring a smooth and responsive user experience.

**The Value of Device Control** 

The MCP protocol gives smart hardware the "ability to act," enabling it to execute specific device operations based on user commands. Through a unified control interface, AI can coordinate multiple devices to work together, realizing complex intelligent scenarios and providing users with a seamless smart experience.

## EMQX End-to-End Solution for Smart Hardware

### **Architecture**

The EMQX end-to-end solution is a layered architecture that integrates the six key components of smart hardware into one complete system. As the diagram shows, the architecture is divided into four layers: the device layer, communication layer, processing layer, and application layer.

Using a unified technology stack of MQTT, WebRTC, and AI, this solution creates a closed loop, allowing the system to seamlessly move from perception to action.

![image.png](https://assets.emqx.com/images/58b9447caf9c0dbfc8804a654b5e0211.png)

- **Device Layer:**
  - Sensor Devices: Temperature, humidity, light, touch, etc.
  - Audio/Video Devices: Microphones, cameras, speakers.
  - Control Devices: Volume adjustment, expression display, device switches, etc.
- **Communication Layer:**
  - EMQX MQTT Broker: Provides millisecond-level message transmission and support for millions of connections.
  - WebRTC Media Server: Handles real-time audio and video stream transmission.
  - [MCP over MQTT](https://www.emqx.com/en/blog/mcp-over-mqtt): Implements intelligent control between AI and devices.
- **Processing Layer:**
  - LLM/VLM Service: Provides semantic understanding and multimodal processing capabilities.
  - ASR/TTS Service: Implements speech recognition and speech synthesis.
  - Media Processing: Noise suppression, echo cancellation, image recognition, etc.
- **Application Layer:**
  - Smart Application: The core application that integrates all functions.
  - User Interface: Provides an intuitive, interactive experience.
  - Management Console: System monitoring and configuration management.

This layered architecture creates a complete technology stack, from low-level hardware to high-level smart applications.

- The **device layer** collects data and performs actions.
- The **communication layer** ensures data is transmitted reliably and in real time.
- The **processing layer** provides intelligent understanding and decision-making.
- The **application layer** offers an intuitive interface for users.

By communicating through standardized interfaces, each layer ensures system stability and scalability while giving developers the flexibility to innovate. This design allows smart hardware to complete a full "perceive-understand-interact-act" loop, providing a natural, smooth, and intelligent user experience.

### **Technical Advantages**

- **Low Latency, Large Scale, and High Availability:**
  - Low-latency message transmission ensures a real-time interactive experience.
  - Supports millions of concurrent connections to meet large-scale deployment needs.
  - High availability guarantees service stability.
- **Standardized Architecture:**
  - Based on the standard MQTT protocol, it avoids vendor lock-in.
  - Supports multiple hardware platforms and operating systems.
  - Complies with international standards and industry norms.
- **Highly Scalable:**
  - Modular design supports flexible functional expansion.
  - Customizable speech recognition and synthesis integration solutions.
  - Custom LLM/VLM integration and Agent development.
  - Supports third-party service integration and custom development.

### **Business Value**

- **Low-Cost Deployment:**
  - Supports private LLM, ASR, and TTS integration.
  - Pay-as-you-go cloud service model.
  - Open-source components reduce development costs.
- **Security Assurance:**
  - Certified by international standards such as GDPR and SOC-2.
  - Supports private deployment to ensure data security.
  - Comprehensive permission control and access management.
- **Rapid Go-to-Market:**
  - Provides complete SDKs and development tools.
  - Rich sample code and documentation.
  - Professional technical support and consulting services.

The EMQX end-to-end solution possesses significant advantages in both its technical architecture and business value. From a technical standpoint, it provides a low-latency, highly reliable, and standardized foundation that can be scaled to fit projects of any size. For businesses, the solution offers a clear path to market with features like low-cost deployment, robust security, and rapid integration. Together, these benefits not only meet the current needs of the smart hardware market but also provide a strong foundation for future intelligent development.

## Related Products and Services

### **Core Products**

- **EMQX**
  - Enterprise-grade MQTT message broker
  - MCP over MQTT protocol support
  - High-availability cluster deployment
- **Media Server**
  - WebRTC audio and video stream processing
  - Real-time media transmission optimization
  - Multi-platform compatibility support

*Third-party media servers can also be chosen and seamlessly integrated with our solution.*

### **Development Tools**

- **MCP SDK (Open Source)**
  - ESP32 C / Paho C: For embedded device development
  - Python / TypeScript / Erlang: For server-side development
  - Complete API documentation and sample code
- **Professional Services:**
  - Technical consulting and architecture design
  - Customized development services
  - 24/7 technical support
  - Training and certification services

EMQX provides a complete product matrix, from the core message broker to media processing services, along with rich development tools and professional services, offering a one-stop technology solution for smart hardware developers. The open-source SDK lowers the development barrier, while professional services ensure the successful implementation of projects, forming a complete ecosystem from products to services.

### Third-Party Services

Integrating third-party services significantly boosts a system's capabilities and flexibility.

- **AI Services:** Developers can access a variety of speech recognition and synthesis services for natural, multi-language interactions. You can also seamlessly integrate major LLMs and VLMs for stronger language and multimodal understanding. For data security, you have the option to privately deploy the Media Server and Agent locally.
- **Infrastructure:** The foundation of smart hardware relies on computing power, bandwidth, and network resources. Cloud storage and databases manage data, while monitoring services ensure the system remains stable and available.
- **Additional Services:** You can add more services as needed. For example, using the MCP to access third-party functions like maps, weather, and music gives devices richer context. RAG (Retrieval-Augmented Generation) services allow the system to intelligently use historical data to improve long-term interactions. Security services provide data encryption and access control to protect sensitive information.

By using these third-party services, the EMQX solution can be adapted for any smart hardware project. Whether you choose fast integration with public clouds or a customized private deployment, you can find the right combination to ensure your project is secure, compliant, and scalable.

### Partners and Ecosystem

**Hardware Partners:**

- **MCU Vendors:** Mainstream hardware platforms like ESP32, Raspberry Pi, Arduino, etc.
- **Sensor Vendors:** Suppliers of sensors for temperature, humidity, light, touch, etc.
- **Audio/Video Equipment:** Multimedia devices like microphones, cameras, and speakers.

**AI Service Partners:**

- **Alibaba Cloud:** Qwen large model, speech recognition, image recognition services.
- **Volcengine:** Doubao large model, multimodal AI services.
- **Azure:** OpenAI services, Cognitive Services.

**Technology Service Providers:**

- **OTA Services:** Device firmware upgrades and remote management.
- **Cloud Service Providers:** Infrastructure services from AWS, Alibaba Cloud, Tencent Cloud, etc.
- **System Integrators:** Providing end-to-end solution implementation.

EMQX has built a complete partner ecosystem, covering the entire industry chain from hardware to software, from AI services to infrastructure. This ecosystem-based cooperation model not only provides developers with a wealth of choices but also ensures the stability and reliability of the solution, offering strong support for the rapid development of the smart hardware industry.

## Summary and Outlook

With the rapid development of artificial intelligence, smart hardware is gradually evolving from single-function devices into intelligent agents with the ability to perceive, understand, interact, and act.

Based on a unified technology stack of MQTT + WebRTC + AI, EMQX provides end-to-end integrated solutions for various industry scenarios, including smart emotional companion toys, smart homes and appliances, embodied intelligent robots, and in-vehicle conversational bots. This will not only meet current technical demands but also solidify a path for future growth, helping smart hardware become an indispensable part of everyday life.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
