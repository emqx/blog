## 引言

随着物流行业的快速发展，以物联网技术作为核心的智慧物流应用愈加广泛。

EMQX 和 MongoDB 的集成为物流行业提供了一种便捷高效的数据采集方案。企业级 MQTT 物联网接入平台 EMQX 能够实现车辆上各种 IoT 传感器数据采集以及各个流程上的数据汇总，MongoDB 数据库则可提供汇聚和分析能力，满足车辆问题与货物状态监测、配送路线优化和货物装载调配等需求。

这一方案可为物流企业提供丰富的管理决策依据，从而优化运输过程优化、提升运输效率、降低运输成本，进一步提高服务质量与客户满意度。

本文将演示如何利用 EMQX 从车辆采集各类传感器数据，并与 MongoDB 集成，实现数据的实时存储和分析。

## 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

这是个简单而高效的架构，无需复杂的组件。主要包括以下关键组件：

| 组件名称                                                 | 版本   | 说明                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/zh/cli)                    | 1.9.3+ | 用于模拟生成运输车辆数据的命令行工具。                       |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.0.4+ | 用于在运输车辆和 MongoDB 之间进行消息传递的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。 |
| [MongoDB](https://mongodb.com/)                          | 4.4.6+ | 用于物流数据的存储和管理。                                   |

## 下载示例项目到本地

使用 Git 将 [emqx/mqtt-to-mongodb](https://github.com/emqx/mqtt-to-mongodb) 存储库代码下载到本地：

```
git clone https://github.com/emqx/mqtt-to-mongodb
cd mqtt-to-mongodb
```

代码库由四部分组成：

- `emqx` 文件夹包含了 EMQX-MongoDB 的集成配置，可以在启动 EMQX 的时候自动创建规则和数据桥接。
- `mongo` 文件夹包含了数据库用户初始化命令。
- `mqttx/logistics.js` 文件提供了物流运输车队模拟脚本，实现接近真实世界的数据上报。
- `docker-compose.yml` 文件可编排所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 MongoDB

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose，使用以下命令启动演示：

```
docker-compose up -d
```

下面，MQTTX CLI 将模拟 5 辆汽车连接到 EMQX，并以每秒 1 条消息的频率向 EMQX 发送其运行与货仓传感器数据。数据以 JSON 格式发送到主题 `mqttx/simulate/logistics/{clientid}`。

数据包含的内容如下表：

| **数据名称**     | **说明**                                                 |
| :--------------- | :------------------------------------------------------- |
| car_id           | 车辆唯一 ID                                              |
| display_name     | 车辆显示名称，方便用户识别车辆                           |
| model            | 车辆型号                                                 |
| latitude         | 纬度坐标，标识车辆当前实时位置                           |
| longitude        | 经度坐标，标识车辆当前实时位置                           |
| speed            | 当前速度，可用于分析是否超速与堵车状态。单位：千米/小时  |
| distance         | 行驶里程，可用于车辆的维护保养、货运里程记录。单位：千米 |
| direction        | 行驶方向                                                 |
| tyre_pressure    | 轮胎气压，数组格式，包含所有轮胎胎压。单位：千帕         |
| warehouse        | 货仓环境温湿度数据，可用于特殊货物环境监测与告警         |
| fuel_consumption | 瞬时百公里油耗，可用于运输成本管理。单位：升/百公里      |
| shift_state      | 车辆档位，可用于驾驶行为分析                             |
| state            | 运行状态                                                 |
| power            | 发动机功率。单位：千瓦                                   |
| windows_open     | 车窗状态                                                 |
| doors_open       | 车门状态                                                 |
| inside_temp      | 车内温度                                                 |
| outside_temp     | 外界温度                                                 |
| timestamp        | 时间戳                                                   |

上报的车辆数据示例：

```
{
    "car_id": "XCRHFDSBFPL011940",
    "display_name": "car_1",
    "model": "J7",
    "latitude": 166.7460400818362,
    "longitude": 142.5736913214525,
    "speed": 74,
    "distance": 20.555555555555557,
    "direction": 46,
    "tyre_pressure": [
        496.2,
        466.4,
        449.6,
        443,
        473.8,
        458.6,
        496.3,
        536.2,
        480.7,
        532.4
    ],
    "warehouse": {
        "humidity": 18.9,
        "temperature": 49.1
    },
    "fuel_consumption": 12.58,
    "shift_state": "D7",
    "state": "moving",
    "power": 288,
    "windows_open": true,
    "doors_open": false,
    "inside_temp": 28.1,
    "outside_temp": -3.8,
    "timestamp": 1699608487632
}
```

EMQX 将创建一条规则接收来自每辆车的消息，其中为了在 MongoDB 写入时间格式数据，需要使用 `mongo_data` 函数对字段进行特殊处理。您也可以稍后修改这个规则，使用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html)添加自定义处理：

```
SELECT
  *,  json_decode(payload) as payload,
  mongo_date(payload.timestamp) as mongo_ts
FROM
  "mqttx/simulate/#"
```

规则处理完数据后，EMQX 将通过数据桥接将消息中的车辆数据写入到 MongoDB 指定的集合中。数据桥接的写入模板可以支持自定义的写入数据结构，结合 MongoDB 灵活的文档数据结构，可以实现复杂数据格式的存储。

## 从 EMQX 订阅数据

Docker Compose 包含一个用于打印所有车辆数据的 MQTT 订阅客户端，可以使用以下命令查看消息：

```
$ docker logs -f mqttx
[11/10/2023] [2023-11-10] [17:28:06] › topic: mqttx/simulate/logistics/mqttx_ee9e6f9e
payload: {"car_id":"XCRHFDSBFPL011940","display_name":"car_1","model":"J7","latitude":151.95961085265282,"longitude":128.29460259535088,"speed":114,"distance":31.666666666666668,"direction":26,"tyre_pressure":[441.1,577.9,510.1,466.4,496.1,556.1,469.2...
```

您也可以使用任何 MQTT 客户端来订阅和接收已发布的数据，例如：

```
mqttx sub -t mqttx/simulate/IEM/+
```

## 结语

在本文中，我们探讨了如何使用 EMQX 作为实时 MQTT Broker，并利用其数据集成功能将数据写入到 MongoDB，从而实现两者的集成来构建智慧物流数据采集应用。

这个演示项目旨在构建一个物流数据汇聚与共享的平台，用于实现物流运输管理过程中各类环节的数据采集、数据处理以及存储分析。通过结合 EMQX 的可靠性和 MongoDB 的灵活存储、丰富的分析能力，我们能够从各类数据中提取有价值的见解。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
