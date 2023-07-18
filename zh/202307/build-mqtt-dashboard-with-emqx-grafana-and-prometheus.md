EMQX 是全球领先的开源分布式 [MQTT 消息服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，具有高性能和高可用性。最新版本 EMQX 5.0 已被验证可扩展至 1 亿并发 MQTT 连接，并且是第一个将 [QUIC](https://www.emqx.com/zh/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) 引入 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的 Broker。

> EMQX GitHub: [https://github.com/emqx/emqx](https://github.com/emqx/emqx)   

在本文中，我们将介绍如何构建一个 MQTT Dashboard，来使用 Prometheus 监控 EMQX 5.0 并通过 Grafana 可视化其数据指标。此外，我们还将引入 EMQX Exporter 来导出 Prometheus API 中未包含的指标，它兼容 EMQX 4.4 和 EMQX 5（开源版和企业版）。

## 构建更完善的 MQTT Dashboard

除了内置的 Dashboard 之外，EMQX 还提供 API 将监控数据集成到第三方监控平台。您可以将 EMQX 与第三方监控系统集成，实现以下扩展功能：

- 将 EMQX 的监控与其他相关系统的监控相结合，形成您工作流程的完整视图；
- 使用易于阅读的图表更直观地展示数据，例如使用 Grafana；
- 使用 Prometheus 的 Alertmanager 在出现问题时获取警报。

下图展示了 Prometheus 收集指标数据时的调用流程。

![调用流程](https://assets.emqx.com/images/0ee38e770c26b75115b8f2fb963d7e47.png)

- Prometheus 直接从 EMQX 提供的 API 接口`/api/v5/prometheus/stats`采集基础监控指标。
- Prometheus 从 EMQX Exporter 提供的 API 接口`/metrics`拉取监控指标，此时 EMQX Expoter 会调用 EMQX 的 Dashboard API 获取额外的运行数据并返回给 Prometheus。

## 准备工作

在开始之前，我们需要进行以下步骤：

1. 准备运行环境，安装并运行 EMQX 5.0；
2. 准备 Prometheus 的安装包；
3. 安装并启动 Grafana。

您也可以使用文中提供的下载地址下载安装或二进制包并自行安装。在示例中，我们将使用 Docker 进行安装和激活。

## 部署 EMQX 5.0

使用 Docker 快速安装并启动 EMQX 5.0：

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx:5.0.2
```

除了使用 Docker 安装 EMQX 外，我们还可以使用 RPM 或 DEB 软件包进行安装。具体安装方法请参阅 [EMQX 5.0 Installation Guide](https://www.emqx.io/docs/en/v5.0/deploy/install.html#install)。

安装完成后，我们可以打开`<http://localhost:18083>`访问 EMQX Dashboard 以查看运行状态。

> Dashboard 的默认用户名密码是 **admin/public**

![EMQX Dashboard](https://assets.emqx.com/images/204975e6e5c2d1ec94a8f56df1d77fa9.png)

## 部署 EMQX Exporter

需要安装 EMQX Exporter。该组件用于收集部分未通过 EMQX 的 Prometheus API 接口暴露的运行状态和指标，比如 License、规则引擎、认证、授权等。

EMQX Exporter 使用 basic auth 的方式访问 EMQX Dashboard API，因此我们需要提前登录 Dashboard 并创建一个专门用于指标采集的 [API key](https://www.emqx.io/docs/en/v5.0/dashboard/system.html#api-keys)，然后将 API key 和 secret 作为 EMQX Exporter 的启动参数。

```
docker run -d \
  -p 8085:8085 \
  --name emqx-exporter \
  emqx-exporter:latest \
  --emqx.nodes="${your_eth_addr}:18083"  \
  --emqx.auth-username="${paste_your_new_api_key_here}" \
  --emqx.auth-password="${paste_your_new_secret_here}"
```

> 注意：`emqx.nodes` 参数可以是以逗号间隔的地址列表，EMQX Exporter 会自动选择任意一个可用的  IP 去建立连接。IP 地址必须是有效的容器地址或者物理机地址，不能是 `localhost` 或者 `127.0.0.1`

使用以下命令查看容器日志：

```
docker logs emqx-exporter
```

如果日志中打印出 EMQX 的版本信息则说明 EMQX Exporter 已成功访问到 Dashboard API。

```
ts=2023-05-26T10:50:27.034Z caller=main.go:136 level=info msg="Starting emqx-exporter" version="(version=, branch=, revision=unknown)"
ts=2023-05-26T10:50:27.034Z caller=main.go:137 level=info msg="Build context" build_context="(go=go1.19.3, platform=linux/amd64, user=, date=, tags=unknown)"
ts=2023-05-26T10:50:27.035Z caller=main.go:60 level=info msg="Enabled collectors"
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=authentication
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=authorization
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=cluster
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=license
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=messages
ts=2023-05-26T10:50:27.035Z caller=main.go:67 level=info collector=rule
ts=2023-05-26T10:50:27.035Z caller=tls_config.go:232 level=info msg="Listening on" address=[::]:8085
ts=2023-05-26T10:50:27.035Z caller=tls_config.go:235 level=info msg="TLS is disabled." http2=false address=[::]:8085
ts=2023-05-26T10:50:27.039Z caller=cluster.go:71 level=info ClusterVersion=5.0.2-OpenSource
```

此外，你也可以通过地址`<http://localhost:8085/metrics>`访问到 EMQX 的监控数据。

![Monitoring data](https://assets.emqx.com/images/3a10de5d2eb7c10c55a26bcf74d946b3.png)

## 部署 Node Exporter

如果您想监控物理机或虚拟机的系统信息，则可选。该组件用于收集物理机或虚拟机的系统状态，如CPU、内存、磁盘、网络等。

在本文中，不建议使用 Docker 来安装 Node Exporter。有关 Node Exporter 的安装和使用，请参阅[官方文档](https://prometheus.io/docs/guides/node-exporter/#monitoring-linux-host-metrics-with-the-node-exporter)。安装完成后，如果能通过地址`<http://localhost:9100/metrics>` 访问到监控数据，则表示 Node Exporter 已成功安装。

![Monitoring data](https://assets.emqx.com/images/5a4d6724119da35d8e27fc9041527d76.png)

## 部署 Prometheus

### 准备 Prometheus 配置文件

同样的，我们在示例中将使用 Docker 来快速安装和使用 Prometheus

> Prometheus 是 SoundCloud 开发的开源监控和报警解决方案，支持多维数据模型、灵活的查询语言、强大的报警管理等功能。Grafana 是一款开源数据可视化工具，可以展示包括 Prometheus 在内的多种数据源。

### 配置 Prometheus 的数据采集

Prometheus 使用配置文件的方式指定需要收集数据的目标信息，默认的配置文件路径为`/etc/prometheus/prometheus.yml`。

EMQX 5.0 提供了一个不需要身份认证的 HTTP API 来获取 Prometheus 格式的监控数据。我们只需要在配置文件中将 metrics_path 配置为`/api/v5/prometheus/stats`即可。

为了使用 Node Exporter 获取主机的监控数据，我们还需要将 Node Exporter 服务的地址配置到配置文件中的static_configs中。

在 Prometheus 配置文件中，通过 scrape_configs 指定数据采集目标。以下是完整的 Prometheus 配置文件示例：

> 注意：实际部署时，需要将其中的 target 地址替换成您所部署的服务的 IP 地址。

```
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'emqx'
    metrics_path: /api/v5/prometheus/stats
    scrape_interval: 5s
    honor_labels: true
    static_configs:
      # EMQX IP address and port
      - targets: [${your_eth_addr}:18083]
        labels:
          # user-defined cluster name, requires unique
          cluster: emqx5
          # fix value, don't modify
          from: emqx
  - job_name: 'emqx-exporter'
    metrics_path: /metrics
    scrape_interval: 5s
    static_configs:
      - targets: [${your_eth_addr}:8085]
        labels:
          # user-defined cluster name, should be the same as the cluster name above
          cluster: emqx5
          # fix value, don't modify
          from: exporter
  - job_name: 'node-exporter'
    scrape_interval: 5s
    static_configs:
      # node-exporter IP endpoint
      - targets: [${your_eth_addr}:9100]
        labels:
          instance: dashboard-local
```

在上面的配置文件中，部分配置项的说明如下：

- **job_name** 数据收集的任务名。
- **targets** 目标地址列表
- **cluster** 自定义集群名字，‘emqx' 和 'emqx-exporter' 两个 job 的 cluster 需保持一致，以表示他们属于同一个集群，不同集群的名字需确保唯一性。
- **from** 用于区分指标数据的来源，保持默认，请勿修改。

最后，我们将上述配置文件内容保存为 prometheus.yaml。至此，我们就完成了 Prometheus 的配置。

### 启动 Pormetheus

完成 Prometheus 的配置后，我们就可以使用该文件启动 Prometheus 服务了。如果您使用 Docker 下载了 Prometheus 镜像，则可以使用以下命令启动 Prometheus：

```
docker run -d --name prometheus -p 9090:9090 -v /path/to/your/prometheus.yaml:/etc/prometheus/prometheus.yaml prom/prometheus
```

> 注：将其中的 `/path/to/your/prometheus.yaml` 替换成您实际的文件路径。

容器启动后，便可通过地址 `<http://localhost:9090>` 访问 Prometheus 并查询 EMQX 相关的监控指标。在搜索框中输入`emqx`，如果下拉框中罗列出了相关的指标，则表示 Prometheus 已成功启动并开始收集 EMQX 指标。

![Prometheus MQTT](https://assets.emqx.com/images/1a4a4b2b2b60fc37d21684ca61a42b1f.png)

## 部署 Grafana

下面是使用 Docker 快速安装并启动 Grafana 的方法：

```
docker run -d --name grafana -p 3000:3000 grafana/grafana:9.3.2
```

容器启动后，可通过地址`<http://localhost:3000>`访问 Grafana。

> Grafana 的默认用户名密码是 **admin/admin**

![Grafana](https://assets.emqx.com/images/1214061b7f200e6b134935e0be0801ca.png)

配置完 Prometheus 之后，我们就可以使用 Grafana 对 EMQX 指标进行可视化。登录成功后，我们就可以添加数据源了。

### 添加 Prometheus 数据源

1. 点击左边的“配置”按钮, 选择“Data Sources”，进入数据源配置页面;
2. 点击”Add data source”，选择`Prometheus`;
3. 在`HTTP`配置项中，`URL` 一栏填写 Prometheus 服务的地址，格式为`http://${your_eth_addr}:9090`；
4. 最后，点击`Save & Test`。如果配置正确，当前页面会看到`Data source is working`的提示。

![Add Prometheus as a Data Source](https://assets.emqx.com/images/d527ab1e3677c5d449ec21b1b6994354.png)

### 导入 Dashboard

我们提供了可直接导入到 Grafana 的 Dashboard [模板](https://github.com/emqx/emqx-exporter/tree/main/config/grafana-template)。模板文件按照企业版和开源版，以及4.4版本和5.x版本进行组织，您可以根据自身情况下载需要的版本。本文中我们需要使用到的是 [EMQX5](https://github.com/emqx/emqx-exporter/tree/main/config/grafana-template/EMQX5) 版本。

您可按照如下步骤导入 Dashboard：

![Import Dashboard](https://assets.emqx.com/images/bc895b86daa8406495f0b3f0cfadde54.png)

1. 鼠标悬停在 ”Dashboard” 图标上，选择“import”。如上图
2. 点击“Upload JSON File”，选择刚才我们下载的模板文件。
3. 点击“Import”进行导入。
4. 重复以上步骤导入其他所有模板文件。

所有模板文件都导入完成后，便可以通过主看板 `EMQX`浏览集群的整体状态和指标。通过顶部的下拉菜单“cluster” 在不同的集群之间切换。”cluster” 的定义来自 Prometheus 配置文件中的 label `cluster`。

其他看板则提供了不同的变量以对集群的指标进行筛选查看，这些看板都可以从主看板`EMQX`的相关 panel 中跳转过去。

![MQTT Dashboard](https://assets.emqx.com/images/fa6999cdeaa0603023a6b04577409f25.png)

## 结语

本文介绍了如何在 Docker 环境下使用 Prometheus 收集 EMQX 5.0 的运行状态和指标数据，同时使用 Grafana 进行数据可视化。您可以浏览 [EMQX Exporter](https://github.com/emqx/emqx-exporter) 仓库以了解如何在其他环境中部署并监控 EMQX。

如果您想了解 Grafana 上所展示的指标的说明，可以查看我们的 [README](https://github.com/emqx/emqx-exporter/tree/main/config/grafana-template) 文档。有关定价和其他问题，请随时[联系我们的团队](https://www.emqx.com/zh/contact)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
