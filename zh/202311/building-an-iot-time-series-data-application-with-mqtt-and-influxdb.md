## 引言

随着太阳能和风能等可再生能源的不断发展，储能成为解决能源输出不稳定问题和实现供需平衡的重要手段。同时，在电动汽车（EV）领域，对电动汽车电池再利用的需求不断增长，也推动了储能市场的繁荣发展。

[EMQX](https://www.emqx.com/zh/products/emqx) 和 InfluxDB 共同构建了一个可扩展的物联网平台，可以高效、实时地采集分布式储能设备的数据。通过对采集的数据进行集中管理和分析，可以支持电力调度和电力交易。本文将详细介绍如何使用 EMQX 将储能设备连接起来，并与 InfluxDB 集成，实现数据的可靠存储和实时分析。

关于利用 EMQX 实现 MQTT 与 InfluxDB、Timesacle 等时序数据库集成的更多内容请查看：[如何将 MQTT 与时序数据库高效应用于物联网场景](https://www.emqx.com/zh/blog/time-series-database-for-iot-the-missing-piece) 

## InfluxDB 简介

InfluxDB 是专为时序数据而设计的数据库，具有高效存储和查询大量时序数据的能力。它以高写入吞吐能力闻名，并提供了灵活的数据保存策略，可在节省存储成本的同时，快速地处理物联网数据的海量写入。此外，InfluxDB 支持类 SQL 的查询语言，可以轻松地对时序数据进行查询和聚合，实现物联网数据的快速分析和监测。这使得它非常适合物联网的应用场景。

目前，EMQX 已经支持连接到各种主流版本的 InfluxDB，包括 InfluxDB Cloud、InfluxDB OSS 以及 InfluxDB Enterprise。

## 准备工作

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

![MQTT to InfluxDB](https://assets.emqx.com/images/2aabbc7e8a0a861e03881f9e4ec85002.png)

这是个简单而高效的架构，无需复杂的组件。主要包括以下几个关键组件：

| 组件名称                                                 | 版本   | 说明                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+ | 用于模拟生成能源数据的命令行工具。                           |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.0.4+ | 用于在储能设备和 InfluxDB 之间进行消息传递的 MQTT Broker。   |
| [InfluxDB](https://influxdata.com/)                      | 2.0.0+ | 用于能源数据的存储和管理，以及为 Grafana 提供时间维度的聚合和分析功能。 |
| [Grafana](https://grafana.com/)                          | 9.5.1+ | 用于展示和分析采集数据的可视化平台。                         |

除了上述基础组件外，EMQX 还提供了丰富的可观测能力。您可以使用以下组件来监测 EMQX 的运行状态和负载情况：

| 组件名称                                               | 版本   | 说明                               |
| :----------------------------------------------------- | :----- | :--------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1    | 用于 EMQX 的 Prometheus Exporter。 |
| [Prometheus](https://prometheus.io/)                   | 2.44.0 | 开源的系统监测和警报工具包。       |

## 下载示例项目至本地

使用 Git 将[示例项目代码](https://github.com/emqx/mqtt-to-influxdb)下载到本地，并初始化子模块以启用 EMQX Exporter（可选）：

```
git clone https://github.com/emqx/mqtt-to-influxdb
cd mqtt-to-influxdb

# Optional
git submodule init
git submodule update
```

代码库由四部分组成：

- `emqx` 文件夹包含了 EMQX-InfluxDB 的集成配置，可以在启动 EMQX 的时候自动创建规则和数据桥接。
- `mqttx` 文件夹包含一个模拟脚本，用于模拟连接到 EMQX 并生成数据的储能设备。
- `emqx-exporter`、`prometheus` 和 `grafana-provisioning` 文件夹包含了 EMQX 的监测配置以及能耗数据的可视化配置。
- `docker-compose.yml` 文件可编排所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 InfluxDB

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose，开始演示：

```
docker-compose up -d
```

现在，MQTTX CLI 将模拟 10 个储能设备接入 EMQX，并定期向特定主题发布设备的能源生成和消耗情况。能源数据以 JSON 格式发送到主题 `mqttx/simulate/Energy-Storage/{clientid}`。

模拟器真实地模拟了现实世界的场景，它从当前时刻的 24 小时前开始运行。每个储能设备都有各自不同的初始电量。电量的产生和消耗在一天中不断波动，因此储能单元不断充电和放电。电池的温度和电压是反映储能系统运行状况的重要指标。

下面是一个具体储能设备发布到 EMQX 的数据示例：

```
{
    "id": "87780204-890a-4b9a-b271-b0cf719ca62f",
    "name": "Energy_Storage_0",
    "type": "FX48-B2800",
    "inputPower": 0.01,
    "outputPower": 136.98,
    "percentage": 100.01,
    "remainingCapacity": 2799.62,
    "timestamp": 1696721283913,
    "temperature": 19.48,
    "voltage": 1230.59,
    "battery": [
        {
            "id": "ec6fd356-2862-44a1-899b-80410890ecf6",
            "name": "Battery_1",
            "voltage": 1230.6,
            "temperature": 19.15,
            "percentage": 100.01,
            "inputPower": 0.01,
            "outputPower": 45.66
        },
        {
            "id": "f07a09de-43a0-4306-8997-a96fd583d76d",
            "name": "Battery_2",
            "voltage": 1230.6,
            "temperature": 19.95,
            "percentage": 100.01,
            "inputPower": 0.01,
            "outputPower": 45.66
        },
        {
            "id": "70e5a888-186b-4ef2-b122-a63ba6c1499b",
            "name": "Battery_3",
            "voltage": 1230.57,
            "temperature": 19.34,
            "percentage": 99.99,
            "inputPower": 0.01,
            "outputPower": 45.66
        }
    ],
    "deltaCapacity": -0.38
}
```

EMQX 将创建一条规则，用于接收储能设备发送的消息。您也可以在之后修改这条规则，利用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html)进行自定义处理。

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

规则处理完数据后，EMQX 将通过数据桥接把消息有效载荷中的能源数据写入到 InfluxDB 的 `iot_data` 存储桶中。

## 从 EMQX 订阅数据

Docker Compose 包含一个用于打印所有能源数据的订阅者。可以使用以下命令查看数据：

```
$ docker logs -f mqttx
[9/24/2023] [10:15:57 AM] › topic: mqttx/simulate/Energy-Storage/mqttx_6d014c26
payload: {"id":"87780204-890a-4b9a-b271-b0cf719ca62f","name":"Energy_Storage_0","type":"FX48-B2800","inputPower":2.41,"outputPower":539.24,"percentage":94.68,"remainingCapacity":2649.52,"timestamp"...
```

使用任何 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)都可以订阅和接收数据：

```
mqttx sub -t mqttx/simulate/IEM/+
```

## 在 Grafana 中查看能源数据

要在 Grafana 仪表板中查看能源数据，请在浏览器中打开 `http://localhost:3000`，使用用户名 `admin` 和密码 `public` 登录。

登录成功后，进入 `Home → Dashboards` 页面，选择 `EMQX Energy Storage`。该仪表板展示了储能设备状态的全面概况，包括当前的储电量、输入和输出功率，以及这些指标在不同时间段的变化趋势。通过这些关键指标，您可以直观地监测储能设备的运行状况，及时发现并解决问题，并根据实时数据制定合理的能源调度方案。仪表板中丰富的可视化功能使得数据分析和决策制定更加高效和直观。

![View Enengy Data in Grafana](https://assets.emqx.com/images/486833a1a4142053e77e6d577a401e07.png)

## 结语

在本文中，我们探讨了如何集成 EMQX 和 InfluxDB 来构建能源存储应用。通过使用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并将数据导入到 InfluxDB，我们实现了一个端到端的解决方案，用于收集和分析时序能源数据。

这个演示项目提供了一个示范，旨在构建可扩展的时序数据平台，以实现能源存储和其他时间敏感场景的实时监测、优化和智能化。借助 EMQX 的可靠性和 InfluxDB 的分析能力，我们能够从时序数据中提取有价值的见解。

欢迎访问 [GitHub](https://github.com/emqx/emqx/mqtt-to-influxdb)，查看将时序数据导入 InfluxDB 的详细演示。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
