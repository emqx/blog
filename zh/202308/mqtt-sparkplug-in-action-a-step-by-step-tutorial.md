## 引言

[Sparkplug](https://www.emqx.com/zh/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot "https://www.emqx.com/zh/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot") 是一种[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)协议，旨在为工业设备和应用之间提供标准化的通信方式。高效、全面的 Sparkplug 解决方案可以促进设备和应用的互联互通，并通过数据分析提升工业物联网用户的决策水平。

本文将使用 EMQX 和 Neuron，展示构建 [MQTT Sparkplug](https://www.emqx.com/zh/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) 解决方案的详细过程。

## 基本组件：EMQX 和 Neuron

[EMQX](https://www.emqx.io/ "https://www.emqx.io/") 是一款支持 Sparkplug 协议的热门 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison "https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison")，Neuron 是一款工业物联网平台，能够从工业设备获取数据，并将数据转换为 Sparkplug 消息发送给应用。

[Neuron](https://neugates.io/ "https://neugates.io/") 可以从设备获取数据，并根据数据变化情况将 Sparkplug 消息发布到 EMQX Broker。EMQX 会把消息转发给订阅了相应 Sparkplug 主题的应用。此外，EMQX 还可以通过规则引擎对 Sparkplug 消息进行解码。这些消息可以用于数据平台、历史数据持久化存储等场景。

> 了解 Sparkplug 解决方案架构详情：[基于 EMQX 和 Neuron 的工业物联网 MQTT Sparkplug 解决方案](https://www.emqx.com/zh/blog/mqtt-sparkplug-solution-for-industrial-iot-using-emqx-and-neuron "https://www.emqx.com/zh/blog/mqtt-sparkplug-solution-for-industrial-iot-using-emqx-and-neuron")


![MQTT Sparkplug solution](https://assets.emqx.com/images/ec53f4b3ec654a85a43d4745e630dd18.png)

在本文中，我们将向您展示如何利用 EMQX 和 Neuron 来入门 MQTT Sparkplug，具体步骤如下：

1. 安装 EMQX

2. 配置 EMQX

3. 安装 Neuron

4. 在 Neuron 中配置设备

5. 将 Neuron 连接到 EMQX

6. 在 MQTTX 中查看结果


让我们开始吧！

## 安装 EMQX

请在您的服务器或机器上下载并安装 EMQX MQTT Broker。EMQX 提供开源版，可从官网免费下载。请访问 [https://www.emqx.io/](https://www.emqx.io/) 并按照文档指引进行操作。

## 配置 EMQX

安装好 EMQX 后，需要对其进行配置，使其支持 Sparkplug 协议。

### 在 EMQX 中创建 Schema Registry

单击 Schema Registry 页面中的创建按钮。

![Schema Registry](https://assets.emqx.com/images/414d1d19937f7b127bf078022516db5b.png)

在**解析类型**下拉框选择 protobuf，并使用 Sparkplug schema 填写 **Schema** 输入框。

![Select the protobuf for **Parse Type**](https://assets.emqx.com/images/92713344955371feef0f189c2714564e.png)

### 在 EMQX 中创建规则

用于解码的 SQL 语句。

```
SELECT
 schema_decode('neuron', payload, 'Payload') as SparkPlugB
FROM
 "spBv1.0/group1/DDATA/node1/modbus"
```

这里的重点是 schema_decode('neuron', payload, 'Payload')：

- `schema_decode()` 根据 Schema 'protobuf_person' 对 payload 字段的内容进行解码。

- `schema_decode()` 把解码得到的值赋给变量 “SparkPlugB”。

- 最后一个参数 `Payload` 指明 payload 里的消息类型是 protobuf schema 里定义的 'Payload' 类型。

![Edit rules](https://assets.emqx.com/images/c86eaf113839e16ac2ef47fe65866ee2.png)

接着添加动作，参数如下：

- 动作类型：消息转发

- 目标主题：SparkPlugB/test

这个动作把解码得到的 “Payload” 以 JSON 格式发布到 SparkPlugB/test 主题。

![Edit action](https://assets.emqx.com/images/a11c438376914cc10bda248d9dbace96.png)

## 安装 Neuron

Neuron 是一个工业物联网平台，可用于收集、存储和分析来自工业设备的数据。您可以从官网下载并安装 Neuron。请访问 [https://www.neugates.io/](https://www.neugates.io/) 并按照文档指引进行操作。

## 在 Neuron 中配置设备

Sparkplug 设备的功能和属性由一组数据点来确定。利用 Neuron 平台，您可以将这些数据点分配给特定设备，从而实现对 Sparkplug 设备进行配置。

为设备选择驱动插件模块。

![Select the driver plugin module for devices](https://assets.emqx.com/images/dee478a56cabf28982d95bc30d15c440.png)

为设备通信设置驱动参数。

![Set up the driver parameters](https://assets.emqx.com/images/95ddaf88bdb5cc305bf8110b9f1ca87c.png)

![Device config](https://assets.emqx.com/images/2da88ff4dddec3ae4ffaca60fa384170.png)

创建组并设置轮询间隔。

![Create group](https://assets.emqx.com/images/aa91471395538ceb7a7edb054f4bff59.png)

为组添加标签，并为每个标签设置地址。

![Add tags](https://assets.emqx.com/images/fb215e69ffcbe4e8ec6d52ac23351935.png)

## 将 Neuron 连接到 EMQX

安装好 Neuron 后，需要将其连接到 EMQX Broker。通过配置 Neuron 中的 MQTT 连接设置，可以将其指向 EMQX Broker。

选择北向通信驱动（SparkplugB）。

![Add app](https://assets.emqx.com/images/8a9ee5ab1a09cb5d70a62999e745722c.png)

为 EMQX 连接设置驱动参数。

![Set up the driver parameters](https://assets.emqx.com/images/c629e130b36ac53f66a21d9adfd8689a.png)

![App config](https://assets.emqx.com/images/64cbe0d49c98ab3dc482b6686f337223.png)

订阅您感兴趣的组。

![Add subscription](https://assets.emqx.com/images/a0f825a4446a6ab52153ec0a5da06efd.png)

## 在 MQTTX 中查看结果

EMQX 和 Neuron 配置并连接成功后，您就可以发布和订阅 Sparkplug 数据了。您可以利用 Neuron 平台给 Sparkplug 设备发送数据，也可以订阅这些设备的数据。

我们使用 [MQTTX](https://mqttx.app/) 客户端工具来订阅 EMQX 规则引擎的编解码功能解码出来的数据，如下图所示：
![MQTTX SparkplugB](https://assets.emqx.com/images/38691752e5463c39951eddec129f91be.png)

## 结语

通过以上步骤，您就可以利用 EMQX 和 Neuron 入门 MQTT Sparkplug。本文只是一个基础的介绍，您还可以利用更多高级的功能和配置定制您的解决方案。我们强烈建议您进一步探索 EMQX 和 Neuron 的强大功能，以助力您的工业物联网开发。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
