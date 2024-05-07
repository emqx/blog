工业企业要实现数据驱动的新质生产力升级，一个重要的环节便是如何准确、可靠地收集并利用生产过程中的数据流。

[NeuronEX](https://www.emqx.com/zh/products/neuronex) 工业边缘软件中的规则调试功能，可帮助用户在安全的环境中模拟数据输入，测试和优化数据处理规则，从而提前发现并解决潜在问题。规则调试功能对于实现智能制造、远程监控和预防性维护等应用尤为关键，能够有效提升生产效率，降低运营成本，同时保障系统的稳定性和安全性。

作为一款专为工业场景设计的工业边缘网关软件，NeuronEX 提供设备数据采集和边缘智能分析服务。该软件主要部署在工业现场，可支持多种工业设备通信及工业总线协议的实时数据采集。NeuronEX 能够实现工业系统数据集成、边端数据过滤分析、AI 算法集成，以及工业互联网平台的对接集成等功能，为工业用户提供低延迟的数据接入管理及智能分析服务，帮助用户快速洞悉业务趋势，提升运营效率和业务可持续性。

NeuronEX 具备强大的多协议接入能力，支持如 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication)、[OPC UA](https://www.emqx.com/zh/blog/opc-ua-protocol)、Ethernet/IP、BACnet、Siemens、Mitsubishi 等数十种工业协议的同时接入，实现企业内 MES（制造执行系统）、WMS（仓库管理系统）等多数据源系统的集成对接。

本文将重点介绍 NeuronEX 的规则调试功能，旨在帮助用户更高效地进行规则的调试和创建。

![NeuronEX](https://assets.emqx.com/images/eba89324c09f2d60ef735fad20e482b4.png)

## 准备工作

在开始调试规则之前，需要创建一个数据源，作为规则的数据输入流。以 MQTT 类型的数据源作为示例，操作步骤如下：

1. 登录到 NeuronEX 系统，进入“数据处理” - “源管理”页面。在“流管理”区域，点击“创建流”按钮。

   ![源管理](https://assets.emqx.com/images/1a412a3098af03ca6cbd49c7febecc14.png)

1. 选择 MQTT 类型，然后点击“下一步”按钮，进入到流配置页面。

   ![创建流](https://assets.emqx.com/images/532643d16b446e3db3bae6f10ef13d42.png)

1. 在流配置页面里，填入流名称和数据源。其它配置信息可保留默认值。数据源应填入计划订阅的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)，以便区分不同的数据流。例如，可以填入 `neuronex/rule_test`，点击“添加配置组”按钮以创建新的配置组。

   ![流配置页面](https://assets.emqx.com/images/0d05337851613589f08ec4b7b568f19a.png)

1. 在源配置组里，填入配置组名称和 MQTT 消息服务器地址。此次演示中，服务器地址使用由 EMQX 提供的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务器是由 EMQX 的 [MQTT 接入平台](https://www.emqx.com/zh/cloud)提供，然后点击“提交”按钮，完成配置组的添加。

   ![源配置组](https://assets.emqx.com/images/68a808ccff7da682a46e6f79568475c8.png)

1. 配置组添加完成后，可看到配置组中已选中刚才添加的 `mqtt_conf` 配置组，接着点击“提交”按钮即可完成数据源的创建。

   ![完成创建](https://assets.emqx.com/images/fe142811c621cae264adbc1d433929fa.png)

## 利用模拟数据源进行规则调试

接下来进入本文核心环节，规则调试：

1. 进入“数据处理” - “规则”页面，点击“新建规则“按钮来创建一条规则。

   ![规则页面](https://assets.emqx.com/images/4153e9ab22a349ff2b07cd83368964c5.png)

1. 在规则新建页面，将默认的数据源替换为之前创建的 MQTT 类型数据源 `mqtt_stream`。接着，点击“模拟数据源”按钮来配置模拟数据源。

   ![规则新建页面](https://assets.emqx.com/images/ec78c8f253d6862cf9addc7a9d95260f.png)

1. 在模拟数据源对话框中，“选择 SQL 中模拟数据源”为我们需要模拟的数据源 `mqtt_stream`，如果 SQL 语句涉及多个数据源，可通过右侧的加号按钮按需添加。在 “payload” 区域填入要模拟的 JSON 数据，支持模拟多条 JSON 数据。设置“发送间隔”以确定每条 JSON 数据的发送频率。启用“循环发送”功能，可让 payload 中定义的 JSON 数据持续循环发送。若有多条 JSON 数据，则会按顺序逐条循环发送。请确保模拟数据源已开启，即红框内容显示为“关闭模拟数据源”。完成配置后，点击“保存”按钮。

   ![模拟数据源](https://assets.emqx.com/images/213a52d3881f5967548bb69e2664a4aa.png)

1. 配置好模拟数据源后，即可开始进行规则调试。点击页面右侧的运行测试按钮。运行后，在输出结果中可看到循环输出上一步配置的两条 JSON 数据。如需暂停调试，点击右侧停止按钮；若要清除输出结果，点击清除按钮。

   ![规则调试](https://assets.emqx.com/images/218a3806b0c56d2a7b170e89aa842fdc.png)

1. 接下来进行一些简单的规则应用。首先，停止测试并清除输出结果。然后，对 SQL 语句稍作修改，使 SELECT 语句仅查询 `a` 属性。修改完成后，再次点击运行测试按钮，输出结果现在就只包含 `a` 属性的数据，充分展示了规则调试的灵活性和便捷性。

   ![调试规则](https://assets.emqx.com/images/cf96e524147c13c237977d05aef5fbdf.png)

## 关闭模拟数据源后的规则调试

先前是在利用模拟数据源完成规则调试，接下来，我们将尝试在关闭模拟数据源的情况下进行规则调试。为此，需用到 MQTTX 客户端，向指定的数据源主题 `neuronex/rule_test` 发送消息。

1. 停止当前的测试并清除输出结果。然后在模拟数据源对话框中，点击“关闭模拟数据源”按钮。关闭后，按钮上文字将更新为“启用模拟数据源”。请记得点击“保存”按钮以确认更改。

   ![关闭模拟数据源](https://assets.emqx.com/images/c14607a5f365db7419736e1f98c9aab6.png)

1. 接下来，点击运行测试按钮，运行后可看到尽管测试正在运行，但输出结果中并没有新数据出现。

   ![点击运行测试按钮](https://assets.emqx.com/images/549ae72c99dff051bd7da7c1368826cc.png)

1. 下面打开 MQTTX 客户端，并连接到之前创建的 `mqtt_conf` 配置组中使用的[免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)。建立连接后，向 `neuronex/rule_test` 主题发送三条消息。

   ![MQTTX 客户端](https://assets.emqx.com/images/b571ef8bda4cccfbf6348a0bcbb8ee6f.png)

1. 发送消息后，返回到 NeuronEX 的规则新建页面，可看到输出结果已更新了三条记录，对应 MQTTX 中发送的三条数据。由于 SQL 语句中指定只查询 `a` 属性，因此输出结果中也仅包含 `a` 属性的数据。

   ![输出结果](https://assets.emqx.com/images/7c8fe464b2a6624f18a8cdad621cf20e.png)

## 总结

至此，我们已经完整介绍了 NeuronEX 的规则调试功能。相信大家已经体会到规则调试功能的便捷和强大。通过实践，用户将能够更深入地理解规则调试的强大功能，并将其应用于实际工作中，以提高开发效率和数据处理的灵活性。



<section class="promotion">
    <div>
        免费试用 NeuronEX
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuronex" class="button is-gradient">开始试用 →</a>
</section>
