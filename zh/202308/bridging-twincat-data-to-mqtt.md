本文将介绍如何将 TwinCAT 数据桥接到 MQTT。我们将使用 Neuron 采集 Twincat PLC 的数据，将采集到的数据上传到 EMQX MQTT Broker，并使用 MQTTX 查看。

## TwinCAT 桥接到 MQTT 的架构

![The Architecture of TwinCAT to MQTT Bridging](https://assets.emqx.com/images/f7b81bd0ef7ed7c4661b4a388f681b37.png)

### 使用 Neuron 转换 TwinCAT 到 MQTT

[Neuron](https://github.com/emqx/neuron) 是一款强大的工业协议网关软件，可以为实时工业数据采集提供必要的物联网连接能力。Neuron 十分轻量，可以运行在各种资源受限的物联网边缘硬件设备中，并通过标准协议或其自有的专用协议与各种各样的工业设备进行通信，将其连接到工业物联网平台。

从发布之初，Neuron 就支持 MQTT 作为其通信协议之一。Neuron [MQTT 插件](https://docs.emqx.com/en/neuron/latest/configuration/north-apps/mqtt/overview.html)允许用户快速构建使用 MQTT 协议的物联网应用程序，实现设备与云之间的通信。

Neuron 2.2.0 版本中发布了 [Beckhoff ADS 插件](https://docs.emqx.com/en/neuron/latest/configuration/south-devices/ads/ads.html)。Neuron Beckhoff ADS 插件实现了基于 TCP 的 ADS 协议。该插件支持与 [Beckhoff TwinCAT](https://www.beckhoff.com/en-us/products/automation/twincat/#stage-special-item-s320986-2_t0) PLC 进行通信，进一步丰富了 Neuron 的连接能力，增强了用户体验，满足更多用户需求。

通过 Beckhoff ADS 插件，用户可以轻松地从 TwinCAT PLC 采集数据。与 MQTT 插件一起使用，用户可以将采集的数据推送到[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)平台，如 [EMQX](https://www.emqx.com/zh/products/emqx)，或将消息发布回 TwinCAT PLC，触发设备操作，例如打开或关闭灯光、电机和其他设备。

### 使用 EMQX 处理 MQTT 消息

[EMQX](https://www.emqx.com/zh/products/emqx) 是一款大规模可弹性伸缩的云原生分布式物联网 [MQTT 消息服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。作为全球最具扩展性的 MQTT 消息服务器，EMQX 提供了高效可靠海量物联网设备连接，能够高性能实时移动与处理消息和事件流数据，帮助用户快速构建关键业务的物联网平台与应用。

EMQX 在桥接架构中的作为 MQTT broker，而 Neuron 则收集来自 TwinCAT PLC 的数据并通过 MQTT 消息将数据传输到代理。在从 Neuron 接收 MQTT 消息后，EMQX 将转发数据或执行进一步的处理。

EMQX 具有丰富而强大的功能集，例如基于 SQL 的规则引擎，可实时提取、过滤、丰富和转换物联网数据，以及数据集成功能，可将 EMQX 连接到外部数据系统，如数据库。

## 通过 Neuron 将 TwinCAT 桥接到 MQTT

本教程使用了在同一个局域网下的 2 台机器，机器 1 为 Linux 系统，安装了 EMQX、MQTTX 和 Neuron 软件；机器 2 为 Windows 系统，安装了倍福 TwinCAT 3 软件。 

|          | 机器1               | 机器2             |
| :------- | :------------------ | :---------------- |
| 操作系统 | Linux               | Windows           |
| IP 地址  | 192.168.1.152       | 192.168.1.107     |
| amsnetid | 192.168.1.152.1.1   | 192.168.1.107.1.1 |
| 安装软件 | EMQX, MQTTX, Neuron | TwinCAT           |
| 网络     | 连通                | 连通              |

### EMQX 快速使用

EMQX 提供多种安装方式，用户可在[安装指南](https://docs.emqx.com/zh/emqx/v5.0/deploy/install.html)在中查看详细的安装方式。本实例采用容器化部署的方式，以便于最快开始体验 EMQX。

运行以下命令获取 Docker 镜像：

```
docker pull emqx/emqx:5.1.0
```

运行以下命令启动 Docker 容器

```
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

通过浏览器访问 `http://localhost:1883` （localhost 可替换为您的实际 IP 地址）以访问 EMQX Dashboard 管理控制台，进行设备连接与相关指标监控管理。本教程保持 docker 启动即可，如有兴趣可以参考[文档](https://docs.emqx.com/zh/emqx/v5.0/)在控制台体验更多功能。

初始用户名： `admin` ，初始密码：`public`

### TwinCAT 配置

您可以前往 [Beckhoff TwinCAT 网站](https://www.beckhoff.com/en-us/products/automation/twincat)下载和安装 TwinCAT 。

让 Neuron 和倍福 PLC 建立通讯，需要添加路由、查找 AMS Net ID、AMS port、以及变量的 index group 和 index offset 。打开 **TwinCAT Static Routes** 对话框，输入下图红框内容，其中 **AmsNetId**，为 Neuron 所在机器与倍福 PLC 相连的网卡的 IP 地址后加上 ".1.1" 。

![Add Route Dialog](https://assets.emqx.com/images/76fa1bf6823b3922ec91a5e8ad908e71.png)

在本文中我们使用以下 TwinCAT PLC 程序，其定义了足够的变量进行演示。

![TwinCAT PLC program](https://assets.emqx.com/images/5dbe48a09eeab228f8e15a3e73e45b92.png)

在项目路径打开 TPY 文件。TPY 文件中包含了 PLC 程序中所有变量的 index group 和 index offset 信息，后续配置 Neuron 点位地址时会用到。

![Open the TPY file in the TwinCAT project directory](https://assets.emqx.com/images/9084517cef1d7754bc4edd3e3b9c55af.png)

### Neuron 快速开始

Neuron 提供多种安装方式，查阅[安装指南](https://docs.emqx.com/zh/neuron/latest/configuration/quick-start/installation.html)以获取详细的 Neuron 安装说明。

打开 Web 浏览器，输入运行 Neuron 的网关地址和端口号，即可进入到管理控制台页面，默认端口号为 7000。通过浏览器访问 `http://localhost:7000` （localhost 可替换为您的实际 IP 地址）。

#### 第一步. 登录

页面打开后，进入到登录界面，用户可使用初始用户名与密码登录（初始用户名：admin，初始密码：0000）。

#### 第二步. 添加南向节点

在 Neuron 仪表板中，点击**配置 -> 南向设备管理 -> 添加设备**来添加一个 *ads* 节点。

![添加南向节点](https://assets.emqx.com/images/699b6ee8b41ab66033cff0b71a839898.png)

#### 第三步. 配置 *ads* 节点

配置新创建的 *ads* 节点, 如下图所示。

![配置 *ads* 节点](https://assets.emqx.com/images/2abaaaae0927d226cb3af3c7c9fd8c00.png)

#### 第四步. 创建组

点击 *ads* 节点进入**组列表**页面，点击**创建**，弹出**创建组**对话框。填写参数并提交：

- 组名称：grp
- 间隔： 1000

#### 第五步. 添加数据点位

对于 TwinCAT PLC 程序中的变量，我们将在 Neuron ADS 节点上添加一个相应的点位。 变量的点位地址由变量的 index group 和 index offset 组成。

![Tag 列表](https://assets.emqx.com/images/7615b3e6ef6e400829fbca7f5373c465.png)

#### 第六步. 数据监控

点击**监控** -> **数据监控**，查看已创建点位读取到的数值，如下图所示。

![数据监控](https://assets.emqx.com/images/120650cdc39c4c6e246ff15be2bc91f1.png)

#### 第七步. 添加北向应用

在 Neuron 仪表板中，点击**配置 -> 北向应用 -> 添加应用**来添加一个 *mqtt* 节点。

![添加北向应用](https://assets.emqx.com/images/d5e7ce56416a74e3eee5fffe54379f43.png)

#### 第八步. 配置 *mqtt* 节点

配置 *mqtt* 节点连接到之前启动的 EMQX 服务器。

![配置 *mqtt* 节点](https://assets.emqx.com/images/27cb36011bc92cccd94674ea501cf4de.png)

#### 第九步. 添加订阅

点击刚创建的 *mqtt* 应用节点进入**组列表**页面，点击**添加订阅** 。订阅成功后，Neuron 会将数据发布到 MQTT 主题 `/neuron/mqtt/ads/grp` 中。

![添加订阅](https://assets.emqx.com/images/0f4172aeb1a616c4d8d6e91548c427fa.png)

### 使用 MQTTX 查看数据

现在，您可以使用 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)连接到 EMQX 并查看报告的数据。本文我们使用 [MQTTX](https://mqttx.app/zh)，这是一个功能强大的跨平台 MQTT 客户端工具，可以从其[官方网站](https://mqttx.app/zh)下载。

启动 MQTTX，并添加一个到之前设置的 EMQX 服务器的新连接，然后订阅主题 `/neuron/mqtt/ads/grp` 。成功订阅后，您将看到 MQTTX 持续收到由 Neuron 采集的数据，如下图所示。

![MQTTX](https://assets.emqx.com/images/232567212ae2a3a9e34a4ef0dfffa98a.png)

## 结语

在本文中，我们介绍了如何使用 Neuron 将 TwinCAT 数据桥接到 MQTT 的整体过程。

作为一款工业自动化平台，TwinCAT 在包括汽车、航空航天、食品和饮料等各种行业中得到了广泛应用。具有强大工业物联网连接能力的 Neuron，可从 TwinCAT PLC 收集数据，并将获取的数据无缝传输到云端，以便在必要时进行方便的远程控制和监控。

除此之外，Neuron 还支持 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication)、OPC UA、SIEMENS 等其他工业。有关更多桥接教程，请阅读我们的文章：[工业物联网数据桥接教程：Modbus 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-modbus-data-to-mqtt-for-iiot#the-architecture-of-modbus-to-mqtt-bridging)。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
