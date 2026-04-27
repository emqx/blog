EMQX Enterprise 6.2 is now available!

This release takes MQTT a step further by adding native support for the A2A protocol over MQTT, enabling AI agents to register, discover, and collaborate directly through the broker without additional infrastructure. 

Alongside this, EMQX 6.2 introduces broker-level Unified Namespace governance to enforce topic structure and data contracts at the source, dynamic keepalive management for large device fleets, two new data integrations with Azure Event Grid and QuasarDB, and strengthened GCP connector security through Workload Identity Federation.

Whether you are building distributed AI systems, operating large-scale IoT fleets, or standardizing data quality across industrial pipelines, EMQX 6.2 delivers the coordination, governance, and operational control to run at enterprise scale.

## Real-Time Agent Discovery and Coordination with A2A over MQTT

At the center of this release is the **A2A Registry**, a standards-aligned agent discovery system built directly into the MQTT broker.

The standard A2A protocol uses HTTP as its transport, which works well in cloud environments but becomes impractical on constrained devices or at the edge, exactly where MQTT already excels. EMQX 6.2 introduces **A2A over MQTT**, a broker-neutral transport profile that brings A2A-compatible agent discovery and coordination to these environments without additional infrastructure.

Agents register by publishing structured Agent Cards as retained messages to standardized discovery topics (`$a2a/v1/discovery/{org_id}/{unit_id}/{agent_id}`). Subscribers receive the full set of registered peers immediately on connection, then live updates as agents join or disconnect. No polling, no separate registry service.

**Key Features:**

- **Event-Driven Discovery**: Agents publish their Agent Card once and immediately become discoverable, with live updates as agents come online or go offline.
- **Built-In Presence Awareness**: EMQX annotates discovery messages with `a2a-status` User Properties (`online`, `offline`, `lwt`), combining discovery and liveness in a single subscription stream.
- **Flexible Interaction Patterns**: Agents communicate via MQTT v5 `Response Topic` and `Correlation Data` properties, supporting request/response, streaming responses, multi-turn conversations, load-balanced pool dispatch, and task handover between agent instances.
- **Schema Validation**: Agent Cards are optionally validated against the A2A specification on registration, with non-conforming cards rejected before entering the registry.
- **Dashboard UI and CLI**: Operators manage Agent Cards through the EMQX Dashboard or `emqx ctl a2a-registry`.
- **Machine-Readable API Spec**: The new `/api-spec.md` and `/api-spec.html` endpoints expose focused slices of the EMQX HTTP API, enabling tools such as Claude Code or Codex to interact with and manage EMQX directly.

The A2A Registry follows emerging A2A protocol specifications and serves as the foundation for upcoming agent-based products, including EMQ's Device Agent, currently in early access.

**Example Use Case:**

In a factory automation system, a Monitor Agent on an edge gateway detects abnormal vibration on motor `line-7`. It discovers a Repair Agent by subscribing to `$a2a/v1/discovery/com.example/factory-a/+`, receives the retained Agent Card, and sends a task request. The Repair Agent streams back status updates, "Analyzing vibration signature…" and "Bearing wear detected", and the Monitor Agent triggers a maintenance ticket. The two agents coordinate without knowing each other's network addresses, with EMQX's authentication and authorization applied uniformly to all agent traffic.

> *Learn more about* [*A2A over MQTT*](https://docs.emqx.com/en/emqx/latest/emqx-ai/a2a-over-mqtt/overview.html)*.*

## Subscription-Level Message Filtering

When `mqtt.subscription_message_filter` is enabled, clients can subscribe with a `?` query suffix to filter messages at the broker before delivery. For example:

```
sensor/+/temperature?location=roomA&value>25
```

EMQX evaluates the expression against MQTT 5.0 User Properties on each incoming message and delivers only those that match. Messages dropped by a filter are tracked under the new `delivery.dropped.filter` metric.

**Key Benefits:**

- **Reduced Bandwidth**: Filtering happens at the broker. Only matching messages are transmitted, saving bandwidth on constrained network paths.
- **Lower Client-Side Load**: Consumer applications process only the data they need, without writing filter logic themselves.
- **High-Throughput Efficiency**: Particularly valuable when a single wildcard subscription covers a high-volume topic space but a consumer only needs a narrow subset of messages.

> *Learn more about* [*Subscription Filters*](https://docs.emqx.com/en/emqx/latest/subscription-filter/subscription-filter-concept.html)*.*

## Dynamic Device Management Without Disruption

EMQX 6.2 introduces the ability to dynamically update client keepalive intervals at runtime, without requiring a disconnect and reconnect cycle.

Clients can adjust their own keepalive by publishing to `$SETOPTS/mqtt/keepalive`. Backend systems can update large device fleets in bulk using `$SETOPTS/mqtt/keepalive-bulk`, applying changes across many sessions simultaneously.

**Example Use Case:**

An electric vehicle manufacturer managing over 100,000 connected vehicles can adjust connectivity behavior across the entire fleet without interrupting active sessions. When vehicles enter a low-power parked state, their keepalive intervals are extended via `$SETOPTS/mqtt/keepalive-bulk`, reducing idle network traffic and battery consumption. When the ignition turns back on, the original interval is restored with no reconnection, no session disruption, and no impact to in-flight messages.

> Learn more about [Dynamic Keep Alive Adjustment](https://docs.emqx.com/en/emqx/latest/configuration/mqtt.html#dynamic-keep-alive-adjustment).

## New and Enhanced Data Integrations

EMQX 6.2 adds two new integration targets and strengthens existing GCP connector security.

### New Integrations:

- [**Azure Event Grid**](https://docs.emqx.com/en/emqx/latest/data-integration/azure-event-grid.html): Bidirectional MQTT bridging between EMQX and Azure's fully managed event-routing service. EMQX connects as an MQTT client, supporting both outbound (Sink) and inbound (Source) data flows over TLS with client certificate authentication. Once data reaches Azure Event Grid, it routes naturally to Azure Functions, Event Hubs, Storage, and other Azure services.
- [**QuasarDB**](https://docs.emqx.com/en/emqx/latest/data-integration/quasardb.html): Direct ingestion of MQTT data into QuasarDB, a high-performance column-oriented time-series database. Messages flow through the rule engine into QuasarDB via ODBC with batch write support, making it a strong fit for high-frequency industrial telemetry workloads that require fast range queries over large time windows.

### Integration Enhancements:

- **GCP Workload Identity Federation:** GCP connectors (Pub/Sub Producer, Pub/Sub Consumer, BigQuery) now support WIF authentication via Service Account Impersonation. EMQX exchanges a short-lived OIDC token from an external identity provider, such as Azure Entra ID, for a temporary GCP credential, eliminating the need to store or rotate long-lived service account key files.

## NATS Gateway: Full Authentication Parity

EMQX's NATS Gateway allows NATS clients to connect to EMQX and exchange messages bidirectionally with MQTT. In 6.2, the gateway adds **token**, **NKey**, and **JWT** internal authentication methods, closing the main remaining gap with a native NATS Server.

**New Authentication Methods:**

- **Token Authentication:** Simple shared-secret authentication for lightweight or development deployments.
- **NKey Authentication:** Cryptographic identity based on Ed25519 key pairs, the standard NATS mechanism for production environments.
- **JWT Authentication:** Full NATS JWT credential chain validation, supporting operator/account/user hierarchies.

Teams migrating NATS workloads to EMQX no longer need to rework client-side authentication configuration. NATS clients authenticate against EMQX exactly as they would against a native NATS server.

> *Learn more about* [*Configure Authentication*](https://docs.emqx.com/en/emqx/latest/gateway/nats.html#configure-authentication) *in NATS Gateway.*

## Unified Namespace Governance: Topic Structure Enforcement at ACL Check Time

EMQX Enterprise 6.2 introduces the **UNS Governance plugin** (`emqx_unsgov`), which enforces Unified Namespace topic structure at ACL check time, with optional payload schema validation in publish processing.

In large IoT deployments, topic structures drift as teams grow and firmware evolves. Without broker-level enforcement, invalid data propagates silently through pipelines before anyone notices. UNS Governance addresses this with a fail-fast approach: non-conforming publishes are rejected at the source, keeping downstream systems clean.

The plugin operates through **models**: JSON documents that define a topic tree, variable segment constraints, and optional payload schemas per endpoint node. Topics are validated against active models at ACL check time. Mismatches are rejected with `Not Authorized` for QoS 1/2 and silently dropped for QoS 0. Payload validation runs separately in publish processing, dropping messages with non-conforming payloads without an auth reject. If no models are active, all non-exempt topics are fail-closed.

**Example Use Case:**

A manufacturing operator defines a model where valid topics follow the pattern `default/{site_id}/Lines/{line_id}/LineControl`, with `site_id` and `line_id` matched against regex constraints, and the `LineControl` endpoint requiring a payload with `Status` and `Mode` fields. A device publishing to a malformed topic is rejected at ACL check time with `Not Authorized`. A device publishing to a valid topic with a non-conforming payload has its message dropped in publish processing. Either way, the violation appears immediately in `recent_drops` before bad data reaches any downstream system.

> *Learn more about* [*UNS Governance*](https://docs.emqx.com/en/emqx/latest/extensions/plugin-catalog/emqx-unsgov.htm)*.*

## Additional Enhancements and Fixes

### Performance Improvements

- **Auth/authz node-level caching is now on by default**, reducing repeated backend lookups for returning clients and improving authentication performance in typical deployments.
- **Kafka source polling** now waits briefly for new data before returning, improving consumer responsiveness and reducing unnecessary polling overhead.

### Data Integration

- **jq library upgraded to 1.8.1** in the Rule Engine, bringing improved standards compliance. This upgrade introduces several subtle behavioral changes. Review the breaking changes guide before upgrading if your rules use jq expressions.
- **GreptimeDB and EMQX Tables** now automatically cast bare integer values to `float64`, preventing insertion failures when the target column type is float.
- **MQTT ingress bridges** now support consuming from remote message queues using the `$queue/{name}/{bind-filter}` format.

### Access Control and Management

- **Auth/authz metrics reset API**: new `POST /authentication/:id/metrics/reset` and `POST /authorization/sources/:type/metrics/reset` endpoints to clear counters on demand.
- **SSO OIDC with jq expressions**: the OIDC SSO backend now accepts jq expressions for extracting role and namespace values when auto-provisioning Dashboard users.
- **API key CLI management**: `emqx ctl api_keys` now supports list, show, add, delete, enable, and disable operations from the command line.

> *For the full list of changes, refer to the* [*Release Notes*](https://docs.emqx.com/en/emqx/latest/changes/changes-ee-v6.html#_6-2-0)*.*

## Get Started with EMQX Enterprise 6.2

[Download EMQX Enterprise 6.2](https://www.emqx.com/en/try?tab=self-managed) today and explore what's new.

Before upgrading, review the breaking changes for 6.2.0, particularly the `jq` 1.8.1 behavioral changes if your rules use jq expressions.

For questions or to discuss your use case, reach out to our [sales team](https://www.emqx.com/en/contact).
