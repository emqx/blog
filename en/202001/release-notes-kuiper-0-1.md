The Kuiper team would like to announce the release of Kuiper 0.1. 

Kuiper 0.1 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.1).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.
![Kuiper architect](https://static.emqx.net/images/dc6d85d8b19d05a990a12f41f46575fb.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

### Features

- Optimized performance
  - Provides configuration for setting concurrency for Kuiper rule, so it can be optimized in different scenarios
    + ``concurrency`` setting in [source](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/sources/mqtt.md): How many instances will be started. By default, only an instance will be run. If more than one instance is specified, the topic must be a shared subscription topic.
    + ``concurrency`` settings in [sink](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/overview.md#actions): Specify how many instances of the sink will be run. If the value is bigger than 1, the order of the messages may not be retained.
    + ``concurrency`` settings in [SQL plans](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/overview.md#options): A rule is processed by several phases of plans according to the SQL statement. This option will specify how many instances will be run for each plan. If the value is bigger than 1, the order of the messages may not be retained.
- Performance test result
    + Raspberry Pi 3B+: 12k messages/second; CPU utilization (sys+user): 70%; Memory: 20M
    + AWS t2.micro( 1 Core * 1 GB, Ubuntu18.04): 10k messages/second; CPU utilization (sys+user): 25%; Memory: 20M
- Support [metrics collection for rules](https://github.com/emqx/kuiper/blob/develop/docs/en_US/cli/rules.md#get-the-status-of-a-rule), which can be used for message processing status tracking.  The metrics includes, 
  - ``in, out, exception`` message count for all operators
  - ``process_latency_ms`` for all operators
  - ``buffer_length``, the used buffer length for all operators
  - ``last_invocation``, the last invocation timestamp for all operators
- Tested in OpenWrt Linux (Chaos Calmer 15.05) with 1core CPU * 256M memory, and it works fine.
- Support re-connect to MQTT broker if MQTT source or sink is disconnected.

### Bug fixes

- Print error message in ``cli`` command if any error is found during starting a rule.
- Fixed several issues in ``rest sink``.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)