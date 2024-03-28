工业边缘网关软件 NeuronEX 3.2.0 版本现已正式发布！本次发布带来了一系列的增强功能和新特性，旨在为用户提供更多数据采集、分析计算以及管理的能力。

最新版本下载：[https://www.emqx.com/zh/try?product=neuronex](https://www.emqx.com/zh/try?product=neuronex) 

## 数据采集驱动更新

### 新增南向驱动

- **MTConnect:** 新增 MTConnect 南向驱动，支持通过 HTTP 协议访问安装有 MTConnect Agent 的设备。[MTConnect | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/mtconnect/mtconnect.html) 
- **Siemens MPI:** 新增 Siemens MPI 南向驱动，支持通过 MPI 通讯协议与 Siemens 设备进行数据交换。[Siemens MPI | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/siemens-mpi/mpi.html) 
- **海德汉 CNC:** 新增海德汉 CNC 南向驱动，可实时采集海德汉各系列机床的运行数据。[HEIDENHAIN CNC | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/heidenhain-cnc/heidenhain-cnc.html) 

### 驱动功能增强

- **驱动功能持续增强：**扩展了 OPC UA、Siemens S7、 Inovance Modbus TCP 以及 Focas 等驱动的数据类型支持，持续优化驱动读写性能。
- **南向驱动节点导入/导出:** 新增南向驱动节点导入导出功能，支持一次性导入导出多个南向驱动配置以及点位数据，简化配置管理流程。
- **南向驱动复制功能:** 通过南向驱动复制功能，可快速创建同类型的驱动节点。
- **简化南向驱动创建流程:** 针对南向驱动创建流程进行了优化，使体验更加顺畅。
- **优化驱动数据统计页面：**提供更详细的驱动状态信息，方便驱动运维管理。

![驱动数据统计页面](https://assets.emqx.com/images/7fe6e88352963b34af5b7376eaeeab43.png)

## 数据处理更新

- **外部算法服务集成:** NeuronEX 现在支持调用外部算法服务，将各类数据源数据发送到外部服务，返回计算结果并输出到 Sink 中。（该功能详细使用请参考文档：[算法集成 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/streaming-processing/extension.html#外部算法函数) ）

  ![创建外部服务](https://assets.emqx.com/images/96f40099b56f2f9cf06c918eff362db0.png)

  <center>创建外部服务</center>

  <br>

  ![规则中使用外部服务](https://assets.emqx.com/images/1bc463cb8ae53e3ed4239dc49f763a74.png)

  <center>规则中使用外部服务</center>

- **规则调试增强：**规则调试功能，可实时查看到经过 SQL 处理后的规则输出结果，可快速对 SQL 语法、内置函数以及数据模板等内容进行测试。在新版本中我们对规则调试功能做了加强，调整了界面样式，更加易用。

- **Kafka Sink:** 新增 Kafka Sink ，支持与 Kafka 直接集成，实现高效的数据流处理。

  ![Kafka Sink](https://assets.emqx.com/images/e77bd835ec8365e96140a783a2afb6cd.png)

## 用户界面优化

同时，我们对 NeuronEX 3.2.0 进行了用户界面的重新设计与优化，旨在进一步提升用户使用体验。通过调整界面布局、优化色彩搭配以及改进交互元素，我们使界面变得更加直观、易于操作。此外，我们还对页面的排版和组件进行了调整，以确保信息的呈现更加清晰。这一系列的界面改进将为用户带来更流畅、直观的操作体验，使其能够更轻松、更高效地完成各项任务，并更好地掌控对工业数据的采集、处理分析和管理过程。

## 其他改进

- **单点登录（SSO）支持:** 增加了单点登录（SSO）支持，简化用户身份验证和访问管理。[系统配置 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/admin/sys-configuration.html#单点登录配置) 
- **代理连接到 ECP 平台:** NeuronEX 现支持代理连接到 ECP 平台，支持在复杂网络情况下，实现与 ECP 的无缝集成。

我们相信这些增强功能和新特性将进一步提升 NeuronEX 的用户体验，助力轻松管理和分析工业数据。了解并体验 NeuronEX 3.2.0，请访问网站并下载最新版本 ([免费下载 NeuronEX](https://www.emqx.com/zh/try?product=neuronex))。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
