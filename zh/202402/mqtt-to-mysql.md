## 引言

在石油石化行业中，实时监控石油管道和环境安全参数对于保障石油开采生产安全和效率至关重要。

企业级 MQTT 物联网接入平台 EMQX 能够实现对各种 IoT 传感器数据的采集，帮助监控压力、流速和温度等管道参数，并将异常情况都及时上报。MySQL 数据库则可以提供数据的存储和分析能力，满足实时监控和历史数据分析的需求。

EMQX 与 MySQL 的集成可以帮助企业实时监控石油管道和环境的状态，及时发现和处理异常情况，从而保障生产安全，提高生产效率，推动石油石化行业数字化转型升级。

本文将演示如何利用 EMQX 采集石油管道各类传感器数据，并与 MySQL 集成，实现数据的实时存储和分析。

## MySQL 在物联网领域的应用

MySQL 具有以下独特优势：

- **结构化数据存储**：MySQL 中的数据以表格形式存储，需要预先定义表结构和字段数据类型，这种结构化的数据存储方式有助于保证数据的一致性和完整性。
- **强大的查询语言**：MySQL 支持标准的 SQL 查询语言，提供了丰富的查询操作，包括过滤、排序、联接、聚合等。
- **扩展性和可用性**：MySQL 支持主从复制和分片，可以实现数据的高可用性和水平扩展。
- **事务处理**：MySQL 支持 ACID 事务，可以保证在并发操作和系统故障的情况下数据的一致性和可靠性。

我们可以发现 MySQL 的结构化数据存储能力和强大的查询语言使其在处理大规模结构化数据和执行复杂数据查询方面具有显著优势。然而对于遥测数据来说，它们通常通常被归类非结构化数据，其特性包括数据操作的简单性、数据之间关系的直接性，以及数据量的庞大。这些数据需要高速的写入吞吐量以及长期的存储能力。在这种情况下，MySQL 可能并不是最佳的选择。

因此，在物联网应用中，MySQL 更适合存储设备的元数据、事件数据以及少量的遥测数据，如设备配置、在线离线状态以及当前传感器读数等。这些数据的存储与使用也是物联网应用中必不可少的一部分，除了一部分特定的应用场景外，还支撑了整个应用的运行管理管理。

## 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

![架构图](https://assets.emqx.com/images/4c20c7a15d465298cb5ad19162aa3d5e.png)

这是个简单而高效的架构，无需复杂的组件。主要包括以下关键组件：

| 组件名称                                                 | 版本   | 说明                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.4+ | 用于模拟生成石油采集设备数据的命令行工具。                   |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.4.1+ | 用于在石油管道现场和 MySQL 之间进行消息传递的 MQTT Broker。  |
| [MongoDB](https://mongodb.com/)                          | 8.0.0+ | 石油开采物联网数据存储和管理，以及为 Grafana 提供时间聚合和分析功能。 |
| [Grafana](https://grafana.com/)                          | 9.5.1+ | 用于展示和分析采集数据的可视化平台。                         |

## 下载示例项目到本地

使用 Git 将 [emqx/mqtt-to-mysql](https://github.com/emqx/mqtt-to-mysql) 存储库代码下载到本地：

```shell
git clone https://github.com/emqx/mqtt-to-mysql
cd mqtt-to-mysql
```

代码库由四部分组成：

- `emqx` 文件夹包含了 EMQX-MySQL 数据集成配置，可以在启动 EMQX 的时候自动创建规则和动作。
- `mqttx` 文件夹包含一个模拟脚本，用于模拟连接到 EMQX 并生成数据的石油管道传感器设备。
- `prometheus` 和 `grafana-provisioning` 文件夹包含了能耗检测可视化配置。
- `docker-compose.yml` 文件可编排所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 MySQL

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose，开始演示：

```shell
docker-compose up -d
```

现在，MQTTX CLI 将模拟 10 组采集设备接入 EMQX，并定期向特定主题发布管道的油压、套压、背压、井口温度、产量等实时数据。采集的数据以 JSON 格式发送到主题 `mqttx/simulate/oil-extraction/{clientid}`。

下面是一个具体采集设备发布到 EMQX 的数据示例：

```json
{
    "oilPressure": 1375829.01,
    "casingPressure": 429647.68,
    "backPressure": 142174.65,
    "wellheadTemperature": 75.03,
    "voltage": 360.84,
    "current": 29.4,
    "flowRate": 127.8,
    "id": "2eb9b000-c6a1-4af1-92c0-6e3026e2db92",
    "name": "oil_well_0"
}
```

### 石油管道数据存储

EMQX 将创建一条规则，用于接收采集设备发送的消息。您也可以在之后修改这条规则，利用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html)进行自定义处理。

```sql
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

规则处理完数据后，EMQX 将通过规则动作把消息有效载荷中的石油管道传感器数据写入到 MySQL 的 `iot_data` 数据库 `oil_well_data` 表中。

EMQX MySQL 数据集成支持通过 SQL 模板插入数据，可以方便地将特定字段的数据写入或更新到 MySQL 数据库的对应表和列中，实现数据的灵活存储和管理：

```sql
INSERT INTO oil_well_data
  (
    oil_well_id,
    NAME,
    oilpressure,
    casingpressure,
    backpressure,
    wellheadtemperature,
    voltage,
    CURRENT,
    flowrate
  )
  VALUES
  (
    ${payload.id},
    ${payload.name},
    ${payload.oilPressure},
    ${payload.casingPressure},
    ${payload.backPressure},
    ${payload.wellheadTemperature},
    ${payload.voltage},
    ${payload.current},
    ${payload.flowRate}
  )
```

### 采集设备事件记录

除此之外，EMQX 还将创建一条规则，用于将记录连接到 EMQX 的采集设备的上下线状态，以便进行设备管理和故障预警。这种情况下，如果设备突然下线，我们可以立即得知，从而快速定位问题并进行处理。

EMQX 规则引擎支持完整的 MQTT 设备生命周期事件处理，您也可以参考[此处](https://docs.emqx.com/zh/enterprise/v5.4/data-integration/rule-sql-events-and-fields.html#客户端事件)通过规则引擎监控更多事件。

```sql
SELECT
  *
FROM
  "$events/client_connected",  "$events/client_disconnected"
```

设备连接成功与断开连接时，EMQX 将触发规则并把事件记录到 MySQL 的 `iot_data` 数据库 `oil_well_events` 表中。

记录包括事件名称与客户端 ID，事件发生时间则由 MySQL 自动生成：

```sql
INSERT INTO oil_well_events(event, clientid) VALUES(${event}, ${clientid})
```

## 从 EMQX 订阅数据

Docker Compose 包含一个用于打印所有传感器数据的订阅者。可以使用以下命令查看数据：

```shell
$ docker logs -f mqttx
[1/12/2024] [10:15:57 AM] › topic: mqttx/simulate/oil-extraction/mqttx_4f113a38
payload: "oilPressure":1375829.01,"casingPressure":429647.68,"backPressure":142174.65,"wellheadTemperature":75.03,"voltage":360.84,"current":29.4,"flowRate":127.8,"id":"2eb9b000-c6a1-4af1-92c0-6e3026e2db92","name":"oil_well_0"}
```

使用任何 [MQTT 客户端](https://www.emqx.com/en/blog/mqtt-client-tools)都可以订阅和接收数据：

```shell
mqttx sub -t mqttx/simulate/oil-extraction/+
```

## 在 Grafana 中查看管道数据

要在 Grafana 仪表板中查看管道数据，请在浏览器中打开 `http://localhost:3000`，使用用户名 `admin` 和密码 `public` 登录。

登录成功后，进入 `Home → Dashboards` 页面，选择 `Oil Extraction`。该仪表板展示了石油管道的全面概况，包括当前的油压、套压、背压、井口温度等指标，以及这些指标在不同时间段的变化趋势。通过这些关键指标，您可以直观地监测石油管道的生产状况，并及时发现任何可能的异常或问题。

![在 Grafana 中查看管道数据](https://assets.emqx.com/images/71f9068bffc355cc8391f527b00d2aa5.png)

## 结语

在本文中，我们探讨了如何集成 EMQX 和 MySQL 来构建是有开采状态监控应用。通过使用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并将数据导入到 MySQL，我们实现了一个端到端的解决方案，用于收集和分析石油开采生产数据。

这个演示项目为构建可扩展的石油石化数据监控平台提供了一个范例，可以实现生产数据和以及设备状态的实时监测。借助 EMQX 的可靠性和 MySQL 的存储分析能力，我们能够通过数据驱动分析和主动维护产线，提高运营效率，最大限度地减少停机时间，并增强安全性。

在石油石化行业，围绕数据采集、边缘计算、 EMQX 云端接入以及 AI 技术，EMQ 提供了一整套的解决方案，将来自油井、边缘网关和云应用程序的数据整合到统一的平台上，实现对生产、维护、安全和环境监测以及资产跟踪等场景的支持，利用统一的 MQTT 和云边数据平台助力石油石化行业数字化转型升级。更多方案详情请参考 [EMQ 石油石化行业实时数据采集解决方案](https://www.emqx.com/zh/solutions/industries/oil-gas)。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
