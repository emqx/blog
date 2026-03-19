Inside a modern smart factory, production floors are buzzing with activity as hundreds of **AI agents** work in concert:

- **Quality Inspection agents** leverage computer vision to analyze thousands of parts per hour.
- **Predictive Maintenance agents** monitor equipment health via machine learning.
- **Production Scheduling agents** optimize workflows in real-time.
- **Inventory Management agents** synchronize the supply chain.

![image.png](https://assets.emqx.com/images/b3cc523e570285a959100041535d490e.png)

These agents do not operate in silos. They must discover one another, coordinate complex workflows, handle long-running tasks spanning hours, and maintain security across distributed networks. This is the reality of **Physical AI**: where artificial intelligence intersects with the physical world through IoT devices, edge computing, and autonomous systems. As organizations deploy more specialized agents, the challenge shifts from building a single agent to **orchestrating an entire agent network**.

The **Agent-to-Agent (A2A) protocol** has emerged as the standard for this coordination, yet significant hurdles remain when deploying at scale in production-grade IoT environments.

## Understanding the A2A Protocol: Foundation for Agent Communication

The A2A protocol provides a standardized framework for agents to communicate, discover capabilities, and collaborate on tasks. It defines several core concepts to enable structured interactions:

- **Agent Cards:** Digital identity documents describing an agent's capabilities, endpoints, authentication requirements, and skills.
- **Messages:** Single-turn communications carrying content via **Parts**, flexible containers for text, files, or structured data.
- **Tasks:** Stateful units of work with unique IDs and defined lifecycles, allowing agents to track progress across multi-step, long-running workflows.
- **Artifacts:** Tangible outputs produced during a task, such as documents, images, or datasets.

![image.png](https://assets.emqx.com/images/98db32a9edb24f14d4131c60ff4c2598.png)

Without standardization, connecting N agents requires N² integrations, complexity that grows exponentially. A2A eliminates this by providing consistent communication patterns across different frameworks and vendors. It supports **dynamic discovery** based on capabilities rather than hard-coded addresses, handles both **instant messaging** and **long-running tasks**, and includes built-in mechanisms for progress tracking and artifact delivery.

These capabilities are critical in **Physical AI** and **IoT** scenarios. In smart manufacturing, for instance, a quality inspection agent must discover available analysis agents, delegate image processing tasks, wait minutes or hours for results, and aggregate findings into reports. While A2A offers a standardized mechanism for these interactions, the implementation details are vital for production.

Currently, most A2A implementations use **HTTP** for transport and **JSON-RPC 2.0** for messaging. While this approach is simple and compatible with web infrastructure — using RESTful APIs for communication and **Server-Sent Events (SSE)** for long-running tasks — it hits significant performance limits when scaled in production-grade IoT environments.

## Challenges in Production-Grade A2A Deployment

Transitioning from a PoC to a production agent network reveals critical limitations in standard HTTP-based implementations:

1. **Inefficient Agent Discovery**

   In a factory with hundreds of agents, manual configuration or centralized registries become operational bottlenecks. In IoT, agents frequently go offline due to network instability; stale registries lead to connection failures and degraded reliability.

2. **Orchestration Complexity**

   Coordinating workflows involving ten or more agents requires managing dependencies and handling partial failures. HTTP’s synchronous nature creates bottlenecks when agents must wait for long-running operations, forcing developers to build brittle, custom "event-driven" workarounds.

3. **Long-Running Task Management**

   Analyzing 10,000 parts can take hours. Standard HTTP relies on polling or Server-Sent Events (SSE). Polling wastes bandwidth, while SSE is notoriously unstable in intermittent IoT environments.

4. **Granular Access Control**

   Each agent must establish trust and verify identities. In IoT, this is complicated by network segmentation and compliance requirements. Most A2A setups lack the integrated, fine-grained authorization needed for enterprise security.

5. **Lack of Observability**

   Debugging a "black box" of agent interactions is nearly impossible without comprehensive metrics. Most implementations offer limited visibility, making proactive management a struggle.

These challenges point to a fundamental limitation: HTTP-based A2A implementations treat agent communication as a series of point-to-point interactions rather than as an event-driven system. IoT architectures naturally align with event-driven patterns where agents publish and subscribe to topics, enabling loose coupling and horizontal scalability. The question becomes: can we leverage these patterns while maintaining A2A protocol compatibility?

## The EMQX A2A Solution: Event-Driven Architecture for Production

EMQX reimagines A2A communication through an **event-driven architecture** based on **MQTT**, the de facto standard for IoT messaging. Instead of treating A2A as a series of rigid HTTP requests, EMQX implements the protocol over a Pub/Sub model.

![image.png](https://assets.emqx.com/images/5fd6850c130841646c6a8b3dad9af025.png)

### Registry Service

The A2A Registry Service is the core component for managing agent lifecycles. Agents register by publishing their **Agent Cards** as **Retained Messages** to standardized discovery topics (e.g., `$a2a/v1/discovery/{org-id}/{agent-id}`). The service validates these cards against A2A schemas and maintains an in-memory index for rapid querying. This design eliminates the need for external databases while meeting production-level performance and reliability requirements.

When an agent needs to discover others, it simply subscribes to the relevant discovery topic pattern. The MQTT broker immediately delivers all matching retained Agent Cards, enabling **instant discovery** without additional queries. This Pub/Sub model scales efficiently, handling thousands of agents without increasing discovery latency.

Agent interactions follow a similar event-driven pattern. Requests flow through MQTT topics (e.g., `$a2a/v1/{org-id}/{namespace}/{agent-id}/requests`), with responses routed back via correlation topics. **MQTT 5.0 properties** ensure request-response correlation and **QoS levels** guarantee reliable delivery. For long-running tasks, agents publish updates to status topics, allowing clients to track progress without polling.

### Dashboard Console

The system extends beyond pure MQTT to provide comprehensive management capabilities. A dashboard offers web-based administration with a built-in **Generic Client Agent** that allows developers and operators to interact with any registered agent through a simple interface. This tool eliminates the need for custom test clients, enabling quick validation of agent functionality, debugging of interactions, and demonstration of capabilities. The dashboard also provides agent card viewing, metrics visualization, and system configuration management.

### HTTP JSON-RPC Gateway

For programmatic access, EMQX exposes a **RESTful HTTP API** that provides standard A2A SDK compatibility. This dual-approach — MQTT for agent communication and HTTP for standard tooling — gives organizations flexibility while maintaining protocol compliance. The HTTP API supports querying, searching, and filtering agents, making it easy for standard A2A SDKs to integrate with the EMQX platform.

### CLI Tools

Command-line tools round out the management interface, providing scriptable operations for automation, CI/CD integration, and batch management. These tools enable infrastructure-as-code approaches and support the operational needs of large-scale deployments.

### Metrics

Metrics and observability capabilities provide the visibility needed for production operations. The system tracks agent-level metrics including request counts, durations, input/output bytes, and task statistics. System-level metrics cover registry operations, query performance, and overall health. These metrics export in standard formats including Prometheus, StatsD, and OpenTelemetry, enabling integration with existing monitoring infrastructure. The dashboard provides built-in visualization, while Grafana integration supports advanced analytics and alerting.

### A2A MQTT SDK

The EMQX A2A solution provides several capabilities that distinguish it from standard implementations, each addressing specific production requirements.

The platform's SDK abstracts transport complexity, allowing developers to write agent code once and deploy it across MQTT, HTTP, or WebSocket. It automatically handles connection management, retries, and error recovery, crucial for volatile IoT networks.

### Security

Authentication and authorization are handled through multi-layered mechanisms. Agent Cards can include **public keys or JWKS** for message signing. The platform enforces organization-level isolation via namespaces, agent-level permissions via ACLs, and capability-based access control, ensuring compliance with standards like **ISO 42001**.

## Conclusion: Making Agent Networks Production-Ready

The shift from isolated AI to collaborative agent networks marks a fundamental change in industrial intelligence. While the A2A protocol provides the language, production environments require a robust dialect capable of scaling.

EMQX’s event-driven A2A implementation aligns the intelligence layer with the underlying IoT infrastructure. By reducing operational friction and providing deep observability, it allows organizations to scale from dozens to thousands of agents without exponential complexity.

For organizations building Physical AI systems, these capabilities translate to faster time-to-market, lower operational costs, and greater system reliability. 

The future of intelligent systems lies in networks of specialized agents working together. EMQX provides the foundation to make this future production-ready today.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
