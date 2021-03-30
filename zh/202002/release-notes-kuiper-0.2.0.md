

日期：2020/2/28

Kuiper 团队宣布发布 Kuiper 0.2.0

Kuiper 0.2.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.2.0)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://static.emqx.net/images/700907497d2735a42224591fb71a8d46.png)

网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

[Kuiper 2020 路线图](https://github.com/emqx/kuiper/projects) 更新到了 Github，并且创建了几个别的项目，例如 [Kuiper & EdgeX 集成项目](https://github.com/emqx/kuiper/projects/4)。用户如有兴趣，请点击相应链接进行查看。

### 功能

- [Rest 管理 API](https://github.com/emqx/kuiper/blob/master/docs/en_US/restapi/overview.md) 现已支持。除了 CLI 工具，用户可以通过 Rest API 来管理流和规则。
  - 流管理
  - 规则管理
- 支持的最大规则数目基准测试
  - 8000 条规则，800 消息/秒吞吐量，AWS 2 核 * 4GB 内存
  - 资源使用
    - 内存: 89% ~ 72%
    - CPU: 25%
- 在[Github action](https://github.com/emqx/kuiper/actions)上建立了 FVT 测试运行流水线，FVT 测试将在代码提交或者接受 PR 的时候自动运行，保证产品质量
- 完成了 8 个 Kuiper [FVT](https://github.com/emqx/kuiper/tree/master/fvt_scripts) (functional verification tests) 测试用例，覆盖了以下场景
  - HTTP REST-API 的所有基本功能
  - 命令行工具 CLI 的基本功能
  - 复杂的端到端测试，覆盖 Kuiper 源、处理和目标等

### 问题修复

- 修复 [the sink result is not correct](https://github.com/emqx/kuiper/issues/101) 问题
- 修复了几个在运行多个规则时期发现的问题

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
