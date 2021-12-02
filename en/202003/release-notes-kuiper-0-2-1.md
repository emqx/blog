Date: 2020/3/23

The Kuiper team would like to announce the release of Kuiper 0.2.1. 

Kuiper 0.2.1 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.2.1).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/af3b2914f224393bd0b8811c76ba0e16.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

[The initial version of Kuiper & EdgeX integration work](https://github.com/emqx/kuiper/projects/4) was just completed, users can start to try it. In the coming EdgeX Geneva release,  Kuiper 0.3.0 or 0.4.0 will be released with EdgeX officially.

### Features

- EdgeX integration

  - EdgeX source support, now Kuiper can consume data from EdgeX Message Bus directly. You can refer to [tutorial doc](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md) for learning how to use Kuiper to analyze data from EdgeX. 
  - [EdgeX sink support](https://github.com/emqx/kuiper/blob/edgex/docs/en_US/rules/sinks/edgex.md), the analysis result can be published to EdgeX Message Bus directly.

- Schemaless stream definition

  In previous Kuiper releases, user must create a stream with schema, but we found that in some user cases, the data schema could be very complex, and it will be difficult to create data schema for it. Now Kuiper supports to create a stream that does not have any fields, in this mode, Kuiper framework can't validate data types during data processing. So user need to very clear about the data types when writing rules, otherwise, it could probably have problems. [EgeX tutorial doc](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md) is a good example of using schemaless stream.

- FVT test schenarios enhancements

  - Added 4 EdgeX testcases 
  - Added testcases for Docker image 

### Bug fixes

- Fixed several problems of Github Actions

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
