## **引言**

在工业 4.0 的浪潮中，将来自 OT（运营技术）层的实时设备数据与 IT（信息技术）层的云端应用无缝对接，是释放数据潜能、实现智能制造的关键。

作为工业自动化领域的基石，西门子 S7-1200 PLC 包含海量生产状态和设备参数。如何高效、可靠地将这些 OT 数据实时传输到 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，以供 MES、SCADA 或云端 AI 分析平台使用，是许多企业面临的核心挑战。

传统解决方案通常涉及复杂的编程和协议转换，既耗时又费力。现在，借助强大的工业边缘网关软件 NeuronEX，您可以在 10分钟内轻松构建从西门子 S7-1200 PLC 到 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的稳定数据桥梁，且无需任何代码。

本文将逐步演示「从 PLC 设置到查看 MQTT 客户端中的数据」的完整配置过程。

## **架构**

本教程旨在从西门子 S7-1200 PLC 中读取指定的变量数据，以 JSON 格式将数据发送到指定的 MQTT Broker 中，并通过客户端软件 [MQTTX](https://mqttx.app/zh) 进行数据验证。技术架构由三个核心组件构成：

- **数据源**：西门子 S7-1200 PLC
- **数据采集软件**：NeuronEX（负责数据采集、处理与转发）
- **数据目的地**：EMQX（本文以公共 `broker.emqx.io` 为例）
- **MQTT 客户端工具**：MQTTX

![image.png](https://assets.emqx.com/images/29cec6d0b4ec0f9ca7a5dcceeee4aacd.png)

## **前提条件**

在开始之前，请确保您已准备好：

- 西门子 S7-1200 PLC 及 博途 (TIA Portal) 编程软件。

- NeuronEX：通过 Docker 快速部署，只需一条命令。

  ```shell
  # 启动 NeuronEX
  docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:latest
  ```

- MQTT 客户端：使用 [MQTTX](https://mqttx.app/zh)，用于后续验证数据。

## **将西门子 S7-1200 PLC 连接到 MQTT**

### **第一步：配置西门子 S7-1200 PLC** 

为了允许 NeuronEX 访问 PLC 数据，请确保 NeuronEX 与 S7-1200 之间的网络畅通。我们将使用 NeuronEX 从西门子 S7-1200 的数据块（DB2）和 M 区采集数据。

需要从数据块（DB2）采集的点位如下图红框中所示：

![image.png](https://assets.emqx.com/images/2b92714de954ce6bfebec033fa4caa0c.png)

### **第二步：在 NeuronEX 中添加南向设备**

现在，让我们告诉 NeuronEX 从哪里去读取数据。

1. 访问 `<http://localhost:8085`> 进入NeuronEX 管理界面。
2. 点击「**数据采集** → **南向设备**」页面下的「**添加设备**」，选择「**Siemens S7 ISOTCP**」插件。
3. 填写设备信息：
   - **名称**：`S7-1200-Workshop`
   - **目标设备 PLC IP 地址**：输入您 PLC 的 IP 地址。
   - 其他参数保持默认即可。

![image.png](https://assets.emqx.com/images/3123ad68be9fc36b7934289b6a7517ed.png)

### **第三步：创建采集点位** 

这是定义「要收集什么数据」的核心步骤。

1. 点击新创建的 `S7-1200-Workshop` 驱动，进入「**组列表**」页面，创建名为 `group1` 的采集组。
2. 进入采集组并开始「**添加点位**」，根据您 PLC 中的地址，精确添加如下点位：

| 数据类型          | PLC 地址示例 | NeuronEX 配置                           | 地址格式说明                      |
| ----------------- | ------------ | --------------------------------------- | --------------------------------- |
| **布尔型 (Bit)**  | `M10.0`      | **类型**: `BIT`, **地址**: `M10.0`      | `M`区，第 10 个字节的第 0 位。    |
| **整型 (Int)**    | `MW20`       | **类型**: `INT16`, **地址**: `MW20`     | `M`区，起始地址为 20 的字(Word)。 |
| **浮点型 (Real)** | `MW30`       | **类型**: `FLOAT`, **地址**: `MW30`     | `M`区，起始地址为 30 的双字。     |
| **DB 块数据**     | `DB2.DBW4`   | **类型**: `INT32`, **地址**: `DB2.DBW4` | DB2中，起始地址为 4 的字。        |

![image.png](https://assets.emqx.com/images/892967caef59c43e8d740314773ae7d6.png)

### **第四步：监控数据收集**

完成第三步以后，您可以在「**南向设备**」页面，实时查看` S7-1200-Workshop` 驱动的实时状态，状态为「连接」则表示 NeuronEX 与 S7-1200 之间连接正常。

![image.png](https://assets.emqx.com/images/99f732172fe7e2a4cda70d671663a157.png)

您可以在「**数据采集** -> **数据监控**」页面实时查看这些点位的值，可以看到 tag4 的值 `-123` 与博途软件中的值相同。

![image.png](https://assets.emqx.com/images/30234a9c912c447b8044badb0d371f99.png)

### **第五步：配置北向 MQTT 应用**

最后，我们来配置数据的「目的地」。

1. 在左侧菜单中选择「**北向应用** -> **添加应用**」，添加北向 MQTT 应用。

2. 选择「**MQTT**」插件，配置 MQTT 连接参数：

   - **名称**：`emqx`
   - **服务器地址**： `broker.emqx.io` ([公共MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker))
   - **端口**：`1883`
   - 其他使用默认配置即可

3. 单击「**创建**」。

   ![image.png](https://assets.emqx.com/images/aeb5deaa28a11e9bed21cbe080648bf6.png)

1. 创建好 MQTT 应用后，点击「**添加订阅**」按钮。

   ![image.png](https://assets.emqx.com/images/5fc1dee2b50c0d81d9d007302b9ca143.png)

1. 将南向驱动 `S7-1200-Workshop` 的采集组添加进订阅，其中上报的 MQTT 主题设置为 `neuronex/s7-1200/data`。

   ![image.png](https://assets.emqx.com/images/52643e09b7f9e686f614bcfc32b6d4bf.png)

### **第六步：订阅并验证数据** 

这是打通数据流的最后一步。

1. 打开您的 MQTTX 客户端，新建连接到 `broker.emqx.io:1883`，订阅主题 `neuronex/s7-1200/data`。
2. 您将看到 NeuronEX 采集到的 PLC 数据以标准的 JSON 格式持续推送到 MQTTX 中。

## **结语**

恭喜！您已成功使用 NeuronEX 在 10 分钟内将西门子 S7-1200 PLC 连接到 MQTT。整个过程无需任何代码，只需通过简单的 Web 界面进行配置，就为工业数据收集和云集成建立了稳定高效的通道。

这展示了 NeuronEX 作为现代工业边缘网关的强大能力：既可以深入 OT 层，精细处理设备协议和数据标签，又能与 IT 世界无缝集成，轻松将数据送达到云端。

立即下载 NeuronEX，开启您的工业物联网智能之旅：[下载 NeuronEX](https://www.emqx.com/zh/downloads-and-install/neuronex)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
