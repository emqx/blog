MQTT topic is a string used in the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) to identify and route messages. It is a key element in communication between MQTT publishers and subscribers. In the [MQTT publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), publishers send messages to specific topics, while subscribers can subscribe to those topics to receive the messages.

In comparison to topics in other messaging systems, for example Kafka and Pulsar, MQTT topics are not to be created in advance. **The client will create the topic automatically when subscribing or publishing, and does not need to delete the topic.**

The following is a simple MQTT publish and subscribe flow. If APP 1 subscribes to the `sensor/2/temperature` topic, it will receive messages from Sensor 2 publishing to this topic.

![MQTT Publish Subscribe](https://assets.emqx.com/images/0c35bfdb730f1d29b7f1b7a249c62f8b.png?imageMogr2/thumbnail/1520x)

## Topics

A topic is a UTF-8 encoded string that is the basis for message routing in the MQTT protocol. A topic is typically leveled and separated with a slash `/` between the levels. This is similar to URL paths, for example:

```awk
chat/room/1
sensor/10/temperature
sensor/+/temperature
sensor/#
```

Although allowed, it is usually not recommended to use topics begin or end with `/`, such as `/chat` or `chat/`.

## MQTT Wildcards

MQTT wildcards are a special type of topic that can only be used for subscription and not publishing. Clients can subscribe to a wildcard topic to receive messages from multiple matching topics, eliminating the need to subscribe to each topic individually and reducing overhead. MQTT supports two types of wildcards: `+` (single-level) and `#` (multi-level).

### Single-level Wildcard

`+` (U+002B) is a wildcard character that matches only one topic level. When using a single-level wildcard, the single-level wildcard must occupy an entire level, for example:

```pgsql
"+" is valid
"sensor/+" is valid
"sensor/+/temperature" is valid
"sensor+" is invalid (does not occupy an entire level)
```

If the client subscribes to the topic `sensor/+/temperature`, it will receive messages from the following topics:

```awk
sensor/1/temperature
sensor/2/temperature
...
sensor/n/temperature
```

But it will not match the following topics:

```bash
sensor/temperature
sensor/bedroom/1/temperature
```

### Multi-level Wildcard

`#` (U+0023) is a wildcard character that matches any number of levels within a topic. When using a multi-level wildcard, it must occupy an entire level and must be the last character of the topic, for example:

```pgsql
"#" is valid, matches all topics
"sensor/#" is valid
"sensor/bedroom#" is invalid (+ or # are only used as a wildcard level)
"sensor/#/temperature" is invalid (# must be the last level)
```

## Topics Beginning with $

### System Topics

The topics starting with `$SYS/` are system topics mainly used to get metadata about the MQTT broker's running status, statistics, client online/offline events, etc. `$SYS/` topic is not defined in the MQTT specification. However, most [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) follow this [recommendation](https://github.com/mqtt/mqtt.org/wiki/SYS-Topics).

For example, the [EMQX](https://www.emqx.io/) supports getting cluster status through the following topics.

| Topic                           | Description              |
| ------------------------------- | ------------------------ |
| `$SYS/brokers`                  | EMQX cluster node list   |
| `$SYS/brokers/${node}/version`  | EMQX Broker version      |
| `$SYS/brokers/${node}/uptime`   | EMQX Broker startup time |
| `$SYS/brokers/${node}/datetime` | EMQX Broker time         |
| `$SYS/brokers/${node}/sysdescr` | EMQX Broker description  |

EMQX also supports rich system topics such as client online/offline events, statistics, system monitoring and alarms. For more details, please see the [EMQX System Topics](https://www.emqx.io/docs/en/v5.0/advanced/system-topic.html) documentation.

### Shared Subscriptions

Shared subscriptions are a feature of MQTT 5.0, a subscription method that achieves load balancing among multiple subscribers. The topic of a shared subscription starts with $share.

> Although the MQTT protocol added shared subscriptions in 5.0, EMQX has supported shared subscriptions since MQTT 3.1.1.

In the following diagram, three subscribers subscribe to the same topic `$share/g/topic` using a shared subscription method, where the `topic` is the real topic name they subscribe to, and the publishers publish messages to the `topic`, but *NOT* to `$share/g/topic`.

![MQTT Shared Subscriptions](https://assets.emqx.com/images/c248e9334ff6d32cbec0ed71cde98b1f.png?imageMogr2/thumbnail/1520x)

In addition, EMQX also supports the use of the shared subscription prefix `$queue` in MQTT 3.1.1. It is a special case of a shared subscription, which is equivalent to having all subscribers in one group.

For more details about shared subscriptions, please refer to [EMQX Shared Subscriptions](https://www.emqx.io/docs/en/v5.0/advanced/shared-subscriptions.html) documentation.

## Topics in Different Scenarios

### Smart Home

For example, we use sensors to monitor the temperature, humidity and air quality of bedrooms, living rooms and kitchens. We can design the following topics:

- `myhome/bedroom/temperature`
- `myhome/bedroom/humidity`
- `myhome/bedroom/airquality`
- `myhome/livingroom/temperature`
- `myhome/livingroom/humidity`
- `myhome/livingroom/airquality`
- `myhome/kitchen/temperature`
- `myhome/kitchen/humidity`
- `myhome/kitchen/airquality`

Next, you can subscribe to the `myhome/bedroom/+` topic to get temperature, humidity and air quality data for the bedroom, the `myhome/+/temperature` topic to get temperature data for all three rooms, and the `myhome/#` topic to get all the data.

### Charging Piles

- `ocpp/cp/cp001/notify/bootNotification`

  Publish an online request to this topic when the charging pile is online.

- `ocpp/cp/cp001/notify/startTransaction`

  Publish a charging request to this topic.

- `ocpp/cp/cp001/reply/bootNotification`

  Before the charging pile goes online, it needs to subscribe to this topic to receive the online response.

- `ocpp/cp/cp001/reply/startTransaction`

  Before the charging pile initiates the charging request, it needs to subscribe to this topic to receive the charging request response.

### Instant Messaging

- `chat/user/${user_id}/inbox`

  **One-to-one chat**: Users subscribe to this topic after they are online and will receive messages from their friends. When replying to a friend, just replace the user_id of the topic with the friend's id.

- `chat/group/${group_id}/inbox`

  **Group chat**: After the user successfully joins a group, they can subscribe to the topic to get the group's messages.

- `req/user/${user_id}/add`

  **Add a friend**: Publish a friend request to this topic (user_id is the friend's id).

  **Receive friend requests**: Subscribe to this topic (user_id is the subscriber's id) to receive friend requests from other users.

- `resp/user/${user_id}/add`

  **Receive replies to friend requests**: Before adding friends, the user needs to subscribe to this topic (user_id is the subscriber's id) to receive the request results.

  **Reply to friend request**: Send a message to this topic (user_id is the friend's id) about whether or not to approve the friend request.

- `user/${user_id}/state`

  **User Status**: Subscribe to this topic to get your friends' online status.

## MQTT Topics FAQ

### What is the maximum level and length of an MQTT topic?

MQTT topic is UTF-8 encoded strings, and it **MUST NOT be more than 65535 bytes**. However in practice, using shorter length topic names and fewer levels means less resource consumption.

Try not to use more topic levels “just because I can”. For example, `my-home/room1/data` is a better choice than `my/home/room1/data`.

### Is there a limit to the number of topics?

Different message servers have different limits on the number of topics. Currently, the default configuration of EMQX has no limit on the number of topics, but the more topics, the more server memory will be used.

Given the large number of devices connected to the MQTT Broker, we recommend that a client subscribes to no more than ten topics.

### Do wildcard subscriptions degrade performance?

When routing messages to wildcard subscriptions, the broker may require more resources than non-wildcard topics. It is a wise choice if the wildcard subscription can be avoided.

This very much depends on how the data schema is modeled for the MQTT message payload.

For example, if a publisher publishes to `device-id/stream1/foo` and `device-id/stream1/bar` and the subscriber needs to subscribe to both, then it may subscribe `device-id/stream1/#`. A better alternative is perhaps to push the foo and bar part of the namespace down to the payload, so it publishes to only one topic `device-id/stream1`, and the subscriber just subscribes to this one topic.

### How are messages received for overlapping subscriptions of normal and wildcard topics?

For example, if a client subscribes to both `#` and `test` topics, will it receive two duplicate messages when publishing to `test`? This depends on the MQTT broker implementation. EMQX will send messages for each matched subscription. Thus, duplicates may occur. However, users can leverage MQTT 5.0 subscription identifiers to differentiate message sources and handle such duplicate messages in the client based on the identifiers.

### Can I subscribe to the same topic with a shared subscription and a normal subscription?

Yes, but it is not recommended.

Per MQTT specification, multiple subscriptions will result in multiple (duplicated) message deliveries.

### What are the best practices for MQTT topics?

- Do not use `#` to subscribe to all topics.
- The topic should not start or end with `/`, such as `/chat` or `chat/`.
- Do not use spaces and non-ASCII characters in the topic.
- Use `_` or `-` to connect words (or camel case) within a topic level.
- Try to use less topic levels.
- Try to model the message data schema in favor to avoid using wildcard topics.
- When wildcard is in use, try to move the more unique topic level closer to root. e.g. `device/00000001/command/#` is a better choice than `device/command/00000001/#`.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
