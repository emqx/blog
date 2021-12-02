Kuiper 团队宣布发布 Kuiper 0.1。Kuiper 0.1 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/0.1)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。
![Kuiper architect](https://static.emqx.net/images/a06aaed50608fd57d53a400f1621cee6.png)

网址：[https://github.com/lf-edge/ekuiper](https://github.com/lf-edge/ekuiper)

Github仓库： [https://github.com/emqx/kuiper](https://github.com/emqx/kuiper)

## 概览

### 功能

- 性能优化
  - 提供了针对 Kuiper 规则设置并发度的配置选项，在不同的场景下可以对其优化
    - 在 [source](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/sources/mqtt.md) 里的``concurrency`` 设置：设置运行的协程数，默认值为1。如果设置协程数大于1，必须使用共享订阅模式。
    - 在 [sink](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/overview.md#actions) 里的``concurrency`` 设置：设置运行的线程数。该参数值大于1时，消息发出的顺序可能无法保证。
    - 在 [SQL 计划](https://github.com/emqx/kuiper/blob/develop/docs/en_US/rules/overview.md#options)中的``concurrency``设置：一条规则运行时会根据 SQL 语句分解成多个计划运行。该参数设置每个计划运行的线程数。该参数值大于1时，消息处理顺序可能无法保证。
  - 性能测试结果
    - 树莓派 3B+：12k 消息/秒; CPU 利用率 (sys+user): 70%; 内存: 20M
    - AWS t2.micro ( 1核 * 1 GB, Ubuntu18.04)：10k 消息/秒; CPU 利用率 (sys+user): 25%; 内存: 20M
- 支持 [规则指标采集](https://github.com/emqx/kuiper/blob/develop/docs/en_US/cli/rules.md#get-the-status-of-a-rule)，可以被用于消息处理状态的跟踪。指标包含有，
  - ``in, out, exception`` 每个处理器的进、出与异常消息数
  - ``process_latency_ms`` 每个处理器的处理时延
  - ``buffer_length``, 每个处理器中用掉的 buff 的长度
  - ``last_invocation``, 每个处理器中最后调用时间
- 在 OpenWrt Linux (Chaos Calmer 15.05) 系统 (1核，256M 内存硬件)中完成测试，工作正常
- 如果 MQTT 源或者目标被断开，支持自动重连

### 问题修复

- 如果在启动规则的时候发现错误，在命令行中打印出相关的错误信息
- 修复了几个 REST Sink 的问题

### 联系

如果对Kuiper有任何问题，请随时通过contact@emqx.io与我们联系。
