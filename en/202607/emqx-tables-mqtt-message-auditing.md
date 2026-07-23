## Why Message-Level Visibility Matters

When an MQTT messaging issue occurs, the first questions are often simple:

- Was the message published?
- Was it delivered to the intended subscriber?
- Was the QoS acknowledgment received?
- What happened to the message after it left the publisher?

Standard Broker metrics such as TPS, connection count, and throughput can indicate overall system health, but they cannot answer these message-level questions or reconstruct the lifecycle of an individual message.

For troubleshooting, operational auditing, and compliance, teams need a way to retain key MQTT message events and review them long after they occur.

## Building an MQTT Message Audit Pipeline with EMQX Tables

To address this challenge, EMQX combines **Event Topics**, **Rule Engine**, and **EMQX Tables** to continuously capture and retain key MQTT message events.

Instead of storing every MQTT packet, this solution records the message events that matter most (such as publish, delivery, and acknowledgment), making historical tracing and auditing possible with minimal infrastructure.

![image.png](https://assets.emqx.com/images/44a8b190f7d18e0ba651ca27a7c4539b.png)

Without Kafka, Elasticsearch, or a dedicated logging platform, message events can be stored, queried, and analyzed through a single workflow.

In this article, you'll build a lightweight MQTT message audit platform that records message publish, delivery, and ACK events, enabling historical message tracing through SQL queries.

## Prerequisites

Before you begin, make sure:

- An [EMQX Cloud deployment](https://docs.emqx.com/en/cloud/latest/create/dedicated.html) has been created.
- EMQX Tables has been enabled.
- The current account has permission to create Rules, Actions, and Tables.
- MQTT clients can connect normally.
- Test messages use QoS 1 or QoS 2.

Note: The `message.acked` event is generated only for QoS 1 or QoS 2. If QoS 0 is used, only Publish and Delivered can be audited, and ACK records cannot be generated.

The example Topic in this article is:

```
emqx/test
```

For production environments, replace it with a specific business Topic, for example:

```
devices/+/events
```

Do not use `#` directly in production to capture all messages unless the data volume and storage cost have been evaluated.

## Create the Audit Log Table

Create an audit log table in EMQX Tables. After all message events are written into the same audit table, historical message behavior can be quickly traced by Message ID, Client ID, or Topic:

```sql
CREATE TABLE mqtt_audit_logs (

  "timestamp" TIMESTAMP TIME INDEX,

  "event" STRING,

  "msg_id" STRING,

  "pub_clientid" STRING,

  "sub_clientid" STRING,

  "topic" STRING,

  "qos" BIGINT,

  "audit_stage" STRING

)

WITH (

  'append_mode'='true',

  'ttl'='90d'

);
```

Field descriptions:

- `timestamp`: Event time.
- `event`: EMQX event name, such as `message.publish`.
- `msg_id`: EMQX message ID.
- `pub_clientid`: Publisher Client ID.
- `sub_clientid`: Subscriber Client ID.
- `topic`: MQTT Topic.
- `qos`: QoS level.
- `audit_stage`: Audit stage. Possible values are `publish`, `delivered`, and `acked`.

Audit logs are append-only event streams. Therefore, it is recommended to enable `append_mode='true'` and avoid primary key designs that would introduce overwrite semantics.

## Create Publish Audit

Publish Audit records messages entering the Broker.

Rule SQL:

```sql
SELECT

  timestamp,

  event,

  id AS msg_id,

  clientid AS pub_clientid,

  topic,

  qos

FROM "emqx/test"
```

Action write syntax:

```
mqtt_audit_logs event=${event},msg_id=${msg_id},pub_clientid=${pub_clientid},sub_clientid=none,topic=${topic},qos=${qos}i,audit_stage=publish ${timestamp}
```

Notes:

- `qos` is an integer and must be written as `${qos}i`.
- A Publish event has no subscriber Client ID, so `sub_clientid` is fixed as `none`.
- Use `${timestamp}` as the timestamp, and make sure the time column in the Tables Connector is `timestamp`.

## Create Delivered Audit

Delivered Audit records messages delivered to subscriber clients.

Rule SQL:

```sql
SELECT

  timestamp,

  event,

  id AS msg_id,

  from_clientid AS pub_clientid,

  clientid AS sub_clientid,

  topic,

  qos

FROM "$events/message_delivered"

WHERE topic = 'emqx/test'
```

Action write syntax:

```
mqtt_audit_logs event=${event},msg_id=${msg_id},pub_clientid=${pub_clientid},sub_clientid=${sub_clientid},topic=${topic},qos=${qos}i,audit_stage=delivered ${timestamp}
```

## Create ACK Audit

ACK Audit records QoS 1 or QoS 2 messages that have received client ACKs.

Rule SQL:

```sql
SELECT

  timestamp,

  event,

  id AS msg_id,

  from_clientid AS pub_clientid,

  clientid AS sub_clientid,

  topic,

  qos

FROM "$events/message_acked"

WHERE topic = 'emqx/test'
```

Action write syntax:

```
mqtt_audit_logs event=${event},msg_id=${msg_id},pub_clientid=${pub_clientid},sub_clientid=${sub_clientid},topic=${topic},qos=${qos}i,audit_stage=acked ${timestamp}
```

## Validate with MQTT Clients

Start the subscriber first, then start the publisher. Keep the subscriber online. After the publisher sends QoS 1 messages, keep the connection for a few seconds to ensure that ACK events are generated completely.

Subscriber example:

```shell
python3 subscriber.py \

  --host xxxx.dedicated.aws.mqttce.net \

  --port 1883 \

  --topic emqx/test \

  --qos 1 \

  --duration-sec 70 \

  --username test \

  --password test
```

Publisher example:

```shell
python3 publisher.py \

  --host xxxx.dedicated.aws.mqttce.net \

  --port 1883 \

  --topic emqx/test \

  --qos 1 \

  --tps 1 \

  --duration-sec 5 \

  --hold-sec 5 \

  --username test \

  --password test
```

## View Audit Logs

Query the latest audit records:

```sql
SELECT

  "timestamp",

  event,

  audit_stage,

  topic,

  qos,

  pub_clientid,

  sub_clientid,

  msg_id

FROM mqtt_audit_logs

ORDER BY "timestamp" DESC

LIMIT 20;
```

Count records by audit stage:

```sql
SELECT

  audit_stage,

  count(*) AS cnt

FROM mqtt_audit_logs

WHERE "timestamp" > now() - INTERVAL '10 minutes'

GROUP BY audit_stage

ORDER BY audit_stage;
```

Query by Topic:

```sql
SELECT

  "timestamp",

  event,

  audit_stage,

  topic,

  qos,

  pub_clientid,

  sub_clientid,

  msg_id

FROM mqtt_audit_logs

WHERE topic = 'emqx/test'

ORDER BY "timestamp" DESC

LIMIT 50;
```

Query by publisher client:

```sql
SELECT

  "timestamp",

  event,

  audit_stage,

  topic,

  qos,

  pub_clientid,

  sub_clientid,

  msg_id

FROM mqtt_audit_logs

WHERE pub_clientid = 'python-mqtt-pub-10407'

ORDER BY "timestamp" DESC

LIMIT 50;
```

Query the full trace by Message ID:

```sql
SELECT

  "timestamp",

  event,

  audit_stage,

  topic,

  qos,

  pub_clientid,

  sub_clientid,

  msg_id

FROM mqtt_audit_logs

WHERE msg_id = 'your-message-id'

ORDER BY "timestamp" ASC;
```

If the same `msg_id` has all three records, `publish`, `delivered`, and `acked`, you can confirm that the message entered the Broker, was delivered to the subscriber, and received a client ACK.

## Validation Results

In actual validation, QoS 1 test messages were successfully written into EMQX Tables:

- Publish Action: write succeeded; `failed` was 0 and `dropped` was 0.
- Delivered Action: write succeeded; `failed` was 0 and `dropped` was 0.
- ACK Action: write succeeded; `failed` was 0 and `dropped` was 0.

Records similar to the following can be queried from EMQX Tables:

```
message.publish    publish    emqx/test    qos=1    pub_clientid=publisher-client    sub_clientid=none message.delivered  delivered  emqx/test    qos=1    pub_clientid=publisher-client    sub_clientid=subscriber-client message.acked      acked      emqx/test    qos=1    pub_clientid=publisher-client    sub_clientid=subscriber-client
```

This indicates that MQTT messages have been successfully written into EMQX Tables through Rule Engine and can be traced historically through SQL.

## Notes

- `message.acked` is generated only for QoS 1 or QoS 2.
- If there is no subscriber, you usually see only Publish events, not Delivered or ACK events.
- In production, match specific business Topics. Do not directly use `#` to capture all messages.
- `qos` is an integer, so it should be written as `${qos}i` in the Action.
- It is not recommended to write the complete JSON Payload directly into line protocol. Commas, spaces, and quotation marks in the Payload may affect write stability. If you need to save the Payload, extract key fields first, or design a dedicated escaping and cleansing process.
- Audit logs are append-only event streams, so it is recommended to enable `append_mode='true'`.

## Practical Value

- **MQTT Device Behavior Audit:** Verify whether devices actually published messages to the Broker.
- **Topic Activity Tracing:** Analyze historical message activity for a specified Topic.
- **Troubleshooting:** Confirm whether a message entered the Broker, whether it was delivered, and whether an ACK was received.
- **Security Audit:** Analyze historical client behavior and help identify abnormal access activity.
- **Compliance Retention:** Retain historical MQTT activity records for audit and operations analysis.

## Summary

In this article, you built a lightweight MQTT message audit platform using EMQX Event Topics, Rule Engine, and EMQX Tables to record, retain, and query key message events.

By storing message event metadata instead of every MQTT packet, EMQX Tables enables efficient historical tracing and auditing with minimal infrastructure.

For MQTT-native applications that require message auditing, troubleshooting, or compliance, EMQX Tables provides a simple and cost-effective foundation for long-term message visibility.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
