In [last article](https://www.emqx.com/en/blog/why-emqx-tables-chose-greptimedb) of this series, we explained why our built-in time-series database service, EMQX Tables, chose GreptimeDB as the underlying engine. This article will dive into the storage layer and answer a key question: **How do you cut storage costs by 10x without increasing your budget?**

The answer lies in a decoupled compute and storage architecture.

## The IoT Storage Dilemma

IoT data has one defining characteristic: **a sharp hot/cold divide**.

Data from the last hour gets accessed constantly for real-time dashboards, alerts, and anomaly detection. Data older than a week sees 100x fewer queries. But you can't delete this "cold" data; it's valuable for trend analysis, root cause investigation, and compliance audits.

Traditional time-series databases store everything on high-performance storage. The consequences:

- **High storage costs**: AWS EBS gp3 SSD runs $0.08/GB monthly (us-east-1), which means 10TB costs $9,600 per year in storage alone
- **Shortened retention**: Budget constraints force many teams to keep only 30–90 days of data
- **Scaling doubles costs**: Need more storage? You must add compute too

This is the IoT storage dilemma: **data volumes explode while budgets stay flat**.

## Decoupled Compute and Storage: The Cloud-Native Answer

The core idea is simple: let compute and storage scale independently[^1].

Traditional architectures tightly couple compute nodes and storage. Scaling up means adding compute nodes even when you only need more storage and vice versa.

Decoupled architecture breaks this coupling:

- **Storage layer**: Object storage (S3, GCS, MinIO), low cost, unlimited capacity
- **Compute layer**: Stateless nodes that scale quickly
- **Cache layer**: Bridges object storage latency

Snowflake, Amazon Aurora, and StarRocks all use similar architectures[^2]. But few time-series databases were designed this way from day one. GreptimeDB is one of them.

## GreptimeDB's Storage Architecture

### Object Storage First

GreptimeDB was built with object storage as the primary layer from the start, not retrofitted later[^3].

The cost advantage is straightforward (us-east-1, storage fees only): S3 Standard costs $0.023/GB monthly, 3.5x cheaper than EBS gp3 at $0.08/GB. S3 Glacier Deep Archive costs just $0.001/GB, 80x cheaper. 

For 10TB stored annually: 

- EBS costs ~$9,600
- S3 Standard costs ~$2,760
- S3 Glacier Deep Archive costs as little as ~$120.

But object storage has higher latency. S3's time-to-first-byte typically ranges from 50–100ms, while local SSDs achieve microsecond latency. GreptimeDB solves this with **multi-level caching**.

### LSM Tree: Write-Optimized and Object Storage Friendly

GreptimeDB's storage engine is built on LSM Tree (Log-Structured Merge Tree), a design that aligns perfectly with both time-series workloads and object storage.

**Write optimization**: LSM Tree converts random writes into sequential writes. Incoming data lands in an in-memory buffer (MemTable), then flushes to disk as immutable sorted files (SSTs) when the buffer fills. This batch-oriented, append-only pattern delivers high write throughput, exactly what IoT ingestion demands.

**Object storage compatibility**: Traditional B-tree storage engines update data in place, conflicting with object storage's immutable-object model. LSM Tree's SST files are never modified after creation; updates and deletes go through compaction, which reads existing files and writes new merged files. This "write-once, read-many" pattern maps naturally to object storage semantics, avoiding the costly read-modify-write cycles that plague B-tree engines on S3.

LSM Tree + Parquet + object storage creates a storage stack purpose-built for time-series: high write throughput, efficient compression, and cloud-native scalability.

### Multi-Level Cache Architecture



GreptimeDB's cache design borrows from OS layering principles[^4]:

![](https://assets.emqx.com/images/61c684010abf054e5389d57b9ff6cce5.png)

Query latency varies by data "temperature":

- **Hot data** (last few hours): Hits memory cache or Write Cache, millisecond latency when cached, comparable to local storage
- **Warm data** (recent history): Reads from Write Cache, low latency when cached
- **Cold data** (long-term history): First query hits object storage, hundreds of milliseconds to seconds. But Parquet's column pruning and predicate pushdown reduce actual read volume, and data backfills to local cache for faster subsequent access

The core value: **store data at object storage prices, access hot data at local disk speeds** (when cache hits).

### Parquet Columnar Format

GreptimeDB uses Apache Parquet as its data file format[^5], ideal for IoT workloads.

IoT queries typically need only a few columns. This query needs just 4:

```sql
SELECT avg(temperature), max(pressure)
FROM device_metrics
WHERE device_id = 'sensor_001'
  AND ts BETWEEN '2025-01-01' AND '2025-01-07'
```

Row-oriented storage (like CSV) reads entire rows even when you need 2 fields. Parquet reads only `temperature`, `pressure`, `device_id`, and `ts`, skipping everything else.

Columnar storage also compresses better. Values in a column share data types and similar distributions, so Parquet can choose optimal encodings per column:

- **Dictionary Encoding**: Low-cardinality columns (device types, status codes) use dictionary indexes instead of raw values
- **Run-Length Encoding**: Consecutive identical values store one value plus a repeat count
- **Delta Encoding**: Monotonically increasing sequences like timestamps store only differences

Parquet files are typically 5–50x smaller than uncompressed CSV. Time-series data, with its regular timestamps and repeated tag values, often achieves compression at the higher end of this range[^6].

Parquet is also the data lake standard. Data in GreptimeDB's object storage can be accessed by Spark, Presto, and Athena via external tables or direct path reads for downstream analytics and machine learning.

### Time-Series Compression Optimizations

GreptimeDB applies further optimizations for time-series data: file-level ZSTD compression (optimal balance of ratio and speed); DELTA_BINARY_PACKED encoding for timestamp columns, storing only differences, millisecond-precision data has small deltas, yielding significant compression; internal sequence numbers also use delta encoding.

In comparison tests against TimescaleDB, **GreptimeDB achieved 18x better compression on the same dataset**. We'll share detailed methodology (including dataset, schema, hardware specs, and software versions) in an upcoming benchmark report.

### High-Cardinality Optimization

IoT has another common challenge: **high-cardinality primary keys**.

When primary keys include request IDs, trace IDs, or user tokens, some traditional time-series database layouts struggle; maintaining separate memory buffers per series causes memory to explode and write performance to degrade at millions of series.

GreptimeDB 1.0 beta introduced **flat format**[^7] to address this: BulkMemtable no longer allocates separate buffers per series; the new Parquet layout stores tag columns independently for better predicate pushdown; multi-series merge-dedupe paths reduce high-cardinality overhead.

In benchmarks with 2 million series, flat format achieved **4x write throughput** and **up to 10x query speedup** versus the traditional layout.

## Limitations of Traditional Solutions

### TimescaleDB

TimescaleDB builds on PostgreSQL, inheriting its mature ecosystem and some architectural constraints: 

- PostgreSQL's storage engine targets OLTP with limited object storage support.
- Distributed features are available in TimescaleDB's managed offering.
- Scaling often requires data migration rather than simply adding storage capacity.

### InfluxDB

InfluxDB pioneered time-series databases, but architectural evolution created challenges: 

- v1/v2 used local storage without native object storage support.
- v3 (InfluxDB 3.0) rewrote the storage engine with different deployment options across editions.
- Major version upgrades typically require migration planning.

This is "cloud-adapted" versus "cloud-native": patching traditional architectures versus designing for cloud from scratch.

## Real-World Value for IoT

### Cost and Retention

A mid-sized IoT project adding 1TB monthly and retaining 2 years (24TB total). Estimates below are for us-east-1, storage fees only; actual costs vary with requests, retrieval, data transfer, and operational overhead:

| Approach         | Annual Storage Cost | Notes                                                        |
| :--------------- | :------------------ | :----------------------------------------------------------- |
| Traditional EBS  | ~$23,000            | All on gp3 SSD                                               |
| Decoupled        | ~$6,600             | All on S3 Standard                                           |
| Hot/Cold Tiering | ~$1,100–$3,000      | 3TB hot (S3 Standard) + 21TB cold (Glacier Deep Archive); range accounts for request/retrieval costs |

**Same data, 3–10x lower cost**. The result is: 3 months of retention becomes 3 years. Long-term retention matters for IoT: seasonal patterns, equipment aging, compliance, and root cause analysis all need historical data.

### True Elastic Scaling

This is decoupled architecture's most underrated advantage.

Scaling traditional databases isn't just "add machines". You must scale compute and storage together. New nodes replicate data from existing nodes, consuming time and bandwidth. Data redistributes across nodes, potentially impacting production. Scaling down requires migrating data, even riskier.

These problems are acute in IoT: millions of devices, wildly fluctuating write volumes. Traditional architectures can't scale fast enough.

Decoupled architecture solves this:

- **Storage is inherently elastic**: S3/GCS scale on demand, no "storage expansion" needed
- **Built-in high availability**: Major object storage services provide multi-replica durability; cross-AZ replication depends on storage class and configuration
- **Stateless compute**: Adding nodes doesn't require data replication; removing nodes doesn't require migration
- **Rapid scaling**: New compute nodes can be ready in minutes with containerized deployments

IoT write volumes vary dramatically: devices batch-connect during launches, collection frequency spikes during promotions, and seasonal factors shift power patterns. Decoupled architecture lets you scale compute up during peaks and down during troughs, without worrying about storage capacity.

**This is what "elastic" really means**, not just "can scale" but "scaling has minimal overhead".

## What's Next

The storage engine solves "where does data go." But when millions of devices write simultaneously, how do you prevent collapse?

Part 3 will explore GreptimeDB's distributed design: how Frontend, Datanode, and Metasrv coordinate; how Regions partition data; and how failures are recovered. Please stay tuned.

Ready to try an IoT time-series solution? Experience [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) today.

[^1]: [Separation of Storage and Compute - David Gomes](https://davidgomes.com/separation-of-storage-and-compute-and-compute-compute-separation-in-databases/)
[^2]: [Learnings from Snowflake and Aurora - SingleStore](https://www.singlestore.com/blog/separating-storage-and-compute-for-transaction-and-analytics/)
[^3]: [GreptimeDB Storage Architecture Deep Dive](https://greptime.com/blogs/2025-03-26-greptimedb-storage-architecture)
[^4]: [GreptimeDB Storage Engine Design](https://greptime.com/blogs/2022-12-21-storage-engine-design)
[^5]: [Apache Parquet](https://parquet.apache.org/)
[^6]: [What is Parquet - Databricks](https://www.databricks.com/glossary/what-is-parquet)
[^7]: [High-Cardinality Optimization: GreptimeDB's Flat Format](https://greptime.com/blogs/2025-12-22-flat-format)
