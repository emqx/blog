## 1. Continuous MQTT Audit Without Long-Term Trace

Intermittent MQTT connection issues are often difficult to troubleshoot. By the time an issue is discovered, Trace may not have been enabled. Even if the problem occurs again, reproducing it can be difficult.

A common request from customers is to retain enough historical information to investigate issues after they occur, without relying on reproducing them.

While EMQX Trace provides detailed MQTT packet interactions, keeping it enabled continuously is not ideal for every deployment. Long-term Trace can introduce additional performance overhead, increase payload retention and compliance concerns, and still cannot recover historical data from before it was enabled.

In many cases, retaining every MQTT packet is unnecessary. What teams really need is a lightweight, always-on way to preserve key client and message events, including connections, authentication, subscriptions, message delivery, and disconnect reasons.

This is where EMQX Tables fits. Rather than replacing Trace, it provides a cost-effective way to continuously store high-value MQTT event metadata. Combined with EMQX Cloud v5 Event Topics, Rule Engine, and Data Integration, it enables long-term auditing of client lifecycle and message flow events.

The solution continuously records:

- Client connection and disconnection times
- Disconnect reasons
- Authentication and authorization results
- Subscribe and unsubscribe events
- Message delivery and acknowledgment events
- Message drop and delivery failure events

All events are written to a single EMQX Tables table, where they can be queried with SQL. Instead of re-enabling Trace or searching Broker logs after an issue occurs, teams can quickly reconstruct a client's historical activity from the stored event records.

## 2. Solution Architecture

![image.png](https://assets.emqx.com/images/0a00a3095c2d0b592fccfe0d68df60ad.png)This solution focuses on retaining event metadata rather than full business payloads. If payloads are large or contain sensitive information, they should be masked, truncated, or omitted altogether.

Without relying on Kafka, a logging system, or an external database, it provides a lightweight way to retain, query, and analyze client lifecycle events over the long term.

## 3. Validation Results

This validation was completed with an EMQX Cloud Dedicated deployment and an EMQX Tables instance.

**Validation environment:**

- MQTT Broker: EMQX Cloud Dedicated
- MQTT port: 1883
- Tables: EMQX Tables
- Tables Database: `public`
- Tables Connector: connected
- MQTT test method: QoS 1 publish, subscribe, unsubscribe, and disconnect

**Validation results:**

| Event                         | Event Topic                           | Validation Result                                            |
| :---------------------------- | :------------------------------------ | :----------------------------------------------------------- |
| `client_connected`            | `$events/client_connected`            | Verified. Written successfully.                              |
| `client_connack`              | `$events/client_connack`              | Verified. Written successfully.                              |
| `client_disconnected`         | `$events/client_disconnected`         | Verified. Written successfully.                              |
| `client_check_authn_complete` | `$events/client_check_authn_complete` | Verified. Written successfully.                              |
| `client_check_authz_complete` | `$events/client_check_authz_complete` | Verified. Written successfully.                              |
| `session_subscribed`          | `$events/session_subscribed`          | Verified. Written successfully.                              |
| `session_unsubscribed`        | `$events/session_unsubscribed`        | Verified. Written successfully.                              |
| `message_delivered`           | `$events/message_delivered`           | Verified. Written successfully.                              |
| `message_acked`               | `$events/message_acked`               | Verified. Written successfully.                              |
| `message_dropped`             | `$events/message_dropped`             | Rule can be created. It is triggered only when a message is dropped by the Broker. |
| `delivery_dropped`            | `$events/delivery_dropped`            | Rule can be created. It is triggered only when delivery is dropped. |

Actual database write summary from this normal MQTT QoS 1 publish/subscribe flow:

```sql
SELECT event_type, count(*) AS cnt
FROM emqx_client_lifecycle_logs
GROUP BY event_type
ORDER BY event_type;
```

Example result:

| event_type                    | cnt  |
| :---------------------------- | :--- |
| `client_check_authn_complete` | 3    |
| `client_check_authz_complete` | 3    |
| `client_connack`              | 3    |
| `client_connected`            | 4    |
| `client_disconnected`         | 3    |
| `message_acked`               | 1    |
| `message_delivered`           | 1    |
| `session_subscribed`          | 2    |
| `session_unsubscribed`        | 1    |

Note: `message_dropped` and `delivery_dropped` are not mandatory events in a normal successful publish/subscribe flow. They are generated only in exceptional scenarios such as message drop, queue expiration, delivery failure, No Local, or an unreachable subscriber.

## 4. Create the Audit Log Table

Create a table in EMQX Tables Data Explorer. By writing all key client events into a single time-series table, you can quickly review the complete behavior path of a single Client through SQL:

```sql
CREATE TABLE emqx_client_lifecycle_logs (
    "timestamp" TIMESTAMP TIME INDEX,
    clientid STRING,
    event_type STRING,
    username STRING,
    peerhost STRING,
    topic STRING FULLTEXT INDEX,
    node STRING,
    raw_event STRING FULLTEXT INDEX,
    PRIMARY KEY (clientid, event_type, topic)
)
WITH (
    append_mode='true',
    ttl='7d'
);
```

Field descriptions:

| Field        | Description                                                  |
| :----------- | :----------------------------------------------------------- |
| `timestamp`  | Event occurrence time                                        |
| `clientid`   | MQTT Client ID                                               |
| `event_type` | Event type                                                   |
| `username`   | MQTT username                                                |
| `peerhost`   | Client source address                                        |
| `topic`      | Event-related Topic. Events without a Topic are written as `none`. |
| `node`       | EMQX node                                                    |
| `raw_event`  | Extended event information as a JSON string                  |

Key design points:

- `append_mode='true'`: Logs are written in append mode and historical records are not overwritten;
- `ttl='7d'`: The default retention period is 7 days and can be adjusted according to the customer scenario;
- `topic='none'`: Connection, authentication, CONNACK, and similar events do not have a Topic. Empty topic tags should not be used in the Action, so it is recommended to write `none` consistently;
- `raw_event`: Stores extended event fields such as `reason`, `qos`, `from_clientid`, `result`, and `action`.

## 5. Create the EMQX Tables Action

Create an EMQX Tables Action in the EMQX Cloud console.

Use the following Action Body:

```
emqx_client_lifecycle_logs,clientid=${clientid},event_type=${event_type},topic=${topic} username=${username},peerhost=${peerhost},node=${node},raw_event=${raw_event} ${ts}
```

Notes:

- `clientid`, `event_type`, and `topic` are used as tags for querying by client, event type, and Topic;
- `username`, `peerhost`, `node`, and `raw_event` are used as fields;
- All Rule SQL statements must output `ts`, `clientid`, `event_type`, `username`, `peerhost`, `topic`, `node`, and `raw_event`;
- Events without Topic, `peerhost`, or `node` must be supplemented with `'none'` in Rule SQL to avoid Action write failures.

Compared with a traditional logging platform, this solution does not require an additional data synchronization pipeline. Events can be written directly into Tables as soon as they are generated and queried immediately.

## 6. Event Topics Rule Configuration

The following Rules can be created separately and bound to the same EMQX Tables Action.

### 6.1 Client Connected

Event topic:

```
$events/client_connected
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  peername AS peerhost,
  'none' AS topic,
  str(node) AS node,
  'client_connected' AS event_type,
  json_encode(
    map_put('proto_ver', proto_ver,
      map_put('proto_name', proto_name,
        map_put('keepalive', keepalive,
          json_decode('{}')
        )
      )
    )
  ) AS raw_event
FROM "$events/client_connected"
```

### 6.2 Client Connack

Event topic:

```
$events/client_connack
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  peername AS peerhost,
  'none' AS topic,
  str(node) AS node,
  'client_connack' AS event_type,
  json_encode(
    map_put('reason_code', reason_code,
      map_put('keepalive', keepalive,
        json_decode('{}')
      )
    )
  ) AS raw_event
FROM "$events/client_connack"
```

### 6.3 Client Disconnected

Event topic:

```
$events/client_disconnected
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  peername AS peerhost,
  'none' AS topic,
  str(node) AS node,
  'client_disconnected' AS event_type,
  json_encode(
    map_put('reason', reason,
      map_put('connected_at', connected_at,
        json_decode('{}')
      )
    )
  ) AS raw_event
FROM "$events/client_disconnected"
```

### 6.4 Authentication

Event topic:

```
$events/client_check_authn_complete
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  'none' AS topic,
  'none' AS node,
  'client_check_authn_complete' AS event_type,
  json_encode(
    map_put('reason_code', reason_code,
      json_decode('{}')
    )
  ) AS raw_event
FROM "$events/client_check_authn_complete"
```

### 6.5 Authorization

Event topic:

```
$events/client_check_authz_complete
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  'none' AS node,
  'client_check_authz_complete' AS event_type,
  json_encode(
    map_put('action', action,
      map_put('result', result,
        json_decode('{}')
      )
    )
  ) AS raw_event
FROM "$events/client_check_authz_complete"
```

### 6.6 Session Subscribed

Event topic:

```
$events/session_subscribed
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'session_subscribed' AS event_type,
  json_encode(
    map_put('qos', qos,
      json_decode('{}')
    )
  ) AS raw_event
FROM "$events/session_subscribed"
```

### 6.7 Session Unsubscribed

Event topic:

```
$events/session_unsubscribed
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'session_unsubscribed' AS event_type,
  json_encode(json_decode('{}')) AS raw_event
FROM "$events/session_unsubscribed"
```

### 6.8 Message Delivered

Event topic:

```
$events/message_delivered
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'message_delivered' AS event_type,
  json_encode(
    map_put('qos', qos,
      map_put('from_clientid', from_clientid,
        map_put('id', id,
          json_decode('{}')
        )
      )
    )
  ) AS raw_event
FROM "$events/message_delivered"
```

### 6.9 Message Acked

Event topic:

```
$events/message_acked
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'message_acked' AS event_type,
  json_encode(
    map_put('qos', qos,
      map_put('from_clientid', from_clientid,
        map_put('id', id,
          json_decode('{}')
        )
      )
    )
  ) AS raw_event
FROM "$events/message_acked"
```

Note: `message_acked` is generated only after a QoS 1 or QoS 2 message is acknowledged by the subscriber.

### 6.10 Message Dropped

Event topic:

```
$events/message_dropped
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'message_dropped' AS event_type,
  json_encode(
    map_put('qos', qos,
      map_put('reason', reason,
        map_put('id', id,
          json_decode('{}')
        )
      )
    )
  ) AS raw_event
FROM "$events/message_dropped"
```

Note: This event is triggered only when a message is dropped inside the Broker. It is not generated by a normal successful publish.

### 6.11 Delivery Dropped

Event topic:

```
$events/delivery_dropped
```

Rule SQL:

```sql
SELECT
  timestamp AS ts,
  clientid,
  username,
  'none' AS peerhost,
  topic,
  str(node) AS node,
  'delivery_dropped' AS event_type,
  json_encode(
    map_put('qos', qos,
      map_put('reason', reason,
        map_put('from_clientid', from_clientid,
          map_put('id', id,
            json_decode('{}')
          )
        )
      )
    )
  ) AS raw_event
FROM "$events/delivery_dropped"
```

Note: This event is triggered only when delivery to the subscriber is dropped, for example because of queue expiration, an unreachable subscriber, or a specific delivery policy.

## 7. Validate with MQTT Clients

### 7.1 Start the Subscriber

```shell
mosquitto_sub \
  -h xxxx.dedicated.aws.mqttce.net \
  -p 1883 \
  -u test \
  -P test \
  -i lifecycle-sub-001 \
  -t 't/test/lifecycle' \
  -q 1 \
  -C 1 \
  -W 30
```

### 7.2 Publish a QoS 1 Message

```shell
mosquitto_pub \
  -h xxxx.dedicated.aws.mqttce.net \
  -p 1883 \
  -u test \
  -P test \
  -i lifecycle-pub-001 \
  -t 't/test/lifecycle' \
  -q 1 \
  -m '{"event":"lifecycle-validation","seq":1}'
```

### 7.3 Trigger Unsubscribe

```shell
mosquitto_sub \
  -h xxxx.dedicated.aws.mqttce.net \
  -p 1883 \
  -u test \
  -P test \
  -i lifecycle-unsub-001 \
  -t 't/test/unsub' \
  -U 't/test/unsub' \
  -q 1 \
  -E \
  -W 10
```

## 8. Query Audit Logs

### 8.1 View Recent Events

```sql
SELECT
  "timestamp",
  clientid,
  event_type,
  username,
  peerhost,
  topic,
  node,
  raw_event
FROM emqx_client_lifecycle_logs
ORDER BY "timestamp" DESC
LIMIT 50;
```

### 8.2 Review the Complete Lifecycle by Client ID

```sql
SELECT
  "timestamp",
  event_type,
  username,
  peerhost,
  topic,
  node,
  raw_event
FROM emqx_client_lifecycle_logs
WHERE clientid='lifecycle-sub-001'
ORDER BY "timestamp" ASC;
```

### 8.3 Query Disconnect Reasons

```sql
SELECT
  "timestamp",
  clientid,
  raw_event
FROM emqx_client_lifecycle_logs
WHERE event_type='client_disconnected'
ORDER BY "timestamp" DESC
LIMIT 20;
```

### 8.4 Query Authorization Results

```sql
SELECT
  "timestamp",
  clientid,
  topic,
  raw_event
FROM emqx_client_lifecycle_logs
WHERE event_type='client_check_authz_complete'
ORDER BY "timestamp" DESC
LIMIT 50;
```

### 8.5 Check Whether Messages Were Delivered and ACKed

```sql
SELECT
  "timestamp",
  clientid,
  event_type,
  topic,
  raw_event
FROM emqx_client_lifecycle_logs
WHERE event_type IN ('message_delivered', 'message_acked')
ORDER BY "timestamp" DESC
LIMIT 50;
```

### 8.6 Query Drop Events

```sql
SELECT
  "timestamp",
  clientid,
  event_type,
  topic,
  raw_event
FROM emqx_client_lifecycle_logs
WHERE event_type IN ('message_dropped', 'delivery_dropped')
ORDER BY "timestamp" DESC
LIMIT 50;
```

## 9. Data Volume and Retention Period Estimation

In high-TPS scenarios, message-related events usually account for most writes. Assume:

- Message In: 305 msg/s;
- Message Out: 161 msg/s;
- QoS 1 ACK events are approximately equal to Message Out;
- Each event is estimated at 300 Bytes.

Estimated daily event volume:

```
message publish    305 * 86400 ≈ 26.35M / day
message delivered  161 * 86400 ≈ 13.91M / day
message acked      161 * 86400 ≈ 13.91M / day
total              ≈ 54M / day
```

Estimated storage size:

```
54,000,000 * 300 Bytes ≈ 16.2 GB / day
7 days ≈ 113 GB
14 days ≈ 227 GB
```

Recommended TTL:

| Scenario                     | Recommended TTL |
| :--------------------------- | :-------------- |
| High-TPS production scenario | 3 days          |
| Test environment             | 7 days          |
| Long-term troubleshooting    | 14 days         |

Recommended default configuration:

```
ttl='7d'
```

If the customer's business message Payload is large, or if message TPS continues to grow, it is recommended to:

- Avoid storing full Payloads;
- Truncate or mask Payloads;
- Shorten TTL;
- Periodically evaluate the Tables storage size based on actual write volume.

## 10. Risks and Limitations

**Best suited for:**

- Troubleshooting MQTT client connection and disconnection issues
- Auditing MQTT authentication, authorization, and subscription activities
- Tracking message delivery and acknowledgment events
- Long-term retention and review of MQTT event metadata

**Not intended for:**

- Full MQTT packet-level tracing
- Long-term retention of complete business payloads
- Troubleshooting the internal execution flow of Data Integration
- Large-scale message archiving or analytics

 

Notes:

- Payload may contain sensitive data, so full Payload retention is not recommended by default;
- Long-term retention must comply with customer data compliance requirements;
- TTL must be controlled in high-TPS scenarios;
- Log query permissions should be restricted;
- `message_dropped` and `delivery_dropped` require exceptional scenarios to be triggered and are not generated by normal successful publish/subscribe flows.

## 11. Conclusion

This validation shows that EMQX Cloud V5 Event Topics, Rule Engine, and EMQX Tables can be used to build a lightweight, continuously running client lifecycle audit and event tracing solution.

The following events were verified and written successfully:

- `client_connected`;
- `client_connack`;
- `client_disconnected`;
- `client_check_authn_complete`;
- `client_check_authz_complete`;
- `session_subscribed`;
- `session_unsubscribed`;
- `message_delivered`;
- `message_acked`.

Compared with keeping Trace enabled continuously, this solution provides:

- Lower storage and operational costs
- Minimal impact on Broker performance
- Continuous, long-term event retention
- Fast SQL-based querying and historical analysis
- Efficient auditing of client lifecycle and message flow events

Rather than replacing Trace, EMQX Tables complements it by providing a lightweight, always-on audit layer for MQTT event metadata. Combined with EMQX Cloud Event Topics, Rule Engine, and Data Integration, it enables long-term retention and rapid investigation of client lifecycle and message flow events without the overhead of continuous packet tracing.

For organizations that need to investigate intermittent connection or message delivery issues, maintain audit records, or review historical client activity, EMQX Tables offers a simple, cost-effective, and natively integrated solution.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
