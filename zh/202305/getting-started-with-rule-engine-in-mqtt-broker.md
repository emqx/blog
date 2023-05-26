## 引言

规则引擎是一种能够根据输入数据按照预设规则进行决策或执行动作的软件系统。本文将向您介绍 [EMQX MQTT Broker](https://www.emqx.io/zh) 的规则引擎功能，并阐述其在 MQTT 消息转换和数据集成方面的重要作用。同时，我们还将提供一份快速入门指南，通过实例帮助您快速上手 MQTT 规则引擎。

## MQTT 的规则引擎是什么？

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种高效可靠的消息传输协议，特别适用于低带宽、高延迟网络（在物联网领域十分常见）。在 [MQTT 的发布/订阅模型](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)中，MQTT Broker 扮演着关键角色，负责接收发布者发送的消息并将其可靠高效地分发给订阅者，确保消息的顺利传递。

MQTT 规则引擎是一种可以针对 MQTT 消息制定和执行规则的组件。该规则引擎具备提取、过滤、加工和转换 MQTT 消息的能力，并且可以在满足特定条件时触发相应的动作。通过规则引擎的应用，可以减少人工干预，提高数据集成和应用开发的效率。

## MQTT Broker 中规则引擎的应用场景

规则引擎在 [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) 中有着广泛的应用，可以实现任务自动化、系统监控、效率提升和安全保障。例如：

- 在智能家居自动化中，规则引擎可以实现一些任务的自动化，比如根据人员进出房间的情况自动开关灯，或者根据不同时间段调节室温。既可以节省能源，也可以让居住者享受更加便捷的生活体验。
- 在工业物联网应用中，它可以监控和控制复杂的系统，比如制造流程或电网。通过制定相应的规则，规则引擎可以发现和处理异常，从而避免设备故障，提高系统性能。
- 在医疗保健行业中，它可以监测患者的健康状态，并及时向医护人员报告可能存在的问题，帮助医护人员更好地关注患者的健康状况，及时采取必要的治疗措施，提高医疗保健的效果和质量。

## EMQX 开箱即用的内置规则引擎

[EMQX](https://www.emqx.io/zh) 是一个开源、高度可扩展的 MQTT Broker，内置了规则引擎组件。它让用户可以用低代码的方式快速构建数据处理的业务逻辑，从而降低了软件架构的复杂度。

我们选择在 Broker 内部嵌入规则引擎功能，而不是依赖 Broker 外部的独立的规则引擎，有两个原因：

- 首先，Broker 内部的规则引擎可以实现更高效和流畅的通信。规则引擎可以直接获取 MQTT 消息，无需额外的通信渠道或协议，这降低了延迟，提升了系统性能。
- 其次，这可以让整个系统的部署和管理更加简单。将规则引擎和 Broker 作为统一的组件部署在一起，无需分别进行集成和管理，从而简化了部署过程，减少了系统复杂度。

## 规则引擎快速入门

这里我们将以 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 为例，以便使用企业版提供的各种数据集成动作和资源。

### 下载 EMQX Enterprise

> 根据您的操作系统类型，在[这里](https://www.emqx.com/zh/try?product=enterprise)下载 EMQX Enterprise。

在下拉列表中选择最新版的 EMQX Enterprise 4.4：

![下载 EMQX Enterprise](https://assets.emqx.com/images/a49d95d395aeedc13c92614bffd3bbf4.png)

**EMQX Enterprise 的默认许可证支持最多 10 个 MQTT 连接**，对于我们体验规则引擎的功能来说已经足够了。如果您需要更多的 MQTT 连接，请点击“下载”按钮下方的链接申请 15 天免费试用。

这里我们以 Ubuntu 20.04 为例，下载 EMQX Enterprise 4.4.17 安装包：

```
$ wget https://www.emqx.com/en/downloads/enterprise/4.4.17/emqx-ee-4.4.17-otp24.3.4.2-1-ubuntu20.04-amd64.zip
$ unzip emqx-ee-4.4.17-otp24.3.4.2-1-ubuntu20.04-amd64.zip
```

接下来，我们启动 EMQX Broker：

```
$ cd emqx
$ ./bin/emqx start
```

### 使用 EMQX Cloud 体验我们的云上 MQTT Broker

如果您不想安装 Linux 操作系统、下载和安装 EMQX，或者执行任何 Linux 命令的话，您可以使用 [EMQX Cloud](https://www.emqx.com/zh/cloud) 来体验规则引擎功能。您只需在网页上进行一些简单的配置即可。

### 配置一条简单规则将 MQTT 消息转发到其它主题

#### 需求

我们假设有个用户名为 “Steve” 的设备周期性地向 `notify` 主题发送 JSON 格式的消息。下面是该设备发送的一条示例消息：

```
{"city": "Stockholm", "value": 21}
```

我们希望从原始消息中提取 `value` 字段值，并用它构造一条带有 `temperature` 字段的新消息，然后根据原始消息中的 `city` 字段值，将新消息动态转发到相应的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)，比如，上述示例消息将被转发到主题 `city/Stockholm`：

```
{"temperature": 21}
```

#### 为规则编写 SQL

既然我们已经明确了需求，就让我们打开 EMQX Dashboard（`http://localhost:18083`）来创建一个规则吧（仪表板的默认用户名/密码是 `admin`/`public`）。

![在 EMQX Dashboard 中创建规则](https://assets.emqx.com/images/d4de7d5894c8daa92637168bdc8c26a7.png)

为了实现上述需求，我们需要编写如下 SQL 语句：

```
SELECT
   payload.city as city,
   payload.value as val
FROM
   "notify"
WHERE
   username = 'Steve'
```

我们只关注主题为 `notify` 的消息，因此在 `FROM` 子句中指定了它。`WHERE` 子句用于筛选出 `username` 字段等于 `Steve` 的消息。

`SELECT` 语句将原始消息中 `city` 和 `value` 字段的值分别赋给了两个新变量：`city` 和 `val`。这两个变量将在接下来创建动作时使用。

#### 为规则绑定 Republish 动作

接下来，我们需要为规则绑定 `Republish` 动作，并设置动作的参数：

- 目标主题：`city/${city}`
- 载荷模板：`{"temperature": ${val}}`

![为规则绑定 Republish 动作](https://assets.emqx.com/images/9bb862e87b3db73d20cb3201abae116a.png)

在前一节中，`SELECT` 语句将 `payload.city` 和 `payload.value` 的值分别赋给了两个新变量：`city` 和 `val`。我们的 `Republish` 动作使用 `${city}` 和 `${val}` 占位符来引用这些变量，规则引擎会在执行时将变量的值替换到相应的位置。

#### 测试规则

规则和动作创建完毕后，我们可以向 Broker 发送满足条件的消息来检验规则是否生效。

我们将使用 [MQTTX](https://mqttx.app/zh) 这款 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)来进行测试。您可以从[这里](https://mqttx.app/)下载并安装它。

首先，我们建立一个 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)，将用户名设为 “Steve”。

![使用 MQTTX 客户端建立一个 MQTT 连接](https://assets.emqx.com/images/9b6675b6e9caca4ca1be0dd1bbbcc187.png)

然后，我们订阅目标主题 `city/Stockholm`，并向 `notify` 主题发送一条消息：

![发布 MQTT 消息](https://assets.emqx.com/images/d0a175b3334b01ae483720b89f925ccf.png)

成功了！我们收到了由规则转发过来的消息：

![成功接收 MQTT 消息](https://assets.emqx.com/images/1a00e6f56a34505b1e01b02a549d8c45.png)

## 结语

MQTT 规则引擎是一种强大的工具，可以根据物联网应用中的特定条件或事件自动触发动作。通过本文的快速入门指南和示例，您可以轻松上手 EMQX 规则引擎，在物联网项目中充分发挥它的优势。

EMQX Enterprise 规则引擎提供了丰富的数据集成动作和资源，可以快速高效地完成大部分与数据处理相关的业务逻辑。我们强烈推荐您自己探索和体验。有关规则引擎 SQL 语法的详细文档，请参考 [Rule SQL 文档](https://docs.emqx.com/en/enterprise/v4.4/rule/rule-engine_grammar_and_examples.html#sql-statement-example)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
