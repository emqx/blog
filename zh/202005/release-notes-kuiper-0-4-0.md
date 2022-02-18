> 该版本声明也包括了 0.3.1 与 0.3.2 版本的内容

日期：2020/5/7

Kuiper 团队宣布发布 Kuiper 0.4.0，[下载 Kuiper](https://github.com/lf-edge/ekuiper)。

EMQX Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://static.emqx.net/images/930d8c9a80229f6f88b7b6c4648a32d7.png)

更多信息请访问 [EMQ 官网](https://github.com/lf-edge/ekuiper) 或 [Kuiper GitHub](https://github.com/emqx/kuiper)。

### 概览

- Kuiper 0.4.0 对比较复杂的插件支持的能力上得到了增强；支持了对所有 sink 的模版支持功能，实现对复杂数据输出的定制能力
- Kuiper 0.3.2 作为 EdgeX Foundry Geneva 集成的版本已经发布
- Kuiper 0.3.1 实现了基于 MQTT 消息总线的支持

### 功能

- 0.4.0

  - 增加了对所有 sink 的[模版功能](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/overview.md#data-template)，用户可以通过模版实现对 sink 中复杂数据输出的定制能力
  - 用户在调用创建插件 API 的时候，用户可以在插件的 zip 文件中加入 install.sh 脚本，实现复杂的依赖库文件安装的能力
  - 增加插件的系统测试脚本
  - 更新了文档的组织结构
  - 增加了基于 Debian 的 Docker 镜像，对于需要更多依赖库的用户可以选择该镜像
  - 增加 Kuiper [插件开发教程 (英文)](https://github.com/emqx/kuiper/blob/develop/docs/en_US/plugins/plugins_tutorial.md)

- 与 EdgeX 的集成

  - 0.3.2
    - Kuiper 0.3.2 为 EdgeX Foundry Geneva 版集成的候选版本，用户可以参考[该教程](https://github.com/emqx/kuiper/blob/master/docs/en_US/edgex/edgex_rule_engine_tutorial.md)来开始使用 EdgeX Foundry Geneva 中的规则引擎.
    - 增加浮点数据处理

  - 0.3.1
    - EdgeX MQTT 消息总线支持。Kuiper [源](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/rules/sources/edgex.md) & [目标](https://github.com/emqx/kuiper/blob/master/docs/zh_CN/rules/sinks/edgex.md) 现可以支持基于 [MQTT 服务器](https://www.emqx.io/zh)的消息总线。
    - EdgeX 源基准性能测试：在  AWS t2.micro ( 1 Core * 1 GB) 配置的运行环境上，EdgeX Kuiper 规则引擎支持 11.4k/秒的消息吞吐量。参考[该文档](https://github.com/emqx/kuiper/tree/master#edgex-throughput-test) 获取更详尽的信息。
    - 在 Docker 环境变量中暴露 Kuiper Rest API 端口。

- 0.3.2 

  - 获取规则列表的时候，返回规则的状态。
  - 编译环境统一为 Golang 1.13

- 0.3.1

  - 增加 Kuiper [插件开发教程 (中文)](https://github.com/emqx/kuiper/blob/develop/docs/zh_CN/plugins/plugins_tutorial.md)。


### 问题修复

- 其它一些控制台输出和文档问题的修复

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
