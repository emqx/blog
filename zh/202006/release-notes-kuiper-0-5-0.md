

日期：2020/6/22

Kuiper 正式发布 Kuiper 0.5.0

Kuiper 0.5.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.5.0)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![Kuiper architect](https://static.emqx.net/images/4681b3bc6324b943acf3f2038dffb1fe.png)

网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 0.5.0 版本增加了一些重要的功能，并且修复了一些从社区中反馈的问题。

### 功能及问题修复

- 在 SQL 语句中支持[使用 Kuiper 关键字](https://github.com/emqx/kuiper/issues/237) 
- 支持 [count window](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/sqls/windows.md#count-window)，用户可以做基于计数的窗口分析
- [更多 JSON 函数](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/json_expr.md#json-path-functions)的支持，包括 `json_path_exists, json_path_query, json_path_query_first`
- 更新了 Github action，在持续集成流水线中加入了 `go fmt` 
- 增加 [贡献指南](https://github.com/emqx/kuiper/blob/master/docs/CONTRIBUTING.md)
- 增加了 [Influxdb sink 样例插件](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/influxdb.md)
- Kuiper 中的 [保留关键字](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/sqls/lexical_elements.md)文档
- 更新了 [插件开发教程文档](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/plugins_tutorial.md)
- 修复了 [规则排序问题](https://github.com/emqx/kuiper/issues/303)
- 修复了问题 `column name with '.' will have an error log`.  
- 修复了 [聚合函数中有 nil 数值的问题](https://github.com/emqx/kuiper/issues/294)
- 修复了 `aarch64` 二进制包的问题

### 感谢

- [@worldmaomao](https://github.com/worldmaomao) 修复了[规则排序问题](https://github.com/emqx/kuiper/issues/303).

- [@smart33690](https://github.com/smart33690) 提供了 [Influxdb sink 样例插件](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/influxdb.md).

## Kuiper 2020 里程碑

2020 年 Kuiper 项目将持续快速发展，包括完善更多的功能、与边缘开源社区更多项目的集成，以及加入更多的持续集成测试，提高软件质量等。主要内容如下，

- EdgeX Hanoi 版本集成（3Q）：Kuiper 将支持 EdgeX 中新加入的数组数据类型；以及支持通过 EdgeX UI 来管理 Kuiper 的流、规则等，用户在使用 Kuiper 的时候更加方便
- KubeEdge 集成（3Q/4Q）：通过扩展 Device Model，使用 Kuiper 实现对于旁路（bypass）设备数据进行清洗、缓存和重传等功能
- State 管理（3Q）：Kuiper 将提供内置 State 支持，并支持容错恢复等功能，Kuiper 通过此功能将实现长时间窗口处理所需的持久化支持，另外也可以让用户在扩展插件过程中，通过 API 调用实现对自定义状态数据的存储
- Kuiper 1.0.0（3Q/4Q）发布：1.0.0 版本将于 2020 年 3Q 或者 4Q 发布

您可以点击 [Kuiper 2020 里程碑](https://github.com/emqx/kuiper/projects/1)获取更加详细的信息，以及最新的更新。

## 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。