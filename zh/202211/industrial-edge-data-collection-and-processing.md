对接繁杂多样的工业协议、对海量设备产生的生产数据进行采集和处理一直是工业领域智能化推进的难点。EMQ 通过提供边缘工业协议网关软件 Neuron 和边缘流式处理引擎 eKuiper，分别解决了边缘侧设备数据的采集与处理。

之前，要想实现两个产品的协同工作，需要额外部署 MQTT broker 进行中转，对于用户来说步骤较为繁琐。自 eKuiper 1.5.0 和 Neuron 2.0 版本开始，两者实现了集成整合，用户可在 Neuron 中直接添加对应的北向应用节点与 eKuiper 进行通信。此前我们曾介绍过如何在 eKuiper 1.5.0 中借助 Neuron source 和 sink，在无需配置的情况下[接入 Neuron 采集到的数据并进行计算](https://www.emqx.com/zh/blog/industrial-iot-data-collection-cleaning-and-control)。

随着 Neuron 2.1 和 2.2 版本的相继发布，用户体验变得更加便捷：通过内置的 data-stream-processing 节点，用户甚至无需手动添加 eKuiper 节点，直接订阅 group 即可实现通信；通过代理 eKuiper 的 API，Docker 运行 Neuron 2.2 时不再需要映射 9081 端口。这些都将帮助大家更快速轻松地享受 Neuron+eKuiper 的工业协议接入与流式数据分析处理能力，实现生产数据的互联互通，挖掘边缘数据价值。

本文将以最新的 2.2 版本为例，详细介绍如何在 Neuron 中利用 eKuiper 将采集的设备端生产数据进行计算后发送到云端，以及 eKuiper 接收云端指令后通过 Neuron 反控设备的流程。


## Neuron 与 eKuiper 通信机制

当前 Neuron 的 ekuiper 插件的实现使用了 NNG 库的 pair0 协议，通过 IPC 传输层与 eKuiper 通信，其中`data-stream-processing`北向节点作为服务器，eKuiper 作为客户端。由于 NNG 的 pair0 协议是一种点对点的协议，ekuiper 插件只允许实例化单个北向节点，并且因为使用的是 NNG 的 IPC 传输层，所以 eKuiper 需要与 Neuron 部署在同一机器中。

### Neuron 上报数据到 eKuiper

在 Neuron 中通过`data-stream-processing`北向节点订阅南向设备节点，被订阅设备的点位数据经 NNG 的 IPC 传输层上报给 eKuiper。上报的数据为固定的 JSON 格式，如下所示：

```
{
  "timestamp": 1646125996000,
  "node_name": "node1", 
  "group_name": "group1",
  "values": {
    "tag_name1": 11.22,
    "tag_name2": "string"
  },
  "errors": {
    "tag_name3": 122
  }
}
```

其中，`"node_name"`域和`"group_name"`域分别是数据所属的节点名和组名。读取成功的点位数据以字典形式放在`"values"`域，点位名为键，点位数据为值。读取失败的点位数据以字典形式放在`"errors"`域中，点位名为键，错误码为值。

### eKuiper 反控 Neuron

eKuiper 可以在数据处理后对 Neuron 进行反控。Neuron `data-stream-processing`北向节点收到数据后将其写入南向节点。

eKuiper 发往 Neuron 的数据需为符合以下格式的 JSON 数据：

```
{
    "node_name": "node1",
    "group_name": "group1",
    "tag_name": "tag_name1",
    "value": 1234
}
```

其中，`"node_name"`域和`"group_name"`域分别是数据所属的节点名和组名，`"tag_name"`域为点位名，`"value"`域为要写入的点位数据。

## 使用 eKuiper 对 Neuron 采集的数据进行处理

本节将通过一个简单的例子介绍如何使用 eKuiper 对 Neuron 采集的数据进行处理。

在这个例子中，我们会通过 Neuron 界面配置两个点位`tag1`和`tag2`，配置一条 eKuiper 规则：当`tag1`的值超过`42`时，将`tag2`的值置 1。对应到实际场景中，`tag1`可以是对应着一个传感器（如温度传感器），`tag2`可以是对应着一个驱动器（如开关）。

### 部署 Neuron

Neuron 2.1 出于便利性考虑，在所支持的二进制安装包和 Docker 镜像中集成了 eKuiper 并为其添加了一个默认流`neuronStream`。Neuron 前端界面也增加了相应功能以支持和 eKuiper 交互，进行规则的添加、更新、删除等常规操作。因此用户无需另外安装 eKuiper，并且可以直接使用流`neuronStream`。Neuron 2.2 版本代理了 eKuiper 的 API，因此 Docker 运行时无需再映射 9081 端口。本节样例采用 Docker 容器部署方案。

运行如下命令启动 Neuron：

```
$ docker run -d                \
             -p 7000:7000      \
             -p 7001:7001      \
             --name neuron     \
             --privileged=true \
             emqx/neuron：2.2.8
```

以上命令暴露了几个端口，`7000`和`7001`是 Neuron 的 RESTFul API 端口。

### 添加南向节点

Neuron 启动之后，我们需要为 Neuron 添加一个 Modbus 南向设备，然后启动模拟器进行模拟数据采集。

南向设备和模拟器配置，请参考 [Neuron 快速教程](https://neugates.io/docs/zh/v2.1/getting-started/quick_start.html#资源准备) ，完成到《运行和使用》中的“第九步，管理组的数据标签”之后，便可获得本例使用的两个点位配置，如下图所示：

![添加南向节点](https://assets.emqx.com/images/a71997407b435a6a82206aac3084688f.png)

### 启动数据流处理应用节点

北向应用管理界面中将有一个默认的`data-stream-processing`节点卡片，如下图所示。

![北向应用管理](https://assets.emqx.com/images/139f8e9a7201352f4965796bbb63efc1.png)

点击 `data-stream-processing` 应用节点开始按钮，启动该节点。

### 订阅南向标签组

点击 `data-stream-processing` 应用节点任意空白处，进入订阅 Group 的界面，如下图所示。

![订阅南向标签组](https://assets.emqx.com/images/aa9197bd27a62636dedd2762145874b3.png)

订阅南向设备的数据组：

1. 点击右上角`添加订阅`；
2. 点击下拉框，选择南向设备，本例中选择上一步构建的`modbus-tcp-1`；
3. 点击下拉框，选择要订阅的 Group，本例中选择上一步构建的 `group-1`；
4. 点击`提交`按键完成订阅。

完成这一步后，`data-stream-processing` 北向节点就能采集到`modbus-tcp-1` 南向节点的数据，并将其转发到 eKuiper 进行处理。

### 添加规则

点击`新建规则`，如下图所示。

![新建规则](https://assets.emqx.com/images/e7965d47697ab6b9373dacb998a7b8ed.png)

在规则编辑界面，填写规则信息，如下图所示。

![填写规则信息](https://assets.emqx.com/images/e8b5acde85a33b256c922b1d6fb31b92.png)

1. 填写 `Rule ID` 
2. 填写`SQL` ：
   `SELECT node_name, group_name, 1 as tag2 FROM neuronStream WHERE values->tag1 > 42`
3. 点击`添加` ，为规则添加 sink 动作，每条规则可添加多条 sink 动作，详见下一步；
4. 点击`提交` 完成规则的定义。

在添加动作的弹窗里设置 sink 的详细信息， 如下图所示。

![设置 sink 的详细信息](https://assets.emqx.com/images/ed6e6efcb45537f19532b160a6f8c940.png)

1. 下拉选择 Sink；
2. 填写节点名称；
3. 填写分组名称；
4. 填写标签字段；
5. 选择 `提交` 完成 sink 动作的添加

### 启动规则

启动规则，如下图所示。

![启动规则](https://assets.emqx.com/images/1c66b7abb96b7490400ce2d441ca8644.png)

### 触发规则

打开 Neuron 数据监控页面，可以看到从模拟器读到的`tag1`和`tag2`的初始值均为 0。

![触发规则](https://assets.emqx.com/images/e0e68557bc50b77ccdc395daff61d82b.png)

在模拟器中将`tag1`的值写为`43`， Neuron 读取到更新的点位值后，`data-stream-processing`节点将其上报给 eKuiper，而这就会触发之前设置的规则，继而使 eKuiper 发送一条写指令将`tag2`的值写为`1`。如下图数据监控页面所示，`tag1`的值为`43`，`tag2`的值为`1`。

![触发规则](https://assets.emqx.com/images/67acf29c4f78794b77f74874d664a50b.png)


## 结语

本文演示了使用 Neuron 与 eKuiper 进行边缘数据采集与处理的详细流程。通过两者的整合使用，工业领域用户可以实现一站式云边协同的数据采集、清理和反控，为打造[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)数据中心奠定基础。





<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
