## What is the topic

[MQTT protocol](https://www.emqx.io/mqtt) transmits application messages over the network. When application messages are transmitted over MQTT, they have an associated quality of service (QoS) and topic (Topic). The topic is essentially a string, and the MQTT protocol specifies that the topic is a UTF-8 encoded string, which means that the comparison of the topic filter and the topic name can be done by comparing the encoded UTF-8 bytes or decoded Unicode characters 

#### Topic name and topic filter

- **Topic name** 
  It is a label attached to the application message that is known to the server and matches the subscription. The server sends a copy of the application message to each matching client subscription.
- **Topic filter** 
  It is an expression contained in a subscription to represent one or more topics that are related. Topic filters can use wildcards.

If the topic filter of the subscription matches the topic name of the message, the application message will be sent to each matching client subscription. Topic resources can be predefined by the administrator on the server, or they can be added dynamically when the server receives the first subscription or application message using that topic name. The server can use a security component to selectively authorize the client to use a topic resource.

#### Rules for naming topics and topic filters

- All topic names and topic filters must contain at least one character.
- Topic names and topic filters are case sensitive. `ACCOUNTS` and ` Accounts` are different topic names.
- Topic names and topic filters can contain space characters. `Accounts payable` is a legal topic name.
- Topic  names or topic filters are distinguished by leading or trailing slashes `/`. `/finance` and ` finance` are different.
- Topic  names or topic filters containing only slashes `/` are legal.
- Topic names and topic filters cannot contain `null` characters (Unicode U + 0000).
- Topic names and topic filters are UTF-8 encoded strings. There are no other restrictions on the number of levels of topic  names or topic filters except that they cannot exceed the length limit of UTF-8 encoded strings.

## Topic level

#### Separator of topic level 

The slash ("/" U + 002F) is used to split each level of the topic, providing a hierarchy for the topic name. The separator is used to introduce structure into the topic name. If there is a separator, it divides the topic name into multiple topic levels, which is an important symbol in the design of message topic level. For example: `aaa/bbb`,` aaa/bbb/ccc`, and `aaa/bbb/ccc/ddd` message topic formats are a hierarchical relationship. They can be matched by multiple wildcards at the same time, or only one single wildcard for one of them. This can be applied in real scenarios, such as department level push of the company, national city level push and so on.

MQTT subscribed packet contain a topic filter and a maximum quality of service (QoS) level. Subscribed topic filters can contain special wildcards that allow clients to subscribe to multiple topics at once. Topic-level separators are useful when the topic filter specified by the client subscription contains two wildcard characters. Topic-level separators can appear anywhere in a topic filter or topic name. Adjacent topic level separators represent a zero-length topic level.

> Wildcard characters can be used in topic filters, but wildcard characters cannot be used in topic names. Single-level and multi-level wildcards can only be used for subscribing to messages and not for publishing messages. Topic level separators can be used in both cases.

#### Multi-level wildcard

The # symbol ("\ #" U + 0023) is a wildcard used to match any level in a topic. A multi-level wildcard represents its parent and any number of child levels.

For example, if a client subscribes to the topic `sport/tennis/player1/#`, it receives a message published with the following topic name:

- `sport/tennis/player1`
- `sport/tennis/player1/ranking`
- `sport/tennis/player1/score/wimbledon`

Because the multi-level wildcard includes its own parent, `sport/#` also matches a single `sport` topic name, and ` sport/tennis/player1/# ` also matches ` sport/tennis/player1`.

A separate multi-level wildcard `#` is valid, and it will receive all application messages.

Multi-level wildcards must be specified individually or following the topic level separator. Multi-level wildcard must be the last character of the topic filter. Therefore, both `sport/tennis#` and `sport/tennis/#/ranking` are invalid multilayer wildcards.

#### Single-level wildcard

“+” ("+" U + 002B) is a wildcard that can only be used for single topic level matching. For example, `sport/tennis/+`  matches `sport/tennis/player1` and `sport/tennis/player2`, but does not match `sport/tennis/player1/ranking`. At the same time, since single-level wildcards can only match one level, `sport/+` does not match `sport` but it does match ` sport/ `.

You can use single-level wildcards at any level of the topic filter, including the first and last level. You can use it in multiple levels in the topic filter, or you can use it with multiple levels of wildcards, `+`, `+/tennis/#` and `sport/+/player1` are both valid. When using a single-level wildcard, the single-level wildcard occupies the entire level of the filter and `sport+` is invalid.

#### Topics starting with \ $

The server cannot match the topic name starting with the character `$` with the topic filter starting with the wildcard character (# or  + ). The client subscribing to # will not receive any messages published to the topic starting with $, and the client subscribing to `+/monitor/Clients` will not receive any messages published to `$SYS/monitor/Clients`. The server should prevent the client from using this topic name to exchange messages with other clients. The client should not use the topic beginning with the '$' character.

Server implementations can use topic names that begin with `$` for other purposes. For example, `$SYS/` is widely used as a prefix for topics that contain server-specific information or control interfaces. Clients subscribing to `$SYS/`will receive messages published to topics starting with `$SYS/`. Clients subscribing to `$SYS/monitor/+` will receive messages published to topics of `$SYS/monitor/Clients` . If the client wants to accept messages with topics starting with ``$SYS/` and messages without topics starting with `$`, it needs to subscribe to both `#` and `$SYS/#`.

## Example

For example, if we use sensors to monitor the temperature, humidity, and air quality of bedrooms, living rooms, and kitchens at home, we can design several following topics:

- `myhome/bedroom/temperature`
- `myhome/bedroom/humidity`
- `myhome/bedroom/airquality`
- `myhome/livingroom/temperature`
- `myhome/livingroom/humidity`
- `myhome/livingroom/airquality`
- `myhome/kitchen/temperature`
- `myhome/kitchen/humidity`
- `myhome/kitchen/airquality`

When we want to get all the bedroom data, we can subscribe to the topic `myhome/bedroom/+`. When we want to get the temperature data of three rooms, we can subscribe the topic `myhom/+/temperature`. When we want to get all the data, we can subscribe to `myhome/#` or `#`.

