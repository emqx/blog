我们非常高兴地宣布，工业边缘网关软件 **NeuronEX 3.5.0** 版本正式发布！NeuronEX 致力于为用户提供更高效、更灵活的工业数字化转型解决方案。本次更新带来了多项新功能和优化，进一步提升了 NeuronEX 在工业数据采集、边缘计算和数据处理方面的能力，让我们一起来看看这个版本的亮点。

## 新增南向驱动，扩展数据采集能力

NeuronEX 3.5.0 新增了两个重要的南向驱动，进一步扩展了其在工业设备数据采集方面的能力：

1. **凯恩帝 CNC 驱动**：支持与凯恩帝 CNC 系统的数据采集，适用于制造业中数控机床设备采集场景。[KND CNC | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/knd/knd.html) 
2. **Mitsubishi 4E 驱动**：支持三菱 iQ-F 系列和 IQ-R 系列 PLC 的数据采集，适用于自动化生产线和工业控制场景。[Mitsubishi 4E | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/mitsubishi-4e/overview.html) 

这些新增驱动使 NeuronEX 能够与更多类型的工业设备无缝集成，为用户提供更广泛的数据采集选择。

## MQTT 驱动功能增强

MQTT 驱动在 3.5.0 版本中得到了多项功能增强，进一步提升了其在工业互联中的应用能力：

1. [**支持自定义数据上报格式**](https://docs.emqx.com/zh/neuronex/latest/configuration/north-apps/mqtt/api.html#custom-自定义格式)：MQTT 插件将采集到的数据以 JSON 形式发布到 MQTT Broker指定的主题。 上报数据的具体格式由**上报数据格式**参数指定，有**Values-format 格式、Tags-format 格式、ECP-format 格式、Custom 自定义格式**多种格式可选。用户可以通过**Custom自定义格式**上报MQTT 数据，满足不同应用场景的需求。

   ![image.png](https://assets.emqx.com/images/2ee6b969ffb078004ff542e277e4e820.png)

1. [**支持配置静态数据点位**](https://docs.emqx.com/zh/neuronex/latest/configuration/north-apps/mqtt/api.html#静态点位)：可为不同南向驱动采集组分别配置设备静态点位数据，在数据MQTT上报时，自动上报该信息。

   ![image.png](https://assets.emqx.com/images/2b5a4bcd6895cf5520b38b9933efc579.png)

1. **支持国密加密**：MQTT 驱动现在支持国密加密，满足国内用户对数据安全的高要求。（需由 EMQ 单独提供安装包）

## OPCUA 驱动功能优化

OPCUA 驱动在 3.5.0 版本中得到了多项功能优化，提升了其在工业自动化中的应用能力：

1. **支持扩展对象类型（Object Extension）采集**：用户可以通过 OPCUA 驱动采集扩展对象类型的数据，满足复杂工业场景的需求。
2. **优化点位浏览功能**：NeuronEX 提供了点位发现功能，帮助用户高效管理 OPC UA 设备的点位。通过扫描 OPC UA 服务器地址空间，用户可以快速发现并添加点位到采集组，实时监控数据，并导出点表以便本地编辑和使用。

![image.png](https://assets.emqx.com/images/37d8f44145b19e0c56998646bc7ac8c1.png)

## IEC61850 驱动功能更新

IEC61850 驱动[IEC61850 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/iec61850/overview.html) 在 3.5.0 版本中得到了显著的功能增强，适用于电力行业的自动化系统：

1. **支持总召唤上报、采集组定时上报、数据变化上报三种模式**：用户可以根据需求选择不同的数据上报模式，灵活应对不同的应用场景。
2. **支持 CID 文件导入**：通过导入 CID 文件，NeuronEX 可以自动根据控制报告块中的内容生成为采集点表 ，简化配置流程。
3. **调整数据上报格式**：IEC61850 驱动根据行业规范，单独定义了数据上报结构，在每个数据点位中，除了点位值外，还包含 `timestamp`、`quality` 字段。

![image.png](https://assets.emqx.com/images/a1c2b48470917bfb63c461f619ee7105.png)

## ModbusTCP 驱动支持主备双 Server

ModbusTCP 驱动在 3.5.0 版本中新增了主备双 Server 配置功能，用户可以通过配置主备双 ModbusTCP Server 来提高系统的可靠性和容错能力，确保在主服务出现故障时，系统能够自动切换到备用服务，保证数据采集的连续性。

## 数据处理功能增强

NeuronEX 3.5.0 在数据处理方面也进行了多项功能增强，进一步提升了其在边缘计算和数据分析方面的能力：

1. **支持 ONNX 插件集成**：用户可以通过 ONNX 插件集成机器学习模型，实现边缘侧的智能数据分析。详细ONNX 插件的使用，欢迎查阅我们的文档[ONNX 插件使用 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/streaming-processing/onnx.html) 

2. **SQL 编辑器支持关键词提示**：SQL 编辑器现在支持关键词提示功能，支持自动补全关键字及内置函数，鼠标悬停内置函数，可查阅函数详细用法，帮助用户更高效地编写 SQL 查询语句。

   ![image.png](https://assets.emqx.com/images/6358e284d26c2c8d46d8d2cd8b74d808.png)

1. **规则功能新增支持增量窗口计算**：用户可以通过增量窗口计算功能，实时处理和分析数据流中的增量数据。
2. **规则通用配置项支持 SendNilField 配置项**：用户可以通过配置 SendNilField 选项，控制是否发送空值字段，满足不同的数据处理需求。
3. [**规则调用外部函数超时时间可配置**](https://docs.emqx.com/zh/neuronex/latest/admin/conf-management.html#环境变量映射为配置文件)：用户可以根据需求配置规则调用外部函数的超时时间，提高系统的灵活性和稳定性。
4. **Video 数据源新增视频格式及视频编码配置项**：用户可以根据需求配置视频格式和编码选项，满足不同的视频处理需求。

## 结语

NeuronEX 3.5.0 版本通过新增驱动支持、增强 MQTT 和 OPCUA 等驱动功能，并优化数据处理功能，进一步提升了其工业数据采集与处理的能力。这些改进将帮助用户更高效地管理工业设备，处理海量数据，并实现更智能的工业自动化。

我们诚挚地邀请您试用 NeuronEX 3.5.0 版本，体验这些激动人心的新功能。同时，感谢您一直以来对 NeuronEX 的支持与信任，我们期待收到您的反馈和建议，并不断改进产品。

立即下载 NeuronEX 3.5.0 版本，开启您的工业数字化转型之旅： [https://www.emqx.com/zh/try?tab=self-managed](https://www.emqx.com/zh/try?tab=self-managed) 

NeuronEX 3.5.0 的完整功能，请查阅文档：[产品概览 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
