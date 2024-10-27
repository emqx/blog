我们很高兴地宣布，工业边缘网关软件 NeuronEX 3.4.0 版本现已正式发布！这次更新带来了多项重要的新功能和改进，进一步增强了 NeuronEX 在工业数据采集、边缘计算和管理方面的能力。让我们一起来看看这个版本的亮点。

## 新增驱动

本次更新新增了多个重要的南向驱动，扩展了 NeuronEX 的数据采集能力：

**DNP 3.0**：支持广泛应用于电力系统自动化的 DNP3 协议。[DNP 3.0 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/dnp3/dnp3.html) 

**HollySys Modbus TCP 和 RTU**：支持和利时 LK/LE 系列 PLC 的数据采集。[Modbus TCP | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-hollysys-tcp/modbus-hollysys-tcp.html) 

**Allen-Bradley 5000 EtherNet/IP**：支持 Allen-Bradley ControlLogix 5xxx 系列，以及 CompactLogix 5xxx 系列 PLC 的数据采集。[Allen-Bradley 5000 EtherNet/IP | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/ab-5000/ab-5000.html) 

**Allen-Bradley DF1**：支持与使用 DF1 协议 Allen-Bradley PLC 的数据采集。[Allen-Bradley DF1 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/df1/df1.html) 

这些新增驱动使 NeuronEX 能够与更多种类的工业设备和系统进行无缝集成，为用户提供更广泛的数据采集选择。

## 驱动功能优化

对多个现有驱动进行了功能优化：

**1、MQTT 驱动支持上报南向驱动状态到 MQTT 主题，使用户能够更方便地监控驱动状态。**

![驱动状态上报](https://assets.emqx.com/images/5bfc4c21aee0e660286f9b001e810699.png)

**2、MQTT 驱动新增对 MQTT 5.0 版本的支持。**

**3、Focas 驱动优化了 PMC 读取功能。**

**4、DLT645 驱动新增支持读取 05 地址区数据。**

**5、ModbusTCP、Inovance Modbus TCP 驱动增加了"是否开启报文头校验"参数。**

**6、ModbusTCP、ModbusRTU 驱动新增设备降级功能。**

使用详情请查阅 [Modbus TCP | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-tcp/modbus-tcp.html#设备配置) 

这些优化提高了相关驱动的性能和可靠性，为用户提供更稳定的数据采集体验。

## 数据处理能力提升

NeuronEX 3.4.0 版本在数据处理方面也有重大改进：

**1、新增连接管理功能：**支持配置 MQTT、SQL 连接器，并支持自动重连。

![连接管理功能](https://assets.emqx.com/images/a43a73a64f3d21f8e4b69df9e8c9d40c.png)

> 在连接器功能方面，NeuronEX 做了兼容性处理，支持从老版本 NeuronEX 导出规则，并在 NeuronEX 3.4上导入使用，规则仍能够正常运行。 同时也支持用户添加连接器，并手动修改 Source 和 Sink 配置。

**2、File 数据源支持读取电力行业 CIME 文件。**

**3、Source/Sink 算子拆分，提供更灵活的数据处理选项。**

**4、增加规则统计指标，并支持在规则停止后仍然查看运行指标。**

**5、Portable 插件增加状态和错误信息显示。**

这些改进大大增强了 NeuronEX 的数据处理能力，使用户能够更高效地管理和分析工业数据。

## 系统功能增强

**1、支持 NeuronEX 完整备份和恢复功能，提供更便捷的配置迁移能力。**

![备份和恢复](https://assets.emqx.com/images/c7e22f20b5a4c08e910dcd0486d3c905.png)

**2、UI 支持密码隐藏，增强安全性。**

![密码隐藏](https://assets.emqx.com/images/27d11ad4843b87629b86779b8423f1bf.png)

**3、支持在启动时选择是否启动数据处理引擎，提供更灵活的部署选项。**

使用详情请查阅配置文件`/opt/neuronex/etc/neuronex.yaml`中`disableKuiper` 配置项。

**4、NeuronEX 支持 HTTPS API，提高 API 调用的安全性。**

使用详情请查阅[配置管理 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/admin/conf-management.html#https-功能使用) 

**5、支持在配置文件中修改启动 admin 密码和 Viewer 账号，增强安全管理。**

使用详情请查阅[配置管理 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/admin/conf-management.html#配置文件) 

**6、配置文件参数支持映射为环境变量使用，提供更灵活的配置方式。**

使用详情请查阅[配置管理 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/admin/conf-management.html#环境变量映射为配置文件) 

## 链路追踪功能

NeuronEX 3.4.0 引入了全新的链路追踪功能，支持以下场景：

**1、MQTT 下行控制指令追踪**

NeuronEX 可结合 EMQX V5 对应用端下发的 MQTT 控制指令进行全链路追踪，监测全链路指令控制时延，分析各节点的时延信息，应用于对控制延迟要求较高的场景，进行故障分析。

**2、NeuronEX API 下行控制指令追踪**

可记录 NeuronEX API 下发控制指令的详细过程，分析 NeuronEX 发送指令到设备到收到设备响应的完整链路和时延，应用于对控制指令下发的可靠性要求较高的场景，进行故障分析。

**3、数采链路追踪**

可记录数据采集、数据计算以及结合 EMQX 的数据链路追踪，应用于采集延迟检测、数据丢失检测等场景。

**4、边缘计算数据追踪**

可记录边缘计算过程中每个算子计算的详细过程，以及在各个算子数据处理后的数据结果。

NeuronEX 通过与集成了 OpenTelemetry 服务的 EMQX ECP 组合使用，大大提高了系统的可观测性，使用户能够更容易地诊断问题和优化性能。

![边缘计算数据追踪](https://assets.emqx.com/images/22e2fd447eed58e07daffb54cba58f15.png)

## 其他改进

1、南向驱动和北向应用页面支持分页显示驱动节点信息，提高有大量节点使用时的用户体验。

2、支持通过环境变量将日志输出到 console 控制台，方便在容器化环境中查看日志。

## 结语

NeuronEX 3.4.0 版本通过新增驱动支持、增强数据处理能力、改进系统功能和引入链路追踪等特性，全面提升了其在工业数据采集与处理领域的能力。这些改进将帮助用户更高效地管理工业设备，处理海量数据，并实现更智能的工业自动化。

我们诚挚地邀请您升级到 NeuronEX 3.4.0 版本，体验这些激动人心的新功能。同时，感谢您一直以来对 NeuronEX 的支持与信任，我们期待收到您的反馈和建议，并不断改进产品。

立即下载 NeuronEX 3.4.0 版本，开启您的工业数字化转型之旅： [下载 NeuronEX](https://www.emqx.com/zh/try?tab=self-managed) 

NeuronEX 3.4.0 的完整功能，请查阅文档：[产品概览 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/) 



<section class="promotion">
    <div>
        免费试用 NeuronEX
    </div>
    <a href="https://www.emqx.com/zh/try?tab=self-managed" class="button is-gradient">开始试用 →</a>
</section>
