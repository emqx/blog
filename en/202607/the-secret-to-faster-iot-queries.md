> EMQX Tables Technical Series Part 4 (final): the complete benchmark report (2.17x write throughput, up to 67x faster queries, 1/18 the storage) plus a walk through the storage engine internals that produce these numbers.

This series has covered why EMQX Tables chose GreptimeDB ([Part 1](https://www.emqx.com/en/blog/why-emqx-tables-chose-greptimedb)), how its cloud-native storage engine cuts storage costs ([Part 2](https://www.emqx.com/en/blog/cloud-native-storage-engine-how-greptimedb-cuts-iot-storage-costs-by-10x)), and how its distributed architecture scales from one node to a cluster ([Part 3](https://www.emqx.com/en/blog/elastic-at-every-scale)). One question remains: when your dashboard fires a query against a billion rows of device telemetry, how fast does the answer come back?

This article answers with numbers. It walks through our TSBS benchmark against TimescaleDB, compares the results with our earlier InfluxDB report, and, most importantly, explains *why* the numbers look the way they do by tracing each result back to specific mechanisms in GreptimeDB's storage engine and query optimizer. Part 2 promised the full methodology behind the "18x compression" claim. This is that report.

## Key Findings



- Write throughput: GreptimeDB ingests at **2.17x** the rate of TimescaleDB (285,301 vs. 131,531 rows/sec)
- Query latency: GreptimeDB is faster in **13 of 15** TSBS query types, with speedups up to **67x**
- Storage footprint: GreptimeDB uses **1/18** the disk space (1.1 GB vs. 20 GB) for the same 103.6 million rows
- Honest caveat: TimescaleDB wins two query types, `lastpoint` and `groupby-orderby-limit`, where PostgreSQL's B-tree indexes shine
- Against InfluxDB v2 (from our [2024 report](https://greptime.com/blogs/2024-08-07-performance-benchmark)): over 2x write throughput, 2–11x faster on heavy queries, and GreptimeDB completed a 1.15-billion-row ingestion test that InfluxDB's open-source version could not finish

## Methodology



We used [TSBS](https://github.com/timescale/tsbs) (Time Series Benchmark Suite), which the TimescaleDB team itself develops. If the benchmark has a home-field advantage, it favors TimescaleDB, not us. Data and queries are pre-generated from the same pseudo-random seed, so both databases load identical data and answer identical queries. We ran the tests with [GreptimeDB's fork](https://github.com/GreptimeTeam/tsbs), which adds a GreptimeDB target; the TimescaleDB loader and query generators are upstream TSBS code.

| Component   | Configuration                       |
| :---------- | :---------------------------------- |
| Instance    | AWS c5d.2xlarge (8 vCPU, 16 GB RAM) |
| OS          | Ubuntu 24.04 LTS                    |
| Storage     | 300 GB gp3 EBS volume               |
| GreptimeDB  | v1.0.0-beta.2                       |
| TimescaleDB | TimescaleDB 2.x on PostgreSQL 17    |

The benchmark ran on GreptimeDB v1.0.0-beta.2. The current release line is v1.1.x, which added further query optimizations on top of these results; we cover those at the end of the engine internals section.

For the query phase, we restarted both databases after ingestion, then ran each query type repeatedly (10–100 runs per type; exact counts are in the reproduction steps) and report the mean latency from TSBS's run logs.

### The Dataset, in IoT Terms



The `cpu-only` scenario simulates 4,000 hosts reporting 10 metrics every 10 seconds for 3 days: 103.6 million rows, over 1 billion individual metric values. Each record carries 10 tags (hostname, region, datacenter, rack, os, arch, team, service, service_version, service_environment) and 10 numeric fields (usage_user, usage_system, and so on).

Rename the columns and this is exactly the shape of IoT telemetry flowing through an MQTT broker: a fleet of 4,000 devices, each identified by a set of metadata tags (device ID, site, firmware version, hardware revision), each reporting a batch of sensor readings on a fixed interval. The query types map to real IoT work too:

| TSBS Query Type          | IoT Equivalent                                    |
| :----------------------- | :------------------------------------------------ |
| cpu-max-all-{1,8}        | Peak readings across the fleet over N hours       |
| single-groupby-X-Y-Z     | Drill into X metrics for Y devices over Z hours   |
| double-groupby-{1,5,all} | Fleet-wide hourly trends, compared per device     |
| high-cpu-{1,all}         | Find devices exceeding a threshold (anomaly scan) |
| lastpoint                | Current status of every device                    |
| groupby-orderby-limit    | Top-N leaderboard (e.g., hottest devices)         |

## Write Performance: 2.17x



Batch size 10,000, 8 concurrent workers, both databases on the same machine and disk, each loaded with its default TSBS-generated schema.

| Metric     | TimescaleDB      | GreptimeDB       | Comparison           |
| :--------- | :--------------- | :--------------- | :------------------- |
| Write rate | 131,531 rows/sec | 285,301 rows/sec | **2.17x**            |
| Disk usage | 20 GB            | 1.1 GB           | **1/18 the storage** |

Disk usage is the data directory size on disk after the load completed. The second row deserves as much attention as the first: 103.6 million rows landed in 1.1 GB on GreptimeDB and 20 GB on TimescaleDB. For an IoT platform ingesting a terabyte of telemetry a month, that ratio decides whether you keep 90 days of history or keep everything. Part 2 explained the cost math; this is the measurement behind it.

## Query Performance: 13 of 15



### Where GreptimeDB Wins



| Query Type            | TimescaleDB (ms) | GreptimeDB (ms) | Speedup  |
| :-------------------- | :--------------- | :-------------- | :------- |
| cpu-max-all-8         | 6,012            | 89              | **67x**  |
| single-groupby-1-1-12 | 571              | 9               | **62x**  |
| high-cpu-1            | 623              | 16              | **39x**  |
| single-groupby-1-8-1  | 439              | 20              | **22x**  |
| cpu-max-all-1         | 411              | 23              | **18x**  |
| single-groupby-5-1-12 | 166              | 14              | **12x**  |
| double-groupby-1      | 8,559            | 1,028           | **8.3x** |
| single-groupby-1-1-1  | 54               | 7               | **7.7x** |
| double-groupby-5      | 7,654            | 1,566           | **4.9x** |
| double-groupby-all    | 10,717           | 2,270           | **4.7x** |
| single-groupby-5-8-1  | 95               | 29              | **3.2x** |
| high-cpu-all          | 8,731            | 5,661           | **1.5x** |
| single-groupby-5-1-1  | 15               | 10              | **1.5x** |

The pattern: the more data a query touches, the wider the gap. `cpu-max-all-8`, the peak of all 10 metrics across every device over 8 hours, drops from 6 seconds to 89 milliseconds. On a live operations dashboard, that's the difference between a panel that refreshes and a panel that spins.

### Where TimescaleDB Wins



| Query Type            | TimescaleDB (ms) | GreptimeDB (ms) | TimescaleDB Advantage |
| :-------------------- | :--------------- | :-------------- | :-------------------- |
| groupby-orderby-limit | 122              | 728             | **6x**                |
| lastpoint             | 131              | 1,131           | **8.7x**              |

No spin here: `lastpoint` (latest value per device) and `groupby-orderby-limit` (aggregate, sort, take top N) are classic B-tree territory, and PostgreSQL's B-tree indexes are excellent at them. GreptimeDB has a planned optimization for the lastpoint pattern in an upcoming release. Until then, if your workload is dominated by high-frequency "show me the current value of every device" queries, factor these two rows into your decision. We'll come back to why this happens in the engine internals section.

## What About InfluxDB?



Part 3 promised a comparison against InfluxDB as well. We published a full TSBS report in [August 2024](https://greptime.com/blogs/2024-08-07-performance-benchmark), which tested GreptimeDB v0.9.1 against InfluxDB v2 (v3 was not yet stable at the time) on the same `cpu-only` scenario and dataset size. The versions are older, so read these numbers as a snapshot from that date rather than a current measurement; the report documents the exact setups. The findings:

- GreptimeDB's write throughput was more than **2x** InfluxDB's.
- On queries scanning 12 hours of data across all hosts (`double-groupby-*`, `high-cpu-all`) and on sorting queries (`groupby-orderby-limit`, `lastpoint`), GreptimeDB was **2–11x faster**.
- On small queries, InfluxDB was slightly faster, with both databases responding in the same order of magnitude.
- With local caching enabled, the report measured GreptimeDB's read/write performance on S3 as comparable to EBS. That's the object storage architecture from Part 2, measured.

Notice something interesting: `lastpoint` and `groupby-orderby-limit`, the two queries GreptimeDB loses to TimescaleDB, are queries it *won* against InfluxDB. Point lookups and top-N sorts aren't a general GreptimeDB weakness; they're a specific PostgreSQL B-tree strength. That distinction matters when you're reading benchmark tables.

### The 1.15-Billion-Row Test



The 2024 report also scaled the dataset to 400,000 hosts: 1.15 billion rows, roughly 380 GB of generated data. In IoT terms, that's a large connected-vehicle or smart-meter fleet, not an exotic scenario.

InfluxDB's open-source version could not complete the ingestion. Writes failed with a `cache-max-memory-size exceeded` error; raising the limit and upgrading to a 24-core machine didn't resolve it. Throughput degraded to around 20,000 rows per second, triggering TSBS backpressure, and the database was practically unavailable while writes were in flight.

GreptimeDB, deployed as a cluster with the table split into 8 regions partitioned by hostname, sustained 250,000–360,000 rows per second and completed the load. This is the distributed architecture from Part 3 doing its job: when one node isn't enough, you add nodes, in the open-source version. A [reproduction manual](https://github.com/GreptimeTeam/tsbs/blob/master/docs/greptimedb-vs-influxdb-manual.md) is available for that test as well.

## Where the Speed Comes From



Benchmark tables tell you *what*; they don't tell you *why*. The "why" is what makes a result trustworthy and predictive for your workload. The internals below describe the current GreptimeDB release (v1.1.x); the core mechanisms were already in the benchmarked version, and everything is verifiable in [GreptimeDB's source code](https://github.com/GreptimeTeam/greptimedb) (Apache 2.0). We cite the relevant modules as we go.

### Why Writes Are 2.17x Faster and 18x Smaller



GreptimeDB's Mito Engine is an LSM-Tree: incoming rows append to a write-ahead log (WAL), accumulate in an in-memory memtable, and flush to immutable Parquet files (`src/mito2`). There are no in-place page updates and no B-tree maintenance on the hot write path; ingestion is mostly sequential batch I/O, which is exactly what an 8-worker, 10,000-row batch workload rewards. TimescaleDB inherits PostgreSQL's heap-and-B-tree write path. Hypertable partitioning helps, but every insert still pays for index maintenance.

The 18x storage gap comes from how those Parquet files are encoded. Because Parquet stores each column contiguously, similar values sit next to each other, and the writer (`src/mito2/src/sst/parquet/writer.rs`) applies two specific choices on top of that layout: ZSTD compression across the file, and DELTA_BINARY_PACKED encoding on the timestamp column. Device telemetry timestamps arrive at nearly fixed intervals, so storing deltas instead of absolute values collapses an 8-byte timestamp into a few bits. Repetitive tag columns (region, firmware version, device type) compress down to almost nothing under Parquet's dictionary encoding. This is the methodology behind Part 2's 18x figure: same dataset, same schema (10 tags + 10 fields), hardware and versions as listed above, measured as on-disk footprint after full ingestion.

### Why Big Scans Are Up to 67x Faster: The Pruning Pipeline



The 67x result on `cpu-max-all-8` is not one optimization. It's a pipeline of pruning steps, each discarding data before the next step pays to read it. In order:

1. **File-level time pruning.** Every SST file records its time range. The scan planner (`src/mito2/src/read/scan_region.rs`) drops entire files (and entire memtables) whose range doesn't intersect the query window. An 8-hour query over 3 days of data skips most of the dataset without a single byte of I/O.
2. **Row-group pruning via min-max statistics.** Within surviving files, Parquet stores min/max values for each row group, a horizontal slice of the file. The reader (`src/mito2/src/sst/parquet/reader.rs`) evaluates query predicates against these statistics first and skips row groups that can't match.
3. **Index-based pruning.** GreptimeDB maintains inverted indexes and bloom filters in companion [Puffin](https://iceberg.apache.org/puffin-spec/) files (`src/mito2/src/sst/index`). A predicate like `hostname = 'host_2043'` consults the index instead of scanning. This is what turns `high-cpu-1` (threshold scan on one device) into a 16 ms query.
4. **Row-level selection.** Index hits convert into fine-grained Parquet row selections (`src/mito2/src/sst/parquet/row_selection.rs`), so the reader decodes only matching row ranges within a row group, not the whole group.
5. **Late materialization.** A prefilter stage (`src/mito2/src/sst/parquet/prefilter.rs`) reads only the columns referenced by filters, computes the final row selection, and only then fetches the remaining columns for surviving rows.

Each stage multiplies the previous one's savings. By the time actual decompression happens, a query that nominally targets 103 million rows reads only the row ranges and columns that survived pruning — a small fraction of the data on disk. TimescaleDB's row-oriented heap must read full rows from every chunk the time filter admits, then discard the unneeded columns after the I/O has already been paid.

This pipeline is what Part 3 meant by "column pruning and predicate pushdown": predicates push down from the SQL layer through the query planner into every one of these stages.

### Why Multi-Device Aggregations Parallelize Well



Whatever survives pruning flows into a query engine built on [Apache DataFusion](https://datafusion.apache.org/), which uses vectorized execution: it processes columnar batches instead of individual rows, keeping CPU caches warm. GreptimeDB adds its own optimizer rules on top (`src/query/src/optimizer`). `parallelize_scan` splits a scan into partition ranges so all 8 cores work simultaneously, and `windowed_sort` exploits the fact that data files are organized into time windows and already sorted by timestamp within them, turning `ORDER BY ts` into a cheap merge instead of a full sort. That's the machinery behind the 22x result on `single-groupby-1-8-1`: eight devices' series scanned and aggregated in parallel.

### Why `lastpoint` Loses (For Now)



The same architecture explains the two losing queries. "Latest value per device" is a point lookup, and a B-tree hands PostgreSQL the answer almost for free: descend the index, read one row. An LSM engine instead locates the newest data per series across memtables and recent SST files and merges. GreptimeDB already has a fast path that pushes `last_value` aggregations down to the storage layer with a dedicated cache (`src/query/src/optimizer/scan_hint.rs`), and extending it to cover more query shapes, including the one TSBS's `lastpoint` uses, is planned optimization work. We'd rather show you the two red rows and explain them than publish a 15-for-15 table you shouldn't trust.

### Since the Benchmark: v1.1 Made This Faster



These numbers come from v1.0.0-beta.2, and the engine hasn't stood still. The v1.1 release line ([v1.1.0 released June 2026](https://github.com/GreptimeTeam/greptimedb/releases/tag/v1.1.0); current release v1.1.2) sharpened the read path further:

- The late-materialization prefilter (stage 5 above), plus a prefilter result cache and remote dynamic filtering on Datanodes, cut unnecessary row reads. With prefiltering enabled, the TSBS `cpu-max-all-8` query — the 67x headline result in this article — ran another **4.5x faster** in our v1.1 testing.
- Parquet page-index reads and range cache reuse reduce how much data scans fetch from storage; in one workload, page-index reads cut SST bytes fetched by **93.2%**.
- PromQL range functions like `rate` and `increase` sped up by as much as 97%, with end-to-end PromQL latency down 20–40% versus v1.0. Relevant if your Grafana dashboards query GreptimeDB through PromQL.

In other words: rerun this benchmark on the current release and the winning rows get faster. The two losing rows are the ones with a named optimization on the roadmap.

## What This Means for an IoT Workload



Match the query patterns to what your platform actually does all day:

| Your Workload                              | Dominant Pattern                   | Better Fit                                             |
| :----------------------------------------- | :--------------------------------- | :----------------------------------------------------- |
| Historical dashboards, trend analysis      | Large time-range aggregation       | GreptimeDB (up to 67x)                                 |
| Fleet-wide anomaly scans                   | Threshold filter across devices    | GreptimeDB (up to 39x)                                 |
| High-frequency ingestion from large fleets | Sustained batch writes             | GreptimeDB (2.17x single-node; scales out, see Part 3) |
| Long retention on a budget                 | Storage efficiency                 | GreptimeDB (1/18 footprint)                            |
| "Current status" board polled every second | `lastpoint`                        | TimescaleDB today; GreptimeDB optimization planned     |
| Deep PostgreSQL ecosystem dependency       | PostgreSQL ecosystem compatibility | TimescaleDB                                            |

For most IoT platforms, ingestion volume and time-range analytics dominate by orders of magnitude: every dashboard panel, every alert rule evaluation, every retrospective analysis is a time-range scan. That's the part of the table where the gaps are largest. A practical note on `lastpoint`, too: in many real deployments, the "current status" problem is served from a continuously maintained aggregation rather than repeated raw-table queries. GreptimeDB's Flow Engine can maintain exactly that (and v1.1 added experimental incremental reads, so append-only Flows no longer rescan the whole source table), so raw `lastpoint` latency matters less than the benchmark row suggests.

If you're running EMQX, this is the engine underneath [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables): MQTT telemetry routes from the broker through EMQX's built-in rule engine into GreptimeDB-backed tables, with no external pipeline to build, and the query characteristics measured here are what your SQL and PromQL hit.

## Reproduce It



Benchmark results deserve skepticism, especially from a vendor. Here are the core steps:

```shell
# Build the TSBS fork with GreptimeDB support
git clone https://github.com/GreptimeTeam/tsbs.git && cd tsbs && make

# Generate identical data for both targets (seed=123)
./bin/tsbs_generate_data --use-case="cpu-only" --seed=123 --scale=4000 \
    --timestamp-start="2023-06-11T00:00:00Z" --timestamp-end="2023-06-14T00:00:00Z" \
    --log-interval="10s" --format="influx" > influx-data.lp
# ... repeat with --format="timescaledb" for TimescaleDB
```

The complete command list, covering query generation for all 15 types, run counts per type, load parameters, and result extraction (`grep "mean:"` on the run logs), is in the [GreptimeDB TSBS fork](https://github.com/GreptimeTeam/tsbs). Hardware, data scale, and query mix all shift results; run it on a machine shaped like your production environment before you decide anything.

## Series Wrap-Up



Four articles, one argument:

- [Part 1](https://www.emqx.com/en/blog/why-emqx-tables-chose-greptimedb): IoT data infrastructure needs changed (object storage economics, unified observability data, open-source distributed clustering), and that's why EMQX Tables runs on GreptimeDB.
- [Part 2](https://www.emqx.com/en/blog/cloud-native-storage-engine-how-greptimedb-cuts-iot-storage-costs-by-10x): the decoupled compute and storage architecture, Parquet on object storage behind multi-level caches, cuts storage cost by 3–10x and makes multi-year retention affordable.
- [Part 3](https://www.emqx.com/en/blog/elastic-at-every-scale): the Frontend/Datanode/Metasrv architecture scales from one node to a cross-region cluster, with Region migration as a metadata operation.
- Part 4 (this article): measured against TimescaleDB and InfluxDB, the architecture delivers 2.17x writes, up to 67x queries, and 1/18 the storage, for reasons you can trace in the source code—and the current v1.1.x release is faster still.

To see it with your own data: connect a device fleet to [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) and route MQTT telemetry straight into it, or deploy open-source [GreptimeDB](https://github.com/GreptimeTeam/greptimedb) and point the TSBS fork at it.

## References

[**1**]    [TSBS Official Repository](https://github.com/timescale/tsbs)

[**2**]    [GreptimeDB TSBS Fork](https://github.com/GreptimeTeam/tsbs)

[**3**]    [GreptimeDB vs. InfluxDB Benchmark (Aug 2024)](https://greptime.com/blogs/2024-08-07-performance-benchmark)

[**4**]    [GreptimeDB vs. InfluxDB Reproduction Manual](https://github.com/GreptimeTeam/tsbs/blob/master/docs/greptimedb-vs-influxdb-manual.md)

[**5**]    [GreptimeDB Storage Engine Design](https://greptime.com/blogs/2022-12-21-storage-engine-design)

[**6**]    [GreptimeDB Source Code](https://github.com/GreptimeTeam/greptimedb) — Mito engine (`src/mito2`), Parquet writer encodings (`src/mito2/src/sst/parquet/writer.rs`), scan pruning (`src/mito2/src/read/scan_region.rs`, `src/mito2/src/sst/parquet/reader.rs`), indexes (`src/mito2/src/sst/index`), optimizer rules (`src/query/src/optimizer`)

[**7**]    [GreptimeDB v1.1.0 Release](https://github.com/GreptimeTeam/greptimedb/releases/tag/v1.1.0)

[**8**]    [Apache DataFusion](https://datafusion.apache.org/)

[**9**]    [Apache Parquet](https://parquet.apache.org/)
