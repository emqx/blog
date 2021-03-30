

日期：2021/03/03

Kuiper 团队宣布发布 Kuiper 1.1.2

Kuiper 1.1.2 Docker 镜像地址：https://hub.docker.com/r/emqx/kuiper/tags?page=1&ordering=last_updated

EMQ X Kuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。

Kuiper 的应用场景包括：运行在各类物联网的边缘使用场景中，比如工业物联网中对生产线数据进行实时处理；车联网中的车机对来自汽车总线数据的即时分析；智能城市场景中，对来自于各类城市设施数据的实时分析。通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

![arch.png](https://static.emqx.net/images/61f22139415d4ce161972a7de1c5b0f2.png)

网址：https://www.emqx.io/products/kuiper

Github仓库： https://github.com/emqx/kuiper

## 概览

Kuiper 1.1.2 添加了一个示例插件 *LabelImage*，用于演示与机器学习框架 TensorFlow Lite 的集成。 此外，我们对函数插件进行了增强，支持在一个插件中定义多个函数，并对函数进行分类管理，降低了创建函数的复杂度。 构建扩展插件时，现在必须添加构建参数 `--trimpath` 来提高兼容性。我们还支持更多内置函数，如geohash 相关函数和 cardinality 函数；支持更多表达式，如数组的负数索引；并支持更多规则属性，如 sendError。最后，我们修复了产品和文档的几个问题。

### 功能与修复

- 与 TensorFlowLite 集成
  - 示例插件 *LabelImage* 可利用提前训练的 TensorFlowLite 模型标记图像
  - [**使用 Kuiper 函数插件运行 TensorFlow Lite 模型**](https://github.com/emqx/kuiper/blob/master/docs/en_US/plugins/functions/tensorflow_lite_tutorial.md)的教程
- 插件增强
  - 在一个函数插件中支持多个函数
  - 支持在上下文 `ctx.GetRootPath()` 中获取 Kuiper 根路径
  - 将图像函数重构为一个插件
  - 添加 [GeoHash 插件](https://github.com/emqx/kuiper/blob/master/docs/en_US/plugins/functions/functions.md#geohash-plugin) 以支持多个 geo hash 函数
- 构建
  - 为 *kuiperd* 构建添加 `--trimpath` 构建选项。 从此版本开始，此属性是[构建扩展插件](https://github.com/emqx/kuiper/blob/master/docs/en_US/extension/overview.md#setup-the-plugin-developing-environment)所必需的
  - 以 *kuiper* 用户身份运行进程/容器，以避免安全风险
- 支持数组负数索引，例如 `array[:-1]`
- 添加内置函数  `cardinality(array)` 以获取数组的长度
- 添加规则属性 *sendError*  以指定是否将运行时错误发送到目标
- 修复
  - 修复了停止规则内存清理问题
  - 恢复 httpPull 数据源支持
  - 修复了关于 bytea 类型的描述流问题
  - 修复了第一次输入时出现的随机会话窗口错误
  - 删除数据中未使用的空文件夹
- 文档修复
  - 修复多个链接
  - 修复内置函数文档的索引错误

### 特别感谢

- @beaufrusetta (Intel) 提供了一个以 *kuiper* 用户身份运行进程/容器的修复程序
- @noahlaux 提供了一个文档修复程序


## 快速开始

使用 Docker 安装 kuiper 1.1.2  :

```shell
docker run -p 9081:9081 -d --name kuiper emqx/kuiper:1.1.2
```

下载安装包 : https://github.com/emqx/kuiper/releases/tag/1.1.2

## Kuiper 2021 里程碑

点击 [Kuiper 2021 里程碑](https://github.com/emqx/kuiper/projects/10)以获取更多详细信息和最新更新。

- Q1 - Q4: 1.1.x - 1.4.x
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

