## 引言

在当前的物联网时代，联网设备在智能家居、自动驾驶汽车和自动化工厂等领域日益普及。这些设备持续产生大量的数据，通常以消息和事件的形式呈现。为了保障这些设备的稳定性和安全性，收集、存储和分析这些数据变得至关重要。在本文中，我们将展示如何通过将 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 与 PostgreSQL 集成，实现设备数据的高效存储。

## PostgreSQL 简介

PostgreSQL，或简称 Postgres，是一个功能强大的开源关系数据库管理系统，以其高度可靠、可扩展及丰富的高级功能而广受欢迎。它在处理复杂查询和多种数据类型方面表现优异，因此成为从小型项目到企业级系统等各种应用的理想选择。PostgreSQL 支持多种数据类型，包括 JSON 和 XML，且具备 ACID 合规性、事务处理以及多版本并发控制（MVCC）等功能，确保了数据的完整性和一致性。此外，PostgreSQL 提供了用户自定义函数、触发器和扩展等高级功能，允许用户根据特定需求定制数据库。凭借其卓越的性能、可扩展性和灵活性，PostgreSQL 被广泛应用于各个行业，成为用途广泛且功能丰富的数据库系统。

## MQTT + PostgreSQL 在物联网领域的优势

在物联网应用中，将 MQTT 与 PostgreSQL 集成可带来多种显著优势，包括：

1. **高效数据传输**：MQTT 是一种专为低带宽、高延迟网络设计的轻量级、高效消息传输协议。将 MQTT 与 PostgreSQL 集成后，可以高效、可靠地将物联网数据传输到数据库中。
2. **实时数据处理**：MQTT 支持实时数据传输，允许物联网设备即时发布和订阅数据流。通过与 PostgreSQL 的集成，能够实时处理和存储这些数据，从而实现即时洞察与快速决策。
3. **数据持久性**：PostgreSQL 是一个功能强大且可靠的开源关系数据库管理系统。通过将 MQTT 与 PostgreSQL 集成，可以确保数据的持久性和稳定性，使物联网数据能够安全存储，以备未来分析和参考之用。
4. **数据分析与洞察**：在 PostgreSQL 中存储物联网数据后，可以利用其强大的查询与分析功能，从数据中提取有价值的见解。与 PostgreSQL 集成能够让用户执行复杂数据分析、生成报告并实现数据可视化，从而帮助用户做出明智的业务决策。
5. **数据安全性**：PostgreSQL 提供高级安全功能，包括基于角色的访问控制、数据加密和身份验证机制。将 MQTT 与 PostgreSQL 集成，能够保障物联网数据的安全性和完整性，有效防止未经授权的访问或数据篡改。
6. **简化开发流程**：将 MQTT 与 PostgreSQL 集成，可以简化物联网应用的开发过程。开发者能够利用 PostgreSQL 的灵活性与可扩展性，以及 MQTT 的轻量级消息传输功能，构建出稳健且高效的物联网解决方案。

总之，将 MQTT 与 PostgreSQL 集成为物联网应用提供了实时数据处理、可扩展性、数据持久性、强大分析功能、安全性以及简化开发流程的强大组合，是需要高效数据管理和分析的物联网项目的理想选择。

## 使用 EMQX 实现 MQTT 与 PostgreSQL 的集成

EMQX 是一款专为物联网和实时消息传输设计的高度可扩展且功能强大的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。EMQX 支持与 PostgreSQL 的无缝集成，使得物联网设备生成的实时数据流能够得到简化管理。通过这种集成，企业可以实现海量数据的存储、精确的查询执行以及复杂的数据关联分析，同时保持数据的完整性。EMQX 的高效消息路由功能与 PostgreSQL 的灵活数据模型相结合，能够轻松实现设备状态监控、事件跟踪和操作审计。这种协同作用为企业提供了深刻的数据洞察能力和强大的商业智能支持，帮助企业做出明智决策，实现卓越运营。

EMQX 的 PostgreSQL 数据集成功能旨在轻松连接基于 MQTT 的物联网数据与 PostgreSQL 的强大数据存储能力。通过内置的规则引擎，将数据从 EMQX 传输到 PostgreSQL 的过程变得非常简单，无需复杂的编码。

下图展示了 EMQX 和 PostgreSQL 之间数据集成的典型架构：

![EMQX 和 PostgreSQL 之间数据集成架构](https://assets.emqx.com/images/782e39ce6d281051c520f6b67433ee42.png)

将 MQTT 数据传输到 PostgreSQL 的工作流程如下：

- **物联网设备连接到 EMQX**：物联网设备通过 MQTT 协议连接到 EMQX 后，会触发上线事件，该事件包含设备 ID、源 IP 地址等信息。
- **消息发布与接收**：设备向指定的主题发布遥测和状态数据。EMQX 接收这些数据后，在其规则引擎中启动匹配流程。
- **规则引擎处理消息**：内置规则引擎根据主题匹配处理来自特定来源的消息和事件。规则引擎会匹配相应的规则并处理消息和事件，如数据格式转换、消息过滤或增加上下文信息。
- **写入 PostgreSQL**：规则引擎触发写入操作，将处理后的消息数据写入 PostgreSQL。通过 SQL 模板，用户可以从规则引擎处理的结果中提取数据构建 SQL 语句，并将其发送到 PostgreSQL 执行，从而将数据写入或更新到数据库的特定表和列中。

在事件和消息数据写入 PostgreSQL 后，开发者可以通过以下方式灵活应用这些数据：

- 连接 Grafana 等可视化工具，根据数据生成图表，展示数据变化趋势。
- 连接设备管理系统，查看设备列表和状态，检测异常设备行为，并及时消除潜在隐患。

## MQTT 与 PostgreSQL 集成演示

在本节中，我们将向您展示如何使用 EMQX 收集车辆的实时位置数据，并将这些数据与 PostgreSQL 无缝集成，实现存储和分析。

### 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### 工作原理

这是个简单而高效的架构，主要包括以下几个关键组件：

| 组件名称                                                 | 版本   | 描述                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/zh/cli)                    | 1.9.3+ | 用于生成测试数据的命令行工具。                               |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.6.0+ | 负责在车辆与 PostgreSQL 之间进行消息交换。                   |
| [PostgreSQL](https://www.postgresql.org/)                | 13+    | 存储和管理车辆数据，并为 Grafana 提供时间聚合和分析功能的数据库。 |
| [Grafana](https://grafana.com/)                          | 9.5.1+ | 用于可视化和分析所收集数据的展示平台。                       |

### 下载示例项目到本地

首先，使用 Git 将 [emqx/mqtt-to-postgres](https://github.com/emqx/mqtt-to-postgres) 存储库代码下载到本地：

```shell
git clone https://github.com/emqx/mqtt-to-postgres 
cd mqtt-to-postgres
tree
```

项目目录结构如下：

```shell
├── LICENSE
├── README.md
├── docker-compose.yml
├── emqx
│   ├── api_secret
│   └── cluster.hocon
├── emqx-exporter
│   └── config
│       └── grafana-template
│           └── EMQX5-enterprise
├── grafana-dashboards
│   └── vehicle-location.json
├── grafana-provisioning
│   ├── dashboard.yaml
│   └── datasource.yaml
├── image
│   ├── mqtt-to-postgres.png
│   └── vehicle_location.png
├── mqttx
│   └── vehicle-location.js
└── postgres
    └── create-table.sql

11 个目录，12 个文件
```

代码库由以下四个部分组成：

- `emqx` 文件夹：包含 EMQX 与 PostgreSQL 集成的配置，用于启动 EMQX 时自动创建连接器、规则和操作。
- `mqttx` 文件夹：包含一个脚本，用于模拟连接到 EMQX 的车辆传感器并生成数据。
- `grafana-provisioning` 文件夹：提供可视化车辆位置数据的配置文件。
- `docker-compose.yml`：用于协调项目的所有组件，实现一键部署。

### 启动 MQTTX CLI、EMQX 和 PostgreSQL

在开始之前，请确保已经安装了 [Docker](https://www.docker.com/)。然后，通过后台运行 Docker Compose 启动演示环境：

```shell
docker-compose up -d
```

在本演示中，MQTTX CLI 将模拟 5 个车辆客户端，这些客户端会主动向指定的主题发布车辆的识别码（VIN）和位置坐标（经纬度）等实时数据。数据将以 JSON 格式定时发送到主题`mqttx/simulate/vehicle-location/{clientid}`，展示了车辆与系统之间的无缝信息流。

以下是向 EMQX 发布数据的示例：

```json
{
  "vin":"1NXBR32E57Z812344",
  "latitude":42.3922,
  "longitude":42.303
}
```

### 存储车辆位置数据

EMQX 将为从客户端接收到的消息创建一条规则。您也可以在之后修改这条规则，利用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html)进行自定义处理。

```sql
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

规则处理完数据后，EMQX 将利用规则操作将消息有效载荷中的车辆位置数据写入 PostgreSQL 的 `vehicle_db` 数据库中的 `vehicle_data` 表。

通过 EMQX 的 PostgreSQL 数据集成功能，可以使用 SQL 模板轻松地将特定字段数据插入或更新到 PostgreSQL 数据库中的相应表和列中，从而实现灵活的数据存储和管理：

```sql
insert into vehicle_location_data(vin, latitude, longitude)
values (${payload.vin}, ${payload.latitude}, ${payload.longitude})
```

### 记录客户端事件

此外，EMQX 还将创建一条规则，用于记录连接到 EMQX 的客户端的上线和离线状态。这些日志记录可用于设备管理和故障预警。如果客户端意外断开连接，系统可以立即发出通知，确保问题得到及时处理。

EMQX 的规则引擎支持完整的 MQTT 设备生命周期事件处理。您可以参考[相关文档](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-events-and-fields.html#mqtt-events)来全面了解和监控各种事件。

```sql
SELECT
  *
FROM
  "$events/client_connected",  "$events/client_disconnected"
```

当客户端成功连接或断开连接时，EMQX 会触发规则，并将事件记录在 PostgreSQL 的 `vehicle_db` 数据库中的 `vehicle_events` 表中。

记录的信息包括事件名称、客户端 ID，以及由 PostgreSQL 自动生成的事件时间：

```sql
insert into vehicle_events(clientid, event) values (${clientid},${event})
```

### 从 EMQX 订阅数据

Docker Compose 包含一个用于打印所有车辆位置数据的订阅者。可以使用以下命令查看数据：

```shell
docker logs -f mqttx
[5/14/2024] [6:24:52 AM] › …  Connecting...
[5/14/2024] [6:24:52 AM] › ✔  Connected
[5/14/2024] [6:24:52 AM] › …  Subscribing to mqttx/simulate/#...
[5/14/2024] [6:24:52 AM] › ✔  Subscribed to mqttx/simulate/#
[5/14/2024] [6:24:53 AM] › topic: mqttx/simulate/vehicle-location/1NXBR32E57Z812341
payload: {"vin":"1NXBR32E57Z812341","latitude":-79.3737,"longitude":-143.3323}
```

您可以使用任何 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)订阅和接收数据：

```shell
mqttx sub -t mqttx/simulate/vehicle-location/+
```

### 在 Grafana 查看车辆位置数据

要在 Grafana 仪表板中查看车辆位置数据，请在浏览器中打开 `http://localhost:3000`，使用用户名 `admin` 和密码 `public` 登录。

登录成功后，点击主页导航栏中的 Dashboards 页面。然后，选择“EMQX Data Integration Demo - Vehicle Location”。该 Dashboard 将展示 PostgreSQL 中存储的车辆位置数据，包括首辆车的当前经纬度，以及车辆历史位置的地图视图。此外，您还能以表格形式查看所有车辆的连接和断开事件。

通过这些视图，您可以直观地监控车辆的当前位置，在地图上追踪其历史移动路线，并以清晰有序的方式实时监控所有车辆的连接状态。

![Grafana](https://assets.emqx.com/images/3588d02d28352b6c40ac38504a8fa9ee.png)

## 结语

在本文中，我们详细介绍了如何将 MQTT 和 PostgreSQL 整合，用于开发车辆位置监控应用程序。通过使用 EMQX 作为实时 MQTT Broker，将数据无缝导入 PostgreSQL，您可以通过数据驱动的分析来提升运营效率，减少停工时间，并增强安全性。这种集成能够实现实时数据处理和分析，帮助您在车辆监控中做出更加明智的决策，并制定预防性维护策略。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
