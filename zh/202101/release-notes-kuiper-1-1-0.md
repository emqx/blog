

日期：2021/1/6

Kuiper 团队宣布发布 Kuiper 1.1.0

Kuiper 1.1.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/1.1.0)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/1cee7069a6f9e0cc96601f2e793c1a80.png)

网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 1.1.0 增加了图像处理插件，可以支持在规则中支持图像的处理；以及 SQL 执行计划的优化。该版本还修复了一些文档问题。

### 功能及问题修复

- 二进制数据支持
  - 在上个版本支持二进制数据的基础上，Kuiper 现 [支持 2 个图像处理函数](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/functions/functions.md). 
  - 增加了二进制处理的 FVT 测试用例
- SQL 执行计划优化
  - 增强了 JOIN 语句中 ON 条件的 PushDownPredicate，如果 INNER JOIN 中条件只跟一个源有关系，将被提前执行
  - 增加 ColumnPruning 规则，所有未被使用到的列或者元数据在预处理阶段将被删除，这样可以减少内存的使用
- kubernetes-tools 支持流和规则的更新操作
- MQTT 源中的共享订阅配置项删除，我们建议用户直接在 MQTT 源中指定「共享订阅」主题
- 文档问题
  - 修复了一些 404 问题
  - 一部分描述和翻译问题

## Kuiper 2021 里程碑

点击 [Kuiper 2021 里程碑](https://github.com/emqx/kuiper/projects/10)以获取更多详细信息和最新更新。

- Q1 - Q4: 1.1.x - 1.4.x
- 插件增强功能
  - 为开发人员提供更友好的插件开发和部署
  - 更好的插件安装体验
- 第三方语言库调用支持
- 更人性化的管理界面
- 规则管道支持
- 规则功能增强， 例如，支持预定规则。
- 更多的数学和函数支持

## 联系

如果对 Kuiper 有任何问题，请随时通过 kuiper@emqx.io 与我们联系。

