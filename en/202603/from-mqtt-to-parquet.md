Modern IoT systems generate massive streams of MQTT messages. Getting value from this data means more than just moving it around; you need to store it efficiently and make it easy to query.

With EMQX’s Amazon S3 integration and **Parquet** support for aggregated uploads, you can turn your MQTT broker into a powerful data ingestion layer for your data lake. In this post, we’ll walk through a practical use case: **Persist MQTT messages to S3 in Parquet format, then analyze them with DuckDB.**

We already cover the configuration details in our documentation for exporting aggregated data in Parquet to **Amazon S3** and other storages. Here, we’ll focus on the *end-to-end workflow* and what it enables for your IoT analytics.

## **Why Parquet for MQTT Data?**

Before jumping into the example, let’s clarify why Parquet is a great fit for MQTT workloads:

- **Columnar storage**: Ideal for analytical queries (e.g., “avg temperature by device per hour”), since only the needed columns are scanned.
- **High compression**: Typically **much smaller** than CSV, reducing S3 storage costs.
- **Query-optimized**: Works natively with modern analytics tools (Athena, Spark, DuckDB, etc.).
- **Schema-aware**: Strong typing for timestamps, integers, floats, booleans, etc., which fits structured telemetry data.

With EMQX, Parquet is now an option for **aggregated uploads** to S3 and Azure Blob Storage, alongside CSV and JSON Lines.

## **Use Case Overview**

Imagine you operate thousands of IoT devices publishing telemetry to EMQX:

- Topic: `sensors/<device_id>/telemetry`
- Payload (JSON):

```json
{
  "device_id": "sensor-001",
  "temperature": 24.7,
  "humidity": 55.2,
  "ts": 1738588245123
}
```

Your goals:

1. **Persist** all telemetry data to **Amazon S3** in an efficient, analytics-friendly format (Parquet).
2. **Analyze** this data using **DuckDB**, both ad hoc (local) and potentially in serverless environments.

We’ll implement:

- EMQX **Connector**: Amazon S3.
- EMQX **Action**: Aggregated upload in **Parquet** format.
- EMQX **Rule**: Select MQTT fields and send them to the S3 Aggregated action.
- **DuckDB**: Query the resulting Parquet files directly from S3.

> **Note:** For detailed step-by-step S3 configuration and UI screenshots, refer to the [official documentation](https://docs.emqx.com/en/emqx/v6.1/data-integration/s3.html) on exporting aggregated data to S3 in Parquet format. In this post, we focus on the end-to-end flow and key configuration points.

## **Step 1: Configure the S3 Connector**

Create an **Amazon S3 connector** in EMQX (via Dashboard or config file). At a high level, you will specify:

- **S3 endpoint** (e.g., `s3.us-east-1.amazonaws.com`)
- **Access key & secret** with permissions to write to your chosen bucket.
- Optional: access mode, encryption, and other S3 options.

Once the connector is configured, you’re ready to define the S3 Aggregated Action with Parquet output.

## **Step 2: Create an S3 Action with Parquet Aggregation**

Next, create an **Action** that uses the S3 connector and selects **Parquet** as the aggregated upload format.

Key aspects to configure:

1. **Upload mode:** `Aggregated`

2. **Bucket name**, e.g., `mqtt-telemetry-parquet`.

3. **Aggregation format:** `Parquet`  
   Choose **Parquet** instead of CSV/JSONL for aggregated uploads.

4. **Parquet schema definition:** Parquet files follow a strict schema to organize and compress data efficiently.  Either refer to an Avro Schema already registered in Schema Registry, or define one inline that matches your incoming data.  e.g.,

   ```json
   {
     "fields": [
       {
         "field-id": 1,
         "name": "device_id",
         "type": "string"
       },
       {
         "field-id": 2,
         "name": "temperature",
         "type": "float"
       },
       {
         "field-id": 3,
         "name": "humidity",
         "type": "float"
       },
       {
         "default": null,
         "field-id": 4,
         "name": "ts",
         "type": [
           "null",
           {
             "adjust-to-utc": false,
             "logicalType": "timestamp-micros",
             "type": "long"
           }
         ]
       }
     ],
     "name": "root",
     "type": "record"
   }
   ```

5. **Upload triggers** (same semantics as existing aggregation):

   - `max_records` – Maximum number of records per file, e.g. `10_000`.
   - `time_interval` – Maximum time window, e.g., `60s`.

   EMQX triggers the upload when **either** condition is met.

6. **Compression**  
   Parquet files support multiple compression algorithms, typically:

   - `snappy` (default; good balance of speed and size)
   - `gzip`
   - `zstd`

   For most IoT analytics workloads, `snappy` is a great default.

7. **S3 object key strategy**  
   Use time-based partitioning to keep directories manageable and to optimize downstream queries, as well as to avoid data collisions in data coming from different nodes and actions in the cluster.

   Example object path pattern:

   ```
   ${action}/${node}/${datetime.rfc3339utc}/N${sequence}.parquet
   ```

Once saved, this action will collect records from the rule, batch them, and upload **compressed Parquet files** to your S3 bucket.

Finally, let’s set up the Rule SQL to tie the Action with incoming device data to be ingested.

## **Step 3: Define the Data Shape with EMQX Rule SQL**

In EMQX, the **Rule SQL** defines both the data routing logic and its transformations. Fields selected in the `SELECT` clause become available for our Action to use in columns in the Parquet file.

For our telemetry example:

```sql
SELECT
  payload.device_id          AS device_id,
  payload.temperature        AS temperature,
  payload.humidity           AS humidity,
  publish_received_at * 1000 AS publish_received_at
FROM
  "sensors/+/telemetry"
```

What this does:

- Subscribes to `sensors/+/telemetry` (all devices).
- Extracts relevant metrics from the JSON payload.
- Casts EMQX message metadata into a well-defined schema that matches the defined Parquet schema:
  - `device_id`: string
  - `temperature`: float
  - `humidity`: float
  - `publish_received_at`: integer (timestamp in microseconds)

## **Step 4: Inspect Parquet Files in S3**

After some data flows through, you should see objects like:

```
s3://mqtt-telemetry-parquet/my_action/emqx@node1.my.cluster/2026-02-03T14_19_32Z/N0.parquet
s3://mqtt-telemetry-parquet/my_action/emqx@node1.my.cluster/2026-02-03T14_19_32Z/N1.parquet
...
```

Each file holds up to `max_records` rows (or less, if `time_interval` triggers earlier). Thanks to Parquet + compression, file sizes should be significantly smaller than equivalent CSV.

## **Step 5: Analyze the Data with DuckDB**

[DuckDB](https://duckdb.org/) is an in-process analytical database that excels at querying Parquet data, both locally and from object storage.

Here’s how to query your S3-based Parquet data from DuckDB.

### **Option A: Download Files Locally**

For quick experiments, you can pull files locally (e.g., via `aws s3 cp s3://... ./data/`) and run DuckDB on them:

```sql
-- In DuckDB shell
CREATE TABLE telemetry AS
SELECT *
FROM read_parquet('data/my_action/emqx@node1.my.cluster/2026-02-03T14_19_32Z/N0.parquet');

-- Example queries
SELECT
  device_id,
  date_trunc('hour', publish_received_at) AS hour,
  avg(temperature) AS avg_temp,
  avg(humidity)    AS avg_humidity
FROM telemetry
GROUP BY device_id, hour
ORDER BY hour, device_id;
```

### **Option B: Query Directly from S3**

DuckDB can read from S3 without downloading all files locally, by configuring S3 access:

```sql
INSTALL httpfs;
LOAD httpfs;

CREATE SECRET (
    TYPE s3,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    REGION 'us-east-1'
);
```

Then query straight from S3:

```sql
SELECT
  device_id,
  date_trunc('hour', publish_received_at) AS hour,
  avg(temperature) AS avg_temp
FROM read_parquet(
  's3://mqtt-telemetry-parquet/my_action/*/*/N*.parquet'
)
GROUP BY device_id, hour
ORDER BY hour, device_id
LIMIT 100;
```

You can run DuckDB:

- Locally on your laptop.
- Inside a container or a lightweight API service.
- In serverless environments for ad hoc analytics or dashboards.

## **Best Practices & Tips**

### **1. Choose Sensible Aggregation Windows**

- High-frequency telemetry → smaller intervals (`10–30s`) or smaller `max_records`.
- Low-frequency or sparse data → larger intervals (e.g., `1–5 minutes`) to avoid too many tiny files.

**Goal:** Balance file size (for efficient queries) and data latency (how fresh your analytics need to be).

### **2. Design a Query-Friendly Partition Layout**

In this example, we partitioned by the simple aggregation timestamp.  Depending on your data rate, further partitioning by date/time could be an option:

- `year=YYYY/month=MM/day=DD/hour=HH`
- Optionally `device_id` if you often query per device, but be careful of too many small partitions.

This allows tools like DuckDB, Spark, and Athena to **prune** partitions efficiently and reduce I/O.

### **3. Keep Schemas Stable**

Adding/removing columns is supported by Parquet, but frequent schema changes can complicate downstream queries. When evolving the schema:

- Add new columns rather than frequently renaming/removing.
- Use views in DuckDB to hide schema complexity from consumers.

### **4. Use Snappy Compression by Default**

`snappy` usually gives the best trade-off for IoT workloads:

- Fast compression/decompression.
- Good enough size reduction for most telemetry data.

Use `gzip` or `zstd` only if storage cost is critical and you can tolerate slower CPU performance during reads.

## **What You Gain with EMQX + S3 Parquet + DuckDB**

By combining EMQX’s Parquet support for S3 with DuckDB, you get:

- **A simple IoT data lake ingestion layer**: MQTT → EMQX → S3 Parquet, no custom ingestion service required.
- **Cost-efficient, analytics-ready storage**: Columnar, compressed Parquet files directly queryable by modern tools.
- **Flexible analytics workflows**: Use DuckDB for:
  - Ad hoc exploratory analysis.
  - Lightweight dashboards.
  - Embedded analytics in internal tools or backends.
- **Future-proof architecture**: The same Parquet files can be used by:
  - AWS Athena / Glue
  - Spark / Flink
  - Pandas/Polars (via Parquet readers)
  - Data warehouses that support external tables on S3.

By streaming MQTT data into S3 as compact, analytics‑ready Parquet files, EMQX turns your broker into a powerful bridge between real‑time IoT workloads and modern data platforms. Paired with DuckDB, you get instant, SQL‑driven insight from raw device data without heavy infrastructure or complex pipelines. Whether you’re validating a new product feature, monitoring fleet health, or building a full IoT data lake, this lightweight architecture lets your team move faster, cut costs, and unlock more value from every message your devices send.
