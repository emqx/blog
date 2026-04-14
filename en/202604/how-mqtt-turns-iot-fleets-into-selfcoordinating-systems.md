What if every device in your fleet had its own AI agent? One that could reason about the device's state, coordinate with neighboring agents, and escalate issues through a multi-step workflow without a central orchestrator bottleneck.

A [previous post](https://www.emqx.com/en/blog/why-mqtt-is-the-missing-infrastructure-layer-for-agentic-ai) made the case that MQTT's pub/sub primitives (retained messages, Last Will and Testament, request-response correlation, shared subscriptions) map structurally to what AI agent coordination demands. This post takes that argument to its logical conclusion for IoT: an architecture where lightweight AI agents run alongside devices, discover each other through the broker, and compose into multi-step workflows that no central orchestrator needs to manage.

## The Device Management Problem AI Agents Should Solve

Today's IoT device management stacks are fundamentally reactive. A device publishes telemetry. A rules engine evaluates thresholds. If a condition matches, an alert fires and a human investigates. The intelligence lives in static rules written months ago by someone who may no longer be on the team.

AI agents can do better. An agent that understands a specific device (its normal operating patterns, its maintenance history, its relationship to adjacent devices in the system) can reason about anomalies in context. It can distinguish between a sensor drift that needs recalibration and a compressor vibration pattern that signals imminent failure. It can draft a maintenance work order, check parts availability, and coordinate with agents managing neighboring equipment to schedule downtime with minimal production impact.

The bottleneck isn't the AI reasoning. It's the coordination layer. How do hundreds of per-device agents discover each other, delegate tasks, pass intermediate results, and recover when something crashes mid-workflow? This is the problem MQTT was built to solve, and with the **A2A Agent Registry** shipping in [EMQX 6.2](https://www.emqx.com/en/blog/emqx-6-2-0-release-notes), the broker now has the native capabilities to manage the full agent lifecycle.

## Why One Agent per Device?

The instinct in most AI architectures is to centralize: one powerful agent that manages all devices, or a small cluster of agents divided by function (monitoring agent, maintenance agent, reporting agent). But MQTT's topology suggests a different approach, one that mirrors how IoT systems already work.

Every device already publishes to its own topic namespace. Every device already has its own connection lifecycle on the broker. MQTT's retained messages already give each device a persistent identity. Assigning an AI agent to each device (or device group) simply extends this existing per-device architecture with a reasoning layer.

The benefits are structural. A per-device agent maintains context about its specific device across interactions: its baseline performance, its maintenance history, and the operational patterns that are normal for *this* unit rather than generic thresholds. When that agent detects something unusual, it publishes a structured request to a diagnostics workflow, passing along the device context that a centralized agent would need to reconstruct from scratch.

This also maps naturally to scaling. Adding a new device to the fleet means deploying one more lightweight agent that subscribes to the device's topics and publishes an Agent Card. No central agent needs to be reconfigured. No routing tables need updating. The broker handles discovery and routing.

And when a device agent crashes? The broker's Last Will and Testament mechanism publishes a death notification automatically. A supervisor agent receives it, respawns the device agent, and the new instance picks up the device's last known state from retained messages. No external health-check system required.

## The Architecture: Broker as Coordination Fabric

The core architectural insight is that the MQTT broker already provides the primitives that agent orchestration systems typically build from scratch. Instead of reimplementing routing, discovery, state persistence, and crash detection in application code, you push those concerns into the broker and keep the agents simple.

The architecture has three layers:

- **Device-level agents.** Lightweight AI agents, one per device or device group, that subscribe to the device's telemetry topics and maintain context about its operational state. These agents understand their device deeply but have a narrow scope. They publish their capabilities as retained Agent Cards on discovery topics so other agents can find them.
- **A stateless supervisor.** A thin coordination layer that listens for incoming requests, creates workflow sessions, and spawns the agents needed to execute them. It makes no AI calls itself. It holds no state in memory; all session state lives in retained MQTT messages on the broker, which means the supervisor can restart at any time without losing track of running workflows.
- **The MQTT broker (EMQX).** The actual coordination engine. EMQX handles routing between agents, persists workflow state as retained messages, detects agent crashes via Last Will and Testament, provides discovery through Agent Cards, and, with the A2A Registry in 6.2, validates registrations, tracks agent liveness, and enforces scoped authorization. The broker isn't just a message bus; it's the runtime that makes the whole system fault-tolerant and observable.

![image.png](https://assets.emqx.com/images/b809db43d619fcbc3e1849b63c2f5ab4.png)

The supervisor is invisible infrastructure. It intercepts requests via a wildcard subscription and spawns the right agents, but the requesting agent addresses its target directly and receives results directly. The supervisor is never in the data path for results.

## Self-Coordinating Workflows

The most powerful aspect of this architecture is how agents compose into multi-step workflows without a central dispatcher managing every handoff.

Consider a predictive maintenance scenario. An HVAC unit's agent detects an abnormal vibration pattern. Rather than alerting a human and waiting, it triggers a workflow:

1. **The device agent** publishes a diagnostic request with the anomaly data and device context.
2. **A diagnostics agent** receives the request, analyzes the vibration signature against known failure modes, and publishes its assessment.
3. **A maintenance planning agent**, which depends on the diagnostics result, picks up the assessment from the broker (as a retained message), checks parts inventory and technician schedules, and publishes a recommended action.
4. **A fleet coordination agent**, which depends on the maintenance plan, evaluates the impact on neighboring equipment and production schedules, then publishes the final work order.

Each agent in this chain is independent. The supervisor created the workflow session and spawned all agents upfront, but after that, the agents coordinate among themselves. Agents with no dependencies start immediately. Agents that depend on upstream results subscribe to the relevant result topics on the broker and wait. Because results are retained messages, the ordering doesn't matter. An agent that starts before its dependency completes simply waits; one that starts after picks up the result instantly.

This is the self-coordination pattern that retained messages make possible. The broker holds the workflow state. The agents read what they need, do their work, and publish their results. No central dispatcher polls for completion. No shared database accumulates state. The agents and the broker are the entire system.

## Broker-Native Agent Discovery: The EMQX A2A Registry

Running per-device agents at fleet scale requires more than a topic convention for Agent Cards. You need:

- **Schema validation**, so malformed registrations don't pollute the discovery namespace. 
- **Liveness tracking**, so other agents know who's actually online. 
- **Administrative visibility**, so operators can inspect and manage the agent fleet. 
- **Scoped authorization**, so agents in one business unit can't reach agents in another.

The [A2A Agent Registry](https://github.com/emqx/eip/blob/0033-agent-reg/active/0033-agent-registry.md), shipping in EMQX 6.2, builds all of this directly into the broker. Agents still self-register by publishing retained Agent Cards to `$a2a/v1/discovery/{org}/{unit}/{agent_id}`, the same topic scheme used throughout this architecture, but the broker now validates, indexes, and manages those registrations as a first-class concern.

What this adds to the coordination fabric:

- **Schema validation on registration.** Agent Cards are validated against a JSON schema before the broker accepts them. In a fleet of device agents that register autonomously, this is the difference between a reliable discovery namespace and one that degrades over time.
- **Broker-managed status tracking.** EMQX tracks each agent's connection state and attaches liveness metadata via MQTT v5 User Properties. Other agents and dashboards can see not just what agents *exist* but which ones are currently *online*, without building a separate health-check system.
- **Administrative visibility.** The Registry exposes CLI commands and a Dashboard interface for listing, inspecting, and managing agent registrations. In a fleet of hundreds of device agents, being able to search by organization, unit, or capability, and see the full Agent Card with security metadata, is the difference between a manageable system and an opaque one.
- **Scoped authorization.** ACL-protected registry topics and optional A2A authorization policies let you scope agent interactions by organization or business unit. A device agent in Building A can discover and communicate with agents in its own unit without seeing (or being able to reach) agents in Building B.

The trajectory here is worth noting. EMQX started as a message broker. Then it absorbed service discovery. Now it's absorbing agent lifecycle management. Each layer that moves into the broker is one less system to deploy, monitor, and debug. The question is how far this integration goes. The answer is probably further than most people expect.

## From Tool Access to Workflow Orchestration

EMQX has been building the foundation for AI agents on MQTT across multiple releases. The [MCP Bridge Plugin](https://docs.emqx.com/en/emqx/latest/emqx-ai/mcp-bridge/overview.html) lets AI agents invoke tools on IoT devices through the broker. [MCP over MQTT](https://www.emqx.com/en/blog/mcp-over-mqtt) extends this with service discovery and load balancing. The [A2A-over-MQTT specification](https://github.com/emqx/mqtt-for-ai/tree/main/a2a-over-mqtt) defines how agents discover each other and delegate tasks. And the A2A Agent Registry in EMQX 6.2 makes agent discovery a managed, validated, broker-native capability.

The agent-per-device architecture described in this post builds the next layer: workflow orchestration. MCP gives agents "hands": the ability to interact with physical devices. The A2A Registry gives agents "identity": validated, discoverable presence on the broker. What's been missing is the "brain," the coordination logic that composes these interactions into multi-step workflows with dependencies, fan-out, fan-in joins, and fault recovery.

Today, that orchestration layer lives in application code. Projects like [Skitter](https://github.com/id/skitter), an open-source Python framework that implements the self-coordinating workflow pattern described in this post over the A2A-over-MQTT topic scheme, demonstrate that it works with standard MQTT v5 primitives on an EMQX broker. But the architectural direction is clear: as each coordination concern moves from application code into the broker platform, the system gets simpler to operate and harder to break. Discovery moved into the broker with the A2A Registry. Workflow orchestration is the natural next candidate.

When you combine all these layers over a single MQTT broker, you get a system where a device agent can detect an anomaly (telemetry over MQTT), invoke diagnostic tools on the device (MCP over MQTT), request analysis from a specialist agent (A2A over MQTT), and trigger a multi-step maintenance workflow (orchestration over MQTT). All through the same protocol, the same broker, and the same security model. One operational surface area, and increasingly, one platform.

## The Bigger Picture

The IoT industry spent years building infrastructure for devices to report data upward. The AI agent era inverts that flow: intelligence moves to the edge, agents reason locally, and coordination happens laterally between peers rather than through a central command-and-control layer.

The infrastructure that connects your devices today is the same infrastructure that will coordinate the agents managing them tomorrow. The platform is already there. The patterns are proven. What remains is making it turnkey.
