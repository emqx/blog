## FINS 协议介绍

Omron FINS（ Factory Interface Network Service ）是 OMRON 为工业自动化控制开发的网络通信协议。它可以通过 FINS 命令实现以太网、控制网络和 RS232C / 485 串行通信之间的无缝通信。FINS 协议在 TCP / IP 模型的应用层上工作，这确保了其良好的可扩展性、实用性和实时性，从而通过 Omron FINS 以太网驱动器将客户端应用程序（包括 HMI、SCADA、Historian、MES、ERP 和无数自定义应用程序）与控制器连接起来。

FINS 协议有两个变种：FINS / UDP 协议使用 UDP 数据包进行通信，FINS / TCP 协议使用 TCP 连接。

### FINS 会话过程

FINS 会话过程基于 TCP / IP 协议。下图描述了 FINS 会话开始时几个数据帧的作用。FINS 协议的会话有一个请求帧，发起方的节点参数附加在请求帧上。服务器端（如 PLCS ）将确认并向请求者返回其节点参数。只有基于 TCP 的 FINS 需要会话进程。

![FINS Session Process](https://assets.emqx.com/images/0d8af5289a27e88ab5a6f415cb8c3b34.png)

### FINS 数据帧结构

FINS 数据帧结构包含三个部分，分别是 FINS 头部、FINS 命令代码段以及 FINS 命令参数段。

![FINS Frame Structure](https://assets.emqx.com/images/c7c31b73393dedb48c4cc1be9e0e1464.png)

命令帧和响应帧都由用于存储传输控制信息的 FINS 头部、用于存储命令的 FINS 命令字段和用于存储命令参数或传输/响应数据的 FINS 参数/数据字段组成。

![FINS header](https://assets.emqx.com/images/58272c4a564c4b6a36879a61c1270837.png)

命令的响应代码（ MRES 和 SRES 各一个字节）被添加到响应帧 FINS 参数/数据字段的开头。

![FINS Response Frame Config](https://assets.emqx.com/images/4ad7fb747e362f0bc2cebf6fcdda12e2.png)

FINS/UDP 只包含两部分: FINS 命令代码段和 FINS 命令参数段。

## FINS 可读写 IO 存储区介绍

下表给出了读取或写入可编程控制器数据时要使用的地址。

- 在对可编程控制器编程时，数据区地址列（ Data area address ）给出了正常的地址范围。

- 通讯使用地址列（ Address used in communications ）就是在 CV 模式命令和回复中使用的地址（ CV 模式命令就是 FINS 命令的别名）。这些地址与存储器区域代码结合起来，指定可编程控制器存储器的位置。它们与数据的实际内存地址不同。

- 字节数列（ No. of bytes ）指定该区域读或写数据的字节数。相同区域的字节数因内存区域代码而异。

不同的 PLC CPU 型号有不同的存储器区域。下面以 CV500 或 CVM1-CPU01-E 为例进行说明。

![FINS Read/Write IO Memory Area](https://assets.emqx.com/images/fb21a9091c3f037fb1b3d5d18e65c80e.png)

## FINS 命令列表

在下表中命令代码字段列（Command Code），每一个小格代表一个字节( 两个 16 进制数据)。表格列出了 CV 系列可编程控制器支持的 FINS 命令和在不同的可编程控制器模式下，哪些命令是可用的。

![Command List](https://assets.emqx.com/images/28160d8d452c41d9c73bc7b1a4c411de.png)

> **注**：当可编程控制器处于 RUN 模式时，不能将数据从文件传输到程序区域，但可以从程序区域传输到文件。

## 为什么需要桥接 FINS 到 MQTT？

随着工业 4.0 浪潮的到来，工业领域对数据智能、互联互通和云边缘协作的需求不断增长。在这种背景下，FINS 协议可能会面临一些问题。

首先，作为一种内网应用协议，FINS 的设计并没有考虑到安全性，其通信方法很简单，容易受到黑客攻击和数据篡改，从而对生产环境构成威胁。此外，FINS 仅能在复杂的应用架构中进行一对一的通信，不能有效支持分布式和云原生应用的开发。

与 FINS 相比，[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 具有显著的优势。MQTT 是一种轻量级的发布-订阅消息传输协议，通常用于物联网应用程序中的远程监控和通信。它提供了一种简单灵活的方式在设备之间传输消息，同时有效处理大量并发连接。它目前用于物联网、移动互联网、智能硬件、网联汽车、智慧城市、远程医疗、电力、石油和能源等各个领域。

在物联网领域，MQTT 显然更适合分布式系统中的消息传输。因此，我们可以将 FINS 与 MQTT 结合，互为补充。

## FINS 桥接到 MQTT 的架构

本文我们使用 EMQ 提供的 [Neuron](https://www.emqx.com/zh/products/neuron) 和 [EMQX](https://www.emqx.com/zh/products/emqx) 来实现 FINS 到 MQTT 的桥接。Neuron 可以将 FINS 协议转换为 MQTT，而 EMQX 充当 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，处理大量连接和数据。

Neuron 是运行在各类物联网边缘网关硬件上的工业协议网关软件，旨在解决工业 4.0 背景下设备数据统一接入难的问题。通过将来自繁杂多样工业设备的不同协议类型数据转换为统一标准的物联网 MQTT 消息，实现设备与[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)系统之间、设备彼此之间的互联互通，进行远程的直接控制和信息获取，为智能生产制造提供数据支撑。

> 了解更多 Neuron: [Neuron: 工业协议网关软件](https://www.emqx.com/zh/products/neuron)

EMQX 是一个大规模且弹性的云原生分布式物联网 MQTT 消息服务器。作为全球最具可扩展性的 MQTT 消息服务器，EMQX 提供了高效可靠的物联网设备大规模连接，能够高性能实时处理消息和事件流数据，帮助用户快速构建关键的物联网平台和应用。

> 了解更多 EMQX: [EMQX Enterprise: 企业级 MQTT 物联网接入平台](https://www.emqx.com/zh/products/emqx)

下图展示了 Neuron 如何从边缘收集数据，将其转换为 MQTT 并上传到 EMQX。

![diagram](https://assets.emqx.com/images/820e4a0fa4ee05c049c40b83ff97a477.png)

## 使用 Neuron 桥接 FINS 到 MQTT

本节将介绍如何使用 Neuron 从 FINS TCP 设备收集数据，将收集到的数据上传到 EMQX，并使用 MQTTX 查看。

### EMQX 快速开始

EMQX 提供了多种安装方法，用户可以在文档中查看详细的安装方法。此示例使用容器部署来快速体验 EMQX。

运行以下命令获取 Docker 镜像：

```
docker pull emqx/emqx-enterprise:5.1.0
```

运行以下命令启动 Docker 容器：

```
docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.1.0
```

通过网页浏览器访问 `http://localhost:18083` （将 “localhost” 替换为实际 IP 地址），进入 EMQX 控制面板。这样，您可以管理设备连接并监控相关指标。请保持 Docker 容器在运行状态以完成本教程。如有兴趣，请参阅[文档](https://www.emqx.io/docs/en/v5.0/)，了解控制面板中的更多功能。

初始用户名：admin，初始密码：public

### Neuron 快速开始

Neuron 提供了多种安装方法，用户可以在[文档](https://neugates.io/docs/en/latest/installation/installation.html)中查看详细的安装方法。这个示例使用了容器化部署。

获取 Docker 镜像：

```
$ docker pull emqx/neuron:latest
```

启动 Docker 容器：

```
$ docker run -d --name neuron -p 7000:7000 --privileged=true --restart=always emqx/neuron:latest
```

打开网页浏览器，输入网关地址和端口号，运行 Neuron。这将带您进入管理控制台页面，默认端口号为7000。您可以通过浏览器访问它 `http://localhost:7000/`（用您的实际 IP 地址替换 “localhost”）。

#### 第一步：登录

使用初始用户名和密码登录：

- 用户名: `admin`

- 密码: `0000`

#### 第二步：添加南向驱动节点

点击**配置**菜单中的南向设备菜单项进入**南向设备**配置页面。点击**添加设备**来添加一个新的南向驱动设备节点。

- 名称: 填入设备节点名称, 例如 “fins-tcp-1”；

- 插件: 从下拉框中选择 **FINS TCP** 驱动插件。

#### 第三步：设置南向设备参数

添加南向设备后，会自动进入设备配置界面，在此界面可以填写参数并提交。演示设备使用 Omron CP2E。

- 设备类型：选择 CP；

- PLC IP 地址：输入 PLC IP 地址；

- PLC 端口：默认9600。

#### 第四步：新建点位分组

点击设备节点卡上的任意空白处，进入组列表管理界面，点击创建，弹出创建组对话框。填写参数并提交：

- 分组名: 填入分组名, 例如 "group-1"；

- 间隔: 1000。

#### 第五步：分组添加数据点位

点击分组卡的任意空白处，进入点列表管理界面，点击创建，进入添加数据点的页面。

![图片png](https://assets.emqx.com/images/ebcb7ae859c18b0830bda06a7ef30e67.png)

填写数据点的参数并提交：

- 名称: 填写点位名称, 例如 ”tag-1”；

- 属性: 从下拉菜单选择节点属性，例如 Read， Write；

- 类型: 从下拉菜单选择节点类型，例如 INT16；

- 地址: 输入节点对应的本驱动的地址，例如，CIO1。 CIO 代表了 PLC 中 的 CIO 区域，1 代表了寄存器的地址。

- 描述，系乘数，精度： 不填。

#### 第六步：使用数据监控查看采集的值数据

使用左侧导航菜单，点击**监控 → 数据监控**。查看由创建的数据点读取的值，如下图所示。

数据监测分组显示值：

![图片png](https://assets.emqx.com/images/1a2c6e0ab3967449ca72411661e04735.png)

- 南向设备：从下拉菜单中选择要查看的南向设备，例如，已创建的 fins-tcp-1；

- 组名称：从下拉菜单中选择要查看的已创建的南向设备下的组，例如，已创建的 group-1；

- 选择后，页面将显示所选组中读取到的所有点位值。

#### 第七步：添加北向应用

通过创建一个北向应用程序，Neuron 建立了与北向应用程序的连接，并将收集的设备数据上传到 EMQX。

在配置菜单，选择北向应用，点击添加应用，如下图所示。

![图片png](https://assets.emqx.com/images/f3dc9e4ef83580bd70ea86211a901502.png)

添加 MQTT broker 连接：

- 名称: 填写应用名，例如 MQTT;

- 插件: 从下拉框选择 MQTT 插件。

#### 第八步：配置北向应用参数

添加北向应用后，它会自动进入应用配置界面，填写参数并提交

设备 MQTT 连接：

- 客户端 ID：注意，此ID应相互独立（重复的 ID 会导致客户端断开）。例如，设置为 MQTT-12123；

- QoS 等级：默认设置0;

- 上报数据格式：默认设置 Values-format;

- 写请求主题：默认设置 /neuron/MQTT/write/req;

- 写响应主题： 默认设置 /neuron/MQTT/write/resp;

- 离线缓存：默认设置 off;

- 服务器地址： 填写已创建 emqx broker 的地址，该地址通常是本地主机，即您的实际 IP 地址；

- 服务器端口： 默认设置 1883；

- 用户名， 密码： 不填；

- SSL: 默认设置 off。

#### 第9步：订阅南向点位分组

点击新创建的 MQTT 应用节点卡片上的任意空白处，进入订阅组界面，点击“添加订阅”

订阅南向设备点位分组:

- 南向设备：从下拉列表中选择已创建的南向设备，例如，fins-tcp-1；

- 组：从下拉列表中选择要订阅的组，例如，group-1；

- 主题：MQTT 主题，默认设置为 /neuron/MQTT/fins-tcp-1/group-1，接下来，订阅该主题并在 MQTTX 中接收消息。

#### 第10步：使用 MQTTX 查看数据

订阅后，您可以使用 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)连接到 EMQX 并查看上报的数据。我们使用 MQTTX，一个功能强大的跨平台 MQTT 客户端工具，可以从[官方网站](https://mqttx.app/zh/downloads)下载。

启动 MQTTX 后，单击主页上的 **+新建连接**，填写配置参数，然后单击右上角的连接。

- 名称：名称有助于查看。例如，将其命名为 fins-tcp；

- 客户端 ID：可以使用默认值；确保 ID 是独立的；

- 服务器地址: 选择 **mqtt://** 和填写 `localhost` （将“localhost”替换为实际 IP 地址）；

- 端口: 1883。

可以填写可选参数，完成后单击右上角的**连接**按钮。成功连接后，订阅该主题。

- 单击**添加订阅**，主题应与步骤9中的主题相同。例如，填写 /neuron/MQTT/fins-tcp-1/group-1；

成功订阅后，您可以看到 MQTTX 继续接收由 Neuron 收集和上报的数据。如下图所示。

![MQTTX](https://assets.emqx.com/images/a84ca7156be60a96e43c4762b7d4b406.png)

## 结语

随着工业4.0浪潮中云端协作的趋势日益明显，FINS 桥接正在成为越来越流行的通用物联网协议选择。通过使用本文中提供的方法将 FINS 协议数据桥接到 MQTT，用户可以更加安全、方便地按需实施连接性更强的 IIoT 平台，从而显著提高生产效率、节约成本和提升产品质量。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
