## 引言

[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)是一种专为物联网应用而设计的轻量级消息传输协议。它具有简单、开放、易于实现的特点，是物联网应用的理想选择。MQTT 数据以连续实时的方式进行传输，非常适合由流处理引擎进行处理。

[EMQX](https://www.emqx.com/zh/products/emqx) 是一款大规模分布式物联网 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，能够高效、可靠地连接海量的物联网设备，并实时处理和分发消息和事件流数据。[eKuiper](https://ekuiper.org/zh) 是一个开源的流处理引擎，可以对流数据进行过滤、转换和聚合等操作。

本文将向您展示如何使用 eKuiper 实时流处理引擎来处理来自 EMQX 的 MQTT 数据。

![MQTT Stream Processing with EMQX and eKuiper](https://assets.emqx.com/images/fae0396b7c04f6b24fd42fa693023746.png)

## 场景描述

假设我们有个 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics) `demo/sensor`，用于在 EMQX 中接收温度和湿度数据。我们希望使用 eKuiper 订阅该主题，并用流处理技术对数据进行处理和分析。然后，我们可以根据分析结果，触发用户的 HTTP 服务，或者将结果保存到外部存储中。

### EMQX

由于 EMQX 支持标准的 MQTT 协议，所以 eKuiper 可以连接到任何版本的 EMQX。在这里，我们使用 [EMQX Cloud](https://www.emqx.com/zh/cloud) 提供的免费公共 MQTT Broker 进行测试：

| 集群  | 集群地址         | 监听端口 |
| :---- | :--------------- | :------- |
| emqx1 | `broker.emqx.io` | 1883     |

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

### eKuiper

eKuiper 可以部署在边缘或云端。我们可以使用 `Docker` 进行快速安装。

```
docker run -p 9081:9081 -d --name kuiper -e MQTT_SOURCE__DEFAULT__SERVER=tcp://broker.emqx.io:1883 lfedge/ekuiper:1.10.0
```

我们可以用这个命令拉取并运行 eKuiper 1.10.0 版本的 docker 镜像。我们将 REST API 端口设置为 9081，在本教程中，我们将使用 REST API 来管理 eKuiper。我们还通过环境变量把默认的 MQTT Broker 地址指向了 EMQX Cloud 集群。

如果您想使用其他方法安装 eKuiper，请查看[安装指南](https://ekuiper.org/docs/en/latest/installation.html)。

> [EMQX ECP](https://www.emqx.cn/products/emqx-ecp) (EMQX Edge-to-Cloud Platform) 是专为云边协同而打造的高级 MQTT 平台。它提供了专业的 Web UI 让您可以方便地管理 eKuiper。在本教程中，您也可以使用 ECP 来管理 eKuiper。更多细节，请参考 [ECP 文档](https://docs.emqx.com/zh/emqx-ecp/latest/)。

## 配置 eKuiper 订阅 MQTT 数据流

MQTT 数据是一种无界的、连续的流式数据。在 eKuiper 中，我们使用流的概念来映射这种类型的数据。要处理 MQTT 数据，我们首先要创建一个流来描述数据。

我们用 eKuiper REST API 来创建一个流：

```
POST http://127.0.0.1:9081/streams
Content-Type: application/json

{
  "sql": "CREATE STREAM demoMqttStream (temperature FLOAT, humidity FLOAT) WITH (TYPE=\"mqtt\", DATASOURCE=\"demo/sensor\", FORMAT=\"json\", SHARED=\"true\")"
}
```

用 Postman 等 HTTP 客户端发送上面的请求，将创建一个名为 `demoMqttStream` 的流，它是 MQTT 类型的数据源。`datasource` 属性的值是 `demo/sensor`，表示订阅 MQTT 的 `demo/sensor` 主题。数据格式是 JSON。`SHARED` 选项表示这个流可以被所有规则共享。

> **注意：**
>
> 我们运行 eKuiper docker 容器时，MQTT Broker 地址默认是 `tcp://broker.emqx.io:1883`。如果您用的是别的 MQTT Broker，请在安装时换成您的 Broker 地址。
>
> 如果您想改变 MQTT Broker 地址或其他 MQTT 连接参数，如认证相关配置，可以修改 `data/mqtt_souce.yaml` 文件里的设置。
>
> 您可以用 `+` 和 `#` 通配符订阅多个主题，在 `datasource` 属性里使用这些通配符。比如，`demo/+` 是订阅所有以 `demo/` 开头的主题。`demo/#` 是订阅所有以 `demo/` 开头的主题和 `demo/` 下的所有子主题。

## 流处理 MQTT 数据

在 eKuiper 中，我们用规则来定义流处理的工作流程。规则是 SQL 语句，它规定了数据处理的方式和处理后执行的动作。除了连续的数据处理，像 eKuiper 这样的流处理引擎还支持有状态处理。我们将演示两个流处理和有状态处理的例子。

### 有状态的报警规则

第一个流处理例子是监测温度和湿度数据，温度上升超过 0.5 或湿度上升超过 1 就触发报警。这要求处理引擎能够记住前一条数据的状态，并和当前数据比较。

假设我们有个 URL 为 `http://yourhost/alert` 的 HTTP webhook，用来接收报警数据。我们首先用下面的 HTTP 请求创建一个规则。

```
###
POST http://{{host}}/rules
Content-Type: application/json

{
  "id": "rule1",
  "sql": "SELECT temperature, humidity FROM demoMqttStream WHERE temperature - LAG(temperature) > 0.5 OR humidity - LAG(humidity) > 1",
  "actions": [{
    "rest": {
      "url": "http://yourhost/alert",
      "method": "post",
      "sendSingle": true
    }
  }]
}

```

上述请求创建了一个名为 `rule1` 的规则，该规则对应的 SQL 语句如下：

```
SELECT temperature, humidity 
FROM demoMqttStream 
WHERE 
  temperature - LAG(temperature) > 0.5 
  OR humidity - LAG(humidity) > 1
```

这个 SQL 从 `demoMqttStream` 里选出变化达到我们条件的温度和湿度数据。`LAG` 函数用来获取前一条数据。

`actions` 属性规定了规则触发后的动作。这里，我们用 `rest` 动作把数据发送到 `http://yourhost/alert` 。发送的是 SQL 筛选出的数据，以 JSON 格式发送。所以，发送的数据是这样的：

```
{
  "temperature": 25.5,
  "humidity": 60.5
}
```

#### 测试规则

我们可以用 [MQTTX](https://mqttx.app/zh) 或者其他 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)来发布 MQTT 数据到 `demo/sensor` 主题。规则会处理这些数据。比如，我们发送以下数据到主题：

```
{"temperature": 25.5, "humidity": 60.5}
{"temperature": 26.1, "humidity": 62}
{"temperature": 25.9, "humidity": 62.1}
{"temperature": 26.5, "humidity": 62.3}
```

我们将在 HTTP 警报服务中收到下列数据：

```
{"temperature": 26.1, "humidity": 62}
{"temperature": 26.5, "humidity": 62.3}
```

这是因为只有第二和第四条消息，温度上升超 0.5 或湿度上升超 1。

如果您在运行规则时遇到任何问题，请参考[如何调试规则 | eKuiper 文档](https://ekuiper.org/docs/en/latest/getting_started/debug_rules.html)

### 时间窗口聚合规则

第二个例子是计算每分钟的平均温度和湿度，并把它发送回 EMQX。这涉及到一个经典的流处理概念，叫做时间窗口。我们可以用以下 HTTP 请求来创建一个规则。

```
###
POST http://{{host}}/rules
Content-Type: application/json

{
  "id": "rule2",
  "sql": "SELECT 
  trunc(avg(temperature), 2) as avg_temperature, trunc(avg(humidity), 2) as avg_humidity, window_end() as ts FROM demoMqttStream GROUP BY TumblingWindow(mi, 1)",
  "actions": [{
    "mqtt": {
      "server": "tcp://broker.emqx.io:1883",
      "topic": "result/aggregation",
      "sendSingle": true
    }
  }]
}
```

上述请求创建了一个名为 `rule2` 的规则，该规则对应的 SQL 语句如下：

```
SELECT 
  trunc(avg(temperature), 2) as avg_temperature, 
  trunc(avg(humidity), 2) as avg_humidity,
  window_end() as ts
FROM demoMqttStream
GROUP BY TumblingWindow(mi, 1)
```

这个 SQL 会选出每分钟的温度和湿度平均值。时间窗口在 `GROUP BY` 子句中用 `TumblingWindow` 定义。这种窗口类型把 MQTT 数据分成固定长度的窗口。在 `SELECT` 子句中，我们用聚合函数 `avg` 来计算时间窗口内温度和湿度的平均值。`window_end()` 函数用来获取时间窗口的结束时间，这样我们就能知道这些平均值对应的时间段。`trunc` 函数用来把平均值四舍五入到两位小数。

`actions` 属性规定了规则触发后的动作。这里，我们用 `mqtt` 动作发送数据到 EMQX 的 `result/aggregation` 主题。发送的是 SQL 筛选出的数据，以 JSON 格式发送。所以，发送到主题的数据是这样的：

```
{
  "avg_temperature": 25.5,
  "avg_humidity": 60.5,
  "ts": 1621419600000
}
```

#### 测试规则

同样，我们可以用 [MQTTX](https://mqttx.app/zh) 或者其他 MQTT 客户端来发布 MQTT 数据到 `demo/sensor` 主题。规则会处理这些数据。比如，我们每 30 秒发送一条数据到主题，两分钟的数据如下所示：

```
{"temperature": 25.5, "humidity": 60.5}
{"temperature": 26.1, "humidity": 62}
{"temperature": 25.9, "humidity": 62.1}
{"temperature": 26.5, "humidity": 62.3}
```

我们将在 HTTP 警报服务中收到下列数据：

```
{"avg_temperature": 25.8, "avg_humidity": 61.25, "ts": 1621419600000}
{"avg_temperature": 26.2, "avg_humidity": 62.2, "ts": 1621419660000}
```

我们发送了两分钟的数据，所以得到了两个每分钟的平均值。

## 结语

在本教程中，我们学习了如何使用 eKuiper 处理 MQTT 数据。通过本教程，您能够：

- 通过订阅 EMQX MQTT Broker 主题接收 MQTT 数据
- 制定规则来处理 MQTT 数据
- 将处理后的数据反馈给 EMQX Broker

我们用两个示例展示了 eKuiper 对 MQTT 数据的流处理能力。eKuiper 强大的流处理能力可以应用于多种流式数据源。欢迎您探索 eKuiper 的各种功能，构建实时高效的 MQTT 数据处理通道。



<section class="promotion">
    <div>
        免费试用 eKuiper
    </div>
    <a href="https://ekuiper.org/zh/downloads" class="button is-gradient px-5">开始试用 →</a>
</section>
