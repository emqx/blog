11 月， [eKuiper](https://ekuiper.org/zh) 团队转入 1.8.0 版本的开发周期之中，目前已完成了一部分实用的新功能：添加了视频流 source，将边缘流式处理能力扩展到视频流领域，可以处理摄像头的视频流或者网络中的直播视频流；发布了通用的 tfLite 函数，用户只需上传训练好的 Tensor Flow Lite 模型，无需额外编写插件或代码即可在 eKuiper SQL 中调用模型进行流数据的 AI 推断，进一步简化了 AI/ML 处理的难度；针对边缘环境运维不便的特点进一步优化了规则自动化运维的能力，为规则添加了自动重启策略的配置，Portable 插件添加了热更新功能；继续完善了有状态分析函数的支持，增加 WHEN 子句进行按条件计算。

## 规则自动化运维

部署在边缘端的规则运维相对困难。而边缘端的部署数量通常较大，手工重启规则或重启 eKuiper 也会成为较为繁琐的工作。新的版本中，我们增强了规则的自治和自适应能力。

### 规则自动重启策略

规则因各种原因出现异常时可能会停止运行，其中有些错误是可恢复的。新的版本中，eKuiper 提供了可配置的规则自动重启功能，使得规则失败后可以自动重试从而从可恢复的错误中恢复运行。

用户可配置全局的规则重启策略，也可以针对每个规则配置单独的重启策略。规则重启配置的选项包括：

- 重试次数
- 重试间隔
- 重试间隔系数，即重试失败后重试时间增加的倍数
- 最大重试间隔
- 随机重试延迟，防止多个规则总是在同一个时间点重试，造成拥塞

通过配置重试，可以在出现偶发错误时自动恢复，减少人工运维的需要。

### Portable 插件热更新

相比原生插件，Portable 插件更加容易打包和部署，因此也有更多的更新需求。之前的版本中，Portable 插件更新后无法立即生效，需要手动重启使用插件的规则或者重启 eKuiper。新的版本中，插件更新后，使用插件的规则可无缝切换到新的插件实现中，减少运维工作。

## 增强分析能力

新的版本继续加强了有状态分析函数的能力，同时提供了通用的 AI 分析函数，提升了产品原生的分析能力。

### 通用 AI 函数

我们提供了 Tensor Flow Lite 函数插件，用于在流式计算中进行实时 AI 推理。这个函数为通用的 AI 函数，可用于处理大部分已预训练好的 Tensor Flow Lite 模型。使用中，用户只需上传或提前部署好需要使用到的模型，无需额外编码即可在规则中使用这些模型。

tfLite 函数接收两个参数，其中第一个参数为模型（扩展名须为 .tflite）的名称，第二个参数为模型的输入。在以下两个例子中，tfLite 函数分别调用 sin_model.tflite 模型和 `fizz_buzz_model`.tflite 模型针对数据流中的 data 字段进行实时 AI 计算。

```
SELECT tfLite(\"sin_model\", data) as result FROM demoModel
SELECT tfLite(\"fizz_buzz_model\", data) as result FROM demoModel
```

函数会在 eKuiper 层面针对输入数据格式进行验证。用户可以通过更多的 SQL 语句对模型的输入和输出做预处理或者后处理。

### 有条件分析函数

分析函数添加了 WHEN 条件判断子句，根据是否满足条件来确定当前事件是否为有效事件。 当为有效事件时，根据分析函数语意计算结果并更新状态。当为无效事件时，忽略事件值，复用保存的状态值。完整的分析函数语法为：

```
AnalyticFuncName(<arguments>...) OVER ([PARTITION BY <partition key>] [WHEN <Expression>])
```

增加了 WHEN 子句之后，分析函数可以实现更加复杂的有状态分析。例如，计算状态的持续时间：

```
SELECT lag(StatusDesc) as status, StartTime - lag(StartTime) OVER (WHEN had_changed(true, StatusCode)), EquipCode FROM demo WHERE had_changed(true, StatusCode)
```

其中，`lag(StartTime) OVER (WHEN had_changed(true, StatusCode))` 将返回上次状态变化时的时间。因此，使用当前时间减去该时间可实时计算出状态的持续时间。

## 连接生态

eKuiper 可以处理二进制图像数据，但是此前的测试中，图像都是经由 MQTT、HTTP 等偏向文本数据传输的协议来发送。新版本提供了视频流源，增加了一种新的二进制数据源。同时，我们也继续适配新版本的 EdgeX。

### 视频流源

视频源用于接入视频流，例如来自摄像头的视频或者直播视频流。视频流源定期采集视频流中的帧，作为二进制流接入 eKuiper 中进行处理。

通过视频源接入的数据，可以使用已有的 SQL 功能，例如 AI 推理函数功能等，转换成数据进行计算或输出为新的二进制图像等。

### EdgeX Levski 适配

eKuiper 1.7.1 及之后的版本适配了 EdgeX Levski 版本。同时，eKuiper EdgeX source 增加了 EdgeX 新增的 Nats 总线的支持。

## 产品新面貌

### 发布流程优化

本月我们优化了产品版本发布的流程。通过优化持续集成的基础设施，我们加快了版本发布的节奏，对于已完成的功能实现尽早交付，方便用户试用和反馈。

例如，本月已完成的 v1.8.0 功能已发布在 1.8.0-alpha.2 版本中，用户可通过 [Docker](https://registry.hub.docker.com/r/lfedge/ekuiper/tags) 或 [Github](https://github.com/lf-edge/ekuiper/releases/tag/1.8.0-alpha.2) 页面进行下载试用。

持续集成同样应用在 1.7.x 版本中，根据用户反馈，我们在本月发布了 3 个 fixpack，修复了一些问题，目前最新的版本为 v1.7.3.

### Logo 更新

eKuiper 的产品 Logo 于本月正式更新。新的 logo 更具动感，多段线条构成的向上不断流动的形象，与 eKuiper 作为运行在边缘端的轻量级物联网数据分析和流处理引擎的产品定位更加吻合。新 Logo 整体呈现出向上流动的动态，代表着 eKuiper 可将海量物联网数据从边缘实时移动到云端的能力，也彰显了无限变化和拥抱万物的概念，正如 eKuiper 所具备的**灵活敏捷的集成能力，可在各类边缘计算框架上快速集成搭建边缘侧的流式数据解决方案。**

![eKuiper New Logo](https://assets.emqx.com/images/d8b14f5674a0a2b9ba2fe227f3975d34.png)

## 即将到来

下个月我们将继续进行 1.8.0 版本的开发，主要包括更高性能的静态 Schema 支持以及 Flow Editor 的推进。敬请期待。
