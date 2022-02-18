日期：2019/12/13

Kuiper团队将宣布发布Kuiper 0.0.4

Kuiper 0.0.4 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.0.4).

EMQX Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

![arch.png](https://static.emqx.net/images/95b75e626481746d4bcb58bf76820527.png)

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

### 功能

- 支持[扩展](https://github.com/emqx/kuiper/blob/master/docs/en_US/extension/overview.md)
  - 在编译、代码架构等完成重构，支持扩展
  - 支持 ZeroMQ 源 (source) 和目标 (sink)
  - 支持 HTTP REST 目标 (sink)
  - 重构代码以支持聚合函数
- Kuiper 可以支持被第三方应用以程序直接调用的方式启动，因此可以很方便地与第三方框架集成（如 EdgeX Foundry 的规则引擎等）
- 优化初始内存使用（启动约使用内存10MB+）
- 构建优化
  - 提供 Docker 镜像, 镜像可以在 https://hub.docker.com/r/emqx/kuiper 获取
  - 提供 Helm 文件,  Kuiper 可以很方便地部署到 [K3s](https://github.com/emqx/kuiper/blob/master/deploy/chart/kuiper/README.md).

### 问题修复

- [#16](https://github.com/emqx/kuiper/issues/16) Rule 状态问题 

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
