[EMQ X Enterprise](https://www.emqx.com/en/products/emqx) is an elastically scalable enterprise-level IoT MQTT messaging platform that supports one-stop access to millions of IoT devices, MQTT&CoAP multi-protocol processing, and low-latency real-time message communication. It provides a SQL-based built-in rule engine to flexibly process/forward messages to back-end services, store message data to various databases, or bridge message middleware such as Kafka, RabbitMQ. It can efficiently, reliably, and flexibly move data bi-directionally between various IoT devices and enterprise systems.

EMQ X Enterprise is applicable to various IoT application scenarios, supports arbitrary deployment of public clouds, private clouds, physical machines, containers/K8s, and can help enterprises quickly build IoT platforms and applications.


Introduction to EMQ X Enterprise: [https://www.emqx.com/en/products/emqx](https://www.emqx.com/en/products/emqx)

Download address: [https://www.emqx.com/en/try](https://www.emqx.com/en/try?product=enterprise)


![EMQ X Enterprise](https://static.emqx.net/images/4b87d5ae6dc17bb84f6414e4d8fc504c.png)


## Overview

EMQ X Enterprise v4.3.0 version inherits many performance and function improvements in the open source version 4.3.0. On this basis, Enterprise v4.3.0 adds support for dynamic expansion of Kafka partitions and a more flexible way of sending MQTT messages through Kafka.

Detailed update log: [https://www.emqx.com/en/changelogs/enterprise/v4.3.0](https://www.emqx.com/en/changelogs/enterprise/v4.3.0)


## Rule engine upgrade: flexible and unlimited data integration

[EMQ X rule engine](https://docs.emqx.io/en/enterprise/v4.3/rule/rule-engine.html) is a SQL-based core data processing and distribution component on the standard MQTT. It can easily filter and Process MQTT messages and device life cycle events and distribute mobile data to more than a dozen databases and messaging systems, including MySQL, InfluxDB, and Kafka. It can integrate enterprise systems with zero-coding and help enterprises quickly build IoT platforms and applications.

As a major function of EMQ X, the rule engine provides a clear and flexible 「configuration」business integration solution based on SQL, which simplifies the business development process, improves user ease of use and reduces the coupling between the business system and EMQ X.

![IoT Rule engine](https://static.emqx.net/images/40b090be34291c0d202613e2598ff767.png)

### Add the function of bridging message to Kafka partition to support dynamic expansion

Combined with Apache Kafka, EMQ X can integrate IoT devices with enterprise systems in a highly reliable and loosely coupled manner. It is also the most commonly used technical solution in the practice of our enterprise customers and even in the IoT industry.

Since the release of the function, the EMQ X + Kafka solution is robust and mature enough to meet the requirements of a large number of enterprise customers for the overall performance of IoT applications and the security and stability of data in key businesses. In the past version iteration, we continued to optimize the Kafka solution. Initially, we used a self-developed driver to improve production performance. Later, we introduced the Kafka production capacity into the rule engine to improve the flexibility of data integration. In the latest version 4.2, we added a caching mechanism for the Kafka driver to further ensure data reliability.

![Bridging MQTT message to Kafka](https://static.emqx.net/images/12d0fb25e06f518e620cf718b094b85c.png)

In Enterprise v4.3.0, we have added the capability of dynamic expansion of Kafka partitions.

The expansion of the Kafka cluster in the production environment is a relatively common requirement and operation. However, after Kafka adds a new node, it will not `rebalance` the data to the new node. After Kafka is expanded, the corresponding topic partition needs to be expanded. The data balance after the expansion is actually the partition redistribution of the topic.

In the current version, no additional operations are required. After the Kafka Topic used by the rule engine is expanded, EMQ X can automatically refresh the number of partitions. 

### All batch operations supported by the rule engine enable batch asynchronous by default

Starting from version 4.2.2, EMQ X rule engine provides asynchronous and batch writing modes for I/O operations such as writing to the database and Kafka. The asynchronous mode can separate device message communication from data processing and provide higher I/O performance and avoid I/O blocking the client's normal [Pub/Sub](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) process. Please see EMQ X Enterprise 4.2.2 release notes for details.

Previously, this function was disabled by default, and it is recommended that users enable it. In this version, we set the option to be enabled by default in order to bring a better experience to users.

### The rule engine supports ClickHouse offline messaging and proxy subscription

It supports the use of ClickHouse as Storage to use offline messaging and proxy subscription functions. Since Clickhouse is not suitable for frequent small data operations, it is not recommended to use Clickhouse for offline messaging and proxy subscription scenarios without strong project needs or necessary scenarios.

### Rules engine refactored InfluxDB to enhance performance

We have added HTTPS support for InfluxDB and support batch writing of InfluxDB.


## Kafka distribution improvement: easier to use Kafka message distribution

EMQ X's module -> Kafka consumer group function can use external Kafka as a [message queue](https://www.emqx.com/en/blog/mqtt5-feature-inflight-window-message-queue) to consume messages from a specified Kafka topic, convert them into MQTT messages and send them to specific MQTT topics. The data flow is shown in the following figure:

![Kafka distribution improvement](https://static.emqx.net/images/9fe7501172ea1e95ec7052c733c1c8ec.png)

### Kafka-MQTT 1:M Topic mapping message distribution

In the current version, we provide Kafka-distributed data selection function. This new function comes from the suggestion of an enterprise customer. Under normal circumstances, Kafka messages contain data of `value`, `topic`, `key`, and `offset`:

```json
{
    "value": "{\"foo\": \"bar\"}",
    "ts_type": "create",
    "ts": 1621419857749,
    "topic": "test",
    "offset": 2,
    "key": "",
    "headers": []
}
```

In the previous design, we only supported forwarding the `value` in the Kafka message to the specified MQTT Topic, and the user can no longer obtain other data. However, these data are also useful in some scenarios. For example, the user expects to use the only `key`  in the message as a part of distributed MQTT Topic.

When configuring the mapping relationship of `Kakfa Topic`-`MQTT Topic`, we provide the content configuration item of MQTT Payload. For a certain mapping, the user can choose to forward the complete Kafka message or the `value` content of the message.

### Combination of Kafka distribution and rule engine

Due to the big difference between Kafka and MQTT, Kafka Topic cannot establish a mapping relationship with MQTT Topic one by one in actual use: the number of Kafka Topic is always small, and the number of MQTT Topic may be large. Therefore, the rule engine function can be combined for data distribution:

- The IoT application puts the distributed instructions into the Kafka message, including the destination MQTT Topic, Payload, etc., such as `{ "topic": "foo", "payload": "bar" }`;
- Write instructions to a topic in Kafka, such as `foo`;
- EMQ X Kafka consumers establish a mapping relationship and map the message in the previous step to a certain MQTT topic such as `foo_mqtt`. In fact, the client will not subscribe to the Topic. This topic is only used in transit, and the purpose is to make the rules engine obtain messages from Kafka;
- Write a rule engine, get data from the transit topic `foo_mqtt`, analyze the topic and payload information in the distributed instruction, select the **message republish** action, extract syntax through variables such as `${topic} ${payload}` etc., and dynamically fill in the fields of **destination topic**, **message content template** to realize the dynamic analysis and distribution of Kafka-MQTT.



## Bug fixes

- Inconsistent editing data for rule engine action
- Dashboard module translation problem
- Rule engine SQL statement supports null function, and undefined is converted to null.
