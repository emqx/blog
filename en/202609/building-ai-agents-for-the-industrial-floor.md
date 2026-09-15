## Introduction

Over the past few years, factories have deployed more and more digital systems: MES, ERP, SCADA, IIoT platforms, and more. Significant investments have been made in digitalization, yet a familiar problem remains.

When a machine triggers an alarm, a production supervisor may need to check the MES for the work order, open SCADA to review real-time trends, search the equipment records for maintenance history, and then call an equipment engineer for more information. Checking the status of a single machine can mean switching between several systems.

The data is there. The systems are there. But getting the right answer when it is needed still requires people to search, connect the dots, and make the judgment. This is the **last mile of factory intelligence**.

The rise of large language models (LLMs) and AI agents offers a new way to address this challenge. But industrial environments have their own constraints. A general-purpose AI agent cannot simply be dropped into a factory and expected to work.

This article explores how to build AI agents for industrial equipment around real-world factory requirements, and how EMQ Device Agent can be applied in this scenario.

## The Evolution of Industrial Digitalization: From MES to IIoT

Before discussing AI agents, it is useful to understand how factory systems have evolved.

**Stage 1: MES and ERP as the central systems**

ERP manages orders, materials, and financial processes, while MES manages production execution. Most interactions between IT and OT have traditionally gone through the MES. It handles business processes while also interacting with equipment through SCADA systems and industrial PCs.

**Stage 2: Custom-built automation units**

In some factories, automation teams develop programs directly on industrial PCs to execute specific logic and solve localized automation problems. These solutions can be effective, but they are often isolated from one another and difficult to replicate and maintain.

**Stage 3: IIoT platforms**

MES is designed for production business logic, not for handling high-frequency, high-volume equipment data. IIoT platforms take on large-scale data collection and command delivery at the infrastructure layer, with architectures designed for high-throughput workloads. Wireless sensors and gateways can also connect large numbers of previously unconnected or "dumb" devices, enabling plant-wide visibility. MES can then focus on higher-level production processes.

At this point, the connectivity problem is largely solved. But connected data does not automatically translate into intelligence. Equipment data may sit in a time-series database while maintenance manuals remain in a document repository. When the information is needed, people still have to search for it and interpret it themselves.

That is the final step AI agents need to address: **making data speak for itself when people need it.**

## Where Traditional Approaches to Industrial AI Agents Fall Short

A common approach to building industrial AI agents today is to combine an LLM with time-series database queries, a vectorized knowledge base, and MCP-based equipment control, then orchestrate these capabilities through workflows.

Technically, this approach is sound. But when deployed on the factory floor, it often runs into three challenges:

1. **Too technical for frontline users**

These agents are often designed from an IT perspective, with workflows, nodes, APIs, and orchestration. The technology may be sophisticated, but production managers, equipment engineers, and shift supervisors may find it difficult to understand and use.

If an agent cannot directly address their day-to-day problems, it can easily end up as a technology demo rather than a production tool.

1. **Fragmented information**

Equipment-related information is scattered across multiple systems: real-time data in the IIoT platform, historical trends in time-series databases, maintenance manuals in document repositories, and work orders in the MES.

Without a unified model connecting factories, production lines, intelligent units, and equipment, an AI agent cannot access the full context it needs to provide complete and accurate answers.

1. **Poor scalability as requirements evolve**

Workflows are effective for executing predefined processes, but that is also their limitation: they are designed around scenarios that have already been anticipated and orchestrated.

Factory requirements are constantly changing. Every new scenario can require another workflow, making it difficult for IT teams to keep pace with evolving business needs.

## A Different Approach: Build AI Agents Around Equipment

A different approach is to **build AI agents around equipment rather than around workflows**.

The "equipment" can be a physical machine or an intelligent unit. This is a much more natural model for people on the factory floor. They do not need to understand workflows, nodes, or orchestration. They simply know that a CNC machine has an AI agent and can talk to it directly.

> **What is an intelligent unit?** An intelligent unit is a group of devices and systems combined to perform a specific production task. For example, an intelligent unit designed to improve the efficiency of small-batch mold-core machining and reduce manual intervention may include CNC machining centers, EDM machines, industrial robots for loading and unloading, automated material storage, intelligent inspection sensors, and a PLC-based central control unit.

This approach addresses three practical constraints in manufacturing:

- **Production lines cannot be extensively reworked.** The solution must be layered on top of existing systems rather than requiring major factory modifications.
- **Deployment must be easy to replicate.** Factories may have dozens or hundreds of machines, so the cost and effort of building each agent must be low enough to support large-scale deployment.
- **Existing systems must remain connected.** Time-series databases, RAG knowledge bases, MES, and IIoT platforms all need to be integrated to provide agents with accurate context.

## EMQ Device Agent: AI Agents Built for Industrial Equipment

**Equipment-centric modeling with zero learning curve for frontline users**

Every machine or intelligent unit can have its own AI agent. If an operator wants to know whether the spindle temperature of CNC #3 is abnormal today, they can simply ask. There is no need to learn technical concepts or navigate complex systems.

**Build agents quickly with natural language**

No coding or workflow design is required. Natural language can be used to configure equipment connectivity, data collection, and control capabilities.

This can reduce the time required to build an agent for a single machine from weeks to days or even hours, which is an essential foundation for scaling across the factory.

**An orchestratable agent architecture that integrates seamlessly with existing systems**

RAG knowledge bases, time-series databases, and other systems can also be connected using natural language. Maintenance manuals and process documentation can be added to the knowledge base, while historical equipment data can be stored in time-series databases.

Capabilities such as historical data analysis, troubleshooting, and predictive maintenance can then be built naturally around the equipment agent.

**Deep integration with enterprise IM platforms**

Equipment agents can integrate bidirectionally with enterprise messaging platforms such as DingTalk, Feishu, and WeCom.

On one side, equipment alarms, status changes, and analysis reports can be automatically pushed to work groups so that the right people are notified immediately. On the other, frontline personnel do not need to install another app or log into another system. They can simply @ the equipment agent in their existing messaging platform to ask questions or issue commands.

Equipment intelligence becomes part of the tools employees already use rather than creating yet another workflow or application entry point.

**Agent collaboration with MES, ERP, and other business systems**

An equipment agent does not operate in isolation. Through standardized agent collaboration mechanisms, it can work with agents representing other enterprise systems.

After confirming a fault, for example, the equipment agent can automatically create and track a maintenance work order in the MES. It can check spare-parts availability in the ERP and trigger a purchase request if inventory is insufficient. During maintenance, it can also coordinate with production scheduling to minimize the impact of downtime.

This connects equipment intelligence with production and business operations.

**Deep integration with IIoT platforms**

Device Agent can access equipment location, operating status, and historical data in real time. The IIoT platform already deployed at the factory does not become obsolete; instead, it becomes the data foundation for AI agents.

Device Agent does not replace existing systems. It adds an intelligent layer on top of them.

**Industrial PC deployment with production-line isolation**

Device Agent can run on industrial PCs close to the equipment. AI agents on different production lines can operate in isolation without affecting one another. Private deployment is also supported, keeping data within the factory.

For equipment-control operations, permission management and confirmation mechanisms provide clear security boundaries.

**Hierarchical management from equipment to shop floor to enterprise**

On top of individual equipment agents, factories can progressively build shop-floor-level and enterprise-level agents, creating a hierarchical equipment intelligence architecture.

A production supervisor might ask, "How is this line performing today?" while a plant manager might ask, "How do equipment health levels compare across production areas?" Each user gets answers at the appropriate level of the organization.

**Continuously improving accuracy**

Conversation history can be used to continuously extract and refine equipment-related Q&A. New troubleshooting experience can be added to the knowledge base after human review and then shared across agents for similar equipment.

As the system is used, the accuracy and usefulness of its answers can continuously improve.

## Typical Use Cases

### Use Case 1: Ask About Equipment Status in Natural Language

During routine inspections, a shift supervisor can simply @ the equipment agent in a work group and ask:

> "What has the mold temperature trend of Injection Molding Machine #1 looked like over the past 24 hours? Were there any out-of-spec conditions?"

The agent can automatically query the time-series database, analyze the data, and return the trend, abnormal periods, and corresponding visualizations.

What previously required hours of manual data export, charting, and comparison can now be completed with a single question.

### Use Case 2: Troubleshooting with On-Demand Access to Knowledge

When an equipment alarm is automatically pushed to the IM work group, the agent can correlate the alarm code with the RAG-based maintenance knowledge base and provide possible causes and step-by-step troubleshooting recommendations.

It can also retrieve similar maintenance incidents from the same equipment over the past three months.

Even newly onboarded maintenance personnel can quickly leverage the experience of senior engineers, significantly reducing the time required to identify and resolve faults.

### Use Case 3: From "Repair After Failure" to "Repair Before Failure"

Based on historical operating data and maintenance records, the agent can regularly analyze degradation trends in critical components.

When equipment requires preventive maintenance, it can proactively send an alert with a recommended maintenance window. By scheduling maintenance outside peak production periods, factories can minimize unplanned downtime.

### Use Case 4: Multi-Agent Collaboration for Equipment Failures

When a critical machine triggers a fault alarm, multiple system agents can coordinate automatically without requiring someone to manually orchestrate the response:

- **Equipment agent:** Identifies the fault and provides a standardized maintenance procedure.
- **MES agent:** Automatically creates a maintenance work order and assigns it to the appropriate maintenance team.
- **ERP agent:** Checks spare-parts inventory in real time and initiates a purchase request if parts are unavailable.
- **Production scheduling agent:** Evaluates the impact of downtime and dynamically adjusts the priority of affected work orders.

The entire process remains visible to relevant roles through the IM group, with people only required to provide confirmation at key decision points.

What previously required one or two days of cross-department coordination can instead be handled through autonomous agent collaboration, significantly improving response efficiency from alarm detection to process completion.

## Value Delivered

From the perspective of factory ROI, the value of EMQ Device Agent can be summarized in four areas:

- **Fast to build:** Natural-language modeling enables equipment agents to go live in days and be rapidly replicated across machines and intelligent units throughout the factory.
- **Minimal disruption:** No production-line changes or equipment replacement are required. Device Agent works on top of existing MES, IIoT platforms, time-series databases, and other systems, protecting existing investments.
- **Low barrier to adoption:** Frontline personnel interact with agents using natural language, with no technical expertise required. Intelligence becomes part of daily operations rather than another IT system to learn.
- **Built to evolve:** The architecture can expand from equipment to shop floor to enterprise, while conversation history continuously feeds back into the knowledge base and improves agent accuracy over time.

## Conclusion

Over the past decade, manufacturers have built the digital foundations for connected equipment and cloud-based data, accumulating production data at an unprecedented scale. Over the next decade, the key challenge will shift to **putting that data to work**, turning static metrics on dashboards into actionable intelligence that supports frontline decisions and solves real production problems.

Equipment-centric AI agents provide a natural path for bringing AI into industrial environments. They do not require production lines to be rebuilt or existing systems to be replaced, nor do they require frontline workers to master complex technologies. Instead, they bring data analysis, troubleshooting, and cross-system collaboration directly into the workflows people already use.

If you are planning to bring intelligent equipment management to your factory, [explore EMQ Device Agent](https://www.emqx.com/en/device-agent) and [talk to us](https://www.emqx.com/en/contact) about your production environment and modernization goals.
