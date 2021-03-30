

Date: 2019/12/13

The Kuiper team would like to announce the release of Kuiper 0.0.4

Kuiper 0.0.4 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.0.4).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/eaa7e57f56a2d6287f49f10298a6374e.png)

This release includes several new features and bug fixes.

Website: https://www.emqx.io/products/kuiper

Github Repository: https://github.com/emqx/kuiper

## Overview 

### Features

- Support [extension](https://github.com/emqx/kuiper/blob/master/docs/en_US/extension/overview.md).
  - Supported the extension at compilation and architect, now support the extension
  - Supported ZeroMQ source and sink
  - Supported HTTP REST sink
  - Refactored code to support aggregate functions
- Kuiper can be programmatically invoked by the 3rd party applications, so it can be easily integrated with the 3rd party frameworks (such as EdgeX Foundry rule engine)
- Optimized memory footprint (memory footprint is 10MB+ when startup)
- Build improvement
  - Provides the Docker images, and images can be pulled at https://hub.docker.com/r/emqx/kuiper
  - Provided Helm file, and Kuiper can be deployed with [K3s](https://github.com/emqx/kuiper/blob/master/deploy/chart/kuiper/README.md).

### Bug fixes

- [#16](https://github.com/emqx/kuiper/issues/16) Rule status issue 

### Contact

If having any problems for Kuiper, feel free to contact us through contact@emqx.io



