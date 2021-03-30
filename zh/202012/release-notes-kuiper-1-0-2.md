 
日期：2020/12/18

Kuiper 团队宣布发布 Kuiper 1.0.2

Kuiper 1.0.2 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/1.0.2)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/dcda7751f0c11500427f5fde928e1af2.png)
网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 1.0.2 优化了 SQL 执行计划和运行时，并在某些场景下大大提高了性能。 Kuiper 在此版本中还支持二进制类型，并且可用于二进制流处理，例如图像。

### 功能及问题修复

- SQL计划优化
  - 优化了 SQL 计划，添加了对 `PushDownPredicate` 的支持，可以根据 WHERE 子句中指定的条件提前过滤一些记录，可以减少长时间窗口处理的内存使用量。
  - 在后续的版本中将引入更多优化。
- 二进制数据类型支持
  - 现在支持二进制数据类型，并且用户可以处理二进制流，例如处理图像。
  - [图像目标插件](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/plugins/sinks/image.md)用于将图像文件保存到本地磁盘。
- 将流和规则存储从文件更改为 SQLite。
- Ping API 支持，用于 Kuiper 服务活动检测。
- 修复了一个内存泄漏问题——删除规则后，某些内存没有释放。
- 禁止将客户端和 REST API 限制为本地主机。
- 当服务器 fileLog=false 时，文件日志记录错误消息。
- 添加了所有目标的重试计数。
- 为日志文件提供 Logrotate 支持——循环时间为 24 小时，最长期限为 3 天。
- 在编译阶段添加了一些 SQL 验证。
- 增强了文档编制。
  - 修复了几个文件问题。
  - 修复了 httppull 源的几个问题。
  - 修复了在 management-ui 中加载数组类型时出现的问题。

## Kuiper 2021 里程碑

点击 [Kuiper 2021 里程碑](https://github.com/emqx/kuiper/projects/10)以获取更多详细信息和最新更新。

- Q1 - Q4: 1.3.x - 1.6.x
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

