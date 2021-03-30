

日期：2020/8/4

Kuiper 团队宣布发布 Kuiper 0.9.0

Kuiper 0.9.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.9.0)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/bcd3fbfb96709c8dd747b0bd6bcaec79.png)

网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 0.9.0 版本是一个重大的版本，包含了对流状态，KubeEdge 设备模型接入、 EdgeX 数组类型支持和 TDengine 数据库存储等大功能的支持。

### 功能及问题修复

- [状态管理功能支持](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/rules/state_and_fault_tolerance.md)。该功能让 Kuiper 实现了有状态的流：
  - 支持容错处理，在流处理过程中如果出现意外中断的时候，流处理在规则重启后可以恢复；
  - 支持检查点的实现 (Checkpointing)，该功能可以让用户在流处理过程中实现 QoS 的设置，包括 At-most-once(0)， At-least-once(1) 和 Exactly-once(2)；
  - 从指定的数据偏移处 (offset) 消费数据，用户可以扩展相关的接口来实现可重新消费数据的数据源，从而实现离线、或者在流处理出现错误的时候可以重新恢复；
  - 可配置的状态持久化存储。系统缺省将状态存储在文件系统中，也支持将状态数据存储在第三方的数据库中，比如 Redis 等；
  - 支持用户在扩展源、目标和函数的时候，调用 Kuiper 提供的接口实现自定义的状态数据的存储；
- 提供了 [KubeEdge 数据模型](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/sources/mqtt.md#kubeedgeversion)的接入支持，以及一个自动执行通过 Kubernetes configmap 下发配置文件的工具。用户可以使用 Kuiper 可以直接支持分析来自于 KubeEdge 的设备数据进行分析；
- 增加了 [TDengine 插件](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/taos.md)，可以支持将分析结果保存到 TDengine 时序数据库中；
- 翻译和同步了所有的中文文档；
- 优化了 Github Action 中 FVT 的执行流程，删除了一些不必要的测试过程；
- 增加了 RPM & APT 安装包的支持；
- 窗口中 `filter ` [过滤数据的支持](https://github.com/emqx/kuiper/blob/cfbdf6503e7e63e0680d038cb06aece0415f91a0/docs/en_US/sqls/windows.md#filter-window-inputs)，实现对数据先进行过滤，然后进行窗口分组；这个功能对于计数窗口比较重要：与通过 WHERE 语句过滤，然后再进行窗口分组的结果会不一样；

### 感谢

- [@chensheng0](https://github.com/emqx/kuiper/commits?author=chensheng0) 提供了 Kubernetes configmap 的修复，可以与百度 Baetyl 框架进行集成
- [@GZJ](https://github.com/emqx/kuiper/commits?author=GZJ) 提供了 Kuiper 退出时能清理现场的修复
- [@smart33690](https://github.com/smart33690) 提供 [Influxdb sink 样例插件](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/influxdb.md)的修复

## Kuiper 2020 里程碑

2020 年 Kuiper 项目将持续快速发展，包括完善更多的功能、与边缘开源社区更多项目的集成，以及加入更多的持续集成测试，提高软件质量等。主要内容如下，

- EdgeX Hanoi 版本集成（Q3）：Kuiper 将支持 EdgeX 中新加入的数组数据类型；以及支持通过 EdgeX UI 来管理 Kuiper 的流、规则等，用户在使用 Kuiper 的时候更加方便
- KubeEdge 集成（Q3/Q4）：通过扩展 Device Model，使用 Kuiper 实现对于旁路（bypass）设备数据进行清洗、缓存和重传等功能
- State 管理（Q3）：Kuiper 将提供内置 State 支持，并支持容错恢复等功能，Kuiper 通过此功能将实现长时间窗口处理所需的持久化支持，另外也可以让用户在扩展插件过程中，通过 API 调用实现对自定义状态数据的存储
- Kuiper 1.0.0（Q3/Q4）发布：1.0.0 版本将于 2020 年 Q3 或者 Q4 发布

您可以点击 [Kuiper 2020 里程碑](https://github.com/emqx/kuiper/projects/1)获取更加详细的信息，以及最新的更新。

## 联系

如果对 Kuiper 有任何问题，请随时通过 contact@emqx.io 与我们联系。