本月 [eKuiper](https://ekuiper.org/zh) 团队继续专注于 1.10 版本的开发，并于月底了发布 [1.10 版本](https://github.com/lf-edge/ekuiper/releases/tag/1.10.0)。本月完成的主要新功能包括：

- 规则定时执行
- EdgeX Foundry Minnesota (v3) 正式版本的适配和测试
- Sink 添加通用参数以更易用且高效地完成常用数据变换
- 更强大的数组和对象处理能力

本月 eKuiper 发布的版本包括：

- eKuiper 1.10.0([Release eKuiper 1.10.0 · lf-edge/ekuiper (github.com)](https://github.com/lf-edge/ekuiper/releases/tag/1.10.0)): 最新的版本，包含大量的新功能，详情请关注后续推送。
- eKuiper 1.9.2([Release eKuiper 1.9.2 · lf-edge/ekuiper (github.com)](https://github.com/lf-edge/ekuiper/releases/tag/1.9.2))：1.9 系列的最新 fixpack，包含了 1.9 系列的所有功能，添加了一些 bug 修复。

## 规则定时执行

某些场景下，用户数据可能是周期性的，为了节省运行资源，用户希望在没有数据的情况下停止规则，而只在指定的时间段启用规则。用户需要规则自动周期性执行，如每天凌晨执行一次，每周执行一次等。用户可以采用 eKuiper 的 API 进行规则的手工启停，但是在边缘大规模部署的情况下，手工启停是不可行的，边缘规则自治迫在眉睫。因此，我们在规则中添加了定时执行的功能，用户可以指定规则的定时执行时间，规则会自动在指定的时间段启动和停止。

规则的 option 添加了两个参数，分别是 `cron` 和 `duration`。

- `cron` 参数指定了规则的定时执行时间，格式遵循 cron 表达式的格式，如 `0 0 0 * * *` 表示每天凌晨 0 点执行一次。
- `duration` 参数指定了规则的执行时间。该参数采用 duration string 格式，包含数字和时间单位，如 `1m` 表示执行 1 分钟。

例如，以下的规则通过 options 里的参数定义了每两分钟执行一次，每次执行 1 分钟。

```
{
  "id": "ruleSchedule",
  "sql": "SELECT * FROM demo;",
  "options": {
    "cron": "*/2 * * * *",
    "duration": "1m"
  },
  "actions": [{
    "mqtt":  {
      "server": "tcp://broker.emqx.io:1883",
      "topic": "result/rule"
    }
  }]
}
```

> 注意：duration 不应该超过两次 cron 周期之间的时间间隔，否则会引起非预期的行为。

计划任务规则的增删改查和状态查询与普通的规则一致，可以通过 API 或者 CLI 进行操作。计划任务执行时，规则为 Running 状态。若计划任务执行时间到期，规则会自动停止等待下次调度，状态变为 Stopped: waiting for next schedule.。通过 Stop 命令停止计划任务，规则将立即停止而且从调度器中移除。

## EdgeX v3 支持

EdgeX v3 是 EdgeX Foundry 的下一个重要版本，eKuiper 1.10.0 版本已经支持了 EdgeX v3。eKuiper 的 EdgeX source 和 sink 已更新适配，用户已有的规则可以无缝迁移到 EdgeX v3。

同时，在我们的测试中，1.10 版本的 eKuiper 仍然可以兼容 EdgeX v2，用户可以根据自己的需要选择 EdgeX v2 或者 EdgeX v3。

需要注意的是，由于 EdgeX 中已移除 ZeroMQ 总线的支持，我们也移除了 eKuiper 中的 EdgeX source/sink 的 zmq 协议支持。采用默认 redis 总线或 MQTT 总线的用户不受影响。

## Sink 数据变换

用户的数据可能会有嵌套结构，例如 Neuron 接入的数据中通常包含一些元数据，payload 里的 values 字段才是用户需要的数据。另外，使用复杂 SQL 语句进行数据处理时，可能 SELECT 子句中会定义一些计算的中间结果，并不需要全部输出到 sink 端。在这种情况下，sink 端需要对数据再进行变换或者格式化。数据模板是一种常用的方式，它功能强大，支持各种格式化。然而它的缺点是需要用户有一定的编写模板能力，同时运行性能较差。新版本中，sink 端支持了更多的常用的数据变换，包括数据抽取，批量发送的相关属性，并扩展到大部分的 sink 类型中。

- 批量发送：默认情况下，sink 为每个事件产生一条数据。但是如果数据吞吐量很大，这样会有一些问题。例如 IO 开销大、若压缩的话压缩比低、发送到云端的网络开销大等。同时，发送速率快可能增加了云端处理压力。为了解决这些问题，新版本中支持了 MQTT sink 中的批量发送功能。批量发送的原理是，sink 会采用一定的策略对数据进行缓存，然后一次性发送到云端。用户可通过配置参数 `batchSize` 和 `lingerInterval` 来控制批量发送的数据量和时间间隔。
- 数据抽取：在使用中间数据或者计算数据与写入数据格式不一致时，我们需要在 sink 端抽取出需要的数据。新版本中，所有 sink 添加了两个通用参数 `fields` 和 `dataField`。 这两个参数在之前的数据存储相关 sink，包括 SQL、Redis、InfluxDB 等中已经支持。因为在数据写入中，目标数据库通常有严格的列定义，而 SQL SELECT 语句不一定能匹配列，往往有冗余选择的字段。在其他的 sink 中，也会有这样的数据抽取的需求。新版本中，这两个属性扩展到了 MQTT、Kafka、File 等 sink 中。其中，`dataField` 参数用于指定表示数据的字段以区分于表示元数据等其他数据的字段，例如 `dataField: values`。`fields` 参数用于指定需要输出的字段，从而可以完全匹配目标系统需求，例如 `fields: ["a","b"]`。

## 数组和对象处理

SQL 语法最初是针对关系数据库设计的，而数据库中的复合数据类型较少，因此对于数组和对象的处理能力有限。在 IoT 场景中，接入的数据格式多为 JSON，嵌套的符合数据类型是一等公民。eKuiper SQL 在最初就加入了对嵌套数据的访问能力。然而，对于其中的更深入的数据变换仍然有很多需求尚未得到满足。新版本中，我们对数组和对象的处理能力进行了增强，包括数组数据转为多行、数组和对象处理函数等。

- 支持数据源的数组 payload：当数据源使用 JSON 格式时，之前的版本只支持 JSON 对象的 payload，新版本中支持了 JSON 数组的 payload。而且，用户无需配置，系统会自动识别 payload 类型。
- Unnest 函数展开数组字段，将一行数据转为多行。
- 持续增加的数组和对象处理函数。

## 其他更新

其他功能更新包括：

- Graph API 中支持访问已定义的流和查询表，支持流表 Join 这样采用可视化编辑器时可完成与 SQL 规则相同的流表合并计算功能。
- 嵌套结构访问语法糖，不产生歧义的情况下可用点（.） 代替箭头符号 （->）访问嵌套对象。

文档方面，我们添加了一篇教程，介绍如何使用外部服务访问已有的 AI 微服务：[使用外部函数运行 AI 算法](https://ekuiper.org/docs/zh/latest/guide/ai/tensorflow_lite_external_function_tutorial.html) 。至此，在 eKuiper 中结合 AI 计算的所有方法都已通过教程覆盖。用户可用根据实际需求选用适合的方法。

## Bugfixes

本月解决的 bug 都发布到了 1.10.0 版本中，较早解决的也发布到了 1.9.2 版本中。

值得一提的 fixes 包括：

- 解决使用 Portable 函数的规则重启偶尔失败的问题
- 解决插件配置错误导致规则崩溃问题
- 窗口使用 where 全部过滤后不再输出空结果 （1.10）
- CAST double 转 string 不再使用科学计数法表示 （1.10）

## 下月计划

下个月我们将开始计划 1.11 版本的开发，我们将支持更多的 SQL 语法，例如 limit 并继续添加数组/对象函数。另外，我们也将研究如何利用 schema 加快数据 IO 解析，提高吞吐量。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
