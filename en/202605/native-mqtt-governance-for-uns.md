> *EMQX 6.2 has recently been released, introducing a broker-level Unified Namespace governance to enforce topic structure and data contracts at the source.*
>
> *We’d been debating topic and schema governance for UNS inside EMQX for a long time. The urgency crystallized after a hallway conversation with a user at an industry conference who described how a single misconfigured gateway had quietly polluted their data lake. We went back, built and shipped the first version as a plugin in EMQX 6.2 so teams could act immediately. Looking ahead, we plan to promote UNS Governance to a native feature in EMQX 6.3 to make it even easier to adopt and operate at scale.*

## The Hidden Cost of an Ungoverned Unified Namespace

The Unified Namespace (UNS) has become the de facto architecture for modern industrial IoT. By organizing all operational data into a single, hierarchical MQTT topic tree — typically following ISA-95 — manufacturers gain a shared data layer that connects OT, IT, and cloud systems without point-to-point integrations.

But there's a problem nobody talks about at the conference keynotes: **topic sprawl**.

Six months after go-live, your clean ISA-95 hierarchy looks like this:

```
v1/WTP1/Intake/PUMP01/Sensors/TRB001/Reading     <- correct
v1/wtp1/Intake/PUMP01/Sensors/TRB001/Reading     <- wrong case
v1/WTP1/Boiling/TANK01/Sensors/TMP001/Reading     <- "Boiling" is not a valid area
v1/WTP1/Intake/filter-3/Sensors/PRS001/Reading    <- wrong ID format
v1/WTP1/Intake/PUMP01/Debug/Log                   <- unauthorized branch
v1/WTP1/Intake/PUMP01/Sensors/TRB001/Reading      <- payload: {"value":"not-a-number"}
```

Every malformed topic or invalid payload is a silent failure. Downstream analytics ingest garbage. Historian queries return incomplete datasets. Dashboards show gaps. And the root cause? Someone on a different shift deployed an edge gateway with a typo in the topic configuration.

Bad data quality in manufacturing costs an average of 15-25% of operating revenue, according to industry estimates. In a Unified Namespace, a single misconfigured device can corrupt the data layer for every consumer downstream.

## What Is MQTT Topic Governance?

Topic governance is the enforcement of a defined schema on your MQTT topic tree. Just as a relational database enforces table schemas and column types, topic governance validates that every MQTT message published to your broker:

1. **Follows an approved topic hierarchy**: only recognized paths are allowed
2. **Uses valid segment values**: site IDs, area names, and equipment IDs match defined patterns
3. **Carries a well-formed payload**: JSON structure, required fields, and value types are validated

You want your UNS to be a contract but not just a suggestion.

## Introducing UNS Governance for EMQX

EMQX 6.2 introduces the **UNS Governance plugin**: a native, broker-level enforcement layer that validates every MQTT publish against your Unified Namespace model.

### How It Works

UNS Governance operates as part of EMQX's message processing pipeline. When a client publishes a message:

1. **Topic-filter pre-check**: The plugin matches the publish topic against compiled topic filters derived from your active models. This is a fast, O(1) lookup, not a tree traversal for every message.
2. **Topic structure validation**: The matched model validates each topic segment. Variables (like `{site_id}` or `{area_id}`) are checked against regex patterns or enumerated value lists.
3. **Payload schema validation**: If enabled, the JSON payload is validated against the endpoint's schema definition — required fields, data types, value enumerations, and whether additional properties are allowed.
4. **Enforcement action**: Invalid messages are rejected (for topic violations) or silently dropped (for payload violations), with detailed counters and recent-drop event logs for observability.

```
MQTT Publish
    |
    v
+---------------------+
|  Topic Filter Match  |---- No match ---> Reject (topic_nomatch)
+---------+-----------+
          | match
          v
+---------------------+
|  Segment Validation  |---- Invalid ----> Reject (topic_invalid)
+---------+-----------+
          | valid
          v
+---------------------+
|  Endpoint Check      |---- Not leaf ---> Reject (not_endpoint)
+---------+-----------+
          | endpoint
          v
+---------------------+
|  Payload Validation  |---- Invalid ----> Drop (payload_invalid)
+---------+-----------+
          | valid
          v
      Delivered
```

### Key Capabilities

**Declarative topic tree models.** Define your UNS schema as a JSON model with ISA-95-aligned hierarchy, variable constraints, and payload schemas. No code required.

![image.png](https://assets.emqx.com/images/6eb2bdbf34a6db16a3905356f5ce9794.png)

The screenshot above is the topic tree editor UI, and below is the raw model spec.

```json
{
  "id": "water-treatment",
  "variable_types": {
    "site_id":   { "type": "string", "pattern": "^WTP[0-9]{1,3}$" },
    "area_id":   { "type": "enum", "values": ["Intake", "Coagulation", "Filtration", "Disinfection"] },
    "unit_id":   { "type": "string", "pattern": "^[A-Z]{2,6}[0-9]{1,3}$" }
  },
  "tree": {
    "v1": {
      "children": {
        "{site_id}": {
          "children": {
            "{area_id}": {
              "children": {
                "{unit_id}": {
                  "children": {
                    "Status":  { "_payload": "equipment_status" },
                    "Alarm":   { "_payload": "alarm" },
                    "Sensors": { "children": { "{sensor_id}": { "children": {
                      "Reading": { "_payload": "sensor_reading" }
                    }}}}
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**JSON Schema payload validation.** Each endpoint in your topic tree can reference a payload schema that enforces required fields, data types, and value enumerations.

```json
{
  "sensor_reading": {
    "type": "object",
    "required": ["value", "unit", "ts"],
    "properties": {
      "value":   { "type": "number" },
      "unit":    { "type": "string", "enum": ["mg/L", "NTU", "pH", "degC", "mbar", "m3/h"] },
      "ts":      { "type": "integer" },
      "quality": { "type": "string", "enum": ["good", "uncertain", "bad"] }
    },
    "additionalProperties": false
  }
```

**Real-time observability.** A built-in dashboard shows cluster-wide metrics — total messages, allowed, dropped — broken down by rejection reason and per-model. A recent-drops event log shows exactly which topics failed and why.

![image.png](https://assets.emqx.com/images/b828762cc666f54faf2f6dc2aaad9ce2.png)

[Realtime Statistics]{.block .text-center}

![image.png](https://assets.emqx.com/images/ff85d42d53f630af4b28074812120452.png)

[Recent Events]{.block .text-center}

**Multiple model support.** Run different UNS models for different namespaces (e.g., `v1/` for production, `v2/` for a pilot line) with deterministic model selection and per-model metrics.

**Exempt topics.** System topics, diagnostics, or legacy integrations can bypass governance via configurable topic filter exemptions.

**Bootstrap models.** Ship a default UNS model with the plugin so governance is active from first boot — no manual configuration required.

**Visual schema editor.** A built-in web UI lets engineers browse the topic tree, edit payload schemas, and validate topics interactively through the EMQX Dashboard.

## Real-World Example 1: Municipal Water Treatment

Consider a municipal water treatment plant running EMQX as the UNS backbone. The ISA-95 topic hierarchy covers six process areas, from raw water intake through distribution:

```
v1/{site_id}/{area_id}/{unit_id}/Sensors/{sensor_id}/Reading
v1/{site_id}/{area_id}/{unit_id}/Status
v1/{site_id}/{area_id}/{unit_id}/Alarm
v1/{site_id}/{area_id}/{unit_id}/Dosing
```

**Without governance**, a misconfigured PLC publishes turbidity readings to `v1/wtp1/Intake/PUMP01/Sensors/TRB001/Reading` (lowercase site ID). The historian ingests it under a different key. The compliance dashboard shows a gap in turbidity monitoring. An operator manually investigates — hours later.

**With UNS Governance**, the publish is rejected at the broker with a `topic_invalid` reason. The device receives a PUBACK error code. The operations team sees the rejection in the Stats dashboard immediately. The PLC vendor fixes the configuration. Total time to resolution: minutes, not hours.

## Real-World Example 2: Multi-Team Plant Management

Consider a large manufacturing plant where different operational teams are responsible for distinct sectors, each deploying and managing their own edge devices. For instance, one team manages the assembly line, another handles quality control, and a third manages raw material intake. Each team has its own developers configuring MQTT publishers for their respective devices.

Without governance, a developer on the quality control team might inadvertently configure a device to publish data to a topic like `v1/FACTORY_A/Quality/InspectionLine01/Sensors/Temperature/reading` using a different casing or an unrecognized segment value, e.g., `v1/factory_a/Quality/InspectionLine01/Sensors/Temperature/reading` (lowercase factory ID). Or, a new team member, unaware of the established schema, might introduce a new topic branch like `v1/FACTORY_A/Quality/TemporaryTesting/Data`. These seemingly small deviations lead to fragmented data, where analytics dashboards fail to correlate data across the entire plant, and critical production insights are missed. Data scientists attempting to build predictive models struggle with inconsistent topic paths and unreliable data sets, leading to a lack of trust in the overall data.

With UNS Governance, any message published with a non-conforming topic path or an invalid payload schema is immediately rejected at the broker. The team responsible gets instant feedback to correct misconfigurations before bad data pollutes the UNS. Centralized enforcement keeps every team aligned to a single contract, ensuring trustworthy data across the entire plant and enabling accurate, real-time decisions.

Payload validation catches subtler issues too. A sensor gateway sends `{"value":"not-a-number","unit":"NTU","ts":1712678400000}` — the `value` field is a string instead of a number. Without governance, this silently corrupts downstream analytics. With governance, the message is dropped, the counter increments, and the event appears in the recent-drops log with the exact validation error.

## Why Enforce Governance at the Broker?

There are three places you can enforce a UNS schema: at the edge device, in application middleware, or at the broker. Here's why the broker is the right layer:

| Approach                               | Coverage                                                     | Latency                                | Maintenance                       |
| :------------------------------------- | :----------------------------------------------------------- | :------------------------------------- | :-------------------------------- |
| Edge device validation                 | Per-device; misses rogue publishers                          | Adds processing at constrained devices | Must update every device firmware |
| Application middleware                 | Per-consumer; doesn't prevent bad data from reaching the bus | Adds a hop                             | Must deploy and scale separately  |
| **Broker-level (EMQX UNS Governance)** | **100% of publishers**                                       | **Sub-millisecond (inline)**           | **Single configuration point**    |

Broker-level enforcement is the only approach that guarantees **no invalid message reaches any subscriber**. It's also the only approach that scales with your MQTT infrastructure rather than requiring a parallel validation fleet.

## Getting Started in 10 Minutes

### Step 1: Install the Plugin

Upload the UNS Governance plugin package through the EMQX Dashboard (Management -> Plugins) or via the REST API. The plugin is compatible with EMQX 6.1 and later.

### Step 2: Define Your Model

Create a JSON model that describes your UNS topic hierarchy. Start with the bundled ISA-95 template and customize the variable constraints and payload schemas for your environment.

### Step 3: Activate and Monitor

Upload the model via the plugin API or Dashboard UI. Set `on_mismatch: deny` and `validate_payload: true`. Every non-conforming publish is now rejected or dropped, with full observability through the Stats dashboard.

```shell
# Upload and activate a model
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -X POST http://localhost:18083/api/v5/plugin_api/emqx_unsgov/models \
     -d '{"activate": true, "model": <your-model-json>}'

# Check enforcement stats
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:18083/api/v5/plugin_api/emqx_unsgov/stats
```

### Step 4: Iterate

Use the visual schema editor to refine your model. Add payload schemas for new endpoint types. Review recent-drops events to identify misconfigured devices. Your UNS schema evolves with your operations — governed from day one.

## Built for Enterprise Scale

UNS Governance is built as a native EMQX plugin, which means:

- **Cluster-wide enforcement**: Models and configuration replicate across all nodes automatically. Stats are aggregated cluster-wide.
- **Hot reconfiguration**: Activate, deactivate, or update models without broker restart.
- **Prometheus integration**: All counters are exposed in Prometheus text format at `/metrics` for integration with Grafana, Datadog, or your existing monitoring stack.
- **Zero-downtime deployment**: Install or upgrade the plugin without disrupting connected clients.

Combined with EMQX's proven ability to handle 100M+ concurrent connections, UNS Governance scales from a single-site pilot to a global multi-plant deployment.

## From Data Chaos to Data Contracts

The Unified Namespace is only as valuable as the data flowing through it. Without governance, it's a convention that erodes over time. With EMQX UNS Governance, it becomes an enforceable contract — validated at wire speed, observable in real time, and managed from a single pane of glass.

**Your 10 minutes start now.** Install the plugin, upload a model, and watch every non-conforming message get caught before it reaches a single subscriber.

Ready to enforce your Unified Namespace? [Download EMQX 6.2](https://www.emqx.com/en/downloads-and-install/enterprise) and [UNS Governance Plugin](https://docs.emqx.com/en/emqx/v6.2/extensions/plugin-catalog/emqx-unsgov.html). Or [contact our solutions team](https://www.emqx.com/en/contact) to discuss your UNS architecture.
