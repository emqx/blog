## TL;DR



- Message History maps an MQTT topic filter to a table in EMQX Tables. Selected fields from matching messages become rows you can query with SQL, and EMQX Cloud manages the connector, rule, and action behind the mapping.
- Operations teams can preview stored records, monitor pipeline metrics, and use SQL in EMQX Tables to investigate historical device behavior.
- Storage starts when a mapping is enabled. Earlier messages aren't backfilled.

## Give Your MQTT Topics a History



An MQTT broker routes messages, but it doesn't keep a history of them. For the topics you map, Message History does.

Customer Support kept hearing the same question: after an incident, how can an operations team tell whether an expected message went missing?

To investigate an incident, operations teams need answers to two questions:

- Did the expected telemetry reach the persistence pipeline?
- What data did the device report during the incident window?

Retained Messages keep the last retained message on a topic and deliver it to new subscribers. That's useful for current state, but it isn't a series of readings you can query. While EMQX Cloud provides [Event History](https://docs.emqx.com/en/cloud/latest/deployments/event_history.html) for troubleshooting recent client activity, it is not designed to retain historical MQTT payload data.

**Message History** fills this gap by capturing selected MQTT message data in EMQX Tables, giving operations teams records they can query with SQL and pipeline metrics for subsequent investigation.

## What Message History Adds



Message History turns selected MQTT traffic into queryable records in EMQX Tables without requiring operators to build and maintain the connector, rule, and action themselves.

To create a message history mapping, an operator:

1. Select the EMQX Tables deployment, database, and user and configure the storage settings.
2. Select the MQTT topic filter.
3. Enter a table name. If the table doesn't exist yet, the first successful write creates it.
4. Map payload fields and message metadata to table columns.
5. Assign each column a role: tag, field, or timestamp.
6. Enable the mapping and verify that data is being written.

Behind the mapping, EMQX Cloud creates or reuses an EMQX Tables connector and creates the corresponding managed rule and action:

![img](https://assets.emqx.com/images/5e8ca3a883d24e6c2acfa049f313334a.png)

EMQX Tables stores the records and runs your SQL queries, while Message History manages the mapping and its associated data integration resources. For configuration steps, management options, and operational considerations, see the [Message History documentation](https://docs.emqx.com/en/cloud/latest/deployments/message_history.html).

## An Operations Example: Investigating Missing Telemetry



Consider a fleet of industrial devices publishing telemetry topics matched by the following filter:

```
factory/+/telemetry
```

A typical payload might look like this:

```json
{
  "device_id": "press-17",
  "temperature": 74.6,
  "pressure": 118.2,
  "recorded_at": 1793152800000
}
```

An operator notices that a machine's telemetry is missing from a downstream monitoring application and needs to determine whether the device reported the data during the incident window.

In the mapping wizard, select the public database, enter factory/+/telemetry as the MQTT Topic and sensor_history as the Table Name, and paste the payload above as the MQTT Message Example. For this investigation, map the payload as follows:

| Source value        | Target column | Table role | Operational purpose                           |
| :------------------ | :------------ | :--------- | :-------------------------------------------- |
| payload.device_id   | `device_id`   | Tag        | Filter and group records by device            |
| payload.temperature | `temperature` | Field      | Analyze the reported measurement              |
| payload.pressure    | `pressure`    | Field      | Analyze the reported measurement              |
| payload.recorded_at | `timestamp`   | Timestamp  | Preserve when the device produced the reading |

Tags work well for identifiers that operators frequently use for filtering and grouping. Fields represent changing measurements. Every mapping must contain at least one field.

Under **Fields**, find `payload.device_id` and click the **Move to Tags** icon on that row. Keep `payload.temperature` and `payload.pressure` under **Fields**.

Under **Timestamp Column**, select `payload.recorded_at` as the **Timestamp Source**, set **Time Precision** to `Milliseconds (ms)`, and keep the column name as `timestamp`. Once selected as the timestamp source, `payload.recorded_at` is automatically removed from **Fields**.

![image.png](https://assets.emqx.com/images/d254937daf3a5f952301bec2034d2bd4.png)

Move `payload.device_id` to **Tags** so operators can filter and group records by device.

If a payload doesn't include a device ID, use **Add Tag** to map the MQTT `clientid` instead, so each row still identifies the client that sent it.

Choose the timestamp based on the question you need to answer:

- **Broker Received Time:** When the message entered EMQX Cloud. Use it to investigate ingestion.
- **A timestamp from the payload:** When the device produced the measurement. Use it to reconstruct device activity, especially when devices buffer messages offline and publish them after reconnecting.

For schema and timestamp recommendations, see [Design and Query Message History Data](https://docs.emqx.com/en/cloud/latest/deployments/message_history_data_design.html).

To test the mapping, open Diagnostics > MQTT Client in the Broker deployment, connect, and publish the payload to factory/press-17/telemetry. Replace `recorded_at` with a new current Unix timestamp in milliseconds before publishing each message, and set time precision to milliseconds (ms). The relative time queries later in this section use `now()`; if you keep the fixed example timestamp, query an explicit historical time range instead.

Back in Message History, expand the mapping row to preview up to 10 recent records, or click the mapping ID to check its Success, Failed, and Dropped metrics.

The preview shows that records are arriving. To filter and aggregate them, open Data Explorer in the linked EMQX Tables deployment and select the public database.

Once messages are stored, an operator can inspect the latest records:

```sql
SELECT *
FROM public."sensor_history"
ORDER BY "timestamp" DESC
LIMIT 10;
```

Or check whether a specific device produced data during the last five minutes:

```sql
SELECT *
FROM public."sensor_history"
WHERE "device_id" = 'press-17'
  AND "timestamp" >= now() - '5 minutes'::INTERVAL
ORDER BY "timestamp" DESC;
```

Because the factory/+/telemetry mapping stores the whole fleet in one table tagged by device_id, one query can compare every machine. This one calculates each device's average temperature for the last hour:

```sql
SELECT device_id, avg(temperature) AS avg_temperature
FROM public."sensor_history"
WHERE "timestamp" >= now() - '1 hour'::INTERVAL
GROUP BY device_id;
```

![image.png](https://assets.emqx.com/images/8fee8deaad74b7fd468e65b6fa3ba5f9.png)

[Average temperature by device from a test run using fixed example timestamps.]{.block .text-center}

## What a Stored Record Does and Does Not Prove



A stored row confirms the storage path, not end-to-end MQTT delivery.

Specifically, it confirms that:

- The message reached the EMQX Cloud Broker.
- Its topic matched the enabled mapping.
- The selected fields were processed successfully.
- The managed EMQX Tables action wrote the record to EMQX Tables.

It does **not** prove that every intended MQTT subscriber received the message. Subscriber delivery is a separate stage of the MQTT message path.

A missing row is less conclusive. Before assuming that the broker dropped the message, check:

1. Whether the mapping was enabled when the message was published.
2. Whether the mapping's action is still enabled in Data Integration. The Enable switch in Message History controls only the rule, so a mapping can look enabled while nothing is written.
3. Whether the topic matched the configured topic filter.
4. Whether the message contained the expected fields and timestamp format.
5. Whether the mapping reported successful, failed, or dropped executions.
6. Whether credentials, network connectivity, schema compatibility, or Data Integration limits affected the write.

For deeper message-lifecycle investigations, operations teams can combine Message History with logs, Log Trace (which can trace a specific client, topic, or rule ID), and Data Integration rules that capture EMQX event topics. EMQX Cloud provides event topics for observing message publication and drop events when more detailed evidence is required. For an example, see [Capture Message Publish and Drop Event Topic Messages via Data Integration](https://docs.emqx.com/en/cloud/latest/best_practices/messages_event_topic.html).

## What EMQX Tables Adds



Message History handles the mapping and the writes. EMQX Tables is the managed time-series database that stores the records and runs queries on them. It's built into EMQX Cloud, powered by GreptimeDB, and managed in the same console as your Broker.

With telemetry in Tables, you can:

- Look back at the readings before and after an incident to see what changed.
- Compare equipment performance across weeks, months, and seasons, as long as the table's TTL keeps the data that long.
- Query with SQL in Data Explorer, or with PromQL and visualize the results in Grafana.
- Set retention periods for databases and tables so older data expires automatically.

## Choose the Right Tool for Each Investigation



| Capability           | Best suited for                                              | Storage and scope                                            |
| :------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Event History**    | Recent connection, authentication, subscription, and disconnection troubleshooting | Short-lived diagnostic records stored locally by EMQX, with no fixed retention period and a 10,000-event query limit |
| **Message History**  | SQL analysis of selected MQTT message fields over time       | Selected payload and metadata fields stored in EMQX Tables   |
| **Data Integration** | Custom event processing, transformations, multiple destinations, and advanced message-lifecycle capture | Operator-defined rules, actions, and external destinations   |

Message History builds on the Data Integration connector, rule, and action model. You can open a mapping's rule in Data Integration to edit its Rule SQL or action settings, while Message History continues to manage the connector and the mapping lifecycle.

## Before You Enable Message History



Before enabling a mapping in production, decide what to store, how long to retain it, and how to monitor writes.

### Limit the Topic Scope



A broad topic filter can store more data than intended and consume additional Data Integration TPS. Store only the topics and fields that your team expects to query.

### Design the Schema for Investigation



Use stable identifiers as tags and changing measurements as fields. Avoid treating every payload attribute as a separate column without considering how operators will query it.

If the target table doesn't exist, the first successful write creates it, and the values in that write set the column types. If a device firmware update changes a field's data type, writes to an existing table may fail because of a schema mismatch. For incompatible schema changes, a new table and mapping may be safer than changing the meaning of an existing column.

### Set an Appropriate Retention Policy



Disabling or deleting a Message History mapping stops new writes but does not delete records already stored in EMQX Tables. Existing records remain until they are explicitly removed or expire according to the table's TTL configuration. Tables created through Message History use the TTL set in the wizard's Storage Location step, which defaults to 30 days. If a mapping reuses an existing Message History connector, the TTL and timestamp column name are read-only, and the TTL applies only to tables created through that connector. It doesn't change the TTL of an existing table.

Retention should balance troubleshooting requirements, compliance obligations, query performance, and storage cost.

### Monitor the Write Path



The mapping exposes success, failure, and dropped execution metrics. These metrics describe the path from the matching rule to EMQX Tables; they are not end-to-end MQTT delivery metrics.

After creating or modifying a mapping, repeat the test from the example above: publish a representative message, check the metrics and preview, then query the table and confirm that identifiers, measurements, and timestamps mean what you intended.

### Remember That History Starts When the Mapping Starts



Message History only stores matching messages received while the mapping is enabled. It does not backfill messages published earlier, and it does not replay stored data to MQTT subscribers.

## Availability and Prerequisites



At the time of writing, Message History is available on EMQX Dedicated and Dedicated Flex deployments running EMQX version 6.1.4 or later.

The Broker and EMQX Tables deployments must be reachable within the same network. An EMQX Tables deployment reached from another network through a NAT Gateway or PrivateLink is not eligible for this workflow. If you don't have an eligible Tables deployment yet, the Message History wizard offers a New EMQX Tables option that creates one in the Broker's project, platform, region, and network.

The Tables user needs the `SqlSelect` and `SqlInsert` privileges. The **Broker Integration** preset grants both.

For high-volume mappings, include Data Integration TPS and connector limits in capacity planning.

Because product availability and limits can change, consult the maintained [Message History documentation](https://docs.emqx.com/en/cloud/latest/deployments/message_history.html) before deployment.

## A Queryable Record of MQTT Traffic



Message History makes historical MQTT data available for operational investigation without manually configuring a data integration pipeline. By combining queryable message records with Event History and Data Integration monitoring, EMQX Cloud gives operations teams better visibility into what devices reported, when messages entered the persistence pipeline, and where data processing issues occurred.

New to EMQX Tables? [Explore EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) and start a 14-day trial.

Already on Dedicated or Dedicated Flex? [Create your first mapping](https://docs.emqx.com/en/cloud/latest/deployments/message_history.html).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
