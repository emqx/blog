本篇文章将使用 MQTT X 的脚本及定时功能模拟温湿度数据上报，EMQX Edge 作为消息中间件进行消息转发，EMQX Kuiper 进行消息接收并进行规则处理，最终将处理过的数据通过 EMQX Edge 下发到 MQTT X。

![mqttxedgekuiper.png](https://assets.emqx.com/images/9f96444f39724baa8ed5ee6d814618ed.png)

## 介绍及安装

本文中所演示的所有运行环境都将通过 Docker 搭建，如有其它安装需求，也可参考下文中提供的下载链接和安装文档进行构建。

### EMQX Kuiper

[EMQX Kuiper](https://github.com/lf-edge/ekuiper) 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。Kuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 [Apache Spark](https://spark.apache.org/)，[Apache Storm](https://storm.apache.org/) 和 [Apache Flink](https://flink.apache.org/) 等）迁移到边缘端。Kuiper 参考了上述云端流式处理项目的架构与实现，结合边缘流式数据处理的特点，采用了编写基于`源 (Source)`，`SQL (业务逻辑处理)`, `目标 (Sink)` 的规则引擎来实现边缘端的流式数据处理。项目地址：[https://github.com/emqx/kuiper](https://github.com/emqx/kuiper)

> 版本：v1.0.2

[下载链接](https://github.com/lf-edge/ekuiper) ｜ [安装文档](https://ekuiper.org/docs/zh/latest/installation.html)

```shell
# 获取 Docker 镜像
$ docker pull emqx/kuiper:1.0.2

# 启动 Docker 容器
$ docker run -p 9081:9081 -d --name kuiper emqx/kuiper:1.0.2
```

### Kuiper-manager

本文将使用 Kuiper-manager 对 EMQX Kuiper 进行可视化管理和使用，Kuiper-manager 是一款可用于管理 Kuiper 节点，流，规则和插件等的 Web 管理控制台。

> 版本：v1.0.2

目前仅支持使用 Docker 镜像

```shell
# 获取 Docker 镜像
$ docker pull emqx/kuiper-manager:1.0.2

# 启动 Docker 容器
$ docker run -p 9082:9082 -d emqx/kuiper-manager:1.0.2
```

### EMQX Edge

[EMQX Edge](https://www.emqx.com/zh/products/emqx) 是轻量级多协议物联网边缘消息中间件，支持部署在资源受限的物联网边缘硬件。项目地址：[https://github.com/emqx/emqx](https://github.com/emqx/emqx)

> 版本：v4.2.4

[下载链接](https://www.emqx.com/zh/try?product=nanomq) | [安装文档](https://nanomq.io/docs/zh/latest/)

```shell
# 获取 Docker 镜像
$ docker pull emqx/emqx-edge:4.2.4

# 启动 Docker 容器
$ docker run -d --name emqx -p 1883:1883 emqx/emqx-edge:4.2.4
```

### MQTT X

[MQTT X](https://mqttx.app/zh) 是由一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接/发布/订阅功能及其他 **MQTT 协议** 特性。项目地址：[https://github.com/emqx/MQTTX](https://github.com/emqx/MQTTX)

> 版本：v1.4.2

[下载链接](https://mqttx.app/zh) | [GitHub](https://github.com/emqx/MQTTX/releases/tag/v1.4.2)

用户可到 MQTT X 官网或 GitHub 下载页下载所对应操作系统的安装包进行安装使用。

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

## 使用教程

在搭建完环境后，我们就可以搭配各模块间的功能来使用，进行功能测试和验证。

### Kuiper-manager 使用

首先我们对 Kuiper 进行流和规则的创建和配置。在安装完并运行 Kuiper-manager 成功后，我们打开浏览器，然后输入 `http://localhost:9082`。 如果您从其他计算机访问 kuiper-manager，请将 `localhost` 更改为运行 kuiper-manager 的 IP 地址。首次打开后需要输入的用户名密码为：`admin` / `public`，建议首次登录后，进行密码修改。

![kuipermanagerlogin.png](https://assets.emqx.com/images/de28b1b45f019523ec9c8ed7b38851e5.png)

#### 节点

登录成功之后会进入到一个节点管理界面，点击 `添加节点` 按钮，会有一个弹出框，需要添加一个 Kuiper 的实例节点。这里我们使用的是普通节点，就选择第一项 `直连节点`。除直连节点外，目前还支持添加华为 IEF 节点，本文将不做阐述。然后输入需要操控的 Kuiper 实例的 `端点地址` ，并输入 `节点名称` 用来标识节点。

> 注意：如果使用 Docker 启动的话，端点地址需要输入 Docker 容器内的 IP 地址

![kuiperaddnodes.png](https://assets.emqx.com/images/e219d0c1d211bb49a88866310ecbd3db.png)

添加成功后，我们在节点列表中，点击节点名称后可进入到该节点实例中。进入后，接下来我们将配置创建该 Kuiper 实例下的流和规则。

#### 流

进入到 Kuiper 实例页面后，会进入到流的 Tab 页面下，我们点击右边 `创建流` 按钮，进入到创建流的页面，此时可按以下步骤来进行操作：

1. 输入一个 `流名称` 用来标识，这里我们输入流名称为 `demo`；

2. 输入结构定义，比如该条流需要接收到的流数据中有哪些字段类型，我们可以提前定义。添加时仅需输入字段名称，和选择类型添加即可，类型包含了 `bigint`, `float`, `string`, `boolean`, `array`, `struct` 等。结构定义为可选，可以勾选结构列表上方的 `是否为带结构的流` 来取消或开启结构定义，当取消结构定义时，将接收任何结构类型的数据。本文中我们已经规定好了需要处理的数据结构，所以我们分别添加两个字段：`temperature` 和 `humidity`，类型都为 `bigint`；

3. 输入 `数据源`，文中我们将使用 MQTT 作为消息源，因此该配置可输入用于接收消息的 `Topic`， 这里我们输入 `/kuiper/stream` ；

4. 选择 `流类型`，这里将选择为 MQTT；

5. 选择 `配置组`，配置组即为流类型下定义的配置信息，比如 MQTT 默认配置组下 `servers` 信息为 `['tcp://127.0.0.1:1883']`。用户可自定义该配置信息，点击上方的 `源配置` 按钮，进入到页面中配置，也可到  `etc`  目录下修改配置文件。这里我们选择重新配置过的 `demo_conf` 配置组；

   > 注意：如果使用的 MQTT Broker 为 Docker 启动的 EMQX Edge 话，Servers 地址需要修改为 Docker 容器内的 IP 地址

6. 选择 `流格式`，最后我们选择流数据格式为 `json`。

![kuipercreatestream.png](https://assets.emqx.com/images/f7d5df43a41e46815c67716567f322da.png)

除以上可视化创建方式外，我们还可以点击页面中最右上角的切换按钮，切换到文本模式。可直接输入创建流的 SQL 语句进行创建，SQL 示例：

```sql
CREATE STREAM demo (
  temperature bigint,
  humidity bigint,
) WITH (DATASOURCE="/kuiper/stream", FORMAT="json", CONF_KEY="demo_conf", TYPE="mqtt");
```

点击 `提交` 按钮后，我们就成功创建了一条流。接下来将为创建好的流设置规则。

#### 规则

点击规则的 Tab 项，进入到规则列表页面，我们点击右边的 `创建规则` 按钮，进入到创建规则的页面，此时可按以下步骤来进行操作：

1. 输入 `规则 ID` 用来标识该规则，这里我们输入 `demoRule`；

2. 输入 `SQL` 语句，为规则运行的 SQL 查询。这里将定义一条查询数据流中的温湿度数据，并设置过滤条件为温度大于 30 时的 SQL 语句。SQL 示例：

   ```sql
   SELECT temperature, humidity FROM demo WHERE temperature > 30
   ```

3. 选择添加规则的 `动作`，即为 Sink 动作组，数据可多选，Sink 为当规则执行后输出的目标。这里我们依然使用 MQTT，通过 MQTT 转发规则执行后的数据。选择完成后，可输入 MQTT Sink 的配置信息，本文就只配置  MQTT Broker 的地址和  `Topic`  信息，`Topic`  即为接收消息的主题。

   > 注意：如果使用的 MQTT Broker 为 Docker 启动的 EMQX Edge 话，Broker 地址需要填写为 Docker 容器内的 IP 地址

4. 设置 `选项`，选项部分为可选，均有默认值，如需修改可参考 [Kuiper 文档](https://ekuiper.org/docs/zh/latest/) 进行设置。

![kuipercreaterule.png](https://assets.emqx.com/images/66bffdc71ba9c49183b080d42d6135b4.png)

除以上可视化创建方式外，我们还可以点击页面中最右上角的切换按钮，切换到文本模式。可直接输入创建规则的 JSON 数据进行创建，JSON 示例：

```json
{
  "id": "demoRule",
  "sql": "SELECT temperature, humidity FROM demo WHERE temperature > 30",
  "actions": [
    {
      "mqtt": {
        "server": "tcp://172.17.0.2:1883",
        "topic": "/kuiper/rule"
      }
    }
  ]
}
```

点击 `提交` 按钮后，我们就成功创建了一条规则。至此，我们就已经完成了 Kuiper 数据流和规则配置，接下来我们将使用 MQTT X 来测试和验证 Kuiper 的流处理功能。

### MQTT X 使用

下载安装完成后，打开 MQTT X，我们新建一个名为 `edge1` 的连接，连接到和 Kuiper Source 配置相同的 EMQX Edge 上。测试连接成功后，我们进入到 ` 脚本` 页面，使用以下提供的示例脚本，来生成模拟数据。

```javascript
/**
 * Simulated temperature and humidity reporting
 * @return Return a simulated temperature and humidity JSON data - { "temperature": 23, "humidity": 40 }
 * @param value, MQTT Payload - {}
 */

function random(min, max) {
  return Math.round(Math.random() * (max - min)) + min
}

function handlePayload(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  _value.temperature = random(10, 40)
  _value.humidity = random(20, 40)
  return JSON.stringify(_value, null, 2)
}

execute(handlePayload)
```

![mqttxscript.png](https://assets.emqx.com/images/5aef8144b3c75fab5730afd7f7545c31.png)

测试发现模拟数据成功，我们到连接页面中，打开脚本使用功能（使用脚本功能本文不做详细描述，可参考 [MQTT X 文档](https://github.com/emqx/MQTTX/blob/main/docs/manual-cn.md#%E8%84%9A%E6%9C%AC)），输入发送的  `Payload`  数据模版为  `{}` ，输入 `Topic` 为流定义中的 `Data Source`，这里就填写 `/kuiper/stream`，然后设置定时消息，设置发送频率为 1 秒，然后点击发送一条消息成功后，MQTT X 将每秒自动发送一条模拟测试数据。

![mqttxtimed.png](https://assets.emqx.com/images/6358d2d739f455bb36670269eb3e2c52.png)

此时再新建一个名为 `edge2` 的连接，连接到和 Kuiper Sink 配置相同的 EMQX Edge 上，然后订阅 MQTT Sink 中配置的  `Topic`，这里就订阅 `/kuiper/rule` 主题，用来接收 Kuiper 处理的过的数据。

![mqttxrule.png](https://assets.emqx.com/images/d3d9bc645f87f0bfe5d63a6c2b6ee62a.png)

### 验证结果

当我们发送了模拟数据后，可以通过在规则列表中点击 `状态` 按钮查看是否有消息流入流出。我们通过以下截图可以看到，Kuiper 总共收到了 40 条消息，过滤流出了 14 条消息。

![kuiperrulestatus.png](https://assets.emqx.com/images/73b59e082e4af79cdc8c7491b6fed441.png)

然后继续查看 MQTT X 内的信息，`edge1` 一共定时发送了 40 条模拟消息，切换到 `edge2` 可以查看到一共收到 14 条消息。发送和接收数据和 Kuiper 内统计流入流出数据一致，且查看接收到的消息中的 `temperature` 都完全大于 30，满足了我们在 Kuiper 中设置的过滤条件。说明我们的 Kuiper 流处理功能已经成功完成了我们所设置的数据处理需求，测试和验证成功。

![mqttxsend.png](https://assets.emqx.com/images/3aabe367e47e56a41033aa3a6cfed18e.png)

![mqttxres.png](https://assets.emqx.com/images/489c0e0422a1eae70a730cb0a70af7ec.png)

除通过状态按钮查看 Kuiper 规则处理的数据信息外，还可点击 `拓扑` 按钮，进入到规则的拓扑图页面，通过规则拓扑图完整的将数据流向与规则状态展示出来，并且可以查看到具体处理数据模块的实时动态信息。

![kuiperruletopo.png](https://assets.emqx.com/images/e6790e6b1ebee6501f96670b8d23129d.png)

## 总结

至此，本文就完成了一个使用 MQTT X 客户端验证 Kuiper 流处理的功能的简易教程。Kuiper 可以运行在各类物联网的边缘使用场景中，通过 Kuiper 在边缘端的处理，可以提升系统响应速度，节省网络带宽费用和存储成本，以及提高系统安全性等。

除文章中所示例的 MQTT Source 和 MQTT Sink 外，Kuiper 还内置了许多多样化的 Source 和 Sink 配置，并且包含了与 EdgeX Foundry、KubeEdge、EMQX Edge 等的集成能力。规则 SQL 内还支持 60+ 常见的函数，提供扩展点可以扩展自定义函数。提供了强大的插件系统，高度可扩展。

本篇文章中所使用三个项目都完全开源，您可以到 GitHub（[EMQX Kuiper](https://github.com/emqx/kuiper)、[EMQX Edge](https://github.com/emqx/emqx)、[MQTTX](https://github.com/emqx/MQTTX)）中来提交使用过程中遇到的问题，或是 Fork 我们的项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
