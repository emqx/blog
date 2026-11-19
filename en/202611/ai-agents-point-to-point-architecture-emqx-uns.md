The agent demo works. Someone wires a language model to a handful of tags, asks it why line 3 is slowing down, and it answers well enough to get the project funded.

Then it goes to the plant, and it stops being clever. It gives confident answers about the wrong machine. It reacts to a condition long after the moment to act on it has gone. It costs more per query than anyone budgeted, and eventually the pilot is quietly parked.

The model did not get worse. It ran out of food. The architecture underneath it cannot feed an agent, and no amount of prompt engineering fixes a data layer problem.

## What the Plant Actually Looks Like Underneath: The Spaghetti Trap



The reference architecture for plant systems is inherently layered. The Purdue Reference Model set out the levels, and ANSI/ISA-95 built its enterprise-control integration on them: sensing and manipulating at Level 1, supervisory control at Level 2, manufacturing operations management (MOM/MES) at Level 3, and enterprise business planning (ERP) at Level 4. A historian sits alongside, collecting whatever it was configured to log.

Data moves upward through layers. Every hop between two systems is a custom integration that translates formats, maps fields, and handles unexpected schema mismatches.

Connecting N systems to M consumers takes N x M custom connectors. The maintenance complexity grows multiplicatively rather than additively. This is "spaghetti architecture": tolerable when the only consumers were humans passively glancing at quarterly dashboards, but fatal for autonomous AI.

## The Four Walls Stifling Industrial AI Agents



An agent is not a human reading a dashboard. It hits four walls, and they compound.

### Latency



An agent that has to wait for a reading to climb through SCADA, get transformed by MES and land in a reporting database is not operating in the present. By the time the number arrives, the moment to act on it has passed.

Polling makes this worse. A poll interval is a decision to be wrong for that long. Set it tight and you load the network and the PLCs. Set it loose and the agent reasons about a plant that has already moved on.

### Loss of Context



A temperature of 87 is not information. It becomes information when it carries which machine, on which line, in which plant.

In a layered architecture, that context lives somewhere else, usually in a tag naming convention nobody wrote down and a mapping table maintained by one person. Stripped of context, the LLM hallucinates assumptions to fill the gap — stating wrong answers with supreme confidence.

### Token Overload



Much of what a PLC emits is repetition: values that have not changed, counters ticking, heartbeat messages. Feed that stream straight into a model, and you pay per token for the repetition while also making the model's job harder. 

Stanford and Berkeley researchers found that model performance "*is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle,*" and that this held even for models built for long contexts. Padding a prompt with unchanged tag values is a good way to bury the one reading that mattered.

Filtering, cleansing and structuring has to happen before the model, and in a point-to-point architecture there is no shared place to put that work. Each integration solves it separately, or not at all.

### Data Access Overload



To answer a single cross-domain question, an agent needs direct access to PLCs, SCADA, MES, ERP, quality databases, and maintenance logs, each with different protocols, credentials, and query languages. One agent against six systems requires six custom integrations. Ten agents against those six systems require sixty. The AI program stops being an innovation initiative and turns into an unmaintainable software maintenance crisis.

## The Paradigm Shift: EMQX UNS as the AI Data Substrate



![1b55c887d47ff374437b9fee84bfbab0.png](https://assets.emqx.com/images/e5478229cd8c4e356264fb116ad2ad89.png)

A Unified Namespace (UNS) inverts this architecture. Instead of agents reaching into isolated silos, every system publishes its state **once** to a central, event-driven message broker. Anything that needs data simply subscribes to it.

By deploying EMQX as the central UNS broker paired with EMQX Neuron at the edge, all four AI architectural failure modes are addressed at the root:

- **On latency.** Publish and subscribe replaces polling. A press publishes when its state changes and the broker delivers it to every subscriber at once, so there is no poll interval sitting between the event and the agent that needs it.
- **On context.** The topic is the context. When a reading arrives on `acme/dallas/press-shop/line-3/press-02`, the agent already knows the plant, the area, the line, and the asset before it looks at the value. The semantics travel with the data instead of living in someone's spreadsheet.
- **On tokens.** EMQX's rule engine sits in the message path, and its documented job is to extract, filter, enrich, transform and store data in flight. That work happens once at the substrate for every consumer, so the model receives structured events rather than raw traffic. EMQX Neuron does the equivalent job further down, reading from more than a hundred industrial protocols including Modbus, OPC UA, BACnet and Siemens S7, and publishing structured messages from the edge.
- **On access.** The agent holds one connection to one broker and reaches everything published to it. Adding a tenth agent adds one client, not sixty integrations. Access is governed in one place too. EMQX authenticates every client, and its authorization layer is permission control over the publish and subscribe operations of each client, decided per client identifier and per topic.

## Start with One Line



None of this requires replacing the historian or rewriting SCADA. Those systems keep running and become publishers and subscribers like everything else.

1. **Pick One Line**: Select a single production line experiencing operational bottlenecks.
2. **Bridge to Broker**: Connect its controllers to EMQX Neuron, mapping tags into a standardized, hierarchical topic structure (`enterprise/site/area/line/asset`) in plain language.
3. **Connect Your Agent**: Point your AI agent to the EMQX topic tree as its primary real-time context source.

When the four architectural failure modes disappear, the difference in agent performance is immediate. An AI agent is only as intelligent as the data substrate feeding it. Provide it with a unified, context-rich stream, and the models you already own will finally deliver on their enterprise promise.

## Reference Sources



1. International Society of Automation, *ISA-95 Standard: Enterprise-Control System Integration* (ANSI/ISA-95, also IEC 62264). Levels 0 to 4 and the Purdue Reference Model basis. [ISA-95 Standard: Enterprise-Control System Integration](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard) 
2. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, Transactions of the Association for Computational Linguistics. [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) 
3. EMQX documentation, *Rule Engine*, on extracting, filtering, enriching, transforming and storing data in flight. https://docs.emqx.com/en/emqx/latest/data-integration/rules.html 
4. EMQ, *EMQX Neuron* product page, on 100+ industrial protocols including Modbus, OPC UA and BACnet. [EMQX Neuron - Modern Industrial Connectivity Server](https://www.emqx.com/en/products/emqx-neuron) 
5. EMQX documentation, *Authentication* and *Authorization*, on per-client authentication and topic-level access control. https://docs.emqx.com/en/emqx/latest/access-control/authn/authn.html  and [Authorization | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/access-control/authz/authz.html)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
