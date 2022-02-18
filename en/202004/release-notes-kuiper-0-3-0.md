Date: 2020/4/7

The Kuiper team would like to announce the release of Kuiper 0.3.0. 

Kuiper 0.3.0 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.3.0).

EMQX Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/e4060fb08581f4c76fd97f4a6421e6be.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

[The Kuiper & EdgeX integration work](https://github.com/emqx/kuiper/projects/4) is almost completed, Kuiper will be integrated with EdgeX nightly Docker composer files soon. Kuiper 0.3.1will be released with EdgeX officially.

### Features

- EdgeX integration

  - Fixed some issues based on user's feedback, and updated the [tutorial doc](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md) . 
  - New implementation [EdgeX sink support](https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/sinks/edgex.md) based on the feedback from community, the analysis result can be published with the required format of EdgeX Message bus.
  - Translated EdgeX document to [Chinese](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/edgex/edgex_rule_engine_tutorial.md).
- Plugin management
- Kuiper now supports plugin management, but it was not provided in old versions. In this version, Kuiper provides REST API & command line tools. User can add, delete and view plugins through management tools. 

### Bug fixes

- [null handling in pre-processor](https://github.com/emqx/kuiper/issues/185)
- Rest sink [exceptions](https://github.com/emqx/kuiper/issues/173)
- Fixes some document issues.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
