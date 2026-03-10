Agentic AI isn't a research preview anymore; it's a shipping product category. OpenAI's [Codex app](https://openai.com/index/introducing-the-codex-app/) launched as a full "command center for agents," with over a million developers running parallel coding agents across projects within its first weeks. Anthropic's Claude Code now lets you [continue agent sessions from your phone](https://code.claude.com/docs/en/remote-control), because long-running autonomous tasks have become normal enough to need mobile monitoring. OpenAI acquired [OpenClaw](https://goodai.substack.com/p/openai-acquired-openclaw-why-workflow), a 50,000-user open-source framework for orchestrating agents across SaaS platforms, signaling that workflow infrastructure, not model capability, is the strategic bottleneck. [Gartner reports](https://thenewstack.io/can-the-50-year-old-actor-model-rescue-agentic-ai/) that 34% of businesses already deploy AI agents and forecasts that by 2028, 15% of daily work decisions will be made autonomously.

The agents are here. What's lagging behind is the infrastructure to coordinate them.

The protocols we've built for the web era — HTTP request-response, REST APIs, server-sent events — were designed for a world where a human clicks a button and waits for a page to load. They were never meant to coordinate a swarm of autonomous agents that need to discover each other, negotiate tasks, stream partial results, and recover gracefully when something goes wrong. As these systems scale from single-agent demos to multi-agent production deployments, we need a messaging backbone purpose-built for this kind of work, and a strong candidate is a protocol that's been powering IoT infrastructure for over a decade: MQTT.

## The Problem with HTTP-Shaped Agent Protocols



The current crop of agent coordination standards, Anthropic's Model Context Protocol (MCP) and Google's Agent-to-Agent (A2A) protocol, represent important first steps toward interoperability. MCP standardizes how AI models connect to external tools and data sources; A2A defines how agents discover and delegate tasks to one another. Both are valuable abstractions.

But both lean heavily on HTTP and server-sent events (SSE) as their primary transports, and that choice carries structural consequences:

- **Point-to-point coupling.** HTTP requires the caller to know the address of the callee. Scaling means adding load balancers, service meshes, and discovery registries on top.
- **Unidirectional streaming.** SSE gives you server-to-client streaming, but not the bidirectional, asynchronous messaging that multi-agent workflows actually demand.
- **No native fan-out.** When one event should trigger reactions from many agents, HTTP forces you to build your own pub/sub layer or bolt on a message queue as an afterthought.
- **Stateless-by-default primitives.** As [The New Stack recently explored](https://thenewstack.io/can-the-50-year-old-actor-model-rescue-agentic-ai/), serverless functions are optimized for short, stateless bursts, but agents need to hold memory and context across long-running tasks. Containers preserve state but keeping thousands of mostly-idle containers alive is operationally painful and financially unsustainable.
- **Synchronous blocking at the orchestrator.** Anthropic's multi-agent system [ran into this directly](https://www.anthropic.com/engineering/multi-agent-research-system): the lead agent waits for each batch of subagents to complete before proceeding, creating an information flow bottleneck where subagents can't coordinate with each other and the orchestrator can't steer them mid-task. This is a structural consequence of HTTP's request-response model, not a bug in their implementation.
- **Imprecise task delegation leading to duplicate work.** In Anthropic's system, vague task descriptions caused multiple subagents to independently investigate overlapping topics. Without a shared message bus where agents can observe each other's work in progress, there's no lightweight mechanism to deduplicate effort in real time.

(MCP does support pluggable transports, which is precisely why the MQTT transport discussed below is possible, but the ecosystem defaults matter.)

What's needed is an infrastructure layer that treats asynchronous, many-to-many messaging as a first-class primitive, not something you retrofit onto a request-response protocol.

![image.png](https://assets.emqx.com/images/113e5dafb97316737b624eeec45a53d2.png)

## Enter MQTT: Infrastructure That Already Understands the Problem



MQTT was designed in 1999 to solve a problem that sounds remarkably like agent coordination: getting small, resource-constrained devices to communicate reliably over unreliable networks, with minimal overhead and maximum flexibility in topology. It's a publish/subscribe protocol built around a central broker, and it has spent over two decades being battle-tested at scale in manufacturing, autonomous vehicles, robotics, and telecom.

The properties that made MQTT dominant in IoT map well to what agentic AI needs:

- **Publish/subscribe decoupling.** An agent doesn't need to know who's listening — just which topic to publish to. Producers and consumers are fully decoupled.
- **Quality of Service (QoS) levels.** Fine-grained delivery guarantees, from fire-and-forget (QoS 0) to exactly-once delivery (QoS 2).
- **Retained messages.** New agents instantly pick up the latest state when they come online. No separate state-sync mechanism needed.
- **Binary and compact.** Meaningfully less per-message overhead than HTTP+JSON for high-frequency inter-agent communication.

MQTT 5.0 added features that are particularly relevant for agent coordination:

- **Request-response correlation** — RPC-style calls over pub/sub, with correlation data for tracking.
- **User properties** — arbitrary metadata on packets without payload pollution.
- **Shared subscriptions** — distributing messages across competing consumers for load balancing.
- **Topic aliases** — reducing bandwidth on chatty connections.

But stock MQTT 5.0 isn't quite enough for the full range of agent coordination patterns. That's where [EMQX's recent work under the mqtt.ai umbrella](https://www.emqx.com/en/mqtt-for-ai) gets interesting. First, though, it's worth understanding *why* MQTT's primitives fit so well — and the answer traces back to a 50-year-old idea.

## The Actor Model Connection



The Actor Model — first described by Carl Hewitt in 1973 and recently [cited by The New Stack](https://thenewstack.io/can-the-50-year-old-actor-model-rescue-agentic-ai/) as a potential rescue for agentic AI's coordination challenges — proposes that the fundamental unit of computation is an *actor*: a lightweight process with private state that communicates exclusively through asynchronous message passing. Actors don't share memory. They receive messages in a mailbox, process them one at a time, and can create other actors, send messages, or update their own state. This model has powered production systems at enormous scale through frameworks like Ray, Akka, and Microsoft Orleans.

The parallel to AI agents is almost exact. An AI agent maintains its own context (private state), receives tasks and information asynchronously (mailbox), processes them using its own judgment (behavior), and delegates subtasks to other agents (spawning actors / sending messages). Look at where the complexity lives in a typical agent codebase: orchestration logic (routing, delegation, error recovery) dominates, tool execution takes the next largest share, and core AI logic — the actual reasoning — is a fraction of the whole. The Actor Model's messaging primitives absorb the orchestration layer by design.

Here's what makes MQTT's architecture relevant: it's essentially an Actor Model runtime at the infrastructure layer, whether or not it was designed that way.

- **Topics as mailboxes.** Each agent subscribes to its own topic — incoming messages queue there exactly like an actor's mailbox. The broker handles delivery, ordering, and buffering.
- **Retained messages as actor state.** An actor's externally visible state can be published as a retained message. New agents (or restarted ones) pick up the latest state immediately on subscription — no separate state-sync protocol.
- **QoS as delivery guarantees.** The Actor Model requires reliable message delivery for correctness. MQTT's QoS levels (at-most-once, at-least-once, exactly-once) let you choose the right guarantee per interaction, from fire-and-forget telemetry to exactly-once task assignments.
- **The broker as supervisor.** In Actor Model frameworks like Akka, supervisors monitor child actors and restart them on failure. MQTT's broker tracks connection state, detects disconnects, publishes Last Will messages, and can trigger reconnection logic — a structural analog to supervision hierarchies.
- **Shared subscriptions as actor pools.** Actor frameworks shard work across actor pools for load balancing. MQTT shared subscriptions distribute messages across competing consumers — the same pattern, at the protocol level.

This isn't a metaphor. It's a structural correspondence. The Actor Model tells you what primitives agent coordination needs; MQTT already implements those primitives at infrastructure scale. The frameworks that AI engineers are reaching for — Ray for distributed Python, Akka for JVM, Orleans for .NET — solve the same problems MQTT solves, but at the application layer. MQTT pushes them down into the network fabric where they can be shared across languages, runtimes, and deployment topologies.

## MCP over MQTT: Tools and Context Without the HTTP Tax



The standard MCP transports, stdio for local processes and HTTP+SSE for remote, work well for the simple case of one model talking to one tool server. But they start to strain when you need service discovery (which tool servers are available?), load balancing (multiple instances of the same tool server), or fine-grained authorization (which agents can access which tools?).

![image.png](https://assets.emqx.com/images/c354eb1bdd218d07a9f7ac2f0f818956.png)

 

[EMQX's MCP-over-MQTT transport](https://www.emqx.com/mqtt-for-ai/mcp-over-mqtt/) addresses all three by leveraging what the broker already does:

- **Service discovery.** MCP servers announce themselves on well-known topics. Clients subscribe to discover available servers — no external registry needed.
- **Load balancing.** MQTT shared subscriptions distribute requests across competing MCP server instances automatically. Spin up more instances and the broker handles dispatch.
- **Authorization.** MQTT's existing topic-level ACLs restrict which agents can reach which tools, without adding another auth layer.

It's worth noting that EMQX positions this as a complement, not a replacement, for existing MCP transports. The sweet spot is remote and edge deployments where MQTT infrastructure is already present — turning MCP server deployment into an MQTT deployment problem, which is a well-understood, well-tooled problem.

## A2A over MQTT: Agent Discovery That Scales



Google's A2A protocol defines a compelling model for how agents find each other and negotiate task delegation. But the reference implementation runs over HTTP, which means it inherits HTTP's scaling characteristics for many-to-many communication.

[EMQX's A2A-over-MQTT profile](https://github.com/emqx/mqtt-for-ai/tree/main/a2a-over-mqtt) reimagines agent discovery using retained messages on standardized topics. Each agent publishes an **Agent Card** — a structured metadata document describing its capabilities, protocol bindings, and security credentials — to a hierarchical discovery topic like `$a2a/v1/discovery/{org_id}/{unit_id}/{agent_id}`. Because these are retained messages, any agent that comes online can immediately query the broker for all available agents without hitting an external registry.

The architectural differences are meaningful:

|                    | **HTTP-based A2A**                  | **MQTT-based A2A**                    |
| :----------------- | :---------------------------------- | :------------------------------------ |
| **Communication**  | Request-response                    | Pub/sub with discrete event pushes    |
| **Streaming**      | Unidirectional (SSE)                | Bidirectional, native binary payloads |
| **Discovery**      | External registry / well-known URLs | Retained messages on broker topics    |
| **Scaling model**  | Point-to-point connections          | Broker-mediated, shared subscriptions |
| **Load balancing** | External (service mesh / LB)        | Built-in shared pool dispatch         |

![image.png](https://assets.emqx.com/images/4b066b1617e0bedecdffc910071f5c9c.png) 

The discovery and task delegation flow in detail:

![image.png](https://assets.emqx.com/images/a81a097df4c73db3f24d6b27b82e21d9.png)

[EMQX's EIP-0033 proposal](https://github.com/emqx/eip/pull/96), an EMQX Improvement Proposal currently under review, takes this further by building agent registry functionality directly into the broker:

- **Schema validation.** Agent Cards are validated against a JSON schema before acceptance, preventing malformed or malicious registrations.
- **Automatic status tracking.** The broker tracks agent online/offline status through MQTT v5 User Properties and injects status metadata automatically.
- **Shared pool dispatch.** Request-response patterns with optional load distribution across multiple agent responders.
- **End-to-end security.** OAuth2 security schemes and public key (JWKS) metadata embedded in Agent Cards for agent-to-agent authentication.

## MQTT-RT: When the Broker Is Too Slow



Not every agent interaction can tolerate the latency of routing through a central broker. Robotics swarms, autonomous vehicle coordination, and real-time industrial control demand deterministic, low-latency communication. For these cases, [EMQX is developing MQTT-RT](https://www.emqx.com/mqtt-for-ai/mqtt-rt/) — a broker-less, peer-to-peer variant of the protocol.

![image.png](https://assets.emqx.com/images/7167119db96f60303431d1d81a638f05.png)

 

The peer-to-peer protocol flow between two agents:

![image.png](https://assets.emqx.com/images/c90cefdd504ce385cc4b2c0752f03b46.png)

 

MQTT-RT peers discover each other over UDP using multicast or static peer lists, establish sessions with standard CONNECT/CONNACK handshakes, and then communicate directly using familiar MQTT publish/subscribe semantics. The key differences from standard MQTT:

- **No broker hop.** Messages travel directly between peers, eliminating the central broker as a latency bottleneck.
- **Flexible transports.** UDP, TCP, TLS, QUIC, and even shared memory — agent systems choose the right latency-throughput tradeoff per interaction.
- **Familiar semantics.** Standard MQTT publish/subscribe API, so developers don't learn a new protocol.

This is particularly compelling for "physical AI" scenarios — robot fleets in a warehouse, drones coordinating a search pattern, autonomous vehicles negotiating an intersection — where agents need to react in real time. MQTT-RT is still in the specification and SDK stage (with C/C++, Python, and Rust implementations), so production readiness remains to be proven, but the design addresses a real gap in the protocol family.

## Queues and Streams: Collapsing the Infrastructure Stack



Consider what a typical HTTP-based multi-agent deployment runs today: HTTP for RPC, Redis or RabbitMQ for task queuing, Kafka for event streaming. That's three separate systems to deploy, monitor, secure, and debug — each with its own failure modes, scaling characteristics, and on-call runbooks. When something goes wrong at 3am, your engineer needs to understand all three to diagnose the issue.

[EMQX's Queues and Streams specification](https://www.emqx.com/mqtt-for-ai/mqtt-queues-streams/) collapses two of those three into the same broker that's already handling your agent communication, using MQTT 5.0 User Properties on SUBSCRIBE packets:

- **Queue subscriptions** (`$queue/{name}/{topic}`) — persistent, exclusive-delivery message queuing with configurable retention and capacity. Ideal for task distribution where each job should be processed by exactly one agent. This is the pattern you'd normally reach for Redis or RabbitMQ to solve.
- **Stream subscriptions** (`$stream/{name}/{topic}`) — ordered, persistent, replayable message streams with consumer offsets and optional partitioning. Similar in concept to Kafka's model, for when agents need to process historical event sequences or multiple consumers need independent views of the same data.

To be clear, this doesn't make MQTT a drop-in replacement for Kafka or RabbitMQ — those systems offer deeper capabilities in throughput tuning, partitioning strategies, and retention policies. But the question isn't whether MQTT Streams can match Kafka at Kafka's scale. It's whether your agent workflow actually needs Kafka's scale, or whether you've adopted Kafka because you needed *some* streaming primitive and Kafka was the default. For agent workflows where messaging volume is moderate and operational surface area is the real cost, having queues and streams native to the same protocol that handles everything else is a meaningful reduction in what can go wrong.

## The Trade-offs



No architecture is free:

- **Operational complexity.** Running a highly available MQTT broker cluster requires attention to cluster consistency, topic namespace design, monitoring, and debugging at scale.
- **Topic design matters.** MQTT's topic-based routing means you need to design your topic hierarchy carefully; a poorly designed namespace can become as painful as a poorly designed database schema.
- **Tooling maturity.** While MQTT's binary protocol is efficient on the wire, the ecosystem of debugging and observability tools is less mature than what exists for HTTP-based systems.
- **Community gap.** The AI agent ecosystem is building on HTTP because that's where the developers are. MQTT expertise is concentrated in IoT and embedded systems engineering — different communities with different toolchains and different instincts. Bridging that gap requires SDKs, tutorials, and reference architectures that speak the language of AI developers.

## The Architectural Argument



Despite those trade-offs, the case for MQTT as the agent coordination layer is compelling. It's about the architectural coherence of solving discovery, messaging, task distribution, streaming, and real-time communication within a single protocol family instead of stitching together HTTP APIs, WebSocket connections, message queues, and streaming platforms.

Consider what a typical multi-agent deployment looks like today: HTTP for A2A discovery and task delegation, SSE for streaming results, Redis or RabbitMQ for task queuing, Kafka for event streaming, a service mesh for load balancing and discovery, and custom logic for health checking and failover. Each of these is a separate system to deploy, monitor, secure, and debug.

With MQTT, the broker becomes the unifying fabric:

| **Concern**       | **HTTP Stack**                      | **MQTT**                      |
| :---------------- | :---------------------------------- | :---------------------------- |
| Agent discovery   | External registry / well-known URLs | Retained messages             |
| Task delegation   | HTTP request-response               | Request-response over pub/sub |
| Load balancing    | Service mesh / external LB          | Shared subscriptions          |
| Task queuing      | Redis / RabbitMQ                    | MQTT Queues                   |
| Event streaming   | Kafka                               | MQTT Streams                  |
| Health monitoring | Custom heartbeat logic              | Built-in connection tracking  |
| Authorization     | Per-service auth layer              | Topic-level ACLs              |
| Real-time P2P     | Not natively supported              | MQTT-RT                       |

## What Comes Next



The convergence of IoT infrastructure and AI agent systems feels inevitable. As agents move beyond cloud-only deployments into edge devices, robots, vehicles, and industrial systems, they'll need a messaging backbone that's proven at scale in exactly those environments. MQTT has that pedigree, and EMQX is actively extending it with the specific primitives — agent registries, MCP transport, request-response patterns, queues, streams, and peer-to-peer real-time communication — that agentic AI demands.

The barrier to trying this out is essentially zero. [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) offers a forever-free tier with 1 million session minutes per month — enough to keep a modest fleet of agents connected around the clock. It deploys in seconds, scales automatically, and requires no infrastructure management. If you're building a multi-agent system and want to see how pub/sub compares to the HTTP plumbing you've been wiring together, you can have a production-grade MQTT broker running before you finish reading this paragraph.

Fifty years ago, the Actor Model taught us that the right unit of concurrency is a lightweight process with a mailbox. Twenty-five years ago, MQTT implemented that lesson at an infrastructure scale. Today, as AI agent engineers rediscover the same coordination problems — state isolation, reliable message delivery, supervision, load-balanced dispatch — the question isn't whether to adopt these patterns. It's whether to reinvent them on top of HTTP, or build on a protocol that's been solving them in production for over a decade.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
