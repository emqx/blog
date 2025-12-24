EMQ recently launched [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables), a fully managed time-series database service built into EMQX Cloud. Among all the time-series databases available, EMQX Cloud chose GreptimeDB as the underlying engine.

Behind this decision lies a fundamental question: **What kind of time-series database does IoT actually need?**

The traditional answer is InfluxDB or TimescaleDB. Both are solid products that solved their era's problems. But IoT data infrastructure requirements are changing, and these changes are exactly what GreptimeDB was designed to address.

## Three New Challenges in IoT Data

### Challenge 1: Data Explosion, Flat Budgets

A decade ago, a mid-sized IoT project might have had a few thousand devices generating GB-scale data daily. Today, the same project might have hundreds of thousands of devices producing TB or even PB-scale data.

But infrastructure budgets haven't grown proportionally. **Storage cost has become the primary factor in time-series database selection.**

Most traditional time-series databases were designed in early cloud days, defaulting to local SSDs or block storage (like AWS EBS). GreptimeDB, by contrast, was designed from the ground up with object storage (like AWS S3) as its primary storage layer. Using AWS as an example:

| Storage Type  | Price ($/GB/month) | 10TB Annual Cost |
| :------------ | :----------------- | :--------------- |
| EBS gp3 (SSD) | $0.08              | $9,600           |
| S3 Standard   | $0.023             | $2,760           |
| S3 Glacier    | $0.004             | $480             |

That's a **3–20x** difference. At PB scale, this gap determines project viability.

### Challenge 2: Beyond Metrics: Logs and Traces Too

Early IoT projects focused on device metrics, like temperature, pressure, and status codes. But modern IoT observability needs go further:

- **Metrics**: Device operational status
- **Logs**: Device events, error messages  
- **Traces**: Request chains, call relationships

The traditional solution: deploy multiple systems. InfluxDB for metrics, Elasticsearch for logs, Jaeger for traces. Three systems mean triple the operational cost, and data silos make troubleshooting painful. When a device fails, you're jumping between three systems, manually correlating timestamps.

### Challenge 3: Elastic Scaling, Not Capacity Planning

IoT data volumes fluctuate significantly. Product launches, promotions, and seasonal factors cause data spikes.

Traditional databases require upfront capacity planning with reserved resources. Over-provision and you waste money; under-provision and services degrade. Modern IoT infrastructure needs to use databases like utilities: scale on demand, pay for what you use.

## Why Traditional Solutions Struggle

### InfluxDB: Great Start, Uncertain Direction

InfluxDB pioneered the time-series database space and defined industry standards (like Line Protocol). But its evolution has confused users:

- **Version fragmentation**: v1, v2, and v3 are essentially three different products. v1 uses InfluxQL, v2 pushed Flux, v3 returns to SQL. Each upgrade is a migration project.
- **Flux's sunset**: The Flux language that InfluxDB v2 championed has been officially deprecated. All investment in learning Flux and Flux code needs reevaluation.
- **Open-source ceiling**: InfluxDB open-source only supports single-node deployment; clustering requires enterprise licensing. At large scale, this is a hard constraint.
- **Metrics only**: InfluxDB focuses on time-series metrics and doesn't natively support logs or traces. For complete observability, you still need Elasticsearch and Jaeger.

InfluxDB still works for small-to-medium scale, metrics-only scenarios. But for IoT platforms needing long-term evolution, version uncertainty and feature limitations are risks.

### TimescaleDB: PostgreSQL's Maturity and Limits

TimescaleDB builds on PostgreSQL, its biggest advantage. Mature ecosystem, familiar SQL, rich tooling. If your team knows PostgreSQL well, TimescaleDB's learning curve is nearly zero.

But PostgreSQL's architecture brings constraints:

- **Scalability requires Enterprise**: Open-source is mainly vertical scaling. Distributed Hypertables are enterprise-only.
- **Cloud-native isn't native**: PostgreSQL was designed for on-premise. It runs on cloud, but object storage support is limited; it can't fully leverage cloud storage cost advantages.
- **Single data model**: Focused on time-series; logs and traces need other systems.

TimescaleDB works well for "PostgreSQL-first" teams, or where time-series is just a small application feature. But for IoT platforms where time-series is core, its architecture isn't optimal.

## GreptimeDB's Design Choices

GreptimeDB is young. That's both a disadvantage (less mature ecosystem) and an advantage (designed from scratch for current needs).

### Design Choice 1: Object Storage First

From day one, GreptimeDB uses object storage (S3/GCS/MinIO) as the primary storage layer, not a feature bolted on later. Data is stored in Apache Parquet columnar format, naturally suited for analytical queries.

Object storage latency is solved through multi-tier caching, write cache handles hot data, read cache accelerates historical queries, metadata cache optimizes query planning.

Beyond cost savings, object storage enables extended data retention. Traditional solutions with expensive storage often retain only months of data. With object storage, you can affordably keep years of historical data. This matters for:

- **Data analysis**: Long-term trend analysis, seasonal pattern discovery
- **Compliance**: Meeting regulatory data retention requirements
- **Incident investigation**: Tracing historical failures, reproducing issue scenarios

**If you can afford to store it, you can actually use it.**

> Storage architecture details coming in Part 2: "Cloud-Native Storage Engine."

### Design Choice 2: Performance-to-Cost Ratio

Object storage is the foundation, but what users ultimately care about is the performance-to-cost ratio: how much performance can the same budget deliver?

In benchmark tests under identical hardware conditions, GreptimeDB shows significant advantages:

- **Write throughput**: Multiple times higher than InfluxDB open-source
- **Query latency**: Lower average response time, more stable P99 tail latency
- **Reliability**: All queries complete successfully, no timeouts

Combined with storage costs (S3 $0.023/GB vs EBS $0.08/GB), GreptimeDB delivers more data, faster queries, and longer retention on the same budget.

> We'll provide a complete performance benchmark report in Part 4 "The Secret to Faster IoT Queries," including detailed comparisons of write throughput, query latency, and resource consumption.

### Design Choice 3: Unified Data Model

GreptimeDB isn't just a time-series database; it can also serve as an observability database. Metrics, Logs, and Traces are stored and queried in the same engine.

This isn't just about fewer systems to operate. It's about connecting the data. When a device fails, one SQL query retrieves metric spikes, related logs, and call traces, no manual piecing across three systems.

By contrast, InfluxDB only handles Metrics. TimescaleDB can store arbitrary data but lacks native optimization for logs and traces. GreptimeDB is designed from storage format to query engine for observability use cases.

### Design Choice 4: Open-Source Means Distributed

This is a key differentiator from InfluxDB and TimescaleDB: the open-source version includes full distributed cluster support.

InfluxDB clustering requires Enterprise licensing. TimescaleDB's Distributed Hypertables are also enterprise-only. GreptimeDB's distributed architecture has been open-source from day one—Frontend, Datanode, and Metasrv components are all available under Apache 2.0.

This means:

- **No vendor lock-in**: You have full control over your data and infrastructure, with flexibility to choose your deployment model based on business needs
- **Architectural consistency**: Whether you choose open-source deployment or managed services (like GreptimeCloud or EMQX Tables), the underlying architecture is identical—migration is frictionless

> Distributed architecture details coming in Part 3: "Supporting Million-Device Data Ingestion."

### Design Choice 5: Protocol Compatibility and PromQL Support

Migration cost is a hidden cost in database selection. GreptimeDB supports:

- **InfluxDB Line Protocol**: Existing InfluxDB/Telegraf pipelines work unchanged
- **Prometheus Remote Write**: Seamless Prometheus ecosystem integration
- **OpenTelemetry (OTLP)**: Cloud-native observability standard
- **SQL + PromQL**: Query languages covering both major camps

PromQL support deserves special mention. If your monitoring stack is built on Prometheus, existing Grafana dashboards and alert rules migrate directly to GreptimeDB, no rewrites needed. InfluxDB doesn't support PromQL, meaning migrating from the Prometheus ecosystem to InfluxDB requires rewriting all queries.

Migrating from InfluxDB? Keep using Line Protocol for writes while gradually moving queries from InfluxQL to SQL. Migration is incremental, not big-bang.

GreptimeDB also provides capabilities that make post-migration evolution easier:

- **Schemaless writes**: No need to define table schemas upfront—tables and columns are created automatically on write, ideal for IoT scenarios with diverse device types
- **Range Query**: Native SQL support for time-window aggregation, similar to PromQL's Range Selector, with clean unified syntax
- **Flow Engine**: Built-in stream processing—define continuous aggregation with SQL, compute as data arrives
- **Trigger Alerting**: Define alerting rules with SQL, send notifications via Webhook, compatible with Prometheus Alertmanager

## Why EMQX + GreptimeDB

EMQX is a leading global [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison); GreptimeDB is a next-generation observability database. The combination logic is clear:

- **EMQX solves connectivity**: Million-device MQTT access, message routing, and protocol conversion.
- **GreptimeDB solves storage**: Efficient storage of massive time-series data, real-time queries, long-term archival.
- **EMQX Tables solves integration**: Native MQTT integration, automatic schema inference, unified management console.

For IoT developers, the complete pipeline from device connection to data analysis runs on a single platform.

## Series Preview

This is Part 1 of the "How GreptimeDB Powers EMQX Tables" series. Upcoming articles dive into technical details:

- **Part 2: Cloud-Native Storage Engine** — Parquet format, multi-tier caching, compression strategies
- **Part 3: Distributed Architecture** — Supporting million-device concurrent writes
- **Part 4: Query Optimizer** — Complete performance benchmarks + the technical principles behind faster IoT queries

Looking for an IoT time-series solution? Try [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) for a quick experience, or [contact our expert](https://www.emqx.com/en/contact?product=cloud) for a customized solution.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
