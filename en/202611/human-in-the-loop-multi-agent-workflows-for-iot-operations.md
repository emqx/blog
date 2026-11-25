## Introduction



AI agents are increasingly capable of analyzing data, making decisions, and carrying out tasks autonomously. In IoT environments, this opens up new possibilities for intelligent operations: agents can monitor device conditions, investigate anomalies, recommend corrective actions, and coordinate responses across systems.

But identifying a problem is only part of the job. In many operational scenarios, resolving an issue requires taking action on physical devices. Such actions may affect equipment behavior, production processes, or operational safety. Allowing an AI agent to execute every action autonomously is not always appropriate.

A more practical approach is to combine multi-agent collaboration with human oversight. Specialized agents can handle different stages of an operational workflow, while human operators retain control over actions that require approval.

This article explores this approach through a simulated cold storage monitoring and control scenario using A2A and EMQX.

## A Three-Agent Architecture for IoT Operations



Consider a cold storage facility where the normal temperature range is between 2°C and 8°C. When the temperature exceeds this range, multiple agents can work together to investigate the cause and coordinate a response:

- **Coordinator Agent:** Manages the overall workflow, delegates tasks to other agents, and consolidates their responses.
- **Diagnostic Agent:** Analyzes device telemetry and identifies potential causes of abnormal conditions.
- **Device Control Agent:** Evaluates possible corrective actions and carries them out when authorized.

![image.png](https://assets.emqx.com/images/55feac5d0a42170e29e8bea3542a7219.png)

These agents collaborate through A2A messages. The Coordinator Agent acts as the entry point for the operator's request, while the Diagnostic and Device Control Agents handle investigation and execution.

For operations involving physical devices, the workflow also needs to account for human approval before proceeding with actions that should not be left entirely to an autonomous agent.

## Human Approval as Part of the Agent Workflow



Take this demo as an example:

### Step 1: Diagnose the Anomaly



The operator submits a request to the Coordinator Agent:

> *Investigate why the cold storage temperature is rising and restore it to the normal range.*

The Coordinator Agent identifies the Diagnostic Agent and delegates the investigation.

The Diagnostic Agent analyzes the simulated telemetry data and determines that insufficient refrigeration power is the primary cause of the temperature increase. It returns its findings as an A2A Artifact.

### Step 2: Request Human Approval



Based on the diagnosis, the Coordinator asks the Device Control Agent to evaluate a corrective action.

The Device Control Agent proposes increasing the simulated refrigeration power to 80%. Instead of executing the operation immediately, it requests human approval.

The Coordinator Agent forwards the approval request to the operator.

The operator reviews the proposed action and approves it. The Coordinator Agent then sends the confirmation back to the Device Control Agent as additional input to the existing task.

### Step 3: Resume Execution and Return the Result



After receiving approval, the Device Control Agent resumes the original task and carries out the operation in the simulated environment.

It then returns an A2A Artifact containing the execution information. The Coordinator Agent consolidates the results and provides the operator with an update on the completed action.

![image.png](https://assets.emqx.com/images/6b0c50f7bc02e827d9081363f9839e93.png)

This workflow demonstrates how multiple agents can handle investigation and execution while keeping a human in control of consequential device operations.

## Why Task Continuity Matters



Human approval is not simply an external confirmation. It is an intermediate step in an ongoing agent task. 

The A2A interaction model provides a structured way to preserve that continuity:

- **Task** tracks the progress and lifecycle of an assigned piece of work.
- **Message** carries the initial request and subsequent information or confirmation.
- **Artifact** delivers the results produced during task execution.

In this scenario, the Device Control Agent pauses the existing Task when approval is needed and resumes it after receiving the operator's confirmation. This preserves the relationship between the original request, the approval step, and the final execution result.

By maintaining task context across interruptions, A2A makes it easier to coordinate multi-step workflows that involve human intervention.

## The Role of EMQX



EMQX provides the messaging infrastructure for multi-agent collaboration through MQTT, along with A2A-related capabilities for agent registration and discovery.

### MQTT-Based Communication Across Distributed Agents



In IoT environments, agents may run on edge gateways, industrial computers, or cloud infrastructure. Establishing direct connections between them can introduce additional networking and deployment complexity.

With A2A over MQTT, agents connect to an MQTT broker as clients and exchange messages through the publish/subscribe model. The broker routes requests, responses, task updates, and results between agents.

In this cold storage demo, all inter-agent messages are routed through EMQX. This allows the Coordinator, Diagnostic, and Device Control Agents to collaborate without requiring direct network connections between each pair of agents.

### EMQX A2A Registry for Agent Capability Management



EMQX A2A Registry provides a centralized way to register, validate, view, and manage Agent Cards. It supports:

- **Agent registration:** Register Agent Cards that describe agent identities, skills, and capabilities.
- **Schema validation:** Validate Agent Card data against JSON Schemas.
- **Centralized visibility:** View registered agents and their information through the EMQX Dashboard.
- **Agent management:** Update or deregister Agent Cards and manage agent online status.

## Design Considerations for Human-in-the-Loop IoT Automation



Building multi-agent workflows for IoT operations requires more than assigning tasks to different agents. Several design considerations help make these workflows easier to manage:

- **Define clear agent responsibilities.** Separate coordination, diagnosis, and device control so that each agent has a well-defined role.
- **Identify actions that require approval.** Determine which operations can be performed autonomously and which must pause for human authorization.
- **Preserve task context.** Keep the original task and its execution state across intermediate steps, including approval requests and subsequent input.
- **Return execution results.** Ensure that agents report what they have executed, rather than only providing recommendations or proposed actions.

These principles help balance agent autonomy with operational oversight, particularly when AI-driven decisions can lead to changes in physical environments.

## Conclusion



Multi-agent workflows can connect IoT anomaly detection, diagnosis, and device operations within a coordinated process. By incorporating human approval as an explicit step, they can support more autonomous operations without removing human oversight.

A2A defines how agents collaborate, while MQTT and EMQX provide the messaging infrastructure and agent capability management needed to connect them across distributed IoT environments.

**Explore more:**

- [A2A over MQTT: How AI Agents Find Each Other at Scale](https://www.emqx.com/en/blog/a2a-over-mqtt) 
- [One AI Agent per Device: How MQTT Turns IoT Fleets into Self-Coordinating Systems](https://www.emqx.com/en/blog/how-mqtt-turns-iot-fleets-into-selfcoordinating-systems) 

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
