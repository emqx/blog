Date: 2020/6/1

The Kuiper team would like to announce the release of Kuiper 0.4.1. 

Kuiper 0.4.1 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.4.1).

EMQX Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

![arch.png](https://static.emqx.net/images/9f804aa223924cf4460028c6f6cd3957.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

Kuiper 0.4.1 version fixed some problems reported from community.

### Features

- Support multi-instances creation for plugins. In previous versions, plugin only supports one single instance, now multiple plugin instances can  be supported by returning a construction function.
- Fixed  `dataTemplate`  usage in [rule document](https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/overview.md).
- Fixed [EdgeX floating data](https://github.com/emqx/kuiper/issues/272) can not be processed problem in some cases.
- Support for updating EdgeX MQTT message bus configurations by Docker environment variables.
- Support for using alias for aggregation functions, and then use alias name in WHERE or HAVING clause, it can greatly improve the performance.
- Returns 404 response code when deleting not existed streams or rules, while previously returns 400.
- Fix [sink infinite resend after rule stopped problem](https://github.com/emqx/kuiper/issues/266). 
- When using `SELECT * `,  now it can correctly process the field name case by reading stream schema definition or actual field name sent in streams.
- Fixed problem of multiple same type of sink cannot work correctly.
- [http_pull source](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/rules/sources/http_pull.md) support, it can pull data from HTTP rest interface by specified interval time.

### Thanks

@worldmaomao provided [EdgeX floating](https://github.com/emqx/kuiper/issues/272) processing fixes.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
