## 引言

随着工业生产的持续发展，工厂设备和系统的能源消耗监控变得越来越重要。实时了解各类设备和产线的能耗情况，可以帮助工厂优化能源管理策略，降低成本开支。[EMQX](https://www.emqx.com/zh/products/emqx) 和 [Timescale](https://timescale.com/) 的集成为构建可扩展的物联网平台奠定了基础，能够高效地收集和分析产线上的海量能耗数据，实现智能化和精细化的能源监控。

在本文中，我们将演示如何利用 EMQX 从工厂采集生产设备能耗数据，并与 Timescale 集成，实现数据的实时存储和分析。EMQX 通过 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)能够可靠地从存储系统收集数据，而 Timescale 则提供了高性能的时序数据库。

## 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

![MQTT to Timescale](https://assets.emqx.com/images/b9dccfd771d8dc7b5ba8aecb3ac12808.png)

这是个简单而高效的架构，无需复杂的组件。主要包括以下关键组件：

| 组件名称                                                 | 版本         | 说明                                                         |
| :------------------------------------------------------- | :----------- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+       | 用于模拟生成工厂能耗数据的命令行工具。                       |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.0.4+       | 用于在工厂和 Timescale 之间进行消息传递的 MQTT Broker。      |
| [Timescale](https://www.timescale.com/)                  | latest-pg12+ | 用于工业物联网数据的存储和管理，以及为 Grafana 提供时间维度的聚合和分析功能。 |
| [Grafana](https://grafana.com/)                          | 9.5.1+       | 用于展示和分析采集数据的可视化平台。                         |

除了上述基础组件外，EMQX 还提供了丰富的可观测能力。您可以使用以下组件来监测 EMQX 的运行状态和负载情况：

| 组件名称                                               | 版本    | 说明                               |
| :----------------------------------------------------- | :------ | :--------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | 用于 EMQX 的 Prometheus Exporter。 |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | 开源的系统监测和警报工具包。       |

## 将项目克隆到本地

将 [emqx/mqtt-to-timescaledb](https://github.com/emqx/mqtt-to-timescaledb) 存储库克隆到本地，并初始化子模块以启用 EMQX Exporter（可选）：

```
git clone https://github.com/emqx/mqtt-to-timescaledb
cd mqtt-to-timescaledb

# Optional
git submodule init
git submodule update
```

代码库由四部分组成：

- `emqx` 文件夹包含了 EMQX-Timescale 的集成配置，可以在启动 EMQX 的时候自动创建规则和数据桥。
- `emqx-exporter`、`prometheus` 和 `grafana-provisioning` 文件夹包含了 EMQX 的监测配置以及能耗数据的可视化配置。
- `create-table.sql` 文件定义了数据库的表结构，它会在初始化的过程中在 Timescale 中创建表。
- `docker-compose.yml` 文件可编排所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 Timescale

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose，使用以下命令启动演示：

```
docker-compose up -d
```

下面，MQTTX CLI 将模拟 10 个工厂连接到 EMQX，并以每秒 1 条消息的频率向 EMQX 发送其生产线上各个设备的能耗数据。能耗数据以 JSON 格式发送到主题 `mqttx/simulate/IEM/{clientid}`。

各个设备将采集当前的瞬时用电量（数据是通过随机模拟生成的，但符合设备的最大功率限制），并计算出 1 秒内的能耗，随后将数据发布到 EMQX。

设备与最大功率对照表：

| 设备名称 | 最大功率（千瓦时） |
| :------- | :----------------- |
| 空压机 1 | 15                 |
| 空压机 2 | 20                 |
| 照明设备 | 5                  |
| 冷却设备 | 100                |
| 加热设备 | 200                |
| 传送带   | 50                 |
| 涂装设备 | 20                 |
| 检测设备 | 10                 |
| 焊接设备 | 20                 |
| 包装设备 | 30                 |
| 切割设备 | 70                 |

上报的能耗数据示例：

```
{
    "factory_id": "08",
    "factory": "Miller and Sons",
    "values": {
        "air_compressor_1": 3.72,
        "air_compressor_2": 5.01,
        "lighting": 0.95,
        "cooling_equipment": 23.19,
        "heating_equipment": 52.66,
        "conveyor": 10.66,
        "coating_equipment": 5.21,
        "inspection_equipment": 2.6,
        "welding_equipment": 5.27,
        "packaging_equipment": 7.38,
        "cutting_equipment": 12.56
    },
    "timestamp": 1691144157583
}
```

EMQX 将创建一条规则接收来自每个工厂的消息。您也可以稍后修改这个规则，使用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html)添加自定义处理：

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

规则处理完数据后，EMQX 将通过数据桥接将消息有效载荷中的能耗数据插入到 Timescale 指定的数据表中。在数据桥接上配置 INSERT SQL 可以灵活地实现这个操作。

![Configuring INSERT SQL](https://assets.emqx.com/images/4fa61dcfe7fbc0f8774268d70b53b21a.png)

## 从 EMQX 订阅数据

Docker Compose 包含一个用于打印所有能耗数据的 MQTT 订阅客户端，可以使用以下命令查看消息：

```
$ docker logs -f mqttx
[8/4/2023] [10:15:57 AM] › topic: mqttx/simulate/IEM/mqttx_85df7038
payload: {"factory_id":"08","factory":"Miller and Sons","values":{"air_compressor_1":3.72,"air_compressor_2":5.01,"lighting":0.95,"cooling_equipment":23.19,"heating_equipment":52.66,"conveyor":10.66,"coating_equipment":5.21,"inspection_equipment":2.6,"welding_equipment":5.27,"packaging_equi...
```

您也可以使用任何 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)来订阅和接收已发布的数据，例如：

```
mqttx sub -t mqttx/simulate/IEM/+
```

## 在 Grafana 中查看能耗数据

要通过 Grafana 仪表板中查看和分析实时的能耗数据，可以在浏览器中打开 `http://localhost:3000`，使用用户名 `admin` 和密码 `public` 登录。

登录成功后，进入到 **Home** → **Dashboards** 页面，选择 **Energy Monitoring data**，该仪表板全面展示了各类工业设备的关键能耗监控指标，包括各设备累计能耗数值，各工厂能耗占比情况，充分呈现了工业系统的实时能源使用情况，方便进行数据驱动的节能管理。

![View MQTT Enengy Data in Grafana](https://assets.emqx.com/images/d00a78b068cc7cdfc435a7f99d36306c.png)

## 结语

在本文中，我们探讨了如何集成 EMQX 和 Timescale 来构建工业能源监测系统。通过使用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并利用其 SQL 数据集成功能将数据导入到 Timescale，我们实现了一个端到端的方案，用于收集和分析时序能耗数据。

这个演示项目旨在构建一个可扩展的时序数据平台，用于实现工业设施和其他时间敏感场景的实时监测、优化和智能化分析处理。通过结合 EMQX 的可靠性和 Timescale 的分析能力，我们能够从时序数据中提取有价值的见解。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
