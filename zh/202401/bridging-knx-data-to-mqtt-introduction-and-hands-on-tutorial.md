本文将介绍如何使用 Neuron 从 [KNX](https://www.emqx.com/zh/blog/knx-protocol) 设备中采集数据，将数据上传到 EMQX，并使用 MQTTX 进行查看。

我们将使用运行 Linux 系统的机器来安装 EMQX、MQTTX 和 Neuron。由于 ETS 和 KNX Virtual 仅支持 Windows，我们将运行一个 Windows 虚拟机来模拟 KNX 安装。

KNX 桥接到 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的架构如下图所示：

![KNX 桥接到 MQTT 的架构图](https://assets.emqx.com/images/812e45b29a893cc73595736a7606ea6f.png)

## EMQX 快速使用

EMQX 提供多种安装方式，用户可在[安装指南](https://docs.emqx.com/zh/emqx/v5.0/deploy/install.html)在中查看详细的安装方式。本实例采用容器化部署的方式，以便于最快开始体验 EMQX。

运行以下命令获取 Docker 镜像：

```
docker pull emqx/emqx:5.1.0
```

运行以下命令启动 Docker 容器

```
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.0
```

通过浏览器访问 `http://localhost:1883`（localhost 可替换为您的实际 IP 地址）以访问 EMQX Dashboard 管理控制台，进行设备连接与相关指标监控管理。本教程保持 docker 启动即可，如有兴趣可以参考[文档](https://docs.emqx.com/zh/emqx/v5.0/)在控制台体验更多功能。

初始用户名： `admin` ，初始密码：`public`

## 使用 ETC 配置 KNX Virtual

To keep things simple, we will simulate a KLiX (D0), a dimming actuator (D0), a blinds/shutter actuator (D2) and a switch actuator (D7) in KNX Virtual. The association between addresses and group objects is shown in the following image.

我们需要[下载并安装 KNX Virtual](https://www.knx.org/knx-en/for-professionals/get-started/knx-virtual/index.php) 。关于如何使用 ETS 和 KNX Virtual 模拟 KNX 安装，可以参考[官方博客](https://www.ets6.org/ets6-and-knx-virtual/)或者[视频教程 KNX Virtual Basics](https://www.youtube.com/watch?v=01MO_zmtGv4)。

为了简化操作，我们将在 KNX Virtual 中模拟一个 KLiX（D0），一个调光执行器（D0），一个百叶窗/卷帘执行器（D2）和一个开关执行器（D7）。地址和组对象之间的关联关系如下图所示。

![使用 ETC 配置 KNX Virtual](https://assets.emqx.com/images/a183a59542de3434a3aa01201e6d6cc6.png)

## Neuron 快速开始

Neuron 提供多种安装方式，查阅[安装指南](https://neugates.io/docs/zh/latest/configuration/quick-start/installation.html)以获取详细的 Neuron 安装说明。

打开 Web 浏览器，输入运行 Neuron 的网关地址和端口号，即可进入到管理控制台页面，默认端口号为 7000。通过浏览器访问 `http://localhost:7000` （localhost 可替换为您的实际 IP 地址）。

#### 第一步. 登录

页面打开后，进入到登录界面，用户可使用初始用户名与密码登录（初始用户名：admin，初始密码：0000）。

#### 第二步. 添加南向节点

在 Neuron 仪表板中，点击**配置 -> 南向设备管理 -> 添加设备**来添加一个 *knx* 节点。

![添加设备](https://assets.emqx.com/images/5f712ce79b53bd16a5170ee75eade8fc.png)

#### 第三步. 配置 *knx* 节点

配置新创建的 *knx* 节点, 如下图所示。

![配置 knx 节点](https://assets.emqx.com/images/91d32239dafc70f2037073baa63997fa.png)

#### 第四步. 创建组

点击 *knx* 节点进入**组列表**页面，点击**创建**，弹出**创建组**对话框。填写参数并提交：

- 组名称：grp
- 间隔： 1000

![创建组](https://assets.emqx.com/images/36bc89c0e101331a297f7d1021abd2a2.png)

#### 第五步. 添加数据点位

对应 KNX Virtual 中的配置，为调光执行器、百叶窗执行器和开关执行器添加四个点位。

![添加数据点位](https://assets.emqx.com/images/261910857cebcc68cd6528c627bf4f10.png)

#### 第六步. 数据监控

点击**监控** -> **数据监控**，查看已创建点位读取到的数值，如下图所示。

![数据监控 1](https://assets.emqx.com/images/c6b42ce56a42fd441e800fce7bd83a46.png)

![数据监控 2](https://assets.emqx.com/images/e342a14913dbbfa00854a6203f531e21.png)

#### 第七步. 添加北向应用

在 Neuron 仪表板中，点击**配置 -> 北向应用 -> 添加应用**来添加一个 *mqtt* 节点。

![添加北向应用](https://assets.emqx.com/images/1db2eb2798bdeddd1a9afbb9bbd6e345.png)

#### 第八步. 配置 *mqtt* 节点

配置 *mqtt* 节点连接到之前启动的 EMQX 服务器。

![配置 mqtt 节点](https://assets.emqx.com/images/96352995da758ab25b0e1c649097ee94.png)

#### 第九步. 添加订阅

点击刚创建的 *mqtt* 应用节点进入**组列表**页面，点击**添加订阅** 。订阅成功后，Neuron 会将数据发布到 MQTT 主题 `/neuron/mqtt/knx/grp` 中。

![添加订阅](https://assets.emqx.com/images/c1ec49d07077c025e2d24042ed4ad464.png)

## 使用 MQTTX 查看数据

现在，您可以使用 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)连接到 EMQX 并查看报告的数据。本文我们使用 MQTTX，这是一个功能强大的跨平台 MQTT 客户端工具，可以从其[官方网站](https://www.emqx.com/en/products/mqttx)下载。

启动 MQTTX，并添加一个到之前设置的 EMQX 服务器的新连接，然后订阅主题 `/neuron/mqtt/knx/grp` 。成功订阅后，您将看到 MQTTX 持续收到由 Neuron 采集的数据，如下图所示。

![使用 MQTTX 查看数据](https://assets.emqx.com/images/5d270c03655b13dafadeba9633baa4fc.png)

## 结语

在这篇博客中，我们介绍了 KNX 协议，并展示了使用 Neuron 将 KNX 数据桥接到 MQTT 的整体过程。

KNX 为家庭和建筑自动化提供了一个强大而灵活的平台。Neuron 作为工业物联网的强大连接性设备，方便地从 KNX 设备收集数据，并将获取的数据无缝传输到云端，以便在需要时进行便捷的远程控制和监控。

同时 Neuron 还支持 Modbus, OPC UA, SIEMENS 等多种工业协议，相关桥接教程请参考：

- [工业物联网数据桥接教程：Modbus 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-modbus-data-to-mqtt-for-iiot)
- [工业物联网数据桥接教程：OPC UA 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-opc-ua-data-to-mqtt-for-iiot)
- [工业物联网数据桥接教程：TwinCAT 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-twincat-data-to-mqtt)
- [工业物联网数据桥接教程：FINS 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-fins-data-to-mqtt)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
