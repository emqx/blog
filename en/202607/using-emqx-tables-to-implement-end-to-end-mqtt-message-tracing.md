## Introduction

In production environments, when issues such as message latency, consumer backlog, ACK timeout, duplicate consumption, or message loss occur, relying only on basic Broker metrics usually makes it difficult to answer the following questions:

- At which stage did the message become delayed?
- Has the message been successfully delivered to the subscriber?
- Has the ACK been returned?
- Did the issue occur on the Publisher, Broker, or Subscriber side?

An MQTT message usually goes through several key stages from publication to final acknowledgment:

- Publisher network transmission latency;
- Broker receiving and internal processing latency;
- Broker-to-Subscriber delivery latency;
- Subscriber ACK return latency;
- Exceptional cases such as failed delivery or missing ACKs.

Therefore, in addition to traditional Broker metric monitoring, you need an end-to-end observability solution that can correlate and analyze the MQTT message lifecycle.

EMQX Cloud can combine Event Topics, Rule Engine, and EMQX Tables to continuously collect and correlate key events in the MQTT message lifecycle. This makes it possible to record message path status and key timestamps from message publication, to Broker delivery, and then to Subscriber ACK confirmation.

The value of EMQX Tables is not only storing message events. It also enables MQTT messages to be queried, correlated, and analyzed like traces in a distributed system, providing end-to-end observability across the full message path.

This article describes how to use EMQX Cloud and EMQX Tables to build an end-to-end MQTT message observability solution with the following capabilities:

- Analyze the message publication, delivery, and ACK confirmation path;
- Correlate `message.publish`, `message.delivered`, and `message.acked` events;
- Measure latency across Publisher, Broker, and Subscriber stages;
- Detect missing ACKs, incomplete message paths, and potential message drop issues;
- Verify whether messages were successfully delivered to subscribers;
- Use SQL to perform lifecycle statistics and troubleshooting.

## Prerequisites

Before you begin, make sure the following requirements are met:

- An EMQX v5 deployment has been created and is accessible.
- Tables has been deployed and is accessible.
- A Tables Connector has been created in EMQX.
- The Publisher and Subscriber system clocks are synchronized.
- The Publisher includes a `publish_at` timestamp in the Payload of each MQTT message.
- QoS 1 or QoS 2 is used so that acknowledgment events can be captured.
- Clients and the database use a consistent timezone for timestamp handling. UTC is recommended.

## Timestamp Definitions

The tracing model uses the following timestamps:

- `publish_at`: The client-side timestamp written by the Publisher into the MQTT Payload.
- `emqx_received_at`: The time when EMQX receives the PUBLISH packet.
- `emqx_delivered_at`: The time when EMQX delivers the message to the Subscriber side.
- `sub_ack_at`: The time when EMQX receives the acknowledgment ACK from the Subscriber.

These timestamps are used to calculate latency at each stage of the transmission path.

## Create the Tables Table

Create a table to store message tracing records. Each message stage is stored as an independent row, and subsequent queries correlate these rows by `msg_id`.

This solution uses an append-only wide-table design. MQTT message path events are typical time-series audit data: they are continuously appended and historical records are not updated.

```sql
CREATE TABLE mqtt_message_traces (
  "timestamp" TIMESTAMP TIME INDEX,
  "event" STRING,
  "msg_id" STRING,
  "trace_key" STRING,
  "publish_at" BIGINT,
  "emqx_received_at" BIGINT,
  "emqx_delivered_at" BIGINT,
  "sub_ack_at" BIGINT,
  "pub_clientid" STRING,
  "sub_clientid" STRING,
  "topic" STRING,
  "qos" BIGINT,
  "msg" BIGINT
)
WITH (
  'append_mode'='true',
  'ttl'='30d'
);
```

Table parameter notes:

- `append_mode='true'`: All tracing events are written in append mode, preserving the complete message path.
- `ttl='30d'`: Keeps tracing data from the most recent 30 days. You can adjust this based on production requirements.

## Configure Tables Data Integration in EMQX Cloud

The traceability workflow uses three rules and three write actions. All three actions write to the same table, but each action captures a different stage of the message lifecycle.

The three rules use a shared correlation key:

```
id as msg_id
```

The same `msg_id` is used to correlate the following three events:

- `message.publish`
- `message.delivered`
- `message.acked`

## Configure the Publish Tracing Rule

The first rule records data from the publish stage. It listens to business topics and captures ordinary MQTT messages.

To collect all business topics, use:

```
FROM "#"
```

To validate a single test topic, use:

```
FROM "emqx/test"
```

Rule SQL:

```sql
SELECT
  timestamp,
  event,
  id as msg_id,
  concat(id, '_publish') as trace_key,
  int(payload.publish_at) as publish_at,
  int(publish_received_at) as emqx_received_at,
  clientid as pub_clientid,
  topic,
  qos,
  int(payload.msg) as msg
FROM "#"
```

Action SQL:

```sql
mqtt_message_traces event=${event},msg_id=${msg_id},trace_key=${trace_key},publish_at=${publish_at}i,emqx_received_at=${emqx_received_at}i,pub_clientid=${pub_clientid},topic=${topic},qos=${qos}i,msg=${msg}i ${timestamp}
```

When the Publisher sends a message to a business topic, this rule writes the publish tracing record into Tables.

## Configure the Delivery Tracing Rule

The second rule records the time point when EMQX delivers the message to the Subscriber path.

Rule SQL:

```sql
SELECT
  timestamp,
  event,
  id as msg_id,
  concat(id, '_delivered') as trace_key,
  int(timestamp) as emqx_delivered_at,
  from_clientid as pub_clientid,
  clientid as sub_clientid,
  topic,
  qos,
  int(payload.msg) as msg
FROM "$events/message_delivered"
```

Action SQL:

```sql
mqtt_message_traces event=${event},msg_id=${msg_id},trace_key=${trace_key},emqx_delivered_at=${emqx_delivered_at}i,pub_clientid=${pub_clientid},sub_clientid=${sub_clientid},topic=${topic},qos=${qos}i,msg=${msg}i ${timestamp}
```

This record is used to calculate Broker-side processing latency and Broker-to-Subscriber path latency.

## Configure the Acknowledgment Tracing Rule

The third rule records data from the acknowledgment stage. This rule is triggered only when an acknowledgment event exists, so QoS 1 or QoS 2 must be used.

Rule SQL:

```sql
SELECT
  timestamp,
  event,
  id as msg_id,
  concat(id, '_acked') as trace_key,
  int(timestamp) as sub_ack_at,
  from_clientid as pub_clientid,
  clientid as sub_clientid,
  topic,
  qos,
  int(payload.msg) as msg
FROM "$events/message_acked"
```

Action SQL:

```sql
mqtt_message_traces event=${event},msg_id=${msg_id},trace_key=${trace_key},sub_ack_at=${sub_ack_at}i,pub_clientid=${pub_clientid},sub_clientid=${sub_clientid},topic=${topic},qos=${qos}i,msg=${msg}i ${timestamp}
```

This record is used to calculate Subscriber-side acknowledgment latency and total end-to-end latency.

## Connector Configuration Notes

From a logical design perspective, the three actions can share a single Tables Connector.

In production environments with sustained high load, you can also configure independent Connectors for the publish, delivery, and acknowledgment stages to isolate write pressure. This choice does not affect the table schema, rule SQL, action SQL, correlation logic, or latency calculation formulas.

## Simulate Message Transmission with the Python SDK

This section describes the Publisher and Subscriber behavior used for validation.

The Publisher sends MQTT messages to the business topic, and each Payload includes a `publish_at` timestamp. The Subscriber listens to the same topic and remains online during the full message flow.

Install the dependency:

```shell
python3 -m pip install paho-mqtt
```

### Publisher

The Publisher must:

- Connect to EMQX
- Publish messages to the target topic
- Use QoS 1
- Include the `publish_at` field in each message Payload

Payload example:

```
{"publish_at":1773579492999,"msg":10000}
```

Publisher script:

```python
#!/usr/bin/env python3

import argparse
import json
import random
import time
from paho.mqtt import client as mqtt_client

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=1883)
parser.add_argument("--topic", default="emqx/test")
parser.add_argument("--qos", type=int, default=1)
parser.add_argument("--count", type=int, default=20)
parser.add_argument("--interval-sec", type=float, default=1.0)
parser.add_argument("--tps", type=float)
parser.add_argument("--duration-sec", type=float)
parser.add_argument("--hold-sec", type=float, default=0.0)
parser.add_argument("--username")
parser.add_argument("--password")
args = parser.parse_args()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        raise RuntimeError(f"connect failed: {reason_code}")
    print(f"Connected to {args.host}:{args.port}")

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION2,
    client_id=f"python-mqtt-pub-{random.randint(0,100000)}",
)
client.on_connect = on_connect

if args.username and args.password:
    client.username_pw_set(args.username, args.password)

client.connect(args.host, args.port)
client.loop_start()

count = 0
start = time.perf_counter()

if args.tps and args.duration_sec:
    interval = 1.0 / args.tps
    deadline = start + args.duration_sec
    next_send = start
    def keep_sending(now, sent):
        return now < deadline
else:
    interval = args.interval_sec
    next_send = start + interval
    def keep_sending(now, sent):
        return sent < args.count

while keep_sending(time.perf_counter(), count):
    now = time.perf_counter()
    if now < next_send:
        time.sleep(next_send - now)
    payload = json.dumps(
        {
            "publish_at": int(time.time() * 1000),
            "msg": count,
        },
        separators=(",", ":"),
    )
    result = client.publish(args.topic, payload, qos=args.qos)
    if result.rc != 0:
        raise RuntimeError(f"publish failed: {result.rc}")
    print(f"Sent: {payload}")
    count += 1
    next_send += interval

publish_elapsed = time.perf_counter() - start

if args.hold_sec > 0:
    time.sleep(args.hold_sec)

total_elapsed = time.perf_counter() - start
print(
    json.dumps(
        {
            "topic": args.topic,
            "sent": count,
            "publish_duration_sec": round(publish_elapsed, 3),
            "total_duration_sec": round(total_elapsed, 3),
            "hold_sec": args.hold_sec,
            "target_tps": args.tps,
            "actual_tps": round(count / publish_elapsed, 3) if publish_elapsed else 0.0,
        }
    )
)

client.disconnect()
client.loop_stop()
```

Run example:

```python
python3 publisher.py \
  --host xxxx.dedicated.aws.mqttce.net \
  --port 1883 \
  --topic emqx/test \
  --qos 1 \
  --tps 1 \
  --duration-sec 5 \
  --hold-sec 5 \
  --username xxxx \
  --password xxxx
```

### Subscriber

The Subscriber must:

- Connect to EMQX
- Subscribe to the same business topic
- Use QoS 1
- Stay connected longer than the publishing phase

Subscriber script:

```python
#!/usr/bin/env python3

import argparse
import json
import random
import time
from paho.mqtt import client as mqtt_client

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=1883)
parser.add_argument("--topic", default="emqx/test")
parser.add_argument("--qos", type=int, default=1)
parser.add_argument("--duration-sec", type=float)
parser.add_argument("--username")
parser.add_argument("--password")
args = parser.parse_args()

counter = {"received": 0}

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        raise RuntimeError(f"connect failed: {reason_code}")
    print(f"Connected to {args.host}:{args.port}")
    print(f"Subscribed to topic: {args.topic}")
    client.subscribe(args.topic, qos=args.qos)

def on_message(client, userdata, msg):
    counter["received"] += 1
    try:
        payload = msg.payload.decode()
        print(f"[{counter['received']}] {payload}")
    except Exception:
        print(f"[{counter['received']}] Message received")

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION2,
    client_id=f"python-mqtt-sub-{random.randint(0, 100000)}",
)
client.on_connect = on_connect
client.on_message = on_message

if args.username and args.password:
    client.username_pw_set(args.username, args.password)

client.connect(args.host, args.port)
client.loop_start()

start = time.perf_counter()
while args.duration_sec is None or time.perf_counter() - start < args.duration_sec:
    time.sleep(1)

elapsed = time.perf_counter() - start
print(
    json.dumps(
        {
            "topic": args.topic,
            "received": counter["received"],
            "duration_sec": round(elapsed, 3),
            "recv_tps": round(counter["received"] / elapsed, 3) if elapsed else 0.0,
        }
    )
)

client.disconnect()
client.loop_stop()
```

Start the Subscriber first:

```python
python3 subscriber.py \
  --host xxxx.dedicated.aws.mqttce.net \
  --port 1883 \
  --topic emqx/test \
  --qos 1 \
  --duration-sec 70 \
  --username xxxx \
  --password xxxx
```

Then start the Publisher.

## Recommended Run Order

Use two terminals:

1. Start the Subscriber first.
2. Start the Publisher.
3. Wait until both commands finish.
4. After message delivery is complete, query EMQX Tables.

## View Message Latency

After the Publisher, Subscriber, rules, and Tables actions are all running, you can use SQL to verify tracing records and calculate latency.

The latency formulas for each stage are:

- Publisher client to EMQX latency: `emqx_received_at - publish_at`
- EMQX processing latency: `emqx_delivered_at - emqx_received_at`
- Subscriber ACK latency: `sub_ack_at - emqx_delivered_at`
- Total end-to-end transmission latency: `sub_ack_at - publish_at`

Notes:

- If a message does not include the `publish_at` timestamp, Publisher-to-Broker latency cannot be calculated.
- QoS 0 does not generate `message.acked` events, so Subscriber-side acknowledgment latency cannot be calculated.

## Query Examples

### 1. Count All Tracing Records

```sql
SELECT COUNT(*) AS total_rows
FROM mqtt_message_traces;
```

### 2. View Recent Publish Records

```sql
SELECT
  "timestamp",
  event,
  msg_id,
  publish_at,
  emqx_received_at,
  pub_clientid,
  topic,
  qos,
  msg
FROM mqtt_message_traces
WHERE event = 'message.publish'
ORDER BY "timestamp" DESC
LIMIT 20;
```

This query verifies that the Publisher-side timestamp and Broker receiving timestamp have both been stored correctly.

### 3. View Recent Delivery Records

```sql
SELECT
  "timestamp",
  event,
  msg_id,
  emqx_delivered_at,
  pub_clientid,
  sub_clientid,
  topic,
  qos,
  msg
FROM mqtt_message_traces
WHERE event = 'message.delivered'
ORDER BY "timestamp" DESC
LIMIT 20;
```

This query verifies that delivery-stage data exists and can be used to calculate Broker-to-Subscriber path latency.

### 4. View Recent Acknowledgment Records

```sql
SELECT
  "timestamp",
  event,
  msg_id,
  sub_ack_at,
  pub_clientid,
  sub_clientid,
  topic,
  qos,
  msg
FROM mqtt_message_traces
WHERE event = 'message.acked'
ORDER BY "timestamp" DESC
LIMIT 20;
```

This query verifies that acknowledgment-stage data exists and can be used to calculate Subscriber-side acknowledgment latency.

### 5. Count Records by Event Type

```sql
SELECT
  event,
  COUNT(*) AS row_count
FROM mqtt_message_traces
GROUP BY event
ORDER BY event;
```

This query quickly checks the completeness of the tracing dataset.

Under normal conditions, for QoS 1 messages with an online Subscriber, you should see:

- `message.publish`
- `message.delivered`
- `message.acked`

### 6. Query Average Latency for Each Stage in the Last Hour

```sql
WITH publish_events AS (
  SELECT
    msg_id,
    MAX(publish_at) AS publish_at,
    MAX(emqx_received_at) AS publish_received_at
  FROM mqtt_message_traces
  WHERE event = 'message.publish'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id
),
delivered_events AS (
  SELECT
    msg_id,
    sub_clientid,
    MAX(emqx_delivered_at) AS message_delivered
  FROM mqtt_message_traces
  WHERE event = 'message.delivered'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id, sub_clientid
),
ack_events AS (
  SELECT
    msg_id,
    sub_clientid,
    MAX(sub_ack_at) AS message_acked
  FROM mqtt_message_traces
  WHERE event = 'message.acked'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id, sub_clientid
),
message_latency AS (
  SELECT
    p.msg_id,
    COALESCE(d.sub_clientid, a.sub_clientid) AS sub_clientid,
    p.publish_at,
    p.publish_received_at,
    d.message_delivered,
    a.message_acked
  FROM publish_events p
  JOIN delivered_events d ON p.msg_id = d.msg_id
  JOIN ack_events a
    ON p.msg_id = a.msg_id
   AND d.sub_clientid = a.sub_clientid
)
SELECT
  COUNT(*) AS sample_count,
  ROUND(AVG(publish_received_at - publish_at), 3) AS publisher_to_emqx_ms,
  ROUND(AVG(message_delivered - publish_received_at), 3) AS emqx_processing_ms,
  ROUND(AVG(message_acked - message_delivered), 3) AS subscriber_ack_ms,
  ROUND(AVG(message_acked - publish_at), 3) AS end_to_end_ms
FROM message_latency
WHERE publish_at IS NOT NULL
  AND publish_received_at IS NOT NULL
  AND message_delivered IS NOT NULL
  AND message_acked IS NOT NULL;
```

Query notes:

- `"timestamp" >= now() - INTERVAL '1 hour'` limits the query range to the last hour to avoid interference from historical data.
- `delivered_events` and `ack_events` are grouped by `msg_id` and `sub_clientid` to avoid merging records from multiple Subscribers.
- `MAX(...)` aggregates timestamps from the same message stage into a single analysis record.
- The final `WHERE ... IS NOT NULL` clause ensures that only records with complete publish, delivery, and acknowledgment paths are used for latency calculation.

### 7. Validate Negative Values

Before accepting the latency results, run the following query. Any non-zero result indicates a timestamp problem, clock synchronization problem, or field mapping error.

```sql
WITH publish_events AS (
  SELECT
    msg_id,
    MAX(publish_at) AS publish_at,
    MAX(emqx_received_at) AS publish_received_at
  FROM mqtt_message_traces
  WHERE event = 'message.publish'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id
),
delivered_events AS (
  SELECT
    msg_id,
    sub_clientid,
    MAX(emqx_delivered_at) AS message_delivered
  FROM mqtt_message_traces
  WHERE event = 'message.delivered'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id, sub_clientid
),
ack_events AS (
  SELECT
    msg_id,
    sub_clientid,
    MAX(sub_ack_at) AS message_acked
  FROM mqtt_message_traces
  WHERE event = 'message.acked'
    AND "timestamp" >= now() - INTERVAL '1 hour'
  GROUP BY msg_id, sub_clientid
),
message_latency AS (
  SELECT
    p.msg_id,
    p.publish_at,
    p.publish_received_at,
    d.message_delivered,
    a.message_acked
  FROM publish_events p
  JOIN delivered_events d ON p.msg_id = d.msg_id
  JOIN ack_events a
    ON p.msg_id = a.msg_id
   AND d.sub_clientid = a.sub_clientid
)
SELECT
  SUM(CASE WHEN publish_received_at - publish_at < 0 THEN 1 ELSE 0 END) AS negative_publisher_to_emqx,
  SUM(CASE WHEN message_delivered - publish_received_at < 0 THEN 1 ELSE 0 END) AS negative_emqx_processing,
  SUM(CASE WHEN message_acked - message_delivered < 0 THEN 1 ELSE 0 END) AS negative_subscriber_ack,
  SUM(CASE WHEN message_acked - publish_at < 0 THEN 1 ELSE 0 END) AS negative_end_to_end
FROM message_latency
WHERE publish_at IS NOT NULL
  AND publish_received_at IS NOT NULL
  AND message_delivered IS NOT NULL
  AND message_acked IS NOT NULL;
```

Only when all four values are 0 can the result be considered valid. If any count is non-zero, check the timestamp mapping and clock synchronization configuration before using the result as a final conclusion.

## Result Validation

Before publishing final latency results, verify all of the following conditions:

- All three tracing record types exist: `message.publish`, `message.delivered`, and `message.acked`.
- Key timestamp fields, including `publish_at`, `emqx_received_at`, `emqx_delivered_at`, and `sub_ack_at`, are populated correctly.
- The average latency query returns a meaningful `sample_count`.
- The negative-value validation query returns 0.
- EMQX Rule Action metrics do not show abnormal failure counts.

## Notes

- The action write syntax in this article uses the stable Tables format, writing values as fields instead of line protocol tags.
- It is not recommended to use `PRIMARY KEY(trace_key)` in this tracing table. Otherwise, it will be inconsistent with the action write semantics and may lead to unstable writes.
- To cover all business topics, change `FROM "emqx/test"` in the publish rule to `FROM "#"`.
- If multiple Subscribers exist, the same message may generate multiple `message.delivered` and `message.acked` records. In queries, correlate records by both `msg_id` and `sub_clientid`.

## Summary

With EMQX Cloud Event Topics, Rule Engine, and Tables, you can build a lightweight end-to-end tracing solution for MQTT messages.

This solution splits the message lifecycle into three stages: publish, delivery, and acknowledgment. It then correlates these stages through a shared `msg_id`, enabling:

- Publisher-to-Broker latency analysis
- Broker delivery path analysis
- Subscriber ACK confirmation analysis
- End-to-end latency calculation
- Missing ACK and incomplete path detection
- SQL-based troubleshooting and statistical analysis

For MQTT scenarios that require diagnosing message latency, message loss, consumption exceptions, and ACK timeouts, EMQX Tables provides more fine-grained message lifecycle observability than relying only on Broker metric monitoring.

With SQL, you can perform message tracing, latency analysis, ACK detection, and exception troubleshooting without deploying an additional tracing system or log platform.

For enterprise scenarios that require diagnosing message latency, message loss, consumption exceptions, and ACK timeout issues, EMQX Tables provides a lightweight, native, and easy-to-implement end-to-end MQTT observability solution.


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
