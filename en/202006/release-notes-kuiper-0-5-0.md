Date: 2020/6/22

The Kuiper team would like to announce the release of Kuiper 0.5.0. 

Kuiper 0.5.0 now is [available for download](https://github.com/lf-edge/ekuiper/releases/tag/0.5.0).

EMQX Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

The user scenarios of Kuiper including, real-time processing of production line data in the [IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges); Gateway of Connected Vehicle analyze the data from data-bus in real time; Real-time analysis of urban facility data in smart city scenarios. Kuiper processing at the edge can reduce system response latency, save network bandwidth and storage costs, and improve system security.

![Kuiper architect](https://assets.emqx.com/images/f92e28acfbf4acdb12ace78f66371cad.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

Kuiper 0.5.0 adds some significant features and also fix problems requested from community.

### Features & fixes

- Support for [using Kuiper keywords](https://github.com/lf-edge/ekuiper/issues/237) in SQL statements.
- Support for [count window](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/sqls/windows.md#count-window), which allows user do count based window analysis.
- [More JSON functions](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/json_expr.md#json-path-functions) are supported, including `json_path_exists, json_path_query, json_path_query_first`.
- Updated Github action and add `go fmt` in continuously integration pipeline.
- Added [contributing guide](https://github.com/lf-edge/ekuiper/blob/master/docs/CONTRIBUTING.md).
- Add [Influxdb sink sample plugin](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/plugins/sinks/influxdb.md).
- A document for [reserved keywords](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/sqls/lexical_elements.md) in Kuiper.
- Update [plugin development tutorial document](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/plugins/plugins_tutorial.md).
- Fixed [rule order issue](https://github.com/lf-edge/ekuiper/issues/303). 
- Fixed the problem with `column name with '.' will have an error log`.  
- Fixed [aggregation functions with nil value](https://github.com/lf-edge/ekuiper/issues/294).
- Fixed `aarch64` binary package issue. 

### Thanks

- [@worldmaomao](https://github.com/worldmaomao) provided [rule order issue](https://github.com/lf-edge/ekuiper/issues/303).

- smart33690 provided [Influxdb sink sample plugin](https://github.com/lf-edge/ekuiper/blob/master/docs/en_US/plugins/sinks/influxdb.md).

## Kuiper 2020 milestone

The Kuiper project will keep the good momentum of rapidly development in 2020, including improving more features, integrating with more projects in the open source community on the edge, and adding more continuous integration tests to improve software quality. The main contents are as follows,

- EdgeX Hanoi version integration (3Q): Kuiper will support the newly added array data type in EdgeX; and support the EdgeX UI to manage Kuiper's streams, rules, etc., it will be more convenient when using Kuiper
- KubeEdge integration (3Q/4Q): By extending the Device Model, Kuiper is used to implement functions such as cleaning, caching, and retransmission of bypass device data. 
- State management (3Q): Kuiper will provide built-in State support and support fault-tolerant recovery and other functions. Kuiper will use this feature to achieve the persistence support required for long-time window processing. In addition, it can also allow users to extend the plug-in process through the API invocation to realize the storage of custom state data.
- Kuiper 1.0.0（3Q/4Q）release: 1.0.0 version will be released at 3Q or 4Q of 2020.

You can click [Kuiper 2020 milestone](https://github.com/lf-edge/ekuiper/projects/1) to get more detailed information, and the latest updates.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
