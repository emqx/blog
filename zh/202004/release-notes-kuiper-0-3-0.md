日期：2020/4/7

Kuiper 团队宣布发布 Kuiper 0.3.0

Kuiper 0.3.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.3.0)。

EMQX Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://assets.emqx.com/images/e32179ace42832e336f2804f38778b20.png)

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

本版本中 [Kuiper & EdgeX 集成](https://github.com/emqx/kuiper/projects/4)已经基本完成，近期将把 Kuiper 的 Docker 镜像包含在 EdgeX 的 nightly Docker composer 文件中。Kuiper 0.3.1 将正式与 EdgeX Geneva 版本一起发布。

### 功能

- 与 EdgeX 的集成

  - 根据用户的使用反馈，我们修复了一些 EdgeX source 的问题，并且更新了[教程文档](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/edgex/edgex_rule_engine_tutorial.md)。
  - 根据用户的使用反馈，[EdgeX 目标（sink）支持](https://github.com/emqx/kuiper/blob/edgex_chn_doc/docs/zh_CN/rules/sinks/edgex.md)重新实现，新版本的实现中，可以将分析结果以 EdgeX 消息总线要求的格式直接写入。
  - 提供了 EdgeX Kuiper 集成的相关[中文文档](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/edgex/edgex_rule_engine_tutorial.md)。

- 插件管理的支持

  Kuiper 支持扩展插件，但是之前未提供插件管理工具的支持。在本版本中，Kuiper 提供了插件管理的 Rest API 和命令行的支持。通过此管理接口，用户可以通过提供的这些接口来新增，删除和查看插件等操作。


### 问题修复

- [在 pre-processor 里对 null 值的处理](https://github.com/emqx/kuiper/issues/185)
- Rest sink 的[异常](https://github.com/emqx/kuiper/issues/173)
- 其它一些文档问题的修复

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
