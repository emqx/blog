日期：2020/3/23

Kuiper 团队宣布发布 Kuiper 0.2.1

Kuiper 0.2.1 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.2.1)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://static.emqx.net/images/f6ef7154f6adcaa53277161827b5165b.png)

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

本版本中 [Kuiper & EdgeX 集成](https://github.com/emqx/kuiper/projects/4)已经初步完成，用户可以开始试用该功能，在后续发布的 0.3.0 或者 0.4.0 将正式与 EdgeX Geneva 版本一起发布。

### 功能

- 与 EdgeX 的集成

  - EdgeX 源支持，从 EdgeX Message Bus 中接入数据。用户可以参考[教程文档 - 英文](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md)来了解如何使用 Kuiper 对 EdgeX 的数据进行分析。
  - [EdgeX 目标（sink）支持]( https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/sinks/edgex.md)，可以将结果直接写入 EdgeX Message Bus。

- Schemaless 流定义的支持

  在 Kuiper 之前的版本中，用户必须创建有 schema 的流定义，但是有些使用场景中，发送的数据格式比较复杂，如果对其进行流的定义会比较麻烦。Kuiper 现在可以支持用户创建一个不包含任何 Field 定义的流，这种 Schemaless 的使用方式下，无法实现对数据类型的验证，需要用户在写规则的时候，对发送的数据结构比较清楚，否则在数据分析过程中会报错。

- FVT 测试用例增强

  - 增加 4 个 EdgeX 的测试用例
  - 增加对 Docker image 的测试用例

### 问题修复

- 修复了几个 Github Action 中流水线的问题

### 联系

使用 Kuiper 过程中如有任何问题，可在 Github 提交 Issue 或通过 [contact@emqx.io](mailto:contact@emqx.io) 与我们联系。
