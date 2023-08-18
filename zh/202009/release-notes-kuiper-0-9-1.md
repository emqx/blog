日期：2020/9/22

Kuiper 团队宣布发布 Kuiper 0.9.1

Kuiper 0.9.1 [可以从这里下载](https://github.com/lf-edge/ekuiper/releases/tag/0.9.1)。

EMQX Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://assets.emqx.com/images/16badd462e9d81fc6d04a2f79667dc5d.png)

网址：https://github.com/lf-edge/ekuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 0.9.1 版本提供了一个管理控制台，用于管理 Kuiper 节点，以及流、规则和插件的可视化操作，这些功能将极大提升用户体验。

### 功能及问题修复

- 可视化管理：该版本随之发布了一个单独的容器镜像，该镜像是一个基于 web 的控制台，提供了对 Kuiper 的节点管理与控制，并且实现了流、规则和插件的可视化管理；详细请[参见文档](https://github.com/lf-edge/ekuiper/tree/master/docs/zh_CN/manager-ui/overview.md)。

  ![stream.png](https://assets.emqx.com/images/1ffbfbbbf9a6a4cb529913c3cca9ad16.png)

  上图为流创建可视化界面，用户可以在界面中选择各种消息源。

  ![sql.png](https://assets.emqx.com/images/b10eecf2402220be71e97d9a9c8722da.png)

  上图为规则 SQL 编辑界面，系统可以在用户写 SQL 的时候给出提示。

   ![mqtt_sink.png](https://assets.emqx.com/images/f5b41e850c709e21638758c22273fde1.png)

  上图为设置 MQTT sink 属性的界面，在界面上通过输入和选择相应的属性就可以实现设置

- 二进制插件：从本版本开始，所有提交到 Github 主项目的插件在版本发布的时候会自动编译，并且会发布到 EMQ 官方网址，用户可以直接进行安装和使用。开发者在提交插件代码的时候，可以提供[插件元数据文件](https://github.com/lf-edge/ekuiper/blob/master/docs/zh_CN/plugins/overview.md)的方式，在管理控制台中可以自动显示相关的信息，方便用户使用插件。

- Kubernetes 配置文件分发工具的多 CPU 架构部署支持

- 用户可以通过 `kuiper.yaml` 中的 `disableCache` 来控制是否将 sink 中转发出错的数据进行缓存

- 增加了 Collect 函数支持，用于返回窗口中的所有数据

- 增加了 Deduplicate 函数支持，用于支持窗口中数据的去重

- 修复了以下问题

  - [Edgex-ui 中不能跨域调用的问题](https://github.com/lf-edge/ekuiper/issues/405)
  - [Kuiper 在日志调试模式下进程退出的问题]( https://github.com/lf-edge/ekuiper/issues/438)
  - [规则创建报错，但是还是会被创建](https://github.com/lf-edge/ekuiper/issues/426)
  - [设置 sendSingle 为 true，但是不指定数据模版，Kuiper 进程退出](https://github.com/lf-edge/ekuiper/issues/416)
  - [使用 describe plugin 命令出错的问题](https://github.com/lf-edge/ekuiper/issues/413)
  - 嵌套结构体定义语法编译报错

### 感谢

- [@soyoo](https://github.com/soyoo) 提供了日志打印的几个修复

## Kuiper 2020 里程碑

2020 年 Kuiper 项目将持续快速发展，包括完善更多的功能、与边缘开源社区更多项目的集成，以及加入更多的持续集成测试，提高软件质量等。主要内容如下，

- State 管理（Q3）：Kuiper 将提供内置 State 支持，并支持容错恢复等功能，Kuiper 通过此功能将实现长时间窗口处理所需的持久化支持，另外也可以让用户在扩展插件过程中，通过 API 调用实现对自定义状态数据的存储
- KubeEdge 集成（Q3/Q4）：通过扩展 Device Model，使用 Kuiper 实现对于旁路（bypass）设备数据进行清洗、缓存和重传等功能
- Kuiper 1.0.0（Q3/Q4）发布：1.0.0 版本将于 2020 年 Q3 或者 Q4 发布
- EdgeX Hanoi 版本集成（Q4）：Kuiper 将支持 EdgeX 中新加入的数组数据类型；以及支持通过 EdgeX UI 来管理 Kuiper 的流、规则等，用户在使用 Kuiper 的时候更加方便 

您可以点击 [Kuiper 2020 里程碑](https://github.com/lf-edge/ekuiper/projects/1)获取更加详细的信息，以及最新的更新。

## 联系

如果对 Kuiper 有任何问题，请随时通过 contact@emqx.io 与我们联系
