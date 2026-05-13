## The Fragmentation of AI: Cross-Runtime Agent Coordination

AI agents can already use tools. Whether through [MCP](https://www.emqx.com/en/blog/mcp-over-mqtt) servers or through skills (agent-native capabilities defined as prompts with tool access, which many practitioners now prefer for their simplicity), agents read databases, call APIs, and control devices. This layer is maturing fast.

Composing multiple agents within a single team is also a solved problem. Frameworks like CrewAI, LangGraph, and AutoGen let you define agents with different roles and wire them into pipelines. If all your agents share a codebase and a runtime, these tools work well.

But consider a smart home with AI agents: A lighting agent, a thermostat agent, a security agent, and an energy optimization agent. Each was built by a different vendor. Different codebases, different programming languages, different deployment environments, different release cycles. You want a workflow that spans all four: "when I leave home, lock the doors, turn off the lights, lower the heating." The kind of cross-agent coordination that makes the whole system more than the sum of its parts.

No framework can compose agents that don't share a runtime. No skill or MCP server handles agent-to-agent communication. The missing piece is a standard protocol that lets independently deployed agents discover each other's capabilities and coordinate work across organizational boundaries.

This is what Google's [A2A protocol](https://a2a-protocol.org/latest) addresses. 

## A2A Protocol: A Standardized Era of Agent Interoperability

A2A defines four core concepts: 

- **Agent Cards** - structured metadata describing an agent's capabilities, interfaces, and security requirements
- **Messages** - single communications between agents: a request, a reply, a clarification
- **Tasks** - stateful units of work that span one or more messages and progress through lifecycle states: submitted, working, completed
- **Artifacts** - results produced incrementally as a task progresses

The protocol standardizes how agents find each other and delegate work, regardless of who built them or where they run.

With A2A in the picture, the landscape breaks down into three categories:

|                   | **Personal Agents**   | **Multi-agent Frameworks** | **A2A**                             |
| :---------------- | :-------------------- | :------------------------- | :---------------------------------- |
| **Model**         | One agent, many tools | Many agents, one process   | Many agents, one protocol           |
| **Communication** | Human to agent        | In-process function calls  | Agent to agent (pub/sub)            |
| **Discovery**     | N/A (single agent)    | Hardcoded in orchestrator  | Dynamic Agent Cards                 |
| **Coupling**      | N/A                   | Shared runtime, same repo  | Independent processes, any language |
| **Interop**       | Proprietary           | Framework-specific         | Open protocol                       |

A2A is transport-agnostic by design. The reference implementation runs over HTTP and server-sent events. But the coordination patterns that multi-agent systems demand (discovery, presence tracking, fan-out, load-balanced dispatch) are a poor fit for point-to-point request-response. A [previous post](https://www.emqx.com/en/blog/why-mqtt-is-the-missing-infrastructure-layer-for-agentic-ai) in this series made the detailed case for why MQTT is a more natural transport for agent coordination. This post goes deeper: how agent discovery actually works over MQTT at the protocol level, what coordination patterns it enables, and how [EMQX 6.2](https://www.emqx.com/en/blog/emqx-6-2-0-release-notes) makes it production-ready.

## What an MQTT Broker Gives You for Free

Before the protocol mechanics, a quick orientation. The coordination primitives that multi-agent systems need aren't separate systems in an MQTT stack: retained messages deliver always-available state to any new subscriber (discovery), Last Will and Testament fires crash notifications without health-check polling (presence), shared subscriptions distribute work across competing consumers (load balancing), and topic-level ACLs constrain each client to paths matching its own `{org_id}/{unit_id}/{agent_id}` identity (authorization scoping). The same protocol runs on an ESP32 or in the cloud, with no gateway translation. One operational surface instead of five. [Our previous post](https://www.emqx.com/en/blog/why-mqtt-is-the-missing-infrastructure-layer-for-agentic-ai) makes the full case; the rest of this one assumes it and goes a layer deeper.

## The Protocol: How A2A Discovery Works over MQTT

The [A2A-over-MQTT specification](https://github.com/emqx/mqtt-for-ai/tree/main/a2a-over-mqtt) defines how agents discover, communicate, and coordinate through an MQTT broker. It's an open spec, hosted on GitHub, designed to work with any MQTT v5 broker.

### Topic Namespace

All A2A communication lives under the `$a2a/v1/` prefix, organized into four namespaces:

![image.png](https://assets.emqx.com/images/4d25bdc06bc3d1c890d874679772a111.png)

The hierarchy is multi-tenant by design: organization, unit, agent. Wildcard discovery follows naturally:

- `$a2a/v1/discovery/{org_id}/+/+` finds every agent in an organization
- `$a2a/v1/discovery/+/+/+` finds every agent on the broker

The `{reply_suffix}` segment on the reply topic is a requester-generated token with high collision resistance, so concurrent in-flight requests don't overlap reply streams.

### Agent Cards

An Agent Card is a JSON document that describes what an agent can do and how to talk to it. Published as a retained message on the discovery topic, it's the agent's "business card" on the network:

```json
{
  "name": "energy-optimizer",
  "description": "Optimizes energy usage across connected devices",
  "version": "1.0",
  "defaultInputModes": ["application/json"],
  "defaultOutputModes": ["application/json"],
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "optimize-schedule",
      "name": "Optimize Energy Schedule",
      "description": "Generates an optimal schedule based on tariffs and occupancy",
      "tags": ["energy", "optimization"]
    }
  ],
  "supportedInterfaces": [
    {
      "url": "mqtt://broker.emqx.io:8883",
      "protocolBinding": "a2a-over-mqtt/0.1",
      "protocolVersion": "0.1"
    }
  ],
  "securitySchemes": {
    "oauth2": {
      "oauth2SecurityScheme": {
        "flows": {
          "clientCredentials": {
            "tokenUrl": "https://auth.example.com/token",
            "scopes": { "energy:read": "Read data", "energy:control": "Control devices" }
          }
        }
      }
    }
  }
}
```

The example omits optional fields for brevity; the [A2A JSON Schema](https://a2a-protocol.org/latest/definitions/#json) defines the full `AgentCard` structure.

Because cards are retained messages, a new subscriber doesn't need to wait for agents to re-announce themselves. Subscribe to the discovery wildcard and the broker delivers every existing card immediately. When an agent updates its capabilities, it publishes a new card; subscribers receive the update as a normal message.

Agents can also be discovered via HTTP `/.well-known/agent-card.json` for interoperability with standard A2A clients. When both transports are available, clients pick MQTT from `supportedInterfaces`.

### Request/Reply Flow

Here's what a complete interaction looks like on the wire:

1. **Discover.** The requester subscribes to `$a2a/v1/discovery/{org_id}/+/+` and receives retained Agent Cards for all available agents.
2. **Subscribe to replies.** The requester subscribes to its own reply topic: `$a2a/v1/reply/{org_id}/{unit_id}/{agent_id}/{reply_suffix}`.
3. **Publish request.** The requester publishes to the target agent's request topic, including:
   - MQTT v5 **Response Topic**, pointing to the requester's reply topic
   - MQTT v5 **Correlation Data**, a unique identifier for this specific request
   - Payload containing the A2A JSON-RPC request with `Task.id`
4. **Broker routes.** The broker delivers the message to the agent subscribed on the request topic.
5. **Agent replies.** The agent processes the task and publishes the result to the Response Topic, copying back the Correlation Data and including the task status in the payload.
6. **Broker delivers.** The requester receives the reply on its subscription, matched by Correlation Data.

The entire flow uses standard MQTT v5 features. Response Topic and Correlation Data were added to the spec precisely for request-response patterns. QoS 1 (at-least-once delivery) is recommended. No custom headers, no protocol hacks.

![image.png](https://assets.emqx.com/images/d500a2092a6de5c2814b5a555b959be3.png)

## What Discovery Enables

Discovery isn't the end goal. It's the foundation that makes real coordination possible. Once agents can find each other and establish communication channels, several powerful patterns emerge, all built on the same MQTT primitives.

### Streaming Task Updates

Not every task completes in a single response. A research agent compiling a report, an analytics agent processing a large dataset, a planning agent evaluating options. These take time.

A2A over MQTT handles this naturally. The agent streams back multiple replies on the requester's Response Topic, all sharing the same Correlation Data. Each reply carries a task status: `submitted` → `working` (with partial artifacts) → `completed`. The requester stays subscribed until it receives a terminal state: `completed`, `failed`, `canceled`, or `rejected`. Artifacts arrive incrementally as the agent produces them.

This is discrete event streaming, not a held-open connection. Each status update is a separate MQTT PUBLISH. If the requester disconnects briefly and reconnects, QoS 1 ensures pending updates are delivered.

### Agent Pools and Load Balancing

When you need multiple instances of the same agent (say, ten instances of a translation agent handling concurrent requests), pool topics and shared subscriptions provide load balancing without external infrastructure.

Agents subscribe to a pool topic using MQTT shared subscriptions: `$share/{group}/$a2a/v1/request/{org_id}/{unit_id}/pool/translators`. The broker picks one subscriber per message and delivers the request to that instance only.

The selected agent includes its specific identity in the reply via the `a2a-responder-agent-id` MQTT v5 User Property. The requester now knows exactly which instance handled the request and routes follow-up messages directly to that agent's individual request topic, maintaining session affinity without sticky sessions or cookies.

Scaling is adding subscribers. An agent instance spins up, subscribes to the shared group, and starts receiving requests. No load balancer reconfiguration, no routing table updates.

### Presence and Liveness

LWT gives you crash detection for free (as covered above), but the A2A-over-MQTT spec builds a richer presence model on top. When an agent publishes its card, it attaches `a2a-status=online` as an MQTT v5 User Property. Its LWT carries the same card with `a2a-status=offline`. The spec also defines `a2a-status-source` to distinguish three cases:

- `agent`: graceful shutdown, the agent published the status itself
- `lwt`: unexpected disconnect, the broker fired the will
- `broker`: status managed by the broker (used by the EMQX A2A Registry)

This distinction matters. A supervisor that sees `lwt` knows to respawn the agent. A dashboard that sees `agent` knows the shutdown was intentional and doesn't page anyone.

### Task Handover

Sometimes the right agent to start a task isn't the right agent to finish it. A generalist front-desk agent receives a request, evaluates it, and decides a specialist is better suited. It replies with `a2a-responder-agent-id` pointing to the specialist agent. The requester re-routes follow-up messages directly to the specialist's request topic.

The Task ID persists across the handover. From the requester's perspective, it's a seamless continuation. The front-desk agent never needs to proxy traffic or remain in the data path. This pattern is natural for hierarchical agent architectures where a triage agent routes work to domain specialists.

### Multi-Turn Conversations

A single exchange isn't always enough. A2A defines two multi-turn shapes, and both work cleanly over MQTT.

**Interrupted task: same Task ID.** A booking agent may need clarification: "What dates? Economy or business?" It replies with `input-required` status instead of `completed`, pausing the task pending more input. The requester sends the answer on the same request topic, reusing the **same Task ID**; the agent resumes where it left off. Correlation Data is fresh on each publish (it's per-exchange), but Task ID is stable for the life of the task.

**Multi-step session: different Task IDs, shared Context ID.** A workflow of distinct tasks ("book the flight, then reserve the hotel") can be grouped into one conversation via **Context ID**. Each task has its own UUIDv4 Task ID; all of them share one UUIDv4 Context ID so the agent can maintain state (conversation history, LLM context) across the whole session.

Context ID is optional by design. Simple request-reply interactions don't need it. Interrupted tasks and multi-step sessions, that's where it earns its place.

## From Spec to Production: The A2A Registry in EMQX 6.2

Everything above works on any MQTT v5 broker, the spec is deliberately broker-neutral. But running discovery at scale exposes two protocol-adjacent questions the spec doesn't answer. The [A2A Agent Registry](https://www.emqx.com/en/blog/emqx-6-2-0-release-notes) in EMQX 6.2 addresses both; a [previous post](https://www.emqx.com/en/blog/how-mqtt-turns-iot-fleets-into-selfcoordinating-systems) covers its full capabilities (schema validation, broker-managed status tracking, Dashboard and CLI management).

**Multiple registration paths, one namespace.** Agents can self-register via MQTT retained publish, operators can register through the Dashboard, and automation can use the REST API. All three produce the same artifact: a retained message on `$a2a/v1/discovery/`. Subscribers see no difference, so you can bootstrap manually in development and switch to self-registration in production without touching the discovery logic.

**Rate and size limits on registration.** When hundreds of agents reconnect after a broker restart or network partition, the discovery namespace can flood with registration publishes. Configurable rate limits and card-size caps absorb these bursts without degrading the broker.

## What Comes Next

The stack for AI agent coordination is crystallizing. Skills and MCP give agents hands: the ability to use tools and access data. A2A gives agents identity (discoverable presence on a network) and voice (a structured protocol for delegating and coordinating work). The MQTT broker is the coordination fabric that connects them, absorbing the infrastructure for discovery, presence, load balancing, and authorization that would otherwise be separate systems to build and operate.

If you want to build on this:

- The [A2A-over-MQTT specification](https://github.com/emqx/mqtt-for-ai/tree/main/a2a-over-mqtt) is open source. [Skitter](https://github.com/id/skitter) is a reference implementation you can clone and run today.
- [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) offers a forever-free tier with a production-grade MQTT broker in seconds, enough to run a multi-agent system without managing infrastructure.
- For the full architectural argument behind MQTT as the agent coordination layer, see the [first post](https://www.emqx.com/en/blog/why-mqtt-is-the-missing-infrastructure-layer-for-agentic-ai) in this series. For how this applies to per-device IoT agents, see [the second](https://www.emqx.com/en/blog/how-mqtt-turns-iot-fleets-into-selfcoordinating-systems).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
