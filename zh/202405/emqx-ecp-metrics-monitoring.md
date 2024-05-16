迈向未来的工业生产，需要的不仅是自动化，更是智能化。如果工业企业的管理者能够实时监测每一生产环节的设备运行状态，每一数据点位情况，洞察和优化每一步生产流程，他们将能够做出更精准的决策，提高生产效率和产品质量。

通过集成先进的指标监测工具，EMQX ECP 工业互联数据平台（下文简称“ECP”），可帮助企业实时监测和控制生产流程。 ECP 提供的指标监测功能，包括指标监控、日志管理和异常告警， 为企业提供了一个全面的数据监控和管理解决方案。

指标监控可帮助工业企业实时跟踪关键设备与生产指标，日志管理则允许企业对日志数据进行集中存储和分析，而异常告警确保企业能够在第一时间发现异常并响应潜在的系统故障和性能问题。这些功能的结合，不仅提升了生产线的透明度和可控性，还为工业生产带来了前所未有的灵活性和响应速度，确保企业在竞争激烈的市场中保持领先。

本文将详细介绍 ECP 指标监控、日志管理和异常告警这三方面的支持能力与使用方式。

## 指标监控

指标监控是确保工业互联数据平台稳定运行的关键环节。ECP 使用 Prometheus 及其 Pushgateway 组件，对[工业边缘网关软件 NeuronEX](https://www.emqx.com/zh/products/neuronex) 进行细致的指标数据收集。NeuronEX 是 EMQ 旗下部署在边缘端，专注在边端提供多源数据接入与集成、以及智能边缘流式计算，是 ECP 边缘侧的核心组件。

当 ECP 对 NeuronEX 进行纳管或托管时，系统会自动下发所需的度量指标、设定指标数据的更新频率，以及提供 Pushgateway 的连接信息。随后，NeuronEX 会根据设定的时间间隔，将指标数据定时推送至 Pushgateway，最终由 Pushgateway 将这些数据推送至 Prometheus 服务器，完成整个数据收集流程。

ECP 已集成安装了 Pushgateway 和 Prometheus，简化了用户的配置工作。用户可直接在 ECP 工作台左侧菜单的**“边缘监控”**选项中查看 NeuronEX 的监控指标数据，无需进行额外设置。

![EMQX ECP 边缘监控](https://assets.emqx.com/images/b4c9475e0b5d29cb93433d38d90590c8.png)

指标数据主要分为三个部分：基础指标数据、NeuronEX 的详细指标数据、以及异常驱动和规则列表。

- **基础指标数据**涵盖了 NeuronEX 的状态统计数据、数采模块的南北向驱动节点的统计数据、数据处理模块规则的统计数据，以及连接的设备点位数的统计数据。
- **NeuronEX 详细指标数据**则进一步细化，展示了南向设备与北向应用各节点的连接与运行状态，以及规则处理中数据的流入流出情况。
- **异常驱动和规则列表**则专注于展示那些处于非正常状态的数采驱动和数据处理规则。用户可以通过筛选功能更迅速地定位出现异常的边缘侧 NeuronEX 位置，并直接进入 NeuronEX 控制面板，进行必要的操作和排查。

如果需要对指标更新频率进行调整，可从“**系统设置”**下的“**通用配置”**中调整 NeuronEX 的推送时间间隔，以实现更加灵活的监控管理。

![推送时间间隔](https://assets.emqx.com/images/9f8efa9ba6b49334921fbed65bf49d97.png)

## 日志分析

在工业互联的云边协同环境中，云端和边缘端的多样化产品会产生不同格式的日志数据。为了有效管理这些数据，ECP 使用 Elasticsearch 日志服务器，它不仅统一存储日志信息，还提供聚合和可视化的查询和分析功能。以下将以边缘侧 NeuronEX 为例，具体介绍日志的使用情况。

边缘侧 NeuronEX 通过 Telegraf 将 syslog 日志数据接入 Elasticsearch。ECP 在纳管或托管 NeuronEX 时下发 Telegraf 服务地址和所需收集的日志级别信息。NeuronEX 收集的日志随后被发送至 Telegraf 的 syslog 输入插件，并通过 Elasticsearch 输出插件最终写入 Elasticsearch 日志服务器。

Telegraf 已集成安装在 ECP 中，并已预配置了 syslog 输入插件信息。Elasticsearch 日志服务器需要用户自行安装。安装完成后，按以下步骤分别配置 Telegraf 输出插件和 ECP 系统配置：

- Telegraf 输出插件配置如下，其中：

  - `urls` `username` `password` 分别为 Elasticsearch HTTP 服务器的访问地址、用户名、密码。
  - `index_name` 为日志在 Elasticsearch 中使用的索引名称，值必须为 `{{appname}}`。
  - `health_check_interval` 是健康检查的频率，可按需要调整。
  - `insecure_skip_verify` 是指定 Elasticsearch 开启 tls/ssl 情况下是否跳过证书链及域名检查。
  - 其他配置项说明，可参考 [Telegraf elasticsearch 插件说明](https://github.com/influxdata/telegraf/blob/master/plugins/outputs/elasticsearch/README.md)。

  ```
  [[outputs.elasticsearch]]
    urls = [ "http://elasticsearch-server:9200" ]
    username = "elastic"
    password = "elastic"
    index_name = "{{appname}}"
    health_check_interval = "10s"
    insecure_skip_verify = true
  ```

- ECP 的**系统设置** → **通用配置** → **日志接收器**默认关闭，在类型中选择“开启”进行启用，并选择需要的日志级别、填写 Elasticsearch 相关配置。

  ![日志接收器](https://assets.emqx.com/images/4eba8000f123f6e8014ca503e066e21d.png)

启用日志功能后，用户可从工作台左侧菜单的日志选项中，查看到边缘侧 NeuronEX 的实时日志，包括边缘服务名称、日志时间、日志级别和具体日志信息。通过时间及关键字段的搜索过滤功能，用户可以快速定位到目标日志，有效排查和定位具体问题。

此外，在 ECP 工作台**“边缘管理”**选项下，用户也可直接从各个 NeuronEX 边缘服务的操作栏中访问该 NeuronEX 的日志列表，进一步简化日志管理流程。

## 异常告警

ECP 为管理大量边缘侧软件提供了灵活的告警机制。该机制旨在统一监控边缘侧软件的运行状况，并在出现故障或异常时及时通知用户。

一方面，ECP 的告警规则中内置了边缘侧 NeuronEX 的主要异常故障问题，用户可配置规则触发的敏感度及规则的严重级别，从而控制告警的严重程度及通知频率。

![告警规则配置](https://assets.emqx.com/images/7a846d1211d1e82abbe4422418839628.png)

另一方面，ECP 支持细粒度的通知范围配置。用户可以为不同的 NeuronEX 配置不同的电子邮件或 Webhook 告警推送接收方式。此外，还可以针对不同告警级别设置不同的通知方式和重复告警时的沉默时效，以满足不同级别的告警通知需求。

![告警推送](https://assets.emqx.com/images/f939a0f5a8c27550deff651722311e25.png)

如果用户有定制化的告警问题需要纳入 ECP 的告警通知机制，ECP 也提供了自定义告警的 REST API。用户可通过此 API 将业务中其他告警信息推送到 ECP， 并进行相应的通知。

![REST API](https://assets.emqx.com/images/47a16f418129b91fd502722b55bbdc03.png)

无论用户选择何种告警推送方式或频率，ECP 都会将 NeuronEX 推送的告警信息实时地展示在告警面板中。用户可以根据时间及关键字段，对告警信息进行筛选、定位，并将已经处理完成的告警信息归档至“历史告警”。

![告警列表](https://assets.emqx.com/images/308c7d50e30810515f7b87ace60a672f.png)

## 总结

ECP 的指标监测功能，包括指标监控、日志管理、和异常告警，都是为了帮助用户全面了解工业系统的运行情况，及时发现问题并进行故障排除，从而提升系统的可靠性、性能和安全性。这些功能也结合了工业场景中大规模数据采集、数据处理的实际需求，提供了关键的数据指标的可视化的观测能力，助力用户实现高效率的智能化生产。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
