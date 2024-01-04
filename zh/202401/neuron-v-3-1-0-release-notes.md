EMQ 旗下的工业边缘网关软件 NeuronEX 3.1.0 版本现已正式发布！

新版本带来了一系列的新功能和优化，提升边缘端数据接入及数据分析的能力。本次更新的重点是扩展接入能力，提高易用性，为数据管理和分析提供强大的工具。

## 1. 操作系统与安装包扩展支持

**操作系统扩展**

NeuronEX 已对更多操作系统的支持。新版本增加了 CentOS 7、Ubuntu 18.04 和 Debian-10 的支持，用户可将 NeuronEX 集成到以上操作系统，确保灵活性和部署的便利性。

**安装包扩展支持**

NeuronEX 现在扩展了对 RPM（[使用 rpm 包安装 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/installation/centos.html) ） 和 DEB（[使用 deb 包安装 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/installation/ubuntu.html) ) 安装方法的支持。

**新增对 ARM v7 架构的支持**

NeuronEX 能在更广泛的硬件范围上部署，提供更大的灵活性和性能。

## 2. 南向驱动更新

### Inovance Modbus TCP

NeuronEX 3.1.0 新增南向驱动 Inovance Modbus TCP。 该驱动是一种基于以太网的 Modbus 协议版本，使用 TCP/IP 协议通信。

Inovance Modbus TCP 插件对汇川 PLC 的数据地址做了适配，更易于采集接入汇川系列 PLC 的数据。

Inovance Modbus TCP 驱动使用说明文档：[Inovance Modbus TCP | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-hc-tcp/modbus-hc-tcp.html) 

### HostLink C-mode

NeuronEX 3.1.0 新增南向驱动 Hostlink C-mode。 该协议是欧姆龙公司定义的一种用于其他设备与欧姆龙公司 PLC 的通信协议。 Hostlink 通讯协议有两种模式：C-mode 和 FINS。 C-mode 采用 ASCII 码，由上位机主动发出指令给 CPU；FINS 采用二进制码，可用在多种网络设备，可被 CPU、IO模块、上位机主动发出。

HostLink Cmode 插件用于通过串口网络与欧姆龙 PLC 进行通信。

HostLink Cmode 驱动使用说明文档：[HOSTLINK CMODE | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/hostlink/hostlink-cmode.html) 

### 新增驱动及驱动替换

NeuronEX 3.1.0 支持通过 Dashboard 上传插件文件，方便导入新插件或对原插件进行升级替换。

## 3. 数据接入及数据转发能力

在工业边缘场景，除了工业设备数据采集，还涉及到各类系统的数据采集接入。新版本增强了数据接入及数据转发能力。

数据处理模块新增了以下数据源：

- **HTTP Pull ：** 从外部 HTTP 服务器中拉取数据。
- **HTTP Push ：**作为 HTTP Server，接受外部的推送数据。
- **SQL ：**从 MySQL、SQL Server、PostgreSQL、SQLite、Oracle 等数据库中查询数据。
- **File ：**从 txt、json、csv 等文件中获取数据。
- **Video：**从视频流中获取数据。
- **Simulator：**内置模拟数据源，生成模拟数据供测试。

NeuronEX 数据处理模块新增了以下动作 Sink 类型：

- **REST：**将数据输出到外部 HTTP 服务器。
- **SQL：**将数据写入到 MySQL、SQL Server、PostgreSQL、SQLite、Oracle 等数据库。
- **InfluxDB V1：** 将数据写入到 InfluxDB v1.x。
- **InfluxDB V2：** 将数据写入到 InfluxDB v2.x。
- **文件：** 将数据写入文件。

### Simulator Source

模拟器源提供了一种用于测试和演示目的的数据生成方式，可用来模拟来自设备或传感器的数据流。使用这种数据源，用户可以快速进行规则场景的验证而无需连接真实的数据源。

### InfluxDB V1/V2 Sink 

InfluxDB 是一个开源的时序数据库，在物联网场景中得到了广泛的应用。新版本支持大量的数据点和批量写入功能，使得这两个 Sink 可以应用于更高数据吞吐量的场景中。

- 支持批量写入设置；
- 支持多个 tag，支持基于数据模板的动态 tag；
- 支持配置动态时间戳以及时间精度；
- 其中 InfluxDB V2 支持行协议模式，支持行协议模式下使用数据模板格式化数据。

进一步了解数据接入及数据转发的功能，可查阅 [NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/)。

## 4. 规则调试

在新版本中，我们引入了规则调试功能。创建规则时，只要开启规则调试功能，即可实时查看到经过 SQL 处理后的规则输出结果，可快速对 SQL 语法、内置函数以及数据模板等内容进行测试。

同时，新版本还支持模拟数据源规则调试，将 SQL 编辑器内的原始数据源替换为自定义的模拟数据源，提供了更加灵活的数据源模拟方式。

![SQL 编辑器](https://assets.emqx.com/images/a0c62cd22e2585bcd38ea6b819306706.png)

## 5. 日志功能增强

NeuronEX 3.1.0 增强了日志功能：

- 支持下载单个数采南向驱动的日志
- 支持下载数据处理模块日志
- 支持配置日志级别
- 支持在 Dashboard 上查看实时日志信息。

## 6. 其他功能优化

除了以上内容更新，NeuronEX 3.1.0 还做了如下方面的优化：

- 优化数据采集与数据处理模块之间的配置过程
- 预创建了 DataProcessing 节点和 neuronStream 流，用户只需将南向驱动数据组添加订阅到 DataProcessing 节点，即可创建规则对数据进行分析处理。
- 优化了 NeuronEX 存储目录
- 优化了 驱动xls模板，增加了组采集间隔
- 优化了数据处理模块规则选项
- 优化了数据处理模块动作高级配置项
- 优化了 NeuronEX 的指标数据集告警信息，并与 ECP无缝集成。


<section class="promotion">
    <div>
        免费试用 NeuronEX
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuronex" class="button is-gradient px-5">开始试用 →</a>
</section>
