## 引言

在当今的物联网领域，[MQTT 和 Kafka](https://www.emqx.com/zh/blog/mqtt-and-kafka) 的集成为各种应用场景提供了巨大的价值。无论是[网联汽车](https://www.emqx.com/zh/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know)和车载信息通信系统、智慧城市基础设施，还是[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)监控、物流管理，MQTT 和 Kafka 的结合都能帮助这些场景实现无缝、高效和实时的数据处理。

本文将为您演示如何高效集成 MQTT 和 Kafka。我们将模拟车辆设备及其动态车联网数据，将它们连接到 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，然后再将数据发送到 Apache Kafka。本文选择 [EMQX](https://www.emqx.com/zh/products/emqx) 作为 MQTT Broker，它内置了 Kafka 数据集成功能，可以简化演示流程。

## 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

MQTT 和 Kafka 集成架构如下图所示：

![MQTT 和 Kafka 集成架构](https://assets.emqx.com/images/414774fb7f5b20256d52eaf70196798a.jpg)

这是一个既简单又有效的架构，没有使用复杂的组件。它只使用了以下 3 个基本组件：

| 组件名称                                                 | 版本   | 说明                                                 |
| :------------------------------------------------------- | :----- | :--------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+ | 用于模拟车辆并生成测试数据的命令行工具。             |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.0.4+ | 车辆与 Kafka 系统之间进行信息交换的 MQTT Broker。    |
| [Kafka](https://kafka.apache.org/)                       | 2.8.0+ | 一个分布式流媒体平台，用于接收、存储和处理车辆数据。 |

除了上述基础组件外，EMQX 还具备丰富的监控功能。您可以利用以下组件来实时监控 EMQX 的性能指标和负载情况：

| 组件名称                                               | 版本    | 说明                                   |
| :----------------------------------------------------- | :------ | :------------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | 用于 EMQX 的 Prometheus Exporter。     |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | 开源的系统监控和警报工具包。           |
| [Grafana](https://grafana.com/)                        | 9.5.1+  | 用于显示和分析收集的数据的可视化平台。 |

现在，您已经了解了这个项目的基本架构，下面让我们开始演示吧！

## 5 步轻松搭建 MQTT 到 Kafka 的演示

### 1. 将项目克隆到本地

将 [emqx/mqtt-to-kafka](https://github.com/emqx/mqtt-to-kafka) 存储库克隆到本地，并初始化子模块以启用 EMQX Exporter（可选）：

```
git clone https://github.com/emqx/mqtt-to-kafka
cd mqtt-to-kafka

# Optional
# 可选
git submodule init
git submodule update
```

代码库由 3 部分组成：

- `emqx` 文件夹包含 EMQX-Kafka 集成配置，用于在自动启动 EMQX 时创建规则和数据桥接。
- `emqx-exporter`、`prometheus` 和 `grafana-provisioning` 文件夹包含 EMQX 的监控配置。
- `docker-compose.yml` 可编排多个组件，一键启动项目。

### 2. 启动 MQTTX CLI、EMQX 和 Kafka

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose，开始演示：

```
docker-compose up -d
```

现在，MQTTX CLI 模拟的 10 辆特斯拉汽车连接到 EMQX，并以每秒一次的频率向 `mqttx/simulate/Tesla/{clientid}` 主题报告其状态。

EMQX 会创建一条规则来接收来自特斯拉的消息。您也可以修改该规则，使用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html)添加自定义消息处理方法：

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

EMQX 还会创建一个数据桥接，通过以下配置将车辆数据传送到 Kafka：

- 向 Kafka 中的 `my-vehicles` 主题发布消息
- 使用每辆车的客户端 ID 作为消息 Key
- 使用消息发布时间作为消息时间戳

![EMQX kafka 配置](https://assets.emqx.com/images/ad15e9decf2e5be01d712ec0b3aa2090.png)

### 3. 从 EMQX 订阅车辆数据

Docker Compose 包含一个用于打印所有车辆数据的订阅者。可以使用以下命令查看数据：

```
$ docker logs -f mqttx
[8/4/2023] [8:56:41 AM] › topic: mqttx/simulate/tesla/mqttx_063105a2
payload: {"car_id":"WLHK53W2GSL511787","display_name":"Roslyn's Tesla","model":"S...
```

使用任何 MQTT 客户端都可以订阅和接收数据：

```
mqttx sub -t mqttx/simulate/tesla/+
```

### 4. 从 Kafka 订阅车辆数据

如果一切运行正常，EMQX 会将车辆中的数据实时传输到 Kafka 的 `my-vehicles` 主题中。您可以使用以下命令从 Kafka 中获取数据：

```
docker exec -it kafka \
   kafka-console-consumer.sh \
   --topic my-vehicles \
   --from-beginning \
   --bootstrap-server localhost:9092
```

您将收到类似下面的 JSON 数据：

```
{"vin":"EDF226K7LZTZ51222","speed":39,"odometer":68234,"soc":87,"elevation":4737,"heading":33,"accuracy":24,"power":97,"shift_state":"D","range":64,"est_battery_range":307,"gps_as_of":1681704127537,"location":{"latitude":"83.3494","longitude":"141.9851"},"timestamp":1681704127537}
```

该数据的灵感来自 [TeslaMate](https://github.com/adriankumpf/teslamate)，这是一个强大的自托管特斯拉数据记录器。您可以查看 MQTTX CLI [脚本](https://github.com/emqx/MQTTX/blob/main/scripts-example/IoT-data-scenarios/tesla.js)，了解数据是如何生成的。

### 5. 查看 EMQX 指标（可选）

如果您在第一步中启用了 EMQX Exporter，它将收集所有 EMQX 的指标，包括客户端连接、消息速率、规则执行情况等等，这将为系统提供有用的信息。

要在 Grafana 仪表板中查看 EMQX 指标，请在浏览器中打开 `http://localhost:3000`, 使用用户名 `admin` 和密码 `public` 登录。

## 结语

本文介绍了如何利用 MQTT 和 Kafka 构建车联网流数据管道。我们采用 EMQX 作为 MQTT Broker，借助 EMQX 的数据集成功能将数据实时传输到 Kafka，从而实现了一个收集和处理流数据的端到端解决方案。

接下来，您可以直接将应用集成到 Kafka 中，获取车辆数据并实现它们的解耦。您还可以利用 Kafka Streams 对汽车数据进行实时流处理，进行统计分析和异常检测。处理结果还可通过 Kafka Connect 输出到其他系统。

本文提供的是构建可扩展和可靠的流数据管道的入门示例。欢迎读者基于本文继续探索 MQTT 和 Kafka 的强大融合为各个领域的实时分析、监控和决策带来的更多可能。

**相关资源：**

- 访问 [GitHub 链接](https://github.com/emqx/mqtt-to-kafka) 查看使用 Kafka 简化 MQTT 数据集成的演示。
- 参考 [EMQX 文档](https://docs.emqx.com/en/enterprise/v5.1/data-integration/data-bridge-kafka.html) 了解如何从头开始配置此数据流管道。


<section class="promotion">
    <div>
        联系 EMQ 解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
