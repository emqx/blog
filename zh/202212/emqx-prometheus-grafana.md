## 前言

作为一款全球下载量超千万的[大规模分布式物联网 MQTT 服务器](https://www.emqx.io/zh)，最新发布的 EMQX 5.0 不仅全球首个达成单集群 1 亿 MQTT 连接支持，也是首个将 QUIC 引入 MQTT 的开创性产品。如今，EMQX 在各个行业为高可靠、高性能的物联网实时数据移动、处理和集成提供着动力，助力企业构建关键业务的 IoT 应用。

> EMQX GitHub: [https://github.com/emqx/emqx](https://github.com/emqx/emqx) 

在使用 EMQX 的过程中，不管是用户、运维人员还是开发者，都需要对其运行状态及产生的指标数据进行监控与观察，以便及时发现问题并处理。除使用内置的 Dashboard 以外，我们还可以通过 EMQX 提供的 API 来将监控数据集成到第三方监控平台中，对包括集群节点状态、连接、订阅主题数、消息吞吐量等 EMQX 运行状态相关指标进行监控。

使用第三方监控系统对 EMQX 进行监控有如下好处：

- 可以将 EMQX 的监控数据与其他系统的监控数据进行整合，形成一个完整的监控系统，如监控服务器主机的相关信息；
- 可以使用更加丰富的监控图表，更直观地展示监控数据，如使用 Grafana 的仪表盘；
- 可以使用更加丰富的告警方式，更及时地发现问题，如使用 Prometheus 的 Alertmanager。

本文将以 Prometheus 和 Grafana 为例，介绍如何将 EMQX 5.0 的监控数据集成到 Prometheus 中，使用 Grafana 来展示 EMQX 的监控数据，并最终搭建出一个简单的 EMQX 监控系统。

> Prometheus 是由 SoundCloud 开源的监控告警解决方案，支持多维数据模型、灵活的查询语言、强大的告警管理等特性。
>
> Grafana 是一款开源的数据可视化工具，支持多种数据源，包括 Prometheus。

## 准备工作

在开始之前，我们需要先准备好以下运行环境，安装并运行所需要的软件工具。本文示例将使用 Docker 来安装和启动，读者也可根据文章中提供的官方下载地址，自行下载安装包进行安装。

### 安装 EMQX 5.0

使用 Docker 快速安装和启动 EMQX 5.0：

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx:latest
```

除 Docker 安装外，EMQX 还支持使用 RPM 或 DEB 包安装，具体安装方法请参考 [EMQX 5.0 安装指南](https://docs.emqx.com/zh/emqx/v5.0/deploy/install.html)。

安装完成后，我们可以打开 `http://localhost:18083` 来访问 EMQX 的 Dashboard，查看 EMQX 的运行状态。如果能够正常访问到 EMQX 的 Dashboard，此时说明 EMQX 已经安装成功。

![MQTT Dashboard](https://assets.emqx.com/images/b8c76e6ebf5d045a9cf89e9bf088e57f.png)

### 安装 Prometheus

同样，示例中我们将使用 Docker 的方式来快速安装和使用 Prometheus，因为此时我们还没有开始配置 Prometheus，所以可以先下载一份 Prometheus 官方提供的 Docker 镜像。

```
docker pull prom/prometheus
```

在安装完成后，需要配置一份 Prometheus 的配置文件，用于指定 Prometheus 的数据源，以及告警规则等信息。因此可先将 Prometheus 的配置文件配置好，在启动时将配置文件挂载到容器中运行即可。具体配置步骤请见后文。

除使用 Docker 外，也可以参考 [Prometheus 官方文档](https://prometheus.io/docs/prometheus/latest/getting_started/)，下载和使用二进制包来安装和运行 Prometheus。

### 安装 Grafana

使用 Docker 快速安装和启动 Grafana：

```
docker run -d --name grafana -p 3000:3000 grafana/grafana-oss
```

读者也可以参考 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)，下载和使用二进制包来安装和运行 Grafana。

当 Grafana 启动完成后，我们可以打开 `http://localhost:3000` 来访问 Grafana，如果能够正常访问到 Grafana 的登录页面，此时说明 Grafana 已经安装成功。

![Grafana](https://assets.emqx.com/images/1a947aabc0fca127676bd2b7ed220a85.png)

### 安装 Node Exporter

这是一个**可选的步骤**。

如果想要监控部署 EMQX 的主机信息，可以使用 Node Exporter 来获取主机的信息。Node Exporter 用于收集服务器的监控数据，例如 CPU、内存、磁盘、网络等信息。

> **注意**：Node Exporter 仅支持获取 **\*nix （类 Unix）系统**的监控数据，Windows 用户推荐使用 [Windows exporter](https://github.com/prometheus-community/windows_exporter)。

本文不建议使用 Docker 来安装 Node Exporter，具体安装和使用操作请参考 [Node Exporter 官方文档](https://prometheus.io/docs/guides/node-exporter/#monitoring-linux-host-metrics-with-the-node-exporter)。安装完成后，我们可以通过 `http://localhost:9100/metrics` 来访问 Node Exporter 的监控数据。如果可以访问到系统主机的监控数据，说明 Node Exporter 已经安装成功。

![Node Exporter](https://assets.emqx.com/images/e80c3be858f7facd0879ee518be4206a.png)

## 配置 Prometheus

完成上述的准备工作后，我们需要配置 Prometheus，使 Prometheus 可以正常采集到 EMQX 的监控数据。

### 配置 Prometheus 数据采集

Prometheus 通过配置文件来指定数据采集的目标，配置文件默认路径为 `/etc/prometheus/prometheus.yml`，可以通过 `--config.file` 参数指定配置文件路径。

EMQX 5.0 提供了一个获取 Prometheus 格式监控数据的 HTTP API -- `/api/v5/prometheus/stats`，使用该 API 时无需认证信息，我们只需要将其配置到 Prometheus 的配置文件中的 `metrics_path` 中即可。

对于使用 Node Exporter 来获取主机监控数据的用户，还需要将 Node Exporter 服务的地址配置到 Prometheus 的配置文件的 `static_configs` 中。

在 Prometheus 配置文件中，通过 `scrape_configs` 指定数据采集的目标，以下为完整的 Prometheus 配置文件内容示例：

> **注意**：在使用配置文件时，需要将各服务对应的 targets 中的 IP 地址替换为您所部署服务的真实 IP 地址。如您使用的是本地部署，则可忽略该提醒。

```
# prometheus.yaml
global:
  scrape_interval:     10s # The default scrape interval is every 10 seconds.
  evaluation_interval: 10s # The default evaluation interval is every 10 seconds.
  # On this machine, every time series will be exported by default.
  external_labels:
    monitor: 'emqx-monitor'
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first.rules"
  # - "second.rules"
  - "/etc/prometheus/rules/*.rules"
# Data pull configuration
scrape_configs:
  # EMQX monitoring
  - job_name: 'emqx'
    metrics_path: /api/v5/prometheus/stats
    scrape_interval: 5s
    honor_labels: true
    static_configs:
      # EMQX IP address and port
      - targets: [127.0.0.1:18083]
  - job_name: 'node-exporter'
    scrape_interval: 5s
    static_configs:
      # node-exporter IP address and port
      - targets: ['127.0.0.1:9100']
        labels:
          instance: dashboard-local
```

在上述配置中，`job_name` 为数据采集的任务名称，`static_configs` 为数据采集的目标，`targets` 为数据采集的目标地址，`127.0.0.1:18083` 为 EMQX 5.0 的 API 服务的地址端口。

最后再将上述的配置文件内容保存为 `prometheus.yaml`，并将其拷贝到 `/etc/prometheus/` 目录下，或存储到您的需要存储该文件的自定义路径下。至此我们就完成了 Prometheus 的简单配置。

### 启动 Prometheus

在完成了 Prometheus 的配置后，我们就可以通过使用配置文件来启动 Prometheus 服务了。如果您是使用 Docker 安装的 Prometheus，可以通过以下命令启动 Prometheus：

```
docker run -d --name prometheus -p 9090:9090 -v /path/to/your/prometheus.yaml:/etc/prometheus.yaml prom/prometheus --config.file=/etc/prometheus/prometheus.yaml
```

如果是通过其它方式下载和安装的，可以在运行 Prometheus 时指定配置文件路径，例如：

```
./prometheus --config.file=prometheus.yml
```

> **注意**：在使用配置文件时，需要将 `/path/to/your/prometheus.yaml` 替换为您存储 Prometheus 配置文件的真实路径。

运行成功后，打开 `http://localhost:9090` 就可以访问 Prometheus 的 Dashboard 了。通过 Dashboard 可以查看 Prometheus 的运行状态，输入 `emqx` 可以查找 EMQX 的监控数据，如果数据显示正常，就表示此时 Prometheus 已经成功启动，并成功采集到 EMQX 的监控数据。

![Prometheus MQTT](https://assets.emqx.com/images/18533ac08e378153aa2ea68eb029947e.png)

### 关于使用 Pushgateway

除直接通过使用包含 EMQX 的 API 配置文件的方式来指定采集数据指标外，EMQX 同样支持使用 Pushgateway 来采集数据指标。

> Pushgateway 为 Prometheus 的一个组件，用于临时存储数据指标，然后由 Prometheus 从 Pushgateway 中拉取数据指标。

通常情况下，我们不需要使用 Pushgateway 服务，因为 EMQX 本身就支持通过 API 来获取数据指标。如果盲目使用 Pushgateway 去获取数据，可能会出现一些问题，例如：Pushgateway 监视多个实例时，Pushgateway 会成为单个故障点，Pushgateway 不会丢弃或者删除其 Series 并且会一直暴露给 Prometheus，等等。

但是在某些情况下，我们可能需要使用 Pushgateway 来采集数据指标，例如：当 EMQX 服务运行在 Docker 容器或 Kubernetes 集群中时，我们可以通过使用 Pushgateway 来采集数据指标，而不需要将 EMQX 的 API 暴露到外部网络中。且通常，Pushgateway 中唯一有效用例是用于捕获服务级批处理作业的结果。点击查看和了解更多，关于[何时使用 Pushgateway](https://prometheus.io/docs/practices/pushing/)。

使用 Docker 安装 Pushgateway 服务：

```
docker run -d --name pushgateway -p 9091:9091 prom/pushgateway
```

更多关于安装和使用 Pushgateway 的信息，请参考 [Pushgateway 安装文档](https://github.com/prometheus/pushgateway#run-it)。此时，我们可以通过 `http://localhost:9091` 来访问 Pushgateway 的 Dashboard。

EMQX 提供了一个配置 Pushgateway 服务的 [API](https://docs.emqx.com/zh/emqx/v5.0/observability/prometheus.html#通过-dashboard-配置)，可以将 EMQX 的数据指标通过配置上报到 Pushgateway 的服务地址中，并最终由 Prometheus 从 Pushgateway 中拉取数据指标。同时也可以直接在 EMQX Dashboard 中配置 Pushgateway 的服务地址，输入完成后，点击更新即可。

![Pushgateway](https://assets.emqx.com/images/e12eda633b664acfeb6cec8998640def.png)

使用 Pushgateway 需要在 Prometheus 的配置文件的 `scrape_configs` 中新增如下配置：

> **注意**：配置中的 targets 需要替换为您真实的 Pushgateway 服务地址。

```
# EMQX Pushgateway monitoring
- job_name: 'pushgateway'
  scrape_interval: 5s
  honor_labels: true
  static_configs:
    # Pushgateway IP address and port
    - targets: ['127.0.0.1:9091']
```

完成配置后，同样根据上述中启动 Prometheus 的操作，使用配置文件启动 Prometheus 服务，即可完成 EMQX 的监控配置。

## 配置 Grafana

在完成了使用 Prometheus 采集 EMQX 数据指标的配置后，我们就可以使用 Grafana 来可视化监控 EMQX 的指标数据了。经过前文的准备工作，我们已经可以成功打开 Grafana 的 Web 控制台了。初次使用 Grafana 的默认账号和密码为 `admin`，登录成功后，我们就可以添加数据源了。

### 添加 Prometheus 数据源

使用 Grafana 可以将 Prometheus 作为数据源，添加 Prometheus 数据源的步骤如下：

1. 点击左侧的 `Configuration`，然后点击 `Data Sources`，进入数据源配置页面；
2. 点击 `Add data source`，选择 `Prometheus`；
3. 在 `HTTP` 配置中，输入 Prometheus 服务的地址，例如：`http://127.0.0.1:9090`；
4. 最后点击 `Save & Test`，如果配置正确，会显示 `Data source is working`，表示配置成功。

![Grafana 添加 Prometheus 数据源](https://assets.emqx.com/images/4867e5e5d3e2d5ae5e8ad19a5b2497bd.png)

配置完成后，我们就可以在 Grafana 中使用 Prometheus 作为数据源来获取监控数据了。接下来我们可以继续添加 Dashboard 的模版来可视化监控 EMQX 的数据指标，也可以手动新建一个 Dashboard，根据自己的需求来添加图表。

### 导入 Dashboard

我们提供给了一个默认的 Grafana 的 Dashboard 模板，可以直接导入到 Grafana 中，然后选择刚才新建的 Prometheus 数据源，倒入成功后打开监控面板后，就可以看到 EMQX 的监控数据了。

默认的 Dashboard 模板可以在 [EMQX | Grafana Dashboard](https://grafana.com/grafana/dashboards/17446-emqx/) 中下载，也可以在 EMQX Dashboard 的 `监控集成` 配置页面中的帮助页面里，点击 `下载` 按钮下载。

具体的导入步骤如下：

1. 点击左侧的 `Import`，进入导入 Dashboard 的页面；

   ![Import](https://assets.emqx.com/images/1d2d8d109635dc95044eafadc9f58b73.png)

2. 点击 `Upload JSON file`，选择刚才下载的 [Dashboard 模板](https://grafana.com/grafana/dashboards/17446-emqx/) 来导入，或直接输入 https://grafana.com/grafana/dashboards/17446-emqx/ 地址在 `Import via grafana.com` 栏下的输入框中；

   ![Upload JSON file](https://assets.emqx.com/images/bf5be1eea4644e8b94410b9fc7e092a2.png)

3. 点击 `Load`，选择刚才新建的 Prometheus 数据源，点击 `Import`，即可导入 Dashboard 模板。

   ![Dashboard 模板](https://assets.emqx.com/images/3dcc03f304d875ee503d28ecbe24a9da.png)

导入 Dashboard 模板后，就可以在监控面板内看到 EMQX 的监控数据了，如下图所示：

![EMQX MQTT Dashboard](https://assets.emqx.com/images/e8d6c6ed1e0bc0122597edb0528310a8.png)

> **注意**：该模版默认情况下将监控整个 EMQX 集群下的指标数据

以下为该模版中默认显示的指标：

- 常规指标，包括连接数、主题数和订阅数；
- 消息指标，包括发布和接收的消息数量，以及每秒发布和接收的消息数量；
- 系统指标，包括进程数、CPU 和 Erlang VM 内存等（需要使用 Node Exporter）；
- 数据报文指标，包括连接、发布、接收的报文数量等。

您也可以根据默认模版，自定义修改 Dashboard，添加自己需要的指标或修改图表的样式等，具体操作步骤可参考 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/getting-started/)。

## 在 EMQX Dashboard 中轻松配置集成 Prometheus

从 EMQX [5.0.11](https://www.emqx.com/zh/changelogs/broker/5.0.11) 版本起，用户可以在 EMQX Dashboard 中的 `功能配置` -> `监控` -> `监控集成` 页面中，选择 Prometheus，并在该选项下点击「帮助」按钮来获取更多的监控集成操作信息，在指导下更轻松地配置 Prometheus。

您只需要根据帮助页面的步骤提示，安装 Prometheus 和 Grafana 服务，然后在配置项填入一些关键的配置信息，如 EMQX 的地址、获取指标数据的 API 等，点击生成按钮就可自动生成并下载配置文件，还可以下载默认的 Grafana Dashboard 模板。

![下载默认的 Grafana Dashboard 模板](https://assets.emqx.com/images/1e76efb16aa3145ad26d770506609ce8.png)

同样在帮助页面中，可以分为默认和使用 Pushgateway 两种配置方式。使用 Pushgateway 的配置方式，可以在页面中打开启动开关，输入 Pushgateway 的地址和上报数据时间，点击保存后，即可完成配置。

更多关于如何在 Dashboard 中配置集成 Prometheus 的信息，可以参考 [EMQX Dashboard 配置监控集成](https://docs.emqx.com/zh/emqx/v5.0/dashboard/configuration.html#监控)的文档。

## 总结

本文介绍了如何使用 Prometheus 采集 EMQX 的数据指标，并使用 Grafana 对其进行可视化监控。

阅读我们的[指标监控](https://docs.emqx.com/zh/emqx/v5.0/observability/metrics-and-stats.html#metrics-stats)文档，了解更多关于您可以查询到的数据指标。

有关使用该监控系统中的规则和配置告警的更多详细教程文章，敬请关注后续推送。



<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
