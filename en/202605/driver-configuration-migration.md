## The Shift to a Modern Edge Data Platform

When selecting an Industrial Connectivity Gateway, organizations typically weigh protocol coverage, sampling performance, and licensing. However, legacy gateways like Kepware or Litmus Edge often function as isolated data silos, tying industrial data to specific operating systems and limiting its use to basic data acquisition.

Transitioning to a modern edge data platform like EMQX Neuron changes this dynamic. Instead of simply collecting data, a modern platform unifies edge connectivity with real-time stream processing and cloud-edge integration. This transition resolves several structural constraints inherent in traditional architectures:

| Dimension                               | Typical Legacy Constraint                                    | Modern Platform Alternative (EMQX Neuron)                    |
| :-------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Deployment & Delivery**               | Binding to a specific OS ecosystem narrows hardware choice; without containerization and orchestration, consistent multi-site rollout is harder. | **Runtime & Orchestration:** Linux-native; x86 / ARM; delivered with Docker / Kubernetes; image-based replication and standardized operations; helps control total cost of ownership (TCO) tied to the OS licensing stack. |
| **Architecture & Component Boundaries** | Suites stack components weakly related to acquisition, raising resource use and operational complexity. | **Southbound Acquisition:** Industrial Connectivity Gateway role; 100+ southbound protocol drivers; balances acquisition throughput and resource use under high concurrency and large tag counts. |
| **Acquisition & Stream Processing**     | At very high frequency and very large tag counts, acquisition-path efficiency and edge stream-processing stability tend to become limiting. | **Edge Computing & Ecosystem:** Built-in SQL stream-processing engine for cleansing, aggregation, alerting, and selective inference at the edge. Works with EMQX for [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) northbound; cloud–edge paths aligned with Unified Namespace (UNS); integrable with Azure IoT Edge, AWS IoT Greengrass, and similar runtimes. |

## Introducing EMQX Neuron Driver Configuration Migration

Planning a move from Kepware (KEPServerEX) or Litmus Edge to EMQX Neuron raises a practical question: must southbound connections, device parameters, and large-scale tag sets already in production be recreated manually?

Manual re-entry lengthens delivery schedules and increases the risk of transcription errors, inconsistent addressing, and integration rework. If southbound configuration rebuild dominates implementation effort, it dilutes the strategic payoff of shifting to a modern edge data architecture.

To eliminate this friction and contain deployment risk, EMQX Neuron provides a hosted **Driver Configuration Migration** service. This tool batch-converts exports from third-party platforms into standard JSON files that can be directly imported into the Neuron Dashboard, aligning seamlessly with existing southbound workflows.

Try it: [Driver Configuration Migration](https://www.emqx.com/en/products/emqx-neuron/migrator)

![image.png](https://assets.emqx.com/images/736115438482d5f92f55290dcd4f5326.png)

### Capability Overview

- **Multi-source**: Converts exports from **KEPServerEX** and **Litmus Edge**, applying source-specific mapping rules. 
- **Protocol-level mapping**: Maps source drivers and tag structures to Neuron southbound devices and Group / Tag models (protocol scope and limits per migration guide). 
- **Reviewable outcomes**: Post-conversion summaries (device counts, tag success / failure metrics); failures include reasons for fixes in Neuron or re-export from the source. 
- **Standard deliverable**: Southbound import JSON for Neuron, consistent with Dashboard import. 

### Typical Use Cases

1. **Industrial Connectivity Gateway replacement**: Transition from Kepware or Litmus Edge to Neuron with bulk migration to shorten cutover windows.  
2. **Proof of concept (POC)**: Validate connectivity and data quality on a limited scope while aligning tags and addressing with the legacy system, limiting acceptance disputes driven by configuration drift.  
3. **Disaster recovery / dual stack**: Keep the incumbent system while reproducing equivalent southbound configuration in Neuron for comparison, drills, or phased migration.

### Source Products and Version Notes

- **Kepware (KEPServerEX)**: Export **JSON** (unencrypted) via **Save As**, then upload with **KEPServerEX** selected. Covers Modbus, [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol) Client, Siemens, Mitsubishi, Omron, BACnet/IP, CODESYS, Allen-Bradley, and other common drivers (BCD, arrays, certificates, and similar caveats per protocol tables in the guide).  
- **Litmus Edge**: Export the **Plain Text** template from Device Management, then upload with **Litmus Edge** selected. Supports Modbus family, OPC UA (Gen1 / Gen2), DF1, Omron FINS / HostLink, Siemens S7, BACnet/IP, and other common protocols.

## Step-by-Step Migration Guide

The Driver Configuration Migration service operates as a hosted web application, removing the need for a separate local client installation.

The migration workflow follows a structured path from the source environment into the running Neuron architecture:

### 1. Inventory & Pre-flight Checks

Consult the migration guides to verify that all active on-site protocols are supported. Note any documented boundaries regarding string lengths, array handling, or cryptographic certificates.

### 2. Source Export

Generate the necessary configuration file from the incumbent platform according to standard procedures:

- **Kepware:** Export in JSON format.
- **Litmus Edge:** Export the Plain Text template.

### 3. Service Conversion

Navigate to the **Driver Configuration Migration** interface on the EMQX website. Select the corresponding source format, upload the asset, and allow the server-side mapping engine to validate the file. Once processing completes, download the generated standard JSON payload.

> **Data Privacy Note:** Configuration payloads are processed strictly within volatile memory and are not persisted on EMQX infrastructure. Review the hosting interface for active file size boundaries and formatting validation rules.

### 4. Import & Runtime Commissioning

Access the target Neuron Dashboard, navigate to the southbound configuration section, and import the processed JSON file. Remediate any flagged exceptions or specialized tags manually, then proceed to validate active connection telemetry and data stream health.

Verify physical network reachability from the Neuron runtime environment to the respective field components (validating IP routes, ports, serial assignments, and active firewall policies) to complete final commissioning.

## Driving Value From Edge Data

Selecting an industrial connectivity architecture ultimately hinges on long-term deployment flexibility, total cost of ownership, and native integration with the broader data ecosystem. By automating tedious rule-based configuration conversion with the Driver Configuration Migration tool, operations teams can bypass migration overhead and rapidly realize the benefits of Neuron’s lightweight footprint, MQTT-native northbound delivery, and UNS-aligned cloud-edge capabilities.

If you are evaluating migration from Kepware or Litmus Edge to Neuron, run a small guided export trial; For full protocol coverage and step-by-step instructions:

- [Driver Configuration Migration (EMQX)](https://www.emqx.com/en/products/emqx-neuron/migrator)  
- [EMQX Neuron documentation - Driver migration tool](https://docs.emqx.com/en/neuronex/latest/configuration/driver-migration-tool.html)
