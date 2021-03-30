

Date: 2020/2/28

The Kuiper team would like to announce the release of Kuiper 0.2.0. 

Kuiper 0.2.0 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.2.0).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/b63c79f46bb2f31e391006193b69ec67.png)

This release includes several new features and bug fixes.

Website: <https://www.emqx.io/products/kuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

[Kuiper 2020 Roadmap](https://github.com/emqx/kuiper/projects) was updated to Github, and several other projects were also created, such as [Kuiper & EdgeX integration project](https://github.com/emqx/kuiper/projects/4). Please click related link if you're interested in it.

### Features

- [Rest mangement API](https://github.com/emqx/kuiper/blob/master/docs/en_US/restapi/overview.md) now is provided. Besides CLI tools, user can manage streams & rules by Rest API.
  - Streams management
  - Rules management
- Max support rule number benchmark
  - 8000 rules with 800 message/second with 2 core * 4GB memory in AWS
  - Resource usage
    - Memory: 89% ~ 72%
    - CPU: 25%
- Setup FVT pipeline in [Github action](https://github.com/emqx/kuiper/actions). FVT test scenarios will be run automatically with any code commit or PR, so the product quality can be ensured.
- 8 Kuiper [FVT](https://github.com/emqx/kuiper/tree/master/fvt_scripts) (functional verification tests) were wrote, and covered following scenarios.
  - Basic functions of HTTP REST-API
  - Basic functions of CLI
  - Complex end-2-end scenario for Kuiper source, processing and sink

### Bug fixes

- Fixed [the sink result is not correct](https://github.com/emqx/kuiper/issues/101) issue
- Fixed several problems for running multiple rules.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)

