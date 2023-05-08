本月 [eKuiper](https://ekuiper.org/zh) 团队投入到了 1.10 版本的开发中。eKuiper 1.10 将适配 EdgeX Foundry Minnesota 版本，预计在 5 月份与 EdgeX 一起发布。

本月完成的主要工作有：

- 包含 EdgeX 在内的多种 source/sink 连接器的优化或添加，从而支持更多系统的集成；
- 更新了 eKuiper 的依赖和基础设施，提升开发的效率；
- 持续增加 SQL 语法和函数，提升表达能力；
- 优化项目文档，添加了更多的示例和教程。

本月 eKuiper 发布的版本包括：

- [eKuiper 1.9.0](https://github.com/lf-edge/ekuiper/releases/tag/1.9.1)：最新的稳定版本，包含了 1.9.0 的所有功能和修复了一些 bug。
- [eKuiper 1.10.0-alpha.0](https://github.com/lf-edge/ekuiper/releases/tag/1.10.0-alpha.0)：包含了 1.10.0 版本的已完成的功能，供用户试用。

## 连接器更新

本月 source/sink 连接器的更新主要有：

- EdgeX source/sink 适配 EdgeX Foundry Minnesota 版本，目前已支持与 EdgeX 开发版的对接。下个月正式版本发布前，我们将进一步集成测试；
- Rest sink 与 EdgeX 安全模式下的 REST API 对接，当前在集成测试中；
- File sink 增强，支持多种文件格式和文件切分；
- 增加 Kafka sink，现在用户可以将数据发送到 Kafka 集群；
- SQL 连接优化，支持设置连接池大小，防止数据库连接过多时导致的性能问题。

### File sink 更新，提升批量传输效率

File sink 是 eKuiper 的一个重要的 sink 连接器，它可以将数据写入到文件系统中。文件系统属于操作系统的内核，无需任何的外部系统依赖，因此具有很高的适用性，几乎可以应用于任何的部署环境中，特别是资源受限的系统中。采用文件 sink，我们可以在安全性要求较高或没有网络的环境中，作为数据批量的持久化的方式，然后再通过其他手段将数据传输到其他的系统中，实现网闸穿透。另外，我们也可以在带宽较低的环境中，将数据先批量写入到文件后再压缩传输，从而实现更大的压缩率，减少带宽消耗。

1.10 版本中的 File sink 支持多种文件格式和文件切分，用户可以通过配置文件指定文件格式，目前支持 JSON、CSV 和 LINES (按行切分) 三种格式。此外，用户还可以指定文件切分的策略，避免单个文件过大，影响传输效率和管理效率。新版本的 File sink 的主要亮点有：

- 支持多种文件格式，且写入的文件可由 File source 读取，实现数据的循环传输。
- 支持多种切分策略：
  - 按时间切分，支持设置文件切分的间隔时间
  - 按消息数目切分
- 切分文件名自动添加时间戳，避免文件名重复，并可设置时间戳的添加位置
- 支持写入多文件，即动态文件名。根据消息内容，可以将消息写入到不同的文件中，实现数据的分流。
- 写入性能优化，支持批量写入，提升写入效率。多文件写入时，支持并发写入，共用定时器，提升写入效率。

下个月，我们还将添加文件 sink 压缩功能，支持将文件压缩后再传输，从而进一步提升传输效率。同时在 source 端添加解压功能，实现数据处理的闭环。

## SQL 语法和函数更新

本月 SQL 语法和函数的更新主要有：

- 提供外部状态访问函数，支持从外部系统例如 Redis 中获取 KV 形式存储的状态；
- 增加 delay 函数，支持延迟处理，防止外部系统限流时被拒绝服务；
- 支持数组下标使用表达式，例如 `array[a]`，实现动态下标访问；
- 增加 rule_id 函数，可获取当前规则 id，方便标注输出数据的来源规则。

### 外部状态访问，更细粒度的流批一体计算

作为有状态的流处理引擎，eKuiper 支持窗口，分析函数以及自定义的有状态函数来设置和访问状态。然而，这些状态都是在 eKuiper 内部维护的，用户无法从外部访问和设置。一部分用户在系统架构中已经包含了 Redis 等 KV 缓存系统，从而实现了状态在各个服务中的共享。 为了更好地支持这类用户 eKuiper 1.10 版本增加了外部状态访问函数，支持从外部系统例如 Redis 和 MySQL 中获取 KV 形式存储的状态。通过外部状态访问，我们可以实现更细粒度的流批一体计算，实现多服务的实时状态共享，例如：

1. 流数据中获取设备的传感器读数，从 Redis 中获取设备的实时状态（由第三方程序更新），例如设备的开关，报警状态等。
2. 流数据中获取设备的传感器读数，从 Redis 中获取设备的基础信息如型号，厂家等。

相比 Lookup Table 的方式，外部状态访问的优势在于：

- 粒度更细：可以实现单个状态的访问，而不是整个行的访问
- 适配已有缓存系统，无需额外的数据导入和管理

## 基础设施更新

作为 EdgeX 大版本的适配版本，我们也同步进行了基础依赖的升级，并借此机会对持续集成的基础设施进行了更新。

### 依赖更新，跟进最新的 Go 语言版本

除了 EdgeX 相关依赖之外，eKuiper 还进行了如下的依赖更新：

- Go 语言版本更新到 1.20
- SQLite 依赖切换到纯 go 实现的版本
- Redis 依赖 [GitHub - redis/go-redis: Redis Go client](http://github.com/redis/go-redis) 更新到 v9
- 移除默认的 ZeroMQ 依赖
- 更新其他依赖库

### 持续集成，提升开发效率

为了提升开发效率，我们对持续集成的基础设施进行了更新，主要包括：

- GitHub action 增加了 lint，检查代码风格
- GitHub action 增加了单元测试覆盖率检查
- GitHub action 增加了 go mod tidy，检查依赖的版本
- GitHub action 增加了 license 检查

## 文档更新

新功能完成后，我们也会同步更新文档，方便用户了解和使用新功能。本月文档更新主要有：

- 添加了 Example 栏目，以案例的形式介绍 eKuiper 的使用
- 更新了 eKuiper 控制 EdgeX 的文档，添加了 eKuiper 中使用 message bus 的方式发送指令的示例

### 案例文档

社区中经常有用户询问，实现某个场景如何编写 SQL，许多场景都是比较通用的。为此，我们计划整理一些常用案例和实现方法，添加到文档新增的 example 专栏中。本周，我们增加了第一个案例，介绍如何合并单流中多传感器的数据，详情请看 [合并单流多设备数据](https://ekuiper.org/docs/zh/latest/example/data_merge/merge_single_stream.html) 

工业网关例如 Neuron 和 EdgeX Foundry 经常会在一个数据流中混杂多种设备的数据。不少用户朋友提问过如何优雅地合并数据，相信这篇文章可以给大家一些启发。

后续我们还会添加更多的案例，欢迎大家提出更多的案例需求。

## Bugfixes

本月解决的 bug 都发布到了 1.9.1 版本中，详情请看 [Release eKuiper 1.9.1 · lf-edge/ekuiper](https://github.com/lf-edge/ekuiper/releases/tag/1.9.1) 

值得一提的 fixes 包括：

- 解决 HoppingWindow 等有数据重合窗口函数的数据重用问题
- 解决缺少预编译 InfluxV2 插件的问题
- MQTT sink 在规则启动时的偶尔的连接报错问题
- 支持 REST sink 网络异常时的缓存重发

## 下月计划

下个月我们将继续推进 eKuiper 1.10 的开发和发布，主要包括 EdgeX minnesota 的集成测试和文件 sink 压缩功能以及连接器运行时的优化。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
