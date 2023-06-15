在当今快速发展的技术环境中，汽车行业正处于变革期。软件定义汽车（Software-Defined Vehicle, SDV）处于这场变革的前沿，为用户提供了无与伦比的互联、智能和数据洞察。SDV 会产生海量的数据，如何实时高效的处理这些数据成为当务之急。

本文将深入分析 SDV 数据的流处理技术，探讨其如何在软件定义汽车领域助力安全、性能和用户体验的创新。

## 什么是软件定义汽车？

软件定义汽车是一种高度互联、自动化和智能化的车辆。它们能够与其他车辆、基础设施、云服务和移动设备实现信息交互，并根据不同的环境和用户需求进行自适应调整。SDV 还可以通过软件应用接受远程控制或更新，从而改变其功能、性能或外观。

例如，通过 SDV 我们可以：

- 根据司机的心情或路况，在环保、运动或自动驾驶等不同的模式之间自由切换。
- 根据乘客的偏好或天气状况，调节其内部灯光、音乐或温度。
- 接收来自制造商或第三方供应商的软件更新，从而提升其功能或安全性。

## 通过流处理技术挖掘 SDV 数据价值

SDV 从传感器、摄像头、GPS、雷达等多种来源生成海量的数据，这些数据具有多样性和复杂性。它们需要实时或近实时地进行处理，以便为 SDV 及其用户提供有用的信息并协助他们决策行动。

流处理是一种针对此类数据流的高效处理技术。它采用数据到达后立即处理的方式，无需在数据库或文件系统中保存。流处理可以对数据流执行各种操作，如过滤、聚合、转换、补全和分析。

此外，流处理可以整合来自多个来源的数据，实现多源数据的集成，从而提供统一的数据视图。它还具有水平扩展的能力，以应对不断增加的数据量和增长速度。

通过流处理，我们可以利用 SDV 数据在以下方面获益：

- **提升安全和性能：**流处理可以发现车辆的异常或故障，并及时通知司机或服务提供商。它还可以根据数据分析结果来调节参数以优化 SDV 的性能。
- **优化用户体验：**流处理可以根据司机或乘客的偏好或行为，为他们提供定制化的建议或反馈。它还可以为 SDV 提供新的功能或服务，如娱乐、导航或社交网络。
- **提高效率和利润：**流处理可以通过提高资源利用和降低能源消耗来减少 SDV 的运营和维护成本。此外，流处理可以通过从数据洞察中衍生的增值服务和产品为服务提供商创造额外的收入。

## eKuiper：适用于 SDV 数据的强大流处理引擎

[LF Edge eKuiper](https://ekuiper.org/zh) 是一款专为物联网边缘设计的轻量级数据流处理引擎。它的核心功能仅占用 10MB 的空间，可以轻松地部署在车辆 MPU 上。用户可以借助 eKuiper 来对 SDV 数据进行流处理。

在我们的文章 [*使用 eKuiper 按需桥接 CAN Bus 数据至 MQTT*](https://www.emqx.com/zh/blog/bridging-demanded-signals-from-can-bus-to-mqtt-by-ekuiper) 中，我们已经演示了 eKuiper 如何连接和解析 CAN 总线数据。此外，eKuiper 还支持 MQTT、HTTP、SQL 数据库和文件等多种数据源。结合 [NanoMQ](https://nanomq.io/zh)，它甚至可以连接到与 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 桥接的 SOA（SomeIP、DDS）数据。通过流处理能力，eKuiper 可以计算和转换来自这些不同数据源的数据，以生成有用的信息并触发相应的操作。

eKuiper 使用 SQL 来创建称为规则的流处理管道。这些规则可以实现热部署和热更新。多个规则可以灵活地串联起来，以构建复杂的场景。通过单个规则，eKuiper 可以实现：

- **信号层数据筛选：**灵活选择想要查看或分析的信号层数据，无论是指定的信号、变化的信号、或符合某些条件的信号。
- **车辆侧规则引擎：**可以在车辆侧设置一些自定义规则，让 eKuiper 在满足某些条件时自动执行一些动作。比如，您可以设置当车速超过 70 公里时，自动关闭所有车窗。
- **智能分析：**利用 eKuiper 的本地分析能力，在不需要编码或连接云端的情况下，可以对数据进行实时处理和分析。您还可以使用 eKuiper 集成的人工智能模型（目前支持 TF Lite）来进行更深入的数据挖掘和预测。它还可以将数据反馈给车辆上的训练模型，以提高模型的准确性和效率。
- **边缘计算：**利用 eKuiper 的边缘计算能力，降低传输带宽和云端计算压力。eKuiper 可以根据时间窗口对数据进行汇总，大幅减少传输的数据量，同时保持数据的趋势不变。它还支持对数据进行下采样和压缩，以节省存储空间和网络资源。
- **异质数据融合：**利用 eKuiper 的数据融合能力，解析来自各种协议（如 TCP、UDP、HTTP、MQTT）和各种格式（如 CAN、JSON、CSV）的数据，并通过灵活的规则将其合并为一个统一的数据流。
- **消息路由：**利用 eKuiper 的消息路由能力，智能地决定哪些数据发送到云端，哪些数据保存在本地供其它车载应用使用。比如，您可以根据 GDPR 或某些白名单来确定消息路由，以保护用户的隐私和安全。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>



## eKuiper 赋能软件定义汽车

根据 eKuiper 的上述能力，我们可以自由搭建 SDV 工作流，并通过执行它们来实现各种可能的场景。

### 安全问题检测

利用车辆的实时数据，eKuiper 可以智能地分析和识别安全问题，并及时地提醒司机采取措施。我们可以使用简单的 SQL 语句来制定自己的安全规则，比如当车速超过限制时发出警告；也可以使用人工智能模型来检测更复杂的安全问题，比如疲劳驾驶、车道偏离、碰撞风险等。我们只需将训练好的 TensorFlow Lite 模型上传到车上，eKuiper 就会自动加载并将数据输入模型。其结果可以用于触发动作或提醒司机。

在下面的示例中，我们将使用 CAN 总线的数据来识别频繁的刹车行为并提醒司机。

```
SELECT CASE WHEN count(*) > 5 THEN 1 ELSE 0 END as alert
FROM CANStream
WHERE SENSOR_TYPE_BRAKE_DEPTH>15
Group by SlidingWindow(ss, 10)
```

它检测最近 10 秒内，是否有超过 5 个刹车深度大于 15 的刹车事件。如果有，它将发出警报。

### 利用自动化功能提升用户体验

利用解析出的有意义的数据，eKuiper 可以自动地触发一些动作，以优化用户的驾驶体验。比如，当您忘记关车窗而车速超过了 80 公里/小时，eKuiper 可以自动关闭车窗；当车辆陷入拥堵而车内温度升高时，eKuiper 可以自动开启空调，并根据您的偏好调节温度和风速。这样，您就可以享受更加舒适和便捷的驾驶体验。

在下面的示例中，我们将使用 CAN 总线的数据，根据预先训练好的人工智能模型，为司机自动推荐最佳驾驶模式。假设我们已经根据之前收集的 CAN 总线数据训练好了能够识别驾驶模式的模型。

1. 通过 REST API 将模型上传到车辆。
2. 定义规则来加载模型，对流数据进行推理，并通过 MQTT 发送警报。`tflite` 函数是 eKuiper 提供的一个插件函数，用于对 TensorFlow lite 模型进行推理。第一个参数是可变的模型名称，接下来的参数是输入数据。结果是模型的输出。

```
SELECT tflite("trained_mode",signal1, signal2) as result FROM CANStream
```

### 派生指标的计算与可视化

收集的数据通常只包含基本的原始数据。为了从数据中获取有用信息，我们需要用算法进行计算。例如，计算指定时间窗口内的平均速度。然后可以在汽车的界面上展示这些数据并提供驾驶建议。

在下面的示例中，我们记录并计算每次刹车的模式，包括平均减速度、刹车距离等。这种分析有助于我们了解用户的刹车习惯，并根据这些信息为司机提供建议。结果可以显示在汽车的界面上，让司机了解自己的刹车习惯。

eKuiper 使用两条规则来完成这个功能。第一条规则检测刹车并选择要计算的信号。第二条规则逐步计算这些指标。这两条规则由内存中的 sink/source 连接，像流水线一样工作。

**规则 1：**检测刹车信号，确定计算的开始条件，并选择适当的信号传递给下一条规则。我们可以使用 SQL 语句来描述这个算法：只有当刹车打开且速度超过 10 时，才开始进行计算。当刹车关闭或速度降低到 3 以下时，停止计算。

```
SELECT CASE WHEN brake = 1 AND speed > 10 THEN 1 ELSE 0 END AS brake_start,
       CASE WHEN brake = 0 OR speed < 3 THEN 1 ELSE 0 END AS brake_end,
       speed, distance, timestamp
FROM CAN_STREAM
WHERE brake_start = 1 OR (brake_end = 1 AND lag(brake_end) = 0)
```

这条规则将在刹车开始或结束时，把数据传送给第二条规则。输出的数据格式如下：

```
{
  "brake_start": 1,
  "brake_end": 0,
  "speed": 20,
  "distance": 100,
  "timestamp": 1622111111
}
{
  "brake_start": 1,
  "brake_end": 0,
  "speed": 18,
  "distance": 120,
  "timestamp": 1622111311
}
...
{
  "brake_start": 0,
  "brake_end": 1,
  "speed": 0,
  "distance": 200,
  "timestamp": 1622112511
}
```

**规则 2：**按照公式 `a=△v/△t` 计算平均减速度，并在刹车停止时输出计算结果。

```
SELECT lag(speed) OVER (WHEN had_changed(brake_end)) as start_speed, speed as end_speed, (start_speed - end_speed) / (timestamp - lag(timestamp) OVER (WHEN had_changed(brake_end)) ) AS deceleration
FROM BRAKE_MEM_STREAM
WHERE brake_end = 1
```

其中，`lag(speed) OVER (WHEN had_changed(brake_end))` 指的是 brake_end 上一次从 1 变成 0 的时刻的速度值，也就是刹车启动时的速度。该 lag 函数也用于计算时间间隔。结果如下图所示，它只有在刹车停止时才会输出一次。

```
{
  "start_speed": 20,
  "end_speed": 0,
  "deceleration": 0.5
}
```

## 结语

在软件定义汽车不断塑造未来交通的过程中，流处理技术已成为发挥 SDV 数据全部价值的关键驱动力。通过实时分析能力，流处理技术提升了安全性、优化了性能，并为智能车辆提供了个性化的体验。随着技术的不断进步和应用的扩展，流处理技术将深刻改变我们对软件定义汽车的认知和互动方式，让我们的出行变得更加安全、舒适和高效。



<section class="promotion">
    <div>
        联系 EMQ 车联网解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
