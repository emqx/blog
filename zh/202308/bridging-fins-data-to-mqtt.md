本文我们将使用 EMQ 提供的 Neuron 和 EMQX 来实现 FINS 到 MQTT 的桥接。Neuron 可以将 FINS 协议转换为 MQTT，EMQX 则充当 MQTT Broker，处理大量连接和数据。

## FINS 桥接到 MQTT 的架构

Neuron 是运行在各类物联网边缘网关硬件上的工业协议网关软件，旨在解决工业 4.0 背景下设备数据统一接入难的问题。通过将来自繁杂多样工业设备的不同协议类型数据转换为统一标准的物联网 MQTT 消息，实现设备与[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)系统之间、设备彼此之间的互联互通，进行远程的直接控制和信息获取，为智能生产制造提供数据支撑。

> 了解更多 Neuron: [Neuron: 工业协议网关软件](https://www.emqx.com/zh/products/neuronex)

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

通过网页浏览器访问 `http://localhost:18083` （将 “localhost” 替换为实际 IP 地址），进入 EMQX 控制面板。这样，您可以管理设备连接并监控相关指标。请保持 Docker 容器在运行状态以完成本教程。如有兴趣，请参阅[文档](https://docs.emqx.com/en/emqx/v5.0/)，了解控制面板中的更多功能。

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
