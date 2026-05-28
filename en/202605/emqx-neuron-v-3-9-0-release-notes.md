We are excited to announce the official release of EMQX Neuron 3.9.0!

The key highlights of this release include: 

- A new online driver configuration migration tool that batch-converts KEPServerEX and Litmus Edge configurations into EMQX Neuron-importable format; 
- A new northbound Kafka plugin for native Microsoft Fabric integration, bridging the industrial edge directly to cloud data lakes; 
- OPC UA Part 9 Conditions & Alarms support, enabling real-time alarm event subscription and remote acknowledgment via method calls.

This release also delivers enhancements across tag configuration, Kafka Connector, Azure IoT Hub offline buffering, standard package content, further improving platform usability, completeness, and stability.

## Migration Tool: Smooth Transition from Kepware and Litmus Edge to EMQX Neuron

When migrating from KEPServerEX (Kepware) or Litmus Edge to EMQX Neuron, the most time-consuming step is rarely the software deployment; it is reconstructing all existing driver connections, device parameters, and large-scale tag configurations from scratch. Manual re-entry not only extends the migration timeline but also introduces transcription errors, addressing inconsistencies, and costly re-commissioning loops.

To address this, EMQX Neuron 3.9.0 ships with an **online driver configuration migration tool** (web-hosted, no installation required) that batch-maps configuration exports from third-party platforms into the standard JSON format used by EMQX Neuron southbound drivers, aligned directly with the Dashboard import workflow. The migration follows four steps: **audit existing protocols → export configuration from the source platform → upload to the migration tool for conversion → import into EMQX Neuron and verify**.

**Supported Sources:**

- **KEPServerEX (Kepware)**: Export via "Save As" to JSON. Covers Modbus, OPC UA Client, Siemens, Mitsubishi, Omron, Allen-Bradley, and more than ten other common driver types.
- **Litmus Edge**: Export Plain Text templates from Device Management. Supports Modbus variants, OPC UA, DF1, Omron FINS/Hostlink, Siemens S7, BACnet/IP, and other common protocols.

After conversion, the tool presents a **summary of device count and tag success/failure statistics**, with failure reasons attached to each failed item. Failed tags can be corrected on the EMQX Neuron side or adjusted at the source before re-running the conversion. All output files are ready for direct import via the Dashboard southbound module.

**Typical Use Cases:**

- **Platform Replacement**: Replace existing Kepware or Litmus Edge deployments with EMQX Neuron, using batch migration to compress the cutover window.
- **Proof of Concept (POC)**: Rapidly replicate existing tag and addressing configurations to minimize validation discrepancies caused by configuration drift.
- **Dual-Stack / Disaster Recovery**: Reconstruct equivalent southbound configurations in EMQX Neuron alongside the existing system for comparison, rehearsal, or gradual cutover.

For step-by-step instructions, see: [Kepware to EMQX Neuron Migration Guide](https://docs.emqx.com/en/neuronex/latest/configuration/driver-migration-tool/kepware-to-neuron.html) and [Litmus Edge to EMQX Neuron Migration Guide](https://docs.emqx.com/en/neuronex/latest/configuration/driver-migration-tool/litmus-edge-to-neuron.html).

![image.png](https://assets.emqx.com/images/73a3c53ac2f36204880526e1717e05fd.png)

## Direct Integration with Microsoft Fabric: From the Factory Floor to the Cloud Data Lake

In Industry 4.0, the challenge is getting that data into the cloud. Fragmented PLC protocols and inconsistent formats make it difficult to feed shop floor data into modern analytics platforms. EMQX Neuron 3.9.0 introduces a **northbound Kafka plugin** that positions EMQX Neuron as a standard Kafka producer. Since Microsoft Fabric's **Eventstream** natively supports the Kafka protocol, the two connect directly without SDK development required, forming a complete pipeline from device data collection to cloud data lake ingestion.

**Why EMQX Neuron + Fabric?**

On the edge, EMQX Neuron connects to 100+ industrial protocols — Modbus, OPC UA, Siemens, Mitsubishi, and more — normalizing time-series data into structured JSON. The northbound Kafka plugin publishes this data directly to a Fabric Eventstream Topic, with no additional middleware or custom adapters. On the cloud side, once data lands in Eventhouse, enterprises can run cross-system historical analysis using Synapse Data Warehouse (e.g., correlating device telemetry with ERP orders), train predictive maintenance models with Synapse Data Science, and build real-time monitoring dashboards with Power BI Direct Lake — all on a unified OneLake foundation, with no data duplication.

**Typical Data Flows:**

- **Real-Time Monitoring**: EMQX Neuron Northbound Kafka → Fabric Eventstream → Eventhouse → Power BI Dashboard
- **Predictive Maintenance**: Eventhouse historical data → Synapse Data Science → Fault prediction model → Unplanned downtime alerts
- **Cross-System Analytics**: Fabric correlates industrial time-series data with ERP orders and MES work orders in OneLake, enabling OEE and other composite KPI calculations

For connection configuration and integration steps, see: [EMQX Neuron and Microsoft Fabric Integration Guide](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/kafka/overview.html#integrating-with-microsoft-fabric)

![image.png](https://assets.emqx.com/images/43ebd575ebe330560931abe7550496e0.png)

## OPC UA Conditions & Alarms (Part 9): Subscribe to Alarm Events and Acknowledge Remotely

EMQX Neuron 3.8.0 added support for OPC DA AE, a classic COM/DCOM-based alarm protocol. The latest version introduces a completely separate capability: **OPC UA Part 9 Conditions & Alarms**.

These are distinct protocol stacks. OPC UA Part 9 is the native alarm model within the modern OPC UA protocol suite. It delivers structured JSON alarm events via a subscription mechanism and supports **Method calls** to perform operations such as alarm acknowledgment directly on the OPC UA Server.

**How It Works:**

- Set the device update mode to **Subscribe** or **Read&Subscribe**, and configure the **event root node** (default `0!2253`, the Server node) to subscribe to alarm events.
- Use the tag browsing feature (address space scan) to locate alarm nodes. The address format is `alarm:<NS>!<NodeID>`, and the data type is **JSON**.
- Each alarm event delivers a complete set of structured fields: `active` (alarm active state), `confirmed` (acknowledgment status), `severity` (0–1000 scale), `message` (alarm text), `source_name` (alarm source), `time` (Unix timestamp in milliseconds), and more.
- Method nodes follow the address format `method:<NS>!<ObjectNodeID>(<MethodNS>!<MethodNodeID>)?<param>=<type>`. With a **write-only** JSON payload, you can invoke methods such as `Confirm` directly on the OPC UA Server to close the alarm acknowledgment loop.

**Use Cases:**

- **Centralized Alarm Management**: Aggregate alarm events from multiple OPC UA devices and forward them via MQTT to a cloud alerting platform for cross-site visibility.
- **Automated Acknowledgment**: Combine with data processing rules to automatically invoke `Confirm` on specific alarm categories, reducing manual intervention.
- **Compliance and Auditing**: Maintain complete records of `event_id`, trigger time, and acknowledgment status to satisfy GMP, ISO 55000, and other regulatory requirements.

For connection configuration steps, see: [OPC UA Conditions and Alarms](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/opc-ua/conditions.html)

## Additional Enhancements

Beyond the highlights above, EMQX Neuron 3.9.0 includes the following important updates:

### Tag Configuration Improvements

Several practical improvements have been made to tag configuration:

- **Unit Support**: Tags can now be assigned a physical unit (e.g., `°C`, `bar`, `rpm`), displayed consistently across the tag configuration interface and the data monitoring view.
- **Tag Rename**: Tag names can now be modified after creation, without needing to delete and recreate the tag.
- **Extended Description Length**: The maximum tag description length has been increased to **256 characters**, supporting more complete operational annotations.

![image.png](https://assets.emqx.com/images/8c28b2fd030cefb7ed77782d7c3662ac.png)

### Kafka Connector: Shared Connection Across Multiple Sinks

A new **Kafka Connector** feature allows multiple Kafka Sinks in the data processing module to share a single Kafka connection configuration. (Note: the Kafka Sink is the output node of the rule engine in the data processing module, distinct from the northbound Kafka plugin described above.) Previously, each Kafka Sink node required its own full set of connection parameters — Broker address, authentication credentials, SSL certificates — leading to redundant configuration and multiple independent physical connections when several rules needed to publish to the same Kafka cluster.

With Kafka Connector, connection parameters are managed once at the Connector level. Multiple Kafka Sink nodes can reference the same Connector and share the underlying Broker connection, reducing both configuration overhead and resource consumption.

![image.png](https://assets.emqx.com/images/cefc5446ede6261226c4f6836ddbf0c2.png)

 

### Azure IoT Hub Offline Data Caching

The northbound Azure IoT Hub plugin now supports **Offline Data Caching**. During network interruptions, collected data is automatically queued to local storage and uploaded in chronological order once connectivity is restored, ensuring data completeness. This is particularly useful for factory Wi-Fi environments, 4G/5G cellular networks, and remote sites such as mines, wind farms, and oil fields where network stability may be limited.

### Full CNC Driver Suite in Standard Package

The standard EMQX Neuron package now includes **all CNC driver plugins** out of the box. Users no longer need to request separate licenses to access the full set of CNC machine tool connectivity capabilities, lowering the barrier to entry for CNC device integration scenarios.

## Conclusion

EMQX Neuron 3.9.0 lowers the barrier to migrating from Kepware and Litmus Edge, opens a direct northbound path to Microsoft Fabric and other modern data platforms via the new Kafka plugin, and completes the industrial alarm management picture with native OPC UA Part 9 Conditions & Alarms support. 

**Download EMQX Neuron 3.9.0:** [Download EMQX Neuron](https://www.emqx.com/en/downloads-and-install/neuronex)

**Full EMQX Neuron 3.9.0 documentation:** [EMQX Neuron Docs](https://docs.emqx.com/en/neuronex/latest/)
