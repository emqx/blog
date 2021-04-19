

日期：2020/6/1

Kuiper 团队宣布发布 Kuiper 0.4.1

Kuiper 0.4.1 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.4.1)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://static.emqx.net/images/60dc5411db7c365da28ec255dcd67b98.png)

网址：https://www.emqx.cn/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 0.4.1 版本主要修复了一些从社区中反馈的问题。

### 功能

- 支持插件多实例的功能。之前的版本中，插件只支持单个实例，现在用户可以通过返回一个构造函数来支持插件多实例功能。
- 修复[规则文档中](https://github.com/emqx/kuiper/blob/master/docs/en_US/rules/overview.md)关于 `dataTemplate` 使用方法的说明
- 修复[ EdgeX 浮点数据](https://github.com/emqx/kuiper/issues/272)在某些情况下不能处理的问题
- 支持通过 Docker 环境变量来修改 EdgeX MQTT 消息总线的配置
- 支持将汇聚函数的运算结果作为别名，然后在 WHERE 或者 HAVING 表达式中使用别名进行引用，这样可以避免多次运算，提高了运行效率
- 删除不存在的流、规则时返回 404，而非之前的 400
- 修复了删除规则后，[未成功发送的数据被无限重发的问题](https://github.com/emqx/kuiper/issues/266)
- 支持在 `SELECT * `的时候，可以根据流中字段定义，实际发送的数据中字段的大小写进行正确处理
- 修复同一类型的 sink，无法准确发送消息的问题
- [http_pull 源](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/rules/sources/http_pull.md)支持，可以定时从 HTTP rest 接口中拉取数据

### 感谢

@worldmaomao 提供了[浮点](https://github.com/emqx/kuiper/issues/272)运算的修复

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。