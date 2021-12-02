日期：2020/11/12

Kuiper 团队宣布发布 Kuiper 1.0.1

Kuiper 1.0.1 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/1.0.1)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/fc9223537026752c219a428aeced805b.png)

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 1.0.1 增强了 Kuiper 管理控制台的功能，并且修复了一些问题。

### 功能及问题修复

- Kuiper 管理控制台
  - 支持流和规则的更新
  - 规则状态的可视化
- 支持将日志写入 Linux syslog
- TDengine ARM64 目标插件支持
- 修改了 EdgeX 使用教程
- 修复的问题

  - [Kuiper 在 ARM64 环境下退出的问题](https://github.com/emqx/kuiper/issues/570).
  - 规则每个执行单元执行时延改成更小的时间单位
  - Kuiper 管理控制台
    - [目标的编辑器中无法显示数组类型的数据](https://github.com/emqx/kuiper/issues/597)
    - 复杂的流定义在界面中显示不正确

## Kuiper 2020 里程碑

2020 年 Kuiper 项目将持续快速发展，包括完善更多的功能、与边缘开源社区更多项目的集成，以及加入更多的持续集成测试，提高软件质量等。主要内容如下，

- KubeEdge 集成（Q3/Q4）：通过扩展 Device Model，使用 Kuiper 实现对于旁路（bypass）设备数据进行清洗、缓存和重传等功能
- Kuiper 1.0.0（Q3/Q4）发布：1.0.0 版本将于 2020 年 Q3 或者 Q4 发布
- EdgeX Hanoi 版本集成（Q4）：Kuiper 将支持 EdgeX 中新加入的数组数据类型；以及支持通过 EdgeX UI 来管理 Kuiper 的流、规则等，用户在使用 Kuiper 的时候更加方便 

您可以点击 [Kuiper 2020 里程碑](https://github.com/emqx/kuiper/projects/1)获取更加详细的信息，以及最新的更新。

## 联系

如果对 Kuiper 有任何问题，请随时通过 contact@emqx.io 与我们联系。
