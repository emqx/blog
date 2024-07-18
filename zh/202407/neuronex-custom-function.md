随着数据要素逐渐成为帮助工业企业提升智能化水平的重要助力，如何灵活采集和处理工业数据，并满足用户定制化的数据需求，成为企业数字化建设的焦点之一。

[NeuronEX](https://www.emqx.com/zh/products/neuronex) 是一款专为工业场景设计的边缘网关软件，具备工业设备数据采集、工业各系统数据集成、边端数据过滤分析、AI 算法集成以及数据转发和平台对接等功能，能够为工业场景提供低延迟的数据接入管理及智能分析服务，帮助用户快速洞悉业务趋势，提升运营效率和业务可持续性。

此外，NeuronEX 还支持通过插件、HTTP、gRPC 等多种方式实现自定义函数扩展与 AI 算法集成功能，通过强大的流式计算和分析能力，该功能可以灵活地适应不同的应用场景和用户需求，为智能化的数据分析和处理提供支持。

本文将重点介绍 NeuronEX 的自定义函数功能，旨在帮助用户更灵活地处理数据流，便于进行模块化的软件协作和维护。

### 准备工作

在开始自定义函数之前，需要创建一个数据源，作为输入流入。以 MQTT 类型的数据源作为示例，操作步骤如下：

1. 登录到 NeuronEX 系统，进入“数据处理” - “源管理”页面。在“流管理”区域，点击“创建流”按钮。

   ![“源管理”页面](https://assets.emqx.com/images/44ddb5c3612efa498f641ca05c8ba811.png)

1. 选择 MQTT 类型，然后点击“下一步”按钮，进入到流配置页面。

   ![创建流](https://assets.emqx.com/images/b3c10957a6bea98bce04a25b2f024ee7.png)

1. 在流配置页面里，填入流名称和数据源。其它配置信息可保留默认值。数据源应填入计划订阅的 MQTT 主题，以便区分不同的数据流。例如，可以填入 `neuronex/func_test`，点击“添加配置组”按钮以创建新的配置组。

   ![流配置页面](https://assets.emqx.com/images/a953bce884aa258817f6537f40786c41.png)

1. 在源配置组里，填入配置组名称和 MQTT 消息服务器地址。此次演示中，服务器地址使用由 EMQX 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)「https://www.emqx.com/zh/mqtt/public-mqtt5-broker 」，该服务器是由 EMQX 的 [MQTT 接入平台](https://www.emqx.com/en/cloud)提供，然后点击“提交”按钮，完成配置组的添加。

   ![源配置组](https://assets.emqx.com/images/e47ac326e1537f7b9ee0c3f39731f016.png)

1. 配置组添加完成后，可看到配置组中已选中刚才添加的 `mqtt_conf` 配置组，接着点击“提交”按钮即可完成数据源的创建。

   ![点击提交](https://assets.emqx.com/images/e5583f1243f7e5c8bc88978e9c9b3ce7.png)

### 创建自定义函数

用户通过创建自定义函数，可以灵活实现复杂的数据处理，这里我们举一个简单的例子，通过自定义函数去计算长方形的面积

1. 进入“数据处理” - “算法集成”页面。在“自定义函数”区域，点击“创建自定义函数”按钮。

   ![“算法集成”页面](https://assets.emqx.com/images/42f242e10806e3d714ca84f3fa6943d2.png)

1. 在创建自定义函数页面，填入函数名称和 JavaScript 脚本内容，然后点击“提交”按钮，完成自定义函数的添加。

   ![创建自定义函数页面](https://assets.emqx.com/images/d91bec49935dbb3cf74629494a00ef01.png)

### 在规则中使用自定义函数

创建好的自定义函数，可以很方便地在规则中进行使用，下面我们通过规则调试来验证刚才创建的自定义函数是否生效

1. 进入“数据处理” - “规则”页面，点击“新建规则”按钮。

   ![点击“新建规则”按钮](https://assets.emqx.com/images/2244029f10d9b6cf72ba335b0702678c.png)

1. 在规则新建页面，SQL 编辑器中输入如下内容，然后点击调试规则中的运行测试按钮。需要注意的是 SQL 语句中的 x 和 y，为数据流消息内容中长、宽对应的字段名。

   ![在规则新建页面](https://assets.emqx.com/images/3950ce469d7e41f75717f943c4363503.png)

1. 下面打开 [MQTTX 客户端](https://mqttx.app/zh)，并连接到之前创建的 `mqtt_conf` 配置组中使用的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。建立连接后，向 `neuronex/func_test` 主题定时发送以下格式的消息，其中 x、y 的值是随机生成的，代表长方形的长和宽。

   ![MQTTX 客户端](https://assets.emqx.com/images/49d14ac3da2b49233d3eff564a7e7222.png)

1. 回到 NeuronEX 的规则新建页面，检查调试规则中的打印结果，可看到计算后的面积值 calArea

   ![NeuronEX 的规则新建页面](https://assets.emqx.com/images/aeeeac0031cf7a7a550682a232dbca71.png)

### 总结

至此，我们已经完整介绍了 NeuronEX 的自定义函数功能。通过实践，用户能更深入地理解自定义函数功能的便捷和强大，并将其应用于实际工作中，以满足不同用户的差异化数据需求，提高数据流处理的灵活性和适应性。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
