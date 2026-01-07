EMQX 6.1.0 is now available!

With the introduction of MQTT Streams, this version brings durable, replayable message streaming directly into the MQTT ecosystem. It also enhances multi-tenancy with improved namespace configuration, clearer isolation, and namespace-level observability, while expanding data integration capabilities for modern time-series and streaming workflows.

Whether you’re building event-driven IoT systems, operating large-scale telemetry pipelines, or running systems with thousands of tenants, EMQX 6.1.0 delivers the replayability, visibility, and operational control needed to run MQTT at enterprise scale.

## Replayable Streaming with MQTT Streams

EMQX 6.1.0 introduces MQTT Streams, a durable streaming capability that extends MQTT’s real-time publish/subscribe model with persistent, replayable message streams. 

MQTT Streams automatically collect messages that match a topic filter during their lifetime and persist them durably. Clients can consume stream data using standard MQTT subscriptions, with support for ordered delivery and time-based replay, allowing multiple consumers to independently read the same data from different points in time.

Streams are accessed using a special MQTT subscription format: `$s/<timestamp>/<topic_filter>`.

**Main Features:**

- **Time-Based Replay**
  Consumers can replay historical data from any point in time, enabling backfilling, debugging, and audit workflows without impacting live consumers. The timestamp specifies the replay starting point and can be a Unix timestamp in microseconds, or one of the special values `earliest` or `latest`.
- **Independent Consumption**
  Multiple consumers can read from the same MQTT Stream independently, each maintaining its own position.
- **Durable by Design**
  Messages are persisted automatically when they match a stream’s topic filter, ensuring resilience against client disconnects.
- **Native MQTT Experience**
  Publishers remain unchanged, while consumers use standard MQTT subscriptions with QoS support to access stream data.
- **Per-Key Ordering**: Strict publish-order delivery for messages sharing the same key (configurable expression), with parallel processing across keys.
- **Last-Value Semantics**: Retain only the latest message per key for state tracking (e.g., device status or digital twins).
- **Retention & Limits**: Time- or size-based policies, plus per-shard caps for controlled storage.

**Example Use Case:** 

In an industrial monitoring system, sensor data published to `sensors/+/readings` is captured by an MQTT Stream. Live dashboards consume data in real time, while analytics pipelines replay historical data from `$s/earliest/sensors/+/readings` for model training. Compliance applications can replay data from a specific incident timestamp, all concurrently from the same durable source.

*Learn more about* [*MQTT Streams*](https://docs.emqx.com/en/emqx/latest/mqtt-stream/mqtt-stream-concept.html)*.*

## Advanced Multi-Tenancy with Enhanced Namespaces

EMQX 6.1.0 enhances Namespace as the foundation for multi-tenant deployments. These improvements make it easier to operate large multi-tenant clusters with clear boundaries and predictable behavior for each tenant.

**Key Enhancements:**

- **Centralized Namespace Configuration**
  Namespace resolution settings (via **Take Namespace From**), isolation options, and authorization behaviors are now grouped together in the Dashboard for simplified management.
- **Automatic Topic Isolation**
  A new `namespace_as_mountpoint` option allows client namespaces to be automatically used as topic mountpoints, enforcing transparent topic separation.
- **Namespaced Authentication and Authorization**
  Built-in authentication and authorization backends now support namespace-specific users and rules, ensuring that tenants only see and affect their own security data.
- **Namespaced Metrics and Observability**
  EMQX now exposes namespace-level metrics for messages, sessions, and data integration operations via Prometheus, as well as JSON-based namespace metrics APIs.
- **Improved Admin Visibility**
  Global administrators can view and manage resources across all namespaces, while still scoping operations to a specific namespace when needed.

**Key Benefits:**

- **Strong Tenant Isolation:** Clear separation of topics, credentials, rules, and metrics across tenants.
- **Operational Simplicity:** Centralized configuration and consistent behavior reduce operational overhead in large deployments.
- **Per-Tenant Observability:** Namespace-scoped metrics enable accurate monitoring, alerting, and usage analysis.

**Example Use Case:** 

A connected fleet SaaS provider derives namespaces from usernames (e.g., `fleetA-client1`). Global settings enable mountpoints and Client ID isolation. Each tenant gets dedicated rate limits, isolated topics/metrics, and namespace-scoped ACLs, delivering secure, scalable multi-tenancy in one cluster.

## New and Enhanced Data Integrations

EMQX 6.1.0 expands data integration capabilities to better support modern time-series databases and secure streaming pipelines.

**New Integrations:**

- [**AWS Timestream for InfluxDB**](https://docs.emqx.com/en/emqx/latest/data-integration/timestream-for-influxdb.html) integration allows EMQX to write MQTT data directly into AWS-managed InfluxDB-compatible time-series storage using InfluxDB Line Protocol, enabling scalable ingestion and real-time analytics without managing database infrastructure.
- [**EMQX Tables**](https://docs.emqx.com/en/emqx/latest/data-integration/emqx-tables.html) integration allows EMQX Enterprise to write MQTT data into EMQX Tables in EMQX Cloud using InfluxDB Line Protocol for centralized time-series storage and analysis.

**Integration Enhancements:**

- **InfluxDB API v3 Support:** Modern API support for both InfluxDB and AWS Timestream connectors.
- **OAuth Authentication for Kafka and Confluent Producers:** Secure, token-based authentication for Kafka-based integrations.
- **Parquet Support in Aggregated Mode:** Azure Blob Storage and S3 Actions now support writing Parquet files for efficient, columnar data storage.

**Example Use Case:** 

Smart grid telemetry is ingested into AWS Timestream for near-real-time analysis, while aggregated Parquet files are periodically written to S3 for long-term storage and regulatory reporting.

## Additional Enhancements and Fixes

### Optimized Durable Storage

This release improves durable storage performance and resource management by introducing durable storage database groups, allowing multiple databases to share resources such as memtable memory and disk usage quotas for better efficiency at scale. The release also adds per-group metrics, configurable storage quotas, along with a new alarm to proactively detect storage quota exhaustion.

### Centralized Certificate Management

Centralized certificate management allows listeners to reference multiple managed certificates. Certificates are selected dynamically based on the client’s SNI during the TLS handshake, with a configurable default fallback.

### **Stability and Reliability Fixes**

Numerous fixes across clustering, message queues, data integrations, gateways, and security improve overall system robustness.

### Unified Dashboard Experience

Style and UX changes to unify the Dashboard and Cloud Console user experience.

*For more information, refer to the* [*Release Notes*](https://www.emqx.com/en/changelogs/enterprise/6.1.0)*.*

## Get Started with EMQX 6.1.0

[Download EMQX 6.1.0](https://www.emqx.com/en/try?tab=self-managed) today, explore the new features, and see how EMQX can power your next-generation IoT and messaging solutions. 

For questions or to discuss your use case, please reach out to our [sales team](https://www.emqx.com/en/contact).



<section class="promotion">
    <div>
        Try EMQX for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
