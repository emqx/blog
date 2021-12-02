Date: 2020/9/22

The Kuiper team would like to announce the release of Kuiper 0.9.1. 

Kuiper 0.9.1 now is [available for download](https://github.com/emqx/kuiper/releases/tag/0.9.1).

EMQ X Kuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices. One goal of Kuiper is to migrate the cloud streaming software frameworks (such as [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) and [Apache Flink](https://flink.apache.org/)) to edge side. Kuiper references these cloud streaming frameworks, and also considered special requirement of edge analytics, and introduced **rule engine**, which is based on `Source`, `SQL (business logic)` and `Sink`, rule engine is used for developing streaming applications at edge side.

The user scenarios of Kuiper including, real-time processing of production line data in the IIoT; Gateway of Connected Vehicle analyze the data from data-bus in real time; Real-time analysis of urban facility data in smart city scenarios. Kuiper processing at the edge can reduce system response latency, save network bandwidth and storage costs, and improve system security.

![arch.png](https://static.emqx.net/images/eec72ada11792bbc3be3b5d0e8e86005.png)

This release includes several new features and bug fixes.

Website: <https://github.com/lf-edge/ekuiper>

Github Repository: <https://github.com/emqx/kuiper>

## Overview

Kuiper 0.9.1 provides a management console, which can be used for Kuiper node management, stream, rule and plugin visualize edit. It greatly improves the using experience.

### Features & fixes

- Visualize management: A separated new Docker image was released with this new version. The image is a web based management console, and it provides streams, rules and plugins management. Please refer to [doc] (https://github.com/emqx/kuiper/tree/master/docs/en_US/manager-ui/overview.md) fore more detailed information.

 ![stream.png](https://static.emqx.net/images/2cc9f228be272beff3785c38bafc04ab.png)

  Stream creation UI, user can select different stream sources in the list.

  ![sql.png](https://static.emqx.net/images/f615a97c77b3ec0deaf83934885f3133.png)

  SQL editor for rule, system prompts user when writing SQLs.

  ![mqtt_sink.png](https://static.emqx.net/images/cf94a8a9f76b8d5fb1f070ed91455355.png)

  MQTT sink configurations setting, user can input or select related properties in the UI.

- Binary plugins: From this version, all of the plugins that submit to Github main repository will be compiled and published automatically when a new version is released. User can install & use the plugins through management console. When developer create PR for plugin code, the [plugin metadata information](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/overview.md) can be provided, and then the related information will be displayed in the management console. It can greatly reduce the effort for using the plugins.

- User can control to cache the data that failed to publish in the sink by set `disableCache` of `kuiper.yaml`. 

- Kubernetes configuration file dispatch tool multiple CPU arch support.

- Add  Collect function support, which can be used for return all of data in the window.

- Add Deduplicate function support, which can deduplicate the data of window.

- Fixed below issues

  - [Edgex-ui cannot post cross-domain requests](https://github.com/emqx/kuiper/issues/405)
  - [Kuiper process exits in log debug mode]( https://github.com/emqx/kuiper/issues/438)
  - [Rule is created even with error reported during rule creation](https://github.com/emqx/kuiper/issues/426)
  - [Set sendSingle as true but no data template is specified, the process is quit](https://github.com/emqx/kuiper/issues/416)
  - [Use describe plugin command error](https://github.com/emqx/kuiper/issues/413)
  - Nested struct definition reports syntax error.

### Thanks

- [@soyoo](https://github.com/soyoo) provides several log print fixes

## Kuiper 2020 milestone

The Kuiper project will keep the good momentum of rapidly development in 2020, including improving more features, integrating with more projects in the open source community on the edge, and adding more continuous integration tests to improve software quality. The main contents are as follows,

- State management (Q3): Kuiper will provide built-in State support and support fault-tolerant recovery and other functions. Kuiper will use this feature to achieve the persistence support required for long-time window processing. In addition, it can also allow users to extend the plug-in process through the API invocation to realize the storage of custom state data.
- KubeEdge integration (Q3 or Q4): By extending the Device Model, Kuiper is used to implement functions such as cleaning, caching, and retransmission of bypass device data. 
- Kuiper 1.0.0（Q3 or Q4）release: 1.0.0 version will be released at Q3 or Q4 of 2020.
- EdgeX Hanoi version integration (Q4): Kuiper will support the newly added array data type in EdgeX; and support the EdgeX UI to manage Kuiper's streams, rules, etc., it will be more convenient when using Kuiper. 

You can click [Kuiper 2020 milestone](https://github.com/emqx/kuiper/projects/1) to get more detailed information, and the latest updates.

## Contact

If having any problems for Kuiper, feel free to contact us through [contact@emqx.io](mailto:contact@emqx.io)
