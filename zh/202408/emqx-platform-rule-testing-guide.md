自 5.7.0 版本起，EMQX 支持了 SQL 调试，并支持在数据集成全流程中进行规则调试，使用户能够在开发阶段就全面验证和优化规则，确保它们在生产环境中的稳定高效运行。

> 点击此处下载 EMQX 最新版本：[https://www.emqx.com/zh/try?tab=self-managed](https://www.emqx.com/zh/try?tab=self-managed)

本文将为您提供 EMQX 数据集成规则的调试指南，通过调试步骤的详细介绍，帮助您充分了解并利用这一强大的功能。

## EMQX 规则引擎介绍

EMQX 规则引擎是一个基于 SQL 的数据处理组件，借助数据集成，用户无需编写代码即可完成物联网数据的提取、过滤、转换、存储和处理任务。

![EMQX 规则引擎原理图](https://assets.emqx.com/images/bc44ca29c18063ca5dca8d90f1cd51c0.png)

**规则引擎的工作原理**：

- **数据源**：通过 SQL 中的 FROM 子句指定。
- **数据处理**：通过 SQL 语句和函数进行描述。
- **结果输出**：通过动作来处理输出结果，比如将其存储到数据库或重新发布到 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)中。

**关键动作**：

- 将消息重新发布到 MQTT 主题
- 输出到控制台
- 发送到外部数据系统，如 Kafka、MySQL、PostgreSQL 等。

本指南将重点介绍如何在 EMQX 数据集成中调试这些规则，以确保它们在生产环境中能够按预期工作。

## 为什么需要规则测试？

目前，在 EMQX 中创建直接可用的规则可能会面临一些挑战，主要体现在以下几个限制：

- **仅限于 SQL 测试**：当前只能通过模拟数据输入来测试 SQL，这虽然有助于用户调整 SQL 语法以实现目标，但无法全面验证规则的整体效果。
- **动作测试**：动作只能在 Sink 资源的生产环境中观察，限制了提前充分测试和验证动作的可能性。每次调整都需要切换不同的系统来检查结果，增加了操作的复杂性。
- **模拟数据限制**：模拟数据通常有限，难以全面反映 MQTT 属性和事件的真实情况，导致测试结果可能无法覆盖所有用户场景。

通过仪表板提供全面反馈并跟踪整个数据集成生命周期中的日志，规则测试可以有效解决上述限制，帮助用户更好地识别和解决问题。规则测试的主要优势包括：

- **端到端验证**：可以使用真实的数据源和动作进行测试，确保从输入到输出的每个数据流环节都按预期运行。
- **更好的问题检测**：在开发和规则编辑阶段，用户界面提供了直观的工具，帮助快速识别和解决潜在问题，从而减少生产环境中的故障发生率。
- **提高开发效率**：测试功能能够缩短开发和测试周期，使规则的部署更加高效。
- **保障系统稳定性**：通过预先测试和验证规则，降低了生产环境中出现未预见问题的风险。

## 规则测试功能使用教程

### 安装 EMQX Enterprise

**推荐下载**：[**EMQX Enterprise**](https://www.emqx.com/zh/try?tab=self-managed) - 此版本提供丰富的数据集成功能，支持 Kafka、RabbitMQ、MySQL、PostgreSQL、InfluxDB、TimescaleDB 等常用的关系型数据库、时序数据库和流处理中间件。

您也可以使用以下 Docker 命令安装：

```shell
docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.7.1
```

安装完成后，在浏览器中打开 `<http://<your-host-address>>:18083`，输入默认的用户名和密码即可登录 Dashboard。

登录后，依次点击**数据集成** → **规则** → **创建**，进入规则引擎创建页面。页面的上半部分用于配置 SQL、数据源和 Sink，而下半部分则是进行规则测试的区域。接下来，我们将通过两个简单的例子演示如何创建和启用规则测试。

![EMQX Dashboard](https://assets.emqx.com/images/2b02ea3b95a1e04c353fd66e3415b29c.png)

### 创建规则

在完成 EMQX 安装后，我们通过一个具体示例来展示规则引擎的使用。该场景模拟车辆数据上报，并在车速超过 120 公里/小时时，将相关数据（包括速度和地理位置）发布到 HTTP 服务。车辆的 ID 和 MQTT 连接信息将存储在 PostgreSQL 数据库中。

- **模拟 MQTT 有效载荷进行测试**：首先，模拟一条 MQTT 有效载荷来模拟车辆数据上报。

  ```json
  {
    "vehicle_id": "VH-958-XYZ",
    "speed": 72,
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "safety_features": {
      "airbag_deployed": false,
      "abs_status": "active"
    },
    "timestamp": "2024-07-11T15:45:00Z"
  }
  ```

- **创建 SQL 规则**：在 SQL 编辑器中创建规则，监听 `devices/#` 主题，并设置条件为车速超过 120 公里/小时时触发。

  ```sql
  SELECT
    username,
    clientid,
    payload.vehicle_id as vehicle_id,
    payload.speed as speed,
    payload.location.latitude as latitude,
    payload.location.longitude as longitude,
    payload.safety_features.airbag_deployed as airbag_deployed,
    payload.safety_features.abs_status as abs_status,
    timestamp
  FROM
    "devices/#"
  WHERE payload.speed > '120'
  ```

- **测试和调试 SQL**：编写完 SQL 后，在 SQL 选项卡中点击“开始测试”按钮，调试 SQL 语法。您可以输入模拟数据进行测试，调整和优化 SQL 语句。关于编写 SQL 的详细指南，请参考 [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/data-integration/rule-sql-syntax.html)。测试完成后，我们将设置 HTTP 和 PostgreSQL 环境，为该规则添加两个动作。

### 设置 HTTP 服务

首先，我们使用 Node.js 创建一个简单的 HTTP 服务，用于接收和显示来自 EMQX 的数据。

```javascript
const express = require("express");
const app = express();
app.use(express.json());

app.post("/speed", (req, res) => {
  const { speed, latitude, longitude } = req.body;
  console.log(`Received data: Speed is ${speed} km/h at coordinates (${latitude}, ${longitude}).`);
  res.status(200. send("Data received successfully!");
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
```

在规则创建页面中，选择添加动作，创建 HTTP 连接器，并配置 HTTP 请求主体，将从 SQL 提取的数据发送到上述 HTTP 服务。

![编辑动作](https://assets.emqx.com/images/797fa6aa566f30f27a837dd7d156424b.png)

### 配置 PostgreSQL 数据库

接下来，我们使用 Docker 快速部署 PostgreSQL 数据库，并使用 Postico 或其他 GUI 客户端管理数据库。

```
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_DB: emqx
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: public
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
```

部署完成后，我们需要创建数据库表，然后添加动作，以便将数据存储到数据库中。

```sql
CREATE TABLE car_infos (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  clientid VARCHAR(255),
  timestamp TIMESTAMP,
  vehicle_id VARCHAR(255),
  speed INT
);
```

数据库表创建完成后，回到规则创建页面中，再次点击添加动作，创建 PostgreSQL 连接器。使用该连接器创建一个动作，并在 SQL 模板中输入如下的 INSERT 语句，以确保当规则触发时，过滤后的数据能够保存到数据库中：

```sql
INSERT INTO car_infos (
  username,
  clientid,
  timestamp,
  vehicle_id,
  speed
) VALUES (
  ${username},
  ${clientid},
  TO_TIMESTAMP(${timestamp}::bigint / 1000),
  ${vehicle_id},
  ${speed}
);
```

![编辑动作](https://assets.emqx.com/images/c9cb2324356a073c8b3a2428f849634b.png)

### 开始测试

> **注意**：在开始测试之前，请务必保存规则。

首先，导航到“规则”选项卡并单击“开始测试”按钮。请确保已经使用页面底部的保存按钮保存了 SQL 规则。保存规则非常重要，只有保存后才能实现测试的端到端跟踪。

对于不使用 MQTT 客户端的用户，可以通过测试界面右侧面板输入模拟测试数据。这种方法虽然能够进行模拟测试，但由于可能存在配置限制，无法完全再现真实场景。

我们建议使用 [MQTTX](https://mqttx.app/zh) 模拟测试数据。连接到当前的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并将真实数据发送到主题 `devices/1`。

![MQTTX](https://assets.emqx.com/images/b9c875a234ca8a51000c1ae954721e39.png)

如果规则未触发（例如，`speed` 值小于 120），您将在输出中看到 `SQL No Result`，表示规则触发条件未被满足。

![规则执行结果](https://assets.emqx.com/images/73737c986e7594bd4c85b589e332c1fb.png)

相反，如果规则成功触发（例如，`speed` 超过 120），每个测试实例将按时间顺序显示在测试界面的左侧面板中，显示事件或主题消息以及测试开始的时间。点击任意实例即可查看测试的详细结果。

每个动作的结果（如 HTTP 服务器或 PostgreSQL 数据库的动作）都将清晰显示。成功的动作以绿色对号表示，而失败的动作则以红色“X”标记。

每个动作的详细信息可以展开以显示“请求”部分，供用户查看规则引擎处理和转发了哪些数据。例如，HTTP 服务的响应会在每个请求之后显示，以便用户深入了解动作结果。类似地，其他动作也会显示结果部分，向用户展示动作详情。

接下来，我们将模拟错误调试。先删除 HTTP 动作中的路径配置，并将有效载荷中 `vehicle_id` 的长度设置为超过 255 个字符，然后触发规则并测试上述修改。

![规则测试](https://assets.emqx.com/images/36f68725154e41f90830822fe57490a6.png)

#### HTTP 服务器

在规则触发后，如果 HTTP 服务器动作失败，您可以通过检查请求的详细信息来诊断问题。查看请求的主体内容是否与预期一致。如果动作失败，“原因”字段将提供具体的错误详情。例如，404 状态通常表示配置错误；如果路径错误地设置为 `/`，则可能会出现“无法发布”之类的错误消息。

![动作执行失败](https://assets.emqx.com/images/10f43854c2ac782058def726141880c0.png)

要解决此问题，请返回规则编辑界面，更新动作以包含 `/speed` 路径，然后保存。此更改无需重新保存整个规则，只需重新发送测试数据即可。如果配置正确，HTTP 服务器将返回操作成功，相关数据也会显示在 HTTP 服务控制台上。

![控制台](https://assets.emqx.com/images/8106bc6e7a59bcb4de21732324aa874f.png)

![响应结果](https://assets.emqx.com/images/220433541507d0342f7134d23e4f38ff.png)

#### PostgreSQL

查看 PostgreSQL 动作时，如果插入动作失败，原因字段将显示错误代码，例如 `string_data_right_truncation` (22001)，表示数据长度超出了数据库中字段的限制。

![发布测试1](https://assets.emqx.com/images/a1ea728a8d8ed7ba6c22b129efc784b7.png)

![发布测试2](https://assets.emqx.com/images/f3d41d15e55b36baf7719901434cbd72.png)

将 `vehicle_id` 的长度调短，重新发送数据，并检查插入操作是否成功。您可以在结果部分查看，并使用 Postico 等工具验证数据库中的数据是否已正确存储。

![发布测试3](https://assets.emqx.com/images/020a99d5922879aa754d7e6519340a61.png)

![查看数据库](https://assets.emqx.com/images/3e16b6eb6cb1e68b4fc6f2eb9ed51003.png)

这种结构化的方法使得规则测试更为准确，同时增强了调试能力，能够帮助用户有效地调整和优化规则。

## 结语

本文通过一个简单的示例，介绍了 EMQX 中规则调试和跟踪的基本流程，展示了其与传统 SQL 测试的区别。端到端规则测试对于维护 EMQX Platform 的稳健性和可靠性至关重要，尤其是在复杂的物联网环境中。通过及早发现问题，端到端测试可以提高开发效率，并确保系统的稳定性。

尽管当前的工具在功能上非常强大，但在内容显示和用户交互方面仍有提升空间。未来我们将进一步优化这些方面，以增强用户体验和系统功能。敬请关注。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
