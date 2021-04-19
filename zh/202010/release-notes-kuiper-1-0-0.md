
日期：2020/10/21

Kuiper 团队宣布发布 Kuiper 1.0.0

Kuiper 1.0.0 [可以从这里下载](https://github.com/emqx/kuiper/releases/tag/1.0.0)。

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/ef5274c57972e38fcb585127413eae03.png)

网址：https://www.emqx.cn/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 1.0.0 是第一个稳定的主版本。该版本与 EMQ 其它边缘软件进行了完整的集成，包括 [Neuron](https://www.emqx.cn/products/neuron)， [Edge](https://www.emqx.cn/products/edge) 和 边缘管理控制平台 (Edge Manager)。读者可以参考  [edge-stack 项目](https://github.com/emqx/edge-stack) 来获取 EMQ 边缘解决方案的信息。

### 功能及问题修复

- 不兼容的更新！如有任何程序或者脚本引用了 Kuiper 的二进制文件名 `bin/server` 和 `bin/cli`，需要将其进行重命名。
  - `bin/server` 重命名为 `bin/kuiperd`
  - `bin/cli` 重命名为 `bin/kuiper`
- EdgeX 增强与修复
  - EdgeX 消息总线使用 redisstreams 的时候报错
  - 更新 EdgeX docker-compose 文件，将 Kuiper 更新至 0.9.1 版本
  - Go 15 升级
  - 消息总线 SDK 升级
  - EdgeX Kuiper 文档和教程更新
  - 只读文件系统下容器化的 Kuiper 无法启动的问题
- 更新文档
  - Kuiper docker 镜像使用文档
  - 写并翻译了 Kuiper 管理控制台的使用文档
- 增强 TDengine 插件
  - 将插件名称 taos 改为 TDengine
  - [TDengine 存储数据的时候允许用户控制时间戳字段](https://github.com/emqx/kuiper/issues/520)
  - [TDengine  插件缺省值的设置](https://github.com/emqx/kuiper/issues/527) 
- 运行在插件安装的脚本中传递参数，这可以让插件的安装过程更灵活
- Rest 服务返回多语言支持
- 修复了以下的问题
  - [日志文件中的行号不正确](https://github.com/emqx/kuiper/issues/518)

### 感谢

- [@TateDeng](https://github.com/TateDeng) 提供了 DynamicChannelBuffer 设置的修复

## Kuiper 2020 里程碑

2020 年 Kuiper 项目将持续快速发展，包括完善更多的功能、与边缘开源社区更多项目的集成，以及加入更多的持续集成测试，提高软件质量等。主要内容如下，

- State 管理（Q3）：Kuiper 将提供内置 State 支持，并支持容错恢复等功能，Kuiper 通过此功能将实现长时间窗口处理所需的持久化支持，另外也可以让用户在扩展插件过程中，通过 API 调用实现对自定义状态数据的存储
- KubeEdge 集成（Q3/Q4）：通过扩展 Device Model，使用 Kuiper 实现对于旁路（bypass）设备数据进行清洗、缓存和重传等功能
- Kuiper 1.0.0（Q3/Q4）发布：1.0.0 版本将于 2020 年 Q3 或者 Q4 发布
- EdgeX Hanoi 版本集成（Q4）：Kuiper 将支持 EdgeX 中新加入的数组数据类型；以及支持通过 EdgeX UI 来管理 Kuiper 的流、规则等，用户在使用 Kuiper 的时候更加方便 

您可以点击 [Kuiper 2020 里程碑](https://github.com/emqx/kuiper/projects/1)获取更加详细的信息，以及最新的更新。

## 联系

如果对 Kuiper 有任何问题，请随时通过 kuiper@emqx.io 与我们联系。