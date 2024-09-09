3 月份，eKuiper 团队主要进行了 1.9.0 版本的开发，增加了一些重要的功能，进一步提高了 eKuiper 的性能和可用性：

1. IO Connectors 增强。新增了多 Neuron 连接的功能；在 HTTP 连接方面，我们提供了类 oAuth 的基于动态 token 的鉴权过程的支持；此外还支持了 MQTT 连接中压缩和解压，减少边云传输的带宽损耗。
2. 分析能力增强。我们添加了许多新的转换函数，包括 JSON 字符串相关、base64 编码相关以及压缩相关的函数，方便用户更灵活地处理和转换数据流。
3. 运营效率增强。新版本中继续优化了数据导入和导出功能，支持选择需要的规则进行导入导出，实现了规则依赖的流、配置和插件等的自动推断和导出。另外，我们优化了 eKuiper manager 中的规则管理界面，可以更准确地展示规则启动中的状态。

eKuiper 1.9.0 将在本月底发布。除此之外，eKuiper 也在 3 月份发布了 1.8.2 版本，主要修复了用户和社区反馈的问题。

## 多 Neuron 对接

[Neuron](https://github.com/emqx/neuron) 是运行在各类物联网边缘网关硬件上的工业协议网关软件，可以采集来自繁杂多样工业设备的不同协议类型数据，采集的数据经由 eKuiper 做流式的实时处理，获取更大的价值。eKuiper 一直在持续优化和 Neruon 的对接和整合。

eKuiper 1.5.0 版本加入了基于 NNG ipc 通信方式的 Neuron source 和 sink，使得用户无需配置即可在 eKuiper 中接入 Neuron 中采集到的数据进行计算；也可以方便地从 eKuiper 中通过 Neuron 控制设备 。NeuronEX 版本中集成了 Neuron + eKuiper ，使得用户无需任何额外部署和配置工作，即可处理采集到的工业数据。集成的方式满足了一部分用户的使用场景，但是在另一类场景中，用户需要单独部署 Neuron 和 eKuiper，而且可能需要两者分别根据数据量等情况进行部署伸缩。这种情况下，我们就需要 eKuiper 可以对接多个 Neuron 实例。

1.9.0 版本中，eKuiper 中的 Neuron source 和 sink 的配置中增加了连接 URL 的配置。基于此， eKuiper 可以配置多个不同的 Neuron 连接，采用不同的 host/IP 和 端口来识别，然后把连接应用到流和 sink 中，实现多 Neuron 连接。连接 URL 默认为 tcp，也可以配置为 ipc，用于与旧版 Neuron 连接。创建流之后，数据处理规则创建和管理的功能与原来的版本相同，详细教程请参考[使用 eKuiper 对 Neuron 采集的数据进行流式处理 | eKuiper 文档](https://ekuiper.org/docs/zh/latest/integrations/neuron/neuron_integration_tutorial.html#使用-ekuiper-对-neuron-采集的数据进行流式处理)。

![Neuron 北向应用配置](https://assets.emqx.com/images/e583ae80c464a7da73a2171d71c3598f.png)

<center>Neuron 北向应用配置</center>

![eKuiper 中配置 Neuron 连接 URL](https://assets.emqx.com/images/1b694ed3018aff26f3c43bf777725030.png)

<center>eKuiper 中配置 Neuron 连接 URL</center>

实现 eKuiper 和 Neuron 多对多连接需要两个组件同时进行开发。各个版本之间的对接关系有以下几种组合：

1. eKuiper 1.9 之后版本与 Neuron 2.4 之后版本可支持多对多对接。
2. eKuiper 1.9 之后版本与 Neuron 2.4 之前版本对接只能通过 ipc，需要配置 `SOURCES__NEURON__DEFAULT__URL: "ipc:///tmp/neuron-ekuiper.ipc"`，并且启用 volumes nng-ipc 的配置。Neuron 无需暴露 7081 端口。
3. eKuiper 1.9 之前版本与 Neuron 2.4 之前版本对接只能通过 ipc，需要去除 `SOURCES__NEURON__DEFAULT__URL` 环境变量配置并且启用 volumes nng-ipc 的配置。Neuron 无需暴露 7081 端口。
4. eKuiper 1.9 之前版本与 Neuron 2.4 之后版本无法直接对接，可通过 MQTT 中转。

## 连接动态 token 的 HTTP 服务

在本次更新中，eKuiper 新增了 HTTPPull 源以及 Rest Sink 的动态令牌鉴权的支持。这些功能使 eKuiper 更容易地连接到各种服务和数据源。

之前的版本中，我们支持通过自定义 header 的方式设置 apikey 等 header 实现基于固定 token 的认证方式。该方式可以覆盖一些安全配置要求较低的接口，例如内部的接口。还有许多接口需要动态获取和更新 token。为了接入这类 HTTP 服务，我们实现了相同的类似 OAuth 的认证流程的配置方式。在这个流程中，用户需提前获取认证码或者 API key。之后，eKuiper 中可配置该认证码，规则运行后会使用认证码来请求访问令牌，并可能在到期后通过刷新令牌来刷新令牌。

有了这个功能之后，eKuiper 可访问动态令牌的 HTTP 服务，例如 Neuron 的 REST API，从而实现对 Neuron 的自动控制。例如，可以配置 HTTPPull 监听 Neuron 的节点 API，当节点变化时自动触发规则。以下为访问 Neuron 节点 API 的 HTTPPull source 配置示例，需要配置 access token 的获取方式，用户也可以在 manager 上进行配置。

```
neuron_pull:
  # url of the request server address
  url: http://127.0.0.1:7000/api/v2/node/state
  # HTTP headers required for the request
  headers:
    Accept: application/json
    Authorization: 'Bearer {{.token}}'
  # Get token
  oAuth:
    # Access token fetch method
    access:
      # Url to fetch access token, always use POST method
      url: http://127.0.0.1:7000/api/v2/login
      # Body of the request
      body: '{"name": "admin","pass": "0000"}'
      # Expire time of the token, time unit is second, allow template
      expire: '3600'
```

## 节省传输带宽：MQTT 压缩/解压

MQTT 是云边协同最常用的数据传输方法。云边传输带宽成本昂贵，通过减小传输数据的大小，可以提高数据传输的效率并降低成本。定位在边缘端的 eKuiper 通过 MQTT sink 上报数据到云端时，支持设置压缩方式，目前支持的算法包括 `zlib`, `gzip` 和 `flate`。使用方式有很简单，新版本中 MQTT sink 添加了属性 `compresson`，配置需要的压缩算法名字即可。

```
"mqtt": {
    "server": "{{mqtt_broker_address}}",
    "topic": "result/sinkcompress",
    "sendSingle": true,
    "compression": "zlib"
  }
```

同时，MQTT source 也支持解压缩，以接收云端下发的压缩数据或者部署在云端时接收边缘端上传的数据。MQTT source 的配置中添加了 `decompression` 属性，配置成所需的解压算法即可。

## 丰富数据转换函数

eKuiper 1.9.0 版本还增加了许多新的转换函数，例如 to_json、parse_json、decode等。这些函数使eKuiper的表达能力更加强大，可以更灵活地处理和转换数据流。例如，如果您要将数据流转换为JSON格式并进行特定字段的过滤，则可以使用以下代码：

```
SELECT id, compress(to_json(object_construct("recordId", newuuid(), "recordDateTime", timestamp, "groupName", group_name, "recordData", values)), \"zlib\") as trainData FROM demo
```

这段代码使用 `object_construct` 函数动态拼接出一个对象，再用 `to_json` 函数将对象转为字符串，最后再用 `compress` 函数，使用 zlib 算法将其压缩作为 trainData 字段。

这个版本中，我们新提供的函数包括：

- compress(value, method ): 压缩字符串或二进制数据，压缩算法支持 zlib, gzip 和 flate
- decompress(value, method): 解压缩二进制数据
- to_json(object)：数据转换为 JSON 字符串
- parse_json(json_str)：将 JSON 字符串解析为对象等数据
- decode(str, method): 解码 base64 字符串，编码方法之前版本已支持

需要注意的是，相比 MQTT 的压缩解压功能，此处的压缩解压方法采用函数提供，可针对局部的字段而非整体的 payload 进行压缩操作。

## Coalesce 函数处理缺失值

eKuiper 现在提供对 Coalesce 函数的支持。该函数返回一组值中的第一个非空值，可用于将流中的 null 值替换为指定的值。当处理包含缺失值或 null 值的数据时，这可以确保数据被正确处理。

```
SELECT COALESCE(email, phone) AS contact_info
FROM customer;
```

在此示例中，`COALESCE` 函数将在 `email` 和 `phone` 列中查找第一个非空值，并将其作为 `contact_info`列的值返回。如果 `email` 列为空，则返回 `phone` 列的值。

## 局部数据导入和导出

eKuiper 前几个版本中陆续添加了一部分导入导出功能，方便节点的迁移。之前的导出为全量导出，导入为覆盖式的全量导入，对增量管理不友好。新版本中，我们支持部分数据导入和导出。该功能使用户可以导入和导出仅部分数据，而不是整个数据集。当使用大型数据集时，这可以节省时间并减少传输的数据量，提高效率。

局部数据导入和导出 API 与全量数据相似，主要特点在于基于规则进行设计，导出时用户仅需指定要导出的规则，API 会计算规则的依赖，包括流定义、配置和插件等等相关信息，一并导出。在 eKuiper manager 中，用户可以在规则管理界面选择需要导出的规则进行导出。

![导入导出功能](https://assets.emqx.com/images/bc66dbc8c34c7089efd6ef4a79e1e893.png)

## 更易用的规则管理

由于规则的启停 API 是异步的，API 调用完成后无法立刻得知启动是否成功，所以在之前版本的 eKuiper manager 中，点击启动或重启，规则立刻变为启动状态。然而，规则有运行时错误时用户无法立刻从界面上获得反馈，从而形成一定程度的误导。新的版本中，规则启动时将即时进入启动中的状态，使得用户可以得到立即的反馈。若启动成功，规则状态会变为绿色，否则会变为红色，使得用户可以感知到启动最终的状态。

![更易用的规则管理](https://assets.emqx.com/images/bbe53b37122a6554e3980e3896268fe3.png)

## Bugfixes

本月我们解决了一些 Python 插件热更新等问题，并发布到 1.8.2 版本中。主要的 bug fix 列表如下：

- 修复 redis source 连接测试问题
- 修复更新规则内容错误时不报错的问题
- 修复窗口过滤条件不满足导致窗口不触发的问题
- Portable 插件超时可配置以防止 AI 模型导入超时
- 修复 Portable 插件更新到不正确的插件时无法热恢复的问题
- 修复 Flow Editor 部分节点参数输入框，描述不正确等问题

## 即将到来

下个月我们将主要进行 1.10.0 版本的开发，这个版本将进行 EdgeX Minisota 版本的适配。另外，我们也会探索外部状态，如 Redis 状态的使用，实现持久化的状态。敬请期待。
