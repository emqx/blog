
Date: 2020/8/5

The Kuiper team would like to announce the release of Kuiper 0.9.0. 

Kuiper 0.9.0 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.9.0).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

The user scenarios of Kuiper including, real-time processing of production line data in the IIoT; Gateway of Connected Vehicle analyze the data from data-bus in real time; Real-time analysis of urban facility data in smart city scenarios. Kuiper processing at the edge can reduce system response latency, save network bandwidth and storage costs, and improve system security.

![arch.png](https://static.emqx.net/images/ee1e8ac493f59310cab642a6948f6af5.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

Kuiper 0.9.0 is a major version that includes the stream state management, KubeEdge device model adoption,  EdgeX array type support and TDengine database sink support.

### Features & fixes

- [State management function is supported](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/rules/state_and_fault_tolerance.md). This feature enables Kuiper to implement stream with state:
  - Fault tolerant processing is supported. If an unexpected interruption occurs during stream processing, it can be resumed after the rule is restarted;
  - Checkpointing is supported, which allows users to implement QoS settings during stream processing, including At-most-once(0), At-least-once(1) and Exactly-once(2);
  - By consuming data from the specified offset, users can extend the relevant interface to realize the data source that can  re-consume the data, so that it can be recovered offline or when there is an error in stream processing;
  - Configurable state persistent storage. The system stores the state in the file system by default, and also supports storing state data in a third-party system, such as Redis;
  - The user is supported to call the API provided by Kuiper to realize the storage of custom state data when extending the source, sink and function;
- Access support for [KubeEdge data model](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/sources/mqtt.md#kubeedgeversion) is provided, with a tool for automatically issuing configuration files through Kubernetes configmap. Users can use Kuiper to directly support the analysis of device data from KubeEdge;
- [TDengine plug-in](https://github.com/emqx/kuiper/blob/master/docs/en_US/plugins/sinks/taos.md) is added, which can support saving analysis results to TDengine time series database;
- All Chinese documents are translated and synchronized;
- The execution process of FVT in Github Action is optimized, and some unnecessary test processes are deleted;
- `filter` in the window with [support for filtering data](https://github.com/emqx/kuiper/blob/cfbdf6503e7e63e0680d038cb06aece0415f91a0/docs/en_US/sqls/windows.md#filter-window-inputs) can realize the data filtering and window grouping; this function is more important for counting windows: the result of filtering through the WHERE statement and then window grouping will be different;

### Thanks

- [@chensheng0](https://github.com/emqx/kuiper/commits?author=chensheng0) provides a fix for Kubernetes configmap, which can be integrated with [Baidu Baetyl](https://github.com/baetyl/baetyl) framework.
- [@GZJ](https://github.com/emqx/kuiper/commits?author=GZJ) provides a fix that cleans up the site when Kuiper exits.
- [@smart33690](https://github.com/smart33690) provided a fix for the [Influxdb sink sample plug-in](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/influxdb.md).

## Kuiper 2020 milestone

The Kuiper project will keep the good momentum of rapidly development in 2020, including improving more features, integrating with more projects in the open source community on the edge, and adding more continuous integration tests to improve software quality. The main contents are as follows,

- EdgeX Hanoi version integration (Q3): Kuiper will support the newly added array data type in EdgeX; and support the EdgeX UI to manage Kuiper's streams, rules, etc., it will be more convenient when using Kuiper
- KubeEdge integration (Q3/Q4): By extending the Device Model, Kuiper is used to implement functions such as cleaning, caching, and retransmission of bypass device data. 
- State management (Q3): Kuiper will provide built-in State support and support fault-tolerant recovery and other functions. Kuiper will use this feature to achieve the persistence support required for long-time window processing. In addition, it can also allow users to extend the plug-in process through the API invocation to realize the storage of custom state data.
- Kuiper 1.0.0（Q3/Q4）release: 1.0.0 version will be released at Q3 or Q4 of 2020.

You can click [Kuiper 2020 milestone](https://github.com/emqx/kuiper/projects/1) to get more detailed information, and the latest updates.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)

