> This release announcement also includes content of 0.3.2 & 0.3.1.

Date: 2020/5/7

The Kuiper team would like to announce the release of Kuiper 0.4.0, [dowload Kuiper](https://github.com/lf-edge/ekuiper).

EMQX Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/9640c89a1e3fb8caf7235517aa3f0425.png)

This release includes several new features and bug fixes.

For more details: [EMQ Website](https://github.com/lf-edge/ekuiper) , [Kuiper GitHub](https://github.com/emqx/kuiper).

### Overview

- Kuiper 0.4.0 now has the capability of supporting more complex plugin; Support template feature for all sinks, so users can customize complex output data.
- Kuiper 0.3.2 is the release that ship with EdgeX Foundry Geneva.
- Kuiper 0.3.1 supports message bus based on MQTT.

### Features

- 0.4.0

  - Supported [template feature](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/rules/overview.md#data-template) for all of sinks, now user can leverage template to customize complex output data in all sinks.

  - When user invoke API for creating a plugin, user can provide a install.sh script in zip file, so that the complex library dependencies installation can be supported.
  - Added FVT scenario for plugin.
  - Updated document structure.
  - Added Docker image based on  Debian, user can select this image if want to have more library dependencies.
  - Add Kuiper [plugin development tutorial](https://github.com/emqx/kuiper/blob/develop/docs/en_US/plugins/plugins_tutorial.md).
- EdgeX integration
  - 0.3.2
    - Kuiper 0.3.2 is the candidate release that ship with EdgeX Foundry Geneva. User can follow [this tutorial](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md) for starting use Kuiper rule engine in EdgeX Foundry Geneva release.
    - Add float decoding support in EdgeX source 
  - 0.3.1
    - EdgeX MQTT message bus support. Kuiper [source](https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/sources/edgex.md) & [sink](https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/sinks/edgex.md) now can support message bus over MQTT broker .
    - Benchmark result for EdgeX: EdgeX Kuiper rule engine supports 11.4k message throughput per second in AWS t2.micro( 1 Core * 1 GB). Refer to [this doc](https://github.com/emqx/kuiper/tree/master#edgex-throughput-test) for detailed info.
    - Expose Kuiper Rest API port in Docker environment variable.
- 0.3.2
  - Return rule status when getting list of rules.
  - Unify all of Golang compile version to 1.13.
- 0.3.1

  - Add a Kuiper [plugin development tutorial (Chinese)](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/plugins/plugins_tutorial.md).

### Bug fixes

- Fixes some output text and document issues.

### Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
