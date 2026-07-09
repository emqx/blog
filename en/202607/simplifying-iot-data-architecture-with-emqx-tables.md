## Why IoT Telemetry Needs a Simpler Data Architecture

In traditional IoT data platforms, the MQTT Broker is often responsible only for device access, while data storage, stream processing, and analytics depend on multiple external components working together.

![image.png](https://assets.emqx.com/images/441d728ebec115af5c3c543d0c14fadc.png)

[Traditional IoT Data Architecture]{.block .text-center}

Although this approach is flexible, system complexity increases quickly as the device fleet grows:

- More and more architecture components
- Longer data paths
- High maintenance cost for ETL and Connectors
- Difficult schema evolution
- Complex data synchronization
- Increasing operations and troubleshooting pressure

In many IoT telemetry scenarios, devices report relatively simple data such as temperature, current, GPS location, vibration, online status, and operating metrics. This data often does not require a full-scale big data platform.

Instead, a lightweight, IoT-native data architecture is often the better choice. Rather than managing increasingly complex data pipelines, enterprises need a simple way to ingest, store, and query MQTT data for large-scale IoT telemetry scenarios.

When MQTT data can be written directly to a time-series database and queried immediately with SQL, the complexity of Kafka, ETL pipelines, and external data platforms can be greatly reduced. That's where EMQX Tables comes in.

## EMQX Tables: A Lighter IoT Data Architecture

EMQX Tables is a built-in time-series database service provided by EMQX Cloud. It integrates directly with EMQX Rule Engine to enable native MQTT data writes and real-time queries.

The core value of EMQX Tables is not to provide yet another database, but to let MQTT data complete the full loop from ingestion to storage and query with minimal infrastructure.

With EMQX Tables, the traditionally complex data path can be simplified to:

![image.png](https://assets.emqx.com/images/ecd5a21ed4d974fbb8d4556552ee83a2.png)

[Simplified IoT Data Architecture with EMQX Tables]{.block .text-center}

The entire process no longer requires deploying Kafka, a stream processing platform, an external TSDB, an ETL Pipeline, or a data synchronization service. MQTT data storage and query can be completed directly inside the EMQX platform.

This means:

- Fewer infrastructure components
- Shorter data paths
- Lower system latency
- Lower operations cost
- Faster project delivery

This article uses a smart factory equipment monitoring scenario to demonstrate how to use EMQX Tables to build a lightweight IoT data architecture and write MQTT data directly into a time-series table through Rule Engine.

## Use Case: Smart Factory Equipment Monitoring

Factory equipment periodically reports the following telemetry data:

| Field             | Description                         |
| :---------------- | :---------------------------------- |
| `machine_id`      | Device ID                           |
| `production_line` | Production line ID                  |
| `temperature`     | Temperature                         |
| `vibration`       | Vibration value                     |
| `machine_status`  | Operating status                    |
| `timestamp`       | Time when EMQX receives the message |

Example MQTT Payload:

```json
{
  "production_line": "A1",
  "machine_id": "M100",
  "temperature": 56.2,
  "vibration": 0.83,
  "machine_status": "running"
}
```

The system needs to provide:

- Real-time MQTT data ingestion
- Real-time time-series data storage
- SQL query support
- Follow-up analysis and alerting support

## Prerequisites

Before you begin, make sure the following preparations are complete:

- An[ EMQX Dedicated deployment ](https://docs.emqx.com/en/cloud/latest/create/dedicated.html)has been created.
- An EMQX Tables instance has been created.
- EMQX Dedicated and EMQX Tables are in the same VPC network.
- When creating Tables, select the network where the Broker is located to ensure that Tables and Broker can communicate over the internal network.
- A username and password for MQTT connection have been created.
- Tables connection information has been obtained, including Host, Database, Username, and Password.

## Create the EMQX Tables Data Table

This article directly uses the database already provided by EMQX Tables, such as `public`. It is not recommended to execute `CREATE DATABASE factory` in customer steps, because different environments may not have permission to create databases, or the database may already exist.

Run the following SQL in EMQX Tables Data Explorer:

```sql
CREATE TABLE machine_metrics (
  "timestamp" TIMESTAMP TIME INDEX,
  "production_line" STRING,
  "machine_id" STRING,
  "temperature" DOUBLE,
  "vibration" DOUBLE,
  "machine_status" STRING
)
WITH (
  'append_mode'='true',
  'ttl'='7d'
);
```

This table stores factory equipment telemetry data. For typical time-series metrics such as temperature, vibration, and status, this single-table model can meet the requirements of most device monitoring scenarios without introducing an additional complex data platform.

Field descriptions:

- `timestamp`: The time when EMQX receives the MQTT message, used as the time index.
- `production_line`: Production line ID.
- `machine_id`: Device ID.
- `temperature`: Temperature.
- `vibration`: Vibration value.
- `machine_status`: Device operating status.

Table parameter descriptions:

- `append_mode='true'`: Telemetry data is continuously appended time-series data and is suitable for Append Mode.
- `ttl='7d'`: Keeps only the most recent 7 days of data. This can be adjusted based on production requirements.

## Configure EMQX Data Integration

EMQX Rule Engine can write MQTT Payloads directly into EMQX Tables.

This article uses:

```
EMQX → Rule Engine → EMQX Tables
```

### Create a Tables Connector

Create a Tables Connector in the EMQX Cloud console:

```
Data Integration
→ Connectors
→ New Connector
→ EMQX Tables
```

When configuring the Connector, select the EMQX Tables instance that has already been created and confirm:

- Database Name is consistent with the Tables database, such as `public`.
- Broker and Tables are in the same VPC network.
- The Connector status is `Connected` after creation.
- The Connector time column remains `timestamp`.

### Configure Rule SQL

Create a Rule to listen to factory device reporting topics:

```sql
SELECT
  timestamp,
  payload.machine_id as machine_id,
  payload.production_line as production_line,
  payload.temperature as temperature,
  payload.vibration as vibration,
  payload.machine_status as machine_status
FROM "factory/+/metrics"
```

This rule listens to:

```
factory/+/metrics
```

and extracts device telemetry fields from the MQTT Payload.

Note: Keep the field name `timestamp` here. Do not change it to `ts`, otherwise the time column configuration in the Tables Connector must also be updated.

### Configure the Action

Create the corresponding EMQX Tables Action with the following write syntax:

```
machine_metrics production_line=${production_line},machine_id=${machine_id},temperature=${temperature},vibration=${vibration},machine_status=${machine_status} ${timestamp}
```

Notes:

- Do not use the old `machine_metrics,production_line=... temperature=...` syntax.
- This article uses field write syntax, which has been verified to write stably to EMQX Tables.
- The timestamp uses `${timestamp}` and remains consistent with the table time column.

At this point, the data write path is complete. Compared with traditional architecture, this data path has no Kafka, no ETL, and no external database synchronization process. MQTT data can directly enter time-series storage and be queried and analyzed immediately.

## Publish MQTT Test Data

Use MQTTX or another MQTT client to publish test messages to the Topic:

```
factory/A/metrics
```

Payload example:

```json
{
  "production_line": "A1",
  "machine_id": "M100",
  "temperature": 56.2,
  "vibration": 0.83,
  "machine_status": "running"
}
```

After the message is sent, EMQX Rule Engine automatically completes:

```
MQTT → Rule Engine → Tables Action → EMQX Tables
```

The entire process does not require any external ETL.

## Query Data

Go to EMQX Tables Data Explorer and run:

```sql
SELECT
  "timestamp",
  production_line,
  machine_id,
  temperature,
  vibration,
  machine_status
FROM machine_metrics
ORDER BY "timestamp" DESC
LIMIT 10;
```

If the query result shows the telemetry data that was just published, MQTT data has been successfully written into EMQX Tables.

You can also query by device:

```sql
SELECT
  "timestamp",
  temperature,
  vibration,
  machine_status
FROM machine_metrics
WHERE machine_id = 'M100'
ORDER BY "timestamp" DESC
LIMIT 20;
```

Or aggregate and analyze device status. After data is written, SQL queries can be executed directly without waiting for data synchronization or offline computing tasks:

```sql
SELECT
  machine_id,
  production_line,
  AVG(temperature) AS avg_temperature,
  MAX(temperature) AS max_temperature,
  AVG(vibration) AS avg_vibration,
  MAX(vibration) AS max_vibration,
  COUNT(*) AS sample_count
FROM machine_metrics
GROUP BY machine_id, production_line
ORDER BY max_temperature DESC;
```

## Validation Results

In actual validation, five QoS 1 test messages were published to `factory/A/metrics`, with the following result:

```
{"published":5,"received":5}
```

Rule metrics showed:

```
{"matched":17,"passed":17,"actions.success":17,"failed":0,"actions.failed":0}
```

Action metrics showed:

```
{"matched":17,"success":17,"failed":0,"dropped":0,"inflight":0}
```

EMQX Tables queries showed the latest data:

```
M100 / A1 / temperature 60.03 / vibration 0.78 / running
M103 / A2 / temperature 56.33 / vibration 0.66 / running
M102 / A1 / temperature 52.63 / vibration 0.54 / running
M101 / A2 / temperature 48.93 / vibration 0.42 / running
```

This shows that the complete path has been verified:

```
MQTT Publish → Rule Engine → EMQX Tables Action → EMQX Tables Query
```

## What Value Does EMQX Tables Deliver

EMQX Tables is more than a built-in database. Its real value lies in simplifying the entire IoT data path.

### 1. Fewer Infrastructure Components

Traditional architecture:

![image.png](https://assets.emqx.com/images/eaccff82170d80776a3d09794b5cf7ef.png)

EMQX Tables architecture:

![image.png](https://assets.emqx.com/images/7f20bfb17961ee8854efc640e6b663fe.png)

This significantly reduces middleware, Connectors, Stream Processors, and data synchronization paths, making the overall architecture lighter.

### 2. Lower Operations Cost

There is no need to maintain a Kafka Cluster, Flink, Debezium, an external TSDB, or an additional data synchronization service.

For small and medium-sized IoT scenarios, this can significantly reduce operations cost and system complexity.

### 3. Native MQTT Data Path

EMQX Rule Engine can directly process MQTT Payloads without protocol conversion, additional Consumers, or an independent ETL Pipeline.

MQTT data can natively enter time-series storage.

### 4. Better Fit for IoT Telemetry Scenarios

IoT telemetry data usually has clear time-series characteristics, such as periodically reported temperature, vibration, status, and location data.

EMQX Tables can directly handle this type of time-series data and provide SQL query capability.

### 5. Lower Latency and Fewer Failures

A shorter data path means:

- Lower latency
- Fewer failure points
- Simpler troubleshooting
- Lower synchronization risk

This is especially suitable for scenarios such as Smart Factory, Edge Telemetry, Device Monitoring, and Real-time Metrics.

### 6. More Secure VPC Internal Communication

EMQX Dedicated and EMQX Tables can be deployed in the same VPC network and communicate directly over the internal network.

This approach can:

- Avoid public network exposure
- Reduce the public network attack surface
- Reduce network hops
- Improve data transmission stability
- Lower network latency

For industrial IoT, device monitoring, and internal enterprise telemetry scenarios, this architecture is more secure and easier to maintain. EMQX Tables is not designed to replace PB-scale data warehouses or complex BI platforms. Its goal is to provide a lighter, simpler, and more native data architecture for the most common IoT telemetry scenarios, allowing MQTT data to be stored and queried directly.

EMQX Tables is especially suitable for:

- IoT Telemetry
- Real-time device monitoring
- Smart Factory
- Edge-to-Cloud
- MQTT-native scenarios
- Lightweight real-time analytics

For PB-scale OLAP, ultra-large-scale offline analytics, or complex BI data warehouses, it is still recommended to use a professional data platform.

## Summary

EMQX Tables provides a lighter and more native data architecture for IoT scenarios.

By combining Rule Engine with built-in time-series storage, you can directly implement:

![image.png](https://assets.emqx.com/images/d7a137d3dbc62c562bdd54b80f8d23f1.png)

No additional ETL, Kafka, or external TSDB is required.

For enterprises that want to quickly build real-time device monitoring and telemetry platforms, EMQX Tables provides a lightweight, cloud-native, and easier-to-operate alternative, enabling MQTT data to complete the loop from ingestion to query within the same platform.

Try it today: [EMQX Tables - Time-Series Database for MQTT IoT Data Storage](https://www.emqx.com/en/cloud/emqx-tables)
