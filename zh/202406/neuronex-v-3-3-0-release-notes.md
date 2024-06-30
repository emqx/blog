工业边缘网关软件 NeuronEX 3.3.0 版本现已正式发布！本次版本更新在数据采集、分析和管理等方面进行了多项增强和改进，进一步强化了 NeuronEX 在工业互联网领域边缘端的应用能力。

## 新增驱动

**Modbus ASCII**：新增 Modbus ASCII 南向驱动，Modbus ASCII 是 Modbus 协议的一种变体，使用 ASCII 字符来编码数据包。[Modbus ASCII | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-ascii/modbus-ascii.html)

**XINJE Modbus RTU**：新增 XINJE Modbus RTU 南向驱动，该驱动采集信捷 PLC 的数据，支持信捷 XC/XD/XL 系列 PLC 的数据采集。[XINJE Modbus RTU | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-xinje-rtu/modbus-xinje-rtu.html) 

**CODESYS V3 TCP**：新增 CODESYS V3 南向驱动，该驱动通过 TCP 协议访问基于 CODESYS V3 平台打造的 PLC 和 运动控制系统。[CODESYS V3 TCP | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/codesys3/codesys3.html) 

**IEC 60870-5-101**：新增 IEC 60870-5-101 南向驱动，IEC 60870-5-101 是一个国际标准，定义了电力变电站控制和监控系统之间的通信协议。[IEC60870-5-101 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/iec-101/iec-101.html) 

**IEC 60870-5-102**： 新增 IEC 60870-5-102 南向驱动，IEC 60870-5-102 是一套用于电力系统自动化的通讯协议的标准，定义了带有测量和控制装置的远程通信标准。[IEC60870-5-102 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/iec-102/iec-102.html) 

**IEC 60870-5-103**：新增 IEC 60870-5-103 南向驱动，IEC 60870-5-103 是一套用于电力系统自动化的通讯协议的标准，定义了保护装置和控制装置间的数据交换标准。[IEC60870-5-103 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/iec-103/iec-103.html) 

**AWS IoT** ：新增 AWS IoT Core 北向应用，为工业设备通过 MQTT 连接到 AWS 云提供了安全的双向数据通道。[AWS IoT Core | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/north-apps/aws-iot/overview.html) 

**Azure IoT**：新增 Azure IoT Hub 北向应用，提供对 Azure IoT Hub 的便捷接入。[Azure IoT | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/north-apps/azure-iot/overview.html) 

**CAN**：新增 CAN 总线数据源接入，可以接收来自 CAN 协议总线的数据，将原始数据解析为结构化数据。[CAN | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/streaming-processing/can.html) 

## 驱动功能增强

- **OPC UA 驱动支持点位发现**：在创建 OPC UA 驱动后，在设备详情页面下的点位发现 Tab 页 ，可扫描查询 OPC UA Server 下的点位信息，方便后续添加点位。

  ![OPC UA 驱动支持点位发现](https://assets.emqx.com/images/ff1a0047b025cd445dcb1a0f28770e93.png)

- **上传 CNC 文件功能**：针对南向驱动中的 CNC 驱动，NeuronEX 支持 CNC 文件上传功能，可以将 CNC 文件发送到 CNC 设备上。

  ![上传 CNC 文件功能](https://assets.emqx.com/images/4f097ec1b576f7ad421f6663b9e402a1.png)

- **支持点位配置偏移量**：当点位属性为 read 时，支持设置偏移量，此时 `设备原始值 + 偏移量 = 上报值`。当点位读写类型包含 write 时，**偏移量**不可用。**偏移量**仅支持数值类型和浮点数类型的数据点。
- **点位精度优化**：在浮点数默认没有设置精度 `Precision` 的情况下，浮点数点位默认保留 5 位小数位。详细的精度舍入规则，请查阅[创建南向驱动 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/south-devices.html#点位精度) 
- **驱动优化：** 对 OPC UA、DLT 645、IEC 61850、IEC 60870-5-104 等多种驱动进行了功能优化和性能提升。

## 数据处理功能增强

- **新增支持 Javascript 自定义函数**：支持在**数据处理 -> 算法集成**页面上，创建自定义函数。通过创建 JavaScript 函数并在规则中使用，可以快速便捷地实现数据的逻辑计算和格式转换。使用详情请查阅[自定义 JavaScript 函数 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/streaming-processing/js_func.html) 

  ![Javascript 自定义函数](https://assets.emqx.com/images/8120364cb3edbc7bc78f3cfda2edefbc.png)

- **新增 Image 动作**：支持将规则处理后的数据流，以图片形式保存到指定文件夹中。
- **数据源及规则优化：**优化 SQL Source 的参数配置，优化规则重试的默认参数，以及规则状态显示优化等。

## 基于 RBAC 的用户管理

在 NeuronEX 3.3.0 版本中，引入了基于角色的访问控制 （RBAC）功能。RBAC 允许根据用户在组织中的角色分配权限。此功能简化了授权管理，通过限制访问权限提高安全性。NeuronEX 新增管理员和查看者两种角色：

- **管理员 (Administrator)**

  Administrator 拥有对 NeuronEX 所有功能和资源的完全管理访问权限，包括数据采集、数据处理、以及系统配置管理。

- **查看者 (Viewer)**

  Viewer 可以访问 NeuronEX 的所有数据和配置信息，对应 REST API 中的所有 `GET` 请求，但无权进行创建、修改和删除操作。

![基于 RBAC 的用户管理](https://assets.emqx.com/images/9b8b2c8548edd2941a8fc95ac1bcb487.png)

## 用户体验提升

- **数据监控页采集错误点位显示**：数据监控页面以组为单位显示采集点位实时值，点击 `仅展示错误点位` 按钮可只显示错误点位，在点位数据特别多的情况，可快速查看是否有点位采集异常的情况。

  ![数据监控页](https://assets.emqx.com/images/5f2231f6940740af043acd5656782f82.png)

- **点位采集测试**：在**添加点位**页面，支持对新增的点位进行点位读取测试。目前仅支持 Modbus TCP 驱动的点位读取测试。

  ![点位采集测试](https://assets.emqx.com/images/ad434601402d11e76911bb104ab146d7.png)

- **驱动连接测试**：新增驱动连接测试功能，在**管理**->**系统配置**页面，输入设备的 IP，可快速确认 NeuronEX 运行环境能否访问到设备的 IP 地址。

  ![驱动连接测试](https://assets.emqx.com/images/1caccd9b7dd20fb40df9b8a631ac125a.png)

- **系统 CPU 及内存负载显示**：在**管理**->**系统信息**页面，增加了对系统 CPU 及内存的使用显示。

## 结语

NeuronEX 3.3.0 通过新增驱动支持、提升数据分析和管理功能、优化用户体验和修复已知问题，进一步强化了 NeuronEX 的功能和稳定性。我们相信，这些改进将帮助用户更加高效地进行数据采集和分析，推动工业智能化转型。

感谢您一直以来对 NeuronEX 的支持与信任，我们期待收到您的反馈和建议，并不断改进产品。有关详细的新功能和改进，请查阅完整版 [NeuronEX 3.3.0 Release Notes](https://docs.emqx.com/zh/neuronex/latest/release_history/release_history.html)。

<section class="promotion">
    <div>
        免费试用 NeuronEX 3.3.0 版本，体验更多新功能
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuronex" class="button is-gradient px-5">立即下载 →</a>
</section>
