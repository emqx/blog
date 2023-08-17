We are excited to announce that [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.1.1 is now officially released!

This version adds QoS level and retain flag checks in authorization to allow more flexible client access control. It also introduces 3 new random functions in rules SQL to meet specific use case needs. Additionally, multiple bugs have been fixed.

> Try the latest version: [https://www.emqx.com/en/try?product=enterprise](https://www.emqx.com/en/try?product=enterprise)

## Authorization Supports Checking QoS Levels and Retain Flags

The publish-subscribe authorization feature in EMQX provides granular control over client behaviors.

The table below shows the composition of publish-subscribe permissions. Previously, only topics were supported in the conditions to specify allowed or denied topic scopes for clients.

EMQX Enterprise 5.1.1 adds QoS level and retain flag checks. Compared to the old rules with only topic checks, the new rules are more comprehensive and allow flexible multi-dimensional control over client access, improving system security.

| Permission | Client (Match)          | Action            | Conditions            |
| ---------- | ----------------------- | ----------------- | --------------------- |
| Allow/Deny | Client ID, Username, IP | Publish/Subscribe | Topics/**QoS/Retain** |

This is a backward-compatible feature. Users can continue to use existing configurations without changes. Or you can simply update the rules data and configurations to enable the new features. For example, with MySQL data source:

```
-- Before --
-- Permission data 
INSERT INTO mqtt_acl(username, topic, permission, action)
  VALUES('emqx_u', 't/1', 'deny');

-- EMQX Permission query SQL
SELECT action, permission, topic FROM mqtt_acl where username = ${username};

-- Now -- 
-- Permission data, added qos_i, retain_i field
INSERT INTO acl(username, topic, permission, action, qos_i, retain_i)  
  VALUES('username', 't/1', 'deny', 'publish', 1, 1);

-- EMQX Permission query SQL
SELECT permission, action, topic, qos_i as qos, retain_i as retain
          FROM mqtt_acl WHERE username = ${username};
```

## Rules SQL Supports Random and UUIDv4 Functions

Rules SQL adds 3 random functions to meet specific use case needs.

### random function

The random function generates a random float between 0 (inclusive) and 1 (exclusive). Here is a usage example:

```
random() = 0.521534842864676 
random() * 100 = 32.04042160431394
```

It can be used for sampling and simulation of massive data. For example, this SQL leverages random for probabilistic filtering in the WHERE clause, making only 50% of messages match the rule and get written to the database:

```
SELECT
  * 
FROM
  "t/#"
WHERE
  random() > 0.5
```

### uuid_v4 function

UUID (Universally Unique Identifier) is a common ID scheme consisting of 32 hexadecimal characters segmented with hyphens in 8-4-4-4-12 format. UUID version 4 (UUIDv4) is randomly generated to ensure strong randomness and broad usage.

In addition to standard UUID, EMQX provides a no-hyphen variant. Here is a usage example:

```
uuid_v4() = 04b31953-2f70-4ca0-a409-5c5f6b0a839f
uuid_v4_no_hyphen() = df272a785ac24d7fb82aa29af9e82dd8
```

The UUID functions can be used as database primary keys or unique identifiers for devices and messages, and for data tracking/auditing. For example, this SQL adds a `myid` field to the event context. The generated UUID can later be extracted in data bridges using `${myid}` syntax, and used as record ID or message ID:

```
SELECT
  uuid_v4() as myid,
  * 
FROM
  "t/#"
```

## Kafka Bridge Supports Setting Message Headers

Kafka message headers allow producers to include message metadata for passing additional context, enabling features like message tracing, deduplication, and data piping.

In EMQX Enterprise 5.1.1, you can define Kafka headers to be carried in Kafka data bridges, enabling the transfer of device information (e.g. clientID, username), message types, QoS levels, and even MQTT 5.0 user properties. This metadata can help backend applications parse and process massive amounts of IoT data with greater ease.

![Kafka Bridge](https://assets.emqx.com/images/52de62aaf7fd809dd377ed6e63be291d.png)

## Bug Fixes

Here are some major bug fixes:

- Wildcards are no longer allowed for the destination topic in topic rewrite [#11004](https://github.com/emqx/emqx/pull/11004).

- Added validation for the maximum number of `worker_pool_size` of a bridge resource [#11106](https://github.com/emqx/emqx/pull/11106).

- Fixed an issue in webhook bridge where, in async query mode, HTTP status codes like 4XX and 5XX would be treated as successes in the bridge metrics [#11162](https://github.com/emqx/emqx/pull/11162).

- REST API `DELETE` operations on non-existent resources now consistently returns `404` [#11211](https://github.com/emqx/emqx/pull/11211).

- In InfluxDB bridging, mixing decimals and integers in a field may lead to serialization failure in the Influx Line Protocol [#11223](https://github.com/emqx/emqx/pull/11223).

Please refer to the [EMQX Enterprise 5.1.1 changelog](https://www.emqx.com/en/changelogs/enterprise/5.1.1) for full details on feature changes and bug fixes.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
